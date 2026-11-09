---
title: 'COFFEE: Ethiopia Scores Highest on Coffee Quality—With Zero Starbucks Stores'
slug: coffee
author: kyle-mcauliffe
pubDate: 2026-04-14T00:00:00.000Z
description: Ethiopia's median CQI cup score is 85.3 — the highest of 16 countries with 20+ samples — yet Starbucks operates zero stores in the top three scoring nations.
heroImage: /images/content/articles/coffee/hero.png
draft: false
tags:
  - culture
  - food
subject: Coffee
tldr: 'Ethiopia''s median CQI cup score of 85.3 is the highest of any country with 20+ samples, yet Starbucks operates zero stores in Ethiopia, Kenya, or Uganda — the top three scoring nations. Quality and retail power do not map to the same geography.'
keyPoints:
  - '85.3 — Ethiopia''s median CQI cup score — highest of any country with 20+ samples, leading on every sensory sub-metric'
  - '0 — Starbucks locations in Ethiopia, Kenya, and Uganda — the top three scoring origins show zero branded retail presence'
  - '1,339 — Coffee samples rated by CQI Q Graders across Arabica and Robusta species in the TidyTuesday dataset'
  - '16 — Countries with 20+ CQI-rated Arabica samples, spanning four continents and representing specialty coffee origins'
  - '7 — Sensory sub-metrics scored per sample — aroma, flavor, aftertaste, acidity, body, balance, cupper points — Ethiopia leads all'
  - '25,600 — Starbucks locations worldwide across 73 countries as of 2018 — none in the highest-scoring African origins'
faq:
  - question: What is Ethiopia's median CQI cup score?
    answer: 'Ethiopia''s median CQI cup score is 85.3, the highest of any country with 20 or more rated samples in the dataset.'
  - question: How many Starbucks stores operate in the top-scoring coffee origins?
    answer: 'Zero. Starbucks operates no locations in Ethiopia, Kenya, or Uganda — the three highest-scoring nations by CQI cupping data.'
  - question: How many coffee samples were rated by CQI Q Graders?
    answer: '1,339 samples across Arabica and Robusta species, with 1,312 Arabica samples from 36 countries after cleaning.'
  - question: Which countries had enough samples for stable quality comparisons?
    answer: '16 countries met the 20-sample threshold, spanning Africa, Latin America, Asia, and North America.'
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Ethiopia's median Coffee Quality Institute cup score is 85.3 — the highest of any country with 20 or more rated samples — yet Starbucks operates zero stores there. The same is true for Kenya and Uganda, the second- and third-highest scoring nations. Coffee's quality map and its retail map describe two unrelated geographies.</p>
<p class="art-p">This analysis uses CQI cupping scores and Starbucks store counts to test whether sensory quality and branded retail power accumulate in the same places. They do not. The countries that grow the best-rated coffee capture little of the value that branded retail extracts downstream.</p>
<h2 id="research-question" class="anchored">Research question</h2>
<p class="art-p">Does the geography of high-scoring coffee match the geography of retail coffee power? This analysis tests whether Coffee Quality Institute cupping scores and Starbucks store counts describe the same global map or two disconnected positions in the commodity chain.</p>
<p class="art-p">The question is where Arabica quality concentrates once country medians and sensory sub-metrics are plotted, and whether that origin map aligns with the markets where a dominant branded retailer operates stores. The answer matters because origin value, sensory quality, and retail capture are often discussed as if they reinforce one another naturally.</p>

