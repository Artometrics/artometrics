---
title: 'WASTEWATER: Singapore''s Wastewater Plants Discharge 200× the Global Norm'
slug: wastewater
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Facility-level data show median discharge at 1,079 m³/day; Singapore''s plants average 223,683.'
heroImage: /images/content/articles/wastewater/hero.png
draft: false
tags:
  - science
  - engineering
subject: Water
tldr: 'Median wastewater discharge across 58,502 facilities is 1,079 m³/day; Singapore''s plants average 223,683, while one U.S. facility exceeds 3 million. Secondary treatment dominates headcount, but advanced plants run 681 m³/day above the median—a mix of technology tier and urban scale.'
keyPoints:
  - '58,502 — Facilities logged in the TidyTuesday extract, covering operational and proposed plants worldwide'
  - '1,079 — Median discharge in m³/day; the top recorded plant exceeds 3 million'
  - '223,683 — Singapore''s average plant discharge, 207× the global median and highest among recorded countries'
  - 'Secondary — Most common treatment level by facility count, but advanced plants average 681 m³/day above median'
  - 'United States — Leads total aggregate discharge due to reporting volume, not per-plant intensity'
faq:
  - question: What is the median wastewater discharge per plant?
    answer: 'The median is 1,079 m³/day across 58,502 facilities in the extract.'
  - question: Which country has the highest average plant discharge?
    answer: 'Singapore, at 223,683 m³/day—far above the global median.'
  - question: Does advanced treatment mean higher discharge?
    answer: 'Advanced plants run 681 m³/day above the median, reflecting larger urban facilities, not just cleaner technology.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Median wastewater discharge across 58,502 facilities is 1,079 m³/day; Singapore's plants average 223,683, while one U.S. facility exceeds 3 million—a 2,800× spread that maps density, infrastructure investment, and the uneven geography of treatment reporting.</p>
<p class="art-p">The TidyTuesday extract from September 2022 covers <strong>58,502</strong> plants worldwide. Median waste discharge (<strong>WASTE DIS</strong>) is <strong>1,079</strong> m³/day; the maximum exceeds <strong>3,073,754</strong>. The United States leads aggregate discharge due to reporting volume, while <strong>Secondary</strong> treatment is the most common level label by count.</p>
<p class="art-p">Scale without treatment tier is incomplete: a large plant with advanced filtration is a different civic asset from a large plant stuck at primary or secondary standards.</p>

<h2 id="breakdown" class="anchored">Discharge by country</h2>
<h3 id="breakdown-look" class="anchored">WASTE DIS by COUNTRY</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wastewater/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wastewater/charts/chart1_breakdown.png" role="img" aria-label="WASTE DIS by COUNTRY"></div>
</figure>
<p class="art-p">Country rollups place high-intensity systems in view. <strong>Singapore</strong> leads near <strong>223,683</strong> m³/day on average plant discharge, while <strong>Nicaragua</strong> sits near <strong>33,649</strong>—a reminder that averages mix plant size, urban concentration, and reporting coverage. The United States leads aggregate discharge by facility count, not per-plant intensity. Large federations with many logged plants dominate totals even when median plants elsewhere run bigger.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Singapore leads at 223,683 — 56,849 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wastewater/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wastewater/charts/chart2_leaders.png" role="img" aria-label="Singapore leads at 223,683 — 56,849 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Among the top dozen countries by intensity, Singapore leads at <strong>223,683</strong> m³/day, and the median of that group is <strong>56,849</strong>—far above the file-wide median of 1,079. Dense city-states and highly instrumented reporting systems rise on these lists. The ranking reflects what gets measured and attributed as much as what flows through pipes.</p>
<h2 id="how-the-field-is-spread" class="anchored">Treatment levels spread discharge</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">WASTE DIS by LEVEL</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wastewater/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wastewater/charts/chart3_distribution.png" role="img" aria-label="WASTE DIS by LEVEL"></div>
</figure>
<p class="art-p">Category boxes by treatment level—secondary, advanced, and related labels—show whether discharge norms are shared or split across tiers. Secondary dominates headcount; advanced plants can dominate intensity. The civic stakes: upgrading level without changing plant counts can shift environmental outcomes more than building another median-sized secondary facility.</p>
<h2 id="who-beats-the-median-and-who-trails" class="anchored">Who beats the median — and who trails</h2>
<h3 id="who-beats-the-median-and-who-trails-look" class="anchored">WASTE DIS vs median by LEVEL</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wastewater/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wastewater/charts/chart4_gap.png" role="img" aria-label="WASTE DIS vs median by LEVEL"></div>
</figure>
<p class="art-p"><strong>Advanced</strong> treatment sits <strong>681</strong> m³/day above the median; <strong>Secondary</strong> trails by <strong>342</strong>. The direction fits only if advanced plants are often larger urban facilities, not merely cleaner ones. Level labels encode technology and city scale. Reading the gap as a pure quality ranking without plant-size context overfits the moral and underfits the engineering.</p>
<h2 id="what-moves-together" class="anchored">Discharge and quality fields</h2>
<h3 id="what-moves-together-look" class="anchored">WASTE DIS vs QUAL WASTE</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/wastewater/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/wastewater/charts/chart5_scatter.png" role="img" aria-label="WASTE DIS vs QUAL WASTE"></div>
</figure>
<p class="art-p">Plotting waste discharge against quality scores reveals clusters that averages erase. Some plants combine high discharge with strong quality marks; others pair modest discharge with weaker flags. The scatter is where big and good stop being synonyms. Infrastructure policy needs both axes: capacity to serve population, and treatment quality sufficient for receiving water.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and uneven national reporting apply. Proposed or non-operational plants can sit beside active ones if status filters are imperfect.</p>
<p class="art-p">Discharge units and quality fields are HydroWASTE-derived attributes in the release—not a substitute for local permit databases or real-time effluent monitoring.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Wastewater is a skewed industry: median discharge near 1,079 m³/day, extremes above three million, and country totals dominated by large reporting systems such as the United States.</p>
<p class="art-p">The citable distinction is treatment level versus size. Secondary is common; advanced sits 681 m³/day above the median; quality and discharge together decide whether a plant is merely large or actually protective.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p"><a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2022/2022-09-20">The source is the TidyTuesday release from 2022-09-20 (R for Data Science community). The working file contains 58,502 rows and 25 columns after merging country, treatment level, discharge, and quality fields.</a></p>
<p class="art-p">Medians handle skew from a handful of enormous plants. Charts export as Plotly JSON with PNG fallbacks. Status labels—operational, proposed, decommissioned—matter: not every row is an active facility.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
</section>
</main>
</div>
