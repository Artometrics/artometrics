---
title: 'RADIO: News/Talk Lives on AM While FM Clusters at 101 MHz'
slug: radio
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: '17,186 station records show Country owns format share while News/Talk owns the upper AM band — frequency and culture answer different questions.'
heroImage: /images/content/articles/radio/hero.png
draft: false
tags:
  - arts
  - music
subject: Radio
tldr: '17,186 U.S. radio station records from TidyTuesday reveal a median frequency of 101 MHz, a high of 1,700 kHz on AM, and Country as the most common format. News/Talk stations sit 1,039 above the median because of their historic AM placement — spectrum physics and format culture tell separate stories about the same dial.'
keyPoints:
  - '17,186 — Station records in the dataset — full U.S. license snapshot from TidyTuesday 2022-11-08'
  - 101 MHz — Median frequency — FM center of gravity for the working file
  - '1,039 kHz — News/Talk elevation above median — heavy AM presence pulls the format into a different band'
  - '34% — Top five call signs'' share of aggregate frequency — concentration reflects dial extremes, not audience'
  - Country — Most common format label — leads station count but not necessarily upper-band placement
faq:
  - question: What is the median frequency for U.S. radio stations in this dataset?
    answer: 'The median frequency is 101 MHz, reflecting FM-band clustering across 17,186 records.'
  - question: Why does News/Talk sit so far above the median?
    answer: 'News/Talk stations concentrate on AM frequencies, pulling their distribution 1,039 kHz above the FM-centered median of 101.'
  - question: Does frequency distribution predict audience share?
    answer: 'No — frequency is spectrum physics, not ratings; format share and dial position answer separate questions.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">17,186 U.S. radio station records from TidyTuesday's 2022-11-08 release show a median frequency of 101 MHz, a high of 1,700 kHz on AM, and Country as the most common format — yet News/Talk stations sit 1,039 kHz above the median because of their historic AM placement.</p>
<p class="art-p">The station license table is a spectrum map, not a ratings book. Call sign WEUP leads the frequency ranking, Country leads format share, and the top five call signs account for 34% of aggregate frequency — a concentration artifact that reflects dial extremes rather than audience consolidation.</p>
<p class="art-p">Frequency and format answer different questions: one measures where stations sit on the electromagnetic spectrum, the other describes what they broadcast.</p>

<h2 id="breakdown" class="anchored">Frequency by call sign</h2>
<h3 id="breakdown-look" class="anchored">Frequency by Call sign</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/radio/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/radio/charts/chart1_breakdown.png" role="img" aria-label="Frequency by Call sign"></div>
</figure>
<p class="art-p">WJCC appears near 1,700 kHz at the high end of the call-sign frequency cut, with neighbors such as KGED near 1,680 kHz. These are upper-AM coordinates, not audience-size claims. Grouping by call sign exposes how the metric varies across licensed identities — a map of where stations sit on the spectrum, not which morning shows win their cities.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Top Call sign</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/radio/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/radio/charts/chart2_leaders.png" role="img" aria-label="Top Call sign"></div>
</figure>
<p class="art-p">WJCC leads at 1,700 kHz, with 1,695 kHz as the median among the top dozen. The entire top band is a tight cluster of high-AM assignments. The finding is the tightness itself: the top of frequency is a narrow technical neighborhood, while format diversity lives on a different axis.</p>
<h2 id="how-the-field-is-spread" class="anchored">Frequency by format</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Frequency by Format</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/radio/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/radio/charts/chart3_distribution.png" role="img" aria-label="Frequency by Format"></div>
</figure>
<p class="art-p">Box plots by format — Country, News/Talk, Sports, Classic Hits, and related labels — show whether frequency consensus is shared or contested across programming types. Country leads station count but does not automatically own the highest dial positions. Format is culture; frequency is spectrum. Confusing the two produces false stories about which genres rule the airwaves.</p>
<h2 id="who-beats-the-median-and-who-trails" class="anchored">Who beats the median — and who trails</h2>
<h3 id="who-beats-the-median-and-who-trails-look" class="anchored">Frequency vs median by Format</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/radio/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/radio/charts/chart4_gap.png" role="img" aria-label="Frequency vs median by Format"></div>
</figure>
<p class="art-p">News/Talk sits 1,039 kHz above the median; Contemporary Christian trails by about 9. News/Talk's elevation reflects its heavy presence on AM frequencies far above the FM-centered median of 101 MHz. The gap is a band-plan story as much as a format story. Talk radio's historic AM home pulls its frequency distribution into a different universe from music formats clustered on FM.</p>
<h2 id="concentration" class="anchored">Concentration on the dial</h2>
<h3 id="concentration-look" class="anchored">The top 5 call sign entries account for 34% of the aggregate frequency</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/radio/charts/chart_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/radio/charts/chart_pareto.png" role="img" aria-label="The top 5 call sign entries account for 34% of the aggregate frequency"></div>
</figure>
<p class="art-p">The top five call-sign entries account for 34% of aggregate frequency in the working cut — a concentration statistic that reflects how large the highest dial numbers are relative to the median, not a claim that five stations own a third of listening. Summing dial positions is not the same as summing audiences. Pareto-on-frequency is a reminder that spectrum physics and market share are separate metrics.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and license-status quirks apply. Frequency is not listenership, and format labels can be stale or contested.</p>
<p class="art-p">Findings describe structural signals about U.S. radio station metadata — not a ratings analysis, and not a complete history of every translator and HD multicast.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The U.S. radio dial in this file centers at 101 MHz with AM extremes near 1,700 kHz, Country as the most common format, and News/Talk pulled high by AM band placement.</p>
<p class="art-p">The citable split is spectrum versus culture: call-sign frequency leaders and format share leaders answer different questions about the same airwaves.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p"><a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2022/2022-11-08">The source is the TidyTuesday release from 2022-11-08, maintained by the R for Data Science community. The working file contains 17,186 rows and 11 columns after cleaning — call signs, frequencies, formats, and license status fields.</a></p>
<p class="art-p">Medians stabilize a dial that mixes FM-looking centers with AM extremes. Charts export as Plotly JSON with PNG fallbacks. Each license row represents permission to exist on the dial, not a measure of listening.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
</section>
</main>
</div>
