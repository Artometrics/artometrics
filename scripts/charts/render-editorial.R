#!/usr/bin/env Rscript
# Redraw an article's chart PNGs (light + dark) in the Artometrics editorial style from the Plotly sidecar
# that already ships with the article, so every number stays exactly what the sidecar holds.
#
#   Rscript scripts/charts/render-editorial.R <slug> [chart_stem ...]        # default: every chart the article body uses
#   Rscript scripts/charts/render-editorial.R --all                          # every article (about 2 minutes)
#   Rscript scripts/charts/render-editorial.R --all --editorial              # only charts with a hand-written headline or an override
#
# Headline and subtitle come from scripts/charts/editorial-overrides.json ("slug/chart_stem") when present,
# otherwise from the Plotly title ("Headline<br><span>SUBTITLE</span>"), otherwise from the axis titles.
# Unsupported chart shapes (multi-series bars, heatmaps, radar, pie) are skipped and keep their current PNG.
# Run `node scripts/charts/optimize-pngs.mjs <dir>` afterwards.
suppressPackageStartupMessages({ library(jsonlite); library(stringr) })
source("scripts/r/artometrics_editorial.R")

decode <- function(v) {
  if (is.null(v)) return(NULL)
  if (is.list(v) && !is.null(v$bdata)) {
    raw <- base64_dec(v$bdata)
    spec <- list(f8 = c("double", 8, TRUE), f4 = c("double", 4, TRUE), i1 = c("integer", 1, TRUE), i2 = c("integer", 2, TRUE),
                 i4 = c("integer", 4, TRUE), u1 = c("integer", 1, FALSE), u2 = c("integer", 2, FALSE), i8 = c("double", 8, TRUE))[[v$dtype]]
    if (is.null(spec)) return(NULL)
    return(readBin(raw, what = spec[1], n = length(raw) %/% as.integer(spec[2]), size = as.integer(spec[2]), signed = as.logical(spec[3]), endian = "little"))
  }
  vals <- lapply(v, function(x) if (is.null(x)) NA else x)
  unlist(vals)
}

plain <- function(x) {
  x <- gsub("<br\\s*/?>", "\n", x, ignore.case = TRUE)
  x <- gsub("<[^>]+>", "", x)
  x <- gsub("&amp;", "&", x, fixed = TRUE)
  trimws(x)
}
PROPER <- character()
ACRONYMS <- character()
sentence <- function(x) art_ed_clean_title(gsub("\n", " ", x), proper = PROPER, acronyms = ACRONYMS)

# Words the article always writes with a capital (names, months). Used to restore them in ALL CAPS Plotly titles.
proper_words <- function(slug) {
  md <- file.path("src/content/blog", paste0(slug, ".md"))
  if (!file.exists(md)) return(character())
  txt <- paste(readLines(md, warn = FALSE), collapse = " ")
  txt <- gsub("<[^>]+>", " ", txt)
  w <- unlist(str_extract_all(txt, "[A-Za-z][A-Za-z']+"))
  ACRONYMS <<- unique(unlist(str_extract_all(txt, "\\b[A-Z]{2,6}\\b")))
  cap <- unique(w[grepl("^[A-Z][a-z]", w)])
  lower <- unique(w[grepl("^[a-z]", w)])
  cap[!(tolower(cap) %in% lower)]
}
axis_title <- function(ax) {
  t <- ax$title
  if (is.list(t)) t <- t$text
  if (is.null(t) || !nzchar(t)) NA_character_ else plain(t)
}

headline_parts <- function(layout) {
  t <- layout$title
  if (is.list(t)) t <- t$text
  if (is.null(t)) return(list(head = NA_character_, sub = NA_character_))
  parts <- strsplit(plain(t), "\n")[[1]]
  head <- sentence(parts[1])
  sub <- if (length(parts) > 1) sentence(paste(parts[-1], collapse = " ")) else NA_character_
  if (!is.na(sub)) sub <- sub(" - TidyTuesday.*$", "", sub)
  list(head = head, sub = sub)
}

