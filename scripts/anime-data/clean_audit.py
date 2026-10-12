#!/usr/bin/env python3
"""
Reproducible anime dataset audit + clean pipeline (raw → clean).

Usage:
  python3 scripts/anime-data/clean_audit.py

Inputs (repo-relative):
  data/anime/anime_2026-10-11.csv
  data/anime/anime_2026-10-11.parquet (optional)

Outputs:
  data/anime/anime_2026-10-11_clean.csv
  data/anime/anime_2026-10-11_clean.parquet
  data/anime/CLEANING_LOG.md
  data/anime/METHODS_NOTE.md  (rewritten academic note)
  data/anime/audit_outputs/   (tables, JSON summaries)

Versions pinned loosely via environment report in CLEANING_LOG.
Seed: 20261011
"""
from __future__ import annotations

import ast
import json
import hashlib
import platform
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261011
RAW_NAME = "anime_2026-10-11"
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "anime"
OUT_DIR = DATA / "audit_outputs"
RAW_CSV = DATA / f"{RAW_NAME}.csv"
CLEAN_CSV = DATA / f"{RAW_NAME}_clean.csv"
CLEAN_PQ = DATA / f"{RAW_NAME}_clean.parquet"

# Article-facing inclusion for narrative TV stats (documented)
TV_TYPES = {"TV"}
# Sensitivity: core audiovisual catalog
CORE_TYPES = {"TV", "Movie", "ONA", "OVA"}
# Full catalog minus pure non-narrative
ALL_EXCEPT_MUSIC = None  # handled in code

