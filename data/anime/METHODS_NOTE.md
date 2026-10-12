# METHODS_NOTE — Artometrics Anime dataset (2026-10-11)

## 1. Purpose and framing

This note documents the refresh from the 2019-04-23 TidyTuesday MyAnimeList export to the 2026-10-11 Tenrai + AniList snapshot, and the reproducible cleaning pass that produces `anime_2026-10-11_clean.*`. The editorial frame is **what changed when we fixed / extended the data**, not a silent rewrite of the published article.

## 2. Data sources and citations

| Source | Role | Access / version |
|--------|------|------------------|
| TidyTuesday `tidy_anime.csv` (Kaggle MyAnimeList scrape by Tam Nguyen) | Baseline catalog | Snapshot **2019-04-23**; SHA-256 `5ea3a14492b5c559c728af0c7ec57b81c919d0efa4d381e54b0f7cde9934a1c2`; <https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-04-23> |
| **Tenrai API** (`api.tenrai.org`) | Jikan-compatible MyAnimeList mirror for title metadata (score, members, genres, themes, studios, etc.) | Accessed **2026-10-12**. Public Jikan v4 (`api.jikan.moe`) was discontinued **2026-10-01**; field names retain the Jikan v4 schema. |
| **AniList GraphQL API** | Enrichment via `idMal` (tags, meanScore, popularity, trending, streaming links) | Docs: <https://anilist.gitbook.io/anilist-apiv2-docs/>; accessed during refresh culminating in snapshot **2026-10-11** (pipeline run logged 2026-10-12). |
| MyAnimeList | Upstream of Tenrai/Jikan fields | User-generated scores and lists; subject to ongoing revision |

**Pipeline code:** `scripts/anime-data/refresh.py` (ingest), `scripts/anime-data/clean_audit.py` (audit + clean; seed `20261011`).

## 3. Unit of analysis and snapshot size

- **Unit:** one row per MyAnimeList `animeID`.
- **Raw snapshot:** **18,818** rows × 41 columns (`anime_2026-10-11.csv`).
- **Tenrai/Jikan fetch success:** **18,662** fetched; **156** unfetched.
- **Baseline:** 13,631 titles (2019-04-23); **+5,187** new MAL ids in the refresh (see `CHANGELOG_2019-04-23_to_2026-10-11.md`).

## 4. Inclusion and exclusion criteria (with flow counts)

See also `CLEANING_LOG.md` and `audit_outputs/inclusion_flow.csv`.

| Step | N | Criterion |
|------|--:|-----------|
| A_raw_snapshot | 18,818 | Rows in anime_2026-10-11.csv |
| B_after_dedupe | 18,818 | After R1 dedupe |
| C_clean_all_types | 18,813 | Clean file (all types; flags only) |
| D_tv_only | 6,095 | Inclusion: type==TV (article narrative frame) |
| E_tv_fetched | 6,094 | TV ∩ jikan_fetched |
| F_tv_scored | 6,073 | TV with non-null score |
| G_core_av | 15,245 | Sensitivity: TV/Movie/ONA/OVA |
| H_excl_music_special | 16,283 | Sensitivity: drop Music+Special |

**Primary analysis set for article-parallel headline shares:** TV titles (`type == "TV"`), year from `aired_from_year` (fallback `season_year`).

**Isekai:** tag match for “isekai” in `themes` ∪ `genre` ∪ `anilist_tags` ∪ `demographics`.

**Sensitivity sets:** (i) TV/Movie/ONA/OVA only; (ii) exclude Music + Special; (iii) TV including vs excluding unfetched rows.

## 5. Cleaning (reproducible)

One command:

```bash
python3 scripts/anime-data/clean_audit.py
```

Rules R1–R7 are enumerated with before/after counts in `CLEANING_LOG.md`. Outputs: `anime_2026-10-11_clean.csv` / `.parquet`.

**Seed:** `20261011` (NumPy Generator + Python `random`).

## 6. Data dictionary / codebook

Canonical column definitions: `data/anime/DATA_DICTIONARY.md`. Clean file adds:

| Column | Type | Definition |
|--------|------|------------|
| `flag_unfetched_jikan` | bool | `not jikan_fetched` |
| `flag_isekai` | bool | Isekai tag rule above |
| `flag_analysis_year` | float | Analysis year |
| `flag_tv` | bool | `type == "TV"` |
| `flag_core_av` | bool | type ∈ {TV, Movie, ONA, OVA} |

