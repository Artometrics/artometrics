---
title: "FRANCHISE: Merchandise Owns the Ledger"
slug: franchise
author: kyle-mcauliffe
pubDate: 2026-04-08T00:00:00.000Z
description: >-
  Pokémon leads 103 Wikipedia-scraped franchises at $91B lifetime (mid-2019). Merchandise is 56% of row-sum revenue. Consolidated Disney totals $426B in the same file.
heroImage: /images/content/articles/franchise/hero.png
draft: false
tags:
  - arts
  - film
subject: Franchises
tldr: >-
  The TidyTuesday 2019-07-02 media-franchise file lists 103 properties with Wikipedia lifetime revenue estimates (mid-2019). Pokémon ranks first at $90.9B. Merchandise, licensing, and retail account for 56% of row-sum revenue; box office is 9%. Consolidating Disney subsidiaries raises attributed franchise lifetime value to $426.2B versus $49.0B for Nintendo on its own owner label. Domestic top-10 films are increasingly franchise installments — 9 of 10 in 2024 on Box Office Mojo yearly charts (manual coding).
keyPoints:
  - "$90.9B — Pokémon lifetime revenue (largest single property row in the file)"
  - "56% — Share of row-sum revenue from merchandise, licensing & retail (recomputed from franchise.csv)"
  - "103 — Franchise rows in the committed TidyTuesday extract (seven sit below a $4B editorial floor)"
  - "~$4B/yr — Pokémon lifetime revenue ÷ years since 1996 (normalization as of 2019)"
  - "$426.2B — Disney owner total when Marvel, Lucasfilm, and Fox consolidate"
  - "90% — Share of 2024 domestic top-10 films coded as franchise installments"
faq:
  - question: Which franchise has the highest lifetime revenue in the dataset?
    answer: >-
      Pokémon at $90.9B in the mid-2019 Wikipedia scrape (TidyTuesday 2019-07-02). Star Wars is $63.0B; the Marvel Cinematic Universe row is $31.0B.
  - question: What revenue stream dominates the franchise ledger?
    answer: >-
      Merchandise, licensing, and retail are 56% of row-sum revenue when recomputed from franchise.csv (61% appeared in earlier published copy with a different franchise count).
  - question: How large is Disney after consolidating acquisitions?
    answer: >-
      $426.2B in summed franchise rows when Marvel Entertainment, Lucasfilm, and 20th Century Fox roll into Disney — versus $49.0B for Nintendo on its standalone owner label.
  - question: Where do the theatrical numbers come from?
    answer: >-
      Franchise-installment shares use Box Office Mojo domestic yearly charts with manual coding (see data/top10_franchise_share_by_year.csv).
---
<div id="quarto-content">
<nav id="TOC" role="doc-toc">
<h2 id="toc-title" class="anchored">IN THIS REPORT</h2>
<ul>
<li><a href="#executive-summary">Executive summary</a></li>
<li><a href="#research-question">Research question</a></li>
<li><a href="#revenue-streams">Where the money pools</a></li>
<li><a href="#top-20-franchises-by-revenue">Top 20 by lifetime revenue</a></li>
<li><a href="#revenue-per-year-of-existence">Revenue per year of existence</a></li>
<li><a href="#disney-consolidated">Disney consolidated</a></li>
<li><a href="#where-franchises-begin">Where franchises begin</a></li>
<li><a href="#theatrical-seriality">Theatrical seriality</a></li>
<li><a href="#disney-acquisitions">Disney acquisitions</a></li>
<li><a href="#disney-segments">Disney segment revenue (10-K)</a></li>
<li><a href="#studio-comparisons">Studio &amp; library comparisons</a></li>
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
<p class="art-p"><strong>Executive summary.</strong> Franchise economics is licensing geometry, not box-office bragging rights. In the mid-2019 Wikipedia/TidyTuesday ledger (103 properties), merchandise-weighted revenue beats theatrical for most rows; Pokémon leads at $90.9B because games, cards, and retail compound — not because it outruns every multi-row universe you could stack against it. Disney’s modern playbook is consolidation: buy libraries (Pixar, Marvel, Lucasfilm, Fox), keep labels, harvest parks, merchandise, and streaming off the same characters. The domestic top ten has become a sequel bar chart — 9 of 10 franchise installments in 2024. Counterexamples (Dark Universe, DC’s false starts) prove IP ownership without slate discipline is expensive noise.</p>
</div>

