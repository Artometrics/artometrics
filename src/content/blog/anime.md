---
title: "ANIME: Source Sets the Audience Floor"
slug: anime
author: kyle-mcauliffe
pubDate: 2026-03-31T00:00:00.000Z
description: >-
  On the October 2026 MyAnimeList ledger, light-novel TV adaptations still draw 27.5 times the median audience of originals. Source mix and isekai tags trace how committees greenlight shows — with wide uncertainty on any single year.
heroImage: /images/content/articles/anime/hero.webp
audioSrc: /audios/anime-r2.mp3
draft: false
tags:
  - arts
  - film
subject: Anime
tldr: >-
  Across 18,813 clean MyAnimeList titles (October 2026 snapshot, Tenrai + AniList), source material is still the strongest signal of a TV show's reach. At the median, light-novel adaptations draw 196,258 members and originals 7,133 — a 27.5× gap. Quality is harder to buy: 3.0% of original TV series and 1.6% of TV game adaptations score 8.0 or higher, against 14.8% of manga adaptations. Isekai tags trace a wave that peaks near 20.4% of 2021 TV premieres; single-year shares move only a few points once bootstrap ranges (about ±5 pts) are applied.
keyPoints:
  - "27.5× — median members, light-novel TV vs original TV (196,258 vs 7,133)"
  - "14.8% — share of scored manga TV titles scoring 8.0 or higher (n = 1,980)"
  - "20.4% — isekai-tagged share among 2021 TV premieres (trend; 95% CI ~±5 pts)"
  - "47.2% — manga plus web manga among 2024 TV premieres (unchanged on clean ledger)"
  - "0.73 — Spearman correlation between score and members (n = 18,704 scored titles)"
  - "11 — stand-alone high scorers buried past popularity rank 3,000"
faq:
  - question: Do light-novel adaptations score higher than original anime?
    answer: >-
      Yes. On scored TV titles in the October 2026 clean file, light-novel adaptations have a median score of 7.11 and originals 6.52. Committees adapt novels that already sell, so the gap reflects selection as well as quality.
  - question: Which studios are most consistent?
    answer: >-
      Among studios with 100 or more titles, OLM has the tightest spread of scores (IQR 0.70) at a median of 6.64. Bones has the tightest spread among the top-scoring studios (IQR 0.95).
  - question: Are anime sequels better than the originals?
    answer: >-
      TV sequels have a higher median score (6.99 vs 6.76). Mostly shows that already did well get a sequel, so this reflects selection, not an effect of being a sequel.
  - question: Does a high MyAnimeList score mean a show made money?
    answer: >-
      No. MyAnimeList reflects English-language enthusiast ratings in an October 2026 snapshot and contains no revenue, broadcast ratings, or box-office data.
---
<div id="quarto-content">
<nav id="TOC" role="doc-toc">
<h2 id="toc-title" class="anchored">IN THIS REPORT</h2>
<ul>
<li><a href="#research-question">Research question</a></li>
<li><a href="#format-waves">Each format wave lines up with a new distribution channel</a></li>
<li><a href="#source-floor">Source material sets the audience floor</a></li>
<li><a href="#isekai-and-source-mix">Isekai tags and source mix (2015–2025)</a></li>
<li><a href="#studio-league">Consistency is a studio trait</a></li>
<li><a href="#sequel-premium">Sequels score higher, consistent with mostly well-received shows getting one</a></li>
<li><a href="#buried-canon">Popularity tracks quality, with a short list of exceptions</a></li>
<li><a href="#limitations">Limitations</a></li>
<li><a href="#conclusion">Conclusion</a></li>
<li><a href="#data-methods-and-sources">Data, methods &amp; sources</a></li>
<li><a href="#editors-note">Editor's note</a></li>
</ul>
</nav>
<main class="art-article-main">
<p class="art-p"><em>Death Note</em> has 1,610,561 MyAnimeList members, more than any other anime in the archive, and scores 8.66. <em>Hanada Shounen-shi</em>, a 2002 series from the same studio, Madhouse, scores 8.11 and has 8,929. A MyAnimeList archive of <strong>18,813</strong> clean titles (October 2026 snapshot via Tenrai + AniList; see <a href="/anime-data-fix">what changed when we fixed the data</a>) suggests that much of a gap like that is set before anyone draws a frame, starting with where the story comes from.</p>
<p class="art-p">On television, light-novel adaptations draw a median of <strong>196,258</strong> platform members. Manga adaptations draw <strong>69,623</strong> and original series <strong>7,133</strong>, which puts light novels about <strong>27.5×</strong> ahead of originals on the clean TV frame. Quality follows a different pattern. Only <strong>3.0%</strong> of original TV series and <strong>1.6%</strong> of TV game adaptations score 8.0 or higher on scored TV rows, compared with <strong>14.8%</strong> of manga adaptations. Across all scored titles, a title's score and its audience move closely together, with a rank correlation of <strong>0.73</strong> (n = 18,704). Every comparison below is measured against the overall median score of <strong>6.36</strong> unless noted.</p>
<p class="art-p">This report reads the archive as the record of a production system, not a list of favorites. In that system, a production committee (seisaku iinkai) of publishers, broadcasters, music labels, and merchandisers pools the budget and splits copyright in proportion to each member's investment. The animation studio is typically a contracted manufacturer that doesn't own the IP (Hernández Hernández, 2018, §4.3; Mihara, 2018). The figures here are observed fan behavior on one platform. They show which projects found audiences, not which ones made money.</p>

<h2 id="research-question" class="anchored">RESEARCH QUESTION</h2>
<p class="art-p">Which decisions made before production (format, source material, studio, and whether to make a sequel) are associated with a title's reach and fan rating, and where does the platform's popularity record miss strong work?</p>

