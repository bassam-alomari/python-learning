# ============================================================
# Project 60 - the bookshop imports a supplier CSV safely
# ============================================================
# What this project teaches:
#   DictReader          read supplier rows by column name
#   normalization       trim titles and compare case-insensitively
#   row-level validation accept valid rows, report invalid ones
#   duplicate handling  reject repeated supplier/title entries
#   merge logic         add new titles or update existing stock
#   audit report        explain rejected rows with line numbers
#   deterministic data fixed fixture and stable output
#   cleanup             temporary input/report files are removed
#
# Everything uses the standard library. No input(), random, network or clock.
#
# Run it:  python project-60-the-bookshop-imports-supplier-csv.py
# ============================================================

import csv
import os
import shutil
import tempfile

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


REQUIRED = ("title", "author", "price", "copies")


def import_supplier_rows(rows, inventory):
    """Validate incoming records and merge accepted books."""
    accepted = []
    rejected = []
    seen = set()
    by_title = {book["title"].casefold(): book for book in inventory}
    for line_number, row in enumerate(rows, start=2):
        missing = [field for field in REQUIRED if field not in row]
        if missing:
            rejected.append((line_number, "missing columns: " + ", ".join(missing)))
            continue
        title = row["title"].strip()
        author = row["author"].strip()
        if not title or not author:
            rejected.append((line_number, "title and author are required"))
            continue
        key = title.casefold()
        if key in seen:
            rejected.append((line_number, "duplicate title in this file"))
            continue
        seen.add(key)
        try:
            price = float(row["price"])
            copies = int(row["copies"])
        except (TypeError, ValueError):
            rejected.append((line_number, "price/copies must be numeric"))
            continue
        if price < 0 or copies < 0:
            rejected.append((line_number, "price/copies cannot be negative"))
            continue
        record = {"title": title, "author": author, "price": round(price, 2), "copies": copies}
        existing = by_title.get(key)
        if existing:
            if existing["author"].casefold() != author.casefold():
                rejected.append((line_number, "title conflicts with existing author"))
                continue
            existing["price"] = record["price"]
            existing["copies"] += copies
            action = "updated"
        else:
            inventory.append(record)
            by_title[key] = record
            action = "added"
        accepted.append((line_number, title, action, copies))
    return accepted, rejected


def read_supplier_csv(path):
    """Return DictReader rows and report a missing header cleanly."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            return [], [("file", "header is missing")]
        missing = [field for field in REQUIRED if field not in reader.fieldnames]
        if missing:
            return [], [("file", "missing columns: " + ", ".join(missing))]
        return list(reader), []


def write_rejection_report(path, rejected):
    """Export rejected source rows and explanations."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("line", "reason"))
        writer.writerows(rejected)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  why read supplier CSV by column names")
print("Q2  what should happen to malformed rows")
print("Q3  how can titles be matched despite extra spaces/case")
print("Q4  what if a duplicate title appears twice in one file")
print("Q5  how should a known book be merged")
print("Q6  how can rejected rows be audited later")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  DictReader maps the header fields to each row")
print("Q2  reject only that row and keep a reason")
print("Q3  strip whitespace and compare case-insensitively")
print("Q4  accept the first occurrence and reject later duplicates")
print("Q5  add copies and update price when the author agrees")
print("Q6  export line number and reason to a rejection CSV")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - create an existing inventory and supplier CSV")
print("TASK 2 - verify required columns")
print("TASK 3 - validate and normalize supplier rows")
print("TASK 4 - merge new titles and update existing stock")
print("TASK 5 - reject bad numbers, conflicts and duplicates")
print("TASK 6 - export rejected rows for review")
print("TASK 7 - verify totals and deterministic ordering")
print("TASK 8 - clean up the temporary workspace")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project60_")
SOURCE = os.path.join(WORK, "supplier.csv")
REJECTIONS = os.path.join(WORK, "rejected.csv")

