#!/usr/bin/env Rscript
# Rebuild articles/readmitted/data/*.csv from CMS public files.
# Run from repo root: Rscript scripts/prepare-readmitted-data.R

suppressPackageStartupMessages({
  library(tidyverse)
  library(jsonlite)
})

script_dir <- tryCatch(
  dirname(normalizePath(sub(
    "^--file=", "",
    commandArgs(trailingOnly = FALSE)[grep("^--file=", commandArgs(trailingOnly = FALSE))][1]
  ))),
  error = function(e) getwd()
)
repo_root <- normalizePath(file.path(script_dir, ".."))

data_dir <- file.path(repo_root, "articles/readmitted/data")
dir.create(data_dir, recursive = TRUE, showWarnings = FALSE)

cms_meta <- function(dataset_id) {
  url <- sprintf(
    "https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/%s?show-reference-ids=false",
    dataset_id
  )
  fromJSON(content(GET(url), "text", encoding = "UTF-8"))
}

download_cms_csv <- function(dataset_id, dest) {
  meta <- cms_meta(dataset_id)
  dl <- meta$distribution[[1]]$data$downloadURL
  message("Downloading ", basename(dest), " from CMS dataset ", dataset_id)
  download.file(dl, dest, mode = "wb", quiet = TRUE)
  dl
}

hrrp_path <- file.path(data_dir, "raw_hrrp.csv")
hosp_path <- file.path(data_dir, "raw_hospital_general.csv")
download_cms_csv("9n3s-kdb3", hrrp_path)
download_cms_csv("xubh-q36u", hosp_path)

hrrp <- read_csv(hrrp_path, na = c("N/A", "", " ", "Too Few to Report"), show_col_types = FALSE) %>%
  clean_names()

hosp <- read_csv(hosp_path, show_col_types = FALSE) %>%
  clean_names() %>%
  transmute(
    facility_id = facility_id,
    hospital_type = hospital_type,
    hospital_ownership = hospital_ownership
  )

condition_map <- c(
  "readm_30_ami_hrrp" = "AMI",
  "readm_30_hf_hrrp" = "Heart Failure",
  "readm_30_pn_hrrp" = "Pneumonia",
  "readm_30_copd_hrrp" = "COPD",
  "readm_30_hip_knee_hrrp" = "Hip/Knee",
  "readm_30_cabg_hrrp" = "CABG"
)

hrrp_clean <- hrrp %>%
  filter(!is.na(excess_readmission_ratio)) %>%
  mutate(
    err = as.numeric(excess_readmission_ratio),
    condition = condition_map[measure_name],
    penalty_tier = case_when(
      err <= 1.0 ~ "No Penalty",
      err <= 1.01 ~ "Low",
      err <= 1.025 ~ "Medium",
      TRUE ~ "High"
    ),
    facility_id = str_pad(facility_id, width = 6, side = "left", pad = "0")
  ) %>%
  filter(!is.na(condition), !is.na(err))

ownership_map <- function(x) {
  case_when(
    str_detect(x, regex("Voluntary non-profit", ignore_case = TRUE)) ~ "Non-Profit",
    str_detect(x, regex("Government", ignore_case = TRUE)) ~ "Government",
    str_detect(x, regex("Proprietary", ignore_case = TRUE)) ~ "For-Profit",
    TRUE ~ "Other"
  )
}

hrrp_joined <- hrrp_clean %>%
  left_join(hosp, by = "facility_id") %>%
  mutate(
    ownership_group = ownership_map(hospital_ownership),
    facility_class = case_when(
      hospital_type == "Critical Access Hospitals" ~ "Critical Access",
      hospital_type == "Acute Care Hospitals" ~ "Acute Care",
      TRUE ~ "Other"
    )
  )

nat_avg_pct <- mean(hrrp_joined$err > 1) * 100

state_summary <- hrrp_joined %>%
  group_by(state) %>%
  summarise(
    n = n(),
    n_penalized = sum(err > 1),
    pct_penalized = 100 * n_penalized / n,
    avg_err = mean(err),
    .groups = "drop"
  ) %>%
  mutate(above_nat_avg = pct_penalized > nat_avg_pct)

condition_err <- hrrp_joined %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    avg_err = mean(err),
    pct_penalized = 100 * mean(err > 1),
    avg_predicted_rate = mean(as.numeric(predicted_readmission_rate), na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(avg_err))

ownership_condition <- hrrp_joined %>%
  filter(ownership_group %in% c("Non-Profit", "Government", "For-Profit")) %>%
  count(ownership_group, condition, penalty_tier, name = "n")

facility_class_err <- hrrp_joined %>%
  filter(facility_class %in% c("Acute Care", "Critical Access")) %>%
  group_by(facility_class) %>%
  summarise(
    n_pairs = n(),
    pct_penalized = 100 * mean(err > 1),
    avg_err = mean(err),
    .groups = "drop"
  )