<h2 id="format-waves" class="anchored">Each format wave lines up with a new distribution channel</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_eras.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_eras.png" data-source="Data: MyAnimeList via TidyTuesday (Kaggle snapshot, early 2019) — ARTOMETRICS" role="img" aria-label="Small multiples of anime releases by year for TV, film, OVA, ONA, specials, and music, through 2018. OVA peaks in 1993 and ONA rises through 2018."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Each wave lines up with a new channel. Direct-to-video output peaked at 115 titles in 1993, and web-first releases grew more than fivefold between 2009 and 2018.</figcaption>
</figure>
<p class="art-p">Anime output is not one growth curve. It's a series of format waves, and each wave lines up with a new channel. Theatrical film dominates the early catalog. Original video animation (OVA), sold directly on tape and disc, ran at roughly 100 titles a year from 1990 to 1993 and peaked at 115 in 1993. Television then became the core of the catalog, with 4,260 TV titles in the archive. Original net animation (ONA), made for web distribution first, grew from 40 titles in 2009 to 104 in 2013 and 216 in 2018, for 1,321 in total.</p>
<p class="art-p">The archive records release format, not financing. Reading these waves as responses to new distribution channels is our editorial frame, not a measured finding, and the data can't show who paid for each wave. The context literature documents one wave directly: starting with Tetsuwan Atom (1963), TV anime was tied to sponsor merchandising (Steinberg, 2012).</p>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Direct-to-video</p>
<p class="art-p">The first OVA, <em>Dallos</em> (Studio Pierrot, December 1983), was co-directed by Mamoru Oshii (Pierrot archive; Anime News Network). The format became known for high production values and experimentation (Anime News Network, 2022). Its standouts include <em>Ginga Eiyuu Densetsu</em> (<em>Legend of the Galactic Heroes</em>, 1988), a 110-episode space epic that scores 9.10, the only OVA in the top 10 by score. <em>Golden Boy</em> (1995) drew the era's largest audience, 171,713 members, and Gainax's <em>Gunbuster</em> (1988) also stands out.</p>
</div>
<aside>
<div class="art-logo-row">
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_studio_pierrot.png" alt="Studio Pierrot" /><p class="art-logo__credit">Studio Pierrot logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_gainax.svg" alt="Gainax" /><p class="art-logo__credit">Gainax logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
</div>
<div class="art-person">
<img class="art-person__photo" src="/images/content/articles/anime/assets/person_mamoru_oshii.jpg" alt="Mamoru Oshii" />
<p class="art-person__name">Mamoru Oshii</p>
<p class="art-person__role">Co-director of <em>Dallos</em> (Studio Pierrot, December 1983), the first OVA.</p>
<p class="art-person__credit">Photo: Niccolò Caranti / Wikimedia Commons, CC BY-SA 4.0</p>
</div>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Television</p>
<p class="art-p">Production committees became the standard way to finance TV anime, and by 2010 nearly 80% of anime was made this way, according to Taniguchi and Asō (2010) as reported by Hernández Hernández (2018). The biggest titles in the archive come from this era: <em>Death Note</em> (Madhouse, 2006), which aired after midnight on NTV, <em>Fullmetal Alchemist: Brotherhood</em> (Bones, 2009), <em>Naruto</em> (Studio Pierrot, 2002), and <em>Code Geass</em> (Sunrise, 2006). After 2010, <em>Shingeki no Kyojin</em> (<em>Attack on Titan</em>, Wit Studio, 2013) reached 1,500,958 members, second only to <em>Death Note</em>.</p>
</div>
<aside>
<div class="art-logo-row">
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_nippon_tv.svg" alt="Nippon TV" /><p class="art-logo__credit">Nippon TV (NTV) logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_madhouse.svg" alt="Madhouse" /><p class="art-logo__credit">Madhouse logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_wit_studio.svg" alt="Wit Studio" /><p class="art-logo__credit">Wit Studio logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_sunrise.svg" alt="Sunrise" /><p class="art-logo__credit">Sunrise logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
</div>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Web-first</p>
<p class="art-p">Crunchyroll began licensed simulcasts in 2008 and went licensed-only in January 2009, after its TV Tokyo deal (Ristola, 2024, p. 4), and that month it began streaming <em>Naruto Shippuden</em> on the same day as its Japanese broadcast. The ONA's biggest title is <em>Devilman: Crybaby</em> (Science SARU), a Netflix original released January 5, 2018, with 261,525 members (Netflix Media Center; Anime News Network). The Chinese production <em>Quanzhi Gaoshou</em> (<em>The King's Avatar</em>, 2017, 8.09) shows the format crossing borders.</p>
</div>
<aside>
<div class="art-logo-row">
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_crunchyroll.png" alt="Crunchyroll" /><p class="art-logo__credit">Crunchyroll logo via Wikimedia Commons (CC0)</p></div>
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_science_saru.png" alt="Science SARU" /><p class="art-logo__credit">Science SARU logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_netflix.svg" alt="Netflix" /><p class="art-logo__credit">Netflix logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
</div>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">For scale, beyond this dataset</p>
<p class="art-p">The Association of Japanese Animations put the Japanese anime industry market at ¥2,180.7 billion in 2018 and ¥3,346.5 billion in 2023, the second time overseas sales passed domestic ones (the first was 2020; AJA, English summaries; Anime Industry Report 2024 summary, p. 8). That is the whole industry's market, not studio revenue.</p>
</div>
<aside>
<div class="art-logo">
<img src="/images/content/articles/anime/assets/logo_aja.png" alt="Association of Japanese Animations" />
<p class="art-logo__credit">Association of Japanese Animations (AJA) logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p>
</div>
</aside>
</div>

<h2 id="source-floor" class="anchored">Source material sets the audience floor</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_scorecard.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_scorecard.png" data-source="Data: MyAnimeList via Tenrai (snapshot 2026-10-11 clean) — ARTOMETRICS" role="img" aria-label="Two panels of scored TV anime by source: median members as lollipops on a log scale, and the share scoring 8.0 or higher as bars."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Light-novel adaptations reach the largest audiences, but manga adaptations produce top-rated shows most often (scored TV titles, n = 6,073 of 6,095).</figcaption>
</figure>
<div class="art-table-wrapper"><table class="art-table"><thead><tr><th>Source (TV)</th><th>Titles</th><th>Median score</th><th>Median members</th><th>Share scoring 8.0+</th></tr></thead><tbody>
<!-- gen:source-table -->
<tr><td>Light novel</td><td>634</td><td>7.11</td><td>196,448</td><td>9.5%</td></tr>
<tr><td>Manga</td><td>1,980</td><td>7.17</td><td>69,623</td><td>14.8%</td></tr>
<tr><td>Novel</td><td>166</td><td>7.07</td><td>16,926</td><td>10.2%</td></tr>
<tr><td>Original</td><td>1,423</td><td>6.52</td><td>7,158</td><td>3.0%</td></tr>
<tr><td>Game</td><td>318</td><td>6.56</td><td>24,510</td><td>1.6%</td></tr>
<!-- /gen:source-table -->
</tbody></table></div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">The light-novel giants</p>
<p class="art-p">Some of the biggest shows on the site sit behind the 153,184 median. <em>Sword Art Online</em> (A-1 Pictures, 2012) has 1,442,099 members, the third-largest audience in the archive, yet it scores 7.58, which shows reach and rating moving apart. <em>No Game No Life</em> (Madhouse, 2014) and <em>Toradora!</em> (J.C.Staff, 2008) both pass a million members and both score 8.38. A typical adaptation is smaller: <em>Mahou Sensou</em> sits at exactly the median, with 153,184 members.</p>
</div>
<aside>
<div class="art-logo-row">
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_a1_pictures.svg" alt="A-1 Pictures" /><p class="art-logo__credit">A-1 Pictures logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_jc_staff.svg" alt="J.C.Staff" /><p class="art-logo__credit">J.C.Staff logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
</div>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">The originals that broke through</p>
<p class="art-p">The median original TV series draws 7,158 members on the clean ledger, but the exceptions rank among the site's biggest. <em>Code Geass</em> (Sunrise, 2006) has 1,082,349 members and scores 8.77. <em>Angel Beats!</em> (P.A. Works, 2010) has 1,105,583. Outside TV, the original film <em>Kimi no Na wa.</em> (<em>Your Name.</em>, CoMix Wave Films, 2016) scores 9.14, tied for second among titles with at least 1,000 ratings. Originals can reach the top, but only <strong>3.0%</strong> of scored original TV series reach 8.0 or higher.</p>
</div>
<aside>
<div class="art-logo-row">
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_pa_works.svg" alt="P.A. Works" /><p class="art-logo__credit">P.A. Works logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_comix_wave_films.svg" alt="CoMix Wave Films" /><p class="art-logo__credit">CoMix Wave Films logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
</div>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">The one TV game adaptation above 8.0</p>
<p class="art-p"><em>IDOLiSH7</em> (2018) adapts Bandai Namco Online's smartphone idol rhythm game. TROYCA animated it from character designs by the manga artist Arina Tanemura (official announcement, idolish7.com, Jan 17, 2017; Anime News Network, 2017). As of the early-2019 snapshot, its 17 episodes scored 8.06, making it the only TV game adaptation at 8.0 or higher (1 of 210), but it had just 18,254 members. Its live MAL score has since slipped to 7.69 (October 2026) as its raters grew from 4,788 to 26,755, so the 8.06 rested on a small, early sample. A later game adaptation, <em>Cyberpunk: Edgerunners</em> (Trigger, 2022), was released as a Netflix ONA rather than a TV series; it scores 8.62 on MAL as of October 2026. In the early-2019 snapshot, the next-best game adaptations are <em>Gungrave</em> (7.93) and <em>Pokémon XY&amp;Z</em> (7.77).</p>
</div>
<aside>
<div class="art-logo-row">
<div class="art-logo"><img src="/images/content/articles/anime/assets/logo_troyca.svg" alt="TROYCA" /><p class="art-logo__credit">TROYCA logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p></div>
<div class="art-logo"><p class="art-wordmark">Bandai Namco Online</p></div>
</div>
<div class="art-person art-person--text">
<p class="art-person__name">Arina Tanemura</p>
<p class="art-person__role">Manga artist. TROYCA animated <em>IDOLiSH7</em> from her character designs (official announcement, idolish7.com, Jan 17, 2017; Anime News Network, 2017).</p>
</div>
</aside>
</div>
<p class="art-p">The source of a story, its gensaku, is the biggest single dividing line in the TV catalog. Light-novel adaptations have the highest median score (7.11) and by far the largest median audience. They reach about three times as many members as manga adaptations and about <strong>27.5×</strong> as many as originals. That gap measures audience size, not quality or staying power. Manga adaptations are close behind on score (7.17), and they produce the highest share of top-rated shows, at <strong>14.8%</strong> scoring 8.0 or higher (294 of 1,980 scored manga TV titles).</p>
<p class="art-p">The mechanism is the media mix. A story is built across print, animation, music, and merchandise at once (Steinberg, 2012). On our reading, a published book also serves as a live test of demand before a committee commits money to animation. This is selection, not proof that adapting a book lowers risk. Committees adapt titles that already have readers, so some of that audience is arriving with the book.</p>
<p class="art-p">Originals face the opposite problem. Their median score is 6.52, and only <strong>3.0%</strong> reach 8.0 or higher. With no print run to test demand first, an original has to prove itself on air. Game adaptations are the weakest group by fan rating. Their median is 6.56, and only <strong>1.6%</strong> of scored TV game adaptations reach 8.0 or higher (5 of 318). For a committee, one practical reading is that a game adaptation is better budgeted as part of the game's marketing than as the start of a stand-alone animated franchise. That reading is an editorial frame, not a result the file measures.</p>

