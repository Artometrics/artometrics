#!/usr/bin/env python3
"""Rebuild Billboard charts 1–5 from articles/billboard/data/dataset.csv.

Uses the same five-chart builders as scripts/artometrics_engine.py.
Chart 5 plots weeks against rating_2 and drops rows with no rating_2, which
is every No. 1 appended from the 2025–2026 Hot 100 file.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from artometrics_engine import DatasetSpec, build_charts, save_chart  # noqa: E402

ISSUE = ROOT / "articles/billboard/data/dataset.csv"
CHARTS = ROOT / "articles/billboard/charts"
DATA_CHARTS = ROOT / "articles/billboard/data/charts"
PUBLIC_CHARTS = ROOT / "public/data/articles/billboard/charts"

CAPTION_NOTE = (
    "New No. 1s from 2025 to 2026 have no secondary-reach value in the source file."
)

NEW_TITLES = {
    "4X4",
    "Luther",
    "What I Want",
    "Ordinary",
    "Manchild",
    "Golden",
    "The Fate Of Ophelia",
    "I Just Might",
    "Aperture",
    "Choosin' Texas",
    "DTMF",
    "Opalite",
    "Swim",
    "Drop Dead",
    "Janice STFU",
    "Hate That I Made You Love Me",
    "I Knew It, I Knew You",
    "Patient Zero",
}


def main() -> None:
    df = pd.read_csv(ISSUE)
    df["weeks_at_number_one"] = pd.to_numeric(df["weeks_at_number_one"], errors="coerce")
    df["rating_2"] = pd.to_numeric(df["rating_2"], errors="coerce")
    df["_art_year"] = pd.to_datetime(df["date"], utc=True, errors="coerce").dt.year

    spec = DatasetSpec(
        "billboard-hot-100",
        "Billboard Hot 100 Number Ones",
        "2025-08-26",
        "billboard.csv",
    )
    meta = {
        "metric": "weeks_at_number_one",
        "metric2": "rating_2",
        "label": "song",
        "category": "artist",
        "year": "_art_year",
    }
    charts = build_charts(df, spec, meta)
    by_id = {chart["id"]: chart for chart in charts}
    expected = [
        "chart1_trend",
        "chart2_leaders",
        "chart3_distribution",
        "chart4_gap",
        "chart5_scatter",
    ]
    missing = [cid for cid in expected if cid not in by_id]
    if missing or len(charts) != 5:
        raise SystemExit(f"STOP: expected charts 1–5, got {[c['id'] for c in charts]}")

    trend_x = list(by_id["chart1_trend"]["fig"].data[0].x)
    trend_y = [float(v) for v in by_id["chart1_trend"]["fig"].data[0].y]
    medians = {int(year): value for year, value in zip(trend_x, trend_y)}
    if medians.get(2025) != 6.5 or medians.get(2026) != 1.0:
        raise SystemExit(f"STOP: chart 1 medians {medians.get(2025)} / {medians.get(2026)}")

    leaders = list(by_id["chart2_leaders"]["fig"].data[0].y)
    if "Choosin' Texas" not in leaders or "A Bar Song (Tipsy)" not in leaders:
        raise SystemExit(f"STOP: chart 2 leaders missing updated songs: {leaders}")

    scatter = by_id["chart5_scatter"]["fig"].data[0]
    raw_text = scatter.text
    labels = [] if raw_text is None else [str(v) for v in list(raw_text)]
    leaked = sorted(set(labels) & NEW_TITLES)
    if leaked:
        raise SystemExit(f"STOP: chart 5 includes new No. 1s: {leaked}")
    if len(labels) != int(df["rating_2"].notna().sum()):
        raise SystemExit("STOP: chart 5 point count does not match rows with rating_2")

    note = by_id["chart5_scatter"]["fig"]
    note.add_annotation(
        text=CAPTION_NOTE,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.18,
        xanchor="left",
        yanchor="top",
        showarrow=False,
        font=dict(size=12, color="#6B6B6B", family="DM Sans, Helvetica, sans-serif"),
    )
    note.update_layout(margin=dict(l=72, r=32, t=88, b=96))

    CHARTS.mkdir(parents=True, exist_ok=True)
    for cid in expected:
        fig = by_id[cid]["fig"]
        save_chart(fig, CHARTS / f"{cid}.plotly.json", CHARTS / f"{cid}.png")
        if cid == "chart5_scatter":
            # save_chart tightens the PNG margin and would clip the caption note.
            png = go.Figure(fig)
            png.update_layout(title=dict(text=""), margin=dict(l=72, r=32, t=28, b=96))
            png.write_image(str(CHARTS / f"{cid}.png"), width=960, height=540, scale=2)
        html_name = f"{cid}.html"
        for folder in (CHARTS, DATA_CHARTS, PUBLIC_CHARTS):
            target = folder / html_name
            if target.exists() or folder == CHARTS:
                folder.mkdir(parents=True, exist_ok=True)
                fig.write_html(target, include_plotlyjs="cdn", full_html=True, config={"displayModeBar": False})
        shutil.copyfile(CHARTS / f"{cid}.plotly.json", DATA_CHARTS / f"{cid}.plotly.json")

    print("chart1 medians", {year: medians[year] for year in (2019, 2024, 2025, 2026) if year in medians})
    print("chart2", list(zip(leaders, by_id["chart2_leaders"]["fig"].data[0].x)))
    print("chart5 points", len(labels), "caption set")
    print("wrote", CHARTS)


if __name__ == "__main__":
    main()
