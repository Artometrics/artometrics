"""Padres derived tables from Lahman 1969–2025 plus verified 2026."""

from __future__ import annotations

import csv
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LAHMAN = REPO / "articles" / "padres" / "data" / "lahman"
RAW = REPO / "data" / "padres" / "raw"
BREF_2026_PATH = RAW / "padres_2026_bref.csv"
CBT_PATH = RAW / "spotrac_cbt_payroll.csv"

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
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if rows:
        key = next(iter(rows[0]))
        if key.startswith("\ufeff"):
            for row in rows:
                row[key.lstrip("\ufeff")] = row.pop(key)
    return rows


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def mean_att(season_rows: list[dict], start: int, end: int) -> tuple[int, int]:
    vals = [
        row["attendance"]
        for row in season_rows
        if start <= row["year"] <= end and row["attendance"] > 0 and row["year"] != 2026
    ]
    return round(sum(vals) / len(vals)), len(vals)


def load_bref_2026() -> dict:
    rows = load_csv(BREF_2026_PATH)
    row = rows[0]
    return {
        "year": int(row["year"]),
        "w": int(row["w"]),
        "l": int(row["l"]),
        "r": int(row["r"]),
        "ra": int(row["ra"]),
        "attendance": int(row["attendance"]),
        "wc": row["wc"],
        "nlds": row["nlds"],
        "lg": row.get("lg", "N"),
        "ws": row.get("ws", "N"),
        "source": row["source"],
    }


def load_cbt() -> dict[int, float]:
    out: dict[int, float] = {}
    for row in load_csv(CBT_PATH):
        out[int(row["year"])] = float(row["cbt_payroll_millions"])
    return out


def compute() -> dict:
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

    season_rows: list[dict] = []
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

    bref = load_bref_2026()
    season_rows.append(
        {
            "year": bref["year"],
            "w": bref["w"],
            "l": bref["l"],
            "g": bref["w"] + bref["l"],
            "r": bref["r"],
            "attendance": bref["attendance"],
            "postseason": 1,
            "pennant": 0,
            "ws": 0,
            "source": "Baseball-Reference team page",
        }
    )

    cbt = load_cbt()
    cbt_rows = load_csv(CBT_PATH)
    payroll_rows = []
    for row in cbt_rows:
        payroll_rows.append(
            {
                "year": int(row["year"]),
                "cbt_payroll_millions": float(row["cbt_payroll_millions"]),
                "cba_threshold_millions": row["cba_threshold_millions"] or "",
                "note": row["note"],
            }
        )

    series_outcomes: list[dict] = []
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

        wp, lp = pct(winner), pct(loser)
        gap = wp - lp
        if abs(gap) < 1e-12:
            tied += 1
            tag = "tied"
        elif gap > 0:
            better += 1
            tag = "better_won"
        else:
            worse += 1
            tag = "worse_won"
        series_outcomes.append(
            {
                "year": year,
                "round": row["round"],
                "winner": row["teamIDwinner"],
                "loser": row["teamIDloser"],
                "winner_win_pct": round(wp, 5),
                "loser_win_pct": round(lp, 5),
                "outcome": tag,
            }
        )

    padres_wins = sum(1 for row in sdp_series if row["teamIDwinner"] in sdp_ids)
    padres_losses = sum(1 for row in sdp_series if row["teamIDloser"] in sdp_ids)

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

    pre_petco = mean_att(season_rows, 1996, 2003)
    petco = mean_att(season_rows, 2004, 2019)
    winning = sum(1 for row in season_rows if row["year"] <= 2025 and row["w"] > row["l"])

    wins_2019_2025 = {
        int(row["yearID"]): int(row["W"])
        for row in sdp
        if 2019 <= int(row["yearID"]) <= 2025
    }

    return {
        "season_rows": season_rows,
        "payroll_rows": payroll_rows,
        "playoff_gap": {
            "better": better,
            "worse": worse,
            "tied": tied,
        },
        "series_outcomes": series_outcomes,
        "padres_series": (padres_wins, padres_losses),
        "expansion_rows": expansion_rows,
        "postseason_years": postseason_years,
        "pennant_years": pennant_years,
        "summary": {
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
            "attendance_2026": bref["attendance"],
            "wins_2019_2025": wins_2019_2025,
            "coin_flip": {"better": better, "worse": worse, "tied": tied},
            "cbt_sum_millions": round(sum(cbt.values()), 1),
            "expansion": expansion_rows,
            "bref_2026": bref,
        },
    }


def write_derived(out_dir: Path, bundle: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        out_dir / "padres_seasons.csv",
        bundle["season_rows"],
        ["year", "w", "l", "g", "r", "attendance", "postseason", "pennant", "ws", "source"],
    )
    bref = bundle["summary"]["bref_2026"]
    write_csv(
        out_dir / "padres_2026_bref.csv",
        [
            {
                "year": bref["year"],
                "w": bref["w"],
                "l": bref["l"],
                "r": bref["r"],
                "ra": bref["ra"],
                "attendance": bref["attendance"],
                "wc": bref["wc"],
                "nlds": bref["nlds"],
                "lg": "N",
                "ws": "N",
                "source": bref["source"],
            }
        ],
        ["year", "w", "l", "r", "ra", "attendance", "wc", "nlds", "lg", "ws", "source"],
    )
    write_csv(
        out_dir / "cbt_payroll.csv",
        bundle["payroll_rows"],
        ["year", "cbt_payroll_millions", "cba_threshold_millions", "note"],
    )
    gap = bundle["playoff_gap"]
    pw, pl = bundle["padres_series"]
    write_csv(
        out_dir / "playoff_series_record_gap.csv",
        [
            {"result": "better_record_won", "series": gap["better"]},
            {"result": "worse_record_won", "series": gap["worse"]},
            {"result": "win_pct_tied", "series": gap["tied"]},
            {"result": "padres_series_wins_through_2025", "series": pw},
            {"result": "padres_series_losses_through_2025", "series": pl},
        ],
        ["result", "series"],
    )
    write_csv(
        out_dir / "playoff_series_outcomes_1995_2025.csv",
        bundle["series_outcomes"],
        ["year", "round", "winner", "loser", "winner_win_pct", "loser_win_pct", "outcome"],
    )
    write_csv(out_dir / "expansion_clubs.csv", bundle["expansion_rows"], list(bundle["expansion_rows"][0].keys()))
    summary = bundle["summary"]
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
