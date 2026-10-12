# Methods note — Franchise data (vintage 2026-10)

**Sources (access 2026-10-12 PT unless noted).** S001 TidyTuesday 2019-07-02 Media Franchise Revenues; S007 Wikipedia "List of highest-grossing media franchises" rev 904026364 (2019-06-29); S017 same page rev 1379832186 (2026-10-12); S091 Wikipedia "2025 in film" rev 1378645325 (citing Box Office Mojo / The Numbers); S092 "2026 in film" rev 1379926625; S090 FRED CPIAUCSL (U.S. BLS CPI-U, through Aug 2026). Raw wikitext snapshots are committed under `articles/franchise/data/raw/` so every number can be rebuilt offline.

**Definitions.** Revenue = Wikipedia editors' lifetime estimate of gross consumer spend (retail sales of licensed goods at retail value, not licensor income), nominal USD, mixed years. Box office = worldwide theatrical gross. These are editorial compilations of press releases and trade estimates, not audited accounts.

**Uncertainty.** The list is not a random sample, so 95% intervals are nonparametric bootstraps over franchises (5,000 draws) and express how sensitive a share is to which franchises happen to be listed — not sampling error in the usual sense. Merchandise share 55.8% [44.0–66.2]; video games 17.9% [11.2–26.2]; box office 18.3% [12.8–25.6]; top owner (Disney) 29.7% [18.2–43.4]; top five owners 58.2% [52.7–72.6].

**Sensitivity.** Shares are stable across: dropping placeholder rows; dropping the unallocated remainder; restricting to the 82 franchises present in both vintages (box office 15.4%, merch 60.2%); and the ≥$4B floor (box office 15.0%).

**Limitations.** (1) Category totals depend on how Wikipedia editors itemise; the 2026 page itemises box office more fully than the 2019 TidyTuesday schema, so part of the box-office jump (8.9%→18.3%) is measurement, not market change. (2) Large revisions (Hello Kitty 80→33.5, Mario 35→9.7, Gundam 25.5→5.0) are source corrections, not declines. (3) Region and parent coding are rule-based with hand overrides. (4) No streaming dollars. (5) 2026 box office is in-progress.