<p class="art-p">A child trades a cardboard Pikachu for lunch money; Bob Iger writes a seventy-one-billion-dollar check for Fox. Both transactions assume the same premise — that characters can be mined long after the premiere weekend. The TidyTuesday file published July 2, 2019 is our x-ray: 103 media franchises scraped from Wikipedia’s “highest-grossing media franchises” list, each split across up to eight revenue streams (merchandise, box office, games, comics, and others). Figures are lifetime estimates through roughly mid-2019, not audited studio financials. They are still the cleanest public ledger for comparing <em>how</em> money attaches to IP.</p>
<p class="art-p">Henry Jenkins’s <em>Convergence Culture</em> (2006) frames the consumer side — audiences follow stories across formats. Marc Steinberg’s media-mix work on Japan shows the extreme: animation as storefront for merchandise. This report stays on the money side: which streams dominate, who owns them after M&A, and how theatrical slates turned serial.</p>

<h2 id="research-question" class="anchored">RESEARCH QUESTION</h2>
<p class="art-p">For franchises in the mid-2019 Wikipedia scrape, (1) how much lifetime value sits in merchandise versus box office, (2) how does consolidating Disney subsidiaries change the ownership map, and (3) how fast did domestic top-grossing films become franchise installments?</p>

<h2 id="revenue-streams" class="anchored">Where the money pools</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart6_revenue_streams.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart6_revenue_streams.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Horizontal bar chart of revenue stream shares across 103 franchises."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Merchandise, licensing, and retail are 56% of row-sum revenue — games 20%, box office 9% (recomputed from franchise.csv).</figcaption>
</figure>
<p class="art-p">Row-sum the committed CSV and merchandise, licensing, and retail account for $852.6B of $1.52T — 56.0%. Video games are 20.0%. Box office is 8.9%. The pattern means what CEOs already suspect: theatrical is marketing infrastructure for most properties at this scale, not the terminal cash-flow line. An earlier Artometrics headline used 61% and “107 franchises”; that reflected rounded copy and a slightly different franchise count in editorial notes. This R2 revision publishes the recomputed share and documents the gap in the methods box.</p>

<h2 id="top-20-franchises-by-revenue" class="anchored">Top 20 by lifetime revenue</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart1_top20_revenue.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart1_top20_revenue.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Stacked horizontal bars of top 20 franchises by revenue stream."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Pokémon ($90.9B) leads Hello Kitty ($80.0B) and Winnie the Pooh ($74.5B); merchandise bands dominate most stacks.</figcaption>
</figure>
<p class="art-p">Pokémon is first at $90.9B — ahead of any single named row, but not ahead of every universe you could stack. Star Wars ($63.0B) plus the Marvel Cinematic Universe row ($31.0B) already exceed Pokémon before you add Spider-Man adjunct rows or Wizarding World ($28.1B). The chart is about composition, not crowning one winner: Hello Kitty is almost entirely merchandise; Mario keeps a thick games slice because Nintendo historically resists licensing Mario into every aisle; Star Wars shows a more balanced theatrical-plus-merchandise mix — the template Disney paid $4.05B to buy in 2012.</p>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Pokémon — game-first flywheel</p>
<p class="art-p">Created 1996 (Game Freak / Nintendo). The anime advertises the card game; the card game advertises the video games. Merchandise rows in the file are enormous because the property was designed as collectible SKUs, not as a single film cycle (Steinberg, 2012 — media-mix logic applied by analogy).</p>
</div>
<aside>
<div class="art-logo"><img src="/images/content/articles/franchise/assets/logo_nintendo.svg" alt="Nintendo" /><p class="art-logo__credit">Nintendo logo via Wikimedia Commons (PD-textlogo; trademark of Nintendo)</p></div>
</aside>
</div>

