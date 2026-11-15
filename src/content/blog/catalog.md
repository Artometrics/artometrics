---
title: 'CATALOG: Netflix''s Movie-Heavy Catalog Hid Its Longest Titles in Interactives'
slug: catalog
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Black Mirror: Bandersnatch hit 312 minutes; median duration rose from 41 to 98 minutes between 2008 and 2021 as the catalog skewed longer.'
dek: "Netflix's longest title runs 312 minutes, and you choose how it ends."
heroImage: /images/content/articles/catalog/hero.png
draft: false
tags:
  - arts
  - film
subject: Netflix
tldr: 'Netflix catalog data from 2008 to 2021 show median duration climbed from 41 to 98 minutes while movies outnumbered TV shows. Black Mirror: Bandersnatch led at 312 minutes, and the top five titles accounted for 38% of aggregate duration—a steep concentration curve beneath the homepage''s long tail.'
keyPoints:
  - '7,787 — Catalog records spanning 2008–2021'
  - 41 to 98 minutes — Median duration rose 139% across the period
  - '312 minutes — Black Mirror: Bandersnatch, the longest single title'
  - 38% — Share of total duration held by the top five titles
  - Movie — Most common type label in the catalog
faq:
  - question: How many Netflix titles are in the dataset?
    answer: '7,787 records spanning 2008 to 2021.'
  - question: What was the longest title on Netflix in this data?
    answer: 'Black Mirror: Bandersnatch at 312 minutes.'
  - question: How concentrated is Netflix's duration inventory?
    answer: The top five titles account for 38% of aggregate duration.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Median duration in Netflix's catalog rose from 41 minutes in 2008 to 98 minutes by 2021—a 139% climb driven by longer films, multi-season TV encodings, and interactive outliers like Black Mirror: Bandersnatch, which clocked 312 minutes.</p>
<p class="art-p">The working file holds <strong>7,787</strong> records. Median duration is <strong>88.0</strong>; the highest observed duration is <strong>312</strong>, led by Black Mirror: Bandersnatch. Movie is the most common type label.</p>

<h2 id="how-the-pattern-changed-over-time" class="anchored">How the pattern changed over time</h2>
<h3 id="how-the-pattern-changed-over-time-look" class="anchored">Median Duration Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/catalog/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/catalog/charts/chart1_trend.png" role="img" aria-label="Median Duration Over Time"></div>
</figure>
<p class="art-p">Median duration rises from 41.0 in the opening period to 98.0 at the close—a catalog whose typical row lengthens as the library ages. That climb reflects more feature-length films, longer TV season encodings, or both. The trend is a mix signal, not a single format story.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Black Mirror: Bandersnatch leads at 312 — 226 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/catalog/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/catalog/charts/chart2_leaders.png" role="img" aria-label="Black Mirror: Bandersnatch leads at 312 — 226 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Black Mirror: Bandersnatch leads at 312; 226 marks the median among the top dozen. Interactive and long-form outliers define the ceiling. Most of the library lives nowhere near those peaks—which is why the median of 88.0 remains the better everyday calibration.</p>
<h2 id="how-the-field-is-spread" class="anchored">How the field is spread</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Duration by Type</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/catalog/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/catalog/charts/chart3_distribution.png" role="img" aria-label="Duration by Type"></div>
</figure>
<p class="art-p">Duration by type separates movies from TV rows in the catalog encoding. The boxes show whether each type shares a tight middle or stretches into long tails. Movie dominance in count does not guarantee movie dominance in duration shape. The distribution is where that distinction becomes visible.</p>
<h2 id="concentration" class="anchored">Concentration</h2>
<h3 id="concentration-look" class="anchored">The top 5 title entries account for 38% of the aggregate duration</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/catalog/charts/chart4_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/catalog/charts/chart4_pareto.png" role="img" aria-label="The top 5 title entries account for 38% of the aggregate duration"></div>
</figure>
<p class="art-p">The top 5 title entries account for 38% of the aggregate duration—a steep head for a library that otherwise looks vast on the homepage. Steep Pareto curves mean a small set of rows drives most of the summed duration signal. The long tail is real inventory; it is not where the aggregate concentrates.</p>
<h2 id="concentration-pareto" class="anchored">Concentration</h2>
<h3 id="concentration-pareto-look" class="anchored">The top 5 title entries account for 38% of the aggregate duration</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/catalog/charts/chart_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/catalog/charts/chart_pareto.png" role="img" aria-label="The top 5 title entries account for 38% of the aggregate duration"></div>
</figure>
<p class="art-p">A second Pareto view of the same 38% concentration confirms the head–tail split under an alternate chart export. When two exhibits agree on the same share, the claim is about structure in the file—not a rendering choice.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and week-of-export coverage limits apply. Merged tables may fan out or duplicate rows when join keys are imperfect.</p>
<p class="art-p">Findings describe the file on hand—structural signals about Netflix title rows through 2021, not today's live catalog in every territory.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Median duration climbed from 41.0 to 98.0 while Movie remained the most common type. A handful of long outliers—Bandersnatch at 312 among them—and a 38% duration concentration in the top five rows show how uneven a "library" can be once you stop counting titles and start summing length.</p>
<p class="art-p">Use the charts to separate mix, length, and concentration before treating any homepage as a flat shelf.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2021-04-20 (R for Data Science community). The working file contains 7,787 rows and 13 columns after merging available tables in the week folder.</p>
<p class="art-p">Duration represents catalog metadata as published—minutes for films, season counts for TV rows where the export encodes type that way. Medians and Plotly exports absorb skew and missing cells without distortion.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2021). <em>TidyTuesday: Netflix Titles</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-04-20/netflix_titles.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-04-20/netflix_titles.csv</a></p>
</section>
</main>
</div>
