# ============================================================
# Project 72 - the bookshop manages event attendance
# ============================================================
# What this project teaches:
#   event capacity       prevent attendance above room limits
#   registration         one active registration per member/event
#   waitlist             queue members when an event is full
#   cancellation         free a seat and promote the first waiter
#   state transitions   distinguish registered, waiting and cancelled
#   CSV report           export attendance and waitlist records
#   validation           reject unknown events and members
#   cleanup              report file is temporary
#
# Everything uses the standard library and fixed fixtures. No input(),
# random, network or clock is used.
#
# Run it:  python project-72-the-bookshop-manages-event-attendance.py
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


class EventError(ValueError):
    """Raised when event registration data is invalid."""


class EventDesk:
    """Manage events, confirmed seats and FIFO waitlists."""

    def __init__(self, events, members):
        self.events = {event["event_id"]: {
            "title": event["title"],
            "capacity": event["capacity"],
            "registrations": [],
            "waitlist": [],
        } for event in events}
        self.members = set(members)
        self.next_id = 1
        for event in self.events.values():
            if not isinstance(event["capacity"], int) or event["capacity"] <= 0:
                raise EventError("event capacity must be positive")

    def register(self, event_id, member_id):
        """Register a member or enqueue them when the event is full."""
        event = self._get_event(event_id)
        if member_id not in self.members:
            raise EventError("member not found")
        if any(row["member_id"] == member_id and row["status"] in ("registered", "waiting")
               for row in event["registrations"]):
            raise EventError("member already registered or waiting")
        status = "registered" if len(event["registrations"]) < event["capacity"] else "waiting"
        registration = {
            "registration_id": "E{0:03d}".format(self.next_id),
            "event_id": event_id,
            "member_id": member_id,
            "status": status,
        }
        self.next_id += 1
        event["registrations"].append(registration)
        if status == "waiting":
            event["waitlist"].append(registration["registration_id"])
        return dict(registration)

    def cancel(self, event_id, member_id):
        """Cancel a registration and promote the first waiter if a seat opens."""
        event = self._get_event(event_id)
        registration = next((row for row in event["registrations"]
                             if row["member_id"] == member_id
                             and row["status"] in ("registered", "waiting")), None)
        if registration is None:
            raise EventError("active registration not found")
        was_registered = registration["status"] == "registered"
        registration["status"] = "cancelled"
        promoted = None
        if was_registered and event["waitlist"]:
            next_id = event["waitlist"].pop(0)
            promoted = next(row for row in event["registrations"]
                            if row["registration_id"] == next_id)
            promoted["status"] = "registered"
        elif not was_registered:
            event["waitlist"].remove(registration["registration_id"])
        return dict(registration), dict(promoted) if promoted else None

    def _get_event(self, event_id):
        event = self.events.get(event_id)
        if event is None:
            raise EventError("event not found")
        return event

    def report_rows(self):
        rows = []
        for event_id in sorted(self.events):
            event = self.events[event_id]
            for registration in event["registrations"]:
                rows.append({
                    "event_id": event_id,
                    "event_title": event["title"],
                    "registration_id": registration["registration_id"],
                    "member_id": registration["member_id"],
                    "status": registration["status"],
                })
        return rows


def export_attendance(path, rows):
    fields = ("event_id", "event_title", "registration_id", "member_id", "status")
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
print("Q1  what happens when an event reaches capacity")
print("Q2  how should waitlisted members be ordered")
print("Q3  what happens when a registered member cancels")
print("Q4  how do we prevent one member registering twice")
print("Q5  what should happen when no one is waiting")
print("Q6  how can staff review attendance and waitlists")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  later registrations join the waitlist")
print("Q2  first-in, first-out")
print("Q3  promote the earliest waiter into the open seat")
print("Q4  reject duplicate active registrations")
print("Q5  leave the seat open")
print("Q6  export all registration states to CSV")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - create capacity-limited events and members")
print("TASK 2 - register attendees until full")
print("TASK 3 - put additional attendees on a waitlist")
print("TASK 4 - cancel a seat holder and promote FIFO waiter")
print("TASK 5 - reject duplicate, unknown and invalid actions")
print("TASK 6 - cancel a waitlisted registration")
print("TASK 7 - export all attendance records to CSV")
print("TASK 8 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project72_")
REPORT = os.path.join(WORK, "event-attendance.csv")
desk = EventDesk(
    [{"event_id": "EV1", "title": "Python Evening", "capacity": 2},
     {"event_id": "EV2", "title": "Book Club", "capacity": 1},
     {"event_id": "EV3", "title": "Data Night", "capacity": 1}],
    members=("M001", "M002", "M003", "M004"),
)

