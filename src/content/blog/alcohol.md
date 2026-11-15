---
title: "ALCOHOL: Who Drinks the Most Per Capita?"
slug: alcohol
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  Country-level consumption data map which nations drink the most per person—and
  how that has shifted.
dek: "Which countries drink the most per person, and what are they pouring?"
heroImage: /images/content/articles/alcohol/hero.png
draft: false
tags:
  - culture
  - food
subject: Alcohol
tldr: >-
  Global alcohol data is often collapsed into a single “drinks per person”
  headline. The TidyTuesday global alcohol extract keeps the beverage split
  intact — beer, spirits, and wine servings — across 193 country-level records.
  Beer is the metric that leads these charts, with a median of 76.0 servings and
  a recorded high of 376 in Namibia. That spread is the story.
keyPoints:
  - 193 — Records in the working dataset
  - 76.0 — Median Beer servings
  - 376 — Highest observed Beer servings
  - Namibia — Top Country by Beer servings
faq:
  - question: >-
      How many records are in this dataset?
    answer: >-
      193 records in the working dataset.
  - question: >-
      What is the median Beer servings?
    answer: >-
      The median Beer servings is 76.0.
  - question: >-
      What is the highest observed value in this extract?
    answer: >-
      The highest observed value in the extract is 376.
  - question: >-
      Which country leads in this extract?
    answer: >-
      Namibia leads the country ranking in this extract.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Global alcohol data is often collapsed into a single “drinks per person” headline. The TidyTuesday global alcohol extract keeps the beverage split intact — beer, spirits, and wine servings — across <strong>193</strong> country-level records. Beer is the metric that leads these charts, with a median of <strong>76.0</strong> servings and a recorded high of <strong>376</strong> in Namibia.</p>
<p class="art-p">That spread is the story. A median of 76 and a maximum of 376 means the top of the beer distribution is not a gentle tail; it is a different consumption regime. Country rankings on beer alone will not match rankings on spirits, and the scatter at the end makes that explicit.</p>
<h2 id="research-question" class="anchored">Research question</h2>
<p class="art-p">When alcohol data is separated by beverage, does a country’s apparent drinking profile still look like one national habit, or does it split into distinct beer, spirits, and wine cultures? This report uses the 2018 TidyTuesday global alcohol extract to ask where beer volume concentrates and whether the beer leaderboard can stand in for total alcohol behavior.</p>
<p class="art-p">The observational question is deliberately narrow: which countries sit in the high-beer tail, how far above the median they are, and whether beer intensity travels with spirits intensity. That focus keeps the charts from becoming a generic public-health ranking and instead treats beverage mix as a measurable cultural and market structure.</p>

