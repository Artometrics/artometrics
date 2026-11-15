# MARKERS: analysis for "Texas Holds One in Four of America's Historical Markers".
# Input : TidyTuesday 2023-07-04 historical_markers.csv and no_markers.csv (Historical Marker Database, hmdb.org)
# Output: articles/markers/data/*.csv, public/data/articles/markers/*, charts in public/images/content/articles/markers/charts
# Run   : Rscript articles/markers/analysis.R [path/to/historical_markers.csv]   (from the repo root)
suppressPackageStartupMessages({ library(dplyr); library(readr); library(stringr); library(tidyr) })
source("scripts/r/artometrics_editorial.R")

args <- commandArgs(trailingOnly = TRUE)
base_url <- "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2023/2023-07-04/"
hm <- read_csv(if (length(args)) args[1] else paste0(base_url, "historical_markers.csv"), show_col_types = FALSE, guess_max = 100000)
nm <- read_csv(paste0(base_url, "no_markers.csv"), show_col_types = FALSE)

n_all <- nrow(hm)
by_state <- hm |> count(state_or_prov, name = "markers", sort = TRUE) |> mutate(share = markers / n_all)
yr <- hm |> filter(!is.na(year_erected))
by_year <- yr |> count(year_erected, name = "markers")
by_decade <- yr |> filter(year_erected >= 1890) |> mutate(decade = floor(year_erected / 10) * 10) |> count(decade, name = "markers")
stop_w <- c("the", "of", "and", "a", "an", "in", "to", "at", "on", "for", "by", "s", "is", "from", "with", "or", "as", "this",
            "that", "first", "old", "new", "county", "st", "no", "de", "la", "e", "w", "n", "i", "ii", "iii", "iv", "north",
            "south", "east", "west", "near", "site")
words <- hm |>
  mutate(id = row_number(), word = str_extract_all(str_to_lower(title), "[a-z]+")) |>
  select(id, word) |> unnest(word) |> distinct() |>
  filter(!word %in% stop_w, nchar(word) > 2) |> count(word, name = "markers", sort = TRUE)
missing_state <- hm |> group_by(state_or_prov) |>
  summarise(markers = n(), flagged = sum(!is.na(missing)), .groups = "drop") |>
  mutate(pct = flagged / markers) |> filter(markers >= 300) |> arrange(desc(pct))
y1936 <- yr |> filter(year_erected == 1936) |> count(state_or_prov, sort = TRUE)
y1890 <- yr |> filter(year_erected == 1890) |> mutate(by = str_detect(erected_by, regex("Chickamauga", ignore_case = TRUE))) |> count(by)

write_csv(by_state, "articles/markers/data/markers_by_state.csv")
write_csv(by_year, "articles/markers/data/markers_by_year.csv")
write_csv(by_decade, "articles/markers/data/markers_by_decade.csv")
write_csv(head(words, 25), "articles/markers/data/top_title_words.csv")
write_csv(missing_state, "articles/markers/data/missing_by_state.csv")
write_csv(count(nm, state, name = "counties_without_markers"), "articles/markers/data/counties_without_markers_by_state.csv")

cat("rows", n_all, " states", n_distinct(hm$state_or_prov), " year known", nrow(yr), " range", range(yr$year_erected), "\n")
print(head(by_state, 10)); print(by_decade); print(head(words, 10)); print(head(missing_state, 6))
cat("1936 total", sum(y1936$n), " Texas", y1936$n[y1936$state_or_prov == "Texas"], "\n"); print(y1890)
cat("flagged", sum(!is.na(hm$missing)), "confirmed", sum(hm$missing == "Confirmed Missing", na.rm = TRUE), "reported", sum(hm$missing == "Reported Missing", na.rm = TRUE), "\n")
cat("no-marker counties", nrow(nm), " Puerto Rico", sum(nm$state == "Puerto Rico"), "\n")
cat("top5 share", sum(head(by_state$markers, 5)) / n_all, " Texas by TX Hist Comm", sum(str_detect(hm$erected_by, "Texas Historical Commission"), na.rm = TRUE), "\n")

