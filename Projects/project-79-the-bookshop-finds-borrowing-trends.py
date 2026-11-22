# ============================================================
# Project 79 - the bookshop finds weekly borrowing trends
# ============================================================
# What this project teaches:
#   loan history       analyze fixed checkout records
#   grouping           aggregate checkout counts by title/week
#   ranking            find most-borrowed titles
#   comparisons        compare two periods and compute change
#   zero baselines     report a new title without dividing by zero
#   validation         reject duplicate loan IDs and unknown titles
#   CSV summary        export deterministic trend metrics
#   cleanup            generated report stays in a temp folder
#
# All dates are fixed fixtures; no input(), random, network or system clock.
#
# Run it:  python project-79-the-bookshop-finds-borrowing-trends.py
# ============================================================

import csv
import os
import shutil
import tempfile
from collections import Counter
from datetime import date

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class TrendError(ValueError):
    """Raised when loan-history data is invalid."""


def validate_history(rows, known_titles):
    """Check history IDs, titles and dates before aggregation."""
    seen = set()
    for row in rows:
        if not all(key in row for key in ("loan_id", "title", "checkout_date")):
            raise TrendError("loan row is missing required fields")
        if row["loan_id"] in seen:
            raise TrendError("duplicate loan ID")
        seen.add(row["loan_id"])
        if row["title"] not in known_titles:
            raise TrendError("unknown book title")
        if not isinstance(row["checkout_date"], date):
            raise TrendError("checkout date must be a date")
    return True


def borrowing_counts(rows, start, end):
    """Count checkouts in a half-open date range [start, end)."""
    return Counter(
        row["title"] for row in rows
        if start <= row["checkout_date"] < end
    )


def percent_change(previous, current):
    """Return percentage change, with a safe zero-baseline label."""
    if previous == 0:
        return None if current == 0 else "new"
    return round((current - previous) * 100 / previous, 1)


def build_trends(rows, titles, previous_start, current_start, current_end):
    """Build sorted borrowing statistics for two adjacent periods."""
    validate_history(rows, set(titles))
    previous = borrowing_counts(rows, previous_start, current_start)
    current = borrowing_counts(rows, current_start, current_end)
    result = []
    for title in titles:
        old_count = previous[title]
        new_count = current[title]
        result.append({
            "title": title,
            "previous": old_count,
            "current": new_count,
            "change_percent": percent_change(old_count, new_count),
        })
    return sorted(result, key=lambda row: (-row["current"], row["title"].casefold()))


def export_trends(path, trends):
    fields = ("title", "previous", "current", "change_percent")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in trends:
            writer.writerow(row)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how can checkout history reveal popular books")
print("Q2  how do we compare two time periods")
print("Q3  what does a zero previous count mean")
print("Q4  why should date ranges have clear boundaries")
print("Q5  how can a trend report be sorted")
print("Q6  what should happen to duplicate or unknown records")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  count each title's checkout records")
print("Q2  compare previous and current counts")
print("Q3  a title may be new; avoid dividing by zero")
print("Q4  use explicit inclusive/exclusive endpoints")
print("Q5  sort by current popularity, then title")
print("Q6  reject malformed history before aggregation")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - prepare a fixed loan-history ledger")
print("TASK 2 - count checkouts in two periods")
print("TASK 3 - calculate percentage change safely")
print("TASK 4 - rank titles by current-period popularity")
print("TASK 5 - validate duplicate IDs and unknown titles")
print("TASK 6 - export the trend table to CSV")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project79_")
REPORT = os.path.join(WORK, "borrowing-trends.csv")
TITLES = ["Dune", "Neuromancer", "Café Society", "New Horizons"]
PREVIOUS_START = date(2026, 10, 1)
CURRENT_START = date(2026, 10, 8)
CURRENT_END = date(2026, 10, 15)
loan_rows = [
    {"loan_id": "L001", "title": "Dune", "checkout_date": date(2026, 10, 1)},
    {"loan_id": "L002", "title": "Dune", "checkout_date": date(2026, 10, 3)},
    {"loan_id": "L003", "title": "Neuromancer", "checkout_date": date(2026, 10, 5)},
    {"loan_id": "L004", "title": "Dune", "checkout_date": date(2026, 10, 8)},
    {"loan_id": "L005", "title": "Dune", "checkout_date": date(2026, 10, 9)},
    {"loan_id": "L006", "title": "Dune", "checkout_date": date(2026, 10, 12)},
    {"loan_id": "L007", "title": "Neuromancer", "checkout_date": date(2026, 10, 10)},
    {"loan_id": "L008", "title": "Café Society", "checkout_date": date(2026, 10, 11)},
    {"loan_id": "L009", "title": "Café Society", "checkout_date": date(2026, 10, 13)},
    {"loan_id": "L010", "title": "New Horizons", "checkout_date": date(2026, 10, 14)},
    {"loan_id": "L011", "title": "Dune", "checkout_date": date(2026, 10, 15)},
]

