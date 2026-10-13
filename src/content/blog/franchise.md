---
title: "FRANCHISE: Merchandise Owns the Ledger"
slug: franchise
author: kyle-mcauliffe
pubDate: 2026-04-08T00:00:00.000Z
updatedDate: 2026-10-12T00:00:00.000Z
description: >-
  140 franchises on the October 2026 Wikipedia ledger sum to $1.45T lifetime revenue. Merchandise is 55.8%; box office 18.3%; Pokémon leads at $130.7B. The US now out-earns Japan ($816B vs $394B), but Japan runs the higher merchandise share (71.4% vs 52.0%). Nine of 2025's ten biggest films were franchise entries.
heroImage: /images/content/articles/franchise/hero.png
audioSrc: /audios/franchise-kore-v4.mp3
draft: false
tags:
  - arts
  - film
subject: Franchises
tldr: >-
  We rebuilt the franchise ledger from Wikipedia's list as of October 12, 2026 (140 franchises, S017), audited the 2019 TidyTuesday file against its own source (S001), and recomputed every headline. Lifetime revenue is $1,448.1B; merchandise, licensing, and retail are 55.8% [95% range 44.0–66.2]; box office 18.3% [12.8–25.6]; video games 17.9%. Pokémon leads at $130.7B. Consolidated Disney holds 29.7% of the ledger and the top five parents 58.2%. US-origin franchises now total $816.5B against Japan's $394.5B, while Japan's merchandise share is 71.4% to the US's 52.0%. Franchise installments took 94.4% of 2025's worldwide top-ten gross.
keyPoints:
  - "$1,448.1B — lifetime revenue, 140 franchises (Wikipedia, Oct 12 2026, S017)"
  - "55.8% — merchandise, licensing & retail share (95% range 44.0–66.2)"
  - "$130.7B — Pokémon, more than Star Wars and the MCU combined ($84.2B)"
  - "29.7% / 58.2% — share held by Disney / the top five parent companies"
  - "71.4% vs 52.0% — merchandise share, Japan-origin vs US-origin franchises"
  - "94.4% — franchise share of 2025's worldwide top-ten box office"
faq:
  - question: Which franchise has the highest lifetime revenue?
    answer: >-
      Pokémon at $130.7B on Wikipedia's October 2026 list (S017), followed by Mickey Mouse &amp; Friends ($61.2B), Winnie-the-Pooh ($50.2B), Star Wars ($46.7B) and Disney Princess ($45.4B).
  - question: What revenue stream dominates?
    answer: >-
      Merchandise, licensing, and retail: 55.8% of lifetime revenue across 140 franchises. Box office is 18.3% and video games 17.9%. The box-office share was 8.9% in the 2019 file; most of that jump is fuller itemisation on Wikipedia, not a market shift.
  - question: How concentrated is ownership?
    answer: >-
      Consolidated to 2026 parent companies, Disney holds $430.7B (29.7%). The top five — Disney, Warner Bros. Discovery, The Pokémon Company, Microsoft and Paramount Skydance — hold 58.2%.
  - question: Why did Hello Kitty fall from $80.0B to $33.5B?
    answer: >-
      Wikipedia editors revised the sourcing. Sanrio did not report a collapse. Mario ($35.0B→$9.74B) and Gundam ($25.5B→$5.0B) are the same kind of correction. See the companion piece, "What changed when we fixed the data."
  - question: How does Japan compare with the United States?
    answer: >-
      On the October 2026 list, 88 US-origin franchises total $816.5B (52.0% merchandise) and 30 Japan-origin franchises total $394.5B (71.4% merchandise). The 2019 file showed the opposite ranking: Japan $681.5B, US $622.6B.
  - question: Are blockbusters still franchise films?
    answer: >-
      Yes. Nine of 2025's ten highest-grossing films worldwide were franchise installments, 94.4% of top-ten gross. 2026 is 62.0% so far, with The Odyssey, Michael and Project Hail Mary as original hits.
