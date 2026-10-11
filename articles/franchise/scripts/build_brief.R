#!/usr/bin/env Rscript
# Franchise R2 — charts + derived tables. From repo root: npm run brief:franchise

ensure_brief_packages <- function(pkgs) {
  user_lib <- Sys.getenv("R_LIBS_USER")
  if (!nzchar(user_lib)) {
    minor <- strsplit(R.version$minor, ".", fixed = TRUE)[[1]][[1]]
    user_lib <- file.path(Sys.getenv("HOME"), "R", paste0(R.version$platform, "-library"),
                          paste0(R.version$major, ".", minor))
  }
  dir.create(user_lib, recursive = TRUE, showWarnings = FALSE)
  .libPaths(c(user_lib, .libPaths()))
  missing <- pkgs[!vapply(pkgs, requireNamespace, quietly = TRUE, FUN.VALUE = logical(1))]
  if (length(missing)) {
    message("Installing: ", paste(missing, collapse = ", "))
    install.packages(missing, lib = user_lib, repos = "https://cloud.r-project.org")
  }
}
ensure_brief_packages(c("tidyverse", "jsonlite", "plotly", "scales", "ragg", "cowplot"))

suppressPackageStartupMessages({
  library(tidyverse)
  library(jsonlite)
  library(plotly)
  library(scales)
})

