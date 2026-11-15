---
title: 'BROADWAY: Springsteen on Broadway Doubled Hamilton''s Average Ticket Price'
slug: broadway
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: Springsteen On Broadway averages $509 per ticket—nearly double Hamilton's $273. Concert residencies occupy the summit; traditional musicals cluster near the $60 industry median.
dek: "Hamilton's tickets cost a fortune. One show charged nearly twice as much."
heroImage: /images/content/articles/broadway/hero.png
draft: false
tags:
  - arts
  - theater
subject: Broadway
tldr: 'Broadway divides into two pricing tiers: long-running musicals cluster near a $60.2 median, while concert residencies push toward $509. Springsteen On Broadway leads the 47,524-record TidyTuesday dataset; Hamilton follows at $273.'
keyPoints:
  - '47,524 — Records in the TidyTuesday grosses dataset, establishing the full working sample'
  - '$60.2 — Median average ticket price across all shows, defining Broadway''s baseline'
  - '$509 — Springsteen On Broadway average ticket price, nearly double Hamilton''s $273'
  - '$182 — Median among the top dozen most expensive shows, marking the premium club threshold'
  - 'Broadhurst Theatre — Most frequently recorded venue, with 1,829 performance records'
faq:
  - question: What is the average ticket price for Springsteen On Broadway?
    answer: 'Springsteen On Broadway averages $509 per ticket, the highest in the 47,524-record dataset.'
  - question: How does Hamilton's ticket price compare to Springsteen?
    answer: 'Hamilton averages $273 per ticket—extraordinary versus the $60.2 industry median, yet still 46% below Springsteen''s $509.'
  - question: What is the median ticket price on Broadway?
    answer: 'The median average ticket price across all 47,524 records is $60.2.'
  - question: Which theater appears most often in Broadway grosses data?
    answer: 'Broadhurst Theatre, with 1,829 performance records in the dataset.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Springsteen On Broadway averages $509 per ticket—nearly double Hamilton's $273 and more than eight times the $60.2 industry median. This gap separates concert-style residencies from long-running musicals and reveals two parallel pricing markets operating inside the same theater district.</p>
<p class="art-p">The TidyTuesday grosses dataset holds 47,524 performance records. Broadhurst Theatre appears most frequently; Springsteen On Broadway claims the highest average ticket price. The data map a clear division: established houses run near stable mid-range prices, while event residencies reset the ceiling.</p>

<h2 id="concert-residencies-rewrite-the-price-ceiling" class="anchored">Concert Residencies Rewrite the Price Ceiling</h2>
<h3 id="concert-residencies-rewrite-the-price-ceiling-look" class="anchored">Avg ticket price by Show</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/broadway/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/broadway/charts/chart1_breakdown.png" role="img" aria-label="Avg ticket price by Show"></div>
</figure>
<p class="art-p">Springsteen On Broadway leads at $508.63 average ticket price—nearly double Hamilton's $273. Dave Chappelle Live, Moulin Rouge!, Mel Brooks on Broadway, Morrissey, and David Byrne's American Utopia follow in the premium band above $175. Concert-style residencies occupy the top tier. Traditional musicals, regardless of critical success, cluster far below the residency model.</p>
<h2 id="even-among-leaders-springsteen-is-an-outlier" class="anchored">Even Among Leaders, Springsteen Is an Outlier</h2>
<h3 id="even-among-leaders-springsteen-is-an-outlier-look" class="anchored">Springsteen On Broadway leads at 509 — 182 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/broadway/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/broadway/charts/chart2_leaders.png" role="img" aria-label="Springsteen On Broadway leads at 509 — 182 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Springsteen On Broadway stands at $509, while the median among the top dozen is $182. Hamilton is extraordinary relative to the $60.2 industry median—yet still 46% below the Springsteen residency. Reference $182 as the premium Broadway median; reference $509 when discussing absolute event-ticket pricing.</p>
<h2 id="house-medians-cluster-near-the-industry-middle" class="anchored">House Medians Cluster Near the Industry Middle</h2>
<h3 id="house-medians-cluster-near-the-industry-middle-look" class="anchored">Avg ticket price by Theatre</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/broadway/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/broadway/charts/chart3_distribution.png" role="img" aria-label="Avg ticket price by Theatre"></div>
</figure>
<p class="art-p">Broadhurst Theatre (n=1,829) shows a median average ticket near $77; Minskoff near $77; Majestic near $60; Ambassador near $66; Imperial near $48. Peak prices within those houses still exceed $100 when hit shows run. Theatre identity matters less than show identity. The same building can host a $50 median season and a $200 event week.</p>
<h2 id="gershwin-leads-the-gap-above-the-median" class="anchored">Gershwin Leads the Gap Above the Median</h2>
<h3 id="gershwin-leads-the-gap-above-the-median-look" class="anchored">Avg ticket price vs median by Theatre</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/broadway/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/broadway/charts/chart4_gap.png" role="img" aria-label="Avg ticket price vs median by Theatre"></div>
</figure>
<p class="art-p">Relative to the overall $60.2 average-ticket median, Gershwin Theatre leads at +$27.67, with Broadhurst and Minskoff also positive. Imperial sits below the median by $12. House premiums track programming: theaters hosting mega-hits and premium brands pull above the baseline.</p>
<h2 id="price-and-performance-counts-are-weakly-coupled" class="anchored">Price and Performance Counts Are Weakly Coupled</h2>
<h3 id="price-and-performance-counts-are-weakly-coupled-look" class="anchored">Avg ticket price vs Performances</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/broadway/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/broadway/charts/chart5_scatter.png" role="img" aria-label="Avg ticket price vs Performances"></div>
</figure>
<p class="art-p">Average ticket price versus performances shows low-price, low-performance weeks and occasional high-price short runs. Long runs at moderate prices remain the traditional musical model. The scatter resists a simple correlation: expensive tickets do not always signal short runs, and longevity does not require discounting. Broadway monetizes both scarcity and stamina.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Grosses data include atypical weeks, previews, and dark periods sometimes coded as zeros. Average ticket price does not reflect face value for every seat. Concert residencies mix genres inside a Broadway dataset.</p>
<p class="art-p">The snapshot timing predates later reopenings and dynamic pricing expansion.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Broadway's median average ticket in this dataset is $60.2, while event residencies reach $509. The top-dozen median of $182 defines the premium club without equating to the Springsteen outlier.</p>
<p class="art-p">Reference house medians when comparing venues; reference show leaders when comparing brands.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2020-04-28 (grosses.csv). After cleaning, 47,524 records remain for analysis.</p>
<p class="art-p">Average ticket price is the primary metric; theatre and show fields provide the grouping. Charts are Plotly JSON with PNG fallbacks.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2020). <em>TidyTuesday: Broadway Musicals</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-04-28/grosses.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-04-28/grosses.csv</a></p>
</section>
</main>
</div>
