# ============================================================
# Project 67 - the bookshop renews memberships and flags expiry
# ============================================================
# What this project teaches:
#   membership status   active, expiring soon, expired
#   date arithmetic     days remaining from a fixed reference date
#   renewals            extend from the later of today or current expiry
#   idempotency         prevent two renewals in one processing batch
#   validation          reject unknown members and invalid periods
#   CSV report          export member status and expiry dates
#   deterministic data fixed date; no system clock is read
#   cleanup             temporary member report is removed
#
# Everything uses the standard library, no input(), random, network or clock.
#
# Run it:  python project-67-the-bookshop-renews-memberships.py
# ============================================================

import csv
import os
import shutil
import tempfile
from datetime import date, timedelta

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class MembershipError(ValueError):
    """Raised when membership data or renewal is invalid."""


def membership_status(expiry, today, warning_days=14):
    """Classify membership relative to an explicit date."""
    if expiry < today:
        return "expired"
    days_left = (expiry - today).days
    if days_left <= warning_days:
        return "expiring soon"
    return "active"


class MembershipDesk:
    """Renew memberships and produce status reports."""

    def __init__(self, members, term_days=365):
        if not isinstance(term_days, int) or term_days <= 0:
            raise MembershipError("membership term must be positive days")
        self.members = {member["id"]: dict(member) for member in members}
        self.term_days = term_days
        self.renewed_in_batch = set()

    def status(self, member_id, today):
        member = self._member(member_id)
        return membership_status(member["expiry"], today)

    def renew(self, member_id, today):
        """Extend from current expiry if valid, otherwise from today."""
        member = self._member(member_id)
        if member_id in self.renewed_in_batch:
            raise MembershipError("member already renewed in this batch")
        base = max(member["expiry"], today)
        member["expiry"] = base + timedelta(days=self.term_days)
        member["renewals"] += 1
        self.renewed_in_batch.add(member_id)
        return member["expiry"]

    def _member(self, member_id):
        if member_id not in self.members:
            raise MembershipError("member not found")
        return self.members[member_id]

    def rows(self, today):
        """Return stable member rows with current status and days left."""
        result = []
        for member_id in sorted(self.members):
            member = self.members[member_id]
            days_left = (member["expiry"] - today).days
            result.append({
                "member_id": member_id,
                "name": member["name"],
                "expiry": member["expiry"].isoformat(),
                "days_left": days_left,
                "status": membership_status(member["expiry"], today),
                "renewals": member["renewals"],
            })
        return result


def export_members(path, rows):
    fields = ("member_id", "name", "expiry", "days_left", "status", "renewals")
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
print("Q1  how can we tell whether a membership is expired")
print("Q2  when should we warn that renewal is near")
print("Q3  from which date should an early renewal extend")
print("Q4  how do we avoid renewing a member twice in one batch")
print("Q5  why should a test use an explicit date")
print("Q6  how can staff review expiry status")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  compare its expiry date with today")
print("Q2  when days remaining are within the warning window")
print("Q3  from the later of today and the existing expiry")
print("Q4  track member IDs already renewed in this batch")
print("Q5  a fixed date makes each run repeatable")
print("Q6  export member status and expiry to CSV")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - create members with different expiry dates")
print("TASK 2 - classify active, expiring and expired members")
print("TASK 3 - renew one member using a fixed term")
print("TASK 4 - reject a duplicate renewal in the batch")
print("TASK 5 - reject unknown members")
print("TASK 6 - export the member status report")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project67_")
REPORT = os.path.join(WORK, "membership-status.csv")
TODAY = date(2026, 6, 1)
desk = MembershipDesk([
    {"id": "M001", "name": "Amina Saleh", "expiry": date(2026, 6, 8), "renewals": 0},
    {"id": "M002", "name": "Omar Nasser", "expiry": date(2026, 5, 20), "renewals": 1},
    {"id": "M003", "name": "Lina Haddad", "expiry": date(2027, 1, 1), "renewals": 2},
], term_days=365)

print("=" * 60)
print("TASK 1 - member records")
print("=" * 60)
print("members ->", len(desk.members))
print("reference date ->", TODAY.isoformat())
print("membership term ->", desk.term_days, "days")
print()

print("=" * 60)
print("TASK 2 - classify membership status")
print("=" * 60)
for member_id in sorted(desk.members):
    member = desk.members[member_id]
    print("{0}: {1}".format(member["name"], desk.status(member_id, TODAY)))
check("all three statuses represented", {desk.status(mid, TODAY) for mid in desk.members} == {"active", "expiring soon", "expired"})
print()

print("=" * 60)
print("TASK 3 - renew a membership")
print("=" * 60)
new_expiry = desk.renew("M001", TODAY)
print("renewed member ->", desk.members["M001"]["name"])
print("new expiry ->", new_expiry.isoformat())
print("renewal count ->", desk.members["M001"]["renewals"])
check("renewal extends from old expiry", new_expiry == date(2027, 6, 8))
print()

print("=" * 60)
print("TASK 4 - renewal batch guard")
print("=" * 60)
try:
    desk.renew("M001", TODAY)
except MembershipError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
print("second renewal ->", duplicate_message)
print("expiry unchanged after duplicate ->", check("duplicate renewal blocked", desk.members["M001"]["expiry"] == date(2027, 6, 8)))
print()

print("=" * 60)
print("TASK 5 - unknown member")
print("=" * 60)
try:
    desk.renew("M999", TODAY)
except MembershipError as error:
    unknown_message = str(error)
else:
    unknown_message = "accepted"
print("unknown ID ->", unknown_message)
print("unknown member rejected ->", check("unknown member blocked", unknown_message == "member not found"))
print()

print("=" * 60)
print("TASK 6 - export expiry report")
print("=" * 60)
rows = desk.rows(TODAY)
fields = export_members(REPORT, rows)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("member rows ->", len(report_text.splitlines()) - 1)
print("status field included ->", "status" in fields)
print("renewed date exported ->", "2027-06-08" in report_text)
check("all member rows exported", len(report_text.splitlines()) == len(desk.members) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary membership report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
