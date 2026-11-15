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
  sub <- if (length(parts) > 1) sentence(paste(vapply(parts[-1], function(z) if (grepl("[.!?:;]$", z)) z else paste0(z, "."), ""), collapse = " ")) else NA_character_
  if (!is.na(sub)) sub <- sub(" - TidyTuesday.*$", "", sub)
  if (!is.na(sub)) {
    segs <- strsplit(sub, "(?<=[.;\u00b7]) ", perl = TRUE)[[1]]
    segs <- segs[!grepl("(dashed|dotted|band|shaded|ribbon|annotat|bubble size)", segs, ignore.case = TRUE) & !grepl("^.{0,60} (lead|leads|lowest)\\.?$", segs, ignore.case = TRUE)]
    sub <- if (length(segs)) trimws(sub("[\\s·;,]+$", "", paste(segs, collapse = " "))) else NA_character_
  }
  list(head = head, sub = sub)
}

num_fmt <- function(v) {
  v <- v[is.finite(v)]
  if (!length(v)) return(scales::label_comma())
  if (all(abs(v - round(v)) < 1e-9) && min(v) >= 1800 && max(v) <= 2100) return(scales::label_number(accuracy = 1, big.mark = ""))
  acc <- if (max(abs(v)) >= 20) 0.1 else if (max(abs(v)) >= 2) 0.1 else 0.01
  if (any(abs(v) < 2 & abs(v - round(v)) > 1e-9)) acc <- 0.01
  if (max(abs(v)) >= 1e6) return(function(x) {
    a <- abs(x)
    ifelse(a >= 1e9, paste0(scales::number(x / 1e9, accuracy = 0.1), "B"),
           ifelse(a >= 1e6, paste0(scales::number(x / 1e6, accuracy = 0.1), "M"), scales::comma(x, accuracy = 1)))
  })
  function(x) ifelse(abs(x - round(x)) < 1e-9, scales::comma(x), scales::number(x, accuracy = acc, big.mark = ","))
}

modal_other <- function(cols, n) {
  if (is.null(cols) || length(cols) != n) return(integer())
  tab <- sort(table(cols), decreasing = TRUE)
  if (length(tab) < 2) return(integer())
  odd <- which(cols != names(tab)[1])
  if (length(odd) <= 3) odd else integer()
}


fnum <- function(f, v) trimws(as.character(f(v)))
year_fmt <- function(v) {
  v <- v[is.finite(v)]
  if (length(v) && all(abs(v - round(v)) < 1e-9) && min(v) >= 1000 && max(v) <= 2100) scales::label_number(accuracy = 1, big.mark = "") else num_fmt(v)
}
# Axis names used mid-sentence: lower-case the first letter unless it starts an acronym or a proper noun.
mid <- function(x) {
  if (is.na(x)) return(x)
  x <- sentence(x)
  if (!grepl(" ", x) && !(tolower(x) %in% tolower(PROPER))) x <- gsub("([a-z])([A-Z])", "\\1 \\L\\2", x, perl = TRUE)
  first <- strsplit(x, " ")[[1]][1]
  if (first %in% ACRONYMS || first %in% PROPER || grepl("^[A-Z]{2,}", first) || grepl("[A-Z]", substr(first, 2, nchar(first)))) x else paste0(tolower(substr(x, 1, 1)), substr(x, 2, nchar(x)))
}
join_sentence <- function(...) {
  parts <- Filter(function(z) !is.null(z) && !is.na(z) && nzchar(z), list(...))
  parts <- vapply(parts, function(z) if (grepl("[.!?]$", z)) z else paste0(z, "."), "")
  paste(parts, collapse = " ")
}

