#!/usr/bin/env python3
"""Refresh the Artometrics anime MAL dataset via Jikan + AniList."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date
from pathlib import Path

import pandas as pd

from anilist_client import AniListClient
from changelog import write_changelog
from config import (
    BASELINE_CSV,
    BASELINE_SNAPSHOT_DATE,
    CACHE_DIR,
    DATA_DIR,
    LEGACY_ARTICLE_CSV,
    REPO_ROOT,
    SEASON_END_YEAR,
    SEASON_START_YEAR,
    SEASONS,
    STATE_DIR,
)
from jikan_client import JikanClient
from normalize import legacy_row_dict, row_from_sources

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("refresh")


def ensure_baseline() -> pd.DataFrame:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "baseline").mkdir(parents=True, exist_ok=True)
    if not BASELINE_CSV.exists():
        src = LEGACY_ARTICLE_CSV if LEGACY_ARTICLE_CSV.exists() else None
        if src is None:
            raise FileNotFoundError("No baseline anime.csv found")
        log.info("Copying baseline from %s", src)
        BASELINE_CSV.write_bytes(src.read_bytes())
    return pd.read_csv(BASELINE_CSV)


def discover_mal_ids(
    baseline: pd.DataFrame,
    jikan: JikanClient,
    anilist: AniListClient,
    *,
    jikan_seasons: bool,
    anilist_seasons: bool,
) -> set[int]:
    ids = set(baseline["animeID"].astype(int).tolist())
    log.info("Baseline MAL ids: %s", len(ids))

    if jikan_seasons and jikan.enabled and not jikan.unreachable:
        for year in range(SEASON_START_YEAR, SEASON_END_YEAR + 1):
            for season in SEASONS:
                entries = jikan.get_season(year, season)
                for entry in entries:
                    mid = entry.get("mal_id")
                    if mid:
                        ids.add(int(mid))
                log.info("Jikan season %s %s → total ids %s", year, season, len(ids))
        if jikan.unreachable:
            log.warning("Jikan season crawl stopped early (unreachable).")

    if anilist_seasons:
        for year in range(SEASON_START_YEAR, SEASON_END_YEAR + 1):
            for season in SEASONS:
                season_ids = anilist.season_mal_ids(year, season)
                ids.update(season_ids)
                log.info("AniList season %s %s → total ids %s", year, season, len(ids))

    return ids


def load_jikan_state() -> set[int]:
    path = STATE_DIR / "jikan_completed.json"
    if not path.exists():
        return set()
    try:
        return set(json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError:
        return set()


def save_jikan_state(done: set[int]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = STATE_DIR / "jikan_completed.json"
    path.write_text(json.dumps(sorted(done)), encoding="utf-8")


def build_dataframe(
    mal_ids: set[int],
    baseline: pd.DataFrame,
    jikan: JikanClient,
    anilist: AniListClient,
    *,
    max_jikan: int | None,
    skip_jikan: bool,
) -> pd.DataFrame:
    legacy_map = legacy_row_dict(baseline)
    sorted_ids = sorted(mal_ids)

    log.info("Fetching AniList media for %s ids (batched)...", len(sorted_ids))
    anilist_map = anilist.fetch_all_media(sorted_ids)

    jikan_done = load_jikan_state()
    rows: list[dict] = []
    jikan_fetched = 0

    for mal_id in sorted_ids:
        j_data = None
        if not skip_jikan and jikan.enabled and not jikan.unreachable:
            if mal_id in jikan_done:
                j_data = jikan.get_anime_full(mal_id)
            elif max_jikan is None or jikan_fetched < max_jikan:
                j_data = jikan.get_anime_full(mal_id)
                if j_data is not None:
                    jikan_fetched += 1
                    jikan_done.add(mal_id)
                    if jikan_fetched % 50 == 0:
                        save_jikan_state(jikan_done)
                        log.info("Jikan progress: %s fetched", jikan_fetched)

        a_data = anilist_map.get(mal_id)
        rows.append(
            row_from_sources(
                mal_id,
                j_data,
                a_data,
                legacy_map.get(mal_id),
            )
        )

    save_jikan_state(jikan_done)
    df = pd.DataFrame(rows)
    df = df.sort_values("animeID").reset_index(drop=True)
    return df


def write_outputs(df: pd.DataFrame, snapshot_date: str) -> tuple[Path, Path]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    stem = DATA_DIR / f"anime_{snapshot_date}"
    csv_path = stem.with_suffix(".csv")
    parquet_path = stem.with_suffix(".parquet")
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    latest_json = DATA_DIR / "anime_latest.json"
    public_json = REPO_ROOT / "public" / "data" / "anime" / "anime_latest.json"
    public_json.parent.mkdir(parents=True, exist_ok=True)
    slim = df[
        [
            "animeID",
            "name",
            "type",
            "source",
            "score",
            "season",
            "season_year",
            "streaming_sites",
            "anilist_trending",
        ]
    ].head(5000)
    payload = slim.to_json(orient="records")
    latest_json.write_text(payload, encoding="utf-8")
    public_json.write_text(payload, encoding="utf-8")
    return csv_path, parquet_path


def write_methods_note(path: Path, stats: dict) -> None:
    text = (
        f"We started with the TidyTuesday MyAnimeList export `tidy_anime.csv` "
        f"(snapshot {BASELINE_SNAPSHOT_DATE}, {stats['baseline_rows']:,} titles), "
        f"then refreshed it to {stats['refresh_date']} via the Tenrai API and AniList, "
        f"adding {stats['new_titles']:,} titles and {stats['new_variables']:,} variables. "
        "MyAnimeList fields (score, members, rank, etc.) come from the Tenrai API (api.tenrai.org), "
        "Jikan-compatible MyAnimeList mirror, accessed 2026-10-12; the public Jikan v4 API "
        "(api.jikan.moe) was discontinued on 2026-10-01."
    )
    path.write_text(text + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=date.today().isoformat(), help="Snapshot date YYYY-MM-DD")
    parser.add_argument("--skip-jikan", action="store_true", help="Skip Jikan fetches (AniList + baseline only)")
    parser.add_argument("--max-jikan", type=int, default=None, help="Cap Jikan full fetches this run")
    parser.add_argument("--no-jikan-seasons", action="store_true", help="Skip Jikan season discovery")
    parser.add_argument("--no-anilist-seasons", action="store_true", help="Skip AniList season discovery")
    args = parser.parse_args(argv)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    baseline = ensure_baseline()

    jikan = JikanClient(enabled=not args.skip_jikan)
    anilist = AniListClient()
    try:
        mal_ids = discover_mal_ids(
            baseline,
            jikan,
            anilist,
            jikan_seasons=not args.no_jikan_seasons,
            anilist_seasons=not args.no_anilist_seasons,
        )
        log.info("Unique MAL ids to build: %s", len(mal_ids))

        df = build_dataframe(
            mal_ids,
            baseline,
            jikan,
            anilist,
            max_jikan=args.max_jikan,
            skip_jikan=args.skip_jikan,
        )
    finally:
        jikan.close()
        anilist.close()

    csv_path, parquet_path = write_outputs(df, args.date)

    changelog_path = DATA_DIR / f"CHANGELOG_{BASELINE_SNAPSHOT_DATE}_to_{args.date}.md"
    stats = write_changelog(baseline, df, changelog_path, BASELINE_SNAPSHOT_DATE, args.date)

    dict_src = Path(__file__).parent / "data_dictionary.md"
    dict_dest = DATA_DIR / "DATA_DICTIONARY.md"
    dict_dest.write_text(dict_src.read_text(encoding="utf-8"), encoding="utf-8")

    methods_path = DATA_DIR / "METHODS_NOTE.md"
    write_methods_note(
        methods_path,
        {
            "baseline_rows": len(baseline),
            "refresh_date": args.date,
            "new_titles": stats["new_titles"],
            "new_variables": stats["new_variables"],
        },
    )

    log.info("Wrote %s and %s", csv_path, parquet_path)
    log.info(
        "Rows: %s | New titles: %s | New variables: %s",
        len(df),
        stats["new_titles"],
        stats["new_variables"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
