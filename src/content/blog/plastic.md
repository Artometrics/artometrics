---
title: 'PLASTIC: Plastic Mismanagement Stayed Uneven as GDP Doubled Since 1700'
slug: plastic
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: '22,204 country-year records show high income funds collection but does not guarantee low leakage; coastal economies face mismanagement risk at any income level.'
heroImage: /images/content/articles/plastic/hero.png
draft: false
tags:
  - culture
  - environment
subject: Plastic
tldr: 'Median GDP per capita rose from 5,891 to 12,592 between 1700 and 2017, but mismanaged plastic waste remains geographically concentrated. High income correlates with collection capacity, not automatic cleanliness; lower-income coastal economies show elevated leakage even at modest per-capita generation rates.'
keyPoints:
  - '22,204 — Country-year records spanning 1700–2017 in the TidyTuesday dataset'
  - '8,447 — Median GDP per capita (PPP, constant 2011 international dollars) — half of observations fall below this threshold'
  - '135,319 — Highest observed GDP per capita (Macao) — 16× the global median and 9× the top-decile floor'
  - '5,891 to 12,592 — Median GDP per capita range over the full historical span — prosperity doubled while waste infrastructure remained uneven'
  - Income–mismanagement scatter shows clusters averages hide — rich economies with low leakage coexist with lower-income coastal hotspots
faq:
  - question: Does higher GDP per capita reduce plastic mismanagement?
    answer: High income correlates with collection infrastructure but does not guarantee low leakage; some lower-income coastal economies show elevated mismanagement despite modest per-capita generation.
  - question: How many country-year records are in this dataset?
    answer: '22,204 records spanning 1700 to 2017, with denser coverage for income than for waste metrics in early centuries.'
  - question: Which country has the highest GDP per capita in this dataset?
    answer: 'Macao, at 135,319 PPP constant 2011 international dollars — 16 times the global median.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Median GDP per capita rose from 5,891 to 12,592 between 1700 and 2017, yet mismanaged plastic waste remains geographically concentrated — high income funds collection capacity but does not guarantee low leakage.</p>
<p class="art-p">A TidyTuesday compilation of country-year records delivers <strong>22,204</strong> rows spanning three centuries. Median GDP per capita sits at <strong>8,447</strong> (PPP, constant 2011 international dollars); the highest observed rate reaches <strong>135,319</strong> in Macao. The year range runs <strong>1700</strong> to <strong>2017</strong> — long enough to track the arrival of modern prosperity and modern waste in tandem.</p>
<p class="art-p">Income alone does not settle the mismanagement question. Rich economies can fund collection systems; lower-income coastal economies can become leakage hotspots even at modest per-person generation. The charts below separate those layers.</p>

