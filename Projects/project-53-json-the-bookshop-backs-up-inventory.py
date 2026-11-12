# ============================================================
# Project 53 - JSON: the bookshop backs up and restores inventory
# ============================================================
# What this project teaches:
#   json.dump / json.load   write and read structured data
#   ensure_ascii=False      keep UTF-8 titles readable
#   schema validation       reject a backup with missing keys
#   safe restore            validate before replacing live data
#   atomic write            write a temp file, then replace the target
#   round trip              save, reload, and compare records
#   error handling          explain malformed JSON without a traceback
#   cleanup                 keep every test file in a temporary folder
#
# Everything uses the standard library. No input(), random, or clock.
# Output is deterministic; files are removed at the end.
#
# Run it:  python project-53-json-the-bookshop-backs-up-inventory.py
# ============================================================

import json
import os
import shutil
import tempfile

CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


REQUIRED_KEYS = ("title", "author", "price", "copies")


class BackupError(ValueError):
    """Raised when a backup cannot be safely restored."""


def validate_backup(payload):
    """Return normalized records or reject an invalid backup."""
    if not isinstance(payload, dict):
        raise BackupError("backup root must be an object")
    if payload.get("format") != "bookshop-inventory":
        raise BackupError("unsupported backup format")
    if payload.get("version") != 1:
        raise BackupError("unsupported backup version")
    records = payload.get("books")
    if not isinstance(records, list):
        raise BackupError("books must be a list")

    normalized = []
    seen_titles = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise BackupError("book row " + str(index) + " must be an object")
        missing = [key for key in REQUIRED_KEYS if key not in record]
        if missing:
            raise BackupError(
                "book row " + str(index) + " missing " + ", ".join(missing)
            )
        title = record["title"]
        author = record["author"]
        if not isinstance(title, str) or not title.strip():
            raise BackupError("book title must be non-empty text")
        if not isinstance(author, str) or not author.strip():
            raise BackupError("book author must be non-empty text")
        try:
            price = float(record["price"])
            copies = int(record["copies"])
        except (TypeError, ValueError) as error:
            raise BackupError("price and copies must be numeric") from error
        if price < 0 or copies < 0:
            raise BackupError("price and copies cannot be negative")
        folded = title.strip().casefold()
        if folded in seen_titles:
            raise BackupError("duplicate title: " + title.strip())
        seen_titles.add(folded)
        normalized.append({
            "title": title.strip(),
            "author": author.strip(),
            "price": round(price, 2),
            "copies": copies,
        })
    return normalized


def make_backup(records):
    """Build a versioned JSON backup document."""
    clean_records = validate_backup({
        "format": "bookshop-inventory",
        "version": 1,
        "books": records,
    })
    return {
        "format": "bookshop-inventory",
        "version": 1,
        "books": clean_records,
    }


def write_backup(path, payload):
    """Validate and atomically replace a JSON backup file."""
    checked = validate_backup(payload)
    document = {
        "format": payload["format"],
        "version": payload["version"],
        "books": checked,
    }
    temporary = path + ".tmp"
    try:
        with open(temporary, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)


