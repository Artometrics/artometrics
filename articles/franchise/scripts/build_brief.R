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
ART_RED <- "#C0392B"
ART_BLUE <- "#1B4F8A"
ART_BLACK <- "#1C1C1E"
ART_MID <- "#6B6B6B"
FONT <- "Helvetica"
FRANCHISE_SOURCE <- "Data: TidyTuesday media franchises (2019-07-02) / Wikipedia estimates — ARTOMETRICS"
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

copy_public <- function(name) {
  for (ext in c(".png", ".plotly.json")) {
    src <- file.path(charts_dir, paste0(name, ext))
    if (!file.exists(src)) next
    file.copy(src, file.path(public_img, paste0(name, ext)), overwrite = TRUE)
    file.copy(src, file.path(public_data, paste0(name, ext)), overwrite = TRUE)
  }
}

plotly_chrome <- function(fig, title, subtitle, takeaway, source, margin = list(l = 60, r = 40, t = 110, b = 90)) {
  layout(
    fig,
    title = list(
      text = paste0("<b>", title, "</b><br><span style='font-size:12px;color:", ART_MID, "'>", subtitle, "</span>"),
      x = 0, xanchor = "left"
    ),
    paper_bgcolor = ART_PAGE, plot_bgcolor = ART_PAGE,
    font = list(family = "DM Sans, Helvetica, sans-serif", color = ART_BLACK, size = 12),
    margin = margin,
    annotations = list(
      list(x = 0, y = 1.12, xref = "paper", yref = "paper", text = paste0("<b>", takeaway, "</b>"),
           showarrow = FALSE, xanchor = "left", font = list(size = 11, color = "#FFFFFF"),
           bgcolor = ART_RED, borderpad = 6),
      list(x = 0, y = -0.2, xref = "paper", yref = "paper", text = art_caption(source),
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
    "Pokémon leads; merchandise is the widest band for most properties",
    FRANCHISE_SOURCE, margin = list(l = 200, r = 40, t = 120, b = 90)
  ) %>%
  layout(barmode = "stack", xaxis = list(title = "Lifetime revenue ($B)"), showlegend = TRUE)
write_plotly_json(fig1, file.path(charts_dir, "chart1_top20_revenue.plotly.json"))
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

message("Franchise brief charts written to ", charts_dir)
