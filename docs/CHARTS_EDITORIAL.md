# Editorial chart style

Charts follow an Economist-inspired Artometrics style: pink flag, bold headline and subtitle on the chart, light grid, direct labels, source line, dark twin for night mode.

- Theme and builders: `scripts/r/artometrics_editorial.R` (`art_ed_hbar`, `art_ed_col`, `art_ed_line`, `art_ed_scatter`, `art_ed_box`, `art_ed_save`).
- Tokens (shared with the older theme): `scripts/charts/art-chart-style.json`.
- Re-render existing reports from their Plotly sidecars (`public/data/articles/<slug>/charts/*.plotly.json`), no data is changed:

```bash
Rscript scripts/charts/render-editorial.R --all                  # every chart used by an article (460 of 503 render today)
Rscript scripts/charts/render-editorial.R --all --editorial      # only charts with a written headline or override
Rscript scripts/charts/render-editorial.R pixar chart1_runtime_timeline
node scripts/charts/optimize-pngs.mjs public/images/content/articles/<slug>/charts
npm run test:chart-style
```

- Headlines and subtitles come from the chart's own title when it was written by hand, or from `scripts/charts/editorial-overrides.json`. Charts with generic titles ("Period or category bar", "Joint distribution", ...) get a headline and subtitle derived from the plotted numbers only (largest bar and its multiple of the next, Spearman rank correlation for scatters, first-to-last change for lines, and so on). Bars that carry their own label text (for example `$130.7B`) keep it, so units survive.
- Supported shapes: horizontal and vertical bars, grouped and stacked bars (2-5 series), histograms, box plots, scatters (pooled groups, log axes), dot plots, small heatmaps and lines (date, numeric or categorical x, up to 6 series).
- Skipped on purpose (43 of 503): radar and network charts, ridgelines, multi-trace annotated timelines with text traces, overlaid bar+line combos, single-point lines and sidecars with no traces (Beyonce and Trademarks).
- Needs R with `ggplot2`, `ragg`, `ggtext`, `ggrepel`, `systemfonts`, `jsonlite` and the fonts in `assets/fonts` (Anton, DM Sans, DM Mono).
- Franchise and Anime are rendered by `--all` like every other report; hand-written headlines in their sidecars are kept.
- New reports: `articles/markers/analysis.R` and `articles/polling/analysis.R` show the full path from TidyTuesday CSV to chart.
