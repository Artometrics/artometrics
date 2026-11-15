---
title: "AIRLINES: How Incident Counts Hide Exposure Differences"
slug: airlines
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  336 airline records show capacity dominates safety rankings—United leads at
  7.1B seat-km/week, but incident counts don't scale linearly with size.
dek: "Raw incident counts rank airlines unfairly. Here is what happens when you account for how much each one flies."
heroImage: /images/content/articles/airlines/hero.png
draft: false
tags:
  - culture
  - travel
subject: Airlines
tldr: >-
  Raw incident counts rank airlines unfairly. The TidyTuesday airlines dataset includes 336 records normalized by available seat kilometers per week—a capacity metric that separates exposure from outcome. United/Continental leads at 7.1 billion seat-km weekly, but event counts don't move in lockstep with scale, showing that size and safety record are distinct questions.
keyPoints:
  - 336 — Records in the working dataset
  - 802,908,893 — Median available seat-km per week
  - 7,139,291,291 — Highest observed available seat-km per week
  - United/Continental — Top airline by capacity
  - Incidents scale independently of available seat-kilometers
faq:
  - question: How many airline records are in this dataset?
    answer: 336 records after merging the TidyTuesday tables from August 7, 2018.
  - question: What capacity metric is used?
    answer: Available seat kilometers per week, with a median of 802.9 million across all carriers.
  - question: Which airline operates the most seat-kilometers?
    answer: United/Continental at 7.1 billion available seat-kilometers per week.
  - question: Do incident counts rise with airline size?
    answer: No. The scatter plot shows clusters where mid-size carriers report high incidents while some megacarriers sit lower relative to their capacity.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Airline safety is usually discussed one crash at a time. The TidyTuesday airlines dataset does something different: it aligns carriers by available seat kilometers per week—a capacity metric—and then asks how incidents, fatal accidents, and fatalities sit against that scale. The working file contains <strong>336</strong> cleaned records after merging the week's tables.</p>
<p class="art-p">Capacity is not the same as risk, but it is the right denominator for a fair first cut. A carrier flying <strong>7.1 billion</strong> available seat kilometers per week operates in a different exposure class than one flying under <strong>2 billion</strong>. The median in this extract is <strong>802,908,893</strong> available seat kilometers per week—a baseline for interpreting every ranking that follows.</p>
<p class="art-p">The most common event type in the file is labeled <strong>incidents</strong>. That distinction matters: the archive mixes routine reportable events with rarer fatal outcomes, and conflating those categories would obscure the real story.</p>

