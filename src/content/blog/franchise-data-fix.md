---
title: "FRANCHISE: What Changed When We Fixed the Data"
slug: franchise-data-fix
author: kyle-mcauliffe
pubDate: 2026-10-12T00:00:00.000Z
description: >-
  We audited the franchise dataset behind our FRANCHISE report, rebuilt it from Wikipedia's October 2026 list and recomputed every published number. Merchandise still dominates (55.8%), but the Japan–US ranking flipped and Hello Kitty's $80B was a source error.
heroImage: /images/content/articles/franchise/hero.png
draft: false
tags:
  - arts
  - film
subject: Franchises
tldr: >-
  The 2019 TidyTuesday file sat below its own Wikipedia source (28 of 39 sampled franchises within 10%). Rebuilt on Wikipedia's October 2026 list (140 franchises), merchandise holds at 55.8%, box office rises from 8.9% to 18.3% mostly through better itemisation, the top five owners rise from 46.4% to 58.2%, and the US overtakes Japan ($816.5B vs $394.5B) while Japan's merchandise share rises to 71.4%.
keyPoints:
  - "28 of 39 — sampled 2019 franchises within 10% of their own Wikipedia source"
  - "55.8% — merchandise share, essentially unchanged from 56.0%"
  - "8.9% → 18.3% — box office share, mostly a measurement change"
  - "$80.0B → $33.5B — Hello Kitty, a source revision, not a collapse"
  - "Japan $681.5B → $394.5B; US $622.6B → $816.5B — the regional ranking flipped"
---
<div id="quarto-content">
<main class="art-article-main">

<div class="art-callout" id="executive-summary">
<p class="art-p"><strong>Executive summary.</strong> Research is only as good as its ledger, so we treat corrections as findings. We re-audited the data behind <a href="/franchise">FRANCHISE: Merchandise Owns the Ledger</a>, rebuilt it from Wikipedia's October 2026 list, and recomputed every number we had published. The core finding survives: merchandise is still 55.8% of franchise revenue. Three readings change. Box office looks twice as big, but mostly because it is now counted more completely. Ownership is more concentrated (top five parents 58.2%, up from 46.4%). And the Japan–US comparison reverses.</p>
</div>

<h2 id="what-we-checked" class="anchored">WHAT WE CHECKED</h2>
<p class="art-p">The original report used the TidyTuesday file of July 2, 2019: 321 rows, 103 franchises, eight revenue categories. It had no missing values or duplicates, but it had 15 placeholder rows under $10 million (Star Wars TV at $0.004B), six cells with leftover Wikipedia citation tags, 59 with stray double spaces, and owner names from 2019 (AT&amp;T, Viacom, Activision Blizzard).</p>
<p class="art-p">We then checked it against the source it was scraped from — the Wikipedia revision of June 29, 2019 — for a random sample of 40 franchises (seed 20261012). Thirty-nine matched. Only 5 agreed with the itemised breakdown within 1%, and 28 of 39 came within 10% of the headline total. The file was always lower, because its eight-category schema dropped line items that did not fit: card games, theme parks, pachinko. James Bond is the extreme case at $13.9B against $19.9B.</p>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart18_verification_2019.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart18_verification_2019.png" data-source="Data: S001, S017 — ARTOMETRICS" role="img" aria-label="Scatter of TidyTuesday sums against Wikipedia 2019 totals."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Every sampled franchise sits on or below the line: the 2019 file under-counts its own source.</figcaption>
</figure>

