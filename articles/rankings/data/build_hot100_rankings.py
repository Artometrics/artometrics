#!/usr/bin/env python3
"""Build the rankings article tables and charts from the pinned Hot 100 file.

Source: utdata/rwd-billboard-data data-out/hot-100-current.csv at commit
ff86f04. The repository code is MIT. The chart rows are Billboard's.
Rows are kept through the chart dated 2026-10-31.

A song is a normalized title plus a normalized performer. Normalization is
only: casefold, "&" read as "and", ft. / feat. / featuring read as
"featuring", punctuation removed, whitespace collapsed.

Each listed position earns 101 minus that position. Distinct counts use the
normalized song once per year. Average weeks in the top 10 is top-10
song-weeks divided by distinct top-10 songs, rounded half up to two decimals.

The script stops, and does not write, if the sheet checks miss.
"""

from __future__ import annotations

import csv
import re
import sys
import tempfile
import urllib.request
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

PIN = "ff86f04"
URL = (
    "https://raw.githubusercontent.com/utdata/rwd-billboard-data/"
    f"{PIN}/data-out/hot-100-current.csv"
)
CUTOFF = "2026-10-31"
WEEKS_2026 = 44

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CHARTS = ROOT / "charts"

ART_HIGHLIGHT = "#C0392B"
ART_SECONDARY = "#2C3E6B"
ART_MID = "#6B6B6B"
ART_CREAM = "#F2F0EB"
ART_DARK = "#1C1C1E"
FONT = "DM Sans, Helvetica, sans-serif"
SOURCE_LINE = (
    "Billboard Hot 100 via utdata/rwd-billboard-data (MIT), commit ff86f04, "
    "through the chart dated Oct 31, 2026."
)
ERA_LINE = (
    "Marks: Nielsen SoundScan and airplay data from November 1991; "
    "streaming added 2012 to 2013."
)
PARTIAL_2026 = "through the chart dated Oct 31, 2026 (44 weeks)"

EXPECTED_TOP10 = {1966: 130, 1992: 77, 2015: 55, 2022: 92, 2025: 74}
EXPECTED_AVG_2015 = Decimal("9.45")
EXPECTED_POINTS = {
    ("lose control", "teddy swims"): 9321,
    ("blinding lights", "the weeknd"): 8089,
    ("beautiful things", "benson boone"): 7963,
}


def stop(message: str) -> None:
    print(f"MISMATCH: {message}", file=sys.stderr)
    raise SystemExit(2)


