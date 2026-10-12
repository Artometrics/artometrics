# Franchise report — source cards (phase 1)

One card per primary source. IDs match `data/sources.csv`.

## S001 — TidyTuesday Media Franchise Revenues (2019-07-02)

- **Claim:** Committed ledger of 103 franchises with eight revenue streams (Wikipedia mid-2019 estimates).
- **Quote:** Dataset README: “Media franchise revenues from Wikipedia.”
- **Locator:** `articles/franchise/data/franchise.csv`; upstream https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-07-02
- **Reliability:** Community mirror of Wikipedia editorial estimates — not audited financials. Strong for relative composition; weak for precision.

## S017 — Wikipedia highest-grossing franchises (2026-10-11 scrape)

- **Claim:** Current list totals (e.g. Pokémon $130.7B) for 2019→2026 delta analysis.
- **Quote:** Table row: “Pokémon … $130.7 billion” (accessed 2026-10-11).
- **Locator:** `data/wikipedia_franchise_revenue_2026.csv`; https://en.wikipedia.org/wiki/List_of_highest-grossing_media_franchises
- **Reliability:** Same Wikipedia methodology issues as S001; footnotes and efn blocks changed materially since 2019.

## S040 — Derek Johnson, *Media Franchising* (2013)

- **Claim:** Franchise production is collaborative licensing across culture industries — not a single “IP owner” story.
- **Quote:** “Franchises are best understood as collaborative production formations.” (paraphrase for card; verify page in print)
- **Locator:** DOI https://doi.org/10.18574/9780814743492
- **Reliability:** Peer-reviewed monograph; framing source.

## S041 — Anita Elberse, *Blockbusters* (2013)

- **Claim:** Hit-driven industries concentrate investment behind a few megabrands.
- **Quote:** Use chapter on blockbuster strategy vs long tail (verify print edition).
- **Locator:** DOI https://doi.org/10.1007/978-1-250-03039-9
- **Reliability:** Trade book; widely cited in entertainment strategy.

## S042 — Arthur De Vany, *Hollywood Economics* (2004)

- **Claim:** Extreme uncertainty in theatrical returns; ancillary markets stabilize some bets.
- **Locator:** DOI https://doi.org/10.4324/9780203400307
- **Reliability:** Academic; supports “film is risky, licensing less so” thesis.

## S009–S012 — Disney SEC deal filings

- **Claim:** Pixar $7.4B (2006); Marvel $4.0B (2009); Lucasfilm $4.05B (2012); Fox ~$71.3B enterprise value (2019 proxy).
- **Quote:** Transaction consideration tables in respective 8-K / DEFM14A filings.
- **Locator:** `data/disney_acquisitions.csv`, `data/entities_companies_deals.csv`
- **Reliability:** Primary for deal prices; franchise “value gained” still uses S001 row anchors.

## S004 — Disney FY2024 10-K segments

- **Claim:** Reportable segment revenue (Entertainment, Sports, Experiences) for fiscal 2024.
- **Locator:** `data/disney_segment_revenue_fy2024.csv`
- **Reliability:** Audited filing — re-check line items against PDF before on-screen use.

## S019 — The Numbers (per-film financial pages)

- **Claim:** Production budget and worldwide box office for flagship franchise installments.
- **Locator:** `data/entities_budgets_grosses.csv` (each row includes `source_url`)
- **Reliability:** Industry aggregator; blank cells left where scrape failed — do not impute.

## S005 / S007 — Box Office Mojo yearly charts + franchise coding

- **Claim:** Share of domestic top-10 gross from franchise installments by year.
- **Locator:** `data/top10_franchise_share_by_year.csv`, `data/box_office_mojo_yearly_urls.csv`
- **Reliability:** Manual Artometrics coding on public charts — reproducible but subjective on “franchise installment.”

## S043 — Licensing International Global Licensing Industry Study

- **Claim:** Global licensed retail scale (industry headline).
- **Locator:** https://licensinginternational.org/news/global-licensing-industry-study-2024/
- **Reliability:** Trade association report; use for macro licensing context only.

## S055–S057 — Comcast / Hasbro / Amazon deals

- **Claim:** DreamWorks Animation $3.8B (2016); eOne ~$4B (2019); MGM $8.45B (2022).
- **Locator:** `data/entities_companies_deals.csv`
- **Reliability:** Press / 8-K; lifetime franchise revenue gained left blank where not tied to S001.
