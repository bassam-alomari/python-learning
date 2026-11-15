# ============================================================
# Project 62 - the bookshop counts stock and reconciles it
# ============================================================
# What this project teaches:
#   stocktake           compare recorded quantity with counted quantity
#   variance            calculate counted minus expected copies
#   valuation           price the discrepancy with Decimal
#   reason codes        require a note for every adjustment
#   audit trail         keep before/after values and signed variance
#   CSV export          write a stable stocktake report
#   validation          reject unknown titles, duplicates and bad counts
#   cleanup             generated report lives in a temp folder
#
# Everything uses the standard library and a fixed inventory fixture.
# No input(), random, network or clock; monetary values use Decimal.
#
# Run it:  python project-62-the-bookshop-reconciles-stocktake.py
# ============================================================

import csv
import os
import shutil
import tempfile
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CHECKS = []
CENT = Decimal("0.01")


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class StocktakeError(ValueError):
    """Raised when a stock count cannot be reconciled."""


def reconcile_stock(records, counts):
    """Return an audit row per title, rejecting ambiguous input."""
    by_title = {row["title"].casefold(): row for row in records}
    seen = set()
    audit = []
    for count_row in counts:
        title = str(count_row.get("title", "")).strip()
        key = title.casefold()
        if not title:
            raise StocktakeError("count row is missing a title")
        if key in seen:
            raise StocktakeError("duplicate count for " + title)
        seen.add(key)
        book = by_title.get(key)
        if book is None:
            raise StocktakeError("unknown title: " + title)
        try:
            counted = int(count_row["counted"])
            price = Decimal(str(book["price"])).quantize(CENT, rounding=ROUND_HALF_UP)
        except (KeyError, TypeError, ValueError, InvalidOperation):
            raise StocktakeError("count and price must be valid numbers")
        if counted < 0:
            raise StocktakeError("count cannot be negative")
        reason = str(count_row.get("reason", "")).strip()
        expected = int(book["copies"])
        variance = counted - expected
        if variance and not reason:
            raise StocktakeError("a reason is required for a variance")
        audit.append({
            "title": book["title"],
            "expected": expected,
            "counted": counted,
            "variance": variance,
            "unit_price": price,
            "variance_value": (price * variance).quantize(CENT),
            "reason": reason if reason else "count matched",
        })
    missing_titles = sorted(set(by_title) - seen)
    if missing_titles:
        raise StocktakeError("missing counts for " + ", ".join(missing_titles))
    return audit


def write_audit(path, audit):
    """Export the stocktake audit as a CSV file."""
    fields = ("title", "expected", "counted", "variance", "unit_price",
              "variance_value", "reason")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in audit:
            exported = dict(row)
            exported["unit_price"] = "{0:.2f}".format(row["unit_price"])
            exported["variance_value"] = "{0:.2f}".format(row["variance_value"])
            writer.writerow(exported)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what does a stocktake compare")
print("Q2  how is a stock variance calculated")
print("Q3  how can a difference be valued in money")
print("Q4  why record a reason for an adjustment")
print("Q5  what happens if a title is counted twice")
print("Q6  how can the audit be kept for later review")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  expected inventory versus physical counted quantity")
print("Q2  counted minus expected")
print("Q3  multiply the signed difference by the unit price")
print("Q4  every inventory adjustment needs an audit explanation")
print("Q5  reject the ambiguous duplicate count")
print("Q6  export a CSV audit trail")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - prepare expected stock records")
print("TASK 2 - enter physical counts and reasons")
print("TASK 3 - calculate variances and values")
print("TASK 4 - reject missing, duplicate or invalid counts")
print("TASK 5 - summarize shortages and surpluses")
print("TASK 6 - export the audit CSV")
print("TASK 7 - verify the total signed adjustment value")
print("TASK 8 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project62_")
REPORT = os.path.join(WORK, "stocktake-audit.csv")
records = [
    {"title": "Dune", "price": "12.50", "copies": 8},
    {"title": "Neuromancer", "price": "9.99", "copies": 5},
    {"title": "Café Society", "price": "7.25", "copies": 3},
]
counts = [
    {"title": "dune", "counted": 7, "reason": "one copy damaged"},
    {"title": "Neuromancer", "counted": 6, "reason": "shelf recount"},
    {"title": "Café Society", "counted": 3, "reason": ""},
]

