# Baseline dataset audit (pre-refresh)

| Field | Value |
|-------|--------|
| **Source** | TidyTuesday / Kaggle MyAnimeList scrape by Tam Nguyen |
| **Upstream URL** | https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-04-23 |
| **Raw file** | `tidy_anime.csv` |
| **SHA-256** | `5ea3a14492b5c559c728af0c7ec57b81c919d0efa4d381e54b0f7cde9934a1c2` |
| **Snapshot date** | 2019-04-23 (published by TidyTuesday) |
| **Scrape era** | Early 2019 MAL export |
| **Copy in repo** | `articles/anime/data/anime.csv`, `public/data/articles/anime/anime.csv` |
| **Row count** | 13,631 titles (one row per `animeID` in `articles/anime/data/anime.csv`) |
| **Column count** | 31 |
| **Primary key** | `animeID` — MyAnimeList anime id (`mal_id`) |

## Columns (legacy export)

`animeID`, `name`, `title_english`, `title_japanese`, `title_synonyms`, `type`, `source`, `producers`, `genre`, `studio`, `episodes`, `status`, `airing`, `aired`, `duration`, `rating`, `score`, `scored_by`, `rank`, `popularity`, `members`, `favorites`, `synopsis`, `background`, `premiered`, `broadcast`, `related`, `start_date`, `end_date`, `aired_from_year`, `aired_to_year`

## Article filter note

The published ANIME report narrative references **13,631** scored TV titles after analysis filters; the raw tidy export contains **13,856** rows across all formats before those filters.