num_fmt <- function(v) {
  v <- v[is.finite(v)]
  if (!length(v)) return(scales::label_comma())
  if (all(abs(v - round(v)) < 1e-9) && min(v) >= 1800 && max(v) <= 2100) return(scales::label_number(accuracy = 1, big.mark = ""))
  acc <- if (max(abs(v)) >= 20) 0.1 else if (max(abs(v)) >= 2) 0.1 else 0.01
  if (any(abs(v) < 2 & abs(v - round(v)) > 1e-9)) acc <- 0.01
  function(x) ifelse(abs(x - round(x)) < 1e-9, scales::comma(x), scales::number(x, accuracy = acc, big.mark = ","))
}

modal_other <- function(cols, n) {
  if (is.null(cols) || length(cols) != n) return(integer())
  tab <- sort(table(cols), decreasing = TRUE)
  if (length(tab) < 2) return(integer())
  odd <- which(cols != names(tab)[1])
  if (length(odd) <= 3) odd else integer()
}

build_chart <- function(spec, ov_key = NULL) {
  tr <- spec$data
  t1 <- tr[[1]]
  type <- t1$type
  if (is.null(type)) return(NULL)
  mk <- t1$marker
  if (identical(spec$layout$xaxis$type, "log") || identical(spec$layout$yaxis$type, "log")) return(NULL)
  if (type == "bar" && length(tr) == 1) {
    if (identical(t1$orientation, "h")) {
      labels <- as.character(decode(t1$y)); values <- as.numeric(decode(t1$x))
    } else {
      labels <- as.character(decode(t1$x)); values <- as.numeric(decode(t1$y))
    }
    if (!length(values) || length(values) != length(labels)) return(NULL)
    cols <- if (!is.null(mk$color) && length(mk$color) == length(values)) unlist(mk$color) else NULL
    odd <- modal_other(cols, length(values))
    if (is.null(ov_key) || is.null(overrides[[ov_key]])) if (length(unique(values[is.finite(values)])) < 2) return(NULL)
    keep <- is.finite(values)
    labels <- labels[keep]; values <- values[keep]; odd_flag <- seq_along(keep)[keep] %in% odd
    if (identical(t1$orientation, "h")) {
      if (!identical(spec$layout$yaxis$autorange, "reversed")) {
        labels <- rev(labels); values <- rev(values); odd_flag <- rev(odd_flag)
      }
      o <- order(values, decreasing = TRUE)
      labels <- labels[o]; values <- values[o]; odd_flag <- odd_flag[o]
      labels <- labels[seq_len(min(14, length(labels)))]; values <- values[seq_along(labels)]; odd_flag <- odd_flag[seq_along(labels)]
      hi <- which(odd_flag); if (!length(hi)) hi <- 1
      return(list(kind = "bar_h", chart = art_ed_hbar(str_trunc(labels, 26), values, highlight = hi, fmt = num_fmt(values)),
                  sub_default = axis_title(spec$layout$xaxis), n = length(values)))
    }
    if (length(values) > 16 || any(nchar(labels) > 18) || !is.null(t1$base) || max(abs(values), na.rm = TRUE) == 0) return(NULL)
    hi <- which(odd_flag); if (!length(hi)) hi <- which.max(values)
    return(list(kind = "bar_v", chart = art_ed_col(str_trunc(labels, 12), values, highlight = hi, fmt = num_fmt(values), every = ceiling(length(values) / 8)),
                sub_default = axis_title(spec$layout$yaxis), n = length(values)))
  }
  if (type == "scatter" && grepl("lines", t1$mode %||% "")) {
    xs <- list(); gs <- list()
    for (i in seq_len(length(tr))) {
      nm_i <- tr[[i]]$name %||% ""
      if (length(tr) > 1 && (grepl("^Series [0-9]+$", nm_i) || length(decode(tr[[i]]$x)) < 3)) return(NULL)
    }
    if (length(tr) > 6) return(NULL)
    for (i in seq_len(min(6, length(tr)))) {
      x <- decode(tr[[i]]$x); y <- as.numeric(decode(tr[[i]]$y))
      if (is.null(x) || length(x) != length(y)) next
      xn <- suppressWarnings(as.numeric(x))
      if (anyNA(xn)) return(NULL)
      nm <- tr[[i]]$name %||% paste0("s", i)
      xs[[i]] <- data.frame(x = xn, y = y, g = nm)
    }
    df <- do.call(rbind, xs)
    if (is.null(df) || nrow(df) < 3) return(NULL)
    df <- df[is.finite(df$x) & is.finite(df$y), ]
    multi <- length(unique(df$g)) > 1
    return(list(kind = "line", chart = art_ed_line(df$x, df$y, group = if (multi) df$g else NULL, fmt = num_fmt(df$y), lfmt = num_fmt(df$y)),
                sub_default = axis_title(spec$layout$yaxis), n = nrow(df)))
  }
  if (type %in% c("scatter", "scattergl") && grepl("markers", t1$mode %||% "")) {
    x <- as.numeric(decode(t1$x)); y <- as.numeric(decode(t1$y))
    if (length(x) != length(y) || sum(is.finite(x) & is.finite(y)) < 3) return(NULL)
    txt <- if (!is.null(t1$text)) as.character(decode(t1$text)) else NULL
    only <- unlist(overrides[[ov_key %||% ""]]$label_only)
    if (!is.null(txt) && (length(txt) != length(x) || any(grepl("<|=", txt), na.rm = TRUE) || any(nchar(txt) > 30, na.rm = TRUE))) txt <- NULL
    ok <- is.finite(x) & is.finite(y)
    hi <- integer(); lab <- NULL
    if (!is.null(txt)) {
      pick <- which(ok & !is.na(txt) & nzchar(txt))
      if (length(only)) pick <- pick[txt[pick] %in% only]
      sc <- function(v) abs(v - median(v[ok])) / (mad(v[ok]) + 1e-9)
      if (!length(only)) pick <- head(pick[order(-(sc(x)[pick] + sc(y)[pick]))], 6)
      hi <- pick; lab <- txt
    }
    return(list(kind = "scatter", chart = art_ed_scatter(x[ok], y[ok], label = if (is.null(lab)) NULL else lab[ok], highlight = match(hi, which(ok)), xfmt = num_fmt(x), yfmt = num_fmt(y)),
                sub_default = paste(na.omit(c(axis_title(spec$layout$yaxis), axis_title(spec$layout$xaxis))), collapse = " by "), n = sum(ok)))
  }
  if (type == "box") {
    vals <- list(); grp <- list()
    for (i in seq_len(min(10, length(tr)))) {
      v <- as.numeric(decode(tr[[i]]$y %||% tr[[i]]$x)); nm <- tr[[i]]$name %||% paste0("g", i)
      v <- v[is.finite(v)]; if (!length(v)) next
      vals[[i]] <- v; grp[[i]] <- rep(str_trunc(nm, 22), length(v))
    }
    if (!length(vals)) return(NULL)
    values <- unlist(vals); groups <- unlist(grp)
    meds <- tapply(values, groups, median)
    ord <- names(sort(meds, decreasing = TRUE))
    groups <- factor(groups, levels = ord)
    return(list(kind = "box", chart = art_ed_box(values, as.character(groups), highlight = ord[1], fmt = num_fmt(values)),
                sub_default = "Distribution by group. Box shows the middle half; the line is the median.", n = length(values)))
  }
  if (type == "histogram") {
    return(NULL)
    x <- as.numeric(decode(t1$x)); x <- x[is.finite(x)]
    if (length(x) < 5) return(NULL)
    h <- hist(x, plot = FALSE, breaks = "FD")
    return(list(kind = "hist", chart = art_ed_hist(h$mids, h$counts, highlight = which.max(h$counts)), sub_default = paste0("Number of records by ", tolower(axis_title(spec$layout$xaxis) %||% "value")), n = length(x)))
  }
  NULL
}

