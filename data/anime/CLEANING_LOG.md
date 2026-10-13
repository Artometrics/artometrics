# CLEANING_LOG — anime_2026-10-11 → anime_2026-10-11_clean

**Run (UTC):** 2026-10-12T19:47:34Z  
**Seed:** `20261011`  
**Raw SHA-256:** `77b0f9112db7bf0337a998730c1f10838d80628831be2c59ea3a1e4c1b619340`  
**Environment:** Python 3.13.5, pandas 3.0.6, numpy 2.5.3, Linux-6.12.94+-x86_64-with-glibc2.41

**Pipeline:** `python3 scripts/anime-data/clean_audit.py` (this file is an output of that script).

## Inclusion / exclusion (PRISMA-style counts)

| Step | N | Description |
|------|--:|-------------|
| `A_raw_snapshot` | 18,818 | Rows in anime_2026-10-11.csv |
| `B_after_dedupe` | 18,818 | After R1 dedupe |
| `C_clean_all_types` | 18,813 | Clean file (all types; flags only) |
| `D_tv_only` | 6,095 | Inclusion: type==TV (article narrative frame) |
| `E_tv_fetched` | 6,094 | TV ∩ jikan_fetched |
| `F_tv_scored` | 6,073 | TV with non-null score |
| `G_core_av` | 15,245 | Sensitivity: TV/Movie/ONA/OVA |
| `H_excl_music_special` | 16,283 | Sensitivity: drop Music+Special |

### Inclusion rule (headline / article-parallel stats)

- **Unit of analysis:** one MyAnimeList anime id (`animeID`).
- **Headline TV frame:** `type == "TV"` (matches the published ANIME report’s TV-centric comparisons).
- **Isekai definition:** case-insensitive match for `"isekai"` in any of `themes`, `genre`, `anilist_tags`, or `demographics` (list fields).
- **Year:** `aired_from_year`, falling back to `season_year`.
- **Unfetched rows** (`jikan_fetched == False`, n=156): **retained** in the clean file with `flag_unfetched_jikan`; excluded only in sensitivity / fetched-only recomputes.

### Exclusion / sensitivity

- Music and Specials remain in the clean file; sensitivity recomputes drop them or restrict to TV/Movie/ONA/OVA (see METHODS_NOTE).
- No rows deleted solely for missing score or missing AniList join.

## Cleaning rules

### R1_dedupe_animeID

- **Description:** Keep one row per animeID; prefer jikan_fetched=True.
- **rows_before:** 18818
- **rows_after:** 18818
- **rows_removed:** 0

### R2_score_range

- **Description:** Set score to NA if outside [0, 10].
- **rows_before:** 18818
- **rows_after:** 18818
- **rows_affected:** 0

### R3_year_range

- **Description:** Set aired_from_year/season_year to NA if outside [1917, 2026].
- **rows_before:** 18818
- **rows_after:** 18818
- **rows_affected:** 0

### R4_end_before_start

- **Description:** Clear end_date/aired_to_year when end < start.
- **rows_before:** 18818
- **rows_after:** 18818
- **rows_affected:** 5

### R5_source_normalize

- **Description:** Normalize source label casing/aliases (Web manga, Light novel, etc.).
- **rows_before:** 18818
- **rows_after:** 18818

### R6_analysis_flags

- **Description:** Add flag_unfetched_jikan, flag_isekai, flag_analysis_year, flag_tv, flag_core_av. Unfetched rows retained.
- **rows_before:** 18818
- **rows_after:** 18818
- **unfetched_n:** 156
- **isekai_n:** 794

### R7_require_id_name

- **Description:** Require non-null animeID and name.
- **rows_before:** 18818
- **rows_after:** 18813
- **rows_removed:** 5

## Profile (raw)

- Rows: **18,818**; cols: **41**
- `jikan_fetched` True/False: **18,662** / **156**
- Duplicate `animeID`: **0**; duplicate casefold `name`: **8**
- Isekai-tagged rows (any list field): **794**

