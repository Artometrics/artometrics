---
title: 'POKEMON: Dragon-types Earn Their Attack Stats—Bug-types Don''t Recover'
slug: pokemon
author: kyle-mcauliffe
pubDate: 2026-05-06T00:00:00.000Z
description: 'Game Freak''s type system encodes stat tradeoffs, power creep clusters at the tail, and Cosmoem weighs 999.9 kg at 0.1 meters.'
heroImage: /images/content/articles/pokemon/hero.png
draft: false
tags:
  - sports
  - gaming
subject: Pokémon
tldr: 'Dragon-types post a median Attack of 100 with no stat below 80. Bug-types sit at 60 across the board. The type system isn''t flavor — it''s a stat schema Game Freak has enforced across 949 Pokémon and nine generations. Power creep exists, but it concentrates in the tail: each generation adds extreme outliers while the median holds. Cosmoem, Wailord, and Celesteela violate the size grammar deliberately — the scatter plot isolates them as design decisions, not statistical accidents.'
keyPoints:
  - '100 — Median Attack for Dragon-types, the stat-elite generalist with no weakness below 80'
  - '60 — Bug-types'' median across all six stats, the lowest-tuned primary type in the dataset'
  - '116 — Steel-types'' median Defense, the single highest stat cell on the heatmap'
  - '999.9 kg — Cosmoem''s weight at 0.1 meters tall, the most extreme density outlier in 1,028 records'
  - '157 — Median base experience across all Pokémon, stable from Gen 1 to Gen 7'
  - '510 — Pokémon with a second type, showing dual-typing as the majority design pattern'
faq:
  - question: Do Dragon-types actually have higher stats than other types?
    answer: 'Yes — Dragon-types post a median Attack of 100 and no single stat below 80, making them the highest-statted generalist type in the dataset.'
  - question: Has Pokémon power creep happened across generations?
    answer: 'The median base experience holds stable, but each generation adds extreme outliers at the high end — the ceiling rises while the center stays put.'
  - question: Why does Cosmoem weigh so much?
    answer: It's a design decision — 999.9 kg at 0.1 meters violates the size grammar to signal cosmic otherness before you check its stats.
  - question: Are Bug-types actually the weakest type?
    answer: 'By base stats, yes — Bug-types post the lowest or near-lowest medians across all six stats, a pattern that has held since Generation I.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Dragon-types post a median Attack of 100 and no stat below 80. Bug-types sit at 60 across the board. The difference isn't lore — it's the stat schema Game Freak has enforced across 949 Pokémon and nine generations. The franchise looks like a cultural phenomenon. The PokéAPI-derived TidyTuesday dataset shows it's a design system with measurable rules, deliberate specialists, and power creep that concentrates in the tail rather than the median.</p>
<p class="art-p">The TidyTuesday 2025-04-01 Pokémon dataset covers every Pokémon through Generation IX. Three questions land cleanly: Do different types actually play differently, or is that a perception? Has Game Freak been inflating Pokémon power over time? And what does physical size reveal about how Pokémon are designed?</p>
<h2 id="research-question" class="anchored">Research question</h2>
<p class="art-p">Can Pokémon's creature design be measured as a system rather than described only as franchise lore? This report asks whether primary type, generation, base experience, height, and weight reveal consistent design rules across the PokéAPI-derived TidyTuesday dataset.</p>
<p class="art-p">The observational question is practical: do Dragon, Steel, Fighting, Bug, Water, and other types carry statistically distinct stat identities; does the upper tail of base experience creep across generations; and do physical dimensions follow a coherent size grammar with deliberate exceptions such as Cosmoem and Wailord?</p>