# Headlines derived from the plotted numbers themselves, so nothing is written by hand and nothing can drift from the data.
derive_bar <- function(labels, values, fmt, periods = FALSE) {
  n <- length(values); o <- order(values, decreasing = TRUE); L <- labels[o]; V <- values[o]
  f <- function(v) fnum(fmt, v)
  if (n >= 2 && min(V) < 0 && max(V) > 0) {
    head <- sprintf("%s is highest at %s and %s lowest at %s", L[1], f(V[1]), L[n], f(V[n]))
    return(list(head = head, sub = sprintf("%d bars, centred on zero.", n)))
  }
  if (n >= 2 && V[1] == V[2]) {
    k <- sum(V == V[1])
    head <- if (k == n) sprintf("All %d bars read %s", n, f(V[1])) else sprintf("%d of %d bars tie at the top, at %s", k, n, f(V[1]))
  } else if (n >= 2 && V[2] > 0 && V[1] > 0 && V[1] / V[2] >= 1.5) {
    head <- sprintf("%s leads at %s, %.1f times the next", L[1], f(V[1]), V[1] / V[2])
  } else if (periods) {
    head <- sprintf("%s is the peak at %s", L[1], f(V[1]))
  } else {
    head <- sprintf("%s leads at %s", L[1], f(V[1]))
  }
  low <- if (n >= 2 && V[n] != V[1]) sprintf("%s is lowest of the %d shown, at %s", L[n], n, f(V[n])) else NULL
  list(head = head, sub = low)
}

derive_line <- function(df, fmt, xfmt) {
  f <- function(v) fnum(fmt, v); fx <- function(v) fnum(xfmt, v)
  df <- df[order(df$g, df$x), ]
  if (length(unique(df$g)) == 1) {
    n <- nrow(df); first <- df[1, ]; last <- df[n, ]; pk <- which.max(df$y); rng <- diff(range(df$y))
    interior <- pk > 1 && pk < n && rng > 0 && (df$y[pk] - max(first$y, last$y)) / rng > 0.15
    head <- if (interior) sprintf("Peaked at %s in %s, ended at %s", f(df$y[pk]), fx(df$x[pk]), f(last$y))
            else sprintf("%s from %s in %s to %s in %s", if (last$y > first$y) "Up" else if (last$y < first$y) "Down" else "Flat", f(first$y), fx(first$x), f(last$y), fx(last$x))
    ch <- if (first$y != 0 && is.finite(first$y)) (last$y / first$y - 1) * 100 else NA
    sub <- if (!is.na(ch) && abs(ch) >= 1 && !interior) sprintf("%s%.0f%% across the %d points plotted", if (ch > 0) "+" else "-", abs(ch), n) else sprintf("%d points plotted", n)
    return(list(head = head, sub = sub))
  }
  ends <- do.call(rbind, lapply(split(df, df$g), function(d) d[which.max(d$x), ]))
  ends <- ends[order(ends$y, decreasing = TRUE), ]
  k <- nrow(ends)
  head <- sprintf("%s ends highest at %s in %s", ends$g[1], f(ends$y[1]), fx(ends$x[1]))
  sub <- sprintf("%s ends lowest, at %s. %d series", ends$g[k], f(ends$y[k]), k)
  list(head = head, sub = sub)
}

derive_scatter <- function(x, y, xname, yname) {
  ok <- is.finite(x) & is.finite(y); x <- x[ok]; y <- y[ok]
  rho <- suppressWarnings(cor(x, y, method = "spearman"))
  if (!is.finite(rho)) return(NULL)
  yn <- if (is.na(yname)) "The vertical measure" else sentence(yname)
  xn <- if (is.na(xname)) "the horizontal one" else xname
  yl <- if (is.na(yname)) "the vertical measure" else mid(yname)
  head <- if (rho >= 0.6) sprintf("%s climbs with %s", yn, xn)
          else if (rho <= -0.6) sprintf("%s falls as %s rises", yn, xn)
          else if (abs(rho) >= 0.3) sprintf("%s and %s are only loosely linked", yn, xn)
          else sprintf("%s tells little about %s", sub("^(.)", "\\U\\1", xn, perl = TRUE), yl)
  list(head = head, sub = sprintf("Spearman rank correlation %.2f across %s points", rho, format(length(x), big.mark = ",")))
}

derive_box <- function(values, groups, fmt) {
  meds <- sort(tapply(values, groups, median), decreasing = TRUE)
  k <- length(meds); f <- function(v) fnum(fmt, v)
  head <- if (k >= 2) sprintf("%s has the highest median, at %s", names(meds)[1], f(meds[1])) else sprintf("Median %s", f(meds[1]))
  list(head = head, sub = if (k >= 2) sprintf("%s is lowest, at %s. Box = middle half; line = median", names(meds)[k], f(meds[k])) else "Box = middle half; line = median")
}

