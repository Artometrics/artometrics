"""Merge Jikan + AniList payloads into flat rows aligned with the legacy article schema."""

from __future__ import annotations

import json
import re
from typing import Any

import pandas as pd

MAL_SOURCE_MAP = {
    "ORIGINAL": "Original",
    "MANGA": "Manga",
    "LIGHT_NOVEL": "Light novel",
    "VISUAL_NOVEL": "Visual novel",
    "GAME": "Game",
    "NOVEL": "Novel",
    "DOUJINSHI": "Doujinshi",
    "ANIME": "Anime",
    "WEB_NOVEL": "Web novel",
    "LIVE_ACTION": "Live action",
    "BOOK": "Book",
    "CARD_GAME": "Card game",
    "MUSIC": "Music",
    "PICTURE_BOOK": "Picture book",
    "RADIO": "Radio",
    "OTHER": "Other",
}

FORMAT_MAP = {
    "TV": "TV",
    "TV_SHORT": "TV Short",
    "MOVIE": "Movie",
    "SPECIAL": "Special",
    "OVA": "OVA",
    "ONA": "ONA",
    "MUSIC": "Music",
}


def _list_names(items: list[dict[str, Any]] | None, key: str = "name") -> list[str]:
    if not items:
        return []
    return [str(x.get(key)) for x in items if x.get(key)]


