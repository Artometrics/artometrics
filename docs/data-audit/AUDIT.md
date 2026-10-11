# Artometrics article data audit

**Generated:** 2026-10-11 23:07 UTC  
**Scope:** Read-only inventory of committed repo data and chart source credits in `src/content/blog/*.md`. Live site not mutated. Article bodies not changed.

## Executive summary

- **Reports in corpus:** 100 (`src/content/blog/`).
- **Tier A investigative homes** (dedicated `articles/<slug>/data/`): anime, padres, franchise, readmitted, youtube, poison.
- **TidyTuesday-driven `dataset.csv` reports:** ~62 rows in inventory (plus other bespoke pipelines).
- **Master registry (existing):** `docs/master/03_DATA_SOURCES_AND_REGISTRY.md`.

## 1. Inventory

Full machine-readable inventory: [`datasets.csv`](./datasets.csv).

### Tier A — dataset ledger

#### `anime`

- **tidy_anime / anime.csv** — MyAnimeList via TidyTuesday 2019-04-23 (Kaggle scrape, Tam Nguyen). Snapshot: 2019-02 (MAL scrape); published 2019-04-23. Rows: 13631. License: Community/TidyTuesday; MAL user data. Obtained: Frozen CSV in repo; SOURCE.txt SHA256.
  - File: `articles/anime/data/anime.csv`

#### `padres`

