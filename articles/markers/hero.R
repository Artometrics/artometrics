# Original data-art for MARKERS: every historical marker in the extract plotted at its coordinates. Texas in pink.
# Writes public/images/content/articles/markers/hero.png (16:9) and square-art-src.png (1:1). No text.
suppressPackageStartupMessages({ library(dplyr); library(readr); library(ggplot2); library(jsonlite) })
args <- commandArgs(trailingOnly = TRUE)
hm <- read_csv(if (length(args)) args[1] else "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2023/2023-07-04/historical_markers.csv",
               show_col_types = FALSE, guess_max = 100000)
pal <- fromJSON("scripts/charts/art-chart-style.json")$dark
d <- hm |> filter(between(longitude_minus_w, -125, -66), between(latitude_minus_s, 24, 50)) |>
  mutate(tx = state_or_prov == "Texas")
out <- "public/images/content/articles/markers"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
draw <- function(file, w, h, xlim = c(-127, -64), ylim = c(23, 51)) {
  g <- ggplot(d, aes(longitude_minus_w, latitude_minus_s)) +
    geom_point(data = d[!d$tx, ], color = pal$ink, alpha = 0.7, size = 0.7, stroke = 0) +
    geom_point(data = d[d$tx, ], color = pal$red, alpha = 0.8, size = 0.7, stroke = 0) +
    coord_fixed(ratio = 1.28, xlim = xlim, ylim = ylim, expand = FALSE) +
    theme_void() + theme(plot.background = element_rect(fill = pal$paper, color = NA), plot.margin = margin(0, 0, 0, 0))
  ragg::agg_png(file, width = w, height = h, units = "px", res = 144, background = pal$paper)
  print(g); dev.off()
}
draw(file.path(out, "hero.png"), 1376, 768)
draw(file.path(out, "square-art-src.png"), 800, 800, xlim = c(-107, -71), ylim = c(24, 52))
