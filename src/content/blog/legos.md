---
title: 'LEGOS: LEGO Sets Shrank to 60 Pieces as Flagships Hit 11,695'
slug: legos
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Median part counts dropped from 142 to 59.5 as World Map and display sets pushed the complexity ceiling past 11,000 pieces.'
heroImage: /images/content/articles/legos/hero.png
draft: false
tags:
  - culture
  - leisure
subject: Lego
tldr: 'The Rebrickable dataset covering 1949–2022 shows a catalog split: median part counts fell from 142 to 59.5 while flagship builds like World Map reached 11,695 pieces. The typical set became smaller as LEGO introduced a new tier of adult display architecture.'
keyPoints:
  - '11,695 — World Map part count — highest in the dataset, seventeen times the top-twelve median of 5,792'
  - 59.5 — Median part count by 2022 — down from 142 in the opening period despite rising flagship complexity
  - 34 — File-wide median — reveals that most sets remain small even as outliers push into five digits
faq:
  - question: How many LEGO sets are in the dataset?
    answer: '19,798 records spanning 1949–2022 after merging set and parts tables.'
  - question: What is the most complex LEGO set by part count?
    answer: 'World Map at 11,695 parts leads the ranking in this extract.'
  - question: Did LEGO sets get simpler over time?
    answer: 'Median part counts fell from 142 to 59.5, but the top tier grew into multi-thousand-piece display builds.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">The Rebrickable dataset covering 1949–2022 shows a catalog split: median part counts fell from 142 to 59.5 while flagship builds like World Map reached 11,695 pieces. The typical set became smaller as LEGO introduced a new tier of adult display architecture.</p>
<p class="art-p">World Map leads at 11,695 parts — the median among the top twelve is 5,792, still 170 times the file-wide median of 34. The drop in median counts does not signal declining complexity; it signals catalog segmentation. LEGO produces more small sets for everyday buyers while reserving ultra-high part counts for adult collectors willing to treat brick builds as furniture-scale architecture.</p>
<p class="art-p">Part count is an industrial signal, not a quality measure. It tracks how much plastic inventory a box commits and how the company balances volume production against showcase releases.</p>

<h2 id="how-the-pattern-changed-over-time" class="anchored">How part counts changed over time</h2>
<h3 id="how-the-pattern-changed-over-time-look" class="anchored">Median Num parts Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/legos/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/legos/charts/chart1_trend.png" role="img" aria-label="Median Num parts Over Time"></div>
</figure>
<p class="art-p">Median part counts fell from 142 in the opening period to 59.5 at the close. LEGO did not abandon complexity — the typical catalog entry became smaller even as a new class of ultra-large display sets appeared at the extreme. A falling median beside a rising ceiling is a catalog split: more small sets for everyday buyers and a thinner tier of destination builds for adults and collectors.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">World Map leads at 11,695 — 5,792 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/legos/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/legos/charts/chart2_leaders.png" role="img" aria-label="World Map leads at 11,695 — 5,792 marks the median among the top dozen"></div>
</figure>
<p class="art-p">World Map leads at 11,695 parts. The median among the top dozen is 5,792 — still orders of magnitude above the file-wide median of 34. NINJAGO City, Hogwarts Express Collectors' Edition, stadium sets, Taj Mahal, Colosseum, and Titanic populate the same high-complexity band. These are not children's starter boxes. They are furniture-scale plastic architecture sold under a toy brand, and the part counts make that product shift quantitative.</p>
<h2 id="how-the-field-is-spread" class="anchored">How the field is spread</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Num parts Distribution</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/legos/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/legos/charts/chart3_distribution.png" role="img" aria-label="Num parts Distribution"></div>
</figure>
<p class="art-p">The distribution is sharply right-skewed: median 34 versus mean 161. The top decile begins near 432 parts. Most sets are modest; a long right tail carries the Instagram-era display pieces. Quoting the mean as the typical LEGO set describes a more complex object than most boxes on the shelf. The median is the honest center; the tail is the brand's adult collector strategy made visible.</p>
<h2 id="leader-trends" class="anchored">Leader trends</h2>
<h3 id="leader-trends-look" class="anchored">Top Name Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/legos/charts/chart4_leader_trends.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/legos/charts/chart4_leader_trends.png" role="img" aria-label="Top Name Over Time"></div>
</figure>
<p class="art-p">The leading names do not move in lockstep. Some franchise icons fade as others surge; licensed themes and modular city sets take turns occupying the complexity frontier. Tracking leaders over time separates sustained flagship lines from one-off mosaic promotions. Both matter commercially; only the sustained lines reshape what LEGO means as a cultural object.</p>
<h2 id="what-moves-together" class="anchored">Parts and quantity</h2>
<h3 id="what-moves-together-look" class="anchored">Num parts vs Quantity</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/legos/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/legos/charts/chart5_scatter.png" role="img" aria-label="Num parts vs Quantity"></div>
</figure>
<p class="art-p">Plotting number of parts against quantity fields shows clusters that averages erase. Some rows describe unique large sets; others describe common small parts used in volume across many builds. The scatter reminds that the database mixes set-level and parts-level grains depending on the joined table. Complexity at the box level and repetition at the brick level are related industrial facts, not the same metric.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and release coverage limits apply. Part counts are not prices, and set names can recur across regions or reissues.</p>
<p class="art-p">Findings describe structural signals about LEGO catalog complexity — not a full financial history of the company or a ranking of which sets are best to build.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">LEGO's catalog is two products sharing one logo: a dense middle of small sets around a few dozen parts and a thin upper tier of multi-thousand-piece display builds that redefine the brand's adult market.</p>
<p class="art-p">The citable tension is the falling median beside the extreme ceiling. Everyday LEGO became smaller in the typical case even as the largest boxes became architectural.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p"><a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2022/2022-09-06">The source is the TidyTuesday release from 2022-09-06 (R for Data Science community). The working file contains 19,798 rows across set and parts tables after merging — set names, years, part counts, and quantity fields.</a></p>
<p class="art-p">Medians are reported because a few architectural and mosaic sets pull means upward. Charts export as Plotly JSON with PNG fallbacks. Part counts describe inventory complexity, not retail price or build time.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
</section>
</main>
</div>
