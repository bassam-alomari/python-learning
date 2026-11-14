# ============================================================
# Project 58 - the bookshop rewards loyal customers
# ============================================================
# What this project teaches:
#   loyalty ledger       associate sales with customer IDs
#   points earning       award whole points from eligible spend
#   redemption           convert points into a bounded discount
#   idempotency          process each receipt only once
#   validation           reject unknown customers and bad amounts
#   statements           summarize earned, redeemed and balance
#   CSV export           save a deterministic customer report
#   cleanup              keep generated files in a temporary folder
#
# Everything uses the standard library. The receipt/customer fixtures
# are fixed; no input(), random, network or clock is used.
#
# Run it:  python project-58-the-bookshop-rewards-loyal-customers.py
# ============================================================

import csv
import os
import shutil
import tempfile
from collections import defaultdict

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class LoyaltyError(ValueError):
    """Raised when a loyalty operation is invalid."""


class LoyaltyProgram:
    """Track earned/redeemed points and processed receipts."""

    POINTS_PER_DOLLAR = 1
    POINTS_PER_DOLLAR_OFF = 10

    def __init__(self, customers):
        self.customers = {customer_id: name for customer_id, name in customers}
        self.balances = {customer_id: 0 for customer_id in self.customers}
        self.earned = defaultdict(int)
        self.redeemed = defaultdict(int)
        self.processed_receipts = set()

    def earn(self, customer_id, receipt_id, amount):
        """Award points for a new eligible sale receipt."""
        self._known_customer(customer_id)
        if receipt_id in self.processed_receipts:
            raise LoyaltyError("receipt already processed")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise LoyaltyError("sale amount must be positive")
        points = int(amount * self.POINTS_PER_DOLLAR)
        self.balances[customer_id] += points
        self.earned[customer_id] += points
        self.processed_receipts.add(receipt_id)
        return points

    def redeem(self, customer_id, points, subtotal):
        """Redeem points, capped by the purchase subtotal."""
        self._known_customer(customer_id)
        if not isinstance(points, int) or points <= 0:
            raise LoyaltyError("points must be a positive integer")
        if not isinstance(subtotal, (int, float)) or subtotal <= 0:
            raise LoyaltyError("subtotal must be positive")
        if points > self.balances[customer_id]:
            raise LoyaltyError("insufficient points")
        requested_discount = points / self.POINTS_PER_DOLLAR_OFF
        discount = min(float(subtotal), requested_discount)
        points_used = min(points, int(discount * self.POINTS_PER_DOLLAR_OFF))
        self.balances[customer_id] -= points_used
        self.redeemed[customer_id] += points_used
        return round(discount, 2), points_used

    def statement(self, customer_id):
        """Return a stable summary for one customer."""
        self._known_customer(customer_id)
        return {
            "customer_id": customer_id,
            "name": self.customers[customer_id],
            "earned": self.earned[customer_id],
            "redeemed": self.redeemed[customer_id],
            "balance": self.balances[customer_id],
        }

    def _known_customer(self, customer_id):
        if customer_id not in self.customers:
            raise LoyaltyError("customer not found")


def export_statements(path, statements):
    """Write customer loyalty statements to a CSV file."""
    fields = ("customer_id", "name", "earned", "redeemed", "balance")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(statements)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how does a customer earn loyalty points")
print("Q2  how can the same receipt be prevented from earning twice")
print("Q3  how are points converted to a discount")
print("Q4  what happens if requested points exceed the balance")
print("Q5  how do we keep a discount within the purchase subtotal")
print("Q6  what belongs in a customer statement")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  award whole points from eligible sale value")
print("Q2  remember processed receipt IDs")
print("Q3  apply the program's points-to-currency rule")
print("Q4  reject redemption without changing the balance")
print("Q5  cap the discount at the subtotal")
print("Q6  earned, redeemed and remaining points")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - register customers")
print("TASK 2 - award points from sale receipts")
print("TASK 3 - block duplicate receipt processing")
print("TASK 4 - redeem points for a capped discount")
print("TASK 5 - reject invalid customers and insufficient balance")
print("TASK 6 - prepare customer statements")
print("TASK 7 - export statements to CSV")
print("TASK 8 - clean up the report file")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project58_")
REPORT = os.path.join(WORK, "loyalty-statements.csv")
program = LoyaltyProgram([
    ("C001", "Amina Saleh"),
    ("C002", "Omar Nasser"),
])

print("=" * 60)
print("TASK 1 - register customers")
print("=" * 60)
print("customers ->", len(program.customers))
print("known customer ->", program.customers["C001"])
check("all balances start at zero", all(points == 0 for points in program.balances.values()))
print()

print("=" * 60)
print("TASK 2 - earn points from receipts")
print("=" * 60)
points_a = program.earn("C001", "R100", 24.75)
points_b = program.earn("C001", "R101", 10.00)
points_c = program.earn("C002", "R102", 18.40)
print("R100 points ->", points_a)
print("R101 points ->", points_b)
print("C002 points ->", points_c)
print("C001 balance ->", program.balances["C001"])
check("whole points awarded", (points_a, points_b, points_c) == (24, 10, 18))
print()

print("=" * 60)
print("TASK 3 - duplicate receipt protection")
print("=" * 60)
balance_before_duplicate = program.balances["C001"]
try:
    program.earn("C001", "R100", 24.75)
except LoyaltyError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
print("duplicate receipt ->", duplicate_message)
print("points not duplicated ->", check("duplicate does not change balance", program.balances["C001"] == balance_before_duplicate))
print()

print("=" * 60)
print("TASK 4 - redeem points for a capped discount")
print("=" * 60)
discount, points_used = program.redeem("C001", 20, subtotal=1.25)
print("requested points ->", 20)
print("discount applied -> ${0:.2f}".format(discount))
print("points actually used ->", points_used)
print("remaining C001 points ->", program.balances["C001"])
check("discount capped at subtotal", discount == 1.25 and points_used == 12)
print()

print("=" * 60)
print("TASK 5 - reject invalid redemption")
print("=" * 60)
balance_before_failure = program.balances["C001"]
try:
    program.redeem("C001", 999, subtotal=50)
except LoyaltyError as error:
    insufficient_message = str(error)
else:
    insufficient_message = "accepted"
print("insufficient points ->", insufficient_message)
print("balance unchanged ->", check("failed redemption is atomic", program.balances["C001"] == balance_before_failure))
try:
    program.earn("C999", "R999", 5)
except LoyaltyError as error:
    unknown_message = str(error)
else:
    unknown_message = "accepted"
print("unknown customer ->", unknown_message)
print()

print("=" * 60)
print("TASK 6 - create customer statements")
print("=" * 60)
statements = [program.statement(customer_id) for customer_id in sorted(program.customers)]
for statement in statements:
    print("{0}: earned {1}, redeemed {2}, balance {3}".format(
        statement["name"], statement["earned"], statement["redeemed"], statement["balance"]
    ))
print("two statements ->", check("one statement per customer", len(statements) == 2))
print()

print("=" * 60)
print("TASK 7 - export statements to CSV")
print("=" * 60)
fields = export_statements(REPORT, statements)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("CSV rows ->", len(report_text.splitlines()) - 1)
print("UTF-8 customer name ->", "Amina Saleh" in report_text)
check("CSV includes both customers", len(report_text.splitlines()) == 3)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("report folder removed", not os.path.exists(WORK))
print("temporary report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