<h2 id="old-vs-new" class="anchored">OLD VS NEW</h2>
<p class="art-p"><strong>Published</strong> is the number in the report before October 2026. <strong>Raw new</strong> recomputes it from the unchanged 2019 file (every figure reproduces exactly). <strong>Clean new</strong> uses the rebuilt October 2026 ledger; brackets are 95% bootstrap ranges. Dollar figures are USD billions, nominal.</p>
<div class="art-table-wrap"><table class="art-table">
<thead><tr><th>Figure</th><th>Published</th><th>Raw new</th><th>Clean new (Oct 2026)</th><th>Why it moved</th></tr></thead>
<tbody>
<tr><td>Franchises in dataset</td><td>103</td><td>103</td><td><strong>140</strong></td><td>Wikipedia's list grew; 82 of 103 franchises carried over, 58 are new, 21 dropped off.</td></tr>
<tr><td>Total lifetime revenue</td><td>1522.2</td><td>1522.2</td><td><strong>1448.1</strong></td><td>More franchises, but large downward source revisions (Hello Kitty, Mario, Gundam) outweigh them.</td></tr>
<tr><td>Merchandise, Licensing &amp; Retail share</td><td>56.0</td><td>56.0</td><td><strong>55.8 [44.0–66.2]</strong></td><td>Essentially unchanged; the 95% range is wide.</td></tr>
<tr><td>Video games share</td><td>20.0</td><td>20.0</td><td><strong>17.9 [11.2–26.2]</strong></td><td>Slightly lower; mobile-game revenue is now itemised under several franchises.</td></tr>
<tr><td>Box office share</td><td>8.9</td><td>8.9</td><td><strong>18.3 [12.8–25.6]</strong></td><td>Mostly measurement: the 2019 file's eight categories dropped line items, and today's list itemises film grosses more fully. 15.4% on franchises in both vintages.</td></tr>
<tr><td>Pokemon lifetime revenue</td><td>90.863</td><td>90.863</td><td><strong>130.7</strong></td><td>Seven more years of sales plus a fuller retail estimate ($119.3B).</td></tr>
<tr><td>Hello Kitty lifetime revenue</td><td>80.026</td><td>80.026</td><td><strong>33.5</strong></td><td>Source revision: editors replaced the older retail estimate.</td></tr>
<tr><td>Winnie the Pooh lifetime revenue</td><td>74.519</td><td>74.519</td><td><strong>50.2</strong></td><td>Source revision of Disney merchandise estimates.</td></tr>
<tr><td>Pokemon 2026 Wikipedia lifetime</td><td>130.7</td><td></td><td><strong>130.7</strong></td><td>Unchanged pair from 2026 list.</td></tr>
<tr><td>Call of Duty 2026 Wikipedia lifetime</td><td>31.0</td><td></td><td><strong>31.0</strong></td><td>Unchanged pair from 2026 list.</td></tr>
<tr><td>Naruto 2026 Wikipedia lifetime</td><td>22.8</td><td></td><td><strong>22.8</strong></td><td>Unchanged pair from 2026 list.</td></tr>
<tr><td>Mortal Kombat 2026 Wikipedia lifetime</td><td>5.06</td><td></td><td><strong>5.06</strong></td><td>Unchanged pair from 2026 list.</td></tr>
<tr><td>Star Wars lifetime</td><td>63.004</td><td>63.004</td><td><strong>46.7</strong></td><td>Source revision; merchandise estimate reduced.</td></tr>
<tr><td>MCU lifetime</td><td>31.0</td><td>31.0</td><td><strong>37.5</strong></td><td>Seven more years of box office (2019–2026 releases).</td></tr>
<tr><td>Disney consolidated owner total</td><td>426.209</td><td></td><td><strong>430.69</strong></td><td>Same consolidation rule applied to the 2026 list.</td></tr>
<tr><td>Top-five owner share after Fox consolidation</td><td>46.4</td><td></td><td><strong>58.2 [52.7–72.6]</strong></td><td>Consolidation since 2019 (Activision Blizzard into Microsoft, Paramount Skydance) and parents assigned as of 2026.</td></tr>
<tr><td>Top owner share after Fox consolidation</td><td>28.0</td><td></td><td><strong>29.7 [18.2–43.4]</strong></td><td>Disney's share barely moves; range shown.</td></tr>
<tr><td>Simpsons 2026 Wikipedia lifetime</td><td>4.9</td><td></td><td><strong>4.9</strong></td><td>Unchanged pair from 2026 list.</td></tr>
<tr><td>Japan region lifetime</td><td>681.494</td><td></td><td><strong>394.46</strong></td><td>Japanese totals revised down at source and several Japanese franchises left the English list.</td></tr>
<tr><td>Japan merchandise share</td><td>49.1</td><td></td><td><strong>71.4</strong></td><td>What remains in Japan's ledger is character-goods engines (Pokémon, Anpanman, Hello Kitty).</td></tr>
<tr><td>US region lifetime</td><td>622.59</td><td></td><td><strong>816.47</strong></td><td>43 more US-origin franchises on the 2026 list.</td></tr>
<tr><td>US merchandise share</td><td>64.6</td><td></td><td><strong>52.0</strong></td><td>New US entries add box office (MCU) and games (Call of Duty, Fortnite).</td></tr>
<tr><td>Japan franchise count</td><td>42</td><td></td><td><strong>30</strong></td><td>Coverage of the English list; region rules in CLEANING_LOG.</td></tr>
<tr><td>US franchise count</td><td>45</td><td></td><td><strong>88</strong></td><td>Coverage of the English list.</td></tr>
<tr><td>Hello Kitty 2026 Wikipedia lifetime</td><td>33.5</td><td></td><td><strong>33.5</strong></td><td>Unchanged pair from 2026 list.</td></tr>
<tr><td>Mario 2026 Wikipedia lifetime</td><td>9.74</td><td></td><td><strong>9.74</strong></td><td>Unchanged pair from 2026 list.</td></tr>
<tr><td>Gundam 2026 Wikipedia lifetime</td><td>5.0</td><td></td><td><strong>5.0</strong></td><td>Unchanged pair from 2026 list.</td></tr>
<tr><td>Toy Story lifetime</td><td>19.54</td><td>19.54</td><td><strong>16.0</strong></td><td>Re-sourced merchandise; Toy Story 5 (2026) not yet fully counted.</td></tr>
<tr><td><strong>New:</strong> franchise share of worldwide top-10 gross, 2025 releases</td><td></td><td></td><td><strong>94.4</strong></td><td></td></tr>
<tr><td><strong>New:</strong> franchise share of worldwide top-10 gross, 2026 releases (to Oct 12)</td><td></td><td></td><td><strong>62.0</strong></td><td></td></tr>
<tr><td><strong>New:</strong> franchises on Oct-2026 list not in ledger</td><td></td><td></td><td><strong>58</strong></td><td></td></tr>
</tbody></table></div>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/franchise/charts/chart17_old_vs_new_2026.plotly.json" data-fallback="/images/content/articles/franchise/charts/chart17_old_vs_new_2026.png" data-source="Data: S001, S017 — ARTOMETRICS" role="img" aria-label="Dumbbell chart of published versus corrected franchise totals."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Grey: published 2019 figure. Blue: October 2026. Pokémon, Call of Duty, Naruto and the MCU grew; Hello Kitty, Mario and Gundam were revised at the source.</figcaption>
</figure>