<h2 id="stat-identity-by-type" class="anchored">Stat Identity By Type</h2>
<h3 id="stat-identity-by-type-look" class="anchored">Stat Heatmap</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pokemon/charts/chart1_stat_heatmap.plotly.json" data-fallback="/images/content/articles/pokemon/charts/chart1_stat_heatmap.png" role="img" aria-label="Stat Heatmap"></div>
</figure>
<p class="art-p">Dragon sits at the top of the heatmap for a reason. With a median Attack of 100 and no single stat below 80, Dragon-types are the closest thing Pokémon has to a generalist elite — high across the board, weak nowhere. The type wasn't always rare by accident. Game Freak made Dragon deliberately difficult to access in the early games because the numbers justified the gatekeeping. The more revealing story is in the specialists. Steel-types clock a median Defense of 116 — the highest single cell on the entire chart — while their Special Attack sits at 60, dead last among Steel's own stats. Fighting-types mirror that tradeoff on offense: Attack of 100, Special Attack of 42, the sharpest stat gap in the dataset. These aren't balanced Pokémon. They're designed to do one thing extremely well and pay for it everywhere else. The heatmap makes that design philosophy impossible to ignore. Bug sits alone at the bottom. Across all six stats, Bug-types post the lowest or near-lowest medians in every column — 60 HP, 65 Attack, 60 Defense, 55 Special Attack, 60 Special Defense, 60 Speed. The type has been statistically undertuned since Generation I and the data across nine generations confirms it hasn't been corrected. Whether that's a deliberate choice to keep early-game Pokémon weak or an oversight that calcified into canon, the result is the same: Bug-types are the worst-statted primary type in the game by a significant margin. One caveat: Flying appears near the top of the chart with an unusually high Speed median of 116, but Flying is almost never a primary type — it's almost always secondary. The dataset's primary Flying entries (Tornadus, Gyarados, Chatot, and a handful of others) are a small and unrepresentative sample, which inflates the type's apparent standing relative to how Flying Pokémon actually play in practice.</p>
<h2 id="generation-creep" class="anchored">Generation Creep</h2>
<h3 id="generation-creep-look" class="anchored">Generation Ridgeline</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pokemon/charts/chart2_generation_ridgeline.plotly.json" data-fallback="/images/content/articles/pokemon/charts/chart2_generation_ridgeline.png" role="img" aria-label="Generation Ridgeline"></div>
</figure>
<p class="art-p">Every generation from Gen 1 through Gen 7 shows the same basic distribution shape — a peak around 60–70 base experience on the left, a second hump around 150–170 for mid-tier Pokémon, and a long tail trailing off toward the high end. What changes is that tail. With each successive generation, it stretches a little further right. The center of mass isn't dramatically shifting, but the ceiling keeps rising. The outliers tell the real story. That thin red thread extending past 600 on Gen 2's row is Blissey — a Normal-type with 255 base HP and the highest base experience yield of any Pokémon in the game at the time of its introduction. Gen 1 has its own isolated tail around 400, anchored by Chansey and the original legendary trio. These aren't flukes of the distribution — they're intentional design decisions that show up as statistical anomalies. Game Freak wasn't inflating power evenly across all Pokémon. They were adding extreme outliers at the top end while keeping the median relatively stable. Gen 7's distribution is the most compressed of any generation — the narrowest spread, the sharpest peak, the least variance. That's partly a function of Game Freak introducing fewer fully-evolved Pokémon with extreme stat totals in Alola, and partly a reflection of a design era that prioritized Mega Evolutions and Z-Moves over raw base stat inflation. The shape of Gen 7's curve is what controlled power creep looks like. Whether Game Freak intended it or stumbled into it, the ridgeline is the evidence.</p>
<h2 id="built-different" class="anchored">Built Different</h2>
<h3 id="built-different-look" class="anchored">Size Scatter</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pokemon/charts/chart3_size_scatter.plotly.json" data-fallback="/images/content/articles/pokemon/charts/chart3_size_scatter.png" role="img" aria-label="Size Scatter"></div>
</figure>
<p class="art-p">The scatter reveals that Pokémon size follows a rule: heavier things are taller, and the relationship is consistent enough across 1,000+ Pokémon that the log-scale correlation is basically a straight line. Game Freak didn't design each Pokémon's physical dimensions independently — there's an implicit size grammar baked into the franchise, and almost every Pokémon obeys it. The exceptions are the entire point of the chart. Cosmoem is the most extreme outlier in the dataset — 999.9 kg crammed into a body 0.1 meters tall, which puts it in the bottom-right corner of the chart completely alone. It weighs more than a polar bear and is smaller than a dinner plate. Wailord goes the other direction: 14.5 meters tall, 398 kg, making it one of the least dense objects in the Pokémon world despite being a whale. Celesteela, a Steel/Flying Ultra Beast, is nearly as heavy as Wailord and taller than a four-story building. These aren't design oversights — they're deliberate choices to make certain Pokémon physically impossible in ways that signal their otherness before you ever check their stats. The type coloring doesn't produce clean clusters, but it does reveal soft patterns. Dragon-types (purple) and Water-types (blue) dominate the upper-right of the chart — the large, heavy end of the distribution. Bug-types (yellow-green) cluster densely in the small, light region on the left. Steel-types scatter across an unusually wide range, from the tiny Klefki to the massive Celesteela. What the scatter ultimately shows is that physical scale is a storytelling tool. The Pokémon at the extremes aren't there because of random number generation — they're there because someone at Game Freak decided that a 14-meter whale or a 999-kilogram cosmic cocoon needed to exist, and the data is just the record of that decision.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">The most significant limitation of this analysis is scope: the dataset covers base stats and physical attributes, but Pokémon competitive viability is determined by factors this data doesn't capture. Abilities, move pools, type matchups, held items, and EV/IV systems all affect how a Pokémon actually performs in battle. A Bug-type with low base stats can still be competitively viable if it has the right ability — Scizor has been a top-tier competitive Pokémon for years despite its type disadvantage, largely due to its access to Bullet Punch and Technician. The numbers here describe design intent, not gameplay outcomes.</p>
<p class="art-p">The generation variable has a known data quality issue: a subset of records carry null generation IDs, most likely alternate forms or entries added outside the standard generational release structure. These were filtered from Chart 2 rather than imputed, which means the ridgeline distributions reflect only records with confirmed generation assignments. The omitted records are a small fraction of the total dataset and are unlikely to meaningfully change the shape of any generation's distribution.</p>
<p class="art-p">Finally, the dataset reflects a single snapshot of PokéAPI data compiled for the TidyTuesday release in April 2025. Base stats, forms, and classifications are subject to change with new game releases and balance patches — particularly for Scarlet and Violet, which introduced a large number of new forms and mechanics that may not be fully represented in this version of the data. Any analysis of the most recent generations should be treated as preliminary.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">The type system isn't just flavor. Dragon-types are statistically elite by design, Bug-types are statistically weak by design, and the specialists in between — Steel's defense, Fighting's attack, Electric's speed — reflect intentional tradeoffs embedded in the numbers from the beginning. The heatmap makes 25 years of Game Freak's design philosophy legible in a single chart. Every type has a signature, and the data confirms it.</p>
<p class="art-p">Power creep is real but it's not uniform. The median Pokémon hasn't gotten dramatically more powerful across nine generations — the distribution shape is remarkably stable from Gen 1 to Gen 7. What has changed is the ceiling. Each generation adds a small number of outliers at the extreme high end: a Blissey, a legendary trio, an Ultra Beast. The franchise inflates not by pulling the average up but by making the top more extreme. That's a different kind of creep, and it's harder to notice until you plot it.</p>
<p class="art-p">The size scatter is the most human chart of the three. It shows that somewhere inside Game Freak, someone made a decision to create a whale that weighs less than a car and a cosmic dust mote that weighs more than a horse. Those aren't statistical accidents — they're creative decisions that left a data signature. That's the throughline of this entire report: the Pokémon franchise is enormous and commercially optimized and thoroughly analyzed by millions of fans, but underneath all of it is a set of design choices made by people, and the numbers are how you read them.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The dataset is TidyTuesday Week 13, 2025 — a cleaned version of the PokéAPI database covering 1,028 Pokémon entries across nine generations. Each row represents a single Pokémon form, which means alternate forms (Mega Evolutions, regional variants, Gigantamax forms) appear as separate records from their base versions. The core fields used in this piece are the six base stats (HP, Attack, Defense, Special Attack, Special Defense, Speed), base experience, primary type, height, weight, and generation ID. All values are drawn directly from the TidyTuesday source — no external APIs were joined for this analysis.</p>
<p class="art-p">Base experience is a commonly misunderstood field. It is not the same as a Pokémon's base stat total, and it is not a measure of overall power. It is the amount of experience a trainer's Pokémon receives when defeating that species in battle — a game mechanic that reflects intended difficulty and progression pacing, not raw strength. A Pokémon with high base experience is meant to be encountered later in the game or to signal a harder fight. It correlates with power, but imperfectly.</p>
<p class="art-p">Height and weight are stored in the dataset in their PokéAPI native units: decimetres for height and hectograms for weight. Both were converted to standard metric units (metres and kilograms respectively) before plotting. The log scale applied in Chart 3 is not a stylistic choice — the raw distributions span roughly four orders of magnitude, from Flabébé at 0.1 metres and 0.1 kilograms to Wailord at 14.5 metres and Cosmoem at 999.9 kilograms. A linear scale would make the chart unreadable.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p class="art-p">The PokéAPI/TidyTuesday file is useful because it exposes the game-design schema behind the franchise: types, stats, generation IDs, dimensions, and battle-related mechanics in a machine-readable form. It is less useful for competitive outcomes because abilities, movesets, items, effort values, individual values, metagame bans, and format-specific rules sit outside the columns plotted here. The report therefore treats the data as design infrastructure, not as a live Smogon, VGC, or Pokémon Showdown viability model.</p>
<p class="art-p">The historical anchors are Satoshi Tajiri, Game Freak, Nintendo, Creatures, and The Pokémon Company because the numbers emerge from a designed commercial system that began with <em>Pocket Monsters Red and Green</em> in 1996. Bulbapedia and PokéAPI provide community and API documentation for mechanics such as base experience, but the interpretation remains tied to the official games' release cadence and the dataset snapshot rather than to fan speculation about future balance changes.</p>
<p class="art-p">
Data Science Learning Community. (2025). <em>TidyTuesday: A weekly
social data project.</em> Week 13, 2025 — Pokémon.
https://tidytues.day
</p>
<p class="art-p">
Tajiri, S. (Director). (1996). <em>Pocket
Monsters Red and Green</em> [Video game]. Game Freak; Nintendo.
</p>
<p class="art-p">
PokéAPI. (2025). <em>The RESTful Pokémon API.</em>
https://pokeapi.co
</p>
<p class="art-p">
Bulbapedia contributors. (2025). <em>Base experience.</em> Bulbapedia,
the community-driven Pokémon encyclopedia.
https://bulbapedia.bulbagarden.net/wiki/Base_experience
</p>
<h2 id="editor-s-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p class="art-p">
This report was researched, written, designed, and produced in active
collaboration with Claude AI (Anthropic). The data pipeline, statistical
analysis, chart design, written analysis, narrative structure, and visual
styling were all developed through a directed partnership between human
editorial judgment and AI execution.
</p>
<p class="art-p">
Artometrics was built on the premise that rigorous analysis and honest
process are not in conflict. The research questions, editorial instincts,
interpretive framing, and brand vision are ours. The execution — every
line of R code, every paragraph of analysis, every design decision — was
a collaboration. We document this not as a disclaimer but as a
description of how we actually work, and as a position: we believe this
is what serious data journalism looks like when the tools available are
used honestly and at full capacity.
</p>
<p class="art-p"><em>— Artometrics Editorial</em></p></div>

<p class="art-github-wrap">
  <a class="art-github-btn" href="https://github.com/Artometrics/pokemon" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a>
</p>
</section>
</main>
</div>
