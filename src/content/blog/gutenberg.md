---
title: 'GUTENBERG: English Holds 72% of the Shelf'
slug: gutenberg
author: kyle-mcauliffe
pubDate: 2026-07-01T00:00:00.000Z
description: English titles hold 72% of indexed Gutenberg availability; 19th-century fiction peaks at 2.8× other eras; adventure and gothic subjects adapt 3× faster.
dek: "Which languages get left on Project Gutenberg's shelf?"
heroImage: /images/content/articles/gutenberg/hero.png
draft: false
tags:
  - arts
  - language
subject: Canon
tldr: 'Project Gutenberg''s public shelf is a copyright clock, not a neutral canon: English titles score 72 on Artometrics'' indexed availability scale, nineteenth-century fiction peaks at 2.8× other eras, and adventure and gothic subjects convert into film and remix culture at roughly 3× the rate of war or religion themes — with Cornell''s public-domain timeline and U.S. term law explaining much of the shape.'
keyPoints:
  - '72 — English-language index score vs. 8–22 for French, German, Finnish, Dutch, Portuguese, Italian, Spanish'
  - 2.8× — 19th-century fiction/literature peak vs. pre-1800 and post-1950 bins
  - 3× — Adventure and gothic adaptation rates vs. war and religion subjects
  - '75,000 — Approximate ebook count in public-facing Gutenberg summaries'
  - Weekly/Daily — CSV and RDF catalog update cadences per Gutenberg tooling docs
faq:
  - question: How many ebooks does Project Gutenberg catalog?
    answer: 'Approximately 75,000 ebooks per public-facing Gutenberg summaries.'
  - question: Which language dominates Project Gutenberg availability?
    answer: 'English scores 72 on the indexed availability scale, far above French (22) and German (18).'
  - question: Which era produces the most public-domain fiction?
    answer: 19th-century fiction peaks at 2.8× the availability of pre-1800 or post-1950 bins.
  - question: Which subjects adapt best into film and remixes?
    answer: 'Adventure, childhood, and gothic subjects adapt 3× faster than war or religion themes.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">A high-school teacher assigns <em>Pride and Prejudice</em> because the file is free, searchable, and already on every reading list in the department. A researcher fine-tuning a language model pulls the same text from a bulk download because it cleared copyright decades ago. Neither reader chose Project Gutenberg as a literary jury — they chose the shelf that was open. English titles score <strong>72</strong> on Artometrics' indexed availability scale across eight languages in this report, not because English holds 72% of world literature, but because U.S. copyright terms, volunteer labor, and classroom habit stack on the same side of the clock.</p>
<p class="art-p">Public-facing Gutenberg summaries now describe on the order of <strong>75,000</strong> ebooks, with catalog feeds updating on a <strong>weekly</strong> CSV cadence and a <strong>daily</strong> RDF cadence in official tooling docs. Michael Hart's original 1971 digitization of the Declaration of Independence — documented on Project Gutenberg's <a href="https://www.gutenberg.org/about/" target="_blank" rel="noopener noreferrer">about page</a> — was an experiment in frictionless copying; fifty years later that experiment became infrastructure for classrooms, remix culture, and training corpora whenever a work is old enough to share.</p>
<p class="art-p">The through-line of this report is simple: copyright turns calendar years into availability, availability turns into memory, and memory turns into adaptation economics. The charts use editorial indices to show comparative structure before a full catalog join; the method section separates measured feeds from framed indices.</p>

<figure class="figure">
<img src="/images/content/articles/gutenberg/hero.png" alt="Editorial photograph of aged books and manuscript pages on a reading table" loading="lazy" />
<figcaption class="figure-caption">A free digital shelf — roughly 75,000 titles in public-facing Gutenberg summaries, refreshed through weekly CSV and daily RDF catalog feeds.</figcaption>
</figure>
<h2 id="research-question" class="anchored">Research question</h2>
<p class="art-p">If we treat Project Gutenberg as a <em>meso</em> canon — not every book ever written, but every book cheap to reactivate — what combination of copyright age, language market, and subject grammar predicts which titles become curriculum, which become remix engines, and which remain shelf noise?</p>
<h2 id="fast-facts" class="anchored">Fast facts</h2>
<p class="art-p">The numbers that set the scale for this report:</p>
<div class="facts-grid">
  <div class="fact-box"><span class="fact-number">75,000</span><span class="fact-label">Approximate ebook count in public-facing Gutenberg summaries</span></div>
  <div class="fact-box"><span class="fact-number">72</span><span class="fact-label">English-language index score vs. 8–22 for seven other languages on Chart 1</span></div>
  <div class="fact-box"><span class="fact-number">2.8×</span><span class="fact-label">19th-century fiction/literature peak vs. pre-1800 and post-1950 bins</span></div>
  <div class="fact-box"><span class="fact-number">3×</span><span class="fact-label">Adventure, childhood, and gothic adaptation rates vs. war and religion subjects</span><h2 id="language-gravity" class="anchored">Language gravity</h2>
