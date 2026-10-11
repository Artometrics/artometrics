---
title: 'POISON: What Star Risk Costs an IP'
slug: poison
author: kyle-mcauliffe
pubDate: 2026-09-22T00:00:00.000Z
description: Merch built Pokémon's $91B; one actor's six films show the bill.
heroImage: /images/content/articles/poison/hero.png
draft: false
tags:
  - arts
  - film
subject: Franchises
tldr: 'This is an editorial synthesis of two published Artometrics datasets plus one small case study. The franchise dataset shows Pokémon earning $91B lifetime across 103 franchise rows in the TidyTuesday 2019-07-02 file, with merchandise driving 56% of row-sum revenue — a cushion no single actor''s box office can match. The margins dataset (median $25,533,818 domestic gross) shows that genre and cast metadata in community-cleaned box-office tables can mislead single-title conclusions. Layered against a small six-film case study of Jared Leto''s 2020s slate — worldwide gross ÷ budget ranging 0.65x to 2.04x, with three of six titles below breakeven — the pattern illustrates what concentrated star risk looks like when there is no licensing revenue to absorb it. The personal-conduct angle on Leto belongs to a separate report, "The Protection Threshold"; this one stays on the economics.'
keyPoints:
  - '$90.9B — Pokémon lifetime revenue (largest single property row in the franchise file)'
  - '56% — Share of row-sum revenue from merchandise, licensing & retail (recomputed from franchise.csv)'
  - '$25,533,818 — Median domestic gross across 3,401 films in the horror-tagged dataset'
  - 0.65x–2.04x — Range of worldwide gross ÷ budget across six 2020s Jared Leto titles
  - 3 of 6 — Leto-slate titles landing below the 1.0x breakeven multiple
  - '103 — Franchise rows in the committed TidyTuesday extract (seven sit below a $4B editorial floor)'
faq:
  - question: Why does merchandise revenue reduce a franchise's exposure to any one person?
    answer: 'Merchandise, licensing, and retail are 56% of row-sum revenue when recomputed from franchise.csv (61% appeared in earlier published copy with a different franchise count). That money ties to characters, cards, and toys rather than to a single actor''s performance or public standing. Pokémon''s $91B lifetime total is built almost entirely on that layer, not box office.'
  - question: What does the Jared Leto case study measure?
    answer: 'Worldwide gross divided by reported production budget across six of his 2020s film credits: Morbius (2.02x), House of Gucci (2.04x), The Little Things (1.03x), Haunted Mansion (0.79x), Masters of the Universe (0.66x), and Tron: Ares (0.65x). Three of the six clear breakeven; three do not.'
  - question: Does this report cover allegations against Jared Leto?
    answer: 'No. Personal-conduct questions are covered in a separate Artometrics report, "The Protection Threshold: When Flops End Hollywood''s Silence." This report is limited to box-office and franchise-revenue economics.'
  - question: Can six films prove that star-fronted vehicles are riskier than IP franchises?
    answer: 'No. Six titles are a small, non-random sample and cannot generalize to "all star vehicles." The report treats the slate as an illustration of what concentrated star risk looks like, not as statistical proof of a causal relationship.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Merchandise-driven IP and star-fronted vehicles do not carry the same economic risk. The TidyTuesday 2019-07-02 media-franchise file lists 103 properties with Wikipedia lifetime revenue estimates (mid-2019); Pokémon leads at $91B, and merchandise, licensing, and retail account for 56% of row-sum revenue in the committed CSV — the same figures published in Artometrics' <a href="/franchise">franchise</a> report. When most of the money attaches to characters and products, a weak theatrical run is a line item, not an existential bet.</p>
<p class="art-p">Jared Leto's six-film 2020s slate is the counterexample: worldwide gross ÷ reported budget ranges from 0.65x to 2.04x, and three of six titles land below breakeven — with no licensing layer to absorb the misses. The charts below pair that small case study with our published <a href="/franchise">franchise</a> and <a href="/margins">margins</a> datasets to compare revenue structure, not scandal; conduct questions stay in <a href="/protection">The Protection Threshold</a>. Methods and citations are in the back matter.</p>
<h2 id="merchandise-is-the-insulation" class="anchored">Merchandise Is the Insulation IP Franchises Have and Star Vehicles Don't</h2>
<figure class="art-chart">
  <div
    class="art-chart-live"
    data-chart="/data/articles/poison/charts/chart1_revenue_stream_share.plotly.json"
    data-fallback="/images/content/articles/poison/charts/chart1_revenue_stream_share.png"
    data-source="Data: TidyTuesday / Box Office Mojo — ARTOMETRICS"
    role="img"
    aria-label="Merchandise share of revenue across 103 franchise rows"
  ></div>
  <figcaption class="art-chart-caption">Merchandise, licensing, and retail account for 56% of row-sum revenue across 103 franchise rows — a stream that does not depend on any one actor's box office weekend.</figcaption>
