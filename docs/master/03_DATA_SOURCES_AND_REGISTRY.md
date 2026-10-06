# Artometrics Master Manual: Data Sourcing and Research Registry

Document ID: ART-DATA-SRC-003  
Version: 2.0  
Classification: Internal Editorial & Analytical Reference  
Author: Artometrics Research Desk & Data Engineering Guild  

---

## 1. Registry Purpose and Governance

This document serves as the master source registry for Artometrics investigative reports, analytical models, and public chart notebooks. Every dataset utilized across our editorial coverage is categorized here with its ingestion protocol, endpoint patterns, update frequencies, citation requirements, and legal licensing terms.

---

## 2. Federal, Healthcare, and Demographic Registries

### 2.1 Centers for Medicare & Medicaid Services (CMS)
- **Primary Domain**: Healthcare economics, hospital quality, clinical accountability.
- **Key Programs**: 
  - Hospital Readmissions Reduction Program (HRRP)
  - Transforming Episode Accountability Model (TEAM)
  - Hospital Inpatient Quality Reporting (IQR)
  - Provider of Services (POS) Files
- **Access Protocol**: Socrata Open Data API (SODA) and bulk CSV dumps at `data.cms.gov`.
- **API Endpoint Pattern**:
  ```
  https://data.cms.gov/resource/{dataset_id}.json?$limit=50000&$where=excess_readmission_ratio IS NOT NULL
  ```
- **Update Frequency**: Annual (October for fiscal year penalties) and quarterly hospital refreshes.
- **Citation Standard**: `U.S. Centers for Medicare & Medicaid Services (CMS), Fiscal Year [YEAR] Inpatient Prospective Payment System (IPPS) Final Rule.`

### 2.2 U.S. Census Bureau
- **Primary Domain**: Demographics, regional housing, income inequality, municipal geography.
- **Key Programs**: American Community Survey (ACS 5-Year Estimates), Decennial Census.
- **Access Protocol**: REST API via `api.census.gov` (requires free API key).
- **API Endpoint Pattern**:
  ```
  https://api.census.gov/data/2023/acs/acs5?get=NAME,B19013_001E&for=county:*&key={CENSUS_API_KEY}
  ```
- **Update Frequency**: Annual (December release for previous 5-year pool).
- **Citation Standard**: `U.S. Census Bureau, American Community Survey 5-Year Estimates, Table [TABLE_ID].`

### 2.3 Bureau of Labor Statistics (BLS)
- **Primary Domain**: Inflation, real wage trajectories, cultural employment.
- **Key Programs**: Consumer Price Index (CPI), Occupational Employment and Wage Statistics (OEWS).
- **Access Protocol**: BLS Public API v2.0 (`api.bls.gov/publicAPI/v2/timeseries/data/`).
- **Update Frequency**: Monthly (CPI) and Annual (OEWS).
- **Citation Standard**: `U.S. Bureau of Labor Statistics, [Survey Name], Series [SERIES_ID].`

### 2.4 Bureau of Economic Analysis (BEA)
- **Primary Domain**: Arts and Cultural Production Satellite Account (ACPSA), State/County GDP.
- **Access Protocol**: BEA Data API (`apps.bea.gov/api/data`).
- **Update Frequency**: Annual.
- **Citation Standard**: `U.S. Bureau of Economic Analysis & National Endowment for the Arts, Arts and Cultural Production Satellite Account.`

### 2.5 Securities and Exchange Commission (SEC EDGAR)
- **Primary Domain**: Corporate entertainment finances, streaming economics, executive compensation.
- **Key Filings**: 10-K (Annual Reports), 10-Q (Quarterly Reports), DEF 14A (Proxy Statements).
- **Access Protocol**: EDGAR REST API (`data.sec.gov/api/xbrl/`).
- **Update Frequency**: Continuous per filing deadlines.
- **Citation Standard**: `U.S. Securities and Exchange Commission, Form 10-K filed by [Company Name] for fiscal year ended [Date].`

---

## 3. Culture, Entertainment, and Media Registries

### 3.1 Music Streaming & Audio Analytics (Spotify / Chartmetric)
- **Primary Domain**: Audio features (acousticness, danceability, energy, speechiness, valence), streaming velocity.
- **Access Protocol**: Spotify Web API (`api.spotify.com/v1/audio-features`) via OAuth2 Client Credentials.
- **Ingestion Tooling**: `spotipy` (Python) or `spotifyr` (R).
- **Update Frequency**: Weekly track extracts and daily chart positions.
- **Citation Standard**: `Spotify Web API Audio Features Database, extracted [Date].`