`%||%` <- function(a, b) if (is.null(a) || (length(a) == 1 && is.na(a))) b else a

overrides <- if (file.exists("scripts/charts/editorial-overrides.json")) fromJSON("scripts/charts/editorial-overrides.json", simplifyVector = FALSE) else list()

source_for <- function(slug, stem) {
  md <- file.path("src/content/blog", paste0(slug, ".md"))
  if (!file.exists(md)) return(NULL)
  txt <- paste(readLines(md, warn = FALSE), collapse = "\n")
  m <- str_match(txt, paste0('data-source="([^"]*)"[^>]*', stem, "\\.png"))[, 2]
  if (is.na(m)) m <- str_match(txt, 'data-source="([^"]*)"')[, 2]
  if (is.na(m)) return(NULL)
  m <- sub(" - ARTOMETRICS$", "", m)
  sub("^Data: ", "Source: ", m)
}

GENERIC <- "^(leaders (by|tracking)|how .* splits|concentration of|above or below|boxplot|distribution of|top .* by median|median .* over time|where .* concentrat)"
EDITORIAL_ONLY <- FALSE
is_editorial <- function(spec, key) {
  if (!is.null(overrides[[key]])) return(TRUE)
  t <- spec$layout$title
  if (is.list(t)) t <- t$text
  if (is.null(t) || !grepl("<br", t, ignore.case = TRUE)) return(FALSE)
  parts <- strsplit(plain(t), "\n")[[1]]
  head_ok <- !grepl(GENERIC, tolower(parts[1]))
  sub_pat <- paste0("^(joint distribution|over time|pareto curve|scatter field|structural slope|interquartile view|",
                    "trend with milestones.*|trend line.*|colored by category|summary view|ranked bar|period or category bar|by .*|.* on top|.* leads)$")
  sub_ok <- length(parts) < 2 || !grepl(sub_pat, tolower(parts[2]))
  head_ok && sub_ok
}

