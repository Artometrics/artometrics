#!/usr/bin/env python3
"""Padres dataset audit: Lahman 1969–2025 + verified 2026, bootstrap CIs, old-vs-new.

Run: python3 scripts/padres-data/clean_audit.py

Inputs (committed):
  articles/padres/data/lahman/*.csv          Lahman 2025 subset (CC BY-SA)
  data/padres/raw/padres_2026_bref.csv       Baseball-Reference figures for publish
  data/padres/raw/spotrac_cbt_payroll.csv    Spotrac CBT compilation (cite only)

MLB Stats API is used for fact-checking 2026 W-L only; see verify/mlb_api_check.json.
Outputs: data/padres/clean/* (mirrored to articles/padres/data/ and public/).
"""

from __future__ import annotations

import json
import shutil
import sys
import urllib.request
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from compute import compute, write_derived  # noqa: E402

OUT = REPO / "data" / "padres" / "clean"
VERIFY = REPO / "data" / "padres" / "verify"
ART_DATA = REPO / "articles" / "padres" / "data"
PUBLIC_DATA = REPO / "public" / "data" / "articles" / "padres" / "data"
SEED = 20261013
B = 5000
rng = np.random.default_rng(SEED)

MLB_TEAM_ID = 135


def mlb_standings_2026() -> dict:
    url = (
        "https://statsapi.mlb.com/api/v1/standings"
        "?leagueId=104&season=2026&standingsTypes=regularSeason"
    )
    with urllib.request.urlopen(url, timeout=60) as resp:
        data = json.load(resp)
    for rec in data.get("records", []):
        for team in rec.get("teamRecords", []):
            if team.get("team", {}).get("id") == MLB_TEAM_ID:
                rec = team.get("leagueRecord", {})
                return {
                    "wins": rec.get("wins"),
                    "losses": rec.get("losses"),
                    "division_rank": team.get("divisionRank"),
                    "wild_card_rank": team.get("wildCardRank"),
                    "source_url": url,
                    "checked_at": "2026-10-13",
                }
    raise RuntimeError("Padres not found in 2026 NL standings")


def bootstrap_rate(successes: int, trials: int, label: str) -> dict:
    if trials <= 0:
        return {"metric": label, "rate": None, "n": trials, "ci_low": None, "ci_high": None}
    draws = rng.binomial(trials, successes / trials, size=B) / trials
    return {
        "metric": label,
        "rate": round(successes / trials, 4),
        "n": trials,
        "ci_low": round(float(np.percentile(draws, 2.5)), 4),
        "ci_high": round(float(np.percentile(draws, 97.5)), 4),
    }


def bootstrap_series_better_rate(outcomes: list[dict]) -> dict:
    untied = [row for row in outcomes if row["outcome"] != "tied"]
    n = len(untied)
    if not n:
        return bootstrap_rate(0, 0, "better_record_win_rate_untied_1995_2025")
    flags = np.array([1 if row["outcome"] == "better_won" else 0 for row in untied])
    draws = rng.choice(flags, size=(B, n), replace=True).mean(axis=1)
    return {
        "metric": "better_record_win_rate_untied_1995_2025",
        "rate": round(float(flags.mean()), 4),
        "n": n,
        "ci_low": round(float(np.percentile(draws, 2.5)), 4),
        "ci_high": round(float(np.percentile(draws, 97.5)), 4),
    }


def bootstrap_expansion_pennant_rate(expansion: list[dict], franch_id: str) -> dict:
    row = next(r for r in expansion if r["franchID"] == franch_id)
    ps = int(row["postseasons"])
    pen = int(row["pennants"])
    if ps == 0:
        return bootstrap_rate(0, 0, f"pennants_per_postseason_{franch_id}")
    draws = rng.binomial(ps, pen / ps, size=B) / ps
    return {
        "metric": f"pennants_per_postseason_{franch_id}",
        "rate": round(pen / ps, 4),
        "n": ps,
        "ci_low": round(float(np.percentile(draws, 2.5)), 4),
        "ci_high": round(float(np.percentile(draws, 97.5)), 4),
    }


