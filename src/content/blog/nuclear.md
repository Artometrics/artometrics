---
title: 'NUCLEAR: Nuclear Test Magnitudes Peaked at 7.40 Across 2,051 Detonations'
slug: nuclear
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: Public seismic catalogs reveal a median magnitude of 0.00—mostly missing data—while maximum recorded yields reached 7.40.
heroImage: /images/content/articles/nuclear/hero.png
draft: false
tags:
  - science
  - physics
subject: Nuclear
tldr: 'Public nuclear test catalogs record 2,051 detonations with a median body-wave magnitude of 0.00—driven by missing measurements—and a maximum of 7.40. The USSR leads by aggregate magnitude, weapons-related tests (WR) dominate purpose codes, and the dataset''s year-span artifact collapses to 1970 in summary fields.'
keyPoints:
  - '2,051 — Detonation records in TidyTuesday working file — most lack magnitude data'
  - '0.00 — Median body-wave magnitude — reflects measurement gaps, not low-yield dominance'
  - 7.40 — Maximum recorded magnitude — upper tail captures seismically loudest events
  - USSR — Highest aggregate magnitude by country — not equivalent to total test count
  - WR — Weapons-related purpose code — most frequent test category in catalog
  - '1970 — Year-span artifact in summary fields — read timelines as event clock, not complete history'
faq:
  - question: Why is the median magnitude zero?
    answer: 'Most events lack filled magnitude values due to incomplete instrumentation or classified data; zeros represent missing measurements, not silent detonations.'
  - question: Which country tested at the highest recorded magnitude?
    answer: The USSR leads by aggregate body-wave magnitude in this extract; individual event maxima and total test counts follow different rankings.
  - question: What does the WR purpose code mean?
    answer: WR marks weapons-related tests; other codes include peaceful nuclear explosions and research detonations with different policy implications.
  - question: Does the 1970 year span mean all tests occurred in one year?
    answer: No—the 1970 collapse is a summary-field artifact; actual event dates span decades but compress in some aggregations.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Public seismology catalogs of nuclear tests record 2,051 detonations with a median body-wave magnitude of 0.00—not because devices were quiet, but because most events lack filled magnitude values—and a maximum of 7.40, marking the upper tail of instrumentally detectable yields.</p>
<p class="art-p">A TidyTuesday working extract shows the <strong>USSR</strong> leads by aggregate magnitude, <strong>WR</strong> (weapons-related) dominates purpose codes, and the year-span artifact collapses to <strong>1970</strong> in summary fields—read timelines as the file's available event clock, not a claim that all testing concentrated in a single year. The <strong>7.40</strong> maximum captures the seismically loudest events that shook global instruments; the <strong>0.00</strong> median reflects structural missingness, not a physics finding.</p>
<p class="art-p">Zeros in the magnitude field mark measurement gaps, non-detections, or unfilled cells—diplomatic secrecy and uneven seismic coverage both shape what enters the public record.</p>

<h2 id="how-the-pattern-changed-over-time" class="anchored">How magnitudes move through the record</h2>
<h3 id="how-the-pattern-changed-over-time-look" class="anchored">Median Magnitude body Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/nuclear/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/nuclear/charts/chart1_trend.png" role="img" aria-label="Median Magnitude body Over Time"></div>
</figure>
<p class="art-p">The time chart of median body-wave magnitude tracks how the typical recorded event sits across the file's date spine. Periods with denser instrumentation and more reported yields diverge from periods dominated by missing magnitude cells. The curve traces what entered the public measurement record, not a complete energy ledger of every device—diplomatic moratoria and underground testing both reshape what seismology detects.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">INDIA leads at 5.00 — 2.50 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/nuclear/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/nuclear/charts/chart2_leaders.png" role="img" aria-label="INDIA leads at 5.00 — 2.50 marks the median among the top dozen"></div>
</figure>
<p class="art-p">On the highlighted leader cut, <strong>INDIA</strong> leads at <strong>5.00</strong>, with <strong>2.50</strong> as the median among the top dozen country entries. Related state labels in the broader ranking—USSR, China, Pakistan, France, USA, UK—confirm that the nuclear club is small and that magnitude leadership in a cleaned table reflects which events were well measured as much as which states tested most often. The USSR's fact-box lead by magnitude body and India's lead on this chart can both be true under different aggregations—always name the cut before converting a bar into a hierarchy of arsenals.</p>
<h2 id="how-the-field-is-spread" class="anchored">Purpose spreads magnitudes</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Magnitude body by Purpose</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/nuclear/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/nuclear/charts/chart3_distribution.png" role="img" aria-label="Magnitude body by Purpose"></div>
</figure>
<p class="art-p">Box plots by purpose code show whether magnitude distributions are shared or contested across test categories. <strong>WR</strong> dominates headcount as the most common purpose label; other purpose codes may rank higher or lower on intensity even with fewer rows. Purpose codes encode political grammar: weapons-related tests, peaceful nuclear explosion labels, and related categories are not interchangeable events even when they share explosive physics.</p>
<h2 id="who-beats-the-median-and-who-trails" class="anchored">Who beats the median — and who trails</h2>
<h3 id="who-beats-the-median-and-who-trails-look" class="anchored">Magnitude body vs median by Purpose</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/nuclear/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/nuclear/charts/chart4_gap.png" role="img" aria-label="Magnitude body vs median by Purpose"></div>
</figure>
<p class="art-p">The gap chart ranks purpose categories above or below the magnitude median. Categories that beat the median concentrate the instrumentally loud events; categories that trail are either genuinely smaller or more missingness-heavy. Because the file-wide median is 0.00, almost any filled magnitude will sit above the mathematical center—that is a data-structure warning as much as a physics finding.</p>
<h2 id="what-moves-together" class="anchored">Magnitude and depth</h2>
<h3 id="what-moves-together-look" class="anchored">Magnitude body vs Depth</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/nuclear/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/nuclear/charts/chart5_scatter.png" role="img" aria-label="Magnitude body vs Depth"></div>
</figure>
<p class="art-p">Plotting body-wave magnitude against depth reveals clusters that averages erase. Atmospheric and surface events occupy different depth regimes from underground tests; the scatter separates testing modes that country labels alone cannot distinguish. Depth is not a perfect proxy for political intent, but it is one of the cleanest engineering signatures in the archive—combined with magnitude, it separates theater from concealment more clearly than country labels alone.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and incomplete yield reporting apply. A median magnitude of 0.00 is a missingness signal as much as a physical one.</p>
<p class="art-p">Findings describe structural signals in the public nuclear-test table—not a classified inventory, not a health study, and not a complete history of every device.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The nuclear test archive in this file is a skewed measurement story: 2,051 records, a median body-wave magnitude at zero because of gaps, and a thin upper tail that reaches 7.40.</p>
<p class="art-p">A small set of states dominates the known record, and the record itself is shaped by what seismology and disclosure were willing to make countable.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p"><a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-08-20">The source is the TidyTuesday nuclear explosions release maintained by the R for Data Science community. The working file assembles event-level rows with country labels, purpose codes, body-wave magnitude, depth, and related fields after cleaning.</a></p>
<p class="art-p">Medians anchor the analysis because missing and zero magnitudes dominate the center of the distribution. Charts export as Plotly JSON with PNG fallbacks. Public test catalogs are incomplete by design—secrecy and uneven seismology limit coverage.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
</section>
</main>
</div>