<h2 id="isekai-and-source-mix" class="anchored">ISEKAI TAGS AND SOURCE MIX (2015–2025)</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_isekai_by_year.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_isekai_by_year.png" data-source="Data: Tenrai clean TV frame · ARTOMETRICS" role="img" aria-label="Share of TV titles tagged isekai by premiere year, with bootstrap uncertainty band."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Isekai is operationalized as a case-insensitive tag match in MAL themes/genres or AniList tags. Read the line as a trend: any single year's share has a bootstrap range of about ±5 percentage points.</figcaption>
</figure>
<p class="art-p">On the clean TV frame, isekai-tagged premieres were rare in the mid-2010s, rose to about <strong>20.4%</strong> of 2021 TV titles, and remained elevated near <strong>18.1%</strong> in 2024 — not a precise dip from the published <strong>17.7%</strong> exploratory figure once uncertainty is applied. The <strong>2015</strong> point moves more materially, from <strong>0.9%</strong> to <strong>2.2%</strong>, because the refresh joins denser AniList tags to MAL theme fields.</p>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_source_mix_2015_2025.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_source_mix_2015_2025.png" data-source="Data: Tenrai clean TV frame · ARTOMETRICS" role="img" aria-label="Stacked area chart of TV source mix from 2015 through 2025."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Manga plus web manga accounted for <strong>47.2%</strong> of 2024 TV premieres on the clean ledger — unchanged from the exploratory recompute. Web manga alone is about <strong>12.5%</strong>.</figcaption>
</figure>
<p class="art-p">Committee financing still skews toward proven print and web serials. The stacked mix shows manga and web manga together near half of recent TV slates, while light novels and games occupy thinner bands. Year-by-year wiggles in the stack should be read the same way as isekai shares: informative as direction, not as exact market-share accounting.</p>

