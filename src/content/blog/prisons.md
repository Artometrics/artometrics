---
title: 'PRISONS: U.S. Jail Populations, County by County, 1970–2016'
slug: prisons
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'County-level population data show regional regimes that diverge for decades, not one national curve.'
dek: "County jail populations did not follow one national story. They followed hundreds of local ones."
heroImage: /images/content/articles/prisons/hero.png
draft: false
tags:
  - civics
  - law
subject: Prisons
tldr: 'County-level incarceration data across 1970–2016 reveal regional regimes that diverge for decades, not a single national mass-incarceration curve. The working extract holds 100,000 records; median population is 3,553, the top observation exceeds 6.8 million, and the South is the most common region label.'
keyPoints:
  - '100,000 — Records spanning 1970–2016 — coverage window includes federal war on drugs, sentencing-policy shifts, and the post-2000s plateau'
  - '3,553 — Median population — typical row far below giant urban systems'
  - '6,801,437 — Highest observed population — California dominates state rollup; DC leads dense-jurisdiction chart'
  - '13,710 — Northeast sits above median; Midwest trails by 1,276 — regional gaps reflect urban weight, not just policy intensity'
  - 'Pretrial population — scales with jurisdiction size in clusters, deviates sharply in others — flags bail, charging, and court-backlog regimes'
faq:
  - question: How many records are in this dataset?
    answer: '100,000 records spanning 1970–2016, with state, region, year, population, and pretrial fields.'
  - question: What is the median population in this extract?
    answer: '3,553 — stabilizes skew from giant counties and city systems.'
  - question: Which state leads by population?
    answer: 'California leads the state rollup; DC leads the dense-jurisdiction chart at 190,209.'
  - question: What does pretrial population measure?
    answer: 'People held in jail before conviction — shaped by bail schedules, risk assessment, prosecutorial charging, and court backlogs.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">County-level incarceration data across 1970–2016 reveal regional regimes that diverge for decades, not a single national mass-incarceration curve. The working extract holds 100,000 records; median population is 3,553, the top observation exceeds 6.8 million, and the South is the most common region label.</p>
<p class="art-p">Population is not identical to incarceration rate, but it is the spine that lets pretrial counts, regional gaps, and long-run change be compared without pretending every county is the same size. The 1970–2016 window covers the main period in which the United States moved from the pre-1970 baseline into what the National Research Council and Bureau of Justice Statistics describe as mass incarceration — including the 1971 declaration of the federal war on drugs, the sentencing-policy changes of the 1980s, and the long plateau after the 2000s.</p>
<h2 id="research-question" class="anchored">Research question</h2>
<p class="art-p">What does the county-and-state structure of the U.S. incarceration file reveal that a single national curve would hide? This report asks how population, region, and pretrial population sit together in the 1970–2016 extract, and where the file points toward divergent local regimes rather than one uniform national process.</p>
<p class="art-p">The question is observational: which geographies dominate the row structure, how far regional medians sit from the file center, and whether pretrial burden scales cleanly with population. Population is treated as the denominator context necessary before any rate-based claim can be trusted, not as a rate itself.</p>

