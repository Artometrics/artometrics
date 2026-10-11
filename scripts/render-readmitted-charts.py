#!/usr/bin/env python3
"""Export readmitted charts as PNG + Plotly JSON for repo and site."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_CHARTS = ROOT / "articles/readmitted/charts"
SITE_DATA = ROOT / "public/data/articles/readmitted/charts"
SITE_IMG = ROOT / "public/images/content/articles/readmitted/charts"

ART_CREAM = "#F2F0EB"
ART_DARK = "#1C1C1E"
ART_HIGHLIGHT = "#C0392B"
ART_SECONDARY = "#1C1C1E"
ART_MID = "#6B6B6B"
ART_MUTED = "#D5D5D5"
FONT = "DM Sans, Helvetica, Arial, sans-serif"

BAR_GRADIENT = [
    "#1C1C1E",
    "#2A2A2A",
    "#3A3A3A",
    "#4A4A4A",
    "#5C5C5C",
    "#6E3A34",
    "#8B3228",
    "#A93226",
    "#C0392B",
    "#E74C3C",
]

TIER_COLORS = {
    "No Penalty": "#1C1C1E",
    "Low": "#6B6B6B",
    "Medium": "#B03A2E",
    "High": "#C0392B",
}

NAT_AVG_PCT = 48.1
WORDMARK_FONT = "Georgia, Times New Roman, serif"


def brand_annotation() -> dict:
    return dict(
        x=0.99,
        y=0.01,
        xref="paper",
        yref="paper",
        text="Artometrics",
        showarrow=False,
        xanchor="right",
        yanchor="bottom",
        font=dict(family=WORDMARK_FONT, size=11, color=ART_MID),
    )


def takeaway_strip(takeaway: str) -> tuple[list[dict], list[dict]]:
    """Economist-style red header band + supporting layout offsets."""
    shapes = [
        dict(
            type="rect",
            xref="paper",
            yref="paper",
            x0=0,
            x1=1,
            y0=1.0,
            y1=1.12,
            fillcolor=ART_HIGHLIGHT,
            line=dict(width=0),
            layer="below",
        )
    ]
    annotations = [
        dict(
            x=0.02,
            y=1.06,
            xref="paper",
            yref="paper",
            text=f"<span style='color:#FFFFFF;font-size:11px'>{takeaway}</span>",
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(family=FONT, size=11, color="#FFFFFF"),
        )
    ]
    return shapes, annotations


def base_layout(title: str, subtitle: str = "", takeaway: str = "", **kwargs) -> dict:
    strip_shapes: list[dict] = []
    strip_annotations: list[dict] = []
    top_margin = 96 if takeaway else 72
    if takeaway:
        strip_shapes, strip_annotations = takeaway_strip(takeaway)
        top_margin = 118

    layout = dict(
        title=dict(
            text=title,
            x=0,
            xanchor="left",
            y=0.98,
            yanchor="top",
            font=dict(family=FONT, size=16, color=ART_DARK),
        ),
        paper_bgcolor=ART_CREAM,
        plot_bgcolor=ART_CREAM,
        font=dict(color=ART_DARK, family=FONT, size=12),
        margin=dict(l=88, r=48, t=top_margin if not subtitle else top_margin + 16, b=72),
        annotations=[*strip_annotations, brand_annotation()],
        shapes=strip_shapes,
    )
    if subtitle:
        layout["annotations"].insert(
            len(strip_annotations),
            dict(
                x=0,
                y=1.0,
                xref="paper",
                yref="paper",
                text=subtitle,
                showarrow=False,
                xanchor="left",
                yanchor="bottom",
                font=dict(family=FONT, size=11, color=ART_MID),
            ),
        )
    extra_shapes = kwargs.pop("shapes", [])
    layout["shapes"] = [*layout.get("shapes", []), *extra_shapes]
    extra_annotations = kwargs.pop("annotations", [])
    layout["annotations"] = [*layout["annotations"], *extra_annotations]
    layout.update(kwargs)
    return layout


def save_chart(fig: go.Figure, name: str, height: int = 700) -> None:
    for dest in [ARTICLE_CHARTS, SITE_DATA]:
        dest.mkdir(parents=True, exist_ok=True)
        pio.write_json(fig, dest / f"{name}.plotly.json")

    for dest in [ARTICLE_CHARTS, SITE_IMG]:
        dest.mkdir(parents=True, exist_ok=True)
        fig.write_image(dest / f"{name}.png", width=1200, height=height, scale=2)
        print(f"Wrote {name} assets")


def chart1(state_df: pd.DataFrame) -> go.Figure:
    flag = state_df["above_nat_avg"]
    if flag.dtype == object:
        flag = flag.astype(str).str.upper().eq("TRUE")
    df = state_df[flag].sort_values("pct_penalized")
    n = len(df)
    colors = BAR_GRADIENT[:n] if n <= len(BAR_GRADIENT) else BAR_GRADIENT
    if n > len(BAR_GRADIENT):
        colors = [BAR_GRADIENT[int(i * (len(BAR_GRADIENT) - 1) / max(n - 1, 1))] for i in range(n)]
    colors[-1] = ART_HIGHLIGHT  # leader NJ

    fig = go.Figure(
        go.Bar(
            x=df["pct_penalized"],
            y=df["state"],
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v:.1f}%" for v in df["pct_penalized"]],
            textposition="outside",
            textfont=dict(family=FONT, size=10, color=ART_DARK),
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>%{x:.1f}% of pairs penalized<extra></extra>",
        )
    )

    annotations = [
        dict(
            x=NAT_AVG_PCT,
            y=1.02,
            xref="x",
            yref="paper",
            text=f"National avg ({NAT_AVG_PCT}%)",
            showarrow=False,
            xanchor="center",
            yanchor="bottom",
            font=dict(family=FONT, size=9, color=ART_SECONDARY),
        ),
        dict(
            x=df["pct_penalized"].iloc[-1],
            y=df["state"].iloc[-1],
            xref="x",
            yref="y",
            text="NJ leads at 65.4%",
            showarrow=True,
            arrowhead=2,
            arrowsize=0.8,
            arrowwidth=1,
            arrowcolor=ART_HIGHLIGHT,
            ax=40,
            ay=-28,
            font=dict(family=FONT, size=9, color=ART_HIGHLIGHT),
        ),
    ]

    fig.update_layout(
        **base_layout(
            "<b>Which <span style='color:#C0392B;'>States</span> Have the Most Penalized Hospitals?</b>",
            "Above-average states only — share of hospital-condition pairs with ERR > 1.0",
            takeaway="Geography isn't destiny — wealthy states lead the penalty list alongside the rural South",
            xaxis=dict(
                title="% of Hospital-Condition Pairs with ERR > 1.0",
                range=[0, max(df["pct_penalized"]) * 1.14],
                gridcolor=ART_MUTED,
                gridwidth=0.5,
                zeroline=False,
            ),
            yaxis=dict(title="", categoryorder="array", categoryarray=list(df["state"])),
            shapes=[
                dict(
                    type="line",
                    x0=NAT_AVG_PCT,
                    x1=NAT_AVG_PCT,
                    y0=0,
                    y1=1,
                    yref="paper",
                    line=dict(color=ART_SECONDARY, dash="dash", width=1.5),
                )
            ],
            annotations=annotations,
            height=520 + n * 22,
        )
    )
    return fig


def chart2(condition_df: pd.DataFrame) -> go.Figure:
    df = condition_df.sort_values("avg_err")

    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[1.0, row["avg_err"]],
                y=[row["condition"], row["condition"]],
                mode="lines",
                line=dict(color=ART_MUTED, width=2),
                showlegend=False,
                hoverinfo="skip",
            )
        )
    fig.add_trace(
        go.Scatter(
            x=df["avg_err"],
            y=df["condition"],
            mode="markers+text",
            marker=dict(color=ART_HIGHLIGHT, size=12, line=dict(width=1, color=ART_DARK)),
            text=[f"{v:.5f}" for v in df["avg_err"]],
            textposition="middle right",
            textfont=dict(family=FONT, size=10, color=ART_DARK),
            hovertemplate="<b>%{y}</b><br>ERR: %{x:.5f}<extra></extra>",
            showlegend=False,
        )
    )

    annotations = [
        dict(
            x=1.00485,
            y="Hip/Knee",
            xref="x",
            yref="y",
            text="Nearly 2× the excess<br>of the next condition",
            showarrow=True,
            arrowhead=2,
            arrowsize=0.8,
            arrowwidth=1,
            arrowcolor=ART_HIGHLIGHT,
            ax=55,
            ay=-35,
            font=dict(family=FONT, size=9, color=ART_HIGHLIGHT),
        ),
        dict(
            x=1.0,
            y=1.02,
            xref="x",
            yref="paper",
            text="ERR = 1.0 (no excess)",
            showarrow=False,
            xanchor="center",
            yanchor="bottom",
            font=dict(family=FONT, size=9, color=ART_MID),
        ),
    ]

    fig.update_layout(
        **base_layout(
            "<b>The <span style='color:#C0392B;'>Hip/Knee</span> Problem: ERR by Condition</b>",
            "All six HRRP conditions exceed 1.0 — but the spread is measured in thousandths",
            takeaway="Elective joint surgery — not heart attacks — carries the highest excess readmission ratio",
            xaxis=dict(
                title="Average Excess Readmission Ratio (ERR)",
                range=[0.9998, 1.0055],
                tickformat=".4f",
                gridcolor=ART_MUTED,
                gridwidth=0.5,
            ),
            yaxis=dict(title=""),
            shapes=[
                dict(
                    type="line",
                    x0=1,
                    x1=1,
                    y0=0,
                    y1=1,
                    yref="paper",
                    line=dict(color=ART_DARK, width=1),
                )
            ],
            annotations=annotations,
            height=420,
        )
    )
    return fig


def chart3(own_df: pd.DataFrame) -> go.Figure:
    grouped = (
        own_df.groupby(["ownership_group", "penalty_tier"], as_index=False)["n"]
        .sum()
        .assign(
            pct=lambda d: d.groupby("ownership_group")["n"].transform(lambda s: s / s.sum())
        )
    )
    ownership_order = ["Non-Profit", "Government", "For-Profit"]
    tier_order = ["No Penalty", "Low", "Medium", "High"]

    fig = go.Figure()
    for tier in tier_order:
        part = grouped[grouped["penalty_tier"] == tier]
        fig.add_trace(
            go.Bar(
                name=tier,
                y=part["ownership_group"],
                x=part["pct"],
                orientation="h",
                marker_color=TIER_COLORS[tier],
                hovertemplate="<b>%{y}</b><br>"
                + tier
                + ": %{x:.1%}<extra></extra>",
            )
        )

    for_profit_high = grouped[
        (grouped["ownership_group"] == "For-Profit") & (grouped["penalty_tier"] == "High")
    ]["pct"]
    high_pct = float(for_profit_high.iloc[0]) if len(for_profit_high) else 0

    annotations = [
        dict(
            x=0.98,
            y="For-Profit",
            xref="paper",
            yref="y",
            text=f"High-tier share: {high_pct:.1%}",
            showarrow=False,
            xanchor="right",
            font=dict(family=FONT, size=9, color=ART_HIGHLIGHT),
        ),
    ]

    fig.update_layout(
        **base_layout(
            "<b><span style='color:#C0392B;'>For-Profit</span> Hospitals Carry More Penalty Weight</b>",
            "Penalty tier distribution by ownership — HCA, Tenet, and Steward sit in the for-profit column",
            takeaway="For-profits carry more penalty weight, but every ownership type still has a majority in the no-penalty band",
            barmode="stack",
            xaxis=dict(
                title="Share of Hospital-Condition Pairs",
                tickformat=".0%",
                range=[0, 1],
                gridcolor=ART_MUTED,
                gridwidth=0.5,
            ),
            yaxis=dict(
                title="",
                categoryorder="array",
                categoryarray=ownership_order,
            ),
            legend=dict(
                title=dict(text="Penalty Tier", font=dict(size=10)),
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=10),
            ),
            annotations=annotations,
            height=380,
        )
    )
    return fig


def chart4(state_df: pd.DataFrame) -> go.Figure:
    df = state_df.sort_values("avg_err").tail(15)
    colors = BAR_GRADIENT[: len(df)]
    if len(df) > len(BAR_GRADIENT):
        colors = [BAR_GRADIENT[int(i * (len(BAR_GRADIENT) - 1) / max(len(df) - 1, 1))] for i in range(len(df))]
    colors[-1] = ART_HIGHLIGHT

    fig = go.Figure(
        go.Bar(
            x=df["avg_err"],
            y=df["state"],
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v:.4f}" for v in df["avg_err"]],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Avg ERR %{x:.5f}<extra></extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "Average excess readmission ratio by state (top 15)",
            "Intensity of excess above CMS expected line (ERR = 1.0)",
            takeaway="Massachusetts runs hotter on intensity even where New Jersey leads on breadth",
            xaxis=dict(title="Average ERR", gridcolor=ART_MUTED, gridwidth=0.5),
            yaxis=dict(title="", categoryorder="array", categoryarray=list(df["state"])),
            shapes=[
                dict(
                    type="line",
                    x0=1,
                    x1=1,
                    y0=0,
                    y1=1,
                    yref="paper",
                    line=dict(color=ART_DARK, dash="dot", width=1),
                )
            ],
            height=520,
        )
    )
    return fig


def chart5(own_df: pd.DataFrame) -> go.Figure:
    order = ["Government", "Non-Profit", "For-Profit"]
    rows = []
    for og in order:
        g = own_df[own_df["ownership_group"] == og]
        total = g["n"].sum()
        high = g.loc[g["penalty_tier"] == "High", "n"].sum()
        rows.append({"ownership_group": og, "pct_high": 100 * high / total if total else 0})
    grouped = pd.DataFrame(rows)
    bar_colors = ["#1C1C1E", "#6B6B6B", ART_HIGHLIGHT]

    fig = go.Figure(
        go.Bar(
            x=grouped["ownership_group"],
            y=grouped["pct_high"],
            marker=dict(color=bar_colors),
            text=[f"{v:.1f}%" for v in grouped["pct_high"]],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>%{x}</b><br>High tier %{y:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "Share of hospital–condition pairs in High penalty tier by ownership",
            "High tier = pairs farthest above CMS expected readmissions",
            takeaway="For-profit hospitals carry the highest share of High-tier penalty pairs",
            yaxis=dict(title="High-tier share (%)", gridcolor=ART_MUTED, gridwidth=0.5),
            xaxis=dict(title="Ownership"),
            height=480,
        )
    )
    return fig


def chart6(timeline_df: pd.DataFrame) -> go.Figure:
    df = timeline_df.dropna(subset=["share_hospitals_penalty_1pct_or_more"])
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["fiscal_year"],
            y=df["max_penalty_pct"],
            name="Max penalty cap (%)",
            marker_color=ART_SECONDARY,
            opacity=0.35,
            yaxis="y2",
            hovertemplate="FY %{x}<br>Cap %{y}%<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["fiscal_year"],
            y=df["share_hospitals_penalty_1pct_or_more"],
            mode="lines+markers",
            name="Hospitals penalized ≥1%",
            line=dict(color=ART_HIGHLIGHT, width=3),
            marker=dict(size=9),
            hovertemplate="FY %{x}<br>%{y:.1f}% of hospitals ≥1% penalty<extra></extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "<b>HRRP penalty cap vs. hospitals paying ≥1%</b>",
            "Cap reached 3% in FY2015; severe penalties ticked up again in FY2026 preliminary data",
            takeaway="CMS can dock up to 3% of every Medicare payment — but most hospitals pay far less than the cap",
            xaxis=dict(title="Medicare fiscal year", dtick=1),
            yaxis=dict(title="Share of hospitals with ≥1% payment reduction (%)", gridcolor=ART_MUTED),
            yaxis2=dict(title="Maximum penalty cap (%)", overlaying="y", side="right", range=[0, 4], showgrid=False),
            legend=dict(orientation="h", y=1.12, x=1, xanchor="right"),
            height=460,
        )
    )
    return fig


def chart7(trends_df: pd.DataFrame) -> go.Figure:
    df = trends_df[trends_df["condition"].isin(["Heart Failure", "Pneumonia", "AMI"])]
    fig = go.Figure()
    palette = {"Heart Failure": ART_HIGHLIGHT, "Pneumonia": ART_DARK, "AMI": ART_SECONDARY}
    for cond, sub in df.groupby("condition"):
        fig.add_trace(
            go.Scatter(
                x=sub["report_year"],
                y=sub["national_readmit_rate_pct"],
                mode="lines+markers",
                name=cond,
                line=dict(color=palette.get(cond, ART_MID), width=2.5),
                hovertemplate=cond + "<br>%{y:.1f}% in %{x}<extra></extra>",
            )
        )
    fig.update_layout(
        **base_layout(
            "National Medicare readmission rates fell after HRRP — then plateaued",
            "AMI, heart failure, and pneumonia; 2012–2015 from Zuckerman et al. (NEJM 2016); 2024 from CMS extract",
            takeaway="Readmissions dropped in the program's first years — the debate is what happened to mortality and observation stays next",
            xaxis=dict(title="Report year", dtick=1),
            yaxis=dict(title="National readmission rate (%)", gridcolor=ART_MUTED),
            legend=dict(orientation="h", y=1.12, x=0),
            height=480,
        )
    )
    return fig


def chart8(proxy_df: pd.DataFrame) -> go.Figure:
    df = proxy_df.sort_values("pct_penalized")
    fig = go.Figure(
        go.Bar(
            x=df["safety_net_proxy"],
            y=df["pct_penalized"],
            marker=dict(color=[ART_DARK, ART_HIGHLIGHT]),
            text=[f"{v:.1f}%" for v in df["pct_penalized"]],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>%{x}</b><br>%{y:.1f}% penalized<extra></extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "Safety-net name proxy vs. other acute-care hospitals",
            "Government/non-profit acute hospitals with County/Public/Memorial/Safety in the name (CMS extract)",
            takeaway="A crude safety-net label barely moves penalty share — peer grouping and dual-eligible mix matter more",
            yaxis=dict(title="% of pairs with ERR > 1.0", gridcolor=ART_MUTED),
            xaxis=dict(title=""),
            height=420,
        )
    )
    return fig


def main() -> None:
    data_dir = ROOT / "articles/readmitted/data"
    if not data_dir.exists():
        data_dir = ROOT / "public/data/articles/readmitted/data"

    state_df = pd.read_csv(data_dir / "hrrp_state_summary.csv")
    own_df = pd.read_csv(data_dir / "hrrp_ownership_condition.csv")
    cond_df = pd.read_csv(data_dir / "hrrp_condition_err.csv")
    timeline_df = pd.read_csv(data_dir / "hrrp_penalty_timeline.csv")
    trends_df = pd.read_csv(data_dir / "hrrp_national_readmit_trends.csv")
    proxy_df = pd.read_csv(data_dir / "hrrp_safety_net_proxy.csv")

    global NAT_AVG_PCT
    NAT_AVG_PCT = round(100 * (cond_df["n"].sum() and state_df["n_penalized"].sum() / state_df["n"].sum()), 2)

    save_chart(chart1(state_df), "chart1_states_penalized", height=900)
    save_chart(chart2(cond_df), "chart2_err_by_condition", height=520)
    save_chart(chart3(own_df), "chart3_penalty_by_ownership", height=420)
    save_chart(chart4(state_df), "chart4_state_avg_err", height=620)
    save_chart(chart5(own_df), "chart5_high_penalty_by_ownership", height=480)
    save_chart(chart6(timeline_df), "chart6_penalty_timeline", height=460)
    save_chart(chart7(trends_df), "chart7_national_readmit_trends", height=480)
    save_chart(chart8(proxy_df), "chart8_safety_net_proxy", height=420)

    # Sync CSVs to public data folder for downloads
    pub_csv = ROOT / "public/data/articles/readmitted/data"
    pub_csv.mkdir(parents=True, exist_ok=True)
    for path in data_dir.glob("*.csv"):
        if path.name.startswith("raw_"):
            continue
        dest = pub_csv / path.name
        dest.write_bytes(path.read_bytes())


if __name__ == "__main__":
    main()
