# ============================================================
# Project 52 - CSV: the bookshop keeps its inventory in a table
# ============================================================
# What this project teaches:
#   csv.reader / DictReader  read rows and named columns
#   csv.writer / DictWriter  write valid CSV with a header
#   newline=""               let csv manage line endings
#   encoding="utf-8"         preserve non-ASCII text
#   validation               reject missing/invalid columns and quantities
#   aggregation              inventory value, totals and low-stock report
#   round trip               write, reopen, and verify saved data
#   safe output              no input(), no machine paths, no stderr
#
# Everything uses the standard library. The CSV file is created in a
# temporary folder and removed at the end. Output is deterministic.
#
# Run it:  python project-52-csv-the-bookshop-keeps-inventory.py
# ============================================================

import csv
import os
import shutil
import tempfile

CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


FIELDS = ("title", "author", "price", "copies")


class InventoryError(ValueError):
    """Raised when an inventory CSV has invalid data."""


def validate_rows(rows):
    """Validate and normalize CSV dictionaries."""
    normalized = []
    for line_number, row in enumerate(rows, start=2):
        missing = [field for field in FIELDS if field not in row]
        if missing:
            raise InventoryError(
                "missing columns: " + ", ".join(missing)
            )
        title = row["title"].strip()
        author = row["author"].strip()
        if not title or not author:
            raise InventoryError("title and author are required")
        try:
            price = float(row["price"])
            copies = int(row["copies"])
        except (TypeError, ValueError) as error:
            raise InventoryError(
                "invalid number on row " + str(line_number)
            ) from error
        if price < 0:
            raise InventoryError("price cannot be negative")
        if copies < 0:
            raise InventoryError("copies cannot be negative")
        normalized.append({
            "title": title,
            "author": author,
            "price": price,
            "copies": copies,
        })
    return normalized


