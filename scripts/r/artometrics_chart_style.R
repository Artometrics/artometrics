# One chart style in two modes, shared with Python.
# Tokens live in scripts/charts/art-chart-style.json. The page shows the render that matches the theme:
#   <slug>.png       light
#   <slug>-dark.png  dark
#
#   source("scripts/r/artometrics_chart_style.R")
#   art_save_modes(art_hbar(labels, values, "Title", "Subtitle", "Source: ..."), "out/chart7", width = 10.4, height = 5.6)

suppressPackageStartupMessages({
  library(ggplot2)
  library(jsonlite)
})

art_style_path <- function(root = getwd()) {
  hit <- file.path(root, "scripts", "charts", "art-chart-style.json")
  if (file.exists(hit)) return(hit)
  stop("art-chart-style.json not found under ", root, ". Run from the repo root.")
}

art_palette <- function(mode = c("light", "dark"), root = getwd()) {
  mode <- match.arg(mode)
  fromJSON(art_style_path(root))[[mode]]
}

theme_art <- function(mode = c("light", "dark"), base_size = 11, root = getwd()) {
  mode <- match.arg(mode)
  p <- art_palette(mode, root)
  theme_minimal(base_size = base_size) +
    theme(
      plot.background = element_rect(fill = p$paper, color = NA),
      panel.background = element_rect(fill = p$paper, color = NA),
      panel.grid.major.x = element_line(color = p$grid, linewidth = 0.3),
      panel.grid.major.y = element_blank(),
      panel.grid.minor = element_blank(),
      axis.text = element_text(color = p$ink),
      axis.title = element_text(color = p$muted),
      plot.title = element_text(color = p$ink, face = "bold", size = rel(1.25)),
      plot.subtitle = element_text(color = p$muted),
      plot.caption = element_text(color = p$muted, hjust = 0, size = rel(0.8)),
      plot.title.position = "plot",
      plot.caption.position = "plot",
      plot.margin = margin(14, 18, 12, 14)
    )
}

# Horizontal bars. `roles` picks a palette role per bar: "red", "blue", "other" or "ink".
art_hbar <- function(labels, values, title, subtitle, source, roles = NULL, fmt = function(v) sprintf("$%.1fB", v)) {
  roles <- if (is.null(roles)) rep("red", length(values)) else roles
  df <- data.frame(label = factor(labels, levels = rev(labels)), value = values, role = roles)
  function(mode = "light", root = getwd()) {
    p <- art_palette(mode, root)
    df$fill <- unlist(lapply(df$role, function(r) p[[r]]))
    ggplot(df, aes(value, label)) +
      geom_col(aes(fill = I(fill)), width = 0.62) +
      geom_text(aes(label = fmt(value)), hjust = -0.15, size = 3.3, color = p$ink) +
      scale_x_continuous(expand = expansion(mult = c(0, 0.3))) +
      labs(title = title, subtitle = subtitle, caption = source, x = NULL, y = NULL) +
      theme_art(mode, root = root)
  }
}

# Writes <stem>.png (light) and <stem>-dark.png (dark).
art_save_modes <- function(chart, stem, width = 10.4, height = 5.6, dpi = 140, root = getwd()) {
  dir.create(dirname(stem), recursive = TRUE, showWarnings = FALSE)
  for (mode in c("light", "dark")) {
    p <- art_palette(mode, root)
    suffix <- if (mode == "dark") "-dark" else ""
    ggsave(paste0(stem, suffix, ".png"), chart(mode, root), width = width, height = height, dpi = dpi,
           device = ragg::agg_png, bg = p$paper)
  }
  invisible(paste0(stem, c("", "-dark"), ".png"))
}
