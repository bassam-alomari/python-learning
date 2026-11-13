# ============================================================
# Project 57 - the bookshop closes the day and reconciles sales
# ============================================================
# What this project teaches:
#   receipt ledger        collect completed sales as records
#   daily aggregation     count sales and total revenue
#   group by payment      reconcile cash/card totals
#   group by title        find best-selling books
#   inventory audit       compare opening stock with sold copies
#   CSV report            export a deterministic end-of-day summary
#   validation            reject malformed or impossible receipts
#   cleanup               all generated files live in a temp folder
#
# This continues projects 54-56. Only the standard library is used.
# No input(), random, network or current time; the sample ledger is fixed.
#
# Run it:  python project-57-the-bookshop-closes-and-reconciles-sales.py
# ============================================================

import csv
import os
import shutil
import tempfile
from collections import defaultdict

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class ReconciliationError(ValueError):
    """Raised when a sales ledger is inconsistent."""


def validate_receipts(receipts, opening_stock):
    """Validate receipt fields and ensure sales fit available stock."""
    required = {"receipt_id", "title", "quantity", "unit_price", "payment"}
    seen_ids = set()
    sold = defaultdict(int)
    for receipt in receipts:
        if not isinstance(receipt, dict) or not required.issubset(receipt):
            raise ReconciliationError("receipt is missing required fields")
        receipt_id = receipt["receipt_id"]
        if receipt_id in seen_ids:
            raise ReconciliationError("duplicate receipt ID")
        seen_ids.add(receipt_id)
        if receipt["payment"] not in ("cash", "card"):
            raise ReconciliationError("unsupported payment method")
        if not isinstance(receipt["quantity"], int) or receipt["quantity"] <= 0:
            raise ReconciliationError("quantity must be a positive integer")
        if receipt["unit_price"] < 0:
            raise ReconciliationError("unit price cannot be negative")
        sold[receipt["title"]] += receipt["quantity"]

    for title, count in sold.items():
        if title not in opening_stock:
            raise ReconciliationError("sale references unknown title")
        if count > opening_stock[title]:
            raise ReconciliationError("sold quantity exceeds opening stock")
    return dict(sold)


def reconcile(receipts, opening_stock):
    """Create deterministic daily summary data from receipts."""
    sold = validate_receipts(receipts, opening_stock)
    by_payment = defaultdict(float)
    by_title = defaultdict(float)
    total_revenue = 0.0
    for receipt in receipts:
        amount = round(receipt["quantity"] * receipt["unit_price"], 2)
        total_revenue += amount
        by_payment[receipt["payment"]] += amount
        by_title[receipt["title"]] += amount
    remaining = {
        title: opening_stock[title] - sold.get(title, 0)
        for title in sorted(opening_stock)
    }
    best_sellers = sorted(
        sold.items(), key=lambda item: (-item[1], item[0].casefold())
    )
    return {
        "receipt_count": len(receipts),
        "item_count": sum(sold.values()),
        "total_revenue": round(total_revenue, 2),
        "by_payment": {key: round(value, 2) for key, value in sorted(by_payment.items())},
        "by_title": {key: round(value, 2) for key, value in sorted(by_title.items())},
        "sold": sold,
        "remaining": remaining,
        "best_sellers": best_sellers,
    }


def write_daily_report(path, summary):
    """Write a compact CSV report with stable ordering."""
    fields = ("section", "name", "quantity", "amount")
    rows = []
    rows.append({"section": "total", "name": "all sales", "quantity": summary["item_count"], "amount": summary["total_revenue"]})
    for method, amount in summary["by_payment"].items():
        rows.append({"section": "payment", "name": method, "quantity": "", "amount": amount})
    for title, amount in summary["by_title"].items():
        rows.append({"section": "title", "name": title, "quantity": summary["sold"][title], "amount": amount})
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what does an end-of-day reconciliation compare")
print("Q2  how can sales be grouped by payment method")
print("Q3  how do we detect stock sold beyond the opening count")
print("Q4  what is the remaining stock after today's sales")
print("Q5  how can the summary be exported for accounting")
print("Q6  what should happen to duplicate receipt IDs")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  receipt ledger totals, payment totals and inventory counts")
print("Q2  aggregate each receipt by cash or card")
print("Q3  reject totals greater than the opening inventory")
print("Q4  opening copies minus all completed-sale quantities")
print("Q5  export stable rows to a CSV file")
print("Q6  reject them, because duplicate transactions corrupt totals")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - prepare a small opening stock and receipt ledger")
print("TASK 2 - validate the receipts against opening stock")
print("TASK 3 - calculate daily sales and revenue")
print("TASK 4 - reconcile cash and card totals")
print("TASK 5 - find best sellers and remaining inventory")
print("TASK 6 - reject duplicate or impossible receipt data")
print("TASK 7 - export a CSV end-of-day report")
print("TASK 8 - clean up the temporary report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project57_")
REPORT_PATH = os.path.join(WORK, "daily-reconciliation.csv")
opening_stock = {"Dune": 8, "Neuromancer": 5, "Café Society": 3}
receipts = [
    {"receipt_id": "R001", "title": "Dune", "quantity": 2, "unit_price": 12.50, "payment": "cash"},
    {"receipt_id": "R002", "title": "Neuromancer", "quantity": 1, "unit_price": 9.99, "payment": "card"},
    {"receipt_id": "R003", "title": "Dune", "quantity": 1, "unit_price": 12.50, "payment": "card"},
    {"receipt_id": "R004", "title": "Café Society", "quantity": 1, "unit_price": 7.25, "payment": "cash"},
]

