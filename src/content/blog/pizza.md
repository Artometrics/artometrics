---
title: "PIZZA: Two Economies in 10,000 Menu Rows"
slug: pizza
author: kyle-mcauliffe
pubDate: 2026-06-15T00:00:00.000Z
description: >-
  10,000 pizza menu records show a median price floor of 0.00 and a premium tier
  reaching 50.0, encoding two separate markets in one dataset.
dek: "A slice at the bottom, a splurge at the top: ten thousand pizza menus, two separate markets."
heroImage: /images/content/articles/pizza/hero.png
draft: false
tags:
  - culture
  - food
subject: Pizza
tldr: >-
  A TidyTuesday pizza extract of 10,000 menu records reveals a median price-range minimum of 0.00 and a premium tier at 50.0. The mass of listings sits at zero or missing values, while a thin tail of destination pizzerias cluster at 40–50, requiring separate citation strategies for market claims.
keyPoints:
  - '10,000 — Records in the dataset'
  - '0.00 — Median price-range minimum across all entries'
  - '50.0 — Highest observed price-range minimum'
  - '40.0 — Median price-range minimum among the top twelve names'
faq:
  - question: How many records are in this dataset?
    answer: 10,000 records from the TidyTuesday pizza_datafiniti.csv extract.
  - question: What is the median price-range minimum?
    answer: The median price-range minimum is 0.00, indicating most listings have zero or missing price floors.
  - question: What price floor marks the premium tier?
    answer: The top-dozen names have a median price-range minimum of 40.0, with leaders reaching 50.0.
  - question: How should I cite pizza price in this file?
    answer: Use the global median of 0.00 for typical listings and the top-dozen median of 40.0 for premium or destination pizzerias.
---
<div id="quarto-content">
<main class="art-article-main">
<p class="art-p">Pizza prices appear simple until you compare 10,000 menu rows. The Datafiniti pizza extract in TidyTuesday (released 2019-10-01) does exactly that: restaurant-level records with price-range fields revealing how "a slice" and "a specialty pie" occupy different economic tiers. The dataset contains <strong>10,000</strong> rows, with a median price-range minimum of <strong>0.00</strong> and a premium peak at <strong>50.0</strong>.</p>
<p class="art-p">The median price-range minimum of <strong>0.00</strong> signals that most listings encode missing or zero price floors rather than free pizza. The highest observed price-range minimum is <strong>50.0</strong>, shared by Oregano and Crust Stone Oven Pizza. That ceiling marks where tasting-menu and destination pizzerias sit — a tier separated by economics and intent from the mass market below.</p>

