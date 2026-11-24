# ============================================================
# Project 83 - the bookshop turns member requests into acquisitions
# ============================================================
# What this project teaches:
#   member suggestions   collect requested titles and authors
#   deduplication        merge repeated requests for the same title
#   voting               count supporting members and prioritize demand
#   status tracking      requested, approved, ordered or declined
#   purchase planning    choose the highest-demand requests within budget
#   validation           reject unknown members and malformed suggestions
#   CSV export           create a transparent acquisitions report
#   cleanup              temporary report is removed
#
# All fixture data is local and deterministic. No input(), network,
# random or clock is used.
#
# Run it:  python project-83-the-bookshop-manages-acquisition-requests.py
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


class AcquisitionError(ValueError):
    """Raised when an acquisition suggestion is invalid."""


class AcquisitionDesk:
    """Collect suggestions, merge votes and create a budgeted buy list."""

    def __init__(self, members):
        self.members = set(members)
        self.suggestions = {}

    def suggest(self, member_id, title, author, estimated_cost):
        if member_id not in self.members:
            raise AcquisitionError("member not found")
        clean_title = title.strip()
        clean_author = author.strip()
        if not clean_title or not clean_author:
            raise AcquisitionError("title and author are required")
        cost = Decimal(str(estimated_cost)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if cost < 0:
            raise AcquisitionError("estimated cost cannot be negative")
        key = clean_title.casefold()
        row = self.suggestions.get(key)
        if row is None:
            row = {
                "title": clean_title,
                "author": clean_author,
                "estimated_cost": cost,
                "votes": set(),
                "status": "requested",
            }
            self.suggestions[key] = row
        else:
            if row["status"] != "requested":
                raise AcquisitionError("suggestion is no longer open")
        if row["author"].casefold() != clean_author.casefold():
            raise AcquisitionError("title has conflicting authors")
        if member_id in row["votes"]:
            raise AcquisitionError("member already suggested this title")
        row["votes"].add(member_id)
        return self._public_row(row)

    def _public_row(self, row):
        return {
            "title": row["title"],
            "author": row["author"],
            "estimated_cost": row["estimated_cost"],
            "votes": len(row["votes"]),
            "status": row["status"],
        }

    def ranked(self):
        return sorted((self._public_row(row) for row in self.suggestions.values()),
                      key=lambda row: (-row["votes"], row["estimated_cost"], row["title"].casefold()))

    def plan_purchase(self, budget):
        """Select highest-vote books that fit a fixed purchase budget."""
        remaining = Decimal(str(budget)).quantize(Decimal("0.01"))
        if remaining < 0:
            raise AcquisitionError("budget cannot be negative")
        selected = []
        for row in self.ranked():
            cost = row["estimated_cost"]
            if cost <= remaining:
                selected.append(dict(row))
                remaining -= cost
        for item in selected:
            self.suggestions[item["title"].casefold()]["status"] = "approved"
        return selected, remaining


def export_acquisitions(path, rows):
    fields = ("title", "author", "estimated_cost", "votes", "status")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["estimated_cost"] = "{0:.2f}".format(row["estimated_cost"])
            writer.writerow(output)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how can members request a book the shop does not have")
print("Q2  how do repeated requests affect priority")
print("Q3  how can a fixed purchase budget be respected")
print("Q4  why should one member vote only once per title")
print("Q5  what makes an acquisition decision transparent")
print("Q6  how can the approved list be sent to purchasing")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  record a title and author suggestion")
print("Q2  merge the request and count distinct members")
print("Q3  select prioritized titles only while budget remains")
print("Q4  prevent duplicate voting from inflating demand")
print("Q5  preserve vote counts, cost estimates and status")
print("Q6  export a CSV purchasing list")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - define members and initial suggestions")
print("TASK 2 - merge repeated titles and count distinct votes")
print("TASK 3 - reject duplicate votes and conflicting authors")
print("TASK 4 - rank requests by votes then estimated cost")
print("TASK 5 - select a purchase list within budget")
print("TASK 6 - export the decision ledger")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project83_")
REPORT = os.path.join(WORK, "acquisition-requests.csv")
desk = AcquisitionDesk({"M001", "M002", "M003", "M004"})

print("=" * 60)
print("TASK 1 - collect member suggestions")
print("=" * 60)
desk.suggest("M001", "The Left Hand of Darkness", "Ursula K. Le Guin", "14.00")
desk.suggest("M002", "The Left Hand of Darkness", "Ursula K. Le Guin", "14.00")
desk.suggest("M003", "The Left Hand of Darkness", "Ursula K. Le Guin", "14.00")
desk.suggest("M004", "The Left Hand of Darkness", "Ursula K. Le Guin", "14.00")
desk.suggest("M002", "Kindred", "Octavia Butler", "9.50")
desk.suggest("M001", "Parable of the Sower", "Octavia Butler", "12.00")
print("distinct title requests ->", len(desk.suggestions))
print("suggestions collected ->", sum(len(row["votes"]) for row in desk.suggestions.values()))
print()

print("=" * 60)
print("TASK 2 - merge and count votes")
print("=" * 60)
ranked = desk.ranked()
for row in ranked:
    print("{0}: {1} vote(s), estimated ${2:.2f}".format(row["title"], row["votes"], row["estimated_cost"]))
print("top request ->", ranked[0]["title"])
print("repeat requests merged ->", check("duplicate title merged", ranked[0]["votes"] == 4 and len(desk.suggestions) == 3))
print()

print("=" * 60)
print("TASK 3 - prevent duplicate vote and author conflict")
print("=" * 60)
try:
    desk.suggest("M003", "The Left Hand of Darkness", "Ursula K. Le Guin", "14.00")
except AcquisitionError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
try:
    desk.suggest("M003", "Kindred", "Different Author", "9.50")
except AcquisitionError as error:
    author_message = str(error)
else:
    author_message = "accepted"
print("duplicate vote ->", duplicate_message)
print("conflicting author ->", author_message)
check("duplicate and conflict rejected", duplicate_message == "member already suggested this title" and author_message == "title has conflicting authors")
print()

print("=" * 60)
print("TASK 4 - plan purchases within budget")
print("=" * 60)
selected, unspent = desk.plan_purchase("25.00")
print("approved titles ->", ", ".join(row["title"] for row in selected))
print("approved cost -> ${0:.2f}".format(sum((row["estimated_cost"] for row in selected), Decimal("0.00"))))
print("remaining budget -> ${0:.2f}".format(unspent))
print("priority title approved ->", check("top-voted title selected", selected[0]["title"] == "The Left Hand of Darkness"))
print()

print("=" * 60)
print("TASK 5 - export the acquisition decision")
print("=" * 60)
all_rows = desk.ranked()
fields = export_acquisitions(REPORT, all_rows)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("report titles ->", len(report_text.splitlines()) - 1)
print("approved status exported ->", "approved" in report_text)
print("vote counts exported ->", "votes" in fields and ",4," in report_text)
check("report includes every request", len(report_text.splitlines()) == len(all_rows) + 1)
print()

print("=" * 60)
print("TASK 6 - reject invalid suggestions and budgets")
print("=" * 60)
invalid_messages = []
for member, title, author, cost in (
    ("M999", "New Book", "Writer", 5),
    ("M001", "", "Writer", 5),
    ("M001", "Free?", "Writer", -1),
):
    try:
        desk.suggest(member, title, author, cost)
    except AcquisitionError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted")
try:
    desk.plan_purchase(-1)
except AcquisitionError as error:
    budget_message = str(error)
else:
    budget_message = "accepted"
print("invalid suggestion cases ->", invalid_messages)
print("negative budget ->", budget_message)
check("invalid inputs rejected", all(message != "accepted" for message in invalid_messages) and budget_message == "budget cannot be negative")
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary acquisition report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
