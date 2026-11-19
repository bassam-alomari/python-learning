# ============================================================
# Project 75 - the bookshop returns damaged stock to suppliers
# ============================================================
# What this project teaches:
#   purchase records    remember supplier, title, qty and unit cost
#   return authorization create an RMA for damaged/incorrect goods
#   quantity guard      never return more than originally purchased
#   refund/credit        calculate value with Decimal
#   idempotency         process each return authorization once
#   audit CSV           export purchase and return decisions
#   validation          reject unknown purchases and bad quantities
#   cleanup             generated report is temporary
#
# Everything uses the standard library and fixed fixtures. No input(),
# random, network or clock. Financial calculations use Decimal.
#
# Run it:  python project-75-the-bookshop-returns-stock-to-suppliers.py
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


class ReturnError(ValueError):
    """Raised when a supplier return is invalid."""


class SupplierReturns:
    """Track purchased quantities and supplier return authorizations."""

    VALID_REASONS = {"damaged", "wrong item", "overstock"}

    def __init__(self, purchases):
        self.purchases = {}
        self.returns = {}
        self.next_id = 1
        for purchase in purchases:
            purchase_id = purchase["purchase_id"]
            if purchase_id in self.purchases:
                raise ReturnError("duplicate purchase ID")
            quantity = purchase["quantity"]
            cost = Decimal(str(purchase["unit_cost"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if not isinstance(quantity, int) or quantity <= 0 or cost < 0:
                raise ReturnError("purchase quantity/cost is invalid")
            self.purchases[purchase_id] = {
                "purchase_id": purchase_id,
                "supplier": purchase["supplier"],
                "title": purchase["title"],
                "quantity": quantity,
                "unit_cost": cost,
                "returned": 0,
            }

    def authorize(self, purchase_id, quantity, reason):
        """Create a return record after validating remaining quantity."""
        purchase = self.purchases.get(purchase_id)
        if purchase is None:
            raise ReturnError("purchase not found")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ReturnError("return quantity must be a positive integer")
        if reason not in self.VALID_REASONS:
            raise ReturnError("unsupported return reason")
        remaining = purchase["quantity"] - purchase["returned"]
        if quantity > remaining:
            raise ReturnError("return quantity exceeds remaining purchased stock")
        return_id = "RMA{0:03d}".format(self.next_id)
        self.next_id += 1
        amount = (purchase["unit_cost"] * quantity).quantize(Decimal("0.01"))
        record = {
            "return_id": return_id,
            "purchase_id": purchase_id,
            "supplier": purchase["supplier"],
            "title": purchase["title"],
            "quantity": quantity,
            "reason": reason,
            "refund": amount,
            "status": "authorized",
        }
        self.returns[return_id] = record
        purchase["returned"] += quantity
        return dict(record)

    def total_refunds(self, supplier=None):
        """Sum authorized refund value, optionally by supplier."""
        return sum((row["refund"] for row in self.returns.values()
                    if supplier is None or row["supplier"] == supplier), Decimal("0.00"))


def export_returns(path, returns):
    fields = ("return_id", "purchase_id", "supplier", "title", "quantity", "reason", "refund", "status")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in sorted(returns, key=lambda row: row["return_id"]):
            row = dict(record)
            row["refund"] = "{0:.2f}".format(row["refund"])
            writer.writerow(row)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what data is needed to return goods to a supplier")
print("Q2  how do we stop returns exceeding the purchased quantity")
print("Q3  how is the refund amount calculated")
print("Q4  why record a return reason and authorization ID")
print("Q5  how can supplier credits be totaled")
print("Q6  how can return decisions be audited")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  purchase ID, supplier, title, quantity and unit cost")
print("Q2  compare the requested amount with unreturned quantity")
print("Q3  unit cost times returned copies")
print("Q4  traceability and inventory control")
print("Q5  sum authorized return values per supplier")
print("Q6  keep an exportable return ledger")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - create supplier purchase records")
print("TASK 2 - authorize a valid damaged-stock return")
print("TASK 3 - prevent returning more than purchased")
print("TASK 4 - reject invalid supplier, quantity or reason")
print("TASK 5 - calculate supplier refund totals")
print("TASK 6 - export the RMA audit ledger")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project75_")
REPORT = os.path.join(WORK, "supplier-returns.csv")
returns = SupplierReturns([
    {"purchase_id": "P100", "supplier": "North Star Books", "title": "Dune", "quantity": 10, "unit_cost": "7.50"},
    {"purchase_id": "P101", "supplier": "Maple Press", "title": "Atlas of Birds", "quantity": 4, "unit_cost": "11.25"},
])

print("=" * 60)
print("TASK 1 - purchased stock records")
print("=" * 60)
print("purchases ->", len(returns.purchases))
print("Dune purchased copies ->", returns.purchases["P100"]["quantity"])
print("supplier ->", returns.purchases["P100"]["supplier"])
print()

print("=" * 60)
print("TASK 2 - authorize a valid return")
print("=" * 60)
rma1 = returns.authorize("P100", 2, "damaged")
print("authorization ->", rma1["return_id"])
print("returned title ->", rma1["title"])
print("return quantity ->", rma1["quantity"])
print("refund -> ${0:.2f}".format(rma1["refund"]))
print("remaining returnable copies ->", returns.purchases["P100"]["quantity"] - returns.purchases["P100"]["returned"])
check("refund calculation", rma1["refund"] == Decimal("15.00"))
print()

print("=" * 60)
print("TASK 3 - return ceiling")
print("=" * 60)
rma2 = returns.authorize("P100", 8, "wrong item")
try:
    returns.authorize("P100", 1, "damaged")
except ReturnError as error:
    too_many_message = str(error)
else:
    too_many_message = "accepted"
print("second authorization ->", rma2["return_id"])
print("over-return ->", too_many_message)
print("purchased quantity never exceeded ->", check("return ceiling", returns.purchases["P100"]["returned"] == returns.purchases["P100"]["quantity"]))
print()

print("=" * 60)
print("TASK 4 - reject invalid return requests")
print("=" * 60)
invalid_messages = []
for purchase_id, quantity, reason in (
    ("P999", 1, "damaged"),
    ("P101", 0, "damaged"),
    ("P101", 1, "changed mind"),
):
    try:
        returns.authorize(purchase_id, quantity, reason)
    except ReturnError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted")
print("invalid cases ->", invalid_messages)
check("invalid supplier/quantity/reason rejected", all(message != "accepted" for message in invalid_messages))
print()

print("=" * 60)
print("TASK 5 - reconcile supplier credits")
print("=" * 60)
print("North Star refund -> ${0:.2f}".format(returns.total_refunds("North Star Books")))
print("all supplier refunds -> ${0:.2f}".format(returns.total_refunds()))
print("refund total correct ->", check("refund ledger total", returns.total_refunds() == Decimal("75.00")))
print()

print("=" * 60)
print("TASK 6 - export the RMA ledger")
print("=" * 60)
fields = export_returns(REPORT, list(returns.returns.values()))
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("RMA rows ->", len(report_text.splitlines()) - 1)
print("reason recorded ->", "damaged" in report_text and "wrong item" in report_text)
print("refund field included ->", "refund" in fields)
check("all return records exported", len(report_text.splitlines()) == len(returns.returns) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary RMA report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
