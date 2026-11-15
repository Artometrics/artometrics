---
title: 'CEOs: CEO Tenure Caps at 2.5 Years in 9,423 Departure Records'
slug: ceos
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: Median tenure coded at 1.0 year; "Interim" label accounts for 218 observations in TidyTuesday departures extract.
dek: "Thousands of CEO departures, one question: how long did they actually last?"
heroImage: /images/content/articles/ceos/hero.png
draft: false
tags:
  - civics
  - business
subject: CEOs
tldr: 'In 9,423 CEO-departure records from TidyTuesday, median max tenure ceodb is 1.00 year and the highest observed value is 4.00. "Interim" is the dominant succession label, appearing in 218 rows; company-level leaders reach 2.0–2.5 years at most.'
keyPoints:
  - '9,423 — Departure records with median max tenure of 1.00 year'
  - '2.50 — Ceiling for company leaders (Stewart Information, Conversant Inc)'
  - '218 — "Interim" label count, median tenure 1.0 year'
  - 1.0 gap — Only CO-ceo variant shows positive distance from file median
faq:
  - question: How many CEO departure records are in this dataset?
    answer: '9,423 records.'
  - question: What is the median max tenure in the file?
    answer: 1.00 year.
  - question: Which company shows the longest max tenure?
    answer: Stewart Information Services and Conversant Inc at 2.50 years.
  - question: How many records carry the Interim label?
    answer: 218 observations.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">In 9,423 TidyTuesday CEO-departure records, median max tenure ceodb is <strong>1.00</strong> year and the ceiling is <strong>4.00</strong>. "Interim" appears in <strong>218</strong> rows—the dominant succession label—while company-level leaders reach <strong>2.0–2.5</strong> years at most.</p>
<p class="art-p">The median of 1.00 sets the baseline: many coded departure spells are short. The data ask which companies show longer max tenures, how interim versus co-CEO labels differ, and whether tenure fields move together.</p>

<h2 id="longer-max-tenures-are-rare-in-the-company-ranking" class="anchored">Longer Max Tenures Are Rare in the Company Ranking</h2>
<h3 id="longer-max-tenures-are-rare-in-the-company-ranking-look" class="anchored">Max tenure ceodb by Coname</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/ceos/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/ceos/charts/chart1_breakdown.png" role="img" aria-label="Max tenure ceodb by Coname"></div>
</figure>
<p class="art-p">Stewart Information Services and Conversant Inc lead at <strong>2.50</strong> on max tenure ceodb. A second tier—Avatex, Intrepid Potash, Bergen Brunswig, SEACOR, Micro Warehouse, RH—clusters at <strong>2.00</strong>. Relative to the file median of 1.00, even these leaders are only modestly longer spells. Extended CEO tenure is the exception, not the rule.</p>
<h2 id="the-top-dozen-caps-out-quickly" class="anchored">The Top Dozen Caps Out Quickly</h2>
<h3 id="the-top-dozen-caps-out-quickly-look" class="anchored">CONVERSANT INC leads at 2.50 — 2.00 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/ceos/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/ceos/charts/chart2_leaders.png" role="img" aria-label="CONVERSANT INC leads at 2.50 — 2.00 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Conversant Inc appears at <strong>2.50</strong>, and the median among the top dozen is <strong>2.00</strong>. There is no long tail of decade-scale max tenures in this ranking metric. Cite 2.00 as the elite-club median for max tenure ceodb—double the overall median, still short of popular narratives about imperial CEOs.</p>
<h2 id="interim-labels-dominate-the-category-mix" class="anchored">Interim Labels Dominate the Category Mix</h2>
<h3 id="interim-labels-dominate-the-category-mix-look" class="anchored">Max tenure ceodb by Interim coceo</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/ceos/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/ceos/charts/chart3_distribution.png" role="img" aria-label="Max tenure ceodb by Interim coceo"></div>
</figure>
<p class="art-p">Interim accounts for <strong>218</strong> observations with a median max tenure of <strong>1.0</strong> and a mean near <strong>1.23</strong>. CO-CEO shows <strong>85</strong> rows with the same median of 1.0 but a slightly higher mean of approximately <strong>1.4</strong>. Smaller capitalization variants are tiny samples. The file is thick with interim spells—a succession-system fact: many departures pass through temporary authority before a permanent appointment.</p>
<h2 id="gaps-to-the-median-are-mostly-flat" class="anchored">Gaps to the Median Are Mostly Flat</h2>
<h3 id="gaps-to-the-median-are-mostly-flat-look" class="anchored">Max tenure ceodb vs median by Interim coceo</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/ceos/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/ceos/charts/chart4_gap.png" role="img" aria-label="Max tenure ceodb vs median by Interim coceo"></div>
</figure>
<p class="art-p">Most interim/co-CEO labels sit at a zero gap to the median on max tenure ceodb, with only a thinly populated CO-ceo variant showing a positive gap of <strong>1.0</strong>. Category labels do not produce a dramatic tenure hierarchy. The larger pattern is the volume of spells coded interim.</p>
<h2 id="tenure-fields-track-closely-within-labels" class="anchored">Tenure Fields Track Closely Within Labels</h2>
<h3 id="tenure-fields-track-closely-within-labels-look" class="anchored">Max tenure ceodb vs Tenure no ceodb</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/ceos/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/ceos/charts/chart5_scatter.png" role="img" aria-label="Max tenure ceodb vs Tenure no ceodb"></div>
</figure>
<p class="art-p">Max tenure ceodb versus tenure no ceodb, colored by interim/co-CEO label, largely follows a tight correspondence—points hug aligned values, especially in the interim cloud (n=218). Where the two tenure fields disagree, coding definitions matter more than boardroom narrative. The scatter is a consistency check on the file's tenure construction.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Tenure fields are database constructions, not calendar biographies. Spelling variants of co-CEO fragment categories. Firm name changes and dual-class structures can split identities.</p>
<p class="art-p">A median of 1.00 may reflect coding granularity as much as calendar instability. Read the metric definition before converting it into a headline.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">In 9,423 departure records, max tenure ceodb centers at 1.00, with company-level leaders reaching only 2.0–2.5. Interim is the dominant succession label.</p>
<p class="art-p">The institutional story: departure files are full of short and interim spells, not a catalog of decades-long reigns.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2021-04-27 (departures.csv). After cleaning, 9,423 rows remain.</p>
<p class="art-p">Max tenure ceodb is the primary ranked metric. Interim/co-CEO spelling variants appear as separate categories and reflect label noise as well as structure. Charts are Plotly JSON with PNG fallbacks.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2021). <em>TidyTuesday: CEO Departures</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-04-27/departures.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-04-27/departures.csv</a></p>
</section>
</main>
</div>
