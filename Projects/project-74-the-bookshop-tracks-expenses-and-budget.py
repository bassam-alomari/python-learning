# ============================================================
# Project 74 - the bookshop tracks expenses against a budget
# ============================================================
# What this project teaches:
#   expense ledger       record amount, category and description
#   category totals      summarize spending by budget category
#   budget comparison    calculate remaining/over-budget amounts
#   Decimal money        keep monetary arithmetic exact
#   validation           reject unknown categories and bad amounts
#   CSV reporting        export expense rows and budget summary
#   stable fixtures      no input(), random, network or clock
#   cleanup              generated reports are temporary
#
# Run it:  python project-74-the-bookshop-tracks-expenses.py
# ============================================================

import csv
import os
import shutil
import tempfile
from collections import defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CHECKS = []
CENT = Decimal("0.01")


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class ExpenseError(ValueError):
    """Raised when an expense record is invalid."""


def normalize_expense(row, categories):
    required = ("expense_id", "category", "description", "amount")
    missing = [field for field in required if field not in row]
    if missing:
        raise ExpenseError("missing fields: " + ", ".join(missing))
    expense_id = str(row["expense_id"]).strip()
    category = str(row["category"]).strip().casefold()
    description = str(row["description"]).strip()
    if not expense_id or not description:
        raise ExpenseError("expense ID and description are required")
    if category not in categories:
        raise ExpenseError("unknown expense category")
    try:
        amount = Decimal(str(row["amount"])).quantize(CENT, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ExpenseError("amount must be numeric")
    if not amount.is_finite() or amount < 0:
        raise ExpenseError("amount must be finite and nonnegative")
    return {"expense_id": expense_id, "category": category,
            "description": description, "amount": amount}


def summarize_budget(expenses, budgets):
    """Return spent, budget and remaining amount per category."""
    spent = defaultdict(lambda: Decimal("0.00"))
    for row in expenses:
        spent[row["category"]] += row["amount"]
    summary = {}
    for category in sorted(budgets):
        budget = Decimal(str(budgets[category])).quantize(CENT)
        amount_spent = spent[category].quantize(CENT)
        remaining = (budget - amount_spent).quantize(CENT)
        summary[category] = {
            "budget": budget,
            "spent": amount_spent,
            "remaining": remaining,
            "status": "over budget" if remaining < 0 else "within budget",
        }
    return summary


def write_expense_report(path, expenses):
    fields = ("expense_id", "category", "description", "amount")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in expenses:
            output = dict(row)
            output["amount"] = "{0:.2f}".format(row["amount"])
            writer.writerow(output)
    return fields


def write_budget_report(path, summary):
    fields = ("category", "budget", "spent", "remaining", "status")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for category, row in sorted(summary.items()):
            writer.writerow({
                "category": category,
                "budget": "{0:.2f}".format(row["budget"]),
                "spent": "{0:.2f}".format(row["spent"]),
                "remaining": "{0:.2f}".format(row["remaining"]),
                "status": row["status"],
            })
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how can the bookshop track its expenses")
print("Q2  why group expenses by category")
print("Q3  how do we know a category is over budget")
print("Q4  why use Decimal for money")
print("Q5  what should happen to a negative expense")
print("Q6  how can a report be saved for review")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  store each expense as an ID, category, description and amount")
print("Q2  compare each category's total with its own budget")
print("Q3  remaining budget is negative")
print("Q4  it avoids binary floating-point currency errors")
print("Q5  reject it unless it is an explicit refund type")
print("Q6  export stable CSV expense and budget reports")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - define monthly budgets by category")
print("TASK 2 - validate and normalize expense rows")
print("TASK 3 - summarize spending and remaining budget")
print("TASK 4 - flag a category that is over budget")
print("TASK 5 - reject duplicate IDs and invalid amounts")
print("TASK 6 - export expense and budget reports")
print("TASK 7 - clean up temporary reports")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project74_")
EXPENSE_PATH = os.path.join(WORK, "expenses.csv")
BUDGET_PATH = os.path.join(WORK, "budget-summary.csv")
budgets = {
    "books": Decimal("120.00"),
    "events": Decimal("60.00"),
    "supplies": Decimal("40.00"),
}
raw_expenses = [
    {"expense_id": "X001", "category": "books", "description": "New releases", "amount": "74.50"},
    {"expense_id": "X002", "category": "books", "description": "Reference shelf", "amount": "55.75"},
    {"expense_id": "X003", "category": "events", "description": "Reading night", "amount": "25.00"},
    {"expense_id": "X004", "category": "supplies", "description": "Bookmarks", "amount": "12.40"},
]
expenses = [normalize_expense(row, set(budgets)) for row in raw_expenses]

print("=" * 60)
print("TASK 1 - monthly budget plan")
print("=" * 60)
print("categories ->", ", ".join(sorted(budgets)))
print("total budget -> ${0:.2f}".format(sum(budgets.values())))
print("expense rows ->", len(expenses))
print()

print("=" * 60)
print("TASK 2 - validate expenses")
print("=" * 60)
print("all amounts are Decimal ->", all(isinstance(row["amount"], Decimal) for row in expenses))
print("all expense IDs unique ->", check("unique expense IDs", len({row["expense_id"] for row in expenses}) == len(expenses)))
print("normalized categories ->", ", ".join(sorted({row["category"] for row in expenses})))
print()

print("=" * 60)
print("TASK 3 - summarize each category")
print("=" * 60)
summary = summarize_budget(expenses, budgets)
for category, row in summary.items():
    print("{0}: spent ${1:.2f} / ${2:.2f}, remaining ${3:.2f}".format(
        category, row["spent"], row["budget"], row["remaining"]
    ))
print("total spending -> ${0:.2f}".format(sum(row["spent"] for row in summary.values())))
check("category totals balance", sum(row["spent"] for row in summary.values()) == sum(row["amount"] for row in expenses))
print()

print("=" * 60)
print("TASK 4 - flag overspending")
print("=" * 60)
over_budget = [category for category, row in summary.items() if row["status"] == "over budget"]
print("over-budget categories ->", ", ".join(over_budget))
print("books over budget ->", summary["books"]["status"])
print("events within budget ->", summary["events"]["status"])
check("overspend identified", over_budget == ["books"] and summary["books"]["remaining"] == Decimal("-10.25"))
print()

print("=" * 60)
print("TASK 5 - invalid expenses are rejected")
print("=" * 60)
invalid_rows = [
    {"expense_id": "X005", "category": "unknown", "description": "Other", "amount": "1.00"},
    {"expense_id": "X006", "category": "books", "description": "Bad", "amount": "not money"},
    {"expense_id": "X007", "category": "books", "description": "Negative", "amount": "-1"},
    {"expense_id": "X008", "category": "books", "description": "", "amount": "1"},
]
invalid_messages = []
for row in invalid_rows:
    try:
        normalize_expense(row, set(budgets))
    except ExpenseError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted")
print("invalid cases rejected ->", len([message for message in invalid_messages if message != "accepted"]))
print("reasons ->", " | ".join(invalid_messages))
check("all invalid inputs refused", all(message != "accepted" for message in invalid_messages))
print()

print("=" * 60)
print("TASK 6 - export expense and budget reports")
print("=" * 60)
expense_fields = write_expense_report(EXPENSE_PATH, expenses)
budget_fields = write_budget_report(BUDGET_PATH, summary)
with open(EXPENSE_PATH, "r", encoding="utf-8", newline="") as handle:
    expense_text = handle.read()
with open(BUDGET_PATH, "r", encoding="utf-8", newline="") as handle:
    budget_text = handle.read()
print("expense CSV header ->", expense_text.splitlines()[0])
print("expense rows ->", len(expense_text.splitlines()) - 1)
print("budget CSV header ->", budget_text.splitlines()[0])
print("budget rows ->", len(budget_text.splitlines()) - 1)
print("overspend label exported ->", "over budget" in budget_text)
check("both reports written", len(expense_text.splitlines()) == 5 and len(budget_text.splitlines()) == 4)
check("report schemas include required fields", "amount" in expense_fields and "remaining" in budget_fields)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary budget reports removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