<h2 id="studio-league" class="anchored">Consistency is a studio trait</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_studios.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_studios.png" data-source="Data: 2019 TidyTuesday deduplicated file (studio section) — ARTOMETRICS" role="img" aria-label="Dot plot of median scores for 20 studios with at least 100 titles, with interquartile bars. Bones, Kyoto Animation, and OLM are highlighted in blue."></div>
<figcaption class="art-chart-caption art-chart-caption--visible"><!-- gen:studio-caption -->
Across the 20 largest studios, medians run from 7.46 to 5.40. Bones has the tightest spread among the top scorers, and OLM is the most consistent overall, at a lower level. DLE (n = 153) mostly makes short-form titles, with a median episode of 3 minutes, so its median score isn't directly comparable to studios making 24-minute episodes.
<!-- /gen:studio-caption --></figcaption>
</figure>
<p class="art-p">In a system where the committee owns the project, the animation studio is usually the prime contractor (motouke), and much of the drawing is subcontracted (shitauke) to other studios and freelancers (Hanzawa, 2004). Inside a studio, production managers (seisaku shinkou) coordinate the work but depend on key creatives, whose drawing skill routinely gives them the upper hand (Morisawa, 2015). That makes a studio's typical output a better guide to what a commission will deliver than its single biggest hit.</p>
<p class="art-p">Bones has 115 titles, a median of 7.46, an interquartile range (IQR, the spread of the middle half of its scores) of 0.95, and 23.5% of its titles scoring 8.0 or higher, the tightest spread among the top-scoring studios (only 7th-tightest of all 20). Kyoto Animation's 110 titles have a median of 7.43 and an IQR of 1.22. Kyoto Animation employs mostly salaried in-house staff and trains animators through its own school, which is unusual in an industry built on subcontracting (Creamer, 2015; Moore, 2017; Kyoto Animation training school). OLM is the counterexample that makes the point. Its 209 titles have a median of only 6.64, but its IQR of 0.70 is the tightest of any studio with 100 or more titles. It delivers a predictable product at a modest level.</p>
<p class="art-p">For anyone choosing a prime contractor, the decision metric is a studio's median and spread, not its best-known title. Across the 20 studios with 100 or more scored titles, median scores run from 7.46 (Bones) down to 5.40 (DLE). DLE (n = 153) mostly makes short-form titles, with a median episode of 3 minutes, so its median score isn't directly comparable to studios making 24-minute episodes. Bones and OLM have a 24-minute median episode. The largest studio, Toei (737 titles), sits near the bottom of the table at 6.68. Of those titles, 2.8% score 8.0 or higher (21 of 737).</p>
<div class="art-table-wrapper"><table class="art-table"><thead><tr><th>Studio</th><th>n</th><th>Median</th><th>Middle 50%</th><th>IQR</th><th>Share 8.0+</th></tr></thead><tbody>
<!-- gen:studio-table -->
<tr><td>Bones</td><td>115</td><td>7.46</td><td>6.95–7.90</td><td>0.95</td><td>23.5%</td></tr>
<tr><td>Kyoto Animation</td><td>110</td><td>7.43</td><td>6.67–7.89</td><td>1.22</td><td>20.9%</td></tr>
<tr><td>A-1 Pictures</td><td>190</td><td>7.31</td><td>6.70–7.73</td><td>1.03</td><td>14.7%</td></tr>
<tr><td>Shaft</td><td>125</td><td>7.25</td><td>6.65–7.86</td><td>1.21</td><td>16.8%</td></tr>
<tr><td>Studio Deen</td><td>264</td><td>7.20</td><td>6.53–7.63</td><td>1.10</td><td>8.3%</td></tr>
<tr><td>Production I.G</td><td>297</td><td>7.16</td><td>6.46–7.71</td><td>1.25</td><td>13.5%</td></tr>
<tr><td>Madhouse</td><td>340</td><td>7.03</td><td>6.47–7.61</td><td>1.15</td><td>15.9%</td></tr>
<tr><td>Gonzo</td><td>123</td><td>7.01</td><td>6.40–7.33</td><td>0.93</td><td>2.4%</td></tr>
<tr><td>J.C.Staff</td><td>322</td><td>7.01</td><td>6.25–7.42</td><td>1.17</td><td>7.5%</td></tr>
<tr><td>Sunrise</td><td>457</td><td>7.00</td><td>6.43–7.46</td><td>1.03</td><td>6.8%</td></tr>
<tr><td>TMS Entertainment</td><td>275</td><td>6.99</td><td>6.28–7.53</td><td>1.26</td><td>10.2%</td></tr>
<tr><td>Xebec</td><td>146</td><td>6.99</td><td>6.57–7.37</td><td>0.80</td><td>2.1%</td></tr>
<tr><td>Studio Pierrot</td><td>251</td><td>6.87</td><td>6.27–7.48</td><td>1.21</td><td>6.0%</td></tr>
<tr><td>AIC</td><td>111</td><td>6.82</td><td>6.30–7.22</td><td>0.93</td><td>0.9%</td></tr>
<tr><td>Toei Animation</td><td>737</td><td>6.68</td><td>6.16–7.23</td><td>1.07</td><td>2.8%</td></tr>
<tr><td>Nippon Animation</td><td>206</td><td>6.67</td><td>6.31–7.12</td><td>0.81</td><td>3.4%</td></tr>
<tr><td>OLM</td><td>209</td><td>6.64</td><td>6.36–7.06</td><td>0.70</td><td>0.5%</td></tr>
<tr><td>Shin-Ei Animation</td><td>156</td><td>6.63</td><td>6.08–7.25</td><td>1.17</td><td>0.6%</td></tr>
<tr><td>Tatsunoko Production</td><td>158</td><td>6.53</td><td>6.14–7.01</td><td>0.86</td><td>3.8%</td></tr>
<tr><td>DLE</td><td>153</td><td>5.40</td><td>4.96–5.94</td><td>0.98</td><td>0.7%</td></tr>
<!-- /gen:studio-table -->
</tbody></table></div>
<p class="art-p">Each card links its numbers to its history. The links are our reading, not measured effects. The section takes its numbers from the league table above and adds no new chart.</p>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Bones</p>
<p class="art-p">115 titles, median 7.46, IQR 0.95. Its signature titles are <em>Fullmetal Alchemist: Brotherhood</em> (2009), the highest-scoring title in the archive at 9.24 with 1,355,349 members, plus <em>My Hero Academia</em> (2016) and <em>Mob Psycho 100 II</em> (8.71). Sunrise producer Masahiko Minami founded Bones in 1998 with the animators Hiroshi Ōsaka and Toshihiro Kawamoto, all from the Sunrise team behind <em>Cowboy Bebop</em>. Minami brought freelance animators in as salaried staff, and the studio works in independent sub-studios (Morrissy, Anime News Network, 2018). A selective studio with a veteran core is consistent with a high median and a tight spread.</p>
</div>
<aside class="art-studio-card">
<img class="art-studio-card__logo" src="/images/content/articles/anime/assets/logo_bones.svg" alt="Bones" />
<p class="art-studio-card__credit">Bones logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p>
<p class="art-studio-card__name">Bones</p>
<ul class="art-studio-card__facts">
<li><span>Titles</span><strong>115</strong></li>
<li><span>Median</span><strong>7.46</strong></li>
<li><span>IQR</span><strong>0.95</strong></li>
<li><span>Founded</span><strong>1998</strong></li>
</ul>
<p class="art-studio-card__sig"><em>Fullmetal Alchemist: Brotherhood</em> (2009), <em>My Hero Academia</em> (2016), <em>Mob Psycho 100 II</em> (8.71).</p>
<p class="art-studio-card__history">Sunrise producer Masahiko Minami founded Bones in 1998 with the animators Hiroshi Ōsaka and Toshihiro Kawamoto, all from the Sunrise team behind <em>Cowboy Bebop</em>. Minami brought freelance animators in as salaried staff, and the studio works in independent sub-studios (Morrissy, Anime News Network, 2018).</p>
<div class="art-league-mini" aria-label="Bones median 7.46 on a studio range from 5.40 to 7.46">
<div class="art-league-mini__track"><span class="art-league-mini__baseline" style="left:47.6%"></span><span class="art-league-mini__dot" style="left:100%"></span></div>
<p class="art-league-mini__label">Median 7.46 · range 5.40–7.46</p>
</div>
<div class="art-person">
<img class="art-person__photo" src="/images/content/articles/anime/assets/person_masahiko_minami.jpg" alt="Masahiko Minami" />
<p class="art-person__name">Masahiko Minami</p>
<p class="art-person__role">Sunrise producer. Founded Bones in 1998 and brought freelance animators in as salaried staff.</p>
<p class="art-person__credit">Photo: Georges Seguin (Okki) / Wikimedia Commons, CC BY-SA 3.0</p>
</div>
<div class="art-person">
<img class="art-person__photo" src="/images/content/articles/anime/assets/person_toshihiro_kawamoto.jpg" alt="Toshihiro Kawamoto" />
<p class="art-person__name">Toshihiro Kawamoto</p>
<p class="art-person__role">Animator and co-founder, from the Sunrise team behind <em>Cowboy Bebop</em>.</p>
<p class="art-person__credit">Photo: Michael Ocampo / Wikimedia Commons, CC BY 2.0</p>
</div>
<div class="art-person art-person--text">
<p class="art-person__name">Hiroshi Ōsaka</p>
<p class="art-person__role">Animator and co-founder, with Minami and Kawamoto, from the Sunrise team behind <em>Cowboy Bebop</em>.</p>
</div>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Kyoto Animation</p>
<p class="art-p">110 titles, median 7.43, IQR 1.22. Its signature titles are <em>Koe no Katachi</em> (<em>A Silent Voice</em>, 2016, 9.03), <em>Clannad: After Story</em> (2008, 9.00), and <em>Suzumiya Haruhi no Shoushitsu</em> (2010, 8.71). Founded in 1981 in Uji, Kyoto, it trains its own animators and hires them on contract with a route to salaried staff, converting most of them (company hiring page; Creamer, 2015; Moore, 2017). Its own book imprint, KA Esuma Bunko, supplies some of its source novels. Its spread is wider than Bones', partly because 43 of its 110 scored titles are specials. Leaving specials out, Kyoto Animation's median is 7.62 with an IQR of 0.99 (n = 67), against 7.51 and 0.92 for Bones (n = 94). In July 2019, after this snapshot, an arson attack on the studio killed 36 people. Nothing in this data reflects it.</p>
</div>
<aside class="art-studio-card">
<img class="art-studio-card__logo" src="/images/content/articles/anime/assets/logo_kyoto_animation.svg" alt="Kyoto Animation" />
<p class="art-studio-card__credit">Kyoto Animation logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p>
<p class="art-studio-card__name">Kyoto Animation</p>
<ul class="art-studio-card__facts">
<li><span>Titles</span><strong>110</strong></li>
<li><span>Median</span><strong>7.43</strong></li>
<li><span>IQR</span><strong>1.22</strong></li>
<li><span>Founded</span><strong>1981</strong></li>
</ul>
<p class="art-studio-card__sig"><em>Koe no Katachi</em> (2016, 9.03), <em>Clannad: After Story</em> (2008, 9.00), <em>Suzumiya Haruhi no Shoushitsu</em> (2010, 8.71).</p>
<p class="art-studio-card__history">Founded in 1981 in Uji, Kyoto, it trains its own animators and hires them on contract with a route to salaried staff, converting most of them (company hiring page; Creamer, 2015; Moore, 2017). Its own book imprint, KA Esuma Bunko, supplies some of its source novels.</p>
<div class="art-league-mini" aria-label="Kyoto Animation median 7.43 on a studio range from 5.40 to 7.46">
<div class="art-league-mini__track"><span class="art-league-mini__baseline" style="left:47.6%"></span><span class="art-league-mini__dot" style="left:98.5%"></span></div>
<p class="art-league-mini__label">Median 7.43 · range 5.40–7.46</p>
</div>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">OLM</p>
<p class="art-p">209 titles, median 6.64, IQR 0.70, the tightest spread of any studio with 100 or more titles. Founded in 1994, OLM has produced the Pokémon TV anime since 1997, and 87 of its 209 scored titles are Pokémon, made by standing production teams (OLM; Anime News Network). It has range beyond that franchise, too: <em>Berserk</em> (1997) scores 8.47. On our reading, one repeatable kids' franchise explains both the consistency and the modest level, because the platform's audience rates kids' titles low.</p>
</div>
<aside class="art-studio-card">
<img class="art-studio-card__logo" src="/images/content/articles/anime/assets/logo_olm.svg" alt="OLM" />
<p class="art-studio-card__credit">OLM logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p>
<p class="art-studio-card__name">OLM</p>
<ul class="art-studio-card__facts">
<li><span>Titles</span><strong>209</strong></li>
<li><span>Median</span><strong>6.64</strong></li>
<li><span>IQR</span><strong>0.70</strong></li>
<li><span>Founded</span><strong>1994</strong></li>
</ul>
<p class="art-studio-card__sig"><em>Berserk</em> (1997, 8.47), and the Pokémon TV anime since 1997.</p>
<p class="art-studio-card__history">Founded in 1994, OLM has produced the Pokémon TV anime since 1997, and 87 of its 209 scored titles are Pokémon, made by standing production teams (OLM; Anime News Network).</p>
<div class="art-league-mini" aria-label="OLM median 6.64 on a studio range from 5.40 to 7.46">
<div class="art-league-mini__track"><span class="art-league-mini__baseline" style="left:47.6%"></span><span class="art-league-mini__dot" style="left:60.2%"></span></div>
<p class="art-league-mini__label">Median 6.64 · range 5.40–7.46</p>
</div>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Toei Animation</p>
<p class="art-p">737 titles, the most of any studio, with a median of 6.68 and 2.8% scoring 8.0 or higher. Its lineage runs from Nihon Dōga (1948), which Toei bought in 1956. Its first TV series aired in 1963, and long runs such as <em>Dragon Ball</em> (from 1986) and <em>Sailor Moon</em> (from 1992) define its model (Toei Animation history). Its franchise titles score well above its median, including <em>Slam Dunk</em> (8.54), <em>One Piece</em> (8.53, 803,871 members), and <em>Dragon Ball Z</em> (8.30). The original horror series <em>Mononoke</em> (2007, 8.44) shows its range. 197 of its 737 titles (27%) belong to seven long-running franchises, led by Precure, One Piece and Dragon Ball (counted by title match). Around them, a large, varied catalog of films, specials, and children's series pulls the median down.</p>
</div>
<aside class="art-studio-card">
<img class="art-studio-card__logo" src="/images/content/articles/anime/assets/logo_toei_animation.png" alt="Toei Animation" />
<p class="art-studio-card__credit">Toei Animation logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p>
<p class="art-studio-card__name">Toei Animation</p>
<ul class="art-studio-card__facts">
<li><span>Titles</span><strong>737</strong></li>
<li><span>Median</span><strong>6.68</strong></li>
<li><span>Share 8.0+</span><strong>2.8%</strong></li>
<li><span>Lineage</span><strong>1948</strong></li>
</ul>
<p class="art-studio-card__sig"><em>Slam Dunk</em> (8.54), <em>One Piece</em> (8.53), <em>Dragon Ball Z</em> (8.30), <em>Mononoke</em> (8.44).</p>
<p class="art-studio-card__history">Its lineage runs from Nihon Dōga (1948), which Toei bought in 1956. Its first TV series aired in 1963, and long runs such as <em>Dragon Ball</em> (from 1986) and <em>Sailor Moon</em> (from 1992) define its model (Toei Animation history).</p>
<div class="art-league-mini" aria-label="Toei Animation median 6.68 on a studio range from 5.40 to 7.46">
<div class="art-league-mini__track"><span class="art-league-mini__baseline" style="left:47.6%"></span><span class="art-league-mini__dot" style="left:62.1%"></span></div>
<p class="art-league-mini__label">Median 6.68 · range 5.40–7.46</p>
</div>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">DLE</p>
<p class="art-p">153 titles, median 5.40. Founded in 2001, DLE began Flash production in 2005 and had its Flash comedy <em>Eagle Talon</em> on TV in 2006. Its model is small teams producing short comedy fast (DLE company history; Anime News Network, 2020). Its median episode runs 3 minutes. Its best-scored title is <em>Gaikotsu Shotenin Honda-san</em> (<em>Skull-face Bookseller Honda-san</em>, 2018, 7.42), and it also animated <em>Thermae Romae</em> (2012). DLE's 5.40 reflects its format, not a failed studio.</p>
</div>
<aside class="art-studio-card">
<img class="art-studio-card__logo" src="/images/content/articles/anime/assets/logo_dle.svg" alt="DLE" />
<p class="art-studio-card__credit">DLE logo via Wikimedia Commons (public domain, PD-textlogo; trademark of its owner)</p>
<p class="art-studio-card__name">DLE</p>
<ul class="art-studio-card__facts">
<li><span>Titles</span><strong>153</strong></li>
<li><span>Median</span><strong>5.40</strong></li>
<li><span>Episode</span><strong>3 min</strong></li>
<li><span>Founded</span><strong>2001</strong></li>
</ul>
<p class="art-studio-card__sig"><em>Gaikotsu Shotenin Honda-san</em> (2018, 7.42) and <em>Thermae Romae</em> (2012).</p>
<p class="art-studio-card__history">Founded in 2001, DLE began Flash production in 2005 and had its Flash comedy <em>Eagle Talon</em> on TV in 2006. Its model is small teams producing short comedy fast (DLE company history; Anime News Network, 2020).</p>
<div class="art-league-mini" aria-label="DLE median 5.40, the low end of the studio range">
<div class="art-league-mini__track"><span class="art-league-mini__baseline" style="left:47.6%"></span><span class="art-league-mini__dot" style="left:0%"></span></div>
<p class="art-league-mini__label">Median 5.40 · range 5.40–7.46</p>
</div>
</aside>
</div>

