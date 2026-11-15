# ============================================================
# Project 61 - the bookshop analyses margins and profitability
# ============================================================
# What this project teaches:
#   unit margin       selling price minus unit cost
#   margin rate       margin divided by selling price
#   stock profit      unit margin times copies on hand
#   ranking           sort titles by projected stock profit
#   warnings          flag negative or low margin records
#   CSV report        export stable, rounded profitability rows
#   validation        reject missing/invalid/negative values
#   cleanup           generated report stays in a temp folder
#
# Everything uses the standard library and fixed data. No input(),
# random, network or clock. Monetary calculations use Decimal.
#
# Run it:  python project-61-the-bookshop-analyses-margins.py
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


class MarginError(ValueError):
    """Raised when a book's cost/price data is invalid."""


def money(value):
    """Parse a nonnegative monetary amount to cents."""
    try:
        amount = Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise MarginError("money value must be numeric")
    if not amount.is_finite() or amount < 0:
        raise MarginError("money value must be finite and nonnegative")
    return amount


def analyze_book(book, low_margin_rate=Decimal("0.20")):
    """Calculate unit margin, rate, and projected stock profit."""
    required = ("title", "cost", "price", "copies")
    missing = [key for key in required if key not in book]
    if missing:
        raise MarginError("missing fields: " + ", ".join(missing))
    title = str(book["title"]).strip()
    if not title:
        raise MarginError("title is required")
    cost = money(book["cost"])
    price = money(book["price"])
    try:
        copies = int(book["copies"])
    except (TypeError, ValueError):
        raise MarginError("copies must be an integer")
    if copies < 0 or str(copies) != str(book["copies"]).strip():
        raise MarginError("copies must be a nonnegative integer")
    margin = (price - cost).quantize(CENT)
    rate = (margin / price).quantize(Decimal("0.0001")) if price else Decimal("0")
    stock_profit = (margin * copies).quantize(CENT)
    if margin < 0:
        status = "loss"
    elif rate < low_margin_rate:
        status = "low margin"
    else:
        status = "healthy"
    return {
        "title": title,
        "cost": cost,
        "price": price,
        "copies": copies,
        "unit_margin": margin,
        "margin_rate": rate,
        "stock_profit": stock_profit,
        "status": status,
    }


def analyze_catalogue(books):
    """Analyze all books and return rows sorted by stock profit."""
    results = [analyze_book(book) for book in books]
    return sorted(results, key=lambda row: (-row["stock_profit"], row["title"].casefold()))


def write_report(path, rows):
    """Write a CSV profitability report with stable formatting."""
    fields = ("title", "cost", "price", "copies", "unit_margin",
              "margin_percent", "stock_profit", "status")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "title": row["title"],
                "cost": "{0:.2f}".format(row["cost"]),
                "price": "{0:.2f}".format(row["price"]),
                "copies": row["copies"],
                "unit_margin": "{0:.2f}".format(row["unit_margin"]),
                "margin_percent": "{0:.2f}".format(row["margin_rate"] * 100),
                "stock_profit": "{0:.2f}".format(row["stock_profit"]),
                "status": row["status"],
            })
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how much does each copy earn before overhead")
print("Q2  what percentage of the selling price is margin")
print("Q3  what is the projected profit in current stock")
print("Q4  how do we find books with weak or negative margins")
print("Q5  why use Decimal for money")
print("Q6  how can the report be sorted and exported")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  selling price minus unit cost")
print("Q2  unit margin divided by selling price")
print("Q3  unit margin times copies on hand")
print("Q4  classify each row by its margin rate and sign")
print("Q5  Decimal avoids binary floating-point money surprises")
print("Q6  sort by projected profit and write a CSV report")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - prepare cost/price/stock records")
print("TASK 2 - calculate unit and percentage margin")
print("TASK 3 - calculate projected profit for current stock")
print("TASK 4 - classify healthy, low-margin and loss titles")
print("TASK 5 - rank books by projected stock profit")
print("TASK 6 - reject invalid prices and quantities")
print("TASK 7 - export the analysis to CSV")
print("TASK 8 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project61_")
REPORT = os.path.join(WORK, "profitability.csv")
books = [
    {"title": "Dune", "cost": "7.00", "price": "12.50", "copies": 4},
    {"title": "Neuromancer", "cost": "8.50", "price": "9.99", "copies": 3},
    {"title": "Café Society", "cost": "6.00", "price": "7.25", "copies": 2},
    {"title": "Loss Leader", "cost": "11.00", "price": "10.00", "copies": 1},
]