args_all <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args_all, value = TRUE)
script_path <- if (length(file_arg)) normalizePath(sub("^--file=", "", file_arg[[1]])) else {
  normalizePath("articles/franchise/scripts/build_brief.R")
}
repo_root <- normalizePath(file.path(dirname(script_path), "../../.."))
article_dir <- file.path(repo_root, "articles/franchise")
data_dir <- file.path(article_dir, "data")
charts_dir <- file.path(article_dir, "charts")
public_img <- file.path(repo_root, "public/images/content/articles/franchise/charts")
public_data <- file.path(repo_root, "public/data/articles/franchise/charts")
dir.create(charts_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(public_img, recursive = TRUE, showWarnings = FALSE)
dir.create(public_data, recursive = TRUE, showWarnings = FALSE)

source(file.path(repo_root, "scripts/r/artometrics_theme.R"))
art_init_fonts(repo_root)

ART_PAGE <- "#FFFFFF"
ART_PAGE_DARK <- "#0D0D0D"
ART_RED <- "#E60000"
ART_BLUE <- "#0047FF"
ART_BLACK <- "#000000"
ART_MID <- "#6B6B6B"
FONT_SANS <- "DM Sans, Helvetica, sans-serif"
FONT_MONO <- "DM Mono, ui-monospace, monospace"
FRANCHISE_N <- "n=103 franchises (TidyTuesday / mid-2019 Wikipedia scrape)"
FRANCHISE_SOURCE <- paste0("Source: S001 · ", FRANCHISE_N)
BOM_SOURCE <- "Data: Box Office Mojo yearly charts (manual franchise coding) — ARTOMETRICS"
DISNEY_10K <- "Data: The Walt Disney Company Form 10-K FY2024 — ARTOMETRICS"

raw_csv <- file.path(data_dir, "franchise.csv")
expected_sha <- "6e556287bad580be04e14d346036a8453f7ce975a7b26cf47d2057b873be1090"
sha256_file <- function(path) {
  line <- system2("sha256sum", shQuote(path), stdout = TRUE)
  strsplit(line, " ", fixed = TRUE)[[1]][[1]]
}
if (!identical(sha256_file(raw_csv), expected_sha)) {
  stop("SHA-256 mismatch for franchise.csv")
}

theme_white <- function() {
  theme_artometrics() +
    theme(
      plot.background = element_rect(fill = ART_PAGE, color = NA),
      panel.background = element_rect(fill = ART_PAGE, color = NA),
      panel.grid.major = element_line(color = "#E8E8E8", linewidth = 0.35)
    )
}

save_png <- function(plot_obj, name, height = 7) {
  ggsave(
    file.path(charts_dir, paste0(name, ".png")),
    plot = plot_obj, width = 12, height = height, dpi = 300, bg = ART_PAGE,
    device = if (requireNamespace("ragg", quietly = TRUE)) ragg::agg_png else "png"
  )
}

write_plotly_json <- function(fig, path) {
  built <- plotly_build(fig)
  payload <- list(data = built$x$data, layout = built$x$layout, config = art_plotly_config())
  write_json(payload, path, auto_unbox = TRUE, pretty = TRUE, null = "null", na = "null")
}

write_motion_html <- function(name, variant = "light") {
  json_path <- file.path(charts_dir, paste0(name, ".plotly.json"))
  html_path <- file.path(charts_dir, paste0(name, ".html"))
  if (!file.exists(json_path)) return(invisible(NULL))
  payload <- fromJSON(json_path, simplifyVector = FALSE)
  bg <- if (identical(variant, "dark")) ART_PAGE_DARK else ART_PAGE
  payload$layout$paper_bgcolor <- bg
  payload$layout$plot_bgcolor <- bg
  if (identical(variant, "dark")) {
    payload$layout$font$color <- "#FFFFFF"
  }
  spec <- toJSON(payload, auto_unbox = TRUE, null = "null")
  html <- paste0(
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"/>",
    "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=DM+Mono:wght@400;500&display=swap\"/>",
    "<script src=\"https://cdn.plot.ly/plotly-2.35.2.min.js\"></script>",
    "<style>html,body{margin:0;height:100%;background:", bg, ";}</style></head><body>",
    "<div id=\"art-chart\" style=\"width:100%;height:100vh;\"></div>",
    "<script>const spec=", spec, ";",
    "const target=JSON.parse(JSON.stringify(spec));",
    "function zeroTraces(d){return d.map(t=>{const c=JSON.parse(JSON.stringify(t));",
    "['x','y','z','values','labels'].forEach(k=>{if(Array.isArray(c[k])&&c[k].every(v=>typeof v==='number'))c[k]=c[k].map(()=>0);});",
    "if(c.type==='bar'&&c.orientation==='h'&&Array.isArray(c.x))c.x=c.x.map(()=>0);",
    "if(c.type==='bar'&&(!c.orientation||c.orientation==='v')&&Array.isArray(c.y))c.y=c.y.map(()=>0);",
    "return c;});}",
    "const start=performance.now();const dur=1400;",
    "Plotly.newPlot('art-chart',{data:zeroTraces(spec.data),layout:spec.layout,config:spec.config}).then(()=>{",
    "function frame(now){const p=Math.min(1,(now-start)/dur);const ease=1-Math.pow(1-p,3);",
    "const d=target.data.map((t,i)=>{const c=JSON.parse(JSON.stringify(t));",
    "['x','y','z','values'].forEach(k=>{if(Array.isArray(c[k])&&target.data[i][k]&&target.data[i][k].every(v=>typeof v==='number'))",
    "c[k]=target.data[i][k].map(v=>v*ease);});return c;});",
    "Plotly.react('art-chart',d,target.layout);if(p<1)requestAnimationFrame(frame);}",
    "requestAnimationFrame(frame);});</script></body></html>"
  )
  writeLines(html, html_path, useBytes = TRUE)
  for (dest in c(public_img, public_data)) {
    file.copy(html_path, file.path(dest, paste0(name, ".html")), overwrite = TRUE)
  }
  invisible(html_path)
}

copy_public <- function(name) {
  for (ext in c(".png", ".plotly.json")) {
    src <- file.path(charts_dir, paste0(name, ext))
    if (!file.exists(src)) next
    file.copy(src, file.path(public_img, paste0(name, ext)), overwrite = TRUE)
    file.copy(src, file.path(public_data, paste0(name, ext)), overwrite = TRUE)
  }
}

plotly_chrome <- function(fig, title, subtitle, takeaway, source, margin = list(l = 60, r = 40, t = 110, b = 90), n_line = FRANCHISE_N) {
  layout(
    fig,
    title = list(
      text = paste0("<b>", title, "</b><br><span style='font-size:12px;color:", ART_MID, "'>", subtitle, "</span>"),
      x = 0, xanchor = "left"
    ),
    paper_bgcolor = ART_PAGE, plot_bgcolor = ART_PAGE,
    font = list(family = FONT_SANS, color = ART_BLACK, size = 12),
    margin = margin,
    annotations = list(
      list(x = 0, y = 1.12, xref = "paper", yref = "paper", text = paste0("<b>", takeaway, "</b>"),
           showarrow = FALSE, xanchor = "left", font = list(size = 11, color = "#FFFFFF"),
           bgcolor = ART_RED, borderwidth = 3, bordercolor = ART_RED, borderpad = 6),
      list(x = 0, y = -0.18, xref = "paper", yref = "paper",
           text = paste0(art_caption(source), "<br><span style='font-family:", FONT_MONO, "'>", n_line, "</span>"),
           showarrow = FALSE, xanchor = "left", font = list(size = 9, color = ART_MID))
    )
  )
}

cat_cols <- c(
  "Merchandise, Licensing & Retail" = ART_RED,
  "Box Office" = ART_BLUE,
  "Video Games/Games" = "#2E5FA3",
  "Comic or Manga" = "#4A6FA5",
  "Home Video/Entertainment" = "#6B6B6B",
  "TV" = "#8A8A8A",
  "Book sales" = "#A0A0A0",
  "Music" = "#B5B5B5"
)

df <- read_csv(raw_csv, show_col_types = FALSE)
franchise_totals <- df %>%
  group_by(franchise, year_created, original_media, owners) %>%
  summarise(total = sum(revenue, na.rm = TRUE), .groups = "drop")

consolidate_owner <- function(owner) {
  vapply(owner, function(o) {
    if (grepl("Disney Company", o, fixed = TRUE)) return("The Walt Disney Company (consolidated)")
    if (grepl("Lucasfilm", o, fixed = TRUE)) return("The Walt Disney Company (consolidated)")
    if (grepl("Marvel Entertainment", o, fixed = TRUE)) return("The Walt Disney Company (consolidated)")
    if (grepl("20th Century Fox", o, fixed = TRUE)) return("The Walt Disney Company (consolidated)")
    o
  }, character(1), USE.NAMES = FALSE)
}

owner_totals <- franchise_totals %>%
  mutate(owner_group = consolidate_owner(owners)) %>%
  group_by(owner_group) %>%
  summarise(lifetime_b = sum(total), .groups = "drop") %>%
  arrange(desc(lifetime_b))

write_csv(owner_totals, file.path(data_dir, "owner_totals_derived.csv"))

# ── Chart 1: Top 20 stacked revenue ───────────────────────────────────────────
top20 <- df %>%
  group_by(franchise) %>%
  summarise(total = sum(revenue), .groups = "drop") %>%
  arrange(desc(total)) %>%
  slice_head(n = 20) %>%
  pull(franchise)

chart1_df <- df %>%
  filter(franchise %in% top20) %>%
  group_by(franchise, revenue_category) %>%
  summarise(revenue = sum(revenue), .groups = "drop") %>%
  mutate(
    franchise = fct_reorder(franchise, revenue, .fun = sum, .desc = TRUE),
    fill_col = unname(cat_cols[revenue_category])
  )

p1 <- ggplot(chart1_df, aes(x = revenue, y = franchise, fill = revenue_category)) +
  geom_col(width = 0.72) +
  scale_fill_manual(values = cat_cols) +
  scale_x_continuous(labels = label_number(suffix = "B"), expand = expansion(mult = c(0, 0.05))) +
  labs(
    title = "Lifetime revenue composition — top 20 franchises",
    subtitle = "Stacked streams (Wikipedia / TidyTuesday estimates, mid-2019)",
    x = "Estimated lifetime revenue ($B)", y = NULL, fill = NULL
  ) +
  theme_white() +
  theme(legend.position = "bottom")
p1 <- finish_art_chart(p1, "Merchandise dominates most bars — box office is rarely the largest slice", FRANCHISE_SOURCE)
save_png(p1, "chart1_top20_revenue", 8)

fig1 <- chart1_df %>%
  group_by(franchise, revenue_category) %>%
  summarise(revenue = sum(revenue), .groups = "drop") %>%
  plot_ly(x = ~revenue, y = ~franchise, color = ~revenue_category, colors = cat_cols,
          type = "bar", orientation = "h") %>%
  plotly_chrome(
    "Top 20 franchises by estimated lifetime revenue",
    "Eight revenue streams (mid-2019 Wikipedia scrape)",
    "Pokémon at $90.9B leads; merchandise is the widest band for most properties",
    FRANCHISE_SOURCE, margin = list(l = 200, r = 40, t = 120, b = 90)
  ) %>%
  layout(barmode = "stack", xaxis = list(title = "Lifetime revenue ($B)", tickfont = list(family = FONT_MONO)), showlegend = TRUE)
write_plotly_json(fig1, file.path(charts_dir, "chart1_top20_revenue.plotly.json"))
write_motion_html("chart1_top20_revenue")
copy_public("chart1_top20_revenue")

# ── Chart 2: Revenue per year ─────────────────────────────────────────────────
chart2_df <- franchise_totals %>%
  mutate(
    years = pmax(2019 - year_created, 1),
    rev_per_year = total / years
  ) %>%
  arrange(desc(rev_per_year)) %>%
  slice_head(n = 20) %>%
  mutate(franchise = fct_reorder(franchise, rev_per_year))

p2 <- ggplot(chart2_df, aes(x = rev_per_year, y = franchise, fill = ART_BLUE)) +
  geom_col(width = 0.65, show.legend = FALSE) +
  geom_text(aes(label = paste0(round(rev_per_year, 1), "B/yr")), hjust = -0.05, size = 3.2, color = ART_BLACK) +
  scale_fill_identity() +
  scale_x_continuous(labels = label_number(suffix = "B"), expand = expansion(mult = c(0, 0.14))) +
  labs(title = "Revenue efficiency — top 20 by $B per year of existence", subtitle = "Lifetime total ÷ (2019 − year_created)", x = "$B per year", y = NULL) +
  theme_white()
p2 <- finish_art_chart(p2, "Pokémon earns the most per calendar year — not only the most in total", FRANCHISE_SOURCE)
save_png(p2, "chart2_revenue_per_year", 7)

fig2 <- plot_ly(chart2_df, x = ~rev_per_year, y = ~franchise, type = "bar", orientation = "h",
               marker = list(color = ART_BLUE)) %>%
  plotly_chrome("Franchise revenue per year of existence", "Top 20 (mid-2019 file)", "Young ecosystems can beat century-old mascots on speed", FRANCHISE_SOURCE, margin = list(l = 200, r = 50, t = 120, b = 90)) %>%
  layout(xaxis = list(title = "$B per year"))
write_plotly_json(fig2, file.path(charts_dir, "chart2_revenue_per_year.plotly.json"))
write_motion_html("chart2_revenue_per_year")
copy_public("chart2_revenue_per_year")

# ── Chart 3a / 3b: Owner totals ───────────────────────────────────────────────
top_owners_raw <- franchise_totals %>%
  group_by(owners) %>%
  summarise(lifetime_b = sum(total), .groups = "drop") %>%
  arrange(desc(lifetime_b)) %>%
  slice_head(n = 14)

top_owners_cons <- franchise_totals %>%
  mutate(owners = consolidate_owner(owners)) %>%
  group_by(owners) %>%
  summarise(lifetime_b = sum(total), .groups = "drop") %>%
  arrange(desc(lifetime_b)) %>%
  slice_head(n = 12)

make_owner_chart <- function(dat, fname, title, takeaway) {
  dat <- dat %>% mutate(owners = fct_reorder(owners, lifetime_b))
  p <- ggplot(dat, aes(x = lifetime_b, y = owners, fill = lifetime_b)) +
    geom_col(width = 0.65, show.legend = FALSE) +
    scale_fill_gradient(low = ART_BLUE, high = ART_RED) +
    scale_x_continuous(labels = label_number(suffix = "B"), expand = expansion(mult = c(0, 0.08))) +
    labs(title = title, subtitle = "Sum of franchise rows in TidyTuesday file", x = "Lifetime $B", y = NULL) +
    theme_white()
  p <- finish_art_chart(p, takeaway, FRANCHISE_SOURCE)
  save_png(p, fname, 6.5)
  fig <- plot_ly(dat, x = ~lifetime_b, y = ~owners, type = "bar", orientation = "h",
                 marker = list(color = ~lifetime_b, colorscale = list(c(0, ART_BLUE), c(1, ART_RED)), showscale = FALSE)) %>%
    plotly_chrome(title, "Owner field as stored in Wikipedia scrape", takeaway, FRANCHISE_SOURCE, margin = list(l = 260, r = 40, t = 120, b = 90)) %>%
    layout(xaxis = list(title = "Lifetime $B"))
  write_plotly_json(fig, file.path(charts_dir, paste0(fname, ".plotly.json")))
  copy_public(fname)
}

make_owner_chart(top_owners_raw, "chart3a_disney_non_consolidated",
                 "Ownership leaderboard — subsidiaries listed separately",
                 "Marvel and Fox look like rivals until you read the footnotes")
make_owner_chart(top_owners_cons, "chart3b_disney_consolidated",
                 "Same file — Disney subsidiaries rolled into one bar",
                 "Consolidated Disney exceeds the next owner by an order of magnitude")

# ── Chart 5: Original media ───────────────────────────────────────────────────
chart5_df <- franchise_totals %>%
  group_by(original_media) %>%
  summarise(lifetime_b = sum(total), .groups = "drop") %>%
  arrange(desc(lifetime_b)) %>%
  slice_head(n = 10) %>%
  mutate(original_media = fct_reorder(original_media, lifetime_b))

p5 <- ggplot(chart5_df, aes(x = lifetime_b, y = original_media, fill = ART_BLUE)) +
  geom_col(width = 0.62, show.legend = FALSE) +
  scale_fill_identity() +
  scale_x_continuous(labels = label_number(suffix = "B"), expand = expansion(mult = c(0, 0.1))) +
  labs(title = "Where franchises start — top origin formats", subtitle = "Sum of lifetime revenue by original_media", x = "Lifetime $B", y = NULL) +
  theme_white()
p5 <- finish_art_chart(p5, "Games and novels punch above the 'franchise = film' stereotype", FRANCHISE_SOURCE)
save_png(p5, "chart5_original_media_revenue", 6)
fig5 <- plot_ly(chart5_df, x = ~lifetime_b, y = ~original_media, type = "bar", orientation = "h", marker = list(color = ART_BLUE)) %>%
  plotly_chrome("Lifetime revenue by original media", "Top 10 origin labels in file", "The seed format sets licensing geometry", FRANCHISE_SOURCE, margin = list(l = 160, r = 40, t = 120, b = 90))
write_plotly_json(fig5, file.path(charts_dir, "chart5_original_media_revenue.plotly.json"))
copy_public("chart5_original_media_revenue")

# ── Chart 6: Revenue stream shares (all 8 categories) ─────────────────────────
stream_df <- df %>%
  group_by(revenue_category) %>%
  summarise(revenue = sum(revenue), .groups = "drop") %>%
  mutate(
    share_pct = round(revenue / sum(revenue) * 100, 1),
    revenue_category = fct_reorder(revenue_category, share_pct),
    bar_color = if_else(grepl("Merchandise", revenue_category, fixed = TRUE), ART_RED, ART_BLUE)
  )
write_csv(stream_df, file.path(data_dir, "revenue_stream_shares_derived.csv"))

p6 <- ggplot(stream_df, aes(x = share_pct, y = revenue_category, fill = bar_color)) +
  geom_col(width = 0.62, show.legend = FALSE) +
  scale_fill_identity() +
  geom_text(aes(label = paste0(share_pct, "%")), hjust = -0.08, fontface = "bold") +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15))) +
  labs(title = "Where franchise money pools — all 103 properties", subtitle = "Row-sum of TidyTuesday franchise.csv", x = "Share of tracked lifetime revenue (%)", y = NULL) +
  theme_white() + theme(panel.grid.major.y = element_blank())