<h2 id="where-great-coffee-comes-from" class="anchored">Where Great Coffee Comes From</h2>
<h3 id="where-great-coffee-comes-from-look" class="anchored">Country Ridgeline</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/coffee/charts/chart1_country_ridgeline.plotly.json" data-fallback="/images/content/articles/coffee/charts/chart1_country_ridgeline.png" role="img" aria-label="Country Ridgeline"></div>
</figure>
<p class="art-p">Ethiopia occupies a different part of the distribution entirely. The median cup score across all 16 qualifying countries is 82.5. Ethiopia's distribution peaks near 85 and has a long right tail that no other origin approaches. Kenya and Uganda sit in second and third, but their distributions overlap substantially with the rest of the field. Ethiopia's does not. Ethiopia is the genetic origin of Arabica coffee — the Kaffa region in southwestern Ethiopia is where the species was first documented growing wild. The country's range of elevation, soil diversity, and processing tradition produces a flavor complexity that Q Graders reward with above-median scores across every sub-metric. The bottom of the chart is equally clear. Nicaragua, Mexico, Honduras, and Taiwan cluster between 81 and 83 — technically specialty grade, but at the floor. Brazil, the world's largest coffee producer by volume, lands in the lower half — market dominance and cup quality are not the same thing.</p>
<h2 id="the-quality-retail-disconnect" class="anchored">The Quality-Retail Disconnect</h2>
<h3 id="the-quality-retail-disconnect-look" class="anchored">Quality Vs Retail</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/coffee/charts/chart2_quality_vs_retail.plotly.json" data-fallback="/images/content/articles/coffee/charts/chart2_quality_vs_retail.png" role="img" aria-label="Quality Vs Retail"></div>
</figure>
<p class="art-p">There is no positive relationship between a country's quality score and Starbucks' retail presence there. The three highest-scoring origins — Ethiopia, Kenya, and Uganda — all sit at zero Starbucks locations. Hawaii (USA) lands near the top of the y-axis not because of its quality rank but because its ISO code maps to the US, which hosts thousands of Starbucks locations. This is structural. Starbucks builds stores in markets where it can sell coffee, not only in markets where it sources coffee. Ethiopia's retail consumer market is too small and too low-income to support the Starbucks price point at scale. The company sources Ethiopian beans, but that sourcing relationship does not translate into a domestic retail presence. Colombia reinforces the pattern: a recognized origin with specialty scores that shows little Starbucks store footprint relative to the fame of its beans. Economic value from growing specialty coffee does not automatically accumulate where the coffee is grown.</p>
<h2 id="the-sub-metric-fingerprint" class="anchored">The Sub-Metric Fingerprint</h2>
<h3 id="the-sub-metric-fingerprint-look" class="anchored">Submetric Heatmap</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/coffee/charts/chart3_submetric_heatmap.plotly.json" data-fallback="/images/content/articles/coffee/charts/chart3_submetric_heatmap.png" role="img" aria-label="Submetric Heatmap"></div>
</figure>
<p class="art-p">Ethiopia scores higher on every single sub-metric among the eight-country heatmap field. Its median acidity, cupper points, and flavor lead the set. Kenya comes close on aroma and flavor but trails on most other dimensions. The heatmap also reveals how flat the remaining countries are. Brazil sits in a narrow mid band across attributes — consistent and undifferentiated. Honduras and Mexico are nearly indistinguishable on several scores. When buyers talk about commodity coffee, this is the sensory data behind the phrase. Guatemala and Colombia show elevated acidity and balance relative to that flat middle — profiles that translate easily into consumer language about brightness and approachability.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">The CQI dataset reflects what Q Graders evaluate — not a random sample of all coffee produced. Farms that can afford evaluation tend to be larger or already tied into specialty chains, so subsistence-grade output is underrepresented.</p>
<p class="art-p">The Starbucks dataset is from 2018. Store counts should not be treated as current, even if the directional finding about missing retail presence in top African origins has remained stable. Starbucks is a proxy for one dominant chain, not the full café and grocery landscape.</p>
<p class="art-p">Country-level analyses were filtered to origins with 20 or more CQI samples, cutting the pool from 36 to 16 countries. Prestigious origins with fewer submissions — including some ultra-premium varieties — are absent from the heatmap.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">Quality and market power are not the same thing, and they do not flow in the same direction. Ethiopia produces the highest-rated coffee in this CQI slice by a significant margin and shows zero Starbucks locations in the joined retail file.</p>
<p class="art-p">Brazil dominates volume while scoring in the lower half of this quality ranking. The countries that grow the best-scoring coffee are not automatically the countries that capture the most retail value from coffee's global brand.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The Coffee Quality Institute trains and certifies Q Graders — licensed sensory evaluators who score coffee using a standardized 100-point protocol. A sample must score 80 or above to qualify as specialty coffee. The CQI dataset from TidyTuesday (2020-07-07) contains 1,339 samples spanning Arabica and Robusta species, with individual scores across ten sub-metrics plus a total cup points aggregate. This analysis uses only Arabica. After removing one data entry error, the working Arabica dataset contains 1,312 samples from 36 countries.</p>
<p class="art-p">The Starbucks locations dataset (TidyTuesday 2018-05-07) documents 25,600 individual store locations across 73 countries, with brand, ownership type, city, and geographic coordinates. For the quality-versus-retail chart, Starbucks counts were aggregated at the country level and joined to CQI quality scores using ISO-2 country codes.</p>
<p class="art-p">The sub-metric fingerprint covers seven of the ten CQI sub-metrics: aroma, flavor, aftertaste, acidity, body, balance, and cupper points. Uniformity, clean cup, and sweetness were excluded because they function as defect-penalty fields rather than sensory attributes. The top eight countries by sample volume were selected for the heatmap to ensure statistically stable medians.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">References</h3>
<p class="art-p">The Coffee Quality Institute data should be read as a specialty-coffee evaluation archive, not a random sample of all coffee output. CQI Q Graders score submitted samples under standardized protocols, which means the file is strongest for comparing evaluated specialty lots and weaker for estimating national output averages. The Starbucks file adds a retail-chain geography from 2018, useful as a branded-store proxy but not as a full measure of café, grocery, roaster, or export-market value.</p>
<p class="art-p">The broader citation frame comes from coffee-development and value-chain research by Daviron, Ponte, Samper, Quiñones-Ruiz, and the International Coffee Organization. Those sources matter because the charts show a classic commodity-chain split: Ethiopia, Kenya, Uganda, Colombia, Brazil, and other origins can produce sensory value, while roasting, branding, retail real estate, and consumer pricing often capture value elsewhere.</p>
<div class="art-references">
  <div class="art-ref-item">
    TidyTuesday (2020-07-07). <em>Coffee Ratings</em>.
    R for Data Science Community.
    <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-07-07" target="_blank">
      github.com/rfordatascience/tidytuesday/…/2020-07-07
    </a>
  </div>
  <div class="art-ref-item">
    TidyTuesday (2018-05-07). <em>Coffee Chains</em>.
    R for Data Science Community.
    <a href="https://github.com/rfordatascience/tidytuesday/blob/master/data/2018/2018-05-07" target="_blank">
      github.com/rfordatascience/tidytuesday/…/2018-05-07
    </a>
  </div>
  <div class="art-ref-item">
    Coffee Quality Institute. (2020). <em>Q Grader Program and Cupping
    Protocols</em>. Retrieved from
    <a href="https://www.coffeeinstitute.org" target="_blank">coffeeinstitute.org</a>
  </div>
  <div class="art-ref-item">
    Samper, L. F., &amp; Quiñones-Ruiz, X. F. (2017). Towards a balanced
    sustainability vision for the coffee industry. <em>Resources</em>, <em>6</em>(2), 17.
    <a href="https://doi.org/10.3390/resources6020017" target="_blank">
      doi.org/10.3390/resources6020017
    </a>
  </div>
  <div class="art-ref-item">
    Daviron, B., &amp; Ponte, S. (2005). <em>The Coffee Paradox: Global Markets,
    Commodity Trade and the Elusive Promise of Development</em>. Zed Books.
  </div>
  <div class="art-ref-item">
    Wintgens, J. N. (Ed.). (2009). <em>Coffee: Growing, Processing, Sustainable
    Production</em> (2nd ed.). Wiley-VCH.
  </div>
<h2 id="editor-s-note" class="anchored">Editor's note</h2>
<div class="art-editorial-note"><p class="art-p">
This analysis was researched, written, designed, and produced in active
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
<p class="art-p">— Artometrics Editorial</p></div>

<p class="art-github-wrap">
  <a class="art-github-btn" href="https://github.com/Artometrics/coffee" target="_blank" rel="noopener noreferrer">Source archive (GitHub)</a>
</p>
</section>
</main>
</div>