OLD_VS_NEW_ROWS = [
    # figure, old_published, raw_new, clean_new, unit, status, source
    ("Franchise seasons counted", "57", "57", "58", "seasons", "updated", "Lahman through 2025; 2026 completed"),
    ("Postseason appearances", "9", "9", "10", "count", "updated", "Lahman SeriesPost + 2026 B-Ref"),
    ("World Series titles", "0", "0", "0", "count", "unchanged", "Lahman WSWin"),
    ("National League pennants", "2", "2", "2", "count", "unchanged", "Lahman LgWin 1984 1998"),
    ("Postseason series record", "7-9", "7-9", "8-10", "W-L", "updated", "Lahman through 2025; +1 W +1 L in 2026"),
    ("Winning seasons (through 2025)", "19", "19", "20", "count", "updated", "Lahman W>L; 2026 91-71"),
    ("2026 regular-season record", "55-53 in progress", "", "91-71", "W-L", "corrected", "MLB Stats API + Baseball-Reference"),
    ("Sale approval status", "waits on 22 of 29 owners", "", "unanimous Aug 17 2026", "text", "corrected", "MLB press release"),
    ("FAQ deciding-game runs (2024+2025)", "combined eight runs", "", "0 + 1", "runs", "corrected", "Baseball-Reference NLDS 2024 G4-5; NLWC 2025 G3"),
    ("Payroll headline wording", "about $1.5bn of payroll / cash spent", "", "$1,500.1M CBT tax payroll sum", "USD millions", "corrected", "Spotrac CBT; not cash"),
    ("Pennant chart first bar label", "years between pennants", "", "debut to first pennant", "axis", "corrected", "chart6_pennant_clock"),
    ("Postseasons since 2020", "four in six years (blueprint)", "five since 2020", "5", "count", "aligned", "2020 2022 2024 2025 2026"),
    ("Better-record series wins 1995-2025", "132", "132", "132", "series", "unchanged", "Lahman SeriesPost join"),
    ("Worse-record series wins 1995-2025", "116", "116", "116", "series", "unchanged", "Lahman SeriesPost join"),
    ("Tied win-pct series 1995-2025", "11", "11", "11", "series", "unchanged", "Lahman SeriesPost join"),
    ("Better record among untied series", "53.2%", "53.2%", "53.2% [bootstrap]", "percent", "unchanged", "132/(132+116)"),
    ("2025 attendance", "3,437,201", "3437201", "3437201", "fans", "unchanged", "Lahman Teams 2025"),
    ("2026 attendance", "", "", "3347081", "fans", "new", "Baseball-Reference team page"),
    ("Petco era avg attendance 2004-19", "~2.37M", "2372417", "2372417", "fans/season", "unchanged", "Lahman mean"),
    ("Pre-Petco avg 1996-2003", "~2.29M", "2292236", "2292236", "fans/season", "unchanged", "Lahman mean"),
    ("Wins 2019", "70", "70", "70", "wins", "unchanged", "Lahman"),
    ("Wins 2020", "37", "37", "37", "wins", "unchanged", "Lahman 60-game season"),
    ("Wins 2021", "79", "79", "79", "wins", "unchanged", "Lahman"),
    ("Wins 2022", "89", "89", "89", "wins", "unchanged", "Lahman"),
    ("Wins 2023", "82", "82", "82", "wins", "unchanged", "Lahman"),
    ("Wins 2024", "93", "93", "93", "wins", "unchanged", "Lahman"),
    ("Wins 2025", "90", "90", "90", "wins", "unchanged", "Lahman"),
    ("CBT payroll sum 2021-26", "~$1.5bn", "1500.1", "1500.1", "USD millions", "unchanged", "Spotrac draft"),
    ("70,000 DTC subscribers", "stated in July draft", "", "removed", "count", "unsourced_removed", "needs SBJ URL"),
    ("25,000 memberships / 3-year wait", "stated in July draft", "", "removed", "count", "unsourced_removed", "needs club or SBJ"),
    ("$858M owed five players", "stated in July draft", "", "removed", "USD", "unsourced_removed", "needs Spotrac/Cot's export"),
    ("$1.48bn more than Cohen Mets", "stated in July draft", "", "removed", "USD", "unsourced_removed", "needs cited Mets price"),
    ("Farm rank last of 30", "stated in July draft", "", "removed", "rank", "unsourced_removed", "needs FanGraphs/BA cite"),
    ("Three bids at least $3.5bn", "stated in July draft", "", "removed", "count", "unsourced_removed", "needs SDUT/SBJ"),
]