p6 <- finish_art_chart(p6, "Merchandise is ~56% of row-sum revenue — not box office", FRANCHISE_SOURCE)
save_png(p6, "chart6_revenue_streams", 6)
fig6 <- plot_ly(stream_df, x = ~share_pct, y = ~revenue_category, type = "bar", orientation = "h",
               marker = list(color = ~bar_color)) %>%
  plotly_chrome("Revenue stream mix across the franchise ledger", "103 franchises in committed CSV", "Licensing and retail beat theatrical", FRANCHISE_SOURCE, margin = list(l = 240, r = 50, t = 120, b = 90))
write_plotly_json(fig6, file.path(charts_dir, "chart6_revenue_streams.plotly.json"))
copy_public("chart6_revenue_streams")

# ── Chart 7: Top-10 franchise share by year ───────────────────────────────────
bom <- read_csv(file.path(data_dir, "top10_franchise_share_by_year.csv"), show_col_types = FALSE)
p7 <- ggplot(bom, aes(x = calendar_year, y = share_pct)) +
  geom_line(color = ART_RED, linewidth = 1.1) +
  geom_point(color = ART_RED, size = 3) +
  scale_y_continuous(labels = function(x) paste0(x, "%"), limits = c(0, 100)) +
  labs(title = "Franchise installments as share of domestic top 10", subtitle = "Manual coding of Box Office Mojo yearly charts", x = NULL, y = "Share of top 10") +
  theme_white()
