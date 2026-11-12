#!/usr/bin/env Rscript
# Draws the Franchise 2026 top-ten chart from its CSV with the shared R style, light and dark.
# Usage (repo root): Rscript scripts/r/render-chart-style-demo.R [out_dir]
source("scripts/r/artometrics_chart_style.R")
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[[1]] else file.path(tempdir(), "art-chart-style-demo")
box <- read.csv("articles/franchise/data/raw/box_office_top10_snapshot_2026-11-10.csv", stringsAsFactors = FALSE)
y26 <- box[box$release_year == 2026, ]
chart <- art_hbar(
  y26$title, y26$worldwide_gross_usd / 1e9,
  "Six of 2026's ten biggest films were already serial",
  "Box Office Mojo, read 10 Nov 2026. Red is a franchise installment. The year is not over.",
  "Source: Box Office Mojo worldwide year page (S005).",
  roles = ifelse(y26$is_franchise_film == "True", "red", "blue"),
  fmt = function(v) sprintf("$%.2fB", v)
)
files <- art_save_modes(chart, file.path(out, "chart16-r"))
cat(files, sep = "\n")
