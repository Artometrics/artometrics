---
title: "FRANCHISE: Merchandise Owns the Ledger"
slug: franchise
author: kyle-mcauliffe
pubDate: 2026-04-08T00:00:00.000Z
description: >-
  One hundred three Wikipedia-scraped franchises (mid-2019) sum to $1.52T lifetime revenue. Merchandise is 56% of row totals; Pokémon leads at $90.9B. Consolidated Disney franchise rows reach $426.2B. By region_origin (chart 15): Japan 42 franchises ($681.5B), US 52 ($770.0B), Korea 2 ($20.0B).
heroImage: /images/content/articles/franchise/hero.png
draft: false
tags:
  - arts
  - film
subject: Franchises
tldr: >-
  The TidyTuesday 2019-07-02 media-franchise file lists 103 properties with Wikipedia lifetime revenue estimates (mid-2019), verified against franchise.csv (S001). Row-sum revenue is $1,522.2B; merchandise, licensing, and retail are 56.0%; box office is 8.9%. Pokémon ranks first at $90.9B lifetime. Consolidating Disney subsidiaries raises attributed franchise lifetime value to $426.2B versus $49.0B for Nintendo on its standalone owner label. Eighty-two franchises pair to 2026 Wikipedia rows (S017); domestic top-10 films were 90% franchise installments in 2024 (Box Office Mojo, manual coding).
keyPoints:
  - "$1,522.2B — row-sum lifetime revenue, 103 franchises (franchise.csv, S001)"
  - "56.0% — merchandise, licensing & retail share of row-sum revenue"
  - "$90.9B — Pokémon lifetime revenue (largest single named property row)"
  - "$426.2B — Disney owner total when Marvel, Lucasfilm, and Fox consolidate"
  - "82 — 2019 franchises with paired 2026 Wikipedia revenue (crosswalk, S017)"
  - "90% — share of 2024 domestic top-10 films coded as franchise installments"
faq:
  - question: Which franchise has the highest lifetime revenue in the dataset?
    answer: >-
      Pokémon at $90.9B in the mid-2019 Wikipedia scrape (TidyTuesday 2019-07-02, S001). Hello Kitty is $80.0B; Winnie the Pooh is $74.5B. Star Wars is $63.0B; the Marvel Cinematic Universe row is $31.0B.
  - question: What revenue stream dominates the franchise ledger?
    answer: >-
      Merchandise, licensing, and retail are 56.0% of row-sum revenue when recomputed from franchise.csv (S001). Video games are 20.0%; box office is 8.9%.
  - question: How large is Disney after consolidating acquisitions?
    answer: >-
      $426.2B in summed franchise rows when Marvel Entertainment, Lucasfilm, and 20th Century Fox roll into The Walt Disney Company — versus $49.0B for Nintendo on its standalone owner label (owner_consolidation_rules.csv, S001).
  - question: Did Wikipedia franchise estimates change after 2019?
    answer: >-
      Yes for many rows. We hand-mapped 103 TidyTuesday franchises to 2026 Wikipedia titles; 82 pairs have revenue in both years (franchise_crosswalk_2019_2026.csv, S017). Chart 10 shows the largest paired deltas. Hello Kitty ($80.0B→$33.5B), Mario ($35.0B→$9.74B), and Gundam ($25.5B→$5.0B) are flagged wiki_source_revision rows — Wikipedia revised sources, not proof of real declines.
  - question: Where do the theatrical numbers come from?
    answer: >-
      Franchise-installment shares use Box Office Mojo domestic yearly charts with manual coding (top10_franchise_share_by_year.csv). 2024: nine of ten top domestic films coded as franchise installments (90%).
  - question: How does Japan compare with the United States in this file?
    answer: >-
      By region_origin tags (entities_franchises.csv), Japan-origin franchises sum to $681.5B (49.1% merchandise share); US-origin sum to $770.0B (64.3%); Korea (CrossFire, Dungeon Fighter Online) sums to $20.0B; China (Westward Journey) $6.0B (chart 15, S001).
