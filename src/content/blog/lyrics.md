---
title: "LYRICS: Beyoncé and Taylor Swift Line by Line"
slug: lyrics
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  A lyric-level comparison of two era-defining catalogs—theme, language, and
  structure.
dek: "What happens when you read Beyoncé and Taylor Swift line by line?"
heroImage: /images/content/articles/lyrics/hero.png
draft: false
tags:
  - arts
  - music
subject: Beyoncé
tldr: >-
  Two catalogs define a generation of pop authorship. Line-level lyric tables
  make it possible to compare them the way a critic compares albums — by
  recurring titles, repeated lines, and how densely each artist’s words fill the
  extract. The working file holds 22,616 records.
keyPoints:
  - '22,616 — Records in the working dataset'
  - Beyoncé — Most common Artist name
faq:
  - question: >-
      How many records are in this dataset?
    answer: >-
      22,616 records in the working dataset.
  - question: >-
      What is Most common Artist name?
    answer: >-
      Beyoncé — Most common Artist name.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Two catalogs define a generation of pop authorship. Line-level lyric tables make it possible to compare them the way a critic compares albums — by recurring titles, repeated lines, and how densely each artist’s words fill the extract.</p>
<p class="art-p">The working file holds <strong>22,616</strong> records. Beyoncé is the most common artist name in the rows on hand — a reminder to read every chart as a view of this extract’s balance, not as a claim that one career is larger than the other in absolute terms.</p>

<h2 id="landscape" class="anchored">Landscape</h2>
<h3 id="landscape-look" class="anchored">Beyoncé dominates with 22,616 records</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lyrics/charts/chart1_category.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lyrics/charts/chart1_category.png" role="img" aria-label="Beyoncé dominates with 22,616 records"></div>
</figure>
<p class="art-p">Beyoncé dominates with 22,616 records in the category view of this extract. The main bucket carries the story; the field does not show a meaningful long-tail split of artist labels once the file is filtered as published. Treat that dominance as a coverage fact about the working table — which lines were included — before treating it as a comparative verdict on two careers.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Top Song name</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lyrics/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lyrics/charts/chart2_leaders.png" role="img" aria-label="Top Song name"></div>
</figure>
<p class="art-p">Lemonade Film (Script) appears 336 times — the most recurring song-name entity in the file. The top dozen account for a visible share of all 22,616 rows. Long scripts and multi-part projects generate more line rows than a three-minute single. Recurrence at the top is often a document-length effect as much as a “favorite song” effect.</p>
<h2 id="category" class="anchored">Category</h2>
<h3 id="category-look" class="anchored">Beyoncé is the largest bucket with 22,616 records</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lyrics/charts/chart3_category.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lyrics/charts/chart3_category.png" role="img" aria-label="Beyoncé is the largest bucket with 22,616 records"></div>
</figure>
<p class="art-p">Beyoncé is the largest bucket with 22,616 records. Category concentration shows where editorial attention should focus first when reading the extract. If the file is Beyoncé-heavy by construction, every later frequency claim inherits that imbalance. Fair comparison starts by stating the row share out loud.</p>
<h2 id="frequency" class="anchored">Frequency</h2>
<h3 id="frequency-look" class="anchored">Most song name entities appear only once; a small head revisits repeatedly</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lyrics/charts/chart5_frequency.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lyrics/charts/chart5_frequency.png" role="img" aria-label="Most song name entities appear only once; a small head revisits repeatedly"></div>
</figure>
<p class="art-p">Most song-name entities appear only once; a small head revisits repeatedly. That power-law shape is typical of lyric catalogs, guest lists, and credit tables: a long tail of unique titles, a short head of projects that keep generating lines.</p>
<h2 id="mix" class="anchored">Mix</h2>
<h3 id="mix-look" class="anchored">If I let you go is the most repeated line in the extract</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lyrics/charts/chart_extra_mix.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lyrics/charts/chart_extra_mix.png" role="img" aria-label="If I let you go is the most repeated line in the extract"></div>
</figure>
<p class="art-p">“If I let you go” is the most repeated line in the extract — a refrain-level recurrence that secondary dimensions surface when the primary table has no numeric score column. Repeated lines are the lyric equivalent of a hook chart: they show what the text keeps returning to, not which song sold the most.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and week-of-export coverage limits apply. Merged tables may fan out or duplicate rows when join keys are imperfect.</p>
<p class="art-p">Findings describe the file on hand — structural signals about lyric rows for Beyoncé and Taylor Swift in this extract, not a complete linguistic theory of either catalog.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Line-by-line tables make authorship countable: 22,616 rows, a Beyoncé-heavy artist share in this extract, Lemonade Film (Script) at 336 appearances, and “If I let you go” as the most repeated line. Frequency and mix answer different questions than sales or streams.</p>
<p class="art-p">Use the charts to see coverage and recurrence — then check how the extract was built before treating any refrain as a career-wide signature.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2020-09-29 (R for Data Science community). The working file contains 22,616 rows and 6 columns after merging available tables in the week folder.</p>
<p class="art-p">Rows are lyric lines and related identifiers — song names, artist labels, and text fields — not audio features. Charts export as Plotly JSON with PNG fallbacks. Frequency and mix plots matter because the primary table has no single numeric “quality” score.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2020). <em>TidyTuesday: Beyoncé & Taylor Swift Lyrics</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-09-29/beyonce_lyrics.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-09-29/beyonce_lyrics.csv</a></p>
</section>
</main>
</div>
