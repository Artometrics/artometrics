---
title: 'PIXAR: Pixar''s Critic Scores Broke Only Twice—Cars 2 and Lightyear'
slug: pixar
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: 'Pixar''s median Rotten Tomatoes score is 96%, but Cars 2 hit 40% and Lightyear stalled the streak—data from 24 rated theatrical features.'
dek: "Pixar almost never misses with critics. Two films did."
heroImage: /images/content/articles/pixar/hero.png
draft: false
tags:
  - arts
  - film
subject: Pixar
tldr: 'Pixar maintained a 96% median Rotten Tomatoes score across 24 rated theatrical releases, but two films—Cars 2 (40%) and Lightyear—broke the streak. Runtimes climbed 17 minutes between early and recent eras, while CinemaScore grades stayed at A+. TidyTuesday 2025-03-11 data shows 27 features, audience affection remained stable even as critic scores split.'
keyPoints:
  - 96% — Median Rotten Tomatoes score — Pixar's critical baseline across rated theatrical releases
  - 40% — Cars 2's Rotten Tomatoes floor — the studio's lowest critic mark
  - +17 minutes — Median runtime gain from early era to 2017–present — structural shift in feature length
  - A+ — Most common CinemaScore grade — opening-weekend audiences rarely graded below A
  - 155 minutes — Longest runtime in the dataset — 81 minutes was Toy Story's floor
  - 0 — PG-13 ratings in this theatrical set — Pixar held the all-ages lane
faq:
  - question: What is Pixar's median Rotten Tomatoes score?
    answer: 96% across 24 rated theatrical releases—elite by studio standards.
  - question: Which Pixar film has the lowest critic score?
    answer: 'Cars 2 at 40% on Rotten Tomatoes, the studio''s critical floor.'
  - question: Did Pixar films get longer over time?
    answer: 'Yes—median runtime rose 17 minutes from the early era to 2017–present, from 98 to 116 minutes.'
  - question: What is the most common CinemaScore grade for Pixar?
    answer: A+—opening-weekend audiences consistently rated films at the top tier.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Pixar holds a 96% median Rotten Tomatoes score across 24 rated theatrical releases, but two films broke the streak: Cars 2 at 40% and Lightyear. The studio stretched runtimes by 17 minutes between early and recent eras while CinemaScore grades held at A+—audiences stayed loyal even when critics split.</p>
<p class="art-p">This analysis joins TidyTuesday 2025-03-11 Pixar films data with public_response scores: 27 theatrical features, 24 with critic and audience metrics attached. Five charts trace runtime creep, critic floors, audience-critic gaps, rating mix, and the relationship between length and reception.</p>
<p class="art-p">Calibration points: a <strong>96%</strong> median Rotten Tomatoes score; Cars 2 at <strong>40%</strong>; <strong>+17</strong> minutes added to median runtime from early to recent eras; CinemaScore grades clustering at <strong>A+</strong>; a longest runtime of <strong>155</strong> minutes; Toy Story's <strong>81</strong>-minute floor; and <strong>zero</strong> PG-13 ratings in the theatrical set.</p>

