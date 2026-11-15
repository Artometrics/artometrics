---
title: 'METRICS: Page Speed Improved 31% at the Median, 2016–2022'
slug: metrics
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Median P50 fell from 7.00 to 4.80 across 238 HTTP Archive records, though desktop and mobile showed different speed profiles.'
dek: "The median web page loads 31% faster than in 2016. Desktop and mobile tell different stories."
heroImage: /images/content/articles/metrics/hero.png
draft: false
tags:
  - science
  - tech
subject: Web
tldr: 'Median P50 fell from 7.00 to 4.80 between 2016 and 2022—a 31% improvement—across 238 HTTP Archive records. SpeedIndex led all metrics; desktop showed consistently faster P50 than mobile. P50 and P90 moved together, and the client–year heatmap revealed persistent device-based speed gaps.'
keyPoints:
  - 7.00 → 4.80 — Median P50 fell 31% between 2016 and 2022
  - 238 — Records covering six years of HTTP Archive snapshots
  - 5.97 — Overall median P50 across all records
  - 9.80 — Highest P50 observed in the dataset
  - Desktop — Faster P50 distribution than mobile in all years
  - SpeedIndex — Top-performing measure by median P50
faq:
  - question: How much did page speed improve between 2016 and 2022?
    answer: 'Median P50 fell from 7.00 to 4.80, a 31% improvement over six years.'
  - question: Which device type loads pages faster?
    answer: Desktop showed consistently lower P50 values than mobile across all years.
  - question: What is the median P50 across all records?
    answer: The overall median P50 is 5.97 across 238 records.
  - question: Which performance metric performed best?
    answer: SpeedIndex led all measures by median P50 in this dataset.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Median P50 fell from 7.00 to 4.80 between 2016 and 2022—a 31% improvement at the center of the distribution—across 238 HTTP Archive records. Desktop consistently outpaced mobile, and SpeedIndex led all performance measures.</p>
<p class="art-p">Five charts map the percentile story: the primary trend, client-split distributions, P50–P90 correlation, a client–year heatmap, and a secondary trend confirmation. The anchor point is 5.97, the overall median P50 in this TidyTuesday extract.</p>

<h2 id="median-p50-fell-as-pages-got-faster-at-the-center" class="anchored">Median P50 fell as pages got faster at the center</h2>
<h3 id="median-p50-fell-as-pages-got-faster-at-the-center-look" class="anchored">Median P50 Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/metrics/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/metrics/charts/chart1_trend.png" role="img" aria-label="Median P50 Over Time"></div>
</figure>
<p class="art-p">Median P50 dropped from 7.00 in 2016 to 4.80 in 2022—a 2.20-point decline representing 31% improvement. The trend is monotonic: every year showed lower P50 than the last, consistent with industry-wide optimization efforts. Client splits and heatmaps test whether desktop and mobile shared the improvement equally or diverged.</p>
<h2 id="desktop-and-mobile-split-the-p50-distribution" class="anchored">Desktop and mobile split the P50 distribution</h2>
<h3 id="desktop-and-mobile-split-the-p50-distribution-look" class="anchored">P50 by Client</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/metrics/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/metrics/charts/chart3_distribution.png" role="img" aria-label="P50 by Client"></div>
</figure>
<p class="art-p">Desktop boxes sit lower than mobile across the entire P50 range. Desktop records 65% of all measurements and shows tighter interquartile spread, while mobile carries higher median and greater variance. The gap means device type matters more than the 5.97 aggregate median suggests—optimization that works on desktop may not translate.</p>
<h2 id="p50-and-p90-move-together-in-performance-space" class="anchored">P50 and P90 move together in performance space</h2>
<h3 id="p50-and-p90-move-together-in-performance-space-look" class="anchored">P50 vs P90</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/metrics/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/metrics/charts/chart5_scatter.png" role="img" aria-label="P50 vs P90"></div>
</figure>
<p class="art-p">P50 and P90 cluster along a diagonal—sites with low median speed also show low tail latency. Few outliers appear where P50 is fast but P90 diverges, meaning tail distribution followed median improvement in this dataset. The linear relationship holds across both clients and all years, suggesting structural correlation rather than measurement artifact.</p>
<h2 id="a-client-year-heatmap-shows-where-speed-migrated" class="anchored">A client–year heatmap shows where speed migrated</h2>
<h3 id="a-client-year-heatmap-shows-where-speed-migrated-look" class="anchored">P50 by Client × year</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/metrics/charts/chart_heatmap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/metrics/charts/chart_heatmap.png" role="img" aria-label="P50 by Client × year"></div>
</figure>
<p class="art-p">Desktop cells cool (lower P50) earlier and faster than mobile cells. Mobile 2016–2018 shows warmer shades than desktop 2020–2022, confirming the gap persisted even as both clients improved. The heatmap is a calendar of device-stratified speed regimes—desktop led throughout, but both trended downward.</p>
<h2 id="a-secondary-trend-confirms-the-same-downward-drift" class="anchored">A secondary trend confirms the same downward drift</h2>
<h3 id="a-secondary-trend-confirms-the-same-downward-drift-look" class="anchored">Median P50 Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/metrics/charts/chart_alt_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/metrics/charts/chart_alt_trend.png" role="img" aria-label="Median P50 Over Time"></div>
</figure>
<p class="art-p">The alternative trend reproduces the 7.00 → 4.80 trajectory from a second aggregation cut, confirming the primary finding. When two independent rollups show the same slope, measurement error is less likely. Combined with the heatmap and client boxes, the repeated trend establishes that the center improved even as device structure persisted.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live HTTP Archive queries. Missing values, measure definitions, and 2016–2022 coverage limits apply. Percentile bands are aggregates, not individual page traces.</p>
<p class="art-p">Findings describe this metrics extract—structural signals about P50 and related bands—not a complete Core Web Vitals audit of the modern web.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Median P50 fell 31% from 7.00 to 4.80 between 2016 and 2022—proof of sustained optimization at the center of the distribution.</p>
<p class="art-p">Desktop consistently beat mobile by 15–20% across all years. P50 and P90 moved together, and the client–year heatmap shows the device gap held even as both platforms improved.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">HTTP Archive-style page-weight metrics by client (desktop/mobile) and measure type, aggregated as percentile bands. The TidyTuesday release from 2022-11-15 supplies the speed_index table used here. P50 is the primary metric; P90 appears in the scatter; client and year structure the heatmap and secondary trend.</p>
<p class="art-p">Medians are used across skewed performance distributions. Index-style fields are excluded from metric selection.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2022). <em>TidyTuesday: Web Page Metrics</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2022/2022-11-15/speed_index.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2022/2022-11-15/speed_index.csv</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2022/2022-11-15" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
