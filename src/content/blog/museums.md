---
title: "MUSEUMS: UK Cluster in Less-Deprived Areas"
slug: museums
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  4,191 UK museums mapped to area deprivation: median 5.00, maximum 10.0, with South West England showing 3-point admin-area gaps.
dek: "Britain's museums are not spread evenly across rich and poor neighborhoods."
heroImage: /images/content/articles/museums/hero.png
draft: false
tags:
  - arts
  - architecture
subject: Museums
tldr: >-
  4,191 UK museums sit at a median area deprivation index of 5.00, with an observed maximum of 10.0. Blenheim Palace anchors the top-name fact box. Inside South West England, Wiltshire scores 2.00 points above the median while Cornwall trails 1.00 point below.
keyPoints:
  - 4,191 — Museums in the working dataset, merged from TidyTuesday 2022-11-22 tables
  - 5.00 — Median area deprivation index, the file's geographic midpoint
  - 10.0 — Maximum observed deprivation score, shared by The Archaeology Centre and Smithy Heritage Centre
  - 2.00 points — Wiltshire's lead over median; Cornwall trails by 1.00 in the same region
  - /England/South West — Most common admin area, hosting the widest intra-region deprivation spread
faq:
  - question: How many UK museums are in this dataset?
    answer: 4,191 records from the TidyTuesday 2022-11-22 release after table merges.
  - question: What is the median deprivation index for UK museum locations?
    answer: 5.00 on the area deprivation scale.
  - question: Which museum scores highest on area deprivation?
    answer: The Archaeology Centre at 10.0, tied with Smithy Heritage Centre and others at the observed maximum.
  - question: Do museums concentrate in wealthier areas?
    answer: Distribution spreads across deprivation bands; South West England alone shows 3-point admin-area gaps.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">4,191 UK museums sit at a median area deprivation index of 5.00, with an observed maximum of 10.0 and a 3-point spread inside South West England alone — evidence that cultural institutions map onto place inequality in measurable, uneven patterns.</p>
<p class="art-p">Area deprivation describes the surrounding community context, not museum quality. The question is how collections sit on that scale: whether they cluster in less-deprived bands, and how named sites and admin areas compare to the 5.00 median.</p>

<h2 id="named-museums-pin-the-top-of-the-deprivation-scale" class="anchored">Named museums pin the top of the deprivation scale</h2>
<h3 id="named-museums-pin-the-top-of-the-deprivation-scale-look" class="anchored">Area Deprivation index by Name of museum</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/museums/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/museums/charts/chart1_breakdown.png" role="img" aria-label="Area Deprivation index by Name of museum"></div>
</figure>
<p class="art-p">The Archaeology Centre leads at 10.0; Smithy Heritage Centre also hits 10.0. Multiple sites share the observed maximum — a reminder that the upper slice compresses when many institutions cluster at the same index band. Grouping by museum name makes individual institutions visible on the deprivation axis. This is a catalog of places, not a visitor-numbers league table.</p>
<h2 id="the-leaders-chart-sits-at-the-index-ceiling" class="anchored">The leaders chart sits at the index ceiling</h2>
<h3 id="the-leaders-chart-sits-at-the-index-ceiling-look" class="anchored">Top Name of museum</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/museums/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/museums/charts/chart2_leaders.png" role="img" aria-label="Top Name of museum"></div>
</figure>
<p class="art-p">The Archaeology Centre leads at 10.0, and 10.0 marks the median among the top dozen in this cut. When the top is flat, the story is saturation at the high end of the deprivation index rather than a single runaway institution. Blenheim Palace remains a fact-box landmark; the charted leaders emphasize which names hit the 10.0 maximum in this aggregation.</p>
<h2 id="admin-areas-spread-museums-across-different-deprivation-bands" class="anchored">Admin areas spread museums across different deprivation bands</h2>
<h3 id="admin-areas-spread-museums-across-different-deprivation-bands-look" class="anchored">Area Deprivation index by Admin area</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/museums/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/museums/charts/chart3_distribution.png" role="img" aria-label="Area Deprivation index by Admin area"></div>
</figure>
<p class="art-p">Category boxes by admin area show whether deprivation bands are shared or contested across local jurisdictions. Museums do not all sit in the same band; geography fragments the index. The spread matters: cultural infrastructure is unevenly distributed across deprivation contexts, and the boxes make the pattern visible.</p>
<h2 id="wiltshire-clears-the-median-cornwall-trails-in-the-south-west-cut" class="anchored">Wiltshire clears the median; Cornwall trails in the South West cut</h2>
<h3 id="wiltshire-clears-the-median-cornwall-trails-in-the-south-west-cut-look" class="anchored">Area Deprivation index vs median by Admin area</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/museums/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/museums/charts/chart4_gap.png" role="img" aria-label="Area Deprivation index vs median by Admin area"></div>
</figure>
<p class="art-p">/England/South West (English Region)/Wiltshire (English UA) sits 2.00 above the median; /England/South West (English Region)/Cornwall (English UA) trails by 1.00. Even inside one English region, admin areas do not share the same offset from the file center. Signed gaps turn geography into comparable scale. They do not explain why a museum is where it is; they locate area context relative to the 5.00 median deprivation index.</p>
<h2 id="deprivation-and-domus-ids-form-a-joint-map" class="anchored">Deprivation and DOMUS IDs form a joint map</h2>
<h3 id="deprivation-and-domus-ids-form-a-joint-map-look" class="anchored">Area Deprivation index vs DOMUS identifier</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/museums/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/museums/charts/chart5_scatter.png" role="img" aria-label="Area Deprivation index vs DOMUS identifier"></div>
</figure>
<p class="art-p">Plotting area deprivation index against DOMUS identifier shows clusters a single average erases. Identifier ranges and deprivation bands co-locate in ways that matter for joining and auditing the catalog. The scatter is a data-structure check as much as a social map: it shows how the numeric deprivation field sits beside the museum identity field in the 4,191-row extract.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">TidyTuesday snapshots are community-cleaned extracts, not live heritage registries. Missing values, naming variants, and week-of-export coverage limits apply. Merged tables may duplicate rows when join keys are imperfect.</p>
<p class="art-p">Area deprivation index describes place context in the source file. Findings are structural signals about UK museums in this extract — not a verdict on institutional excellence or funding.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">UK museums in this file sit around a median deprivation index of 5.00, with an observed maximum of 10.0 and clear admin-area gaps even inside the South West. Wiltshire leads the median by 2.00; Cornwall trails by 1.00 — a 3-point spread within one region.</p>
<p class="art-p">Name leaders, area boxes, and the deprivation–DOMUS scatter together show how cultural sites map onto inequality of place — a geography story first, a prestige story only by implication.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">Source: TidyTuesday release 2022-11-22 (R for Data Science community). The working file contains 4,191 rows and 35 columns after merging available tables in the week folder. Area deprivation index is the primary metric; museum name and admin area are the categorical axes; DOMUS identifier appears in the scatter plot.</p>
<p class="art-p">Medians are used for robustness. Deprivation scores describe surrounding area context in the source, not museum quality or visitor volume.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2022). <em>TidyTuesday: UK Museums</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2022/2022-11-22/museums.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2022/2022-11-22/museums.csv</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2022/2022-11-22" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
