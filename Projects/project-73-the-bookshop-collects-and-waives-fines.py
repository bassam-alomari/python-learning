# ============================================================
# Project 73 - the bookshop collects and waives overdue fines
# ============================================================
# What this project teaches:
#   fine assessment      calculate late fees from fixed due/return dates
#   payments             accept full or partial payments
#   balance tracking     keep unpaid fine balances per loan
#   overpayment guard    reject payments above the outstanding balance
#   waivers              record an authorized zero-balance adjustment
#   ledger report        export fine, paid, waived and outstanding amounts
#   Decimal money        avoid binary floating-point currency errors
#   cleanup              generated ledger is temporary
#
# Everything is standard library and uses fixed dates. No input(),
# random, network or current system clock.
#
# Run it:  python project-73-the-bookshop-collects-overdue-fines.py
# ============================================================

import csv
import os
import shutil
import tempfile
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class FineError(ValueError):
    """Raised when a fine payment or waiver is invalid."""


def assess_fine(due_date, returned_date, rate_per_day):
    """Calculate fine for late days only; return amount and day count."""
    if not isinstance(due_date, date) or not isinstance(returned_date, date):
        raise FineError("due and return values must be dates")
    rate = Decimal(str(rate_per_day)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if rate < 0:
        raise FineError("daily rate cannot be negative")
    days_late = max(0, (returned_date - due_date).days)
    return (rate * days_late).quantize(Decimal("0.01")), days_late


class FineDesk:
    """Track fine balances, payments and authorized waivers."""

    def __init__(self, loans):
        self.accounts = {}
        for loan in loans:
            fine, days_late = assess_fine(
                loan["due_date"], loan["returned_date"], loan["rate_per_day"]
            )
            if loan["loan_id"] in self.accounts:
                raise FineError("duplicate loan ID")
            self.accounts[loan["loan_id"]] = {
                "loan_id": loan["loan_id"],
                "member": loan["member"],
                "title": loan["title"],
                "days_late": days_late,
                "fine": fine,
                "paid": Decimal("0.00"),
                "waived": Decimal("0.00"),
                "balance": fine,
                "waiver_reason": "",
            }

    def pay(self, loan_id, amount):
        """Apply a positive payment without exceeding outstanding balance."""
        account = self._get(loan_id)
        payment = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if payment <= 0:
            raise FineError("payment must be positive")
        if payment > account["balance"]:
            raise FineError("payment exceeds outstanding balance")
        account["paid"] += payment
        account["balance"] -= payment
        return account["balance"]

    def waive(self, loan_id, reason):
        """Waive remaining balance with a required audit reason."""
        account = self._get(loan_id)
        note = reason.strip()
        if not note:
            raise FineError("waiver reason is required")
        amount = account["balance"]
        account["waived"] += amount
        account["balance"] = Decimal("0.00")
        account["waiver_reason"] = note
        return amount

    def _get(self, loan_id):
        if loan_id not in self.accounts:
            raise FineError("fine account not found")
        return self.accounts[loan_id]

    def rows(self):
        return [self.accounts[key] for key in sorted(self.accounts)]


def export_fines(path, rows):
    fields = ("loan_id", "member", "title", "days_late", "fine", "paid", "waived", "balance", "waiver_reason")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for account in rows:
            row = dict(account)
            for key in ("fine", "paid", "waived", "balance"):
                row[key] = "{0:.2f}".format(row[key])
            writer.writerow(row)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how are overdue fees calculated")
print("Q2  can a member pay a fine in parts")
print("Q3  what prevents overpayment")
print("Q4  how can staff forgive a balance with accountability")
print("Q5  how do we know a fine is settled")
print("Q6  what information belongs in a fine ledger")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  late days multiplied by the fixed daily rate")
print("Q2  yes, payments reduce but need not clear the balance")
print("Q3  reject a payment larger than the outstanding amount")
print("Q4  record an explicit waiver reason")
print("Q5  its remaining balance equals zero")
print("Q6  assessed, paid, waived, remaining and reason")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - assess fees from fixed loan dates")
print("TASK 2 - accept partial and full payments")
print("TASK 3 - reject overpayment and unknown accounts")
print("TASK 4 - waive a remaining balance with a reason")
print("TASK 5 - reconcile assessed = paid + waived + balance")
print("TASK 6 - export the fine ledger as CSV")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project73_")
REPORT = os.path.join(WORK, "fine-ledger.csv")
loans = [
    {"loan_id": "L101", "member": "Amina Saleh", "title": "Dune", "due_date": date(2026, 10, 1), "returned_date": date(2026, 10, 8), "rate_per_day": "0.50"},
    {"loan_id": "L102", "member": "Omar Nasser", "title": "Neuromancer", "due_date": date(2026, 10, 10), "returned_date": date(2026, 10, 10), "rate_per_day": "0.50"},
    {"loan_id": "L103", "member": "Lina Haddad", "title": "Café Society", "due_date": date(2026, 10, 2), "returned_date": date(2026, 10, 6), "rate_per_day": "0.75"},
]
desk = FineDesk(loans)

print("=" * 60)
print("TASK 1 - assess late fees")
print("=" * 60)
for account in desk.rows():
    print("{0}: {1} late day(s), fine ${2:.2f}".format(account["loan_id"], account["days_late"], account["fine"]))
print("L101 fine correct ->", check("first fine", desk.accounts["L101"]["fine"] == Decimal("3.50")))
print("on-time loan fine -> ${0:.2f}".format(desk.accounts["L102"]["fine"]))
print()

print("=" * 60)
print("TASK 2 - partial then full payment")
print("=" * 60)
remaining = desk.pay("L101", "1.00")
print("after partial payment -> ${0:.2f}".format(remaining))
remaining = desk.pay("L101", "2.50")
print("after final payment -> ${0:.2f}".format(remaining))
print("fine fully paid ->", check("payment clears balance", remaining == Decimal("0.00") and desk.accounts["L101"]["paid"] == Decimal("3.50")))
print()

print("=" * 60)
print("TASK 3 - reject overpayment")
print("=" * 60)
try:
    desk.pay("L103", "9.00")
except FineError as error:
    overpay_message = str(error)
else:
    overpay_message = "accepted"
print("overpayment ->", overpay_message)
print("balance unchanged ->", check("overpayment is atomic", desk.accounts["L103"]["balance"] == Decimal("3.00")))
print()

print("=" * 60)
print("TASK 4 - waive with an audit reason")
print("=" * 60)
waived = desk.waive("L103", "staff-approved courtesy")
print("waived amount -> ${0:.2f}".format(waived))
print("waiver reason ->", desk.accounts["L103"]["waiver_reason"])
print("remaining balance -> ${0:.2f}".format(desk.accounts["L103"]["balance"]))
check("waiver recorded", waived == Decimal("3.00") and desk.accounts["L103"]["balance"] == Decimal("0.00"))
try:
    desk.waive("L102", "   ")
except FineError as error:
    waiver_message = str(error)
else:
    waiver_message = "accepted"
print("empty waiver reason ->", waiver_message)
print()

print("=" * 60)
print("TASK 5 - reconcile the fine ledger")
print("=" * 60)
for account in desk.rows():
    reconciles = account["fine"] == account["paid"] + account["waived"] + account["balance"]
    print("{0} reconciles -> {1}".format(account["loan_id"], reconciles))
print("all accounts reconcile ->", check("ledger equation", all(row["fine"] == row["paid"] + row["waived"] + row["balance"] for row in desk.rows())))
print("total outstanding -> ${0:.2f}".format(sum((row["balance"] for row in desk.rows()), Decimal("0.00"))))
print()

print("=" * 60)
print("TASK 6 - export fine ledger")
print("=" * 60)
fields = export_fines(REPORT, desk.rows())
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("ledger rows ->", len(report_text.splitlines()) - 1)
print("waiver reason exported ->", "staff-approved courtesy" in report_text)
print("balance field exported ->", "balance" in fields)
check("CSV contains all accounts", len(report_text.splitlines()) == len(loans) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary fine ledger removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