inventory = [
    {"title": "Dune", "author": "Frank Herbert", "price": 12.50, "copies": 3},
    {"title": "Neuromancer", "author": "William Gibson", "price": 9.99, "copies": 2},
]
supplier_rows = [
    {"title": " DUNE ", "author": "Frank Herbert", "price": "13.00", "copies": "4"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "price": "8.50", "copies": "5"},
    {"title": "Bad Price", "author": "Nobody", "price": "free", "copies": "1"},
    {"title": "Ghost", "author": "Unknown", "price": "4.00", "copies": "-2"},
    {"title": "Dune", "author": "Frank Herbert", "price": "13.00", "copies": "1"},
    {"title": "Dune", "author": "Different Author", "price": "10.00", "copies": "1"},
    {"title": "  ", "author": "Nobody", "price": "2.00", "copies": "1"},
]
with open(SOURCE, "w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=REQUIRED, lineterminator="\n")
    writer.writeheader()
    writer.writerows(supplier_rows)

print("=" * 60)
print("TASK 1 - starting inventory and supplier file")
print("=" * 60)
print("existing titles ->", len(inventory))
print("supplier data rows ->", len(supplier_rows))
print("supplier file exists ->", os.path.isfile(SOURCE))
print()

print("=" * 60)
print("TASK 2 - import and validate by header")
print("=" * 60)
loaded_rows, file_errors = read_supplier_csv(SOURCE)
accepted, rejected = import_supplier_rows(loaded_rows, inventory)
check("supplier rows loaded", len(loaded_rows) == 7 and not file_errors)
check("valid rows accepted", len(accepted) == 2)
check("invalid rows reported", len(rejected) == 5)
print("required header ->", ", ".join(REQUIRED))
print("rows loaded ->", len(loaded_rows))
print("file-level errors ->", len(file_errors))
print("accepted rows ->", len(accepted))
print("rejected rows ->", len(rejected))
print()

print("=" * 60)
print("TASK 3 - accepted and merged rows")
print("=" * 60)
for line_number, title, action, quantity in accepted:
    print("line {0}: {1} {2} ({3} copies)".format(line_number, action, title, quantity))
dune = next(book for book in inventory if book["title"] == "Dune")
hobbit = next(book for book in inventory if book["title"] == "The Hobbit")
print("Dune updated copies ->", dune["copies"])
print("Dune updated price -> ${0:.2f}".format(dune["price"]))
print("new title copies ->", hobbit["copies"])
print()

print("=" * 60)
print("TASK 4 - rejection reasons")
print("=" * 60)
for line_number, reason in rejected:
    print("line {0}: {1}".format(line_number, reason))
print("bad price rejected ->", check("bad price rejected", any("numeric" in reason for _, reason in rejected)))
print("negative copies rejected ->", check("negative copies rejected", any("negative" in reason for _, reason in rejected)))
print("duplicate row rejected ->", check("duplicate row rejected", any("duplicate" in reason for _, reason in rejected)))
print("empty title rejected ->", check("empty title rejected", any("required" in reason for _, reason in rejected)))
print()

print("=" * 60)
print("TASK 5 - write rejection report")
print("=" * 60)
write_rejection_report(REJECTIONS, rejected)
with open(REJECTIONS, "r", encoding="utf-8", newline="") as handle:
    rejection_text = handle.read()
print("rejection report header ->", rejection_text.splitlines()[0])
print("rejection report rows ->", len(rejection_text.splitlines()) - 1)
print("line numbers preserved ->", check("rejection line numbers preserved", all(str(line) in rejection_text for line, _ in rejected)))
print()

print("=" * 60)
print("TASK 6 - inventory integrity")
print("=" * 60)
print("inventory titles ->", ", ".join(sorted(book["title"] for book in inventory)))
print("Dune copies after merge ->", dune["copies"])
print("Dune copies equal old plus delivery ->", check("existing stock increased", dune["copies"] == 7))
print("bad row did not enter inventory ->", check("bad title absent", not any(book["title"] == "Bad Price" for book in inventory)))
print("title count ->", len(inventory))
check("new title added", hobbit["copies"] == 5)
check("inventory count correct", len(inventory) == 3)
print()

print("=" * 60)
print("TASK 7 - malformed schema is rejected at file level")
print("=" * 60)
BAD_SOURCE = os.path.join(WORK, "wrong-header.csv")
with open(BAD_SOURCE, "w", encoding="utf-8", newline="") as handle:
    handle.write("name,quantity\nDune,4\n")
wrong_rows, wrong_errors = read_supplier_csv(BAD_SOURCE)
print("rows returned ->", len(wrong_rows))
print("schema error ->", wrong_errors[0][1])
check("wrong header rejected", not wrong_rows and wrong_errors[0][0] == "file")
print()

print("=" * 60)
print("TASK 8 - cleanup and report")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary supplier workspace removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