# ---- charts ----------------------------------------------------------------
src <- "Source: Historical Marker Database via TidyTuesday, 2023-07-04"
img <- "public/images/content/articles/markers/charts"
dat <- "public/data/articles/markers"
dir.create(file.path(dat, "charts"), recursive = TRUE, showWarnings = FALSE)

d1 <- head(by_state, 10)
art_ed_save(art_ed_hbar(d1$state_or_prov, d1$markers, highlight = 1), file.path(img, "chart1_states"),
  headline = "One state holds a quarter of the markers",
  subtitle = sprintf("Markers in the index extract by state (n = %s). The ten biggest states.", scales::comma(n_all)), source = src)
art_ed_sidecar(file.path(dat, "charts/chart1_states.plotly.json"), "bar_h", d1$state_or_prov, d1$markers, "Markers by state", highlight = 1)

yy <- data.frame(year = 1880:2023) |> left_join(by_year, by = c("year" = "year_erected")) |> mutate(markers = coalesce(markers, 0L))
notes <- data.frame(x = c(1890, 1936, 2003), y = c(686, 887, 785), label = c("1890: 686", "1936: 887", "2003: 785"), hj = c(0.1, 0.5, 0.5))
art_ed_save(art_ed_line(yy$year, yy$markers, label_last = FALSE, notes = notes, xbreaks = c(1900, 1950, 2000)), file.path(img, "chart2_years"),
  headline = "Marker-building spikes in 1890 and 1936",
  subtitle = sprintf("Markers by year erected, where the year is known (%s of %s). The extract is thin for 2023.", scales::comma(nrow(yr)), scales::comma(n_all)), source = src)
art_ed_sidecar(file.path(dat, "charts/chart2_years.plotly.json"), "line", yy$year, yy$markers, "Markers by year erected")

dd <- by_decade |> filter(decade >= 1950)
art_ed_save(art_ed_col(paste0(dd$decade, "s"), dd$markers, highlight = which.max(dd$markers), every = 1, show_values = TRUE), file.path(img, "chart3_decades"),
  headline = "The 2000s built the most markers",
  subtitle = "Markers by decade erected, 1950s to 2020s. The 2020s run only through 2023.", source = src)
art_ed_sidecar(file.path(dat, "charts/chart3_decades.plotly.json"), "bar", paste0(dd$decade, "s"), dd$markers, "Markers by decade erected", highlight = which.max(dd$markers))

w8 <- head(words, 8)
art_ed_save(art_ed_hbar(str_to_title(w8$word), w8$markers, highlight = 1), file.path(img, "chart4_words"),
  headline = "Church is the most common word on a marker",
  subtitle = "Markers whose title contains each word, after filler words are removed.", source = src)
art_ed_sidecar(file.path(dat, "charts/chart4_words.plotly.json"), "bar_h", str_to_title(w8$word), w8$markers, "Markers by title word", highlight = 1)

m8 <- head(missing_state, 8)
art_ed_save(art_ed_hbar(m8$state_or_prov, m8$pct, highlight = 1, fmt = scales::label_percent(accuracy = 0.1)), file.path(img, "chart5_missing"),
  headline = "In Washington, D.C., about one marker in seven is missing",
  subtitle = "Share of markers flagged missing, reported or confirmed. States and districts with at least 300 markers.", source = src)
art_ed_sidecar(file.path(dat, "charts/chart5_missing.plotly.json"), "bar_h", m8$state_or_prov, round(m8$pct * 100, 2), "Share of markers flagged missing (%)", highlight = 1)

# ---- downloadable datasets -----------------------------------------------------
write_csv(by_state, file.path(dat, "dataset.csv"))
for (f in c("markers_by_year", "markers_by_decade", "top_title_words", "missing_by_state", "counties_without_markers_by_state")) {
  file.copy(sprintf("articles/markers/data/%s.csv", f), file.path(dat, paste0(f, ".csv")), overwrite = TRUE)
}
