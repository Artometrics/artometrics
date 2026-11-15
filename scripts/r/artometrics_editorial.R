# Artometrics editorial chart style.
#
# Original house look, in the tradition of newspaper data desks: warm paper, one loud highlight,
# a pink flag top-left, a bold headline and a plain-language subtitle ON the chart, direct value
# labels instead of legends, thin horizontal rules, and type big enough to read at 340px wide.
#
# Tokens come from scripts/charts/art-chart-style.json (light and dark). Fonts come from assets/fonts.
#
#   source("scripts/r/artometrics_editorial.R")
#   art_ed_save(
#     art_ed_hbar(c("A", "B", "C"), c(3, 7, 5), highlight = 2, fmt = scales::label_comma()),
#     "out/chart", headline = "B is more than twice A", subtitle = "Median score by group",
#     source = "Source: Example Survey, 2024"
#   )
#
# art_ed_save() writes <stem>.png (light) and <stem>-dark.png (dark).

suppressPackageStartupMessages({
  library(ggplot2)
  library(jsonlite)
  library(ggtext)
  library(grid)
})

ART_ED_ROOT <- getwd()

art_ed_palette <- function(mode = c("light", "dark"), root = ART_ED_ROOT) {
  mode <- match.arg(mode)
  fromJSON(file.path(root, "scripts", "charts", "art-chart-style.json"))[[mode]]
}

art_ed_fonts <- local({
  done <- FALSE
  function(root = ART_ED_ROOT) {
    if (done) return(invisible(TRUE))
    reg <- function(name, file) {
      path <- file.path(root, "assets", "fonts", file)
      if (file.exists(path)) systemfonts::register_font(name, plain = path)
    }
    reg("Art Anton", "Anton-Regular.ttf")
    reg("Art Sans", "DMSans.ttf")
    reg("Art Mono", "DMMono-Regular.ttf")
    done <<- TRUE
    invisible(TRUE)
  }
})

ART_ED_HEAD <- "Art Anton"
ART_ED_BODY <- "Art Sans"
ART_ED_MONO <- "Art Mono"

# Sentence-case an ALL CAPS label and strip Plotly markup.
art_ed_short_words_unused <- c("a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "has", "had", "her", "his", "how", "if", "in",
  "is", "it", "its", "not", "of", "on", "or", "our", "out", "so", "the", "to", "up", "was", "we", "who", "why", "you", "vs", "per", "all",
  "can", "did", "get", "got", "may", "now", "off", "one", "two", "yet", "than", "that", "then", "this", "with", "over", "into", "when")

# Sentence-case an ALL CAPS label and strip Plotly markup. `proper` lists words that should keep a capital
# (taken from the article text), so "OCTOBER" becomes "October" and "FIRST" becomes "first".
art_ed_clean_title <- function(x, proper = character(), acronyms = character()) {
  x <- gsub("<br\\s*/?>", " \u2014 ", x, ignore.case = TRUE)
  x <- gsub("<[^>]+>", "", x)
  x <- gsub("&amp;", "&", x, fixed = TRUE)
  x <- trimws(gsub("\\s+", " ", x))
  letters_only <- gsub("[^A-Za-z]", "", x)
  if (nchar(letters_only) > 6 && sum(grepl("[A-Z]", strsplit(letters_only, "")[[1]])) / nchar(letters_only) > 0.8) {
    words <- strsplit(x, " ")[[1]]
    core <- gsub("[^A-Za-z]", "", words)
    low <- tolower(words)
    keep <- grepl("[0-9]", words) | (core %in% acronyms) | (nchar(core) <= 3 & nchar(core) > 0 & (core %in% c("US", "UK", "EU", "UN", "TV", "AI")))
    low[keep] <- words[keep]
    hit <- tolower(core) %in% tolower(proper) & !keep
    low[hit] <- paste0(toupper(substr(words[hit], 1, 1)), tolower(substr(words[hit], 2, nchar(words[hit]))))
    x <- paste(low, collapse = " ")
    x <- paste0(toupper(substr(x, 1, 1)), substr(x, 2, nchar(x)))
  }
  x
}

