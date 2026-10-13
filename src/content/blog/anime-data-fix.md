---
title: "ANIME: What Changed When We Fixed the Data"
slug: anime-data-fix
author: kyle-mcauliffe
pubDate: 2026-10-13T00:00:00.000Z
description: >-
  We refreshed the MyAnimeList catalog behind ANIME after Jikan shut down, moved to the Tenrai-compatible API, and recomputed every headline on the clean TV frame. The light-novel reach premium fell from 32× to 27.5×; manga's 8.0+ share fell to 14.8%; 2015 isekai was under-counted at 0.9% (now 2.2%).
heroImage: /images/content/articles/anime/hero.webp
draft: false
tags:
  - arts
  - film
subject: Anime
tldr: >-
  MyAnimeList's free Jikan API ended 2026-10-01; we rebuilt on Tenrai + AniList (18,813 clean rows). On TV: LN÷Original median members 32.0× → 27.5×; manga ≥8.0 share 17.0% → 14.8%; isekai share 2015 0.9% → 2.2%, 2021 20.4% (unchanged), 2024 17.7% → 18.1%; manga+web manga 2024 holds 47.2%. Validation: 73% AniList score agreement within 0.5 (n=200).
keyPoints:
  - "27.5× — LN vs original median members on TV (was 32.0×)"
  - "14.8% — manga TV titles scoring 8.0+ (was 17.0%)"
  - "2.2% — isekai-tagged TV share in 2015 (was 0.9%); 2021 still 20.4%"
  - "47.2% — manga + web manga among 2024 TV premieres (unchanged)"
  - "73% — AniList agreement within 0.5 on scores (n = 200)"
---
<div id="quarto-content">
<main class="art-article-main">

<div class="art-callout" id="executive-summary">
<p class="art-p"><strong>Executive summary.</strong> The ANIME report's core story survives on the October 2026 ledger: source material still sets the audience floor, and isekai tags trace a real production wave. What changed is measurement. When MyAnimeList's public Jikan mirror shut down on <strong>2026-10-01</strong>, we finished the refresh through <strong>Tenrai</strong> (<code>api.tenrai.org</code>, Jikan-compatible) and recomputed every headline on <code>anime_2026-10-11_clean</code> with one script. The light-novel reach multiple narrows from <strong>32.0×</strong> to <strong>27.5×</strong>. Manga's high-score share falls from <strong>17.0%</strong> to <strong>14.8%</strong>. The 2015 isekai point was an under-tag in the old exploratory frame (<strong>0.9% → 2.2%</strong>); 2021 stays <strong>20.4%</strong> and 2024 edges to <strong>18.1%</strong>. Single-year shares are trends, not precise point estimates — bootstrap ranges are about <strong>±5 percentage points</strong>.</p>
</div>

<h2 id="why-we-refreshed" class="anchored">WHY WE REFRESHED</h2>
<p class="art-p">The published report rested on the TidyTuesday export of <strong>2019-04-23</strong> (13,631 unique titles). A parallel pipeline had already grown the catalog to <strong>18,818</strong> rows with AniList tags, streaming links, and season fields. On <strong>2026-10-01</strong>, MyAnimeList discontinued the free <strong>Jikan v4</strong> API (<code>api.jikan.moe</code>). We completed metadata fetches through <strong>Tenrai</strong>, which mirrors the same Jikan field schema, then ran <code>scripts/anime-data/clean_audit.py</code> (seed <code>20261011</code>) to produce <code>anime_2026-10-11_clean.*</code> with documented inclusion rules and bootstrap ranges.</p>

<h2 id="old-vs-new" class="anchored">OLD VS NEW</h2>
<p class="art-p"><strong>Published / exploratory</strong> is what readers saw before this audit. <strong>Clean new</strong> is the October 2026 TV frame from the clean file; brackets are 95% bootstrap ranges where shown.</p>
<div class="art-table-wrap"><table class="art-table">
<thead><tr><th>Figure (TV unless noted)</th><th>Published</th><th>Clean new (Oct 2026)</th><th>Why it moved</th></tr></thead>
<tbody>
<tr><td>Rows in catalog</td><td>13,631 (2019 snapshot)</td><td><strong>18,813</strong> clean</td><td>+5,187 new MAL ids; scores and members updated to October 2026.</td></tr>
<tr><td>LN ÷ Original median members</td><td>32.0×</td><td><strong>27.5×</strong></td><td>2026 member counts on a wider TV catalog; originals grew slightly faster at the median.</td></tr>
<tr><td>Manga share scoring 8.0+</td><td>17.0%</td><td><strong>14.8%</strong></td><td>More manga TV titles in the denominator; scores drifted over seven years.</td></tr>
<tr><td>Isekai share, 2015 premieres</td><td>0.9%</td><td><strong>2.2% [0.4%–4.3%]</strong> (n=230)</td><td>Explicit tag rule across MAL themes and AniList tags; old figure used a thinner tag field.</td></tr>
<tr><td>Isekai share, 2021 premieres</td><td>20.4%</td><td><strong>20.4% [15.2%–25.6%]</strong> (n=211)</td><td>Stable under the new rule — the wave peak still lands here.</td></tr>
<tr><td>Isekai share, 2024 premieres</td><td>17.7%</td><td><strong>18.1% [13.7%–23.0%]</strong> (n=248)</td><td>Within uncertainty; read as elevated vs pre-2018, not a precise YoY tick.</td></tr>
<tr><td>Manga + web manga, 2024 premieres</td><td>47.2%</td><td><strong>47.2% [41.1%–53.2%]</strong> (n=248)</td><td>Unchanged point estimate; web manga share still ~12.5%.</td></tr>
<tr><td>Tenrai fetch failures</td><td>—</td><td><strong>156</strong> rows flagged</td><td>Retained with <code>flag_unfetched_jikan</code>; sensitivity shows no material shift for isekai 2024.</td></tr>
</tbody></table></div>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_shares_old_vs_corrected.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_shares_old_vs_corrected.png" data-source="Data: clean_audit.py · ARTOMETRICS" role="img" aria-label="Dumbbell chart of published versus corrected headline shares."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Grey: published or exploratory figures. Blue: October 2026 clean TV frame.</figcaption>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_ln_ratio_old_vs_clean.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_ln_ratio_old_vs_clean.png" data-source="Data: 2019 TidyTuesday vs Tenrai clean · ARTOMETRICS" role="img" aria-label="Light-novel versus original median member ratio by premiere year, old versus clean catalogs."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">The headline 32.0× → 27.5× gap is the all-years median ratio; within-year ratios track the same narrowing pattern.</figcaption>
</figure>