---
<div id="quarto-content">
<nav id="TOC" role="doc-toc">
<h2 id="toc-title" class="anchored">IN THIS REPORT</h2>
<ul>
<li><a href="#executive-summary">Executive summary</a></li>
<li><a href="#research-question">Research question</a></li>
<li><a href="#one-ledger">One ledger, two playgrounds</a></li>
<li><a href="#merchandise-pools">Merchandise pools — Japan’s media-mix vs Hollywood’s vertical stack</a></li>
<li><a href="#top-twenty">Who tops the table — and who is not crowned</a></li>
<li><a href="#wiki-drift">Wikipedia moved (2019 vs 2026)</a></li>
<li><a href="#region-origin">Japan, the United States, Korea, and China</a></li>
<li><a href="#original-medium">Original medium sets the extraction layer</a></li>
<li><a href="#box-office-slice">Box office is a thin slice for most of the top twenty</a></li>
<li><a href="#revenue-per-year">Revenue per year of existence</a></li>
<li><a href="#disney-consolidated">Disney consolidated — ownership literacy</a></li>
<li><a href="#owner-concentration">Owner concentration after Fox</a></li>
<li><a href="#disney-acquisitions">Disney acquisitions — check size vs row anchor</a></li>
<li><a href="#disney-segments">Disney segment revenue (10-K)</a></li>
<li><a href="#theatrical-seriality">Theatrical seriality</a></li>
<li><a href="#fragmented-libraries">Sony, Universal, Nintendo — fragmented vs married IP</a></li>
<li><a href="#failure-modes">When franchises break</a></li>
<li><a href="#decision-tools">Decision tools for executives</a></li>
<li><a href="#limitations">Limitations</a></li>
<li><a href="#conclusion">Conclusion</a></li>
<li><a href="#data-methods-and-sources">Data, methods &amp; sources</a></li>
<li><a href="#editors-note">Editor's note</a></li>
</ul>
</nav>
<main class="art-article-main">

<div class="art-callout" id="executive-summary">
<p class="art-p"><strong>Executive summary.</strong> Franchise economics is licensing geometry: who owns repeatable rights, and which revenue streams compound after the premiere. In the mid-2019 Wikipedia/TidyTuesday ledger (103 properties, $1,522.2B row-sum lifetime revenue, S001), merchandise-weighted rows beat theatrical for most names; box office is 8.9% of the file. Pokémon leads at $90.9B because games, cards, and retail compound — not because it beats every stacked Marvel and Star Wars row you could add. Japan’s media-mix and production-committee history explain why animation often functions as a storefront for objects; Hollywood’s answer is studio-owned IP wired to parks and retail — The Walt Disney Company’s consolidated franchise rows sum to $426.2B while FY2024 Experiences segment revenue alone is $34.2B (10-K, S081). The domestic top ten has become a sequel chart (90% franchise installments in 2024). Counterexamples — Universal’s Dark Universe, DC slate churn, mobile peaks like Angry Birds — prove ownership without operating discipline is expensive noise.</p>
</div>

<h2 id="one-ledger" class="anchored">ONE LEDGER, TWO PLAYGROUNDS</h2>
<p class="art-p">A child trades a cardboard Pikachu for lunch money; Bob Iger signs a seventy-one-point-three-billion-dollar check for Twenty-First Century Fox. Both trades assume the same premise — that characters can be mined long after opening weekend. The TidyTuesday file published July 2, 2019 is our x-ray: 103 media franchises scraped from Wikipedia’s “highest-grossing media franchises” list, each split across up to eight revenue streams (merchandise, box office, games, comics, and others). Figures are lifetime estimates through roughly mid-2019, not audited studio financials. They are still the cleanest public ledger for comparing <em>how</em> money attaches to IP — verified against <code>franchise.csv</code> (SHA-256 logged in <code>verified_numbers.csv</code>, source S001).</p>
<p class="art-p">This report reads that ledger the way an anime R2 report reads MyAnimeList: as the footprint of a production system, not a popularity contest. Henry Jenkins’s <em>Convergence Culture</em> (2006) frames the audience side — stories that jump formats because fans follow characters. Marc Steinberg’s media-mix work on Japan shows the extreme case: sponsored television animation as billboard for merchandise (Steinberg, 2012). American conglomerates built a parallel stack — own the character, own the park turnstile, own the streaming shelf. Below, each pattern states what it means for a buyer, how we know it (source and method), what mechanism explains it, and a cross-market comparison or counterexample.</p>

