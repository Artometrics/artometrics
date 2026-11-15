---
title: 'EMPERORS: Constantine Lasted 31 Years; the Nerva–Antonine Line Averaged 12.5 More'
slug: emperors
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: Constantine ruled 31 years; the median emperor lasted 6.5—dynasty membership did not close that gap.
dek: "The median Roman emperor lasted 6.5 years. One lasted 31."
heroImage: /images/content/articles/emperors/hero.png
draft: false
tags:
  - humanities
  - history
subject: Emperors
tldr: '68 emperors yield a median reign of 6.50 years—half the tenure of the typical top-dozen ruler. Constantine the Great''s 31.0-year reign sits at the ceiling. Dynasty membership mattered, but unevenly: Nerva–Antonine emperors averaged 12.5 years above median; Gordian, despite being the most common dynasty label, trailed by 4.0.'
keyPoints:
  - 68 — emperors in the dataset — median reign of 6.50 years marks the center of a violent turnover system
  - '31.0 — Constantine the Great''s reign in years — the longest tenure in the extract, triple the elite-emperor median'
  - 12.5 — years above median for Nerva–Antonine dynasty — the only house to clear the file center by more than a decade
  - 40% — share of aggregate reign years held by the top five emperors — concentration means a few long rulers dominate institutional time
  - 'Gordian — most common dynasty label — volume without longevity, trailing median by 4.0 years'
faq:
  - question: Who ruled Rome longest in this dataset?
    answer: 'Constantine the Great at 31.0 years, from 306–337 CE.'
  - question: What is the median reign length for Roman emperors?
    answer: 6.50 years across 68 emperors.
  - question: Did dynasty membership extend reign length?
    answer: Unevenly. Nerva–Antonine emperors averaged 12.5 years above median; Gordian emperors trailed by 4.0.
  - question: How much imperial time did the longest emperors control?
    answer: The top five names account for 40% of aggregate reign years.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Constantine the Great ruled for 31.0 years. The median Roman emperor in this 68-record file lasted 6.50. That five-to-one gap frames the question: did dynasty membership buy stability, or did survival depend on forces that overwhelmed house labels? The answer is both, but unevenly—Nerva–Antonine emperors averaged 12.5 years above median, while Gordian, despite being the most common dynasty name, trailed by 4.0.</p>
<p class="art-p">The file covers 68 emperors drawn from the TidyTuesday Roman Emperors release. Reign length is measured from recorded start and end dates; dynasty labels come from the source table. The charts separate name-level longevity from dynasty-level structure so the two are not confused.</p>
<h2 id="research-question" class="anchored">Research question</h2>
<p class="art-p">Did dynastic identity extend Roman imperial tenure, or did individual political survival overwhelm house-level labels? The report asks whether reign length concentrates around exceptional rulers, whether dynasties show distinct tenure distributions, and how much aggregate imperial time is carried by the longest-reigning names.</p>
<p class="art-p">The question is observational. This 68-record TidyTuesday file is not a full constitutional model of Rome. It uses recorded reign spans to compare names and dynasties, treating the median emperor's 6.50-year tenure as the baseline.</p>

