---
title: "WINE: Austria and Chile, Two Points Apart"
slug: wine
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: Austria leads Chile by 2.00 points; the median sits at 88.0 in a dataset where the top dozen titles all score 100.
heroImage: /images/content/articles/wine/banner.png
draft: false
tags:
  - culture
  - food
subject: Wine
tldr: >-
  100,000 wine ratings from the TidyTuesday archive show a median score of 88.0, a perfect-score ceiling among elite titles, and Austria leading Chile by 2.00 points — a modest gap in a scoring culture that uses the high end of the scale. The points–price scatter reveals clusters that averages erase.
keyPoints:
  - '100,000 — Records — enough to test whether price predicts points across countries and titles'
  - '88.0 — Median score — the mathematical center of a compressed rating scale'
  - "2.00 — Austria's lead over Chile — a small gap in a system that clusters in the high 80s"
  - "100 — Top-dozen median — the elite band is flat at the scale's ceiling"
  - 'US — Most frequent origin — country variation matters less than the dinner-table theory suggests'
faq:
  - question: >-
      How many wine ratings does this analysis cover?
    answer: >-
      100,000 records from the TidyTuesday 2019-05-28 release.
  - question: >-
      What is the median score in this dataset?
    answer: >-
      The median is 88.0; the scale's action happens in a narrow band around that center.
  - question: >-
      Which country scores highest?
    answer: >-
      Austria sits 2.00 points above the median; Chile trails by the same margin.
  - question: >-
      Does price predict critic points?
    answer: >-
      The scatter shows clusters — cheap high scorers, expensive middling bottles — without a clean line.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">100,000 wine ratings from the TidyTuesday archive show a median score of 88.0, a perfect-score ceiling among elite titles, and Austria leading Chile by 2.00 points. The points–price scatter reveals clusters that averages erase: cheap high scorers, expensive middling bottles, and a familiar cloud where spending more often accompanies higher scores without guaranteeing them.</p>
<p class="art-p">The calibration point is 88.0 — the mathematical center of a scoring culture that uses the high end of the scale and leaves the bottom half empty.</p>

<h2 id="perfect-scores-crowd-the-title-breakdown-s-top-slice" class="anchored">Perfect scores crowd the title breakdown's top slice</h2>
<h3 id="perfect-scores-crowd-the-title-breakdown-s-top-slice-look" class="anchored">Points by Title</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wine/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wine/charts/chart1_breakdown.png" role="img" aria-label="Points by Title"></div>
</figure>
<p class="art-p">Château Léoville Barton 2010 Saint-Julien leads at 100; Cardinale 2006 Cabernet Sauvignon (Napa Valley) anchors the low end of the plotted top group at 100 — a flat elite band at the ceiling. When the top slice is all 100s, the chart shows saturation at the maximum, not a ladder of near-misses.</p>

<h2 id="the-leaders-chart-is-a-wall-of-100-point-wines" class="anchored">The leaders chart is a wall of 100-point wines</h2>
<h3 id="the-leaders-chart-is-a-wall-of-100-point-wines-look" class="anchored">Château Léoville Barton 2010 Saint-Julien leads at 100 — 100 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wine/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wine/charts/chart2_leaders.png" role="img" aria-label="Château Léoville Barton 2010 Saint-Julien leads at 100 — 100 marks the median among the top dozen"></div>
</figure>
<p class="art-p">The top dozen's median is 100, not 95 or 97 — the elite is compressed at the ceiling. Charles Smith 2006 Royal City remains a fact-box landmark for the title ranking rule used there, but the wall of perfect scores is the structural signal.</p>

<h2 id="countries-spread-points-around-a-high-center" class="anchored">Countries spread points around a high center</h2>
<h3 id="countries-spread-points-around-a-high-center-look" class="anchored">Points by Country</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wine/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wine/charts/chart3_distribution.png" role="img" aria-label="Points by Country"></div>
</figure>
<p class="art-p">Category boxes by country show whether points consensus is shared or contested across origins. The United States is the most common country by frequency; the boxes test how much score variation place carries in this file.</p>

<h2 id="austria-clears-the-median-chile-trails" class="anchored">Austria clears the median; Chile trails</h2>
<h3 id="austria-clears-the-median-chile-trails-look" class="anchored">Points vs median by Country</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wine/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wine/charts/chart4_gap.png" role="img" aria-label="Points vs median by Country"></div>
</figure>
<p class="art-p">Austria sits 2.00 points above the median; Chile trails by 2.00. Those signed gaps are modest in points terms — a reminder that this scoring culture lives in a narrow band around 88.0. Small gaps can still be meaningful when the whole scale's action happens between the high 80s and the low 90s for most bottles.</p>

<h2 id="points-and-price-form-the-real-test-of-the-dinner-table-theory" class="anchored">Points and price form the real test of the dinner-table theory</h2>
<h3 id="points-and-price-form-the-real-test-of-the-dinner-table-theory-look" class="anchored">Points vs Price</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wine/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wine/charts/chart5_scatter.png" role="img" aria-label="Points vs Price"></div>
</figure>
<p class="art-p">Plotting points against price shows clusters that averages erase: cheap high scorers, expensive middling bottles, and the familiar cloud where spending more often accompanies higher scores without guaranteeing them. The scatter is the relationship the title promised — it shows the joint distribution in the 100,000-row extract without claiming a coefficient beyond what the chart displays.</p>

<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live Wine Enthusiast APIs. Missing prices, title variants, and coverage limits apply. Critic points reflect the source's scoring practice, which uses a compressed high end of the scale.</p>
<p class="art-p">Findings describe this wine extract — structural signals about points, country, and price — not a universal law of taste.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Wine scores in this file center on a median of 88.0, peak at 100 among title leaders, and show only modest country gaps around that high center. Austria sits 2.00 points above the median and Chile 2.00 below, while the points–price scatter is where the cost-versus-score question becomes visible without reducing 100,000 tastings to a slogan.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2019-05-28 (R for Data Science community). The working file contains 100,000 rows and 13 columns after merging available tables. Points is the primary metric; price appears in the scatter; title and country are categorical axes.</p>
<p class="art-p">Medians are used because wine scores cluster tightly and prices skew right.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2019). <em>TidyTuesday: Wine Ratings</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-05-28/winemag-data-130k-v2.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-05-28/winemag-data-130k-v2.csv</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-05-28" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