def _jikan_themes_demographics(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    themes = _list_names(data.get("themes"))
    demographics = _list_names(data.get("demographics"))
    return themes, demographics


def _anilist_tag_buckets(tags: list[dict[str, Any]] | None) -> tuple[list[str], list[str]]:
    themes: list[str] = []
    demographics: list[str] = []
    if not tags:
        return themes, demographics
    for tag in tags:
        cat = (tag.get("category") or "").lower()
        name = tag.get("name")
        if not name:
            continue
        if "demographic" in cat or cat.startswith("demographic"):
            demographics.append(name)
        elif cat.startswith("theme") or cat.startswith("setting"):
            themes.append(name)
    return themes, demographics


def _streaming_sites(links: list[dict[str, Any]] | None) -> list[str]:
    if not links:
        return []
    sites: list[str] = []
    for link in links:
        site = link.get("site")
        if not site or site == "Official Site":
            continue
        sites.append(site)
    return sorted(set(sites))


def _mal_score_from_anilist(mean_score: int | None) -> float | None:
    if mean_score is None:
        return None
    return round(mean_score / 10.0, 2)


def _rankings_map(rankings: list[dict[str, Any]] | None) -> tuple[int | None, int | None]:
    """Best-effort MAL-like rank and popularity rank from AniList rankings."""
    if not rankings:
        return None, None
    rated = [r for r in rankings if r.get("type") == "RATED" and r.get("context") == "highest rated all time"]
    popular = [r for r in rankings if r.get("type") == "POPULAR" and r.get("context") == "most popular all time"]
    rank = rated[0]["rank"] if rated else None
    if rank is None:
        rated_any = [r for r in rankings if r.get("type") == "RATED"]
        rank = rated_any[0]["rank"] if rated_any else None
    pop_rank = popular[0]["rank"] if popular else None
    if pop_rank is None:
        pop_any = [r for r in rankings if r.get("type") == "POPULAR"]
        pop_rank = pop_any[0]["rank"] if pop_any else None
    return rank, pop_rank


def row_from_sources(
    mal_id: int,
    jikan: dict[str, Any] | None,
    anilist: dict[str, Any] | None,
    legacy: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build one output row; legacy fills gaps when APIs omit fields."""
    legacy = legacy or {}
    j = jikan or {}
    a = anilist or {}

    title = j.get("title") or (a.get("title") or {}).get("romaji") or legacy.get("name")
    title_english = j.get("title_english") or (a.get("title") or {}).get("english")
    title_japanese = j.get("title_japanese") or (a.get("title") or {}).get("native")

    j_type = j.get("type")
    if not j_type and a.get("format"):
        j_type = FORMAT_MAP.get(a["format"], a["format"])

    source = j.get("source")
    if not source and a.get("source"):
        source = MAL_SOURCE_MAP.get(a["source"], a["source"])

    genres = _list_names(j.get("genres")) or list(a.get("genres") or [])
    themes_j, demo_j = _jikan_themes_demographics(j)
    themes_a, demo_a = _anilist_tag_buckets(a.get("tags"))
    themes = themes_j or themes_a
    demographics = demo_j or demo_a

    studios = _list_names(j.get("studios")) or _list_names((a.get("studios") or {}).get("nodes"))
    producers = _list_names(j.get("producers"))
    licensors = _list_names(j.get("licensors"))

    score = j.get("score")
    if score is None and a.get("meanScore") is not None:
        score = _mal_score_from_anilist(a["meanScore"])
    if score is None and legacy.get("score") is not None and pd.notna(legacy.get("score")):
        score = legacy.get("score")

    scored_by = j.get("scored_by") or legacy.get("scored_by")
    members = j.get("members") or legacy.get("members")
    favorites = j.get("favorites") or a.get("favourites") or legacy.get("favorites")
    rank = j.get("rank") or legacy.get("rank")
    popularity = j.get("popularity") or legacy.get("popularity")

    if rank is None or popularity is None:
        r2, p2 = _rankings_map(a.get("rankings"))
        rank = rank if rank is not None else r2
        popularity = popularity if popularity is not None else p2

    season = j.get("season") or (a.get("season") or "").lower() if a.get("season") else None
    season_year = j.get("year") or a.get("seasonYear")

    episodes = j.get("episodes") if j.get("episodes") is not None else a.get("episodes")
    duration = j.get("duration")
    if not duration and a.get("duration"):
        duration = f"{a['duration']} min per ep"

    status = j.get("status") or a.get("status")
    if status and "_" in str(status):
        status = str(status).replace("_", " ").title()

    streaming_j = _streaming_sites(j.get("streaming"))
    streaming_a = _streaming_sites(a.get("externalLinks"))
    streaming_sites = streaming_j or streaming_a

    anilist_tags = a.get("tags") or []
    tag_names = [t.get("name") for t in anilist_tags if t.get("name")]

    row = {
        "animeID": mal_id,
        "name": title,
        "title_english": title_english,
        "title_japanese": title_japanese,
        "title_synonyms": json.dumps(a.get("synonyms") or [], ensure_ascii=False),
        "type": j_type,
        "source": source,
        "producers": json.dumps(producers, ensure_ascii=False),
        "licensors": json.dumps(licensors, ensure_ascii=False),
        "genre": json.dumps(genres, ensure_ascii=False),
        "themes": json.dumps(themes, ensure_ascii=False),
        "demographics": json.dumps(demographics, ensure_ascii=False),
        "studio": json.dumps(studios, ensure_ascii=False),
        "episodes": episodes,
        "status": status,
        "airing": j.get("airing"),
        "duration": duration,
        "rating": j.get("rating") or legacy.get("rating"),
        "score": score,
        "scored_by": scored_by,
        "rank": rank,
        "popularity": popularity,
        "members": members,
        "favorites": favorites,
        "season": season,
        "season_year": season_year,
        "premiered": legacy.get("premiered"),
        "broadcast": j.get("broadcast") or legacy.get("broadcast"),
        "anilist_id": a.get("id"),
        "anilist_trending": a.get("trending"),
        "anilist_tags": json.dumps(tag_names, ensure_ascii=False),
        "anilist_mean_score": a.get("meanScore"),
        "anilist_popularity": a.get("popularity"),
        "anilist_favourites": a.get("favourites"),
        "streaming_sites": json.dumps(streaming_sites, ensure_ascii=False),
        "jikan_fetched": bool(jikan),
        "anilist_fetched": bool(anilist),
        "start_date": legacy.get("start_date"),
        "end_date": legacy.get("end_date"),
        "aired_from_year": legacy.get("aired_from_year"),
        "aired_to_year": legacy.get("aired_to_year"),
    }

    if j.get("aired"):
        aired = j["aired"]
        if isinstance(aired, dict):
            row["start_date"] = (aired.get("from") or "")[:10] or row["start_date"]
            to_val = aired.get("to")
            row["end_date"] = (to_val or "")[:10] if to_val else row["end_date"]
    elif a.get("startDate"):
        sd = a["startDate"]
        if sd.get("year"):
            row["start_date"] = f"{sd.get('year')}-{sd.get('month') or 1:02d}-{sd.get('day') or 1:02d}"
            row["aired_from_year"] = sd.get("year")
        ed = a.get("endDate") or {}
        if ed.get("year"):
            row["end_date"] = f"{ed.get('year')}-{ed.get('month') or 1:02d}-{ed.get('day') or 1:02d}"
            row["aired_to_year"] = ed.get("year")

    if row["premiered"] is None and season and season_year:
        row["premiered"] = f"{str(season).title()} {season_year}"

    return row


def legacy_row_dict(df: pd.DataFrame) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for _, row in df.iterrows():
        mal_id = int(row["animeID"])
        out[mal_id] = row.to_dict()
    return out


def parse_legacy_list_field(val: Any) -> list[str]:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return []
    if isinstance(val, list):
        return val
    text = str(val)
    if text.startswith("["):
        try:
            parsed = json.loads(text.replace("'", '"'))
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            pass
    return re.findall(r"'([^']+)'", text)
