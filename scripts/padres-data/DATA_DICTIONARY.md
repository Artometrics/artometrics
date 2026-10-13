# Data dictionary — `data/padres/clean/`

- **padres_seasons.csv** — One row per season 1969–2026. `postseason`/`pennant`/`ws` flags; `source` is Lahman 2025 or Baseball-Reference for 2026.
- **padres_2026_bref.csv** — Publish row for 2026 only (W-L, runs, attendance, wild-card and NLDS result codes).
- **cbt_payroll.csv** — Spotrac CBT payroll ($M) and CBA threshold where applicable.
- **playoff_series_record_gap.csv** — Aggregate counts for Lopez-style coin-flip chart and Padres series W-L through 2025.
- **playoff_series_outcomes_1995_2025.csv** — Series-level rows for bootstrap (`outcome`: better_won, worse_won, tied).
- **expansion_clubs.csv** — Fourteen expansion franchises: titles, pennants, postseasons, series record, pennants per postseason, median attendance rank.
- **summary.json** — Machine-readable headline stats for charts and prose checks.
- **rate_bootstrap.csv** — Point estimates and 95% bootstrap intervals for key rates.
- **old_vs_new.csv** — Published July 2026 figures vs October 2026 audit (`status`, `source` columns).
- **audit_summary.json** — Run metadata, MLB API check, bootstrap snapshot.

Verification only: **data/padres/verify/mlb_api_check.json** (not mirrored to `public/`).