<h2 id="how-the-pattern-changed-over-time" class="anchored">How the pattern changed over time</h2>
<h3 id="how-the-pattern-changed-over-time-look" class="anchored">Median Population Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/prisons/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/prisons/charts/chart1_trend.png" role="img" aria-label="Median Population Over Time"></div>
</figure>
<p class="art-p">Median population in the working series falls from about 4,123 in the opening period to about 3,359 at the close. That movement can reflect changing county coverage, urban-rural composition, and how incomplete early rows enter the sample — not a simple story that places got smaller. The time chart forces the rest of the analysis to admit that the typical row in 1970 and the typical row in 2016 are not drawn from identical geographic mixes. Because this file is row-based, the median population line is partly a coverage diagnostic. A county with a small jail, a large urban system, and a state-level aggregate can coexist in the same extract if the source tables carry them forward. The trend line therefore tells readers how the analytic unit changes over time before it tells them anything about punishment intensity.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">DC leads at 190,209 — 24,944 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/prisons/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/prisons/charts/chart2_leaders.png" role="img" aria-label="DC leads at 190,209 — 24,944 marks the median among the top dozen"></div>
</figure>
<p class="art-p">On the leader cut highlighted in the file, DC leads at 190,209, with 24,944 as the median among the top dozen. Dense jurisdictions and large states occupy the same head for different reasons — capital-city concentration versus sheer statewide population. California's fact-box lead on state population and DC's lead on this chart can both be true. They answer different aggregation questions. Confusing them produces false arguments about which place is most incarcerated rather than which place is largest or densest in the extract. The District of Columbia is a warning case because it is not a state, not an ordinary county, and not a simple municipal equivalent. Its criminal-justice system has long involved federal oversight, local jail custody, and post-sentencing arrangements that differ from state prison systems. A high DC entry in a population leader chart should trigger questions about geography and institutional definition before it triggers a national ranking claim. California's presence in the state rollup points to a different scale issue. Los Angeles County, the California Department of Corrections and Rehabilitation, and statewide demographic size all shape the visibility of California in criminal-justice data. Large population does not automatically mean high rate; it means the denominator and administrative footprint are large enough to dominate many raw-count charts.</p>
<h2 id="how-the-field-is-spread" class="anchored">How regions spread</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Population by Region</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/prisons/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/prisons/charts/chart3_distribution.png" role="img" aria-label="Population by Region"></div>
</figure>
<p class="art-p">Regional box plots show whether population consensus is shared or contested across the South, Northeast, Midwest, and West. The South's frequency as the most common region label does not automatically mean it has the highest median population per row. Spread within regions often exceeds spread between region medians. County inequality inside a region is part of the incarceration story, not noise around a regional average. The regional labels matter because U.S. criminal justice is federal in vocabulary but local in operation. Sheriffs, county commissioners, state legislatures, prosecutors, bail rules, jail financing, and prison siting vary sharply across the South, Northeast, Midwest, and West. The South's high row frequency in the file is consistent with its large county count and centrality in incarceration scholarship, but it is not itself proof of a higher imprisonment rate. Within-region spread is where the policy story begins. A rural Southern county, Harris County in Texas, Cook County in Illinois, and New York City's jail system do not share the same scale or pretrial process simply because they fit under regional labels. Box plots protect that variation from being erased by a single national average.</p>
<h2 id="who-beats-the-median-and-who-trails" class="anchored">Who beats the median — and who trails</h2>
<h3 id="who-beats-the-median-and-who-trails-look" class="anchored">Population vs median by Region</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/prisons/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/prisons/charts/chart4_gap.png" role="img" aria-label="Population vs median by Region"></div>
</figure>
<p class="art-p">On the gap chart, the Northeast sits 13,710 above the median; the Midwest trails by 1,276. Those gaps capture the urban weight of Northeastern counties in the sample as much as any single policy variable. Regional gaps are starting points for rate-based follow-ups, not final moral rankings. A high-population region can have lower incarceration rates, and a lower-population region can incarcerate more intensively per resident. The Northeast's positive gap is plausibly shaped by the presence of dense metropolitan jurisdictions such as New York, Philadelphia, Boston, Newark, and surrounding counties, where raw population denominators are large. The Midwest's negative gap does not mean Midwestern incarceration is low; it means the population field in this working extract sits below the file median for that regional cut. That distinction is not pedantry. Prison Policy Initiative, Vera Institute, and BJS reports routinely separate jail admissions, jail population, prison custody, and incarceration rates per 100,000 residents because raw headcounts can move in the opposite direction of rates. The gap chart is a routing map for those follow-ups, not a replacement for them.</p>
<h2 id="what-moves-together" class="anchored">Population and pretrial population</h2>
<h3 id="what-moves-together-look" class="anchored">Population vs Pretrial population</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/prisons/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/prisons/charts/chart5_scatter.png" role="img" aria-label="Population vs Pretrial population"></div>
</figure>
<p class="art-p">Plotting population against pretrial population shows clusters that averages erase. Some large jurisdictions carry large pretrial counts in rough proportion; others deviate — the places where jail composition, not just city size, is doing extra work. Pretrial population is one of the most policy-sensitive fields in modern jail debate. The scatter does not prove causation, but it flags where scale and pretrial burden travel together and where they separate. Pretrial detention is legally different from sentenced imprisonment. People held pretrial have generally not been convicted in the case that keeps them in jail, which makes bail schedules, risk assessment tools, prosecutorial charging, and court backlogs central to the count. The Bureau of Justice Statistics has repeatedly documented that local jails hold a large share of unconvicted people, making this field a direct bridge between data and constitutional policy. The scatter can therefore guide a more serious audit. Jurisdictions far above the population-pretrial trend are candidates for closer inspection of bail practices, case-processing time, and jail-capacity politics. Jurisdictions below the trend may have diversion programs, lower detention thresholds, different offense mixes, or simply different data coverage. The chart identifies candidates; it does not adjudicate causes.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and coverage limits apply. Population columns are not a substitute for official imprisonment rates per 100,000 residents.</p>
<p class="art-p">Findings describe the file on hand — structural signals about how geographies and pretrial counts sit across 1970–2016 — not a complete causal history of mass incarceration.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Incarceration trends in this extract are a story of divergent geographies sharing one national vocabulary. Median rows sit near 3,553 people; extremes exceed millions; regional gaps reach five figures above the median.</p>
<p class="art-p">The citable caution is simple: size, region, and pretrial burden are related but not identical. Any claim about the U.S. incarceration rate that skips those splits is summarizing away the map.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2019-01-22 (R for Data Science community). The working file contains 100,000 rows and 10 columns after assembly — state, region, year, population, and pretrial population among the fields carried forward.</p>
<p class="art-p">Medians stabilize skew from giant counties and city systems. Charts export as Plotly JSON with PNG fallbacks. Because the table mixes geographies of very different scale, every ranking should be read with population context attached.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2019). <em>TidyTuesday: Incarceration Trends</em>. <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-01-22" target="_blank" rel="noopener noreferrer">https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-01-22</a></p>
<p>Bureau of Justice Statistics. <em>Correctional Populations in the United States</em>. <a href="https://bjs.ojp.gov/library/publications/list?series_filter=Correctional%20Populations%20in%20the%20United%20States" target="_blank" rel="noopener noreferrer">https://bjs.ojp.gov/library/publications/list?series_filter=Correctional%20Populations%20in%20the%20United%20States</a></p>
<p>National Research Council. (2014). <em>The Growth of Incarceration in the United States: Exploring Causes and Consequences</em>. <a href="https://doi.org/10.17226/18613" target="_blank" rel="noopener noreferrer">https://doi.org/10.17226/18613</a></p>
<p>Vera Institute of Justice. <em>Incarceration Trends</em>. <a href="https://trends.vera.org/" target="_blank" rel="noopener noreferrer">https://trends.vera.org/</a></p>
</section>
</main>
</div>