p7 <- finish_art_chart(p7, "Theatrical hits are increasingly serial products", BOM_SOURCE)
save_png(p7, "chart7_top10_franchise_share", 5.5)
fig7 <- plot_ly(bom, x = ~calendar_year, y = ~share_pct, type = "scatter", mode = "lines+markers",
                line = list(color = ART_RED, width = 3), marker = list(color = ART_RED, size = 8)) %>%
  plotly_chrome("Domestic top 10 — franchise installment share", "Selected years (see data/top10_franchise_share_by_year.csv)", "By 2024 nine of ten were franchise entries", BOM_SOURCE)
write_plotly_json(fig7, file.path(charts_dir, "chart7_top10_franchise_share.plotly.json"))
copy_public("chart7_top10_franchise_share")

# ── Chart 8: Disney acquisitions — price vs franchise anchor value ────────────
deals <- read_csv(file.path(data_dir, "disney_acquisitions.csv"), show_col_types = FALSE) %>%
  mutate(label = paste0(target, " (", year_closed, ")"))

p8 <- ggplot(deals, aes(x = price_usd_b, y = franchise_lifetime_revenue_b_mid2019)) +
  geom_point(color = ART_RED, size = 4) +
  geom_text(aes(label = target), vjust = -0.8, hjust = 0, size = 3.2) +
  scale_x_continuous(labels = label_number(suffix = "B")) +
  scale_y_continuous(labels = label_number(suffix = "B")) +
  labs(title = "Disney M&A — check price vs mid-2019 franchise ledger anchor", subtitle = "Y-axis is one flagship row in franchise.csv (not deal IRR)", x = "Acquisition price ($B)", y = "Anchor franchise lifetime ($B, file)") +
  theme_white()
