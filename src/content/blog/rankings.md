---
title: "RANKINGS: How the Chart Top Got Crowded"
slug: rankings
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: Large-scale Hot 100 data show how rankings compress at the summit.
dek: "The Hot 100 gets more crowded the closer you get to number one."
heroImage: /images/content/articles/rankings/hero.png
draft: false
tags:
  - arts
  - music
subject: Billboard
tldr: >-
  The Billboard Hot 100 is a weekly ranking machine: 100 positions, endlessly
  refreshed. The TidyTuesday billboard extract used here holds 100,000 song-week
  rows, with a median week position of 50.0 — exactly mid-chart — and a highest
  observed week position of 100 (the bottom rung).
keyPoints:
  - '100,000 — Records in the working dataset'
  - 50.0 — Median Week position
  - 100 — Highest observed Week position
  - Down By The River — Top Song by Week position
faq:
  - question: >-
      How many records are in this dataset?
    answer: >-
      100,000 records in the working dataset.
  - question: >-
      What is the median Week position?
    answer: >-
      The median Week position is 50.0.
  - question: >-
      What is the highest observed value in this extract?
    answer: >-
      The highest observed value in the extract is 100.
  - question: >-
      Which Song leads in this extract?
    answer: >-
      Down By The River leads the Song ranking in this extract.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">The Billboard Hot 100 is a weekly ranking machine: 100 positions, endlessly refreshed. The TidyTuesday billboard extract used here holds <strong>100,000</strong> song-week rows, with a median week position of <strong>50.0</strong> — exactly mid-chart — and a highest observed week position of <strong>100</strong> (the bottom rung).</p>
<p class="art-p">That median of 50 is almost tautological in a full 1–100 ranking, which is why the interesting questions shift to concentration, re-entries (instance), and which titles spend time at the chart’s edges. “Down By The River” appears among the fact-box leaders for week position in this working file.</p>

<h2 id="song-level-position-averages-crowd-the-bottom-rung" class="anchored">Song-Level Position Averages Crowd the Bottom Rung</h2>
<h3 id="song-level-position-averages-crowd-the-bottom-rung-look" class="anchored">Week position by Song</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/rankings/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/rankings/charts/chart1_breakdown.png" role="img" aria-label="Week position by Song"></div>
</figure>
<p class="art-p">When songs are ranked by week-position summaries, a block of titles ties at <strong>100</strong> — including Girl (You Captivate Me), Time Seller, Gee Baby (I’m Sorry), and others. Those are songs whose observed positions in this aggregation sit at the chart floor. The chart is less a hall of fame than a map of how many titles live at the margins of the Hot 100’s attention economy.</p>
<h2 id="leaders-by-week-position-are-a-flat-elite" class="anchored">Leaders by Week Position Are a Flat Elite</h2>
<h3 id="leaders-by-week-position-are-a-flat-elite-look" class="anchored">(Quarter To Four) Stomp leads at 100 — 100 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/rankings/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/rankings/charts/chart2_leaders.png" role="img" aria-label="(Quarter To Four) Stomp leads at 100 — 100 marks the median among the top dozen"></div>
</figure>
<p class="art-p">(Quarter To Four) Stomp and peer titles in the leaders view hit <strong>100</strong>, and the median among the top dozen is also <strong>100</strong>. There is no graded ladder here — the “leaders” by this numeric field are a plateau at the bottom rank. That flatness is informative: many songs brush the Hot 100 without climbing. Presence is not the same as dominance.</p>
<h2 id="weekly-positions-fill-the-chart-almost-uniformly" class="anchored">Weekly Positions Fill the Chart Almost Uniformly</h2>
<h3 id="weekly-positions-fill-the-chart-almost-uniformly-look" class="anchored">Week position Distribution</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/rankings/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/rankings/charts/chart3_distribution.png" role="img" aria-label="Week position Distribution"></div>
</figure>
<p class="art-p">The distribution of week positions across the 100,000-row sample is remarkably even: bin counts hover near <strong>5,000</strong> observations across the 1–100 range. A full Hot 100 every week produces that rectangular shape by design. Uniform position counts are the baseline. Deviations in other charts — concentration among songs, re-entry instances — are where the cultural story lives.</p>
<h2 id="concentration-among-songs-is-mechanical-at-first" class="anchored">Concentration Among Songs Is Mechanical at First</h2>
<h3 id="concentration-among-songs-is-mechanical-at-first-look" class="anchored">Cumulative Week position</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/rankings/charts/chart4_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/rankings/charts/chart4_pareto.png" role="img" aria-label="Cumulative Week position"></div>
</figure>
<p class="art-p">The Pareto curve over leading song entries rises in near-equal steps in this view, reaching 100% by the fifteenth plotted entry. Within the restricted leader set, share accumulates steadily rather than in a single spike. Full-catalog fame concentration is a different question; this curve describes the ranked subset on display, not every Hot 100 occupant since the 1950s.</p>
<h2 id="re-entries-stretch-a-song-s-life-without-guaranteeing-rank" class="anchored">Re-Entries Stretch a Song’s Life Without Guaranteeing Rank</h2>
<h3 id="re-entries-stretch-a-song-s-life-without-guaranteeing-rank-look" class="anchored">Week position vs Instance</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/rankings/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/rankings/charts/chart5_scatter.png" role="img" aria-label="Week position vs Instance"></div>
</figure>
<p class="art-p">Week position versus instance (re-entry or appearance count) shows titles returning to the chart at many ranks. High instance values appear across both strong and weak positions. Longevity on Billboard is not only about peaking at No. 1. It is also about how many times a song is allowed to reappear — a second career path the scatter makes visible.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Billboard’s chart methodology has changed over decades (sales, airplay, streaming). A pooled file mixes eras with different rules. Song-title collisions and punctuation variants can split or merge identities.</p>
<p class="art-p">Numeric “leaders” by week position in this stack highlight the bottom of the chart, not the cultural canon. Read rank direction carefully before citing.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">A 100,000-row Hot 100 extract is mostly a uniform grid of weekly ranks — median 50, full coverage from 1 to 100. The drama is in which songs repeatedly occupy that grid and which only touch position 100.</p>
<p class="art-p">Cite the uniform distribution when explaining the chart’s structure; cite instance versus position when explaining how hits persist.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2021-09-14 (billboard.csv). After cleaning, the analysis sample contains 100,000 records.</p>
<p class="art-p">Week position is the primary metric; lower numbers are better ranks in Billboard’s native scale, but several charts here rank the numeric position field directly as stored. Charts are Plotly JSON with PNG fallbacks.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2021). <em>TidyTuesday: Billboard Top 100</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-09-14/billboard.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-09-14/billboard.csv</a></p>
</section>
</main>
</div>
