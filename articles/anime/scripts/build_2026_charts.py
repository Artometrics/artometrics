#!/usr/bin/env python3
"""Oct-2026 anime charts from data/anime clean snapshot (house style: #0047FF, DM Sans/Mono, no red)."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

SEED = 20261011
ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "anime"
CLEAN_CSV = DATA / "anime_2026-10-11_clean.csv"
BASELINE_CSV = DATA / "baseline" / "anime_tidy_anime_2019-04-23.csv"
ARTICLE = ROOT / "articles" / "anime"
CHARTS = ARTICLE / "charts"
PUBLIC = ROOT / "public" / "data" / "articles" / "anime" / "charts"
IMG = ROOT / "public" / "images" / "content" / "articles" / "anime" / "charts"
AUDIT = DATA / "audit_outputs" / "chart_series"

BLUE, LIGHT, GREY, INK = "#0047FF", "#A9BDFF", "#B8B8B8", "#000000"
SRC = (
    "Source: MyAnimeList via Tenrai API (api.tenrai.org) + AniList enrichment · "
    "snapshot 2026-10-11 · clean_audit.py"
)

rng = np.random.default_rng(SEED)

OLD_HEADLINE = {
    "isekai_2015": 0.9,
    "isekai_2021": 20.4,
    "isekai_2024": 17.7,
    "manga_ge8": 17.0,
    "manga_web_2024": 47.2,
    "ln_orig_ratio": 32.0,
}

SOURCE_GROUPS = {
    "Manga": {"Manga"},
    "Web manga": {"Web manga"},
    "Light novel": {"Light novel"},
    "Original": {"Original"},
    "Game": {"Game"},
}
OTHER_SOURCES = None  # computed as remainder


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
        return [str(x) for x in out] if isinstance(out, list) else [str(out)]
    except Exception:
        return [s]


def has_isekai(row) -> bool:
    for col in ("themes", "genre", "anilist_tags", "demographics"):
        for item in parse_list(row.get(col)):
            if "isekai" in item.lower():
                return True
    return False


def analysis_year(df: pd.DataFrame) -> pd.Series:
    y = pd.to_numeric(df["aired_from_year"], errors="coerce")
    if "season_year" in df.columns:
        y = y.fillna(pd.to_numeric(df["season_year"], errors="coerce"))
    return y


def collapse_baseline(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path, low_memory=False)
    raw = raw.sort_values(["animeID"]).drop_duplicates("animeID", keep="first")
    return raw.reset_index(drop=True)


def tv_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df[df["type"].fillna("").eq("TV")].copy()
    out["_year"] = analysis_year(out)
    if "flag_isekai" in out.columns:
        out["_isekai"] = out["flag_isekai"].astype(bool)
    else:
        out["_isekai"] = out.apply(has_isekai, axis=1)
    return out


def bootstrap_share(mask: np.ndarray, n_boot: int = 2000) -> tuple[float, float, float]:
    mask = np.asarray(mask, dtype=float)
    n = len(mask)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    point = float(mask.mean())
    idx = rng.integers(0, n, size=(n_boot, n))
    boots = mask[idx].mean(axis=1)
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return point, float(lo), float(hi)


def pct1(x: float) -> float:
    return round(100 * x, 1)


def pct1_str(x: float) -> str:
    return f"{pct1(x):.1f}%"


def ratio1_str(x: float) -> str:
    return f"{x:.1f}×"


def style(fig, title, sub, kicker, source, h=560, l=200):
    title, sub, kicker = (x.replace("$", "&#36;") for x in (title, sub, kicker))
    fig.update_layout(
        title=dict(
            text=(
                f"<span style='font-size:11px;color:{BLUE};font-family:DM Mono, monospace'>"
                f"{kicker.upper()}</span><br><b>{title}</b><br>"
                f"<span style='font-size:12px;color:#6B6B6B'>{sub}</span>"
            ),
            x=0.01,
            xanchor="left",
            xref="container",
            y=0.97,
            yanchor="top",
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=h,
        width=900,
        font=dict(family="DM Sans, Helvetica, sans-serif", color=INK, size=12),
        margin=dict(l=l, r=50, t=130, b=150),
        showlegend=fig.layout.showlegend or False,
        hovermode="closest",
        annotations=list(fig.layout.annotations)
        + [
            dict(
                x=0,
                y=0,
                xref="paper",
                yref="paper",
                yshift=-125,
                showarrow=False,
                xanchor="left",
                yanchor="top",
                text=f"<span style='font-family:DM Mono, ui-monospace, monospace'>{source} · Artometrics</span>",
                font=dict(size=9, color="#6B6B6B"),
            )
        ],
    )
    fig.update_xaxes(gridcolor="#EEEEEE", zeroline=False)
    fig.update_yaxes(gridcolor="#EEEEEE")
    return fig


def save(fig, name: str):
    for d in (CHARTS, PUBLIC, IMG):
        d.mkdir(parents=True, exist_ok=True)
    (CHARTS / f"{name}.plotly.json").write_text(fig.to_json())
    (PUBLIC / f"{name}.plotly.json").write_text(fig.to_json())
    fig.write_image(CHARTS / f"{name}.png", scale=2)
    fig.write_image(PUBLIC / f"{name}.png", scale=2)
    fig.write_image(IMG / f"{name}.png", scale=2)
    fig.write_html(CHARTS / f"{name}.html", include_plotlyjs="cdn")


def source_bucket(src) -> str:
    if pd.isna(src):
        return "Other"
    if src in SOURCE_GROUPS["Manga"]:
        return "Manga"
    if src in SOURCE_GROUPS["Web manga"]:
        return "Web manga"
    if src in SOURCE_GROUPS["Light novel"]:
        return "Light novel"
    if src in SOURCE_GROUPS["Original"]:
        return "Original"
    if src in SOURCE_GROUPS["Game"]:
        return "Game"
    return "Other"


def yearly_isekai(tv: pd.DataFrame, years: range) -> pd.DataFrame:
    rows = []
    for yr in years:
        sub = tv[tv["_year"] == yr]
        if len(sub) < 20:
            continue
        p, lo, hi = bootstrap_share(sub["_isekai"].to_numpy())
        rows.append({"year": yr, "share": p, "lo": lo, "hi": hi, "n": len(sub)})
    return pd.DataFrame(rows)


def yearly_ln_ratio(tv: pd.DataFrame, years: range) -> pd.DataFrame:
    rows = []
    mem = pd.to_numeric(tv["members"], errors="coerce")
    for yr in years:
        sub = tv[tv["_year"] == yr]
        if len(sub) < 15:
            continue
        m = pd.to_numeric(sub["members"], errors="coerce")
        ln = m[sub["source"] == "Light novel"].median()
        orig = m[sub["source"] == "Original"].median()
        if pd.isna(ln) or pd.isna(orig) or orig == 0:
            continue
        rows.append({"year": yr, "ratio": float(ln / orig), "n": len(sub)})
    return pd.DataFrame(rows)


def yearly_source_mix(tv: pd.DataFrame, years: range) -> pd.DataFrame:
    rows = []
    for yr in years:
        sub = tv[tv["_year"] == yr]
        if len(sub) < 20:
            continue
        buckets = sub["source"].map(source_bucket)
        counts = buckets.value_counts()
        for label in ["Manga", "Web manga", "Light novel", "Original", "Game", "Other"]:
            share = counts.get(label, 0) / len(sub)
            rows.append({"year": yr, "source": label, "share": share, "n": len(sub)})
    return pd.DataFrame(rows)


def scorecard_sources(tv_scored: pd.DataFrame) -> pd.DataFrame:
    order = ["Light novel", "Manga", "Novel", "Original", "Game"]
    rows = []
    for src in order:
        sub = tv_scored[tv_scored["source"] == src]
        if len(sub) == 0:
            continue
        sc = pd.to_numeric(sub["score"], errors="coerce")
        mem = pd.to_numeric(sub["members"], errors="coerce")
        rows.append(
            {
                "source": src,
                "n": len(sub),
                "median_score": float(sc.median()),
                "median_members": float(mem.median()),
                "share_ge8": float((sc >= 8.0).mean()),
            }
        )
    return pd.DataFrame(rows)


def main() -> int:
    assert CLEAN_CSV.exists(), CLEAN_CSV
    clean = pd.read_csv(CLEAN_CSV, low_memory=False)
    baseline = collapse_baseline(BASELINE_CSV)

    tv_clean = tv_frame(clean)
    tv_base = tv_frame(baseline)
    tv_scored = tv_clean[pd.to_numeric(tv_clean["score"], errors="coerce").notna()].copy()
    tv_scored["score"] = pd.to_numeric(tv_scored["score"])
    tv_scored["members"] = pd.to_numeric(tv_scored["members"], errors="coerce")

    years_isekai = range(2010, 2026)
    years_mix = range(2015, 2026)
    years_ratio = range(2010, 2026)

    isekai_clean = yearly_isekai(tv_clean, years_isekai)
    isekai_base = yearly_isekai(tv_base, years_isekai)
    mix = yearly_source_mix(tv_clean, years_mix)
    ratio_clean = yearly_ln_ratio(tv_clean, years_ratio)
    ratio_base = yearly_ln_ratio(tv_base, years_ratio)

    AUDIT.mkdir(parents=True, exist_ok=True)
    isekai_clean.to_csv(AUDIT / "isekai_share_by_year_clean.csv", index=False)
    isekai_base.to_csv(AUDIT / "isekai_share_by_year_baseline.csv", index=False)
    mix.to_csv(AUDIT / "source_mix_2015_2025.csv", index=False)
    ratio_clean.to_csv(AUDIT / "ln_orig_ratio_by_year_clean.csv", index=False)
    ratio_base.to_csv(AUDIT / "ln_orig_ratio_by_year_baseline.csv", index=False)

    # --- 1. Isekai share by year ---
    f = go.Figure()
    f.add_scatter(
        x=isekai_clean["year"],
        y=isekai_clean["share"] * 100,
        mode="lines+markers",
        name="Oct 2026 clean",
        line=dict(color=BLUE, width=3),
        marker=dict(size=7),
    )
    f.add_scatter(
        x=isekai_clean["year"],
        y=isekai_clean["lo"] * 100,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip",
    )
    f.add_scatter(
        x=isekai_clean["year"],
        y=isekai_clean["hi"] * 100,
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(0,71,255,0.12)",
        line=dict(width=0),
        name="95% bootstrap range",
        hoverinfo="skip",
    )
    f.update_layout(showlegend=True, legend=dict(orientation="h", y=1.08, x=1, xanchor="right"))
    f.update_xaxes(title="TV premiere year", dtick=1)
    f.update_yaxes(title="share of TV titles tagged isekai (%)", ticksuffix="%")
    save(
        style(
            f,
            "Isekai tags peaked in 2021 and stayed elevated",
            "TV titles only; tag match in themes, genres, or AniList tags · bands = 95% bootstrap",
            "2021: 20.4% · 2024: 18.1%",
            SRC,
            h=520,
        ),
        "chart_isekai_by_year",
    )

    # --- 2. Source mix 2015–2025 ---
    pal = {
        "Manga": BLUE,
        "Web manga": "#5C85FF",
        "Light novel": "#001F70",
        "Original": LIGHT,
        "Game": GREY,
        "Other": "#DDDDDD",
    }
    f = go.Figure()
    for label in ["Manga", "Web manga", "Light novel", "Original", "Game", "Other"]:
        s = mix[mix["source"] == label].sort_values("year")
        f.add_scatter(
            x=s["year"],
            y=s["share"] * 100,
            mode="lines",
            stackgroup="one",
            name=label,
            line=dict(width=0.8, color=pal[label]),
            fillcolor=pal[label],
        )
    f.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.12, font=dict(size=10)))
    f.update_xaxes(title="TV premiere year", dtick=1)
    f.update_yaxes(title="share of TV premieres (%)", ticksuffix="%", range=[0, 100])
    save(
        style(
            f,
            "Manga plus web manga still near half of TV premieres",
            "Stacked shares by source label · 2024 manga+web manga = 47.2%",
            "2015–2025 TV catalog",
            SRC,
            h=560,
            l=220,
        ),
        "chart_source_mix_2015_2025",
    )

    # --- 3. Old vs corrected headline shares ---
    clean_stats = json.loads((DATA / "audit_outputs" / "summary.json").read_text())["clean_stats"]
    new_vals = {
        "Isekai share 2015": pct1(clean_stats["isekai_2015"]["share"]),
        "Isekai share 2021": pct1(clean_stats["isekai_2021"]["share"]),
        "Isekai share 2024": pct1(clean_stats["isekai_2024"]["share"]),
        "Manga scoring 8.0+ (TV)": pct1(clean_stats["manga_share_score_ge_8"]),
        "Manga + web manga 2024": pct1(clean_stats["manga_plus_web_2024"]["share"]),
        "LN ÷ Original median members": round(clean_stats["ln_vs_original_median_members_ratio"], 1),
    }
    old_vals = {
        "Isekai share 2015": OLD_HEADLINE["isekai_2015"],
        "Isekai share 2021": OLD_HEADLINE["isekai_2021"],
        "Isekai share 2024": OLD_HEADLINE["isekai_2024"],
        "Manga scoring 8.0+ (TV)": OLD_HEADLINE["manga_ge8"],
        "Manga + web manga 2024": OLD_HEADLINE["manga_web_2024"],
        "LN ÷ Original median members": OLD_HEADLINE["ln_orig_ratio"],
    }
    labels = list(new_vals.keys())[::-1]
    f = go.Figure()
    for lab in labels:
        a, b = old_vals[lab], new_vals[lab]
        f.add_scatter(x=[a, b], y=[lab, lab], mode="lines", line=dict(color=GREY, width=3), showlegend=False, hoverinfo="skip")
    f.add_scatter(
        x=[old_vals[l] for l in labels],
        y=labels,
        mode="markers",
        name="Published / exploratory",
        marker=dict(color=GREY, size=12),
    )
    f.add_scatter(
        x=[new_vals[l] for l in labels],
        y=labels,
        mode="markers",
        name="Oct 2026 clean",
        marker=dict(color=BLUE, size=12),
    )
    f.update_layout(showlegend=True, legend=dict(orientation="h", y=1.08, x=1, xanchor="right"))
    f.update_xaxes(title="value (% or × for median-member ratio)")
    save(
        style(
            f,
            "What moved when we recomputed on the clean TV frame",
            "Grey = earlier article or exploratory figures · Blue = clean_audit.py (seed 20261011)",
            "2015 isekai: 0.9% → 2.2%",
            SRC,
            h=620,
            l=280,
        ),
        "chart_shares_old_vs_corrected",
    )

    # --- 4. LN / Original ratio by year: baseline vs clean ---
    f = go.Figure()
    f.add_scatter(
        x=ratio_base["year"],
        y=ratio_base["ratio"],
        mode="lines+markers",
        name="2019 TidyTuesday frame",
        line=dict(color=GREY, width=2, dash="dot"),
        marker=dict(size=6),
    )
    f.add_scatter(
        x=ratio_clean["year"],
        y=ratio_clean["ratio"],
        mode="lines+markers",
        name="Oct 2026 clean",
        line=dict(color=BLUE, width=3),
        marker=dict(size=7),
    )
    f.update_layout(showlegend=True, legend=dict(orientation="h", y=1.08, x=1, xanchor="right"))
    f.update_xaxes(title="TV premiere year", dtick=1)
    f.update_yaxes(title="median members (light novel) ÷ median members (original)")
    save(
        style(
            f,
            "The light-novel reach premium narrowed but did not vanish",
            "Ratio of within-year medians · headline all-years: 32.0× → 27.5×",
            "2024 ratio ≈ "
            + f"{ratio_clean[ratio_clean['year']==2024]['ratio'].iloc[0]:.1f}×"
            if (ratio_clean["year"] == 2024).any()
            else "27.5× headline",
            SRC,
            h=520,
        ),
        "chart_ln_ratio_old_vs_clean",
    )

    # --- 5. Scorecard (updated) ---
    sc = scorecard_sources(tv_scored)
    sources = sc["source"].tolist()
    f = make_subplots(rows=1, cols=2, subplot_titles=("Median members (log scale)", "Share scoring 8.0+ (%)"))
    colors = [BLUE if s == "Light novel" else LIGHT for s in sources]
    f.add_trace(
        go.Scatter(
            x=sources,
            y=sc["median_members"],
            mode="markers+lines",
            line=dict(color=BLUE, width=1),
            marker=dict(size=12, color=colors),
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    f.add_trace(
        go.Bar(x=sources, y=sc["share_ge8"] * 100, marker_color=colors, showlegend=False),
        row=1,
        col=2,
    )
    f.update_yaxes(type="log", title_text="Members", row=1, col=1)
    f.update_yaxes(title_text="%", ticksuffix="%", row=1, col=2)
    ln_r = clean_stats["ln_vs_original_median_members_ratio"]
    save(
        style(
            f,
            "Light novels still set the audience floor; manga still yields the most 8.0s",
            f"Scored TV titles (n = {len(tv_scored):,}) · LN÷Original = {ln_r:.1f}× · manga ≥8.0 = {pct1(clean_stats['manga_share_score_ge_8'])}%",
            "Manga ≥8.0: 14.8%",
            SRC,
            h=520,
            l=180,
        ),
        "chart_scorecard",
    )

    meta = {
        "scorecard": sc.to_dict(orient="records"),
        "new_headline": new_vals,
        "old_headline": old_vals,
    }
    (AUDIT / "build_2026_meta.json").write_text(json.dumps(meta, indent=2))
    print("ok", json.dumps(new_vals))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
