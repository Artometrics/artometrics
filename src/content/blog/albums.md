---
title: 'ALBUMS: Rolling Stone''s 2003 Canon, Rank by Rank'
slug: albums
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'The 2003 Rolling Stone list puts median rank at 250; "Touch" sits at 500, studio albums dominate, and 1955–2019 releases populate the canon.'
heroImage: /images/content/articles/albums/hero.png
draft: false
tags:
  - arts
  - music
subject: Albums
tldr: 'Rolling Stone''s 2003 greatest-albums list contains 691 records with a median rank of 250. "Touch" leads the numeric rank field at 500, studio albums dominate the type distribution, and release years span 1955–2019. The list is an editorial artifact — a frozen moment of taste presented as permanent infrastructure.'
keyPoints:
  - 691 — Records in the working dataset — the full scope of this TidyTuesday extract
  - 250 — Median 2003 rank — the midpoint of the canonical numbering system
  - 500 — Highest observed 2003 rank — "Touch" sits at the numeric edge of the list
  - 1955–2019 — Release-year span — six decades of albums frozen in a 2003 ranking
  - Studio — Most common album type — the format Rolling Stone's canon privileges
faq:
  - question: How many albums are in the dataset?
    answer: 691 records from the TidyTuesday Rolling Stone extract.
  - question: What is the median 2003 rank?
    answer: 250 — the midpoint of the ranked list.
  - question: Which album has the highest numeric rank?
    answer: '"Touch" at 500, the far edge of the list''s numbering.'
  - question: What album type dominates the canon?
    answer: Studio albums — the format historically privileged by rock criticism.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Rolling Stone's 2003 greatest-albums list contains 691 records with a median rank of 250, and "Touch" sits at 500 — the numeric edge of a canon that spans 1955–2019 and privileges studio albums over all other formats.</p>
<p class="art-p">The list is an editorial artifact. It freezes taste at a moment, then presents that freeze as permanent infrastructure. The working file shows how the freeze distributes: median rank at <strong>250</strong>, highest observed rank at <strong>500</strong>, studio albums as the default type, and a six-decade release span that carries albums from mid-century to the cusp of streaming.</p>
<p class="art-p">Rank numbers run inverse to prestige — lower is better — but the charts below follow the file's stated leaders and medians without imposing a second scoring system.</p>

<h2 id="how-the-pattern-changed-over-time" class="anchored">How ranks sit across release years</h2>
<h3 id="how-the-pattern-changed-over-time-look" class="anchored">Median Rank 2003 Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/albums/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/albums/charts/chart1_trend.png" role="img" aria-label="Median Rank 2003 Over Time"></div>
</figure>
<p class="art-p">Median 2003 rank across release years shows which eras the list favored when the ranking was locked. Mid-century and classic-rock decades sit differently from later indie and hip-hop entries — a fingerprint of the canon's compositional politics. The rank field is anchored in 2003, so later release years in the file mark albums added after the original freeze or coverage quirks in the TidyTuesday extract.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top of the numeric rank field</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Touch leads at 500 — 494 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/albums/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/albums/charts/chart2_leaders.png" role="img" aria-label="Touch leads at 500 — 494 marks the median among the top dozen"></div>
</figure>
<p class="art-p"><strong>Touch</strong> leads at <strong>500</strong>, with <strong>494</strong> as the median among the top dozen in this ordering. The upper numeric band clusters albums near the far end of the 2003 list's numbering. Nearby titles — Guitar Town, Entertainment!, All the Young Dudes, Vitalogy, She's So Unusual — show how the list's lower prestige tier remains a hall of fame by ordinary standards. Being near 500 on a Rolling Stone 500 is not obscurity.</p>
<h2 id="how-the-field-is-spread" class="anchored">Ranks by album type</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Rank 2003 by Type</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/albums/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/albums/charts/chart3_distribution.png" role="img" aria-label="Rank 2003 by Type"></div>
</figure>
<p class="art-p">Box plots by type show whether rank consensus is shared or contested across release formats. Studio albums dominate because rock-critical canons historically privileged them over compilations, live records, and other forms. Type concentration is an editorial fingerprint. A canon that underweights non-studio formats makes an aesthetic argument, not a neutral count of what exists.</p>
<h2 id="who-beats-the-median-and-who-trails" class="anchored">Who beats the median — and who trails</h2>
<h3 id="who-beats-the-median-and-who-trails-look" class="anchored">Rank 2003 vs median by Type</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/albums/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/albums/charts/chart4_gap.png" role="img" aria-label="Rank 2003 vs median by Type"></div>
</figure>
<p class="art-p">The gap chart ranks types above or below the median 2003 rank. Differences encode which formats the list treated as central versus peripheral when the ranking was composed. The entire file is already an elite list, so trailing the median still means membership in a magazine's chosen 500 — a narrow world compared with all recorded music.</p>
<h2 id="what-moves-together" class="anchored">Rank and artist age</h2>
<h3 id="what-moves-together-look" class="anchored">Rank 2003 vs Ave age at top 500</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/albums/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/albums/charts/chart5_scatter.png" role="img" aria-label="Rank 2003 vs Ave age at top 500"></div>
</figure>
<p class="art-p">Plotting 2003 rank against average age at the top-500 marker shows clusters that averages erase. Some high-prestige albums come from young breakthrough artists; others from later-career peaks. The scatter refuses a single myth about youth and canonization. Age is not destiny on a critical list, but it is a recurring covariate in rock historiography. The cloud shows variation that simplistic narratives hide.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and list-version mismatches apply. A 2003 rank is not a 2020s streaming share, and Rolling Stone's taste is not the world's taste.</p>
<p class="art-p">Findings describe structural signals about one magazine canon's metadata — not a universal ranking of recorded music, and not a substitute for listening.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Rolling Stone's 2003 album canon contains 691 rows with a median rank of 250, studio albums as the dominant type, and a numeric range that runs to 500. The file encodes genre and generation politics: canons freeze taste at a moment, then teach that freeze as permanent.</p>
<p class="art-p">The charts make the freeze measurable — the rest is interpretation.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p"><a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2024/2024-05-07">The source is the TidyTuesday Rolling Stone albums release from the R for Data Science community. The working file contains 691 rows — album titles, artists, release years, types, genre labels, and 2003 rank fields.</a></p>
<p class="art-p">Medians summarize a curated elite, not a random sample of recorded music. Charts export as Plotly JSON with PNG fallbacks. A magazine canon is an editorial object; treating it as market data misreads the politics of taste.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
</section>
</main>
</div>
