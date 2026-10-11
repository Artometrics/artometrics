"""CPI-U deflator (base year configurable). FRED CPIAUCSL primary; BLS optional."""

from __future__ import annotations

import csv
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CPI_DIR = ROOT / "data/reference/cpi"
CPI_MONTHLY = CPI_DIR / "cpi_monthly.csv"
CPI_ANNUAL = CPI_DIR / "cpi_annual.csv"
SOURCE_TXT = CPI_DIR / "SOURCE.txt"

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL"
BLS_SERIES = "CUUR0000SA0"  # CPI-U All Items, U.S. city average, NSA


def _fetch_fred_monthly() -> list[tuple[str, float]]:
    with urllib.request.urlopen(FRED_CSV, timeout=60) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    rows: list[tuple[str, float]] = []
    for line in text.strip().splitlines()[1:]:
        parts = line.split(",")
        if len(parts) < 2:
            continue
        date, val = parts[0].strip(), parts[1].strip()
        if val in (".", ""):
            continue
        try:
            rows.append((date, float(val)))
        except ValueError:
            continue
    return rows


def _fetch_bls_monthly(api_key: str) -> list[tuple[str, float]]:
    # BLS API v2 — one series, all years
    payload = json.dumps(
        {
            "seriesid": [BLS_SERIES],
            "startyear": "1913",
            "endyear": str(datetime.now(timezone.utc).year),
            "registrationkey": api_key,
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.bls.gov/publicAPI/v2/timeseries/data/",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)
    out: list[tuple[str, float]] = []
    for series in data.get("Results", {}).get("series", []):
        for pt in series.get("data", []):
            year, period = pt["year"], pt["period"]
            if not period.startswith("M"):
                continue
            month = int(period[1:])
            val = float(pt["value"])
            out.append((f"{year}-{month:02d}-01", val))
    out.sort(key=lambda x: x[0])
    return out


def monthly_to_annual(monthly: list[tuple[str, float]]) -> dict[int, float]:
    buckets: dict[int, list[float]] = {}
    for date_s, val in monthly:
        year = int(date_s[:4])
        buckets.setdefault(year, []).append(val)
    return {y: sum(v) / len(v) for y, v in buckets.items()}


def refresh_cpi_cache(prefer_bls: bool = False) -> Path:
    CPI_DIR.mkdir(parents=True, exist_ok=True)
    monthly: list[tuple[str, float]]
    source_note = ""
    if prefer_bls and os.environ.get("BLS_API_KEY"):
        monthly = _fetch_bls_monthly(os.environ["BLS_API_KEY"])
        source_note = f"BLS Public API v2 series {BLS_SERIES}"
    else:
        monthly = _fetch_fred_monthly()
        source_note = "FRED series CPIAUCSL (via fredgraph.csv export)"

    with CPI_MONTHLY.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "cpi_index"])
        w.writerows(monthly)

    annual = monthly_to_annual(monthly)
    with CPI_ANNUAL.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "cpi_annual_avg"])
        for y in sorted(annual):
            w.writerow([y, f"{annual[y]:.3f}"])

    write_cpi_source_txt(source_note)
    return CPI_ANNUAL


def write_cpi_source_txt(source_note: str) -> None:
    from lib.provenance import write_source_txt

    write_source_txt(
        SOURCE_TXT,
        [
            "Artometrics CPI-U reference cache",
            f"Primary source: {source_note}",
            "Annual values: unweighted mean of monthly index levels per calendar year.",
            "Deflator: nominal_usd * (cpi_base_year / cpi_value_year).",
            "Default publication base year: 2025 USD (see scripts/data/build_real_usd_charts.py).",
        ],
        [CPI_MONTHLY, CPI_ANNUAL],
    )


def load_annual_cpi() -> dict[int, float]:
    if not CPI_ANNUAL.exists():
        refresh_cpi_cache()
    out: dict[int, float] = {}
    with CPI_ANNUAL.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[int(row["year"])] = float(row["cpi_annual_avg"])
    return out


def deflate_to_base(
    nominal: float,
    value_year: int,
    base_year: int = 2025,
    cpi: dict[int, float] | None = None,
) -> float:
    cpi = cpi or load_annual_cpi()
    by = cpi.get(base_year)
    vy = cpi.get(value_year)
    if by is None or vy is None:
        raise KeyError(f"Missing CPI for year {value_year} or base {base_year}")
    return nominal * (by / vy)
