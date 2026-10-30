#!/usr/bin/env python3
"""Download pinned Hot 100 data and write a number-ones table.

Source: utdata/rwd-billboard-data data-out/hot-100-current.csv at commit
ff86f04. The repository code is MIT. The chart rows are Billboard's.

The table is one row per title and performer credited at No. 1: first No. 1
week, last No. 1 week, and the count of weeks at No. 1, through the chart
dated 2026-10-31.

Running this script also refreshes the Billboard issue extract:
articles/billboard/data/dataset.csv. Songs whose first No. 1 week is after
2025-01-11 are appended with weeks and dates only. Die with a Smile is set
to 5 weeks. All I Want for Christmas Is You is set to Billboard's cumulative
22 weeks. Every other existing field stays as it was.
"""

from __future__ import annotations

import csv
import sys
import tempfile
import urllib.request
from collections import defaultdict
from datetime import datetime
from io import StringIO
from pathlib import Path

PIN = "ff86f04"
FULL_PIN = "ff86f0456f55f8174ea5e91c0872a00df21b8603"
URL = (
    "https://raw.githubusercontent.com/utdata/rwd-billboard-data/"
    f"{PIN}/data-out/hot-100-current.csv"
)
CUTOFF = datetime(2026, 10, 31)
AFTER = "2025-01-11"

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "data/masters/raw/billboard"
OUT = OUT_DIR / "number_ones.csv"
ISSUE = ROOT / "articles/billboard/data/dataset.csv"
NOTE = ROOT / "articles/billboard/data/method_note.txt"

# Billboard's published longest runs, chart dated Oct 31, 2026.
# https://www.billboard.com/lists/ella-langley-choosin-texas-hot-100-number-one-25th-week
EXPECTED_WEEKS = {
    ("Choosin' Texas", "Ella Langley"): 25,
    ("All I Want For Christmas Is You", "Mariah Carey"): 22,
    ("A Bar Song (Tipsy)", "Shaboozey"): 19,
    ("Old Town Road", "Lil Nas X Featuring Billy Ray Cyrus"): 19,
    ("Last Night", "Morgan Wallen"): 16,
    ("Despacito", "Luis Fonsi & Daddy Yankee Featuring Justin Bieber"): 16,
    ("One Sweet Day", "Mariah Carey & Boyz II Men"): 16,
}

FIELDS = [
    "title",
    "performer",
    "first_no1_week",
    "last_no1_week",
    "weeks_at_number_one",
]

DIE_OLD = "Die with a Smile,Bruno Mars & Lady Gaga,2025-01-11T00:00:00Z,2,"
DIE_NEW = "Die with a Smile,Bruno Mars & Lady Gaga,2025-01-11T00:00:00Z,5,"
XMAS_OLD = "All I Want for Christmas is You,Mariah Carey,2019-12-21T00:00:00Z,8,"
XMAS_NEW = "All I Want for Christmas is You,Mariah Carey,2019-12-21T00:00:00Z,22,"

METHOD_NOTE = """All I Want for Christmas Is You is set to 22 weeks at No. 1.

That figure is Billboard's cumulative total through the chart dated Oct 31, 2026, from Gary Trust, "Ella Langley's 'Choosin' Texas' Rebounds for Record-Extending 25th Week at No. 1 on Hot 100" (Billboard, Oct. 26, 2026):
https://www.billboard.com/lists/ella-langley-choosin-texas-hot-100-number-one-25th-week

The same 22 is the count of Hot 100 weeks at No. 1 for "All I Want For Christmas Is You" by Mariah Carey in utdata/rwd-billboard-data data-out/hot-100-current.csv at commit ff86f04 (first week 2019-12-21, last week 2026-01-03).

On the issue file this replaces the TidyTuesday value of 8 in weeks_at_number_one. The row is still titled "All I Want for Christmas is You". No other column on that row was changed.
"""


def stop(message: str) -> None:
    print(f"STOP: {message}", file=sys.stderr)
    raise SystemExit(2)