<h2 id="research-question" class="anchored">RESEARCH QUESTION</h2>
<p class="art-p">For franchises in the mid-2019 Wikipedia scrape, (1) how much lifetime value sits in merchandise versus box office and games, (2) how do Japan-origin and US-origin properties differ in that mix, (3) how did paired Wikipedia estimates move by 2026, (4) how does consolidating Disney subsidiaries change the ownership map, and (5) how fast did domestic top-grossing films become franchise installments?</p>

<h2 id="merchandise-pools" class="anchored">MERCHANDISE POOLS — JAPAN’S MEDIA-MIX VS HOLLYWOOD’S VERTICAL STACK</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart6_revenue_streams.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart6_revenue_streams.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Horizontal bar chart of revenue stream shares across 103 franchises."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Merchandise, licensing, and retail are 56.0% of row-sum revenue — games 20.0%, box office 8.9% (franchise.csv, S001).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> At franchise scale, theatrical is usually marketing infrastructure; repeatable SKUs and licensing desks carry the ledger.</p>
<p class="art-p"><strong>How we know.</strong> Sum every revenue row in the committed CSV: $1,522.2B total; merchandise, licensing, and retail $852.6B (56.0%); video games 20.0%; box office 8.9% — recomputed in <code>verified_numbers.csv</code> (S001). Method: category sums ÷ total revenue.</p>
<p class="art-p"><strong>Mechanism.</strong> Japan’s production committees split copyright among publishers, broadcasters, and toy makers, which hard-wires plush, magazines, and cards into budgets (Hernández Hernández, 2018, on committees; Steinberg, 2012, on media-mix). Hollywood historically licensed characters outward, but vertically integrated studios — especially Disney — internalised parks, cruise, and retail as Experiences segment revenue (FY2024 audited total $34.151B, S081).</p>
<p class="art-p"><strong>Counterexample.</strong> Video-game-origin franchises sum to $334.9B lifetime by original medium — larger than film-origin totals ($111.7B). Mario still shows a thick games slice in the 2019 file. Nintendo licenses the character selectively — the 2023 film, Super Nintendo World, LEGO Mario — and keeps creative control.</p>