num_labels <- function(v) {
  v <- v[is.finite(v)]
  function(x) vapply(x, function(z) format(signif(z, 3), big.mark = ",", trim = TRUE, scientific = FALSE), "")
}

derive_dist <- function(mids, counts, xf) {
  tot <- sum(counts); pk <- which.max(counts)
  head <- sprintf("The busiest bin, around %s, holds %.0f%% of the total", fnum(xf, mids[pk]), 100 * counts[pk] / tot)
  list(head = head, sub = sprintf("%d bins, from about %s to %s", length(mids), fnum(xf, min(mids)), fnum(xf, max(mids))))
}

derive_grouped <- function(cats, series, values, stacked, fmt) {
  f <- function(v) fnum(fmt, v)
  if (stacked) {
    tot <- tapply(values, factor(cats, levels = unique(cats)), sum)
    top <- names(which.max(tot))
    return(list(head = sprintf("%s has the largest total, at %s", top, f(max(tot))),
                sub = sprintf("%d series stacked across %d categories", length(unique(series)), length(unique(cats)))))
  }
  i <- which.max(values); j <- which.min(values)
  list(head = sprintf("%s peaks at %s in %s", series[i], f(values[i]), cats[i]),
       sub = sprintf("Lowest bar: %s in %s, at %s. %d series across %d categories", series[j], cats[j], f(values[j]), length(unique(series)), length(unique(cats))))
}

derive_heat <- function(rows, cols, values, fmt) {
  i <- which.max(values); j <- which.min(values); f <- function(v) fnum(fmt, v)
  list(head = sprintf("%s on %s is the highest cell, at %s", rows[i], cols[i], f(values[i])),
       sub = sprintf("Lowest: %s on %s, at %s. %d rows by %d columns", rows[j], cols[j], f(values[j]), length(unique(rows)), length(unique(cols))))
}

derive_line_cat <- function(df, fmt, labs) {
  f <- function(v) fnum(fmt, v)
  i <- which.max(df$y); j <- which.min(df$y); multi <- length(unique(df$g)) > 1
  head <- if (multi) sprintf("%s peaks at %s in %s", df$g[i], f(df$y[i]), labs[df$x[i]]) else sprintf("%s is highest at %s", labs[df$x[i]], f(df$y[i]))
  sub <- if (multi) sprintf("Lowest point: %s in %s, at %s. %d series", df$g[j], labs[df$x[j]], f(df$y[j]), length(unique(df$g))) else sprintf("%s is lowest, at %s", labs[df$x[j]], f(df$y[j]))
  list(head = head, sub = sub)
}

tidy_labels <- function(l) {
  l <- gsub(",(?=[^ ,0-9])", ", ", l, perl = TRUE)
  n <- suppressWarnings(as.numeric(l))
  if (anyNA(n) || all(abs(n - round(n)) < 1e-9)) return(l)
  for (d in 3:6) { r <- signif(n, d); if (!anyDuplicated(r) || anyDuplicated(n)) return(as.character(r)) }
  l
}

# Bars that carry their own label text (e.g. "$130.7B") keep it, so units survive into the value labels and headline.
text_fmt <- function(txt, values) {
  if (is.null(txt)) return(NULL)
  txt <- unlist(txt)
  if (!is.character(txt) || length(txt) != length(values) || any(!grepl("[0-9]", txt))) return(NULL)
  key <- function(v) format(v, digits = 10)
  lut <- setNames(trimws(txt), key(values))
  function(v) { out <- unname(lut[key(v)]); ifelse(is.na(out), scales::comma(v), out) }
}

