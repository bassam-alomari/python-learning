# ============================================================
# Project 84 - the bookshop finds slow-moving stock
# ============================================================
# What this project teaches:
#   last activity       measure days since the most recent checkout
#   velocity            estimate borrowing pace over an observation window
#   carrying cost      estimate shelf/handling cost with Decimal
#   classification     active, slow-moving or dormant titles
#   action suggestion   keep, promote or consider donating
#   validation         reject malformed dates, costs and duplicate titles
#   CSV report          export one actionable row per title
#   deterministic      fixed as-of date; no system clock is read
#
# Run it:  python project-84-the-bookshop-finds-slow-moving-stock.py
# ============================================================

import csv
import os
import shutil
import tempfile
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CHECKS = []
CENT = Decimal("0.01")


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class SlowStockError(ValueError):
    """Raised when activity or carrying-cost input is invalid."""


def analyze_title(record, as_of, observation_days=90):
    required = ("title", "copies", "last_checkout", "unit_cost")
    missing = [field for field in required if field not in record]
    if missing:
        raise SlowStockError("missing fields: " + ", ".join(missing))
    title = str(record["title"]).strip()
    if not title:
        raise SlowStockError("title is required")
    try:
        copies = int(record["copies"])
        unit_cost = Decimal(str(record["unit_cost"])).quantize(CENT, rounding=ROUND_HALF_UP)
    except (TypeError, ValueError, InvalidOperation):
        raise SlowStockError("copies and unit cost must be numeric")
    if copies < 0 or unit_cost < 0 or observation_days <= 0:
        raise SlowStockError("copies/cost must be nonnegative and window positive")
    last_checkout = record["last_checkout"]
    if last_checkout is not None and not isinstance(last_checkout, date):
        raise SlowStockError("last_checkout must be a date or None")
    if last_checkout is None:
        days_idle = None
        activity_rate = Decimal("0.00")
        status = "dormant"
    else:
        days_idle = (as_of - last_checkout).days
        if days_idle < 0:
            raise SlowStockError("last checkout cannot be in the future")
        activity_rate = (Decimal("1") / Decimal(max(1, days_idle + 1))).quantize(Decimal("0.0001"))
        status = "active" if days_idle <= 30 else "slow-moving" if days_idle <= 90 else "dormant"
    carrying_cost = (unit_cost * copies * Decimal("0.02")).quantize(CENT, rounding=ROUND_HALF_UP)
    action = "keep" if status == "active" else "promote" if status == "slow-moving" else "review/donate"
    return {
        "title": title,
        "copies": copies,
        "unit_cost": unit_cost,
        "last_checkout": last_checkout,
        "days_idle": days_idle,
        "activity_rate": activity_rate,
        "carrying_cost": carrying_cost,
        "status": status,
        "action": action,
    }


def analyze_catalogue(records, as_of, observation_days=90):
    rows = [analyze_title(record, as_of, observation_days) for record in records]
    seen = set()
    for row in rows:
        key = row["title"].casefold()
        if key in seen:
            raise SlowStockError("duplicate title in catalogue")
        seen.add(key)
    return sorted(rows, key=lambda row: (row["days_idle"] is not None,
                                         -(row["days_idle"] or 0), row["title"].casefold()))


def export_slow_stock(path, rows):
    fields = ("title", "copies", "last_checkout", "days_idle", "activity_rate",
              "unit_cost", "carrying_cost", "status", "action")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["last_checkout"] = row["last_checkout"].isoformat() if row["last_checkout"] else "never"
            output["days_idle"] = row["days_idle"] if row["days_idle"] is not None else ""
            output["activity_rate"] = "{0:.4f}".format(row["activity_rate"])
            output["unit_cost"] = "{0:.2f}".format(row["unit_cost"])
            output["carrying_cost"] = "{0:.2f}".format(row["carrying_cost"])
            writer.writerow(output)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how can the shop identify books that rarely move")