theme_art_ed <- function(mode = "light", base = 14, root = ART_ED_ROOT) {
  art_ed_fonts(root)
  p <- art_ed_palette(mode, root)
  theme_minimal(base_size = base, base_family = ART_ED_BODY) +
    theme(
      text = element_text(color = p$ink, family = ART_ED_BODY),
      plot.background = element_rect(fill = p$paper, color = NA),
      panel.background = element_rect(fill = p$paper, color = NA),
      panel.grid.major.y = element_line(color = p$grid, linewidth = 0.45),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      axis.text = element_text(color = p$muted, size = rel(0.92)),
      axis.text.y = element_text(color = p$ink),
      axis.title = element_blank(),
      axis.ticks = element_blank(),
      axis.line.x = element_line(color = p$ink, linewidth = 0.6),
      legend.position = "none",
      plot.title.position = "plot",
      plot.caption.position = "plot",
      plot.title = element_text(
        family = ART_ED_HEAD, size = rel(1.9), color = p$ink, lineheight = 1.08, hjust = 0, vjust = 1,
        margin = margin(t = 22, b = 10)
      ),
      plot.subtitle = element_textbox_simple(
        family = ART_ED_BODY, size = rel(1.02), color = p$muted, lineheight = 1.25,
        width = unit(1, "npc"), margin = margin(b = 14)
      ),
      plot.caption = element_textbox_simple(
        family = ART_ED_MONO, size = rel(0.7), color = p$muted, lineheight = 1.3,
        width = unit(1, "npc"), margin = margin(t = 14)
      ),
      plot.margin = margin(14, 22, 14, 22)
    )
}

art_ed_fill <- function(n, highlight, mode, root = ART_ED_ROOT) {
  p <- art_ed_palette(mode, root)
  fills <- rep(p$other, n)
  if (length(highlight)) fills[highlight] <- p$red
  fills
}

# Horizontal bars in the order given (first on top). `highlight` is a vector of positions.
art_ed_hbar <- function(labels, values, highlight = integer(), fmt = scales::label_comma(), expand = 0.22) {
  force(labels); force(values); force(highlight); force(fmt)
  function(mode = "light", root = ART_ED_ROOT) {
    art_ed_fonts(root)
    p <- art_ed_palette(mode, root)
    shown <- values
    mixed <- any(values < 0) && any(values > 0)
    if (all(values <= 0)) values <- abs(values)
    df <- data.frame(label = factor(labels, levels = rev(labels)), value = values, shown = shown)
    df$fill <- rev(art_ed_fill(nrow(df), if (length(highlight)) nrow(df) + 1 - highlight else integer(), mode, root))
    base <- 14
    ggplot(df, aes(value, label)) +
      geom_col(aes(fill = I(fill)), width = 0.66) +
      geom_text(aes(label = fmt(shown), hjust = if (mixed) ifelse(value >= 0, -0.12, 1.12) else -0.12),
                size = base * 0.3, family = ART_ED_HEAD, color = p$ink) +
      { if (mixed) geom_vline(xintercept = 0, color = p$ink, linewidth = 0.5) } +
      scale_x_continuous(expand = expansion(mult = if (mixed) c(0.18, expand) else c(0, expand))) +
      theme_art_ed(mode, base, root) +
      theme(
        panel.grid.major.y = element_blank(),
        panel.grid.major.x = element_blank(),
        axis.text.x = element_blank(),
        axis.line.x = element_blank(),
        axis.text.y = element_text(color = p$ink, size = rel(1.0))
      )
  }
}

# Vertical columns with an optional highlight. Use for few categories or ordered time bins.
art_ed_col <- function(labels, values, highlight = integer(), fmt = scales::label_comma(), show_values = TRUE, every = 1) {
  force(labels); force(values); force(highlight); force(fmt)
  function(mode = "light", root = ART_ED_ROOT) {
    art_ed_fonts(root)
    p <- art_ed_palette(mode, root)
    df <- data.frame(label = factor(labels, levels = unique(labels)), value = values)
    df$fill <- art_ed_fill(nrow(df), highlight, mode, root)
    base <- 14
    brks <- levels(df$label)[seq(1, nlevels(df$label), by = every)]
    g <- ggplot(df, aes(label, value)) +
      geom_col(aes(fill = I(fill)), width = 0.72) +
      scale_x_discrete(breaks = brks) +
      scale_y_continuous(expand = expansion(mult = c(0, 0.12)), labels = fmt) +
      theme_art_ed(mode, base, root)
    if (show_values) {
      g <- g + geom_text(aes(label = fmt(value)), vjust = -0.45, size = base * 0.28, family = ART_ED_HEAD, color = p$ink)
    }
    g
  }
}

