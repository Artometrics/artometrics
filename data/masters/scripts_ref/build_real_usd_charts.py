#!/usr/bin/env python3
"""Build inflation-adjusted (2025 USD) CSV mirrors and alternate Plotly chart files.

Does not overwrite nominal chart assets; writes *_real2025usd* siblings.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.cpi import deflate_to_base, load_annual_cpi, refresh_cpi_cache  # noqa: E402

BASE_YEAR = 2025
MANIFEST = ROOT / "docs/data-upgrades/REAL_USD_CHARTS.md"

# chart_id -> (data csv relative to repo, year column, value columns, article slug)
JOBS: list[dict] = [
    {
        "slug": "youtube",
        "chart_id": "chart4_youtube_ads_revenue_real2025usd",
        "nominal_chart": "chart4_youtube_ads_revenue",
        "csv": "articles/youtube/data/alphabet_youtube_ads_revenue.csv",
        "year_col": "fiscal_year",
        "value_cols": ["revenue_usd_millions"],
        "out_csv": "articles/youtube/data/alphabet_youtube_ads_revenue_real2025usd.csv",
        "title": f"YouTube ads revenue ({BASE_YEAR} USD billions, CPI-U adjusted)",
        "y_scale": 1 / 1000,
        "y_label": f"{BASE_YEAR} USD billions",
    },
    {
        "slug": "youtube",
        "chart_id": "chart8_youtube_vs_netflix_revenue_real2025usd",
        "nominal_chart": "chart8_youtube_vs_netflix_revenue",
        "csv": "articles/youtube/data/platform_revenue_fy2024.csv",
        "year_col": "fiscal_year",
        "value_cols": ["revenue_usd_billions"],
        "out_csv": "articles/youtube/data/platform_revenue_fy2024_real2025usd.csv",
        "title": f"FY2024 platform revenue ({BASE_YEAR} USD billions, CPI-U adjusted)",
        "y_scale": 1,
        "y_label": f"{BASE_YEAR} USD billions",
    },
    {
        "slug": "franchise",
        "chart_id": "chart9_disney_segments_fy2024_real2025usd",
        "nominal_chart": "chart9_disney_segments_fy2024",
        "csv": "articles/franchise/data/disney_segment_revenue_fy2024.csv",
        "year_col": "fiscal_year",
        "value_cols": ["revenue_usd_b"],
        "out_csv": "articles/franchise/data/disney_segment_revenue_fy2024_real2025usd.csv",
        "title": f"Disney segment revenue FY2024 ({BASE_YEAR} USD billions)",
        "y_scale": 1,
        "y_label": f"{BASE_YEAR} USD billions",
        "bar_labels": "segment",
    },
    {
        "slug": "padres",
        "chart_id": "chart3_tax_payroll_real2025usd",
        "nominal_chart": "chart3_tax_payroll",
        "csv": "articles/padres/data/cbt_payroll.csv",
        "year_col": "year",
        "value_cols": ["cbt_payroll_millions", "cba_threshold_millions"],
        "out_csv": "articles/padres/data/cbt_payroll_real2025usd.csv",
        "title": f"Padres CBT payroll vs threshold ({BASE_YEAR} USD millions)",
        "y_scale": 1,
        "y_label": f"{BASE_YEAR} USD millions",
        "multi_series": True,
    },
]


def write_deflated_csv(
    src: Path,
    dest: Path,
    year_col: str,
    value_cols: list[str],
    cpi: dict[int, float],
) -> None:
    with src.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return
    fieldnames = list(rows[0].keys()) + [
        f"{c}_real{BASE_YEAR}usd" for c in value_cols
    ]
    for row in rows:
        y = int(float(row[year_col]))
        for col in value_cols:
            raw = row.get(col, "").strip()
            if not raw:
                continue
            nominal = float(raw)
            row[f"{col}_real{BASE_YEAR}usd"] = round(
                deflate_to_base(nominal, y, BASE_YEAR, cpi), 4
            )
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def simple_bar_plotly(
    labels: list,
    values: list,
    title: str,
    y_label: str,
    source: str,
) -> dict:
    return {
        "data": [
            {
                "type": "bar",
                "x": labels,
                "y": values,
                "marker": {"color": "#2C3E6B"},
                "hovertemplate": "%{x}<br>%{y:.2f}<extra></extra>",
            }
        ],
        "layout": {
            "title": {"text": title},
            "yaxis": {"title": y_label},
            "annotations": [
                {
                    "text": f"{source} · CPI-U → {BASE_YEAR} USD · Artometrics",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0,
                    "y": -0.15,
                    "showarrow": False,
                    "font": {"size": 10},
                }
            ],
        },
        "config": {"displayModeBar": False},
    }


def write_plotly(job: dict, cpi: dict[int, float]) -> None:
    src = ROOT / job["csv"]
    out_csv = ROOT / job["out_csv"]
    write_deflated_csv(src, out_csv, job["year_col"], job["value_cols"], cpi)

    with out_csv.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    slug = job["slug"]
    chart_id = job["chart_id"]
    val_col = f"{job['value_cols'][0]}_real{BASE_YEAR}usd"
    scale = job.get("y_scale", 1)

    if job.get("multi_series"):
        years = [int(r[job["year_col"]]) for r in rows]
        payroll = [
            float(r.get(f"cbt_payroll_millions_real{BASE_YEAR}usd", 0)) * scale
            for r in rows
        ]
        thresh = [
            float(r.get(f"cba_threshold_millions_real{BASE_YEAR}usd") or 0) * scale
            for r in rows
            if r.get(f"cba_threshold_millions_real{BASE_YEAR}usd")
        ]
        fig = {
            "data": [
                {
                    "type": "bar",
                    "name": "CBT payroll",
                    "x": years,
                    "y": payroll,
                },
                {
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "CBA threshold",
                    "x": years[-len(thresh) :],
                    "y": thresh,
                },
            ],
            "layout": {
                "title": {"text": job["title"]},
                "yaxis": {"title": job["y_label"]},
            },
            "config": {"displayModeBar": False},
        }
    elif job.get("bar_labels") == "segment":
        labels = [r["segment"] for r in rows]
        values = [float(r[val_col]) * scale for r in rows]
        fig = simple_bar_plotly(
            labels,
            values,
            job["title"],
            job["y_label"],
            "BLS CPI-U via FRED CPIAUCSL",
        )
    elif job["slug"] == "youtube" and "platform" in job["csv"]:
        labels = [r["company"] for r in rows]
        values = [float(r[val_col]) * scale for r in rows]
        fig = simple_bar_plotly(
            labels, values, job["title"], job["y_label"], "BLS CPI-U via FRED CPIAUCSL"
        )
    else:
        labels = [r[job["year_col"]] for r in rows]
        values = [float(r[val_col]) * scale for r in rows]
        fig = simple_bar_plotly(
            labels, values, job["title"], job["y_label"], "BLS CPI-U via FRED CPIAUCSL"
        )

    for base in (
        ROOT / f"articles/{slug}/charts",
        ROOT / f"public/data/articles/{slug}/charts",
    ):
        base.mkdir(parents=True, exist_ok=True)
        (base / f"{chart_id}.plotly.json").write_text(
            json.dumps(fig, indent=2), encoding="utf-8"
        )


def main() -> None:
    if not (ROOT / "data/reference/cpi/cpi_annual.csv").exists():
        refresh_cpi_cache()
    cpi = load_annual_cpi()
    touched: list[str] = []
    for job in JOBS:
        write_plotly(job, cpi)
        touched.append(
            f"- `{job['slug']}`: nominal `{job['nominal_chart']}` → alternate `{job['chart_id']}` "
            f"(data `{job['out_csv']}`)"
        )

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        "# Real-dollar (2025 USD) chart siblings\n\n"
        "Nominal charts unchanged. CPI-U annual average; base year **2025**.\n\n"
        + "\n".join(touched)
        + "\n\nRegenerate: `python3 scripts/data/build_real_usd_charts.py`\n",
        encoding="utf-8",
    )
    print(f"Built {len(JOBS)} real-USD chart siblings; manifest {MANIFEST}")


if __name__ == "__main__":
    main()
