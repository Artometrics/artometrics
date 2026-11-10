---
title: 'PARKS: Golden Gate Draws 94× the Median National Park Visit'
slug: parks
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Golden Gate National Recreation Area recorded 14.6 million visits in the dataset''s peak year — 94 times the system median of 155,219 across 21,560 park-year records from 1904–2016.'
heroImage: /images/content/articles/parks/hero.png
draft: false
tags:
  - culture
  - travel
subject: Parks
tldr: 'National Park Service visitation from 1904–2016 reveals a two-tier system: median annual visits rose from 2,200 to 198,478, while the top five parks captured 52% of all recorded traffic. Golden Gate leads at 14.6 million; Alaska trails the median by 142,104.'
keyPoints:
  - '21,560 — Park-year records spanning 1904–2016 in the TidyTuesday dataset'
  - '155,219 — Median annual visits across all park units and years'
  - '14,554,750 — Golden Gate''s peak annual visits, 94× the median'
  - 52% — Share of total visits concentrated in the top five parks
  - '12,634,481 — National Capital region''s lead over the median; Alaska trails by 142,104'
  - '2,200 to 198,478 — Median visits rose 90× from the earliest to latest period'
faq:
  - question: Which national park records the most visits?
    answer: 'Golden Gate National Recreation Area leads at 14,554,750 annual visits in the dataset''s peak year.'
  - question: What is the median annual visit count across all parks?
    answer: 'The median is 155,219 visits per park per year across 21,560 records from 1904–2016.'
  - question: How concentrated is national park visitation?
    answer: The top five parks account for 52% of all recorded visits in the dataset.
  - question: How much has park visitation grown over time?
    answer: 'Median visits rose from 2,200 in the earliest period to 198,478 by 2016 — a 90-fold increase.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Golden Gate National Recreation Area recorded 14,554,750 annual visits at its dataset peak — 94 times the system median of 155,219 — because proximity to San Francisco matters more than wilderness purity in the visitation ledger.</p>
<p class="art-p">A TidyTuesday working file of <strong>21,560</strong> park-year records spans <strong>1904–2016</strong>. Median visits sit at <strong>155,219</strong>; the highest single observation reaches <strong>871,922,828</strong>. <strong>Golden Gate</strong> leads the park-name ranking, and region code <strong>IM</strong> (Intermountain) appears most frequently in the data.</p>
<p class="art-p">Urban gateways and memorial parkways often outdraw remote wilderness. The leaderboard reflects access and metropolitan adjacency as much as scenic reputation.</p>

<h2 id="how-the-pattern-changed-over-time" class="anchored">How visits grew over time</h2>
<h3 id="how-the-pattern-changed-over-time-look" class="anchored">Median Visitors Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/parks/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/parks/charts/chart1_trend.png" role="img" aria-label="Median Visitors Over Time"></div>
</figure>
<p class="art-p">Median visitors rose from <strong>2,200</strong> in the opening period to <strong>198,478</strong> by 2016 — a 90-fold increase driven by automobile access, population growth, system expansion, and the conversion of outdoor recreation into a middle-class norm. The median's climb is the system story; the leaders are the celebrity story.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Golden Gate leads at 14,554,750 — 5,151,270 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/parks/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/parks/charts/chart2_leaders.png" role="img" aria-label="Golden Gate leads at 14,554,750 — 5,151,270 marks the median among the top dozen"></div>
</figure>
<p class="art-p"><strong>Golden Gate</strong> leads at <strong>14,554,750</strong> annual visits, with <strong>5,151,270</strong> as the median among the top dozen. Other high-traffic units include urban memorials and parkways — Vietnam Veterans Memorial, World War II Memorial, Lake Mead, Natchez Trace, Cape Cod — where recreation, commuting, and civic pilgrimage overlap. Wilderness icons still matter culturally. They do not win the raw visit count contest against metropolitan National Park Service units that function as public squares with transit access.</p>
<h2 id="how-the-field-is-spread" class="anchored">How regions spread visits</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Visitors by Region</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/parks/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/parks/charts/chart3_distribution.png" role="img" aria-label="Visitors by Region"></div>
</figure>
<p class="art-p">Regional box plots show whether visitor consensus is shared or contested across NPS regions. Some regions host many modest units; others host a few magnets that dominate the regional total. Spread within a region can exceed differences between region medians. A single gateway park can outdraw an entire cluster of remote units.</p>
<h2 id="who-beats-the-median-and-who-trails" class="anchored">Who beats the median — and who trails</h2>
<h3 id="who-beats-the-median-and-who-trails-look" class="anchored">Visitors vs median by Region</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/parks/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/parks/charts/chart4_gap.png" role="img" aria-label="Visitors vs median by Region"></div>
</figure>
<p class="art-p">Region <strong>NT</strong> (National Capital) sits <strong>12,634,481</strong> above the median; <strong>AK</strong> (Alaska) trails by <strong>142,104</strong>. Those gaps encode access and population gravity — Alaska's vast parklands are not built for weekend volume. The gap is a map of visitation pressure, not beauty.</p>
<h2 id="concentration" class="anchored">Concentration of visits</h2>
<h3 id="concentration-look" class="anchored">The top 5 parkname entries account for 52% of the aggregate visitors</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/parks/charts/chart_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/parks/charts/chart_pareto.png" role="img" aria-label="The top 5 parkname entries account for 52% of the aggregate visitors"></div>
</figure>
<p class="art-p">The top five park-name entries account for <strong>52%</strong> of aggregate visitors in the working file. Infrastructure stress, concession economics, and reservation politics concentrate in a short list of places — even while the agency's mission names a much longer list.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and century-scale definition changes apply. Visitor counts are not unique individuals and are not measures of ecological impact.</p>
<p class="art-p">Findings describe structural signals about National Park Service visitation patterns in the file — not a conservation audit or a ranking of which landscapes matter most.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Median park traffic rose 90-fold from 1904 to 2016, while the top five units absorbed 52% of all visits. The citable tension is access versus myth: America's most visited park units are often the ones closest to cities and memorials, not the ones on the wilderness postcard.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p"><a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-09-17">The source is the TidyTuesday release from 2019-09-17 (R for Data Science community). The working file contains 21,560 rows and 13 columns — park names, regions, years, and visitor totals.</a></p>
<p class="art-p">Medians handle skew from hyper-visited units. Charts export as Plotly JSON with PNG fallbacks. Visitor totals are administrative counts; definition changes over a century mean long-run levels are directional, not exact.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
</section>
</main>
</div>
