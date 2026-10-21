# Artometrics shared ggplot2 export helpers.
# House style (Style Lab, Oct 2026): green-black ground, pink bars,
# Tiffany line, cream ink. Source from chart scripts:
# source("scripts/r/artometrics_theme.R")
#
# PNG posters already on the site keep their old colors until a report is
# re-exported. Live Plotly picks the same palette up in lib/charts/plotlyTheme.ts.
# 9B zero baseline, 10C scatter stroke, 12A Equal Earth, and 15B sign colors
# are opt-in helpers below. They do not recompute a series.

suppressPackageStartupMessages({
  library(ggplot2)
  library(scales)
})

ART_GROUND <- "#0e1110"
ART_INK <- "#f4f7f6"
ART_HIGHLIGHT <- "#ff3d8a"
ART_SECONDARY <- "#7fded6"
ART_MID <- "#8fb8b2"
ART_CREAM <- ART_GROUND
ART_DARK <- ART_INK
ART_MUTED <- "#2a3330"
ART_RED <- "#e60000"
ART_CYAN <- "#21e4ff"
ART_SPLIT_RED <- "#ff2a2a"

ART_BAR_GRADIENT <- c(
  "#7fded6", "#9adfd6", "#f3ead7", "#ffb3d4", "#ff3d8a"
)

ART_TIER_COLORS <- c(
  "No Penalty" = "#8fb8b2",
  "Low" = "#7fded6",
  "Medium" = "#f3ead7",
  "High" = "#ff3d8a"
)

ART_SOURCE_DEFAULT <- "Source: CMS Hospital Readmissions Reduction Program (HRRP), FY2025 supplemental data"

#' Register Chomsky wordmark font from repo (showtext)
art_init_fonts <- function(repo_root = getwd()) {
  chomsky_path <- file.path(repo_root, "src/fonts/Chomsky.otf")
  if (!requireNamespace("showtext", quietly = TRUE) ||
      !requireNamespace("sysfonts", quietly = TRUE) ||
      !file.exists(chomsky_path)) {
    return(invisible(FALSE))
  }

  if (!"Chomsky" %in% sysfonts::font_families()) {
    sysfonts::font_add("Chomsky", regular = chomsky_path)
  }
  showtext::showtext_auto(enable = TRUE)
  invisible(TRUE)
}

art_has_chomsky <- function() {
  requireNamespace("showtext", quietly = TRUE) &&
    "Chomsky" %in% sysfonts::font_families()
}

art_wordmark_family <- function() {
  if (art_has_chomsky()) "Chomsky" else "serif"
}

art_title_theme <- function() {
  if (requireNamespace("ggtext", quietly = TRUE)) {
    ggtext::element_markdown(color = ART_DARK, face = "bold", size = rel(1.15), margin = margin(b = 8))
  } else {
    element_text(color = ART_DARK, face = "bold", size = rel(1.15), margin = margin(b = 8))
  }
}

#' Artometrics ggplot2 theme
theme_artometrics <- function(base_size = 11) {
  theme_minimal(base_size = base_size, base_family = "Helvetica") +
    theme(
      plot.background = element_rect(fill = ART_GROUND, color = NA),
      panel.background = element_rect(fill = ART_GROUND, color = NA),
      panel.grid.major.y = element_line(color = ART_MUTED, linewidth = 0.32),
      panel.grid.major.x = element_line(color = "#1c2422", linewidth = 0.22),
      panel.grid.minor = element_blank(),
      axis.line.x = element_line(color = ART_MUTED, linewidth = 0.35),
      axis.ticks = element_line(color = ART_MUTED, linewidth = 0.3),
      axis.ticks.length = unit(3, "pt"),
      axis.title = element_text(color = ART_MID, size = rel(0.82), margin = margin(t = 6, r = 6)),
      axis.text = element_text(color = ART_DARK, size = rel(0.78)),
      plot.title = art_title_theme(),
      plot.subtitle = element_text(color = ART_MID, size = rel(0.88), margin = margin(b = 12)),
      plot.caption = element_text(color = ART_MID, size = rel(0.7), hjust = 0, margin = margin(t = 14)),
      legend.title = element_text(color = ART_DARK, face = "bold", size = rel(0.74)),
      legend.text = element_text(color = ART_MID, size = rel(0.72)),
      legend.position = "bottom",
      legend.key.height = unit(10, "pt"),
      legend.key.width = unit(14, "pt"),
      strip.text = element_text(face = "bold", color = ART_DARK, size = rel(0.8)),
      strip.background = element_rect(fill = "#121014", color = NA),
      plot.margin = margin(t = 14, r = 18, b = 16, l = 14)
    )
}

#' Canonical Plotly config for magazine embeds (hover only — no zoom/pan)
art_plotly_config <- function() {
  list(
    displayModeBar = FALSE,
    displaylogo = FALSE,
    responsive = TRUE,
    scrollZoom = FALSE,
    doubleClick = FALSE,
    staticPlot = FALSE,
    editable = FALSE,
    showTips = FALSE
  )
}

#' Chomsky wordmark bottom-right
art_wordmark <- function(label = "Artometrics") {
  annotate(
    "text",
    x = Inf, y = -Inf,
    label = label,
    hjust = 1.05, vjust = -0.5,
    size = 3.8,
    color = ART_MID,
    family = art_wordmark_family()
  )
}