p8 <- finish_art_chart(p8, "Lucasfilm and Marvel paid single-digit billions for triple-digit franchise rows", FRANCHISE_SOURCE)
save_png(p8, "chart8_disney_acquisitions", 6)
fig8 <- plot_ly(deals, x = ~price_usd_b, y = ~franchise_lifetime_revenue_b_mid2019, text = ~target,
                type = "scatter", mode = "markers+text", textposition = "top center",
                marker = list(color = ART_RED, size = 12)) %>%
  plotly_chrome("Acquisition check vs franchise-row scale", "Deal prices from SEC; franchise totals from Wikipedia scrape", "Price and ledger anchor are different units — both matter", FRANCHISE_SOURCE)
write_plotly_json(fig8, file.path(charts_dir, "chart8_disney_acquisitions.plotly.json"))
copy_public("chart8_disney_acquisitions")

# ── Chart 9: Disney FY2024 segment revenue ──────────────────────────────────────
seg <- read_csv(file.path(data_dir, "disney_segment_revenue_fy2024.csv"), show_col_types = FALSE) %>%
  mutate(segment = fct_reorder(segment, revenue_usd_b))

p9 <- ggplot(seg, aes(x = revenue_usd_b, y = segment, fill = segment)) +
  geom_col(width = 0.6, show.legend = FALSE) +
  scale_fill_manual(values = c(ART_BLUE, ART_RED, "#4A6FA5")) +
  scale_x_continuous(labels = label_number(suffix = "B"), expand = expansion(mult = c(0, 0.1))) +
  labs(title = "Disney FY2024 revenue by reportable segment", subtitle = "Form 10-K (fiscal year ended Sept 28, 2024)", x = "Revenue ($B)", y = NULL) +
  theme_white()