<h2 id="revenue-per-year-of-existence" class="anchored">Revenue per year of existence</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart2_revenue_per_year.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart2_revenue_per_year.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Top franchises by lifetime revenue divided by years since creation."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Pokémon clears about $4B per calendar year of existence; legacy mascots look slower when age is the denominator.</figcaption>
</figure>
<p class="art-p">Lifetime totals reward age. Dividing by years alive as of 2019 (lifetime ÷ (2019 − year_created), minimum one year) rewards ecosystems that monetize monthly — cards, games, retail endcaps — over properties that spike at release. Hello Kitty’s $80B still impresses, but forty-five years of denominator pulls its per-year rate below Pokémon’s.</p>

<h2 id="disney-consolidated" class="anchored">Disney consolidated</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart3a_disney_non_consolidated.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart3a_disney_non_consolidated.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Owner totals with Disney subsidiaries listed separately."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Raw owner field lists Disney, Marvel, and Fox as separate bars — strategically misleading for benchmarking.</figcaption>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart3b_disney_consolidated.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart3b_disney_consolidated.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Owner totals with Disney subsidiaries merged."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Consolidated Disney: $426.2B in summed franchise rows — an order of magnitude above standalone Nintendo ($49.0B).</figcaption>
</figure>
<p class="art-p">Marvel Entertainment (Disney) and 20th Century Fox (Disney) are not independent competitors — they are divisions that send licensing upward. Unconsolidated, Disney shows $259B while Marvel adds $20B and Fox $17B. Consolidated, the same rows sum to $426.2B. Nintendo’s $49B on its owner label is the fair comparator for “single balance sheet,” not the Pokémon Company string that mixes trademark holders.</p>

<h2 id="where-franchises-begin" class="anchored">Where franchises begin</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart5_original_media_revenue.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart5_original_media_revenue.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Lifetime revenue summed by original media type."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Game- and novel-origin franchises punch above the “franchise = film” stereotype in lifetime totals.</figcaption>
</figure>
<p class="art-p">Original-media tags in the scrape are coarse, but the totals are clear: video-game seeds and comic/novel seeds produce billion-dollar ceilings, not only theatrical premieres. That complements the merchandise story — the extraction layer matters more than the debut format.</p>

<h2 id="theatrical-seriality" class="anchored">Theatrical seriality</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart7_top10_franchise_share.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart7_top10_franchise_share.png" data-source="Data: Box Office Mojo yearly charts — ARTOMETRICS" role="img" aria-label="Line chart of franchise installments as share of domestic top 10 films by year."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Franchise installments rose from 60% of the domestic top 10 (2010) to 90% (2024) — manual coding, see CSV for sources.</figcaption>
</figure>
<p class="art-p">Box Office Mojo publishes domestic calendar-gross rankings by year. We code an entry as a franchise installment when it is a sequel, prequel, spin-off, or shared-universe episode of existing IP (method in <code>data/top10_franchise_share_by_year.csv</code>; URLs in <code>box_office_mojo_yearly_urls.csv</code>). Eight of ten in 2019 matches year-end press coverage; nine of ten in 2024 matches the year chart dominated by <em>Inside Out 2</em>, <em>Deadpool &amp; Wolverine</em>, <em>Moana 2</em>, and similar rows. This is risk management dressed as culture — recognition lowers marketing cost.</p>