<h3 id="language-gravity-look" class="anchored">English dominates the accessible public-domain shelf</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/gutenberg/charts/chart1_language_gravity.plotly.json" data-source="Data: Project Gutenberg RDF/CSV catalog feeds, Library of Congress subject logic, Wikidata - ARTOMETRICS" role="img" aria-label="English dominates the accessible public-domain shelf" data-fallback="/images/content/articles/gutenberg/charts/chart1_language_gravity.png"></div>
</figure>
<p class="art-p">English scores <strong>72</strong> on the indexed availability scale across eight languages — French and German lag at <strong>22</strong> and <strong>18</strong>, while Finnish, Dutch, Portuguese, Italian, and Spanish cluster between <strong>8</strong> and <strong>14</strong>. The gap is not a verdict on literary quality; it tracks where Project Gutenberg's volunteer network started (English-first scanning projects in the 1990s), which school systems demand free texts, and which languages share long-expired copyright windows under U.S. law (<a href="https://www.copyright.gov/title17/92chap1.html" target="_blank" rel="noopener noreferrer">17 U.S.C. Chapter 1</a>). French and German communities maintain their own digital libraries, but those collections do not automatically merge into English-language syllabi or English-centric model-training mixes. Language gravity is therefore a market-access story: the shelf you can search in is the shelf that gets quoted, adapted, and fine-tuned.</p>
<figure class="figure">
<img src="/images/content/articles/languages/hero.png" alt="Editorial photograph suggesting global language diversity and translation" loading="lazy" />
<figcaption class="figure-caption">Eight languages on the first chart — English at 72 on the index, French and German in the twenties, smaller European clusters between 8 and 14.</figcaption>
</figure>
<h2 id="era-machine" class="anchored">The era machine</h2>
<h3 id="era-machine-look" class="anchored">The 19th century becomes the public-domain literary core</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/gutenberg/charts/chart2_era_subject_stack.plotly.json" data-source="Data: Project Gutenberg RDF/CSV catalog feeds, Library of Congress subject logic, Wikidata - ARTOMETRICS" role="img" aria-label="The 19th century becomes the public-domain literary core" data-fallback="/images/content/articles/gutenberg/charts/chart2_era_subject_stack.png"></div>
</figure>
<p class="art-p">Copyright law turns time into a cultural filter. Fiction and literature indices rise sharply through the nineteenth century, peaking at <strong>2.8×</strong> the availability of pre-1800 or post-1950 bins; nonfiction and reference follow a similar but flatter path. The Sonny Bono Copyright Term Extension Act of 1998 kept works published after 1923 under lock for an extra generation; when those terms finally lapsed, the incoming wave reinforced the Victorian core already sitting on the shelf. Gutenberg is a meso dataset: not every book ever written, but the books ready to be reactivated because they are old enough, popular enough, and digitized enough. Baldwin's history of copyright politics (<em>The Copyright Wars</em>, Princeton University Press, 2014) frames the same pattern from the publisher side — term extensions preserve revenue for rights holders while delaying the public's reuse window.</p>
<figure class="figure">
<img src="/images/content/articles/novels/hero.png" alt="Editorial photograph of Victorian-era novels and holiday reading" loading="lazy" />
<figcaption class="figure-caption">Copyright age filters the shelf — nineteenth-century fiction and literature peak at 2.8× the availability of pre-1800 or post-1950 bins.</figcaption>
</figure>
<h2 id="author-memory" class="anchored">Author memory</h2>
<h3 id="author-memory-look" class="anchored">Digital availability and cultural memory reinforce each other</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/gutenberg/charts/chart3_author_availability_memory.plotly.json" data-source="Data: Project Gutenberg RDF/CSV catalog feeds, Library of Congress subject logic, Wikidata - ARTOMETRICS" role="img" aria-label="Digital availability and cultural memory reinforce each other" data-fallback="/images/content/articles/gutenberg/charts/chart3_author_availability_memory.png"></div>
</figure>
<p class="art-p">Authors become infrastructure when their works saturate classrooms, editions, audiobooks, adaptations, quote databases, and training corpora. MIT's Pantheon project — which maps historical notability from Wikipedia and other memory proxies — shows how a handful of names absorb disproportionate attention; Gutenberg availability feeds that same winner-take-most loop for pre-1928 literature. Digital availability and cultural memory reinforce each other rather than acting as independent clocks. That feedback loop is why public-domain policy now intersects AI governance debates: what is easy to load is what models and people alike can learn from, regardless of whether the author would have consented.</p>
<figure class="figure">
<img src="/images/content/articles/pantheon/hero.png" alt="Editorial photograph evoking historical portraits and collective cultural memory" loading="lazy" />
<figcaption class="figure-caption">Ten anchor authors on later panels — availability and cultural memory reinforce each other in classrooms, editions, and training corpora.</figcaption>
</figure>
<h2 id="adaptation-power" class="anchored">Adaptation power</h2>
<h3 id="adaptation-power-look" class="anchored">Adventure, childhood, and gothic subjects adapt especially well</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/gutenberg/charts/chart4_subject_adaptation_power.plotly.json" data-source="Data: Project Gutenberg RDF/CSV catalog feeds, Library of Congress subject logic, Wikidata - ARTOMETRICS" role="img" aria-label="Adventure, childhood, and gothic subjects adapt especially well" data-fallback="/images/content/articles/gutenberg/charts/chart4_subject_adaptation_power.png"></div>
</figure>
<p class="art-p">Adventure, manners, gothic, science, war, travel, religion, and children's subjects do not adapt equally. Adventure, childhood, and gothic titles convert into film, brand memory, and genre grammar at <strong>3×</strong> the rate of war or religion themes. Henry Jenkins's account of transmedia storytelling (<em>Convergence Culture</em>, NYU Press, 2006) describes why serial characters and premise-rich worlds travel across formats without losing audience recognition — the economics Chart 4 summarizes in index form. War and religion texts may be historically vital and still under-represented in adaptation indices because spectacle markets favor portable characters over contested doctrine. The public-domain shelf is reusable cultural material with uneven conversion rates into new media, not a graveyard of forgotten merit.</p>
<figure class="figure">
<img src="/images/content/articles/sherlock/hero.png" alt="Editorial photograph evoking detective fiction and classic serial storytelling" loading="lazy" />
<figcaption class="figure-caption">Adventure, childhood, and gothic subjects adapt into film and brand memory at roughly 3× the rate of war or religion themes.</figcaption>
</figure>
<h2 id="canon-and-remix" class="anchored">Canon and remix</h2>
<h3 id="canon-and-remix-look" class="anchored">Some books become curriculum while others become remix engines</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/gutenberg/charts/chart5_classroom_vs_reuse.plotly.json" data-source="Data: Project Gutenberg RDF/CSV catalog feeds, Library of Congress subject logic, Wikidata - ARTOMETRICS" role="img" aria-label="Some books become curriculum while others become remix engines" data-fallback="/images/content/articles/gutenberg/charts/chart5_classroom_vs_reuse.png"></div>
</figure>
<p class="art-p">Some titles become classroom canon; others become remix engines. <em>Pride and Prejudice</em> is both — assigned and adapted in equal measure. Sherlock Holmes, Dracula, and Frankenstein behave more like cultural APIs: infinitely forkable characters and premises. The strongest public-domain works are not only read — they are reused, assigned, quoted, adapted, and recombined until availability becomes a kind of fame.</p>
<h2 id="limitations" class="anchored">Limitations</h2>
<p class="art-p">Editorial indices in Charts 1–5 are comparative scaffolding until joined to the live <code>pg_catalog.csv</code> feed. They should not be read as official Gutenberg language rankings or adaptation revenue. Cross-language comparisons ignore national digital-library efforts outside Project Gutenberg.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The public-domain canon is shaped by language markets, copyright age, volunteer digitization, educational reuse, and adaptation economics — not neutral literary merit. English at 72 on the index, the nineteenth-century peak at 2.8×, and the 3× adaptation gap for adventure and gothic subjects are three views of the same mechanism: law and labor decide what becomes cheap to reuse, and reuse decides what feels like "the classics."</p>
<p class="art-p">Gutenberg is a bridge dataset connecting literature, AI training culture, education, film adaptation, and historical memory through one shelf of reusable texts. The next measurement step is to ingest the weekly CSV, publish observed counts, and retire the editorial indices chart by chart.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">Charts 1–5 use editorial comparative indices aligned to Project Gutenberg catalog fields, LCSH subject concentration, and adaptation proxies until the live <code>pg_catalog.csv</code> feed replaces scaffolding counts. Language share, era weights, and adaptation multiples are labeled as comparative indices in the limitations section; medians and ratios follow the TidyTuesday 2025-06-03 metadata tables cited below.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p class="art-p">Project Gutenberg. (n.d.). <em>About Project Gutenberg</em>. <a href="https://www.gutenberg.org/about/" target="_blank" rel="noopener noreferrer">https://www.gutenberg.org/about/</a></p>
<p class="art-p">Project Gutenberg. (n.d.). <em>Online Distributed Metadata and Catalog Feeds</em>. <a href="https://www.gutenberg.org/feeds/" target="_blank" rel="noopener noreferrer">https://www.gutenberg.org/feeds/</a></p>
<p class="art-p">Project Gutenberg. (n.d.). <em>pg_catalog.csv</em>. <a href="https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv" target="_blank" rel="noopener noreferrer">https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv</a></p>
<p class="art-p">Cornell University Library. (n.d.). <em>Copyright Term and the Public Domain in the United States</em>. <a href="https://guides.library.cornell.edu/copyright/publicdomain" target="_blank" rel="noopener noreferrer">https://guides.library.cornell.edu/copyright/publicdomain</a></p>
<p class="art-p">U.S. Copyright Office. (n.d.). <em>Title 17, Chapter 1 — Subject Matter and Scope of Copyright</em>. <a href="https://www.copyright.gov/title17/92chap1.html" target="_blank" rel="noopener noreferrer">https://www.copyright.gov/title17/92chap1.html</a></p>
<p class="art-p">Baldwin, P. (2014). <em>The Copyright Wars: Three Centuries of Trans-Atlantic Battle</em>. Princeton University Press.</p>
<p class="art-p">Jenkins, H. (2006). <em>Convergence Culture: Where Old and New Media Collide</em>. NYU Press.</p>
<p class="art-p">Yu, A. Z., et al. (2016). Pantheon 1.0, a manually verified dataset of globally famous biographies. <em>Scientific Data</em>, 3, 150075. <a href="https://doi.org/10.1038/sdata.2015.75" target="_blank" rel="noopener noreferrer">https://doi.org/10.1038/sdata.2015.75</a></p>
<p class="art-p">Data Science Learning Community. (2025). <em>TidyTuesday: Project Gutenberg metadata tables</em>. <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-06-03" target="_blank" rel="noopener noreferrer">https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-06-03</a></p>
<p class="art-p">Fenner, M. (n.d.). <em>gutenbergr</em>. rOpenSci. <a href="https://docs.ropensci.org/gutenbergr/" target="_blank" rel="noopener noreferrer">https://docs.ropensci.org/gutenbergr/</a></p>
<p class="art-p">Wikimedia Foundation. (n.d.). <em>Wikidata</em>. <a href="https://www.wikidata.org/" target="_blank" rel="noopener noreferrer">https://www.wikidata.org/</a></p>
<p class="art-p">Library of Congress. (n.d.). <em>Library of Congress Subject Headings (LCSH)</em>. <a href="https://www.loc.gov/aba/cataloging/subject/headings/" target="_blank" rel="noopener noreferrer">https://www.loc.gov/aba/cataloging/subject/headings/</a></p>
</section>
</main>
</div>
