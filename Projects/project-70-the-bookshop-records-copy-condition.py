# ============================================================
# Project 70 - the bookshop records damage and replacement fees
# ============================================================
# What this project teaches:
#   condition tracking   record each physical copy's condition
#   checkout/return      update availability and return condition
#   fee rules            distinguish normal, damaged and lost copies
#   state transitions    prevent duplicate return processing
#   inventory integrity  keep copy states consistent
#   audit CSV            export per-copy condition and fee history
#   validation           reject unknown copies and invalid conditions
#   cleanup              generated report is temporary
#
# Everything uses the standard library and fixed fixtures. No input(),
# random, network or clock. Money is handled with Decimal.
#
# Run it:  python project-70-the-bookshop-records-copy-condition.py
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


class ConditionError(ValueError):
    """Raised when a copy state transition is invalid."""


class CopyDesk:
    """Track each copy's state and assessed return fees."""

    ALLOWED_CONDITIONS = {"good", "damaged", "lost"}

    def __init__(self, copies, damage_fee="3.00", replacement_fee="12.00"):
        self.copies = {row["copy_id"]: dict(row) for row in copies}
        self.damage_fee = Decimal(str(damage_fee)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.replacement_fee = Decimal(str(replacement_fee)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.events = []

    def checkout(self, copy_id, member):
        copy = self._get(copy_id)
        if copy["status"] != "available":
            raise ConditionError("copy is not available")
        if not member.strip():
            raise ConditionError("member is required")
        copy["status"] = "loaned"
        copy["member"] = member.strip()
        self.events.append({"copy_id": copy_id, "event": "checkout", "member": member.strip(), "condition": copy["condition"], "fee": Decimal("0.00")})
        return dict(copy)

    def return_copy(self, copy_id, condition):
        copy = self._get(copy_id)
        if copy["status"] != "loaned":
            raise ConditionError("copy is not currently loaned")
        if condition not in self.ALLOWED_CONDITIONS:
            raise ConditionError("unknown return condition")
        if condition == "good":
            fee = Decimal("0.00")
            copy["status"] = "available"
        elif condition == "damaged":
            fee = self.damage_fee
            copy["status"] = "available"
        else:
            fee = self.replacement_fee
            copy["status"] = "lost"
        copy["condition"] = condition
        member = copy.pop("member")
        self.events.append({"copy_id": copy_id, "event": "return", "member": member, "condition": condition, "fee": fee})
        return fee

    def _get(self, copy_id):
        if copy_id not in self.copies:
            raise ConditionError("copy not found")
        return self.copies[copy_id]

    def available_count(self, title):
        return sum(1 for copy in self.copies.values()
                   if copy["title"].casefold() == title.casefold()
                   and copy["status"] == "available")


def export_events(path, events):
    fields = ("copy_id", "event", "member", "condition", "fee")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for event in events:
            row = dict(event)
            row["fee"] = "{0:.2f}".format(row["fee"])
            writer.writerow(row)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  why track condition for each physical copy")
print("Q2  what happens when a book returns damaged")
print("Q3  how is a lost copy different from a damaged one")
print("Q4  how should duplicate return attempts be handled")
print("Q5  what should an audit record contain")
print("Q6  how can fees be reviewed later")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  availability and future lending depend on copy state")
print("Q2  assess the damage fee and return it to available stock")
print("Q3  lost copies leave circulation and incur replacement cost")
print("Q4  reject them because the copy is no longer loaned")
print("Q5  copy, event, member, condition and fee")
print("Q6  export a CSV audit ledger")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - prepare individually identified copies")
print("TASK 2 - check out available copies")
print("TASK 3 - return a good copy with no fee")
print("TASK 4 - return a damaged copy and assess a fee")
print("TASK 5 - mark a lost copy unavailable and charge replacement")
print("TASK 6 - reject invalid state transitions")
print("TASK 7 - export the condition audit CSV")
print("TASK 8 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project70_")
REPORT = os.path.join(WORK, "copy-condition-audit.csv")
desk = CopyDesk([
    {"copy_id": "D-001", "title": "Dune", "status": "available", "condition": "good"},
    {"copy_id": "D-002", "title": "Dune", "status": "available", "condition": "good"},
    {"copy_id": "N-001", "title": "Neuromancer", "status": "available", "condition": "good"},
])

print("=" * 60)
print("TASK 1 - copy-level inventory")
print("=" * 60)
print("copies tracked ->", len(desk.copies))
print("available Dune copies ->", desk.available_count("Dune"))
print("copy IDs unique ->", check("copy IDs unique", len(desk.copies) == len({row["copy_id"] for row in desk.copies.values()})))
print()

print("=" * 60)
print("TASK 2 - check out copies")
print("=" * 60)
desk.checkout("D-001", "Amina")
desk.checkout("D-002", "Omar")
desk.checkout("N-001", "Lina")
print("available Dune copies after checkout ->", desk.available_count("Dune"))
print("loaned copies ->", sum(copy["status"] == "loaned" for copy in desk.copies.values()))
check("checkout changes status", all(desk.copies[copy_id]["status"] == "loaned" for copy_id in ("D-001", "D-002", "N-001")))
print()

print("=" * 60)
print("TASK 3 - good return has no fee")
print("=" * 60)
good_fee = desk.return_copy("D-001", "good")
print("good-return fee -> ${0:.2f}".format(good_fee))
print("Dune available copies ->", desk.available_count("Dune"))
check("good copy returned to shelf", good_fee == Decimal("0.00") and desk.copies["D-001"]["status"] == "available")
print()

print("=" * 60)
print("TASK 4 - damaged return has repair fee")
print("=" * 60)
damage_fee = desk.return_copy("D-002", "damaged")
print("damage fee -> ${0:.2f}".format(damage_fee))
print("damaged copy condition ->", desk.copies["D-002"]["condition"])
print("damaged copy remains available ->", desk.copies["D-002"]["status"] == "available")
check("damage fee applied", damage_fee == Decimal("3.00"))
print()

print("=" * 60)
print("TASK 5 - lost return removes copy from circulation")
print("=" * 60)
replacement_fee = desk.return_copy("N-001", "lost")
print("replacement fee -> ${0:.2f}".format(replacement_fee))
print("lost copy status ->", desk.copies["N-001"]["status"])
print("available Neuromancer copies ->", desk.available_count("Neuromancer"))
check("lost copy not available", replacement_fee == Decimal("12.00") and desk.copies["N-001"]["status"] == "lost")
print()

print("=" * 60)
print("TASK 6 - reject invalid transitions and conditions")
print("=" * 60)
try:
    desk.return_copy("D-001", "good")
except ConditionError as error:
    second_return_message = str(error)
else:
    second_return_message = "accepted"
try:
    desk.checkout("N-001", "Omar")
except ConditionError as error:
    lost_checkout_message = str(error)
else:
    lost_checkout_message = "accepted"
print("second return ->", second_return_message)
print("lost copy checkout ->", lost_checkout_message)
print("invalid actions rejected ->", check("invalid transition guard", second_return_message == "copy is not currently loaned" and lost_checkout_message == "copy is not available"))
print()

print("=" * 60)
print("TASK 7 - export condition audit")
print("=" * 60)
fields = export_events(REPORT, desk.events)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    audit_text = handle.read()
print("CSV header ->", audit_text.splitlines()[0])
print("audit events ->", len(audit_text.splitlines()) - 1)
print("damage fee recorded ->", "3.00" in audit_text)
print("replacement fee recorded ->", "12.00" in audit_text)
print("condition field included ->", "condition" in fields)
check("all copy events exported", len(audit_text.splitlines()) == len(desk.events) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary condition report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
