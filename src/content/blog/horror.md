---
title: 'HORROR: Horror Ratings Rose as Catalog Volume Grew 50× in Seven Decades'
slug: horror
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: '32,540 horror films from 1950–2022 show median vote average climbed from 5.65 to 6.00 — modest quality gain amid explosive catalog growth.'
dek: "Horror films multiplied 50-fold since 1950. Did they get any better?"
heroImage: /images/content/articles/horror/hero.png
draft: false
tags:
  - arts
  - film
subject: Horror
tldr: '32,540 horror-tagged films from TMDB (1950–2022) carry a median vote average of 4.00. The median rose from 5.65 in early decades to 6.00 by 2022 — a 0.35-point climb as catalog volume expanded. Perfect 10.0 scores cluster at the top, signaling sparse vote counts rather than universal consensus.'
keyPoints:
  - '32,540 — Total horror films analyzed, 1950–2022'
  - 4.00 — Median vote average across entire catalog
  - 0.35 — Increase in median rating from early period (5.65) to close (6.00)
  - '10.0 — Highest observed vote average, shared by multiple low-vote-count titles'
  - +1.00 — Crime-tagged films exceed median; Animation-tagged trail by –4.00
faq:
  - question: How many horror films are in the dataset?
    answer: '32,540 records spanning 1950 through 2022.'
  - question: Did horror quality improve over time?
    answer: 'The median vote average rose 0.35 points (5.65 to 6.00), a modest gain as tens of thousands of new titles entered the catalog.'
  - question: Why do many films score a perfect 10.0?
    answer: Perfect scores often reflect small rater pools rather than broad critical acclaim; low vote counts concentrate enthusiastic niche audiences.
  - question: Which genre tags score highest within horror?
    answer: Crime-tagged horror films average 1.00 point above the median; Animation-tagged films trail by 4.00 points.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">The median vote average for horror films climbed from 5.65 to 6.00 between 1950 and 2022 — a 0.35-point rise across seven decades that added 32,540 titles to the catalog.</p>
<p class="art-p">TMDB metadata for horror-tagged films yields 32,540 records from 1950–2022. The median vote average is 4.00; the highest observed average is 10.0. Horror is the most common primary genre label, as expected in a horror-tagged extract.</p>

<h2 id="how-the-pattern-changed-over-time" class="anchored">How the pattern changed over time</h2>
<h3 id="how-the-pattern-changed-over-time-look" class="anchored">Median Vote average Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/horror/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/horror/charts/chart1_trend.png" role="img" aria-label="Median Vote average Over Time"></div>
</figure>
<p class="art-p">Median vote average rises from 5.65 in the opening period to 6.00 at the close — a 0.35-point lift across decades of catalog growth. Volume exploded while the middle of the scoreboard edged up. More titles filled the shelf; the median shifted modestly upward rather than holding flat or declining.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">The House Guest leads at 10.0 — 10.0 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/horror/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/horror/charts/chart2_leaders.png" role="img" aria-label="The House Guest leads at 10.0 — 10.0 marks the median among the top dozen"></div>
</figure>
<p class="art-p">The House Guest leads at 10.0, and 10.0 also marks the median among the top dozen. The head of the leaderboard is a cluster of perfect averages, not a gentle taper. In large rating tables, that pattern signals low vote counts or niche titles with small, enthusiastic rater pools. The top is a ceiling effect, not a ranked canon.</p>
<h2 id="how-the-field-is-spread" class="anchored">How the field is spread</h2>
<h3 id="how-the-field-is-spread-look" class="anchored">Vote average by Primary genre</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/horror/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/horror/charts/chart3_distribution.png" role="img" aria-label="Vote average by Primary genre"></div>
</figure>
<p class="art-p">Primary-genre boxes reveal whether vote averages converge across hybrid tags or split by outliers. Horror-tagged films carry secondary labels — crime, animation, drama — and those buckets disagree about quality. Consensus is uneven once the tag set widens.</p>
<h2 id="who-beats-the-median-and-who-trails" class="anchored">Who beats the median — and who trails</h2>
<h3 id="who-beats-the-median-and-who-trails-look" class="anchored">Vote average vs median by Primary genre</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/horror/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/horror/charts/chart4_gap.png" role="img" aria-label="Vote average vs median by Primary genre"></div>
</figure>
<p class="art-p">Crime sits 1.00 above the median; Animation trails by 4.00. Those gaps are relative to this file's middle, not absolute statements about every crime or animated horror title. They mark where hybrid labeling and rater pools pull averages apart.</p>
<h2 id="what-moves-together" class="anchored">What moves together</h2>
<h3 id="what-moves-together-look" class="anchored">Vote average vs Vote count</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/horror/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/horror/charts/chart5_scatter.png" role="img" aria-label="Vote average vs Vote count"></div>
</figure>
<p class="art-p">Vote average and vote count do not move as a simple line. Perfect scores with tiny counts sit apart from widely watched mid-range films. Popularity and perceived quality are related but not interchangeable — the scatter shows where that distinction becomes visible.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and week-of-export coverage limits apply. Merged tables may fan out or duplicate rows when join keys are imperfect.</p>
<p class="art-p">Findings describe the file on hand — structural signals about horror-tagged ratings, not a complete history of the genre's artistry.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The median vote average rose 0.35 points (5.65 to 6.00) as the catalog expanded by tens of thousands of titles. Perfect 10.0 leaders reflect sparse vote counts rather than broad acclaim.</p>
<p class="art-p">Read leaders, gaps, and the average–count scatter together before treating any title as proof of a golden age.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The file merges TMDB metadata for thousands of horror-tagged films: ratings, budgets, runtimes, and genre tags from 1950 through 2022, released via TidyTuesday.</p>
<p class="art-p">Charts ship as Plotly JSON with PNG fallbacks. Medians handle skew better than means. Perfect 10.0 scores often sit on thin vote counts — treat the ceiling as a signal about sparse ratings, not universal critical consensus.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2022). <em>TidyTuesday: Horror Movies</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2022/2022-11-01/horror_movies.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2022/2022-11-01/horror_movies.csv</a></p>
</section>
</main>
</div>
