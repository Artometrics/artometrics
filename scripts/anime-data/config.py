"""Shared paths and constants for the anime refresh pipeline."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "anime"
CACHE_DIR = DATA_DIR / ".cache"
STATE_DIR = DATA_DIR / ".state"
BASELINE_CSV = DATA_DIR / "baseline" / "anime_tidy_anime_2019-04-23.csv"
LEGACY_ARTICLE_CSV = REPO_ROOT / "articles" / "anime" / "data" / "anime.csv"

JIKAN_BASE = "https://api.jikan.moe/v4"
ANILIST_URL = "https://graphql.anilist.co"

# Jikan: 3 req/s and 60/min — stay under both.
JIKAN_MIN_INTERVAL_S = 1.05
JIKAN_CONNECT_TIMEOUT_S = 15.0
JIKAN_READ_TIMEOUT_S = 45.0

ANILIST_MIN_INTERVAL_S = 2.5
ANILIST_BATCH_SIZE = 10

SEASONS = ("winter", "spring", "summer", "fall")
SEASON_START_YEAR = 1963
SEASON_END_YEAR = 2026

BASELINE_SNAPSHOT_DATE = "2019-04-23"
BASELINE_SHA256 = "5ea3a14492b5c559c728af0c7ec57b81c919d0efa4d381e54b0f7cde9934a1c2"