---
<div id="quarto-content">
<nav id="TOC" role="doc-toc">
<h2 id="toc-title" class="anchored">IN THIS REPORT</h2>
<ul>
<li><a href="#executive-summary">Executive summary</a></li>
<li><a href="#research-question">Research question</a></li>
<li><a href="#one-ledger">One ledger, two playgrounds</a></li>
<li><a href="#merchandise-pools">Merchandise pools — Japan’s media-mix vs Hollywood’s vertical stack</a></li>
<li><a href="#top-twenty">Who tops the table — and who is not crowned</a></li>
<li><a href="#wiki-drift">Wikipedia moved (2019 vs 2026)</a></li>
<li><a href="#region-origin">Japan, the United States, and the United Kingdom — the flip</a></li>
<li><a href="#original-medium">Original medium sets the extraction layer</a></li>
<li><a href="#box-office-slice">Box office is a thin slice for most of the top twenty</a></li>
<li><a href="#revenue-per-year">Revenue per year of existence</a></li>
<li><a href="#disney-consolidated">Disney consolidated — ownership literacy</a></li>
<li><a href="#owner-concentration">Owner concentration — five parents, 58%</a></li>
<li><a href="#disney-acquisitions">Disney acquisitions — check size vs row anchor</a></li>
<li><a href="#disney-segments">Disney segment revenue (10-K)</a></li>
<li><a href="#theatrical-seriality">Theatrical seriality</a></li>
<li><a href="#fragmented-libraries">Sony, Universal, Nintendo — fragmented vs married IP</a></li>
<li><a href="#failure-modes">When franchises break</a></li>
<li><a href="#decision-tools">Decision tools for executives</a></li>
<li><a href="#limitations">Limitations</a></li>
<li><a href="#conclusion">Conclusion</a></li>
<li><a href="#data-methods-and-sources">Data, methods &amp; sources</a></li>
<li><a href="#editors-note">Editor's note</a></li>
</ul>
</nav>
<main class="art-article-main">

<div class="art-callout" id="executive-summary">
<p class="art-p"><strong>Executive summary.</strong> Franchise economics is licensing geometry: who owns repeatable rights, and which revenue streams compound after the premiere. On Wikipedia's October 2026 ledger (140 properties, $1,448.1B lifetime, S017), merchandise, licensing and retail are 55.8% of revenue; box office is 18.3% and games 17.9%. Pokémon leads at $130.7B — more than Star Wars ($46.7B) and the Marvel Cinematic Universe ($37.5B) combined. Consolidated to today's parents, Disney holds 29.7% of the ledger and five companies hold 58.2%. The regional story flipped when we rebuilt the data: US-origin franchises now out-earn Japan's ($816.5B vs $394.5B), but Japan's are the purer merchandise machines (71.4% vs 52.0%). In theaters the sequel economy deepened — franchise installments took 94.4% of 2025's worldwide top-ten gross. Several big 2019 figures (Hello Kitty $80.0B, Mario $35.0B) were source errors, not declines; the companion piece <a href="/franchise-data-fix">“What changed when we fixed the data”</a> documents every revision.</p>
</div>

<h2 id="one-ledger" class="anchored">ONE LEDGER, TWO PLAYGROUNDS</h2>
<p class="art-p">A child trades a cardboard Pikachu for lunch money; Bob Iger signs a seventy-one-point-three-billion-dollar check for Twenty-First Century Fox. Both trades assume the same premise — that characters can be mined long after opening weekend. Our x-ray is Wikipedia's “highest-grossing media franchises” list as of October 12, 2026 (revision 1379832186, S017): 140 franchises, each itemised into revenue streams that we map to one standard schema. The earlier edition of this report used the TidyTuesday file of July 2, 2019 (103 franchises, S001); we keep it as a baseline and audited it against the Wikipedia revision it was scraped from. Figures are editors' lifetime estimates of consumer spend in nominal dollars, not audited studio financials — still the cleanest public ledger for comparing <em>how</em> money attaches to IP.</p>
<p class="art-p">This report reads that ledger the way an anime R2 report reads MyAnimeList: as the footprint of a production system, not a popularity contest. Henry Jenkins’s <em>Convergence Culture</em> (2006) frames the audience side — stories that jump formats because fans follow characters. Marc Steinberg’s media-mix work on Japan shows the extreme case: sponsored television animation as billboard for merchandise (Steinberg, 2012). American conglomerates built a parallel stack — own the character, own the park turnstile, own the streaming shelf. Below, each pattern states what it means for a buyer, how we know it (source and method), what mechanism explains it, and a cross-market comparison or counterexample.</p>

<h2 id="research-question" class="anchored">RESEARCH QUESTION</h2>
<p class="art-p">For franchises on the October 2026 Wikipedia ledger, (1) how much lifetime value sits in merchandise versus box office and games, (2) how do Japan-origin and US-origin properties differ in that mix, (3) how did estimates move since the 2019 file, (4) how does consolidating Disney subsidiaries change the ownership map, and (5) how dominant are franchise installments in the 2025 and 2026 box office?</p>

