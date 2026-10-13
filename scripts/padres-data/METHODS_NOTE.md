# Methods note — Padres data (vintage 2026-10)

**Sources (access 2026-10-11 through 2026-10-13 PT).** Lahman Baseball Database 2025 edition (Teams, SeriesPost, TeamsFranchises; Salaries retained but not used in this report). Baseball-Reference San Diego Padres 2026 team page and cited postseason pages. MLB Stats API NL regular-season standings 2026 (fact-check only). Spotrac competitive-balance-tax payrolls as compiled for the July 2026 draft (`data/padres/raw/spotrac_cbt_payroll.csv`).

**Definitions.** A postseason appearance is a calendar year with at least one Padres row in `SeriesPost`. Series record counts each postseason round row as one win or loss. Tax payroll is Spotrac's CBT accounting average, not cash paid. Attendance is Lahman home attendance through 2025; 2026 from Baseball-Reference.

**Uncertainty.** Bootstrap intervals (5,000 draws, seed 20261013) treat each qualifying playoff series (or franchise-season for rate metrics) as an exchangeable unit. They describe sensitivity to the observed sample, not a full hierarchical model of team strength.

**Reported intervals (95%).**

- Better regular-season record wins among **untied** series, 1995–2025: see `rate_bootstrap.csv` row `better_record_win_rate_untied_1995_2025`.
- Padres pennants per postseason (Lahman through 2025 only): `pennants_per_postseason_SDP`.
- Postseason rate 10/58 and pennants given postseason 2/10 include 2026 as a postseason year without a pennant.

**Limitations.** (1) Lahman 2025 does not include 2026; publish rows are external. (2) Spotrac payrolls are proprietary snapshots. (3) Coin-flip join cannot resolve teams with missing Lahman rows. (4) October runs-per-game chart deferred (Retrosheet not yet ingested). (5) MLB API terms prohibit bulk republication of API-derived tables.