<h2 id="runtime-creep" class="anchored">Runtime Creep</h2>
<h3 id="runtime-creep-look" class="anchored">Runtime Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pixar/charts/chart1_runtime_timeline.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pixar/charts/chart1_runtime_timeline.png" role="img" aria-label="Runtime Over Time"></div>
</figure>
<p class="art-p">Pixar's theatrical releases did not stay the compact 81-minute package of Toy Story. Median runtime climbed from 98 minutes (through 2006) to 116 minutes for films since 2017—a structural shift in what a Pixar feature is allowed to be. The longest entry runs 155 minutes. Early films clustered around 98 minutes; recent releases expanded by 17 minutes at the median. The change is not noise—it is embedded in the studio's evolving production model.</p>
<h2 id="critic-scores" class="anchored">Critic Scores</h2>
<h3 id="critic-scores-look" class="anchored">Rotten Tomatoes Ranking</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pixar/charts/chart2_rt_ranking.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pixar/charts/chart2_rt_ranking.png" role="img" aria-label="Rotten Tomatoes Ranking"></div>
</figure>
<p class="art-p">The median Rotten Tomatoes score across rated films is 96%—elite by any studio standard. Pixar built a reputation on consistency, not occasional brilliance. Cars 2 sits at 40%, the critic floor. Toy Story and several sequels hit 100%. The spread is narrow by Hollywood standards, but the low end clusters around mid-2000s franchise experiments and later IP-forward releases.</p>
<h2 id="audience-vs-critics" class="anchored">Audience vs Critics</h2>
<h3 id="audience-vs-critics-look" class="anchored">Critics vs CinemaScore</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pixar/charts/chart3_critic_audience_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pixar/charts/chart3_critic_audience_gap.png" role="img" aria-label="Critics vs CinemaScore"></div>
</figure>
<p class="art-p">CinemaScore grades cluster at A and A+ across the board. Audiences who showed up opening weekend were rarely disappointed—or at least rarely admitted it on exit polls. Critics were the discriminating layer. Films that earned A+ crowd grades still span a 74–100% Rotten Tomatoes range. Pixar optimized for mass affection first, prestige second.</p>
<h2 id="rating-mix" class="anchored">Rating Mix</h2>
<h3 id="rating-mix-look" class="anchored">MPAA Rating Mix</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pixar/charts/chart4_rating_mix.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pixar/charts/chart4_rating_mix.png" role="img" aria-label="MPAA Rating Mix"></div>
</figure>
<p class="art-p">Thirteen films carry a G rating; ten are PG. The brand's family positioning is embedded in the rating structure—zero titles in this file carry PG-13. Pixar expanded runtime and thematic weight without abandoning the all-ages lane in the theatrical set on hand.</p>
<h2 id="runtime-vs-reception" class="anchored">Runtime vs Reception</h2>
<h3 id="runtime-vs-reception-look" class="anchored">Runtime vs Rotten Tomatoes</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pixar/charts/chart5_runtime_vs_rt.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pixar/charts/chart5_runtime_vs_rt.png" role="img" aria-label="Runtime vs Rotten Tomatoes"></div>
</figure>
<p class="art-p">Longer films do not automatically score worse—Up, Wall-E, and Inside Out combine runtimes above 95 minutes with scores above 95%. The outliers sit in the lower-right and upper-left: Cars 2 (shorter, weaker Rotten Tomatoes) versus epics that tested patience and still won. Bubble size tracks Metacritic where available—the reception stack is consistent across review systems.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Reception scores are snapshots from Wikipedia-curated tables, not live API pulls. Rotten Tomatoes percentages can shift as reviews are added. CinemaScore is ordinal, not interval—treat cross-film comparisons as directional.</p>
<p class="art-p">The dataset ends with the films included in the March 2025 TidyTuesday release. It does not include Disney+ exclusives or shorts. Runtime and rating analysis covers theatrical features only.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Pixar's measurable story is stability with drift: critics stayed harsh at the margins (Cars 2 at 40%), audiences stayed generous (A+ CinemaScores), and runtimes marched upward (+17 minutes at the median between eras). The brand did not break—it stretched.</p>
<p class="art-p">The myth is magic; the data is a studio learning it could ask for more minutes, more sequels, and still keep the crowd on its side.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The core file pixar_films.csv lists theatrical features with release date, runtime, and MPAA rating. The companion public_response.csv adds Rotten Tomatoes, Metacritic, CinemaScore, and Critics' Choice scores. Three recent releases lack complete reception fields—treat absent values as missing data, not zero-quality signals.</p>
<p class="art-p">This is not box-office data. The TidyTuesday readme points to a separate box_office extract in the {pixarfilms} R package for revenue analysis. Reception and runtime are the focus here because they are complete in-repo.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2025). <em>TidyTuesday: Pixar Films</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-03-11/pixar_films.csv" target="_blank" rel="noopener noreferrer">pixar_films.csv</a>; <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-03-11/public_response.csv" target="_blank" rel="noopener noreferrer">public_response.csv</a>. Original pixarfilms R package by Eric Leung.</p>
<h2 id="editor-s-note" class="anchored">Editor's note</h2>

<div class="art-editorial-note"><p><em>This report replaces the initial batch-generated Pixar draft with a hand-tuned analysis joining both TidyTuesday files. Charts use Artometrics styling and Plotly JSON exports.</em></p></div>
<p class="art-github-wrap"><a class="art-github-btn" href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-03-11" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a></p>
</section>
</main>
</div>
