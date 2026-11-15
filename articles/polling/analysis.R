# POLLING: analysis for "The Count of Polling Places Fell 15% Across 23 States, 2012-2020".
# Input : TidyTuesday 2024-01-16 polling_places.csv (Center for Public Integrity, PublicI/us-polling-places)
# Output: articles/polling/data/*.csv, public/data/articles/polling/*, charts in public/images/content/articles/polling/charts
# Run   : Rscript articles/polling/analysis.R [path/to/polling_places.csv]   (from the repo root)
suppressPackageStartupMessages({ library(dplyr); library(readr); library(stringr); library(tidyr) })
source("scripts/r/artometrics_editorial.R")

args <- commandArgs(trailingOnly = TRUE)
raw <- if (length(args)) args[1] else "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2024/2024-01-16/polling_places.csv"
pp <- read_csv(raw, show_col_types = FALSE, col_types = cols(.default = col_character()))

gen_dates <- c("2012-11-06", "2014-11-04", "2016-11-08", "2018-11-06", "2020-11-03")
yrs <- substr(gen_dates, 1, 4)

# One row per distinct address per state per general election. Only case and whitespace are normalised.
places <- pp |>
  filter(election_date %in% gen_dates) |>
  mutate(key = str_squish(str_to_upper(coalesce(address, name)))) |>
  filter(!is.na(key)) |>
  distinct(state, election_date, key)

by_state <- places |>
  count(state, election_date) |>
  mutate(year = substr(election_date, 1, 4)) |>
  select(state, year, n) |>
  pivot_wider(names_from = year, values_from = n)

complete <- by_state |>
  filter(if_all(all_of(yrs), ~ !is.na(.x))) |>
  mutate(change = `2020` - `2012`, pct = change / `2012`) |>
  arrange(change)

coverage <- pp |>
  filter(election_date %in% gen_dates) |>
  group_by(election_date) |>
  summarise(rows = n(), states = n_distinct(state), .groups = "drop") |>
  mutate(year = substr(election_date, 1, 4))

totals <- complete |>
  summarise(across(all_of(yrs), sum)) |>
  pivot_longer(everything(), names_to = "year", values_to = "places") |>
  mutate(year = as.integer(year), index = 100 * places / places[1])

write_csv(complete, "articles/polling/data/states_complete_2012_2020.csv")
write_csv(by_state, "articles/polling/data/places_by_state_election.csv")
write_csv(coverage, "articles/polling/data/coverage_by_election.csv")
write_csv(totals, "articles/polling/data/totals_complete_states.csv")

cat("rows", nrow(pp), " dates", n_distinct(pp$election_date), " states", n_distinct(pp$state), "\n")
cat("complete states:", nrow(complete), "\n")
print(totals)
cat("decline", sum(complete$change), "pct", sum(complete$change) / sum(complete$`2012`), "\n")
print(head(complete, 8)); print(tail(complete, 5))
cat("states up:", sum(complete$change > 0), " flat/down:", sum(complete$change <= 0), "\n")
top4 <- head(complete, 4); cat("top4 decline", sum(top4$change), "share", sum(top4$change) / sum(complete$change), "\n")
ex <- complete |> filter(state != "MD"); cat("excl MD pct", sum(ex$change) / sum(ex$`2012`), "\n")
print(coverage)

# ---- charts ----------------------------------------------------------------
src <- "Source: Center for Public Integrity via TidyTuesday, 2024-01-16"
img <- "public/images/content/articles/polling/charts"
dat <- "public/data/articles/polling"
dir.create(file.path(dat, "charts"), recursive = TRUE, showWarnings = FALSE)
minus <- function(x) ifelse(x < 0, paste0("\u2212", scales::comma(abs(x))), paste0("+", scales::comma(x)))
pminus <- function(x) ifelse(x < 0, paste0("\u2212", scales::number(abs(x) * 100, accuracy = 0.1), "%"), paste0("+", scales::number(x * 100, accuracy = 0.1), "%"))

d1 <- head(complete, 10)
art_ed_save(art_ed_hbar(d1$state, d1$change, highlight = 1:4, fmt = minus, expand = 0.3), file.path(img, "chart1_net_change"),
  headline = "Four states account for 69% of the net loss",
  subtitle = "Net change in distinct polling-place addresses, 2012 to 2020. The ten biggest declines among 23 states.", source = src)
art_ed_sidecar(file.path(dat, "charts/chart1_net_change.plotly.json"), "bar_h", d1$state, d1$change, "Net change in polling places, 2012 to 2020", highlight = 1:4)

art_ed_save(art_ed_line(totals$year, totals$index, fmt = scales::label_number(accuracy = 1), xbreaks = totals$year[c(1, 3, 5)], lfmt = scales::label_number(accuracy = 0.1)), file.path(img, "chart2_index"),
  headline = "A slow slide, then a 9% drop in 2020",
  subtitle = "Distinct polling-place addresses in the 23 states with data for every general election. 2012 = 100.", source = src)
art_ed_sidecar(file.path(dat, "charts/chart2_index.plotly.json"), "line", totals$year, round(totals$index, 2), "Polling-place index, 23 states, 2012 = 100")

d3 <- complete |> arrange(pct) |> head(8)
art_ed_save(art_ed_hbar(d3$state, d3$pct, highlight = 1:2, fmt = pminus, expand = 0.3), file.path(img, "chart3_pct_change"),
  headline = "Maryland and North Dakota cut deepest",
  subtitle = "Percent change in distinct polling-place addresses, 2012 to 2020. The eight biggest declines.", source = src)
art_ed_sidecar(file.path(dat, "charts/chart3_pct_change.plotly.json"), "bar_h", d3$state, round(d3$pct * 100, 2), "Percent change in polling places, 2012 to 2020", highlight = 1:2)

md <- complete |> filter(state == "MD") |> select(all_of(yrs)) |> unlist()
art_ed_save(art_ed_col(yrs, as.integer(md), highlight = 5), file.path(img, "chart4_maryland"),
  headline = "Maryland went from 1,566 places to 320 in one cycle",
  subtitle = "Distinct polling-place addresses in Maryland, general elections 2012 to 2020. In 2020 the state used Election Day vote centers.", source = src)
art_ed_sidecar(file.path(dat, "charts/chart4_maryland.plotly.json"), "bar", yrs, as.integer(md), "Maryland polling-place addresses", highlight = 5)

art_ed_save(art_ed_col(coverage$year, coverage$states, highlight = 5, show_values = TRUE), file.path(img, "chart5_coverage"),
  headline = "The map keeps changing: 30 states in 2012, 35 in 2020",
  subtitle = "States with any records in the extract, by general election. Only 23 appear in all five.", source = src)
art_ed_sidecar(file.path(dat, "charts/chart5_coverage.plotly.json"), "bar", coverage$year, coverage$states, "States with data, by general election", highlight = 5)

# ---- downloadable dataset ------------------------------------------------------
out <- by_state |>
  mutate(in_all_five = state %in% complete$state) |>
  rename_with(~ paste0("places_", .x), all_of(yrs)) |>
  arrange(desc(in_all_five), state)
write_csv(out, file.path(dat, "dataset.csv"), na = "")
file.copy("articles/polling/data/states_complete_2012_2020.csv", file.path(dat, "states_complete_2012_2020.csv"), overwrite = TRUE)
file.copy("articles/polling/data/coverage_by_election.csv", file.path(dat, "coverage_by_election.csv"), overwrite = TRUE)
