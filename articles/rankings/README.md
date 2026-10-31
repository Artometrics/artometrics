# How the Top of the Hot 100 Slowed Down, Then Sped Up Again

**Desk:** arts · **Live:** https://artometrics.com/rankings/

Distinct songs in the Hot 100 top 10, from the chart dated Aug 4, 1958 through the chart dated Oct 31, 2026. A song earns 101 minus its position each week. Position 1 is best.

## Layout

```text
rankings/
  _quarto.yml
  billboard-top-100.qmd
  data/
    build_hot100_rankings.py
    crowding_by_year.csv
    song_points.csv
    merged_name_pairs.csv
    dataset.csv          # 2021 TidyTuesday extract, kept, unreferenced
  charts/                # five new charts, plus the previous PNGs
```

The previous chart PNGs stay in `charts/`. The new files are `distinct-top10-songs-by-year`, `avg-weeks-in-top10-by-year`, `distinct-number-ones-by-year`, `all-time-top20-points`, and `era-top5-points`, each as Plotly JSON and PNG.

## Rebuild

```bash
python3 articles/rankings/data/build_hot100_rankings.py
```

The script downloads `data-out/hot-100-current.csv` from utdata/rwd-billboard-data at commit ff86f04. The repository code is MIT. The chart rows are Billboard's. It stops if the sheet checks do not match. It does not rewrite `dataset.csv` or the previous chart PNGs.

```bash
cd articles/rankings
quarto render
```
