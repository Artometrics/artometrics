#!/usr/bin/env python3
"""Rebuild articles/readmitted/data/*.csv from CMS public files (stdlib only)."""

from __future__ import annotations

import csv
import json
import re
import statistics
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "articles/readmitted/data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CONDITION_MAP = {
    "READM-30-AMI-HRRP": "AMI",
    "READM-30-HF-HRRP": "Heart Failure",
    "READM-30-PN-HRRP": "Pneumonia",
    "READM-30-COPD-HRRP": "COPD",
    "READM-30-HIP-KNEE-HRRP": "Hip/Knee",
    "READM-30-CABG-HRRP": "CABG",
}


def cms_download(dataset_id: str, dest: Path) -> None:
    meta_url = (
        "https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/"
        f"{dataset_id}?show-reference-ids=false"
    )
    with urllib.request.urlopen(meta_url) as resp:
        meta = json.load(resp)
    dl = meta["distribution"][0]["data"]["downloadURL"]
    print(f"Downloading {dest.name} from {dataset_id}")
    urllib.request.urlretrieve(dl, dest)


def ownership_group(val: str) -> str:
    if not val:
        return "Other"
    if re.search(r"voluntary non-profit", val, re.I):
        return "Non-Profit"
    if re.search(r"government", val, re.I):
        return "Government"
    if re.search(r"proprietary", val, re.I):
        return "For-Profit"
    return "Other"


def penalty_tier(err: float) -> str:
    if err <= 1.0:
        return "No Penalty"
    if err <= 1.01:
        return "Low"
    if err <= 1.025:
        return "Medium"
    return "High"