p9 <- finish_art_chart(p9, "Parks and experiences are a full third of Disney — not a side hustle", DISNEY_10K)
save_png(p9, "chart9_disney_segments_fy2024", 5.5)
fig9 <- plot_ly(seg, x = ~revenue_usd_b, y = ~segment, type = "bar", orientation = "h",
                marker = list(color = c(ART_BLUE, ART_RED, "#4A6FA5"))) %>%
  plotly_chrome("The Walt Disney Company — FY2024 segment revenue", "Audited 10-K totals", "Experiences rivals Entertainment in scale", DISNEY_10K, margin = list(l = 200, r = 40, t = 120, b = 90))
write_plotly_json(fig9, file.path(charts_dir, "chart9_disney_segments_fy2024.plotly.json"))
copy_public("chart9_disney_segments_fy2024")

assets_src <- file.path(article_dir, "assets")
assets_pub <- file.path(repo_root, "public/images/content/articles/franchise/assets")
if (dir.exists(assets_src)) {
  dir.create(assets_pub, recursive = TRUE, showWarnings = FALSE)
  for (name in list.files(assets_src, pattern = "^logo_.*\\.(svg|png)$")) {
    file.copy(file.path(assets_src, name), file.path(assets_pub, name), overwrite = TRUE)
  }
}

# ── Chart 10: 2019 vs 2026 Wikipedia totals (matched franchises) ───────────────
delta <- read_csv(file.path(data_dir, "franchise_revenue_2019_vs_2026.csv"), show_col_types = FALSE) %>%
  filter(is.finite(pct_change)) %>%
  arrange(desc(pct_change)) %>%
  slice_head(n = 20) %>%
  mutate(franchise = fct_reorder(franchise, pct_change))

p10 <- ggplot(delta, aes(x = pct_change, y = franchise, fill = if_else(pct_change >= 0, ART_RED, ART_BLUE))) +
  geom_col(width = 0.62, show.legend = FALSE) +
  scale_fill_identity() +
  labs(
    title = "Wikipedia lifetime estimates — percent change 2019 file → 2026 list",
    subtitle = "Matched franchise names (fuzzy); not inflation-adjusted",
    x = "% change in reported lifetime $B", y = NULL
  ) +
  theme_white()
p10 <- finish_art_chart(p10, "Methodology shifts inflate some rows — read footnotes before comparing levels", paste0("Source: S001 + S017 · n=", nrow(delta), " matched"))
save_png(p10, "chart10_wiki_2019_vs_2026", 7)
delta <- delta %>% mutate(bar_color = if_else(pct_change >= 0, ART_RED, ART_BLUE))
fig10 <- plot_ly(delta, x = ~pct_change, y = ~franchise, type = "bar", orientation = "h",
                 marker = list(color = ~bar_color)) %>%
  plotly_chrome(
    "2019 TidyTuesday row vs 2026 Wikipedia total",
    "Top 20 movers among matched names",
    "Pokémon’s 2026 list total reflects new licensing disclosures — not just inflation",
    "Source: S001 + S017",
    n_line = paste0("n=", nrow(delta), " matched franchises")
  )
write_plotly_json(fig10, file.path(charts_dir, "chart10_wiki_2019_vs_2026.plotly.json"))
write_motion_html("chart10_wiki_2019_vs_2026")
copy_public("chart10_wiki_2019_vs_2026")