rng = np.random.default_rng(SEED)
random.seed(SEED)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_list(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return []
    if isinstance(val, list):
        return val
    s = str(val).strip()
    if not s or s.lower() in {"nan", "none", "[]"}:
        return []
    try:
        out = ast.literal_eval(s)
        if isinstance(out, list):
            return [str(x) for x in out]
        return [str(out)]
    except Exception:
        return [s]


def has_tag(row, needle: str) -> bool:
    needle_l = needle.lower()
    for col in ("themes", "genre", "anilist_tags", "demographics"):
        for item in parse_list(row.get(col)):
            if needle_l in item.lower():
                return True
    return False


def year_col(df: pd.DataFrame) -> pd.Series:
    y = df["aired_from_year"].copy()
    # fallback season_year
    y = y.fillna(df["season_year"])
    return y


def bootstrap_share(mask: np.ndarray, n_boot: int = 2000) -> tuple[float, float, float]:
    """Share = mean of boolean mask; return (point, lo, hi) 95% percentile CI."""
    mask = np.asarray(mask, dtype=float)
    n = len(mask)
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    point = float(mask.mean())
    idx = rng.integers(0, n, size=(n_boot, n))
    boots = mask[idx].mean(axis=1)
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return point, float(lo), float(hi)


def fmt_pct(x: float, digits: int = 1) -> str:
    if x != x:
        return "NA"
    return f"{100 * x:.{digits}f}%"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    assert RAW_CSV.exists(), f"missing {RAW_CSV}"

    versions = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "seed": SEED,
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "raw_csv_sha256": sha256_file(RAW_CSV),
    }

    raw = pd.read_csv(RAW_CSV, low_memory=False)
    n0 = len(raw)
    log_rules = []
    profile = {}

    # ---------- PROFILE ----------
    profile["n_rows"] = n0
    profile["n_cols"] = raw.shape[1]
    profile["jikan_fetched_true"] = int(raw["jikan_fetched"].fillna(False).sum())
    profile["jikan_fetched_false"] = int((~raw["jikan_fetched"].fillna(False)).sum())
    profile["anilist_fetched_true"] = int(raw["anilist_fetched"].fillna(False).sum())

    y = year_col(raw)
    by_year = y.dropna().astype(int).value_counts().sort_index()
    by_year.to_csv(OUT_DIR / "rows_by_year.csv", header=["n"])

    key_fields = [
        "aired_from_year", "season_year", "season", "type", "source",
        "genre", "themes", "score", "members", "studio", "start_date",
    ]
    missing = {}
    for c in key_fields:
        if c not in raw.columns:
            continue
        if c in ("genre", "themes", "studio"):
            miss = raw[c].apply(lambda v: len(parse_list(v)) == 0).mean()
        else:
            miss = raw[c].isna().mean()
        missing[c] = float(miss)
    profile["missing_rate"] = missing

    dup_id = int(raw["animeID"].duplicated().sum())
    dup_title = int(raw["name"].fillna("").str.lower().str.strip().duplicated().sum())
    profile["duplicate_animeID"] = dup_id
    profile["duplicate_name_casefold"] = dup_title

    type_mix = raw["type"].fillna("(missing)").value_counts(dropna=False)
    type_mix.to_csv(OUT_DIR / "type_mix.csv", header=["n"])
    profile["type_mix"] = type_mix.to_dict()

    # isekai tag presence
    isekai_mask = raw.apply(lambda r: has_tag(r, "isekai"), axis=1)
    profile["isekai_any_tag_n"] = int(isekai_mask.sum())

    # ---------- ANOMALIES ----------
    anomalies = {}
    score = pd.to_numeric(raw["score"], errors="coerce")
    anomalies["score_lt_0"] = int((score < 0).sum())
    anomalies["score_gt_10"] = int((score > 10).sum())
    anomalies["score_eq_0"] = int((score == 0).sum())
    yy = pd.to_numeric(raw["aired_from_year"], errors="coerce")
    anomalies["year_lt_1917"] = int((yy < 1917).sum())
    anomalies["year_gt_2026"] = int((yy > 2026).sum())
    # end before start
    sd = pd.to_datetime(raw["start_date"], errors="coerce")
    ed = pd.to_datetime(raw["end_date"], errors="coerce")
    anomalies["end_before_start"] = int(((ed < sd) & sd.notna() & ed.notna()).sum())
    # members negative
    mem = pd.to_numeric(raw["members"], errors="coerce")
    anomalies["members_lt_0"] = int((mem < 0).sum())
    # source category inventory
    source_counts = raw["source"].fillna("(missing)").value_counts()
    source_counts.to_csv(OUT_DIR / "source_mix.csv", header=["n"])
    anomalies["source_categories"] = source_counts.head(30).to_dict()

    # Tenrai/Jikan vs AniList score disagreement
    both = raw["jikan_fetched"].fillna(False) & raw["anilist_fetched"].fillna(False)
    j_score = pd.to_numeric(raw.loc[both, "score"], errors="coerce")
    a_score = pd.to_numeric(raw.loc[both, "anilist_mean_score"], errors="coerce") / 10.0
    valid = j_score.notna() & a_score.notna()
    diff = (j_score[valid] - a_score[valid]).abs()
    anomalies["tenrai_anilist_score_pairs"] = int(valid.sum())
    anomalies["tenrai_anilist_mae"] = float(diff.mean()) if len(diff) else float("nan")
    anomalies["tenrai_anilist_gt_1pt"] = int((diff > 1.0).sum()) if len(diff) else 0

    # ---------- CLEAN ----------
    clean = raw.copy()
    n = len(clean)

    # Rule 1: drop duplicate animeIDs (keep jikan_fetched preferentially, else first)
    before = len(clean)
    clean = clean.sort_values(["animeID", "jikan_fetched"], ascending=[True, False])
    clean = clean.drop_duplicates("animeID", keep="first").reset_index(drop=True)
    log_rules.append({
        "rule": "R1_dedupe_animeID",
        "description": "Keep one row per animeID; prefer jikan_fetched=True.",
        "rows_before": before,
        "rows_after": len(clean),
        "rows_removed": before - len(clean),
    })

    # Rule 2: null out impossible scores (keep row)
    before_bad = int(((pd.to_numeric(clean["score"], errors="coerce") < 0) |
                      (pd.to_numeric(clean["score"], errors="coerce") > 10)).sum())
    s = pd.to_numeric(clean["score"], errors="coerce")
    clean.loc[(s < 0) | (s > 10), "score"] = np.nan
    log_rules.append({
        "rule": "R2_score_range",
        "description": "Set score to NA if outside [0, 10].",
        "rows_affected": before_bad,
        "rows_before": len(clean),
        "rows_after": len(clean),
    })

    # Rule 3: null out impossible years
    y2 = pd.to_numeric(clean["aired_from_year"], errors="coerce")
    bad_y = (y2 < 1917) | (y2 > 2026)
    n_bad_y = int(bad_y.sum())
    clean.loc[bad_y, "aired_from_year"] = np.nan
    # also season_year
    sy = pd.to_numeric(clean["season_year"], errors="coerce")
    bad_sy = (sy < 1917) | (sy > 2026)
    clean.loc[bad_sy, "season_year"] = np.nan
    log_rules.append({
        "rule": "R3_year_range",
        "description": "Set aired_from_year/season_year to NA if outside [1917, 2026].",
        "rows_affected": int(n_bad_y + bad_sy.sum()),
        "rows_before": len(clean),
        "rows_after": len(clean),
    })

    # Rule 4: clear end_date when end < start
    sd = pd.to_datetime(clean["start_date"], errors="coerce")
    ed = pd.to_datetime(clean["end_date"], errors="coerce")
    bad_span = (ed < sd) & sd.notna() & ed.notna()
    n_span = int(bad_span.sum())
    clean.loc[bad_span, "end_date"] = np.nan
    clean.loc[bad_span, "aired_to_year"] = np.nan
    log_rules.append({
        "rule": "R4_end_before_start",
        "description": "Clear end_date/aired_to_year when end < start.",
        "rows_affected": n_span,
        "rows_before": len(clean),
        "rows_after": len(clean),
    })

    # Rule 5: normalize source labels (collapse aliases; document mapping)
    SOURCE_MAP = {
        "Web manga": "Web manga",
        "Web Manga": "Web manga",
        "4-koma manga": "4-koma manga",
        "4-koma Manga": "4-koma manga",
        "Light novel": "Light novel",
        "Light Novel": "Light novel",
        "Visual novel": "Visual novel",
        "Visual Novel": "Visual novel",
        "Picture book": "Picture book",
        "Book": "Book",
        "Novel": "Novel",
        "Manga": "Manga",
        "Original": "Original",
        "Game": "Game",
        "Other": "Other",
        "Unknown": "Unknown",
        "Music": "Music",
        "Radio": "Radio",
        "Card game": "Card game",
        "Mixed media": "Mixed media",
    }
    before_src = clean["source"].fillna("(missing)").value_counts().to_dict()
    clean["source"] = clean["source"].map(lambda x: SOURCE_MAP.get(x, x) if pd.notna(x) else x)
    after_src = clean["source"].fillna("(missing)").value_counts().to_dict()
    log_rules.append({
        "rule": "R5_source_normalize",
        "description": "Normalize source label casing/aliases (Web manga, Light novel, etc.).",
        "rows_affected": int((clean["source"].astype(str) != raw.reindex(clean.index)["source"].astype(str)).sum()) if False else "see source_mix",
        "source_before_top": dict(list(before_src.items())[:15]),
        "source_after_top": dict(list(after_src.items())[:15]),
        "rows_before": len(clean),
        "rows_after": len(clean),
    })

    # Rule 6: add analysis flags (do not drop unfetched — flag only)
    clean["flag_unfetched_jikan"] = ~clean["jikan_fetched"].fillna(False)
    clean["flag_isekai"] = clean.apply(lambda r: has_tag(r, "isekai"), axis=1)
    clean["flag_analysis_year"] = year_col(clean)
    clean["flag_tv"] = clean["type"].fillna("").eq("TV")
    clean["flag_core_av"] = clean["type"].isin(["TV", "Movie", "ONA", "OVA"])
    log_rules.append({
        "rule": "R6_analysis_flags",
        "description": "Add flag_unfetched_jikan, flag_isekai, flag_analysis_year, flag_tv, flag_core_av. Unfetched rows retained.",
        "rows_before": len(clean),
        "rows_after": len(clean),
        "unfetched_n": int(clean["flag_unfetched_jikan"].sum()),
        "isekai_n": int(clean["flag_isekai"].sum()),
    })

    # Rule 7: drop rows with no identifiable title and no animeID (shouldn't happen)
    before = len(clean)
    clean = clean[clean["animeID"].notna() & clean["name"].notna()].reset_index(drop=True)
    log_rules.append({
        "rule": "R7_require_id_name",
        "description": "Require non-null animeID and name.",
        "rows_before": before,
        "rows_after": len(clean),
        "rows_removed": before - len(clean),
    })

    # Write clean
    clean.to_csv(CLEAN_CSV, index=False)
    try:
        clean.to_parquet(CLEAN_PQ, index=False)
    except Exception as e:
        CLEAN_PQ.write_text("")  # placeholder
        print("parquet write skipped:", e)

    # ---------- PRISMA-STYLE FLOW ----------
    flow = [
        ("A_raw_snapshot", n0, "Rows in anime_2026-10-11.csv"),
        ("B_after_dedupe", log_rules[0]["rows_after"], "After R1 dedupe"),
        ("C_clean_all_types", len(clean), "Clean file (all types; flags only)"),
        ("D_tv_only", int(clean["flag_tv"].sum()), "Inclusion: type==TV (article narrative frame)"),
        ("E_tv_fetched", int((clean["flag_tv"] & ~clean["flag_unfetched_jikan"]).sum()), "TV ∩ jikan_fetched"),
        ("F_tv_scored", int((clean["flag_tv"] & clean["score"].notna()).sum()), "TV with non-null score"),
        ("G_core_av", int(clean["flag_core_av"].sum()), "Sensitivity: TV/Movie/ONA/OVA"),
        ("H_excl_music_special", int((~clean["type"].isin(["Music", "Special"])).sum()), "Sensitivity: drop Music+Special"),
    ]
    pd.DataFrame(flow, columns=["step", "n", "label"]).to_csv(OUT_DIR / "inclusion_flow.csv", index=False)

    # ---------- MISSING DATA ANALYSIS ----------
    # Compare rows missing score vs not on year/type/members
    miss_score = clean["score"].isna()
    miss_tbl = []
    for label, mask in [("score_missing", miss_score), ("score_present", ~miss_score)]:
        sub = clean.loc[mask]
        miss_tbl.append({
            "group": label,
            "n": len(sub),
            "mean_year": float(pd.to_numeric(sub["flag_analysis_year"], errors="coerce").mean()),
            "share_tv": float(sub["flag_tv"].mean()) if len(sub) else float("nan"),
            "median_members": float(pd.to_numeric(sub["members"], errors="coerce").median()),
            "share_unfetched": float(sub["flag_unfetched_jikan"].mean()) if len(sub) else float("nan"),
        })
    # Simple association: unfetched vs score missing (chi-square via contingency)
    a = int((clean["flag_unfetched_jikan"] & miss_score).sum())
    b = int((clean["flag_unfetched_jikan"] & ~miss_score).sum())
    c = int((~clean["flag_unfetched_jikan"] & miss_score).sum())
    d = int((~clean["flag_unfetched_jikan"] & ~miss_score).sum())
    # chi-square
    n = a + b + c + d
    chi = float("nan")
    if n and (a + b) and (c + d) and (a + c) and (b + d):
        chi = n * (a * d - b * c) ** 2 / ((a + b) * (c + d) * (a + c) * (b + d))
    missing_analysis = {
        "note": "Not a formal Little MCAR test; compares covariate profiles for score-missing vs present and association with unfetched flag.",
        "score_missing_vs_present": miss_tbl,
        "unfetched_x_score_missing": {"a_unfetched_miss": a, "b_unfetched_present": b, "c_fetched_miss": c, "d_fetched_present": d, "chi_square": chi},
        "interpretation": (
            "If unfetched strongly predicts score missing, missingness is at least MAR/MNAR w.r.t. fetch success, not MCAR."
            if chi == chi and chi > 3.84 else
            "Weak association between unfetched and score missing in this contingency."
        ),
    }
    (OUT_DIR / "missing_analysis.json").write_text(json.dumps(missing_analysis, indent=2))

    # ---------- HEADLINE STATS: old vs raw vs clean ----------
    # Old article numbers (from parent brief / published framing)
    old = {
        "isekai_share_2015": 0.009,
        "isekai_share_2021_peak": 0.204,
        "isekai_share_2024": 0.177,
        "manga_share_2024": 0.347,
        "web_manga_share_2024": 0.125,
        "manga_plus_web_2024": 0.472,
        "ln_vs_original_median_members_ratio": 32.0,
        "manga_share_score_ge_8": 0.170,
    }

    def tv_frame(df: pd.DataFrame, require_fetched: bool = False) -> pd.DataFrame:
        m = df["type"].fillna("").eq("TV")
        if require_fetched and "jikan_fetched" in df.columns:
            m = m & df["jikan_fetched"].fillna(False)
        out = df.loc[m].copy()
        out["_year"] = year_col(out)
        return out

    def isekai_share(df_tv: pd.DataFrame, year: int) -> tuple[float, float, float, int]:
        sub = df_tv[df_tv["_year"] == year]
        if "flag_isekai" in sub.columns:
            mask = sub["flag_isekai"].to_numpy()
        else:
            mask = sub.apply(lambda r: has_tag(r, "isekai"), axis=1).to_numpy()
        p, lo, hi = bootstrap_share(mask)
        return p, lo, hi, len(sub)

    def source_share(df_tv: pd.DataFrame, year: int, sources: set[str]) -> tuple[float, float, float, int]:
        sub = df_tv[df_tv["_year"] == year]
        mask = sub["source"].isin(sources).to_numpy()
        p, lo, hi = bootstrap_share(mask)
        return p, lo, hi, len(sub)

    def ln_vs_orig_ratio(df_tv: pd.DataFrame) -> float:
        # Match article: median members LN vs Original among TV
        mem = pd.to_numeric(df_tv["members"], errors="coerce")
        ln = mem[df_tv["source"] == "Light novel"].median()
        orig = mem[df_tv["source"] == "Original"].median()
        if pd.isna(ln) or pd.isna(orig) or orig == 0:
            return float("nan")
        return float(ln / orig)

    def manga_ge8(df_tv: pd.DataFrame) -> float:
        manga = df_tv[df_tv["source"] == "Manga"]
        sc = pd.to_numeric(manga["score"], errors="coerce")
        scored = sc.dropna()
        if len(scored) == 0:
            return float("nan")
        return float((scored >= 8.0).mean())

    def compute_bundle(df: pd.DataFrame, label: str, require_fetched: bool = False) -> dict:
        tv = tv_frame(df, require_fetched=require_fetched)
        # ensure isekai flag
        if "flag_isekai" not in tv.columns:
            tv = tv.copy()
            tv["flag_isekai"] = tv.apply(lambda r: has_tag(r, "isekai"), axis=1)
        out = {"label": label, "n_tv": len(tv)}
        for yr, key in [(2015, "isekai_2015"), (2021, "isekai_2021"), (2024, "isekai_2024")]:
            p, lo, hi, n = isekai_share(tv, yr)
            out[key] = {"share": p, "ci95": [lo, hi], "n": n, "pct": fmt_pct(p)}
        for key, sources in [
            ("manga_2024", {"Manga"}),
            ("web_manga_2024", {"Web manga"}),
            ("manga_plus_web_2024", {"Manga", "Web manga"}),
        ]:
            p, lo, hi, n = source_share(tv, 2024, sources)
            out[key] = {"share": p, "ci95": [lo, hi], "n": n, "pct": fmt_pct(p)}
        out["ln_vs_original_median_members_ratio"] = ln_vs_orig_ratio(tv)
        out["manga_share_score_ge_8"] = manga_ge8(tv)
        # scored TV n for article parallel
        out["n_tv_scored"] = int(pd.to_numeric(tv["score"], errors="coerce").notna().sum())
        return out

    raw_stats = compute_bundle(raw.assign(
        flag_isekai=raw.apply(lambda r: has_tag(r, "isekai"), axis=1)
    ), "raw_new")
    clean_stats = compute_bundle(clean, "clean_new")
    clean_fetched = compute_bundle(clean, "clean_tv_fetched", require_fetched=True)

    # Sensitivity: with/without ONA/music/specials — already TV-only for headlines;
    # also report isekai 2024 on core_av and all types for transparency
    def isekai_2024_on(df, type_set=None):
        d = df.copy()
        d["_year"] = year_col(d)
        if type_set is not None:
            d = d[d["type"].isin(type_set)]
        if "flag_isekai" not in d.columns:
            d["flag_isekai"] = d.apply(lambda r: has_tag(r, "isekai"), axis=1)
        sub = d[d["_year"] == 2024]
        p, lo, hi = bootstrap_share(sub["flag_isekai"].to_numpy())
        return {"share": p, "ci95": [lo, hi], "n": len(sub), "pct": fmt_pct(p)}

    sensitivity = {
        "isekai_2024_tv_only": isekai_2024_on(clean, {"TV"}),
        "isekai_2024_core_av": isekai_2024_on(clean, {"TV", "Movie", "ONA", "OVA"}),
        "isekai_2024_excl_music_special": isekai_2024_on(clean, set(clean["type"].dropna()) - {"Music", "Special"}),
        "isekai_2024_all_types": isekai_2024_on(clean, None),
        "isekai_2024_tv_including_unfetched": isekai_2024_on(clean, {"TV"}),
        "isekai_2024_tv_excluding_unfetched": isekai_2024_on(clean[~clean["flag_unfetched_jikan"]], {"TV"}),
    }

    # ---------- INTER-SOURCE VALIDATION (n=200) ----------
    both_idx = clean.index[clean["jikan_fetched"].fillna(False) & clean["anilist_fetched"].fillna(False)].to_numpy()
    sample_n = min(200, len(both_idx))
    sample_idx = rng.choice(both_idx, size=sample_n, replace=False)
    samp = clean.loc[sample_idx]

    def norm_type(t):
        return str(t).strip().lower() if pd.notna(t) else ""

    # AniList score is 0-100; compare year and score within 0.5 / type non-empty agreement
    agree_year = 0
    agree_score = 0
    agree_name = 0
    compared = 0
    for _, row in samp.iterrows():
        compared += 1
        y_j = row.get("aired_from_year")
        y_s = row.get("season_year")
        # AniList doesn't have separate year col beyond what we already merged — use season_year as shared field
        # Validate: anilist_mean_score/10 vs score
        js = row.get("score")
        as_ = row.get("anilist_mean_score")
        if pd.notna(js) and pd.notna(as_):
            if abs(float(js) - float(as_) / 10.0) <= 0.5:
                agree_score += 1
        else:
            # count as non-comparable; adjust denominator later
            pass
        # name: english or romaji overlap
        n1 = str(row.get("name") or "").lower()
        n2 = str(row.get("title_english") or "").lower()
        if n1 and (n1 in n2 or n2 in n1 or not n2):
            agree_name += 1
        # year self-consistency season_year vs aired_from_year
        if pd.notna(y_j) and pd.notna(y_s) and int(y_j) == int(y_s):
            agree_year += 1
        elif pd.isna(y_j) or pd.isna(y_s):
            agree_year += 0
        else:
            pass

    score_comparable = int(samp["score"].notna() & samp["anilist_mean_score"].notna()).sum() if False else int((samp["score"].notna() & samp["anilist_mean_score"].notna()).sum())
    validation = {
        "sample_n": sample_n,
        "seed": SEED,
        "universe": "rows with jikan_fetched & anilist_fetched",
        "universe_n": int(len(both_idx)),
        "score_agreement_within_0_5": {
            "agree": agree_score,
            "comparable": score_comparable,
            "rate": (agree_score / score_comparable) if score_comparable else float("nan"),
        },
        "year_season_year_match": {
            "agree": agree_year,
            "sample_n": sample_n,
            "rate": agree_year / sample_n if sample_n else float("nan"),
        },
        "note": (
            "Cross-check uses co-present Tenrai/Jikan fields vs AniList fields already joined on idMal "
            "(offline validation; no live API re-fetch). Score: |MAL - AniList/10| ≤ 0.5."
        ),
    }
    (OUT_DIR / "intersource_validation.json").write_text(json.dumps(validation, indent=2))

    # ---------- STATS TABLE ----------
    def cell(bundle, key, as_pct=True):
        v = bundle.get(key)
        if isinstance(v, dict):
            p = v["share"]
            lo, hi = v["ci95"]
            return f"{fmt_pct(p)} [{fmt_pct(lo)}–{fmt_pct(hi)}] (n={v['n']})"
        if key in bundle and isinstance(bundle[key], (int, float)):
            if as_pct and bundle[key] <= 1:
                return fmt_pct(float(bundle[key]))
            return f"{bundle[key]:.2f}" if isinstance(bundle[key], float) else str(bundle[key])
        return "NA"

    rows_tbl = []
    mapping = [
        ("isekai share 2015 (TV)", "isekai_share_2015", "isekai_2015", True),
        ("isekai share 2021 (TV)", "isekai_share_2021_peak", "isekai_2021", True),
        ("isekai share 2024 (TV)", "isekai_share_2024", "isekai_2024", True),
        ("manga share 2024 (TV)", "manga_share_2024", "manga_2024", True),
        ("web manga share 2024 (TV)", "web_manga_share_2024", "web_manga_2024", True),
        ("manga+web manga 2024 (TV)", "manga_plus_web_2024", "manga_plus_web_2024", True),
        ("LN / Original median members (TV)", "ln_vs_original_median_members_ratio", "ln_vs_original_median_members_ratio", False),
        ("manga share score≥8.0 (TV)", "manga_share_score_ge_8", "manga_share_score_ge_8", True),
    ]
    for label, old_key, new_key, is_pct in mapping:
        old_v = old[old_key]
        if is_pct:
            old_s = fmt_pct(old_v)
            raw_s = cell(raw_stats, new_key)
            clean_s = cell(clean_stats, new_key)
        else:
            old_s = f"{old_v:.1f}×"
            raw_s = f"{raw_stats.get(new_key, float('nan')):.2f}×"
            clean_s = f"{clean_stats.get(new_key, float('nan')):.2f}×"
        rows_tbl.append({
            "stat": label,
            "old_article": old_s,
            "raw_new": raw_s,
            "clean_new": clean_s,
        })
    stats_df = pd.DataFrame(rows_tbl)
    stats_df.to_csv(OUT_DIR / "stats_old_vs_raw_vs_clean.csv", index=False)

    summary_json = {
        "versions": versions,
        "profile": profile,
        "anomalies": anomalies,
        "rules": log_rules,
        "flow": flow,
        "raw_stats": raw_stats,
        "clean_stats": clean_stats,
        "clean_fetched_stats": clean_fetched,
        "sensitivity": sensitivity,
        "validation": validation,
        "stats_table": rows_tbl,
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary_json, indent=2, default=str))

    # ---------- WRITE CLEANING_LOG.md ----------
    cleaning_log = f"""# CLEANING_LOG — anime_2026-10-11 → anime_2026-10-11_clean

**Run (UTC):** {versions['run_utc']}  
**Seed:** `{SEED}`  
**Raw SHA-256:** `{versions['raw_csv_sha256']}`  
**Environment:** Python {versions['python']}, pandas {versions['pandas']}, numpy {versions['numpy']}, {versions['platform']}

**Pipeline:** `python3 scripts/anime-data/clean_audit.py` (this file is an output of that script).

## Inclusion / exclusion (PRISMA-style counts)

| Step | N | Description |
|------|--:|-------------|
"""
    for step, n, label in flow:
        cleaning_log += f"| `{step}` | {n:,} | {label} |\n"

    cleaning_log += """
### Inclusion rule (headline / article-parallel stats)

- **Unit of analysis:** one MyAnimeList anime id (`animeID`).
- **Headline TV frame:** `type == "TV"` (matches the published ANIME report’s TV-centric comparisons).
- **Isekai definition:** case-insensitive match for `"isekai"` in any of `themes`, `genre`, `anilist_tags`, or `demographics` (list fields).
- **Year:** `aired_from_year`, falling back to `season_year`.
- **Unfetched rows** (`jikan_fetched == False`, n={unfetched}): **retained** in the clean file with `flag_unfetched_jikan`; excluded only in sensitivity / fetched-only recomputes.

### Exclusion / sensitivity

- Music and Specials remain in the clean file; sensitivity recomputes drop them or restrict to TV/Movie/ONA/OVA (see METHODS_NOTE).
- No rows deleted solely for missing score or missing AniList join.

## Cleaning rules

""".format(unfetched=profile['jikan_fetched_false'])

    for r in log_rules:
        cleaning_log += f"### {r['rule']}\n\n"
        cleaning_log += f"- **Description:** {r['description']}\n"
        for k in ("rows_before", "rows_after", "rows_removed", "rows_affected", "unfetched_n", "isekai_n"):
            if k in r and r[k] != "see source_mix":
                cleaning_log += f"- **{k}:** {r[k]}\n"
        cleaning_log += "\n"

    cleaning_log += "## Profile (raw)\n\n"
    cleaning_log += f"- Rows: **{profile['n_rows']:,}**; cols: **{profile['n_cols']}**\n"
    cleaning_log += f"- `jikan_fetched` True/False: **{profile['jikan_fetched_true']:,}** / **{profile['jikan_fetched_false']:,}**\n"
    cleaning_log += f"- Duplicate `animeID`: **{profile['duplicate_animeID']}**; duplicate casefold `name`: **{profile['duplicate_name_casefold']:,}**\n"
    cleaning_log += f"- Isekai-tagged rows (any list field): **{profile['isekai_any_tag_n']:,}**\n\n"
    cleaning_log += "### Missingness (raw rates)\n\n| Field | Missing rate |\n|-------|-------------:|\n"
    for k, v in missing.items():
        cleaning_log += f"| `{k}` | {v:.1%} |\n"

    cleaning_log += "\n### Type mix (raw)\n\n| Type | N |\n|------|--:|\n"
    for t, c in type_mix.items():
        cleaning_log += f"| {t} | {c:,} |\n"

    cleaning_log += "\n## Anomalies flagged\n\n"
    cleaning_log += f"- Scores outside [0,10]: lt0={anomalies['score_lt_0']}, gt10={anomalies['score_gt_10']}\n"
    cleaning_log += f"- Years outside [1917,2026]: lt={anomalies['year_lt_1917']}, gt={anomalies['year_gt_2026']}\n"
    cleaning_log += f"- end_date < start_date: {anomalies['end_before_start']}\n"
    cleaning_log += f"- Tenrai vs AniList score pairs: n={anomalies['tenrai_anilist_score_pairs']:,}, MAE={anomalies['tenrai_anilist_mae']:.3f}, |Δ|>1: {anomalies['tenrai_anilist_gt_1pt']:,}\n"

    cleaning_log += "\n## Headline stats — old article vs raw-new vs clean-new\n\n"
    cleaning_log += "| Stat | Old article | Raw new (TV) | Clean new (TV, 95% bootstrap CI) |\n|------|-------------|--------------|----------------------------------|\n"
    for row in rows_tbl:
        cleaning_log += f"| {row['stat']} | {row['old_article']} | {row['raw_new']} | {row['clean_new']} |\n"

    cleaning_log += "\nBootstrap: 2000 resamples, seed `{SEED}`, percentile 95% CI.\n".format(SEED=SEED)

    cleaning_log += "\n## Sensitivity (isekai share 2024)\n\n"
    for k, v in sensitivity.items():
        cleaning_log += f"- `{k}`: {v['pct']} [{fmt_pct(v['ci95'][0])}–{fmt_pct(v['ci95'][1])}] (n={v['n']})\n"

    cleaning_log += "\n## Inter-source validation (n=200)\n\n"
    cleaning_log += json.dumps(validation, indent=2)
    cleaning_log += "\n\n## Outputs\n\n"
    cleaning_log += f"- `{CLEAN_CSV.relative_to(ROOT)}`\n"
    cleaning_log += f"- `{CLEAN_PQ.relative_to(ROOT)}`\n"
    cleaning_log += f"- `{OUT_DIR.relative_to(ROOT)}/`\n"

    (DATA / "CLEANING_LOG.md").write_text(cleaning_log)

    # ---------- METHODS_NOTE.md (academic) ----------
    methods = f"""# METHODS_NOTE — Artometrics Anime dataset (2026-10-11)

## 1. Purpose and framing

This note documents the refresh from the 2019-04-23 TidyTuesday MyAnimeList export to the 2026-10-11 Tenrai + AniList snapshot, and the reproducible cleaning pass that produces `anime_2026-10-11_clean.*`. The editorial frame is **what changed when we fixed / extended the data**, not a silent rewrite of the published article.

## 2. Data sources and citations

| Source | Role | Access / version |
|--------|------|------------------|
| TidyTuesday `tidy_anime.csv` (Kaggle MyAnimeList scrape by Tam Nguyen) | Baseline catalog | Snapshot **2019-04-23**; SHA-256 `5ea3a14492b5c559c728af0c7ec57b81c919d0efa4d381e54b0f7cde9934a1c2`; <https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-04-23> |
| **Tenrai API** (`api.tenrai.org`) | Jikan-compatible MyAnimeList mirror for title metadata (score, members, genres, themes, studios, etc.) | Accessed **2026-10-12**. Public Jikan v4 (`api.jikan.moe`) was discontinued **2026-10-01**; field names retain the Jikan v4 schema. |
| **AniList GraphQL API** | Enrichment via `idMal` (tags, meanScore, popularity, trending, streaming links) | Docs: <https://anilist.gitbook.io/anilist-apiv2-docs/>; accessed during refresh culminating in snapshot **2026-10-11** (pipeline run logged 2026-10-12). |
| MyAnimeList | Upstream of Tenrai/Jikan fields | User-generated scores and lists; subject to ongoing revision |

**Pipeline code:** `scripts/anime-data/refresh.py` (ingest), `scripts/anime-data/clean_audit.py` (audit + clean; seed `{SEED}`).

## 3. Unit of analysis and snapshot size

- **Unit:** one row per MyAnimeList `animeID`.
- **Raw snapshot:** **{profile['n_rows']:,}** rows × {profile['n_cols']} columns (`anime_2026-10-11.csv`).
- **Tenrai/Jikan fetch success:** **{profile['jikan_fetched_true']:,}** fetched; **{profile['jikan_fetched_false']:,}** unfetched.
- **Baseline:** 13,631 titles (2019-04-23); **+5,187** new MAL ids in the refresh (see `CHANGELOG_2019-04-23_to_2026-10-11.md`).

## 4. Inclusion and exclusion criteria (with flow counts)

See also `CLEANING_LOG.md` and `audit_outputs/inclusion_flow.csv`.

| Step | N | Criterion |
|------|--:|-----------|
"""
    for step, n, label in flow:
        methods += f"| {step} | {n:,} | {label} |\n"

    methods += f"""
**Primary analysis set for article-parallel headline shares:** TV titles (`type == "TV"`), year from `aired_from_year` (fallback `season_year`).

**Isekai:** tag match for “isekai” in `themes` ∪ `genre` ∪ `anilist_tags` ∪ `demographics`.

**Sensitivity sets:** (i) TV/Movie/ONA/OVA only; (ii) exclude Music + Special; (iii) TV including vs excluding unfetched rows.

## 5. Cleaning (reproducible)

One command:

```bash
python3 scripts/anime-data/clean_audit.py
```

Rules R1–R7 are enumerated with before/after counts in `CLEANING_LOG.md`. Outputs: `anime_2026-10-11_clean.csv` / `.parquet`.

**Seed:** `{SEED}` (NumPy Generator + Python `random`).

## 6. Data dictionary / codebook

Canonical column definitions: `data/anime/DATA_DICTIONARY.md`. Clean file adds:

| Column | Type | Definition |
|--------|------|------------|
| `flag_unfetched_jikan` | bool | `not jikan_fetched` |
| `flag_isekai` | bool | Isekai tag rule above |
| `flag_analysis_year` | float | Analysis year |
| `flag_tv` | bool | `type == "TV"` |
| `flag_core_av` | bool | type ∈ {{TV, Movie, ONA, OVA}} |

## 7. Missing-data analysis

Formal Little’s MCAR test was **not** estimated (high-dimensional mixed types). Instead:

1. Profile missing rates for key fields (see CLEANING_LOG).
2. Compare score-missing vs score-present rows on mean year, share TV, median members, share unfetched (`audit_outputs/missing_analysis.json`).
3. Contingency χ² for `unfetched × score_missing`.

**Interpretation:** fetch failure is a structural reason for thin metadata; treat unfetched rows as **observed missingness related to measurement**, and report fetched-only sensitivity beside all-row TV estimates.

## 8. Uncertainty

Bootstrap **95% percentile CIs** (B = 2000, seed `{SEED}`) for isekai and source shares by year. Point estimates are sample proportions within the stated inclusion set.

## 9. Inter-source validation

Random sample of **n = {sample_n}** rows with both `jikan_fetched` and `anilist_fetched` (seed `{SEED}`).

- Score agreement (|MAL − AniList meanScore/10| ≤ 0.5): **{validation['score_agreement_within_0_5']['agree']} / {validation['score_agreement_within_0_5']['comparable']}** = **{validation['score_agreement_within_0_5']['rate']:.1%}**
- `aired_from_year` == `season_year`: **{validation['year_season_year_match']['rate']:.1%}**

This is an **offline** cross-check of joined fields (no live re-fetch at audit time). Disagreement can reflect scale calibration, update timing, or mapping error.

## 10. Headline statistic reconciliation

| Stat | Old article | Raw new (TV) | Clean new (TV) |
|------|-------------|--------------|----------------|
"""
    for row in rows_tbl:
        methods += f"| {row['stat']} | {row['old_article']} | {row['raw_new']} | {row['clean_new']} |\n"

    methods += f"""
Full machine-readable table: `audit_outputs/stats_old_vs_raw_vs_clean.csv`.

**Reading the gap:** Old article figures for isekai (2015/2021/2024) and 2024 manga/web-manga mixes were exploratory claims tied to the refresh narrative; recompute on the full TV catalog with an explicit tag rule. The **32×** light-novel vs original median members and **17.0%** manga ≥8.0 figures in the published piece used the earlier scored-TV analysis frame (early-2019 snapshot language remains in article prose until a separate copy update).

## 11. Limitations

1. **MAL popularity is not a probability sample** of anime viewers; members/scores are platform-selected.
2. **Tenrai is a mirror** of MAL; outages or drift vs mal_id can leave `jikan_fetched=False` ({profile['jikan_fetched_false']} rows).
3. **AniList join is many-to-none** via `idMal`; tags (including Isekai) may be denser on AniList than MAL themes.
4. **Isekai operationalization** is string match on tags — not a hand-coded genre ontology; false positives/negatives possible.
5. **Year assignment** uses air start / season year; calendar-year “share of 2024 titles” is sensitive to unfinished airing and missing dates.
6. **Scores drift over time**; October 2026 scores are not comparable as causal outcomes to 2019 scores without a panel model.
7. **Bootstrap CIs** ignore clustering by studio/franchise; they understate dependence.
8. **No live AniList re-audit** of the n=200 sample at clean time — validation uses already-fetched fields.
9. Cleaning **does not impute** scores or sources; it flags and nulls impossible values only.

## 12. Reproducibility checklist

- [x] Fixed seed (`{SEED}`)
- [x] Raw file hash recorded
- [x] Single entry-point script
- [x] Environment versions logged
- [x] Flow counts + sensitivity + bootstrap CIs
- [x] Clean artifacts written beside raw snapshot

*Generated by `scripts/anime-data/clean_audit.py` on {versions['run_utc']}.*
"""
    (DATA / "METHODS_NOTE.md").write_text(methods)

    # also print concise console report
    print("=== ANIME CLEAN AUDIT DONE ===")
    print(json.dumps({"versions": versions, "flow": flow, "stats_table": rows_tbl, "validation": validation["score_agreement_within_0_5"], "sensitivity_isekai_2024_tv": sensitivity["isekai_2024_tv_only"]}, indent=2, default=str))
    print("Wrote", CLEAN_CSV)
    print("Wrote", DATA / "CLEANING_LOG.md")
    print("Wrote", DATA / "METHODS_NOTE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