<h2 id="sequel-premium" class="anchored">Sequels score higher, consistent with mostly well-received shows getting one</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_sequel.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_sequel.png" data-source="Data: MyAnimeList via TidyTuesday (Kaggle snapshot, early 2019) — ARTOMETRICS" role="img" aria-label="Overlaid distributions of TV sequel and non-sequel scores, with medians marked."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">TV sequels score higher at the median and are about twice as likely to reach 8.0, consistent with mostly well-received shows getting a second season.</figcaption>
</figure>
<p class="art-p">Of the 4,240 scored TV titles, 867 are sequels. We count a title as a sequel when its chain of prequels, every one of which aired earlier, reaches an earlier TV series. That rule keeps promotional specials from making a first season look like a sequel. Sequels have a median score of 6.99, against 6.76 for the other 3,373 titles, and 14.8% of them score 8.0 or higher (128 of 867), against 6.5% (218 of 3,373). The median gap ranges from 0.15 to 0.30 points depending on how "sequel" is defined, but every definition we tested points the same way.</p>
<p class="art-p">The pattern is consistent with selection, not with any effect of being a sequel. Committees mostly order second seasons of shows that did well, and the viewers who come back already liked the first one. Among the top TV sequels by audience are <em>Sword Art Online II</em>, <em>Naruto: Shippuuden</em>, <em>Code Geass R2</em>, and <em>Clannad: After Story</em> (9.00). For a buyer, a sequel's score says more about the strength of the property than about the sequel itself.</p>