def normalize(name: str) -> str:
    text = name.casefold().strip()
    text = text.replace("&", " and ")
    text = re.sub(r"\b(featuring|feat\.?|ft\.?)\b", " featuring ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def round_half_up(numer: int, denom: int) -> Decimal:
    return (Decimal(numer) / Decimal(denom)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def download(dest: Path) -> None:
    print(f"Downloading {URL}")
    urllib.request.urlretrieve(URL, dest)


def load_rows(src: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with src.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["chart_week"] > CUTOFF:
                continue
            rows.append(row)
    if not rows:
        stop("the pinned file has no rows on or before 2026-10-31")
    return rows


def build(rows: list[dict[str, str]]) -> dict:
    by_year_weeks: dict[int, set[str]] = defaultdict(set)
    by_year_songs: dict[int, set[tuple[str, str]]] = defaultdict(set)
    by_year_top10: dict[int, set[tuple[str, str]]] = defaultdict(set)
    by_year_top10_weeks: dict[int, dict[tuple[str, str], int]] = defaultdict(lambda: defaultdict(int))
    by_year_no1: dict[int, set[tuple[str, str]]] = defaultdict(set)
    points: dict[tuple[str, str], int] = defaultdict(int)
    weeks: dict[tuple[str, str], set[str]] = defaultdict(set)
    first: dict[tuple[str, str], str] = {}
    last: dict[tuple[str, str], str] = {}
    raw_counts: dict[tuple[str, str], dict[tuple[str, str], int]] = defaultdict(lambda: defaultdict(int))
    era_points = {1: defaultdict(int), 2: defaultdict(int), 3: defaultdict(int)}
    seen_week_key: set[tuple[str, str, str]] = set()
    seen_top10: set[tuple[str, str, str]] = set()
    double_weeks: list[tuple[str, str, str, str]] = []

    for row in rows:
        week = row["chart_week"]
        year = int(week[:4])
        position = int(float(row["current_week"]))
        if position < 1 or position > 100:
            stop(f"position {position} on {week} is outside 1 to 100")
        title = row["title"]
        performer = row["performer"]
        key = (normalize(title), normalize(performer))
        stamp = (week, key[0], key[1])
        if stamp in seen_week_key:
            double_weeks.append((week, title, performer, str(position)))
        seen_week_key.add(stamp)

        by_year_weeks[year].add(week)
        by_year_songs[year].add(key)
        earned = 101 - position
        points[key] += earned
        weeks[key].add(week)
        first[key] = week if key not in first else min(first[key], week)
        last[key] = week if key not in last else max(last[key], week)
        raw_counts[key][(title, performer)] += 1
        if year <= 1991:
            era_points[1][key] += earned
        elif year <= 2011:
            era_points[2][key] += earned
        else:
            era_points[3][key] += earned
        if position <= 10:
            top10_stamp = (week, key[0], key[1])
            if top10_stamp in seen_top10:
                stop(f"{title} / {performer} is listed twice in the top 10 on {week}")
            seen_top10.add(top10_stamp)
            by_year_top10[year].add(key)
            by_year_top10_weeks[year][key] += 1
        if position == 1:
            by_year_no1[year].add(key)

    display = {}
    for key, counts in raw_counts.items():
        display[key] = sorted(counts, key=lambda pair: (-counts[pair], pair[0], pair[1]))[0]

    years = sorted(by_year_weeks)
    crowding = []
    for year in years:
        top10_slots = sum(by_year_top10_weeks[year].values())
        distinct_top10 = len(by_year_top10[year])
        crowding.append(
            {
                "year": year,
                "chart_weeks": len(by_year_weeks[year]),
                "distinct_songs": len(by_year_songs[year]),
                "distinct_top10_songs": distinct_top10,
                "distinct_number_ones": len(by_year_no1[year]),
                "top10_song_weeks": top10_slots,
                "avg_weeks_in_top10": round_half_up(top10_slots, distinct_top10),
            }
        )

    song_rows = []
    for key, total in points.items():
        title, performer = display[key]
        song_rows.append(
            {
                "title": title,
                "performer": performer,
                "points": total,
                "weeks": len(weeks[key]),
                "first_chart_week": first[key],
                "last_chart_week": last[key],
                "title_key": key[0],
                "performer_key": key[1],
            }
        )
    song_rows.sort(key=lambda row: (-row["points"], row["title"], row["performer"]))

    merges = []
    for key, counts in raw_counts.items():
        variants = sorted(counts)
        if len(variants) < 2:
            continue
        for index, left in enumerate(variants):
            for right in variants[index + 1 :]:
                merges.append(
                    {
                        "title_a": left[0],
                        "performer_a": left[1],
                        "title_b": right[0],
                        "performer_b": right[1],
                        "title_key": key[0],
                        "performer_key": key[1],
                    }
                )
    merges.sort(
        key=lambda row: (row["title_key"], row["performer_key"], row["title_a"], row["performer_a"], row["title_b"])
    )

    return {
        "crowding": crowding,
        "songs": song_rows,
        "merges": merges,
        "points": points,
        "display": display,
        "weeks": weeks,
        "first": first,
        "last": last,
        "era_points": era_points,
        "double_weeks": double_weeks,
        "n_rows": len(rows),
    }


def check(result: dict) -> None:
    by_year = {row["year"]: row for row in result["crowding"]}
    misses = []
    for year, expected in EXPECTED_TOP10.items():
        got = by_year[year]["distinct_top10_songs"]
        if got != expected:
            misses.append(f"{year} distinct top-10 songs: expected {expected}, got {got}")
    if by_year[2015]["avg_weeks_in_top10"] != EXPECTED_AVG_2015:
        misses.append(
            f"2015 average weeks in the top 10: expected {EXPECTED_AVG_2015}, "
            f"got {by_year[2015]['avg_weeks_in_top10']}"
        )
    for key, expected in EXPECTED_POINTS.items():
        got = result["points"].get(key)
        if got != expected:
            misses.append(f"{key[0]} / {key[1]}: expected {expected} points, got {got}")
    if by_year[2026]["chart_weeks"] != WEEKS_2026:
        misses.append(
            f"2026 chart weeks: expected {WEEKS_2026}, got {by_year[2026]['chart_weeks']}"
        )
    latest = max(row["last_chart_week"] for row in result["songs"])
    if latest != CUTOFF:
        misses.append(f"latest chart week: expected {CUTOFF}, got {latest}")
    if misses:
        print("Sheet checks did not match. Article text was not written from these figures.", file=sys.stderr)
        for miss in misses:
            print(f"MISMATCH: {miss}", file=sys.stderr)
        raise SystemExit(2)
    print("Sheet checks matched.")
    print(f"Double-listed song-weeks: {len(result['double_weeks'])}")


def write_tables(result: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    crowding_fields = [
        "year",
        "chart_weeks",
        "distinct_songs",
        "distinct_top10_songs",
        "distinct_number_ones",
        "top10_song_weeks",
        "avg_weeks_in_top10",
    ]
    with (DATA / "crowding_by_year.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=crowding_fields, lineterminator="\n")
        writer.writeheader()
        for row in result["crowding"]:
            out = dict(row)
            out["avg_weeks_in_top10"] = f"{row['avg_weeks_in_top10']:.2f}"
            writer.writerow(out)

    song_fields = [
        "title",
        "performer",
        "points",
        "weeks",
        "first_chart_week",
        "last_chart_week",
    ]
    with (DATA / "song_points.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=song_fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(result["songs"])

    merge_fields = [
        "title_a",
        "performer_a",
        "title_b",
        "performer_b",
        "title_key",
        "performer_key",
    ]
    with (DATA / "merged_name_pairs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=merge_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(result["merges"])
    print(f"Wrote {len(result['crowding'])} year rows, {len(result['songs'])} songs, {len(result['merges'])} merged pairs")


def base_layout(title: str, height: int, bottom: int = 96) -> dict:
    return dict(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(family=FONT, size=15, color=ART_DARK),
            x=0.5,
            xanchor="center",
        ),
        paper_bgcolor=ART_CREAM,
        plot_bgcolor=ART_CREAM,
        font=dict(family=FONT, color=ART_DARK, size=12),
        margin=dict(l=72, r=36, t=88, b=bottom),
        height=height,
        width=1100,
        hovermode="closest",
        showlegend=False,
    )


def style_time_axes(fig: go.Figure, y_title: str) -> None:
    fig.update_xaxes(
        title="Chart year",
        showgrid=True,
        gridcolor="#E0DDD6",
        linecolor=ART_MID,
        zeroline=False,
        tickfont=dict(color=ART_MID, size=11),
        dtick=5,
        range=[1957.4, 2027.4],
    )
    fig.update_yaxes(
        title=y_title,
        showgrid=True,
        gridcolor="#E0DDD6",
        linecolor=ART_MID,
        zeroline=False,
        tickfont=dict(color=ART_MID, size=11),
        rangemode="tozero",
    )


def add_era_marks(fig: go.Figure) -> None:
    fig.add_vline(
        x=1991 + 10 / 12,
        line_dash="dot",
        line_color=ART_MID,
        line_width=1.4,
    )
    fig.add_vrect(
        x0=2011.5,
        x1=2013.5,
        fillcolor="rgba(192,57,43,0.12)",
        line_width=0,
        layer="below",
    )
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0,
        y=-0.22,
        text=ERA_LINE,
        showarrow=False,
        xanchor="left",
        font=dict(family=FONT, size=11, color=ART_MID),
    )
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0,
        y=-0.30,
        text=SOURCE_LINE,
        showarrow=False,
        xanchor="left",
        font=dict(family=FONT, size=11, color=ART_MID),
    )


def add_2026_label(fig: go.Figure, y_value: float, ax: int, ay: int) -> None:
    fig.add_annotation(
        x=2026,
        y=y_value,
        text=PARTIAL_2026,
        showarrow=True,
        arrowhead=0,
        arrowwidth=1,
        arrowcolor=ART_HIGHLIGHT,
        ax=ax,
        ay=ay,
        xanchor="right",
        yanchor="bottom" if ay < 0 else "top",
        font=dict(family=FONT, size=12, color=ART_HIGHLIGHT),
    )


def save_chart(fig: go.Figure, stem: str) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    json_path = CHARTS / f"{stem}.plotly.json"
    png_path = CHARTS / f"{stem}.png"
    json_path.write_text(fig.to_json(), encoding="utf-8")
    fig.write_image(str(png_path), width=fig.layout.width, height=fig.layout.height, scale=2)
    print(f"Wrote {png_path.name} and {json_path.name}")


def yearly(result: dict, field: str) -> tuple[list[int], list[float]]:
    years = [row["year"] for row in result["crowding"]]
    values = [row[field] for row in result["crowding"]]
    return years, values


def chart_top10(result: dict) -> None:
    years, values = yearly(result, "distinct_top10_songs")
    y2026 = values[years.index(2026)]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=years,
            y=values,
            mode="lines",
            line=dict(color=ART_SECONDARY, width=2.4),
            hovertemplate="%{x}: %{y} distinct top-10 songs<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[year for year in years if year != 2026],
            y=[value for year, value in zip(years, values) if year != 2026],
            mode="markers",
            marker=dict(size=7, color=ART_SECONDARY),
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[2026],
            y=[y2026],
            mode="markers",
            marker=dict(size=13, color=ART_CREAM, line=dict(color=ART_HIGHLIGHT, width=2.5)),
            hovertemplate="2026: %{y} distinct top-10 songs<br>" + PARTIAL_2026 + "<extra></extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "DISTINCT TOP-10 SONGS PER YEAR<br><span style='color:#C0392B'>130 IN 1966 · 55 IN 2015</span>",
            620,
            128,
        )
    )
    style_time_axes(fig, "Distinct songs in the top 10")
    add_era_marks(fig)
    add_2026_label(fig, y2026, ax=-210, ay=-78)
    save_chart(fig, "distinct-top10-songs-by-year")


def chart_avg_weeks(result: dict) -> None:
    years = [row["year"] for row in result["crowding"]]
    values = [float(row["avg_weeks_in_top10"]) for row in result["crowding"]]
    y2026 = values[years.index(2026)]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=years,
            y=values,
            mode="lines",
            line=dict(color=ART_SECONDARY, width=2.4),
            hovertemplate="%{x}: %{y:.2f} weeks<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[year for year in years if year != 2026],
            y=[value for year, value in zip(years, values) if year != 2026],
            mode="markers",
            marker=dict(size=7, color=ART_SECONDARY),
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[2026],
            y=[y2026],
            mode="markers",
            marker=dict(size=13, color=ART_CREAM, line=dict(color=ART_HIGHLIGHT, width=2.5)),
            hovertemplate="2026: %{y:.2f} weeks<br>" + PARTIAL_2026 + "<extra></extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "AVERAGE WEEKS IN THE TOP 10<br><span style='color:#C0392B'>9.45 WEEKS IN 2015</span>",
            620,
            128,
        )
    )
    style_time_axes(fig, "Average weeks per top-10 song")
    add_era_marks(fig)
    add_2026_label(fig, y2026, ax=-200, ay=72)
    save_chart(fig, "avg-weeks-in-top10-by-year")