def load_backup(path):
    """Load JSON, translate parse failures, and validate its schema."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as error:
        raise BackupError("invalid JSON at line " + str(error.lineno)) from error
    except OSError as error:
        raise BackupError("backup file unavailable") from error
    return make_backup(validate_backup(payload))


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  why use JSON for an inventory backup")
print("Q2  why include a format name and version")
print("Q3  when is it safe to replace the live backup")
print("Q4  how do we preserve a title such as Café")
print("Q5  what should happen when JSON is malformed")
print("Q6  why validate a backup before restoring it")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  JSON stores nested records in a portable text format")
print("Q2  format and version make future schema changes explicit")
print("Q3  only after the new document is written and validated")
print("Q4  UTF-8 plus ensure_ascii=False")
print("Q5  report a controlled BackupError, not a traceback")
print("Q6  malformed data must never replace valid inventory")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - build a versioned backup document")
print("TASK 2 - validate record fields and numeric ranges")
print("TASK 3 - save JSON atomically using UTF-8")
print("TASK 4 - reopen and restore the same records")
print("TASK 5 - reject invalid schema and duplicate titles")
print("TASK 6 - reject malformed JSON without a crash")
print("TASK 7 - preserve a known-good file after a rejected write")
print("TASK 8 - clean up the temporary backup folder")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project53_")
BACKUP = os.path.join(WORK, "inventory.json")
BAD_JSON = os.path.join(WORK, "broken.json")

books = [
    {"title": "Dune", "author": "Frank Herbert", "price": 12.50, "copies": 4},
    {"title": "Neuromancer", "author": "William Gibson", "price": 9.99, "copies": 2},
    {"title": "Café Society", "author": "Mina Haddad", "price": 7.25, "copies": 1},
]
backup = make_backup(books)
check("format marker present", backup["format"] == "bookshop-inventory")
check("version marker present", backup["version"] == 1)
check("all books retained", backup["books"] == books)

print("=" * 60)
print("TASK 1 - build a versioned backup")
print("=" * 60)
print("format ->", backup["format"])
print("version ->", backup["version"])
print("books ->", len(backup["books"]))
print("versioned document ->", check("backup envelope", set(backup) == {"format", "version", "books"}))
print()

print("=" * 60)
print("TASK 2 - validate fields and values")
print("=" * 60)
normalized = validate_backup(backup)
print("required fields ->", ", ".join(REQUIRED_KEYS))
print("nonnegative values ->", check("valid ranges", all(row["price"] >= 0 and row["copies"] >= 0 for row in normalized)))
print("title trimmed ->", check("trim title", normalized[0]["title"] == "Dune"))
print("UTF-8 text ->", normalized[2]["title"])
print()

print("=" * 60)
print("TASK 3 - atomic UTF-8 save")
print("=" * 60)
write_backup(BACKUP, backup)
with open(BACKUP, "r", encoding="utf-8") as handle:
    saved_text = handle.read()
print("backup file created ->", os.path.isfile(BACKUP))
print("Café stays readable ->", "Café Society" in saved_text)
print("temporary file cleaned ->", not os.path.exists(BACKUP + ".tmp"))
print()

print("=" * 60)
print("TASK 4 - load and restore")
print("=" * 60)
restored = load_backup(BACKUP)
print("restored books ->", len(restored["books"]))
print("round trip matches ->", check("restore round trip", restored == backup))
print("restored UTF-8 title ->", restored["books"][2]["title"])
print()

print("=" * 60)
print("TASK 5 - reject invalid records")
print("=" * 60)
invalid_messages = []
for bad_payload in (
    {"format": "wrong", "version": 1, "books": []},
    {"format": "bookshop-inventory", "version": 99, "books": []},
    {"format": "bookshop-inventory", "version": 1,
     "books": [{"title": "Only title"}]},
    {"format": "bookshop-inventory", "version": 1,
     "books": [books[0], dict(books[0], title="dUnE")]},
):
    try:
        validate_backup(bad_payload)
    except BackupError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted invalid backup")
print("invalid cases rejected ->", len(invalid_messages))
print("all have explanations ->", check("controlled validation", all(message != "accepted invalid backup" for message in invalid_messages)))
print("format failure ->", invalid_messages[0])
print("schema failure ->", invalid_messages[2])
print()

print("=" * 60)
print("TASK 6 - malformed JSON is a controlled error")
print("=" * 60)
with open(BAD_JSON, "w", encoding="utf-8", newline="\n") as handle:
    handle.write('{"books": [')
try:
    load_backup(BAD_JSON)
except BackupError as error:
    malformed_message = str(error)
else:
    malformed_message = "accepted malformed JSON"
print("malformed JSON ->", malformed_message)
print("malformed file rejected ->", check("JSON parse failure wrapped", malformed_message.startswith("invalid JSON at line")))
print()

print("=" * 60)
print("TASK 7 - bad backup cannot replace good backup")
print("=" * 60)
with open(BACKUP, "r", encoding="utf-8") as handle:
    known_good = handle.read()
invalid_payload = {"format": "wrong", "version": 1, "books": []}
try:
    write_backup(BACKUP, invalid_payload)
except BackupError:
    rejected = True
else:
    rejected = False
with open(BACKUP, "r", encoding="utf-8") as handle:
    after_rejection = handle.read()
print("invalid replacement rejected ->", rejected)
print("known-good backup preserved ->", check("old backup intact", after_rejection == known_good))
print("no temp file left ->", not os.path.exists(BACKUP + ".tmp"))
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("temporary folder removed", not os.path.exists(WORK))
print("temporary backup folder removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