<h2 id="buried-canon" class="anchored">Popularity tracks quality, with a short list of exceptions</h2>
<figure class="art-chart">
<div class="art-chart-live" data-chart="/data/articles/anime/charts/chart_reach.plotly.json" data-fallback="/images/content/articles/anime/charts/chart_reach.png" data-source="Data: 2019 TidyTuesday deduplicated file (reach chart) — ARTOMETRICS" role="img" aria-label="Scatter of score against member count on a log scale. Spearman correlation 0.73 on October 2026 clean scored titles. Eleven shortlist titles are highlighted."></div>
<figcaption class="art-chart-caption art-chart-caption--visible">Across 18,704 scored titles on the October 2026 clean file, score and reach rise together (rank correlation 0.73). Only a handful of stand-alone, highly rated titles remain obscure.</figcaption>
</figure>
<p class="art-p">Member counts are extremely skewed. A rank (Spearman) correlation gives <strong>0.73</strong> on the clean ledger, and correlating score with the log of member count gives a similar reading. On this platform, well-rated titles are usually well watched.</p>
<p class="art-p">The exceptions are rare and specific. Of 603 titles scoring 8.0 or higher, 78 sit beyond popularity rank 3,000. Requiring at least 1,000 user ratings cuts that to 43. Of the 43 titles with at least 1,000 ratings, 12 continue an earlier TV series (5 of them as TV seasons); we count sequels by following each title's prequel chain back to an earlier TV series. Limiting the list to TV series and films with no earlier prequel, parent story, or full story of any type leaves 11.</p>
<p class="art-p">The Buried Canon is an editorial shortlist, not a measured ranking: score of 8.0 or higher, popularity rank past 3,000, 1,000 or more ratings, TV or film, and no earlier prequel, parent story, or full story of any type. Related titles with missing start dates do not count.</p>
<div class="art-split art-split--titles">
<div class="art-split__copy">
<div class="art-table-wrapper"><table class="art-table"><thead><tr><th>Title</th><th>Year</th><th>Studio</th><th>Score</th><th>Popularity rank</th><th>Ratings</th><th>Legal US stream (JustWatch, Oct 10, 2026)</th></tr></thead><tbody>
<tr><td>Ginga Nagareboshi Gin</td><td>1986</td><td>Toei Animation</td><td>8.12</td><td>3,292</td><td>7,030</td><td>Not available in US (JustWatch, Oct 2026)</td></tr>
<tr><td>Kindaichi Shounen no Jikenbo</td><td>1997</td><td>Toei Animation</td><td>8.11</td><td>3,425</td><td>2,876</td><td>Not available in US</td></tr>
<tr><td>Hanada Shounen-shi</td><td>2002</td><td>Madhouse</td><td>8.11</td><td>4,157</td><td>2,616</td><td>Not available in US; JustWatch lists offers in Japan and South Korea only</td></tr>
<tr><td>Omae Umasou da na (film)</td><td>2010</td><td>Ajia-Do</td><td>8.08</td><td>3,973</td><td>4,076</td><td>No US listing found on JustWatch</td></tr>
<tr><td>IDOLiSH7</td><td>2018</td><td>TROYCA</td><td>8.06</td><td>3,037</td><td>4,788</td><td>Crunchyroll, Netflix</td></tr>
<tr><td>Ginga Sengoku Gunyuuden Rai</td><td>1994</td><td>E&amp;G Films</td><td>8.06</td><td>4,316</td><td>2,956</td><td>Not available in US</td></tr>
<tr><td>Hyouge Mono</td><td>2011</td><td>Bee Train</td><td>8.04</td><td>3,194</td><td>2,098</td><td>Not available in US</td></tr>
<tr><td>Tanoshii Muumin Ikka</td><td>1990</td><td>Telescreen</td><td>8.03</td><td>3,777</td><td>5,418</td><td>Not available in US</td></tr>
<tr><td>Igano Kabamaru</td><td>1983</td><td>Group TAC</td><td>8.03</td><td>4,602</td><td>2,816</td><td>Not available in US</td></tr>
<tr><td>Ie Naki Ko Remy</td><td>1996</td><td>Nippon Animation</td><td>8.02</td><td>3,866</td><td>4,793</td><td>Not available in US</td></tr>
<tr><td>Takarajima</td><td>1978</td><td>TMS, with Madhouse</td><td>8.02</td><td>4,057</td><td>3,442</td><td>Not available in US</td></tr>
</tbody></table></div>
<p class="art-p">Do the 11 have anything in common? Little beyond age and format. Eight are TV series that began before 2003, nine ran 21 episodes or more, and all 11 are adaptations, six of them from manga. They come from 10 different studios, span 1978 to 2018, and range from samurai history (<em>Hyouge Mono</em>) to the 1990 <em>Moomin</em> series (<em>Tanoshii Muumin Ikka</em>). The one thread is distribution. 10 of the 11 can't be watched legally in the US today (JustWatch, October 10, 2026). Only <em>IDOLiSH7</em> streams on Crunchyroll and Netflix. On our reading, most of them are under-distributed, not overlooked by viewers who could watch them. We haven't tested that. <em>IDOLiSH7</em> is the exception: a recent, available show whose small audience fits an idol-game niche.</p>
</div>
<aside>
<div class="art-title-card"><p class="art-title-card__name">Ginga Nagareboshi Gin</p><a class="art-title-card__link" href="https://lineup.toei-anim.co.jp/ja/tv/nagareboshi_gin/">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">Hanada Shounen-shi</p><a class="art-title-card__link" href="https://madhouse.co.jp/works/tv_hanadashounen/">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">Kindaichi Shounen no Jikenbo</p><a class="art-title-card__link" href="https://lineup.toei-anim.co.jp/ja/tv/kindaichi/">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">Omae Umasou da na</p><a class="art-title-card__link" href="https://ttcg.jp/distribution/0000010.html">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">Ginga Sengoku Gunyuuden Rai</p><a class="art-title-card__link" href="https://ja.wikipedia.org/wiki/%E9%8A%80%E6%B2%B3%E6%88%A6%E5%9B%BD%E7%BE%A4%E9%9B%84%E4%BC%9D%E3%83%A9%E3%82%A4">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">IDOLiSH7</p><a class="art-title-card__link" href="https://idolish7.com/aninana/">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">Hyouge Mono</p><a class="art-title-card__link" href="https://web.archive.org/web/20160907072200/http://www9.nhk.or.jp/anime/hyouge/story/index.html">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">Tanoshii Muumin Ikka</p><p class="art-wordmark">Telescreen</p><a class="art-title-card__link" href="https://www.animenewsnetwork.com/encyclopedia/anime.php?id=2006">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">Igano Kabamaru</p><a class="art-title-card__link" href="https://ja.wikipedia.org/wiki/%E4%BC%8A%E8%B3%80%E9%87%8E%E3%82%AB%E3%83%90%E4%B8%B8">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">Ie Naki Ko Remy</p><a class="art-title-card__link" href="https://www.nippon-animation.co.jp/work/1751/">Key art: official page</a></div>
<div class="art-title-card"><p class="art-title-card__name">Takarajima</p><a class="art-title-card__link" href="https://www.tms-e.co.jp/alltitles/1970s/026101.html">Key art: official page</a></div>
</aside>
</div>