<h2 id="how-the-pattern-changed-over-time" class="anchored">How prosperity moved over time</h2>
<h3 id="how-the-pattern-changed-over-time-look" class="anchored">Median GDP per capita, PPP (constant 2011 international $) (Rate) Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/plastic/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/plastic/charts/chart1_trend.png" role="img" aria-label="Median GDP per capita, PPP (constant 2011 international $) (Rate) Over Time"></div>
</figure>
<p class="art-p">Median GDP per capita rises from roughly <strong>5,891</strong> in the opening period to about <strong>12,592</strong> at the close. That climb is the backdrop for plastic: mass polymers are a late-twentieth-century material arriving inside an income distribution that was already diverging for centuries. The time chart is not a plastic-generation curve. It is the economic stage on which generation and mismanagement later play out — and it shows that global medians hide enormous cross-country gaps in the same year.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top of income</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Qatar leads at 118,396 — 67,799 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/plastic/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/plastic/charts/chart2_leaders.png" role="img" aria-label="Qatar leads at 118,396 — 67,799 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Among the highest GDP-per-capita observations, <strong>Qatar</strong> leads near <strong>118,396</strong>. The median among the top dozen sits around <strong>67,799</strong> — still eight times the file-wide median of 8,447. Macao, Singapore, Switzerland, and other high-income city-states and petro-economies fill the same thin upper band. These leaders matter for plastic debates because high income correlates with high consumption — but not automatically with high mismanagement. Collection infrastructure can rise with prosperity even as packaging intensity rises with it.</p>
<h2 id="how-the-field-is-spread" class="anchored">How income is spread</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">GDP per capita, PPP (constant 2011 international $) (Rate) Distribution</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/plastic/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/plastic/charts/chart3_distribution.png" role="img" aria-label="GDP per capita, PPP (constant 2011 international $) (Rate) Distribution"></div>
</figure>
<p class="art-p">The distribution is right-skewed: median <strong>8,447</strong> versus mean <strong>14,926</strong>. The top decile begins near <strong>37,969</strong>. That tail is where high-income cases live — and where mean-based storytelling will overstate how typical prosperity feels. Most country-year observations sit far below the headline petro-state and city-state peaks. Any claim about the world and plastic that starts from the mean income will describe a richer planet than the median resident actually inhabits.</p>
<h2 id="leader-trends" class="anchored">Leader trends</h2>
<h3 id="leader-trends-look" class="anchored">Top Entity Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/plastic/charts/chart4_leader_trends.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/plastic/charts/chart4_leader_trends.png" role="img" aria-label="Top Entity Over Time"></div>
</figure>
<p class="art-p">The leading names do not move in lockstep. Some high-income series fade as others surge; oil-price cycles and small-population city economies can reshuffle the top of a PPP ranking without changing the deeper structure of global waste. Tracking leaders over time separates sustained dominance from one-off spikes. For plastic policy, sustained high-income systems with strong waste services are a different object than briefly elevated GDP readings in small jurisdictions.</p>
<h2 id="what-moves-together" class="anchored">Income versus mismanaged plastic</h2>
<h3 id="what-moves-together-look" class="anchored">GDP per capita, PPP (constant 2011 international $) (Rate) vs Per capita mismanaged plastic waste (kilograms per person per day)</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/plastic/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/plastic/charts/chart5_scatter.png" role="img" aria-label="GDP per capita, PPP (constant 2011 international $) (Rate) vs Per capita mismanaged plastic waste (kilograms per person per day)"></div>
</figure>
<p class="art-p">Plotting GDP per capita against per-capita mismanaged plastic waste shows clusters that averages erase. Some rich economies sit low on mismanagement — consumption with collection. Some lower-income coastal economies sit high on mismanagement even when generation per person is modest. That scatter is the core policy map. Generation without management becomes ocean-bound leakage; management without reduced generation becomes an expensive success. The file cannot settle every causal claim, but it stops the false equation that wealth alone explains visible plastic pollution.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and week-of-export coverage limits apply. Early historical GDP rows are not paired with modern waste instrumentation.</p>
<p class="art-p">Mismanaged waste estimates depend on modeling assumptions about litter, dumping, and collection coverage. Treat the relationship charts as structural signals about income and leakage risk — not as a courtroom inventory of every country's shoreline.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Plastic waste sits at the intersection of prosperity and infrastructure. Median incomes in the file roughly doubled over the long span, while mismanagement risk remained geographically uneven.</p>
<p class="art-p">The citable lesson: high GDP per capita identifies capacity, not automatic cleanliness, and low GDP per capita identifies constraint, not automatic innocence. The scatter of income against mismanagement is where those two truths become visible at once.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p"><a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-05-21">The source is the TidyTuesday release from 2019-05-21 (R for Data Science community). The working file contains 22,204 rows and 7 columns after assembling the week's tables — including GDP per capita (PPP) and per-capita mismanaged plastic waste in kilograms per person per day.</a></p>
<p class="art-p">Medians are used where distributions skew. Charts export as Plotly JSON with PNG fallbacks. Country names, missing years, and sparse early coverage mean the long historical span is denser for income than for waste metrics; early centuries provide context for prosperity, not a continuous waste census.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
</section>
</main>
</div>
