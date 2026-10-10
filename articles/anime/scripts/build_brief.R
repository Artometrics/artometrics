#!/usr/bin/env Rscript
# Anime greenlight brief.
# One command from the repo root: npm run brief:anime
#
# Reads the raw TidyTuesday tidy_anime.csv (77,911 rows), collapses to one row
# per animeID before any title-level count, and writes the five charts plus
# the derived tables the page publishes.

suppressPackageStartupMessages({
  library(tidyverse)
  library(jsonlite)
})

args_all <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args_all, value = TRUE)
script_path <- if (length(file_arg)) {
  normalizePath(sub("^--file=", "", file_arg[[1]]))
} else {
  normalizePath("articles/anime/scripts/build_brief.R")
}
repo_root <- normalizePath(file.path(dirname(script_path), "../../.."))
article_dir <- file.path(repo_root, "articles/anime")
raw_dir <- file.path(article_dir, "data/raw")
raw_csv <- file.path(raw_dir, "tidy_anime.csv")
charts_dir <- file.path(article_dir, "charts")
public_dir <- file.path(repo_root, "public/data/articles/anime")
dir.create(raw_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(charts_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(public_dir, recursive = TRUE, showWarnings = FALSE)

expected_sha <- "5ea3a14492b5c559c728af0c7ec57b81c919d0efa4d381e54b0f7cde9934a1c2"
source_url <- "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-04-23/tidy_anime.csv"
source_page <- "https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-04-23"

sha256_file <- function(path) {
  unname(tools::md5sum(path)) # placeholder replaced below
}
# tools has md5sum, not sha256. Use openssl.
sha256_file <- function(path) {
  line <- system2("sha256sum", shQuote(path), stdout = TRUE)
  strsplit(line, " ", fixed = TRUE)[[1]][[1]]
}

if (!file.exists(raw_csv)) {
  message("Downloading tidy_anime.csv")
  download.file(source_url, raw_csv, mode = "wb", quiet = TRUE)
}
got_sha <- sha256_file(raw_csv)
if (!identical(got_sha, expected_sha)) {
  stop("SHA-256 mismatch for tidy_anime.csv: ", got_sha)
}

RED <- "#E60000"
INK <- "#1C1C1E"
GRAY <- "#6B6B6B"
PALE <- "#B5B5B5"
GRID <- "#E6E6E6"
BASELINE <- 6.38

title_family <- "sans"
body_family <- "sans"
if (requireNamespace("showtext", quietly = TRUE) && requireNamespace("sysfonts", quietly = TRUE)) {
  sysfonts::font_add("Anton", file.path(repo_root, "assets/fonts/Anton-Regular.ttf"))
  sysfonts::font_add("DM Sans", file.path(repo_root, "assets/fonts/DMSans.ttf"))
  showtext::showtext_auto(enable = TRUE)
  showtext::showtext_opts(dpi = 160)
  title_family <- "Anton"
  body_family <- "DM Sans"
}

theme_brief <- function() {
  theme_minimal(base_size = 12, base_family = body_family) +
    theme(
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA),
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(color = GRID, linewidth = 0.3),
      axis.title = element_text(color = "#525252", family = body_family),
      axis.text = element_text(color = INK, family = body_family),
      plot.title = element_text(family = title_family, face = "plain", size = 15, hjust = 0, color = "black"),
      plot.subtitle = element_text(family = body_family, color = "#525252", hjust = 0, size = 9.5),
      plot.caption = element_text(family = body_family, color = "#525252", hjust = 0, size = 8),
      strip.text = element_text(family = title_family, hjust = 0, color = INK, size = 11),
      legend.position = "bottom",
      legend.text = element_text(family = body_family, color = INK),
      plot.margin = margin(12, 14, 10, 12)
    )
}

caption_src <- "MyAnimeList via TidyTuesday (Kaggle snapshot, early 2019). One row per title."

write_plotly <- function(name, data, layout) {
  payload <- list(
    data = data,
    layout = modifyList(
      list(
        paper_bgcolor = "#FFFFFF",
        plot_bgcolor = "#FFFFFF",
        font = list(family = "DM Sans, Helvetica, Arial, sans-serif", color = INK, size = 13),
        margin = list(t = 64, r = 24, b = 48, l = 64)
      ),
      layout
    ),
    config = list(
      displayModeBar = FALSE,
      displaylogo = FALSE,
      responsive = TRUE,
      scrollZoom = FALSE,
      staticPlot = FALSE
    )
  )
  write_json(payload, file.path(charts_dir, paste0(name, ".plotly.json")), auto_unbox = TRUE, null = "null")
}

save_plot <- function(plot, name, width, height) {
  ggsave(
    file.path(charts_dir, paste0(name, ".png")),
    plot,
    width = width,
    height = height,
    dpi = 160,
    bg = "white"
  )
}

# Drop leftover charts from earlier cuts so only this brief's five ship.
old <- list.files(charts_dir, full.names = TRUE)
if (length(old)) file.remove(old)

raw <- read_csv(raw_csv, show_col_types = FALSE, progress = FALSE)
stopifnot(nrow(raw) == 77911)

raw <- raw %>%
  mutate(
    score = suppressWarnings(as.numeric(score)),
    members = suppressWarnings(as.numeric(members)),
    scored_by = suppressWarnings(as.numeric(scored_by)),
    popularity = suppressWarnings(as.numeric(popularity)),
    year = as.integer(substr(start_date, 1, 4)),
    studio = if_else(is.na(studio), "", studio),
    genre = if_else(is.na(genre), "", genre),
    related = if_else(is.na(related), "", related),
    is_sequel = str_detect(related, "'Prequel'\\s*:") |
      str_detect(related, "'Parent story'\\s*:") |
      str_detect(related, "'Full story'\\s*:")
  )

# Title-level: one row per animeID. Repeated studio/genre rows carry the same score.
titles <- raw %>%
  arrange(animeID) %>%
  distinct(animeID, .keep_all = TRUE)
stopifnot(nrow(titles) == 13631)

scored <- titles %>% filter(!is.na(score))
stopifnot(nrow(scored) == 13518)
stopifnot(median(scored$score) == BASELINE)

tv <- titles %>% filter(type == "TV")
tv_scored <- tv %>% filter(!is.na(score))
stopifnot(nrow(tv) == 4260)
stopifnot(nrow(tv_scored) == 4240)

source_levels <- c("Light novel", "Manga", "Novel", "Original", "Game")
source_tbl <- tv_scored %>%
  filter(source %in% source_levels) %>%
  group_by(source) %>%
  summarise(
    n = n(),
    median_score = median(score),
    q1 = quantile(score, 0.25, type = 7),
    q3 = quantile(score, 0.75, type = 7),
    median_members = median(members),
    n_ge_8 = sum(score >= 8),
    .groups = "drop"
  ) %>%
  mutate(
    share_ge_8 = n_ge_8 / n,
    source = factor(source, levels = source_levels)
  ) %>%
  arrange(source)

stopifnot(source_tbl$n == c(283, 1232, 122, 1012, 210))
stopifnot(source_tbl$median_score == c(7.35, 7.29, 7.13, 6.63, 6.63))
stopifnot(source_tbl$n_ge_8 == c(37, 210, 19, 47, 1))

reach <- scored %>% filter(!is.na(members), members > 0)
stopifnot(nrow(reach) == 13518)
spearman <- cor(reach$score, reach$members, method = "spearman")
pearson <- cor(reach$score, reach$members, method = "pearson")
pearson_log <- cor(reach$score, log(reach$members), method = "pearson")
stopifnot(round(spearman, 2) == 0.74)
stopifnot(abs(pearson - 0.38942848408708325) < 1e-9)

studio_rows <- raw %>%
  filter(!is.na(score), studio != "") %>%
  distinct(animeID, studio, .keep_all = TRUE)

league <- studio_rows %>%
  group_by(studio) %>%
  summarise(
    n = n(),
    median_score = median(score),
    q1 = quantile(score, 0.25, type = 7),
    q3 = quantile(score, 0.75, type = 7),
    n_ge_8 = sum(score >= 8),
    .groups = "drop"
  ) %>%
  mutate(iqr = q3 - q1, share_ge_8 = n_ge_8 / n) %>%
  filter(n >= 100) %>%
  arrange(desc(median_score), studio)

stopifnot(nrow(league) == 20)
stopifnot(league$studio[[1]] == "Bones")
stopifnot(league$n[league$studio == "Bones"] == 115)
stopifnot(league$n[league$studio == "OLM"] == 209)
stopifnot(league$n[league$studio == "Kyoto Animation"] == 110)
stopifnot(league$n[league$studio == "Toei Animation"] == 737)
stopifnot(league$n_ge_8[league$studio == "Toei Animation"] == 21)
stopifnot(league$median_score[league$studio == "Bones"] == 7.46)
stopifnot(league$median_score[league$studio == "DLE"] == 5.40)

# Tightest-IQR rank among the 20, 1 = tightest. Bones should be 7th.
league <- league %>% mutate(iqr_rank = rank(iqr, ties.method = "min"))
stopifnot(league$iqr_rank[league$studio == "Bones"] == 7)
stopifnot(league$studio[which.min(league$iqr)] == "OLM")

genre_rows <- raw %>%
  filter(!is.na(score), genre != "") %>%
  distinct(animeID, genre, .keep_all = TRUE)
genre_tbl <- genre_rows %>%
  group_by(genre) %>%
  summarise(n = n(), median_score = median(score), .groups = "drop")
stopifnot(genre_tbl$n[genre_tbl$genre == "Thriller"] == 102)
stopifnot(genre_tbl$n[genre_tbl$genre == "Kids"] == 2158)
stopifnot(genre_tbl$n[genre_tbl$genre == "Music"] == 1510)
stopifnot(round(genre_tbl$median_score[genre_tbl$genre == "Thriller"], 2) == 7.49)
stopifnot(round(genre_tbl$median_score[genre_tbl$genre == "Kids"], 2) == 5.86)
stopifnot(round(genre_tbl$median_score[genre_tbl$genre == "Music"], 2) == 5.44)

sequel_tv <- tv_scored %>% filter(is_sequel)
other_tv <- tv_scored %>% filter(!is_sequel)
stopifnot(nrow(sequel_tv) == 1084)
stopifnot(nrow(other_tv) == 3156)
stopifnot(median(sequel_tv$score) == 7.02)
stopifnot(median(other_tv$score) == 6.73)
stopifnot(sum(sequel_tv$score >= 8) == 159)
stopifnot(sum(other_tv$score >= 8) == 187)

buried_78 <- scored %>% filter(score >= 8, popularity > 3000)
buried_43 <- buried_78 %>% filter(scored_by >= 1000)
stopifnot(nrow(buried_78) == 78)
stopifnot(nrow(buried_43) == 43)
stopifnot(sum(buried_43$is_sequel) == 30)
shortlist <- buried_43 %>%
  filter(!is_sequel, type %in% c("TV", "Movie")) %>%
  arrange(desc(score), popularity)
stopifnot(nrow(shortlist) == 10)

format_years <- titles %>%
  filter(!is.na(year), year <= 2018, type %in% c("TV", "Movie", "OVA", "ONA", "Special", "Music")) %>%
  count(year, type, name = "n")
ova_1993 <- format_years %>% filter(type == "OVA", year == 1993) %>% pull(n)
stopifnot(ova_1993 == 115)
ona_expect <- c(`2009` = 40, `2011` = 67, `2013` = 104, `2015` = 120, `2016` = 162, `2017` = 214, `2018` = 216)
for (yr in names(ona_expect)) {
  got <- format_years %>% filter(type == "ONA", year == as.integer(yr)) %>% pull(n)
  stopifnot(got == unname(ona_expect[[yr]]))
}

parse_minutes <- function(x) {
  x <- tolower(ifelse(is.na(x), "", x))
  hr <- suppressWarnings(as.numeric(str_match(x, "(\\d+)\\s*hr")[, 2]))
  mn <- suppressWarnings(as.numeric(str_match(x, "(\\d+)\\s*min")[, 2]))
  sec <- suppressWarnings(as.numeric(str_match(x, "(\\d+)\\s*sec")[, 2]))
  out <- ifelse(is.na(hr), 0, hr * 60) + ifelse(is.na(mn), 0, mn) + ifelse(is.na(sec), 0, sec / 60)
  known <- !is.na(hr) | !is.na(mn) | !is.na(sec)
  ifelse(known, out, NA_real_)
}

duration_median <- function(studio_name) {
  studio_rows %>%
    filter(studio == studio_name) %>%
    mutate(minutes = parse_minutes(duration)) %>%
    filter(!is.na(minutes)) %>%
    pull(minutes) %>%
    median()
}
stopifnot(duration_median("DLE") == 3)
stopifnot(duration_median("Bones") == 24)
stopifnot(duration_median("OLM") == 24)

# Analyst display table, used only to record rounding differences. The page
# keeps the locked figures. This script does not rewrite them.
analyst <- tribble(
  ~studio, ~n, ~median_score, ~q1, ~q3, ~iqr, ~share,
  "Bones", 115, 7.46, 6.95, 7.90, 0.95, 23.5,
  "Kyoto Animation", 110, 7.43, 6.67, 7.89, 1.21, 20.9,
  "A-1 Pictures", 190, 7.30, 6.70, 7.73, 1.03, 14.7,
  "Shaft", 125, 7.25, 6.65, 7.86, 1.21, 16.8,
  "Studio Deen", 264, 7.20, 6.53, 7.62, 1.10, 8.3,
  "Production I.G", 297, 7.16, 6.46, 7.71, 1.25, 13.5,
  "Madhouse", 340, 7.03, 6.46, 7.61, 1.15, 15.9,
  "Gonzo", 123, 7.01, 6.40, 7.32, 0.93, 2.4,
  "J.C.Staff", 322, 7.01, 6.25, 7.42, 1.17, 7.5,
  "Sunrise", 457, 7.00, 6.43, 7.46, 1.03, 6.8,
  "TMS Entertainment", 275, 6.99, 6.28, 7.53, 1.25, 10.2,
  "Xebec", 146, 6.98, 6.57, 7.37, 0.80, 2.1,
  "Studio Pierrot", 251, 6.87, 6.26, 7.48, 1.21, 6.0,
  "AIC", 111, 6.82, 6.30, 7.22, 0.92, 0.9,
  "Toei Animation", 737, 6.68, 6.16, 7.23, 1.07, 2.8,
  "Nippon Animation", 206, 6.67, 6.31, 7.12, 0.81, 3.4,
  "OLM", 209, 6.64, 6.36, 7.06, 0.70, 0.5,
  "Shin-Ei Animation", 156, 6.63, 6.08, 7.25, 1.17, 0.6,
  "Tatsunoko Production", 158, 6.52, 6.14, 7.00, 0.86, 3.8,
  "DLE", 153, 5.40, 4.96, 5.94, 0.98, 0.7
)

shown <- league %>%
  transmute(
    studio,
    n,
    median_score = round(median_score, 2),
    q1 = round(q1, 2),
    q3 = round(q3, 2),
    iqr = round(iqr, 2),
    share = round(100 * share_ge_8, 1)
  )
cmp <- shown %>% inner_join(analyst, by = "studio", suffix = c("_r", "_analyst"))
diffs <- cmp %>%
  filter(
    n_r != n_analyst |
      median_score_r != median_score_analyst |
      q1_r != q1_analyst |
      q3_r != q3_analyst |
      iqr_r != iqr_analyst |
      share_r != share_analyst
  )

notes <- c(
  "Rounding: quantiles are type 7. Display rounding uses R's round(), applied to the raw quantile, not to an already-rounded quartile.",
  sprintf("Spearman score vs members = %.6f (n = %d), displayed 0.74.", spearman, nrow(reach)),
  sprintf("Pearson score vs members = %.6f, displayed 0.389 in the locked copy.", pearson),
  sprintf("Pearson score vs log(members) = %.6f, displayed 0.72.", pearson_log),
  sprintf(
    "Non-sequel TV median members raw = %.1f. R round() = %.0f. Locked copy displays 8,013.",
    median(other_tv$members),
    round(median(other_tv$members))
  ),
  sprintf(
    "Sequel TV median members raw = %.1f, R round() = %.0f (locked 11,430).",
    median(sequel_tv$members),
    round(median(sequel_tv$members))
  )
)
dle_known <- studio_rows %>%
  filter(studio == "DLE") %>%
  mutate(minutes = parse_minutes(duration)) %>%
  filter(!is.na(minutes))
notes <- c(
  notes,
  sprintf(
    "DLE episode length: median %s minutes on %d scored titles with a parsed duration, of %d scored titles. Share at or under 5 minutes = %d/%d = %.1f%%. The locked draft's 78%% figure does not reproduce; the page uses the verified 3-minute median instead.",
    format(median(dle_known$minutes), nsmall = 1),
    nrow(dle_known),
    league$n[league$studio == "DLE"],
    sum(dle_known$minutes <= 5),
    nrow(dle_known),
    100 * mean(dle_known$minutes <= 5)
  )
)
if (nrow(diffs)) {
  notes <- c(notes, "League cells where R round() differs from the analyst display table (page keeps the analyst/locked figures):")
  notes <- c(notes, capture.output(print(diffs, n = 30)))
} else {
  notes <- c(notes, "League display table matches R round() on n, median, quartiles, IQR, and share.")
}

writeLines(notes, file.path(article_dir, "data/discrepancies.txt"))
writeLines(
  c(
    paste("url:", source_page),
    paste("download:", source_url),
    "file: tidy_anime.csv",
    paste("sha256:", expected_sha),
    "snapshot: Kaggle MyAnimeList scrape by Tam Nguyen, early 2019, published by TidyTuesday on 2019-04-23.",
    "dedup: title-level stats are one row per animeID; studio stats are one row per animeID x studio; genre stats are one row per animeID x genre.",
    "sequel: related lists a Prequel, Parent story, or Full story.",
    "quantiles: type 7. Correlations: Spearman on score and members; Pearson reported only as the raw and log comparisons in the text."
  ),
  file.path(article_dir, "data/SOURCE.txt")
)
writeLines(capture.output(sessionInfo()), file.path(article_dir, "data/sessionInfo.txt"))

studio_list <- studio_rows %>%
  group_by(animeID) %>%
  summarise(studios = paste(sort(unique(studio)), collapse = ", "), .groups = "drop")
genre_list <- genre_rows %>%
  group_by(animeID) %>%
  summarise(genres = paste(sort(unique(genre)), collapse = ", "), .groups = "drop")

titles_out <- titles %>%
  left_join(studio_list, by = "animeID") %>%
  left_join(genre_list, by = "animeID") %>%
  transmute(
    animeID, name, title_english, type, source, year, episodes, duration, rating,
    score, scored_by, popularity, members, is_sequel, studios, genres
  )
readr::write_csv(titles_out, file.path(article_dir, "data/titles.csv"))
readr::write_csv(source_tbl, file.path(article_dir, "data/tv_by_source.csv"))
readr::write_csv(league, file.path(article_dir, "data/studios.csv"))
readr::write_csv(genre_tbl, file.path(article_dir, "data/genres.csv"))
readr::write_csv(
  shortlist %>% transmute(animeID, name, title_english, type, year, source, score, scored_by, popularity, members),
  file.path(article_dir, "data/shortlist.csv")
)
readr::write_csv(format_years, file.path(article_dir, "data/format_years.csv"))

# --- charts ---
eras <- format_years %>%
  mutate(type = factor(type, levels = c("TV", "Movie", "OVA", "ONA", "Special", "Music"))) %>%
  complete(year = 1960:2018, type, fill = list(n = 0)) %>%
  filter(year >= 1960)

p_eras <- ggplot(eras, aes(year, n)) +
  geom_col(fill = "#4A4A4A", width = 1) +
  geom_col(data = filter(eras, type == "OVA", year == 1993), fill = RED, width = 1) +
  geom_col(data = filter(eras, type == "ONA", year == 2018), fill = RED, width = 1) +
  facet_wrap(~type, scales = "free_y", ncol = 3) +
  labs(
    title = "Each wave lines up with a new channel",
    subtitle = "Titles by first year, through 2018. OVA peaks at 115 in 1993. ONA reaches 216 in 2018. Panels do not share a vertical scale.",
    x = NULL, y = "Titles",
    caption = caption_src
  ) +
  theme_brief()
save_plot(p_eras, "chart_eras", 11.2, 6.8)
write_plotly(
  "chart_eras",
  list(list(
    type = "bar",
    x = eras$year,
    y = eras$n,
    marker = list(color = "#4A4A4A"),
    transforms = list(list(type = "groupby", groups = eras$type))
  )),
  list(title = list(text = "Releases by year and format, through 2018"), barmode = "group")
)

scorecard <- source_tbl %>% mutate(source = as.character(source))
p1 <- ggplot(scorecard, aes(source, median_members, fill = source == "Light novel")) +
  geom_col(width = 0.72) +
  scale_y_log10(labels = scales::comma) +
  scale_fill_manual(values = c(`TRUE` = RED, `FALSE` = "#4A4A4A"), guide = "none") +
  labs(x = NULL, y = "Median members") +
  theme_brief() +
  theme(axis.text.x = element_text(size = 8))
p2 <- ggplot(scorecard, aes(source, 100 * share_ge_8, fill = source == "Manga")) +
  geom_col(width = 0.72) +
  scale_fill_manual(values = c(`TRUE` = RED, `FALSE` = "#4A4A4A"), guide = "none") +
  labs(x = NULL, y = "Share scoring 8.0 or higher (%)") +
  theme_brief() +
  theme(axis.text.x = element_text(size = 8))
png(
  file.path(charts_dir, "chart_scorecard.png"),
  width = 11.2, height = 6.4, units = "in", res = 160, bg = "white"
)
grid::grid.newpage()
grid::pushViewport(grid::viewport(layout = grid::grid.layout(
  3, 2,
  heights = grid::unit(c(0.9, 4.6, 0.7), "in")
)))
grid::grid.text(
  "Light novels set the audience floor. Manga produces more 8.0s.",
  x = 0.02, y = 0.65, just = c("left", "center"),
  gp = grid::gpar(fontfamily = title_family, fontsize = 15)
)
grid::grid.text(
  "Scored television only (n = 4,240 of 4,260 TV titles). Left axis is a log scale.",
  x = 0.02, y = 0.15, just = c("left", "center"),
  gp = grid::gpar(fontfamily = body_family, fontsize = 9, col = "#525252")
)
print(p1 + theme(plot.caption = element_blank()), vp = grid::viewport(layout.pos.row = 2, layout.pos.col = 1))
print(p2 + theme(plot.caption = element_blank()), vp = grid::viewport(layout.pos.row = 2, layout.pos.col = 2))
grid::grid.text(
  caption_src, x = 0.02, just = "left",
  gp = grid::gpar(fontfamily = body_family, fontsize = 8, col = "#525252"),
  vp = grid::viewport(layout.pos.row = 3, layout.pos.col = 1:2)
)
dev.off()
write_plotly(
  "chart_scorecard",
  list(
    list(type = "bar", name = "Median members", x = scorecard$source, y = scorecard$median_members, marker = list(color = ifelse(scorecard$source == "Light novel", RED, "#4A4A4A"))),
    list(type = "bar", name = "Share at or above 8.0", x = scorecard$source, y = round(100 * scorecard$share_ge_8, 1), xaxis = "x2", yaxis = "y2", marker = list(color = ifelse(scorecard$source == "Manga", RED, "#4A4A4A")))
  ),
  list(
    title = list(text = "TV source: median members and share at 8.0"),
    xaxis = list(domain = c(0, 0.45)),
    yaxis = list(type = "log", title = list(text = "Median members")),
    xaxis2 = list(domain = c(0.55, 1), anchor = "y2"),
    yaxis2 = list(anchor = "x2", title = list(text = "Share at or above 8.0 (%)"))
  )
)

league_plot <- league %>%
  mutate(
    studio_label = paste0(studio, "   n=", n),
    studio_label = factor(studio_label, levels = rev(studio_label)),
    focal = studio %in% c("Bones", "Kyoto Animation", "OLM")
  )
p_league <- ggplot(league_plot, aes(median_score, studio_label)) +
  geom_errorbarh(aes(xmin = q1, xmax = q3, color = focal), height = 0, linewidth = 0.8) +
  geom_point(aes(size = n, color = focal)) +
  geom_vline(xintercept = BASELINE, linetype = "dashed", color = GRAY, linewidth = 0.4) +
  scale_color_manual(values = c(`TRUE` = RED, `FALSE` = "#4A4A4A"), guide = "none") +
  scale_size_area(max_size = 8, guide = "none") +
  labs(
    title = "Bones has the tightest spread among the top-scoring studios",
    subtitle = "Studios with at least 100 scored titles, sorted by median. Bars are the middle half of scores. Dashed line: catalog median 6.38.",
    x = "Median score", y = NULL,
    caption = paste0(caption_src, " DLE (n = 153) mostly makes short-form titles, with a median episode of 3 minutes, so its median score isn't directly comparable to studios making 24-minute episodes.")
  ) +
  theme_brief()
save_plot(p_league, "chart_studios", 11.2, 8.4)
write_plotly(
  "chart_studios",
  list(list(
    type = "scatter",
    mode = "markers",
    x = league$median_score,
    y = league$studio,
    marker = list(
      size = pmax(8, league$n / 40),
      color = ifelse(league$studio %in% c("Bones", "Kyoto Animation", "OLM"), RED, "#4A4A4A")
    ),
    error_x = list(
      type = "data",
      array = league$q3 - league$median_score,
      arrayminus = league$median_score - league$q1,
      color = "#4A4A4A"
    )
  )),
  list(
    title = list(text = "Studio median and IQR, n at least 100"),
    xaxis = list(title = list(text = "Median score")),
    shapes = list(list(type = "line", x0 = BASELINE, x1 = BASELINE, y0 = 0, y1 = 1, yref = "paper", line = list(dash = "dash", color = GRAY)))
  )
)

seq_long <- bind_rows(
  sequel_tv %>% transmute(score, group = "Sequel"),
  other_tv %>% transmute(score, group = "Not a sequel")
) %>%
  mutate(group = factor(group, levels = c("Not a sequel", "Sequel")))
meds <- seq_long %>% group_by(group) %>% summarise(median_score = median(score), n = n(), .groups = "drop")
p_seq <- ggplot(seq_long, aes(score, fill = group)) +
  geom_histogram(bins = 28, position = "identity", alpha = 0.85, color = NA) +
  geom_vline(data = meds, aes(xintercept = median_score, color = group), linetype = "dashed", linewidth = 0.5) +
  geom_vline(xintercept = BASELINE, color = INK, linetype = "dashed", linewidth = 0.3) +
  scale_fill_manual(values = c("Not a sequel" = "#8A8A8A", "Sequel" = RED)) +
  scale_color_manual(values = c("Not a sequel" = "#4A4A4A", "Sequel" = RED), guide = "none") +
  labs(
    title = "TV sequels score higher because only shows that already did well get one",
    subtitle = sprintf(
      "Sequels n = %s, median %.2f. Others n = %s, median %.2f. This is selection, not an effect of making a sequel. Solid gray line: catalog median.",
      format(nrow(sequel_tv), big.mark = ","),
      median(sequel_tv$score),
      format(nrow(other_tv), big.mark = ","),
      median(other_tv$score)
    ),
    x = "Score", y = "Titles", fill = NULL,
    caption = caption_src
  ) +
  theme_brief()
save_plot(p_seq, "chart_sequel", 11.2, 6.2)
write_plotly(
  "chart_sequel",
  list(
    list(type = "histogram", name = "Not a sequel", x = other_tv$score, marker = list(color = "#8A8A8A"), opacity = 0.85),
    list(type = "histogram", name = "Sequel", x = sequel_tv$score, marker = list(color = RED), opacity = 0.75)
  ),
  list(barmode = "overlay", title = list(text = "TV sequel and non-sequel scores"), xaxis = list(title = list(text = "Score")))
)

short_ids <- shortlist$animeID
reach_plot <- reach %>% mutate(on_shortlist = animeID %in% short_ids)
p_reach <- ggplot(reach_plot, aes(members, score)) +
  geom_point(data = filter(reach_plot, !on_shortlist), color = PALE, alpha = 0.35, size = 0.7) +
  geom_point(data = filter(reach_plot, on_shortlist), color = RED, size = 2.2) +
  geom_hline(yintercept = BASELINE, linetype = "dashed", color = INK, linewidth = 0.35) +
  scale_x_log10(labels = scales::comma) +
  labs(
    title = "Score and reach move together (Spearman 0.74)",
    subtitle = "n = 13,518 scored titles. Red points are the 10-title editorial shortlist. Dashed line: catalog median 6.38.",
    x = "Members", y = "Score",
    caption = caption_src
  ) +
  theme_brief()
save_plot(p_reach, "chart_reach", 11.2, 6.6)
write_plotly(
  "chart_reach",
  list(
    list(type = "scatter", mode = "markers", name = "Scored titles", x = reach_plot$members[!reach_plot$on_shortlist], y = reach_plot$score[!reach_plot$on_shortlist], marker = list(size = 4, color = PALE, opacity = 0.35)),
    list(type = "scatter", mode = "markers", name = "Shortlist", x = reach_plot$members[reach_plot$on_shortlist], y = reach_plot$score[reach_plot$on_shortlist], marker = list(size = 8, color = RED))
  ),
  list(
    title = list(text = "Score vs members, Spearman 0.74"),
    xaxis = list(type = "log", title = list(text = "Members")),
    yaxis = list(title = list(text = "Score")),
    shapes = list(list(type = "line", x0 = 0, x1 = 1, xref = "paper", y0 = BASELINE, y1 = BASELINE, line = list(dash = "dash", color = INK)))
  )
)

zip_files <- c(
  file.path(article_dir, "scripts/build_brief.R"),
  file.path(article_dir, "data/titles.csv"),
  file.path(article_dir, "data/tv_by_source.csv"),
  file.path(article_dir, "data/studios.csv"),
  file.path(article_dir, "data/genres.csv"),
  file.path(article_dir, "data/shortlist.csv"),
  file.path(article_dir, "data/format_years.csv"),
  file.path(article_dir, "data/SOURCE.txt"),
  file.path(article_dir, "data/sessionInfo.txt"),
  file.path(article_dir, "data/discrepancies.txt")
)
zip_out <- file.path(public_dir, "source.zip")
if (file.exists(zip_out)) file.remove(zip_out)
utils::zip(zip_out, zip_files, flags = "-j")
file.copy(zip_out, file.path(article_dir, "source.zip"), overwrite = TRUE)

message("Wrote charts to ", charts_dir)
message("Spearman ", round(spearman, 3), " Pearson ", round(pearson, 3), " log ", round(pearson_log, 3))
message("Discrepancies: ", file.path(article_dir, "data/discrepancies.txt"))
