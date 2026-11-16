# ============================================================
# Project 66 - the bookshop manages a fair reservation queue
# ============================================================
# What this project teaches:
#   reservations       queue members waiting for an unavailable title
#   FIFO policy       serve the earliest reservation first
#   copy arrival      promote the next waiting member when stock returns
#   cancellation      remove a member's active reservation safely
#   duplicate guard   one active reservation per member/title
#   status tracking   distinguish waiting, ready and cancelled records
#   CSV export        save the queue for staff review
#   cleanup           all report files stay in a temp folder
#
# This continues projects 64-65's lending workflow. Everything is
# deterministic and local; no input(), network, random or clock.
#
# Run it:  python project-66-the-bookshop-manages-reservation-queues.py
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


class QueueError(ValueError):
    """Raised when a reservation queue operation is invalid."""


class ReservationQueue:
    """Maintain a FIFO waitlist per title."""

    def __init__(self, titles):
        self.titles = {title.casefold(): title for title in titles}
        self.records = []
        self.next_id = 1

    def reserve(self, title, member):
        """Add a member to a known title's queue."""
        key = title.casefold()
        if key not in self.titles:
            raise QueueError("book not found")
        if not member.strip():
            raise QueueError("member name is required")
        duplicate = any(
            row["title"].casefold() == key
            and row["member"].casefold() == member.casefold()
            and row["status"] in ("waiting", "ready")
            for row in self.records
        )
        if duplicate:
            raise QueueError("member already has an active reservation")
        reservation_id = "Q{0:03d}".format(self.next_id)
        self.next_id += 1
        row = {"id": reservation_id, "title": self.titles[key],
               "member": member.strip(), "status": "waiting"}
        self.records.append(row)
        return dict(row)

    def queue_for(self, title):
        """Return active reservations in FIFO order."""
        key = title.casefold()
        return [row for row in self.records
                if row["title"].casefold() == key
                and row["status"] == "waiting"]

    def copy_returned(self, title):
        """Mark the next waiting member ready for pickup."""
        queue = self.queue_for(title)
        if not queue:
            return None
        queue[0]["status"] = "ready"
        return dict(queue[0])

    def cancel(self, reservation_id):
        """Cancel an active waiting or ready reservation."""
        row = next((item for item in self.records if item["id"] == reservation_id), None)
        if row is None:
            raise QueueError("reservation not found")
        if row["status"] not in ("waiting", "ready"):
            raise QueueError("reservation is already closed")
        row["status"] = "cancelled"
        return dict(row)

    def collect(self, reservation_id):
        """Close a ready reservation when the member collects the book."""
        row = next((item for item in self.records if item["id"] == reservation_id), None)
        if row is None:
            raise QueueError("reservation not found")
        if row["status"] != "ready":
            raise QueueError("reservation is not ready")
        row["status"] = "collected"
        return dict(row)


def export_queue(path, records):
    """Write reservation history with a stable header."""
    fields = ("id", "title", "member", "status")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row[field] for field in fields} for row in records)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how should a waitlist order members")
print("Q2  who gets offered a returned copy first")
print("Q3  how do we stop a member joining the same queue twice")
print("Q4  what happens when a reservation is cancelled")
print("Q5  what does ready mean")
print("Q6  how can staff review the reservation history")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  first-in, first-out")
print("Q2  the earliest waiting member")
print("Q3  reject a second active reservation for that title/member")
print("Q4  close it without disturbing other members")
print("Q5  a copy has been assigned and is ready for pickup")
print("Q6  export the queue to CSV")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - create queues for known titles")
print("TASK 2 - reserve a title in FIFO order")
print("TASK 3 - prevent duplicate active reservations")
print("TASK 4 - assign a returned copy to the next member")
print("TASK 5 - cancel or collect reservations")
print("TASK 6 - reject invalid transitions")
print("TASK 7 - export reservation history to CSV")
print("TASK 8 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project66_")
REPORT = os.path.join(WORK, "reservation-queue.csv")
waitlist = ReservationQueue(["Dune", "Neuromancer"])

print("=" * 60)
print("TASK 1 - create a waitlist")
print("=" * 60)
first = waitlist.reserve("Dune", "Amina")
second = waitlist.reserve("Dune", "Omar")
third = waitlist.reserve("Dune", "Mina")
print("reservation IDs ->", ", ".join(row["id"] for row in (first, second, third)))
print("queue order ->", " -> ".join(row["member"] for row in waitlist.queue_for("Dune")))
check("FIFO queue order", [row["member"] for row in waitlist.queue_for("Dune")] == ["Amina", "Omar", "Mina"])
print()

print("=" * 60)
print("TASK 2 - reject a duplicate active reservation")
print("=" * 60)
try:
    waitlist.reserve("dUnE", "Amina")
except QueueError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
print("duplicate result ->", duplicate_message)
print("queue length unchanged ->", check("duplicate prevented", len(waitlist.queue_for("Dune")) == 3))
print()

print("=" * 60)
print("TASK 3 - returned copies follow FIFO")
print("=" * 60)
ready_first = waitlist.copy_returned("Dune")
print("first pickup ->", ready_first["member"])
print("first status ->", ready_first["status"])
ready_second = waitlist.copy_returned("Dune")
print("second pickup ->", ready_second["member"])
print("next waiting member ->", waitlist.queue_for("Dune")[0]["member"])
print("ready assignments preserve FIFO ->", check("FIFO promotion", [ready_first["member"], ready_second["member"]] == ["Amina", "Omar"]))
print()

print("=" * 60)
print("TASK 4 - collect and cancel")
print("=" * 60)
collected = waitlist.collect(first["id"])
cancelled = waitlist.cancel(third["id"])
print("collected status ->", collected["status"])
print("cancelled status ->", cancelled["status"])
print("remaining waiting ->", len(waitlist.queue_for("Dune")))
check("states recorded", collected["status"] == "collected" and cancelled["status"] == "cancelled")
print()

print("=" * 60)
print("TASK 5 - invalid transitions are rejected")
print("=" * 60)
print("TASK 5 - invalid transitions are rejected")
print("=" * 60)
try:
    waitlist.collect(third["id"])
except QueueError as error:
    not_ready_message = str(error)
else:
    not_ready_message = "accepted"
try:
    waitlist.cancel(third["id"])
except QueueError as error:
    closed_message = str(error)
else:
    closed_message = "accepted"
print("collect cancelled reservation ->", not_ready_message)
print("cancel closed reservation ->", closed_message)
check("invalid transitions rejected", not_ready_message == "reservation is not ready" and closed_message == "reservation is already closed")
print()

print("=" * 60)
print("TASK 6 - unknown titles and empty queues")
print("=" * 60)
try:
    waitlist.reserve("Foundation", "Ari")
except QueueError as error:
    unknown_title_message = str(error)
else:
    unknown_title_message = "accepted"
no_waiter = waitlist.copy_returned("Neuromancer")
print("unknown title ->", unknown_title_message)
print("empty queue result ->", no_waiter)
check("unknown title refused", unknown_title_message == "book not found")
check("empty queue is safe", no_waiter is None)
print()

print("=" * 60)
print("TASK 7 - export the queue ledger")
print("=" * 60)
fields = export_queue(REPORT, waitlist.records)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("history rows ->", len(report_text.splitlines()) - 1)
print("status column included ->", "status" in fields)
print("collected state exported ->", "collected" in report_text)
check("all queue records exported", len(report_text.splitlines()) == len(waitlist.records) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary queue report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
