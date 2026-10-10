#!/usr/bin/env Rscript
# Anime greenlight brief.
# One command from the repo root: npm run brief:anime
#
# Reads the raw TidyTuesday tidy_anime.csv (77,911 rows), collapses to one row
# per animeID before any title-level count, and writes the five charts plus
# the derived tables the page publishes.

# Fresh machines do not have a user library yet. Install the packages this
# script loads so `npm run brief:anime` is one command. Versions are pinned
# in articles/anime/renv.lock; this path installs current CRAN releases of
# anything still missing, then continues.
ensure_brief_packages <- function(pkgs) {
  user_lib <- Sys.getenv("R_LIBS_USER")
  if (!nzchar(user_lib)) {
    minor <- strsplit(R.version$minor, ".", fixed = TRUE)[[1]][[1]]
    user_lib <- file.path(
      Sys.getenv("HOME"),
      "R",
      paste0(R.version$platform, "-library"),
      paste0(R.version$major, ".", minor)
    )
  }
  dir.create(user_lib, recursive = TRUE, showWarnings = FALSE)
  .libPaths(c(user_lib, .libPaths()))
  missing <- pkgs[!vapply(pkgs, requireNamespace, quietly = TRUE, FUN.VALUE = logical(1))]
  if (length(missing)) {
    message("Installing R packages into ", user_lib, ": ", paste(missing, collapse = ", "))
    install.packages(
      missing,
      lib = user_lib,
      repos = "https://cloud.r-project.org",
      dependencies = c("Depends", "Imports", "LinkingTo")
    )
  }
  failed <- pkgs[!vapply(pkgs, requireNamespace, quietly = TRUE, FUN.VALUE = logical(1))]
  if (length(failed)) {
    stop(
      "Could not install: ", paste(failed, collapse = ", "),
      ". From the repo root: Rscript -e 'install.packages(c(\"tidyverse\", \"jsonlite\", \"showtext\", \"sysfonts\"), repos=\"https://cloud.r-project.org\")'"
    )
  }
}
ensure_brief_packages(c("tidyverse", "jsonlite", "showtext", "sysfonts"))

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

library(showtext)
sysfonts::font_add("Anton", file.path(repo_root, "assets/fonts/Anton-Regular.ttf"))
sysfonts::font_add("DM Sans", file.path(repo_root, "assets/fonts/DMSans.ttf"))
showtext::showtext_auto(enable = TRUE)
showtext::showtext_opts(dpi = 160)
title_family <- "Anton"
body_family <- "DM Sans"

# Round half up on the exact decimal. Never R's round(), which uses banker's rounding.
round_half_up <- function(x, d) {
  sign(x) * floor(abs(x) * 10^d + 0.5 + 1e-9) / 10^d
}
fmt_fixed <- function(x, d) {
  trimws(format(round_half_up(x, d), nsmall = d, scientific = FALSE, trim = TRUE))
}
fmt_int <- function(x) {
  trimws(format(round_half_up(x, 0), big.mark = ",", scientific = FALSE, trim = TRUE))
}
# Published summary stats: 4 decimal places, trailing zeros dropped, so a
# downloader's own half-up lands on the page figures (1.215 -> 1.22, 6.565 -> 6.57).
fmt_publish <- function(x, d = 4) {
  rounded <- round_half_up(x, d)
  s <- sprintf(paste0("%.", d, "f"), rounded)
  s <- sub("0+$", "", s)
  s <- sub("\\.$", "", s)
  ifelse(is.na(rounded), NA_character_, s)
}
publish_csv <- function(df, path, cols, digits = 4) {
  out <- as.data.frame(df)
  for (col in intersect(cols, names(out))) {
    out[[col]] <- fmt_publish(out[[col]], digits)
  }
  readr::write_csv(out, path)
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
        margin = list(t = 100, r = 28, b = 56, l = 72),
        title = list(x = 0, xanchor = "left", font = list(family = "Anton, Impact, sans-serif", size = 18, color = "#111111"))
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
  write_json(
    payload,
    file.path(charts_dir, paste0(name, ".plotly.json")),
    auto_unbox = TRUE,
    null = "null",
    digits = 4
  )
}