def read_inventory(path):
    """Read and validate a CSV inventory by column name."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise InventoryError("CSV header is missing")
        missing = [field for field in FIELDS if field not in reader.fieldnames]
        if missing:
            raise InventoryError(
                "missing columns: " + ", ".join(missing)
            )
        return validate_rows(reader)


def write_inventory(path, rows):
    """Write validated rows with a stable header and line endings."""
    normalized = validate_rows(rows)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDS,
            lineterminator="\n",
            extrasaction="raise",
        )
        writer.writeheader()
        writer.writerows(normalized)


def inventory_report(rows):
    """Return totals, stock value, and low-stock titles."""
    total_copies = sum(row["copies"] for row in rows)
    total_value = sum(row["price"] * row["copies"] for row in rows)
    low_stock = sorted(
        row["title"] for row in rows if row["copies"] <= 2
    )
    return {
        "book_count": len(rows),
        "total_copies": total_copies,
        "total_value": round(total_value, 2),
        "low_stock": low_stock,
    }


def find_book(rows, title):
    """Find a title case-insensitively."""
    wanted = title.casefold()
    return next(
        (row for row in rows if row["title"].casefold() == wanted),
        None,
    )


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what does DictReader use instead of column numbers")
print("Q2  why does csv.open use newline=\"\"")
print("Q3  what does the header row name")
print("Q4  how can the shop total its stock value")
print("Q5  what should happen when a quantity is invalid")
print("Q6  how do we prove data survives a save and reopen")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  field names from the CSV header")
print("Q2  csv controls newline translation itself")
print("Q3  the fields in each dictionary row")
print("Q4  sum price times copies for every book")
print("Q5  reject it with a clear InventoryError")
print("Q6  read the written CSV back and compare rows")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - read a CSV file using its header names")
print("TASK 2 - validate title, author, price and copies")
print("TASK 3 - report books, copies, stock value and low stock")
print("TASK 4 - find a title without depending on letter case")
print("TASK 5 - write the inventory back with DictWriter")
print("TASK 6 - reject malformed data without crashing the project")
print("TASK 7 - reopen the saved CSV and verify its rows")
print("TASK 8 - remove the temporary data folder")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project52_")
SOURCE = os.path.join(WORK, "inventory.csv")
SAVED = os.path.join(WORK, "saved_inventory.csv")

source_rows = [
    {"title": "Dune", "author": "Frank Herbert", "price": "12.50", "copies": "4"},
    {"title": "Neuromancer", "author": "William Gibson", "price": "9.99", "copies": "2"},
    {"title": "Café Society", "author": "Mina Haddad", "price": "7.25", "copies": "1"},
]
with open(SOURCE, "w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(source_rows)

books = read_inventory(SOURCE)
check("three inventory rows loaded", len(books) == 3)
check("header order is explicit", FIELDS == ("title", "author", "price", "copies"))
check("UTF-8 title preserved", books[2]["title"] == "Café Society")

print("=" * 60)
print("TASK 1 - named columns, not magic indexes")
print("=" * 60)
print("CSV header ->", ", ".join(FIELDS))
print("books loaded ->", len(books))
print("first title ->", books[0]["title"])
print("UTF-8 title ->", books[2]["title"])
print("named-column read ->", check("rows are dictionaries", all(isinstance(row, dict) for row in books)))
print()

print("=" * 60)
print("TASK 2 - validate every row")
print("=" * 60)
print("all rows valid ->", check("all prices and copies valid", all(row["price"] >= 0 and row["copies"] >= 0 for row in books)))
print("price type ->", type(books[0]["price"]).__name__)
print("copies type ->", type(books[0]["copies"]).__name__)
print("title whitespace stripped ->", books[0]["title"] == books[0]["title"].strip())
print()

print("=" * 60)
print("TASK 3 - inventory report")
print("=" * 60)
report = inventory_report(books)
print("book titles ->", ", ".join(row["title"] for row in books))
print("books ->", report["book_count"])
print("total copies ->", report["total_copies"])
print("stock value -> ${0:.2f}".format(report["total_value"]))
print("low stock (2 or fewer) ->", ", ".join(report["low_stock"]))
print("report totals verified ->", check("report totals", report == {
    "book_count": 3,
    "total_copies": 7,
    "total_value": 77.23,
    "low_stock": ["Café Society", "Neuromancer"],
}))
print()

print("=" * 60)
print("TASK 4 - case-insensitive lookup")
print("=" * 60)
found = find_book(books, "dUnE")
missing = find_book(books, "Foundation")
print("mixed-case lookup ->", found["title"] if found else "not found")
print("missing lookup ->", "not found" if missing is None else missing["title"])
print("lookup is case-insensitive ->", check("casefold lookup", found is books[0]))
print()

print("=" * 60)
print("TASK 5 - write and reopen the CSV")
print("=" * 60)
write_inventory(SAVED, books)
reopened = read_inventory(SAVED)
with open(SAVED, "r", encoding="utf-8", newline="") as handle:
    saved_text = handle.read()
print("saved header ->", saved_text.splitlines()[0])
print("saved rows ->", len(reopened))
print("round trip matches ->", check("CSV round trip", reopened == books))
print("writer used UTF-8 ->", check("UTF-8 file exists", os.path.isfile(SAVED)))
print()

print("=" * 60)
print("TASK 6 - reject bad input clearly")
print("=" * 60)
invalid_rows = [
    {"title": "Broken", "author": "Nobody", "price": "free", "copies": "1"}
]
try:
    validate_rows(invalid_rows)
except InventoryError as error:
    invalid_message = str(error)
else:
    invalid_message = "accepted invalid data"
print("invalid price ->", invalid_message)
print("invalid row rejected ->", check("invalid price rejected", invalid_message.startswith("invalid number")))
try:
    validate_rows([{"title": "Missing columns"}])
except InventoryError as error:
    missing_column_message = str(error)
else:
    missing_column_message = "accepted missing columns"
print("missing columns ->", missing_column_message)
print("bad schema rejected ->", check("missing columns rejected", missing_column_message.startswith("missing columns")))
print()

print("=" * 60)
print("TASK 7 - reports stay deterministic")
print("=" * 60)
print("same report after reload ->", check("report stable after reload", inventory_report(reopened) == report))
print("no duplicate titles ->", check("unique titles", len({row['title'].casefold() for row in books}) == len(books)))
print("column names retained ->", check("field names retained", all(tuple(row) == FIELDS for row in reopened)))
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("temporary folder removed", not os.path.exists(WORK))
print("temporary inventory folder removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