<h2 id="disney-acquisitions" class="anchored">Disney acquisitions — price vs ledger anchor</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart8_disney_acquisitions.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart8_disney_acquisitions.png" data-source="Data: SEC deal prices + TidyTuesday franchise rows — ARTOMETRICS" role="img" aria-label="Scatter of acquisition price versus anchor franchise lifetime revenue."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Deal checks (SEC) vs mid-2019 franchise-row anchors — different units, same strategic question.</figcaption>
</figure>
<p class="art-p">Pixar (2006, $7.4B), Marvel (2009, $4.0B), Lucasfilm (2012, $4.05B), and 21st Century Fox (2019, ~$71.3B) are capitalization events. Compare price to a single flagship row in the Wikipedia ledger — Star Wars at $63B, MCU at $31B — and you see why conglomerates buy libraries. Fox is infrastructure: the Simpsons row is $13.5B in the file, but the deal bought cable, Hulu stake, and decades of catalog.</p>

<h2 id="disney-segments" class="anchored">Disney segment revenue — audited FY2024</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart9_disney_segments_fy2024.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart9_disney_segments_fy2024.png" data-source="Data: Disney Form 10-K FY2024 — ARTOMETRICS" role="img" aria-label="Bar chart of Disney FY2024 revenue by segment."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Experiences (parks &amp; products) $34.2B rivals Entertainment $42.2B — characters monetize off-screen.</figcaption>
</figure>
<p class="art-p">Wikipedia franchise rows are illustrative lifetime totals; Disney’s 10-K is audited annual revenue. Experiences — parks, resorts, merchandise — reported $34.154B in FY2024; Entertainment $42.233B; Sports (ESPN) $17.974B (Form 10-K, fiscal year ended September 28, 2024). Parks are not a side business; they are the physical licensing engine for the same IP box office promotes.</p>

<h2 id="studio-comparisons" class="anchored">Studio &amp; library comparisons</h2>
<p class="art-p"><strong>Warner / DC.</strong> DC Entertainment rows sum to ~$44.4B in the file (Batman, Harry Potter/Wizarding World, etc.) but theatrical execution lagged Marvel for a decade — a reminder that tables do not operate slates.</p>
<p class="art-p"><strong>Universal / Sony.</strong> Fast &amp; Furious, Jurassic, and Spider-Man adjunct rows show blockbuster economics without Disney-scale consolidation — high upside, fragmented libraries.</p>
<p class="art-p"><strong>Nintendo / Pokémon.</strong> Nintendo keeps hardware and mascot IP tightly coupled; Pokémon demonstrates game-first franchise design beating many film-first properties on per-year efficiency.</p>
<p class="art-p"><strong>Toho / Japan.</strong> Godzilla rows are smaller in the English Wikipedia table but show how national icons can be underrepresented when a $4B inclusion floor filters the world.</p>

<h2 id="failure-modes" class="anchored">When franchises break</h2>
<p class="art-p">Ownership without discipline fails. Universal shelved the Dark Universe after <em>The Mummy</em> (2017). Warner’s Wizarding World sequels fell far from <em>Harry Potter</em> peaks. DC’s extended universe spent years in turnaround before the 2023 DC Studios reset. <em>Ghostbusters</em> (2016) showed reboot backlash; mobile-native <em>Angry Birds</em> shows revenue can peak and fade while rows remain in the table. See <code>data/franchise_failures.csv</code> for case links.</p>

<div class="art-callout" id="method-box">
<p class="art-p"><strong>Data &amp; method box.</strong> Primary ledger: TidyTuesday <code>media_franchises.csv</code> (2019-07-02), SHA-256 verified in <code>npm run brief:franchise</code>. 103 unique franchises; seven sum below $4B — the Wikipedia list’s editorial floor is not strictly enforced in every row. Revenue categories are Wikipedia estimates (mid-2019). Disney consolidation rules in <code>data/owner_consolidation_rules.csv</code>. Theatrical share charts use Box Office Mojo yearly pages with manual franchise coding. Disney segment chart uses FY2024 Form 10-K totals. Do not treat franchise rows as studio P&amp;L.</p>
</div>