<h2 id="beer-consumption-has-a-steep-country-ladder" class="anchored">Beer Consumption Has a Steep Country Ladder</h2>
<h3 id="beer-consumption-has-a-steep-country-ladder-look" class="anchored">Beer servings by Country</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/alcohol/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/alcohol/charts/chart1_breakdown.png" role="img" aria-label="Beer servings by Country"></div>
</figure>
<p class="art-p">Namibia leads the beer ranking at <strong>376</strong> servings, followed by the Czech Republic at <strong>361</strong>, Gabon at <strong>347</strong>, and Germany at <strong>346</strong>. Lithuania and Poland tie near <strong>343</strong>. Ireland sits lower in the top dozen at <strong>313</strong>. These are not clustered scores around the global median of 76. The leaders occupy roughly four to five times the typical country’s beer volume in this file — a reminder that beer culture is geographically concentrated, not evenly shared. The country names matter because they point to different beverage systems. Namibia and Gabon place African markets in the same high-beer conversation as the Czech Republic, Germany, Lithuania, Poland, and Ireland — countries often associated with long-standing brewing industries, beer taxation regimes, and pub or lager cultures. A single “Europe drinks beer” shortcut would miss the African leaders; a single “income predicts beer” shortcut would miss the spread across very different economies. The 2018 TidyTuesday file descends from World Health Organization alcohol indicators that summarize recorded servings rather than clinical outcomes. That distinction is important: a serving count can identify beverage concentration, but it does not measure binge patterns, liver disease, drunk-driving deaths, or unrecorded home output. The chart is strongest as a map of recorded beverage preference.</p>
<h2 id="the-top-dozen-has-its-own-median" class="anchored">The Top Dozen Has Its Own Median</h2>
<h3 id="the-top-dozen-has-its-own-median-look" class="anchored">Namibia leads at 376 — 338 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/alcohol/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/alcohol/charts/chart2_leaders.png" role="img" aria-label="Namibia leads at 376 — 338 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Among the top twelve beer countries, Namibia’s <strong>376</strong> still leads, while the median of that elite group is <strong>338</strong>. Even inside the high-beer club, the distribution has a ceiling that most of the world never approaches. Reading only the global median would hide that club entirely. Reading only Namibia would hide how many Central European and other high-beer countries sit just behind it. The top-dozen median of 338 is almost as revealing as the maximum. It says the leaders are not one outlier and eleven ordinary countries; they are a compact high-consumption band. Czech, German, Lithuanian, Polish, and Irish entries sit in a historically industrial beer belt, while Namibia and Gabon remind us that contemporary beer markets also reflect colonial trade routes, urban retail systems, and modern commercial breweries. For public-health interpretation, this is where volume and harm begin to diverge. WHO and OECD alcohol reports usually emphasize liters of pure alcohol, age-standardized mortality, and sex-specific patterns because beverage-specific servings alone cannot compare the ethanol load of beer, wine, and spirits. This Artometrics cut keeps the serving metric because it asks a cultural-economy question first: where is beer, as a category, unusually dominant?</p>
<h2 id="most-countries-cluster-far-below-the-peaks" class="anchored">Most Countries Cluster Far Below the Peaks</h2>
<h3 id="most-countries-cluster-far-below-the-peaks-look" class="anchored">Beer servings Distribution</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/alcohol/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/alcohol/charts/chart3_distribution.png" role="img" aria-label="Beer servings Distribution"></div>
</figure>
<p class="art-p">The distribution chart piles most countries into lower beer-serving bins. Counts peak in the low double-digit and mid-range bins, while the extreme high bins that hold Namibia and the Czech Republic contain only a handful of countries. That shape is why the median (76.0) is the right headline number: it describes the typical country, not the viral maximum. The skew also changes how readers should interpret “per capita” comparisons. A country can sit below the median because beer is less available, because spirits or wine dominate the market, because alcohol consumption is lower overall, or because religious and legal rules suppress recorded sales. Those mechanisms are not interchangeable, even if they all land in the same low-beer bins. The lower half of the distribution should therefore be read as a mixture of abstention, substitution, market structure, and reporting practice. In many Muslim-majority countries, for example, recorded beer servings will reflect legal and religious constraints as much as consumer taste. In wine-producing countries, the same low beer value may simply mean the alcohol profile has moved to another column.</p>
<h2 id="concentration-rises-quickly-among-the-leaders" class="anchored">Concentration Rises Quickly Among the Leaders</h2>
<h3 id="concentration-rises-quickly-among-the-leaders-look" class="anchored">Cumulative Beer servings</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/alcohol/charts/chart4_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/alcohol/charts/chart4_pareto.png" role="img" aria-label="Cumulative Beer servings"></div>
</figure>
<p class="art-p">The Pareto curve shows how cumulative beer servings accumulate as countries are added from the top. The first five entries already account for about <strong>37%</strong> of the aggregate among the plotted leaders; by fifteen entries the curve reaches 100% of that restricted total. Beer volume at the top is not democratic. A short list of countries carries a disproportionate share of the servings represented in this ranking view. A Pareto view is useful because alcohol markets often look concentrated at multiple scales: a few beverage categories, a few dominant firms, and a few countries with unusually high recorded intake. The first five countries in this leader-only curve are not a global share of all alcohol; they are the head of the beer ranking. That narrower denominator is exactly why the curve is steep. Concentration also affects policy comparison. If a small set of countries drives the visual range, then a dashboard built around maxima will exaggerate the distance between most countries. Median-centered views and beverage-specific scatterplots are better for separating ordinary national profiles from the high-consumption head.</p>
<h2 id="beer-and-spirits-are-not-the-same-map" class="anchored">Beer and Spirits Are Not the Same Map</h2>
<h3 id="beer-and-spirits-are-not-the-same-map-look" class="anchored">Beer servings vs Spirit servings</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/alcohol/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/alcohol/charts/chart5_scatter.png" role="img" aria-label="Beer servings vs Spirit servings"></div>
</figure>
<p class="art-p">Plotting beer servings against spirit servings across all 193 countries breaks the assumption that “heavy drinking” is one behavior. Some countries post high beer with moderate spirits; others invert the pattern. The joint distribution is the corrective lens: beverage preference is cultural and economic, not a single alcohol intensity score. Namibia’s beer lead does not automatically imply a spirits lead. The scatter is the most important methodological guardrail in the report. Eastern European and post-Soviet alcohol research, for example, often emphasizes spirits because high-proof beverages can dominate harm profiles even when beer is not the leading column. Mediterranean comparisons often separate wine from both. A beer-only table cannot adjudicate those patterns. That is why the article does not collapse the file into a total-servings index. Total alcohol may be the right measure for burden-of-disease work; beverage separation is the right measure for understanding culture, taxation, retail systems, and substitution. The same country can be a beer outlier, a spirits moderate, and a wine footnote.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Country-level serving estimates inherit survey, sales, and tourism distortions. Unrecorded alcohol, home output, and cross-border purchases can bias official figures. The 2018 TidyTuesday snapshot is not a live WHO dashboard.</p>
<p class="art-p">Rankings on beer servings alone should not be quoted as total alcohol harm rankings. Spirits and wine columns exist precisely because the beverage mix differs.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Beer consumption in this extract is a steep hierarchy: Namibia at 376 servings against a world median of 76. The top dozen forms its own high plateau around a median of 338.</p>
<p class="art-p">The lasting insight is comparative: beer leaders and spirits leaders are not the same set of countries, and any serious alcohol map has to keep those axes separate.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2018-06-26 (week13_alcohol_global.csv), maintained by the R for Data Science community. The working file used here contains 193 rows after cleaning.</p>
<p class="art-p">Beer servings are the primary ranked metric in the chart stack. Medians are used where distributions skew. Charts are Plotly JSON with PNG fallbacks.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2018). <em>TidyTuesday: Alcohol Consumption</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2018/2018-06-26/week13_alcohol_global.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2018/2018-06-26/week13_alcohol_global.csv</a></p>
<p>World Health Organization. (2018). <em>Global status report on alcohol and health 2018</em>. <a href="https://www.who.int/publications/i/item/9789241565639" target="_blank" rel="noopener noreferrer">https://www.who.int/publications/i/item/9789241565639</a></p>
<p>World Health Organization. (2024). <em>Global status report on alcohol and health and treatment of substance use disorders</em>. <a href="https://www.who.int/publications/i/item/9789240096745" target="_blank" rel="noopener noreferrer">https://www.who.int/publications/i/item/9789240096745</a></p>
<p>OECD. (2021). <em>Preventing Harmful Alcohol Use</em>. <a href="https://doi.org/10.1787/6e4b4ffb-en" target="_blank" rel="noopener noreferrer">https://doi.org/10.1787/6e4b4ffb-en</a></p>
<p>Rehm, J., et al. (2009). Global burden of disease and injury and economic cost attributable to alcohol use and alcohol-use disorders. <em>The Lancet</em>, 373(9682), 2223–2233. <a href="https://doi.org/10.1016/S0140-6736(09)60746-7" target="_blank" rel="noopener noreferrer">https://doi.org/10.1016/S0140-6736(09)60746-7</a></p>
</section>
</main>
</div>
