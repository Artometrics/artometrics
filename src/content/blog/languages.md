---
title: 'LANGUAGES: Glottolog''s 8,612 Records Map Fieldwork, Not Where People Speak'
slug: languages
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: '2,363 of 8,612 language records sit in Africa''s macroarea bucket — a signal of documentation density, not speaker counts.'
dek: "Glottolog's map shows where linguists have looked, not where people talk."
heroImage: /images/content/articles/languages/hero.png
draft: false
tags:
  - arts
  - language
subject: Languages
tldr: 'A TidyTuesday Glottolog extract shows 8,612 language records clustered by region: 2,363 in Africa, with most language names appearing once while a short head repeats. The file maps documentation effort — where grammars, identifiers, and fieldwork concentrate — not the lived geography of speech communities.'
keyPoints:
  - '2,363 — Africa records in 8,612-row extract — 27% of total catalog visibility'
  - '8,612 — Total records in working file — singleton majority, repeated-name minority'
  - 'Fasu — Top recurring name — reflects dialect clusters and alternate glottonyms, not speaker count'
faq:
  - question: How many language records are in the Glottolog extract?
    answer: '8,612 records after cleaning, drawn from the December 2025 TidyTuesday release.'
  - question: Why does Africa lead in record count?
    answer: 'Africa holds 2,363 records (27%), reflecting dense family documentation and fieldwork history, not raw speaker population.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">2,363 of 8,612 language records in a Glottolog-derived TidyTuesday extract sit in the Africa macroarea bucket — 27% of the catalog. The concentration maps documentation density — where grammars, identifiers, and fieldwork accumulate — not the lived geography of speech.</p>
<p class="art-p">The working file holds 8,612 records. Africa is the largest macroarea at 2,363 entries; most language names appear once while a short head repeats. Row counts are not speaker counts, and macroarea labels are database shortcuts, not political borders.</p>
<p class="art-p">A language catalog is also an archive of scholarly attention. Regions with denser fieldwork traditions show higher row counts even when underlying human diversity is more even — or more endangered — than the table suggests.</p>
<h2 id="research-question" class="anchored">Research question</h2>
<p class="art-p">What does a Glottolog-derived catalog reveal about the geography of linguistic documentation, not the geography of language itself? This report asks where the 8,612-record extract concentrates by macroarea, where names and identifiers repeat, and how much of the visible language map is shaped by catalog infrastructure.</p>
<p class="art-p">The question is observational because row counts are not speaker counts, vitality scores, or political claims. The aim is to distinguish language diversity as lived by communities from language visibility as preserved in databases, grammars, ISO-style identifiers, and scholarly citation systems.</p>