print("=" * 60)
print("TASK 1 - opening stock and receipt ledger")
print("=" * 60)
print("opening titles ->", len(opening_stock))
print("receipts ->", len(receipts))
print("opening copies ->", sum(opening_stock.values()))
print("unique receipt IDs ->", len({receipt["receipt_id"] for receipt in receipts}))
print()

print("=" * 60)
print("TASK 2 - validate stock and receipts")
print("=" * 60)
sold = validate_receipts(receipts, opening_stock)
print("sold quantities ->", dict(sorted(sold.items())))
print("all sales fit opening stock ->", check("stock not oversold", all(sold[title] <= opening_stock[title] for title in sold)))
print("all receipt IDs unique ->", check("receipt IDs unique", len({r["receipt_id"] for r in receipts}) == len(receipts)))
print()

print("=" * 60)
print("TASK 3 - calculate daily totals")
print("=" * 60)
summary = reconcile(receipts, opening_stock)
print("receipts processed ->", summary["receipt_count"])
print("items sold ->", summary["item_count"])
print("daily revenue -> ${0:.2f}".format(summary["total_revenue"]))
print("revenue matches receipt sum ->", check("revenue total", summary["total_revenue"] == 54.74))
print()

print("=" * 60)
print("TASK 4 - payment reconciliation")
print("=" * 60)
print("cash total -> ${0:.2f}".format(summary["by_payment"]["cash"]))
print("card total -> ${0:.2f}".format(summary["by_payment"]["card"]))
print("payments sum to revenue ->", check("payment reconciliation", round(sum(summary["by_payment"].values()), 2) == summary["total_revenue"]))
print()

print("=" * 60)
print("TASK 5 - best sellers and remaining stock")
print("=" * 60)
print("best seller ->", summary["best_sellers"][0][0])
print("best seller quantity ->", summary["best_sellers"][0][1])
print("remaining stock ->", summary["remaining"])
print("remaining copy count ->", sum(summary["remaining"].values()))
print("stock equation holds ->", check("opening equals sold plus remaining", sum(opening_stock.values()) == summary["item_count"] + sum(summary["remaining"].values())))
print()

print("=" * 60)
print("TASK 6 - reject duplicate and impossible receipts")
print("=" * 60)
duplicate_receipts = receipts + [dict(receipts[0])]
try:
    validate_receipts(duplicate_receipts, opening_stock)
except ReconciliationError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
print("duplicate receipt ->", duplicate_message)
print("duplicate rejected ->", check("duplicate receipt refused", duplicate_message == "duplicate receipt ID"))
over_sale = receipts + [{"receipt_id": "R999", "title": "Dune", "quantity": 99, "unit_price": 12.5, "payment": "cash"}]
try:
    validate_receipts(over_sale, opening_stock)
except ReconciliationError as error:
    over_sale_message = str(error)
else:
    over_sale_message = "accepted"
print("oversold inventory ->", over_sale_message)
print("oversell rejected ->", check("oversell refused", over_sale_message == "sold quantity exceeds opening stock"))
print()

print("=" * 60)
print("TASK 7 - export CSV for accounting")
print("=" * 60)
report_rows = write_daily_report(REPORT_PATH, summary)
with open(REPORT_PATH, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("report data rows ->", report_rows)
print("report includes Café ->", "Café Society" in report_text)
print("report file exists ->", os.path.isfile(REPORT_PATH))
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary report folder removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
