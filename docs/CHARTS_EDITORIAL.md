# Editorial chart style

Charts follow an Economist-inspired Artometrics style: pink flag, bold headline and subtitle on the chart, light grid, direct labels, source line, dark twin for night mode.

- Theme and builders: `scripts/r/artometrics_editorial.R` (`art_ed_hbar`, `art_ed_col`, `art_ed_line`, `art_ed_scatter`, `art_ed_box`, `art_ed_save`).
- Tokens (shared with the older theme): `scripts/charts/art-chart-style.json`.
- Re-render existing reports from their Plotly sidecars (`public/data/articles/<slug>/charts/*.plotly.json`), no data is changed:

```bash
Rscript scripts/charts/render-editorial.R --all --editorial      # every chart with a written headline or override
Rscript scripts/charts/render-editorial.R pixar chart1_runtime_timeline
node scripts/charts/optimize-pngs.mjs public/images/content/articles/<slug>/charts
npm run test:chart-style
```

- Headlines and subtitles come from the chart's own title or from `scripts/charts/editorial-overrides.json`. Charts with auto-generated generic titles are skipped on purpose.
- Needs R with `ggplot2`, `ragg`, `ggtext`, `ggrepel`, `systemfonts`, `jsonlite` and the fonts in `assets/fonts` (Anton, DM Sans, DM Mono).
- Franchise and Anime keep their bespoke charts and are never overwritten by `--all`.
- New reports: `articles/markers/analysis.R` and `articles/polling/analysis.R` show the full path from TidyTuesday CSV to chart.
