# FRANCHISE: Merchandise Owns the Ledger

**Desk:** arts · **Live:** https://artometrics.com/franchise/

Wikipedia's franchise list (revision 1384334611, 7 November 2026, read 10 November 2026) sums 140 franchises to $1,460.1B in lifetime consumer-spend estimates. Merchandise, licensing and retail are 55.6%. Pokémon, at $130.7B, is larger than Star Wars and the Marvel Cinematic Universe combined ($84.2B). Nine of 2025's ten biggest films were franchise installments.

These are nominal estimates compiled by Wikipedia's editors. They are not profit, not a valuation, and not cash paid to a rights holder. What changed since the 12 October article is in `data/CHANGELOG.md`.

## Layout

```text
franchise/
  _quarto.yml
  franchise.qmd
  data/
  charts/
  figures/
```

```bash
cd articles/franchise
quarto render
npm run sync:article -- --slug franchise
```

## Charts

Charts are drawn by `scripts/build_theme_a_charts.py` from the CSVs in `data/`, once in light and once in dark (`name.png`, `name-dark.png`). Colors come from `scripts/charts/art-chart-style.json`, which `scripts/r/artometrics_chart_style.R` also reads, so R and Python draw the same style. The site swaps the two files by theme.

```bash
python3 articles/franchise/scripts/build_theme_a_charts.py
npm run test:charts
```