print("=" * 60)
print("TASK 1 - catalogue inputs")
print("=" * 60)
print("books ->", len(books))
print("first title ->", books[0]["title"])
print("prices and costs are text inputs ->", isinstance(books[0]["cost"], str))
print()

print("=" * 60)
print("TASK 2 - unit margins and rates")
print("=" * 60)
rows = analyze_catalogue(books)
by_title = {row["title"]: row for row in rows}
print("Dune unit margin -> ${0:.2f}".format(by_title["Dune"]["unit_margin"]))
print("Dune margin rate -> {0:.2f}%".format(by_title["Dune"]["margin_rate"] * 100))
print("Neuromancer unit margin -> ${0:.2f}".format(by_title["Neuromancer"]["unit_margin"]))
print("Dune calculation correct ->", check("Dune margin math", by_title["Dune"]["unit_margin"] == Decimal("5.50") and by_title["Dune"]["margin_rate"] == Decimal("0.4400")))
print()

print("=" * 60)
print("TASK 3 - projected profit in stock")
print("=" * 60)
print("Dune stock profit -> ${0:.2f}".format(by_title["Dune"]["stock_profit"]))
print("catalogue stock profit -> ${0:.2f}".format(sum(row["stock_profit"] for row in rows)))
print("stock profit uses copies ->", check("stock profit formula", by_title["Dune"]["stock_profit"] == Decimal("22.00")))
print()

print("=" * 60)
print("TASK 4 - classify margins")
print("=" * 60)
for row in sorted(rows, key=lambda item: item["title"].casefold()):
    print("{0} -> {1}".format(row["title"], row["status"]))
print("loss identified ->", check("negative margin classified", by_title["Loss Leader"]["status"] == "loss"))
print("low margin identified ->", check("low margin classified", by_title["Neuromancer"]["status"] == "low margin"))
print()

print("=" * 60)
print("TASK 5 - rank by projected stock profit")
print("=" * 60)
print("ranking ->", " > ".join(row["title"] for row in rows))
print("highest is Dune ->", check("profit sort descending", rows[0]["title"] == "Dune"))
print("last is loss leader ->", rows[-1]["title"])
print()

print("=" * 60)
print("TASK 6 - reject invalid input")
print("=" * 60)
invalid_cases = [
    {"title": "Bad Cost", "cost": "x", "price": "4", "copies": 1},
    {"title": "Negative", "cost": "1", "price": "4", "copies": -1},
    {"title": "Missing", "price": "4", "copies": 1},
]
messages = []
for item in invalid_cases:
    try:
        analyze_book(item)
    except MarginError as error:
        messages.append(str(error))
    else:
        messages.append("accepted")
print("invalid cases rejected ->", messages)
print("all invalid rows refused ->", check("invalid input rejected", all(message != "accepted" for message in messages)))
print()

print("=" * 60)
print("TASK 7 - export profitability CSV")
print("=" * 60)
fields = write_report(REPORT, rows)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("CSV data rows ->", len(report_text.splitlines()) - 1)
print("report includes margin percent ->", "margin_percent" in fields)
print("UTF-8 title exported ->", "Café Society" in report_text)
check("CSV contains all books", len(report_text.splitlines()) == len(books) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