<h2 id="validation" class="anchored">WHAT WE CHECKED</h2>
<p class="art-p">We drew <strong>n = 200</strong> rows with both Tenrai/Jikan and AniList fields present (seed <code>20261011</code>). Score agreement within <strong>0.5</strong> points on the MAL 0–10 scale (<code>|MAL − AniList meanScore/10| ≤ 0.5</code>): <strong>146 / 200 = 73%</strong>. This is an offline check of already-joined fields — not a live re-fetch at audit time. Year agreement between <code>aired_from_year</code> and <code>season_year</code> was weaker (59.5%), which is why calendar-year shares carry wide bootstrap bands.</p>
<p class="art-p">Cleaning removed <strong>5</strong> rows missing id/name, normalized source labels, and nulled five end-before-start dates. No scores were imputed. Full PRISMA counts and rules R1–R7 are in <code>data/anime/CLEANING_LOG.md</code>.</p>

<h2 id="reading-shares" class="anchored">HOW TO READ SINGLE-YEAR SHARES</h2>
<p class="art-p">For any one premiere year, the 95% bootstrap interval is typically about <strong>±5 percentage points</strong> around the point estimate. That is wide enough that <strong>17.7% vs 18.1%</strong> for 2024 isekai should be read as <em>still elevated after the 2021 peak</em>, not as proof of a 0.4-point decline. The charts in the main report show the full 2010–2025 trend lines and stacked source mix instead of over-interpreting one year.</p>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_isekai_by_year.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_isekai_by_year.png" data-source="Data: Tenrai clean · ARTOMETRICS" role="img" aria-label="Isekai share of TV titles by premiere year with bootstrap band."></div>
</figure>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_source_mix_2015_2025.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_source_mix_2015_2025.png" data-source="Data: Tenrai clean · ARTOMETRICS" role="img" aria-label="Stacked source mix for TV premieres 2015 through 2025."></div>
</figure>

<h2 id="limitations" class="anchored">LIMITATIONS</h2>
<p class="art-p">MyAnimeList popularity is not a probability sample. Tenrai is a mirror — 156 unfetched ids remain thin. AniList tags can label isekai more densely than MAL themes. Bootstrap intervals ignore studio clustering. Scores and members drift; October 2026 values are not a panel continuation of 2019 scores without modeling. The long-form ANIME video and some studio tables still describe the 2019 deduplicated file until a later pass; headline source and isekai figures in the report body now match this clean ledger.</p>

<h2 id="method" class="anchored">METHOD NOTES</h2>
<p class="art-p">One entry point rebuilds the audit artifacts: <code>python3 scripts/anime-data/clean_audit.py</code>. Charts: <code>python3 articles/anime/scripts/build_2026_charts.py</code>. Dictionary and academic note: <code>data/anime/DATA_DICTIONARY.md</code>, <code>data/anime/METHODS_NOTE.md</code>. Sources: TidyTuesday 2019-04-23 baseline; Tenrai API accessed 2026-10-12; AniList GraphQL via <code>idMal</code>. Seed <code>20261011</code>; bootstrap B = 2000.</p>

<h2 id="editors-note" class="anchored">EDITOR'S NOTE</h2>
<div class="art-editorial-note"><p class="art-p"><em>Part of our corrections series: we publish what changed, and why, whenever we fix a dataset. See also <a href="/franchise-data-fix">FRANCHISE: What changed when we fixed the data</a>. Human editorial direction; AI-assisted analysis per Artometrics workflow.</em></p><p class="art-p">— Artometrics Editorial Desk</p></div>
</main>
</div>
