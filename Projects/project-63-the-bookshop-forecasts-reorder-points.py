# ============================================================
# Project 63 - the bookshop forecasts reorder points
# ============================================================
# What this project teaches:
#   demand history       derive average daily sales from fixed periods
#   lead time            estimate demand while waiting for a supplier
#   safety stock         hold a buffer for uncertainty
#   reorder point        average daily demand * lead time + safety stock
#   order quantity       target stock minus current stock
#   validation           reject missing, negative or inconsistent inputs
#   CSV report           export stable reorder recommendations
#   cleanup              all generated files stay in a temp folder
#
# The forecast is intentionally simple and explainable, not a guarantee.
# No input(), random, network or clock; all fixture data is deterministic.
#
# Run it:  python project-63-the-bookshop-forecasts-reorder-points.py
# ============================================================

import csv
import os
import shutil
import tempfile
from decimal import Decimal, InvalidOperation, ROUND_CEILING

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class ForecastError(ValueError):
    """Raised when sales or stock planning inputs are invalid."""


def recommend_reorder(item):
    """Calculate demand, reorder point and suggested order quantity."""
    required = ("title", "daily_sales", "lead_days", "safety_stock",
                "on_hand", "target_days")
    missing = [key for key in required if key not in item]
    if missing:
        raise ForecastError("missing fields: " + ", ".join(missing))
    title = str(item["title"]).strip()
    if not title:
        raise ForecastError("title is required")
    try:
        sales = Decimal(str(item["daily_sales"]))
        lead = int(item["lead_days"])
        safety = int(item["safety_stock"])
        on_hand = int(item["on_hand"])
        target_days = int(item["target_days"])
    except (TypeError, ValueError, InvalidOperation):
        raise ForecastError("planning values must be numeric")
    if sales < 0 or lead < 0 or safety < 0 or on_hand < 0 or target_days <= 0:
        raise ForecastError("stock values must be nonnegative and target_days positive")
    reorder_point = int((sales * lead).to_integral_value(rounding=ROUND_CEILING)) + safety
    target_stock = int((sales * target_days).to_integral_value(rounding=ROUND_CEILING)) + safety
    order_quantity = max(0, target_stock - on_hand)
    return {
        "title": title,
        "daily_sales": sales,
        "lead_days": lead,
        "safety_stock": safety,
        "on_hand": on_hand,
        "reorder_point": reorder_point,
        "target_stock": target_stock,
        "order_quantity": order_quantity,
        "status": "reorder" if on_hand <= reorder_point else "sufficient",
    }


def average_daily_sales(units_sold, days):
    """Compute average demand per day from a historical window."""
    if not isinstance(units_sold, int) or not isinstance(days, int):
        raise ForecastError("units_sold and days must be integers")
    if units_sold < 0 or days <= 0:
        raise ForecastError("units_sold must be nonnegative and days positive")
    return (Decimal(units_sold) / Decimal(days)).quantize(Decimal("0.01"))


def write_recommendations(path, rows):
    """Export reorder recommendations as a stable CSV."""
    fields = ("title", "daily_sales", "lead_days", "safety_stock", "on_hand",
              "reorder_point", "target_stock", "order_quantity", "status")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["daily_sales"] = "{0:.2f}".format(row["daily_sales"])
            writer.writerow(output)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how can past sales estimate average daily demand")
print("Q2  what is lead time")
print("Q3  why add safety stock")
print("Q4  how is the reorder point calculated")
print("Q5  how many copies should be ordered")
print("Q6  why is a forecast an estimate, not a promise")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  divide sold units by the number of observed days")
print("Q2  the number of days between ordering and delivery")
print("Q3  it buffers demand and delivery uncertainty")
print("Q4  rounded-up daily demand times lead days plus safety stock")
print("Q5  target stock minus stock on hand, never below zero")
print("Q6  actual demand and delivery times can change")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - calculate daily demand from history")
print("TASK 2 - set supplier lead time and safety stock")
print("TASK 3 - calculate reorder point and target stock")
print("TASK 4 - recommend order quantities")
print("TASK 5 - distinguish reorder from sufficient stock")
print("TASK 6 - reject invalid planning data")
print("TASK 7 - export recommendations to CSV")
print("TASK 8 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project63_")
REPORT = os.path.join(WORK, "reorder-recommendations.csv")