# One or more lines. `x`, `y` numeric; `group` optional. The last point of each line is labelled directly.
art_ed_line <- function(x, y, group = NULL, highlight = NULL, fmt = scales::label_comma(), label_last = TRUE, points = FALSE, xbreaks = NULL, notes = NULL, lfmt = NULL) {
  if (is.null(lfmt)) lfmt <- fmt
  force(x); force(y); force(group); force(highlight); force(fmt); force(notes)
  function(mode = "light", root = ART_ED_ROOT) {
    art_ed_fonts(root)
    p <- art_ed_palette(mode, root)
    df <- data.frame(x = x, y = y, g = if (is.null(group)) "all" else group)
    groups <- unique(df$g)
    cols <- setNames(rep(p$other, length(groups)), groups)
    hi <- if (is.null(highlight)) groups[1] else highlight
    cols[hi] <- p$red
    if (length(groups) > 1 && length(hi) == 1) cols[setdiff(groups, hi)[1]] <- p$blue
    base <- 14
    g <- ggplot(df, aes(x, y, color = g, group = g)) +
      geom_line(linewidth = 1.5, lineend = "round") +
      scale_color_manual(values = cols) +
      scale_y_continuous(labels = fmt, expand = expansion(mult = c(0.04, 0.16))) +
      scale_x_continuous(breaks = if (is.null(xbreaks)) scales::breaks_pretty(5) else xbreaks, labels = if (all(df$x >= 1800 & df$x <= 2100)) function(v) format(v, big.mark = "", trim = TRUE) else waiver(), expand = expansion(mult = c(0.02, if (length(groups) > 1) 0.24 else 0.1))) +
      theme_art_ed(mode, base, root)
    if (points) g <- g + geom_point(size = 2.6)
    if (!is.null(notes)) {
      g <- g + geom_point(data = notes, aes(x, y), inherit.aes = FALSE, color = p$ink, size = 2.6) +
        geom_text(data = notes, aes(x, y, label = label, hjust = hj), inherit.aes = FALSE, vjust = -0.6,
                  size = base * 0.3, family = ART_ED_HEAD, color = p$ink, lineheight = 0.9)
    }
    if (label_last) {
      last <- do.call(rbind, lapply(split(df, df$g), function(d) d[which.max(d$x), ]))
      if (length(groups) > 1) {
        g <- g + ggrepel::geom_text_repel(
          data = transform(last, g = ifelse(nchar(g) > 13, paste0(substr(g, 1, 12), "\u2026"), g)), aes(label = g), direction = "y", hjust = 0, nudge_x = diff(range(df$x)) * 0.02, point.size = NA,
          size = base * 0.27, family = ART_ED_BODY, segment.color = NA, show.legend = FALSE, xlim = c(NA, Inf)
        )
      } else {
        g <- g + geom_point(data = last, size = 3.4) +
          geom_text(data = last, aes(label = lfmt(y)), hjust = -0.25, vjust = 0.4, size = base * 0.3, family = ART_ED_HEAD, color = p$ink, show.legend = FALSE)
      }
    }
    g
  }
}

# Scatter. `label` marks points to name directly (others stay unlabelled); `highlight` colours points.
art_ed_scatter <- function(x, y, label = NULL, highlight = integer(), xfmt = scales::label_comma(), yfmt = scales::label_comma(), alpha = 0.55) {
  force(x); force(y); force(label); force(highlight)
  function(mode = "light", root = ART_ED_ROOT) {
    art_ed_fonts(root)
    p <- art_ed_palette(mode, root)
    df <- data.frame(x = x, y = y, lab = if (is.null(label)) NA_character_ else label)
    df$hi <- seq_len(nrow(df)) %in% highlight
    base <- 14
    g <- ggplot(df, aes(x, y)) +
      geom_point(data = df[!df$hi, ], color = p$other, alpha = alpha, size = if (nrow(df) > 400) 1.4 else 3.2, stroke = 0) +
      geom_point(data = df[df$hi, ], color = p$red, size = 4, stroke = 0) +
      scale_x_continuous(labels = xfmt, breaks = scales::breaks_pretty(5)) +
      scale_y_continuous(labels = yfmt, breaks = scales::breaks_pretty(5)) +
      theme_art_ed(mode, base, root)
    named <- df[df$hi & !is.na(df$lab), ]
    if (nrow(named)) {
      g <- g + ggrepel::geom_text_repel(
        data = named, aes(label = lab), size = base * 0.27, family = ART_ED_BODY, color = p$ink,
        min.segment.length = 0, segment.color = p$muted, box.padding = 0.6, max.overlaps = Inf
      )
    }
    g
  }
}

# Histogram of precomputed bins: `mids` and `counts`.
art_ed_hist <- function(mids, counts, highlight = integer(), fmt = scales::label_comma()) {
  force(mids); force(counts)
  function(mode = "light", root = ART_ED_ROOT) {
    art_ed_fonts(root)
    p <- art_ed_palette(mode, root)
    df <- data.frame(x = mids, n = counts)
    width <- if (nrow(df) > 1) min(diff(sort(df$x))) * 0.92 else 1
    base <- 14
    ggplot(df, aes(x, n)) +
      geom_col(aes(fill = I(art_ed_fill(nrow(df), highlight, mode, root))), width = width) +
      scale_x_continuous(breaks = scales::breaks_pretty(6)) +
      scale_y_continuous(labels = fmt, expand = expansion(mult = c(0, 0.08))) +
      theme_art_ed(mode, base, root)
  }
}

