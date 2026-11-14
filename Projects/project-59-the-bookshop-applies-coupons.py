# ============================================================
# Project 59 - the bookshop applies coupons and promotions
# ============================================================
# What this project teaches:
#   coupon rules        percent/fixed discounts with validity checks
#   minimum subtotal    refuse a coupon below its threshold
#   usage limits        stop a code after its allowed redemptions
#   stacking policy     prevent combining exclusive promotions
#   price safety        never discount below zero
#   receipt breakdown   show subtotal, discount and amount due
#   deterministic data  fixed cart and coupon definitions
#   cleanup             all generated report files are temporary
#
# Everything uses the standard library. No input(), random, network or clock.
#
# Run it:  python project-59-the-bookshop-applies-coupons.py
# ============================================================

import csv
import os
import shutil
import tempfile

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class CouponError(ValueError):
    """Raised when a coupon cannot be applied."""


class PromotionDesk:
    """Validate and apply coupon codes to a shopping cart."""

    def __init__(self, coupons):
        self.coupons = {coupon["code"].casefold(): dict(coupon) for coupon in coupons}
        self.uses = {code: 0 for code in self.coupons}

    def apply(self, code, subtotal, active_promotions=()):
        """Return a priced receipt or reject an invalid promotion."""
        if not isinstance(subtotal, (int, float)) or subtotal < 0:
            raise CouponError("subtotal must be nonnegative")
        key = code.casefold()
        coupon = self.coupons.get(key)
        if coupon is None:
            raise CouponError("coupon not found")
        if self.uses[key] >= coupon["max_uses"]:
            raise CouponError("coupon usage limit reached")
        if subtotal < coupon["minimum"]:
            raise CouponError("minimum subtotal not met")
        if active_promotions and not coupon["stackable"]:
            raise CouponError("coupon cannot be stacked")

        if coupon["kind"] == "percent":
            discount = subtotal * coupon["value"] / 100
        elif coupon["kind"] == "fixed":
            discount = coupon["value"]
        else:
            raise CouponError("unsupported coupon kind")
        discount = round(min(float(subtotal), discount), 2)
        total = round(float(subtotal) - discount, 2)
        self.uses[key] += 1
        return {
            "code": coupon["code"],
            "subtotal": round(float(subtotal), 2),
            "discount": discount,
            "total": total,
            "uses_left": coupon["max_uses"] - self.uses[key],
        }


def apply_best(coupons, subtotal):
    """Compute possible discounts without consuming coupon uses."""
    options = []
    for coupon in coupons:
        if subtotal < coupon["minimum"] or coupon["max_uses"] <= 0:
            continue
        if coupon["kind"] == "percent":
            amount = subtotal * coupon["value"] / 100
        else:
            amount = coupon["value"]
        options.append((min(float(subtotal), amount), coupon["code"]))
    return sorted(options, key=lambda item: (-item[0], item[1]))


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what can a coupon rule contain")
print("Q2  when should a coupon be rejected")
print("Q3  how do usage limits prevent unlimited redemption")
print("Q4  what does non-stackable mean")
print("Q5  how can a discount avoid a negative total")
print("Q6  how should competing offers be compared")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  code, type, value, minimum spend and maximum uses")
print("Q2  unknown code, low subtotal, exhausted or conflicting offer")
print("Q3  count successful applications and enforce the cap")
print("Q4  do not combine it with another active promotion")
print("Q5  cap the discount at the subtotal")
print("Q6  compare eligible discounts before consuming a code")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - define percentage and fixed coupons")
print("TASK 2 - apply a valid coupon and print a receipt")
print("TASK 3 - reject low subtotal and unknown codes")
print("TASK 4 - enforce max uses and no-stacking rules")
print("TASK 5 - prevent negative totals")
print("TASK 6 - compare eligible offers without consuming them")
print("TASK 7 - export the receipt breakdown to CSV")
print("TASK 8 - clean up the report file")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project59_")
RECEIPT_PATH = os.path.join(WORK, "discount-receipt.csv")
coupons = [
    {"code": "WELCOME10", "kind": "percent", "value": 10, "minimum": 20, "max_uses": 2, "stackable": False},
    {"code": "SAVE5", "kind": "fixed", "value": 5, "minimum": 15, "max_uses": 1, "stackable": True},
    {"code": "HALFOFF", "kind": "percent", "value": 50, "minimum": 0, "max_uses": 1, "stackable": False},
]
desk = PromotionDesk(coupons)

