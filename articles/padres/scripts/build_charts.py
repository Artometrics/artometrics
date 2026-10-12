#!/usr/bin/env python3
"""Rebuild Padres R2 charts from the Lahman 2025 subset.

Reads articles/padres/data/lahman/*.csv (CC BY-SA 3.0) and writes derived
tables plus PNG and Plotly JSON under articles/padres/charts/ and public/.

The 2026 season is not in Lahman. Wins, the wild-card and division-series
results, attendance, and runs are taken from the Baseball-Reference team
page and stored in data/padres_2026_bref.csv. Competitive-balance-tax
payrolls are the July 2026 Spotrac compilation already published in this
article; they are not a fresh export.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "articles" / "padres"
LAHMAN = ART / "data" / "lahman"
DATA = ART / "data"
CHARTS = ART / "charts"
PUBLIC_CHARTS = ROOT / "public" / "data" / "articles" / "padres" / "charts"
PUBLIC_IMG = ROOT / "public" / "images" / "content" / "articles" / "padres" / "charts"
PUBLIC_DATA = ROOT / "public" / "data" / "articles" / "padres" / "data"

RED = "#E60000"
BLUE = "#0047FF"
INK = "#1C1C1E"
WHITE = "#FFFFFF"
GRID = "#E6E6E6"
MUTED = "#525252"

# Spotrac competitive-balance-tax payrolls, $ millions, as compiled for the
# July 31, 2026 draft. 2026 is a July 29 snapshot, not a closed season total.
# TODO: replace with a Spotrac or Cot's export before treating these as final.
CBT_PAYROLL = {
    2021: 216.5,
    2022: 235.1,
    2023: 291.2,
    2024: 227.8,
    2025: 270.4,
    2026: 259.1,
}
# 2022–26 Basic Agreement, p. 117. The 2021 threshold is not in that document.
CBT_THRESHOLD = {2022: 230, 2023: 233, 2024: 237, 2025: 241, 2026: 244}

# Baseball-Reference, 2026 San Diego Padres team page, read October 11, 2026.
# https://www.baseball-reference.com/teams/SDP/2026.shtml
BREF_2026 = {
    "year": 2026,
    "w": 91,
    "l": 71,
    "r": 722,
    "ra": 681,
    "attendance": 3347081,
    "attendance_note": "2nd of 15, National League",
    "wc": "W",
    "wc_note": "Won NL Wild Card Series 2-0 over the Chicago Cubs (89-73)",
    "nlds": "L",
    "nlds_note": "Lost NL Division Series 1-3 to the Milwaukee Brewers (103-59)",
    "lg": "N",
    "ws": "N",
    "source": "https://www.baseball-reference.com/teams/SDP/2026.shtml",
}

EXPANSION = [
    ("ANA", "Angels", 1961),
    ("TEX", "Rangers", 1961),
    ("HOU", "Astros", 1962),
    ("NYM", "Mets", 1962),
    ("KCR", "Royals", 1969),
    ("MIL", "Brewers", 1969),
    ("SDP", "Padres", 1969),
    ("WSN", "Nationals", 1969),
    ("SEA", "Mariners", 1977),
    ("TOR", "Blue Jays", 1977),
    ("COL", "Rockies", 1993),
    ("FLA", "Marlins", 1993),
    ("ARI", "D-backs", 1998),
    ("TBD", "Rays", 1998),
]

PLAYOFF_ROUNDS = {
    "WS",
    "NLCS",
    "ALCS",
    "NLDS",
    "ALDS",
    "NLDS1",
    "NLDS2",
    "ALDS1",
    "ALDS2",
    "NLWC",
    "ALWC",
    "NLWC1",
    "NLWC2",
    "NLWC3",
    "NLWC4",
    "ALWC1",
    "ALWC2",
    "ALWC3",
    "ALWC4",
}


def load_csv(path: Path) -> list[dict]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if rows:
        key = next(iter(rows[0]))
        if key.startswith("\ufeff"):
            for row in rows:
                row[key.lstrip("\ufeff")] = row.pop(key)
    return rows


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def setup_fonts() -> tuple[fm.FontProperties, fm.FontProperties]:
    sans_path = ROOT / "assets" / "fonts" / "DMSans.ttf"
    mono_path = ROOT / "assets" / "fonts" / "DMMono-Regular.ttf"
    fm.fontManager.addfont(str(sans_path))
    fm.fontManager.addfont(str(mono_path))
    sans = fm.FontProperties(fname=str(sans_path))
    mono = fm.FontProperties(fname=str(mono_path))
    return sans, mono


SANS, MONO = setup_fonts()


def style_ax(ax, title: str, subtitle: str) -> None:
    ax.set_facecolor(WHITE)
    ax.figure.set_facecolor(WHITE)
    ax.set_title("")
    ax.text(0.0, 1.14, title, transform=ax.transAxes, fontproperties=SANS, fontsize=16, color=INK, va="bottom")
    ax.text(
        0.0,
        1.02,
        subtitle,
        transform=ax.transAxes,
        fontproperties=SANS,
        fontsize=9.5,
        color=MUTED,
        va="bottom",
    )
    ax.tick_params(colors=INK, length=0)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(MONO)
        label.set_fontsize(9)
        label.set_color(INK)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.figure.subplots_adjust(top=0.78, bottom=0.16, left=0.08, right=0.98)


def save(fig, stem: str, plotly: dict) -> None:
    for folder in (CHARTS, PUBLIC_CHARTS, PUBLIC_IMG):
        folder.mkdir(parents=True, exist_ok=True)
    png = CHARTS / f"{stem}.png"
    fig.savefig(png, dpi=160, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    (PUBLIC_IMG / f"{stem}.png").write_bytes(png.read_bytes())
    (PUBLIC_CHARTS / f"{stem}.png").write_bytes(png.read_bytes())
    payload = json.dumps(plotly, separators=(",", ":"))
    (CHARTS / f"{stem}.plotly.json").write_text(payload)
    (PUBLIC_CHARTS / f"{stem}.plotly.json").write_text(payload)


def credit(ax, line: str) -> None:
    ax.figure.text(0.01, 0.01, line, fontproperties=SANS, fontsize=8, color=MUTED)


def main() -> None:
    teams = load_csv(LAHMAN / "Teams.csv")
    series = load_csv(LAHMAN / "SeriesPost.csv")
    by_team_year = {(row["yearID"], row["teamID"]): row for row in teams}

    sdp = [row for row in teams if row["franchID"] == "SDP"]
    sdp.sort(key=lambda row: int(row["yearID"]))
    sdp_ids = {row["teamID"] for row in sdp}

    sdp_series = [
        row
        for row in series
        if row["teamIDwinner"] in sdp_ids or row["teamIDloser"] in sdp_ids
    ]
    postseason_years = {int(row["yearID"]) for row in sdp_series}
    pennant_years = {int(row["yearID"]) for row in sdp if row["LgWin"] == "Y"}

    season_rows = []
    for row in sdp:
        year = int(row["yearID"])
        wins = int(row["W"])
        losses = int(row["L"])
        attendance = int(row["attendance"] or 0)
        season_rows.append(
            {
                "year": year,
                "w": wins,
                "l": losses,
                "g": int(row["G"]),
                "r": int(row["R"] or 0),
                "attendance": attendance,
                "postseason": int(year in postseason_years),
                "pennant": int(year in pennant_years),
                "ws": int(row["WSWin"] == "Y"),
                "source": "Lahman 2025",
            }
        )
    season_rows.append(
        {
            "year": 2026,
            "w": BREF_2026["w"],
            "l": BREF_2026["l"],
            "g": BREF_2026["w"] + BREF_2026["l"],
            "r": BREF_2026["r"],
            "attendance": BREF_2026["attendance"],
            "postseason": 1,
            "pennant": 0,
            "ws": 0,
            "source": "Baseball-Reference team page",
        }
    )
    write_csv(
        DATA / "padres_seasons.csv",
        season_rows,
        ["year", "w", "l", "g", "r", "attendance", "postseason", "pennant", "ws", "source"],
    )
    write_csv(
        DATA / "padres_2026_bref.csv",
        [BREF_2026],
        list(BREF_2026.keys()),
    )

    # Chart 1 — season strip
    years = [row["year"] for row in season_rows]
    wins = [row["w"] for row in season_rows]
    colors = []
    hatches = []
    for row in season_rows:
        if row["year"] == 2026:
            colors.append(RED)
            hatches.append("//")
        elif row["postseason"]:
            colors.append(RED)
            hatches.append("")
        else:
            colors.append(BLUE)
            hatches.append("")
    fig, ax = plt.subplots(figsize=(11.2, 5.6))
    bars = ax.bar(years, wins, color=colors, width=0.82, zorder=2)
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
        bar.set_edgecolor(INK)
        bar.set_linewidth(0.3)
    for row in season_rows:
        if row["pennant"]:
            ax.scatter(row["year"], row["w"] + 4, marker="D", s=28, color=INK, zorder=3)
    ax.set_xlim(1968, 2027)
    ax.set_ylabel("Wins", fontproperties=SANS, fontsize=10, color=INK)
    ax.set_xlabel("Season", fontproperties=SANS, fontsize=10, color=INK)
    style_ax(
        ax,
        "Ten Octobers in 58 seasons",
        "Red bars made the postseason. Diamonds are pennants (1984, 1998). The hatched bar is 2026, from Baseball-Reference.",
    )
    credit(ax, "Lahman Baseball Database, 2025 (CC BY-SA). 2026: Baseball-Reference. Artometrics.")
    save(
        fig,
        "chart1_ten_octobers",
        {
            "data": [
                {
                    "type": "bar",
                    "x": years,
                    "y": wins,
                    "marker": {"color": colors, "line": {"color": INK, "width": 0.4}},
                    "hovertemplate": "%{x}: %{y} wins<extra></extra>",
                }
            ],
            "layout": {
                "title": {"text": "Ten Octobers in 58 seasons", "font": {"family": "DM Sans", "color": INK}},
                "paper_bgcolor": WHITE,
                "plot_bgcolor": WHITE,
                "font": {"family": "DM Sans", "color": INK},
                "yaxis": {"title": {"text": "Wins"}, "tickfont": {"family": "DM Mono"}},
                "xaxis": {"title": {"text": "Season"}, "tickfont": {"family": "DM Mono"}},
            },
        },
    )

    # Chart 2 — attendance vs wins, drop the empty 2020 gate
    scatter_rows = [row for row in season_rows if row["year"] != 2026 and row["attendance"] > 0]
    fig, ax = plt.subplots(figsize=(11.2, 5.8))
    for row in scatter_rows:
        color = RED if row["postseason"] else BLUE
        ax.scatter(row["w"], row["attendance"] / 1_000_000, s=42, color=color, zorder=3, edgecolors=INK, linewidths=0.3)
    for year in (2004, 2023, 2025):
        row = next(item for item in scatter_rows if item["year"] == year)
        ax.annotate(
            str(year),
            (row["w"], row["attendance"] / 1_000_000),
            textcoords="offset points",
            xytext=(6, 6),
            fontproperties=MONO,
            fontsize=8,
            color=INK,
        )
    ax.set_xlabel("Regular-season wins", fontproperties=SANS, fontsize=10, color=INK)
    ax.set_ylabel("Attendance, millions", fontproperties=SANS, fontsize=10, color=INK)
    style_ax(
        ax,
        "The park filled without a title",
        "Each dot is a Padres season, 1969–2025. Red made October. 2020 is omitted: Lahman records no attendance.",
    )
    credit(ax, "Attendance and wins: Lahman Baseball Database, 2025 (CC BY-SA). Artometrics.")
    save(
        fig,
        "chart2_demand_wins",
        {
            "data": [
                {
                    "type": "scatter",
                    "mode": "markers",
                    "x": [row["w"] for row in scatter_rows],
                    "y": [round(row["attendance"] / 1_000_000, 3) for row in scatter_rows],
                    "text": [str(row["year"]) for row in scatter_rows],
                    "marker": {
                        "color": [RED if row["postseason"] else BLUE for row in scatter_rows],
                        "size": 9,
                        "line": {"color": INK, "width": 0.4},
                    },
                }
            ],
            "layout": {
                "title": {"text": "The park filled without a title", "font": {"family": "DM Sans", "color": INK}},
                "paper_bgcolor": WHITE,
                "plot_bgcolor": WHITE,
                "font": {"family": "DM Sans", "color": INK},
                "xaxis": {"title": {"text": "Wins"}, "tickfont": {"family": "DM Mono"}},
                "yaxis": {"title": {"text": "Attendance, millions"}, "tickfont": {"family": "DM Mono"}},
            },
        },
    )

    # Chart 3 — tax payroll vs threshold
    pay_years = sorted(CBT_PAYROLL)
    fig, ax = plt.subplots(figsize=(11.2, 5.6))
    ax.bar(
        [str(year) for year in pay_years],
        [CBT_PAYROLL[year] for year in pay_years],
        color=BLUE,
        edgecolor=INK,
        linewidth=0.4,
        zorder=2,
    )
    thresh_years = sorted(CBT_THRESHOLD)
    ax.plot(
        [str(year) for year in thresh_years],
        [CBT_THRESHOLD[year] for year in thresh_years],
        color=INK,
        marker="o",
        linewidth=1.6,
        label="CBA base threshold",
        zorder=3,
    )
    ax.legend(prop=SANS, frameon=False)
    ax.set_ylabel("Millions of dollars", fontproperties=SANS, fontsize=10, color=INK)
    style_ax(
        ax,
        "The tax bill bought October access",
        "Bars are competitive-balance-tax payroll, not cash. The line is the CBA base threshold. 2026 is a July 29 snapshot.",
    )
    credit(ax, "Thresholds: 2022–26 Basic Agreement, p. 117. Payrolls: Spotrac compilation in the July 2026 draft. Artometrics.")
    save(
        fig,
        "chart3_tax_payroll",
        {
            "data": [
                {
                    "type": "bar",
                    "x": [str(year) for year in pay_years],
                    "y": [CBT_PAYROLL[year] for year in pay_years],
                    "marker": {"color": BLUE},
                    "name": "Tax payroll",
                },
                {
                    "type": "scatter",
                    "mode": "lines+markers",
                    "x": [str(year) for year in thresh_years],
                    "y": [CBT_THRESHOLD[year] for year in thresh_years],
                    "line": {"color": INK, "width": 2},
                    "name": "CBA threshold",
                },
            ],
            "layout": {
                "title": {"text": "The tax bill bought October access", "font": {"family": "DM Sans", "color": INK}},
                "paper_bgcolor": WHITE,
                "plot_bgcolor": WHITE,
                "font": {"family": "DM Sans", "color": INK},
                "yaxis": {"title": {"text": "Millions of dollars"}, "tickfont": {"family": "DM Mono"}},
            },
        },
    )
    payroll_rows = []
    for year in pay_years:
        payroll_rows.append(
            {
                "year": year,
                "cbt_payroll_millions": CBT_PAYROLL[year],
                "cba_threshold_millions": CBT_THRESHOLD.get(year, ""),
                "note": "July 29 snapshot" if year == 2026 else "Spotrac CBT, July 2026 draft",
            }
        )
    write_csv(
        DATA / "cbt_payroll.csv",
        payroll_rows,
        ["year", "cbt_payroll_millions", "cba_threshold_millions", "note"],
    )

    # Chart 4 — better-record series, 1995–2025
    better = worse = tied = 0
    for row in series:
        year = int(row["yearID"])
        if year < 1995 or year > 2025 or row["round"] not in PLAYOFF_ROUNDS:
            continue
        winner = by_team_year.get((row["yearID"], row["teamIDwinner"]))
        loser = by_team_year.get((row["yearID"], row["teamIDloser"]))
        if not winner or not loser:
            continue

        def pct(team: dict) -> float:
            w, l = int(team["W"]), int(team["L"])
            return w / (w + l) if w + l else 0.0

        gap = pct(winner) - pct(loser)
        if abs(gap) < 1e-12:
            tied += 1
        elif gap > 0:
            better += 1
        else:
            worse += 1
    padres_wins = sum(1 for row in sdp_series if row["teamIDwinner"] in sdp_ids)
    padres_losses = sum(1 for row in sdp_series if row["teamIDloser"] in sdp_ids)
    fig, ax = plt.subplots(figsize=(11.2, 5.4))
    labels = ["Better record\nwon the series", "Worse record\nwon the series", "Win percentage\ntied"]
    values = [better, worse, tied]
    bar_colors = [BLUE, RED, INK]
    ax.bar(labels, values, color=bar_colors, edgecolor=INK, linewidth=0.4, zorder=2)
    for index, value in enumerate(values):
        ax.text(index, value + 2, str(value), ha="center", fontproperties=MONO, fontsize=12, color=INK)
    ax.set_ylabel("Postseason series, 1995–2025", fontproperties=SANS, fontsize=10, color=INK)
    style_ax(
        ax,
        "October is close to a coin flip",
        f"Of {better + worse + tied} series, the better regular-season team won {better}. Padres series record through 2025: {padres_wins}–{padres_losses}.",
    )
    for label in ax.get_xticklabels():
        label.set_fontproperties(SANS)
    credit(ax, "SeriesPost and Teams, Lahman Baseball Database, 2025 (CC BY-SA). Method: compare regular-season win percentage. Artometrics.")
    save(
        fig,
        "chart4_coin_flip",
        {
            "data": [
                {
                    "type": "bar",
                    "x": ["Better record won", "Worse record won", "Win percentage tied"],
                    "y": values,
                    "marker": {"color": bar_colors, "line": {"color": INK, "width": 0.4}},
                }
            ],
            "layout": {
                "title": {"text": "October is close to a coin flip", "font": {"family": "DM Sans", "color": INK}},
                "paper_bgcolor": WHITE,
                "plot_bgcolor": WHITE,
                "font": {"family": "DM Sans", "color": INK},
                "yaxis": {"tickfont": {"family": "DM Mono"}},
            },
        },
    )
    write_csv(
        DATA / "playoff_series_record_gap.csv",
        [
            {"result": "better_record_won", "series": better},
            {"result": "worse_record_won", "series": worse},
            {"result": "win_pct_tied", "series": tied},
            {"result": "padres_series_wins_through_2025", "series": padres_wins},
            {"result": "padres_series_losses_through_2025", "series": padres_losses},
        ],
        ["result", "series"],
    )

    # Chart 5 — expansion titles
    expansion_rows = []
    for franch_id, label, debut in EXPANSION:
        rows = [row for row in teams if row["franchID"] == franch_id and int(row["yearID"]) >= 1961]
        team_ids = {row["teamID"] for row in rows}
        titles = sum(1 for row in rows if row["WSWin"] == "Y")
        pennants = sum(1 for row in rows if row["LgWin"] == "Y")
        title_years = sorted(int(row["yearID"]) for row in rows if row["WSWin"] == "Y")
        ps_years = sorted(
            {
                int(row["yearID"])
                for row in series
                if row["teamIDwinner"] in team_ids or row["teamIDloser"] in team_ids
            }
        )
        series_wins = sum(1 for row in series if row["teamIDwinner"] in team_ids)
        series_losses = sum(1 for row in series if row["teamIDloser"] in team_ids)
        ranks = []
        for row in rows:
            if not row["attendance"] or int(row["attendance"]) == 0:
                continue
            season = [
                other
                for other in teams
                if other["yearID"] == row["yearID"]
                and other["lgID"] in ("AL", "NL")
                and other["attendance"]
                and int(other["attendance"]) > 0
            ]
            season.sort(key=lambda other: -int(other["attendance"]))
            rank = next(index for index, other in enumerate(season, 1) if other["teamID"] == row["teamID"])
            ranks.append(rank)
        ranks.sort()
        median_rank = ranks[len(ranks) // 2] if ranks else ""
        expansion_rows.append(
            {
                "franchID": franch_id,
                "club": label,
                "debut": debut,
                "titles": titles,
                "title_years": " ".join(str(year) for year in title_years),
                "pennants": pennants,
                "postseasons": len(ps_years),
                "series_wins": series_wins,
                "series_losses": series_losses,
                "pennants_per_postseason": round(pennants / len(ps_years), 3) if ps_years else "",
                "median_attendance_rank": median_rank,
                "attendance_seasons": len(ranks),
            }
        )
    expansion_rows.sort(key=lambda row: (row["titles"], row["pennants"], row["postseasons"]))
    write_csv(DATA / "expansion_clubs.csv", expansion_rows, list(expansion_rows[0].keys()))
    fig, ax = plt.subplots(figsize=(11.2, 6.4))
    clubs = [row["club"] for row in expansion_rows]
    title_counts = [row["titles"] for row in expansion_rows]
    bar_colors = [RED if row["franchID"] == "SDP" else BLUE for row in expansion_rows]
    ax.barh(clubs, title_counts, color=bar_colors, edgecolor=INK, linewidth=0.4, zorder=2)
    ax.set_xlabel("World Series titles", fontproperties=SANS, fontsize=10, color=INK)
    style_ax(
        ax,
        "Nine of the 14 expansion clubs have a title",
        "Clubs added since 1961. San Diego, Milwaukee, Seattle, Colorado, and Tampa Bay are still at zero.",
    )
    for label in ax.get_yticklabels():
        label.set_fontproperties(SANS)
    credit(ax, "Lahman Baseball Database, 2025 (CC BY-SA). Titles are WSWin seasons. Artometrics.")
    save(
        fig,
        "chart5_expansion_titles",
        {
            "data": [
                {
                    "type": "bar",
                    "orientation": "h",
                    "y": clubs,
                    "x": title_counts,
                    "marker": {"color": bar_colors, "line": {"color": INK, "width": 0.4}},
                }
            ],
            "layout": {
                "title": {"text": "Nine of the 14 expansion clubs have a title", "font": {"family": "DM Sans", "color": INK}},
                "paper_bgcolor": WHITE,
                "plot_bgcolor": WHITE,
                "font": {"family": "DM Sans", "color": INK},
                "xaxis": {"title": {"text": "World Series titles"}, "tickfont": {"family": "DM Mono"}},
                "height": 640,
            },
        },
    )

    # Chart 6 — pennant clock. The first bar is not a gap between pennants.
    clock = [
        ("1969–84\nDebut to first pennant", 15, BLUE),
        ("1984–98\nYears between pennants", 14, BLUE),
        ("1998–2026\nYears since the last pennant", 28, RED),
    ]
    fig, ax = plt.subplots(figsize=(11.2, 5.4))
    ax.bar(
        [item[0] for item in clock],
        [item[1] for item in clock],
        color=[item[2] for item in clock],
        edgecolor=INK,
        linewidth=0.4,
        zorder=2,
    )
    for index, item in enumerate(clock):
        ax.text(index, item[1] + 0.6, str(item[1]), ha="center", fontproperties=MONO, fontsize=12, color=INK)
    ax.set_ylabel("Years", fontproperties=SANS, fontsize=10, color=INK)
    style_ax(
        ax,
        "The wait that matters started in 1998",
        "The first bar runs from the 1969 debut to the first pennant. It is not a gap between pennants.",
    )
    for label in ax.get_xticklabels():
        label.set_fontproperties(SANS)
    credit(ax, "Pennant years 1984 and 1998: Lahman LgWin. The 2026 endpoint is the completed season. Artometrics.")
    save(
        fig,
        "chart6_pennant_clock",
        {
            "data": [
                {
                    "type": "bar",
                    "x": ["Debut to first pennant", "Years between pennants", "Years since the last pennant"],
                    "y": [15, 14, 28],
                    "marker": {"color": [BLUE, BLUE, RED], "line": {"color": INK, "width": 0.4}},
                }
            ],
            "layout": {
                "title": {"text": "The wait that matters started in 1998", "font": {"family": "DM Sans", "color": INK}},
                "paper_bgcolor": WHITE,
                "plot_bgcolor": WHITE,
                "font": {"family": "DM Sans", "color": INK},
                "yaxis": {"title": {"text": "Years"}, "tickfont": {"family": "DM Mono"}},
            },
        },
    )

    # Attendance checkpoints used in the prose
    def mean_att(start: int, end: int) -> tuple[int, int]:
        vals = [
            row["attendance"]
            for row in season_rows
            if start <= row["year"] <= end and row["attendance"] > 0 and row["year"] != 2026
        ]
        return round(sum(vals) / len(vals)), len(vals)

    pre_petco = mean_att(1996, 2003)
    petco = mean_att(2004, 2019)
    winning = sum(1 for row in season_rows if row["year"] <= 2025 and row["w"] > row["l"])
    summary = {
        "lahman_seasons": 57,
        "seasons_through_2026": 58,
        "postseasons_through_2025": len(postseason_years),
        "postseason_years": sorted(postseason_years),
        "postseasons_through_2026": len(postseason_years) + 1,
        "pennants": sorted(pennant_years),
        "winning_seasons_through_2025": winning,
        "series_through_2025": f"{padres_wins}-{padres_losses}",
        "series_through_2026": f"{padres_wins + 1}-{padres_losses + 1}",
        "attendance_1996_2003": pre_petco,
        "attendance_2004_2019": petco,
        "attendance_2004": next(row["attendance"] for row in season_rows if row["year"] == 2004),
        "attendance_2025": next(row["attendance"] for row in season_rows if row["year"] == 2025),
        "coin_flip": {"better": better, "worse": worse, "tied": tied},
        "cbt_sum_millions": round(sum(CBT_PAYROLL.values()), 1),
        "expansion": expansion_rows,
    }
    (DATA / "summary.json").write_text(json.dumps(summary, indent=2))
    PUBLIC_DATA.mkdir(parents=True, exist_ok=True)
    for name in (
        "padres_seasons.csv",
        "padres_2026_bref.csv",
        "cbt_payroll.csv",
        "playoff_series_record_gap.csv",
        "expansion_clubs.csv",
        "summary.json",
    ):
        (PUBLIC_DATA / name).write_bytes((DATA / name).read_bytes())
    license_src = LAHMAN / "LICENSE_NOTE.txt"
    (DATA / "LAHMAN_CREDIT.txt").write_text(
        license_src.read_text()
        + "\nDerived tables in this folder are CC BY-SA 3.0. Attribute: Lahman Baseball Database, SABR.\n"
        + "2026 rows and padres_2026_bref.csv are Baseball-Reference team-page figures, cited on that page, not Lahman.\n"
        + "cbt_payroll.csv is a Spotrac compilation carried from the July 2026 draft, not a Lahman table.\n"
    )
    (PUBLIC_DATA / "LAHMAN_CREDIT.txt").write_text((DATA / "LAHMAN_CREDIT.txt").read_text())
    print(json.dumps({k: summary[k] for k in summary if k != "expansion"}, indent=2))
    print("--- expansion ---")
    for row in expansion_rows:
        print(
            f"{row['club']:12} titles {row['titles']} ({row['title_years']}) penn {row['pennants']} "
            f"PS {row['postseasons']} series {row['series_wins']}-{row['series_losses']} "
            f"conv {row['pennants_per_postseason']} attRank {row['median_attendance_rank']}"
        )


if __name__ == "__main__":
    main()