<h2 id="merchandise-pools" class="anchored">MERCHANDISE POOLS — JAPAN’S MEDIA-MIX VS HOLLYWOOD’S VERTICAL STACK</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart6_revenue_streams_2026.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart6_revenue_streams_2026.png" data-source="Data: Wikipedia franchise list, Oct 12 2026 (S017) — ARTOMETRICS" role="img" aria-label="Revenue stream shares, October 2026, with 95% bootstrap ranges and 2019 markers."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Merchandise, licensing and retail 55.8% [44.0–66.2]; box office 18.3% [12.8–25.6]; games 17.9% [11.2–26.2]. Black ticks mark the 2019 file.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> At franchise scale, theatrical is usually marketing infrastructure; repeatable SKUs and licensing desks carry more than half the ledger.</p>
<p class="art-p"><strong>How we know.</strong> Sum every itemised stream on the October 2026 list: $1,448.1B total; merchandise, licensing and retail $809.4B (55.8%); box office $265.3B (18.3%); video games $259.2B (17.9%); $27.2B (1.9%) is listed in totals but not itemised. Ranges are 95% bootstrap intervals from resampling franchises 5,000 times — they show how much a share depends on which franchises the list includes.</p>
<p class="art-p"><strong>Mechanism.</strong> Japan’s production committees split copyright among publishers, broadcasters and toy makers, which hard-wires plush, magazines and cards into budgets (Hernández Hernández, 2018; Steinberg, 2012). Hollywood historically licensed characters outward, but vertically integrated studios — especially Disney — internalised parks, cruise and retail as Experiences segment revenue (FY2024 $34.151B, S081).</p>
<p class="art-p"><strong>Counterexample.</strong> Box office looks twice as big as in 2019 (18.3% vs 8.9%), but most of that is measurement: the 2019 file's eight-category schema dropped line items, and today's list itemises film grosses more fully. Restricted to the 82 franchises present in both vintages, box office is 15.4%.</p>

<h2 id="top-twenty" class="anchored">WHO TOPS THE TABLE — AND WHO IS NOT CROWNED</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart1_top20_revenue_2026.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart1_top20_revenue_2026.png" data-source="Data: Wikipedia franchise list, Oct 12 2026 (S017) — ARTOMETRICS" role="img" aria-label="Stacked horizontal bars of the top 20 franchises by revenue stream, October 2026."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Pokémon ($130.7B) leads Mickey Mouse &amp; Friends ($61.2B) and Winnie-the-Pooh ($50.2B); merchandise bands dominate most stacks.</figcaption>
</figure>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Pokémon — game-first flywheel</p>
<p class="art-p"><strong>What it means.</strong> Pokémon is more than twice the size of the next property — the template for game-first franchise design.</p>
<p class="art-p"><strong>How we know.</strong> $130.7B lifetime, of which $119.3B is retail sales and $10.2B mobile games (S017). It was $90.9B in the 2019 file.</p>
<p class="art-p"><strong>Mechanism.</strong> Created 1996 (Game Freak / Nintendo). Anime promotes cards; cards promote video games — collectible SKUs with a cartoon as advertising.</p>
<p class="art-p"><strong>Counterexample.</strong> In 2019, Star Wars plus the MCU exceeded Pokémon. In 2026 they do not: $46.7B + $37.5B = $84.2B. Mickey Mouse &amp; Friends ($61.2B) is a new top-two entry the 2019 file did not list.</p>
</div>
<aside>
<div class="art-logo"><img src="/images/content/articles/franchise/assets/logo_nintendo.svg" alt="Nintendo" /><p class="art-logo__credit">Nintendo logo via Wikimedia Commons (PD-textlogo; trademark of Nintendo)</p></div>
</aside>
</div>

<h2 id="wiki-drift" class="anchored">WIKIPEDIA MOVED (2019 VS 2026)</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart10_wiki_2019_vs_2026.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart10_wiki_2019_vs_2026.png" data-source="Data: TidyTuesday 2019 + Wikipedia 2026 scrape — ARTOMETRICS" role="img" aria-label="Largest revenue deltas between 2019 and 2026 Wikipedia pairs."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Eighty-two franchises with revenue in both years. Gray bars flag Wikipedia source revisions — e.g. Hello Kitty $80.0B→$33.5B, Mario $35.0B→$9.74B, Gundam $25.5B→$5.0B — not real franchise declines (S001; S017).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Public franchise tables are editor-maintained surveys, and the October 2026 list is now our primary ledger — they drift when categories like mobile games or live-service revenue enter the infobox.</p>
<p class="art-p"><strong>How we know.</strong> 103 hand-mapped crosswalk rows; 82 with non-empty 2026 pairs and both-year revenue for chart 10 (<code>franchise_crosswalk_2019_2026.csv</code>, <code>franchise_revenue_2019_vs_2026.csv</code>; S001, S017). A 2026 index parse lists 140 Wikipedia franchise rows (S017).</p>
<p class="art-p"><strong>Mechanism.</strong> English Wikipedia aggregates press estimates; editors add streams the 2019 scrape under-weighted. The largest dollar increases among paired rows are Pokémon (+$39.8B, from $90.9B in 2019 to $130.7B in 2026), then Call of Duty and Naruto (about +$14B each). Mortal Kombat rises only about $3.9B, from $1.17B to $5.06B, and it is a fighting-game franchise, not a mobile title.</p>
<p class="art-p"><strong>Counterexample.</strong> Hello Kitty, Mario, and Gundam show large negative percent changes in the paired file because English Wikipedia revised its sourcing between scrapes — not because Sanrio or Nintendo reported collapsing revenue. Chart 10 colors those rows gray. Other drops may reflect renames, splits, or scope changes (e.g., The Simpsons after Fox consolidation). Quote growth only when the crosswalk documents a pair and the match note flags a true like-for-like total. Our audit also found the 2019 file running below its own source: in a random sample of 40 franchises, only 28 of 39 matched Wikipedia’s June 2019 headline within 10%.</p>

