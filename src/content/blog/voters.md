---
title: 'VOTERS: National Turnout Hit 132 Million; Most States Stayed Near 1.2 Million'
slug: voters
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: National turnout reached 132.6 million in 2014 while the median state recorded 1.17 million votes across 936 elections from 1980–2014.
dek: "How many people actually vote in a typical state? Far fewer than the national total makes it sound."
heroImage: /images/content/articles/voters/hero.png
draft: false
tags:
  - civics
  - politics
subject: Voters
tldr: 'National turnout reached 132,609,063 in 2014 while the median state recorded 1,170,867 votes, according to 936 election records from 1980–2014. The national aggregate appears as a separate entity in the dataset, sitting 113 times higher than the typical state. Median state turnout rose 52% from 910,290 to 1,387,622 over the period.'
keyPoints:
  - '132,609,063 — Peak national turnout in 2014 — 113× the median state'
  - '1,170,867 — Median state turnout — below mean of 3,074,280 due to right skew'
  - '52% — Rise in median state turnout from 910,290 (1980) to 1,387,622 (2014)'
  - '4,659,000 — Top-decile threshold — separating high-volume from typical states'
  - 936 — Elections analyzed — spanning 35 years and 50 states plus national totals
faq:
  - question: What was the highest recorded voter turnout?
    answer: 'National turnout reached 132,609,063 in 2014, the highest value in the 936-record dataset spanning 1980–2014.'
  - question: How does median differ from mean turnout?
    answer: 'Median state turnout was 1,170,867 versus mean of 3,074,280; large states and national totals create right skew.'
  - question: Which states led voter turnout?
    answer: 'National aggregate topped the dataset at 90,912,015 average votes; among states, the top dozen averaged 4,209,538.'
  - question: How much did state turnout grow from 1980 to 2014?
    answer: 'Median state turnout rose 52% from 910,290 to 1,387,622 over the 35-year period.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">National turnout reached 132,609,063 in 2014 while the median state recorded 1,170,867 votes, according to 936 election records from 1980–2014. The national aggregate appears as a separate entity in the dataset, sitting 113 times higher than the typical state.</p>
<p class="art-p">Five charts separate trend, leaders, distribution shape, state trajectories, and the relationship between votes cast and eligible voters. The median of 1,170,867 divides smaller states below from larger electorates and national totals above.</p>

<h2 id="median-votes-rose-across-three-decades-of-elections" class="anchored">Median votes rose across three decades of elections</h2>
<h3 id="median-votes-rose-across-three-decades-of-elections-look" class="anchored">Median Votes Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/voters/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/voters/charts/chart1_trend.png" role="img" aria-label="Median Votes Over Time"></div>
</figure>
<p class="art-p">Median state turnout rose 52% from 910,290 in 1980 to 1,387,622 in 2014. Population growth, eligibility expansion, and election-type composition all contribute to the upward trend. The rising median provides context for state-level comparisons: leader states and national totals amplify the trend, while smaller jurisdictions track within the shifting distribution.</p>
<h2 id="the-united-states-total-dwarfs-the-state-ladder" class="anchored">The United States total dwarfs the state ladder</h2>
<h3 id="the-united-states-total-dwarfs-the-state-ladder-look" class="anchored">United States leads at 90,912,015 — 4,209,538 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/voters/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/voters/charts/chart2_leaders.png" role="img" aria-label="United States leads at 90,912,015 — 4,209,538 marks the median among the top dozen"></div>
</figure>
<p class="art-p">The national aggregate averages 90,912,015 votes across the period, while the median among the top dozen states sits at 4,209,538. The national row represents the sum of all state turnout, not a peer comparison. The peak of 132,609,063 reflects this national-scale aggregation. Individual state rankings occur far below that ceiling.</p>
<h2 id="a-right-skewed-distribution-with-a-heavy-upper-tail" class="anchored">A right-skewed distribution with a heavy upper tail</h2>
<h3 id="a-right-skewed-distribution-with-a-heavy-upper-tail-look" class="anchored">Median 1,170,867 vs mean 3,074,280 — the shape is right-skewed</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/voters/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/voters/charts/chart3_distribution.png" role="img" aria-label="Median 1,170,867 vs mean 3,074,280 — the shape is right-skewed"></div>
</figure>
<p class="art-p">Median state turnout of 1,170,867 sits below the mean of 3,074,280 because large states and national totals create a long right tail. The top decile begins at 4,659,000, separating high-volume states from the rest. Right skew explains why turnout analysis requires medians and rates rather than raw averages alone.</p>
<h2 id="leading-states-reshuffle-across-election-cycles" class="anchored">Leading states reshuffle across election cycles</h2>
<h3 id="leading-states-reshuffle-across-election-cycles-look" class="anchored">Top State Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/voters/charts/chart4_leader_trends.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/voters/charts/chart4_leader_trends.png" role="img" aria-label="Top State Over Time"></div>
</figure>
<p class="art-p">State trajectories diverge over time: some maintain high turnout while others surge or fade. Tracking individual states separates sustained volume from cycle-specific spikes. Presidential versus midterm composition within the dataset can shift the state ladder even when the overall median rises.</p>
<h2 id="votes-scale-with-eligible-voters-in-clusters" class="anchored">Votes scale with eligible voters — in clusters</h2>
<h3 id="votes-scale-with-eligible-voters-in-clusters-look" class="anchored">Votes vs Eligible voters</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/voters/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/voters/charts/chart5_scatter.png" role="img" aria-label="Votes vs Eligible voters"></div>
</figure>
<p class="art-p">Votes cast rise with eligible-voter pools, but the scatter plot reveals clusters that averages obscure. Larger eligibility produces larger turnout, yet the pattern's texture shows variation in how tightly that relationship holds across states and years. The joint distribution captures turnout as a rate problem without requiring a calculated rate column: eligibility and votes move together, and the clusters show where exceptions occur.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">TidyTuesday snapshots are community-cleaned extracts, not live election records. Missing values, jurisdiction-naming variants, and 1980–2014 coverage limits apply. National and state rows coexist in ways that require care when ranking.</p>
<p class="art-p">Findings describe this voter-turnout extract — structural patterns in vote totals — not a complete model of registration law, suppression, or mobilization.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Median state turnout rose 52% from 910,290 to 1,387,622 between 1980 and 2014, while the national aggregate reached 132,609,063 at its peak. Vote totals are right-skewed around the median of 1,170,867, with the top decile beginning at 4,659,000.</p>
<p class="art-p">State rankings shift across election cycles, and votes track eligible-voter pools in clusters — a volume atlas of American elections across 35 years.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2018-10-09 (R for Data Science community). The working file contains 936 rows and 7 columns after merging available tables. Votes is the primary metric; eligible voters appears in the scatter plot; state and national totals form the entity axis.</p>
<p class="art-p">Median turnout is the central measure because vote totals are right-skewed: mean of 3,074,280 versus median of 1,170,867. Large states and the national aggregate pull the average upward.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2018). <em>TidyTuesday: US Voter Turnout</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2018/2018-10-09/voter_turnout.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2018/2018-10-09/voter_turnout.csv</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2018/2018-10-09" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
