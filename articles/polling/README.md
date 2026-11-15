# POLLING

Source: TidyTuesday 2024-01-16, US Polling Places 2012-2020 (Center for Public Integrity, PublicI/us-polling-places).

```sh
Rscript articles/polling/analysis.R      # tables in data/, charts and Plotly sidecars, public/data/articles/polling
Rscript articles/polling/hero.R          # cover data-art (one dot per 100 addresses in 2012)
node scripts/charts/optimize-pngs.mjs public/images/content/articles/polling/charts
```

The raw file is 73 MB and is not committed. The script downloads it from GitHub; pass a local `polling_places.csv` path as the first argument to run offline. Only the 23 states with data in all five general elections are compared (see `data/states_complete_2012_2020.csv`).