<h2 id="landscape" class="anchored">A geographically uneven landscape</h2>
<h3 id="landscape-look" class="anchored">Language documentation is geographically uneven</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/languages/charts/chart1_category.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/languages/charts/chart1_category.png" role="img" aria-label="Language documentation is geographically uneven"></div>
</figure>
<p class="art-p">Africa dominates with 2,363 records in the primary macroarea cut. Other macroareas — Papunesia, Eurasia, the Americas, Australia — follow at lower counts. The main bucket carries 27% of the story; this field does not behave like a gentle long-tail split across dozens of equal regions. Uneven documentation is not identical to uneven linguistic diversity, but it shapes what comparative science can see. Extinction risk, revitalization, and typology research all inherit the map of what has been recorded. Africa's lead is plausible in linguistic terms: the continent contains large families such as Niger-Congo, Afro-Asiatic, Nilo-Saharan groupings as traditionally defined, and Khoisan-associated lineages, alongside intense contact zones and multilingual states. But the chart does not validate any particular family taxonomy; it records how the Glottolog-style file assigns macroarea metadata to rows. Papunesia and Australia are especially important comparison cases because they contain many small language communities with high typological diversity and severe endangerment pressure. A lower row count than Africa does not mean lower scientific importance. It means the record is distributed unevenly across regions, fieldwork histories, and naming conventions.</p>
<h2 id="who-sits-at-the-top" class="anchored">Who sits at the top of name repetition</h2>
<h3 id="who-sits-at-the-top-look" class="anchored">Repeated language names show documentation density</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/languages/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/languages/charts/chart2_leaders.png" role="img" aria-label="Repeated language names show documentation density"></div>
</figure>
<p class="art-p">Fasu appears among the recurring names in the file; the top dozen account for a visible share of all 8,612 rows even though most languages appear only once. Name repetition can reflect dialect documentation, alternate glottonyms, or multiple database entries tied to related varieties. Fasu is a Papuan language name associated with Papua New Guinea, and its recurrence is a reminder that catalog entries are not always one-to-one with what a lay reader calls a language. Varieties, dialect clusters, alternate names, bibliographic records, and genealogical nodes can all push the same surface name into repeated view. This is where Glottolog's infrastructure differs from a census. A national census might ask who speaks a language at home; Glottolog asks how a language or lineage is classified and documented in the linguistic literature. The same community can be highly visible in one system and nearly invisible in another.</p>
<h2 id="category" class="anchored">Regional concentration</h2>
<h3 id="category-look" class="anchored">Regional concentration shapes the language map</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/languages/charts/chart3_category.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/languages/charts/chart3_category.png" role="img" aria-label="Regional concentration shapes the language map"></div>
</figure>
<p class="art-p">Africa is again the largest bucket with 2,363 records on the regional concentration chart. Category concentration shows where editorial and scientific attention should look first if the goal is to understand the file's center of gravity. Mixed macroarea labels in the data — combinations such as Eurasia with Papunesia — remind readers that languages and contact zones do not always respect tidy continental borders. The macroarea scheme is a practical database compromise. Eurasia contains Indo-European, Uralic, Turkic, Sino-Tibetan, Japonic, Koreanic, Dravidian, and many other lineages; the Americas contain hundreds of Indigenous languages with colonial-era documentation gaps; Papunesia compresses a spectacularly dense set of Papuan and Austronesian histories into one label. The labels help chart structure, but they are not theory in themselves. Regional concentration also encodes academic history. Missionary grammars, colonial surveys, national language academies, SIL International work, university field programs, and contemporary community-led documentation all leave traces in catalogs. The chart is therefore a map of evidence output as much as a map of human speech.</p>
<h2 id="frequency" class="anchored">Most languages appear once</h2>
<h3 id="frequency-look" class="anchored">Most languages appear once while a small head repeats</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/languages/charts/chart5_frequency.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/languages/charts/chart5_frequency.png" role="img" aria-label="Most languages appear once while a small head repeats"></div>
</figure>
<p class="art-p">Most name entities appear only once; a small head revisits repeatedly. That power-law shape is typical of catalog-style tables: a few repeatedly documented varieties, and a long inventory of singleton entries. For endangered-language work, the singleton majority is the point. Visibility in a database is already a scarce resource; languages that appear once may still be under-described relative to their social importance. A singleton entry can represent a language with thousands of speakers, a severely endangered variety with only elders remaining, or a poorly documented name whose classification remains uncertain. Without speaker counts, vitality levels, and bibliographic depth, the frequency chart should be read as documentation structure, not community scale. UNESCO's language vitality framework and Ethnologue-style speaker estimates answer different questions than Glottolog identifiers. The chart is valuable precisely because it shows the catalog layer that those other systems need to join against before scholars can ask about endangerment, education policy, or intergenerational transmission.</p>
<h2 id="mix" class="anchored">Identifiers as metadata</h2>
<h3 id="mix-look" class="anchored">Identifier fields are metadata rather than a reader-facing thesis</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/languages/charts/chart_extra_mix.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/languages/charts/chart_extra_mix.png" role="img" aria-label="Identifier fields are metadata rather than a reader-facing thesis"></div>
</figure>
<p class="art-p">Glottolog-style IDs such as fasu1242 are the most repeated identifiers in the extract. Secondary dimensions add context when the primary table has no numeric score column — they are join keys for typology databases, not a popularity contest. Reading IDs as if they were rankings misunderstands the infrastructure. The useful claim is that documentation systems create machine-readable handles that make some languages easier to cite, map, and study than others. Identifier fields are the quiet machinery of comparative linguistics. Glottocodes such as fasu1242, ISO 639-3 codes, and family IDs let researchers connect grammars, lexicons, sound inventories, phylogenies, and geographic coordinates without relying on unstable spelling variants. The identifier is not the language; it is the database handle that lets the language remain findable. That infrastructure has real consequences. A language with a stable identifier can be linked into typological databases such as WALS, Glottolog, PHOIBLE, or Grambank more easily than a language whose names are fragmented across archives. Machine readability becomes a form of scholarly visibility.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Community-cleaned TidyTuesday snapshots are not live APIs. Missing values, spelling variants, and release coverage limits apply. Row counts are not speaker counts, and macroarea labels are not political maps.</p>
<p class="art-p">The file cannot by itself measure vitality, endangerment, or intergenerational transmission. It measures documentation structure — a necessary but incomplete layer of the global language story.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">World linguistic diversity, as seen through this Glottolog-derived extract, is geographically lumpy: Africa leads the macroarea counts at 2,363 of 8,612 records, while most language names appear once.</p>
<p class="art-p">The citable lesson is about visibility. What scholars can count depends on where fieldwork and cataloging have been dense — and that density is itself a cultural and scientific fact.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from December 23, 2025 (R for Data Science community). The working file contains 8,612 rows and 9 columns after cleaning — language names, identifiers, macroarea labels, and related Glottolog metadata.</p>
<p class="art-p">Because many fields are categorical rather than scored, the analysis leans on counts, concentration, and repetition rather than medians of a single numeric quality metric. Charts export as Plotly JSON with PNG fallbacks.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2025). <em>TidyTuesday: Glottolog / language data</em>. <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-12-23" target="_blank" rel="noopener noreferrer">https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-12-23</a></p>
<p>Hammarström, H., Forkel, R., Haspelmath, M., &amp; Bank, S. <em>Glottolog</em>. Max Planck Institute for Evolutionary Anthropology. <a href="https://glottolog.org/" target="_blank" rel="noopener noreferrer">https://glottolog.org/</a></p>
<p>UNESCO. <em>Atlas of the World's Languages in Danger</em>. <a href="https://www.unesco.org/languages-atlas/" target="_blank" rel="noopener noreferrer">https://www.unesco.org/languages-atlas/</a></p>
<p>Dryer, M. S., &amp; Haspelmath, M. (Eds.). <em>The World Atlas of Language Structures Online</em>. <a href="https://wals.info/" target="_blank" rel="noopener noreferrer">https://wals.info/</a></p>
<p>Skirgård, H., et al. (2023). Grambank reveals the importance of genealogical constraints on linguistic diversity and highlights the impact of language loss. <em>Science Advances</em>, 9(16). <a href="https://doi.org/10.1126/sciadv.adg6175" target="_blank" rel="noopener noreferrer">https://doi.org/10.1126/sciadv.adg6175</a></p>
</section>
</main>
</div>