<h2 id="constantine-s-thirty-one-years-set-the-name-level-ceiling" class="anchored">Constantine's thirty-one years set the name-level ceiling</h2>
<h3 id="constantine-s-thirty-one-years-set-the-name-level-ceiling-look" class="anchored">Reign years by Name</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emperors/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emperors/charts/chart1_breakdown.png" role="img" aria-label="Reign years by Name"></div>
</figure>
<p class="art-p">Constantine the Great leads at 31.0 reign years. Valentinian II anchors the low end of the top group at 17.0—still far above the file median of 6.50. The chart shows a curated upper slice, not the full distribution. Grouping by name makes the catalog's major entities comparable on a single scale. The question is not who is famous, but who lasted. The gap between Constantine and the rest of the top tier shows that longevity was exceptional rather than routine. Constantine's 306–337 CE reign sits at a hinge in Roman institutional history: civil war, Tetrarchic succession, Christian legalization after the Edict of Milan, the Council of Nicaea in 325, and the foundation of Constantinople all fall inside or around his rule. The dataset reduces that to 31.0 years, but the named entity carries enough historical context to explain why the ceiling is not a spreadsheet oddity.</p>
<h2 id="the-top-dozen-still-sits-far-above-the-median-emperor" class="anchored">The top dozen still sits far above the median emperor</h2>
<h3 id="the-top-dozen-still-sits-far-above-the-median-emperor-look" class="anchored">Constantine the Great leads at 31.0 — 20.0 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emperors/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emperors/charts/chart2_leaders.png" role="img" aria-label="Constantine the Great leads at 31.0 — 20.0 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Among the top dozen emperors, the median is 20.0 years—three times the full-file median of 6.50. Even the typical elite tenure in this slice is a different political animal from the typical emperor in the dataset. That separation matters for interpretation. Leaderboards describe the right tail, not Rome's everyday succession reality, which lived closer to half a decade than to two decades. The 20.0-year median among the top dozen contains the familiar names that make imperial history feel more stable than it was: Augustus, Tiberius, Hadrian, Antoninus Pius, Marcus Aurelius, Constantine. The full-file median pulls the reader back toward usurpers, assassinations, co-rule, civil wars, and short-lived crisis reigns.</p>
<h2 id="dynasty-boxes-show-contested-not-uniform-tenure" class="anchored">Dynasty boxes show contested, not uniform, tenure</h2>
<h3 id="dynasty-boxes-show-contested-not-uniform-tenure-look" class="anchored">Reign years by Dynasty</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emperors/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emperors/charts/chart3_distribution.png" role="img" aria-label="Reign years by Dynasty"></div>
</figure>
<p class="art-p">When reign years are split by dynasty, the boxes do not collapse into a single shared consensus. Some houses stretch higher; others sit tighter and lower. The spread shows dynasty is a contested axis for tenure rather than deterministic. Read the boxes as structural signals: belonging to a named dynasty did not automatically purchase Constantine-length stability. It bought a distribution, and those distributions differ. The Nerva-Antonine adoption sequence has long been associated with high imperial stability, while the third-century crisis illustrates how military acclamation and rapid turnover can shred dynastic continuity. The box plot asks whether succession packages mattered—and the answer is yes, but variably.</p>
<h2 id="nerva-antonine-sits-above-the-median-gordian-trails" class="anchored">Nerva–Antonine sits above the median; Gordian trails</h2>
<h3 id="nerva-antonine-sits-above-the-median-gordian-trails-look" class="anchored">Reign years vs median by Dynasty</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emperors/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emperors/charts/chart4_gap.png" role="img" aria-label="Reign years vs median by Dynasty"></div>
</figure>
<p class="art-p">Relative to the file median, Nerva-Antonine sits 12.5 years above; Gordian trails by 4.0. That is the cleanest dynasty-level contrast in the gap chart: one house systematically above the center of the distribution, another systematically below. Gordian is also the most common dynasty label in the fact boxes—volume without longevity. Frequency of naming and length of rule are not the same political achievement. The Nerva-Antonine result aligns with the conventional account of fewer violent turnovers and longer administrative horizons in the second century. A positive gap does not prove the dynasty caused stability, but it matches the historical pattern. The Gordian contrast points to the opposite problem. Gordian I and Gordian II ruled briefly in 238 CE during the Year of the Six Emperors, while Gordian III lasted longer but still belongs to a crisis environment shaped by military pressure and senatorial maneuvering. A repeated dynasty label can mark a famous rupture rather than a durable house.</p>
<h2 id="five-names-carry-forty-percent-of-aggregate-reign-years" class="anchored">Five names carry forty percent of aggregate reign years</h2>
<h3 id="five-names-carry-forty-percent-of-aggregate-reign-years-look" class="anchored">Cumulative Reign years</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/emperors/charts/chart_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/emperors/charts/chart_pareto.png" role="img" aria-label="Cumulative Reign years"></div>
</figure>
<p class="art-p">The top five emperors account for 40% of aggregate reign years in the working file. A steep head means a small set of long rulers dominates the sum, while the long tail of shorter reigns fills out the catalog without moving the total as much. That shape reframes the median. A 6.50-year center can coexist with heavily concentrated aggregate if a few Constantine-scale tenures exist. Both facts are true; they answer different questions. Concentration connects biography to institutions. Long reigns give rulers time to appoint governors, restructure armies, mint ideological programs, build capitals, codify religious settlements, and shape elite careers. Short reigns often leave the opposite signature: coinage, military proclamation, purge, assassination, or succession crisis.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">This is a community-cleaned TidyTuesday snapshot, not a continuously updated classical-history database. Missing values, spelling variants, and week-of-export coverage limits apply. Reign years depend on how start and end dates were recorded and cleaned; disputed chronologies are not adjudicated here.</p>
<p class="art-p">Dynasty labels are editorial categories in the source table. Findings describe the file on hand—structural signals about tenure and dynasty in this emperors extract—not a complete political history of imperial Rome.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The median emperor lasted 6.50 years. Constantine the Great lasted 31.0. Dynasty membership did not flatten that gap. Nerva–Antonine clears the median by 12.5 years; Gordian, despite being the most common dynasty label, trails it by 4.0.</p>
<p class="art-p">Use the charts as three separate instruments—name leaders, dynasty spreads, and concentration—rather than collapsing them into a single verdict. Longevity, frequency, and aggregate share each tell a different part of the succession story.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">Reign spans are derived from start and end dates in the emperors table. Negative or zero spans are excluded. The source is the TidyTuesday Roman Emperors release (2019-08-13), a community-cleaned historical table rather than a live prosopography API.</p>
<p class="art-p">Medians are preferred over means because reign distributions skew—a handful of long rulers pull averages up while the typical emperor sits near the 6.50-year center. Index fields are excluded so charts answer questions about tenure, not spreadsheet order.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2019). <em>TidyTuesday: Roman Emperors</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-08-13/emperors.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-08-13/emperors.csv</a></p>
<p>Data Science Learning Community. (2019). <em>TidyTuesday Roman Emperors source folder</em>. <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-08-13" target="_blank" rel="noopener noreferrer">https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-08-13</a></p>
<p>Boatwright, M. T., Gargola, D. J., Lenski, N., &amp; Talbert, R. J. A. (2012). <em>The Romans: From Village to Empire</em> (2nd ed.). Oxford University Press.</p>
<p>Potter, D. S. (2014). <em>The Roman Empire at Bay, AD 180–395</em> (2nd ed.). Routledge. <a href="https://doi.org/10.4324/9780203080971" target="_blank" rel="noopener noreferrer">https://doi.org/10.4324/9780203080971</a></p>
<p>Ando, C. (2012). <em>Imperial Rome AD 193 to 284: The Critical Century</em>. Edinburgh University Press. <a href="https://edinburghuniversitypress.com/book-imperial-rome-ad-193-to-284.html" target="_blank" rel="noopener noreferrer">https://edinburghuniversitypress.com/book-imperial-rome-ad-193-to-284.html</a></p>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p><em>Artometrics data report from the TidyTuesday research pipeline. Charts and aggregates are reproducible from the embedded exhibits and public source files.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-08-13" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
