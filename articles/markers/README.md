# MARKERS

Source: TidyTuesday 2023-07-04, Historical Markers (Historical Marker Database, hmdb.org).

```sh
Rscript articles/markers/analysis.R      # tables in data/, charts and Plotly sidecars, public/data/articles/markers
Rscript articles/markers/hero.R          # cover data-art (every marker at its coordinates)
node scripts/charts/optimize-pngs.mjs public/images/content/articles/markers/charts
```

The scripts read the TidyTuesday CSVs from GitHub; pass a local `historical_markers.csv` path as the first argument to run offline. Requires R with `dplyr`, `readr`, `stringr`, `tidyr`, `ggplot2`, `ggtext`, `ggrepel`, `ragg`, `systemfonts`, `jsonlite`.