# Distribution per group as horizontal boxes. `values` and `groups` are parallel vectors.
art_ed_box <- function(values, groups, highlight = character(), fmt = scales::label_number(accuracy = 0.1)) {
  force(values); force(groups); force(highlight)
  function(mode = "light", root = ART_ED_ROOT) {
    art_ed_fonts(root)
    p <- art_ed_palette(mode, root)
    df <- data.frame(v = values, g = factor(groups, levels = rev(unique(groups))))
    fills <- setNames(rep(p$other, nlevels(df$g)), levels(df$g))
    if (length(highlight)) fills[highlight] <- p$red
    base <- 14
    ggplot(df, aes(v, g, fill = g)) +
      geom_boxplot(width = 0.55, color = p$ink, linewidth = 0.5, outlier.size = 1, outlier.alpha = 0.35, outlier.color = p$muted, alpha = 0.9) +
      scale_fill_manual(values = fills) +
      scale_x_continuous(labels = fmt, breaks = scales::breaks_pretty(5)) +
      theme_art_ed(mode, base, root) +
      theme(panel.grid.major.x = element_line(color = p$grid, linewidth = 0.45), panel.grid.major.y = element_blank(),
            axis.text.y = element_text(color = p$ink), axis.line.x = element_blank())
  }
}

# Balanced line breaks for the headline, so no line is a single stranded word.
art_ed_wrap <- function(x, max_chars = 30) {
  n <- ceiling(nchar(x) / max_chars)
  if (n <= 1) return(x)
  for (w in seq(ceiling(nchar(x) / n), nchar(x))) {
    lines <- strwrap(x, width = w)
    if (length(lines) <= n) return(paste(lines, collapse = "\n"))
  }
  x
}

# Adds the headline, subtitle and source to a chart and saves light + dark PNGs with the pink flag.
art_ed_save <- function(chart, stem, headline, subtitle = NULL, source = NULL,
                        width = 6.4, height = 6.6, dpi = 220, root = ART_ED_ROOT, modes = c("light", "dark")) {
  dir.create(dirname(stem), recursive = TRUE, showWarnings = FALSE)
  out <- character()
  for (mode in modes) {
    p <- art_ed_palette(mode, root)
    gg <- chart(mode, root) +
      labs(title = art_ed_wrap(headline), subtitle = subtitle, caption = if (is.null(source)) NULL else paste0(source, "  \u00b7  ARTOMETRICS"))
    file <- paste0(stem, if (mode == "dark") "-dark" else "", ".png")
    ragg::agg_png(file, width = width, height = height, units = "in", res = dpi, background = p$paper)
    grid.newpage()
    grid.draw(ggplotGrob(gg))
    grid.rect(x = unit(22 / (width * 72), "npc"), y = unit(1, "npc"), width = unit(54, "pt"), height = unit(9, "pt"),
              just = c("left", "top"), gp = gpar(fill = p$red, col = NA))
    dev.off()
    out <- c(out, file)
  }
  invisible(out)
}

# Minimal Plotly JSON sidecar so the numbers behind a chart ship with it. kind: "bar_h", "bar" or "line".
art_ed_sidecar <- function(file, kind, x, y, title, xtitle = "", ytitle = "", highlight = integer()) {
  dir.create(dirname(file), recursive = TRUE, showWarnings = FALSE)
  col <- rep("#8a8178", length(x))
  if (length(highlight)) col[highlight] <- "#ff3d8a"
  trace <- switch(kind,
    bar_h = list(type = "bar", orientation = "h", x = as.list(y), y = as.list(x), marker = list(color = as.list(col))),
    bar = list(type = "bar", x = as.list(x), y = as.list(y), marker = list(color = as.list(col))),
    line = list(type = "scatter", mode = "lines", x = as.list(x), y = as.list(y), line = list(color = "#ff3d8a", width = 3))
  )
  spec <- list(
    data = list(trace),
    layout = list(
      title = list(text = title), paper_bgcolor = "#f7f4ee", plot_bgcolor = "#f7f4ee",
      font = list(family = "DM Sans, sans-serif", color = "#14110e"),
      xaxis = list(title = list(text = xtitle)), yaxis = list(title = list(text = ytitle), autorange = if (kind == "bar_h") "reversed" else TRUE)
    )
  )
  writeLines(toJSON(spec, auto_unbox = TRUE, null = "null", digits = NA), file)
  invisible(file)
}