make_hbar <- function(labels, values, spec, hi = NULL, total = length(values), txt = NULL) {
  vf <- text_fmt(txt, values); if (is.null(vf)) vf <- num_fmt(values)
  o <- order(values, decreasing = TRUE)
  full <- labels[o]
  labels <- make.unique(str_trunc(labels[o], 26), sep = " ")[seq_len(min(16, length(o)))]; values <- values[o][seq_along(labels)]
  if (is.null(hi) || !length(hi)) hi <- 1
  auto <- derive_bar(str_trunc(full[seq_along(values)], 64), values, vf)
  if (total > length(values)) auto$sub <- join_sentence(auto$sub, sprintf("Top %d of %d shown", length(values), total))
  list(kind = "bar_h", chart = art_ed_hbar(labels, values, highlight = hi, fmt = vf),
       auto = auto, sub_default = axis_title(spec$layout$xaxis), n = length(values))
}

series_name <- function(tr_i) { nm <- tr_i$name; if (is.null(nm) || !nzchar(nm)) NA_character_ else as.character(nm) }

build_chart <- function(spec, ov_key = NULL) {
  tr <- spec$data
  t1 <- tr[[1]]
  type <- t1$type
  if (is.null(type)) return(NULL)
  mk <- t1$marker
  lay <- spec$layout
  xlog <- identical(lay$xaxis$type, "log"); ylog <- identical(lay$yaxis$type, "log")
  if ((xlog || ylog) && !(type %in% c("scatter", "scattergl") && grepl("markers", t1$mode %||% "") && !grepl("lines", t1$mode %||% ""))) return(NULL)
  forced <- !is.null(ov_key) && !is.null(overrides[[ov_key]])

  if (type == "bar" && length(tr) == 1) {
    horiz <- identical(t1$orientation, "h")
    if (horiz) { labels <- as.character(decode(t1$y)); values <- as.numeric(decode(t1$x)) }
    else { labels <- as.character(decode(t1$x)); values <- as.numeric(decode(t1$y)) }
    if (!length(values) || length(values) != length(labels)) return(NULL)
    labels <- tidy_labels(labels)
    cols <- if (!is.null(mk$color) && length(mk$color) == length(values)) unlist(mk$color) else NULL
    odd <- modal_other(cols, length(values))
    keep <- is.finite(values)
    odd_flag <- seq_along(keep)[keep] %in% odd
    txt <- if (length(t1$text) == length(keep)) unlist(t1$text)[keep] else NULL
    labels <- labels[keep]; values <- values[keep]
    if (!length(values)) return(NULL)
    if (horiz) {
      if (!identical(lay$yaxis$autorange, "reversed")) { labels <- rev(labels); values <- rev(values); odd_flag <- rev(odd_flag) }
      return(make_hbar(labels, values, spec, which(odd_flag[order(values, decreasing = TRUE)]), total = length(values), txt = if (!is.null(txt) && !identical(lay$yaxis$autorange, "reversed")) rev(txt) else txt))
    }
    if (!is.null(t1$base) || max(abs(values)) == 0) return(NULL)
    labels <- tidy_labels(labels)
    nums <- suppressWarnings(as.numeric(labels))
    numeric_x <- !anyNA(nums)
    if (numeric_x && anyDuplicated(nums)) {
      if (!isTRUE(lay$barmode %in% c("stack", "relative"))) return(NULL)
      agg <- tapply(values, nums, sum)
      nums <- as.numeric(names(agg)); values <- as.numeric(agg); labels <- as.character(nums)
    }
    if (numeric_x && length(values) > 16) {
      years <- all(abs(nums - round(nums)) < 1e-9) && min(nums) >= 1000 && max(nums) <= 2100
      xf <- if (years) year_fmt(nums) else num_labels(nums)
      auto <- if (years) derive_bar(as.character(round(nums)), values, num_fmt(values), TRUE) else derive_dist(nums, values, xf)
      if (years) auto$sub <- join_sentence(auto$sub, sprintf("%d periods plotted", length(values)))
      return(list(kind = "hist", chart = art_ed_hist(nums, values, highlight = which.max(values), xfmt = xf), auto = auto,
                  sub_default = axis_title(lay$yaxis), n = length(values)))
    }
    if (!numeric_x && (length(values) > 16 || any(nchar(labels) > 18))) {
      return(make_hbar(labels, values, spec, NULL, total = length(values)))
    }
    hi <- which(odd_flag); if (!length(hi)) hi <- which.max(values)
    periods <- all(grepl("^[0-9]{3,4}", labels))
    return(list(kind = "bar_v", chart = art_ed_col(str_trunc(labels, 12), values, highlight = hi, fmt = num_fmt(values), every = ceiling(length(values) / 8)),
                auto = derive_bar(labels, values, num_fmt(values), periods),
                sub_default = axis_title(lay$yaxis), n = length(values)))
  }

  if (type == "bar" && length(tr) >= 2 && length(tr) <= 5 && all(vapply(tr, function(z) identical(z$type, "bar"), TRUE))) {
    horiz <- identical(t1$orientation, "h")
    cats <- as.character(decode(if (horiz) t1$y else t1$x))
    nm <- vapply(tr, series_name, "")
    if (anyNA(nm) || length(cats) < 2 || length(cats) > 14) return(NULL)
    vals <- lapply(tr, function(z) as.numeric(decode(if (horiz) z$x else z$y)))
    if (any(vapply(vals, length, 1L) != length(cats)) || any(vapply(vals, function(v) any(!is.finite(v)), TRUE))) return(NULL)
    if (any(unlist(vals) < 0)) return(NULL)
    stacked <- identical(lay$barmode, "stack")
    flip <- horiz || any(nchar(cats) > 10)
    cats_f <- str_trunc(cats, 24)
    if (anyDuplicated(cats_f)) return(NULL)
    cc <- rep(cats_f, times = length(tr)); ss <- rep(str_trunc(nm, 32), each = length(cats)); vv <- unlist(vals)
    fmt <- num_fmt(vv)
    return(list(kind = if (flip) "gbar_h" else "gbar_v", chart = art_ed_gbar(cc, ss, vv, stacked = stacked, horizontal = flip, fmt = fmt),
                auto = derive_grouped(cc, ss, vv, stacked, fmt), sub_default = NULL, n = length(cats)))
  }

  if (type == "heatmap" && length(tr) == 1) {
    z <- t1$z
    if (is.null(z)) return(NULL)
    zm <- tryCatch({
      if (!is.null(z$bdata)) {
        dims <- as.integer(strsplit(z$shape, ",\\s*")[[1]])
        matrix(as.numeric(decode(z)), nrow = dims[1], ncol = dims[2], byrow = TRUE)
      } else do.call(rbind, lapply(z, function(r) as.numeric(unlist(lapply(r, function(v) if (is.null(v)) NA else v)))))
    }, error = function(e) NULL)
    xs <- as.character(decode(t1$x)); ys <- as.character(decode(t1$y))
    if (is.null(zm) || nrow(zm) != length(ys) || ncol(zm) != length(xs) || length(zm) > 150) return(NULL)
    cl <- function(z) sub("\\.0$", "", z)
    rr <- rep(str_trunc(cl(ys), 22), times = length(xs)); cc <- rep(str_trunc(cl(xs), 14), each = length(ys)); vv <- as.vector(zm)
    if (anyDuplicated(unique(data.frame(rr, cc))) || sum(is.finite(vv)) < 4) return(NULL)
    fmt <- num_fmt(vv[is.finite(vv)])
    ok <- is.finite(vv)
    return(list(kind = "heat", chart = art_ed_heat(rr, cc, vv, fmt = fmt, show_values = length(vv) <= 60),
                auto = derive_heat(rr[ok], cc[ok], vv[ok], fmt), sub_default = NULL, n = length(vv)))
  }

  if (type == "scatter" && grepl("lines", t1$mode %||% "")) {
    keep_tr <- list(); gnames <- character()
    for (i in seq_along(tr)) {
      ti <- tr[[i]]
      if (!grepl("lines", ti$mode %||% "")) next
      nm_i <- series_name(ti)
      if (length(tr) > 1 && grepl("^Series [0-9]+$", nm_i %||% "")) return(NULL)
      if (length(tr) > 1 && (is.na(nm_i) || grepl("(range|interval|band|bootstrap)", nm_i, ignore.case = TRUE))) next
      if (length(decode(ti$x)) < 2) { if (length(tr) > 1) next else return(NULL) }
      keep_tr[[length(keep_tr) + 1]] <- ti; gnames <- c(gnames, if (is.na(nm_i)) "all" else nm_i)
    }
    if (!length(keep_tr) || length(keep_tr) > 6) return(NULL)
    if (anyDuplicated(gnames)) return(NULL)
    rawx <- lapply(keep_tr, function(z) decode(z$x))
    allx <- unlist(lapply(rawx, as.character))
    nums <- suppressWarnings(as.numeric(allx))
    xlab <- NULL; cat_labs <- NULL; dates <- FALSE
    if (!anyNA(nums)) {
      xn <- lapply(rawx, function(v) as.numeric(v))
    } else if (all(grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}", allx))) {
      xn <- lapply(rawx, function(v) as.numeric(as.Date(substr(as.character(v), 1, 10)))); dates <- TRUE
      span <- diff(range(unlist(xn)))
      xlab <- function(v) format(as.Date(v, origin = "1970-01-01"), if (span > 1100) "%Y" else if (span > 200) "%b %Y" else "%b %d")
    } else {
      cat_labs <- unique(allx)
      if (length(cat_labs) > 12) return(NULL)
      xn <- lapply(rawx, function(v) match(as.character(v), cat_labs))
      xlab <- function(v) ifelse(abs(v - round(v)) < 1e-9 & round(v) >= 1 & round(v) <= length(cat_labs), str_trunc(cat_labs[pmax(1, round(v))], 12), "")
    }
    dfs <- list()
    for (i in seq_along(keep_tr)) {
      y <- as.numeric(decode(keep_tr[[i]]$y))
      if (length(y) != length(xn[[i]])) return(NULL)
      dfs[[i]] <- data.frame(x = xn[[i]], y = y, g = gnames[i])
    }
    df <- do.call(rbind, dfs)
    df <- df[is.finite(df$x) & is.finite(df$y), ]
    if (nrow(df) < 2) return(NULL)
    multi <- length(unique(df$g)) > 1
    fmt <- num_fmt(df$y)
    if (!is.null(cat_labs)) {
      auto <- derive_line_cat(transform(df, g = str_trunc(g, 26)), fmt, cat_labs)
      chart <- art_ed_line(df$x, df$y, group = if (multi) df$g else NULL, fmt = fmt, lfmt = fmt, xbreaks = seq_along(cat_labs), xlab = xlab, points = TRUE)
    } else {
      xf <- if (dates) xlab else year_fmt(df$x)
      auto <- derive_line(transform(df, g = str_trunc(g, 26)), fmt, xf)
      chart <- art_ed_line(df$x, df$y, group = if (multi) df$g else NULL, fmt = fmt, lfmt = fmt, xlab = xlab, points = nrow(df) <= 12)
    }
    return(list(kind = "line", chart = chart, auto = auto, sub_default = axis_title(lay$yaxis), n = nrow(df)))
  }

  if (type == "scatter" && identical(t1$mode, "markers") && length(tr) == 1 && is.character(unlist(t1$y)) && length(t1$y) >= 3 && length(t1$y) <= 20) {
    labels <- as.character(decode(t1$y)); values <- as.numeric(decode(t1$x))
    if (length(labels) == length(values) && all(is.finite(values))) {
      ex <- t1$error_x
      lo <- hi <- NULL
      if (!is.null(ex) && !is.null(ex$array) && !is.null(ex$arrayminus) && length(unlist(ex$array)) == length(values) && length(unlist(ex$arrayminus)) == length(values)) {
        hi <- values + as.numeric(unlist(ex$array)); lo <- values - as.numeric(unlist(ex$arrayminus))
      }
      o <- order(values, decreasing = TRUE); labels <- make.unique(str_trunc(labels[o], 28), sep = " "); values <- values[o]
      if (!is.null(lo)) { lo <- lo[o]; hi <- hi[o] }
      auto <- derive_bar(labels, values, num_fmt(values))
      return(list(kind = "dot", chart = art_ed_dot(labels, values, fmt = scales::label_number(accuracy = 0.1), lo = lo, hi = hi), auto = auto, sub_default = axis_title(lay$xaxis), n = length(values)))
    }
  }

  if (type %in% c("scatter", "scattergl") && grepl("markers", t1$mode %||% "")) {
    mtr <- Filter(function(z) grepl("markers", z$mode %||% "") && !grepl("lines", z$mode %||% ""), tr)
    pooled <- length(mtr) > 1
    pool_hi <- integer(); pool_note <- NULL
    if (pooled) {
      x <- unlist(lapply(mtr, function(z) as.numeric(decode(z$x)))); y <- unlist(lapply(mtr, function(z) as.numeric(decode(z$y))))
      if (length(mtr) == 2 && !is.na(series_name(mtr[[2]]))) {
        n1 <- length(decode(mtr[[1]]$x)); pool_hi <- seq(n1 + 1, length(x)); pool_note <- series_name(mtr[[2]])
      }
      if (any(vapply(mtr, function(z) length(decode(z$x)) != length(decode(z$y)), TRUE))) return(NULL)
      txt <- NULL
    } else {
      x <- as.numeric(decode(t1$x)); y <- as.numeric(decode(t1$y))
      txt <- if (!is.null(t1$text)) as.character(decode(t1$text)) else NULL
    }
    if (length(x) != length(y) || sum(is.finite(x) & is.finite(y)) < 3) return(NULL)
    if (xlog && any(x <= 0, na.rm = TRUE)) return(NULL)
    if (ylog && any(y <= 0, na.rm = TRUE)) return(NULL)
    only <- unlist(overrides[[ov_key %||% ""]]$label_only)
    if (!is.null(txt) && (length(txt) != length(x) || any(grepl("<|=", txt), na.rm = TRUE) || any(nchar(txt) > 30, na.rm = TRUE))) txt <- NULL
    ok <- is.finite(x) & is.finite(y)
    hi <- pool_hi; lab <- NULL
    if (!is.null(txt) && length(txt[ok]) && mean(duplicated(txt[ok])) > 0.3 && !length(only)) txt <- NULL
    if (!is.null(txt)) {
      pick <- which(ok & !is.na(txt) & nzchar(txt))
      if (length(only)) pick <- pick[txt[pick] %in% only]
      sc <- function(v) abs(v - median(v[ok])) / (mad(v[ok]) + 1e-9)
      if (!length(only)) { pick <- pick[order(-(sc(x)[pick] + sc(y)[pick]))]; pick <- head(pick[!duplicated(txt[pick])], 6) }
      hi <- pick; lab <- txt
    }
    xname <- mid(axis_title(lay$xaxis)); yname <- axis_title(lay$yaxis)
    auto <- derive_scatter(x, y, xname, yname)
    if (!is.null(auto) && pooled) auto$sub <- paste0(auto$sub, if (!is.null(pool_note)) paste0(". Pink: ", pool_note) else paste0(", ", length(mtr), " groups pooled"))
    return(list(kind = "scatter", chart = art_ed_scatter(x[ok], y[ok], label = if (is.null(lab)) NULL else lab[ok], highlight = match(hi, which(ok)), xfmt = num_fmt(x), yfmt = num_fmt(y), xlog = xlog, ylog = ylog),
                auto = auto,
                sub_default = paste(na.omit(c(axis_title(lay$yaxis), axis_title(lay$xaxis))), collapse = " by "), n = sum(ok)))
  }

  if (type == "box") {
    vals <- list(); grp <- list()
    for (i in seq_len(min(10, length(tr)))) {
      v <- as.numeric(decode(tr[[i]]$y %||% tr[[i]]$x)); nm <- tr[[i]]$name %||% paste0("g", i)
      v <- v[is.finite(v)]; if (!length(v)) next
      vals[[i]] <- v; grp[[i]] <- rep(str_trunc(nm, 32), length(v))
    }
    if (!length(vals)) return(NULL)
    values <- unlist(vals); groups <- unlist(grp)
    meds <- tapply(values, groups, median)
    ord <- names(sort(meds, decreasing = TRUE))
    groups <- factor(groups, levels = ord)
    return(list(kind = "box", chart = art_ed_box(values, as.character(groups), highlight = ord[1], fmt = num_fmt(values)),
                auto = derive_box(values, as.character(groups), num_fmt(values)),
                sub_default = "Distribution by group. Box shows the middle half; the line is the median.", n = length(values)))
  }

  if (type == "histogram" && length(tr) >= 2 && length(tr) <= 6 && all(vapply(tr, function(z) identical(z$type, "histogram") && !is.null(series_name(z)) && !is.na(series_name(z)), TRUE))) {
    vals <- lapply(tr, function(z) { v <- as.numeric(decode(z$x)); v[is.finite(v)] })
    grp <- unlist(Map(function(v, z) rep(str_trunc(series_name(z), 32), length(v)), vals, tr)); values <- unlist(vals)
    if (length(values) < 20) return(NULL)
    meds <- tapply(values, grp, median); ord <- names(sort(meds, decreasing = TRUE))
    return(list(kind = "box", chart = art_ed_box(values, grp, highlight = ord[1], fmt = num_fmt(values)),
                auto = derive_box(values, grp, num_fmt(values)), sub_default = NULL, n = length(values)))
  }

  if (type == "histogram" && length(tr) == 1) {
    x <- as.numeric(decode(t1$x)); x <- x[is.finite(x)]
    if (length(x) < 20) return(NULL)
    q99 <- quantile(x, 0.99); clipped <- max(x) > q99 * 1.0001 && (max(x) - q99) > 0.25 * diff(range(x))
    xs <- if (clipped) x[x <= q99] else x
    h <- hist(xs, plot = FALSE, breaks = min(30, max(8, nclass.FD(xs))))
    xf <- num_labels(h$mids)
    auto <- derive_dist(h$mids, h$counts, xf)
    if (clipped) auto$sub <- join_sentence(auto$sub, sprintf("Shows values up to the 99th percentile (%s); the maximum is %s", fnum(xf, q99), fnum(xf, max(x))))
    return(list(kind = "hist", chart = art_ed_hist(h$mids, h$counts, highlight = which.max(h$counts), xfmt = xf), auto = auto,
                sub_default = paste0("Number of records by ", tolower(axis_title(lay$xaxis) %||% "value")), n = length(x)))
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
  m <- sub("\\s*[-·–—]\\s*ARTOMETRICS$", "", m)
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
  if (length(parts) > 1) parts[2] <- sub(" - (tidytuesday|source|data).*$", "", parts[2], ignore.case = TRUE)
  head_words <- lengths(strsplit(trimws(parts[1]), "\\s+"))
  head_ok <- !grepl(GENERIC, tolower(parts[1])) && (head_words >= 5 || grepl("[0-9]", parts[1]))
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
  if (is_editorial(spec, key) || is.null(built$auto)) {
    headline <- ov$headline %||% hp$head %||% stem
    subtitle <- ov$subtitle %||% hp$sub %||% built$sub_default
  } else {
    headline <- built$auto$head
    context <- if (!is.na(hp$head)) hp$head else NA_character_
    subtitle <- join_sentence(context, built$auto$sub)
    if (!is.na(hp$head) && !is.na(hp$sub) && !grepl("^(joint distribution|over time|full sample|by .*|structural slope|colored by category|trend with milestones|summary view|ranked bar|scatter field|period or category bar|.* on top|.* leads|.* lowest|interquartile view|pareto curve|robustness check|flat line|country|name|title|song|source|type|records by year|trend line|trend with milestones.*)$", sub("\\.$", "", tolower(hp$sub))) && !grepl("(source|tidytuesday)", tolower(hp$sub))) subtitle <- join_sentence(hp$head, hp$sub, built$auto$sub)
  }
  src <- ov$source %||% source_for(slug, stem)
  out <- file.path("public/images/content/articles", slug, "charts", stem)
  if (!dir.exists(dirname(out))) return(FALSE)
  ok <- tryCatch({
    height <- if (built$kind %in% c("bar_h")) min(6.8, max(4.4, 3.4 + 0.34 * built$n)) else if (built$kind %in% c("dot", "gbar_h")) min(8.6, max(5.6, 3.6 + 0.3 * built$n * (if (built$kind == "gbar_h") 2.2 else 1))) else 6.6
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
