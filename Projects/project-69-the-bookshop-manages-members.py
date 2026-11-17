# ============================================================
# Project 69 - the bookshop manages members and loan eligibility
# ============================================================
# What this project teaches:
#   member records       validate IDs, names, status and limits
#   eligibility          allow borrowing only for active members
#   loan limits          enforce a per-member active-loan cap
#   return tracking      close a loan and free a borrowing slot
#   suspension           block new loans while suspended
#   CSV export           produce a member/loan status report
#   deterministic dates  membership states are explicit fixture values
#   cleanup              generated report stays in a temp folder
#
# Everything uses the standard library. No input(), random, network
# or system clock; all scenarios are fixed and repeatable.
#
# Run it:  python project-69-the-bookshop-manages-members.py
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


class MemberError(ValueError):
    """Raised when a member action violates lending policy."""


class MemberDesk:
    """Track members, active loans and lending eligibility."""

    def __init__(self, members, max_active_loans=2):
        if max_active_loans <= 0:
            raise MemberError("loan limit must be positive")
        self.members = {}
        for member in members:
            member_id = member["id"]
            if member_id in self.members:
                raise MemberError("duplicate member ID")
            self.members[member_id] = {
                "id": member_id,
                "name": member["name"].strip(),
                "status": member["status"],
                "active_loans": set(),
            }
        self.max_active_loans = max_active_loans
        self.loan_to_member = {}

    def borrow(self, member_id, loan_id):
        """Record a loan if member is active and under the cap."""
        member = self._get_member(member_id)
        if member["status"] != "active":
            raise MemberError("member is not active")
        if loan_id in self.loan_to_member:
            raise MemberError("loan ID already exists")
        if len(member["active_loans"]) >= self.max_active_loans:
            raise MemberError("active loan limit reached")
        member["active_loans"].add(loan_id)
        self.loan_to_member[loan_id] = member_id
        return len(member["active_loans"])

    def return_loan(self, loan_id):
        """Close a known active loan and release its member slot."""
        member_id = self.loan_to_member.get(loan_id)
        if member_id is None:
            raise MemberError("active loan not found")
        member = self.members[member_id]
        member["active_loans"].remove(loan_id)
        del self.loan_to_member[loan_id]
        return len(member["active_loans"])

    def _get_member(self, member_id):
        member = self.members.get(member_id)
        if member is None:
            raise MemberError("member not found")
        return member

    def report_rows(self):
        """Return one stable report row per member."""
        return [
            {
                "member_id": member_id,
                "name": member["name"],
                "status": member["status"],
                "active_loans": len(member["active_loans"]),
                "loan_limit": self.max_active_loans,
                "available_slots": self.max_active_loans - len(member["active_loans"]),
            }
            for member_id, member in sorted(self.members.items())
        ]


def export_member_report(path, rows):
    fields = ("member_id", "name", "status", "active_loans", "loan_limit", "available_slots")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  who may borrow a book")
print("Q2  how do we enforce a member loan limit")
print("Q3  what happens when a loan is returned")
print("Q4  can a suspended member borrow")
print("Q5  how do we report a member's available loan slots")
print("Q6  why should member IDs be unique")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  an active member")
print("Q2  count active loans before creating a new one")
print("Q3  remove it from active loans and release one slot")
print("Q4  no")
print("Q5  loan limit minus active loans")
print("Q6  loans and reports must identify one member unambiguously")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - register active, suspended and expired members")
print("TASK 2 - allow an eligible member to borrow")
print("TASK 3 - enforce the active-loan limit")
print("TASK 4 - return a loan and free a slot")
print("TASK 5 - block suspended, expired and unknown members")
print("TASK 6 - export a member eligibility report")
print("TASK 7 - clean up the CSV file")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project69_")
REPORT = os.path.join(WORK, "member-eligibility.csv")
desk = MemberDesk([
    {"id": "M001", "name": "Amina Saleh", "status": "active"},
    {"id": "M002", "name": "Omar Nasser", "status": "suspended"},
    {"id": "M003", "name": "Lina Haddad", "status": "expired"},
], max_active_loans=2)

print("=" * 60)
print("TASK 1 - member directory")
print("=" * 60)
print("members ->", len(desk.members))
print("active members ->", sum(member["status"] == "active" for member in desk.members.values()))
print("loan limit ->", desk.max_active_loans)
check("members registered", len(desk.members) == 3)
print()

print("=" * 60)
print("TASK 2 - an active member borrows")
print("=" * 60)
active_count = desk.borrow("M001", "L100")
print("active loans after first borrow ->", active_count)
print("available slots ->", desk.max_active_loans - active_count)
check("active member allowed", active_count == 1)
print()

print("=" * 60)
print("TASK 3 - enforce the loan cap")
print("=" * 60)
desk.borrow("M001", "L101")
try:
    desk.borrow("M001", "L102")
except MemberError as error:
    cap_message = str(error)
else:
    cap_message = "accepted"
print("third loan ->", cap_message)
print("active loans remain capped ->", check("loan cap enforced", len(desk.members["M001"]["active_loans"]) == 2))
print()

print("=" * 60)
print("TASK 4 - return a loan and borrow again")
print("=" * 60)
remaining = desk.return_loan("L100")
new_count = desk.borrow("M001", "L102")
print("loans after return ->", remaining)
print("loans after next borrow ->", new_count)
print("slot reused ->", check("return frees slot", remaining == 1 and new_count == 2))
print()

print("=" * 60)
print("TASK 5 - block ineligible members")
print("=" * 60)
messages = []
for member_id, loan_id in (("M002", "L200"), ("M003", "L300"), ("M999", "L900")):
    try:
        desk.borrow(member_id, loan_id)
    except MemberError as error:
        messages.append(str(error))
    else:
        messages.append("accepted")
print("suspended member ->", messages[0])
print("expired member ->", messages[1])
print("unknown member ->", messages[2])
check("ineligible members refused", messages == ["member is not active", "member is not active", "member not found"])
print()

print("=" * 60)
print("TASK 6 - member availability report")
print("=" * 60)
rows = desk.report_rows()
for row in rows:
    print("{0}: {1}, active {2}/{3}, slots {4}".format(
        row["name"], row["status"], row["active_loans"], row["loan_limit"], row["available_slots"]
    ))
print("report rows ->", len(rows))
check("active loan count is reported", rows[0]["active_loans"] == 2)
print()

print("=" * 60)
print("TASK 7 - export CSV")
print("=" * 60)
fields = export_member_report(REPORT, rows)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("CSV members ->", len(report_text.splitlines()) - 1)
print("availability field included ->", "available_slots" in fields)
print("suspended status exported ->", "suspended" in report_text)
check("CSV includes all members", len(report_text.splitlines()) == len(rows) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary member report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
