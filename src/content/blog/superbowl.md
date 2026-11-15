---
title: "SUPERBOWL: Five Brands Capture 87% of Ad Views"
slug: superbowl
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: NFL leads at 403,641 views; median dropped from 111,814 to 33,766 as the 2006–2021 archive filled with ordinary uploads.
dek: "Five brands drew 87% of the views on Super Bowl ads in this archive. Which five?"
heroImage: /images/content/articles/superbowl/hero.png
draft: false
tags:
  - civics
  - communication
subject: Super Bowl
tldr: >-
  Super Bowl commercials live a second life on YouTube. In 247 uploads from 2006–2021, median views fell from 111,814 to 33,766 as the archive grew, while the ceiling hit 176,373,378. Five brands—NFL, Doritos, and three others—account for 87% of aggregate views.
keyPoints:
  - 87% — Five brands control this share of aggregate views
  - 41,379 — Median views across 247 uploads, down from 111,814 in the earliest period
  - 176,373,378 — Peak view count, 4,200× the median
  - 403,641 — NFL's median among top-twelve brands; Doritos leads the full-file ranking
  - 2006–2021 — Fifteen-year span; falling median reflects archive expansion, not ad quality
  - youtube#video — Dominant format; view-to-like clusters reveal uneven engagement conversion
faq:
  - question: >-
      How many Super Bowl ads are in this dataset?
    answer: >-
      247 YouTube uploads spanning 2006–2021, drawn from the TidyTuesday archive.
  - question: >-
      Why did median views drop over time?
    answer: >-
      The archive added more ordinary uploads; the ceiling stayed stratospheric while the center fell to 33,766.
  - question: >-
      Which brand has the most views?
    answer: >-
      NFL leads the top-twelve median at 403,641; Doritos ranks first in the full-file aggregation.
  - question: >-
      What share of views do the top five brands capture?
    answer: >-
      87% of aggregate views, a steep Pareto concentration.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Five brands capture 87% of all post-game Super Bowl ad views on YouTube, according to 247 uploads spanning 2006–2021. Median views fell from 111,814 to 33,766 as the archive expanded, but the ceiling reached 176,373,378—proof that a handful of commercials become folklore while most settle into inventory. NFL leads the top-twelve brand median at 403,641 views; Doritos ranks first in the full-file aggregation.</p>
<p class="art-p">Post-game streaming attention operates as its own economy. Broadcast buys the first audience; YouTube decides which spots circulate for years. The dataset tracks that second life through trend, brand leaders, format distribution, concentration, and the relationship between views and likes.</p>

<h2 id="median-views-fell-as-the-archive-got-denser" class="anchored">Median views fell as the archive got denser</h2>
<h3 id="median-views-fell-as-the-archive-got-denser-look" class="anchored">Median View count Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/superbowl/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/superbowl/charts/chart1_trend.png" role="img" aria-label="Median View count Over Time"></div>
</figure>
<p class="art-p">Median view count fell from 111,814 in the earliest period to 33,766 at the end of the span. That decline does not signal deteriorating ad quality—it reflects the archive filling out with more ordinary uploads, pulling the center down while the ceiling remained stratospheric at 176,373,378. The falling median and the fixed ceiling coexist because attention is power-law distributed: most ads cluster near the median, a few explode into viral territory.</p>
<h2 id="nfl-leads-the-brand-ladder-on-youtube-views" class="anchored">NFL leads the brand ladder on YouTube views</h2>
<h3 id="nfl-leads-the-brand-ladder-on-youtube-views-look" class="anchored">NFL leads at 403,641 — 46,661 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/superbowl/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/superbowl/charts/chart2_leaders.png" role="img" aria-label="NFL leads at 403,641 — 46,661 marks the median among the top dozen"></div>
</figure>
<p class="art-p">NFL leads the top-twelve brands at 403,641 views; the median within that group sits at 46,661. Doritos remains the top brand in the full-file aggregation; the chart isolates the highest performers in this particular cut. The gap between #1 and the top-dozen median shows how quickly the ladder drops. A few brands own the conversation; most of the competitive set operates closer to tens of thousands than hundreds of thousands.</p>
<h2 id="almost-everything-in-the-file-is-a-youtube-video" class="anchored">Almost everything in the file is a YouTube video</h2>
<h3 id="almost-everything-in-the-file-is-a-youtube-video-look" class="anchored">View count by Kind</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/superbowl/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/superbowl/charts/chart3_distribution.png" role="img" aria-label="View count by Kind"></div>
</figure>
<p class="art-p">Splitting view count by format produces a near-monoculture: youtube#video is the dominant kind. The distribution confirms the archive's platform identity rather than revealing contested formats. This matters for scope. The dataset tracks post-game internet lives of Super Bowl ads on YouTube, not a complete census of every commercial that aired during the broadcast.</p>
<h2 id="five-brands-hold-eighty-seven-percent-of-aggregate-views" class="anchored">Five brands hold eighty-seven percent of aggregate views</h2>
<h3 id="five-brands-hold-eighty-seven-percent-of-aggregate-views-look" class="anchored">Cumulative View count</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/superbowl/charts/chart4_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/superbowl/charts/chart4_pareto.png" role="img" aria-label="Cumulative View count"></div>
</figure>
<p class="art-p">The top five brands account for 87% of aggregate views—a steep Pareto curve. Post-game attention is not distributed evenly; a small group drives the bulk of summed engagement. Concentration at this level explains why brand strategy obsesses over a handful of breakthrough spots. The long tail exists but does not move the aggregate the way the head does.</p>
<h2 id="views-and-likes-travel-together-with-clusters" class="anchored">Views and likes travel together — with clusters</h2>
<h3 id="views-and-likes-travel-together-with-clusters-look" class="anchored">View count vs Like count</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/superbowl/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/superbowl/charts/chart5_scatter.png" role="img" aria-label="View count vs Like count"></div>
</figure>
<p class="art-p">Plotting view count against like count reveals clusters that a single correlation coefficient would obscure. Some ads convert attention into likes efficiently; others accumulate views without the same approval signal. The scatter maps how the two engagement measures co-move in this 247-row extract, not a quality ranking.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">TidyTuesday snapshots are community-cleaned archives, not live YouTube APIs. View and like counts are frozen at export; missing values, brand spelling variants, and coverage gaps apply. Merged tables may duplicate or fan out rows when join keys are imperfect.</p>
<p class="art-p">Findings describe this Super Bowl ads extract and its structural signals, not a comprehensive history of every commercial creative or every platform where ads circulated.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Post-game Super Bowl attention is concentrated: median views sit at 41,379, the ceiling reaches 176,373,378, and five brands capture 87% of aggregate views.</p>
<p class="art-p">The falling median from 111,814 to 33,766 reflects archive expansion, not declining ad quality. NFL and Doritos-scale leaders anchor the archive's memory. Views and likes move together in clusters, which is how engagement looks when a few spots become folklore and most settle into inventory.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2021-03-02, maintained by the R for Data Science community. The working file contains 247 rows and 26 columns after merging available tables. View count is the primary metric; like count appears in the scatter analysis; brand and kind are the main categorical dimensions.</p>
<p class="art-p">Medians are used throughout because ad view counts follow a power-law distribution—a few viral spots dwarf the typical upload. Index fields are excluded so charts describe attention patterns, not row order.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2021). <em>TidyTuesday: Super Bowl Ads</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-03-02/youtube.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-03-02/youtube.csv</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2021/2021-03-02" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
