---
title: "GAMES: Crowd Scale Meets Elite Ratings"
slug: games
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  Ratings and popularity across thousands of titles find games that win both
  mass attention and esteem.
dek: "Some games win the crowd. Some win the critics. Which win both?"
heroImage: /images/content/articles/games/hero.png
draft: false
tags:
  - sports
  - gaming
subject: Board Games
tldr: >-
  BoardGameGeek ratings are a public taste machine: tens of thousands of titles,
  each scored by the people willing to log plays. The TidyTuesday games
  extract used here holds 10,532 records with a median average rating of 6.39
  and a high of 9.00 for Small World Designer Edition. Wargame, World War II is
  the most common category label in the file.
keyPoints:
  - '10,532 — Records in the working dataset'
  - 6.39 — Median Average rating
  - 9.00 — Highest observed Average rating
  - Small World Designer Edition — Top Name by Average rating
  - 1970–1970 — Year span covered in the file
  - 'Wargame,World War II — Most common Category'
faq:
  - question: >-
      How many records are in this dataset?
    answer: >-
      10,532 records in the working dataset.
  - question: >-
      What is the median Average rating?
    answer: >-
      The median Average rating is 6.39.
  - question: >-
      What is the highest observed value in this extract?
    answer: >-
      The highest observed value in the extract is 9.00.
  - question: >-
      Which Name leads in this extract?
    answer: >-
      Small World Designer Edition leads the Name ranking in this extract.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">BoardGameGeek ratings are a public taste machine: tens of thousands of titles, each scored by the people willing to log plays. The TidyTuesday games extract used here holds <strong>10,532</strong> records with a median average rating of <strong>6.39</strong> and a high of <strong>9.00</strong> for Small World Designer Edition.</p>
<p class="art-p">Wargame, World War II is the most common category label in the file. That already tilts the catalog toward conflict simulations — a hobby subculture with its own rating norms. The charts ask how ratings split by category, how leaders separate from the median, and whether crowdfunding-scale user counts track with elite scores.</p>

<h2 id="the-catalog-s-median-rating-sits-near-6-39" class="anchored">The Catalog’s Median Rating Sits Near 6.39</h2>
<h3 id="the-catalog-s-median-rating-sits-near-6-39-look" class="anchored">Median Average rating Over Time</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/games/charts/chart1_trend.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/games/charts/chart1_trend.png" role="img" aria-label="Median Average rating Over Time"></div>
</figure>
<p class="art-p">The time view in this extract collapses to a median average rating of about <strong>6.39</strong> — the same calibration point as the fact box. In BoardGameGeek terms, that mid-6s band is ordinary: playable, not legendary. Everything that follows should be read against that baseline. A 9.00 specialty edition is not “a bit better than average”; it is a different prestige tier.</p>
<h2 id="designer-editions-and-heavy-games-own-the-peak" class="anchored">Designer Editions and Heavy Games Own the Peak</h2>
<h3 id="designer-editions-and-heavy-games-own-the-peak-look" class="anchored">Small World Designer Edition leads at 9.00 — 8.78 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/games/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/games/charts/chart2_leaders.png" role="img" aria-label="Small World Designer Edition leads at 9.00 — 8.78 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Small World Designer Edition leads at <strong>9.00</strong>. Kingdom Death: Monster (~<strong>8.93</strong>), Terra Mystica: Big Box (~<strong>8.85</strong>), and a run of deep wargames — Last Chance for Victory, The Greatest Day, Last Blitzkrieg, Enemy Action: Ardennes — fill out the top dozen. The median among those leaders is about <strong>8.78</strong>. These are not mass-market party games. They are hobby-complete objects — big boxes, campaign systems, hex-and-counter epics — rated by audiences selected for intensity.</p>
<h2 id="wargame-categories-rate-higher-than-card-games" class="anchored">Wargame Categories Rate Higher Than Card Games</h2>
<h3 id="wargame-categories-rate-higher-than-card-games-look" class="anchored">Average rating by Category</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/games/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/games/charts/chart3_distribution.png" role="img" aria-label="Average rating by Category"></div>
</figure>
<p class="art-p">Category boxes show Napoleonic wargames with a median near <strong>7.04</strong> (n=124) and World War II wargames near <strong>6.89</strong> (n=449). Card games sit lower, with a median near <strong>6.03</strong> (n=438). Abstract strategy lands near <strong>6.28</strong> (n=284). Volume and prestige diverge: card games are numerous but center closer to the catalog median; dedicated wargame labels clear a higher bar among the people who rate them.</p>
<h2 id="civil-war-and-napoleonic-titles-beat-the-median-most" class="anchored">Civil War and Napoleonic Titles Beat the Median Most</h2>
<h3 id="civil-war-and-napoleonic-titles-beat-the-median-most-look" class="anchored">Average rating vs median by Category</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/games/charts/chart4_gap.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/games/charts/chart4_gap.png" role="img" aria-label="Average rating vs median by Category"></div>
</figure>
<p class="art-p">Gaps to the overall median are largest for American Civil War wargames (~<strong>+0.66</strong>) and Napoleonic wargames (~<strong>+0.65</strong>), with World War II wargames also positive. Dice and generic card-game labels sit below the median. The pattern is consistent: historical conflict simulations, as tagged in this file, are the categories that most reliably clear the 6.39 baseline.</p>
<h2 id="crowd-size-and-rating-are-related-loosely" class="anchored">Crowd Size and Rating Are Related — Loosely</h2>
<h3 id="crowd-size-and-rating-are-related-loosely-look" class="anchored">Average rating vs Users rated</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/games/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/games/charts/chart5_scatter.png" role="img" aria-label="Average rating vs Users rated"></div>
</figure>
<p class="art-p">Average rating versus users rated shows popular hits with tens of thousands of ratings landing across the mid-to-high 7s, while many high-rated titles still have modest user counts. Elite scores without crowd scale remain possible. The scatter’s lesson is citable: popularity predicts attention, not a precise quality score. A 9.00 designer edition and a 7.4 smash hit solve different problems in the hobby economy.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">BoardGameGeek ratings are self-selected by hobbyists; children’s games and mass-market titles can be systematically under- or over-represented. Multi-label categories double-count games across boxes.</p>
<p class="art-p">Expansions and designer editions inflate prestige relative to base games. The file is a 2019 community snapshot, not a live BGG API pull.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Across 10,532 games, the median rating is 6.39; the top dozen lives near 8.8–9.0. Wargame categories clear the baseline more often than broad card-game labels.</p>
<p class="art-p">Cite 6.39 as the catalog’s center of gravity, and treat 9.00 specialty editions as a separate prestige economy — not as proof that “games got better.”</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2019-03-12 (board_games.csv). After cleaning, 10,532 rows remain in the working frame.</p>
<p class="art-p">Average rating is the primary metric. Category fields can be multi-label strings. Charts are Plotly JSON with PNG fallbacks. The year span encoded in the fact box reflects the filtered time field present in this build of the file.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2019). <em>TidyTuesday: Board Games</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-03-12/board_games.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-03-12/board_games.csv</a></p>
</section>
</main>
</div>