def chart_number_ones(result: dict) -> None:
    years, values = yearly(result, "distinct_number_ones")
    y2026 = values[years.index(2026)]
    colors = [ART_CREAM if year == 2026 else ART_SECONDARY for year in years]
    lines = [ART_HIGHLIGHT if year == 2026 else ART_SECONDARY for year in years]
    widths = [1.6 if year == 2026 else 0 for year in years]
    fig = go.Figure(
        go.Bar(
            x=years,
            y=values,
            marker=dict(color=colors, line=dict(color=lines, width=widths)),
            hovertemplate="%{x}: %{y} distinct No. 1s<extra></extra>",
        )
    )
    fig.update_layout(
        **base_layout(
            "DISTINCT NO. 1s PER YEAR<br><span style='color:#C0392B'>36 IN 1974</span>",
            620,
            128,
        )
    )
    style_time_axes(fig, "Distinct No. 1 songs")
    add_era_marks(fig)
    add_2026_label(fig, y2026, ax=-170, ay=-96)
    save_chart(fig, "distinct-number-ones-by-year")


def song_label(row: dict, rank: int) -> str:
    return f"{rank}. {row['title']} — {row['performer']}"


def horizontal_bars(rows: list[dict], stem: str, title: str, height: int, margin_l: int) -> None:
    ordered = list(rows)
    labels = [song_label(row, index) for index, row in enumerate(ordered, start=1)]
    # categoryarray runs bottom to top, so the best song (rank 1) is last.
    colors = [ART_HIGHLIGHT if index == 0 else ART_SECONDARY for index in range(len(ordered))]
    fig = go.Figure(
        go.Bar(
            x=[row["points"] for row in ordered],
            y=labels,
            orientation="h",
            marker=dict(color=colors, line=dict(color=ART_DARK, width=0.4)),
            hovertemplate="%{y}<br>%{x:,} points<extra></extra>",
        )
    )
    layout = base_layout(title, height, 88)
    layout["margin"] = dict(l=margin_l, r=48, t=88, b=88)
    fig.update_layout(**layout)
    fig.update_xaxes(
        title="Inverse-rank points (101 minus position)",
        showgrid=True,
        gridcolor="#E0DDD6",
        linecolor=ART_MID,
        zeroline=False,
        tickfont=dict(color=ART_MID, size=11),
    )
    fig.update_yaxes(
        categoryorder="array",
        categoryarray=list(reversed(labels)),
        showgrid=False,
        linecolor=ART_MID,
        tickfont=dict(color=ART_DARK, size=11),
        automargin=True,
    )
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0,
        y=-0.12,
        text="No. 1 is the highest point total. " + SOURCE_LINE,
        showarrow=False,
        xanchor="left",
        font=dict(family=FONT, size=11, color=ART_MID),
    )
    save_chart(fig, stem)