def read_csv_dict(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


hrrp_path = DATA_DIR / "raw_hrrp.csv"
hosp_path = DATA_DIR / "raw_hospital_general.csv"
cms_download("9n3s-kdb3", hrrp_path)
cms_download("xubh-q36u", hosp_path)

hosp_by_id: dict[str, dict[str, str]] = {}
for row in read_csv_dict(hosp_path):
    fid = str(row["Facility ID"]).zfill(6)
    hosp_by_id[fid] = {
        "hospital_type": row.get("Hospital Type", ""),
        "hospital_ownership": row.get("Hospital Ownership", ""),
    }

joined: list[dict] = []
for row in read_csv_dict(hrrp_path):
    try:
        err = float(row["Excess Readmission Ratio"])
    except (TypeError, ValueError):
        continue
    cond = CONDITION_MAP.get(row.get("Measure Name", ""))
    if not cond:
        continue
    fid = str(row["Facility ID"]).zfill(6)
    meta = hosp_by_id.get(fid, {})
    joined.append(
        {
            "state": row["State"],
            "facility_id": fid,
            "facility_name": row["Facility Name"],
            "condition": cond,
            "err": err,
            "penalty_tier": penalty_tier(err),
            "predicted_rate": row.get("Predicted Readmission Rate", ""),
            "ownership_group": ownership_group(meta.get("hospital_ownership", "")),
            "hospital_type": meta.get("hospital_type", ""),
            "facility_class": (
                "Critical Access"
                if meta.get("hospital_type") == "Critical Access Hospitals"
                else "Acute Care"
                if meta.get("hospital_type") == "Acute Care Hospitals"
                else "Other"
            ),
        }
    )

nat_avg_pct = 100 * sum(1 for r in joined if r["err"] > 1) / len(joined)

state_acc: dict[str, list[float]] = defaultdict(list)
for r in joined:
    state_acc[r["state"]].append(r["err"])

state_summary = []
for state, errs in state_acc.items():
    n = len(errs)
    n_pen = sum(1 for e in errs if e > 1)
    pct = 100 * n_pen / n
    state_summary.append(
        {
            "state": state,
            "n": n,
            "n_penalized": n_pen,
            "pct_penalized": round(pct, 2),
            "avg_err": round(statistics.mean(errs), 6),
            "above_nat_avg": "TRUE" if pct > nat_avg_pct else "FALSE",
        }
    )
state_summary.sort(key=lambda x: x["pct_penalized"], reverse=True)

cond_acc: dict[str, list] = defaultdict(lambda: {"err": [], "pred": []})
for r in joined:
    cond_acc[r["condition"]]["err"].append(r["err"])
    try:
        cond_acc[r["condition"]]["pred"].append(float(r["predicted_rate"]))
    except (TypeError, ValueError):
        pass

condition_err = []
for cond, buckets in cond_acc.items():
    errs = buckets["err"]
    condition_err.append(
        {
            "condition": cond,
            "n": len(errs),
            "avg_err": round(statistics.mean(errs), 6),
            "pct_penalized": round(100 * sum(1 for e in errs if e > 1) / len(errs), 2),
            "avg_predicted_rate": round(statistics.mean(buckets["pred"]), 4) if buckets["pred"] else "",
        }
    )
condition_err.sort(key=lambda x: x["avg_err"], reverse=True)

own_counts: dict[tuple[str, str, str], int] = defaultdict(int)
for r in joined:
    if r["ownership_group"] not in ("Non-Profit", "Government", "For-Profit"):
        continue
    own_counts[(r["ownership_group"], r["condition"], r["penalty_tier"])] += 1
ownership_condition = [
    {"ownership_group": k[0], "condition": k[1], "penalty_tier": k[2], "n": v}
    for k, v in sorted(own_counts.items())
]

def class_summary(class_name: str) -> dict | None:
    rows = [r for r in joined if r["facility_class"] == class_name]
    errs = [r["err"] for r in rows]
    if not errs:
        return None
    return {
        "facility_class": class_name,
        "n_pairs": len(errs),
        "pct_penalized": round(100 * sum(1 for e in errs if e > 1) / len(errs), 2),
        "avg_err": round(statistics.mean(errs), 6),
    }


facility_class_err = [x for x in (class_summary("Acute Care"), class_summary("Critical Access")) if x]

safety_buckets: dict[str, list[float]] = defaultdict(list)
for r in joined:
    if r["facility_class"] != "Acute Care":
        continue
    proxy = (
        "Safety-net name proxy"
        if r["ownership_group"] in ("Government", "Non-Profit")
        and re.search(r"county|public|memorial|safety", r["facility_name"], re.I)
        else "Other acute care"
    )
    safety_buckets[proxy].append(r["err"])

safety_net_proxy = []
for label, errs in safety_buckets.items():
    safety_net_proxy.append(
        {
            "safety_net_proxy": label,
            "n_pairs": len(errs),
            "pct_penalized": round(100 * sum(1 for e in errs if e > 1) / len(errs), 2),
            "avg_err": round(statistics.mean(errs), 6),
        }
    )

penalty_timeline = [
    {
        "fiscal_year": 2013,
        "max_penalty_pct": 1,
        "share_hospitals_any_penalty_pct": "",
        "share_hospitals_penalty_1pct_or_more": "",
        "source_note": "ACA HRRP first payment year; 1% cap (CMS IPPS FY2013 final rule)",
    },
    {
        "fiscal_year": 2014,
        "max_penalty_pct": 2,
        "share_hospitals_any_penalty_pct": "",
        "share_hospitals_penalty_1pct_or_more": "",
        "source_note": "Cap rose to 2% (CMS IPPS FY2014 final rule)",
    },
    {
        "fiscal_year": 2015,
        "max_penalty_pct": 3,
        "share_hospitals_any_penalty_pct": "",
        "share_hospitals_penalty_1pct_or_more": "",
        "source_note": "Cap rose to 3%, where it remains (CMS IPPS FY2015 final rule)",
    },
    {
        "fiscal_year": 2024,
        "max_penalty_pct": 3,
        "share_hospitals_any_penalty_pct": "",
        "share_hospitals_penalty_1pct_or_more": "",
        "source_note": "CMS estimated 2,356 hospitals with operating DRG payment reductions (BDO summary of FY2024 IPPS final rule)",
    },
    {
        "fiscal_year": 2025,
        "max_penalty_pct": 3,
        "share_hospitals_any_penalty_pct": 78.6,
        "share_hospitals_penalty_1pct_or_more": 7.0,
        "source_note": "Advisory Board analysis of CMS preliminary FY2025 HRRP file",
    },
    {
        "fiscal_year": 2026,
        "max_penalty_pct": 3,
        "share_hospitals_any_penalty_pct": 79.9,
        "share_hospitals_penalty_1pct_or_more": 8.1,
        "source_note": "Advisory Board analysis of CMS preliminary FY2026 HRRP file",
    },
]

pred_2024 = {c: statistics.mean(b["pred"]) for c, b in cond_acc.items() if b["pred"]}
national_trends = [
    {"report_year": 2012, "condition": "Heart Failure", "national_readmit_rate_pct": 24.8, "source_note": "CMS national rate cited in Zuckerman et al. NEJM 2016"},
    {"report_year": 2015, "condition": "Heart Failure", "national_readmit_rate_pct": 22.0, "source_note": "Zuckerman et al. NEJM 2016"},
    {"report_year": 2012, "condition": "Pneumonia", "national_readmit_rate_pct": 18.4, "source_note": "Zuckerman et al. NEJM 2016"},
    {"report_year": 2015, "condition": "Pneumonia", "national_readmit_rate_pct": 16.7, "source_note": "Zuckerman et al. NEJM 2016"},
    {"report_year": 2012, "condition": "AMI", "national_readmit_rate_pct": 19.7, "source_note": "Zuckerman et al. NEJM 2016"},
    {"report_year": 2015, "condition": "AMI", "national_readmit_rate_pct": 16.7, "source_note": "Zuckerman et al. NEJM 2016"},
    {
        "report_year": 2024,
        "condition": "Heart Failure",
        "national_readmit_rate_pct": round(pred_2024.get("Heart Failure", 0), 1),
        "source_note": "CMS extract mean predicted readmission rate (Jul 2021–Jun 2024 window)",
    },
    {
        "report_year": 2024,
        "condition": "Pneumonia",
        "national_readmit_rate_pct": round(pred_2024.get("Pneumonia", 0), 1),
        "source_note": "CMS extract mean predicted readmission rate",
    },
    {
        "report_year": 2024,
        "condition": "AMI",
        "national_readmit_rate_pct": round(pred_2024.get("AMI", 0), 1),
        "source_note": "CMS extract mean predicted readmission rate",
    },
]

write_csv(DATA_DIR / "hrrp_state_summary.csv", state_summary, list(state_summary[0].keys()))
write_csv(DATA_DIR / "hrrp_condition_err.csv", condition_err, list(condition_err[0].keys()))
write_csv(
    DATA_DIR / "hrrp_ownership_condition.csv",
    ownership_condition,
    ["ownership_group", "condition", "penalty_tier", "n"],
)
write_csv(
    DATA_DIR / "hrrp_facility_class_err.csv",
    facility_class_err,
    ["facility_class", "n_pairs", "pct_penalized", "avg_err"],
)
write_csv(
    DATA_DIR / "hrrp_safety_net_proxy.csv",
    safety_net_proxy,
    ["safety_net_proxy", "n_pairs", "pct_penalized", "avg_err"],
)
write_csv(
    DATA_DIR / "hrrp_penalty_timeline.csv",
    penalty_timeline,
    [
        "fiscal_year",
        "max_penalty_pct",
        "share_hospitals_any_penalty_pct",
        "share_hospitals_penalty_1pct_or_more",
        "source_note",
    ],
)
write_csv(
    DATA_DIR / "hrrp_national_readmit_trends.csv",
    national_trends,
    ["report_year", "condition", "national_readmit_rate_pct", "source_note"],
)

(DATA_DIR / "SOURCE.txt").write_text(
    "\n".join(
        [
            "Artometrics READMITTED working data",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Primary CMS files:",
            "- HRRP supplemental: dataset 9n3s-kdb3 (raw_hrrp.csv)",
            "- Hospital General Information: dataset xubh-q36u (raw_hospital_general.csv)",
            "",
            "Licence: U.S. government public data (CMS Provider Data Catalog).",
            "",
            f"Working pairs after suppression filter: {len(joined)}",
            f"National penalized share: {round(nat_avg_pct, 2)}%",
        ]
    )
    + "\n",
    encoding="utf-8",
)

print(f"Wrote CSVs to {DATA_DIR} ({len(joined)} pairs, {nat_avg_pct:.2f}% penalized)")