</figure>
<p class="art-p">Artometrics' franchise-revenue report established that merchandise is not one revenue stream among several — it is the dominant one, at 56% of row-sum revenue across 103 franchise rows in the TidyTuesday extract (61% and a count of 107 appeared in earlier published copy). Pokémon's $91B total, the highest of any tracked property, was built almost entirely on cards, games, and retail rather than any theatrical run. Henry Jenkins's transmedia framework (<em>Convergence Culture</em>, NYU Press, 2006) helps explain why: revenue attached to a character or mascot can move across games, apparel, and film without routing through a single performer's weekend gross. Contrast that with a franchise or vehicle built around one performer's draw. When merchandise, licensing, and games are absent or minor, the entire revenue case rests on box office and, downstream, on home video and streaming licensing tied to that same theatrical result. There is no secondary economy running in parallel the way there is for Pokémon or, per the same report, for Star Wars — the one franchise in that dataset the report specifically flagged as fully diversified across box office, merchandise, home video, and games. A star-fronted film without that diversification is, in revenue-structure terms, closer to a single bet than to a franchise.</p>
<h2 id="what-concentrated-poison-looks-like" class="anchored">What Concentrated Star Risk Looks Like: A Six-Film Case Study</h2>
<figure class="art-chart">
  <div
    class="art-chart-live"
    data-chart="/data/articles/poison/charts/chart2_leto_slate_ratios.plotly.json"
    data-fallback="/images/content/articles/poison/charts/chart2_leto_slate_ratios.png"
    data-source="Data: TidyTuesday / Box Office Mojo — ARTOMETRICS"
    role="img"
    aria-label="Six-film Jared Leto slate: worldwide gross divided by reported budget"
  ></div>
  <figcaption class="art-chart-caption">Three of six titles in the case-study slate clear breakeven comfortably; three land at or below 1.0x — a spread with no merchandise layer to soften it.</figcaption>
</figure>
<p class="art-p">The case-study dataset is small and deliberately narrow: six of actor Jared Leto's 2020s film credits, each expressed as worldwide gross divided by reported production budget, using trade-reported budget bands from Box Office Mojo. House of Gucci (2021, ensemble) returned 2.04x on a $75M budget. Morbius (2022, lead) returned 2.02x on $83M. Those two clear breakeven with room. The other four sit closer to the line or under it: The Little Things (2021, lead, released into a pandemic-narrowed theatrical window) landed at 1.03x; Haunted Mansion (2023, ensemble) at 0.79x; Masters of the Universe (2026, supporting) at 0.66x; and Tron: Ares (2025, lead) at 0.65x, on the largest reported budget in the slate at $220M. Read individually, each figure is a data point about one film. Read as a slate, the pattern is a distribution centered near or below 1.0x rather than comfortably above it — half the titles below breakeven, and only two of six clearing 2.0x. That is the shape of concentrated star risk: revenue tied tightly to one theatrical outcome per title, with no licensing or merchandise base underneath it the way Pokémon's $91B or Star Wars' diversified mix has. When a title in this kind of slate underperforms, the studio absorbs the loss directly — there is no secondary revenue stream to blunt it. This is a small, non-random sample, and the report treats it as illustration, not proof; see Limitations below.</p>
<h2 id="why-genre-and-cast-metadata-can-mislead" class="anchored">Why Genre and Cast Metadata Can Mislead Single-Title Conclusions</h2>
<figure class="art-chart">
  <div
    class="art-chart-live"
    data-chart="/data/articles/poison/charts/chart3_scale_comparison.plotly.json"
    data-fallback="/images/content/articles/poison/charts/chart3_scale_comparison.png"
    data-source="Data: TidyTuesday / Box Office Mojo — ARTOMETRICS"
    role="img"
    aria-label="IP-franchise scale vs single-title scale, dollars in millions, log axis"
  ></div>
  <figcaption class="art-chart-caption">Pokémon's $91B lifetime total dwarfs both a median single film ($25.53M domestic) and the largest single budget in the case-study slate ($220M) — different orders of magnitude, not different points on the same curve.</figcaption>
