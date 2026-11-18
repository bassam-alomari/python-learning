# ============================================================
# Project 71 - the bookshop books study rooms without conflicts
# ============================================================
# What this project teaches:
#   room capacity      reject a booking larger than the room
#   time intervals     prevent overlapping reservations
#   half-open ranges   adjacent bookings may meet at an endpoint
#   cancellation       close a booking and release the time slot
#   deterministic sort list the day's schedule by room and start
#   CSV report         export confirmed/cancelled bookings
#   validation         reject invalid times, rooms and attendees
#   cleanup            generated schedule report is temporary
#
# This extends the library/bookshop system into study-room operations.
# It uses fixed dates and times; no input(), network or wall clock.
#
# Run it:  python project-71-the-bookshop-books-study-rooms.py
# ============================================================

import csv
import os
import shutil
import tempfile
from datetime import datetime

CHECKS = []


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class BookingError(ValueError):
    """Raised when a room booking is invalid or conflicts."""


class RoomDesk:
    """Manage room capacities and non-overlapping bookings."""

    def __init__(self, rooms):
        self.rooms = {room["room_id"]: dict(room) for room in rooms}
        self.bookings = []
        self.next_id = 1

    @staticmethod
    def _parse(value):
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except (TypeError, ValueError):
            raise BookingError("time must use YYYY-MM-DD HH:MM")

    def book(self, room_id, organizer, start, end, attendees):
        """Create a booking if capacity and time rules allow."""
        room = self.rooms.get(room_id)
        if room is None:
            raise BookingError("room not found")
        if not isinstance(attendees, int) or attendees <= 0:
            raise BookingError("attendees must be a positive integer")
        if attendees > room["capacity"]:
            raise BookingError("room capacity exceeded")
        if not organizer.strip():
            raise BookingError("organizer is required")
        start_dt, end_dt = self._parse(start), self._parse(end)
        if end_dt <= start_dt:
            raise BookingError("end must be after start")
        for booking in self.bookings:
            if booking["room_id"] != room_id or booking["status"] != "confirmed":
                continue
            old_start = self._parse(booking["start"])
            old_end = self._parse(booking["end"])
            if start_dt < old_end and old_start < end_dt:
                raise BookingError("room time conflict")
        booking = {
            "booking_id": "B{0:03d}".format(self.next_id),
            "room_id": room_id,
            "room_name": room["name"],
            "organizer": organizer.strip(),
            "start": start,
            "end": end,
            "attendees": attendees,
            "status": "confirmed",
        }
        self.next_id += 1
        self.bookings.append(booking)
        return dict(booking)

    def cancel(self, booking_id):
        """Cancel a confirmed booking and release its interval."""
        booking = next((row for row in self.bookings if row["booking_id"] == booking_id), None)
        if booking is None:
            raise BookingError("booking not found")
        if booking["status"] != "confirmed":
            raise BookingError("booking is not confirmed")
        booking["status"] = "cancelled"
        return dict(booking)

    def schedule(self):
        """Return bookings sorted by room, start, and ID."""
        return sorted(self.bookings,
                      key=lambda row: (row["room_id"], row["start"], row["booking_id"]))


def export_schedule(path, bookings):
    fields = ("booking_id", "room_id", "room_name", "organizer", "start", "end", "attendees", "status")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row[field] for field in fields} for row in bookings)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what should be checked before confirming a room")
print("Q2  how do we detect overlapping times")
print("Q3  may one booking end when another begins")
print("Q4  what happens when a booking is cancelled")
print("Q5  how do we keep a stable daily schedule")
print("Q6  how can staff share the room bookings")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  room exists, attendee count fits, and times are valid")
print("Q2  intervals overlap if each begins before the other ends")
print("Q3  yes, intervals are half-open: [start, end)")
print("Q4  its slot becomes available again")
print("Q5  sort by room, start time and booking ID")
print("Q6  export the schedule to CSV")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - define rooms with capacities")
print("TASK 2 - book valid, non-overlapping intervals")
print("TASK 3 - reject over-capacity and overlapping requests")
print("TASK 4 - allow adjacent bookings")
print("TASK 5 - cancel a booking and reuse the slot")
print("TASK 6 - sort the schedule deterministically")
print("TASK 7 - export bookings as CSV")
print("TASK 8 - clean up the temporary report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project71_")
REPORT = os.path.join(WORK, "room-schedule.csv")
desk = RoomDesk([
    {"room_id": "R1", "name": "Reading Room", "capacity": 4},
    {"room_id": "R2", "name": "Study Room", "capacity": 2},
])

