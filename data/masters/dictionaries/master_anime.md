# Data dictionary — master_anime

Built: 2026-10-29T07:32:36Z

| column | type | description | source |
|---|---|---|---|
| animeID | int | MyAnimeList id | Tenrai/MAL |
| name | str | Primary title | Tenrai/MAL |
| type | str | TV/Movie/OVA/ONA/… | Tenrai/MAL |
| source | str | Manga/Original/Light novel/… | Tenrai/MAL |
| score | float | MAL score 0–10 | Tenrai/MAL |
| members | int | MAL members | Tenrai/MAL |
| season_year | int | Premier year | Tenrai/MAL |
| aired_from_year | int | Start year | Tenrai/MAL |
| genre | str | Comma-separated genres | Tenrai/MAL |
| studio | str | Comma-separated studios | Tenrai/MAL |
| jikan_fetched | bool | Fetched from Tenrai this pipeline | pipeline |
| as_of | date | Master build date | pipeline |
