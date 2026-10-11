# Artometrics — reproducible R chart snippet
# Run from the artometrics-web repository root.
# Requires: tidyverse, scales, plotly, jsonlite, ragg

suppressPackageStartupMessages({
  library(tidyverse)
  library(scales)
  library(plotly)
  library(jsonlite)
})

script_dir <- tryCatch(
  dirname(normalizePath(sub(
    "^--file=", "",
    commandArgs(trailingOnly = FALSE)[grep("^--file=", commandArgs(trailingOnly = FALSE))][1]
  ))),
  error = function(e) getwd()
)
repo_root <- normalizePath(file.path(script_dir, ".."))
source(file.path(repo_root, "scripts/r/artometrics_theme.R"))
art_init_fonts(repo_root)

ART_PAGE <<- "#FFFFFF"
ART_CREAM <<- "#FFFFFF"
ART_BLUE <<- "#1B4F8A"
ART_BLACK <<- "#000000"
FONT <- "Helvetica"
slug <- "poison"
article_dir <- file.path(repo_root, "articles", slug)
data_dir <- file.path(article_dir, "data")
charts_dir <- file.path(article_dir, "charts")
dir.create(charts_dir, recursive = TRUE, showWarnings = FALSE)

FRANCHISE_SOURCE <- "Data: TidyTuesday / Box Office Mojo — ARTOMETRICS"
LETO_SOURCE <- "Data: Box Office Mojo trade-reported budgets — ARTOMETRICS"
SCALE_SOURCE <- "Data: Artometrics franchise + horror-tagged box-office reports — ARTOMETRICS"

wordmark_family <- function() {
  if (art_has_chomsky()) "Chomsky" else "Georgia, serif"
}

save_png <- function(plot_obj, name, height = 7) {
  path <- file.path(charts_dir, paste0(name, ".png"))
  ggsave(
    filename = path,
    plot = plot_obj,
    width = 12,
    height = height,
    dpi = 300,
    bg = ART_PAGE,
    device = ragg::agg_png
  )
  invisible(path)
}

write_plotly_json <- function(fig, path) {
  built <- plotly_build(fig)
  payload <- list(
    data = built$x$data,
    layout = built$x$layout,
    config = art_plotly_config()
  )
  write_json(payload, path, auto_unbox = TRUE, pretty = TRUE, null = "null", na = "null")
}


chart1 <- read_csv(
  file.path(data_dir, "chart1_revenue_stream_share.csv"),
  show_col_types = FALSE
) %>%
  mutate(
    stream = fct_reorder(stream, share_pct),
    bar_color = if_else(
      grepl("Merchandise", stream, fixed = TRUE),
      ART_HIGHLIGHT,
      ART_BLUE
    )
  )

p1 <- ggplot(chart1, aes(x = share_pct, y = stream)) +
  geom_col(aes(fill = bar_color), width = 0.62, show.legend = FALSE) +
  scale_fill_identity() +
  geom_text(
    aes(label = paste0(share_pct, "%")),
    hjust = -0.12,
    size = 4.2,
    color = ART_DARK,
    family = FONT,
    fontface = "bold"
  ) +
  scale_x_continuous(
    labels = function(x) paste0(x, "%"),
    expand = expansion(mult = c(0, 0.16))
  ) +
  labs(
    title = "Merchandise share of revenue across <span style='color:#C0392B;'>103</span> franchise rows",
    subtitle = "Share of row-sum lifetime revenue by stream (franchise.csv, TidyTuesday 2019-07-02)",
    x = "Share of tracked lifetime revenue (%)",
    y = NULL
  ) +
  theme_white() +
  theme(panel.grid.major.y = element_blank())

p1 <- finish_art_chart(
  p1,
  takeaway = "Merchandise and licensing — not box office — carry most franchise revenue",
  source = FRANCHISE_SOURCE
)
save_png(p1, "chart1_revenue_stream_share", height = 5.8)

fig1 <- plot_ly(
  chart1,
  x = ~share_pct,
  y = ~stream,
  type = "bar",
  orientation = "h",
  marker = list(color = ~bar_color, line = list(width = 0)),
  text = ~paste0(share_pct, "%"),
  textposition = "outside",
  hovertemplate = "<b>%{y}</b><br>%{x}% of tracked revenue<extra></extra>"
) %>%
  plotly_chrome(
    title = "Merchandise share of revenue across 103 franchise rows",
    subtitle = "Share of tracked lifetime revenue by stream",
    takeaway = "Merchandise and licensing — not box office — carry most franchise revenue",
    source = FRANCHISE_SOURCE,
    margin = list(l = 240, r = 50, t = 110, b = 90)
  ) %>%
  layout(
    xaxis = list(title = "Share of tracked lifetime revenue (%)", range = c(0, 72)),
    yaxis = list(title = "", categoryorder = "array", categoryarray = rev(as.character(chart1$stream))),
    showlegend = FALSE
  )