print("=" * 60)
print("TASK 1 - expected inventory")
print("=" * 60)
print("titles ->", len(records))
print("expected copies ->", sum(row["copies"] for row in records))
print("unit prices ->", ", ".join(row["price"] for row in records))
print()

print("=" * 60)
print("TASK 2 - reconcile physical counts")
print("=" * 60)
audit = reconcile_stock(records, counts)
for row in audit:
    print("{0}: expected {1}, counted {2}, variance {3}".format(
        row["title"], row["expected"], row["counted"], row["variance"]
    ))
print("all titles counted ->", check("complete stocktake", len(audit) == len(records)))
print()

print("=" * 60)
print("TASK 3 - value the variance")
print("=" * 60)
for row in audit:
    print("{0} variance value -> ${1:.2f}".format(row["title"], row["variance_value"]))
net_value = sum((row["variance_value"] for row in audit), Decimal("0.00"))
print("net adjustment value -> ${0:.2f}".format(net_value))
print("signed variance correct ->", check("variance signs", [row["variance"] for row in audit] == [-1, 1, 0]))
print()

print("=" * 60)
print("TASK 4 - reasons are required for changes")
print("=" * 60)
print("changed rows have reasons ->", check("variance reason audit", all(row["reason"] for row in audit if row["variance"])))
print("unchanged row label ->", next(row["reason"] for row in audit if row["variance"] == 0))
invalid_cases = [
    counts + [{"title": "Dune", "counted": 1, "reason": "duplicate"}],
    counts[:-1],
    [{"title": "Dune", "counted": -1, "reason": "bad count"}, counts[1], counts[2]],
    [{"title": "Dune", "counted": 7, "reason": ""}, counts[1], counts[2]],
]
invalid_messages = []
for case in invalid_cases:
    try:
        reconcile_stock(records, case)
    except StocktakeError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted")
print("invalid scenarios rejected ->", len([m for m in invalid_messages if m != "accepted"]))
print("duplicate reason ->", invalid_messages[0])
print("missing count reason ->", invalid_messages[3])
check("invalid count scenarios refused", all(m != "accepted" for m in invalid_messages))
print()

print("=" * 60)
print("TASK 5 - shortage and surplus summary")
print("=" * 60)
shortages = sum(row["variance"] < 0 for row in audit)
surpluses = sum(row["variance"] > 0 for row in audit)
print("titles short ->", shortages)
print("titles over ->", surpluses)
print("titles matched ->", sum(row["variance"] == 0 for row in audit))
print("summary covers every title ->", check("variance categories", shortages + surpluses + sum(row["variance"] == 0 for row in audit) == len(audit)))
print()

print("=" * 60)
print("TASK 6 - export audit CSV")
print("=" * 60)
fields = write_audit(REPORT, audit)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("report data rows ->", len(report_text.splitlines()) - 1)
print("reason exported ->", "one copy damaged" in report_text)
print("UTF-8 title exported ->", "Café Society" in report_text)
check("CSV contains every audited title", len(report_text.splitlines()) == len(audit) + 1)
print()

print("=" * 60)
print("TASK 7 - verify signed adjustment total")
print("=" * 60)
expected_net = Decimal("-12.50") + Decimal("9.99")
print("calculated net -> ${0:.2f}".format(net_value))
print("expected net -> ${0:.2f}".format(expected_net))
print("net value reconciles ->", check("net adjustment reconciliation", net_value == expected_net))
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary stocktake workspace removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