print("=" * 60)
print("TASK 1 - room directory")
print("=" * 60)
print("rooms ->", len(desk.rooms))
print("Reading Room capacity ->", desk.rooms["R1"]["capacity"])
print()

print("=" * 60)
print("TASK 2 - confirm bookings")
print("=" * 60)
b1 = desk.book("R1", "Amina", "2026-11-20 09:00", "2026-11-20 10:00", 3)
b2 = desk.book("R1", "Omar", "2026-11-20 10:00", "2026-11-20 11:00", 4)
print("first booking ->", b1["booking_id"], b1["status"])
print("adjacent booking ->", b2["booking_id"], b2["status"])
print("adjacent slots allowed ->", check("endpoint adjacency", len(desk.bookings) == 2))
print()

print("=" * 60)
print("TASK 3 - reject capacity and overlap")
print("=" * 60)
try:
    desk.book("R2", "Lina", "2026-11-20 09:00", "2026-11-20 10:00", 3)
except BookingError as error:
    capacity_message = str(error)
else:
    capacity_message = "accepted"
try:
    desk.book("R1", "Mina", "2026-11-20 09:30", "2026-11-20 10:30", 1)
except BookingError as error:
    conflict_message = str(error)
else:
    conflict_message = "accepted"
print("over capacity ->", capacity_message)
print("overlapping time ->", conflict_message)
check("invalid booking constraints enforced", capacity_message == "room capacity exceeded" and conflict_message == "room time conflict")
print()

print("=" * 60)
print("TASK 4 - cancel and reuse a slot")
print("=" * 60)
cancelled = desk.cancel(b1["booking_id"])
reused = desk.book("R1", "Mina", "2026-11-20 09:15", "2026-11-20 09:45", 2)
print("cancelled status ->", cancelled["status"])
print("reused slot ->", reused["booking_id"], reused["status"])
print("cancel releases slot ->", check("cancelled interval reusable", reused["status"] == "confirmed"))
print()

print("=" * 60)
print("TASK 5 - invalid times and unknown rooms")
print("=" * 60)
invalid_messages = []
for room_id, start, end in (
    ("R9", "2026-11-20 09:00", "2026-11-20 10:00"),
    ("R2", "2026-11-20 11:00", "2026-11-20 10:00"),
    ("R2", "not a date", "2026-11-20 12:00"),
):
    try:
        desk.book(room_id, "Tester", start, end, 1)
    except BookingError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted")
print("invalid requests ->", invalid_messages)
check("invalid requests rejected", all(message != "accepted" for message in invalid_messages))
print()

print("=" * 60)
print("TASK 6 - deterministic schedule")
print("=" * 60)
schedule = desk.schedule()
print("schedule order ->", ", ".join(row["booking_id"] for row in schedule))
print("schedule sorted ->", check("schedule key order", schedule == sorted(schedule, key=lambda row: (row["room_id"], row["start"], row["booking_id"]))))
print("confirmed bookings ->", sum(row["status"] == "confirmed" for row in schedule))
print()

print("=" * 60)
print("TASK 7 - export CSV")
print("=" * 60)
fields = export_schedule(REPORT, schedule)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("CSV booking rows ->", len(report_text.splitlines()) - 1)
print("status field included ->", "status" in fields)
print("cancelled record exported ->", "cancelled" in report_text)
check("all schedule rows exported", len(report_text.splitlines()) == len(schedule) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary schedule removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
