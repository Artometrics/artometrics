---
title: 'SCHOOLS: School Diversity Peaks at 85.3 While the Median Holds at 2.38'
slug: schools
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Butteville Union Elementary scores 85.3 on the Multi index while the national median sits at 2.38 across 27,944 local education agencies.'
dek: "Across 27,944 school agencies, one is off the chart on diversity. Which?"
heroImage: /images/content/articles/schools/hero.png
draft: false
tags:
  - civics
  - education
subject: Schools
tldr: 'Across 27,944 U.S. local education agencies, the median Multi diversity score is 2.38, while Butteville Union Elementary leads at 85.3. Oklahoma sits 4.25 above the national median; New Jersey trails by 0.81. A flat center coexists with extreme upper-tail values.'
keyPoints:
  - '27,944 — Local education agencies in the working file — establishes coverage'
  - 2.38 — Median Multi across all schools — defines the flat center of the distribution
  - 85.3 — Butteville Union Elementary's Multi score — marks the upper extreme
  - +4.25 — Oklahoma's gap above the median — shows positive geographic offset
  - −0.81 — New Jersey's gap below the median — reveals negative offset despite diverse state demographics
faq:
  - question: What is the median diversity score in this dataset?
    answer: 'The median Multi score is 2.38 across 27,944 local education agencies.'
  - question: Which school district has the highest diversity score?
    answer: Butteville Union Elementary leads at 85.3 on the Multi index.
  - question: Does a diverse state automatically mean diverse schools?
    answer: 'No; New Jersey trails the median by 0.81 despite high population diversity, showing that district boundaries and residential sorting separate state demographics from school-level composition.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Butteville Union Elementary scores 85.3 on the Multi diversity index while the national median sits at 2.38 across 27,944 local education agencies. The 35-fold gap between the top district and the median defines the shape of U.S. school diversity: a flat center and an extreme upper tail.</p>
<p class="art-p">Texas is the most common state in the file by record count, but frequency does not equal high diversity scores. Oklahoma sits 4.25 above the median; New Jersey trails by 0.81. The Multi–Variance scatter reveals that schools cluster rather than form a smooth cloud, indicating that composition patterns vary independently of overall diversity level.</p>
<h2 id="research-question" class="anchored">Research question</h2>
<p class="art-p">Where does student-body diversity concentrate when the unit of analysis is the local education agency rather than the nation as a whole? This report asks whether the Multi metric behaves like a broad national baseline or a long-tailed distribution in which a few LEAs and states sit far above the typical row.</p>
<p class="art-p">The observational question is constrained to the source file: how stable is the median, which LEA names define the upper tail, how do state abbreviations structure the spread, and how does Multi relate to Variance? It does not treat one diversity metric as the full moral or demographic story of American education.</p>