<h2 id="region-origin" class="anchored">JAPAN, THE UNITED STATES, AND THE UNITED KINGDOM — THE FLIP</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart15_region_2026.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart15_region_2026.png" data-source="Data: Wikipedia franchise list, Oct 12 2026 (S017) — ARTOMETRICS" role="img" aria-label="Lifetime revenue, franchise count and merchandise share by region of origin, October 2026."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">US: 88 franchises, $816.5B (52.0% merchandise). Japan: 30, $394.5B (71.4%). UK: 9, $136.1B (53.9%). Korea $27.0B, Sweden $26.3B, Canada $20.1B (S017).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> The previous edition said Japan out-earned the US ($681.5B vs $622.6B) while the US leaned harder on merchandise (64.6% vs 49.1%). On the rebuilt ledger both findings reverse. The US is now the scale player at twice Japan's total; Japan is the merchandise specialist, with seven of every ten dollars coming from goods.</p>
<p class="art-p"><strong>How we know.</strong> Region of origin is the creator's home market when the property launched, coded from the existing hand-audited table, owner-string rules, and 23 documented hand assignments for franchises new to the list (CLEANING_LOG, rule R9). Totals come from the October 2026 list; merchandise share is merchandise, licensing and retail ÷ region total.</p>
<p class="art-p"><strong>Mechanism.</strong> Two things moved. The list grew from 103 to 140 franchises, and 43 more US-origin properties came in — Fortnite, Avatar, Madden NFL, Scooby-Doo, The Sims — against Japanese additions that skew smaller (Rilakkuma, Demon Slayer). And several big Japanese totals were revised down at the source: Hello Kitty $80.0B→$33.5B, Mario $35.0B→$9.74B, Gundam $25.5B→$5.0B. What remains in Japan's ledger are character-goods engines — Pokémon, Anpanman, Hello Kitty — which pushes its merchandise share up. US franchises add box office (MCU 92.5% theatrical) and games (Call of Duty), which dilutes theirs.</p>
<p class="art-p"><strong>Counterexample.</strong> The flip is partly a coverage artefact of an English-language list: Japanese properties such as Detective Conan, Digimon and Bleach appear in the 2019 file but not on the 2026 table. Treat “the US out-earns Japan” as a statement about this ledger, not about national industries.</p>