### Missingness (raw rates)

| Field | Missing rate |
|-------|-------------:|
| `aired_from_year` | 28.1% |
| `season_year` | 7.3% |
| `season` | 43.1% |
| `type` | 0.6% |
| `source` | 0.8% |
| `genre` | 8.8% |
| `themes` | 22.9% |
| `score` | 0.5% |
| `members` | 0.1% |
| `studio` | 20.1% |
| `start_date` | 0.5% |

### Type mix (raw)

| Type | N |
|------|--:|
| TV | 6,095 |
| OVA | 4,044 |
| Movie | 3,189 |
| ONA | 1,917 |
| Special | 1,527 |
| Music | 1,003 |
| TV Special | 586 |
| CM | 247 |
| (missing) | 122 |
| PV | 86 |
| Unknown | 2 |

## Anomalies flagged

- Scores outside [0,10]: lt0=0, gt10=0
- Years outside [1917,2026]: lt=0, gt=0
- end_date < start_date: 5
- Tenrai vs AniList score pairs: n=11,777, MAE=0.370, |Δ|>1: 608

## Headline stats — old article vs raw-new vs clean-new

| Stat | Old article | Raw new (TV) | Clean new (TV, 95% bootstrap CI) |
|------|-------------|--------------|----------------------------------|
| isekai share 2015 (TV) | 0.9% | 2.2% [0.4%–4.3%] (n=230) | 2.2% [0.4%–4.3%] (n=230) |
| isekai share 2021 (TV) | 20.4% | 20.4% [15.2%–26.1%] (n=211) | 20.4% [15.2%–25.6%] (n=211) |
| isekai share 2024 (TV) | 17.7% | 18.1% [13.7%–23.0%] (n=248) | 18.1% [13.7%–23.0%] (n=248) |
| manga share 2024 (TV) | 34.7% | 34.7% [29.0%–41.1%] (n=248) | 34.7% [29.0%–40.7%] (n=248) |
| web manga share 2024 (TV) | 12.5% | 12.5% [8.5%–16.5%] (n=248) | 12.5% [8.5%–16.5%] (n=248) |
| manga+web manga 2024 (TV) | 47.2% | 47.2% [41.1%–53.2%] (n=248) | 47.2% [41.1%–53.2%] (n=248) |
| LN / Original median members (TV) | 32.0× | 27.51× | 27.51× |
| manga share score≥8.0 (TV) | 17.0% | 14.8% | 14.8% |

Bootstrap: 2000 resamples, seed `20261011`, percentile 95% CI.

## Sensitivity (isekai share 2024)

- `isekai_2024_tv_only`: 18.1% [13.7%–23.0%] (n=248)
- `isekai_2024_core_av`: 11.7% [8.6%–14.5%] (n=429)
- `isekai_2024_excl_music_special`: 11.4% [8.7%–14.4%] (n=439)
- `isekai_2024_all_types`: 11.1% [8.2%–14.0%] (n=450)
- `isekai_2024_tv_including_unfetched`: 18.1% [13.7%–23.4%] (n=248)
- `isekai_2024_tv_excluding_unfetched`: 18.1% [13.7%–23.0%] (n=248)

## Inter-source validation (n=200)

{
  "sample_n": 200,
  "seed": 20261011,
  "universe": "rows with jikan_fetched & anilist_fetched",
  "universe_n": 11804,
  "score_agreement_within_0_5": {
    "agree": 146,
    "comparable": 200,
    "rate": 0.73
  },
  "year_season_year_match": {
    "agree": 119,
    "sample_n": 200,
    "rate": 0.595
  },
  "note": "Cross-check uses co-present Tenrai/Jikan fields vs AniList fields already joined on idMal (offline validation; no live API re-fetch). Score: |MAL - AniList/10| \u2264 0.5."
}

## Outputs

- `data/anime/anime_2026-10-11_clean.csv`
- `data/anime/anime_2026-10-11_clean.parquet`
- `data/anime/audit_outputs/`