def download(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(URL, dest)


def number_ones(src: Path) -> list[dict[str, str | int]]:
    groups: dict[tuple[str, str], list[datetime]] = defaultdict(list)
    with src.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["current_week"] not in {"1", "1.0"}:
                continue
            week = datetime.strptime(row["chart_week"], "%Y-%m-%d")
            if week > CUTOFF:
                continue
            groups[(row["title"], row["performer"])].append(week)

    table: list[dict[str, str | int]] = []
    for (title, performer), weeks in groups.items():
        weeks.sort()
        table.append(
            {
                "title": title,
                "performer": performer,
                "first_no1_week": weeks[0].date().isoformat(),
                "last_no1_week": weeks[-1].date().isoformat(),
                "weeks_at_number_one": len(weeks),
            }
        )
    table.sort(key=lambda row: (row["first_no1_week"], row["title"], row["performer"]))
    return table


def verify(table: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
    by_key = {(row["title"], row["performer"]): row for row in table}
    if len(by_key) != len(table):
        stop("duplicate title/performer rows in number_ones")
    for key, weeks in EXPECTED_WEEKS.items():
        got = by_key.get(key)
        if got is None or got["weeks_at_number_one"] != weeks:
            stop(f"{key[0]} / {key[1]} expected {weeks} weeks, archive has {got}")
    die = by_key.get(("Die With A Smile", "Lady Gaga & Bruno Mars"))
    if (
        die is None
        or die["weeks_at_number_one"] != 5
        or die["first_no1_week"] != "2025-01-11"
    ):
        stop(f"Die With A Smile expected 5 weeks from 2025-01-11, archive has {die}")
    fresh = [row for row in table if str(row["first_no1_week"]) > AFTER]
    if len(fresh) != 18:
        stop(f"expected 18 songs first at No. 1 after {AFTER}, got {len(fresh)}")
    latest = max(str(row["last_no1_week"]) for row in table)
    if latest != "2026-10-31":
        stop(f"expected the file to reach the chart dated 2026-10-31, last week is {latest}")
    return fresh


def write_table(table: list[dict[str, str | int]]) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(table)
    (OUT_DIR / "SOURCE.txt").write_text(
        "\n".join(
            [
                "number_ones.csv is built from utdata/rwd-billboard-data",
                "path: data-out/hot-100-current.csv",
                f"commit: {FULL_PIN}",
                "chart weeks included: current_week == 1 and chart_week <= 2026-10-31",
                "Repository code is MIT. Chart data is Billboard's.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def apply_issue(fresh: list[dict[str, str | int]]) -> None:
    text = ISSUE.read_text(encoding="utf-8")
    if text.count(DIE_OLD) + text.count(DIE_NEW) != 1:
        stop("Die with a Smile row was not found once")
    if text.count(XMAS_OLD) + text.count(XMAS_NEW) != 1:
        stop("All I Want for Christmas is You row was not found once")
    text = text.replace(DIE_OLD, DIE_NEW, 1).replace(XMAS_OLD, XMAS_NEW, 1)
    if not text.endswith("\n"):
        text += "\n"

    reader = csv.DictReader(text.splitlines())
    if reader.fieldnames is None:
        stop("issue dataset has no header")
    columns = list(reader.fieldnames)
    existing = {row["song"].casefold() for row in reader}
    missing = [row for row in fresh if str(row["title"]).casefold() not in existing]
    buffer_io = StringIO()
    writer = csv.writer(buffer_io, lineterminator="\n")
    for row in missing:
        values = [""] * len(columns)
        values[columns.index("song")] = str(row["title"])
        values[columns.index("artist")] = str(row["performer"])
        values[columns.index("date")] = f"{row['first_no1_week']}T00:00:00Z"
        values[columns.index("weeks_at_number_one")] = str(row["weeks_at_number_one"])
        writer.writerow(values)
    extra = buffer_io.getvalue()
    if extra and not text.endswith("\n"):
        text += "\n"
    ISSUE.write_text(text + extra, encoding="utf-8")
    NOTE.write_text(METHOD_NOTE, encoding="utf-8")
    print(f"Issue rows appended: {len(missing)}")


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "hot-100-current.csv"
        print(f"Downloading {URL}")
        download(src)
        table = number_ones(src)
    fresh = verify(table)
    write_table(table)
    apply_issue(fresh)
    print(f"Wrote {OUT} ({len(table)} number-one runs)")
    print(f"Wrote {NOTE}")


if __name__ == "__main__":
    main()