<h2 id="capacity-concentrates-among-megacarriers" class="anchored">Capacity Concentrates Among Megacarriers</h2>
<h3 id="capacity-concentrates-among-megacarriers-look" class="anchored">Available seat-km per week by airline</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/airlines/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/airlines/charts/chart1_breakdown.png" role="img" aria-label="Available seat-km per week by airline"></div>
</figure>
<p class="art-p">United/Continental* anchors the top at <strong>7,139,291,291</strong> available seat kilometers per week. Delta/Northwest* follows at approximately <strong>6.53 billion</strong>, then American* at <strong>5.23 billion</strong>. The next tier—Lufthansa*, Southwest, British Airways*, Air France—occupies the <strong>3.0 to 3.4 billion</strong> range. That gap is structural. The top three merged U.S. brands operate at a different scale than even large European flag carriers in this extract. When event counts are later compared across airlines, those capacity differences provide essential context.</p>
<h2 id="the-same-names-dominate-the-leader-board" class="anchored">The Same Names Dominate the Leader Board</h2>
<h3 id="the-same-names-dominate-the-leader-board-look" class="anchored">United/Continental* leads at 7,139,291,291—3,091,881,806 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/airlines/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/airlines/charts/chart2_leaders.png" role="img" aria-label="United/Continental* leads at 7,139,291,291—3,091,881,806 marks the median among the top dozen"></div>
</figure>
<p class="art-p">The leaders chart restates the capacity hierarchy with precision: United/Continental* leads at <strong>7,139,291,291</strong>, while the median among the top dozen sits near <strong>3,091,881,806</strong>. Half of the top tier still operates at less than half the leader's scale. Large airline is not a single category. It is a steep pyramid. Any analysis that ranks raw incident counts without accounting for this pyramid will systematically penalize the largest networks.</p>
<h2 id="event-type-does-not-rewrite-the-capacity-story" class="anchored">Event Type Does Not Rewrite the Capacity Story</h2>
<h3 id="event-type-does-not-rewrite-the-capacity-story-look" class="anchored">Available seat-km per week by event type</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/airlines/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/airlines/charts/chart3_distribution.png" role="img" aria-label="Available seat-km per week by event type"></div>
</figure>
<p class="art-p">Box plots separate available seat kilometers by event type—incidents, fatal_accidents, and fatalities. Each group shows the same median of <strong>802,908,893</strong> and the same maximum of <strong>7,139,291,291</strong> across 112 observations per box. That consistency is the finding. Event labels do not sort carriers into different capacity worlds; the same megacarrier scale appears whether the row is marked as an incident or a fatality record. The distribution reflects who operates the most seat-kilometers, not which label the row carries.</p>
<h2 id="gaps-to-the-median-are-flat-across-labels" class="anchored">Gaps to the Median Are Flat Across Labels</h2>
<h3 id="gaps-to-the-median-are-flat-across-labels-look" class="anchored">Available seat-km per week vs median by event type</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/airlines/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/airlines/charts/chart4_gap.png" role="img" aria-label="Available seat-km per week vs median by event type"></div>
</figure>
<p class="art-p">When available seat kilometers are compared to the sample median by event type, incidents, fatal_accidents, and fatalities all register essentially zero gap. This is a stability check, not a ranking. The chart's purpose is to rule out a false narrative: that one event category concentrates among unusually large or unusually small carriers. In this extract, the labels do not shift capacity away from the median.</p>
<h2 id="scale-and-event-counts-do-not-move-as-one-line" class="anchored">Scale and Event Counts Do Not Move as One Line</h2>
<h3 id="scale-and-event-counts-do-not-move-as-one-line-look" class="anchored">Available seat-km per week vs event count</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/airlines/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/airlines/charts/chart5_scatter.png" role="img" aria-label="Available seat-km per week vs event count"></div>
</figure>
<p class="art-p">Plotting available seat kilometers against event count reveals clusters that aggregate statistics erase. Some mid-size carriers report high incident counts; some of the largest networks register moderate totals relative to their seat-kilometer footprint. The fatality panel is particularly uneven: the highest fatality totals are not always concentrated at the absolute capacity leaders. Exposure and outcome are related, but not linearly—which is why capacity and counts must be read together.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">This is a community-cleaned TidyTuesday snapshot, not a live regulatory feed. Missing values, spelling variants on airline names (including starred merger labels), and the week-of-export coverage window all apply. Merged tables may duplicate or expand rows when join keys are imperfect.</p>
<p class="art-p">Available seat kilometers measure exposure opportunity, not proven risk. The file cannot determine which carriers are safest in a causal sense; it can only show how capacity and event tallies align in this extract.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The clearest finding is structural: a handful of megacarriers dominate available seat kilometers, with United/Continental* at the apex and a median near <strong>803 million</strong> seat kilometers per week for the wider field.</p>
<p class="art-p">Event-type labels do not reorder that hierarchy. The meaningful question is not which airline has the most recorded events—it is how those events scale against the seat-kilometers actually flown.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release dated August 7, 2018 from the R for Data Science community. After merging the week's CSV and XLSX tables, the working dataset contains 336 rows and five analysis columns used in these charts.</p>
<p class="art-p">Medians are preferred wherever available seat kilometers skew toward megacarriers. Index-style fields are excluded. Charts ship as Plotly JSON with PNG fallbacks so values remain inspectable on hover.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2018). <em>TidyTuesday: Airline Safety</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2018/2018-08-07/week19_airline_safety.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2018/2018-08-07/week19_airline_safety.csv</a></p>
</section>
</main>
</div>
