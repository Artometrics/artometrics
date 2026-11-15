# Original data-art for POLLING: one dot per 100 polling-place addresses in the 23 complete states in 2012.
# Pink dots are the ~67 hundreds that were gone by 2020, scattered at random so the grid reads as holes. Writes hero.png (16:9) and square-art-src.png (1:1). No text.
suppressPackageStartupMessages({ library(dplyr); library(readr); library(ggplot2); library(jsonlite) })
pal <- fromJSON("scripts/charts/art-chart-style.json")$dark
tot <- read_csv("articles/polling/data/totals_complete_states.csv", show_col_types = FALSE)
before <- tot$places[tot$year == 2012]; after <- tot$places[tot$year == 2020]
n <- round(before / 100); kept <- round(after / 100)
out <- "public/images/content/articles/polling"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
draw <- function(file, w, h, cols) {
  rows <- ceiling(n / cols)
  set.seed(2012); lost_ids <- sample(n, n - kept)
  df <- data.frame(i = seq_len(n)) |> mutate(x = (i - 1) %% cols, y = rows - 1 - (i - 1) %/% cols, lost = i %in% lost_ids)
  g <- ggplot(df, aes(x, y, color = lost)) + geom_point(size = if (cols > 25) 4.6 else 5.4, shape = 16) +
    scale_color_manual(values = c(`FALSE` = pal$ink, `TRUE` = pal$red)) +
    coord_fixed(xlim = c(-1, cols), ylim = c(-1, rows), expand = FALSE) +
    theme_void() + theme(legend.position = "none", plot.background = element_rect(fill = pal$paper, color = NA))
  ragg::agg_png(file, width = w, height = h, units = "px", res = 144, background = pal$paper)
  print(g); dev.off()
}
draw(file.path(out, "hero.png"), 1376, 768, 30)
draw(file.path(out, "square-art-src.png"), 800, 800, 22)