<h2 id="original-medium" class="anchored">ORIGINAL MEDIUM SETS THE EXTRACTION LAYER (2019 BASELINE)</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart11_mix_by_original_medium.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart11_mix_by_original_medium.png" data-source="Data: franchise.csv — ARTOMETRICS" role="img" aria-label="Revenue stream mix by original media type."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Game- and manga-origin properties carry different stream mixes than film-first seeds (revenue_mix_by_original_medium.csv).</figcaption>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart5_original_media_revenue.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart5_original_media_revenue.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Lifetime revenue summed by original media type."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Video-game seeds lead lifetime totals ($334.9B), then manga ($253.8B) — not only theatrical premieres.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Debut format is less important than which streams the rights holder chooses to license.</p>
<p class="art-p"><strong>How we know.</strong> Sum lifetime revenue by <code>original_media</code> (chart 5); stream mix shares by medium (chart 11, S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Jump comics rows stack publishing, animation, and games on one bible; Disney Princess is a retail line built atop film assets (99.9% merchandise in the Disney Princess row).</p>
<p class="art-p"><strong>Counterexample.</strong> Novel-first Wizarding World — books set canon, but Warner Bros. had to build theatrical and merchandise desks to capture value; slate fatigue on <em>Fantastic Beasts</em> shows literary IP still needs discipline.</p>

<h2 id="box-office-slice" class="anchored">BOX OFFICE IS A THIN SLICE FOR MOST OF THE TOP TWENTY (2019 BASELINE)</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart14_box_office_share_top20.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart14_box_office_share_top20.png" data-source="Data: franchise.csv — ARTOMETRICS" role="img" aria-label="Box office share of lifetime revenue for top 20 franchises."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Marvel Cinematic Universe row is 67.7% box office; Hello Kitty and Mario near zero — same top twenty, different economics.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Ranking franchises by theatrical gross mis-ranks mascot-led properties.</p>
<p class="art-p"><strong>How we know.</strong> Box-office dollars ÷ franchise row total for each top-twenty name (chart 14, S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Film-first universes amortise development across sequels; character-first mascots skip the cinema tax.</p>
<p class="art-p"><strong>Counterexample.</strong> Star Wars keeps a thicker theatrical band (9.0% of row in entities table) while still running merchandise — the template Lucasfilm sold to Disney for $4.05B (S011).</p>

<h2 id="revenue-per-year" class="anchored">REVENUE PER YEAR OF EXISTENCE (2019 BASELINE)</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart2_revenue_per_year.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart2_revenue_per_year.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Top franchises by lifetime revenue divided by years since creation."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Pokémon clears about $3.95B per calendar year of existence; Hello Kitty’s $80B spans forty-five years of denominator.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Efficiency — how fast a property compounds — is a design choice, not fandom.</p>
<p class="art-p"><strong>How we know.</strong> Lifetime ÷ max(1, 2019 − <code>year_created</code>) for each franchise (chart 2, S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Monthly billing (games, cards) beats one-off theatrical cycles in the denominator.</p>
<p class="art-p"><strong>Counterexample.</strong> Legacy mascots with huge lifetime totals but long denominators look “slow” per year even when retail never stopped.</p>

<h2 id="disney-consolidated" class="anchored">DISNEY CONSOLIDATED — OWNERSHIP LITERACY (2019 BASELINE)</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart3a_disney_non_consolidated.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart3a_disney_non_consolidated.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Owner totals with Disney subsidiaries listed separately."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Raw owner field lists Disney ($258.9B), Lucasfilm ($63.0B), and Marvel labels separately — misleading for benchmarking.</figcaption>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart3b_disney_consolidated.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart3b_disney_consolidated.png" data-source="Data: TidyTuesday media franchises (2019-07-02) — ARTOMETRICS" role="img" aria-label="Owner totals with Disney subsidiaries merged."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Consolidated Disney: $426.2B in summed franchise rows — Nintendo standalone owner label $49.0B.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> M&amp;A is how modern libraries are assembled; owner fields in a 2019 scrape still list pre-consolidation labels.</p>
<p class="art-p"><strong>How we know.</strong> <code>owner_consolidation_rules.csv</code> rolls Marvel Entertainment, Lucasfilm, and 20th Century Fox into The Walt Disney Company; totals in <code>owner_totals_derived.csv</code> (S001).</p>
<p class="art-p"><strong>Mechanism.</strong> Buy the copyright stack, keep theatrical labels, harvest parks and merchandise off the same characters.</p>
<p class="art-p"><strong>Counterexample.</strong> Pokémon rows list The Pokémon Company / Nintendo strings — consolidating trademarks is a separate legal exercise from summing Wikipedia rows.</p>

<h2 id="owner-concentration" class="anchored">OWNER CONCENTRATION — FIVE PARENTS, 58%</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart12_owner_concentration_2026.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart12_owner_concentration_2026.png" data-source="Data: Wikipedia franchise list, Oct 12 2026 (S017) — ARTOMETRICS" role="img" aria-label="Share of lifetime revenue held by the top ten parent companies, October 2026."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Disney 29.7% [18.2–43.4]; top five parents 58.2% [52.7–72.6] — Disney, Warner Bros. Discovery, The Pokémon Company, Microsoft, Paramount Skydance.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> A handful of consolidators sit on well over half the public ledger — acquisition targets at scale are scarce, and most of them are already owned.</p>
<p class="art-p"><strong>How we know.</strong> Each franchise is assigned to its 2026 parent (Fox→Disney, Activision Blizzard and King→Microsoft, Viacom/CBS→Paramount Skydance, WarnerMedia→Warner Bros. Discovery), using the first-listed rights holder. Disney $430.7B, Warner Bros. Discovery $133.0B, The Pokémon Company $130.7B, Microsoft $75.2B, Paramount Skydance $72.8B.</p>
<p class="art-p"><strong>Mechanism.</strong> Capital markets reward libraries that can be wired to Experiences and streaming; Microsoft's $69B Activision purchase (2023) put a games publisher in the top five.</p>
<p class="art-p"><strong>Counterexample.</strong> The previous edition put the top five at 46.4%. On the same 2019 franchises with today's parents it is 62.8%, so the rise is consolidation (Activision into Microsoft) more than new franchises.</p>

<h2 id="disney-acquisitions" class="anchored">DISNEY ACQUISITIONS — CHECK SIZE VS ROW ANCHOR (2019 BASELINE)</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart8_disney_acquisitions.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart8_disney_acquisitions.png" data-source="Data: SEC deal prices + TidyTuesday franchise rows — ARTOMETRICS" role="img" aria-label="Scatter of acquisition price versus anchor franchise lifetime revenue."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Deal checks (SEC) vs mid-2019 franchise-row anchors — different units, same strategic question.</figcaption>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart13_deal_price_vs_revenue.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart13_deal_price_vs_revenue.png" data-source="Data: entities_companies_deals.csv — ARTOMETRICS" role="img" aria-label="M&A price vs franchise row scale."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Pixar $7.4B vs Toy Story row $19.5B; Fox $71.3B vs Simpsons anchor $13.5B — infrastructure, not one IP.</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Acquisition price is capitalization of licensing you believe remains — not applause for one weekend.</p>
<p class="art-p"><strong>How we know.</strong> SEC filings S009–S012 in <code>entities_companies_deals.csv</code>; anchor franchise rows from S001.</p>
<p class="art-p"><strong>Mechanism.</strong> Pixar (2006, $7.4B), Marvel (2009, $4.0B), Lucasfilm (2012, $4.05B), 21st Century Fox (2019, ~$71.3B enterprise value per merger proxy).</p>
<p class="art-p"><strong>Counterexample.</strong> Fox’s check dwarfs The Simpsons row ($13.5B) because the deal bought cable, Hulu stake, and catalog infrastructure — compare price to parks and distribution capacity, not a single infobox.</p>

<h2 id="disney-segments" class="anchored">DISNEY SEGMENT REVENUE — AUDITED FY2024</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart9_disney_segments_fy2024.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart9_disney_segments_fy2024.png" data-source="Data: Disney Form 10-K FY2024 — ARTOMETRICS" role="img" aria-label="Bar chart of Disney FY2024 revenue by segment."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Entertainment $41.2B, Sports $17.6B, Experiences $34.2B — fiscal year ended September 28, 2024 (S081).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> Wikipedia franchise rows are illustrative lifetime totals; Disney’s 10-K is audited annual revenue — Experiences is the physical licensing engine.</p>
<p class="art-p"><strong>How we know.</strong> Segment revenues table in FY2024 Q4 earnings exhibit: Entertainment $41.186B, Sports $17.619B, Experiences $34.151B (<code>disney_segment_revenue_fy2024.csv</code>, S004, S081).</p>
<p class="art-p"><strong>Mechanism.</strong> Characters promoted in Entertainment segment monetise again at parks, resorts, cruise, and merchandise.</p>
<p class="art-p"><strong>Counterexample.</strong> Sports (ESPN) is large but not character-licensing — do not attribute ESPN dollars to Mickey Mouse rows.</p>

<h2 id="theatrical-seriality" class="anchored">THEATRICAL SERIALITY</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart7_top10_franchise_share.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart7_top10_franchise_share.png" data-source="Data: Box Office Mojo yearly charts — ARTOMETRICS" role="img" aria-label="Line chart of franchise installments as share of domestic top 10 films by year."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Franchise installments: 60% of domestic top 10 (2010) → 90% (2024) — manual coding (<code>top10_franchise_share_by_year.csv</code>).</figcaption>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart16_worldwide_top10_2025_2026.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart16_worldwide_top10_2025_2026.png" data-source="Data: Wikipedia 2025/2026 in film (Box Office Mojo, The Numbers) — ARTOMETRICS" role="img" aria-label="Worldwide top-ten films of 2025 and 2026, franchise installments highlighted."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">2025: nine of ten worldwide hits were franchise entries (94.4% of top-ten gross). 2026 to October 12: six of ten (62.0%).</figcaption>
</figure>
<p class="art-p"><strong>What it means.</strong> The hit wide release is a serial product — recognition lowers marketing cost. 2026 is the first year in the series where originals hold real ground.</p>
<p class="art-p"><strong>How we know.</strong> Domestic: Box Office Mojo yearly rankings with manual coding (2019: 80%; 2024: 90%). Worldwide: the top-ten tables on Wikipedia's “2025 in film” and “2026 in film” pages (revisions 1378645325 and 1379926625, citing Box Office Mojo and The Numbers), coded as an installment if sequel, prequel, spin-off, remake or shared-universe entry. 2025 worldwide: 94.4% of top-ten gross, led by Ne Zha 2 ($2.32B) and Zootopia 2 ($1.87B); F1 was the only original.</p>
<p class="art-p"><strong>Mechanism.</strong> Shared universes amortise development; global day-and-date extends the theatrical window's marketing function for the merchandise that follows.</p>
<p class="art-p"><strong>Counterexample.</strong> 2026 so far is 62.0% franchise: The Odyssey ($1.78B), Michael ($1.03B), Project Hail Mary and Obsession are originals. Several 2026 titles are still in theaters, so the share will move.</p>

<h2 id="fragmented-libraries" class="anchored">SONY, UNIVERSAL, NINTENDO — FRAGMENTED VS MARRIED IP</h2>
<p class="art-p"><strong>Warner / DC.</strong> DC’s $46.1B on the 2026 list is Batman ($29.9B) plus Superman ($8.2B) plus the DC Extended Universe ($8.0B); it was $44.4B in the 2019 file. Wizarding World ($35.1B) is a separate Warner row, not DC. <strong>How we know:</strong> summed franchise rows in <code>franchise.csv</code> (S001). <strong>What it means:</strong> a CEO comparing “DC” to Harry Potter is mixing two libraries. <strong>Counterexample:</strong> a decade of extended-universe restarts shows that a large comic total does not run a film slate by itself.</p>
<p class="art-p"><strong>Sony / Marvel split.</strong> Spider-Man lists Marvel Entertainment (Disney) on merchandise with Sony Pictures on films. <strong>Mechanism:</strong> co-production splits enterprise value across balance sheets. <strong>Counterexample:</strong> Universal’s Fast &amp; Furious and Jurassic rows — blockbuster scale without Disney consolidation.</p>
<p class="art-p"><strong>Nintendo.</strong> The standalone Nintendo owner label was $49.0B in the 2019 file, and Mario alone is now listed at $9.74B after a source revision. The Pokémon row is $130.7B on the 2026 list. Those Pokémon dollars sit on The Pokémon Company string — Nintendo, Game Freak, and Creatures share the copyright — so they are not added to Nintendo’s $49.0B label. Nintendo licenses Mario selectively (the 2023 film, Super Nintendo World, LEGO Mario) while keeping creative control; it does not refuse every outside product.</p>

<h2 id="failure-modes" class="anchored">WHEN FRANCHISES BREAK</h2>
<p class="art-p">Ownership without discipline fails. Universal shelved the Dark Universe after <em>The Mummy</em> (2017). Warner’s Wizarding World sequels fell far from <em>Harry Potter</em> peaks. DC’s extended universe spent years in turnaround before the 2023 DC Studios reset. <em>Ghostbusters</em> (2016) showed reboot backlash; mobile-native <em>Angry Birds</em> shows revenue can peak and fade while rows remain in the table. See <code>data/franchise_failures.csv</code> for case links.</p>

<div class="art-callout" id="method-box">
<p class="art-p"><strong>Data &amp; method box.</strong> Primary ledger: Wikipedia's “List of highest-grossing media franchises”, revision 1379832186 (October 12, 2026), parsed by <code>scripts/franchise-data/clean_audit.py</code> into one row per franchise and stream. Wikipedia's stream labels are mapped to the original eight categories plus Live &amp; Other, Mixed and Unallocated. Baseline: TidyTuesday 2019-07-02 (S001), audited against the June 2019 Wikipedia revision it came from. Parent companies are as of October 2026. Ranges are 95% bootstraps over franchises. Sensitivity checks (dropping placeholders, the unallocated remainder, franchises below $4B, or new entries) move headline shares by under five points. Worldwide box office: Wikipedia's 2025 and 2026 film pages. Full rules, counts and sources: <code>CLEANING_LOG.md</code> and <code>METHODS_NOTE.md</code>. Do not treat franchise rows as studio profit. Sections on original medium, revenue per year, Disney consolidation, box-office share and acquisitions still use the 2019 file and say so.</p>
</div>

<h2 id="decision-tools" class="anchored">DECISION TOOLS FOR EXECUTIVES</h2>
<ul>
<li><strong>Ownership lens.</strong> Consolidate subsidiaries before benchmarking Disney vs Nintendo — otherwise you compare an incomplete parent to a consolidated rival (58.2% of the October 2026 ledger sits with five parent companies).</li>
<li><strong>Margin lens.</strong> Map cash to streams (merchandise, games, parks, subscription). Box office rank alone mis-ranks Hello Kitty against Pokémon; chart 14 is the reminder.</li>
<li><strong>Capital lens.</strong> A deal price is what you pay for the rights you still expect to sell. Set Pixar’s $7.4B, Marvel’s $4.0B, Lucasfilm’s $4.05B, and Fox’s $71.3B next to the franchise rows they anchor, then next to Experiences revenue of $34.2B in FY2024.</li>
<li><strong>Time lens.</strong> Name the vintage. Pokémon is $90.9B in the 2019 file and $130.7B in October 2026; Hello Kitty’s drop is a source revision, not a collapse.</li>
<li><strong>Theatrical lens.</strong> Franchise entries took 94.4% of 2025’s worldwide top-ten gross; 2026’s originals show the window is not closed.</li>
</ul>

<h2 id="limitations" class="anchored">LIMITATIONS</h2>
<p class="art-p">Wikipedia estimates are editorial compilations of press and trade figures, revised over time; they measure consumer spend, not licensor income or profit. Totals are nominal sums across decades and cannot be inflation-adjusted honestly. Itemisation varies by franchise: eight franchises list more than 5% of their total without a breakdown (Transformers itemises $10.1B of $25.0B). The English list under-covers some Japanese and Chinese properties. Streaming revenue is not in the data — no free source reports it per franchise in dollars. Region and parent coding are rule-based with documented hand overrides. 2026 box office is in progress. Bootstrap ranges describe sensitivity to which franchises are listed, not sampling error in the usual sense.</p>

<h2 id="conclusion" class="anchored">CONCLUSION</h2>
<p class="art-p">Franchise economics rewards objects you can sell repeatedly — cards, toys, park tickets — more than minutes in a theater: 55.8% of the October 2026 ledger is merchandise. Pokémon ($130.7B) now outsells Star Wars and the MCU combined. Five parent companies own 58.2% of the table. The US holds the scale; Japan holds the merchandise share. The box office became a sequel chart, with 94.4% of 2025's top-ten gross going to franchises, although 2026's originals show the door is not shut. For a buyer: name the vintage, name the parent, and check whether a big move is a market change or a source revision.</p>

<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">Rebuild charts and derived CSVs: <code>npm run brief:franchise</code> from the repository root (<code>articles/franchise/scripts/build_brief.R</code>, then <code>scripts/sync-article.mjs</code>). Verify headline figures: <code>npm run verify:franchise</code>. Bibliography: <code>articles/franchise/references.bib</code>. Image credits: <code>articles/franchise/CREDITS</code>. Video scripts and storyboard CSVs: <code>articles/franchise/video/</code> (no audio rendered in-repo).</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<ul>
<li>TidyTuesday (2019-07-02). <em>Media Franchise Revenues</em> (S001). <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-07-02" rel="noopener noreferrer">github.com/rfordatascience/tidytuesday/…/2019-07-02</a></li>
<li>Wikipedia. <em>List of highest-grossing media franchises</em> — revision 904026364, 2019-06-29 (audit of S001); revision 1379832186, 2026-10-12 (primary ledger, S017). Accessed 2026-10-12.</li>
<li>Wikipedia. <em>2025 in film</em> (rev. 1378645325) and <em>2026 in film</em> (rev. 1379926625), citing Box Office Mojo and The Numbers (S091, S092). Accessed 2026-10-12.</li>
<li>Federal Reserve Bank of St. Louis. CPI-U, CPIAUCSL (S090). Accessed 2026-10-12.</li>
<li>Robinson, D. (2019). <em>Analyzing Franchise Revenue — TidyTuesday Screencast</em>. <a href="https://youtu.be/1xsbTs9-a50" rel="noopener noreferrer">youtu.be/1xsbTs9-a50</a></li>
<li>Jenkins, H. (2006). <em>Convergence Culture</em>. NYU Press.</li>
<li>Steinberg, M. (2012). <em>Anime's Media Mix</em>. University of Minnesota Press.</li>
<li>Hernández Hernández, Á. D. (2018). Production committees (Arts 7(3): 42). <a href="https://doi.org/10.3390/arts7030042" rel="noopener noreferrer">doi:10.3390/arts7030042</a></li>
<li>The Walt Disney Company. Form 10-K FY2024; segment revenues exhibit (S004, S081).</li>
<li>Box Office Mojo yearly domestic charts (2010–2024) — <code>data/box_office_mojo_yearly_urls.csv</code>.</li>
</ul>
</section>

<h2 id="editors-note" class="anchored">EDITOR'S NOTE</h2>
<div class="art-editorial-note"><p class="art-p"><em>October 2026 update: the ledger was rebuilt from Wikipedia’s current list (140 franchises), the 2019 file was audited against its source, every headline was recomputed with 95% ranges, the Japan–US section was rewritten after the ranking reversed, and 2025–2026 worldwide box office was added. See <a href="/franchise-data-fix">What changed when we fixed the data</a>. Earlier note: this R2 revision recomputes headline percentages from the committed franchise.csv, adds 2019–2026 Wikipedia crosswalk charts, region and stream-mix views, Box Office Mojo and Disney 10-K charts, and ships three video scripts with phrase-level storyboard CSVs. Human editorial direction; AI-assisted analysis and chart code per Artometrics workflow.</em></p><p class="art-p">— Artometrics Editorial Desk</p></div>

<p class="art-github-wrap">
<a class="art-github-btn" href="https://github.com/Artometrics/artometrics-web/tree/main/articles/franchise" target="_blank" rel="noopener noreferrer">Article monorepo folder</a>
</p>
</main>
</div>
