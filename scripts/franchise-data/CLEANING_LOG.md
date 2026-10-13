# Franchise dataset — cleaning & update log (2026-10-12)

Script: `scripts/franchise-data/clean_audit.py` (seed 20261012, 5,000 bootstrap draws). Outputs in `articles/franchise/data/clean/`. Raw inputs are never edited.

## Audit findings (2019 TidyTuesday ledger, `franchise.csv`)
| Check | Result |
|---|---|
| Rows / franchises | 321 / 103 |
| Missing cells, duplicate franchise×category | 0 / 0 |
| Placeholder rows (< $0.01B, e.g. Star Wars TV $0.004B) | 15 |
| Wiki citation residue (e.g. `Khara[dc][279][280]`) | 6 cells |
| Double spaces in names/owners | 59 cells |
| Year created | 1924–2013 (no franchise younger than 2013) |
| Owners | 2019 corporate parents (AT&T, Viacom, Activision Blizzard, 21st Century Fox) now stale |
| Verification vs Wikipedia rev 904026364 (2019-06-29), random 40 | 39 matched; **5/39 (13%) match the itemised breakdown within 1%; 28/39 (72%) within 10% of the headline total.** TidyTuesday sums are systematically *below* Wikipedia: its 8-category schema dropped line items that did not fit (card games, theme parks, pachinko, etc.). James Bond is the worst case ($13.9B vs $19.9B). |

## Rules applied
- R1 Strip `[xx]` citation residue and collapse whitespace in franchise/creators/owners.
- R2 Harmonise original media synonyms (Cartoon/Cartoon character → Animated cartoon; Anime → Animated series; Book/Novel → Novel/Book). Raw column kept.
- R3 Flag (not drop) the 15 placeholder rows; sensitivity run excludes them (no headline share moves ≥0.1 pt).
- R4 Add `owner_parent_2026` (Fox→Disney, AT&T/WarnerMedia→Warner Bros. Discovery, Activision Blizzard/King→Microsoft, Viacom/CBS→Paramount Skydance); earliest-matching token in the owner string wins.
- R5 Add `region_origin` (existing REGION table + owner-keyword inference).
- R6 **Update to Oct 2026:** build a new ledger from the current Wikipedia list (rev 1379832186, 2026-10-12T04:29Z) — 140 franchises, itemised breakdown parsed into long format and mapped to the original 8 categories plus two new ones: `Live & Other` (stage, museums, tours) and `Mixed (unsplit)`.
- R7 If itemised lines exceed the stated total by >5%, scale lines to the total (0 cases this revision).
- R8 Where itemised lines sum below the stated total, the remainder is kept as `Unallocated` (8 franchises >5% unallocated; e.g. Transformers $25B total vs $10.1B itemised).
- R9 Hand-code origin for 23 new-only franchises the inference could not resolve (list in script).
- R10 Clean owner strings of trailing table markup (Farm Heroes Saga row).

## Flow (2026 ledger)
| Step | Count |
|---|---|
| Rows parsed from Wikipedia | 140 |
| Dropped: no parseable total / duplicate name | 0 / 0 |
| Clean franchises | 140 |
| …matched to a 2019 franchise (hand crosswalk) | 82 |
| …new since 2019 | 58 |
| …below the article's $4B floor | 53 |
| 2019 franchises with no 2026 row (kept only in 2019 vintage) | 21 |

## Additions
- `franchise_entities_2026-10.csv`, `franchise_revenue_long_2026-10.csv` — current ledger (why: 2019 file is seven years stale; 58 franchises added).
- `worldwide_top10_box_office_2025_2026.csv` — 2025 (final) and 2026 (as of Oct 12, several titles still in release) worldwide top-10 with franchise tag (why: article's box-office trend ends in 2024).
- `fred_CPIAUCSL` CPI-U (why: real-dollar conversion; factor FY2024→Aug 2026 stored in audit_summary.json).
- Bootstrap CIs, sensitivity tables, verification sample, old-vs-new table.

## Not added / dropped (and why)
- Streaming revenue/viewing: no free, franchise-level, comparable source (Netflix engagement reports are hours, not dollars; other platforms do not publish). Documented as a limitation rather than imputed.
- Disney FY2025 segment revenue: not refreshed in this pass (needs 10-K exhibit pull); FY2024 figures still valid as labelled.
- Inflation-adjusting lifetime totals: dropped as a goal — totals are nominal sums across decades with no year split, so any deflator would be invented. CPI is applied only to dated figures.
- No rows deleted from the 2019 file.