# ── Chart 11: Revenue mix by original medium (stacked share) ─────────────────
mix <- read_csv(file.path(data_dir, "revenue_mix_by_original_medium.csv"), show_col_types = FALSE) %>%
  group_by(original_media) %>%
  summarise(medium_total = sum(revenue_usd_b), .groups = "drop") %>%
  arrange(desc(medium_total)) %>%
  slice_head(n = 8) %>%
  pull(original_media)

mix_plot <- read_csv(file.path(data_dir, "revenue_mix_by_original_medium.csv"), show_col_types = FALSE) %>%
  filter(original_media %in% mix) %>%
  mutate(original_media = fct_reorder(original_media, revenue_usd_b, .fun = sum))

p11 <- ggplot(mix_plot, aes(x = revenue_usd_b, y = original_media, fill = revenue_category)) +
  geom_col(position = "fill", width = 0.7) +
  scale_fill_manual(values = cat_cols) +
  scale_x_continuous(labels = scales::percent_format()) +
  labs(title = "Revenue mix by original medium", subtitle = "Stacked share within each origin label (mid-2019 file)", x = "Share within medium", y = NULL, fill = NULL) +
  theme_white() +
  theme(legend.position = "bottom")
p11 <- finish_art_chart(p11, "Game-first and book-first IPs skew toward merch + games, not box office", FRANCHISE_SOURCE)
save_png(p11, "chart11_mix_by_original_medium", 7)
fig11 <- plot_ly(mix_plot, x = ~revenue_usd_b, y = ~original_media, color = ~revenue_category, colors = cat_cols,
                 type = "bar", orientation = "h") %>%
  layout(barmode = "stack", xaxis = list(title = "Share")) %>%
  plotly_chrome("Origin medium predicts revenue geometry", "Top 8 origin labels by lifetime $B", "Theatrical-first is not the modal template", FRANCHISE_SOURCE)
write_plotly_json(fig11, file.path(charts_dir, "chart11_mix_by_original_medium.plotly.json"))
write_motion_html("chart11_mix_by_original_medium")
copy_public("chart11_mix_by_original_medium")

# ── Chart 12: Owner concentration before / after Fox rollup ───────────────────
conc <- read_csv(file.path(data_dir, "owner_concentration_scenarios.csv"), show_col_types = FALSE) %>%
  mutate(scenario = recode(scenario,
    "before_fox_split" = "Before Fox deal (Disney split)",
    "after_fox_consolidated" = "After Fox (Disney consolidated)"
  ))

p12 <- ggplot(conc, aes(x = scenario, y = top5_owner_share_pct, fill = ART_RED)) +
  geom_col(width = 0.5, show.legend = FALSE) +
  geom_text(aes(label = paste0(top5_owner_share_pct, "%")), vjust = -0.4, family = "Helvetica") +
  scale_fill_identity() +
  labs(title = "Top-five owners’ share of franchise-row revenue", subtitle = "Same mid-2019 Wikipedia scrape; consolidation rules in owner_consolidation_rules.csv", x = NULL, y = "Share of $1,522.2B row-sum (%)") +
  theme_white()
p12 <- finish_art_chart(p12, "Rolling Fox into Disney barely moves the top-five share — the tail is long", FRANCHISE_SOURCE)
save_png(p12, "chart12_owner_concentration", 5)
fig12 <- plot_ly(conc, x = ~scenario, y = ~top5_owner_share_pct, type = "bar", marker = list(color = ART_RED)) %>%
  plotly_chrome("Owner concentration — two consolidation lenses", "Top 5 owners", "Disney consolidation is dominant but not the whole market", FRANCHISE_SOURCE)
write_plotly_json(fig12, file.path(charts_dir, "chart12_owner_concentration.plotly.json"))
write_motion_html("chart12_owner_concentration")
copy_public("chart12_owner_concentration")

# ── Chart 13: Deal price vs lifetime revenue gained ───────────────────────────
deals_ext <- read_csv(file.path(data_dir, "entities_companies_deals.csv"), show_col_types = FALSE) %>%
  filter(!is.na(lifetime_revenue_gained_usd_b) & lifetime_revenue_gained_usd_b != "") %>%
  mutate(lifetime_revenue_gained_usd_b = as.numeric(lifetime_revenue_gained_usd_b), label = paste0(target, " (", year, ")"))

p13 <- ggplot(deals_ext, aes(x = price_usd_b, y = lifetime_revenue_gained_usd_b)) +
  geom_point(color = ART_BLUE, size = 4) +
  geom_text(aes(label = target), vjust = -0.8, size = 3) +
  scale_x_continuous(labels = label_number(suffix = "B")) +
  scale_y_continuous(labels = label_number(suffix = "B")) +
  labs(title = "Deal check — price vs mid-2019 franchise-row anchor", subtitle = "Verified Disney deals; Y is one flagship total from franchise.csv", x = "Price ($B)", y = "Anchor franchise lifetime ($B)") +
  theme_white()
