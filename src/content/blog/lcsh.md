---
title: "LCSH: 69,027 Headings Anchor Gutenberg's Core"
slug: lcsh
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: LCSH accounts for 69% of subject headings; PS (American literature) appears 4,684 times — concentration defines the reusable public-domain canon.
dek: "Most subject headings in Project Gutenberg appear exactly once. A few appear thousands of times."
heroImage: /images/content/articles/lcsh/hero.png
draft: false
tags:
  - arts
  - language
subject: Gutenberg
tldr: >-
  A 100,000-record TidyTuesday extract shows Library of Congress Subject Headings (lcsh) accounting for 69,027 entries — 69% of all subjects. A small set of codes — PS at 4,684 instances — recurs thousands of times while most labels appear once, revealing which public-domain works volunteers digitized and classified at scale.
keyPoints:
  - '69,027 — lcsh records dominate the 100,000-row dataset, defining the catalog core'
  - '4,684 — PS (American literature) subject appearances, the most repeated label'
  - 'Power-law distribution — most subjects appear once; a reusable canon of headings anchors repeated use'
faq:
  - question: >-
      How many Project Gutenberg records use LCSH subject headings?
    answer: >-
      69,027 of 100,000 records in the TidyTuesday extract use lcsh as the subject type.
  - question: >-
      Which subject code appears most often in Project Gutenberg?
    answer: >-
      PS (American literature) appears 4,684 times, more than any other subject label.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Library of Congress Subject Headings (lcsh) account for 69,027 records in a 100,000-row TidyTuesday extract of Project Gutenberg — 69% of all subject entries. The catalog is not a popularity contest; it is a map of which public-domain books volunteers could digitize and classify at scale.</p>
<p class="art-p">Subject code <strong>PS</strong> — American literature — recurs <strong>4,684</strong> times, leading all labels. A short head of repeated classifications anchors the catalog while most subject entities appear once. The pattern is typical of library metadata: a reusable canon of headings, and a long inventory of singleton assignments.</p>
<p class="art-p">Reading Gutenberg as a concentration map of reusable works is where the data help.</p>

<h2 id="landscape" class="anchored">Public-domain books cluster by subject type</h2>
<h3 id="landscape-look" class="anchored">Public-domain books cluster by subject type</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lcsh/charts/chart1_category.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lcsh/charts/chart1_category.png" role="img" aria-label="Public-domain books cluster by subject type"></div>
</figure>
<p class="art-p"><strong>lcsh</strong> dominates with <strong>69,027</strong> records, far ahead of thinner subject-type buckets. The main classification family carries the story; this field does not split into many equal long-tail types. That concentration means most navigational claims about what Gutenberg contains are really claims about how LCSH-style headings organize the digitized shelf.</p>
<h2 id="who-sits-at-the-top" class="anchored">A small set of subjects anchors the catalog</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">A small set of subjects anchors the catalog</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lcsh/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lcsh/charts/chart2_leaders.png" role="img" aria-label="A small set of subjects anchors the catalog"></div>
</figure>
<p class="art-p"><strong>PS</strong> appears <strong>4,684</strong> times — the most recurring subject name in the file. The top dozen account for a visible share of all 100,000 rows even though most subject entities appear only once. American literature codes, fiction labels, and related headings form a reusable core. They are the catalog's gravitational center for teachers, scrapers, and adaptation hunters.</p>
<h2 id="category" class="anchored">Subject families show the catalog center of gravity</h2>
<h3 id="category-look" class="anchored">Subject families show the catalog's center of gravity</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lcsh/charts/chart3_category.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lcsh/charts/chart3_category.png" role="img" aria-label="Subject families show the catalog's center of gravity"></div>
</figure>
<p class="art-p">lcsh is again the largest bucket on the category chart. Subject families show where editorial attention should focus first if the goal is to understand the shelf's center of gravity rather than its exotic edges. The edges still matter for discovery. They do not define the statistical middle of a 100,000-row extract.</p>
<h2 id="frequency" class="anchored">Repeated subjects reveal the reusable canon</h2>
<h3 id="frequency-look" class="anchored">Repeated subjects reveal the reusable canon</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lcsh/charts/chart5_frequency.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lcsh/charts/chart5_frequency.png" role="img" aria-label="Repeated subjects reveal the reusable canon"></div>
</figure>
<p class="art-p">Most subject entities appear only once; a small head recurs repeatedly. That power-law shape is typical of catalog tables: a reusable canon of headings, and a long inventory of singleton classifications. Repeated subjects are the ones most likely to support classroom packs, themed collections, and machine-learning corpora. Frequency is a reuse forecast as much as a shelf description.</p>
<h2 id="names" class="anchored">Subject labels become the map of the shelf</h2>
<h3 id="names-look" class="anchored">Subject labels become the map of the shelf</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/lcsh/charts/chart_top_names.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/lcsh/charts/chart_top_names.png" role="img" aria-label="Subject labels become the map of the shelf"></div>
</figure>
<p class="art-p">PS and related labels become the map of the shelf when numeric scores are sparse. Frequency leaders reveal franchise depth in literature the way studio logos reveal franchise depth in film. The practical claim for cultural analytics is simple: if you can only afford to study a slice of Gutenberg, the repeated subject head is where coverage of the reusable public-domain canon begins.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and sampling limits apply. Subject headings are not sales, downloads, or reading-time proof.</p>
<p class="art-p">Findings describe structural signals about Project Gutenberg subject metadata — not a complete history of world literature, and not a ranking of artistic merit.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Gutenberg's subject catalog is concentrated: lcsh dominates subject type, a short head of codes such as PS recurs thousands of times, and most labels appear once.</p>
<p class="art-p">The citable lesson is about reusable canon. Public-domain literature becomes infrastructure when classification and digitization make the same subjects easy to find again and again.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday Project Gutenberg release from the R for Data Science community. The working file contains 100,000 rows after assembly — subject types, subject labels, and related catalog metadata.</p>
<p class="art-p">Because many fields are categorical, the analysis leans on counts and repetition rather than a single quality score. Charts export as Plotly JSON with PNG fallbacks. Subject headings are librarian infrastructure, not reader reviews.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p class="art-p">Data Science Learning Community. (2025). <em>TidyTuesday: Project Gutenberg</em> (curated via {lcshr}). <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-06-03" target="_blank" rel="noopener noreferrer">https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-06-03</a></p>
<p class="art-p">Data Science Learning Community. (2025). <em>TidyTuesday: lcsh_subjects.csv</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/lcsh_subjects.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/lcsh_subjects.csv</a> — subject types and labels (lcsh, lcc, and related fields) used for the counts in this report.</p>
<p class="art-p">Fenner, M. (n.d.). <em>lcshr: Download and Process Public Domain Works from Project Gutenberg</em>. rOpenSci. <a href="https://docs.ropensci.org/lcshr/" target="_blank" rel="noopener noreferrer">https://docs.ropensci.org/lcshr/</a></p>
<p class="art-p">Project Gutenberg. (n.d.). <em>Project Gutenberg</em>. <a href="https://www.gutenberg.org/" target="_blank" rel="noopener noreferrer">https://www.gutenberg.org/</a></p>
<p class="art-p">Library of Congress. (n.d.). <em>Library of Congress Subject Headings (LCSH)</em>. <a href="https://www.loc.gov/aba/cataloging/subject/headings/" target="_blank" rel="noopener noreferrer">https://www.loc.gov/aba/cataloging/subject/headings/</a></p>
</section>
</main>
</div>
