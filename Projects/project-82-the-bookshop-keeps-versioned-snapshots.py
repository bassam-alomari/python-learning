# ============================================================
# Project 82 - the bookshop keeps versioned inventory snapshots
# ============================================================
# What this project teaches:
#   snapshots          save named, immutable inventory states
#   restore            reload a selected snapshot after validation
#   diff               compare two snapshots by title and fields
#   schema validation  reject corrupt/unsupported snapshot data
#   stable IDs         deterministic snapshot labels
#   CSV diff report    export changes between snapshots
#   safe workflow      restore only after all checks pass
#   cleanup            snapshots and reports stay in a temp folder
#
# Everything uses the standard library and fixed data; no input(),
# random, network or wall clock.
#
# Run it:  python project-82-the-bookshop-keeps-versioned-snapshots.py
# ============================================================

import csv
import json
import os
import shutil
import tempfile

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class SnapshotError(ValueError):
    """Raised when a saved inventory snapshot is invalid."""


REQUIRED_BOOK_FIELDS = ("title", "author", "price", "copies")


def validate_snapshot(payload):
    """Validate a versioned snapshot and return normalized book rows."""
    if not isinstance(payload, dict):
        raise SnapshotError("snapshot root must be an object")
    if payload.get("format") != "bookshop-snapshot" or payload.get("version") != 1:
        raise SnapshotError("unsupported snapshot format or version")
    books = payload.get("books")
    if not isinstance(books, list):
        raise SnapshotError("snapshot books must be a list")
    normalized = []
    seen = set()
    for row in books:
        if not isinstance(row, dict) or any(key not in row for key in REQUIRED_BOOK_FIELDS):
            raise SnapshotError("book row is missing required fields")
        title = str(row["title"]).strip()
        author = str(row["author"]).strip()
        if not title or not author:
            raise SnapshotError("title and author are required")
        key = title.casefold()
        if key in seen:
            raise SnapshotError("duplicate title in snapshot")
        seen.add(key)
        try:
            price = round(float(row["price"]), 2)
            copies = int(row["copies"])
        except (TypeError, ValueError):
            raise SnapshotError("price/copies must be numeric")
        if price < 0 or copies < 0:
            raise SnapshotError("price/copies cannot be negative")
        normalized.append({"title": title, "author": author, "price": price, "copies": copies})
    return sorted(normalized, key=lambda book: book["title"].casefold())


def make_snapshot(label, books):
    if not label.strip():
        raise SnapshotError("snapshot label is required")
    return {"format": "bookshop-snapshot", "version": 1,
            "label": label.strip(), "books": validate_snapshot({
                "format": "bookshop-snapshot", "version": 1, "books": books})}


