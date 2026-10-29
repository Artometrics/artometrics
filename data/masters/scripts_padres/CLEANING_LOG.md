# Padres data cleaning log (vintage 2026-10)

Script: `scripts/padres-data/clean_audit.py` (seed 20261013, 5,000 bootstrap draws).  
Outputs: `data/padres/clean/` (mirrored to `articles/padres/data/` and `public/data/articles/padres/data/`).  
Lahman raw tables under `articles/padres/data/lahman/` are never edited in place.

## R1 — Lahman scope

- Filter `Teams.csv` to `franchID == SDP` for season strips (1969–2025, n = 57).
- Postseason years: any `SeriesPost` row where Padres `teamID` is winner or loser (not division flags alone).
- Pennants: `LgWin == Y` on Padres team rows.
- Expansion peer set: 14 franchises with debut ≥ 1961 per plan (Angels through Rays).

## R2 — 2026 season (not in Lahman)

- Publish wins, losses, attendance, and series outcomes from `data/padres/raw/padres_2026_bref.csv` (Baseball-Reference, per-page credit).
- Fact-check W-L against MLB Stats API NL standings (`verify/mlb_api_check.json`). API rows are not republished as a dataset.

## R3 — Competitive-balance tax payroll

- Values live in `data/padres/raw/spotrac_cbt_payroll.csv` (Spotrac compilation, July 2026 draft).
- Label everywhere as **tax payroll**, not cash spent. Sum 2021–26 = $1,500.1M.
- CBA thresholds 2022–26 from Basic Agreement p. 117 ($230 / $233 / $237 / $241 / $244 million).

## R4 — Coin-flip series (Lopez et al. method)

- Join `SeriesPost` to both clubs' `Teams` regular-season records, 1995–2025.
- Qualifying rounds: division series, LCS, wild card, World Series (see `compute.PLAYOFF_ROUNDS`).
- “Better record” = higher regular-season win percentage; ties counted separately.
- Bootstrap resamples series rows (untied only) for the 53.2% rate CI.

## R5 — Pennant clock chart

- Bar 1: 1969 debut → first pennant (1984), 15 years — **not** a gap between pennants.
- Bar 2: 1984 → 1998, 14 years between pennants.
- Bar 3: 1998 → 2026 endpoint, 28 years since last pennant.

## R6 — Attendance

- Drop 2020 from scatter (Lahman attendance 0). Do not gross up the 60-game 2020 season for wins charts.
- Means: 1996–2003 pre-Petco; 2004–2019 Petco opening era (exclude 2020 zero gate).

## R7 — Old vs new ledger

- `old_vs_new.csv` maps every number that appeared on the July 2026 live page or sports-canon generator to the October 2026 audited value, with `status` (unchanged, updated, corrected, unsourced_removed).

## Flow counts (2026-10-13 run)

| Stage | Count |
|-------|------:|
| Lahman Padres seasons | 57 |
| With 2026 publish row | 58 |
| Postseasons through 2025 | 9 |
| Postseasons through 2026 | 10 |
| MLB playoff series 1995–2025 | 259 |
| Better / worse / tied | 132 / 116 / 11 |
| Expansion clubs | 14 |

## Sources

- Lahman Baseball Database 2025 (CC BY-SA 3.0), SABR.
- Baseball-Reference team and postseason pages (2026, 2024 NLDS, 2025 NLWC).
- MLB Stats API standings (verification only).
- Spotrac CBT payroll compilation (cite, do not redistribute).
