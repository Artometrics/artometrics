---
title: "BILLBOARD: How Long Number-Ones Stay on Top"
slug: billboard
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  Since 1958, most chart-toppers lasted weeks; a few held for months—and
  streaming rewrote the pattern.
heroImage: /images/content/articles/billboard/hero.png
draft: false
tags:
  - arts
  - music
subject: Billboard
tldr: >-
  The Billboard Hot 100 has published a number-one song every week since August
  1958. In that time it has absorbed the British Invasion, the disco era, the
  rise of hip-hop, the collapse of the album format, and the complete
  restructuring of the music industry by streaming platforms.
keyPoints:
  - '1,195 — Number-one songs in the dataset (1958–2026)'
  - '2 wks — Median run length — most #1s are fleeting'
  - '25 wks — Choosin'' Texas leads as of the chart dated Oct 31, 2026'
  - The Beatles — Most appearances in the dataset — 20 number-one songs
  - '68 yrs — Span of the dataset: 1958 to 2026'
  - Taylor Swift — Highest average run length among modern artists
faq:
  - question: >-
      What is Number-one songs in the dataset?
    answer: >-
      1,195 — Number-one songs in the dataset (1958–2026).
  - question: >-
      What is the median run length?
    answer: >-
      The median run length is 2 wks.
  - question: >-
      What is Longest single run in the dataset?
    answer: >-
      25 weeks for Choosin' Texas, 22 for All I Want for Christmas Is You, 19 for A Bar Song (Tipsy) and Old Town Road, and 16 for Last Night, Despacito, and One Sweet Day, as of the chart dated Oct 31, 2026.
  - question: >-
      What is Most appearances in the dataset?
    answer: >-
      The Beatles — Most appearances in the dataset.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">The Billboard Hot 100 has published a number-one song every week since August 1958. In that time it has absorbed the British Invasion, the disco era, the rise of hip-hop, the collapse of the album format, and the complete restructuring of the music industry by streaming platforms. Through all of it, the same basic question persists: how long can a song stay at the top?</p>
<p class="art-p">The file covers 1,195 distinct number-one entries as of the chart dated Oct 31, 2026. The median run lasts just 2 weeks. The longest runs are 25 weeks for Choosin' Texas, 22 for All I Want for Christmas Is You, 19 for A Bar Song (Tipsy) and Old Town Road, and 16 for Last Night, Despacito, and One Sweet Day. Between those facts sits the entire history of popular music.</p>
<p class="art-p">Start with the scale: <strong>1,195</strong> number-one songs (1958–2026); <strong>2 wks</strong> median run length; The Beatles with the most appearances; Taylor Swift with the highest average run length among modern artists.</p>

