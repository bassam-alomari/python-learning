# ============================================================
# Project 54 - the bookshop sells stock and snapshots it safely
# ============================================================
# What this project teaches:
#   CSV input          load the starting catalogue by column name
#   domain operation   sell books without allowing negative stock
#   atomic persistence write JSON through a temp file and os.replace
#   backup validation  reject corrupt or incompatible snapshots
#   rollback           failed writes leave the last good snapshot intact
#   transaction flow   validate, calculate, persist, then publish result
#   cleanup            all files live in a temporary workspace
#
# This project combines projects 52 (CSV inventory) and 53 (JSON backup).
# It uses only the standard library, no input(), no random, no clock.
# The scenario is deterministic and runs entirely in a temporary folder.
#
# Run it:  python project-54-the-bookshop-sells-and-snapshots-safely.py
# ============================================================

import csv
import json
import os
import shutil
import tempfile

CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


FIELDS = ("title", "author", "price", "copies")


class ShopError(ValueError):
    """Raised when a sale or persistence operation is invalid."""


def read_catalogue(path):
    """Read a CSV catalogue and validate its basic record shape."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(FIELDS):
            raise ShopError("unexpected catalogue columns")
        books = []
        for row in reader:
            try:
                price = float(row["price"])
                copies = int(row["copies"])
            except (TypeError, ValueError) as error:
                raise ShopError("invalid catalogue number") from error
            if not row["title"].strip() or not row["author"].strip():
                raise ShopError("title and author are required")
            if price < 0 or copies < 0:
                raise ShopError("price and copies cannot be negative")
            books.append({
                "title": row["title"].strip(),
                "author": row["author"].strip(),
                "price": round(price, 2),
                "copies": copies,
            })
        return books


def make_snapshot(books):
    """Create a small versioned persistence document."""
    return {
        "format": "bookshop-state",
        "version": 1,
        "books": [dict(book) for book in books],
    }


def validate_snapshot(snapshot):
    """Check a loaded snapshot before trusting its contents."""
    if not isinstance(snapshot, dict):
        raise ShopError("snapshot root must be an object")
    if snapshot.get("format") != "bookshop-state" or snapshot.get("version") != 1:
        raise ShopError("unsupported snapshot format or version")
    books = snapshot.get("books")
    if not isinstance(books, list):
        raise ShopError("snapshot books must be a list")
    for book in books:
        if not isinstance(book, dict) or any(key not in book for key in FIELDS):
            raise ShopError("snapshot book is missing required fields")
        if int(book["copies"]) < 0 or float(book["price"]) < 0:
            raise ShopError("snapshot contains negative stock or price")
    return books


def atomic_save(path, snapshot):
    """Write a complete snapshot, then atomically replace its target."""
    validate_snapshot(snapshot)
    temporary = path + ".tmp"
    try:
        with open(temporary, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(snapshot, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)


def load_snapshot(path):
    """Read and validate a saved snapshot."""
    with open(path, "r", encoding="utf-8") as handle:
        return validate_snapshot(json.load(handle))


def sell(books, title, quantity):
    """Sell quantity copies and return a receipt, without partial changes."""
    if not isinstance(quantity, int) or quantity <= 0:
        raise ShopError("quantity must be a positive integer")
    wanted = title.casefold()
    book = next((item for item in books if item["title"].casefold() == wanted), None)
    if book is None:
        raise ShopError("book not found")
    if book["copies"] < quantity:
        raise ShopError("not enough copies")
    book["copies"] -= quantity
    return {
        "title": book["title"],
        "quantity": quantity,
        "unit_price": book["price"],
        "total": round(book["price"] * quantity, 2),
        "remaining": book["copies"],
    }


def restore_into(target_books, snapshot_books):
    """Replace in-memory inventory only after validating the snapshot."""
    validated = validate_snapshot({
        "format": "bookshop-state",
        "version": 1,
        "books": snapshot_books,
    })
    target_books[:] = [dict(book) for book in validated]


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  when should a sale update the stock count")
print("Q2  how do we prevent selling more than we have")
print("Q3  why save through a temporary file")
print("Q4  what should happen if snapshot validation fails")
print("Q5  how can we prove a restart restores the sale")
print("Q6  what should a sale receipt contain")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  after validating the title and available quantity")
print("Q2  reject the sale before mutating any record")
print("Q3  a partial write must not replace a good snapshot")
print("Q4  reject it and leave current inventory unchanged")
print("Q5  reload the saved state and compare stock values")
print("Q6  title, quantity, unit price, total and remaining stock")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - load a small CSV catalogue")
print("TASK 2 - save the initial state as a versioned JSON snapshot")
print("TASK 3 - sell a valid quantity and produce a receipt")
print("TASK 4 - reject overselling without changing stock")
print("TASK 5 - save, reload, and verify the updated quantity")
print("TASK 6 - reject a corrupt snapshot without altering inventory")
print("TASK 7 - restore the saved snapshot into a fresh catalogue")
print("TASK 8 - clean up all temporary files")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project54_")
CSV_PATH = os.path.join(WORK, "catalogue.csv")
STATE_PATH = os.path.join(WORK, "state.json")
BAD_STATE_PATH = os.path.join(WORK, "bad-state.json")

starting_rows = [
    {"title": "Dune", "author": "Frank Herbert", "price": "12.50", "copies": "5"},
    {"title": "Neuromancer", "author": "William Gibson", "price": "9.99", "copies": "2"},
    {"title": "Café Society", "author": "Mina Haddad", "price": "7.25", "copies": "1"},
]
with open(CSV_PATH, "w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(starting_rows)

inventory = read_catalogue(CSV_PATH)
check("three catalogue records", len(inventory) == 3)
check("CSV title preserved", inventory[2]["title"] == "Café Society")

print("=" * 60)
print("TASK 1 - load the catalogue")
print("=" * 60)
print("books loaded ->", len(inventory))
print("starting Dune copies ->", inventory[0]["copies"])
print("CSV columns ->", ", ".join(FIELDS))
print()

print("=" * 60)
print("TASK 2 - save the initial snapshot")
print("=" * 60)
initial_snapshot = make_snapshot(inventory)
atomic_save(STATE_PATH, initial_snapshot)
print("snapshot format ->", initial_snapshot["format"])
print("snapshot version ->", initial_snapshot["version"])
print("snapshot file exists ->", os.path.isfile(STATE_PATH))
print("temporary file gone ->", not os.path.exists(STATE_PATH + ".tmp"))
print()

print("=" * 60)
print("TASK 3 - sell a valid quantity")
print("=" * 60)
receipt = sell(inventory, "dUnE", 2)
print("receipt title ->", receipt["title"])
print("receipt quantity ->", receipt["quantity"])
print("receipt unit price -> ${0:.2f}".format(receipt["unit_price"]))
print("receipt total -> ${0:.2f}".format(receipt["total"]))
print("remaining copies ->", receipt["remaining"])
print("sale total correct ->", check("receipt total", receipt["total"] == 25.00))
print()

print("=" * 60)
print("TASK 4 - reject overselling without a partial mutation")
print("=" * 60)
before_failed_sale = inventory[1]["copies"]
try:
    sell(inventory, "Neuromancer", 3)
except ShopError as error:
    oversell_message = str(error)
else:
    oversell_message = "oversell accepted"
print("oversell result ->", oversell_message)
print("stock unchanged ->", check("failed sale leaves stock", inventory[1]["copies"] == before_failed_sale))
print()

print("=" * 60)
print("TASK 5 - persist the successful sale")
print("=" * 60)
updated_snapshot = make_snapshot(inventory)
atomic_save(STATE_PATH, updated_snapshot)
reopened_books = load_snapshot(STATE_PATH)
dune_after_reload = next(book for book in reopened_books if book["title"] == "Dune")
print("Dune copies after reload ->", dune_after_reload["copies"])
print("updated state restored ->", check("reloaded stock reflects sale", dune_after_reload["copies"] == 3))
with open(STATE_PATH, "r", encoding="utf-8") as handle:
    saved_json_text = handle.read()
print("JSON is readable UTF-8 ->", check("UTF-8 title in file", "Caf\u00e9 Society" in saved_json_text))
print()

print("=" * 60)
print("TASK 6 - reject a corrupt snapshot safely")
print("=" * 60)
with open(BAD_STATE_PATH, "w", encoding="utf-8", newline="\n") as handle:
    json.dump({"format": "wrong", "version": 1, "books": []}, handle)
current_before_restore = [dict(book) for book in inventory]
try:
    restore_into(inventory, load_snapshot(BAD_STATE_PATH))
except (ShopError, ValueError, json.JSONDecodeError) as error:
    corrupt_message = str(error)
else:
    corrupt_message = "corrupt snapshot accepted"
print("corrupt snapshot ->", corrupt_message)
print("current inventory unchanged ->", check("failed restore leaves live data", inventory == current_before_restore))
print()

print("=" * 60)
print("TASK 7 - restore a valid snapshot")
print("=" * 60)
fresh_inventory = []
restore_into(fresh_inventory, reopened_books)
print("restored row count ->", len(fresh_inventory))
print("restored Dune copies ->", fresh_inventory[0]["copies"])
print("restore matches saved state ->", check("restore matches reload", fresh_inventory == reopened_books))
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary workspace removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
