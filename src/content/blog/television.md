---
title: 'TELEVISION: Prestige TV Scores Drifted Up—Slowly—From 1990 to 2018'
slug: television
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Median season ratings climbed from 7.86 to 8.15 across 2,266 records—a raised floor, not a sudden elite leap.'
dek: "Is prestige TV actually getting better? The ratings crept up, but slowly."
heroImage: /images/content/articles/television/hero.png
draft: false
tags:
  - arts
  - film
subject: Television
tldr: 'The median TV season rating rose from 7.86 to 8.15 between 1990 and 2018—a 0.29-point gain that suggests the "golden age" raised the floor more than it crowned new peaks. Among 2,266 records, the overall median stood at 8.11, while the top decile began at 8.79. Touched by an Angel led at 9.60, but the distribution skewed less sharply than golden-age rhetoric implies.'
keyPoints:
  - '0.29 — Point increase in median rating from 1990 to 2018—a raised floor, not a spike'
  - '8.11 — Overall median rating across 2,266 season records—the typical row'
  - 8.79 — Threshold for the top decile—where defining cases live
  - 9.60 — Touched by an Angel's lead score—the file's ceiling
  - '2,266 — Season records spanning 1990–2018 from IMDb/Economist extract'
faq:
  - question: How much did median TV ratings rise during the golden age?
    answer: 'Median ratings climbed 0.29 points, from 7.86 in the early 1990s to 8.15 by 2018.'
  - question: What is the median rating across all records?
    answer: 'The overall median is 8.11 across 2,266 season records.'
  - question: Which show scored highest in the dataset?
    answer: Touched by an Angel led at 9.60.
  - question: How skewed is the prestige-TV score distribution?
    answer: 'Nearly symmetric: median 8.11 versus mean 8.06, suggesting less inequality than golden-age rhetoric implies.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Median season ratings rose 0.29 points—from 7.86 to 8.15—between 1990 and 2018, raising the typical show's score without the sharp elite-vs-mediocrity split that golden-age rhetoric promised.</p>
<p class="art-p">The working file holds <strong>2,266</strong> records from <strong>1990–2018</strong>. Median average rating is <strong>8.11</strong>; the highest observed average is <strong>9.68</strong>. Parenthood leads the title ranking in the extract.</p>

<h2 id="how-the-pattern-changed-over-time" class="anchored">How the pattern changed over time</h2>
<h3 id="how-the-pattern-changed-over-time-look" class="anchored">Median Av rating Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/television/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/television/charts/chart1_trend.png" role="img" aria-label="Median Av rating Over Time"></div>
</figure>
<p class="art-p">Median average rating rises from 7.86 in the opening period to 8.15 at the close—a 0.29-point climb that describes the typical row, not the headline cases. The middle of the scoreboard edged upward while prestige TV became a cultural brand. That is not the same shape as an explosion of elite outliers.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Touched by an Angel leads at 9.60 — 9.24 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/television/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/television/charts/chart2_leaders.png" role="img" aria-label="Touched by an Angel leads at 9.60 — 9.24 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Touched by an Angel leads at 9.60; 9.24 marks the median among the top dozen. The head of the board is densely packed at the high end. High averages can reflect passionate rater pools as much as critical consensus. Read the leaders as the file's ceiling, then compare them to the 8.11 median that describes the typical row.</p>
<h2 id="how-the-field-is-spread" class="anchored">How the field is spread</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Av rating Distribution</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/television/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/television/charts/chart3_distribution.png" role="img" aria-label="Av rating Distribution"></div>
</figure>
<p class="art-p">Median 8.11 versus mean 8.06—the shape is nearly symmetric. The top decile begins at 8.79; that tail is where defining cases live. A symmetric prestige-TV scoreboard contradicts the thin-elite-versus-wide-mediocrity story. The distribution is tighter than golden-age rhetoric suggests.</p>
<h2 id="leader-trends" class="anchored">Leader Trends</h2>
<h3 id="leader-trends-look" class="anchored">Top Title Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/television/charts/chart4_leader_trends.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/television/charts/chart4_leader_trends.png" role="img" aria-label="Top Title Over Time"></div>
</figure>
<p class="art-p">Leading names do not move in lockstep—some fade as others surge. Tracking medians over time separates sustained dominance from one-off spikes. A peak season is not the same data shape as a long plateau above 8.</p>
<h2 id="what-moves-together" class="anchored">What moves together</h2>
<h3 id="what-moves-together-look" class="anchored">Av rating vs SeasonNumber</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/television/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/television/charts/chart5_scatter.png" role="img" aria-label="Av rating vs SeasonNumber"></div>
</figure>
<p class="art-p">Average rating and season number show clusters that a single summary would erase—early-season highs, late-season drift, and shows that hold the middle across many seasons. Longevity and quality are related but not identical. The scatter is where that distinction becomes visible.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and week-of-export coverage limits apply. Merged tables may fan out or duplicate rows when join keys are imperfect.</p>
<p class="art-p">Findings describe the file on hand—structural signals about prestige-TV ratings through 2018, not a complete canon of the streaming era that followed.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The median climbed 0.29 points—from 7.86 to 8.15—while the overall middle stayed near 8.11. A raised floor, not a sudden leap. Leaders near 9.6 and a top decile from 8.79 show how much room remains above the typical row.</p>
<p class="art-p">Read trends, distribution, and season scatter together before treating any single title as proof that critics and audiences agreed.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2019-01-08 (R for Data Science community)—the IMDb/Economist TV ratings extract. The working file contains 2,266 rows and 8 columns after merging available tables in the week folder.</p>
<p class="art-p">Charts export as Plotly JSON with PNG fallbacks. Medians handle skew; season numbers join ratings so longevity can be plotted against score.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2019). <em>TidyTuesday: TV Golden Age</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-01-08/IMDb_Economist_tv_ratings.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-01-08/IMDb_Economist_tv_ratings.csv</a></p>
</section>
</main>
</div>
