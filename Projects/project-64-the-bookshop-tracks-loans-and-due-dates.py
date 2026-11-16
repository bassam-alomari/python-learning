# ============================================================
# Project 64 - the bookshop tracks loans and due dates
# ============================================================
# What this project teaches:
#   loan validation       require a known member and available title
#   due dates             compute a date using a fixed reference day
#   returns               restore one copy when a loan is returned
#   overdue fees          calculate a predictable per-day fine
#   duplicate guards      do not return the same loan twice
#   CSV report            export loan status and balances
#   validation            reject impossible loan operations
#   cleanup               generated report lives in a temp folder
#
# Everything uses the standard library and a fixed date fixture.
# No input(), random, network or current system clock is used.
#
# Run it:  python project-64-the-bookshop-tracks-loans-and-due-dates.py
# ============================================================

import csv
import os
import shutil
import tempfile
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class LoanError(ValueError):
    """Raised when a loan or return operation is invalid."""


class LendingDesk:
    """Manage available copies, active loans and returns."""

    def __init__(self, books, members, loan_days=14, fine_per_day="0.50"):
        self.books = {book["title"].casefold(): dict(book) for book in books}
        self.members = {member["id"]: member["name"] for member in members}
        self.loan_days = loan_days
        self.fine_per_day = Decimal(str(fine_per_day))
        self.loans = {}
        self.next_id = 1

    def checkout(self, member_id, title, today):
        """Create a loan with a due date based on the supplied date."""
        if member_id not in self.members:
            raise LoanError("member not found")
        key = title.casefold()
        if key not in self.books:
            raise LoanError("book not found")
        if self.books[key]["copies"] <= 0:
            raise LoanError("no copies available")
        if not isinstance(today, date):
            raise LoanError("today must be a date")
        self.books[key]["copies"] -= 1
        loan_id = "L{0:03d}".format(self.next_id)
        self.next_id += 1
        due_date = today + timedelta(days=self.loan_days)
        self.loans[loan_id] = {
            "loan_id": loan_id,
            "member_id": member_id,
            "member": self.members[member_id],
            "title": self.books[key]["title"],
            "checkout_date": today,
            "due_date": due_date,
            "returned": False,
            "fine": Decimal("0.00"),
        }
        return dict(self.loans[loan_id])

    def return_book(self, loan_id, returned_on):
        """Close a loan, restore stock and compute any fine."""
        loan = self.loans.get(loan_id)
        if loan is None:
            raise LoanError("loan not found")
        if loan["returned"]:
            raise LoanError("loan already returned")
        if not isinstance(returned_on, date):
            raise LoanError("return date must be a date")
        if returned_on < loan["checkout_date"]:
            raise LoanError("return date precedes checkout")
        days_late = max(0, (returned_on - loan["due_date"]).days)
        fine = (self.fine_per_day * days_late).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        loan["returned"] = True
        loan["return_date"] = returned_on
        loan["fine"] = fine
        self.books[loan["title"].casefold()]["copies"] += 1
        return {"loan_id": loan_id, "days_late": days_late, "fine": fine,
                "copies_available": self.books[loan["title"].casefold()]["copies"]}


def export_loans(path, loans):
    """Write stable loan records to CSV."""
    fields = ("loan_id", "member_id", "member", "title", "checkout_date",
              "due_date", "return_date", "returned", "fine")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for loan in sorted(loans, key=lambda row: row["loan_id"]):
            writer.writerow({
                "loan_id": loan["loan_id"],
                "member_id": loan["member_id"],
                "member": loan["member"],
                "title": loan["title"],
                "checkout_date": loan["checkout_date"].isoformat(),
                "due_date": loan["due_date"].isoformat(),
                "return_date": loan.get("return_date", ""),
                "returned": loan["returned"],
                "fine": "{0:.2f}".format(loan["fine"]),
            })
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what should be checked before lending a book")
print("Q2  how is the due date calculated")
print("Q3  when should a late fee be charged")
print("Q4  what changes when a book is returned")
print("Q5  how do we prevent returning one loan twice")
print("Q6  why use a fixed date in an automated test")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  member, title and available copies")
print("Q2  checkout date plus the configured loan period")
print("Q3  only for days after the due date")
print("Q4  close the loan and restore one available copy")
print("Q5  mark the loan returned and reject repeated returns")
print("Q6  fixed dates make every run deterministic")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - prepare a small catalogue and members")
print("TASK 2 - check out a book and calculate its due date")
print("TASK 3 - reject an unavailable copy and unknown member")
print("TASK 4 - return a book on time")
print("TASK 5 - return a late book and calculate its fee")
print("TASK 6 - reject a duplicate return")
print("TASK 7 - export loan history to CSV")
print("TASK 8 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project64_")
REPORT = os.path.join(WORK, "loans.csv")
FIXED_TODAY = date(2026, 1, 10)
desk = LendingDesk(
    [{"title": "Dune", "copies": 2}, {"title": "Neuromancer", "copies": 0}],
    [{"id": "M001", "name": "Amina Saleh"}, {"id": "M002", "name": "Omar Nasser"}],
    loan_days=14,
    fine_per_day="0.50",
)