### 3.2 Theatrical Film & Box Office (The Numbers / Box Office Mojo)
- **Primary Domain**: Historical box office grosses, production budgets, distributor market shares.
- **Access Protocol**: Structured web extracts and Nash Information Services data partnerships.
- **Normalization Standard**: All historical grosses must be converted to real purchasing power using BLS CPI-U historical deflators.
- **Citation Standard**: `The Numbers (Nash Information Services LLC) and Box Office Mojo, Historical Box Office Database.`

### 3.3 Screen Media & Ratings (IMDb)
- **Primary Domain**: Filmography credits, episode ratings, runtime distributions.
- **Access Protocol**: Official non-commercial TSV releases (`datasets.imdbws.com`).
  - `title.basics.tsv.gz`
  - `title.ratings.tsv.gz`
  - `title.crew.tsv.gz`
- **Update Frequency**: Daily snapshots.
- **Citation Standard**: `IMDb Non-Commercial Datasets, accessed [Date].`

### 3.4 Animation & International Media (MyAnimeList / Jikan)
- **Primary Domain**: Global anime catalog ratings, studio output, format hit-rates.
- **Access Protocol**: Jikan REST API v4 (`api.jikan.moe/v4/`).
- **Data Dictionary**: Minimum threshold for score reliability is $\ge 1,000$ user reviews.
- **Citation Standard**: `MyAnimeList API via Jikan v4, historical archive.`

### 3.5 Video Game & Digital Platforms (SteamDB / SteamSpy)
- **Primary Domain**: Concurrent player peaks, player retention curves, pricing elasticity.
- **Access Protocol**: Steamworks Web API and SteamSpy public endpoints.
- **Citation Standard**: `SteamDB and Valve Corporation, Player Activity Analytics.`

### 3.6 Literary Corpora & Fine Art (Project Gutenberg / WikiArt)
- **Primary Domain**: Historical texts, lexical complexity, artistic movement classifications.
- **Access Protocol**: Standardized text corpora under `public/data/reference/`.
- **Citation Standard**: `Project Gutenberg Electronic Public Library / WikiArt Visual Arts Encyclopedia.`

---

## 4. Sports Analytics Registries

### 4.1 Baseball (MLB Statcast / Baseball Savant)
- **Primary Domain**: Pitch velocity, horizontal/vertical break, launch angle, sprint speed.
- **Access Protocol**: `baseballr` (R package) and Baseball Savant search CSV endpoints.
- **Citation Standard**: `Major League Baseball Advanced Media (MLBAM), Statcast Tracking System.`

### 4.2 Basketball (NBA Stats API)
- **Primary Domain**: Player tracking, shot coordinate zones, true shooting efficiency.
- **Access Protocol**: `stats.nba.com/stats/` via custom headers mimicking client browser sessions.
- **Citation Standard**: `NBA Stats API, Official League Data.`

---

## 5. Global Trade, Complexity, and Environmental Registries

### 5.1 Bilateral Trade (UN Comtrade / OEC)
- **Primary Domain**: National exports, trade balance, Economic Complexity Index (ECI).
- **Access Protocol**: UN Comtrade API v1 / Observatory of Economic Complexity bulk datasets.
- **Standard**: Harmonized System (HS) 6-digit classification codes.
- **Citation Standard**: `United Nations Comtrade Database and The Observatory of Economic Complexity.`

### 5.2 Environmental & Climate (NOAA NCEI)
- **Primary Domain**: Global temperature anomalies, extreme weather occurrences.
- **Access Protocol**: National Centers for Environmental Information CDO API (`www.ncdc.noaa.gov/cdo-web/api/v2/`).
- **Citation Standard**: `National Oceanic and Atmospheric Administration (NOAA), National Centers for Environmental Information.`

---

## 6. Sourcing Protocol and Legal Compliance

1. **Attribution Requirement**: Every published chart must include a `Source:` credit in the figure subtitle or caption referencing the primary registry.
2. **Archival Integrity**: Whenever an analysis is completed, a frozen copy of the exact query result must be archived in `articles/<slug>/data/raw/` in Parquet or compressed CSV format. Live URL dependencies in production code are strictly prohibited.
3. **Terms of Service**: Web scraping must respect `robots.txt` directives, rate limits, and non-commercial terms. Commercial research APIs must use dedicated Artometrics project tokens.
4. **Zero Emojis**: All database column mappings, data dictionaries, research memos, and scripts must adhere to the zero-emoji policy.