print("=" * 60)
print("TASK 1 - event capacity")
print("=" * 60)
print("events ->", len(desk.events))
print("Python Evening capacity ->", desk.events["EV1"]["capacity"])
print("members ->", len(desk.members))
print()

print("=" * 60)
print("TASK 2 - register until full")
print("=" * 60)
r1 = desk.register("EV1", "M001")
r2 = desk.register("EV1", "M002")
r3 = desk.register("EV1", "M003")
r4 = desk.register("EV1", "M004")
print("first registration ->", r1["status"])
print("second registration ->", r2["status"])
print("third registration ->", r3["status"])
print("fourth registration ->", r4["status"])
print("waitlist order ->", [row["member_id"] for row in desk.events["EV1"]["registrations"] if row["status"] == "waiting"])
print()

print("=" * 60)
print("TASK 3 - duplicate and unknown checks")
print("=" * 60)
try:
    desk.register("EV1", "M003")
except EventError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
try:
    desk.register("EV9", "M004")
except EventError as error:
    unknown_message = str(error)
else:
    unknown_message = "accepted"
print("duplicate registration ->", duplicate_message)
print("unknown event ->", unknown_message)
check("invalid registrations refused", duplicate_message == "member already registered or waiting" and unknown_message == "event not found")
print()

print("=" * 60)
print("TASK 4 - cancel and promote FIFO")
print("=" * 60)
cancelled, promoted = desk.cancel("EV1", "M001")
print("cancelled status ->", cancelled["status"])
print("promoted member ->", promoted["member_id"])
print("promoted status ->", promoted["status"])
print("next waiter remains ->", next(row["member_id"] for row in desk.events["EV1"]["registrations"] if row["status"] == "waiting"))
check("FIFO promotion", promoted["member_id"] == "M003" and next(row["member_id"] for row in desk.events["EV1"]["registrations"] if row["status"] == "waiting") == "M004")
print()

print("=" * 60)
print("TASK 5 - empty a waitlist")
print("=" * 60)
_, promoted_second = desk.cancel("EV1", "M002")
print("second cancellation promoted ->", promoted_second["member_id"] if promoted_second else "none")
print("remaining waitlist ->", len(desk.events["EV1"]["waitlist"]))
print("all queued members assigned ->", check("waitlist drains", not desk.events["EV1"]["waitlist"]))
print()

print("=" * 60)
print("TASK 6 - cancel a waiting record")
print("=" * 60)
r5 = desk.register("EV2", "M001")
r6 = desk.register("EV2", "M002")
waiting_cancelled, no_promotion = desk.cancel("EV2", "M002")
print("waiting cancellation ->", waiting_cancelled["status"])
print("no promotion without open seat ->", no_promotion is None)
print("waitlist cleared ->", desk.events["EV2"]["waitlist"] == [])
seat_holder = desk.register("EV3", "M001")
waiting_member = desk.register("EV3", "M002")
print("full event second registration ->", waiting_member["status"])
print()

print("=" * 60)
print("TASK 7 - export attendance ledger")
print("=" * 60)
rows = desk.report_rows()
fields = export_attendance(REPORT, rows)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("registration rows ->", len(report_text.splitlines()) - 1)
print("waiting status retained ->", "waiting" in report_text)
check("CSV retains waiting state", "waiting" in report_text)
print("cancelled status retained ->", "cancelled" in report_text)
print("status column present ->", "status" in fields)
check("CSV exports all records", len(report_text.splitlines()) == len(rows) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary attendance report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