def write_snapshot(directory, label, books):
    """Atomically save one JSON snapshot under a deterministic name."""
    snapshot = make_snapshot(label, books)
    filename = label.strip().casefold().replace(" ", "-") + ".json"
    path = os.path.join(directory, filename)
    temporary = path + ".tmp"
    try:
        with open(temporary, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(snapshot, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)
    return path


def read_snapshot(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as error:
        raise SnapshotError("invalid JSON on line " + str(error.lineno)) from error
    except OSError as error:
        raise SnapshotError("snapshot file unavailable") from error
    books = validate_snapshot(payload)
    return {"format": payload["format"], "version": payload["version"],
            "label": payload.get("label", ""), "books": books}


def compare_snapshots(old_books, new_books):
    """Report titles added/removed and fields changed."""
    old = {book["title"].casefold(): book for book in old_books}
    new = {book["title"].casefold(): book for book in new_books}
    changes = []
    for key in sorted(set(old) | set(new)):
        if key not in old:
            changes.append({"title": new[key]["title"], "change": "added", "field": "", "before": "", "after": ""})
        elif key not in new:
            changes.append({"title": old[key]["title"], "change": "removed", "field": "", "before": "", "after": ""})
        else:
            for field in ("author", "price", "copies"):
                if old[key][field] != new[key][field]:
                    changes.append({"title": new[key]["title"], "change": "updated", "field": field,
                                    "before": old[key][field], "after": new[key][field]})
    return changes


def write_diff(path, changes):
    fields = ("title", "change", "field", "before", "after")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(changes)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  why save more than one inventory snapshot")
print("Q2  how can an older state be restored safely")
print("Q3  how do we compare two saved states")
print("Q4  what must be validated before restore")
print("Q5  how can added and changed titles be explained")
print("Q6  what if a snapshot file is corrupt")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  retain a history and a recovery point")
print("Q2  load and validate it before replacing current data")
print("Q3  compare each title and its fields")
print("Q4  format version, required fields and valid values")
print("Q5  create a structured difference report")
print("Q6  reject it with a controlled error")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - create a starting catalogue")
print("TASK 2 - save two named inventory snapshots")
print("TASK 3 - restore a selected snapshot")
print("TASK 4 - compare snapshots and report changes")
print("TASK 5 - reject invalid snapshots and duplicate titles")
print("TASK 6 - export a difference CSV")
print("TASK 7 - verify atomic files and cleanup")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project82_")
DIFF_PATH = os.path.join(WORK, "snapshot-diff.csv")
base_books = [
    {"title": "Dune", "author": "Frank Herbert", "price": 12.50, "copies": 4},
    {"title": "Neuromancer", "author": "William Gibson", "price": 9.99, "copies": 2},
]
updated_books = [
    {"title": "Dune", "author": "Frank Herbert", "price": 13.00, "copies": 3},
    {"title": "Neuromancer", "author": "William Gibson", "price": 9.99, "copies": 2},
    {"title": "Kindred", "author": "Octavia Butler", "price": 8.25, "copies": 5},
]

print("=" * 60)
print("TASK 1 - initial catalogue")
print("=" * 60)
print("starting titles ->", len(base_books))
print("starting copies ->", sum(book["copies"] for book in base_books))
print()

print("=" * 60)
print("TASK 2 - save versioned snapshots")
print("=" * 60)
base_path = write_snapshot(WORK, "opening stock", base_books)
updated_path = write_snapshot(WORK, "after delivery", updated_books)
print("snapshot files ->", os.path.basename(base_path), ",", os.path.basename(updated_path))
print("both snapshots exist ->", os.path.isfile(base_path) and os.path.isfile(updated_path))
print("temp files removed ->", not os.path.exists(base_path + ".tmp") and not os.path.exists(updated_path + ".tmp"))
print()

print("=" * 60)
print("TASK 3 - restore a chosen snapshot")
print("=" * 60)
restored = read_snapshot(base_path)
print("restored label ->", restored["label"])
print("restored title count ->", len(restored["books"]))
print("restored copies ->", sum(book["copies"] for book in restored["books"]))
print("restore equals original ->", check("snapshot round trip", restored["books"] == validate_snapshot({"format": "bookshop-snapshot", "version": 1, "books": base_books})))
print()

print("=" * 60)
print("TASK 4 - compare snapshots")
print("=" * 60)
changes = compare_snapshots(read_snapshot(base_path)["books"], read_snapshot(updated_path)["books"])
for change in changes:
    print("{0}: {1} {2}".format(change["title"], change["change"], change["field"]))
print("change count ->", len(changes))
print("Kindred added ->", any(row["title"] == "Kindred" and row["change"] == "added" for row in changes))
print("Dune price updated ->", any(row["title"] == "Dune" and row["field"] == "price" for row in changes))
print("Dune copies updated ->", any(row["title"] == "Dune" and row["field"] == "copies" for row in changes))
check("diff identifies expected changes", len(changes) == 3)
print()

print("=" * 60)
print("TASK 5 - invalid snapshots are rejected")
print("=" * 60)
invalid_payloads = [
    {"format": "wrong", "version": 1, "books": []},
    {"format": "bookshop-snapshot", "version": 1,
     "books": [base_books[0], dict(base_books[0], title="dUnE")]},
    {"format": "bookshop-snapshot", "version": 1,
     "books": [{"title": "Bad", "author": "Nobody", "price": -1, "copies": 1}]},
]
invalid_messages = []
for payload in invalid_payloads:
    try:
        validate_snapshot(payload)
    except SnapshotError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted")
print("invalid snapshot errors ->", invalid_messages)
check("all bad snapshots refused", all(message != "accepted" for message in invalid_messages))
print()

print("=" * 60)
print("TASK 6 - export the snapshot diff")
print("=" * 60)
fields = write_diff(DIFF_PATH, changes)
with open(DIFF_PATH, "r", encoding="utf-8", newline="") as handle:
    diff_text = handle.read()
print("CSV header ->", diff_text.splitlines()[0])
print("diff rows ->", len(diff_text.splitlines()) - 1)
print("added title exported ->", "Kindred" in diff_text)
print("field column included ->", "field" in fields)
check("all changes exported", len(diff_text.splitlines()) == len(changes) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary snapshot folder removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