## 7. Missing-data analysis

Formal Little’s MCAR test was **not** estimated (high-dimensional mixed types). Instead:

1. Profile missing rates for key fields (see CLEANING_LOG).
2. Compare score-missing vs score-present rows on mean year, share TV, median members, share unfetched (`audit_outputs/missing_analysis.json`).
3. Contingency χ² for `unfetched × score_missing`.

**Interpretation:** fetch failure is a structural reason for thin metadata; treat unfetched rows as **observed missingness related to measurement**, and report fetched-only sensitivity beside all-row TV estimates.

## 8. Uncertainty

Bootstrap **95% percentile CIs** (B = 2000, seed `20261011`) for isekai and source shares by year. Point estimates are sample proportions within the stated inclusion set.

## 9. Inter-source validation

Random sample of **n = 200** rows with both `jikan_fetched` and `anilist_fetched` (seed `20261011`).

- Score agreement (|MAL − AniList meanScore/10| ≤ 0.5): **146 / 200** = **73.0%**
- `aired_from_year` == `season_year`: **59.5%**

This is an **offline** cross-check of joined fields (no live re-fetch at audit time). Disagreement can reflect scale calibration, update timing, or mapping error.

## 10. Headline statistic reconciliation

| Stat | Old article | Raw new (TV) | Clean new (TV) |
|------|-------------|--------------|----------------|
| isekai share 2015 (TV) | 0.9% | 2.2% [0.4%–4.3%] (n=230) | 2.2% [0.4%–4.3%] (n=230) |
| isekai share 2021 (TV) | 20.4% | 20.4% [15.2%–26.1%] (n=211) | 20.4% [15.2%–25.6%] (n=211) |
| isekai share 2024 (TV) | 17.7% | 18.1% [13.7%–23.0%] (n=248) | 18.1% [13.7%–23.0%] (n=248) |
| manga share 2024 (TV) | 34.7% | 34.7% [29.0%–41.1%] (n=248) | 34.7% [29.0%–40.7%] (n=248) |
| web manga share 2024 (TV) | 12.5% | 12.5% [8.5%–16.5%] (n=248) | 12.5% [8.5%–16.5%] (n=248) |
| manga+web manga 2024 (TV) | 47.2% | 47.2% [41.1%–53.2%] (n=248) | 47.2% [41.1%–53.2%] (n=248) |
| LN / Original median members (TV) | 32.0× | 27.51× | 27.51× |
| manga share score≥8.0 (TV) | 17.0% | 14.8% | 14.8% |

Full machine-readable table: `audit_outputs/stats_old_vs_raw_vs_clean.csv`.

**Reading the gap:** Old article figures for isekai (2015/2021/2024) and 2024 manga/web-manga mixes were exploratory claims tied to the refresh narrative; recompute on the full TV catalog with an explicit tag rule. The **32×** light-novel vs original median members and **17.0%** manga ≥8.0 figures in the published piece used the earlier scored-TV analysis frame (early-2019 snapshot language remains in article prose until a separate copy update).

## 11. Limitations

1. **MAL popularity is not a probability sample** of anime viewers; members/scores are platform-selected.
2. **Tenrai is a mirror** of MAL; outages or drift vs mal_id can leave `jikan_fetched=False` (156 rows).
3. **AniList join is many-to-none** via `idMal`; tags (including Isekai) may be denser on AniList than MAL themes.
4. **Isekai operationalization** is string match on tags — not a hand-coded genre ontology; false positives/negatives possible.
5. **Year assignment** uses air start / season year; calendar-year “share of 2024 titles” is sensitive to unfinished airing and missing dates.
6. **Scores drift over time**; October 2026 scores are not comparable as causal outcomes to 2019 scores without a panel model.
7. **Bootstrap CIs** ignore clustering by studio/franchise; they understate dependence.
8. **No live AniList re-audit** of the n=200 sample at clean time — validation uses already-fetched fields.
9. Cleaning **does not impute** scores or sources; it flags and nulls impossible values only.

## 12. Reproducibility checklist

- [x] Fixed seed (`20261011`)
- [x] Raw file hash recorded
- [x] Single entry-point script
- [x] Environment versions logged
- [x] Flow counts + sensitivity + bootstrap CIs
- [x] Clean artifacts written beside raw snapshot

*Generated by `scripts/anime-data/clean_audit.py` on 2026-10-12T19:47:34Z.*