print("=" * 60)
print("TASK 1 - loan history and periods")
print("=" * 60)
print("loan records ->", len(loan_rows))
print("previous period ->", PREVIOUS_START.isoformat(), "to", CURRENT_START.isoformat())
print("current period ->", CURRENT_START.isoformat(), "to", CURRENT_END.isoformat())
print("range rule -> start inclusive, end exclusive")
print()

print("=" * 60)
print("TASK 2 - count and compare borrowing")
print("=" * 60)
trends = build_trends(loan_rows, TITLES, PREVIOUS_START, CURRENT_START, CURRENT_END)
for row in trends:
    change = "new" if row["change_percent"] == "new" else "{0:.1f}%".format(row["change_percent"])
    print("{0}: previous {1}, current {2}, change {3}".format(
        row["title"], row["previous"], row["current"], change
    ))
dune_trend = next(row for row in trends if row["title"] == "Dune")
check("Dune count comparison", dune_trend["previous"] == 2 and dune_trend["current"] == 3 and dune_trend["change_percent"] == 50.0)
print()

print("=" * 60)
print("TASK 3 - rank current-period popularity")
print("=" * 60)
print("ranked titles ->", " > ".join(row["title"] for row in trends))
print("most borrowed ->", trends[0]["title"])
print("new title marked ->", next(row["change_percent"] for row in trends if row["title"] == "New Horizons"))
check("ranking and new baseline", trends[0]["title"] == "Dune" and next(row["change_percent"] for row in trends if row["title"] == "New Horizons") == "new")
print()

print("=" * 60)
print("TASK 4 - date boundaries")
print("=" * 60)
previous_counts = borrowing_counts(loan_rows, PREVIOUS_START, CURRENT_START)
current_counts = borrowing_counts(loan_rows, CURRENT_START, CURRENT_END)
print("previous total ->", sum(previous_counts.values()))
print("current total ->", sum(current_counts.values()))
print("boundary event excluded from current ->", current_counts["Dune"] == 3)
print("end-day event excluded ->", loan_rows[-1]["checkout_date"] == CURRENT_END and "L011" not in [row["loan_id"] for row in loan_rows if CURRENT_START <= row["checkout_date"] < CURRENT_END])
print()

print("=" * 60)
print("TASK 5 - invalid history is rejected")
print("=" * 60)
invalid_cases = [
    loan_rows + [dict(loan_rows[0])],
    loan_rows + [{"loan_id": "L999", "title": "Unknown Book", "checkout_date": date(2026, 10, 9)}],
]
invalid_messages = []
for invalid in invalid_cases:
    try:
        build_trends(invalid, TITLES, PREVIOUS_START, CURRENT_START, CURRENT_END)
    except TrendError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted")
print("invalid history ->", invalid_messages)
check("duplicate/unknown history rejected", invalid_messages == ["duplicate loan ID", "unknown book title"])
print()

print("=" * 60)
print("TASK 6 - export trend CSV")
print("=" * 60)
fields = export_trends(REPORT, trends)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("trend rows ->", len(report_text.splitlines()) - 1)
print("new title exported ->", "New Horizons" in report_text)
print("change field included ->", "change_percent" in fields)
check("CSV contains all titles", len(report_text.splitlines()) == len(TITLES) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary trend report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