- **Lahman Teams/SeriesPost/Salaries** — Lahman Baseball Database 2025. Snapshot: 2025 release (+ 2026 B-Ref supplement). Rows: 3614. License: CC BY-SA 4.0. Obtained: articles/padres/data/lahman/*.csv.
  - File: `articles/padres/data/lahman/Teams.csv`
- **cbt_payroll.csv** — Spotrac compilation (article cites July 2026 draft). Snapshot: 2026-07. Rows: 6. License: Spotrac ToS. Obtained: Manual editorial CSV.
  - File: `articles/padres/data/cbt_payroll.csv`
- **padres_seasons.csv / summary.json** — Derived from Lahman + editorial 2026 endpoint. Snapshot: 2026. Rows: 58. License: CC BY-SA 4.0 (Lahman-derived). Obtained: npm run brief:padres.
  - File: `articles/padres/data/padres_seasons.csv`

#### `franchise`

- **franchise.csv (long)** — TidyTuesday 2019-07-02 → Wikipedia highest-grossing franchises. Snapshot: 2019-07. Rows: 321. License: Wikipedia CC BY-SA; revenue estimates. Obtained: SOURCE.txt.
  - File: `articles/franchise/data/franchise.csv`
- **top10_franchise_share_by_year.csv** — Box Office Mojo yearly charts (manual franchise coding). Snapshot: Varies by year. Rows: 6. License: Editorial + BOM ToS. Obtained: box_office_mojo_yearly_urls.csv index.
  - File: `articles/franchise/data/top10_franchise_share_by_year.csv`
- **disney_segment_revenue_fy2024.csv** — Disney Form 10-K FY2024. Snapshot: 2024-09-28 FY. Rows: 3. License: SEC public filing. Obtained: Manual extract.
  - File: `articles/franchise/data/disney_segment_revenue_fy2024.csv`

#### `readmitted`

- **raw_hrrp.csv** — CMS dataset 9n3s-kdb3 (HRRP supplemental). Snapshot: 2026-10 extract; window 2021-07–2024-06. Rows: 18330. License: U.S. government public data. Obtained: npm run brief:readmitted / CMS bulk.
  - File: `articles/readmitted/data/raw_hrrp.csv`
- **raw_hospital_general.csv** — CMS dataset xubh-q36u. Snapshot: Paired with HRRP refresh. Rows: 5419. License: U.S. government public data. Obtained: Offline join on Facility ID.
  - File: `articles/readmitted/data/raw_hospital_general.csv`

#### `youtube`

- **alphabet_youtube_ads_revenue.csv** — Alphabet 10-K YouTube ads line. Snapshot: FY2018–FY2024. Rows: 7. License: SEC filing. Obtained: Manual.
  - File: `articles/youtube/data/alphabet_youtube_ads_revenue.csv`
- **nielsen_youtube_tv_screen_share.csv** — Nielsen The Gauge / Media Distributor Gauge press. Snapshot: 2024-07–2025-07 monthly. Rows: 4. License: Nielsen press release terms. Obtained: Manual from press PDFs.
  - File: `articles/youtube/data/nielsen_youtube_tv_screen_share.csv`
- **h3.csv / h3_*** — Artometrics h3 pipeline (YouTube API, Podchaser, Arctic Shift). Snapshot: 2026-04 per article. Rows: 1638. License: Mixed; API ToS. Obtained: External repo + frozen CSVs.
  - File: `articles/youtube/data/h3.csv`

#### `poison`

- **chart1_revenue_stream_share.csv** — Derived from franchise.csv (≥$4B subset). Snapshot: 2019 franchise ledger. Rows: 2. License: Same as franchise. Obtained: Recomputed for R2 alignment (56/44).
  - File: `articles/poison/data/chart1_revenue_stream_share.csv`
- **chart2–3 case studies** — Editorial locked values from prior embeds. Snapshot: Static. Rows: 6. License: Editorial. Obtained: CSV lock.
  - File: `articles/poison/data/chart2_leto_slate_ratios.csv`

### Bulk template reports (TidyTuesday / `dataset.csv`)

Dozens of culture and civics reports pull a single weekly TidyTuesday extract into `public/data/articles/<slug>/dataset.csv` (mirrored under `articles/<slug>/data/` when materialized). Each post’s Methods section and `data-source` chart credits name the upstream week. See `datasets.csv` filtered by `article_class=tidytuesday_template`.

### Sports / federal / SEC patterns

- **MLB family** (padres, yankees, dodgers, …): Lahman + Baseball-Reference supplements; Spotrac for CBT.
- **CMS** (readmitted): frozen HRRP + Hospital General Information joins.
- **SEC** (youtube, franchise Disney table): manual 10-K extracts.

## 2. Health check

### Claim vs data spot checks

| Article | Published claim | Committed data | Severity | Note |
| --- | --- | --- | --- | --- |
| readmitted | 48.2% pairs ERR>1 (prose) | 48.15% (n=11720) | low | SOURCE.txt records 48.15%; rounding to 48.2% in headline |
| anime | 13,631 unique titles | 13631 | low | matches deduped animeID file |
| poison | 56% merchandise share (chart1) | 56% in CSV | low | Documented reconciliation vs older 61/39 copy |

### Structural issues (by severity)

| Severity | Article | File | Issue | Suggested fix |
| --- | --- | --- | --- | --- |
| high | anime | `articles/anime/data/anime.csv` | MAL snapshot ends ~2019; post-2019 hits absent | Refresh via Jikan/AniList; archive new snapshot |
| high | franchise | `articles/franchise/data/franchise.csv` | Wikipedia revenue estimates (mid-2019); not audited financials | Cross-walk to SEC segments + TMDB collections; CPI-adjust |
| medium | readmitted | `articles/readmitted/data/raw_hrrp.csv` | 18,330 raw rows vs 11,720 analytic pairs (CMS suppression) | Keep ≥25-discharge filter documented in brief script |
| medium | padres | `articles/padres/data/cbt_payroll.csv` | Spotrac payroll is manual/snapshot; not cash payroll | Document refresh cadence; add MLB CBT official where available |
| medium | youtube | `articles/youtube/data/` | Goldman/Nielsen tables are third-party; H3 excludes Shorts | Label projections; optional Shorts sensitivity appendix |
| low | poison | `articles/poison/data/chart2_leto_slate_ratios.csv` | Case-study constants not tied to external API | Link to franchise + box office sources per title |
| medium | tidytuesday_* | `public/data/articles/*/dataset.csv` | Many extracts frozen 2018–2020; stale for newsy topics | Prioritize refresh by traffic; keep SHA256 in SOURCE.txt |
| medium | bikeshare | `articles/bikeshare/data/dataset.csv` | column 'TripType' missing 100% | impute, filter, or document suppression |
| medium | breweries | `articles/breweries/data/dataset.csv` | column 'ibu' missing 42% | impute, filter, or document suppression |
| medium | broadway | `articles/broadway/data/dataset.csv` | column 'potential_gross' missing 100% | impute, filter, or document suppression |
| medium | broadway | `articles/broadway/data/dataset.csv` | column 'top_ticket_price' missing 100% | impute, filter, or document suppression |
| medium | calories | `articles/calories/data/dataset.csv` | 2 duplicate rows | dedupe on primary key |
| medium | calories | `articles/calories/data/dataset.csv` | column 'vit_a' missing 42% | impute, filter, or document suppression |
| medium | calories | `articles/calories/data/dataset.csv` | column 'vit_c' missing 41% | impute, filter, or document suppression |
| medium | ceos | `articles/ceos/data/dataset.csv` | column 'interim_coceo' missing 97% | impute, filter, or document suppression |
| medium | ceos | `articles/ceos/data/dataset.csv` | column 'still_there' missing 83% | impute, filter, or document suppression |
| medium | cetaceans | `articles/cetaceans/data/dataset.csv` | column 'mother' missing 73% | impute, filter, or document suppression |
| medium | cetaceans | `articles/cetaceans/data/dataset.csv` | column 'father' missing 78% | impute, filter, or document suppression |
| medium | cetaceans | `articles/cetaceans/data/dataset.csv` | column 'transfers' missing 63% | impute, filter, or document suppression |
| medium | comics | `articles/comics/data/dataset.csv` | column 'eye' missing 45% | impute, filter, or document suppression |
| medium | comics | `articles/comics/data/dataset.csv` | column 'gsm' missing 99% | impute, filter, or document suppression |
| medium | games | `articles/games/data/dataset.csv` | column 'compilation' missing 97% | impute, filter, or document suppression |
| medium | legos | `articles/legos/data/dataset.csv` | column 'inventory_id' missing 88% | impute, filter, or document suppression |
| medium | legos | `articles/legos/data/dataset.csv` | column 'quantity' missing 88% | impute, filter, or document suppression |
| medium | mac | `articles/mac/data/dataset.csv` | column 'gdp_dollar' missing 49% | impute, filter, or document suppression |
| medium | mac | `articles/mac/data/dataset.csv` | column 'adj_price' missing 49% | impute, filter, or document suppression |
| medium | mac | `articles/mac/data/dataset.csv` | column 'usd_adjusted' missing 49% | impute, filter, or document suppression |
| medium | margins | `articles/margins/data/dataset.csv` | 1 duplicate rows | dedupe on primary key |
| medium | medium | `articles/medium/data/dataset.csv` | column 'subtitle' missing 40% | impute, filter, or document suppression |
| medium | medium | `articles/medium/data/dataset.csv` | column 'publication' missing 59% | impute, filter, or document suppression |
| medium | museums | `articles/museums/data/dataset.csv` | column 'Address_line_2' missing 67% | impute, filter, or document suppression |
| medium | netflix | `articles/netflix/data/dataset.csv` | 1 duplicate rows | dedupe on primary key |

## 3. Upgrade research — candidate sources

See [`candidate_sources.csv`](./candidate_sources.csv) for the full table (APIs, cost, license, cadence, effort, Apify gap, ToU risk).

Highlights by Tier A topic:

| Topic | Priority additions |
| --- | --- |
| Anime | Jikan v4, AniList GraphQL, Wikidata studios |
| Padres | Lahman annual refresh, MLB Stats API, Retrosheet game logs |
| Franchise | TMDB collections, SEC EDGAR, BLS CPI deflation, BOM via controlled extract |
| Readmitted | CMS API refresh, Care Compare outcomes, HCRIS margins |
| YouTube | SEC XBRL automation, YouTube Data API quota plan, Nielsen press archive |
| Poison | Recompute from refreshed franchise ledger + box office case files |

**Apify / scraper gaps (ToU-sensitive):** Box Office Mojo yearly pages, Spotrac payroll tables, Nielsen PDF tables, and legacy MAL bulk scrape should use Apify only with robots/ToS review — prefer official APIs (CMS, SEC, BLS, FRED, TMDB, Jikan) where available.

## 4. Cross-article enrichment ideas

1. **Wikidata entity graph** — Map studios (anime), distributors (franchise), teams (MLB), and parent companies to QIDs for consistent labels and external links.
2. **BLS CPI-U (and optional FRED FX)** — Inflation-adjust all nominal USD franchise/box-office/ payroll figures to a stated base year (e.g. 2025 USD).
3. **Shared `SOURCE.txt` + SHA256** — Extend anime/franchise/readmitted pattern to every `articles/<slug>/data/` home.
4. **SEC segment crosswalk** — Join Disney/Warner/Netflix/Alphabet revenue lines to media-franchise narratives (youtube, franchise, streaming).
5. **CMS hospital ID bridge** — Propagate CCN from readmitted to any future health reports.
6. **IMDb/TMDB title IDs** — For film/television reports, unify sequel/franchise logic.
7. **OpenAlex institution IDs** — For phds/metrics science desks.
8. **Reference catalogs** — Leverage `public/data/reference/` (Gutenberg, WikiArt) as join keys for culture reports.

## 5. Top 10 upgrades (impact vs effort)

| Rank | Upgrade | Impact | Effort | Rationale |
| --- | --- | --- | --- | --- |
| 1 | CMS HRRP automated refresh + SOURCE SHA | Credibility | S | Flagship health report; data already pipelined |
| 2 | Anime MAL refresh (Jikan/AniList) | Story + credibility | M | Removes 7-year staleness on flagship culture report |
| 3 | BLS CPI deflator on all USD charts | Credibility | S | Single lib used across franchise, sports payroll, film |
| 4 | SEC XBRL pull for YouTube/Disney/Netflix lines | Credibility | M | Cuts manual 10-K transcription errors |
| 5 | Franchise revenue re-base (Wikidata + SEC) | Story | L | Replaces 2019 Wikipedia estimates |
| 6 | Lahman + MLB API annual sync for baseball desk | Story | S | Padres/yankees/dodgers share pipeline |
| 7 | TMDB franchise collections | Story | M | Improves sequel/franchise tagging vs manual BOM |
| 8 | Wikidata studio/company join | Story | M | Cross-links anime, franchise, streaming |
| 9 | TidyTuesday refresh queue (traffic-ranked) | Credibility | M | Fixes stale civics/culture templates at scale |
| 10 | Nielsen/press PDF structured archive | Story | S | YouTube TV-share charts reproducible without re-OCR |

## Reproduction

```bash
python3 scripts/data-audit/generate_audit.py
```

Outputs: this file, `datasets.csv`, `candidate_sources.csv`.