</figure>
<p class="art-p">Artometrics' margins report already demonstrated a caution that applies directly here: community-cleaned genre and metadata tags in box-office tables are unreliable enough to mislead a reader trying to draw conclusions about any single title or person. That report's dataset, nominally tagged "horror," was topped by Star Wars Episode I: The Phantom Menace at $474,544,677 domestic — a science-fiction adventure film, not a horror film, sitting atop a genre-labeled table because of a tagging error in the community-cleaned merge. The median across all 3,401 films in that file was $25,533,818 domestic, spanning 1936–2019. The lesson generalizes beyond genre tags: any table that mixes lead, supporting, and ensemble billing, or that blends pandemic-window releases with ordinary theatrical runs, risks producing headline numbers that look like a verdict on one person when they are really an artifact of how the underlying rows were labeled and merged. The six-film case study above mixes exactly those roles — lead, supporting, and ensemble — and one pandemic-era release. That mix is disclosed, not hidden, because the margins report's central caution is that undisclosed metadata quietly drives conclusions readers think are about content, when they are really about cleaning decisions.</p>
<h2 id="limitations" class="anchored">LIMITATIONS</h2>
<p class="art-p">Six films is a small sample. It cannot generalize to "all star vehicles" or to any actor's career as a whole, and it should not be read as a ranking or grade of any individual film. The gross-to-budget ratios use trade-reported budget bands, which studios do not always disclose precisely or consistently; treat them as order-of-magnitude figures, not audited production accounting. No causal link between reputational risk and box-office softness is established, tested, or claimed in this report — the framework below is an editorial hypothesis about revenue structure, not a measured finding, and is labeled as such. The franchise and horror datasets describe different populations (103 franchise rows in the committed CSV; 3,401 individual films) and different time windows; combining them illustrates a structural argument, not a single unified statistical model.</p>
<h2 id="conclusion" class="anchored">Conclusion</h2>
<p class="art-p">Editorial framework, not measured finding: the evidence assembled here is consistent with the idea that merchandise-driven IP carries structurally less exposure to any one person's performance than a star-fronted vehicle does. The six-film case study illustrates concentrated theatrical exposure when that cushion is absent — not proof about any particular result. De Vany and Walls (2004) show why theatrical outcomes alone behave like lottery tickets; this report asks whether merchandise share is the hedge studios buy when they want something sturdier than a lottery ticket. A future report with a larger sample could test whether merchandise share predicts how much a single underperforming title costs the studio that owns it.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">This report combines two previously published Artometrics analyses with one small case-study dataset assembled for this piece. It introduces no new franchise-level or film-level dataset of its own.</p>
<p class="art-p">First, the TidyTuesday 2019-07-02 media-franchise file (103 franchise rows with Wikipedia lifetime revenue estimates as of mid-2019), as analyzed in Artometrics' <a href="/franchise">franchise</a> report — source bundle: <a href="https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-07-02" target="_blank" rel="noopener noreferrer">TidyTuesday 2019-07-02</a>. Merchandise, licensing, and retail are 56% of row-sum revenue when recomputed from <code>franchise.csv</code> (61% appeared in earlier published copy with a different franchise count). Second, the TidyTuesday horror-tagged box-office dataset (3,401 films, 1936–2019), as analyzed in Artometrics' <a href="/margins">margins</a> report. Franchise figures are cited as published in the franchise report; no independent recalculation was performed on the horror file for this piece.</p>
<p class="art-p">Third, a case-study table of six Jared Leto credits in the 2020s: worldwide gross and trade-reported production budget from <a href="https://www.boxofficemojo.com/" target="_blank" rel="noopener noreferrer">Box Office Mojo</a>, with gross ÷ budget as a simple derived ratio. The synthesis connecting all three — merchandise insulation versus concentrated theatrical exposure — is an editorial reading, not a unified statistical model, and is labeled as such throughout.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">References</h3>
<div class="art-references">
  <div class="art-ref-item">
    De Vany, A., &amp; Walls, W. D. (2004). Motion pictures and the risk of product market failure. <em>Journal of Economic Perspectives</em>, 18(3), 173–186. <a href="https://pubs.aeaweb.org/doi/pdfplus/10.1257/0895330042162378" target="_blank" rel="noopener noreferrer">AEA Web</a>
  </div>
  <div class="art-ref-item">
    Jenkins, H. (2006). <em>Convergence Culture: Where Old and New Media Collide</em>. NYU Press.
  </div>
  <div class="art-ref-item">
    Data Science Learning Community. (2019). <em>TidyTuesday: Media franchise revenues</em>. <a href="https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-07-02" target="_blank" rel="noopener noreferrer">GitHub</a>
  </div>
  <div class="art-ref-item">
    Box Office Mojo. <em>Title-level worldwide gross and trade-reported budget figures</em>, 2021–2026. <a href="https://www.boxofficemojo.com/" target="_blank" rel="noopener noreferrer">boxofficemojo.com</a>
  </div>
  <div class="art-ref-item">
    Artometrics. <em>Franchise revenue report</em>. <a href="/franchise">artometrics.com/franchise</a>
  </div>
  <div class="art-ref-item">
    Artometrics. <em>Horror-profit / margins report</em>. <a href="/margins">artometrics.com/margins</a>
  </div>
  <div class="art-ref-item">
    Artometrics. <em>The Protection Threshold</em>. <a href="/protection">artometrics.com/protection</a>
  </div>
</div>
<h2 id="editors-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note">
<p class="art-p">
This report is a cross-report synthesis: it cites facts already published in two Artometrics data reports and layers them against a small, separately sourced case-study dataset. It does not re-derive or re-audit the underlying TidyTuesday files, and it does not address personal-conduct questions about any individual named in it — that ground is covered separately in "The Protection Threshold: When Flops End Hollywood's Silence." This piece is limited to box-office and franchise-revenue economics.
</p>
<p class="art-p">
This report was researched, written, and produced in active collaboration with Claude AI (Anthropic), following the same disclosed process used across Artometrics reporting: human editorial judgment directs the research question and framework; execution — analysis, prose, and chart design — is a documented collaboration.
</p>
<p class="art-p">— Artometrics Editorial</p>
</div>
</section>
</main>
</div>
