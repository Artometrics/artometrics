---
title: "NOVELS: Victorian Authors Own the Christmas Canon"
slug: novels
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  A Gutenberg holiday corpus shows a median author birthdate of 1859 and Dickens as the most common name.
dek: "Christmas fiction on Project Gutenberg is a Victorian club, with Dickens at the door."
heroImage: /images/content/articles/novels/hero.png
draft: false
tags:
  - arts
  - language
subject: Christmas
tldr: >-
  The TidyTuesday Christmas-novel extract holds 35 records with a median author birthdate of 1859 and a latest birthdate of 1891. Charles Dickens is the most common author label. The shelf is Victorian-centered: industrial-era childhood, Christian seasonal ritual, serialized storytelling.
keyPoints:
  - 35 — Dataset size — a curated canon, not a market census
  - 1859 — Median author birthdate — Victorian and immediately post-Victorian writers anchor the shelf
  - 1891 — Latest observed birthdate — even the "late" edge is still nineteenth-century
  - Dickens, Charles — Most common author — canon gravity pulls toward earlier births
  - 1970 — Year span covered — single-year Gutenberg snapshot
faq:
  - question: How many records are in this dataset?
    answer: 35 records after cleaning.
  - question: What is the median author birthdate?
    answer: 1859, placing the shelf's center in the Victorian era.
  - question: Which author appears most often?
    answer: Charles Dickens is the most common author label in the file.
  - question: Does this dataset cover modern Christmas romances?
    answer: No — the latest birthdate is 1891, so modern holiday romances are mostly absent.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">The median author birthdate in this 35-record Christmas-novel extract is 1859, the latest is 1891, and Charles Dickens is the most common name. The shelf is Victorian-centered: Dickensian ghosts, children's mysteries, parlor sentimentalism.</p>
<p class="art-p">Because the sample is tiny, every chart maps a curated canon rather than a complete market. Birthdate becomes a proxy for which literary generations stock the holiday shelf.</p>

<h2 id="the-shelf-centers-on-mid-nineteenth-century-births" class="anchored">The Shelf Centers on Mid-Nineteenth-Century Births</h2>
<h3 id="the-shelf-centers-on-mid-nineteenth-century-births-look" class="anchored">Median Birthdate Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/novels/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/novels/charts/chart1_trend.png" role="img" aria-label="Median Birthdate Over Time"></div>
</figure>
<p class="art-p">The median birthdate is 1859 — Victorian and immediately post-Victorian authors anchor the holiday novel list. That center of gravity explains the tone of the canon: industrial-era childhood, Christian seasonal ritual, and serialized storytelling habits.</p>
<h2 id="later-born-titles-mark-the-edge-of-the-canon" class="anchored">Later-Born Titles Mark the Edge of the Canon</h2>
<h3 id="later-born-titles-mark-the-edge-of-the-canon-look" class="anchored">The Camp Fire Girls Solve a Mystery; Or, The Christmas Adventure at Carver House leads at 1,891 — 1,872 marks the median among the...</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/novels/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/novels/charts/chart2_leaders.png" role="img" aria-label="The Camp Fire Girls Solve a Mystery; Or, The Christmas Adventure at Carver House leads at 1,891 — 1,872 marks the median among the..."></div>
</figure>
<p class="art-p">The Camp Fire Girls Solve a Mystery; Or, The Christmas Adventure at Carver House leads at birthdate 1891. Other later births include Uncle Noah's Christmas Inspiration (1884) and Christmas Outside of Eden (1883). The median among the top dozen by birthdate is about 1872. Even the "late" edge of this shelf is still nineteenth-century. Modern holiday romances are mostly outside this particular extract.</p>
<h2 id="birthdates-cluster-around-the-1860s" class="anchored">Birthdates Cluster Around the 1860s</h2>
<h3 id="birthdates-cluster-around-the-1860s-look" class="anchored">Median 1,859 vs mean 1,849 — the shape is relatively symmetric</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/novels/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/novels/charts/chart3_distribution.png" role="img" aria-label="Median 1,859 vs mean 1,849 — the shape is relatively symmetric"></div>
</figure>
<p class="art-p">The distribution piles several authors near the early 1860s bins, with smaller counts in earlier nineteenth-century bands. Mean birthdate (approximately 1849) sits close to the median, producing a relatively symmetric distribution for such a small n. With only 35 rows, bin heights are fragile — but the Victorian concentration is robust enough to cite.</p>
<h2 id="dickens-and-thackeray-sit-earlier-than-the-median" class="anchored">Dickens and Thackeray Sit Earlier Than the Median</h2>
<h3 id="dickens-and-thackeray-sit-earlier-than-the-median-look" class="anchored">Birthdate vs median by Author</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/novels/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/novels/charts/chart4_gap.png" role="img" aria-label="Birthdate vs median by Author"></div>
</figure>
<p class="art-p">Author gaps to the median birthdate show Rupert Hughes furthest above (+13), while Dickens (−47) and Thackeray (−48) sit well earlier. Louisa May Alcott is also clearly before the median (−27). The holiday shelf's most famous names are often older than the shelf's statistical middle — canon gravity pulling toward earlier births.</p>
<h2 id="birth-and-death-dates-trace-finite-author-lives" class="anchored">Birth and Death Dates Trace Finite Author Lives</h2>
<h3 id="birth-and-death-dates-trace-finite-author-lives-look" class="anchored">Birthdate vs Deathdate</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/novels/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/novels/charts/chart5_scatter.png" role="img" aria-label="Birthdate vs Deathdate"></div>
</figure>
<p class="art-p">Birthdate versus deathdate for 32 plotted authors follows the expected upward diagonal: later-born authors die later, with points stretching from early-nineteenth-century pairs into mid-twentieth-century deaths. The scatter is a mortality timeline for a seasonal literature, not a sales chart — useful for placing which generations could still be writing when Christmas publishing industrialized.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">n=35 is a teaching canon, not a market census. Missing modern titles and non-English traditions are structural absences. Birthdate as a ranking metric is biographical, not a measure of holiday popularity.</p>
<p class="art-p">Author name authority control may still split or merge identities in a small file.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">This Christmas-novel shelf is a Victorian-centered canon: median birthdate 1859, latest 1891, with Dickens as the recurring name.</p>
<p class="art-p">Cite the small n alongside any ranking. The value is literary geography — which generations stock the holiday imagination — not a bestseller index.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2025-12-30 (christmas_novels.csv). After cleaning, 35 rows remain.</p>
<p class="art-p">Author birthdate is the primary numeric metric in this chart stack; deathdate appears in the joint plot. Charts are Plotly JSON with PNG fallbacks.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2025). <em>TidyTuesday: Christmas Novels</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-12-30/christmas_novels.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-12-30/christmas_novels.csv</a></p>
</section>
</main>
</div>
