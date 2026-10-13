# Data dictionary — articles/franchise/data/clean/
- **franchise_2019_clean.csv**: raw columns + `original_media_std`, `placeholder_flag` (revenue < $0.0105B), `owner_parent_2026`, `region_origin`. Revenue in USD billions, nominal.
- **franchise_entities_2026-10.csv**: one row per franchise. `total_usd_b` (Wikipedia headline), `breakdown_sum_usd_b`, `unallocated_usd_b`, `breakdown_exceeds_total`, `original_media`, `owners_raw`, `owner_parent_2026`, `region_origin`, `franchise_2019_name` (blank if new), `in_2019_ledger`.
- **franchise_revenue_long_2026-10.csv**: `franchise`, `category_raw` (Wikipedia label), `category` (standardised; adds Live & Other, Mixed (unsplit), Unallocated), `revenue_usd_b`.
- **worldwide_top10_box_office_2025_2026.csv**: `release_year`, `rank`, `title`, `distributor`, `worldwide_gross_usd`, `franchise_tag`, `is_franchise_film`, `gross_as_of`.
- **category_shares_bootstrap.csv**, **owner_concentration_bootstrap.csv**, **sensitivity_category_shares.csv**, **region_summary_2026-10.csv**, **verification_sample_2019.csv**, **old_vs_new.csv**, **audit_summary.json** (profile, verification rates, flow, CPI factor).
