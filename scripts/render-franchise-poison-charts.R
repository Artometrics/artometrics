#!/usr/bin/env Rscript
# Export poison charts (PNG + Plotly JSON).

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

# Brand palette — white field, blue / red / black
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

public_img <- file.path(repo_root, "public/images/content/articles", slug, "charts")
public_data <- file.path(repo_root, "public/data/articles", slug, "charts")
dir.create(public_img, recursive = TRUE, showWarnings = FALSE)
dir.create(public_data, recursive = TRUE, showWarnings = FALSE)

FRANCHISE_SOURCE <- "Data: TidyTuesday / Box Office Mojo — ARTOMETRICS"
LETO_SOURCE <- "Data: Box Office Mojo trade-reported budgets — ARTOMETRICS"
SCALE_SOURCE <- "Data: Artometrics franchise + horror-tagged box-office reports — ARTOMETRICS"

wordmark_family <- function() {
  if (art_has_chomsky()) "Chomsky" else "Georgia, serif"
}

verify_chart1_from_franchise_csv <- function() {
  path <- file.path(repo_root, "articles/franchise/data/franchise.csv")
  if (!file.exists(path)) {
    message("Note: ", path, " not found — skipping chart1 verification.")
    return(invisible(NULL))
  }
  df <- read_csv(path, show_col_types = FALSE)
  merch_cat <- "Merchandise, Licensing & Retail"
  tot <- sum(df$revenue, na.rm = TRUE)
  merch <- sum(df$revenue[df$revenue_category == merch_cat], na.rm = TRUE)
  pct <- round(merch / tot * 100)
  message(
    "Chart 1 verification: franchise.csv row-sum gives ~", pct, "% merchandise / ",
    100 - pct, "% other (", n_distinct(df$franchise), " franchises). ",
    "Chart uses CSV shares (aligned with franchise R2) — see articles/", slug, "/data/README.md."
  )
}

write_plotly_json <- function(fig, path) {
  built <- plotly_build(fig)
  payload <- list(
    data = built$x$data,
    layout = built$x$layout,
    config = art_plotly_config()
  )
  write_json(payload, path, auto_unbox = TRUE, pretty = TRUE, null = "null", na = "null")
  message("Wrote ", path)
}

copy_to_public <- function(name) {
  file.copy(
    file.path(charts_dir, paste0(name, ".png")),
    file.path(public_img, paste0(name, ".png")),
    overwrite = TRUE
  )
  file.copy(
    file.path(charts_dir, paste0(name, ".plotly.json")),
    file.path(public_data, paste0(name, ".plotly.json")),
    overwrite = TRUE
  )
  r_path <- file.path(charts_dir, paste0(name, ".r"))
  if (file.exists(r_path)) {
    file.copy(
      r_path,
      file.path(public_data, paste0(name, ".r")),
      overwrite = TRUE
    )
  }
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
    device = if (requireNamespace("ragg", quietly = TRUE)) ragg::agg_png else "png"
  )
  message("Wrote ", path)
  invisible(path)
}

plotly_chrome <- function(fig, title, subtitle, takeaway, source, margin = list(l = 60, r = 40, t = 110, b = 90)) {
  layout(
    fig,
    title = list(
      text = paste0(
        "<b>", title, "</b>",
        "<br><span style='font-size:12px;color:", ART_MID, "'>", subtitle, "</span>"
      ),
      x = 0,
      xanchor = "left"
    ),
    paper_bgcolor = ART_PAGE,
    plot_bgcolor = ART_PAGE,
    font = list(family = FONT, color = ART_DARK, size = 12),
    xaxis = list(
      gridcolor = "#E5E5E5",
      linecolor = "#D5D5D5",
      zerolinecolor = "#D5D5D5"
    ),
    yaxis = list(
      gridcolor = "#E5E5E5",
      linecolor = "#D5D5D5",
      zerolinecolor = "#D5D5D5"
    ),
    margin = margin,
    annotations = list(
      list(
        x = 0, y = 1.14, xref = "paper", yref = "paper",
        text = paste0("<b>", takeaway, "</b>"),
        showarrow = FALSE, xanchor = "left", align = "left",
        font = list(size = 11, color = "#FFFFFF"),
        bgcolor = ART_HIGHLIGHT,
        borderpad = 6
      ),
      list(
        x = 0, y = -0.22, xref = "paper", yref = "paper",
        text = art_caption(source),
        showarrow = FALSE, xanchor = "left",
        font = list(size = 9, color = ART_MID)
      ),
      list(
        x = 0.99, y = -0.22, xref = "paper", yref = "paper",
        text = "Artometrics",
        showarrow = FALSE, xanchor = "right",
        font = list(size = 12, color = ART_DARK, family = wordmark_family())
      )
    )
  )
}

