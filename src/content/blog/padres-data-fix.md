---
title: "PADRES: What Changed When We Fixed the Data"
slug: padres-data-fix
author: kyle-mcauliffe
pubDate: 2026-10-13T00:00:00.000Z
description: >-
  We audited the Padres dataset behind our record-sale report, rebuilt it from Lahman 1969–2025 plus a verified 2026 season, and reconciled every number the July 2026 live page had published—including a corrupted HTML sync, stale sale copy, and an FAQ that claimed eight runs in two deciding games.
heroImage: /images/content/articles/padres/hero.png
draft: false
tags:
  - sports
  - baseball
subject: Padres
tldr: >-
  The July live page lost four sections and broke three charts; audio pointed at the wrong file. Rebuilt on Lahman (CC BY-SA) with 2026 from Baseball-Reference (91–71, swept the Cubs, lost the NLDS to Milwaukee). Ten postseasons in 58 seasons; series record 8–10. Tax payroll sum is $1,500.1M, not cash. Better-record teams won 53.2% of untied playoff series, 1995–2025 [47.2–59.3% bootstrap].
keyPoints:
  - "10 — postseasons in 58 seasons after the completed 2026 campaign (was 9 in 57)"
  - "91-71 — 2026 record; MLB Stats API matches Baseball-Reference"
  - "0 + 1 — runs in the 2024 and 2025 deciding games (FAQ had claimed eight combined)"
  - "Unanimous — owners approved the sale Aug 17, 2026 (page had still waited on 22 owners)"
  - "53.2% [47.2–59.3] — share of untied playoff series the better regular-season team won, 1995–2025"
---
<div id="quarto-content">
<main class="art-article-main">

<div class="art-callout" id="executive-summary">
<p class="art-p"><strong>Executive summary.</strong> Research is only as good as its ledger, so we treat corrections as findings. We re-audited the data behind <a href="/padres">PADRES: Record Sale, Zero Championships</a>, fixed a broken sync to the live HTML body, and recomputed every number we had published. The thesis survives: demand and tax payroll are solved; conversion is not; franchise values still track the market. What changed is the calendar. The sale is approved. Milwaukee ended 2026. The FAQ no longer claims eight runs in two winner-take-all games.</p>
</div>

<h2 id="what-we-checked" class="anchored">WHAT WE CHECKED</h2>
<p class="art-p">The July 2026 live page in <code>src/content/blog/padres.md</code> had lost four sections (Fifty-seven seasons, Preller doctrine, tax-bill section, expansion peers), spliced the expansion “alibi” paragraph onto the Wrigley opener, and left charts 1, 3, and 4 without working embeds. <code>audioSrc</code> pointed at <code>/audios/padres.mp3</code> (SPA fallback) instead of <code>/audios/padres-the-artometrics-of-paying-for-october.mp3</code>. The Quarto source at <code>articles/padres/</code> was intact; the publish merge was not.</p>
<p class="art-p">We rebuilt the numeric ledger from Lahman’s 2025 database (Padres 1969–2025, CC BY-SA 3.0), added the completed 2026 season from Baseball-Reference, and fact-checked 91–71 against the MLB Stats API NL standings (see <code>data/padres/verify/mlb_api_check.json</code>). Competitive-balance-tax payrolls remain the Spotrac compilation in the July 2026 draft—labeled as tax payroll, not cash. One script reproduces the clean tables: <code>python3 scripts/padres-data/clean_audit.py</code> (rules in <code>CLEANING_LOG.md</code>, intervals in <code>METHODS_NOTE.md</code>).</p>

