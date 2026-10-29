"""AniList GraphQL client (season discovery + batched Media by idMal)."""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from config import ANILIST_BATCH_SIZE, ANILIST_MIN_INTERVAL_S, ANILIST_URL, CACHE_DIR
from rate_limit import RateLimiter

log = logging.getLogger(__name__)

_anilist_limiter = RateLimiter(ANILIST_MIN_INTERVAL_S)

MEDIA_FRAGMENT = """
fragment MediaFields on Media {
  id
  idMal
  title { romaji english native }
  format
  status
  episodes
  duration
  season
  seasonYear
  source
  meanScore
  averageScore
  popularity
  favourites
  trending
  isLicensed
  genres
  synonyms
  studios(isMain: true) { nodes { name } }
  externalLinks { site url type }
  tags { name rank category }
  startDate { year month day }
  endDate { year month day }
}
"""

SEASON_PAGE_QUERY = """
query ($page: Int, $perPage: Int, $year: Int, $season: MediaSeason) {
  Page(page: $page, perPage: $perPage) {
    pageInfo { hasNextPage currentPage lastPage }
    media(seasonYear: $year, season: $season, type: ANIME, sort: ID) {
      idMal
      id
    }
  }
}
"""

BATCH_BY_MAL_QUERY = MEDIA_FRAGMENT + """
query(%s) {
%s
}
"""


def _cache_read(key: str) -> Any | None:
    path = CACHE_DIR / "anilist" / f"{key}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _cache_write(key: str, payload: Any) -> None:
    path = CACHE_DIR / "anilist" / f"{key}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


class AniListClient:
    def __init__(self) -> None:
        self._client = httpx.Client(timeout=httpx.Timeout(60.0, connect=15.0))

    def close(self) -> None:
        self._client.close()

    @retry(stop=stop_after_attempt(12), wait=wait_exponential(multiplier=2, min=5, max=120))
    def _post(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        import time

        _anilist_limiter.wait()
        resp = self._client.post(
            ANILIST_URL,
            json={"query": query, "variables": variables or {}},
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code == 429:
            time.sleep(60)
            raise httpx.HTTPStatusError("anilist rate limit", request=resp.request, response=resp)
        if resp.status_code == 404:
            return {"data": {}}
        resp.raise_for_status()
        body = resp.json()
        errors = body.get("errors") or []
        fatal = [
            e
            for e in errors
            if e.get("status") != 404 and "Not Found" not in e.get("message", "")
        ]
        if fatal and not body.get("data"):
            raise RuntimeError(f"AniList errors: {fatal}")
        return body

    def season_mal_ids(self, year: int, season: str) -> set[int]:
        season_enum = season.upper()
        cache_key = f"season_ids_{year}_{season_enum}"
        cached = _cache_read(cache_key)
        if cached is not None:
            return set(cached)

        mal_ids: set[int] = set()
        page = 1
        while True:
            body = self._post(
                SEASON_PAGE_QUERY,
                {"page": page, "perPage": 50, "year": year, "season": season_enum},
            )
            page_data = body["data"]["Page"]
            for media in page_data["media"]:
                if media.get("idMal"):
                    mal_ids.add(int(media["idMal"]))
            info = page_data["pageInfo"]
            if not info.get("hasNextPage"):
                break
            page += 1
        _cache_write(cache_key, sorted(mal_ids))
        return mal_ids

    def fetch_media_batch(self, mal_ids: list[int]) -> dict[int, dict[str, Any]]:
        """Return mapping mal_id -> Media (AniList); skips unknown ids."""
        if not mal_ids:
            return {}
        cache_key = f"batch_{'-'.join(str(i) for i in mal_ids)}"
        cached = _cache_read(cache_key)
        if cached is not None:
            return {int(k): v for k, v in cached.items()}

        var_defs: list[str] = []
        fields: list[str] = []
        variables: dict[str, int] = {}
        for idx, mal_id in enumerate(mal_ids):
            name = f"m{idx}"
            var_defs.append(f"${name}: Int")
            variables[name] = mal_id
            fields.append(
                f"  {name}: Media(idMal: ${name}, type: ANIME) {{ ...MediaFields }}"
            )
        query = BATCH_BY_MAL_QUERY % (", ".join(var_defs), "\n".join(fields))
        body = self._post(query, variables)
        out: dict[int, dict[str, Any]] = {}
        for key, media in (body.get("data") or {}).items():
            if media and media.get("idMal"):
                out[int(media["idMal"])] = media
        _cache_write(cache_key, {str(k): v for k, v in out.items()})
        return out

    def fetch_all_media(self, mal_ids: list[int]) -> dict[int, dict[str, Any]]:
        merged: dict[int, dict[str, Any]] = {}
        unique = sorted(set(mal_ids))
        for i in range(0, len(unique), ANILIST_BATCH_SIZE):
            chunk = unique[i : i + ANILIST_BATCH_SIZE]
            merged.update(self.fetch_media_batch(chunk))
        return merged
