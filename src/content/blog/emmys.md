---
title: "EMMYS: SNL's 859 Records Beat Every Show"
slug: emmys
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  Saturday Night Live appears 859 times across 29,678 Emmy records from 1957–2021—three times the next-closest show.
dek: "Which show appears in Emmy history three times more often than any other?"
heroImage: /images/content/articles/emmys/hero.png
draft: false
tags:
  - arts
  - film
subject: Emmys
tldr: >-
  Sixty-four years of Emmy records reveal a concentrated awards landscape: Saturday Night Live appears 859 times, 2019 holds 2,613 records—the densest year on file—and 80% of all entries carry the "nominee" label, not "winner." Long-running variety programs accumulate nominations the way careers accumulate credits, producing a recurrence map rather than a single-night sweep story.
keyPoints:
  - '859 — Saturday Night Live appearances across the dataset—three times more than the next show'
  - '2,613 — Record count in 2019, the densest Emmy year from 1957–2021'
  - '23,739 — Nominee entries out of 29,678 total rows—wins comprise a thin slice'
faq:
  - question: >-
      Which show has the most Emmy records?
    answer: >-
      Saturday Night Live with 859 appearances across the 1957–2021 dataset.
  - question: >-
      What year had the most Emmy activity?
    answer: >-
      2019 with 2,613 records—the highest in the file.
  - question: >-
      How many records are nominations versus wins?
    answer: >-
      23,739 are labeled "nominee"; wins and other types fill the remainder of 29,678 rows.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Saturday Night Live appears 859 times across 29,678 Emmy records from 1957–2021—three times more than the next-closest show and a sign that Emmy concentration tilts toward programs that return year after year rather than one-night sweeps.</p>
<p class="art-p">The working file holds <strong>29,678</strong> records spanning <strong>1957–2021</strong>. Nominee is the most common label, accounting for <strong>23,739</strong> rows—wins and other designations occupy a thinner slice, which means any leaderboard drawn from this extract ranks recurrence more than victory.</p>

<h2 id="landscape" class="anchored">Landscape</h2>
<h3 id="landscape-look" class="anchored">Nominee dominates with 23,739 records</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emmys/charts/chart1_category.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emmys/charts/chart1_category.png" role="img" aria-label="Nominee dominates with 23,739 records"></div>
</figure>
<p class="art-p">Nominee dominates with 23,739 records. The file is built around nomination rows; wins and other type labels sit in a thinner slice. That imbalance is structural—any leaderboard drawn from this extract ranks how often names enter the nominee column, not how often they win.</p>
<h2 id="volume" class="anchored">Volume</h2>
<h3 id="volume-look" class="anchored">Records By Period</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emmys/charts/chart1_volume.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emmys/charts/chart1_volume.png" role="img" aria-label="Records By Period"></div>
</figure>
<p class="art-p">Activity peaks in 2019 with 2,613 records—the densest year in the span. Period-level counts show when Emmy paperwork thickened: more categories, more programs, more named credits. Volume is the first signal that awards seasons are not equally crowded across decades.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Saturday Night Live appears 859 times — the most recurring name in the file</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emmys/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emmys/charts/chart2_leaders.png" role="img" aria-label="Saturday Night Live appears 859 times — the most recurring name in the file"></div>
</figure>
<p class="art-p">Saturday Night Live appears 859 times—the most recurring name in the file. The top dozen account for a visible share of all 29,678 rows. Long-running variety and franchise programs accumulate nominations the way long careers accumulate credits. Dominance here is recurrence, not a single sweep night.</p>
<h2 id="category" class="anchored">Category</h2>
<h3 id="category-look" class="anchored">Nominee is the largest bucket with 23,739 records</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emmys/charts/chart3_category.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emmys/charts/chart3_category.png" role="img" aria-label="Nominee is the largest bucket with 23,739 records"></div>
</figure>
<p class="art-p">Nominee is the largest bucket with 23,739 records. Category concentration shows where editorial attention should focus when reading the table. If the question is "who swept," separate win rows carefully. If the question is "who kept getting invited," this nominee-heavy landscape is the right map.</p>
<h2 id="timeline" class="anchored">Timeline</h2>
<h3 id="timeline-look" class="anchored">Leaders Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emmys/charts/chart4_timeline.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emmys/charts/chart4_timeline.png" role="img" aria-label="Leaders Over Time"></div>
</figure>
<p class="art-p">Leading names do not move in lockstep—some fade as others surge. Tracking counts over time separates sustained presence from one-off spikes. A show that dominates a single ceremony is a different data shape from a name that returns for decades.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and week-of-export coverage limits apply. Merged tables may fan out or duplicate rows when join keys are imperfect.</p>
<p class="art-p">Findings describe the file on hand—structural signals about Emmy nomination volume and recurrence through 2021, not a complete history of television quality.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Emmy concentration shows up as recurrence: Saturday Night Live at 859 appearances, a nominee column that holds 23,739 of 29,678 rows, and a 2019 peak of 2,613 records. Leaders, volume, and timelines each answer a different question about how lopsided the season became.</p>
<p class="art-p">Use the charts to separate invitation from victory—then check the type field before treating any name as a sweep.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2021-09-21 (R for Data Science community). The working file contains 29,678 rows and 11 columns after merging available tables in the week folder.</p>
<p class="art-p">Charts export as Plotly JSON with PNG fallbacks. Counts by type, period, and recurring name are the main instruments—this table captures volume and recurrence rather than a single quality score.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2021). <em>TidyTuesday: Emmy Awards</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-09-21/nominees.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-09-21/nominees.csv</a></p>
</section>
</main>
</div>
