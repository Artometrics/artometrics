---
title: "STEAM: Ten Hours per Dollar Owns the Shelf"
slug: steam
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  26,688 Steam titles show critic scores rising from 70 to 73 between 2004–2018 while million-owner games beat the median by 10 points.
dek: "Games with a million owners beat the median critic score by ten points. Is hours per dollar the reason?"
heroImage: /images/content/articles/steam/hero.png
draft: false
tags:
  - sports
  - gaming
subject: Steam
tldr: >-
  26,688 Steam titles logged between 2004–2018 show median Metascore rising from 70.0 to 73.0. Games with 2–5 million owners score 10 points above the catalog median, while the smallest ownership tier trails by 5 points. Little Triangle leads at 98.0.
keyPoints:
  - '26,688 — Titles in Steam Spy extract spanning 2004–2018'
  - '73.0 — Median Metascore, rising from 70.0 at period open'
  - '98.0 — Peak Metascore held by Little Triangle'
  - '+10.0 — Score advantage for 2–5 million owner tier above catalog median'
  - '0–20,000 — Most common ownership band in the dataset'
faq:
  - question: >-
      Which Steam game scored highest in this dataset?
    answer: >-
      Little Triangle leads at 98.0 Metascore.
  - question: >-
      How did median critic score change from 2004 to 2018?
    answer: >-
      Median Metascore rose from 70.0 to 73.0 across the period.
  - question: >-
      Do games with more owners score higher?
    answer: >-
      The 2–5 million owner tier sits 10 points above the catalog median; smallest-owner games trail by 5 points.
  - question: >-
      How many games are in the Steam Spy extract?
    answer: >-
      26,688 titles with Metascore, price, and owner data.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Median critic score for Steam titles rose from 70.0 in 2004 to 73.0 by 2018, while games with 2–5 million owners scored 10 points above the catalog median and the smallest-owner tier trailed by 5 points, according to 26,688 titles logged in the Steam Spy extract.</p>
<p class="art-p">Metascore tracks critical consensus; owner tiers measure commercial reach. The catalog median of 73.0 divides the critically strong from the ordinary. Little Triangle leads at 98.0.</p>

<h2 id="median-metascore-edged-up-across-the-store-s-expansion-years" class="anchored">Median Metascore edged up across the store's expansion years</h2>
<h3 id="median-metascore-edged-up-across-the-store-s-expansion-years-look" class="anchored">Median Metascore Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/steam/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/steam/charts/chart1_trend.png" role="img" aria-label="Median Metascore Over Time"></div>
</figure>
<p class="art-p">Median Metascore rose from 70.0 at period open to 73.0 at close — landing on the catalog median. The typical scored game ended the window three points higher than it began. A rising median reflects stronger releases, expanded critic coverage of titles receiving scores, or both.</p>

<h2 id="little-triangle-tops-a-tightly-packed-critical-elite" class="anchored">Little Triangle tops a tightly packed critical elite</h2>
<h3 id="little-triangle-tops-a-tightly-packed-critical-elite-look" class="anchored">Little Triangle leads at 98.0 — 95.5 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/steam/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/steam/charts/chart2_leaders.png" role="img" aria-label="Little Triangle leads at 98.0 — 95.5 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Little Triangle leads at 98.0, while 95.5 marks the median among the top dozen. The elite band compresses near the ceiling — high scores clustered together rather than a lonely outlier. DEEP SPACE WAIFU: NEKOMIMI also appears among notable titles in the ranking rules used in fact boxes.</p>

<h2 id="owner-tiers-carry-different-metascore-distributions" class="anchored">Owner tiers carry different Metascore distributions</h2>
<h3 id="owner-tiers-carry-different-metascore-distributions-look" class="anchored">Metascore by Owners</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/steam/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/steam/charts/chart3_distribution.png" role="img" aria-label="Metascore by Owners"></div>
</figure>
<p class="art-p">Games with millions of owners are not the same statistical population as the 0–20,000 band that dominates row counts. Boxes show whether Metascore consensus is shared or contested across popularity bands. Volume in the smallest owner bucket is a catalog fact; the boxes reveal how scores spread inside each ownership tier.</p>

<h2 id="mid-million-owner-games-clear-the-median-tiny-audiences-trail" class="anchored">Mid-million owner games clear the median; tiny audiences trail</h2>
<h3 id="mid-million-owner-games-clear-the-median-tiny-audiences-trail-look" class="anchored">Metascore vs median by Owners</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/steam/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/steam/charts/chart4_gap.png" role="img" aria-label="Metascore vs median by Owners"></div>
</figure>
<p class="art-p">The 2,000,000–5,000,000 owners band sits 10.0 above the median; the 0–20,000 band trails by 5.00. Broader ownership tiers sit higher on Metascore relative to the catalog center than the sparsest shelf. That gap is an association, not proof that owners cause scores — but it is a citable structural pattern.</p>

<h2 id="metascore-and-price-form-a-joint-market-map" class="anchored">Metascore and price form a joint market map</h2>
<h3 id="metascore-and-price-form-a-joint-market-map-look" class="anchored">Metascore vs Price</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/steam/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/steam/charts/chart5_scatter.png" role="img" aria-label="Metascore vs Price"></div>
</figure>
<p class="art-p">Plotting Metascore against price shows clusters that averages erase — cheap high scores, expensive middling scores, and every bargain or premium pattern between. The scatter answers the storefront question: what combinations of critic score and sticker price actually appear in the 26,688-row extract.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">TidyTuesday snapshots are not live Steam or Metacritic APIs. Missing Metascores, owner-band binning, price currency assumptions, and 2004–2018 coverage limits apply. Findings describe this Steam Spy extract — structural signals about Metascore, owners, and price — not a complete quality ranking of every game ever shipped.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Median Metascore rose from 70.0 to 73.0 across the 2004–2018 window; Little Triangle leads at 98.0. Games with 2–5 million owners sit 10 points above the catalog median, while the smallest ownership tier trails by 5 points. Metascore–price clusters show how critic standing and sticker price co-occur on the shelf.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2019-07-30 (R for Data Science community). The working file contains 26,688 rows and 11 columns after merging available tables. Metascore is the primary metric; owners is the categorical size axis; price appears in the scatter. Medians are used because scores and prices both skew.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2019). <em>TidyTuesday: Video Games Steam Spy</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-07-30/video_games.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-07-30/video_games.csv</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-07-30" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