def write_old_vs_new(path: Path, bundle: dict) -> None:
    gap = bundle["playoff_gap"]
    untied = gap["better"] + gap["worse"]
    rate = gap["better"] / untied if untied else 0
    boot = bootstrap_series_better_rate(bundle["series_outcomes"])
    rate_ci = f"{boot['rate']*100:.1f}% [{boot['ci_low']*100:.1f}–{boot['ci_high']*100:.1f}]"

    import csv

    rows = []
    for item in OLD_VS_NEW_ROWS:
        figure, old, raw, clean, unit, status, source = item
        if figure.startswith("Better record among untied"):
            clean = rate_ci
        rows.append(
            {
                "figure": figure,
                "old_published": old,
                "raw_new": raw,
                "clean_new_oct2026": clean,
                "unit": unit,
                "status": status,
                "source": source,
            }
        )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "figure",
                "old_published",
                "raw_new",
                "clean_new_oct2026",
                "unit",
                "status",
                "source",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def mirror_outputs() -> None:
    ART_DATA.mkdir(parents=True, exist_ok=True)
    PUBLIC_DATA.mkdir(parents=True, exist_ok=True)
    credit = (REPO / "data" / "padres" / "LAHMAN_CREDIT.txt").read_text(encoding="utf-8")
    for name in (
        "padres_seasons.csv",
        "padres_2026_bref.csv",
        "cbt_payroll.csv",
        "playoff_series_record_gap.csv",
        "playoff_series_outcomes_1995_2025.csv",
        "expansion_clubs.csv",
        "summary.json",
        "rate_bootstrap.csv",
        "old_vs_new.csv",
        "audit_summary.json",
    ):
        src = OUT / name
        if src.exists():
            shutil.copy2(src, ART_DATA / name)
            shutil.copy2(src, PUBLIC_DATA / name)
    (ART_DATA / "LAHMAN_CREDIT.txt").write_text(credit, encoding="utf-8")
    (PUBLIC_DATA / "LAHMAN_CREDIT.txt").write_text(credit, encoding="utf-8")
    lahman_src = REPO / "articles" / "padres" / "data" / "lahman"
    lahman_dst = REPO / "data" / "padres" / "lahman"
    if lahman_src.exists() and not lahman_dst.exists():
        shutil.copytree(lahman_src, lahman_dst)


def main() -> None:
    VERIFY.mkdir(parents=True, exist_ok=True)
    mlb = mlb_standings_2026()
    bref = compute()["summary"]["bref_2026"]
    check = {
        "mlb_api": mlb,
        "bref_publish_row": {"w": bref["w"], "l": bref["l"]},
        "wins_match": mlb["wins"] == bref["w"] and mlb["losses"] == bref["l"],
    }
    (VERIFY / "mlb_api_check.json").write_text(json.dumps(check, indent=2), encoding="utf-8")
    if not check["wins_match"]:
        raise SystemExit(f"MLB API {mlb['wins']}-{mlb['losses']} != B-Ref {bref['w']}-{bref['l']}")

    bundle = compute()
    write_derived(OUT, bundle)

    gap = bundle["playoff_gap"]
    boot_rows = [
        bootstrap_series_better_rate(bundle["series_outcomes"]),
        bootstrap_rate(gap["better"], gap["better"] + gap["worse"] + gap["tied"], "better_record_won_share_all_series"),
        bootstrap_expansion_pennant_rate(bundle["expansion_rows"], "SDP"),
        bootstrap_rate(10, 58, "padres_postseason_rate_through_2026"),
        bootstrap_rate(2, 10, "padres_pennant_rate_given_postseason_through_2026"),
    ]
    import csv

    with (OUT / "rate_bootstrap.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "rate", "n", "ci_low", "ci_high"])
        writer.writeheader()
        writer.writerows(boot_rows)

    write_old_vs_new(OUT / "old_vs_new.csv", bundle)

    audit = {
        "seed": SEED,
        "bootstrap_draws": B,
        "lahman_tables": ["Teams", "SeriesPost", "TeamsFranchises", "Salaries"],
        "mlb_api_check": check,
        "summary_keys": {k: bundle["summary"][k] for k in bundle["summary"] if k != "expansion"},
        "bootstrap": boot_rows,
    }
    (OUT / "audit_summary.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

    mirror_outputs()
    print(json.dumps(audit["summary_keys"], indent=2))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