def chart_top20(result: dict) -> None:
    horizontal_bars(
        result["songs"][:20],
        "all-time-top20-points",
        "ALL-TIME TOP 20 BY POINTS<br><span style='color:#C0392B'>NO. 1 IS BEST</span>",
        860,
        390,
    )


def chart_eras(result: dict) -> None:
    panels = [
        (1, "1958 to 1991"),
        (2, "1992 to 2011"),
        (3, "2012 to Oct 31, 2026"),
    ]
    fig = make_subplots(rows=3, cols=1, subplot_titles=[name for _, name in panels], vertical_spacing=0.10)
    for index, (era, _name) in enumerate(panels, start=1):
        ranked = sorted(result["era_points"][era].items(), key=lambda item: (-item[1], item[0][0], item[0][1]))[:5]
        labels = []
        values = []
        for rank, (key, total) in enumerate(ranked, start=1):
            title, performer = result["display"][key]
            labels.append(f"{rank}. {title} — {performer}")
            values.append(total)
        colors = [ART_HIGHLIGHT if rank == 0 else ART_SECONDARY for rank in range(len(labels))]
        fig.add_trace(
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker=dict(color=colors, line=dict(color=ART_DARK, width=0.4)),
                hovertemplate="%{y}<br>%{x:,} points<extra></extra>",
                showlegend=False,
            ),
            row=index,
            col=1,
        )
        fig.update_yaxes(
            categoryorder="array",
            categoryarray=list(reversed(labels)),
            showgrid=False,
            automargin=True,
            tickfont=dict(color=ART_DARK, size=11),
            row=index,
            col=1,
        )
        fig.update_xaxes(
            showgrid=True,
            gridcolor="#E0DDD6",
            zeroline=False,
            tickfont=dict(color=ART_MID, size=11),
            title="",
            row=index,
            col=1,
        )
    layout = base_layout(
        "TOP 5 BY POINTS INSIDE EACH ERA<br><span style='color:#C0392B'>NO. 1 IS BEST</span>",
        1040,
        120,
    )
    layout["margin"] = dict(l=360, r=48, t=96, b=120)
    layout["width"] = 1100
    fig.update_layout(**layout)
    fig.update_annotations(font=dict(family=FONT, size=13, color=ART_DARK))
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0,
        y=-0.08,
        text="Points count only on chart weeks inside the era. No. 1 is the highest total.",
        showarrow=False,
        xanchor="left",
        font=dict(family=FONT, size=11, color=ART_MID),
    )
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0,
        y=-0.12,
        text=SOURCE_LINE,
        showarrow=False,
        xanchor="left",
        font=dict(family=FONT, size=11, color=ART_MID),
    )
    save_chart(fig, "era-top5-points")


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "hot-100-current.csv"
        download(src)
        rows = load_rows(src)
    result = build(rows)
    check(result)
    write_tables(result)
    chart_top10(result)
    chart_avg_weeks(result)
    chart_number_ones(result)
    chart_top20(result)
    chart_eras(result)
    print(f"Rows kept: {result['n_rows']}")


if __name__ == "__main__":
    main()