<h2 id="top-twenty" class="anchored">WHO TOPS THE TABLE — AND WHO IS NOT CROWNED</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart1_top20_revenue.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart1_top20_revenue.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Stacked horizontal bars of top 20 franchises by revenue stream."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Pokémon ($90.9B) leads Hello Kitty ($80.0B) and Winnie the Pooh ($74.5B); merchandise bands dominate most stacks.</figcaption>
</figure>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Pokémon — game-first flywheel</p>
<p class="art-p"><strong>What it means.</strong> Pokémon is the largest single named property row — a template for game-first franchise design.</p>
<p class="art-p"><strong>How we know.</strong> $90.863B lifetime in the file ($90.9B on screen); Hello Kitty $80.026B; Winnie the Pooh $74.519B (S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Created 1996 (Game Freak / Nintendo). Anime promotes cards; cards promote video games — collectible SKUs with a cartoon as advertising.</p>
<p class="art-p"><strong>Counterexample.</strong> Star Wars ($63.0B) plus the Marvel Cinematic Universe row ($31.0B) already exceed Pokémon before Spider-Man adjunct rows or Wizarding World ($28.1B). The chart teaches composition, not a single winner.</p>
</div>
<aside>
<div class="art-logo"><img src="/images/content/articles/franchise/assets/logo_nintendo.svg" alt="Nintendo" /><p class="art-logo__credit">Nintendo logo via Wikimedia Commons (PD-textlogo; trademark of Nintendo)</p></div>
</aside>
</div>

<h2 id="wiki-drift" class="anchored">WIKIPEDIA MOVED (2019 VS 2026)</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart10_wiki_2019_vs_2026.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart10_wiki_2019_vs_2026.png" data-source="Data: TidyTuesday 2019 + Wikipedia 2026 scrape — ARTOMETRICS" role="img" aria-label="Largest revenue deltas between 2019 and 2026 Wikipedia pairs."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Eighty-two franchises with revenue in both years. Gray bars flag Wikipedia source revisions — e.g. Hello Kitty $80.0B→$33.5B, Mario $35.0B→$9.74B, Gundam $25.5B→$5.0B — not real franchise declines (S001; S017).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Public franchise tables are editor-maintained surveys — they drift when categories like mobile games or live-service revenue enter the infobox.</p>
<p class="art-p"><strong>How we know.</strong> 103 hand-mapped crosswalk rows; 82 with non-empty 2026 pairs and both-year revenue for chart 10 (<code>franchise_crosswalk_2019_2026.csv</code>, <code>franchise_revenue_2019_vs_2026.csv</code>; S001, S017). A 2026 index parse lists 140 Wikipedia franchise rows (S017).</p>
<p class="art-p"><strong>Mechanism.</strong> English Wikipedia aggregates press estimates; editors add streams the 2019 scrape under-weighted. The largest dollar increases among paired rows are Pokémon (+$39.8B, from $90.9B in 2019 to $130.7B in 2026), then Call of Duty and Naruto (about +$14B each). Mortal Kombat rises only about $3.9B, from $1.17B to $5.06B, and it is a fighting-game franchise, not a mobile title.</p>
<p class="art-p"><strong>Counterexample.</strong> Hello Kitty, Mario, and Gundam show large negative percent changes in the paired file because English Wikipedia revised its sourcing between scrapes — not because Sanrio or Nintendo reported collapsing revenue. Chart 10 colors those rows gray. Other drops may reflect renames, splits, or scope changes (e.g., The Simpsons after Fox consolidation). Quote growth only when the crosswalk documents a pair and the match note flags a true like-for-like total.</p>

<h2 id="region-origin" class="anchored">JAPAN, THE UNITED STATES, KOREA, AND CHINA</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart15_region_japan_us_other.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart15_region_japan_us_other.png" data-source="Data: entities_franchises.csv — ARTOMETRICS" role="img" aria-label="Lifetime revenue and merchandise share by region of origin."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Japan: 42 franchises, $681.5B (49.1% merch). US: 52, $770.0B (64.3%). Korea: 2, $20.0B. China: 1, $6.0B. Other: 6, $44.8B (S001).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> The ledger is Anglo-table biased but still shows two different optimisation paths — Japanese media-mix density versus US theatrical-and-parks scale.</p>
<p class="art-p"><strong>How we know.</strong> Hand-audited <code>region_origin</code> tags in <code>entities_franchises.csv</code> (Japan: Evangelion, Sonic, Monster Strike, Puzzle &amp; Dragons, Fate, Gran Turismo; Korea: CrossFire, Dungeon Fighter Online; China: Westward Journey; US: Peanuts, TMNT), summed in <code>franchise_region_summary.csv</code> (S001).</p>
<p class="art-p"><strong>Mechanism.</strong> US studios built global theatrical pipelines and theme-park engines; Japanese franchises optimised for domestic retail and long-tail collectibles (Steinberg, 2012; AJA industry reports for macro anime market context — whole-industry, not per-row).</p>
<p class="art-p"><strong>Counterexample.</strong> There is no four-billion-dollar inclusion floor. Mortal Kombat sits in the 2019 file at $1.17B. National icons can still be missing from the English table, but that is an editorial gap, not a cutoff we can quote.</p>

<h2 id="original-medium" class="anchored">ORIGINAL MEDIUM SETS THE EXTRACTION LAYER</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart11_mix_by_original_medium.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart11_mix_by_original_medium.png" data-source="Data: franchise.csv — ARTOMETRICS" role="img" aria-label="Revenue stream mix by original media type."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Game- and manga-origin properties carry different stream mixes than film-first seeds (revenue_mix_by_original_medium.csv).</figcaption>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart5_original_media_revenue.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart5_original_media_revenue.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Lifetime revenue summed by original media type."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Video-game seeds lead lifetime totals ($334.9B), then manga ($253.8B) — not only theatrical premieres.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Debut format is less important than which streams the rights holder chooses to license.</p>
<p class="art-p"><strong>How we know.</strong> Sum lifetime revenue by <code>original_media</code> (chart 5); stream mix shares by medium (chart 11, S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Jump comics rows stack publishing, animation, and games on one bible; Disney Princess is a retail line built atop film assets (99.9% merchandise in the Disney Princess row).</p>
<p class="art-p"><strong>Counterexample.</strong> Novel-first Wizarding World — books set canon, but Warner Bros. had to build theatrical and merchandise desks to capture value; slate fatigue on <em>Fantastic Beasts</em> shows literary IP still needs discipline.</p>

<h2 id="box-office-slice" class="anchored">BOX OFFICE IS A THIN SLICE FOR MOST OF THE TOP TWENTY</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart14_box_office_share_top20.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart14_box_office_share_top20.png" data-source="Data: franchise.csv — ARTOMETRICS" role="img" aria-label="Box office share of lifetime revenue for top 20 franchises."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Marvel Cinematic Universe row is 67.7% box office; Hello Kitty and Mario near zero — same top twenty, different economics.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Ranking franchises by theatrical gross mis-ranks mascot-led properties.</p>
<p class="art-p"><strong>How we know.</strong> Box-office dollars ÷ franchise row total for each top-twenty name (chart 14, S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Film-first universes amortise development across sequels; character-first mascots skip the cinema tax.</p>
<p class="art-p"><strong>Counterexample.</strong> Star Wars keeps a thicker theatrical band (9.0% of row in entities table) while still running merchandise — the template Lucasfilm sold to Disney for $4.05B (S011).</p>

<h2 id="revenue-per-year" class="anchored">REVENUE PER YEAR OF EXISTENCE</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart2_revenue_per_year.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart2_revenue_per_year.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Top franchises by lifetime revenue divided by years since creation."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Pokémon clears about $3.95B per calendar year of existence; Hello Kitty’s $80B spans forty-five years of denominator.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Efficiency — how fast a property compounds — is a design choice, not fandom.</p>
<p class="art-p"><strong>How we know.</strong> Lifetime ÷ max(1, 2019 − <code>year_created</code>) for each franchise (chart 2, S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Monthly billing (games, cards) beats one-off theatrical cycles in the denominator.</p>
<p class="art-p"><strong>Counterexample.</strong> Legacy mascots with huge lifetime totals but long denominators look “slow” per year even when retail never stopped.</p>

<h2 id="disney-consolidated" class="anchored">DISNEY CONSOLIDATED — OWNERSHIP LITERACY</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart3a_disney_non_consolidated.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart3a_disney_non_consolidated.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Owner totals with Disney subsidiaries listed separately."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Raw owner field lists Disney ($258.9B), Lucasfilm ($63.0B), and Marvel labels separately — misleading for benchmarking.</figcaption>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart3b_disney_consolidated.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart3b_disney_consolidated.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Owner totals with Disney subsidiaries merged."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Consolidated Disney: $426.2B in summed franchise rows — Nintendo standalone owner label $49.0B.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> M&amp;A is how modern libraries are assembled; owner fields in a 2019 scrape still list pre-consolidation labels.</p>
<p class="art-p"><strong>How we know.</strong> <code>owner_consolidation_rules.csv</code> rolls Marvel Entertainment, Lucasfilm, and 20th Century Fox into The Walt Disney Company; totals in <code>owner_totals_derived.csv</code> (S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Buy the copyright stack, keep theatrical labels, harvest parks and merchandise off the same characters.</p>
<p class="art-p"><strong>Counterexample.</strong> Pokémon rows list The Pokémon Company / Nintendo strings — consolidating trademarks is a separate legal exercise from summing Wikipedia rows.</p>

<h2 id="owner-concentration" class="anchored">OWNER CONCENTRATION AFTER FOX</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart12_owner_concentration.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart12_owner_concentration.png" data-source="Data: franchise.csv — ARTOMETRICS" role="img" aria-label="Share of lifetime revenue held by top owners."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Top owner (Disney consolidated) holds 28.0% of row-sum revenue; top five owners 46.4% (owner_concentration_scenarios.csv, S001).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> A handful of consolidators sit on nearly half the public ledger — acquisition targets are scarce at scale.</p>
<p class="art-p"><strong>How we know.</strong> Cumulative owner shares under Fox-consolidated rules (chart 12, S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Capital markets reward libraries that can be wired to Experiences and streaming; smaller owners license outward.</p>
<p class="art-p"><strong>Counterexample.</strong> Sanrio (Hello Kitty) and Shueisha-linked Jump rows show billion-dollar ceilings without Disney-scale M&amp;A.</p>

<h2 id="disney-acquisitions" class="anchored">DISNEY ACQUISITIONS — CHECK SIZE VS ROW ANCHOR</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart8_disney_acquisitions.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart8_disney_acquisitions.png" data-source="Data: SEC deal prices + TidyTuesday franchise rows — ARTOMETRICS" role="img" aria-label="Scatter of acquisition price versus anchor franchise lifetime revenue."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Deal checks (SEC) vs mid-2019 franchise-row anchors — different units, same strategic question.</figcaption>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart13_deal_price_vs_revenue.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart13_deal_price_vs_revenue.png" data-source="Data: entities_companies_deals.csv — ARTOMETRICS" role="img" aria-label="M&A price vs franchise row scale."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Pixar $7.4B vs Toy Story row $19.5B; Fox $71.3B vs Simpsons anchor $13.5B — infrastructure, not one IP.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Acquisition price is capitalization of licensing you believe remains — not applause for one weekend.</p>
<p class="art-p"><strong>How we know.</strong> SEC filings S009–S012 in <code>entities_companies_deals.csv</code>; anchor franchise rows from S001.</p>
<p class="art-p"><strong>Mechanism.</strong> Pixar (2006, $7.4B), Marvel (2009, $4.0B), Lucasfilm (2012, $4.05B), 21st Century Fox (2019, ~$71.3B enterprise value per merger proxy).</p>
<p class="art-p"><strong>Counterexample.</strong> Fox’s check dwarfs The Simpsons row ($13.5B) because the deal bought cable, Hulu stake, and catalog infrastructure — compare price to parks and distribution capacity, not a single infobox.</p>

<h2 id="disney-segments" class="anchored">DISNEY SEGMENT REVENUE — AUDITED FY2024</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart9_disney_segments_fy2024.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart9_disney_segments_fy2024.png" data-source="Data: Disney Form 10-K FY2024 — ARTOMETRICS" role="img" aria-label="Bar chart of Disney FY2024 revenue by segment."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Entertainment $41.2B, Sports $17.6B, Experiences $34.2B — fiscal year ended September 28, 2024 (S081).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Wikipedia franchise rows are illustrative lifetime totals; Disney’s 10-K is audited annual revenue — Experiences is the physical licensing engine.</p>
<p class="art-p"><strong>How we know.</strong> Segment revenues table in FY2024 Q4 earnings exhibit: Entertainment $41.186B, Sports $17.619B, Experiences $34.151B (<code>disney_segment_revenue_fy2024.csv</code>, S004, S081).</p>
<p class="art-p"><strong>Mechanism.</strong> Characters promoted in Entertainment segment monetise again at parks, resorts, cruise, and merchandise.</p>
<p class="art-p"><strong>Counterexample.</strong> Sports (ESPN) is large but not character-licensing — do not attribute ESPN dollars to Mickey Mouse rows.</p>

<h2 id="theatrical-seriality" class="anchored">THEATRICAL SERIALITY</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart7_top10_franchise_share.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart7_top10_franchise_share.png" data-source="Data: Box Office Mojo yearly charts — ARTOMETRICS" role="img" aria-label="Line chart of franchise installments as share of domestic top 10 films by year."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Franchise installments: 60% of domestic top 10 (2010) → 90% (2024) — manual coding (<code>top10_franchise_share_by_year.csv</code>).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> The hit wide release is increasingly a serial product — recognition lowers marketing cost.</p>
<p class="art-p"><strong>How we know.</strong> Box Office Mojo domestic calendar-gross rankings by year; franchise installment if sequel, prequel, spin-off, or shared-universe episode (URLs in <code>box_office_mojo_yearly_urls.csv</code>). 2019: eight of ten (80%); 2024: nine of ten (90%).</p>
<p class="art-p"><strong>Mechanism.</strong> Shared universes amortise development; streaming and global day-and-date extend the theatrical window’s marketing function.</p>
<p class="art-p"><strong>Counterexample.</strong> 2024’s year chart still included one non-franchise breakout — the bar is not absolute, but the slope is.</p>

<h2 id="fragmented-libraries" class="anchored">SONY, UNIVERSAL, NINTENDO — FRAGMENTED VS MARRIED IP</h2>
<p class="art-p"><strong>Warner / DC.</strong> DC Entertainment’s $44.4B is Batman ($25.04B) plus Superman ($13.15B) plus the DC Extended Universe row ($6.20B). Wizarding World ($28.1B) is a separate Warner row, not DC. <strong>How we know:</strong> summed franchise rows in <code>franchise.csv</code> (S001). <strong>What it means:</strong> a CEO comparing “DC” to Harry Potter is mixing two libraries. <strong>Counterexample:</strong> a decade of extended-universe restarts shows that a large comic total does not run a film slate by itself.</p>
<p class="art-p"><strong>Sony / Marvel split.</strong> Spider-Man lists Marvel Entertainment (Disney) on merchandise with Sony Pictures on films. <strong>Mechanism:</strong> co-production splits enterprise value across balance sheets. <strong>Counterexample:</strong> Universal’s Fast &amp; Furious and Jurassic rows — blockbuster scale without Disney consolidation.</p>
<p class="art-p"><strong>Nintendo.</strong> The standalone Nintendo owner label is $49.0B in the 2019 file. The Pokémon row is $90.9B in that same file, and $130.7B on the 2026 Wikipedia list. Those Pokémon dollars sit on The Pokémon Company string — Nintendo, Game Freak, and Creatures share the copyright — so they are not added to Nintendo’s $49.0B label. Nintendo licenses Mario selectively (the 2023 film, Super Nintendo World, LEGO Mario) while keeping creative control; it does not refuse every outside product.</p>

<h2 id="failure-modes" class="anchored">WHEN FRANCHISES BREAK</h2>
<p class="art-p">Ownership without discipline fails. Universal shelved the Dark Universe after <em>The Mummy</em> (2017). Warner’s Wizarding World sequels fell far from <em>Harry Potter</em> peaks. DC’s extended universe spent years in turnaround before the 2023 DC Studios reset. <em>Ghostbusters</em> (2016) showed reboot backlash; mobile-native <em>Angry Birds</em> shows revenue can peak and fade while rows remain in the table. See <code>data/franchise_failures.csv</code> for case links.</p>

<div class="art-callout" id="method-box">
<p class="art-p"><strong>Data &amp; method box.</strong> Primary ledger: TidyTuesday media franchises committed as <code>franchise.csv</code> (2019-07-02). Spoken and headline figures are recomputed into <code>verified_numbers.csv</code>, including owner totals, per-year rates, box-office shares, medium and region splits, the DC sum (Batman + Superman + DCEU), deal prices, and Disney’s FY2024 segments. Pokémon’s 2019 total ($90.9B) and 2026 Wikipedia total ($130.7B) are stored as separate rows. Revenue categories are Wikipedia estimates. The 2026 index is a paired audit, not a replacement ledger. Disney consolidation follows <code>owner_consolidation_rules.csv</code>. Theatrical shares use Box Office Mojo yearly pages with manual coding. Do not treat franchise rows as studio profit. There is no $4B cutoff: Mortal Kombat is in the file at $1.17B.</p>
</div>

<h2 id="decision-tools" class="anchored">DECISION TOOLS FOR EXECUTIVES</h2>
<ul>
<li><strong>Ownership lens.</strong> Consolidate subsidiaries before benchmarking Disney vs Nintendo — otherwise you compare an incomplete parent to a consolidated rival (46.4% of revenue sits with the top five owners after Fox rules).</li>
<li><strong>Margin lens.</strong> Map cash to streams (merchandise, games, parks, subscription). Box office rank alone mis-ranks Hello Kitty against Pokémon; chart 14 is the reminder.</li>
<li><strong>Capital lens.</strong> A deal price is what you pay for the rights you still expect to sell. Set Pixar’s $7.4B, Marvel’s $4.0B, Lucasfilm’s $4.05B, and Fox’s $71.3B next to the franchise rows they anchor, then next to Experiences revenue of $34.2B in FY2024.</li>
<li><strong>Time lens.</strong> Pair S001 with S017 when quoting growth; chart 10 shows where editors revised lifetime totals.</li>
</ul>

<h2 id="limitations" class="anchored">LIMITATIONS</h2>
<p class="art-p">Wikipedia estimates vary by editor and year; the 2019 scrape stops mid-year. Owner fields predate some corporate renames. Merchandise buckets are broad. Box-office franchise coding is manual — edge cases exist. Disney 10-K segments are corporate totals, not per-IP profit. The file includes properties well below $4B (Mortal Kombat at $1.17B), so there is no inclusion floor to cite. 2026 Wikipedia rows are not merged into the 2019 row-sum totals — they are a paired audit, not a single ledger. Quote Pokémon as $90.9B only for 2019, and as $130.7B only for the 2026 list.</p>

<h2 id="conclusion" class="anchored">CONCLUSION</h2>
<p class="art-p">Franchise economics rewards objects you can sell repeatedly — cards, toys, park tickets — more than minutes in a theater. In the mid-2019 ledger Pokémon leads at $90.9B; on the 2026 Wikipedia list the same name reads $130.7B. Disney leads consolidated ownership because it bought libraries and wired them to parks. Japan’s media-mix history and America’s studio-owned characters meet on the same lesson. The domestic top ten became a sequel chart. For a buyer: name the year, name the owner string, and separate DC from Wizarding World before you compare anyone.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">Rebuild charts and derived CSVs: <code>npm run brief:franchise</code> from the repository root (<code>articles/franchise/scripts/build_brief.R</code>, then <code>scripts/sync-article.mjs</code>). Verify headline figures: <code>npm run verify:franchise</code>. Bibliography: <code>articles/franchise/references.bib</code>. Image credits: <code>articles/franchise/CREDITS</code>. Video scripts and storyboard CSVs: <code>articles/franchise/video/</code> (no audio rendered in-repo).</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<ul>
<li>TidyTuesday (2019-07-02). <em>Media Franchise Revenues</em> (S001). <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-07-02" rel="noopener noreferrer">github.com/rfordatascience/tidytuesday/…/2019-07-02</a></li>
<li>Wikipedia. <em>List of highest-grossing media franchises</em> — 2019 underlying estimates (S001); 2026 index scrape (S017).</li>
<li>Robinson, D. (2019). <em>Analyzing Franchise Revenue — TidyTuesday Screencast</em>. <a href="https://youtu.be/1xsbTs9-a50" rel="noopener noreferrer">youtu.be/1xsbTs9-a50</a></li>
<li>Jenkins, H. (2006). <em>Convergence Culture</em>. NYU Press.</li>
<li>Steinberg, M. (2012). <em>Anime's Media Mix</em>. University of Minnesota Press.</li>
<li>Hernández Hernández, Á. D. (2018). Production committees (Arts 7(3): 42). <a href="https://doi.org/10.3390/arts7030042" rel="noopener noreferrer">doi:10.3390/arts7030042</a></li>
<li>The Walt Disney Company. Form 10-K FY2024; segment revenues exhibit (S004, S081).</li>
<li>Box Office Mojo yearly domestic charts (2010–2024) — <code>data/box_office_mojo_yearly_urls.csv</code>.</li>
</ul>
</section>

<h2 id="editors-note" class="anchored">EDITOR'S NOTE</h2>
<div class="art-editorial-note"><p class="art-p"><em>This R2 revision recomputes headline percentages from the committed franchise.csv, adds 2019–2026 Wikipedia crosswalk charts, region and stream-mix views, Box Office Mojo and Disney 10-K charts, and ships three video scripts with phrase-level storyboard CSVs. Human editorial direction; AI-assisted analysis and chart code per Artometrics workflow.</em></p><p class="art-p">— Artometrics Editorial Desk</p></div>

<p class="art-github-wrap">
<a class="art-github-btn" href="https://github.com/Artometrics/artometrics-web/tree/main/articles/franchise" target="_blank" rel="noopener noreferrer">Article monorepo folder</a>
</p>
</main>
</div>