<h2 id="price-floors-separate-everyday-shops-from-destination-pies" class="anchored">Price Floors Separate Everyday Shops From Destination Pies</h2>
<h3 id="price-floors-separate-everyday-shops-from-destination-pies-look" class="anchored">Price range min by Name</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pizza/charts/chart1_breakdown.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pizza/charts/chart1_breakdown.png" role="img" aria-label="Price range min by Name"></div>
</figure>
<p class="art-p">At the top of the price-range-minimum ranking, Oregano and Crust Stone Oven Pizza both reach <strong>50.0</strong>. Just below, a cluster of shops—Papa's Pizza, Apizza Scholls, Barbaro, La Montanara, Spin, Dough Pizzeria Napoletana—sits at <strong>40.0</strong>. These are not typical delivery-store price floors. They mark the upper edge of how this dataset encodes premium positioning. Most of the 10,000-row catalog never approaches that band.</p>
<h2 id="the-top-dozen-is-a-premium-plateau" class="anchored">The Top Dozen Is a Premium Plateau</h2>
<h3 id="the-top-dozen-is-a-premium-plateau-look" class="anchored">Crust Stone Oven Pizza leads at 50.0 — 40.0 marks the median among the top dozen</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pizza/charts/chart2_leaders.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pizza/charts/chart2_leaders.png" role="img" aria-label="Crust Stone Oven Pizza leads at 50.0 — 40.0 marks the median among the top dozen"></div>
</figure>
<p class="art-p">Crust Stone Oven Pizza leads at <strong>50.0</strong>, and the median among the top dozen is <strong>40.0</strong>. Inside the premium tier, the story is less about a single outlier than about a shared price floor. That plateau is useful for citation: when asked what "expensive pizza" looks like in this file, the answer is a top-dozen median of 40—not the global median of 0.</p>
<h2 id="almost-everything-sits-in-the-low-bins" class="anchored">Almost Everything Sits in the Low Bins</h2>
<h3 id="almost-everything-sits-in-the-low-bins-look" class="anchored">Price range min Distribution</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pizza/charts/chart3_distribution.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pizza/charts/chart3_distribution.png" role="img" aria-label="Price range min Distribution"></div>
</figure>
<p class="art-p">The distribution is extreme. Roughly <strong>8,167</strong> rows fall in the lowest price-range-minimum bin, with about <strong>1,801</strong> in the next populated band. Only a few dozen observations occupy the high bins near 40–50. This is why the median of 0.00 is technically correct yet narratively incomplete. The market's mass is coded at zero or missing; the cultural story lives in the thin right tail.</p>
<h2 id="premium-names-concentrate-quickly" class="anchored">Premium Names Concentrate Quickly</h2>
<h3 id="premium-names-concentrate-quickly-look" class="anchored">Cumulative Price range min</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pizza/charts/chart4_pareto.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pizza/charts/chart4_pareto.png" role="img" aria-label="Cumulative Price range min"></div>
</figure>
<p class="art-p">The Pareto view of price-range minimum among leading names climbs steeply: the first five entries hold roughly <strong>43%</strong> of the plotted aggregate, and the curve reaches the full total by the fifteenth name. Concentration here measures how high price-floor labels cluster among a short list of restaurant names, not sales volume or market share.</p>
<h2 id="minimum-and-maximum-ranges-move-together-until-they-don-t" class="anchored">Minimum and Maximum Ranges Move Together — Until They Don't</h2>
<h3 id="minimum-and-maximum-ranges-move-together-until-they-don-t-look" class="anchored">Price range min vs Price range max</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/pizza/charts/chart5_scatter.plotly.json" data-source="Data: TidyTuesday / R for Data Science community - ARTOMETRICS" data-fallback="/images/content/articles/pizza/charts/chart5_scatter.png" role="img" aria-label="Price range min vs Price range max"></div>
</figure>
<p class="art-p">Scatter points of price-range minimum against price-range maximum show the expected diagonal: shops with higher floors also list higher ceilings, with some pairs reaching from 40 up toward 55. The mismatches are instructive—low floors with wide ceilings, or compressed ranges signaling a single-price menu. Those are the places where "pizza" stops being one product and becomes a price architecture.</p>
<h2 id="what-this-file-cannot-tell-you" class="anchored">What this file cannot tell you</h2>
<p class="art-p">Datafiniti restaurant scrapes are not audited menus. Zero price-range values may indicate missing data rather than free food. Name collisions and chain-versus-independent ambiguity persist.</p>
<p class="art-p">The extract cannot address ingredient costs, tip culture, or city-level rent. It measures listed price-range fields in a 2019 community snapshot.</p>
<h2 id="what-to-take-away" class="anchored">What to take away</h2>
<p class="art-p">In 10,000 pizza rows, the market's mass sits at a median price-range minimum of 0.00, while a thin premium tier reaches 50.0.</p>
<p class="art-p">Cite the top-dozen median of 40 when discussing destination pizza; cite the global median when discussing typical listings. They describe different economies.</p>
<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The source is the TidyTuesday release from 2019-10-01 (pizza_datafiniti.csv). The analysis frame contains 10,000 records after cleaning.</p>
<p class="art-p">Price-range minimum is the ranked metric across all charts. Medians are used because the distribution clusters heavily at low values. Charts are Plotly JSON with PNG fallbacks.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p>Data Science Learning Community. (2019). <em>TidyTuesday: All The Pizza</em>. <a href="https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-10-01/pizza_datafiniti.csv" target="_blank" rel="noopener noreferrer">https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-10-01/pizza_datafiniti.csv</a></p>
</section>
</main>
</div>
