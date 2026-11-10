---
title: 'CALORIES: Fast Food''s 2,430-Calorie Ceiling'
slug: calories
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: '515 U.S. calories menu items show a median of 490 calories — top 12 items median 1,315; Sonic sits 80 above median, Chick-fil-A 100 below.'
heroImage: /images/content/articles/calories/hero.png
draft: false
tags:
  - culture
  - food
subject: Fast Food
tldr: '515 calories menu items from major U.S. chains show a median of 490 calories. The heaviest item — a 20-piece buttermilk crispy chicken tray — reaches 2,430 calories. The top 12 items median 1,315 calories, 2.7× the dataset median. Sonic sits 80 calories above median; Chick-fil-A trails by 100.'
keyPoints:
  - 515 — Items in dataset span major U.S. chains from 2018 TidyTuesday snapshot
  - '490 — Median calories across all items; top 12 items median 1,315 (2.7× higher)'
  - '2,430 — 20-piece buttermilk crispy chicken tender tray leads all items'
  - 80 — Sonic's calorie gap above median; Chick-fil-A trails median by 100
  - '1,510 — 12-piece tender tray sits mid-tier; portion size drives calorie spread'
faq:
  - question: What is the median calorie count for calories menu items?
    answer: 490 calories across 515 items from major U.S. chains in the 2018 TidyTuesday dataset.
  - question: Which calories item has the most calories?
    answer: 'A 20-piece buttermilk crispy chicken tender tray at 2,430 calories.'
  - question: How do chain calorie averages compare to the median?
    answer: Sonic sits 80 calories above median; Chick-fil-A trails by 100 calories.
  - question: Do calories and fat track together across items?
    answer: Yes — high-calorie items cluster with high fat in the upper-right of the scatter plot.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">515 menu items from major U.S. calories chains show a median of 490 calories, but the top tier — shareable trays and stacked sandwiches — reaches 2,430 calories, nearly five times higher.</p>
<p class="art-p">The dataset, from TidyTuesday's 2018-09-04 release, records restaurant name, item, calories, total fat, and related nutrition fields. Taco Bell appears most often in the file, but frequency does not equal intensity. The signal is in which items and chains sit above the median and how portion size drives the calorie ceiling.</p>
<p class="art-p">Chain averages without portion context mis-rank brands that sell both modest sandwiches and extreme trays under the same logo. Catalog comparisons are more useful than chain-level means.</p>

<h2 id="breakdown" class="anchored">Calorie ceilings by item</h2>
<h3 id="breakdown-look" class="anchored">Calories by Item</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/calories/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/calories/charts/chart1_breakdown.png" role="img" aria-label="Calories by Item"></div>
</figure>
<p class="art-p">The 20-piece buttermilk crispy chicken tender tray leads at 2,430 calories. Related tender trays populate the upper tier: the 12-piece sits near 1,510, the 10-piece near 1,210. Portion size drives the ceiling. Doubling the piece count nearly doubles the calorie load. Burger King and Sonic doubles — Farmhouse King, Rodeo King, Super Sonic doubles — fill the same high band for a different reason: stacked patties, sauces, and bun mass rather than tray size.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">20-piece Buttermilk Crispy Chicken Tenders leads at 2,430 — 1,315 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/calories/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/calories/charts/chart2_leaders.png" role="img" aria-label="20-piece Buttermilk Crispy Chicken Tenders leads at 2,430 — 1,315 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Among the top 12 calorie items, the median is 1,315 — more than 2.5 times the dataset-wide median of 490. The head of the menu is not a gentle slope; it is a separate altitude. Shareable trays and king-style sandwiches dominate the list. Chain averages without portion context will mis-rank brands that sell both modest sandwiches and extreme trays under the same logo.</p>
<h2 id="how-the-field-is-spread" class="anchored">How chains spread calories</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Calories by Restaurant</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/calories/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/calories/charts/chart3_distribution.png" role="img" aria-label="Calories by Restaurant"></div>
</figure>
<p class="art-p">Box plots by restaurant show whether a chain's calorie consensus is shared or contested. Some menus cluster tightly around the middle. Others stretch from light sides to extreme trays, producing wide interquartile ranges that averages erase. Taco Bell's heavy representation in the file does not place it at the caloric peak. Volume of SKUs and intensity of SKUs are different questions — the distribution chart is where that split becomes visible.</p>
<h2 id="who-beats-the-median-and-who-trails" class="anchored">Who beats the median — and who trails</h2>
<h3 id="who-beats-the-median-and-who-trails-look" class="anchored">Calories vs median by Restaurant</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/calories/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/calories/charts/chart4_gap.png" role="img" aria-label="Calories vs median by Restaurant"></div>
</figure>
<p class="art-p">Relative to the dataset median, Sonic sits 80 calories above center. Chick-fil-A trails by 100. Burger King, Arby's, and McDonald's sit on the high side of the gap chart; Subway and Taco Bell sit below. These gaps are menu-composition effects as much as health branding. A chain that lists more grilled items and fewer shareable trays will land below the median even if its signature sandwich is not light. The gap chart ranks catalogs, not single hero products.</p>
<h2 id="what-moves-together" class="anchored">Calories and fat move together</h2>
<h3 id="what-moves-together-look" class="anchored">Calories vs Total fat</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/calories/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/calories/charts/chart5_scatter.png" role="img" aria-label="Calories vs Total fat"></div>
</figure>
<p class="art-p">Plotting calories against total fat produces the expected positive slope — and the clusters that averages erase. Dense clumps of ordinary sandwiches sit in the middle; extreme trays and stacked burgers occupy the upper-right corner where both axes spike together. Fat is not a perfect proxy for calories, but in this menu file the two metrics rarely disagree about which items are extreme. When they do separate, it is usually because sugar-heavy drinks or desserts pull calories without matching fat.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and week-of-export coverage limits apply. Merged tables may fan out or duplicate rows when join keys are imperfect.</p>
<p class="art-p">The file does not measure how often items are ordered, how portions are actually consumed, or how recipes have changed since the 2018 release. Treat the numbers as a structural map of listed menu calories — not a verdict on every current drive-through board.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The median calories item in this catalog sits near 490 calories. The items that define the public argument about fast food often sit two to five times higher — trays and stacked sandwiches that are easy to order and hard to compare without portion context.</p>
<p class="art-p">Chain gaps of 80 to 100 calories around the median are real, but they are catalog effects. The clearest signal is the ceiling: once shareable chicken trays enter the frame, the conversation about a typical item and the conversation about the heaviest item are no longer the same conversation.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p"><a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2018/2018-09-04">The source is the TidyTuesday release from 2018-09-04, maintained by the R for Data Science community. The working file contains 515 rows and 17 columns after merging available CSV tables — restaurant name, item, calories, total fat, and related nutrition fields.</a></p>
<p class="art-p">Medians are preferred where distributions skew. Index-style fields and sequential IDs are excluded from metric selection. Charts ship as Plotly JSON with PNG fallbacks. The snapshot is a menu catalog for a fixed release window, not a live API.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
</section>
</main>
</div>