print("=" * 60)
print("TASK 1 - coupon catalogue")
print("=" * 60)
print("coupon codes ->", ", ".join(coupon["code"] for coupon in coupons))
print("coupon count ->", len(coupons))
check("codes unique ignoring case", len(desk.coupons) == len(coupons))
print()

print("=" * 60)
print("TASK 2 - apply a percentage coupon")
print("=" * 60)
receipt = desk.apply("welcome10", subtotal=50)
print("code ->", receipt["code"])
print("subtotal -> ${0:.2f}".format(receipt["subtotal"]))
print("discount -> ${0:.2f}".format(receipt["discount"]))
print("amount due -> ${0:.2f}".format(receipt["total"]))
print("uses left ->", receipt["uses_left"])
check("percent math", receipt["discount"] == 5.0 and receipt["total"] == 45.0)
print()

print("=" * 60)
print("TASK 3 - reject ineligible coupons")
print("=" * 60)
try:
    desk.apply("WELCOME10", subtotal=10)
except CouponError as error:
    low_message = str(error)
else:
    low_message = "accepted"
try:
    desk.apply("UNKNOWN", subtotal=100)
except CouponError as error:
    unknown_message = str(error)
else:
    unknown_message = "accepted"
print("below minimum ->", low_message)
print("unknown code ->", unknown_message)
check("both invalid cases rejected", low_message == "minimum subtotal not met" and unknown_message == "coupon not found")
print()

print("=" * 60)
print("TASK 4 - enforce usage and stacking")
print("=" * 60)
second_welcome = desk.apply("WELCOME10", subtotal=30)
try:
    desk.apply("WELCOME10", subtotal=30)
except CouponError as error:
    exhausted_message = str(error)
else:
    exhausted_message = "accepted"
try:
    desk.apply("HALFOFF", subtotal=30, active_promotions=("member day",))
except CouponError as error:
    stacking_message = str(error)
else:
    stacking_message = "accepted"
print("second welcome uses left ->", second_welcome["uses_left"])
print("third welcome ->", exhausted_message)
print("stacked welcome ->", stacking_message)
check("usage cap enforced", exhausted_message == "coupon usage limit reached")
check("exclusive offer enforced", stacking_message == "coupon cannot be stacked")
print()

print("=" * 60)
print("TASK 5 - discount cannot make a negative total")
print("=" * 60)
half_receipt = desk.apply("HALFOFF", subtotal=4)
print("large coupon discount -> ${0:.2f}".format(half_receipt["discount"]))
print("amount due -> ${0:.2f}".format(half_receipt["total"]))
print("total is nonnegative ->", check("no negative total", half_receipt["total"] >= 0))
print()

print("=" * 60)
print("TASK 6 - compare offers before using one")
print("=" * 60)
best_options = apply_best(coupons, subtotal=50)
print("best eligible offer ->", best_options[0][1])
print("best discount -> ${0:.2f}".format(best_options[0][0]))
print("comparison did not consume codes ->", check("comparison is side-effect free", desk.uses["halfoff"] == 1))
print()

print("=" * 60)
print("TASK 7 - export the receipt")
print("=" * 60)
fields = ("code", "subtotal", "discount", "total", "uses_left")
with open(RECEIPT_PATH, "w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerow(receipt)
with open(RECEIPT_PATH, "r", encoding="utf-8", newline="") as handle:
    receipt_csv = handle.read()
print("CSV header ->", receipt_csv.splitlines()[0])
print("receipt CSV row ->", receipt_csv.splitlines()[1])
check("receipt file exists", os.path.isfile(RECEIPT_PATH))
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("temporary report removed", not os.path.exists(WORK))
print("temporary receipt folder removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