<h2 id="why-it-moved" class="anchored">WHY THE BIG NUMBERS MOVED</h2>
<p class="art-p"><strong>Source revisions, not declines.</strong> Hello Kitty ($80.0B→$33.5B), Mario ($35.0B→$9.74B) and Gundam ($25.5B→$5.0B) fell because Wikipedia editors replaced older estimates with better-sourced ones. Neither Sanrio nor Nintendo reported a collapse. We flag these rows rather than quote them as change.</p>
<p class="art-p"><strong>Real growth.</strong> Pokémon (+$39.8B), Call of Duty (+$14.0B) and Naruto (+$13.9B) added seven years of sales and newly itemised mobile revenue.</p>
<p class="art-p"><strong>Measurement.</strong> Box office went from 8.9% to 18.3% of the ledger. On the 82 franchises in both vintages it is 15.4%, and on franchises above $4B it is 15.0%. Most of the jump is the 2026 list counting theatrical grosses more completely.</p>
<p class="art-p"><strong>Coverage.</strong> The list grew from 103 to 140. Forty-three of the 58 additions are US-origin (Fortnite, Avatar, Madden NFL), while Japanese titles such as Detective Conan, Digimon and Bleach left the English table. Together with the downward revisions, that turns “Japan out-earns the US” into “the US out-earns Japan, and Japan is more merchandise-heavy.”</p>
<p class="art-p"><strong>Consolidation.</strong> Assigning franchises to today's parents (Activision Blizzard and King into Microsoft, Fox into Disney, Viacom into Paramount Skydance) lifts the top-five share. On the same 2019 franchises it would be 62.8%.</p>

<h2 id="what-we-added" class="anchored">WHAT WE ADDED AND DROPPED</h2>
<ul>
<li><strong>Added:</strong> the full October 2026 ledger (140 franchises, every itemised stream), worldwide top-ten box office for 2025 and 2026, 2026 parent companies, region of origin with documented hand assignments, 95% ranges and sensitivity checks.</li>
<li><strong>Kept, flagged:</strong> the 15 placeholder rows (excluding them changes no share), and $27.2B listed in totals but not itemised (kept as “Unallocated”).</li>
<li><strong>Not added:</strong> streaming revenue, because no free source reports it per franchise in dollars; inflation-adjusted lifetime totals, because they mix decades with no year split; Disney FY2025 segments, which are a pending update.</li>
<li><strong>Dropped:</strong> no rows from the 2019 file. It stays as the audited baseline.</li>
</ul>

<h2 id="method" class="anchored">METHOD NOTES</h2>
<p class="art-p">One script rebuilds everything from committed snapshots: <code>scripts/franchise-data/clean_audit.py</code>, with rules R1–R10, flow counts, and sources in <code>CLEANING_LOG.md</code>, <code>METHODS_NOTE.md</code> and <code>DATA_DICTIONARY.md</code>. Sources: Wikipedia “List of highest-grossing media franchises” revisions 904026364 (2019-06-29) and 1379832186 (2026-10-12); “2025 in film” and “2026 in film” (citing Box Office Mojo and The Numbers); FRED CPI-U. All accessed October 12, 2026. Bootstrap: 5,000 resamples of franchises.</p>

<h2 id="limitations" class="anchored">LIMITATIONS</h2>
<p class="art-p">Wikipedia figures are editors' estimates of consumer spend, not audited revenue or profit, and they will be revised again. The list is not a random sample, so bootstrap ranges describe sensitivity to which franchises appear, not sampling error. Region and parent coding involve judgment, documented line by line. 2026 box office is still moving. The video versions of FRANCHISE still use 2019 figures and will be re-recorded.</p>

<h2 id="editors-note" class="anchored">EDITOR'S NOTE</h2>
<div class="art-editorial-note"><p class="art-p"><em>Part of our corrections series: we publish what changed, and why, whenever we fix a dataset. Human editorial direction; AI-assisted analysis per Artometrics workflow.</em></p><p class="art-p">— Artometrics Editorial Desk</p></div>
</main>
</div>
