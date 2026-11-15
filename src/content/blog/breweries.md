---
title: 'BREWERIES: U.S. Craft Beer Peaks at 12.8% ABV While the Median Stays at 6%'
slug: breweries
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Analysis of 2,410 U.S. craft beers shows median ABV of 6%, maximum 12.8%, and high bitterness concentrated in the IPA cluster.'
dek: "Most craft beers sit at 6% ABV. One is more than double that."
heroImage: /images/content/articles/breweries/hero.png
draft: false
tags:
  - culture
  - food
subject: Beer
tldr: 'U.S. craft beer''s strength distribution centers on 6% ABV across 2,410 records. Lee Hill Series Vol. 5 — Belgian Style Quadrupel Ale tops the range at 12.8%. High-ABV outliers above 10% represent a boutique tail; most beers cluster near session strength, and bitterness (IBU) rises with alcohol but not uniformly.'
keyPoints:
  - '2,410 — Records in the dataset after cleaning'
  - '6% — Median ABV, the typical breweries strength'
  - '12.8% — Maximum ABV, held by Lee Hill Series Vol. 5'
  - 37% — Share of aggregate ABV held by the top five high-strength beers
faq:
  - question: What is the median ABV of U.S. craft beer in this dataset?
    answer: The median ABV is 6% (0.06).
  - question: Which beer has the highest ABV?
    answer: 'Lee Hill Series Vol. 5 — Belgian Style Quadrupel Ale, at 12.8%.'
  - question: Do high-ABV beers always have high IBU?
    answer: 'No; stouts and quads reach high ABV with low bitterness, while IPAs pair both.'
  - question: How many beers exceed 10% ABV?
    answer: Fewer than a dozen in the top tier; the distribution is right-skewed with a thin high-gravity tail.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">The strongest U.S. craft beer in this 2,410-record extract reaches <strong>12.8% ABV</strong> (Lee Hill Series Vol. 5 — Belgian Style Quadrupel Ale), but the median sits at <strong>6%</strong>. High-gravity outliers above 10% form a boutique tail; the bulk of the catalog clusters near session-to-standard strength, with bitterness (IBU) rising alongside alcohol in hop-forward styles but diverging in malt-heavy quads and stouts.</p>
<p class="art-p">The distribution is right-skewed: hundreds of beers occupy the 5–6% bins, counts fall past 9%, and the famous 12–13% outliers are rare.</p>

<h2 id="high-abv-outliers-are-named-experiments" class="anchored">High-ABV Outliers Are Named Experiments</h2>
<h3 id="high-abv-outliers-are-named-experiments-look" class="anchored">Abv by Name</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/breweries/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/breweries/charts/chart1_breakdown.png" role="img" aria-label="Abv by Name"></div>
</figure>
<p class="art-p">Lee Hill Series Vol. 5 leads at <strong>0.128</strong> ABV, London Balling at <strong>0.125</strong>, and Csar at <strong>0.120</strong>. The next cluster — Lee Hill Vol. 4, 4Beans, Johan the Barleywine, Wizard Burial Ground, Hi-Res — sits near <strong>0.10</strong>. These titles are the marketing edge of craft, not the median pint.</p>
<h2 id="the-top-dozen-still-doubles-everyday-strength" class="anchored">The Top Dozen Still Doubles Everyday Strength</h2>
<h3 id="the-top-dozen-still-doubles-everyday-strength-look" class="anchored">Lee Hill Series Vol</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/breweries/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/breweries/charts/chart2_leaders.png" role="img" aria-label="Lee Hill Series Vol"></div>
</figure>
<p class="art-p">The leaders cap at 0.128, with the rest of the top dozen occupying the 0.10–0.12 band — roughly double the 0.06 median. Use 0.06 as the typical craft ABV in this extract and 0.10+ as the specialty high-gravity threshold.</p>
<h2 id="most-beers-pile-up-near-5-6-abv" class="anchored">Most Beers Pile Up Near 5–6% ABV</h2>
<h3 id="most-beers-pile-up-near-5-6-abv-look" class="anchored">Median 0.06 vs mean 0.06 — the shape is right-skewed</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/breweries/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/breweries/charts/chart3_distribution.png" role="img" aria-label="Median 0.06 vs mean 0.06 — the shape is right-skewed"></div>
</figure>
<p class="art-p">The tallest bins sit at <strong>0.05–0.06</strong> ABV (hundreds of beers each), with counts falling as ABV climbs toward 0.09–0.10 and almost vanishing above 0.11. Right skew is real but thin: the famous 12–13% outliers are rare relative to the pale-ale middle.</p>
<h2 id="high-abv-names-concentrate-in-a-short-list" class="anchored">High-ABV Names Concentrate in a Short List</h2>
<h3 id="high-abv-names-concentrate-in-a-short-list-look" class="anchored">The top 5 name entries account for 37% of the aggregate abv</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/breweries/charts/chart4_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/breweries/charts/chart4_pareto.png" role="img" aria-label="The top 5 name entries account for 37% of the aggregate abv"></div>
</figure>
<p class="art-p">The first five high-ABV beers hold <strong>37%</strong> of the aggregate strength share, rising toward the full total by the fifteenth entry. Extreme ABV is boutique — concentrated among a few strong releases.</p>
<h2 id="bitterness-and-strength-rise-together-imperfectly" class="anchored">Bitterness and Strength Rise Together — Imperfectly</h2>
<h3 id="bitterness-and-strength-rise-together-imperfectly-look" class="anchored">Abv vs Ibu</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/breweries/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/breweries/charts/chart5_scatter.png" role="img" aria-label="Abv vs Ibu"></div>
</figure>
<p class="art-p">ABV versus IBU across roughly 1,400 plotted points shows many high-IBU IPAs in the 0.06–0.09 ABV band, with some beers exceeding 120 IBU. High ABV does not guarantee high IBU; stouts and quads can be strong without chasing hop extremes. The joint distribution maps the craft design space: hop-forward versus malt-forward paths to intensity.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">ABV and IBU fields can be missing or rounded. Style coverage depends on which breweries entered the scrape. "Craft" definitions and the 2018 vintage miss later hard-seltzer and nonalcoholic shifts.</p>
<p class="art-p">Name-level leaders may be one-off specialty releases, not flagship year-round beers.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Across 2,410 U.S. craft beers, median ABV is 0.06 while the ceiling reaches 0.128. Most of the catalog lives near everyday strength; the high-gravity tail is short and famous.</p>
<p class="art-p">Use the ABV–IBU scatter to explain style strategy: bitterness and alcohol are correlated tools, not a single dial.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2018-07-10 (week15_beers.xlsx). After cleaning, 2,410 rows remain.</p>
<p class="art-p">ABV is the primary ranked metric; IBU joins in the scatter. Charts are Plotly JSON with PNG fallbacks.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2018). <em>TidyTuesday: Craft Beer USA</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2018/2018-07-10/week15_beers.xlsx" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2018/2018-07-10/week15_beers.xlsx</a></p>
</section>
</main>
</div>