#' Build caption with source line
art_caption <- function(source = ART_SOURCE_DEFAULT) {
  paste0(source, "  ·  ", "Artometrics")
}

#' Gradient fill vector for n bars (leader gets brightest emerald)
art_bar_colors <- function(n, highlight_last = TRUE) {
  if (n <= 0) return(character(0))
  if (n <= length(ART_BAR_GRADIENT)) {
    colors <- ART_BAR_GRADIENT[seq_len(n)]
  } else {
    idx <- round(seq(1, length(ART_BAR_GRADIENT), length.out = n))
    colors <- ART_BAR_GRADIENT[idx]
  }
  if (highlight_last && n > 0) colors[n] <- ART_HIGHLIGHT
  colors
}

#' Fallback in-plot takeaway strip when cowplot unavailable
art_takeaway_strip <- function(takeaway, fill = "#100e0c") {
  list(
    annotate(
      "rect",
      xmin = -Inf, xmax = Inf, ymin = Inf, ymax = Inf,
      fill = fill, color = NA
    ),
    annotate(
      "text",
      x = -Inf, y = Inf,
      label = takeaway,
      hjust = -0.02, vjust = 1.8,
      color = ART_INK,
      size = 3.2,
      fontface = "bold",
      family = "Helvetica"
    )
  )
}

#' Emerald takeaway strip (Economist-style header band)
art_takeaway_grob <- function(takeaway, fill = "#100e0c", width = 12, height = 0.55) {
  if (!requireNamespace("cowplot", quietly = TRUE)) {
    return(NULL)
  }
  cowplot::ggdraw() +
    cowplot::draw_label(
      takeaway,
      x = 0.015,
      hjust = 0,
      fontface = "bold",
      color = ART_INK,
      size = 11,
      fontfamily = "Helvetica"
    ) +
    ggplot2::theme(
      plot.background = ggplot2::element_rect(fill = fill, color = NA),
      plot.margin = ggplot2::margin(6, 10, 6, 10)
    )
}

#' Compose takeaway strip + chart (+ optional wordmark handled in chart)
finish_art_chart <- function(plot_obj, takeaway, source = ART_SOURCE_DEFAULT) {
  plot_obj <- plot_obj +
    art_wordmark() +
    labs(caption = art_caption(source)) +
    coord_cartesian(clip = "off") +
    theme(
      plot.margin = margin(t = 12, r = 16, b = 18, l = 14),
      plot.caption = element_text(
        color = ART_MID,
        size = rel(0.72),
        hjust = 0,
        margin = margin(t = 14),
        family = "Helvetica"
      )
    )

  strip <- art_takeaway_grob(takeaway)
  if (is.null(strip)) {
    return(
      plot_obj +
        art_takeaway_strip(takeaway) +
        theme(plot.margin = margin(t = 32, r = 16, b = 18, l = 14))
    )
  }

  cowplot::plot_grid(
    strip,
    plot_obj,
    ncol = 1,
    rel_heights = c(0.07, 1)
  )
}

#' Save ggplot PNG (and optional Plotly JSON)
save_art_chart <- function(
  plot_obj,
  filename,
  charts_dir = "charts",
  width = 12,
  height = 7,
  dpi = 300,
  plotly_obj = NULL
) {
  dir.create(charts_dir, recursive = TRUE, showWarnings = FALSE)
  png_path <- file.path(charts_dir, paste0(filename, ".png"))

  ggsave(
    filename = paste0(filename, ".png"),
    plot = plot_obj,
    path = charts_dir,
    width = width,
    height = height,
    dpi = dpi,
    bg = ART_GROUND
  )

  if (!is.null(plotly_obj)) {
    if (!requireNamespace("plotly", quietly = TRUE) ||
        !requireNamespace("jsonlite", quietly = TRUE)) {
      warning("Install plotly and jsonlite to export .plotly.json for ", filename)
      return(invisible(png_path))
    }

    built <- plotly::plotly_build(plotly_obj)
    payload <- list(
      data = built$x$data,
      layout = built$x$layout,
      config = art_plotly_config()
    )
    json_path <- file.path(charts_dir, paste0(filename, ".plotly.json"))
    jsonlite::write_json(payload, json_path, auto_unbox = TRUE, pretty = TRUE)
  }

  invisible(png_path)
}

#' 9B — include zero on a continuous y scale. Opt in; do not wrap published series.
art_zero_scale <- function() {
  scale_y_continuous(expand = expansion(mult = c(0, 0.06)))
}

#' 10C — red point, cyan stroke. Pass the real x/y; this does not offset them.
art_scatter_layer <- function(...) {
  geom_point(
    color = ART_CYAN,
    fill = ART_SPLIT_RED,
    shape = 21,
    stroke = 1.1,
    ...
  )
}

#' 12A — Equal Earth proj string (EPSG:8857). Caller applies it; this does not reproject data.
art_equal_earth <- function() {
  "+proj=eqearth +datum=WGS84 +units=m +no_defs"
}

#' 15B — color an already-computed change column by sign. Does not difference levels.
art_change_colors <- function(change) {
  ifelse(change < 0, ART_SECONDARY, ifelse(change > 0, ART_HIGHLIGHT, ART_MID))
}
