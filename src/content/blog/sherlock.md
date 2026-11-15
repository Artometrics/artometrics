---
title: "SHERLOCK: Twelve Words per Tokenized Record"
slug: sherlock
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: Tokenized Holmes corpus from TidyTuesday shows median 12.0 words, mean 10.9, with top five titles holding 34% of aggregate count.
dek: "We broke the Sherlock Holmes stories into 65,958 pieces. No single book runs away with it."
heroImage: /images/content/articles/sherlock/hero.png
draft: false
tags:
  - arts
  - language
subject: Sherlock
tldr: >-
  A tokenized Sherlock Holmes corpus of 65,958 records shows a median word count of 12.0 and mean of 10.9—a near-symmetric distribution. The top five book entries account for 34% of total word count, while the leading title, The Yellow Face, reaches only 13.0, barely above the file-wide median.
keyPoints:
  - '65,958 — Records in tokenized corpus — each row represents one text unit, not a complete story'
  - '12.0 — Median word count — identical to the median among the top twelve titles'
  - '34% — Share held by top five books — modest concentration with no runaway leader'
faq:
  - question: What does word count measure in this dataset?
    answer: >-
      Word count is a field in the tokenized corpus, not total story length; each of 65,958 records represents a text segment.
  - question: Which story has the highest word count?
    answer: >-
      The Yellow Face leads at 13.0 words per record, one word above the corpus median of 12.0.
  - question: How concentrated is the corpus across books?
    answer: >-
      The top five books hold 34% of aggregate word count; the remainder distributes across a long tail of titles.
  - question: Is the distribution skewed?
    answer: >-
      Median 12.0 and mean 10.9 indicate near symmetry with minimal right skew.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">The tokenized Sherlock Holmes corpus from TidyTuesday contains 65,958 records with a median word count of 12.0 and a mean of 10.9—evidence of a nearly symmetric distribution. The top-ranked title, The Yellow Face, reaches 13.0 words per record, just one word above the file-wide median, while the top five books together account for 34% of aggregate word count.</p>
<p class="art-p">The Adventure of the Beryl Coronet appears as the top-ranked book by word count in the fact box; The Yellow Face leads the charted breakdown at 13.0. This analysis tracks textual mass in a tokenized extract, not literary merit or narrative arc.</p>

<h2 id="story-level-medians-sit-in-a-narrow-band" class="anchored">Story-level medians sit in a narrow band</h2>
<h3 id="story-level-medians-sit-in-a-narrow-band-look" class="anchored">Word count by Book</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/sherlock/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/sherlock/charts/chart1_breakdown.png" role="img" aria-label="Word count by Book"></div>
</figure>
<p class="art-p">The Yellow Face leads at 13.0 words per record; A Case of Identity anchors the low end at 12.0. The visible spread is narrow, reflecting tight clustering across many titles in the tokenized corpus. Grouping by book exposes length variation across the catalog without requiring plot summaries. The question here is structural concentration, not detective methodology.</p>
<h2 id="even-the-leaders-barely-clear-the-file-median" class="anchored">Even the leaders barely clear the file median</h2>
<h3 id="even-the-leaders-barely-clear-the-file-median-look" class="anchored">The Yellow Face leads at 13.0 — 12.0 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/sherlock/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/sherlock/charts/chart2_leaders.png" role="img" aria-label="The Yellow Face leads at 13.0 — 12.0 marks the median among the top dozen"></div>
</figure>
<p class="art-p">The Yellow Face leads at 13.0, while the median among the top twelve is 12.0—identical to the file-wide median. Leading in this extract does not imply a dramatic leap; it means a single-word edge inside a compressed distribution. That compression is the finding. Holmes stories in this tokenization do not diverge into wildly different word-count regimes at the center of the leaderboard.</p>
<h2 id="median-12-0-mean-10-9-a-mostly-symmetric-shape" class="anchored">Median 12.0, mean 10.9 — a mostly symmetric shape</h2>
<h3 id="median-12-0-mean-10-9-a-mostly-symmetric-shape-look" class="anchored">Word count Distribution</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/sherlock/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/sherlock/charts/chart3_distribution.png" role="img" aria-label="Word count Distribution"></div>
</figure>
<p class="art-p">The full-sample distribution shows median 12.0 and mean 10.9—near symmetry rather than heavy right skew. The top decile begins at 14.0; that upper slice contains the longer textual segments in this metric. Symmetry matters for citation. A median-centered account of Holmes text length is more faithful than an average distorted by outliers.</p>
<h2 id="five-books-account-for-a-third-of-aggregate-word-count" class="anchored">Five books account for a third of aggregate word count</h2>
<h3 id="five-books-account-for-a-third-of-aggregate-word-count-look" class="anchored">Cumulative Word count</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/sherlock/charts/chart4_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/sherlock/charts/chart4_pareto.png" role="img" aria-label="Cumulative Word count"></div>
</figure>
<p class="art-p">The top five book entries account for 34% of aggregate word count. Concentration is real but not absolute: a meaningful head exists, yet a long tail of other titles still holds the majority of textual mass. This concentration curve means editorial attention can begin with a small set of books without ignoring the rest of the canon.</p>
<h2 id="a-second-concentration-cut-confirms-the-same-head" class="anchored">A second concentration cut confirms the same head</h2>
<h3 id="a-second-concentration-cut-confirms-the-same-head-look" class="anchored">Cumulative Word count</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/sherlock/charts/chart_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/sherlock/charts/chart_pareto.png" role="img" aria-label="Cumulative Word count"></div>
</figure>
<p class="art-p">A second cumulative chart repeats the concentration view: the top five book entries again account for 34% of aggregate word count. Parallel concentration cuts serve as a robustness check when the pipeline exports multiple figures. The takeaway holds. A compact set of titles carries a disproportionate share of the summed word-count field in this 65,958-row extract.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">TidyTuesday snapshots are community-cleaned teaching datasets, not live literary APIs. Tokenization choices, spelling variants in titles, and week-of-export coverage limits apply. Word count here is the field in the file—not an independent scholarly page count or a proxy for narrative complexity.</p>
<p class="art-p">Findings describe this extract. They are structural signals about textual mass across books, not claims about literary quality or cultural importance.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The tokenized Holmes corpus centers tightly: median word count 12.0, mean 10.9, top decile from 14.0, and leaders such as The Yellow Face only one word above the median.</p>
<p class="art-p">Concentration is modest—the top five books hold 34% of aggregate word count—but no single title dominates. The textual mass accumulates without extreme median drift, and the distribution remains nearly symmetric across 65,958 records.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2025-11-18, published by the R for Data Science community. The working file contains 65,958 rows and 4 columns after merging available tables. Book titles serve as the primary categorical axis; word count is the primary numeric metric.</p>
<p class="art-p">Medians are used because text-length fields can skew. The distribution here shows median 12.0 and mean 10.9, indicating relative symmetry. Index-style fields are excluded from metric selection.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2025). <em>TidyTuesday: Sherlock Holmes</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-11-18/holmes.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-11-18/holmes.csv</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-11-18" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