<h2 id="a-flat-median-hides-how-extreme-the-upper-tail-is" class="anchored">A flat median hides how extreme the upper tail is</h2>
<h3 id="a-flat-median-hides-how-extreme-the-upper-tail-is-look" class="anchored">Median Multi Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/schools/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/schools/charts/chart1_trend.png" role="img" aria-label="Median Multi Over Time"></div>
</figure>
<p class="art-p">The median Multi sits at 2.38 in the opening period and 2.38 at the close — a flat line at the center of the distribution. Stability at the median does not mean stability everywhere; it means the typical school's Multi did not move in this snapshot window. That flat center is the baseline against which the leaderboard should be read. The action in school diversity here is not a national median march — it is how far individual LEAs sit above that center. U.S. school diversity is often narrated through landmark legal periods: <em>Brown v. Board of Education</em> in 1954, the busing and desegregation orders of the 1960s and 1970s, the release from court supervision in later decades, and contemporary residential segregation. Those histories are real, but this chart is not a long legal history; it is a snapshot-style metric view where the center does not move. A stable center can coexist with sharp local change because public education is geographically partitioned. District boundaries, housing markets, charter growth, school assignment rules, and private-school exit can all alter individual LEAs without moving the national median much. The chart tells readers to look for distributional extremes rather than assume a single national trend.</p>
<h2 id="butteville-union-elementary-leads-a-steep-lea-ladder" class="anchored">Butteville Union Elementary leads a steep LEA ladder</h2>
<h3 id="butteville-union-elementary-leads-a-steep-lea-ladder-look" class="anchored">Top LEA NAME</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/schools/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/schools/charts/chart2_leaders.png" role="img" aria-label="Top LEA NAME"></div>
</figure>
<p class="art-p">Butteville Union Elementary leads at 85.3 Multi. Among the top dozen LEAs, the median is 52.0 — still many times the file-wide median of 2.38. The leaderboard is an upper-tail map of districts whose composition scores sit far from the typical school. LEA names on this chart carry the highest observed Multi values in the file. They are not a random sample of American schooling; they are the extreme cases the metric surfaces first. Butteville Union Elementary is a named local education agency rather than a state system, which is exactly why the scale warning matters. A small district can produce an extreme composition metric if its enrollment mix is unusual, if denominators are small, or if categories split more evenly than in larger systems. The top of the ladder is a place to investigate, not a national template. The top-dozen median of 52.0 confirms that the upper tail is not one data-entry spike. Several LEAs sit in a high-Multi band that is many times the file-wide center. In education data, that kind of gap often reflects the interaction of neighborhood demography, district boundaries, grade configuration, and reporting categories.</p>
<h2 id="state-boxes-show-how-multi-spreads-geographically" class="anchored">State boxes show how Multi spreads geographically</h2>
<h3 id="state-boxes-show-how-multi-spreads-geographically-look" class="anchored">Multi by ST</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/schools/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/schools/charts/chart3_distribution.png" role="img" aria-label="Multi by ST"></div>
</figure>
<p class="art-p">Splitting Multi by state (ST) produces category boxes that reveal whether diversity scores are shared or contested across jurisdictions. Texas appears most often in the file, but frequency of rows is not the same as high Multi; volume and score must be read separately. The state axis is useful because education policy and demography both vary geographically. The boxes show the within-state spread that a single national median erases. Texas appearing most often is not surprising in a school file: it is a large state with many districts, fast-growing metropolitan regions, and substantial racial and ethnic diversity across Houston, Dallas-Fort Worth, San Antonio, Austin, the Rio Grande Valley, and rural counties. But row frequency mainly measures how much Texas appears in the extract, not whether every Texas LEA scores high on Multi. State boxes are also institutional boxes. School finance rules, district consolidation, county governance, accountability systems, and enrollment reporting vary by state education agencies. A state-level spread therefore mixes demography with administrative design, which is why the box plot is more informative than a single state average.</p>
<h2 id="oklahoma-clears-the-median-new-jersey-trails" class="anchored">Oklahoma clears the median; New Jersey trails</h2>
<h3 id="oklahoma-clears-the-median-new-jersey-trails-look" class="anchored">Multi vs median by ST</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/schools/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/schools/charts/chart4_gap.png" role="img" aria-label="Multi vs median by ST"></div>
</figure>
<p class="art-p">Relative to the median, Oklahoma sits 4.25 above; New Jersey trails by 0.81. That gap chart converts state boxes into signed distance from the file center — a quick way to see who systematically lands higher or lower on Multi. These are structural offsets in the working extract, not causal claims about state policy. They locate where the distribution's weight sits once the national median is the reference line. Oklahoma's positive gap and New Jersey's negative gap should be read against the metric definition and the units in the file. Oklahoma contains urban districts, rural districts, and tribal-nation contexts that can produce different student-body compositions across local agencies. New Jersey contains highly diverse metropolitan areas as well, but district boundaries and within-state sorting can produce lower values on this particular Multi summary. The signed-distance format resists a common error in education debate: assuming that states with diverse populations automatically have diverse schools. Residential segregation, municipal fragmentation, selective programs, and district borders can separate population diversity from school-level diversity.</p>
<h2 id="multi-and-variance-move-together-in-clusters" class="anchored">Multi and Variance move together in clusters</h2>
<h3 id="multi-and-variance-move-together-in-clusters-look" class="anchored">Multi vs Variance</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/schools/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/schools/charts/chart5_scatter.png" role="img" aria-label="Multi vs Variance"></div>
</figure>
<p class="art-p">Plotting Multi against Variance shows joint structure that averages erase: schools and districts form clusters rather than a single smooth cloud. High Multi with different Variance profiles is a different composition story from moderate Multi with tight Variance. The scatter's job is relational. It does not crown a winner; it shows which combinations of diversity level and dispersion appear together in the 27,944-row file. Variance adds a second lens because two LEAs can have similar Multi values while distributing students across categories differently. One district may be broadly balanced across several groups; another may be split sharply between two groups; a third may have a small high-Multi subgroup inside a mostly homogeneous system. Multi alone cannot distinguish those patterns. This is where school diversity connects to the measurement literature on segregation and exposure. Researchers often use dissimilarity, isolation, entropy, and exposure indices because no single measure captures both representation and distribution. The scatter does not replace those indices, but it shows why a one-column metric needs a dispersion companion.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live federal education APIs. Missing values, spelling variants in LEA names, and week-of-export coverage limits apply. Merged tables may fan out or duplicate rows when join keys are imperfect.</p>
<p class="art-p">Multi is the metric as defined in the source file. Findings describe this schools extract — not a complete census of every U.S. school in every year.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The national median Multi of 2.38 is stable in the available trend window, while individual LEAs such as Butteville Union Elementary reach 85.3. Diversity here is a long-tailed property: the center barely moves, and the extremes define the drama.</p>
<p class="art-p">State gaps (Oklahoma above the median, New Jersey below) and the Multi–Variance scatter add geography and joint structure. Together they show where student-body diversity concentrates without pretending one number explains the whole map.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2019-09-24 (R for Data Science community). The working file contains 27,944 rows and 15 columns after merging available tables in the week folder. Multi is the primary observed metric used for ranking and distribution charts; Variance appears alongside it in the scatter.</p>
<p class="art-p">Medians are used because school-level diversity metrics skew. Index-style fields are excluded from metric selection. State codes (ST) and LEA names are categorical axes for comparing how Multi sits across geography and district identity.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2019). <em>TidyTuesday: School Diversity</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-09-24/school_diversity.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-09-24/school_diversity.csv</a></p>
<p>Data Science Learning Community. (2019). <em>TidyTuesday School Diversity source folder</em>. <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-09-24" target="_blank" rel="noopener noreferrer">https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-09-24</a></p>
<p>National Center for Education Statistics. <em>Common Core of Data</em>. <a href="https://nces.ed.gov/ccd/" target="_blank" rel="noopener noreferrer">https://nces.ed.gov/ccd/</a></p>
<p>Reardon, S. F., &amp; Owens, A. (2014). 60 years after Brown: Trends and consequences of school segregation. <em>Annual Review of Sociology</em>, 40, 199–218. <a href="https://doi.org/10.1146/annurev-soc-071913-043152" target="_blank" rel="noopener noreferrer">https://doi.org/10.1146/annurev-soc-071913-043152</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-09-24" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
