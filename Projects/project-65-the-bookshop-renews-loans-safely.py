# ============================================================
# Project 65 - the bookshop renews loans safely
# ============================================================
# What this project teaches:
#   renewals            extend a due date by the loan period
#   renewal limits      cap extensions per loan
#   reservations        deny renewal when another member is waiting
#   state guards        reject closed/unknown loans
#   deterministic dates use an explicit reference date
#   CSV report          export renewal and loan status
#   validation          reject invalid dates and limits
#   cleanup             generated report is temporary
#
# This continues project 64's lending workflow. Only the standard
# library is used; the dates are fixed and no clock/network is consulted.
#
# Run it:  python project-65-the-bookshop-renews-loans-safely.py
# ============================================================

import csv
import os
import shutil
import tempfile
from datetime import date, timedelta

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class RenewalError(ValueError):
    """Raised when a loan cannot be renewed."""


class RenewalDesk:
    """Track checkouts, reservations and bounded renewals."""

    def __init__(self, loan_days=14, max_renewals=2):
        if loan_days <= 0 or max_renewals < 0:
            raise RenewalError("invalid renewal policy")
        self.loan_days = loan_days
        self.max_renewals = max_renewals
        self.loans = {}
        self.waiting = set()

    def add_loan(self, loan_id, member, title, due_date):
        if loan_id in self.loans:
            raise RenewalError("duplicate loan ID")
        self.loans[loan_id] = {
            "loan_id": loan_id,
            "member": member,
            "title": title,
            "due_date": due_date,
            "renewals": 0,
            "returned": False,
        }

    def reserve(self, title, member):
        """Record a waiting member for a title."""
        self.waiting.add((title.casefold(), member))

    def renew(self, loan_id, member, today):
        """Extend the due date if policy and reservation rules allow."""
        loan = self.loans.get(loan_id)
        if loan is None:
            raise RenewalError("loan not found")
        if loan["member"] != member:
            raise RenewalError("loan belongs to another member")
        if loan["returned"]:
            raise RenewalError("returned loan cannot be renewed")
        if not isinstance(today, date):
            raise RenewalError("today must be a date")
        if any(title == loan["title"].casefold() and waiting_member != member
               for title, waiting_member in self.waiting):
            raise RenewalError("another member is waiting for this title")
        if loan["renewals"] >= self.max_renewals:
            raise RenewalError("renewal limit reached")
        loan["due_date"] += timedelta(days=self.loan_days)
        loan["renewals"] += 1
        return dict(loan)

    def mark_returned(self, loan_id):
        loan = self.loans.get(loan_id)
        if loan is None:
            raise RenewalError("loan not found")
        if loan["returned"]:
            raise RenewalError("loan already returned")
        loan["returned"] = True


def export_loan_status(path, loans):
    fields = ("loan_id", "member", "title", "due_date", "renewals", "returned")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for loan in sorted(loans.values(), key=lambda row: row["loan_id"]):
            row = dict(loan)
            row["due_date"] = row["due_date"].isoformat()
            writer.writerow(row)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what does renewing a loan change")
print("Q2  how many times may a loan be renewed")
print("Q3  when should a renewal be denied")
print("Q4  can another member's reservation affect renewal")
print("Q5  why use an explicit date in tests")
print("Q6  how can renewal history be exported")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  the due date and renewal counter")
print("Q2  according to a configured maximum")
print("Q3  when closed, over limit or invalid by policy")
print("Q4  yes, a waiting member can block an extension")
print("Q5  fixed dates make each run reproducible")
print("Q6  write loan state and due date to CSV")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - create a loan with a fixed due date")
print("TASK 2 - renew once and move the due date forward")
print("TASK 3 - deny renewal when another member is waiting")
print("TASK 4 - enforce the maximum renewal count")
print("TASK 5 - deny closed loans")
print("TASK 6 - export current loan status to CSV")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project65_")
REPORT = os.path.join(WORK, "loan-status.csv")
TODAY = date(2026, 3, 1)
desk = RenewalDesk(loan_days=14, max_renewals=2)
desk.add_loan("L001", "Amina", "Dune", date(2026, 3, 10))
desk.add_loan("L002", "Omar", "Neuromancer", date(2026, 3, 12))

print("=" * 60)
print("TASK 1 - starting loan")
print("=" * 60)
print("loan due date ->", desk.loans["L001"]["due_date"].isoformat())
print("renewal count ->", desk.loans["L001"]["renewals"])
print()

print("=" * 60)
print("TASK 2 - renew once")
print("=" * 60)
first_renewal = desk.renew("L001", "Amina", TODAY)
print("new due date ->", first_renewal["due_date"].isoformat())
print("renewals used ->", first_renewal["renewals"])
print("due date moved 14 days ->", check("first extension", first_renewal["due_date"] == date(2026, 3, 24)))
print()

print("=" * 60)
print("TASK 3 - reservation blocks another renewal")
print("=" * 60)
desk.reserve("Dune", "Omar")
due_before_waitlist_attempt = desk.loans["L001"]["due_date"]
try:
    desk.renew("L001", "Amina", TODAY)
except RenewalError as error:
    waiting_message = str(error)
else:
    waiting_message = "accepted"
print("renewal with waiting member ->", waiting_message)
print("due date unchanged ->", check("waiting list blocks", desk.loans["L001"]["due_date"] == due_before_waitlist_attempt))
print()

print("=" * 60)
print("TASK 4 - renewal cap")
print("=" * 60)
desk.waiting.clear()
second_renewal = desk.renew("L001", "Amina", TODAY)
try:
    desk.renew("L001", "Amina", TODAY)
except RenewalError as error:
    limit_message = str(error)
else:
    limit_message = "accepted"
print("renewals after second extension ->", second_renewal["renewals"])
print("third extension ->", limit_message)
print("maximum respected ->", check("renewal cap", limit_message == "renewal limit reached"))
print()

print("=" * 60)
print("TASK 5 - closed loans cannot renew")
print("=" * 60)
desk.mark_returned("L002")
try:
    desk.renew("L002", "Omar", TODAY)
except RenewalError as error:
    closed_message = str(error)
else:
    closed_message = "accepted"
print("closed loan renewal ->", closed_message)
print("closed loan rejected ->", check("returned loan blocked", closed_message == "returned loan cannot be renewed"))
print()

print("=" * 60)
print("TASK 6 - export status report")
print("=" * 60)
fields = export_loan_status(REPORT, desk.loans)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("loan rows ->", len(report_text.splitlines()) - 1)
print("due date exported ->", check("renewed due date in report", "2026-04-07" in report_text))
print("returned status exported ->", "True" in report_text)
check("CSV contains both loans", len(report_text.splitlines()) == 3)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary renewal report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
