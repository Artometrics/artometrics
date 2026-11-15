---
title: "MAC: Twenty Years of Big Mac Prices"
slug: mac
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  Global burger prices illustrate how currency and wages shape the real cost of
  everyday goods.
dek: "The same burger costs nearly three times the median price in one country. Which one?"
heroImage: /images/content/articles/mac/hero.png
draft: false
tags:
  - civics
  - economics
subject: Burgers
tldr: >-
  A Big Mac is the same product everywhere on Earth — same bun, same patties,
  same sauce. That sameness is exactly what makes its price interesting. The
  Economist’s Big Mac Index, running since 1986, converts local burger prices
  into US dollars to reveal how far currencies stray from purchasing power
  parity.
keyPoints:
  - $3.04 — Median dollar price across all countries and years
  - $8.31 — Peak price — Switzerland at its most expensive
  - 83% — Price increase from 2000 to 2020 at the global median
  - Norway — Highest average dollar price over the full 20-year span
  - '20 yrs — Timespan: 2000 through 2020'
faq:
  - question: >-
      What is the median dollar price across all countries and years?
    answer: >-
      The median dollar price across all countries and years is $3.04.
  - question: >-
      What is Peak price?
    answer: >-
      $8.31 — Peak price.
  - question: >-
      What is Price increase from 2000 to 2020 at the global median?
    answer: >-
      83% — Price increase from 2000 to 2020 at the global median.
  - question: >-
      What time period does this dataset cover?
    answer: >-
      The file covers Norway.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">A Big Mac is the same product everywhere on Earth — same bun, same patties, same sauce. That sameness is exactly what makes its price interesting. The Economist’s Big Mac Index, running since 1986, converts local burger prices into US dollars to reveal how far currencies stray from purchasing power parity. The working extract covers <strong>1,386</strong> observations spanning <strong>2000 through 2020</strong>.</p>
<p class="art-p">The gap between the cheapest and most expensive burger in any given year is not noise. It maps onto wage structures, agricultural policy, taxes, and the raw purchasing power of local currencies. Switzerland’s peak above <strong>$8</strong> encodes a high-wage cost structure; a sub-$2 burger elsewhere tells a symmetrically different story.</p>
<p class="art-p">Keep the calibration numbers close: the median dollar price across all country-years is <strong>$3.04</strong>, the peak observed is <strong>$8.31</strong>, and the global median rose about <strong>83%</strong> from 2000 to 2020.</p>