<h2 id="limitations" class="anchored">LIMITATIONS</h2>
<p class="art-p">Coverage window. Headline source, isekai, and member statistics use the October 2026 clean snapshot (<code>anime_2026-10-11_clean</code>). Format-wave, studio-league, sequel, and buried-canon sections still use the deduplicated 2019 TidyTuesday export through 2018 for chart continuity until those exhibits are regenerated. See <a href="/anime-data-fix">what changed when we fixed the data</a>.</p>
<p class="art-p">Platform audience. MyAnimeList is an English-language enthusiast site. Its scores reflect that audience's expectations. Kids titles (median 5.86, n = 2,158) and music titles (median 5.44, n = 1,510) score lowest, which more likely reflects a mismatch between audience and content than weak production. Thriller (7.50, n = 102), Mystery (7.27, n = 605), and Psychological (7.23, n = 279) score highest.</p>
<p class="art-p">No commercial data. The file has no revenue, broadcast ratings, disc sales, box office, or merchandise figures. A low score doesn't mean a franchise lost money.</p>
<p class="art-p">Selection, not causation. Source material, studio, and sequel status are all chosen with an eye to expected demand, so none of the gaps above should be read as the effect of that choice alone. The format chart lines each wave up with a channel. It does not show that the channel shaped what got made.</p>
<p class="art-p">Deduplication. The source file repeats each title once per studio and genre (77,911 rows for 13,631 titles). All title-level figures here use one row per title.</p>
<p class="art-p">Context after the snapshot. Events after early 2019, including the 2019 Kyoto Animation arson, later Netflix commissions, and current streaming availability, come from outside sources. The data can't reflect them.</p>