theme_white <- function() {
  theme_artometrics() +
    theme(
      plot.background = element_rect(fill = ART_PAGE, color = NA),
      panel.background = element_rect(fill = ART_PAGE, color = NA),
      panel.grid.major = element_line(color = "#E8E8E8", linewidth = 0.35),
      strip.background = element_rect(fill = "#F5F5F5", color = NA)
    )
}

verify_chart1_from_franchise_csv()

# ── Chart 1: Merchandise vs all other revenue ───────────────────────────────

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
write_plotly_json(fig1, file.path(charts_dir, "chart1_revenue_stream_share.plotly.json"))
copy_to_public("chart1_revenue_stream_share")

# ── Chart 2: Leto slate gross ÷ budget ────────────────────────────────────────

chart2 <- read_csv(
  file.path(data_dir, "chart2_leto_slate_ratios.csv"),
  show_col_types = FALSE
) %>%
  mutate(
    title = fct_reorder(title, ratio),
    bar_color = if_else(below_breakeven, ART_HIGHLIGHT, ART_BLUE)
  )

p2 <- ggplot(chart2, aes(x = title, y = ratio)) +
  geom_hline(yintercept = 1, linetype = "dashed", color = ART_BLACK, linewidth = 0.7) +
  geom_col(aes(fill = bar_color), width = 0.62, show.legend = FALSE) +
  scale_fill_identity() +
  geom_text(
    aes(label = paste0(ratio, "x")),
    vjust = -0.35,
    size = 3.4,
    color = ART_DARK,
    family = FONT,
    fontface = "bold"
  ) +
  annotate(
    "text",
    x = 0.6,
    y = 1.08,
    label = "Breakeven (1.0x)",
    color = ART_MID,
    size = 3,
    family = FONT
  ) +
  scale_y_continuous(
    limits = c(0, 2.35),
    expand = expansion(mult = c(0, 0.05))
  ) +
  labs(
    title = "Six-film Jared Leto slate: <span style='color:#C0392B;'>worldwide gross</span> ÷ reported budget",
    subtitle = "Three titles at or below breakeven — no merchandise layer underneath",
    x = NULL,
    y = "Gross ÷ budget multiple"
  ) +
  theme_white() +
  theme(
    axis.text.x = element_text(angle = 35, hjust = 1, size = rel(0.72)),
    panel.grid.major.x = element_blank()
  )

p2 <- finish_art_chart(
  p2,
  takeaway = "Half this slate lands at or below 1.0x — concentrated theatrical exposure",
  source = LETO_SOURCE
)
save_png(p2, "chart2_leto_slate_ratios", height = 6.2)