<h2 id="global-price-trend" class="anchored">Global Price Trend</h2>
<h3 id="global-price-trend-look" class="anchored">Global median Big Mac dollar price, 2000–2020</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/mac/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/mac/charts/chart1_trend.png" role="img" aria-label="Global median Big Mac dollar price, 2000–2020"></div>
</figure>
<p class="art-p">The median dollar price nearly doubles over two decades, climbing from about <strong>$1.91</strong> in 2000 to about <strong>$3.50</strong> by 2020. The path is not linear: medians stall and dip in the mid-2010s as a strong U.S. dollar compresses dollar-equivalent prices recorded in many markets, then recover toward the end of the sample. Using the median — rather than the mean — keeps Switzerland, Norway, and other extreme outliers from rewriting the global story. The median says what a typical country pays; the mean says what the expensive tail can afford.</p>
<h2 id="most-expensive-countries" class="anchored">Most Expensive Countries</h2>
<h3 id="most-expensive-countries-look" class="anchored">Top 12 countries by average Big Mac dollar price</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/mac/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/mac/charts/chart2_leaders.png" role="img" aria-label="Top 12 countries by average Big Mac dollar price"></div>
</figure>
<p class="art-p">Switzerland leads average dollar prices at about <strong>$6.54</strong>, with Norway close behind near <strong>$6.24</strong>. Sweden, Denmark, Brazil, Canada, Israel, and the Euro area fill out the upper tier. Norway holds the highest average dollar price over the full 20-year span among the fact-box leaders. The gap between Switzerland and the twelfth-ranked country is larger than the gap between that twelfth country and the global median of $3.04. The top of the distribution is thin air.</p>
<h2 id="how-prices-spread" class="anchored">How Prices Spread</h2>
<h3 id="how-prices-spread-look" class="anchored">Distribution of Big Mac dollar prices across all country-year observations</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/mac/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/mac/charts/chart3_distribution.png" role="img" aria-label="Distribution of Big Mac dollar prices across all country-year observations"></div>
</figure>
<p class="art-p">Most country-year observations cluster between roughly <strong>$2 and $4</strong>, with a long right tail of wealthy, high-price markets. The median ($3.04) sits below the mean because that tail pulls the average upward. “Expensive” is a select club in this histogram, not a smooth continuum. The bottom half of the world, in this sample, pays between the low end of the distribution and the $3.04 median for the same standardized burger.</p>
<h2 id="tracking-the-leaders" class="anchored">Tracking the Leaders</h2>
<h3 id="tracking-the-leaders-look" class="anchored">Price trajectories for the top-ranked countries over time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/mac/charts/chart4_leader_trends.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/mac/charts/chart4_leader_trends.png" role="img" aria-label="Price trajectories for the top-ranked countries over time"></div>
</figure>
<p class="art-p">Country trajectories do not rise in unison. Argentina, Australia, Brazil, and Canada each show distinct dollar-price paths — commodity cycles, currency crashes, and local inflation leave different fingerprints. Membership in the expensive-burger club is relatively stable; rankings inside it are not. Sustained dominance requires sustained structural advantage, not a one-year FX spike.</p>
<h2 id="local-vs-dollar-price" class="anchored">Local vs Dollar Price</h2>
<h3 id="local-vs-dollar-price-look" class="anchored">Local currency price vs US dollar price — scatter plot</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/mac/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/mac/charts/chart5_scatter.png" role="img" aria-label="Local currency price vs US dollar price — scatter plot"></div>
</figure>
<p class="art-p">The scatter of local-currency prices against dollar prices makes exchange-rate distortion visible. Points far from a simple correspondence are countries where conversion, not the kitchen, does most of the work. Emerging-market currencies often produce low dollar prices even when local nominal prices look large. That joint distribution is the index’s entire point: sameness of product, difference of money.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">McDonald’s does not charge a uniform markup everywhere: franchise agreements, competition, and brand positioning move prices independently of pure PPP. Coverage is uneven — the series misses many countries where McDonald’s has little or no presence.</p>
<p class="art-p">The snapshot ends in 2020 and excludes the post-pandemic inflation surge. Treat the findings as a structural portrait of two decades, not a live FX dashboard.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Twenty years of Big Mac prices describe a slow rise in global living costs and a persistent hierarchy between high-wage and lower-wage economies. The median nearly doubles; the gap between Switzerland and the median barely disappears.</p>
<p class="art-p">The index collapses complex macroeconomics into one comparable number. What it measures unambiguously is concentration at the top — a small cluster of high-cost economies that the rest of the sample does not reach.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">Purchasing power parity (PPP) theory says exchange rates should eventually converge so identical goods cost the same everywhere. In practice they rarely do — tariffs, non-tradeable costs (rent, labor), and monetary policy all interfere. The Big Mac Index sidesteps complex econometric models: if a burger costs less in dollar terms than the U.S. price implies, that currency is often read as undervalued; if it costs more, overvalued.</p>
<p class="art-p">The TidyTuesday snapshot (2020-12-22) supplies the country-year price series used here. The index is deliberately blunt: better at identifying structural divergence than at predicting short-run FX moves.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2020). <em>TidyTuesday: Big Mac Index</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-12-22/mac.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-12-22/mac.csv</a></p>
<p>The Economist. (2020). <em>The Big Mac Index</em>. <a href="https://www.economist.com/mac" target="_blank" rel="noopener noreferrer">economist.com/mac</a></p>
<h2 id="editor-s-note" class="anchored">Editor’s note</h2>

<div class="art-editorial-note"><p>This analysis is part of the Artometrics TidyTuesday series. All charts are interactive (hover for values) with static PNG fallbacks. Source data is publicly available and reproducible from the GitHub link below.</p><p><em>Dollar prices reflect the raw local price converted at the prevailing exchange rate — not adjusted for inflation or PPP. All medians computed on the full annual sample for each year.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-12-22" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