render_one <- function(slug, stem) {
  PROPER <<- proper_words(slug)
  json <- file.path("public/data/articles", slug, "charts", paste0(stem, ".plotly.json"))
  if (!file.exists(json)) return(FALSE)
  spec <- tryCatch(fromJSON(json, simplifyVector = FALSE), error = function(e) NULL)
  if (is.null(spec)) return(FALSE)
  if (EDITORIAL_ONLY && !is_editorial(spec, paste0(slug, "/", stem))) return(FALSE)
  built <- tryCatch(build_chart(spec, paste0(slug, "/", stem)), error = function(e) { message("  ! ", slug, "/", stem, ": ", conditionMessage(e)); NULL })
  if (is.null(built)) { message("  skip ", slug, "/", stem); return(FALSE) }
  key <- paste0(slug, "/", stem)
  ov <- overrides[[key]]
  hp <- headline_parts(spec$layout)
  headline <- ov$headline %||% hp$head %||% stem
  subtitle <- ov$subtitle %||% hp$sub %||% built$sub_default
  src <- ov$source %||% source_for(slug, stem)
  out <- file.path("public/images/content/articles", slug, "charts", stem)
  if (!dir.exists(dirname(out))) return(FALSE)
  ok <- tryCatch({
    height <- if (built$kind == "bar_h") min(6.8, max(4.4, 3.4 + 0.34 * built$n)) else 6.6
    art_ed_save(built$chart, out, headline = headline, subtitle = subtitle, source = src, height = height)
    TRUE
  }, error = function(e) { graphics.off(); message("  ! ", key, ": ", conditionMessage(e)); FALSE })
  if (ok) message("  ok   ", key, "  (", built$kind, ")")
  ok
}

used_stems <- function(slug) {
  md <- file.path("src/content/blog", paste0(slug, ".md"))
  txt <- paste(readLines(md, warn = FALSE), collapse = "\n")
  unique(str_match_all(txt, paste0("/images/content/articles/", slug, "/charts/([A-Za-z0-9_\\-]+)\\.png"))[[1]][, 2])
}

args <- commandArgs(trailingOnly = TRUE)
if ("--editorial" %in% args) { EDITORIAL_ONLY <- TRUE; args <- setdiff(args, "--editorial") }
if (!length(args)) stop("usage: render-editorial.R <slug> [chart_stem ...] | --all")
slugs <- if (args[1] == "--all") sub("\\.md$", "", list.files("src/content/blog", pattern = "\\.md$")) else args[1]
done <- 0
for (slug in slugs) {
  stems <- if (length(args) > 1 && args[1] != "--all") args[-1] else used_stems(slug)
  stems <- stems[!grepl("-dark$", stems)]
  for (stem in stems) done <- done + render_one(slug, stem)
}
message("rendered ", done, " chart(s)")