fig2 <- plot_ly() %>%
  add_trace(
    data = chart2,
    x = ~title,
    y = ~ratio,
    type = "bar",
    marker = list(color = ~bar_color, line = list(width = 0)),
    text = ~paste0(ratio, "x"),
    textposition = "outside",
    hovertemplate = "<b>%{x}</b><br>%{y}x gross ÷ budget<extra></extra>",
    name = "Gross ÷ budget"
  ) %>%
  add_trace(
    x = chart2$title,
    y = rep(1, nrow(chart2)),
    type = "scatter",
    mode = "lines",
    line = list(color = ART_BLACK, width = 1.5, dash = "dash"),
    hoverinfo = "skip",
    name = "Breakeven (1.0x)",
    showlegend = TRUE
  ) %>%
  plotly_chrome(
    title = "Six-film Jared Leto slate: worldwide gross ÷ reported budget",
    subtitle = "Case-study slate — trade-reported budgets",
    takeaway = "Half this slate lands at or below 1.0x — concentrated theatrical exposure",
    source = LETO_SOURCE,
    margin = list(l = 60, r = 30, t = 110, b = 120)
  ) %>%
  layout(
    yaxis = list(title = "Gross ÷ budget multiple", range = c(0, 2.4)),
    xaxis = list(title = "", tickangle = -35),
    legend = list(orientation = "h", y = -0.35, x = 0)
  )
write_plotly_json(fig2, file.path(charts_dir, "chart2_leto_slate_ratios.plotly.json"))
copy_to_public("chart2_leto_slate_ratios")

# ── Chart 3: Scale comparison (log) ───────────────────────────────────────────

chart3 <- read_csv(
  file.path(data_dir, "chart3_scale_comparison.csv"),
  show_col_types = FALSE
) %>%
  mutate(
    label = fct_reorder(label, value_millions),
    bar_color = case_when(
      color_role == "highlight" ~ ART_HIGHLIGHT,
      color_role == "secondary" ~ ART_BLUE,
      TRUE ~ ART_BLACK
    ),
    text_label = case_when(
      value_millions >= 1000 ~ paste0("$", comma(value_millions), "M"),
      TRUE ~ paste0("$", value_millions, "M")
    )
  )

p3 <- ggplot(chart3, aes(x = value_millions, y = label)) +
  geom_col(aes(fill = bar_color), width = 0.62, show.legend = FALSE) +
  scale_fill_identity() +
  geom_text(
    aes(label = text_label),
    hjust = -0.08,
    size = 3.5,
    color = ART_DARK,
    family = FONT,
    fontface = "bold"
  ) +
  scale_x_log10(
    labels = function(x) paste0("$", comma(x), "M"),
    expand = expansion(mult = c(0.05, 0.25))
  ) +
  labs(
    title = "IP-franchise scale vs. <span style='color:#C0392B;'>single-title</span> scale",
    subtitle = "US dollars, millions (log axis) — different orders of magnitude, not one curve",
    x = "US dollars, millions (log scale)",
    y = NULL
  ) +
  theme_white() +
  theme(panel.grid.major.y = element_blank())

p3 <- finish_art_chart(
  p3,
  takeaway = "Pokémon's $91B lifetime total dwarfs a median film or a single blockbuster budget",
  source = SCALE_SOURCE
)
save_png(p3, "chart3_scale_comparison", height = 5.6)

fig3 <- plot_ly(
  chart3,
  x = ~value_millions,
  y = ~label,
  type = "bar",
  orientation = "h",
  marker = list(color = ~bar_color, line = list(width = 0)),
  text = ~text_label,
  textposition = "outside",
  hovertemplate = "<b>%{y}</b><extra></extra>",
  name = "Scale ($M, log axis)"
) %>%
  plotly_chrome(
    title = "IP-franchise scale vs. single-title scale ($M, log axis)",
    subtitle = "Pokémon lifetime revenue vs median film vs largest case-study budget",
    takeaway = "Pokémon's $91B lifetime total dwarfs a median film or a single blockbuster budget",
    source = SCALE_SOURCE,
    margin = list(l = 320, r = 70, t = 110, b = 90)
  ) %>%
  layout(
    xaxis = list(title = "US dollars, millions (log scale)", type = "log"),
    yaxis = list(title = "", categoryorder = "array", categoryarray = as.character(chart3$label)),
    showlegend = FALSE
  )
write_plotly_json(fig3, file.path(charts_dir, "chart3_scale_comparison.plotly.json"))
copy_to_public("chart3_scale_comparison")

message("Done — charts synced to public/images and public/data for ", slug)
