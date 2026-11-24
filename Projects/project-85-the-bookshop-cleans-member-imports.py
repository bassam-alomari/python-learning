# ============================================================
# Project 85 - the bookshop imports and cleans member records
# ============================================================
# What this project teaches:
#   CSV import          read member rows with DictReader
#   normalization       trim names and lowercase email addresses
#   validation          check IDs, names and simple email shape
#   duplicate handling  reject repeated IDs and email addresses
#   row isolation       keep valid rows even when others are bad
#   audit report        export line numbers and rejection reasons
#   clean output        write normalized members to a new CSV
#   cleanup             all generated files live in a temp folder
#
# Everything uses the standard library and fixed data. No input(),
# network, random or clock.
#
# Run it:  python project-85-the-bookshop-cleans-member-imports.py
# ============================================================

import csv
import os
import shutil
import tempfile

CHECKS = []
REQUIRED_FIELDS = ("member_id", "name", "email")


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


def normalize_member(row):
    """Normalize basic member fields and validate their shape."""
    missing = [field for field in REQUIRED_FIELDS if field not in row]
    if missing:
        return None, "missing fields: " + ", ".join(missing)
    member_id = str(row["member_id"]).strip().upper()
    name = " ".join(str(row["name"]).split())
    email = str(row["email"]).strip().casefold()
    if not member_id:
        return None, "member ID is required"
    if not name:
        return None, "name is required"
    if email.count("@") != 1 or "." not in email.split("@")[-1]:
        return None, "email format is invalid"
    return {"member_id": member_id, "name": name, "email": email}, None


def import_members(rows):
    """Return normalized rows and (source-line, reason) errors."""
    accepted = []
    rejected = []
    seen_ids = set()
    seen_emails = set()
    for line_number, row in enumerate(rows, start=2):
        member, error = normalize_member(row)
        if error:
            rejected.append((line_number, error))
            continue
        if member["member_id"] in seen_ids:
            rejected.append((line_number, "duplicate member ID"))
            continue
        if member["email"] in seen_emails:
            rejected.append((line_number, "duplicate email"))
            continue
        seen_ids.add(member["member_id"])
        seen_emails.add(member["email"])
        accepted.append(member)
    return accepted, rejected


def read_member_csv(path):
    """Read source rows, reporting file-level schema errors."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            return [], [("file", "header is missing")]
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            return [], [("file", "missing fields: " + ", ".join(missing))]
        return list(reader), []


def write_members(path, members):
    fields = REQUIRED_FIELDS
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(members)


def write_errors(path, rejected):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("source_line", "reason"))
        writer.writerows(rejected)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  why normalize imported member data")
print("Q2  how should duplicate IDs or emails be handled")
print("Q3  should one bad row discard the entire import")
print("Q4  why preserve source line numbers")
print("Q5  how can staff review cleaned data")
print("Q6  what should happen when the header is incomplete")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  consistent values make matching and reporting reliable")
print("Q2  reject the duplicate row and explain why")
print("Q3  keep valid rows and report bad rows separately")
print("Q4  staff can locate the original bad record")
print("Q5  write a normalized clean CSV")
print("Q6  stop the file import with a schema error")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - create a supplier-style member CSV")
print("TASK 2 - normalize whitespace and email case")
print("TASK 3 - accept valid members and reject bad rows")
print("TASK 4 - detect duplicate IDs and emails")
print("TASK 5 - export clean members and rejection reasons")
print("TASK 6 - reject a file with missing header fields")
print("TASK 7 - clean up temporary import files")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project85_")
SOURCE = os.path.join(WORK, "members-source.csv")
CLEAN = os.path.join(WORK, "members-clean.csv")
ERRORS = os.path.join(WORK, "members-rejected.csv")
BAD_SOURCE = os.path.join(WORK, "members-wrong-schema.csv")

source_rows = [
    {"member_id": " m001 ", "name": "  Amina   Saleh ", "email": " AMINA@EXAMPLE.COM "},
    {"member_id": "M002", "name": "Omar Nasser", "email": "omar@example.org"},
    {"member_id": "M001", "name": "Duplicate ID", "email": "other@example.org"},
    {"member_id": "M003", "name": "Email Duplicate", "email": "OMAR@example.org"},
    {"member_id": "M004", "name": "Bad Email", "email": "not-an-email"},
    {"member_id": "M005", "name": "   ", "email": "empty@example.net"},
]
with open(SOURCE, "w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=REQUIRED_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(source_rows)

print("=" * 60)
print("TASK 1 - read source CSV")
print("=" * 60)
loaded_rows, file_errors = read_member_csv(SOURCE)
print("source rows ->", len(loaded_rows))
print("file-level errors ->", len(file_errors))
print("required columns ->", ", ".join(REQUIRED_FIELDS))
print()

print("=" * 60)
print("TASK 2 - normalize valid member rows")
print("=" * 60)
accepted, rejected = import_members(loaded_rows)
for member in accepted:
    print("accepted {0}: {1} <{2}>".format(member["member_id"], member["name"], member["email"]))
print("accepted rows ->", len(accepted))
print("normalized first name ->", accepted[0]["name"])
print("normalized first email ->", accepted[0]["email"])
print("normalization correct ->", check("trim/case normalization", accepted[0] == {
    "member_id": "M001", "name": "Amina Saleh", "email": "amina@example.com"
}))
print()

print("=" * 60)
print("TASK 3 - rejected rows have reasons")
print("=" * 60)
for line_number, reason in rejected:
    print("line {0} -> {1}".format(line_number, reason))
print("rejected rows ->", len(rejected))
print("rejection reasons present ->", check("bad rows explained", all(reason for _, reason in rejected)))
print()

print("=" * 60)
print("TASK 4 - duplicate protection")
print("=" * 60)
print("duplicate ID reason ->", next(reason for _, reason in rejected if "duplicate member ID" in reason))
print("duplicate email reason ->", next(reason for _, reason in rejected if "duplicate email" in reason))
print("invalid email reason ->", next(reason for _, reason in rejected if "email format" in reason))
print("only two members accepted ->", check("duplicate rows excluded", len(accepted) == 2))
print()

print("=" * 60)
print("TASK 5 - export clean and rejected reports")
print("=" * 60)
write_members(CLEAN, accepted)
write_errors(ERRORS, rejected)
with open(CLEAN, "r", encoding="utf-8", newline="") as handle:
    clean_text = handle.read()
with open(ERRORS, "r", encoding="utf-8", newline="") as handle:
    error_text = handle.read()
print("clean CSV header ->", clean_text.splitlines()[0])
print("clean member rows ->", len(clean_text.splitlines()) - 1)
print("error report rows ->", len(error_text.splitlines()) - 1)
print("normalized email exported ->", "amina@example.com" in clean_text)
check("both exports complete", len(clean_text.splitlines()) == 3 and len(error_text.splitlines()) == len(rejected) + 1)
print()

print("=" * 60)
print("TASK 6 - reject malformed file schema")
print("=" * 60)
with open(BAD_SOURCE, "w", encoding="utf-8", newline="\n") as handle:
    handle.write("name,email\nOnly Name,only@example.com\n")
bad_rows, schema_errors = read_member_csv(BAD_SOURCE)
print("rows returned ->", len(bad_rows))
print("schema error ->", schema_errors[0][1])
check("schema error reported", not bad_rows and schema_errors[0][0] == "file")
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary import workspace removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
