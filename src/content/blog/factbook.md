---
title: 'FACTBOOK: Five Countries Hold 72% of World Population'
slug: factbook
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: China's 1.36 billion against a 5.2 million median — the top five countries hold 72% of aggregate population in the CIA World Factbook extract.
dek: "Half the places in the CIA World Factbook have under 5.2 million people. Five hold 72% of everyone."
heroImage: /images/content/articles/factbook/hero.png
draft: false
tags:
  - civics
  - economics
subject: Nations
tldr: '259 countries in the CIA World Factbook extract show a median population of 5,220,371 while China reaches 1,355,692,576. The top five countries account for 72% of aggregate population. High birth rates cluster among smaller nations, not demographic giants.'
keyPoints:
  - 259 — Factbook entries with complete population data
  - '5,220,371 — Median population; mean is 32,294,361 due to right skew'
  - 72% — Aggregate population share held by the top five countries
  - 'Zero correlation — High birth rates appear in small countries, not population leaders'
faq:
  - question: How many countries are in the CIA World Factbook dataset?
    answer: 259 entries with population data in the October 2024 TidyTuesday extract.
  - question: What is the median population in the dataset?
    answer: '5,220,371 people.'
  - question: Which country has the largest population?
    answer: 'China at 1,355,692,576.'
  - question: What share of global population do the top five countries hold?
    answer: Approximately 72% of the aggregate in this ranking.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">China's 1,355,692,576 people sit against a global median of 5,220,371 in the CIA World Factbook extract — a 260-fold gap that drives every concentration metric. The top five countries hold 72% of aggregate population; most nations operate at a scale closer to the median than to the summit.</p>
<p class="art-p">Mean population (~32 million) sits far above the median because a handful of giants pull the average upward. The distribution is right-skewed: 218 of 259 entries fall into the smallest bin.</p>

<h2 id="a-handful-of-giants-dominate-headcount" class="anchored">A Handful of Giants Dominate Headcount</h2>
<h3 id="a-handful-of-giants-dominate-headcount-look" class="anchored">Population by Country</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/factbook/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/factbook/charts/chart1_breakdown.png" role="img" aria-label="Population by Country"></div>
</figure>
<p class="art-p">China leads at 1.36 billion, India at 1.24 billion, the European Union aggregate near 511 million, the United States near 319 million, Indonesia near 254 million, and Brazil near 203 million. These six operate in a different scale class than the median country at 5.2 million. They are not outliers; they are the architectural beams of every global concentration statistic.</p>
<h2 id="even-the-top-dozen-has-a-steep-internal-drop" class="anchored">Even the Top Dozen Has a Steep Internal Drop</h2>
<h3 id="even-the-top-dozen-has-a-steep-internal-drop-look" class="anchored">China leads at 1,355,692,576 — 199,415,584 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/factbook/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/factbook/charts/chart2_leaders.png" role="img" aria-label="China leads at 1,355,692,576 — 199,415,584 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Within the top twelve, the median is 199,415,584 — less than one-sixth of China's total. The drop from first to sixth is steeper than the drop from sixth to twelfth. "Large country" is a pyramid, not a plateau. Second-tier giants are already far smaller than the demographic summit.</p>
<h2 id="most-countries-sit-in-the-small-population-mass" class="anchored">Most Countries Sit in the Small-Population Mass</h2>
<h3 id="most-countries-sit-in-the-small-population-mass-look" class="anchored">Median 5,220,371 vs mean 32,294,361 — the shape is right-skewed</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/factbook/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/factbook/charts/chart3_distribution.png" role="img" aria-label="Median 5,220,371 vs mean 32,294,361 — the shape is right-skewed"></div>
</figure>
<p class="art-p">The first bin holds 218 of 259 entries. Only a handful of observations reach the billionaire tier or approach it. The median (5.2 million) describes the typical country; the mean (~32 million) is pulled upward by the giants. Use the median when the question is "most countries" and the top five when the question is "most people."</p>
<h2 id="the-top-five-already-hold-most-of-the-people" class="anchored">The Top Five Already Hold Most of the People</h2>
<h3 id="the-top-five-already-hold-most-of-the-people-look" class="anchored">The top 5 country entries account for 72% of the aggregate population</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/factbook/charts/chart4_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/factbook/charts/chart4_pareto.png" role="img" aria-label="The top 5 country entries account for 72% of the aggregate population"></div>
</figure>
<p class="art-p">The Pareto curve shows the top five countries accounting for 72% of aggregate population. By fifteen entries the curve approaches the full plotted total. Global population is not evenly distributed across flags. It is concentrated in a short list of demographic powers.</p>
<h2 id="high-birth-rates-cluster-among-smaller-populations" class="anchored">High Birth Rates Cluster Among Smaller Populations</h2>
<h3 id="high-birth-rates-cluster-among-smaller-populations-look" class="anchored">Population vs Birth rate</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/factbook/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/factbook/charts/chart5_scatter.png" role="img" aria-label="Population vs Birth rate"></div>
</figure>
<p class="art-p">Birth rates above 40 per 1,000 cluster among countries well below the mega-population tier. Several large countries sit at lower birth rates. Demographic giants are not fertility leaders. Scale and birth rate are independent stories in the Factbook.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Factbook figures are estimates with uneven vintage and methodology across entities. Including the European Union alongside countries double-counts if users sum naively. Small territories and disputed entities add definitional noise.</p>
<p class="art-p">Population totals are not prosperity scores. Pairing with birth rate is descriptive, not a development ranking.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">In 259 Factbook rows, the median country has 5.2 million people while China exceeds 1.35 billion. The top five entries hold 72% of the aggregate in the concentration view.</p>
<p class="art-p">Cite the median for a typical state; cite China, India, and the Pareto share when the question is planetary concentration.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2024-10-22 (cia_factbook.csv). After cleaning, 259 rows remain.</p>
<p class="art-p">Population is the primary ranked metric; birth rate appears in the joint scatter. Charts are Plotly JSON with PNG fallbacks.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2024). <em>TidyTuesday: CIA World Factbook</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2024/2024-10-22/cia_factbook.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2024/2024-10-22/cia_factbook.csv</a></p>
</section>
</main>
</div>
