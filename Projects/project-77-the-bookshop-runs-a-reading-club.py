# ============================================================
# Project 77 - the bookshop runs a shared reading club
# ============================================================
# What this project teaches:
#   reading lists       create an ordered list of book titles
#   membership          add members to a club
#   progress tracking   record each member's completed position
#   validation          reject unknown titles/members and backwards moves
#   completion          calculate percentage and completed lists
#   CSV report          export member progress for the club
#   deterministic data  fixed sample list and members
#   cleanup              generated report is temporary
#
# Everything uses the standard library. No input(), random, network or clock.
#
# Run it:  python project-77-the-bookshop-runs-a-reading-club.py
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


class ReadingClubError(ValueError):
    """Raised when reading-list or member progress data is invalid."""


class ReadingClub:
    """Manage an ordered reading list and member progress."""

    def __init__(self, name, titles):
        normalized = [title.strip() for title in titles]
        if not name.strip() or not normalized or any(not title for title in normalized):
            raise ReadingClubError("club name and nonempty titles are required")
        keys = [title.casefold() for title in normalized]
        if len(keys) != len(set(keys)):
            raise ReadingClubError("reading list contains duplicate titles")
        self.name = name.strip()
        self.titles = normalized
        self.members = {}

    def add_member(self, member_id, name):
        if not member_id.strip() or not name.strip():
            raise ReadingClubError("member ID and name are required")
        if member_id in self.members:
            raise ReadingClubError("member already exists")
        self.members[member_id] = {"name": name.strip(), "completed": 0}

    def mark_read(self, member_id, title):
        """Mark the next book complete; require list order."""
        member = self._get_member(member_id)
        expected_index = member["completed"]
        if expected_index >= len(self.titles):
            raise ReadingClubError("reading list is already complete")
        expected_title = self.titles[expected_index]
        if title.casefold() != expected_title.casefold():
            raise ReadingClubError("next title must be " + expected_title)
        member["completed"] += 1
        return self.progress(member_id)

    def progress(self, member_id):
        member = self._get_member(member_id)
        completed = member["completed"]
        percent = round(completed * 100 / len(self.titles), 1)
        next_title = self.titles[completed] if completed < len(self.titles) else "complete"
        return {"member_id": member_id, "name": member["name"],
                "completed": completed, "total": len(self.titles),
                "percent": percent, "next_title": next_title}

    def _get_member(self, member_id):
        member = self.members.get(member_id)
        if member is None:
            raise ReadingClubError("member not found")
        return member

    def report(self):
        return [self.progress(member_id) for member_id in sorted(self.members)]


def export_progress(path, rows):
    fields = ("member_id", "name", "completed", "total", "percent", "next_title")
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
print("Q1  what does a shared reading list contain")
print("Q2  how can a club track each member's progress")
print("Q3  why might reading order matter")
print("Q4  how is completion percentage calculated")
print("Q5  what happens if a member skips the next title")
print("Q6  how can the club share a progress report")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  an ordered list of book titles")
print("Q2  store the count completed for each member")
print("Q3  the project may require the next listed title")
print("Q4  completed titles divided by total titles")
print("Q5  reject it and explain which title is next")
print("Q6  export member progress as CSV")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - define a shared ordered reading list")
print("TASK 2 - add club members")
print("TASK 3 - mark books read in order")
print("TASK 4 - calculate member completion")
print("TASK 5 - reject skipped titles and unknown members")
print("TASK 6 - export a progress report")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project77_")
REPORT = os.path.join(WORK, "reading-club-progress.csv")
club = ReadingClub("Autumn Reads", ["Dune", "The Hobbit", "Kindred"])
club.add_member("M001", "Amina Saleh")
club.add_member("M002", "Omar Nasser")

print("=" * 60)
print("TASK 1 - reading list")
print("=" * 60)
print("club ->", club.name)
print("titles ->", " -> ".join(club.titles))
print("title count ->", len(club.titles))
print()

print("=" * 60)
print("TASK 2 - member progress starts at zero")
print("=" * 60)
print("members ->", len(club.members))
print("Amina initial progress ->", club.progress("M001")["percent"], "%")
check("members start at zero", all(club.progress(member_id)["completed"] == 0 for member_id in club.members))
print()

print("=" * 60)
print("TASK 3 - record completed titles in order")
print("=" * 60)
progress_one = club.mark_read("M001", "Dune")
progress_two = club.mark_read("M001", "The Hobbit")
print("after one title ->", progress_one["completed"], "of", progress_one["total"])
print("after two titles ->", progress_two["completed"], "of", progress_two["total"])
print("completion percent ->", progress_two["percent"], "%")
print("next title ->", progress_two["next_title"])
check("ordered progress", progress_two["completed"] == 2 and progress_two["percent"] == 66.7 and progress_two["next_title"] == "Kindred")
print()

print("=" * 60)
print("TASK 4 - finish the list")
print("=" * 60)
finished = club.mark_read("M001", "Kindred")
print("completed ->", finished["completed"], "of", finished["total"])
print("completion ->", finished["percent"], "%")
print("next ->", finished["next_title"])
print("finished exactly ->", check("full completion", finished["percent"] == 100.0 and finished["next_title"] == "complete"))
print()

print("=" * 60)
print("TASK 5 - reject invalid progress updates")
print("=" * 60)
try:
    club.mark_read("M002", "The Hobbit")
except ReadingClubError as error:
    skipped_message = str(error)
else:
    skipped_message = "accepted"
try:
    club.mark_read("M999", "Dune")
except ReadingClubError as error:
    unknown_message = str(error)
else:
    unknown_message = "accepted"
print("skipped title ->", skipped_message)
print("unknown member ->", unknown_message)
check("invalid progress refused", skipped_message == "next title must be Dune" and unknown_message == "member not found")
print()

print("=" * 60)
print("TASK 6 - export club progress")
print("=" * 60)
rows = club.report()
fields = export_progress(REPORT, rows)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("member rows ->", len(report_text.splitlines()) - 1)
print("completed member included ->", "Amina Saleh" in report_text and ",100.0,complete" in report_text)
print("next-title field included ->", "next_title" in fields)
check("report includes all members", len(report_text.splitlines()) == len(club.members) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary club report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