<h2 id="decision-tools" class="anchored">Decision tools for executives</h2>
<ul>
<li><strong>Ownership lens.</strong> Consolidate subsidiaries before benchmarking Disney vs Nintendo — otherwise you compare an incomplete parent to a consolidated rival.</li>
<li><strong>Margin lens.</strong> Map cash to streams (merchandise, games, parks, subscription). Box office rank alone mis-ranks Hello Kitty against Pokémon.</li>
<li><strong>Capital lens.</strong> Acquisition price is the NPV of licensing you believe remains — compare SEC deal size to franchise-row scale, then to parks and retail capacity, not opening weekend.</li>
</ul>

<h2 id="limitations" class="anchored">LIMITATIONS</h2>
<p class="art-p">Wikipedia estimates vary by editor and year; the scrape stops in 2019. Owner fields predate some corporate renames. Merchandise buckets are broad. Box-office franchise coding is manual — edge cases exist. Disney 10-K segments are corporate totals, not per-IP profit. Cross-border franchises (anime, tokusatsu) are under-counted at the $4B floor.</p>

<h2 id="conclusion" class="anchored">CONCLUSION</h2>
<p class="art-p">Franchise economics rewards objects you can sell repeatedly — cards, plush, park tickets — more than minutes in a theater. Pokémon leads the mid-2019 ledger because it built that machine early. Disney leads consolidated ownership because it bought libraries and wired them to parks and streaming. The domestic top ten became a sequel chart. The actionable read: measure streams, consolidate owners, and price acquisitions as licensing NPV — or end up with icons you cannot operate.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">Rebuild charts and derived CSVs: <code>npm run brief:franchise</code> from the repository root (R script <code>articles/franchise/scripts/build_brief.R</code>, then <code>scripts/sync-article.mjs</code>). Bibliography: <code>articles/franchise/references.bib</code>. Image credits: <code>articles/franchise/CREDITS</code>. Video scripts and storyboards: <code>articles/franchise/video/</code>.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<ul>
<li>TidyTuesday (2019-07-02). <em>Media Franchise Revenues</em>. <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-07-02" rel="noopener noreferrer">github.com/rfordatascience/tidytuesday/…/2019-07-02</a></li>
<li>Wikipedia. <em>List of highest-grossing media franchises</em> (underlying estimates for the scrape).</li>
<li>Robinson, D. (2019). <em>Analyzing Franchise Revenue — TidyTuesday Screencast</em>. <a href="https://youtu.be/1xsbTs9-a50" rel="noopener noreferrer">youtu.be/1xsbTs9-a50</a></li>
<li>Jenkins, H. (2006). <em>Convergence Culture</em>. NYU Press.</li>
<li>Steinberg, M. (2012). <em>Anime's Media Mix</em>. University of Minnesota Press.</li>
<li>The Walt Disney Company. Form 10-K, fiscal year ended September 28, 2024 (segment revenue).</li>
<li>Box Office Mojo yearly domestic charts (2010–2024) — see <code>data/box_office_mojo_yearly_urls.csv</code>.</li>
</ul>
</section>

<h2 id="editors-note" class="anchored">EDITOR'S NOTE</h2>
<div class="art-editorial-note"><p class="art-p"><em>This R2 revision recomputes headline percentages from the committed franchise.csv, adds Box Office Mojo and Disney 10-K charts, and ships video scripts with storyboards. Human editorial direction; AI-assisted analysis and chart code per Artometrics workflow.</em></p><p class="art-p">— Artometrics Editorial Desk</p></div>

<p class="art-github-wrap">
<a class="art-github-btn" href="https://github.com/Artometrics/artometrics-web/tree/main/articles/franchise" target="_blank" rel="noopener noreferrer">Article monorepo folder</a>
</p>
</main>
</div>