<h2 id="run-length-over-the-decades" class="anchored">Run Length Over the Decades</h2>
<h3 id="run-length-over-the-decades-look" class="anchored">Median weeks at number one per year — 1958 to 2026</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/billboard/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/billboard/charts/chart1_trend.png" role="img" aria-label="Median weeks at number one per year — 1958 to 2026"></div>
</figure>
<p class="art-p">The trend line tells a story in two halves. From 1958 through the 1990s, median run length drifts between 2 and 3 weeks — an era when radio play and physical sales set natural limits on how long one song could dominate. Post-2012, the median begins a slow climb as streaming rewrites the economics: a song that goes viral accumulates plays continuously, making it structurally harder for anything else to unseat it. The highest single-year medians in the dataset cluster in the 2015–2025 range. The 2025 median is 6.5 weeks. The 2026 median is 1 week so far. This is the streaming era in action: longer runs, fewer number-ones per year, and a winner-take-most dynamic that concentrates attention on a shrinking pool of mega-hits.</p>
<h2 id="longest-runs-ever" class="anchored">Longest Runs Ever</h2>
<h3 id="longest-runs-ever-look" class="anchored">Top 12 songs by total weeks at number one</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/billboard/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/billboard/charts/chart2_leaders.png" role="img" aria-label="Top 12 songs by total weeks at number one"></div>
</figure>
<p class="art-p">As of the chart dated Oct 31, 2026, Billboard's longest Hot 100 runs are Choosin' Texas by Ella Langley at 25 weeks, All I Want for Christmas Is You by Mariah Carey at 22, A Bar Song (Tipsy) by Shaboozey and Old Town Road at 19, and Last Night, Despacito, and One Sweet Day at 16. The median among the top dozen is 16 weeks. The most striking feature of this chart is what is absent: no Beatles song, no Motown classic, no 1970s or 1980s blockbuster. Every song on this list is from 1992 or later, with the majority from 2010 onward. The longest runs in Hot 100 history are a product of the modern era — of digital music, streaming infrastructure, and the global distribution of taste.</p>
<h2 id="how-artists-compare" class="anchored">How Artists Compare</h2>
<h3 id="how-artists-compare-look" class="anchored">Distribution of run lengths for the most frequently appearing artists</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/billboard/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/billboard/charts/chart3_distribution.png" role="img" aria-label="Distribution of run lengths for the most frequently appearing artists"></div>
</figure>
<p class="art-p">Box plots for the most frequent number-one artists reveal two distinct patterns. Artists like The Beatles have many short-run entries — they reached #1 often, but rarely held it for long, because the pre-SoundScan era cycled songs faster. Modern artists like Mariah Carey or Drake show wider distributions — some short runs, a handful of extended ones — reflecting both more volatile streaming behavior and longer careers in the streaming era. Wide whiskers are the signal here: they identify artists whose success is inconsistent rather than structural. A narrow box with a high median is the mark of a reliable hitmaker. A wide box means the artist occasionally breaks through in a massive way but usually does not.</p>
<h2 id="above-or-below-the-line" class="anchored">Above Or Below the Line</h2>
<h3 id="above-or-below-the-line-look" class="anchored">Artist average run length vs the global median of 2 weeks</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/billboard/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/billboard/charts/chart4_gap.png" role="img" aria-label="Artist average run length vs the global median of 2 weeks"></div>
</figure>
<p class="art-p">Taylor Swift sits above the median — her number-one runs average longer than the historical norm, reflecting both her sustained streaming dominance and an unusually loyal fanbase that streams at high volume across long windows. The diverging bar chart makes the gap visible across artists: those to the right outperform the median; those at the line are average performers despite reaching #1. Reaching number one is necessary but not sufficient for dominance. This chart separates artists who briefly claim the top from those who hold it — and that distinction maps cleanly onto streaming-era versus pre-streaming careers.</p>
<h2 id="scatter-weeks-vs-reach" class="anchored">Scatter: Weeks vs Reach</h2>
<h3 id="scatter-weeks-vs-reach-look" class="anchored">Weeks at number one vs secondary chart reach — scatter of all songs</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/billboard/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/billboard/charts/chart5_scatter.png" role="img" aria-label="Weeks at number one vs secondary chart reach — scatter of all songs"></div>
</figure>
<p class="art-p">New No. 1s from 2025 to 2026 have no secondary-reach value in the source file.</p>
<p class="art-p">The scatter of all songs against a secondary reach metric shows the expected cluster near the origin — most songs arrive briefly and reach a moderate audience — and a sparse upper-right region of true blockbusters: long runs, broad reach, and the kind of cultural saturation that transcends a single chart. The outliers in the upper right are not outliers in the statistical sense — they are archetypes. They represent what the entire industry is optimized to produce, and what it very rarely achieves. Studying them is studying the ceiling, not the average.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">The Hot 100 methodology has changed several times since 1958, making strict historical comparisons difficult. Pre-1991 data relies on self-reported retail sales rather than verified scan data. Streaming weights have increased continuously since 2012. These changes mean that a 10-week run in 1970 and a 10-week run in 2020 represent very different things about commercial culture.</p>
<p class="art-p">The TidyTuesday dataset captures only number-one entries — not the full chart. An artist who dominated the Top 10 for a year without reaching #1 is invisible in this data. Artist name standardization is also imperfect: collaborations and featuring credits may split what is functionally one artist's run across multiple rows.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The Hot 100 is not simply a popularity measure. It is a structural reading of how the music industry concentrates and distributes attention — and that structure has changed fundamentally in the streaming era. The median run length has crept upward. The longest runs have become the longest in history. The artists who dominate now hold the top slot for reasons that pre-streaming hitmakers never had to contend with.</p>
<p class="art-p">The data does not tell you which songs are good. It tells you which songs won the structural game of a particular era. That distinction is the Artometrics mandate — not to celebrate the victor, but to understand the game.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The Hot 100 blends sales, radio airplay, and streaming data into a single weekly ranking. This matters for the reading: the rules of what counts have changed substantially over the decades. Before 1991, physical sales data came from store-reported estimates, not actual scan data — which made the chart easier to game. The introduction of SoundScan in 1991 made the chart dramatically more accurate but also temporarily destabilized it as real sales data replaced guesswork. Streaming was added in 2012, and its weight has grown continuously since.</p>
<p class="art-p">The consequence: a long run in 1965 means something different from a long run in 2025. Streaming amplifies hits — the same song can accumulate streams 24 hours a day, seven days a week, without the bottleneck of radio scheduling. This structural change is visible in the data.</p>
<p class="art-p">All I Want for Christmas Is You is carried at 22 weeks, Billboard's cumulative total as of the chart dated Oct 31, 2026. The weekly file at utdata/rwd-billboard-data commit ff86f04 counts the same 22 No. 1 weeks. That replaces the prior value of 8 on this row. Other fields on the row are unchanged.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2025). <em>TidyTuesday: Billboard Hot 100 Number Ones</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-08-26/billboard.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-08-26/billboard.csv</a></p>
<p>Billboard. (2025). <em>Hot 100 chart history</em>. <a href="https://www.billboard.com/charts/hot-100/" target="_blank" rel="noopener noreferrer">billboard.com/charts/hot-100</a></p>
<p>Billboard Hot 100 chart data, via utdata/rwd-billboard-data (MIT), through the chart dated Oct 31, 2026. <a href="https://github.com/utdata/rwd-billboard-data/blob/ff86f0456f55f8174ea5e91c0872a00df21b8603/data-out/hot-100-current.csv" target="_blank" rel="noopener noreferrer">https://github.com/utdata/rwd-billboard-data/blob/ff86f0456f55f8174ea5e91c0872a00df21b8603/data-out/hot-100-current.csv</a></p>
<p>Trust, Gary. (2026). <em>Ella Langley's 'Choosin' Texas' Rebounds for Record-Extending 25th Week at No. 1 on Hot 100</em>. Billboard. <a href="https://www.billboard.com/lists/ella-langley-choosin-texas-hot-100-number-one-25th-week" target="_blank" rel="noopener noreferrer">https://www.billboard.com/lists/ella-langley-choosin-texas-hot-100-number-one-25th-week</a></p>
<h2 id="editor-s-note" class="anchored">Editor’s note</h2>

<div class="art-editorial-note"><p>This report covers all 1,195 number-one entries in the Hot 100 dataset as of the chart dated Oct 31, 2026. Chart 3 shows the top 10–15 artists by frequency of number-one appearances; the box plots represent the spread of run lengths across each artist's career, not a single song.</p><p><em>All run-length metrics are in weeks. The global median (2 weeks) is used as the baseline in Chart 4. Streaming-era songs (post-2012) systematically outperform the historical median and are over-represented in the top-10 longest runs.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-08-26" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
