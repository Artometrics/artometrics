#!/usr/bin/env python3
"""Build YouTube R2 charts. Run from repo root: python3 articles/youtube/scripts/build_brief.py"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

ROOT = Path(__file__).resolve().parents[3]
ARTICLE = ROOT / "articles/youtube"
DATA = ARTICLE / "data"
CHARTS = ARTICLE / "charts"
PUBLIC_DATA = ROOT / "public/data/articles/youtube"
PUBLIC_CHARTS = PUBLIC_DATA / "charts"
PUBLIC_IMG = ROOT / "public/images/content/articles/youtube/charts"

RED = "#E60000"
BLUE = "#2C3E6B"
INK = "#1C1C1E"
GRAY = "#6B6B6B"
CREAM = "#F2F0EB"
GRID = "#E6E6E6"

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": False,
    "doubleClick": False,
}


def ensure_dirs() -> None:
    for d in (CHARTS, PUBLIC_DATA, PUBLIC_CHARTS, PUBLIC_IMG):
        d.mkdir(parents=True, exist_ok=True)


def base_layout(title: str, source: str, height: int = 480) -> dict:
    return dict(
        title=dict(text=title, font=dict(family="DM Sans, Helvetica, Arial", size=18, color=INK)),
        paper_bgcolor=CREAM,
        plot_bgcolor=CREAM,
        font=dict(family="DM Sans, Helvetica, Arial", color=INK, size=12),
        margin=dict(l=60, r=40, t=70, b=80),
        height=height,
        annotations=[
            dict(
                text=f"{source} · Artometrics",
                xref="paper",
                yref="paper",
                x=0,
                y=-0.18,
                showarrow=False,
                font=dict(size=10, color=GRAY),
                align="left",
            )
        ],
    )


def write_chart(fig: go.Figure, chart_id: str) -> None:
    built = json.loads(pio.to_json(fig, validate=False))
    built["config"] = PLOTLY_CONFIG
    for path in (
        CHARTS / f"{chart_id}.plotly.json",
        PUBLIC_CHARTS / f"{chart_id}.plotly.json",
    ):
        path.write_text(json.dumps(built, indent=2))
    for path in (
        CHARTS / f"{chart_id}.png",
        PUBLIC_IMG / f"{chart_id}.png",
    ):
        fig.write_image(str(path), width=1200, height=fig.layout.height or 480, scale=2)


def chart4_youtube_ads_revenue() -> None:
    df = pd.read_csv(DATA / "alphabet_youtube_ads_revenue.csv")
    fig = go.Figure(
        go.Bar(
            x=df["fiscal_year"],
            y=df["revenue_usd_millions"] / 1000,
            marker_color=[BLUE] * (len(df) - 1) + [RED],
            text=[f"${v:.1f}B" for v in df["revenue_usd_millions"] / 1000],
            textposition="outside",
            hovertemplate="FY%{x}<br>$%{y:.2f}B<extra>YouTube ads</extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "YouTube advertising revenue crossed $36B in FY2024",
            "Source: Alphabet Form 10-K — YouTube ads (USD billions)",
        ),
        xaxis=dict(title="", tickmode="linear", dtick=1, gridcolor=GRID),
        yaxis=dict(title="USD billions", gridcolor=GRID, zeroline=False),
    )
    write_chart(fig, "chart4_youtube_ads_revenue")


def chart5_nielsen_tv_share() -> None:
    df = pd.read_csv(DATA / "nielsen_youtube_tv_screen_share.csv")
    x_pos = list(range(len(df)))
    last = x_pos[-1]
    # Sit the method-change marker after August 2026 and leave the area after it empty.
    marker_x = last + 0.45
    fig = go.Figure(
        go.Scatter(
            x=x_pos,
            y=df["share_pct"],
            mode="lines+markers",
            line=dict(color=RED, width=3),
            marker=dict(size=10, color=BLUE, line=dict(width=2, color=INK)),
            customdata=df["month_label"],
            hovertemplate="%{customdata}<br>%{y:.1f}% of U.S. TV (TV screen)<extra></extra>",
        )
    )
    layout = base_layout(
        "YouTube’s TV-screen share keeps climbing in Nielsen’s Gauge",
        "Source: Nielsen Media Distributor Gauge press releases",
        height=520,
    )
    layout["margin"] = dict(l=60, r=72, t=70, b=120)
    layout["annotations"][0]["y"] = -0.20
    layout["annotations"][0]["xanchor"] = "left"
    layout["annotations"].append(
        dict(
            text="August 2026 was a five-week interval",
            xref="paper",
            yref="paper",
            x=0,
            y=-0.30,
            showarrow=False,
            font=dict(family="DM Sans, Helvetica, Arial", size=10, color=GRAY),
            align="left",
            xanchor="left",
        )
    )
    fig.update_layout(
        **layout,
        xaxis=dict(
            title="",
            gridcolor=GRID,
            tickmode="array",
            tickvals=x_pos,
            ticktext=df["month_label"].tolist(),
            range=[-0.35, last + 1.2],
        ),
        yaxis=dict(title="Share of total U.S. TV usage (%)", gridcolor=GRID, zeroline=False),
    )
    # Add the marker after layout so Plotly does not drop the source annotation.
    fig.add_vline(
        x=marker_x,
        line_dash="dash",
        line_color=GRAY,
        line_width=1.5,
    )
    fig.add_annotation(
        x=marker_x,
        y=0.55,
        yref="paper",
        text="Nielsen method change from Sep 2026",
        textangle=-90,
        showarrow=False,
        font=dict(family="DM Sans, Helvetica, Arial", size=11, color=INK),
        xanchor="center",
        yanchor="middle",
        xshift=12,
    )
    write_chart(fig, "chart5_nielsen_tv_share")


def chart6_platform_tv_share() -> None:
    df = pd.read_csv(DATA / "nielsen_tv_share_july_2025.csv").sort_values("share_pct")
    colors = [BLUE, GRAY, RED] if len(df) == 3 else [BLUE] * len(df)
    colors[df["distributor"].tolist().index("YouTube")] = RED
    fig = go.Figure(
        go.Bar(
            y=df["distributor"],
            x=df["share_pct"],
            orientation="h",
            marker_color=colors,
            text=[f"{v:.1f}%" for v in df["share_pct"]],
            textposition="outside",
            hovertemplate="%{y}<br>%{x:.1f}% of TV<extra>July 2025</extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "On the TV screen, YouTube beat Disney and Netflix in July 2025",
            "Source: Nielsen Media Distributor Gauge, July 2025",
            height=420,
        ),
        xaxis=dict(title="Share of U.S. TV usage (%)", gridcolor=GRID, range=[0, 16]),
        yaxis=dict(title=""),
    )
    write_chart(fig, "chart6_platform_tv_share")


def chart7_creator_economy_tam() -> None:
    df = pd.read_csv(DATA / "creator_economy_tam_goldman.csv")
    fig = go.Figure()
    obs = df[df["metric_type"].str.startswith("observed")]
    proj = df[df["metric_type"].str.startswith("projection")]
    fig.add_trace(
        go.Scatter(
            x=obs["year"],
            y=obs["tam_usd_billions"],
            mode="markers+lines",
            name="Goldman estimate",
            line=dict(color=BLUE, width=2, dash="solid"),
            marker=dict(size=12, color=BLUE),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[obs["year"].iloc[-1], proj["year"].iloc[-1]],
            y=[obs["tam_usd_billions"].iloc[-1], proj["tam_usd_billions"].iloc[-1]],
            mode="lines+markers",
            name="Projection",
            line=dict(color=RED, width=2, dash="dot"),
            marker=dict(size=12, color=RED),
        )
    )
    fig.update_layout(
        **base_layout(
            "Goldman Sachs sizes the creator economy near half a trillion by 2027",
            "Source: Goldman Sachs Research, Apr 2023",
        ),
        showlegend=False,
        xaxis=dict(title="Year", dtick=1, gridcolor=GRID),
        yaxis=dict(title="TAM (USD billions)", gridcolor=GRID),
    )
    write_chart(fig, "chart7_creator_economy_tam")


def chart8_youtube_vs_netflix_revenue() -> None:
    df = pd.read_csv(DATA / "platform_revenue_fy2024.csv")
    fig = go.Figure(
        go.Bar(
            x=df["metric_label"],
            y=df["revenue_usd_billions"],
            marker_color=[RED, BLUE],
            text=[f"${v:.1f}B" for v in df["revenue_usd_billions"]],
            textposition="outside",
            hovertemplate="%{x}<br>$%{y:.2f}B<extra>FY2024</extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "YouTube ads and Netflix subscriptions converged near $39B in FY2024",
            "Source: Alphabet & Netflix Form 10-K FY2024 (different revenue definitions)",
            height=440,
        ),
        xaxis=dict(title="", gridcolor=GRID),
        yaxis=dict(title="USD billions", gridcolor=GRID, zeroline=False),
    )
    write_chart(fig, "chart8_youtube_vs_netflix_revenue")


def chart9_shorts_ad_share_projection() -> None:
    df = pd.read_csv(DATA / "goldman_youtube_shorts_ad_share.csv")
    fig = go.Figure(
        go.Bar(
            x=df["year"].astype(str),
            y=df["pct_of_youtube_ads"],
            marker_color=[BLUE, RED],
            text=[f"{v:.1f}%" for v in df["pct_of_youtube_ads"]],
            textposition="outside",
            name="Share of YouTube ads",
        )
    )
    fig.update_layout(
        **base_layout(
            "Goldman projected Shorts ads rising to 26% of YouTube ad revenue by 2027",
            "Source: Goldman Sachs Research, Apr 2023 (estimates)",
        ),
        xaxis=dict(title="Year", gridcolor=GRID),
        yaxis=dict(title="Shorts ads as % of YouTube ads", gridcolor=GRID),
    )
    write_chart(fig, "chart9_shorts_ad_share")


def chart10_ypp_split() -> None:
    df = pd.read_csv(DATA / "ypp_revenue_share.csv")
    fig = go.Figure()
    for i, row in df.iterrows():
        fig.add_trace(
            go.Bar(
                name=row["format"],
                x=["Creator share", "Platform share"],
                y=[row["creator_share_pct"], row["platform_share_pct"]],
                marker_color=[RED, BLUE],
                text=[f"{row['creator_share_pct']}%", f"{row['platform_share_pct']}%"],
                textposition="inside",
                offsetgroup=row["format"],
            )
        )
    fig.update_layout(
        barmode="group",
        **base_layout(
            "Partner Program splits favor long-form creators on watch-page ads",
            "Source: Google YouTube Help & YouTube Blog (YPP terms)",
            height=460,
        ),
        xaxis=dict(title="", gridcolor=GRID),
        yaxis=dict(title="Revenue share (%)", gridcolor=GRID, range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    write_chart(fig, "chart10_ypp_split")


def sync_data_and_assets() -> None:
    """Copy economics CSVs and logos into public/data mirror."""
    dest = PUBLIC_DATA
    for name in DATA.glob("*.csv"):
        shutil.copy2(name, dest / name.name)
    shutil.copy2(DATA / "SOURCE.txt", dest / "SOURCE.txt")
    if (DATA / "h3.csv").exists():
        shutil.copy2(DATA / "h3.csv", dest / "h3.csv")
    assets_src = ARTICLE / "assets"
    assets_dest = ROOT / "public/images/content/articles/youtube/assets"
    assets_dest.mkdir(parents=True, exist_ok=True)
    for logo in ("logo_youtube.svg", "logo_google.svg", "logo_netflix.svg", "logo_twitch.svg"):
        p = assets_src / logo
        if p.exists():
            shutil.copy2(p, assets_dest / logo)


def main() -> None:
    ensure_dirs()
    chart4_youtube_ads_revenue()
    chart5_nielsen_tv_share()
    chart6_platform_tv_share()
    chart7_creator_economy_tam()
    chart8_youtube_vs_netflix_revenue()
    chart9_shorts_ad_share_projection()
    chart10_ypp_split()
    sync_data_and_assets()
    # Preserve legacy chart ids 1–3 (H3 case study); new charts are 4–10.
    print("Built charts chart4–chart10 under", CHARTS)


if __name__ == "__main__":
    main()