<h2 id="conclusion" class="anchored">CONCLUSION: Choose the source, judge the studio by its median, and read sequel scores as property scores</h2>
<p class="art-p">The archive doesn't show what makes anime good. It does show where the industry's early decisions leave a mark. Adapting a light novel or manga brings an audience that is already there, while an original has to find one. Studios differ clearly in their typical output, which is the better guide to a commission. Sequel scores mostly reflect the shows that earned them. Beyond those patterns lies a short list of strong titles the platform's audience never found. The next useful question is commercial. Matching these fan signals to revenue data would show whether the platform's audience floor is also a revenue floor.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The refreshed ledger is <code>data/anime/anime_2026-10-11_clean.csv</code> (18,813 rows after cleaning), built from Tenrai (<code>api.tenrai.org</code>, Jikan-compatible after the 2026-10-01 shutdown of <code>api.jikan.moe</code>) with AniList enrichment on <code>idMal</code>. One command audits and writes bootstrap ranges: <code>python3 scripts/anime-data/clean_audit.py</code> (seed <code>20261011</code>). October 2026 charts for source, isekai, and scorecard: <code>python3 articles/anime/scripts/build_2026_charts.py</code>. Headline TV statistics use <code>type == "TV"</code>, analysis year from <code>aired_from_year</code> (fallback <code>season_year</code>), isekai via tag match in themes/genres/AniList tags, and percentile bootstrap CIs (B = 2000). Percentages and ratios in copy use one-decimal rounding (e.g. 27.5×, 14.8%).</p>
<p class="art-p">Score comparisons on television use scored TV titles, n = 6,073 of 6,095 on the clean file. The rank correlation of score and members is Spearman, n = 18,704 scored titles. Legacy studio, sequel, and format exhibits still come from <code>npm run brief:anime</code> on the 2019 TidyTuesday export (SHA-256 <code>5ea3a14492b5c559c728af0c7ec57b81c919d0efa4d381e54b0f7cde9934a1c2</code>). The sequel rule follows MAL Prequel links back in time. The Buried Canon shortlist rules are unchanged. US availability checked on JustWatch, October 10, 2026. Full reconciliation tables: <a href="/anime-data-fix">ANIME: What changed when we fixed the data</a> and <code>data/anime/CLEANING_LOG.md</code>.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p class="art-p">Primary data. MyAnimeList metadata via Tenrai API, snapshot 2026-10-11; baseline comparison TidyTuesday 2019-04-23. <a href="https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-04-23" rel="noopener noreferrer">TidyTuesday 2019-04-23</a> · <code>data/anime/METHODS_NOTE.md</code>.</p>
<p class="art-p">Context literature.</p>
<ul>
<li>Hernández Hernández, Á. D. (2018). "The Anime Industry, Networks of Participation, and Environments for the Management of Content in Japan." Arts 7(3): 42. Cited for §4.3 (pp. 8–9), the committee mechanism. <a href="https://doi.org/10.3390/arts7030042" rel="noopener noreferrer">doi:10.3390/arts7030042</a>.</li>
<li>Hanzawa, Seiji (2004). "The Japanese Animation and Home Video Game Industries." Japanese Journal of Human Geography 56(6): 587–602. Cited for subcontracting and freelance labor. <a href="https://doi.org/10.4200/jjhg1948.56.587" rel="noopener noreferrer">doi:10.4200/jjhg1948.56.587</a>.</li>
<li>Mihara, Ryotaro (2018). "Involution: a perspective for understanding Japanese animation's domestic business in a global context." Japan Forum 32(1): 102–125. Published online 2018. <a href="https://doi.org/10.1080/09555803.2018.1442362" rel="noopener noreferrer">doi:10.1080/09555803.2018.1442362</a>.</li>
<li>Morisawa, Tomohiro (2015). "Managing the unmanageable: Emotional labour and creative hierarchy in the Japanese animation industry." Ethnography 16(2): 262–284. Cited only for the production-management layer (seisaku shinkou) that depends on key creatives. <a href="https://doi.org/10.1177/1466138114547624" rel="noopener noreferrer">doi:10.1177/1466138114547624</a>.</li>
<li>Steinberg, M. (2012). Anime's Media Mix: Franchising Toys and Characters in Japan. University of Minnesota Press. Cited for the media mix and for the television wave beginning with Tetsuwan Atom (1963) and sponsor merchandising.</li>
<li>Creamer, Nick (2015-12-02). "What Makes Kyoto Animation So Special?" Anime News Network. <a href="https://www.animenewsnetwork.com/feature/2015-12-02/what-makes-kyoto-animation-so-special/.95559" rel="noopener noreferrer">animenewsnetwork.com</a>.</li>
<li>Moore, D. M. (2017-10-20). "A Silent Voice shows why Kyoto Animation is one of the top animation studios." The Verge. <a href="https://www.theverge.com/2017/10/20/16482234/a-silent-voice-kyoto-animation-kyoani" rel="noopener noreferrer">theverge.com</a>.</li>
<li>Kyoto Animation, training school. <a href="https://www.kyotoanimation.co.jp/school/" rel="noopener noreferrer">kyotoanimation.co.jp/school</a>.</li>
<li>Morrissy, Kim (2018-12-12). "Looking Back on 20 Years of Studio Bones." Anime News Network. <a href="https://www.animenewsnetwork.com/feature/2018-12-12/looking-back-on-20-years-of-studio-bones/.139456" rel="noopener noreferrer">animenewsnetwork.com</a>.</li>
<li>Kyoto Animation, company outline. <a href="https://www.kyotoanimation.co.jp/company/outline/" rel="noopener noreferrer">kyotoanimation.co.jp/company/outline</a>. Hiring page. <a href="https://www.kyotoanimation.co.jp/recruit/outline/newgrads-animator/" rel="noopener noreferrer">new-graduate animator terms</a>.</li>
<li>OLM, company site. <a href="https://www.olm.co.jp/about?lang=en" rel="noopener noreferrer">olm.co.jp/about</a>. Anime News Network encyclopedia entry. <a href="https://www.animenewsnetwork.com/encyclopedia/company.php?id=33" rel="noopener noreferrer">animenewsnetwork.com</a>.</li>
<li>Toei Animation, company history. <a href="https://corp.toei-anim.co.jp/en/company/history.html" rel="noopener noreferrer">corp.toei-anim.co.jp</a>.</li>
<li>DLE, company history. <a href="https://www.dle.jp/jp/company/" rel="noopener noreferrer">dle.jp/jp/company</a>. Anime News Network (2020) on <em>Eagle Talon</em>. <a href="https://www.animenewsnetwork.com/news/2020-09-09/eagle-talon-golden-spell-anime-casts-kenjiro-tsuda-kazuhiro-nakaya-rina-satou/.163811" rel="noopener noreferrer">animenewsnetwork.com</a>.</li>
<li>IDOLiSH7 official announcement (Jan 17, 2017). <a href="https://idolish7.com/news/2017/4582" rel="noopener noreferrer">idolish7.com</a>. Anime News Network (2017). <a href="https://www.animenewsnetwork.com/news/2017-09-10/idolish-7-tv-anime-reveals-january-2018-debut-opening-scene-more-of-voice-cast/.121169" rel="noopener noreferrer">animenewsnetwork.com</a>.</li>
<li>Netflix Media Center, <em>Devilman: Crybaby</em>. <a href="https://media.netflix.com/en/only-on-netflix/80174974" rel="noopener noreferrer">media.netflix.com</a>. Anime News Network (2017). <a href="https://www.animenewsnetwork.com/news/2017-03-15/masaaki-yuasa-directs-new-devilman-anime-for-netflix/.113478" rel="noopener noreferrer">animenewsnetwork.com</a>.</li>
<li>Studio Pierrot, <em>Dallos</em> archive. <a href="https://pierrot.jp/archive/ova/title01.html" rel="noopener noreferrer">pierrot.jp</a>. Pineda, Rafael Antonio (2022-11-21). "1st Ever OVA Dallos Gets Blu-ray Disc Release in March 2023." Anime News Network. <a href="https://www.animenewsnetwork.com/news/2022-11-21/1st-ever-ova-dallos-gets-blu-ray-disc-release-in-march-2023/.192119" rel="noopener noreferrer">animenewsnetwork.com</a>.</li>
<li>Ristola, Jacqueline C. R. (2024). "Going Gonzo: Crunchyroll, Anime Streaming, and Unpaid Digital Labour." Kinephanos 10(1): 145–174. Cited for p. 4: Crunchyroll began licensed simulcasts in 2008 and went licensed-only in January 2009, after its TV Tokyo deal. <a href="https://doi.org/10.7202/1113453ar" rel="noopener noreferrer">doi:10.7202/1113453ar</a>.</li>
<li>Same-day <em>Naruto Shippuden</em> (January 2009), as reported by Anime News Network. <a href="https://www.animenewsnetwork.com/press-release/2009-01-08/naruto-shippuden-and-gintama-arrives-on-crunchyroll-today" rel="noopener noreferrer">2009</a>. August 2008 Gonzo license announcement. <a href="https://www.animenewsnetwork.com/press-release/2008-08-09/crunchyroll-licenses-multiple-gonzo-anime-titles" rel="noopener noreferrer">2008</a>.</li>
<li>Association of Japanese Animations, Anime Industry Report English summaries (2019 and 2024 editions). 2023 was the second time overseas sales passed domestic ones (the first was 2020; 2024 summary, p. 8). <a href="https://aja.gr.jp/download/2023_anime_ind_rpt_summary_en?refresh=6604b4af938671711584431&amp;wpdmdl=2304" rel="noopener noreferrer">2023 summary</a>. <a href="https://aja.gr.jp/download/anime-industry-report-2024-summary_20250321?refresh=68acc124d94f91756152100&amp;wpdmdl=2485" rel="noopener noreferrer">2024 summary</a>. Whole-industry market, not studio revenue.</li>
<li>JustWatch US, accessed October 10, 2026. Subscription, free-with-ads, rental, and purchase offers. Checked by hand for the Buried Canon shortlist.</li>
</ul>
</section>

<h2 id="editors-note" class="anchored">EDITOR'S NOTE</h2>
<div class="art-editorial-note"><p class="art-p"><em>October 2026 update: headline source, isekai, and member statistics were recomputed on <code>anime_2026-10-11_clean</code> after the Jikan shutdown; bootstrap ranges and a full old-vs-new ledger are in <a href="/anime-data-fix">What changed when we fixed the data</a>. Studio, sequel, and format-wave exhibits remain on the 2019 brief until regenerated. Human editorial direction; AI-assisted analysis per Artometrics workflow.</em></p><p class="art-p">— Artometrics Editorial Desk</p></div>
</main>
</div>