<h2 id="old-vs-new" class="anchored">OLD VS NEW</h2>
<p class="art-p"><strong>Published</strong> is what the July 2026 live page or sports-canon generator stated. <strong>Raw new</strong> recomputes from Lahman without changing the file. <strong>Clean new</strong> is the October 2026 audit, including 2026 and copy fixes. Brackets on rates are 95% bootstrap ranges (5,000 draws, seed 20261013).</p>
<div class="art-table-wrap"><table class="art-table">
<thead><tr><th>Figure</th><th>Published</th><th>Raw new</th><th>Clean new (Oct 2026)</th><th>Status</th></tr></thead>
<tbody>
<tr><td>Franchise seasons counted</td><td>57</td><td>57</td><td><strong>58</strong></td><td>updated</td></tr>
<tr><td>Postseason appearances</td><td>9</td><td>9</td><td><strong>10</strong></td><td>updated</td></tr>
<tr><td>2026 regular-season record</td><td>55-53 in progress</td><td></td><td><strong>91-71</strong></td><td>corrected</td></tr>
<tr><td>Postseason series record</td><td>7-9</td><td>7-9</td><td><strong>8-10</strong></td><td>updated</td></tr>
<tr><td>Sale approval</td><td>waits on 22 of 29 owners</td><td></td><td><strong>unanimous Aug 17, 2026</strong></td><td>corrected</td></tr>
<tr><td>FAQ deciding-game runs (2024+2025)</td><td>combined eight runs</td><td></td><td><strong>0 + 1</strong></td><td>corrected</td></tr>
<tr><td>Payroll headline</td><td>about $1.5bn of payroll / cash spent</td><td>1500.1</td><td><strong>$1,500.1M CBT tax payroll sum</strong></td><td>corrected</td></tr>
<tr><td>Pennant chart first bar</td><td>years between pennants</td><td></td><td><strong>debut to first pennant (15 years)</strong></td><td>corrected</td></tr>
<tr><td>Better record among untied series, 1995–2025</td><td>53.2%</td><td>53.2%</td><td><strong>53.2% [47.2–59.3]</strong></td><td>unchanged</td></tr>
<tr><td>2025 attendance</td><td>3,437,201</td><td>3,437,201</td><td><strong>3,437,201</strong></td><td>unchanged</td></tr>
<tr><td>2026 attendance</td><td></td><td></td><td><strong>3,347,081</strong></td><td>new</td></tr>
<tr><td>70,000 DTC subscribers</td><td>stated</td><td></td><td><strong>removed</strong></td><td>unsourced_removed</td></tr>
<tr><td>$858M owed five players</td><td>stated</td><td></td><td><strong>removed</strong></td><td>unsourced_removed</td></tr>
<tr><td>Farm rank last of 30</td><td>stated</td><td></td><td><strong>removed</strong></td><td>unsourced_removed</td></tr>
</tbody>
</table></div>
<p class="art-p">The full machine-readable ledger is <code>data/padres/clean/old_vs_new.csv</code> (mirrored under <code>public/data/articles/padres/data/</code>).</p>

<h2 id="why-it-moved" class="anchored">WHY THE BIG NUMBERS MOVED</h2>
<p class="art-p"><strong>Calendar, not math.</strong> Lahman through 2025 was already correct on wins, attendance, and the 132/116/11 coin-flip split. The step change is 2026: a third straight postseason, a wild-card sweep of the Cubs, and an NLDS loss to the Brewers—the club the July draft had used as a low-payroll alibi.</p>
<p class="art-p"><strong>Copy and sync, not sources.</strong> The eight-run FAQ line had no box-score support (Games 4–5 of the 2024 NLDS were shutouts; the 2025 wild-card deciding game was 1–3). The sale paragraph was stale after the unanimous August vote. The pennant-gap chart mislabeled the first bar; the axis now distinguishes debut-to-first-pennant from gaps between flags.</p>
<p class="art-p"><strong>Wording on payroll.</strong> Summing six Spotrac competitive-balance-tax payrolls is not the same as cash spent. The report now says $1,500.1 million of <em>tax payroll</em>, with 2026 still a July snapshot.</p>

<h2 id="method" class="anchored">METHOD NOTES</h2>
<p class="art-p">Bootstrap rates in <code>rate_bootstrap.csv</code>: better record among untied series 0.5323 [0.4718–0.5927], n = 248; Padres postseason rate 10/58 = 0.1724 [0.0862–0.2759]; pennants per postseason (Lahman-era PS only) 0.2222 [0.0–0.5556], n = 9. See <code>scripts/padres-data/METHODS_NOTE.md</code> and <code>DATA_DICTIONARY.md</code>.</p>

<h2 id="editors-note" class="anchored">EDITOR'S NOTE</h2>
<div class="art-editorial-note"><p class="art-p"><em>Part of our corrections series: we publish what changed, and why, whenever we fix a dataset. Human editorial direction; AI-assisted analysis per Artometrics workflow.</em></p><p class="art-p">— Artometrics Editorial Desk</p></div>
</main>
</div>
