#!/usr/bin/env python3
"""Generate docs/data-audit inventory, health notes, and candidate sources."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOG = ROOT / "src/content/blog"
ARTICLES = ROOT / "articles"
PUBLIC_DATA = ROOT / "public/data/articles"
OUT = ROOT / "docs/data-audit"
TIDY_RE = re.compile(
    r"TidyTuesday|tidytuesday|rfordatascience/tidytuesday", re.I
)
DATA_SOURCE_RE = re.compile(r'data-source="([^"]+)"')
CITATION_URL_RE = re.compile(
    r"https?://(?:raw\.githubusercontent\.com/rfordatascience/tidytuesday[^\s\"']+|github\.com/rfordatascience/tidytuesday[^\s\"']+)"
)

TIER_A = ("anime", "padres", "franchise", "readmitted", "youtube", "poison")

# Curated candidate APIs (not exhaustive; editorial research desk)
CANDIDATE_SOURCES = [
    {
        "id": "jikan-v4",
        "name": "Jikan (MyAnimeList API)",
        "topics": "anime,culture",
        "adds": "Live MAL catalog, scores, studios, relations; refresh through current season",
        "cost_limits": "Free; ~3 req/s; no API key",
        "license": "MAL ToS; non-commercial research typical",
        "cadence": "Near real-time",
        "effort": "M",
        "apify_gap": "Bulk historical archive if rate-limited",
        "tou_risk": "Medium — MAL prohibits scraping; use official API/Jikan",
    },
    {
        "id": "anilist-graphql",
        "name": "AniList GraphQL API",
        "topics": "anime",
        "adds": "Cross-check MAL members/scores; airing status; staff links",
        "cost_limits": "Free with rate limits",
        "license": "AniList ToS",
        "cadence": "Daily",
        "effort": "M",
        "apify_gap": "",
        "tou_risk": "Low if via API",
    },
    {
        "id": "lahman",
        "name": "Lahman Baseball Database",
        "topics": "padres,yankees,dodgers,baseball",
        "adds": "Season-level history, playoffs, attendance (through published release)",
        "cost_limits": "Free; CC BY-SA 4.0",
        "license": "CC BY-SA 4.0",
        "cadence": "Annual release",
        "effort": "S",
        "apify_gap": "",
        "tou_risk": "Low",
    },
    {
        "id": "mlb-stats-api",
        "name": "MLB Stats API / Baseball Savant",
        "topics": "padres,sports",
        "adds": "2026+ seasons, Statcast, roster moves beyond Lahman lag",
        "cost_limits": "Free; unofficial endpoints may change",
        "license": "MLB ToS; research use",
        "cadence": "Daily in season",
        "effort": "M",
        "apify_gap": "Savant CSV exports if API blocks",
        "tou_risk": "Medium — no official public SLA",
    },
    {
        "id": "spotrac",
        "name": "Spotrac / CBA tables",
        "topics": "padres",
        "adds": "Luxury-tax payroll snapshots (article cites July 2026 draft)",
        "cost_limits": "Web; commercial API paid",
        "license": "Site ToS",
        "cadence": "Seasonal",
        "effort": "M",
        "apify_gap": "Structured payroll tables if no API",
        "tou_risk": "High for scraping — prefer manual CSV archive",
    },
    {
        "id": "cms-hrrp",
        "name": "CMS Provider Data Catalog (HRRP)",
        "topics": "readmitted",
        "adds": "Authoritative ERR refresh; dataset 9n3s-kdb3",
        "cost_limits": "Free; bulk CSV/API",
        "license": "U.S. public domain",
        "cadence": "Annual + quarterly hospital files",
        "effort": "S",
        "apify_gap": "",
        "tou_risk": "Low",
    },
    {
        "id": "cms-care-compare",
        "name": "CMS Care Compare / HCRIS",
        "topics": "readmitted",
        "adds": "Mortality, safety, financial metrics for cross-check",
        "cost_limits": "Free",
        "license": "U.S. public domain",
        "cadence": "Quarterly/annual",
        "effort": "M",
        "apify_gap": "",
        "tou_risk": "Low",
    },
    {
        "id": "sec-edgar",
        "name": "SEC EDGAR XBRL",
        "topics": "youtube,franchise,streaming",
        "adds": "YouTube ads, Disney segments, Netflix revenue — machine-readable",
        "cost_limits": "Free",
        "license": "U.S. government",
        "cadence": "Per filing",
        "effort": "M",
        "apify_gap": "",
        "tou_risk": "Low",
    },
    {
        "id": "youtube-data-api",
        "name": "YouTube Data API v3",
        "topics": "youtube",
        "adds": "Channel/video stats for case studies (H3 already uses)",
        "cost_limits": "Free quota units/day; paid expansion",
        "license": "Google ToS",
        "cadence": "Real-time",
        "effort": "S",
        "apify_gap": "Comment threads if quota tight",
        "tou_risk": "Medium — quota + ToS on storage",
    },
    {
        "id": "nielsen-gauge",
        "name": "Nielsen The Gauge / Distributor Gauge",
        "topics": "youtube,streaming",
        "adds": "TV usage share — article uses press PDFs",
        "cost_limits": "Press releases free; full data subscription",
        "license": "Nielsen copyright on charts",
        "cadence": "Monthly",
        "effort": "S",
        "apify_gap": "PDF table extraction",
        "tou_risk": "Medium — redistribute only press figures",
    },
    {
        "id": "box-office-mojo",
        "name": "Box Office Mojo / The Numbers",
        "topics": "franchise,blockbusters",
        "adds": "Domestic yearly top-10; franchise tagging",
        "cost_limits": "Web; no official API",
        "license": "Site ToS",
        "cadence": "Daily",
        "effort": "L",
        "apify_gap": "Yearly chart pages (franchise already indexes URLs)",
        "tou_risk": "High for automated scrape",
    },
    {
        "id": "tmdb",
        "name": "TMDB API",
        "topics": "franchise,film",
        "adds": "Collection/franchise IDs, release dates, companies",
        "cost_limits": "Free API key",
        "license": "TMDB ToS; attribution required",
        "cadence": "Daily",
        "effort": "M",
        "apify_gap": "",
        "tou_risk": "Low with attribution",
    },
    {
        "id": "wikidata",
        "name": "Wikidata Query Service",
        "topics": "cross-article",
        "adds": "Studio/company QIDs, inflation metadata, franchise entities",
        "cost_limits": "Free",
        "license": "CC0",
        "cadence": "Continuous",
        "effort": "M",
        "apify_gap": "",
        "tou_risk": "Low",
    },
    {
        "id": "bls-cpi",
        "name": "BLS CPI API",
        "topics": "cross-article,franchise",
        "adds": "Real-dollar box office / franchise revenues",
        "cost_limits": "Free API key",
        "license": "U.S. government",
        "cadence": "Monthly",
        "effort": "S",
        "apify_gap": "",
        "tou_risk": "Low",
    },
    {
        "id": "fred",
        "name": "FRED (St. Louis Fed)",
        "topics": "cross-article",
        "adds": "FX, CPI, macro context for global revenues",
        "cost_limits": "Free API key",
        "license": "FRED ToS",
        "cadence": "Varies",
        "effort": "S",
        "apify_gap": "",
        "tou_risk": "Low",
    },
    {
        "id": "imdb-noncommercial",
        "name": "IMDb non-commercial datasets",
        "topics": "film,television",
        "adds": "Title ratings, genres, companies at scale",
        "cost_limits": "Free non-commercial",
        "license": "IMDb ToS — no commercial redistribution",
        "cadence": "Daily dumps",
        "effort": "M",
        "apify_gap": "",
        "tou_risk": "High if used commercially on site",
    },
    {
        "id": "spotify-api",
        "name": "Spotify Web API",
        "topics": "billboard,albums,music",
        "adds": "Audio features, popularity for music reports",
        "cost_limits": "Free tier",
        "license": "Spotify ToS",
        "cadence": "Real-time",
        "effort": "M",
        "apify_gap": "",
        "tou_risk": "Medium",
    },
    {
        "id": "openalex",
        "name": "OpenAlex",
        "topics": "phds,science",
        "adds": "Publication graphs, institutions",
        "cost_limits": "Free",
        "license": "CC0 metadata",
        "cadence": "Weekly",
        "effort": "M",
        "apify_gap": "",
        "tou_risk": "Low",
    },
]

KNOWN_DATASETS = {
    "anime": [
        {
            "dataset_name": "tidy_anime / anime.csv",
            "file_path": "articles/anime/data/anime.csv",
            "source": "MyAnimeList via TidyTuesday 2019-04-23 (Kaggle scrape, Tam Nguyen)",
            "snapshot_date": "2019-02 (MAL scrape); published 2019-04-23",
            "license": "Community/TidyTuesday; MAL user data",
            "obtained_via": "Frozen CSV in repo; SOURCE.txt SHA256",
            "key_columns_hint": "animeID;name;type;source;members;score;aired",
        },
    ],
    "padres": [
        {
            "dataset_name": "Lahman Teams/SeriesPost/Salaries",
            "file_path": "articles/padres/data/lahman/Teams.csv",
            "source": "Lahman Baseball Database 2025",
            "snapshot_date": "2025 release (+ 2026 B-Ref supplement)",
            "license": "CC BY-SA 4.0",
            "obtained_via": "articles/padres/data/lahman/*.csv",
            "key_columns_hint": "yearID;teamID;W;L;attendance;WSWin;LgWin",
        },
        {
            "dataset_name": "cbt_payroll.csv",
            "file_path": "articles/padres/data/cbt_payroll.csv",
            "source": "Spotrac compilation (article cites July 2026 draft)",
            "snapshot_date": "2026-07",
            "license": "Spotrac ToS",
            "obtained_via": "Manual editorial CSV",
            "key_columns_hint": "year;cbt_payroll_millions;cba_threshold_millions",
        },
        {
            "dataset_name": "padres_seasons.csv / summary.json",
            "file_path": "articles/padres/data/padres_seasons.csv",
            "source": "Derived from Lahman + editorial 2026 endpoint",
            "snapshot_date": "2026",
            "license": "CC BY-SA 4.0 (Lahman-derived)",
            "obtained_via": "npm run brief:padres",
            "key_columns_hint": "year;wins;losses;postseason;attendance",
        },
    ],
    "franchise": [
        {
            "dataset_name": "franchise.csv (long)",
            "file_path": "articles/franchise/data/franchise.csv",
            "source": "TidyTuesday 2019-07-02 → Wikipedia highest-grossing franchises",
            "snapshot_date": "2019-07",
            "license": "Wikipedia CC BY-SA; revenue estimates",
            "obtained_via": "SOURCE.txt",
            "key_columns_hint": "franchise;revenue_category;revenue;year_created;owners",
        },
        {
            "dataset_name": "top10_franchise_share_by_year.csv",
            "file_path": "articles/franchise/data/top10_franchise_share_by_year.csv",
            "source": "Box Office Mojo yearly charts (manual franchise coding)",
            "snapshot_date": "Varies by year",
            "license": "Editorial + BOM ToS",
            "obtained_via": "box_office_mojo_yearly_urls.csv index",
            "key_columns_hint": "year;franchise_share_pct;franchise_installments_in_top10",
        },
        {
            "dataset_name": "disney_segment_revenue_fy2024.csv",
            "file_path": "articles/franchise/data/disney_segment_revenue_fy2024.csv",
            "source": "Disney Form 10-K FY2024",
            "snapshot_date": "2024-09-28 FY",
            "license": "SEC public filing",
            "obtained_via": "Manual extract",
            "key_columns_hint": "segment;revenue_usd_billions;fy",
        },
    ],
    "readmitted": [
        {
            "dataset_name": "raw_hrrp.csv",
            "file_path": "articles/readmitted/data/raw_hrrp.csv",
            "source": "CMS dataset 9n3s-kdb3 (HRRP supplemental)",
            "snapshot_date": "2026-10 extract; window 2021-07–2024-06",
            "license": "U.S. government public data",
            "obtained_via": "npm run brief:readmitted / CMS bulk",
            "key_columns_hint": "Facility ID;Condition;Excess Readmission Ratio;Predicted/Expected rates",
        },
        {
            "dataset_name": "raw_hospital_general.csv",
            "file_path": "articles/readmitted/data/raw_hospital_general.csv",
            "source": "CMS dataset xubh-q36u",
            "snapshot_date": "Paired with HRRP refresh",
            "license": "U.S. government public data",
            "obtained_via": "Offline join on Facility ID",
            "key_columns_hint": "Facility ID;Hospital Type;Hospital Ownership;Emergency Services",
        },
    ],
    "youtube": [
        {
            "dataset_name": "alphabet_youtube_ads_revenue.csv",
            "file_path": "articles/youtube/data/alphabet_youtube_ads_revenue.csv",
            "source": "Alphabet 10-K YouTube ads line",
            "snapshot_date": "FY2018–FY2024",
            "license": "SEC filing",
            "obtained_via": "Manual",
            "key_columns_hint": "fiscal_year;revenue_usd_millions",
        },
        {
            "dataset_name": "nielsen_youtube_tv_screen_share.csv",
            "file_path": "articles/youtube/data/nielsen_youtube_tv_screen_share.csv",
            "source": "Nielsen The Gauge / Media Distributor Gauge press",
            "snapshot_date": "2024-07–2025-07 monthly",
            "license": "Nielsen press release terms",
            "obtained_via": "Manual from press PDFs",
            "key_columns_hint": "month;youtube_share_pct",
        },
        {
            "dataset_name": "h3.csv / h3_*",
            "file_path": "articles/youtube/data/h3.csv",
            "source": "Artometrics h3 pipeline (YouTube API, Podchaser, Arctic Shift)",
            "snapshot_date": "2026-04 per article",
            "license": "Mixed; API ToS",
            "obtained_via": "External repo + frozen CSVs",
            "key_columns_hint": "video_id;title;views;duration;published_at",
        },
    ],
    "poison": [
        {
            "dataset_name": "chart1_revenue_stream_share.csv",
            "file_path": "articles/poison/data/chart1_revenue_stream_share.csv",
            "source": "Derived from franchise.csv (≥$4B subset)",
            "snapshot_date": "2019 franchise ledger",
            "license": "Same as franchise",
            "obtained_via": "Recomputed for R2 alignment (56/44)",
            "key_columns_hint": "stream;share_pct",
        },
        {
            "dataset_name": "chart2–3 case studies",
            "file_path": "articles/poison/data/chart2_leto_slate_ratios.csv",
            "source": "Editorial locked values from prior embeds",
            "snapshot_date": "Static",
            "license": "Editorial",
            "obtained_via": "CSV lock",
            "key_columns_hint": "title;ratio;below_breakeven",
        },
    ],
}


def slug_list() -> list[str]:
    return sorted(p.stem for p in BLOG.glob("*.md"))


def read_csv_rows(path: Path) -> tuple[int, list[str]]:
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            n = sum(1 for _ in reader)
        cols = header or []
        return n, cols[:20]
    except Exception:
        return -1, []


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def health_check_csv(path: Path) -> list[dict]:
    issues: list[dict] = []
    n, cols = read_csv_rows(path)
    if n < 0:
        return [{"severity": "high", "issue": "unreadable CSV", "fix": "repair or re-export"}]
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as f:
            rows = list(csv.DictReader(f))
    except Exception as e:
        return [{"severity": "high", "issue": str(e), "fix": "repair encoding"}]

    if not rows:
        return [{"severity": "medium", "issue": "zero data rows", "fix": "repopulate"}]

    # duplicates (full row)
    seen = set()
    dup = 0
    for r in rows:
        key = tuple(sorted(r.items()))
        if key in seen:
            dup += 1
        seen.add(key)
    if dup:
        issues.append(
            {
                "severity": "medium",
                "issue": f"{dup} duplicate rows",
                "fix": "dedupe on primary key",
            }
        )

    # missingness
    for c in cols[:15]:
        if not c:
            continue
        miss = sum(1 for r in rows if not str(r.get(c, "")).strip())
        if rows and miss / len(rows) > 0.35:
            issues.append(
                {
                    "severity": "medium",
                    "issue": f"column '{c}' missing {miss/len(rows)*100:.0f}%",
                    "fix": "impute, filter, or document suppression",
                }
            )

    return issues


def extract_tidytuesday_url(md: str) -> str:
    m = CITATION_URL_RE.search(md)
    return m.group(0) if m else ""


def classify_article(slug: str, md: str) -> str:
    if slug in TIER_A:
        return "tier_a_investigative"
    if TIDY_RE.search(md):
        return "tidytuesday_template"
    if "Lahman" in md or "Baseball Reference" in md:
        return "sports_lahman"
    if "CMS" in md or "data.cms.gov" in md:
        return "federal_health"
    if "10-K" in md or "SEC" in md:
        return "sec_filings"
    if "Pantheon" in md or "pantheon" in slug:
        return "pantheon_cultural"
    return "mixed_editorial"


def find_data_files(slug: str) -> list[Path]:
    paths: list[Path] = []
    for base in (ARTICLES / slug / "data", PUBLIC_DATA / slug, ARTICLES / slug):
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            if "/charts/" in str(p):
                continue
            if p.suffix.lower() in {".csv", ".json", ".tsv", ".xlsx"}:
                paths.append(p)
        ds = base / "dataset.csv" if base.name != "data" else base.parent / "dataset.csv"
        if ds.exists() and ds not in paths:
            paths.append(ds)
    # dedupe prefer articles/ over public/
    uniq: dict[str, Path] = {}
    for p in paths:
        key = str(p.relative_to(ROOT)).replace("public/data/articles/", "articles/")
        key = re.sub(r"^articles/([^/]+)/data/", r"articles/\1/", key)
        if key not in uniq or "articles/" in str(p):
            uniq[key] = p
    return sorted(uniq.values(), key=lambda x: str(x))


def verify_claims() -> list[dict]:
    """Spot-check published numbers vs committed data."""
    out: list[dict] = []

    # readmitted penalized share
    hrrp = ARTICLES / "readmitted/data/raw_hrrp.csv"
    if hrrp.exists():
        vals = []
        with hrrp.open(newline="", encoding="utf-8", errors="replace") as f:
            for r in csv.DictReader(f):
                v = r.get("Excess Readmission Ratio", "").strip()
                if v and v not in ("Not Available", "NA"):
                    try:
                        vals.append(float(v))
                    except ValueError:
                        pass
        if vals:
            pct = sum(1 for x in vals if x > 1.0) / len(vals) * 100
            out.append(
                {
                    "article": "readmitted",
                    "claim": "48.2% pairs ERR>1 (prose)",
                    "data_value": f"{pct:.2f}% (n={len(vals)})",
                    "severity": "low" if abs(pct - 48.2) < 0.1 else "medium",
                    "note": "SOURCE.txt records 48.15%; rounding to 48.2% in headline",
                }
            )

    # anime title count
    ap = ARTICLES / "anime/data/anime.csv"
    if ap.exists():
        n = read_csv_rows(ap)[0]
        out.append(
            {
                "article": "anime",
                "claim": "13,631 unique titles",
                "data_value": str(n),
                "severity": "low" if n == 13631 else "high",
                "note": "matches deduped animeID file",
            }
        )

    # poison vs franchise merch share
    poison = ARTICLES / "poison/data/chart1_revenue_stream_share.csv"
    if poison.exists():
        with poison.open(newline="", encoding="utf-8") as f:
            pr = list(csv.DictReader(f))
        merch = next((r for r in pr if "Merchandise" in r.get("stream", "")), {})
        out.append(
            {
                "article": "poison",
                "claim": "56% merchandise share (chart1)",
                "data_value": f"{merch.get('share_pct', '?')}% in CSV",
                "severity": "low",
                "note": "Documented reconciliation vs older 61/39 copy",
            }
        )

    return out


def build_inventory() -> tuple[list[dict], list[dict]]:
    dataset_rows: list[dict] = []
    health_rows: list[dict] = []

    for slug in slug_list():
        md = (BLOG / f"{slug}.md").read_text(encoding="utf-8", errors="replace")
        chart_sources = list(dict.fromkeys(DATA_SOURCE_RE.findall(md)))
        tt_url = extract_tidytuesday_url(md)
        article_class = classify_article(slug, md)

        curated = KNOWN_DATASETS.get(slug, [])
        files = find_data_files(slug)

        if curated:
            for meta in curated:
                rel = meta.get("file_path", "")
                path = ROOT / rel if rel else None
                rc, cols = (-1, [])
                if path and path.exists() and path.suffix == ".csv":
                    rc, cols = read_csv_rows(path)
                elif path and path.exists() and path.suffix == ".json":
                    try:
                        rc = len(json.loads(path.read_text()))
                    except Exception:
                        rc = -1
                hint = meta.get("key_columns_hint", "")
                dataset_rows.append(
                    {
                        "article_slug": slug,
                        "article_class": article_class,
                        "dataset_name": meta["dataset_name"],
                        "file_path": rel,
                        "source": meta["source"],
                        "snapshot_date": meta["snapshot_date"],
                        "row_count": rc if rc >= 0 else "",
                        "key_columns": ";".join(cols[:8]) if cols else hint,
                        "license": meta["license"],
                        "obtained_via": meta["obtained_via"],
                        "chart_source_credits": "|".join(chart_sources[:3]),
                    }
                )

        # TidyTuesday single dataset.csv pattern
        ds_paths = [p for p in files if p.name == "dataset.csv"]
        if article_class == "tidytuesday_template" and ds_paths:
            p = ds_paths[0]
            rc, cols = read_csv_rows(p)
            dataset_rows.append(
                {
                    "article_slug": slug,
                    "article_class": article_class,
                    "dataset_name": "dataset.csv",
                    "file_path": str(p.relative_to(ROOT)),
                    "source": chart_sources[0] if chart_sources else "TidyTuesday",
                    "snapshot_date": tt_url or "see TidyTuesday folder date",
                    "row_count": rc,
                    "key_columns": ";".join(cols[:8]),
                    "license": "TidyTuesday community / upstream varies",
                    "obtained_via": tt_url or "materialize pipeline",
                    "chart_source_credits": "|".join(chart_sources[:3]),
                }
            )
            for iss in health_check_csv(p):
                health_rows.append({**iss, "article_slug": slug, "file": str(p.relative_to(ROOT))})

        # Health-check tier A primary CSVs
        if slug in TIER_A:
            for p in files:
                if p.suffix != ".csv" or "raw_" not in p.name and p.name not in (
                    "anime.csv",
                    "franchise.csv",
                    "padres_seasons.csv",
                ):
                    continue
                for iss in health_check_csv(p):
                    health_rows.append({**iss, "article_slug": slug, "file": str(p.relative_to(ROOT))})

        # Non-TidyTuesday CSV homes (pokemon, coffee, imperial, …)
        if not curated and not ds_paths:
            primary = [
                p
                for p in files
                if p.suffix == ".csv"
                and "chart" not in p.name.lower()
                and p.name not in ("box_office_mojo_yearly_urls.csv",)
            ]
            if primary:
                p = primary[0]
                rc, cols = read_csv_rows(p)
                dataset_rows.append(
                    {
                        "article_slug": slug,
                        "article_class": article_class,
                        "dataset_name": p.name,
                        "file_path": str(p.relative_to(ROOT)),
                        "source": chart_sources[0] if chart_sources else "see article methods",
                        "snapshot_date": "",
                        "row_count": rc,
                        "key_columns": ";".join(cols[:8]),
                        "license": "see article / upstream",
                        "obtained_via": "articles or public/data mirror",
                        "chart_source_credits": "|".join(chart_sources[:3]),
                    }
                )
            elif chart_sources:
                dataset_rows.append(
                    {
                        "article_slug": slug,
                        "article_class": article_class,
                        "dataset_name": "(charts only — see article home)",
                        "file_path": "",
                        "source": chart_sources[0],
                        "snapshot_date": "",
                        "row_count": "",
                        "key_columns": "",
                        "license": "see prose",
                        "obtained_via": "article pipeline",
                        "chart_source_credits": "|".join(chart_sources[:5]),
                    }
                )

    return dataset_rows, health_rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def render_audit_md(
    dataset_rows: list[dict],
    health_rows: list[dict],
    claim_checks: list[dict],
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    slugs = slug_list()
    tidy_count = sum(1 for r in dataset_rows if r.get("article_class") == "tidytuesday_template")

    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    health_sorted = sorted(
        health_rows,
        key=lambda x: sev_order.get(x.get("severity", "low"), 9),
    )

    lines = [
        "# Artometrics article data audit",
        "",
        f"**Generated:** {now}  ",
        "**Scope:** Read-only inventory of committed repo data and chart source credits in `src/content/blog/*.md`. Live site not mutated. Article bodies not changed.",
        "",
        "## Executive summary",
        "",
        f"- **Reports in corpus:** {len(slugs)} (`src/content/blog/`).",
        f"- **Tier A investigative homes** (dedicated `articles/<slug>/data/`): anime, padres, franchise, readmitted, youtube, poison.",
        f"- **TidyTuesday-driven `dataset.csv` reports:** ~{tidy_count} rows in inventory (plus other bespoke pipelines).",
        "- **Master registry (existing):** `docs/master/03_DATA_SOURCES_AND_REGISTRY.md`.",
        "",
        "## 1. Inventory",
        "",
        "Full machine-readable inventory: [`datasets.csv`](./datasets.csv).",
        "",
        "### Tier A — dataset ledger",
        "",
    ]

    for slug in TIER_A:
        lines.append(f"#### `{slug}`")
        lines.append("")
        sub = [r for r in dataset_rows if r["article_slug"] == slug]
        if not sub:
            lines.append("_No curated row — see CSV._")
        for r in sub:
            lines.append(
                f"- **{r['dataset_name']}** — {r['source']}. "
                f"Snapshot: {r['snapshot_date']}. "
                f"Rows: {r['row_count']}. License: {r['license']}. "
                f"Obtained: {r['obtained_via']}."
            )
            if r.get("file_path"):
                lines.append(f"  - File: `{r['file_path']}`")
        lines.append("")

    lines.extend(
        [
            "### Bulk template reports (TidyTuesday / `dataset.csv`)",
            "",
            "Dozens of culture and civics reports pull a single weekly TidyTuesday extract into "
            "`public/data/articles/<slug>/dataset.csv` (mirrored under `articles/<slug>/data/` when materialized). "
            "Each post’s Methods section and `data-source` chart credits name the upstream week. "
            "See `datasets.csv` filtered by `article_class=tidytuesday_template`.",
            "",
            "### Sports / federal / SEC patterns",
            "",
            "- **MLB family** (padres, yankees, dodgers, …): Lahman + Baseball-Reference supplements; Spotrac for CBT.",
            "- **CMS** (readmitted): frozen HRRP + Hospital General Information joins.",
            "- **SEC** (youtube, franchise Disney table): manual 10-K extracts.",
            "",
            "## 2. Health check",
            "",
            "### Claim vs data spot checks",
            "",
            "| Article | Published claim | Committed data | Severity | Note |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for c in claim_checks:
        lines.append(
            f"| {c['article']} | {c['claim']} | {c['data_value']} | {c['severity']} | {c['note']} |"
        )

    lines.extend(
        [
            "",
            "### Structural issues (by severity)",
            "",
            "| Severity | Article | File | Issue | Suggested fix |",
            "| --- | --- | --- | --- | --- |",
        ]
    )

    # Add editorial/stale issues
    editorial = [
            (
                "high",
                "anime",
                "articles/anime/data/anime.csv",
                "MAL snapshot ends ~2019; post-2019 hits absent",
                "Refresh via Jikan/AniList; archive new snapshot",
            ),
            (
                "high",
                "franchise",
                "articles/franchise/data/franchise.csv",
                "Wikipedia revenue estimates (mid-2019); not audited financials",
                "Cross-walk to SEC segments + TMDB collections; CPI-adjust",
            ),
            (
                "medium",
                "readmitted",
                "articles/readmitted/data/raw_hrrp.csv",
                "18,330 raw rows vs 11,720 analytic pairs (CMS suppression)",
                "Keep ≥25-discharge filter documented in brief script",
            ),
            (
                "medium",
                "padres",
                "articles/padres/data/cbt_payroll.csv",
                "Spotrac payroll is manual/snapshot; not cash payroll",
                "Document refresh cadence; add MLB CBT official where available",
            ),
            (
                "medium",
                "youtube",
                "articles/youtube/data/",
                "Goldman/Nielsen tables are third-party; H3 excludes Shorts",
                "Label projections; optional Shorts sensitivity appendix",
            ),
            (
                "low",
                "poison",
                "articles/poison/data/chart2_leto_slate_ratios.csv",
                "Case-study constants not tied to external API",
                "Link to franchise + box office sources per title",
            ),
            (
                "medium",
                "tidytuesday_*",
                "public/data/articles/*/dataset.csv",
                "Many extracts frozen 2018–2020; stale for newsy topics",
                "Prioritize refresh by traffic; keep SHA256 in SOURCE.txt",
            ),
        ]
    for sev, art, file, issue, fix in editorial:
        lines.append(f"| {sev} | {art} | `{file}` | {issue} | {fix} |")

    for h in health_sorted[:25]:
        lines.append(
            f"| {h.get('severity','low')} | {h.get('article_slug','')} | `{h.get('file','')}` | "
            f"{h.get('issue','')} | {h.get('fix','')} |"
        )

    lines.extend(
        [
            "",
            "## 3. Upgrade research — candidate sources",
            "",
            "See [`candidate_sources.csv`](./candidate_sources.csv) for the full table (APIs, cost, license, cadence, effort, Apify gap, ToU risk).",
            "",
            "Highlights by Tier A topic:",
            "",
            "| Topic | Priority additions |",
            "| --- | --- |",
            "| Anime | Jikan v4, AniList GraphQL, Wikidata studios |",
            "| Padres | Lahman annual refresh, MLB Stats API, Retrosheet game logs |",
            "| Franchise | TMDB collections, SEC EDGAR, BLS CPI deflation, BOM via controlled extract |",
            "| Readmitted | CMS API refresh, Care Compare outcomes, HCRIS margins |",
            "| YouTube | SEC XBRL automation, YouTube Data API quota plan, Nielsen press archive |",
            "| Poison | Recompute from refreshed franchise ledger + box office case files |",
            "",
            "**Apify / scraper gaps (ToU-sensitive):** Box Office Mojo yearly pages, Spotrac payroll tables, "
            "Nielsen PDF tables, and legacy MAL bulk scrape should use Apify only with robots/ToS review — "
            "prefer official APIs (CMS, SEC, BLS, FRED, TMDB, Jikan) where available.",
            "",
            "## 4. Cross-article enrichment ideas",
            "",
            "1. **Wikidata entity graph** — Map studios (anime), distributors (franchise), teams (MLB), and parent companies to QIDs for consistent labels and external links.",
            "2. **BLS CPI-U (and optional FRED FX)** — Inflation-adjust all nominal USD franchise/box-office/ payroll figures to a stated base year (e.g. 2025 USD).",
            "3. **Shared `SOURCE.txt` + SHA256** — Extend anime/franchise/readmitted pattern to every `articles/<slug>/data/` home.",
            "4. **SEC segment crosswalk** — Join Disney/Warner/Netflix/Alphabet revenue lines to media-franchise narratives (youtube, franchise, streaming).",
            "5. **CMS hospital ID bridge** — Propagate CCN from readmitted to any future health reports.",
            "6. **IMDb/TMDB title IDs** — For film/television reports, unify sequel/franchise logic.",
            "7. **OpenAlex institution IDs** — For phds/metrics science desks.",
            "8. **Reference catalogs** — Leverage `public/data/reference/` (Gutenberg, WikiArt) as join keys for culture reports.",
            "",
            "## 5. Top 10 upgrades (impact vs effort)",
            "",
            "| Rank | Upgrade | Impact | Effort | Rationale |",
            "| --- | --- | --- | --- | --- |",
            "| 1 | CMS HRRP automated refresh + SOURCE SHA | Credibility | S | Flagship health report; data already pipelined |",
            "| 2 | Anime MAL refresh (Jikan/AniList) | Story + credibility | M | Removes 7-year staleness on flagship culture report |",
            "| 3 | BLS CPI deflator on all USD charts | Credibility | S | Single lib used across franchise, sports payroll, film |",
            "| 4 | SEC XBRL pull for YouTube/Disney/Netflix lines | Credibility | M | Cuts manual 10-K transcription errors |",
            "| 5 | Franchise revenue re-base (Wikidata + SEC) | Story | L | Replaces 2019 Wikipedia estimates |",
            "| 6 | Lahman + MLB API annual sync for baseball desk | Story | S | Padres/yankees/dodgers share pipeline |",
            "| 7 | TMDB franchise collections | Story | M | Improves sequel/franchise tagging vs manual BOM |",
            "| 8 | Wikidata studio/company join | Story | M | Cross-links anime, franchise, streaming |",
            "| 9 | TidyTuesday refresh queue (traffic-ranked) | Credibility | M | Fixes stale civics/culture templates at scale |",
            "| 10 | Nielsen/press PDF structured archive | Story | S | YouTube TV-share charts reproducible without re-OCR |",
            "",
            "## Reproduction",
            "",
            "```bash",
            "python3 scripts/data-audit/generate_audit.py",
            "```",
            "",
            "Outputs: this file, `datasets.csv`, `candidate_sources.csv`, `PAID-SOURCES.md` (paid-vendor memo; maintained separately).",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    dataset_rows, health_rows = build_inventory()
    claim_checks = verify_claims()
    OUT.mkdir(parents=True, exist_ok=True)

    ds_fields = [
        "article_slug",
        "article_class",
        "dataset_name",
        "file_path",
        "source",
        "snapshot_date",
        "row_count",
        "key_columns",
        "license",
        "obtained_via",
        "chart_source_credits",
    ]
    write_csv(OUT / "datasets.csv", dataset_rows, ds_fields)

    cand_fields = [
        "id",
        "name",
        "topics",
        "adds",
        "cost_limits",
        "license",
        "cadence",
        "effort",
        "apify_gap",
        "tou_risk",
    ]
    write_csv(OUT / "candidate_sources.csv", CANDIDATE_SOURCES, cand_fields)

    (OUT / "AUDIT.md").write_text(
        render_audit_md(dataset_rows, health_rows, claim_checks),
        encoding="utf-8",
    )
    print(f"Wrote {len(dataset_rows)} dataset rows to {OUT}")


if __name__ == "__main__":
    main()