p13 <- finish_art_chart(p13, "Marvel and Lucasfilm traded single-digit billions for triple-digit row scale", "Source: S009–S012 + S001")
save_png(p13, "chart13_deal_price_vs_revenue", 6)
fig13 <- plot_ly(deals_ext, x = ~price_usd_b, y = ~lifetime_revenue_gained_usd_b, text = ~target, type = "scatter", mode = "markers+text",
                 marker = list(color = ART_BLUE, size = 12), textposition = "top center") %>%
  plotly_chrome("M&A price vs franchise-row scale", "Disney core deals with both price and anchor", "Price and ledger totals measure different things", "Source: S009–S012 + S001")
write_plotly_json(fig13, file.path(charts_dir, "chart13_deal_price_vs_revenue.plotly.json"))
write_motion_html("chart13_deal_price_vs_revenue")
copy_public("chart13_deal_price_vs_revenue")

# ── Chart 14: Box office share of lifetime revenue (top 20) ─────────────────
bo_share <- franchise_totals %>%
  left_join(df %>% group_by(franchise) %>% summarise(bo = sum(revenue[revenue_category == "Box Office"], na.rm = TRUE), .groups = "drop"), by = "franchise") %>%
  mutate(bo_share_pct = bo / total * 100) %>%
  arrange(desc(total)) %>%
  slice_head(n = 20) %>%
  mutate(franchise = fct_reorder(franchise, bo_share_pct))

p14 <- ggplot(bo_share, aes(x = bo_share_pct, y = franchise, fill = ART_BLUE)) +
  geom_col(width = 0.65, show.legend = FALSE) +
  scale_fill_identity() +
  labs(title = "Box office as a share of lifetime franchise revenue", subtitle = "Top 20 by total lifetime $B (mid-2019 file)", x = "Box office % of row-sum", y = NULL) +
  theme_white()
p14 <- finish_art_chart(p14, "For most megabrands, the film is the ad — not the profit center", FRANCHISE_SOURCE)
save_png(p14, "chart14_box_office_share_top20", 7)
fig14 <- plot_ly(bo_share, x = ~bo_share_pct, y = ~franchise, type = "bar", orientation = "h", marker = list(color = ART_BLUE)) %>%
  plotly_chrome("Theatrical is a thin slice of the ledger", "Top 20 franchises", "Merch and games carry the median mega-IP", FRANCHISE_SOURCE, n_line = "n=20 franchises")
write_plotly_json(fig14, file.path(charts_dir, "chart14_box_office_share_top20.plotly.json"))
write_motion_html("chart14_box_office_share_top20")
copy_public("chart14_box_office_share_top20")

# ── Chart 15: Japan vs US vs Other ────────────────────────────────────────────
reg <- read_csv(file.path(data_dir, "franchise_region_summary.csv"), show_col_types = FALSE)
p15 <- ggplot(reg, aes(x = region, y = lifetime_revenue_usd_b, fill = region)) +
  geom_col(width = 0.55, show.legend = FALSE) +
  scale_fill_manual(values = c("Japan" = ART_RED, "US" = ART_BLUE, "Other" = ART_BLACK)) +
  labs(title = "Franchise revenue by origin region (heuristic)", subtitle = "Classifier uses owner/creator/franchise name markers — not GDP", x = NULL, y = "Lifetime $B (mid-2019 file)") +
  theme_white()
p15 <- finish_art_chart(p15, "Japan-origin rows punch above their count on merch-heavy mix", FRANCHISE_SOURCE)
save_png(p15, "chart15_region_japan_us_other", 5)
fig15 <- plot_ly(reg, labels = ~region, values = ~lifetime_revenue_usd_b, type = "pie", marker = list(colors = c(ART_RED, ART_BLUE, ART_BLACK))) %>%
  plotly_chrome("Regional split of franchise-row revenue", "Heuristic Japan / US / Other", "Cross-market comparison anchor", FRANCHISE_SOURCE, n_line = paste0("n=", sum(reg$franchise_count), " franchises"))
write_plotly_json(fig15, file.path(charts_dir, "chart15_region_japan_us_other.plotly.json"))
write_motion_html("chart15_region_japan_us_other", "dark")
copy_public("chart15_region_japan_us_other")

for (nm in list.files(charts_dir, pattern = "^chart[0-9].*\\.plotly\\.json$")) {
  write_motion_html(sub("\\.plotly\\.json$", "", nm))
}

message("Franchise brief charts written to ", charts_dir)