print("Q2  how are days since last checkout calculated")
print("Q3  why estimate the cost of keeping stock on shelves")
print("Q4  what actions may fit different activity levels")
print("Q5  how should a never-borrowed title be represented")
print("Q6  why should activity analysis use a fixed as-of date")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  compare last checkout dates and activity windows")
print("Q2  report date minus most recent checkout date")
print("Q3  storage and handling tie up money")
print("Q4  keep active titles, promote slow titles, review dormant ones")
print("Q5  use None/never rather than inventing a date")
print("Q6  fixed dates make results repeatable")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - prepare a fixed catalogue and as-of date")
print("TASK 2 - calculate idle days and stock status")
print("TASK 3 - classify keep/promote/review actions")
print("TASK 4 - estimate carrying cost")
print("TASK 5 - reject duplicate and impossible records")
print("TASK 6 - export the slow-stock report")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project84_")
REPORT = os.path.join(WORK, "slow-stock.csv")
AS_OF = date(2026, 11, 24)
records = [
    {"title": "Dune", "copies": 5, "last_checkout": date(2026, 11, 20), "unit_cost": "7.00"},
    {"title": "Neuromancer", "copies": 3, "last_checkout": date(2026, 9, 10), "unit_cost": "8.50"},
    {"title": "Café Society", "copies": 2, "last_checkout": None, "unit_cost": "6.00"},
    {"title": "Kindred", "copies": 4, "last_checkout": date(2026, 7, 1), "unit_cost": "9.25"},
]

print("=" * 60)
print("TASK 1 - catalogue and as-of date")
print("=" * 60)
print("titles ->", len(records))
print("as-of date ->", AS_OF.isoformat())
print("observation window ->", 90, "days")
print()

print("=" * 60)
print("TASK 2 - classify stock activity")
print("=" * 60)
rows = analyze_catalogue(records, AS_OF)
for row in sorted(rows, key=lambda item: item["title"].casefold()):
    idle = "never" if row["days_idle"] is None else str(row["days_idle"])
    print("{0}: idle {1}, {2}".format(row["title"], idle, row["status"]))
print("Dune active ->", next(row for row in rows if row["title"] == "Dune")["status"])
print("Café never borrowed ->", next(row for row in rows if row["title"] == "Café Society")["days_idle"] is None)
check("activity classes", {row["status"] for row in rows} == {"active", "slow-moving", "dormant"})
print()

print("=" * 60)
print("TASK 3 - suggest inventory actions")
print("=" * 60)
for row in sorted(rows, key=lambda item: item["title"].casefold()):
    print("{0} -> {1}".format(row["title"], row["action"]))
print("action mapping correct ->", check("actions map to statuses", all((row["status"], row["action"]) in (("active", "keep"), ("slow-moving", "promote"), ("dormant", "review/donate")) for row in rows)))
print()

print("=" * 60)
print("TASK 4 - carrying cost estimate")
print("=" * 60)
for row in sorted(rows, key=lambda item: item["title"].casefold()):
    print("{0}: ${1:.2f}".format(row["title"], row["carrying_cost"]))
total_carrying = sum((row["carrying_cost"] for row in rows), Decimal("0.00"))
print("total carrying cost -> ${0:.2f}".format(total_carrying))
print("Dune cost estimate -> ${0:.2f}".format(next(row for row in rows if row["title"] == "Dune")["carrying_cost"]))
check("carrying cost formula", total_carrying == Decimal("2.19"))
print()

print("=" * 60)
print("TASK 5 - invalid catalogue data is rejected")
print("=" * 60)
invalid = [
    dict(records[0], copies=-1),
    dict(records[0], last_checkout=date(2026, 12, 1)),
    dict(records[0], unit_cost="bad"),
]
messages = []
for record in invalid:
    try:
        analyze_title(record, AS_OF)
    except SlowStockError as error:
        messages.append(str(error))
    else:
        messages.append("accepted")
print("invalid cases ->", messages)
print("all invalid values refused ->", check("invalid records refused", all(message != "accepted" for message in messages)))
try:
    analyze_catalogue(records + [dict(records[0])], AS_OF)
except SlowStockError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
print("duplicate title ->", duplicate_message)
check("duplicate titles rejected", duplicate_message == "duplicate title in catalogue")
print()

print("=" * 60)
print("TASK 6 - export slow-stock report")
print("=" * 60)
fields = export_slow_stock(REPORT, rows)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("report rows ->", len(report_text.splitlines()) - 1)
print("dormant action exported ->", "review/donate" in report_text)
print("never-borrowed value exported ->", "Café Society" in report_text and ",never," in report_text)
print("activity rate field included ->", "activity_rate" in fields)
check("all titles exported", len(report_text.splitlines()) == len(records) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary slow-stock report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