chart_title <- function(title, subtitle = NULL) {
  text <- paste0("<span style=\"font-family:Anton,Impact,sans-serif;\">", title, "</span>")
  if (!is.null(subtitle) && nzchar(subtitle)) {
    text <- paste0(
      text,
      "<br><span style=\"font-family:'DM Sans',Helvetica,Arial,sans-serif;font-size:12px;color:#525252;\">",
      subtitle,
      "</span>"
    )
  }
  list(
    text = text,
    x = 0,
    xanchor = "left",
    font = list(family = "Anton, Impact, sans-serif", size = 18, color = "#111111")
  )
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
stopifnot(fmt_fixed(genre_tbl$median_score[genre_tbl$genre == "Thriller"], 2) == "7.50")
stopifnot(fmt_fixed(genre_tbl$median_score[genre_tbl$genre == "Mystery"], 2) == "7.27")
stopifnot(fmt_fixed(genre_tbl$median_score[genre_tbl$genre == "Psychological"], 2) == "7.23")
stopifnot(fmt_fixed(genre_tbl$median_score[genre_tbl$genre == "Kids"], 2) == "5.86")
stopifnot(fmt_fixed(genre_tbl$median_score[genre_tbl$genre == "Music"], 2) == "5.44")

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

# Display figures use round-half-up. The page tables and the sentences that
# quote them are written from this output.
pick <- function(frame, studio, col) frame[[col]][frame$studio == studio]

league_disp <- league %>%
  transmute(
    studio,
    n = as.integer(n),
    median = round_half_up(median_score, 2),
    q1 = round_half_up(q1, 2),
    q3 = round_half_up(q3, 2),
    iqr = round_half_up(iqr, 2),
    share = round_half_up(100 * share_ge_8, 1),
    focal = studio %in% c("Bones", "Kyoto Animation", "OLM")
  )

stopifnot(fmt_fixed(pick(league, "Kyoto Animation", "iqr"), 2) == "1.22")
stopifnot(fmt_fixed(pick(league, "A-1 Pictures", "median_score"), 2) == "7.31")
stopifnot(fmt_fixed(pick(league, "Xebec", "median_score"), 2) == "6.99")
stopifnot(fmt_fixed(pick(league, "Tatsunoko Production", "median_score"), 2) == "6.53")
stopifnot(fmt_fixed(pick(league, "Madhouse", "q1"), 2) == "6.47")
stopifnot(fmt_fixed(pick(league, "Studio Pierrot", "q1"), 2) == "6.27")
stopifnot(fmt_fixed(pick(league, "Studio Deen", "q3"), 2) == "7.63")
stopifnot(fmt_fixed(pick(league, "Gonzo", "q3"), 2) == "7.33")
stopifnot(fmt_fixed(pick(league, "Tatsunoko Production", "q3"), 2) == "7.01")
stopifnot(fmt_fixed(pick(league, "TMS Entertainment", "iqr"), 2) == "1.26")
stopifnot(fmt_fixed(pick(league, "AIC", "iqr"), 2) == "0.93")
stopifnot(fmt_int(median(other_tv$members)) == "8,013")
stopifnot(fmt_int(median(sequel_tv$members)) == "11,430")
stopifnot(league$iqr_rank[league$studio == "Bones"] == 7)
stopifnot(sum(buried_43$is_sequel) == 30)
stopifnot(nrow(buried_43) == 43)

million <- titles %>% filter(!is.na(members), members >= 1000000)
stopifnot(nrow(million) == 13)
top_title <- titles %>% slice_max(members, n = 1, with_ties = FALSE)
stopifnot(top_title$members == 1610561)
stopifnot(any(grepl("Death Note", c(top_title$name, top_title$title_english))))

source_disp <- source_tbl %>%
  mutate(
    source = as.character(source),
    n_lab = fmt_int(n),
    median_lab = fmt_fixed(median_score, 2),
    members_lab = fmt_int(median_members),
    share_lab = paste0(fmt_fixed(100 * share_ge_8, 1), "%"),
    members_d = round_half_up(median_members, 0),
    share_d = round_half_up(100 * share_ge_8, 1)
  )
stopifnot(source_disp$members_lab[source_disp$source == "Light novel"] == "153,184")
stopifnot(source_disp$members_lab[source_disp$source == "Manga"] == "37,500")
stopifnot(source_disp$members_lab[source_disp$source == "Original"] == "4,738")
stopifnot(source_disp$share_lab[source_disp$source == "Manga"] == "17.0%")
stopifnot(source_disp$share_lab[source_disp$source == "Game"] == "0.5%")

dle_known <- studio_rows %>%
  filter(studio == "DLE") %>%
  mutate(minutes = parse_minutes(duration)) %>%
  filter(!is.na(minutes))
dle_short <- sum(dle_known$minutes <= 5)
dle_known_n <- nrow(dle_known)
stopifnot(dle_short == 114)
stopifnot(dle_known_n == 148)
stopifnot(fmt_fixed(100 * dle_short / dle_known_n, 1) == "77.0")

gmed <- function(name) fmt_fixed(genre_tbl$median_score[genre_tbl$genre == name], 2)
gn <- function(name) fmt_int(genre_tbl$n[genre_tbl$genre == name])

notes <- c(
  "Display rounding is round-half-up on the exact decimal: sign(x) * floor(abs(x) * 10^d + 0.5 + 1e-9) / 10^d. This is not R's round(). Quantiles are type 7 and are rounded only at display, from the raw quantile.",
  "The page tables, the sentences that quote those figures, and the chart data are written from this script. The page matches the script output under round-half-up.",
  sprintf("Spearman score vs members = %.6f (n = %d), displayed 0.74.", spearman, nrow(reach)),
  sprintf("Pearson score vs log(members) = %.6f, displayed 0.72.", pearson_log),
  sprintf(
    "Non-sequel TV median members raw = %.1f, round-half-up = %s.",
    median(other_tv$members),
    fmt_int(median(other_tv$members))
  ),
  sprintf(
    "Sequel TV median members raw = %.1f, round-half-up = %s.",
    median(sequel_tv$members),
    fmt_int(median(sequel_tv$members))
  ),
  sprintf(
    "DLE: %d of %d scored DLE titles with known duration (%.1f%%) are 5 minutes or shorter. The page keeps the 3-minute median caption.",
    dle_short,
    dle_known_n,
    100 * dle_short / dle_known_n
  ),
  sprintf(
    "Bones IQR rank among the 20 studios is %d (1 = tightest). OLM remains the tightest overall.",
    league$iqr_rank[league$studio == "Bones"]
  ),
  sprintf("Shortlist check: %d of %d high scorers with at least 1,000 ratings are sequels.", sum(buried_43$is_sequel), nrow(buried_43)),
  "League table as published (round-half-up):",
  capture.output(print(
    league_disp %>% transmute(
      studio, n,
      median = fmt_fixed(median, 2),
      q1 = fmt_fixed(q1, 2),
      q3 = fmt_fixed(q3, 2),
      iqr = fmt_fixed(iqr, 2),
      share = paste0(fmt_fixed(share, 1), "%")
    ),
    n = 30
  ))
)
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
    "quantiles: type 7. Displayed figures use round-half-up on the exact value, not R's round()."
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
publish_csv(
  source_tbl,
  file.path(article_dir, "data/tv_by_source.csv"),
  c("median_score", "q1", "q3", "median_members")
)
publish_csv(
  league,
  file.path(article_dir, "data/studios.csv"),
  c("median_score", "q1", "q3", "iqr")
)
publish_csv(
  genre_tbl,
  file.path(article_dir, "data/genres.csv"),
  "median_score"
)
readr::write_csv(
  shortlist %>% transmute(animeID, name, title_english, type, year, source, score, scored_by, popularity, members),
  file.path(article_dir, "data/shortlist.csv")
)
readr::write_csv(format_years, file.path(article_dir, "data/format_years.csv"))

splice_marker <- function(text, name, inner) {
  start <- paste0("<!-- gen:", name, " -->")
  end <- paste0("<!-- /gen:", name, " -->")
  i <- regexpr(start, text, fixed = TRUE)
  j <- regexpr(end, text, fixed = TRUE)
  if (i < 1 || j < 1 || j < i) stop("Page is missing generation markers for ", name)
  paste0(
    substr(text, 1, i + nchar(start) - 1),
    "\n", inner, "\n",
    substr(text, j, nchar(text))
  )
}
replace_once <- function(text, pattern, repl) {
  hit <- gregexpr(pattern, text, perl = TRUE)[[1]]
  if (hit[[1]] < 1 || length(hit) != 1) stop("Expected exactly one match for: ", pattern)
  sub(pattern, repl, text, perl = TRUE)
}

source_rows <- paste(vapply(seq_len(nrow(source_disp)), function(i) {
  sprintf(
    "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>",
    source_disp$source[[i]],
    source_disp$n_lab[[i]],
    source_disp$median_lab[[i]],
    source_disp$members_lab[[i]],
    source_disp$share_lab[[i]]
  )
}, character(1)), collapse = "\n")

studio_rows_html <- paste(vapply(seq_len(nrow(league_disp)), function(i) {
  sprintf(
    "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s\u2013%s</td><td>%s</td><td>%s</td></tr>",
    league_disp$studio[[i]],
    fmt_int(league_disp$n[[i]]),
    fmt_fixed(league_disp$median[[i]], 2),
    fmt_fixed(league_disp$q1[[i]], 2),
    fmt_fixed(league_disp$q3[[i]], 2),
    fmt_fixed(league_disp$iqr[[i]], 2),
    paste0(fmt_fixed(league_disp$share[[i]], 1), "%")
  )
}, character(1)), collapse = "\n")

studio_caption <- sprintf(
  paste0(
    "Across the 20 largest studios, medians run from %s to %s. ",
    "Bones has the tightest spread among the top scorers, and OLM is the most consistent overall, at a lower level. ",
    "DLE (n = %s) mostly makes short-form titles, with a median episode of 3 minutes, so its median score isn't directly comparable to studios making 24-minute episodes."
  ),
  fmt_fixed(pick(league, "Bones", "median_score"), 2),
  fmt_fixed(pick(league, "DLE", "median_score"), 2),
  fmt_int(pick(league, "DLE", "n"))
)

md_path <- file.path(repo_root, "src/content/blog/anime.md")
page <- paste(readLines(md_path, encoding = "UTF-8", warn = FALSE), collapse = "\n")
page <- splice_marker(page, "source-table", source_rows)
page <- splice_marker(page, "studio-table", studio_rows_html)
page <- splice_marker(page, "studio-caption", studio_caption)
page <- replace_once(
  page,
  "Kyoto Animation's [0-9,]+ titles have a median of [0-9.]+ and an IQR of [0-9.]+\\.",
  sprintf(
    "Kyoto Animation's %s titles have a median of %s and an IQR of %s.",
    fmt_int(pick(league, "Kyoto Animation", "n")),
    fmt_fixed(pick(league, "Kyoto Animation", "median_score"), 2),
    fmt_fixed(pick(league, "Kyoto Animation", "iqr"), 2)
  )
)
page <- replace_once(
  page,
  "Sequels also draw more members at the median, [0-9,]+ against [0-9,]+\\.",
  sprintf(
    "Sequels also draw more members at the median, %s against %s.",
    fmt_int(median(sequel_tv$members)),
    fmt_int(median(other_tv$members))
  )
)
page <- replace_once(
  page,
  "Kids titles \\(median [0-9.]+, n = [0-9,]+\\) and music titles \\(median [0-9.]+, n = [0-9,]+\\) score lowest, which more likely reflects a mismatch between audience and content than weak production\\. Thriller \\([0-9.]+, n = [0-9,]+\\), Mystery \\([0-9.]+, n = [0-9,]+\\), and Psychological \\([0-9.]+, n = [0-9,]+\\) score highest\\.",
  sprintf(
    "Kids titles (median %s, n = %s) and music titles (median %s, n = %s) score lowest, which more likely reflects a mismatch between audience and content than weak production. Thriller (%s, n = %s), Mystery (%s, n = %s), and Psychological (%s, n = %s) score highest.",
    gmed("Kids"), gn("Kids"), gmed("Music"), gn("Music"),
    gmed("Thriller"), gn("Thriller"), gmed("Mystery"), gn("Mystery"),
    gmed("Psychological"), gn("Psychological")
  )
)
if (grepl("0.389", page, fixed = TRUE)) stop("Page still contains 0.389")
if (grepl("most anime", page, ignore.case = TRUE)) stop("Page must not say most anime is committee-financed")
if (grepl("Steinberg, 2012; Mihara, 2018", page, fixed = TRUE)) stop("Mihara is still cited on the demand-test sentence")
stopifnot(grepl("30 of the 43 high scorers with at least 1,000 ratings are sequels.", page, fixed = TRUE))
stopifnot(grepl("(Creamer, 2015; Moore, 2017; Kyoto Animation training school)", page, fixed = TRUE))
stopifnot(grepl("the tightest spread among the top-scoring studios (only 7th-tightest of all 20).", page, fixed = TRUE))
stopifnot(grepl("On our reading, a published book also serves as a live test of demand before a committee commits money to animation.", page, fixed = TRUE))
stopifnot(grepl("Hernández Hernández, 2018, §4.3; Mihara, 2018", page, fixed = TRUE))
stopifnot(grepl("Each format wave lines up with a new distribution channel", page, fixed = TRUE))
stopifnot(grepl("round-half-up", page, fixed = TRUE))
stopifnot(grepl("more than a million fans", page, fixed = TRUE))
writeLines(page, md_path, useBytes = TRUE)

# --- charts ---
title_eras <- "Each wave lines up with a new channel"
sub_eras <- "Titles by first year, through 2018. OVA peaks at 115 in 1993. ONA reaches 216 in 2018. Panels do not share a vertical scale."
title_score <- "Light novels set the audience floor. Manga produces more 8.0s."
sub_score <- "Scored television only (n = 4,240 of 4,260 TV titles). Left axis is a log scale."
title_studios <- "Bones has the tightest spread among the top-scoring studios"
sub_studios <- "Studios with at least 100 scored titles, sorted by median. Bars are the middle half of scores. Dashed line: catalog median 6.38."
title_sequel <- "TV sequels score higher, consistent with only well-received shows getting one"
sub_sequel <- sprintf(
  "Sequels n = %s, median %s. Others n = %s, median %s. The pattern is consistent with selection, not an effect of being a sequel.",
  fmt_int(nrow(sequel_tv)),
  fmt_fixed(median(sequel_tv$score), 2),
  fmt_int(nrow(other_tv)),
  fmt_fixed(median(other_tv$score), 2)
)
title_reach <- "Score and reach move together (Spearman 0.74)"
sub_reach <- "n = 13,518 scored titles. Red points are the 10-title editorial shortlist. Dashed line: catalog median 6.38."

eras <- format_years %>%
  mutate(type = factor(type, levels = c("TV", "Movie", "OVA", "ONA", "Special", "Music"))) %>%
  complete(year = 1960:2018, type, fill = list(n = 0)) %>%
  filter(year >= 1960)

p_eras <- ggplot(eras, aes(year, n)) +
  geom_col(fill = "#4A4A4A", width = 1) +
  geom_col(data = filter(eras, type == "OVA", year == 1993), fill = RED, width = 1) +
  geom_col(data = filter(eras, type == "ONA", year == 2018), fill = RED, width = 1) +
  facet_wrap(~type, scales = "free_y", ncol = 3) +
  labs(title = title_eras, subtitle = sub_eras, x = NULL, y = "Titles", caption = caption_src) +
  theme_brief()
save_plot(p_eras, "chart_eras", 11.2, 6.8)
write_plotly(
  "chart_eras",
  list(list(
    type = "bar",
    x = eras$year,
    y = eras$n,
    marker = list(color = "#4A4A4A"),
    hovertemplate = "%{x}<br>%{y} titles<extra></extra>",
    transforms = list(list(type = "groupby", groups = eras$type))
  )),
  list(title = chart_title(title_eras, sub_eras), barmode = "group")
)

scorecard <- source_disp
ln_red <- scorecard$source == "Light novel"
member_floor <- 1000
member_colors <- ifelse(ln_red, RED, "#4A4A4A")
label_colors <- ifelse(ln_red, RED, INK)
p1 <- ggplot(scorecard, aes(source, members_d)) +
  geom_segment(
    aes(xend = source, y = member_floor, yend = members_d, color = ln_red),
    linewidth = 0.7
  ) +
  geom_point(aes(color = ln_red), size = 3.4) +
  geom_text(
    aes(label = members_lab, color = ln_red),
    vjust = -1.15,
    size = 3.15,
    family = body_family,
    fontface = "bold",
    show.legend = FALSE
  ) +
  scale_y_log10(
    labels = scales::comma,
    expand = expansion(mult = c(0.04, 0.22))
  ) +
  scale_color_manual(values = c(`TRUE` = RED, `FALSE` = "#4A4A4A"), guide = "none") +
  labs(x = NULL, y = "Median members") +
  theme_brief() +
  theme(axis.text.x = element_text(size = 8))
p2 <- ggplot(scorecard, aes(source, share_d, fill = ln_red)) +
  geom_col(width = 0.72) +
  scale_fill_manual(values = c(`TRUE` = RED, `FALSE` = "#4A4A4A"), guide = "none") +
  labs(x = NULL, y = "Share scoring 8.0 or higher (%)") +
  theme_brief() +
  theme(axis.text.x = element_text(size = 8))
png(
  file.path(charts_dir, "chart_scorecard.png"),
  width = 11.2, height = 6.6, units = "in", res = 160, bg = "white"
)
grid::grid.newpage()
grid::pushViewport(grid::viewport(layout = grid::grid.layout(
  3, 2,
  heights = grid::unit(c(1.05, 4.7, 0.7), "in")
)))
print(p1 + theme(plot.caption = element_blank()), vp = grid::viewport(layout.pos.row = 2, layout.pos.col = 1))
print(p2 + theme(plot.caption = element_blank()), vp = grid::viewport(layout.pos.row = 2, layout.pos.col = 2))
# Draw the takeaway after the panels so the white panel backgrounds cannot cover it.
grid::grid.text(
  title_score,
  x = grid::unit(0.18, "in"), y = 0.68, just = c("left", "center"),
  gp = grid::gpar(fontfamily = title_family, fontsize = 16, col = "black"),
  vp = grid::viewport(layout.pos.row = 1, layout.pos.col = 1:2)
)
grid::grid.text(
  sub_score,
  x = grid::unit(0.18, "in"), y = 0.28, just = c("left", "center"),
  gp = grid::gpar(fontfamily = body_family, fontsize = 10, col = "#525252"),
  vp = grid::viewport(layout.pos.row = 1, layout.pos.col = 1:2)
)
grid::grid.text(
  caption_src, x = grid::unit(0.18, "in"), just = "left",
  gp = grid::gpar(fontfamily = body_family, fontsize = 8, col = "#525252"),
  vp = grid::viewport(layout.pos.row = 3, layout.pos.col = 1:2)
)
dev.off()
write_plotly(
  "chart_scorecard",
  list(
    list(
      type = "scatter",
      mode = "markers+text",
      name = "Median members",
      x = scorecard$source,
      y = scorecard$members_d,
      text = scorecard$members_lab,
      textposition = "top center",
      textfont = list(
        family = "DM Sans, Helvetica, Arial, sans-serif",
        size = 12,
        color = label_colors
      ),
      marker = list(size = 12, color = member_colors),
      error_y = list(
        type = "data",
        symmetric = FALSE,
        array = rep(0, nrow(scorecard)),
        arrayminus = scorecard$members_d - member_floor,
        color = member_colors,
        thickness = 2,
        width = 0
      ),
      cliponaxis = FALSE,
      hovertemplate = "%{x}<br>%{y:,.0f} members<extra></extra>"
    ),
    list(
      type = "bar",
      name = "Share at or above 8.0",
      x = scorecard$source,
      y = scorecard$share_d,
      xaxis = "x2",
      yaxis = "y2",
      marker = list(color = member_colors),
      hovertemplate = "%{x}<br>%{y:.1f}% scoring 8.0 or higher<extra></extra>"
    )
  ),
  list(
    title = chart_title(title_score, sub_score),
    xaxis = list(domain = c(0, 0.45)),
    yaxis = list(
      type = "log",
      title = list(text = "Median members"),
      range = c(log10(700), log10(max(scorecard$members_d) * 2.8))
    ),
    xaxis2 = list(domain = c(0.55, 1), anchor = "y2"),
    yaxis2 = list(
      type = "linear",
      anchor = "x2",
      title = list(text = "Share at or above 8.0 (%)")
    )
  )
)

league_plot <- league_disp %>%
  mutate(
    studio_label = paste0(studio, "  n=", n),
    studio_label = factor(studio_label, levels = rev(studio_label))
  )
p_league <- ggplot(league_plot, aes(median, studio_label)) +
  geom_errorbarh(aes(xmin = q1, xmax = q3, color = focal), height = 0, linewidth = 0.8) +
  geom_point(aes(size = n, color = focal)) +
  geom_vline(xintercept = BASELINE, linetype = "dashed", color = GRAY, linewidth = 0.4) +
  scale_color_manual(values = c(`TRUE` = RED, `FALSE` = "#4A4A4A"), guide = "none") +
  scale_size_area(max_size = 8, guide = "none") +
  labs(
    title = title_studios,
    subtitle = sub_studios,
    x = "Median score", y = NULL,
    caption = paste0(
      caption_src, "\n",
      "DLE (n = 153) mostly makes short-form titles, with a median episode of 3 minutes,\n",
      "so its median score isn't directly comparable to studios making 24-minute episodes."
    )
  ) +
  theme_brief() +
  theme(
    plot.caption = element_text(family = body_family, color = "#525252", hjust = 0, size = 8, lineheight = 1.2),
    plot.margin = margin(12, 18, 28, 12)
  )
save_plot(p_league, "chart_studios", 11.2, 9.0)
write_plotly(
  "chart_studios",
  list(list(
    type = "scatter",
    mode = "markers",
    x = league_disp$median,
    y = as.character(league_plot$studio_label),
    customdata = unname(as.matrix(transmute(
      league_disp,
      q1 = round_half_up(q1, 2),
      q3 = round_half_up(q3, 2),
      iqr = round_half_up(iqr, 2)
    ))),
    marker = list(
      size = pmax(8, league_disp$n / 40),
      color = ifelse(league_disp$focal, RED, "#4A4A4A")
    ),
    error_x = list(
      type = "data",
      array = round_half_up(league_disp$q3 - league_disp$median, 2),
      arrayminus = round_half_up(league_disp$median - league_disp$q1, 2),
      color = ifelse(league_disp$focal, RED, "#4A4A4A"),
      thickness = 1.4
    ),
    hovertemplate = paste0(
      "%{y}<br>Median %{x:.2f}",
      "<br>Middle half %{customdata[0]:.2f}\u2013%{customdata[1]:.2f}",
      "<br>IQR %{customdata[2]:.2f}<extra></extra>"
    )
  )),
  list(
    title = chart_title(
      title_studios,
      paste0(sub_studios, " DLE (n = 153) is mostly short-form, so its median isn't like-for-like.")
    ),
    margin = list(l = 168),
    xaxis = list(title = list(text = "Median score"), tickformat = ".2f"),
    yaxis = list(autorange = "reversed", automargin = TRUE),
    shapes = list(list(
      type = "line", x0 = BASELINE, x1 = BASELINE, y0 = 0, y1 = 1, yref = "paper",
      line = list(dash = "dash", color = GRAY)
    ))
  )
)

seq_long <- bind_rows(
  sequel_tv %>% transmute(score = round_half_up(score, 2), group = "Sequel"),
  other_tv %>% transmute(score = round_half_up(score, 2), group = "Not a sequel")
) %>%
  mutate(group = factor(group, levels = c("Not a sequel", "Sequel")))
meds <- tibble(
  group = factor(c("Not a sequel", "Sequel"), levels = c("Not a sequel", "Sequel")),
  median_score = c(
    round_half_up(median(other_tv$score), 2),
    round_half_up(median(sequel_tv$score), 2)
  )
)
p_seq <- ggplot(seq_long, aes(score, fill = group)) +
  geom_histogram(bins = 28, position = "identity", alpha = 0.85, color = NA) +
  geom_vline(data = meds, aes(xintercept = median_score, color = group), linetype = "dashed", linewidth = 0.5) +
  geom_vline(xintercept = BASELINE, color = INK, linetype = "dashed", linewidth = 0.3) +
  scale_fill_manual(values = c("Not a sequel" = "#8A8A8A", "Sequel" = RED)) +
  scale_color_manual(values = c("Not a sequel" = "#4A4A4A", "Sequel" = RED), guide = "none") +
  labs(
    title = title_sequel,
    subtitle = sub_sequel,
    x = "Score", y = "Titles", fill = NULL,
    caption = caption_src
  ) +
  theme_brief()
save_plot(p_seq, "chart_sequel", 11.2, 6.2)
write_plotly(
  "chart_sequel",
  list(
    list(
      type = "histogram", name = "Not a sequel",
      x = round_half_up(other_tv$score, 2),
      marker = list(color = "#8A8A8A"), opacity = 0.85,
      hovertemplate = "Score %{x:.2f}<br>Titles %{y}<extra></extra>"
    ),
    list(
      type = "histogram", name = "Sequel",
      x = round_half_up(sequel_tv$score, 2),
      marker = list(color = RED), opacity = 0.75,
      hovertemplate = "Score %{x:.2f}<br>Titles %{y}<extra></extra>"
    )
  ),
  list(
    barmode = "overlay",
    title = chart_title(title_sequel, sub_sequel),
    xaxis = list(title = list(text = "Score"), tickformat = ".2f")
  )
)

short_ids <- shortlist$animeID
reach_plot <- reach %>%
  mutate(
    on_shortlist = animeID %in% short_ids,
    score_d = round_half_up(score, 2),
    members_d = round_half_up(members, 0)
  )
p_reach <- ggplot(reach_plot, aes(members_d, score_d)) +
  geom_point(data = filter(reach_plot, !on_shortlist), color = PALE, alpha = 0.35, size = 0.7) +
  geom_point(data = filter(reach_plot, on_shortlist), color = RED, size = 2.2) +
  geom_hline(yintercept = BASELINE, linetype = "dashed", color = INK, linewidth = 0.35) +
  scale_x_log10(labels = scales::comma) +
  labs(
    title = title_reach,
    subtitle = sub_reach,
    x = "Members", y = "Score",
    caption = caption_src
  ) +
  theme_brief()
save_plot(p_reach, "chart_reach", 11.2, 6.6)
reach_bg <- filter(reach_plot, !on_shortlist)
reach_hi <- filter(reach_plot, on_shortlist)
write_plotly(
  "chart_reach",
  list(
    list(
      type = "scattergl",
      mode = "markers",
      name = "Scored titles",
      x = reach_bg$members_d,
      y = reach_bg$score_d,
      marker = list(size = 4, color = PALE, opacity = 0.35),
      hovertemplate = "Score %{y:.2f}<br>Members %{x:,.0f}<extra></extra>"
    ),
    list(
      type = "scattergl",
      mode = "markers",
      name = "Shortlist",
      x = reach_hi$members_d,
      y = reach_hi$score_d,
      marker = list(size = 8, color = RED),
      hovertemplate = "Score %{y:.2f}<br>Members %{x:,.0f}<extra></extra>"
    )
  ),
  list(
    title = chart_title(title_reach, sub_reach),
    xaxis = list(type = "log", title = list(text = "Members")),
    yaxis = list(title = list(text = "Score"), tickformat = ".2f"),
    shapes = list(list(
      type = "line", x0 = 0, x1 = 1, xref = "paper", y0 = BASELINE, y1 = BASELINE,
      line = list(dash = "dash", color = INK)
    ))
  )
)

oxipng <- Sys.which("oxipng")
if (!nzchar(oxipng)) {
  candidate <- path.expand("~/.local/bin/oxipng")
  if (file.exists(candidate)) oxipng <- candidate
}
pngs <- list.files(charts_dir, "\\.png$", full.names = TRUE)
if (!nzchar(oxipng)) {
  warning("oxipng not found; chart PNGs were not optimized")
} else {
  status <- system2(oxipng, c("-o", "4", "--strip", "safe", pngs))
  if (!identical(status, 0L)) stop("oxipng failed")
}

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
extra_zip <- file.path(article_dir, "source.zip")
if (file.exists(extra_zip)) file.remove(extra_zip)

jsons <- list.files(charts_dir, "\\.plotly\\.json$", full.names = TRUE)
for (path in jsons) {
  txt <- paste(readLines(path, warn = FALSE), collapse = "\n")
  if (grepl("\\.[0-9]*0{6}|\\.[0-9]*9{6}", txt)) stop("Noisy float in ", path)
  if (!grepl("\"t\":100", txt, fixed = TRUE)) stop("Plotly top margin is not 100 in ", basename(path))
}
studios_lines <- readLines(file.path(article_dir, "data/studios.csv"), warn = FALSE)
genre_lines <- readLines(file.path(article_dir, "data/genres.csv"), warn = FALSE)
if (!any(grepl("^Kyoto Animation,110,7\\.43,6\\.6725,7\\.8875,.*,1\\.215,", studios_lines))) {
  stop("Published studios.csv did not clean Kyoto Animation's IQR to 1.215")
}
if (!any(grepl("^Historical,[0-9]+,6\\.565$", genre_lines))) {
  stop("Published genres.csv did not clean Historical median to 6.565")
}
reach_bytes <- file.info(file.path(charts_dir, "chart_reach.plotly.json"))$size
message("chart_reach.plotly.json ", reach_bytes, " bytes")
message("Wrote charts to ", charts_dir)
message("Spearman ", fmt_fixed(spearman, 2), " log-Pearson ", fmt_fixed(pearson_log, 2))
message("Discrepancies: ", file.path(article_dir, "data/discrepancies.txt"))