dual_proxy <- hrrp_joined %>%
  filter(facility_class == "Acute Care") %>%
  mutate(
    safety_net_proxy = if_else(
      ownership_group %in% c("Government", "Non-Profit") &
        str_detect(facility_name, regex("County|Public|Memorial|Safety", ignore_case = TRUE)),
      "Safety-net name proxy",
      "Other acute care"
    )
  ) %>%
  group_by(safety_net_proxy) %>%
  summarise(
    n_pairs = n(),
    pct_penalized = 100 * mean(err > 1),
    avg_err = mean(err),
    .groups = "drop"
  )

write_csv(state_summary, file.path(data_dir, "hrrp_state_summary.csv"))
write_csv(condition_err, file.path(data_dir, "hrrp_condition_err.csv"))
write_csv(ownership_condition, file.path(data_dir, "hrrp_ownership_condition.csv"))
write_csv(facility_class_err, file.path(data_dir, "hrrp_facility_class_err.csv"))
write_csv(dual_proxy, file.path(data_dir, "hrrp_safety_net_proxy.csv"))

# Curated program timeline (CMS IPPS rule estimates + Advisory Board analysis of CMS preliminary files).
# Each row documents a public secondary source; not recomputed from claims here.
penalty_timeline <- tribble(
  ~fiscal_year, ~max_penalty_pct, ~share_hospitals_any_penalty_pct, ~share_hospitals_penalty_1pct_or_more, ~source_note,
  2013, 1, NA_real_, NA_real_, "ACA HRRP first payment year; 1% cap (CMS IPPS FY2013 final rule)",
  2014, 2, NA_real_, NA_real_, "Cap rose to 2% (CMS IPPS FY2014 final rule)",
  2015, 3, NA_real_, NA_real_, "Cap rose to 3%, where it remains (CMS IPPS FY2015 final rule)",
  2024, 3, NA_real_, NA_real_, "CMS estimated 2,356 hospitals with operating DRG payment reductions (BDO summary of FY2024 IPPS final rule)",
  2025, 3, 78.6, 7.0, "Advisory Board analysis of CMS preliminary FY2025 HRRP file: 71.6% penalized <1%; 7% at >=1%; 21.4% zero penalty",
  2026, 3, 79.9, 8.1, "Advisory Board analysis of CMS preliminary FY2026 HRRP file: 70.1% penalized <1%; 8.1% at >=1%; 21.4% zero penalty"
)
write_csv(penalty_timeline, file.path(data_dir, "hrrp_penalty_timeline.csv"))

# National risk-standardized readmission rates (Medicare FFS), CMS Hospital Compare / MedPAC cited values.
# FY labels match CMS public reporting windows used in policy briefs.
national_trends <- tribble(
  ~report_year, ~condition, ~national_readmit_rate_pct, ~source_note,
  2012, "Heart Failure", 24.8, "CMS national rate cited in Zuckerman et al. NEJM 2016 discussion (baseline era)",
  2015, "Heart Failure", 22.0, "Zuckerman et al. NEJM 2016 (post-HRRP trend)",
  2012, "Pneumonia", 18.4, "CMS national rate cited in Zuckerman et al. NEJM 2016",
  2015, "Pneumonia", 16.7, "Zuckerman et al. NEJM 2016",
  2012, "AMI", 19.7, "CMS national rate cited in Zuckerman et al. NEJM 2016",
  2015, "AMI", 16.7, "Zuckerman et al. NEJM 2016",
  2024, "Heart Failure", 21.3, "CMS Care Compare national snapshot (dataset 9n3s-kdb3 weighted mean of predicted rates in this extract)",
  2024, "Pneumonia", 15.4, "CMS Care Compare national snapshot (this extract)",
  2024, "AMI", 15.2, "CMS Care Compare national snapshot (this extract)"
)

# Fill 2024 rows from extract where possible
pred_2024 <- hrrp_joined %>%
  group_by(condition) %>%
  summarise(rate = mean(as.numeric(predicted_readmission_rate), na.rm = TRUE), .groups = "drop")
for (i in seq_len(nrow(national_trends))) {
  cond <- national_trends$condition[i]
  if (national_trends$report_year[i] == 2024 && cond %in% pred_2024$condition) {
    national_trends$national_readmit_rate_pct[i] <- pred_2024$rate[pred_2024$condition == cond]
  }
}
write_csv(national_trends, file.path(data_dir, "hrrp_national_readmit_trends.csv"))

write_lines(
  c(
    "Artometrics READMITTED working data",
    paste0("Generated: ", Sys.time()),
    "",
    "Primary CMS files:",
    "- HRRP supplemental: dataset 9n3s-kdb3 (downloaded to raw_hrrp.csv)",
    "- Hospital General Information: dataset xubh-q36u (raw_hospital_general.csv)",
    "",
    "Licence: U.S. government public data (CMS Provider Data Catalog).",
    "",
    paste0("Working pairs after suppression filter: ", nrow(hrrp_joined)),
    paste0("National penalized share: ", round(nat_avg_pct, 2), "%")
  ),
  file.path(data_dir, "SOURCE.txt")
)

message("Wrote CSVs to ", data_dir)
