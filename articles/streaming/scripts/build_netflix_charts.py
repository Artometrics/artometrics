#!/usr/bin/env python3
"""Download Netflix's free H1 2026 files and build the three streaming charts.

Sources (no API key):
  What We Watched, January–June 2026, published July 16, 2026
    https://about.netflix.com/news/what-we-watched-the-first-half-of-2026
  Global Top 10, all-weeks-global.tsv
    https://www.netflix.com/tudum/top10/data/all-weeks-global.tsv

Named titles exclude the "Other Shows" and "Other Movies" rows. The census
from the workbook downloaded for this build is 17,370 (8,193 shows and
9,177 movies). Global Top 10 rows are the weeks ending January 4 through
June 28, 2026. Titles are matched by name. One charted name does not match:
the Top 10 file lists "Furies: Season 2: : Resistance" (a double colon) and
the engagement report lists "Furies: Season 2: Furies: Resistance".

Run from the repo root:
  python3 articles/streaming/scripts/build_netflix_charts.py
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
import urllib.request
from collections import defaultdict
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "articles" / "streaming" / "data"
HTML_JSON_DIRS = [
    ROOT / "articles" / "streaming" / "charts",
    DATA / "charts",
    ROOT / "public" / "data" / "articles" / "streaming" / "charts",
]
PNG_DIRS = [
    ROOT / "articles" / "streaming" / "charts",
    ROOT / "public" / "images" / "content" / "articles" / "streaming" / "charts",
]
JPG_DIRS = [
    ROOT / "public" / "img" / "images" / "content" / "articles" / "streaming" / "charts",
]

ANNOUNCEMENT = "https://about.netflix.com/news/what-we-watched-the-first-half-of-2026"
TOP10_URL = "https://www.netflix.com/tudum/top10/data/all-weeks-global.tsv"
WEEK_START = "2026-01-04"
WEEK_END = "2026-06-28"
FURIES_CHART = "Furies: Season 2: : Resistance"
FURIES_REPORT = "Furies: Season 2: Furies: Resistance"
OTHERS = {"Other Shows", "Other Movies"}
CURVE_PCTS = [0.1, 0.5, 1, 2, 5, 10, 20, 30, 50, 75, 100]

RED = "#E60000"
BLUE = "#0047FF"
INK = "#1C1C1E"
GRAY = "#6B6B6B"
LIGHT = "#C8C8C8"
GRID = "#E6E6E6"
PAPER = "#FAFAF8"
UA = "Artometrics/streaming-charts (research; +https://artometrics.com/methodology/)"


def fetch(url: str) -> bytes:
    last_error: Exception | None = None
    for _ in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as response:
                return response.read()
        except Exception as error:  # noqa: BLE001 — retry transient download cuts
            last_error = error
    sys.exit(f"Download failed for {url}: {last_error}")


def xlsx_url() -> str:
    html = fetch(ANNOUNCEMENT).decode("utf-8", "replace")
    found = re.findall(r"https?://[^\"']+\.xlsx", html)
    if not found:
        sys.exit("No .xlsx link on the What We Watched announcement page.")
    return found[0]


def norm(value: str) -> str:
    text = unicodedata.normalize("NFKC", str(value))
    text = (
        text.replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
        .replace("\u00a0", " ")
        .replace("\u3000", " ")
    )
    return re.sub(r"\s+", " ", text).strip().casefold()


def english_name(title: str) -> str:
    return str(title).split(" // ")[0].replace("\u00a0", " ").replace("\u3000", " ").strip()


def match_key(title: str) -> str:
    return norm(re.sub(r"\s*\(\d{4}\)", "", english_name(title)))


def load_engagement(blob: bytes) -> pd.DataFrame:
    frames = []
    for sheet, kind in (("Shows", "Show"), ("Movies", "Movie")):
        frame = pd.read_excel(BytesIO(blob), sheet_name=sheet, header=5)
        frame = frame[frame["Title"].notna()].copy()
        frame["title"] = frame["Title"].astype(str).str.strip()
        frame = frame[~frame["title"].str.startswith("*")]
        frame = frame[~frame["title"].isin(OTHERS)]
        frame["kind"] = kind
        frame["hours"] = pd.to_numeric(frame["Hours Viewed"], errors="coerce")
        frame["views"] = pd.to_numeric(frame["Views"], errors="coerce")
        frame["available_globally"] = frame["Available Globally?"].astype(str).str.strip()
        frame["runtime"] = frame["Runtime"].astype(str).str.strip()
        frame["release_date"] = pd.to_datetime(frame["Release Date"], errors="coerce")
        frames.append(frame)
    out = pd.concat(frames, ignore_index=True)
    if out["hours"].isna().any() or out["views"].isna().any():
        sys.exit("Named titles include a non-numeric hours or views cell.")
    if set(out["available_globally"]) != {"Yes", "No"}:
        sys.exit(f"Unexpected Available Globally values: {set(out['available_globally'])}")
    out["english"] = out["title"].map(english_name)
    out["en_n"] = out["english"].map(norm)
    out["key"] = out["title"].map(match_key)
    return out


def chart_name(row: pd.Series) -> str:
    season = row["season_title"]
    if pd.notna(season) and str(season).strip():
        return str(season).strip()
    return str(row["show_title"]).strip()


def load_top10(blob: bytes) -> pd.DataFrame:
    frame = pd.read_csv(BytesIO(blob), sep="\t")
    frame["week"] = pd.to_datetime(frame["week"])
    window = frame[(frame["week"] >= WEEK_START) & (frame["week"] <= WEEK_END)].copy()
    window["chart_name"] = window.apply(chart_name, axis=1)
    return window


def attach_top10(titles: pd.DataFrame, top10: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    by_key: dict[str, list[int]] = defaultdict(list)
    for index, key in enumerate(titles["key"]):
        by_key[key].append(index)

    weeks = top10.groupby("chart_name")["week"].nunique().to_dict()
    chosen: dict[int, str] = {}
    unmatched: list[str] = []
    for name in sorted(set(top10["chart_name"])):
        key = match_key(name)
        indexes = by_key.get(key, [])
        if not indexes:
            unmatched.append(name)
            continue
        exact = [index for index in indexes if titles.at[index, "en_n"] == norm(name)]
        pool = exact or indexes
        pick = max(pool, key=lambda index: (titles.at[index, "hours"], -index))
        chosen[pick] = name

    titles = titles.copy()
    titles["global_top10_weeks"] = 0
    titles["matched_chart_name"] = ""
    for index, name in chosen.items():
        titles.at[index, "global_top10_weeks"] = int(weeks[name])
        titles.at[index, "matched_chart_name"] = name
    return titles, unmatched


def cut_k(n: int, pct: float) -> int:
    if pct >= 100:
        return n
    return int(round(n * pct / 100.0))


def curve_table(hours: pd.Series) -> pd.DataFrame:
    ordered = hours.sort_values(ascending=False)
    total = float(ordered.sum())
    rows = []
    for pct in CURVE_PCTS:
        k = cut_k(len(ordered), pct)
        share = float(ordered.iloc[:k].sum()) / total * 100
        rows.append(
            {
                "top_pct_of_titles": pct,
                "titles": k,
                "cum_share_of_hours_pct": round(share, 2),
            }
        )
    return pd.DataFrame(rows)


def concentration(frame: pd.DataFrame, pct: float) -> float:
    ordered = frame.sort_values("hours", ascending=False)
    k = cut_k(len(ordered), pct)
    return float(ordered["hours"].iloc[:k].sum()) / float(ordered["hours"].sum())


def require(condition: bool, message: str) -> None:
    if not condition:
        sys.exit(message)


def check_figures(titles: pd.DataFrame, top10: pd.DataFrame, unmatched: list[str]) -> dict:
    shows = titles[titles["kind"] == "Show"]
    movies = titles[titles["kind"] == "Movie"]
    total_hours = float(titles["hours"].sum())
    require(len(shows) == 8193, f"shows {len(shows)} != 8193")
    require(len(movies) == 9177, f"movies {len(movies)} != 9177")
    require(len(titles) == 17370, f"named titles {len(titles)} != 17370")
    require(int(total_hours) == 96_804_600_000, f"named hours {total_hours} != 96804600000")
    require(round(concentration(titles, 1) * 100, 1) == 25.2, "top 1% hours share drifted")
    require(round(concentration(titles, 10) * 100, 1) == 67.9, "top 10% hours share drifted")
    require(round(concentration(titles, 20) * 100, 1) == 82.6, "top 20% hours share drifted")
    bottom = 1 - concentration(titles, 50)
    require(round(bottom * 100, 1) == 3.2, f"bottom 50% is {bottom * 100}")

    global_yes = titles["available_globally"].eq("Yes")
    title_share = float(global_yes.mean())
    hour_share = float(titles.loc[global_yes, "hours"].sum()) / total_hours
    require(round(title_share * 100, 1) == 30.4, "Available Globally title share drifted")
    require(round(hour_share * 100, 1) == 47.0, "Available Globally hours share drifted")

    charted_names = top10["chart_name"].nunique()
    require(charted_names == 489, f"charted names {charted_names} != 489")
    require(unmatched == [FURIES_CHART], f"unmatched chart names: {unmatched}")
    require(
        titles["title"].str.startswith("Furies: Season 2: Furies: Resistance").any(),
        "engagement report is missing the Furies Season 2 title used in the method note",
    )
    matched = titles["global_top10_weeks"] > 0
    matched_n = int(matched.sum())
    matched_hours = float(titles.loc[matched, "hours"].sum()) / total_hours
    require(matched_n == 488, f"matched titles {matched_n} != 488")
    require(round(matched_n / len(titles) * 100, 1) == 2.8, "Top 10 title share drifted")
    require(round(matched_hours * 100, 1) == 26.6, f"Top 10 hours share {matched_hours * 100}")

    top100 = titles.sort_values(["hours", "title"], ascending=[False, True]).head(100)
    never = top100[top100["global_top10_weeks"] == 0]
    require(len(never) == 29, f"never-charted top 100 is {len(never)}")
    weeks = top10["week"].nunique()
    require(weeks == 26, f"expected 26 Top 10 weeks, found {weeks}")
    return {
        "shows": len(shows),
        "movies": len(movies),
        "titles": len(titles),
        "hours": int(total_hours),
        "top1": round(concentration(titles, 1) * 100, 1),
        "top10": round(concentration(titles, 10) * 100, 1),
        "top20": round(concentration(titles, 20) * 100, 1),
        "bottom50": round(bottom * 100, 1),
        "global_title_pct": round(title_share * 100, 1),
        "global_hour_pct": round(hour_share * 100, 1),
        "not_global_title_pct": round((1 - title_share) * 100, 1),
        "not_global_hour_pct": round((1 - hour_share) * 100, 1),
        "charted_titles": matched_n,
        "charted_title_pct": round(matched_n / len(titles) * 100, 1),
        "charted_hour_pct": round(matched_hours * 100, 1),
        "never_top100": len(never),
    }


def write_tables(titles: pd.DataFrame, top10: pd.DataFrame, curve: pd.DataFrame) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    export = titles.copy()
    export["release_date"] = export["release_date"].dt.strftime("%Y-%m-%d").fillna("")
    export = export[
        [
            "title",
            "kind",
            "available_globally",
            "release_date",
            "hours",
            "runtime",
            "views",
            "global_top10_weeks",
            "matched_chart_name",
        ]
    ].rename(columns={"hours": "hours_viewed", "views": "views_count"})
    export.to_csv(DATA / "netflix_h1_2026_titles.csv", index=False)

    top = top10.copy()
    top["week"] = top["week"].dt.strftime("%Y-%m-%d")
    top = top[
        [
            "week",
            "category",
            "weekly_rank",
            "show_title",
            "season_title",
            "chart_name",
            "weekly_hours_viewed",
            "runtime",
            "weekly_views",
            "cumulative_weeks_in_top_10",
        ]
    ]
    top.to_csv(DATA / "netflix_top10_global_2026h1.csv", index=False)
    curve.to_csv(DATA / "library_shape_curve.csv", index=False)


def style(fig: go.Figure, title: str, subtitle: str, source: str, height: int = 700) -> go.Figure:
    fig.update_layout(
        title=dict(
            text=(
                f"<b>{title}</b><br>"
                f"<span style='font-size:13px;color:{GRAY}'>{subtitle}</span>"
            ),
            x=0.01,
            xanchor="left",
            y=0.97,
            yanchor="top",
        ),
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        font=dict(family="DM Sans, Helvetica, Arial, sans-serif", color=INK, size=13),
        width=1200,
        height=height,
        margin=dict(l=70, r=40, t=110, b=90),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        annotations=[
            dict(
                text=f"{source} · Artometrics",
                xref="paper",
                yref="paper",
                x=0,
                y=-0.16,
                showarrow=False,
                xanchor="left",
                font=dict(size=11, color=GRAY),
            )
        ],
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    return fig


def cumulative(frame: pd.DataFrame) -> tuple[list[float], list[float]]:
    ordered = frame.sort_values("hours", ascending=False)
    hours = ordered["hours"].to_numpy()
    share_titles = [0.0]
    share_hours = [0.0]
    running = 0.0
    total = float(hours.sum())
    count = len(hours)
    for index, value in enumerate(hours, start=1):
        running += float(value)
        share_titles.append(index / count * 100)
        share_hours.append(running / total * 100)
    return share_titles, share_hours


def chart_library(titles: pd.DataFrame, stats: dict) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[0, 100],
            y=[0, 100],
            mode="lines",
            name="Equal share",
            line=dict(color=LIGHT, width=1.5, dash="dash"),
            hoverinfo="skip",
        )
    )
    for kind, color in (("Show", RED), ("Movie", BLUE)):
        x, y = cumulative(titles[titles["kind"] == kind])
        label = "Shows" if kind == "Show" else "Movies"
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=label,
                line=dict(color=color, width=2.5),
                hovertemplate=f"{label}<br>%{{x:.1f}}% of titles<br>%{{y:.1f}}% of hours<extra></extra>",
            )
        )
    fig.add_vline(x=10, line_color=GRID, line_width=1)
    fig.add_vline(x=20, line_color=GRID, line_width=1)
    style(
        fig,
        f"The top 10% of titles drew {stats['top10']}% of viewing",
        (
            f"Share of titles, largest first, against share of named hours. "
            f"All named titles: top 10% drew {stats['top10']}%, top 20% drew {stats['top20']}%, "
            f"bottom half drew {stats['bottom50']}%. "
            f"{stats['shows']:,} shows and {stats['movies']:,} movies."
        ),
        "Source: Netflix, What We Watched, January–June 2026 (published July 16, 2026)",
    )
    fig.update_xaxes(title="Share of titles, largest first (%)", range=[0, 100], dtick=10)
    fig.update_yaxes(title="Share of named hours (%)", range=[0, 100], dtick=10)
    return fig


def chart_concentration(stats: dict) -> go.Figure:
    labels = ["Available globally", "Not available globally"]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Share of titles",
            x=labels,
            y=[stats["global_title_pct"], stats["not_global_title_pct"]],
            marker_color=BLUE,
            text=[f"{stats['global_title_pct']}%", f"{stats['not_global_title_pct']}%"],
            textposition="outside",
            hovertemplate="%{x}<br>%{y:.1f}% of titles<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Share of hours",
            x=labels,
            y=[stats["global_hour_pct"], stats["not_global_hour_pct"]],
            marker_color=RED,
            text=[f"{stats['global_hour_pct']}%", f"{stats['not_global_hour_pct']}%"],
            textposition="outside",
            hovertemplate="%{x}<br>%{y:.1f}% of hours<extra></extra>",
        )
    )
    style(
        fig,
        f"Available Globally titles were {stats['global_title_pct']}% of titles and {stats['global_hour_pct']}% of hours",
        "This is Netflix's availability flag, not ownership. Named titles, January–June 2026.",
        "Source: Netflix, What We Watched, January–June 2026 (published July 16, 2026)",
        height=640,
    )
    fig.update_layout(barmode="group", margin=dict(l=70, r=40, t=120, b=90))
    fig.update_yaxes(title="Percent", range=[0, 100], dtick=10)
    fig.update_xaxes(title="")
    return fig


def short_label(title: str) -> str:
    text = re.sub(r"\s*\(\d{4}\)", "", english_name(title))
    text = re.sub(r": Season (\d+)", r" S\1", text)
    text = re.sub(r": Limited Series", "", text)
    if len(text) > 34:
        return text[:33].rstrip() + "…"
    return text


def chart_gap(titles: pd.DataFrame, stats: dict) -> go.Figure:
    frame = titles.copy()
    frame["hours_m"] = frame["hours"] / 1_000_000
    top100 = set(frame.sort_values(["hours", "title"], ascending=[False, True]).head(100).index)
    never = frame.index.isin(top100) & frame["global_top10_weeks"].eq(0)
    charted = frame["global_top10_weeks"] > 0
    other = ~never & ~charted
    fig = go.Figure()
    fig.add_trace(
        go.Scattergl(
            x=frame.loc[other, "global_top10_weeks"],
            y=frame.loc[other, "hours_m"],
            mode="markers",
            name="Other named titles",
            marker=dict(color=LIGHT, size=5, opacity=0.45),
            text=frame.loc[other, "title"],
            hovertemplate="%{text}<br>%{y:.1f}M hours<br>%{x} weeks<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=frame.loc[charted, "global_top10_weeks"],
            y=frame.loc[charted, "hours_m"],
            mode="markers",
            name="On a global Top 10",
            marker=dict(color=BLUE, size=8, opacity=0.85),
            text=frame.loc[charted, "title"],
            hovertemplate="%{text}<br>%{y:.1f}M hours<br>%{x} weeks<extra></extra>",
        )
    )
    called = frame.loc[never].sort_values("hours", ascending=False)
    fig.add_trace(
        go.Scatter(
            x=called["global_top10_weeks"],
            y=called["hours_m"],
            mode="markers",
            name="Top 100, never charted globally",
            marker=dict(color=RED, size=9, line=dict(color=INK, width=0.5)),
            text=called["title"],
            hovertemplate="%{text}<br>%{y:.1f}M hours<br>0 weeks on the global Top 10<extra></extra>",
        )
    )
    callout = "<br>".join(
        f"{short_label(row.title)} · {row.hours_m:.0f}M hours"
        for _, row in called.head(5).iterrows()
    )
    style(
        fig,
        f"{stats['never_top100']} of the 100 most-watched titles never made the global Top 10",
        (
            f"Weeks ending Jan 4–Jun 28, 2026. Charted titles were {stats['charted_title_pct']}% of "
            f"named titles and {stats['charted_hour_pct']}% of named hours. "
            f"Only global lists were checked, and titles were matched by name."
        ),
        "Source: Netflix What We Watched, Jan–Jun 2026, and global Top 10. Furies Season 2 did not match (double colon in the Top 10 file).",
    )
    fig.update_layout(margin=dict(l=70, r=36, t=120, b=100))
    fig.add_annotation(
        x=13,
        y=820,
        xref="x",
        yref="y",
        text=f"<b>Highest hours, never on a global Top 10</b><br>{callout}",
        showarrow=False,
        align="left",
        xanchor="left",
        yanchor="top",
        bgcolor="#FFFFFF",
        bordercolor=GRID,
        borderwidth=1,
        borderpad=8,
        font=dict(size=12, color=INK),
    )
    fig.update_xaxes(title="Weeks on the global Top 10", dtick=2, range=[-0.6, 27])
    fig.update_yaxes(title="Hours viewed (millions)")
    return fig


def write_chart(fig: go.Figure, stem: str) -> None:
    html = pio.to_html(
        fig,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": False, "responsive": True, "displaylogo": False},
    )
    payload = fig.to_json()
    png_buf = pio.to_image(fig, format="png", width=1200, height=fig.layout.height or 700, scale=2)
    for folder in HTML_JSON_DIRS:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{stem}.html").write_text(html)
        (folder / f"{stem}.plotly.json").write_text(payload)
    for folder in PNG_DIRS:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{stem}.png").write_bytes(png_buf)
    image = Image.open(BytesIO(png_buf)).convert("RGB")
    jpg = image.resize((1000, 583), Image.Resampling.LANCZOS)
    for folder in JPG_DIRS:
        folder.mkdir(parents=True, exist_ok=True)
        jpg.save(folder / f"{stem}.jpg", format="JPEG", quality=85, optimize=True)


def main() -> None:
    print("Downloading What We Watched workbook…")
    workbook_url = xlsx_url()
    print(workbook_url)
    titles = load_engagement(fetch(workbook_url))
    print("Downloading global Top 10…")
    top10 = load_top10(fetch(TOP10_URL))
    titles, unmatched = attach_top10(titles, top10)
    stats = check_figures(titles, top10, unmatched)
    curve = curve_table(titles["hours"])
    write_tables(titles, top10, curve)
    write_chart(chart_library(titles, stats), "library-shape")
    write_chart(chart_concentration(stats), "concentration")
    write_chart(chart_gap(titles, stats), "availability-gap")
    print(json.dumps(stats, indent=2))
    print(curve.to_string(index=False))
    print(f"Unmatched chart name: {unmatched[0]}")
    print(f"Engagement title: {FURIES_REPORT}")


if __name__ == "__main__":
    main()