sold_last_30 = {"Dune": 90, "Neuromancer": 30, "Café Society": 15}
demand = {title: average_daily_sales(units, 30) for title, units in sold_last_30.items()}
print("=" * 60)
print("TASK 1 - average daily demand")
print("=" * 60)
for title in sorted(demand):
    print("{0} -> {1:.2f} copies/day".format(title, demand[title]))
print("Dune average correct ->", check("daily demand", demand["Dune"] == Decimal("3.00")))
print()

print("=" * 60)
print("TASK 2 - planning inputs")
print("=" * 60)
plans = [
    {"title": "Dune", "daily_sales": demand["Dune"], "lead_days": 7, "safety_stock": 5, "on_hand": 20, "target_days": 14},
    {"title": "Neuromancer", "daily_sales": demand["Neuromancer"], "lead_days": 10, "safety_stock": 3, "on_hand": 8, "target_days": 21},
    {"title": "Café Society", "daily_sales": demand["Café Society"], "lead_days": 5, "safety_stock": 2, "on_hand": 20, "target_days": 14},
]
print("items planned ->", len(plans))
print("lead-time range ->", min(row["lead_days"] for row in plans), "to", max(row["lead_days"] for row in plans), "days")
print("target days positive ->", all(row["target_days"] > 0 for row in plans))
print()

print("=" * 60)
print("TASK 3 - reorder points and target stock")
print("=" * 60)
recommendations = [recommend_reorder(plan) for plan in plans]
for row in recommendations:
    print("{0}: reorder at {1}, target {2}".format(row["title"], row["reorder_point"], row["target_stock"]))
dune_plan = next(row for row in recommendations if row["title"] == "Dune")
print("Dune reorder point correct ->", check("reorder point math", dune_plan["reorder_point"] == 26))
print()

print("=" * 60)
print("TASK 4 - order quantities")
print("=" * 60)
for row in recommendations:
    print("{0}: order {1} ({2})".format(row["title"], row["order_quantity"], row["status"]))
print("Neuromancer quantity correct ->", check("target minus on-hand", next(row for row in recommendations if row["title"] == "Neuromancer")["order_quantity"] == 16))
print("sufficient Dune stock ->", next(row for row in recommendations if row["title"] == "Dune")["status"])
print()

print("=" * 60)
print("TASK 5 - test reorder threshold boundary")
print("=" * 60)
boundary_plan = dict(plans[0], on_hand=dune_plan["reorder_point"])
boundary = recommend_reorder(boundary_plan)
print("stock exactly at reorder point ->", boundary["status"])
print("boundary triggers reorder ->", check("inclusive threshold", boundary["status"] == "reorder"))
empty_plan = dict(plans[0], on_hand=0)
print("zero stock order quantity ->", recommend_reorder(empty_plan)["order_quantity"])
print()

print("=" * 60)
print("TASK 6 - reject invalid planning data")
print("=" * 60)
invalid = [
    dict(plans[0], lead_days=-1),
    dict(plans[0], target_days=0),
    dict(plans[0], daily_sales="many"),
]
invalid_messages = []
for item in invalid:
    try:
        recommend_reorder(item)
    except ForecastError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted")
print("invalid cases ->", invalid_messages)
print("all invalid inputs rejected ->", check("invalid planning inputs", all(message != "accepted" for message in invalid_messages)))
print()

print("=" * 60)
print("TASK 7 - export CSV recommendations")
print("=" * 60)
fields = write_recommendations(REPORT, recommendations)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("CSV data rows ->", len(report_text.splitlines()) - 1)
print("CSV includes order quantity ->", "order_quantity" in fields)
print("CSV includes Café Society ->", "Café Society" in report_text)
check("report contains all items", len(report_text.splitlines()) == len(recommendations) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary forecast report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
