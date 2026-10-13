# Anime dataset dictionary

One row per MyAnimeList anime id (`animeID`). Snapshot files live at `data/anime/anime_YYYY-MM-DD.parquet` (and `.csv`).

## Provenance

| Item | Value |
|------|--------|
| Baseline | TidyTuesday `tidy_anime.csv` (Kaggle MyAnimeList scrape by Tam Nguyen, early 2019) |
| Baseline snapshot date | 2019-04-23 |
| Baseline SHA-256 | `5ea3a14492b5c559c728af0c7ec57b81c919d0efa4d381e54b0f7cde9934a1c2` |
| Refresh APIs | Tenrai API (api.tenrai.org), Jikan-compatible MyAnimeList mirror, accessed 2026-10-12 (replaces Jikan v4, discontinued 2026-10-01; field names below keep the Jikan v4 schema), [AniList GraphQL](https://anilist.gitbook.io/anilist-apiv2-docs/) (`idMal`) |
| Pipeline | `scripts/anime-data/refresh.py` |

## Columns

| Column | Type | Source |
|--------|------|--------|
| `animeID` | int | MAL anime id (primary key); discovery via Jikan seasons + AniList season pages + baseline ids |
| `name` | string | Jikan `title`; else AniList `title.romaji`; else baseline |
| `title_english` | string | Jikan `title_english`; else AniList `title.english` |
| `title_japanese` | string | Jikan `title_japanese`; else AniList `title.native` |
| `title_synonyms` | JSON list | AniList `synonyms` |
| `type` | string | Jikan `type`; else AniList `format` mapped to MAL-style label |
| `source` | string | Jikan `source`; else AniList `source` enum mapped to MAL label |
| `producers` | JSON list | Jikan `producers[].name` |
| `licensors` | JSON list | Jikan `licensors[].name` |
| `genre` | JSON list | Jikan `genres[].name`; else AniList `genres` |
| `themes` | JSON list | Jikan `themes[].name`; else AniList tags with theme/setting categories |
| `demographics` | JSON list | Jikan `demographics[].name`; else AniList demographic tags |
| `studio` | JSON list | Jikan `studios[].name`; else AniList main `studios.nodes` |
| `episodes` | int | Jikan `episodes`; else AniList `episodes` |
| `status` | string | Jikan `status`; else AniList `status` (normalized) |
| `airing` | bool | Jikan `airing` |
| `duration` | string | Jikan `duration`; else AniList `duration` (minutes) formatted |
| `rating` | string | Jikan `rating`; else baseline |
| `score` | float | Jikan `score` (0–10); else AniList `meanScore`/10; else baseline |
| `scored_by` | int | Jikan `scored_by`; else baseline |
| `rank` | int | Jikan `rank`; else AniList `rankings` (rated); else baseline |
| `popularity` | int | Jikan `popularity`; else AniList `rankings` (popular); else baseline |
| `members` | int | Jikan `members`; else baseline |
| `favorites` | int | Jikan `favorites`; else AniList `favourites`; else baseline |
| `season` | string | Jikan `season`; else AniList `season` (lowercase) |
| `season_year` | int | Jikan `year`; else AniList `seasonYear` |
| `premiered` | string | Derived `Season YYYY` or baseline `premiered` |
| `broadcast` | string | Jikan `broadcast`; else baseline |
| `start_date` | date string | Jikan `aired.from`; else AniList `startDate`; else baseline |
| `end_date` | date string | Jikan `aired.to`; else AniList `endDate`; else baseline |
| `aired_from_year` | int | Parsed from start date or baseline |
| `aired_to_year` | int | Parsed from end date or baseline |
| `anilist_id` | int | AniList internal `Media.id` |
| `anilist_trending` | int | AniList `trending` |
| `anilist_tags` | JSON list | AniList `tags[].name` |
| `anilist_mean_score` | int | AniList `meanScore` (0–100) |
| `anilist_popularity` | int | AniList `popularity` (user-list count) |
| `anilist_favourites` | int | AniList `favourites` |
| `streaming_sites` | JSON list | Jikan `streaming[].name`; else AniList `externalLinks[].site` (excludes Official Site) |
| `jikan_fetched` | bool | Whether Jikan `/anime/{id}/full` succeeded this run |
| `anilist_fetched` | bool | Whether AniList returned `Media` for `idMal` |

Legacy narrative fields (`synopsis`, `background`, `related`, `aired` blob) are omitted from refreshed snapshots to keep files smaller; they remain in the 2019 baseline export under `data/anime/baseline/`.


## Clean-file analysis flags (`anime_2026-10-11_clean.*`)

Added by `scripts/anime-data/clean_audit.py` (seed 20261011). See `CLEANING_LOG.md` / `METHODS_NOTE.md`.

| Column | Type | Definition |
|--------|------|------------|
| `flag_unfetched_jikan` | bool | `not jikan_fetched` |
| `flag_isekai` | bool | "isekai" in themes/genre/anilist_tags/demographics |
| `flag_analysis_year` | float | `aired_from_year` with `season_year` fallback |
| `flag_tv` | bool | `type == "TV"` |
| `flag_core_av` | bool | type in TV, Movie, ONA, OVA |
