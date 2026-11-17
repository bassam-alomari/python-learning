# ============================================================
# Project 68 - the bookshop follows up overdue loans
# ============================================================
# What this project teaches:
#   overdue detection   compare due dates with a fixed report date
#   days late           calculate lateness without using the system clock
#   fee calculation     apply a per-day fine with Decimal
#   member summaries    group overdue loans and total their fees
#   prioritization      sort oldest overdue loans first
#   CSV export          create a deterministic follow-up list
#   validation          reject duplicate IDs and invalid fee inputs
#   cleanup             generated report lives in a temp folder
#
# Everything uses the standard library. Dates are fixtures; no input(),
# random, network or current clock is used.
#
# Run it:  python project-68-the-bookshop-follows-up-overdue-loans.py
# ============================================================

import csv
import os
import shutil
import tempfile
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class OverdueError(ValueError):
    """Raised when loan or fee data is invalid."""


def overdue_report(loans, as_of, fee_per_day="0.50"):
    """Return overdue loans and member-level fee totals."""
    try:
        rate = Decimal(str(fee_per_day)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise OverdueError("fee rate must be numeric")
    if rate < 0:
        raise OverdueError("fee rate cannot be negative")
    seen = set()
    overdue = []
    for loan in loans:
        required = ("loan_id", "member_id", "member", "title", "due_date", "returned")
        if any(key not in loan for key in required):
            raise OverdueError("loan row is missing required fields")
        if loan["loan_id"] in seen:
            raise OverdueError("duplicate loan ID")
        seen.add(loan["loan_id"])
        if not isinstance(loan["due_date"], date) or not isinstance(as_of, date):
            raise OverdueError("due date and report date must be dates")
        if loan["returned"]:
            continue
        days_late = (as_of - loan["due_date"]).days
        if days_late <= 0:
            continue
        row = dict(loan)
        row["days_late"] = days_late
        row["fee"] = (rate * days_late).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        overdue.append(row)
    overdue.sort(key=lambda row: (-row["days_late"], row["loan_id"]))
    by_member = {}
    for row in overdue:
        total = by_member.setdefault(row["member_id"], {
            "member": row["member"], "loans": 0, "days_late": 0, "fees": Decimal("0.00")
        })
        total["loans"] += 1
        total["days_late"] += row["days_late"]
        total["fees"] += row["fee"]
    return overdue, by_member


def write_followup(path, overdue):
    """Export overdue loans with stable date and money strings."""
    fields = ("loan_id", "member_id", "member", "title", "due_date", "days_late", "fee")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in overdue:
            writer.writerow({
                "loan_id": row["loan_id"],
                "member_id": row["member_id"],
                "member": row["member"],
                "title": row["title"],
                "due_date": row["due_date"].isoformat(),
                "days_late": row["days_late"],
                "fee": "{0:.2f}".format(row["fee"]),
            })
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how do we identify an overdue loan")
print("Q2  how are days late calculated")
print("Q3  how can fees be grouped by member")
print("Q4  how should staff prioritize follow-up")
print("Q5  what should be excluded from overdue notices")
print("Q6  how can the follow-up list be shared")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  compare an unreturned loan's due date with the report date")
print("Q2  report date minus due date")
print("Q3  sum fees for each member")
print("Q4  sort by most days late first")
print("Q5  returned loans and loans not yet due")
print("Q6  export the report to CSV")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - prepare loans and a fixed as-of date")
print("TASK 2 - detect overdue loans and compute fees")
print("TASK 3 - summarize loans and fees per member")
print("TASK 4 - prioritize the longest-overdue loans")
print("TASK 5 - exclude returned and not-yet-due loans")
print("TASK 6 - reject duplicate or invalid input")
print("TASK 7 - export a CSV follow-up report")
print("TASK 8 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project68_")
REPORT = os.path.join(WORK, "overdue-follow-up.csv")
AS_OF = date(2026, 11, 17)
loans = [
    {"loan_id": "L001", "member_id": "M001", "member": "Amina Saleh", "title": "Dune", "due_date": date(2026, 11, 10), "returned": False},
    {"loan_id": "L002", "member_id": "M002", "member": "Omar Nasser", "title": "Neuromancer", "due_date": date(2026, 11, 16), "returned": False},
    {"loan_id": "L003", "member_id": "M001", "member": "Amina Saleh", "title": "The Hobbit", "due_date": date(2026, 11, 12), "returned": False},
    {"loan_id": "L004", "member_id": "M003", "member": "Lina Haddad", "title": "Café Society", "due_date": date(2026, 11, 15), "returned": True},
    {"loan_id": "L005", "member_id": "M004", "member": "Samir Ali", "title": "Python Guide", "due_date": date(2026, 11, 20), "returned": False},
]

print("=" * 60)
print("TASK 1 - report date and loan ledger")
print("=" * 60)
print("as-of date ->", AS_OF.isoformat())
print("loan records ->", len(loans))
print("returned records ->", sum(row["returned"] for row in loans))
print()

print("=" * 60)
print("TASK 2 - find overdue loans")
print("=" * 60)
overdue, by_member = overdue_report(loans, AS_OF, fee_per_day="0.50")
for row in overdue:
    print("{0} {1}: {2} days late, fee ${3:.2f}".format(
        row["loan_id"], row["title"], row["days_late"], row["fee"]
    ))
print("overdue count ->", len(overdue))
print("oldest overdue ->", overdue[0]["loan_id"])
check("overdue dates detected", [row["loan_id"] for row in overdue] == ["L001", "L003", "L002"])
print()

print("=" * 60)
print("TASK 3 - member summaries")
print("=" * 60)
for member_id in sorted(by_member):
    summary = by_member[member_id]
    print("{0}: {1} loan(s), ${2:.2f} fees".format(
        summary["member"], summary["loans"], summary["fees"]
    ))
print("Amina fee total -> ${0:.2f}".format(by_member["M001"]["fees"]))
check("member fee aggregation", by_member["M001"]["fees"] == Decimal("6.00"))
print()

print("=" * 60)
print("TASK 4 - priority ordering")
print("=" * 60)
print("follow-up order ->", " > ".join(row["loan_id"] for row in overdue))
print("days late order ->", [row["days_late"] for row in overdue])
check("longest overdue first", overdue[0]["days_late"] >= overdue[-1]["days_late"])
print()

print("=" * 60)
print("TASK 5 - returned and future loans are excluded")
print("=" * 60)
active_ids = {row["loan_id"] for row in overdue}
print("returned L004 excluded ->", "L004" not in active_ids)
print("not-yet-due L005 excluded ->", "L005" not in active_ids)
print("eligible loans only ->", check("exclusion rules", active_ids == {"L001", "L002", "L003"}))
print()

print("=" * 60)
print("TASK 6 - malformed ledger input is rejected")
print("=" * 60)
try:
    overdue_report(loans + [dict(loans[0])], AS_OF)
except OverdueError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
try:
    overdue_report(loans, AS_OF, fee_per_day="bad")
except OverdueError as error:
    fee_message = str(error)
else:
    fee_message = "accepted"
print("duplicate ID ->", duplicate_message)
print("invalid fee ->", fee_message)
check("invalid report input rejected", duplicate_message == "duplicate loan ID" and fee_message == "fee rate must be numeric")
print()

print("=" * 60)
print("TASK 7 - export follow-up CSV")
print("=" * 60)
fields = write_followup(REPORT, overdue)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("report rows ->", len(report_text.splitlines()) - 1)
print("late fee exported ->", "3.50" in report_text)
print("date exported ->", "2026-11-10" in report_text)
check("CSV contains overdue loans", len(report_text.splitlines()) == len(overdue) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary follow-up report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
