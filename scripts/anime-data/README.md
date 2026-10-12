# Anime data refresh pipeline

Reproducibly extends the Artometrics **ANIME** report dataset (baseline: TidyTuesday `tidy_anime.csv`, 2019-04-23) with current MyAnimeList ids via the **Tenrai API** (Jikan v4-compatible; `api.jikan.moe` was discontinued 2026-10-01; override with `JIKAN_BASE`) and **AniList GraphQL** (`idMal`).

## Setup

```bash
cd scripts/anime-data
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.lock
```

## Refresh

For long Jikan/Tenrai passes, warm the cache first (new titles first, resumable):

```bash
python prefetch_jikan.py --snapshot ../../data/anime/anime_YYYY-MM-DD.csv --deadline-hours 6
python refresh.py --date YYYY-MM-DD --max-jikan 0 --no-jikan-seasons
```

```bash
python refresh.py --date 2026-10-11
```

Options:

- `--skip-jikan` — AniList + baseline merge only (useful when `api.jikan.moe` is unreachable).
- `--max-jikan N` — cap per-run Jikan `/anime/{id}/full` calls; resume state in `data/anime/.state/`.
- `--no-jikan-seasons` / `--no-anilist-seasons` — disable season discovery on one API.

Outputs (under `data/anime/`):

- `anime_YYYY-MM-DD.parquet` and `.csv`
- `CHANGELOG_2019-04-23_to_YYYY-MM-DD.md`
- `DATA_DICTIONARY.md`, `METHODS_NOTE.md`
- `anime_latest.json` (slim static export for the site)
- `.cache/` — API response cache (gitignored)

## Exploratory charts

```bash
python correlations.py
```

Writes PNGs to `data/anime/exploratory/` (not wired into the live article).

## Rate limits

- Jikan: ≥1.05s between requests (under 3/s and 60/min); cached responses are not re-fetched.
- AniList: ≥0.7s between GraphQL calls; batched 25 `Media` nodes per query.
