# CPI-U deflator helpers (mirrors scripts/lib/cpi.py)
# Usage: source(file.path(repo_root, "scripts/r/cpi.R"))

cpi_paths <- function(repo_root = normalizePath(".")) {
  dir <- file.path(repo_root, "data/reference/cpi")
  list(
    dir = dir,
    monthly = file.path(dir, "cpi_monthly.csv"),
    annual = file.path(dir, "cpi_annual.csv"),
    source = file.path(dir, "SOURCE.txt")
  )
}

load_cpi_annual <- function(repo_root = normalizePath(".")) {
  p <- cpi_paths(repo_root)$annual
  if (!file.exists(p)) {
    stop("Missing CPI cache. Run: python3 scripts/data/refresh_cpi.py", call. = FALSE)
  }
  df <- read.csv(p, stringsAsFactors = FALSE)
  stats::setNames(df$cpi_annual_avg, df$year)
}

deflate_to_base <- function(nominal, value_year, base_year = 2025L, cpi = NULL) {
  if (is.null(cpi)) cpi <- load_cpi_annual()
  by <- cpi[[as.character(base_year)]]
  vy <- cpi[[as.character(value_year)]]
  if (is.null(by) || is.null(vy)) {
    stop(sprintf("Missing CPI for year %s or base %s", value_year, base_year))
  }
  nominal * (by / vy)
}
