# ============================================================
# Project 76 - the bookshop handles customer returns and refunds
# ============================================================
# What this project teaches:
#   sales ledger       retain original receipt lines and quantities
#   return validation  require a known receipt and unreturned copies
#   refund calculation unit price times returned quantity
#   payment choice    refund to original method or store credit
#   duplicate guard   reject repeated return transaction IDs
#   audit CSV          export return reason, amount and disposition
#   Decimal money     exact currency calculations
#   cleanup           generated reports live in a temporary folder
#
# Everything uses the standard library and fixed records. No input(),
# random, network or clock.
#
# Run it:  python project-76-the-bookshop-processes-customer-returns.py
# ============================================================

import csv
import os
import shutil
import tempfile
from decimal import Decimal, ROUND_HALF_UP

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class CustomerReturnError(ValueError):
    """Raised when a customer return is invalid."""


class ReturnDesk:
    """Process refunds and store credit against original receipts."""

    ALLOWED_REASONS = {"damaged", "wrong item", "unwanted"}
    ALLOWED_METHODS = {"original", "store credit"}

    def __init__(self, sales):
        self.sales = {}
        self.returns = []
        self.processed_return_ids = set()
        for sale in sales:
            receipt_id = sale["receipt_id"]
            if receipt_id in self.sales:
                raise CustomerReturnError("duplicate receipt ID")
            quantity = sale["quantity"]
            unit_price = Decimal(str(sale["unit_price"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if not isinstance(quantity, int) or quantity <= 0 or unit_price < 0:
                raise CustomerReturnError("invalid sale record")
            self.sales[receipt_id] = {
                "receipt_id": receipt_id,
                "customer": sale["customer"],
                "title": sale["title"],
                "quantity": quantity,
                "unit_price": unit_price,
                "returned": 0,
            }

    def process(self, return_id, receipt_id, quantity, reason, method):
        """Validate and record a partial or full customer return."""
        if return_id in self.processed_return_ids:
            raise CustomerReturnError("return ID already processed")
        sale = self.sales.get(receipt_id)
        if sale is None:
            raise CustomerReturnError("receipt not found")
        if not isinstance(quantity, int) or quantity <= 0:
            raise CustomerReturnError("return quantity must be positive")
        if quantity > sale["quantity"] - sale["returned"]:
            raise CustomerReturnError("return quantity exceeds unreturned items")
        if reason not in self.ALLOWED_REASONS:
            raise CustomerReturnError("unsupported return reason")
        if method not in self.ALLOWED_METHODS:
            raise CustomerReturnError("unsupported refund method")
        amount = (sale["unit_price"] * quantity).quantize(Decimal("0.01"))
        record = {
            "return_id": return_id,
            "receipt_id": receipt_id,
            "customer": sale["customer"],
            "title": sale["title"],
            "quantity": quantity,
            "reason": reason,
            "method": method,
            "amount": amount,
        }
        sale["returned"] += quantity
        self.processed_return_ids.add(return_id)
        self.returns.append(record)
        return dict(record)


def write_return_report(path, records):
    fields = ("return_id", "receipt_id", "customer", "title", "quantity", "reason", "method", "amount")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in sorted(records, key=lambda row: row["return_id"]):
            row = dict(record)
            row["amount"] = "{0:.2f}".format(row["amount"])
            writer.writerow(row)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how do we know what was originally purchased")
print("Q2  how do we prevent returning more copies than sold")
print("Q3  how is the refund amount calculated")
print("Q4  where can the refund be sent")
print("Q5  why use unique return IDs")
print("Q6  what should an audit record preserve")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  use the original receipt ID")
print("Q2  track returned quantity per receipt line")
print("Q3  original unit price times returned quantity")
print("Q4  original payment method or store credit")
print("Q5  prevent processing the same return twice")
print("Q6  receipt, customer, item, reason, method and amount")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - load original sale receipts")
print("TASK 2 - process partial returns")
print("TASK 3 - calculate refund or store-credit amount")
print("TASK 4 - reject over-returns and duplicate IDs")
print("TASK 5 - preserve a return reason and payment method")
print("TASK 6 - export the customer-return ledger")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project76_")
REPORT = os.path.join(WORK, "customer-returns.csv")
desk = ReturnDesk([
    {"receipt_id": "S101", "customer": "Amina Saleh", "title": "Dune", "quantity": 3, "unit_price": "12.50"},
    {"receipt_id": "S102", "customer": "Omar Nasser", "title": "Neuromancer", "quantity": 2, "unit_price": "9.99"},
])

print("=" * 60)
print("TASK 1 - original sales")
print("=" * 60)
print("receipts ->", len(desk.sales))
print("S101 item ->", desk.sales["S101"]["title"])
print("S101 quantity ->", desk.sales["S101"]["quantity"])
print()

print("=" * 60)
print("TASK 2 - partial customer return")
print("=" * 60)
r1 = desk.process("CR001", "S101", 1, "damaged", "original")
print("return ID ->", r1["return_id"])
print("item ->", r1["title"])
print("quantity returned ->", r1["quantity"])
print("refund -> ${0:.2f}".format(r1["amount"]))
print("remaining returnable copies ->", desk.sales["S101"]["quantity"] - desk.sales["S101"]["returned"])
check("partial refund math", r1["amount"] == Decimal("12.50"))
print()

print("=" * 60)
print("TASK 3 - store credit for remaining items")
print("=" * 60)
r2 = desk.process("CR002", "S101", 2, "unwanted", "store credit")
print("second return ->", r2["return_id"])
print("store credit -> ${0:.2f}".format(r2["amount"]))
print("original sale fully returned ->", desk.sales["S101"]["returned"] == desk.sales["S101"]["quantity"])
print("total S101 refunds -> ${0:.2f}".format(sum((r["amount"] for r in desk.returns if r["receipt_id"] == "S101"), Decimal("0.00"))))
print()

print("=" * 60)
print("TASK 4 - prevent excess and duplicate returns")
print("=" * 60)
try:
    desk.process("CR003", "S101", 1, "damaged", "original")
except CustomerReturnError as error:
    excess_message = str(error)
else:
    excess_message = "accepted"
try:
    desk.process("CR001", "S102", 1, "wrong item", "original")
except CustomerReturnError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
print("excess quantity ->", excess_message)
print("duplicate return ID ->", duplicate_message)
check("excess and duplicate blocked", excess_message == "return quantity exceeds unreturned items" and duplicate_message == "return ID already processed")
print()

print("=" * 60)
print("TASK 5 - reject invalid receipt, reason and method")
print("=" * 60)
messages = []
for return_id, receipt_id, reason, method in (
    ("CR004", "S999", "damaged", "original"),
    ("CR005", "S102", "other", "original"),
    ("CR006", "S102", "damaged", "crypto"),
):
    try:
        desk.process(return_id, receipt_id, 1, reason, method)
    except CustomerReturnError as error:
        messages.append(str(error))
    else:
        messages.append("accepted")
print("invalid cases ->", messages)
check("invalid return requests rejected", all(message != "accepted" for message in messages))
print()

print("=" * 60)
print("TASK 6 - export customer return ledger")
print("=" * 60)
fields = write_return_report(REPORT, desk.returns)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("return rows ->", len(report_text.splitlines()) - 1)
print("store credit recorded ->", "store credit" in report_text)
print("reasons recorded ->", "damaged" in report_text and "unwanted" in report_text)
check("all returns exported", len(report_text.splitlines()) == len(desk.returns) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary return report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