print("=" * 60)
print("TASK 1 - catalogue and members")
print("=" * 60)
print("books ->", len(desk.books))
print("members ->", len(desk.members))
print("Dune copies before ->", desk.books["dune"]["copies"])
print()

print("=" * 60)
print("TASK 2 - check out a book")
print("=" * 60)
loan_on_time = desk.checkout("M001", "Dune", FIXED_TODAY)
print("loan ID ->", loan_on_time["loan_id"])
print("member ->", loan_on_time["member"])
print("checkout date ->", loan_on_time["checkout_date"].isoformat())
print("due date ->", loan_on_time["due_date"].isoformat())
print("Dune copies after checkout ->", desk.books["dune"]["copies"])
print("due date calculation correct ->", check("due date uses loan days", loan_on_time["due_date"] == date(2026, 1, 24)))
print()

print("=" * 60)
print("TASK 3 - reject unavailable copies and unknown members")
print("=" * 60)
try:
    desk.checkout("M002", "Neuromancer", FIXED_TODAY)
except LoanError as error:
    unavailable_message = str(error)
else:
    unavailable_message = "accepted"
try:
    desk.checkout("M999", "Dune", FIXED_TODAY)
except LoanError as error:
    member_message = str(error)
else:
    member_message = "accepted"
print("unavailable title ->", unavailable_message)
print("unknown member ->", member_message)
print("both invalid requests rejected ->", check("checkout guards", unavailable_message == "no copies available" and member_message == "member not found"))
print()

print("=" * 60)
print("TASK 4 - return on time")
print("=" * 60)
on_time_result = desk.return_book(loan_on_time["loan_id"], date(2026, 1, 20))
print("days late ->", on_time_result["days_late"])
print("fine -> ${0:.2f}".format(on_time_result["fine"]))
print("copies restored ->", on_time_result["copies_available"])
check("on-time return no fine", on_time_result["days_late"] == 0 and on_time_result["fine"] == Decimal("0.00"))
print()

print("=" * 60)
print("TASK 5 - return late")
print("=" * 60)
loan_late = desk.checkout("M002", "Dune", FIXED_TODAY)
late_result = desk.return_book(loan_late["loan_id"], date(2026, 1, 28))
print("days late ->", late_result["days_late"])
print("late fine -> ${0:.2f}".format(late_result["fine"]))
print("fine calculation correct ->", check("late fee calculation", late_result["days_late"] == 4 and late_result["fine"] == Decimal("2.00")))
print("Dune copies restored ->", late_result["copies_available"])
print()

print("=" * 60)
print("TASK 6 - a returned loan cannot be returned again")
print("=" * 60)
try:
    desk.return_book(loan_late["loan_id"], date(2026, 1, 29))
except LoanError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
print("duplicate return ->", duplicate_message)
print("stock not double-restored ->", check("duplicate return guard", duplicate_message == "loan already returned" and desk.books["dune"]["copies"] == 2))
print()

print("=" * 60)
print("TASK 7 - export loan report")
print("=" * 60)
fields = export_loans(REPORT, list(desk.loans.values()))
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("loan rows ->", len(report_text.splitlines()) - 1)
print("report includes late fee ->", "2.00" in report_text)
print("CSV columns ->", len(fields))
check("report includes both loans", len(report_text.splitlines()) == 3)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary loan report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
