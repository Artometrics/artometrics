---
title: 'SLICES: A Dozen Steam Titles Captured Half the Audience'
slug: slices
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Median concurrent players climbed from 212 to 309 across the decade, but Dota 2''s 475,924 average dwarfs the top-twelve median of 64,656.'
dek: "A dozen Steam games grabbed half the audience. Which ones?"
heroImage: /images/content/articles/slices/hero.png
draft: false
tags:
  - sports
  - gaming
subject: Games
tldr: 'The TidyTuesday 2021-03-16 video-games extract contains 83,631 Steam title-months from 2012 through 2021. Median average concurrent players (Avg) rose from 212 to 309, a 46 % climb, while the file median sits at 203. Dota 2 leads at 475,924 Avg; the highest single observation reaches 1,584,887. January runs 36.9 above the median; October trails by 23.3.'
keyPoints:
  - '203 — Median Avg across all 83,631 title-months, the center of a long-tailed concurrency distribution'
  - 46 % — Growth from opening median of 212 to closing median of 309 between 2012 and 2021
  - '475,924 — Dota 2 leads the top-twelve by a factor of 7.4 over the group''s median of 64,656'
  - '1,584,887 — Highest observed Avg in the file, flagging the extreme ceiling above charted leaders'
  - '36.9 — January''s offset above the file median, the largest positive month effect'
  - 'February — Most common month label in the file, a coverage artifact rather than a concurrency claim'
faq:
  - question: How much did median concurrency grow from 2012 to 2021?
    answer: 'Median Avg rose from 212 to 309, a 46 % increase over the period covered.'
  - question: What is Dota 2's average concurrent player count in this dataset?
    answer: 'Dota 2 leads at 475,924 Avg, 7.4 times the top-twelve median of 64,656.'
  - question: Which month shows the highest concurrency relative to the file median?
    answer: 'January sits 36.9 above the median, the largest positive month offset in the file.'
  - question: What is the highest single Avg observation recorded?
    answer: 'The file''s peak Avg reaches 1,584,887, appearing in the PLAYERUNKNOWN''S BATTLEGROUNDS record set.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Median average concurrent players on Steam rose from 212 to 309 between 2012 and 2021, a 46 % climb that still leaves the typical title-month at 203 in an 83,631-row extract. Dota 2 leads at 475,924 Avg — 7.4 times the top-twelve median — and the file's single highest observation reaches 1,584,887. January runs 36.9 above the median; October trails by 23.3.</p>
<p class="art-p">The file is the TidyTuesday 2021-03-16 video-games release, merged from community-cleaned Steam player-count snapshots. Charts trace the median's climb, rank the leaders by Avg, map month offsets, and plot Avg against Gain to show how level and change co-occur in a long-tailed market.</p>

<h2 id="median-concurrency-climbed-across-the-decade" class="anchored">Median concurrency climbed across the decade</h2>
<h3 id="median-concurrency-climbed-across-the-decade-look" class="anchored">Median Avg Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/slices/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/slices/charts/chart1_trend.png" role="img" aria-label="Median Avg Over Time"></div>
</figure>
<p class="art-p">Median Avg rises from 212 at the series open to 309 at the close, crossing above the file median of 203 midway through the period. The 46 % gain reflects either platform growth, survivor bias among tracked titles, or both. The chart reports the center's path. Individual titles distribute around that median in ways the trend line does not capture.</p>
<h2 id="dota-2-leads-a-top-tier-that-drops-off-fast" class="anchored">Dota 2 leads a top tier that drops off fast</h2>
<h3 id="dota-2-leads-a-top-tier-that-drops-off-fast-look" class="anchored">Dota 2 leads at 475,924 — 64,656 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/slices/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/slices/charts/chart2_leaders.png" role="img" aria-label="Dota 2 leads at 475,924 — 64,656 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Dota 2 leads at 475,924 Avg, 7.4 times the top-twelve median of 64,656. The gap from first to the elite-tier median defines the live-service economy: a few titles sustain city-scale populations; the rest of the top dozen are large but operate in a different order of magnitude. The file's highest single Avg — 1,584,887, appearing in the PLAYERUNKNOWN'S BATTLEGROUNDS record set — sits above even the charted leaders, marking the extreme ceiling of the distribution.</p>
<h2 id="months-carry-different-concurrency-distributions" class="anchored">Months carry different concurrency distributions</h2>
<h3 id="months-carry-different-concurrency-distributions-look" class="anchored">Avg by Month</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/slices/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/slices/charts/chart3_distribution.png" role="img" aria-label="Avg by Month"></div>
</figure>
<p class="art-p">Box plots by month reveal whether Avg spreads uniformly or clusters around distinct medians across the calendar. Seasonal launches, holidays, and school schedules can shift who is online. February's frequency in the file is a coverage fact, not a player-count claim; the boxes measure dispersion within each month, not record volume.</p>
<h2 id="january-clears-the-median-october-trails" class="anchored">January clears the median; October trails</h2>
<h3 id="january-clears-the-median-october-trails-look" class="anchored">Avg vs median by Month</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/slices/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/slices/charts/chart4_gap.png" role="img" aria-label="Avg vs median by Month"></div>
</figure>
<p class="art-p">January sits 36.9 above the file median; October trails by 23.3. Those signed offsets convert the calendar into a comparable scale against the center, revealing structural month effects in this extract. The offsets are not proof of a universal gaming season — coverage dates, launch windows, and sample composition all shape the pattern — but they are concrete enough to cite when asking when concurrency runs hot or cold in this snapshot.</p>
<h2 id="avg-and-gain-form-a-joint-cloud-of-winners-and-churn" class="anchored">Avg and Gain form a joint cloud of winners and churn</h2>
<h3 id="avg-and-gain-form-a-joint-cloud-of-winners-and-churn-look" class="anchored">Avg vs Gain</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/slices/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/slices/charts/chart5_scatter.png" role="img" aria-label="Avg vs Gain"></div>
</figure>
<p class="art-p">Plotting Avg against Gain reveals clusters that medians erase: high average with stable gain is a different audience story from high average with volatile gain, and low average with positive gain signals a trajectory invisible in rank tables. The scatter maps how level and change co-occur across the 83,631 title-months, showing the joint distribution that single-metric summaries cannot capture.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live SteamCharts APIs. Missing values, title variants, and 2012–2021 coverage limits apply. Merged tables may fan out or duplicate rows when join keys are imperfect, inflating counts.</p>
<p class="art-p">Avg and Gain are the metrics as defined in the source tables. Findings describe concurrency structure in this extract, not complete commercial P&amp;L for every title or the full Steam catalog.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The file median of 203 Avg anchors an 83,631-row distribution that rose from 212 to 309 at the median between 2012 and 2021, a 46 % climb. Dota 2 leads at 475,924, 7.4 times the top-twelve median, and the single highest observation reaches 1,584,887.</p>
<p class="art-p">January sits 36.9 above the median; October trails by 23.3. Avg–Gain scatter plots show how level and momentum travel together in a long-tailed live-service market where a few titles capture city-scale audiences and the typical game serves hundreds.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2021-03-16, published by the R for Data Science community. The working file contains 83,631 rows and 8 columns after merging available tables. Avg is the primary metric; Gain appears in scatter analysis; month and game name are categorical axes.</p>
<p class="art-p">Medians replace means because player counts follow a power-law distribution. Index fields are excluded from aggregation.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2021). <em>TidyTuesday: Video Games</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-03-16/sliced-tidytuesday.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-03-16/sliced-tidytuesday.csv</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2021/2021-03-16" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
