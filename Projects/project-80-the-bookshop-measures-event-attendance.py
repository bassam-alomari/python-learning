# ============================================================
# Project 80 - the bookshop measures event attendance
# ============================================================
# What this project teaches:
#   capacity use       compare attendees with event capacity
#   attendance rate    calculate check-ins / registrations
#   no-show tracking   distinguish cancelled and absent guests
#   revenue summary    total ticket income per event
#   aggregation        summarize multiple events deterministically
#   validation         reject duplicate IDs and impossible counts
#   CSV reporting      export event-level metrics
#   cleanup            generated report stays in a temporary folder
#
# Everything uses the standard library and fixed records. No input(),
# random, network or clock.
#
# Run it:  python project-80-the-bookshop-measures-event-attendance.py
# ============================================================

import csv
import os
import shutil
import tempfile
from decimal import Decimal, ROUND_HALF_UP

CHECKS = []
CENT = Decimal("0.01")


def check(name, condition):
    """A claim this project is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class EventReportError(ValueError):
    """Raised when event attendance records are invalid."""


def summarize_event(event):
    required = ("event_id", "title", "capacity", "ticket_price", "registrations")
    missing = [key for key in required if key not in event]
    if missing:
        raise EventReportError("missing fields: " + ", ".join(missing))
    capacity = event["capacity"]
    if not isinstance(capacity, int) or capacity <= 0:
        raise EventReportError("capacity must be a positive integer")
    price = Decimal(str(event["ticket_price"])).quantize(CENT, rounding=ROUND_HALF_UP)
    registrations = event["registrations"]
    if not isinstance(registrations, list):
        raise EventReportError("registrations must be a list")
    seen = set()
    checked_in = 0
    cancelled = 0
    no_show = 0
    for registration in registrations:
        if "registration_id" not in registration or "status" not in registration:
            raise EventReportError("registration is missing fields")
        registration_id = registration["registration_id"]
        if registration_id in seen:
            raise EventReportError("duplicate registration ID")
        seen.add(registration_id)
        status = registration["status"]
        if status not in ("checked-in", "cancelled", "no-show"):
            raise EventReportError("unknown registration status")
        checked_in += status == "checked-in"
        cancelled += status == "cancelled"
        no_show += status == "no-show"
    if len(registrations) > capacity:
        raise EventReportError("registrations exceed capacity")
    attendance_rate = round(checked_in * 100 / len(registrations), 1) if registrations else 0.0
    return {
        "event_id": event["event_id"],
        "title": event["title"],
        "capacity": capacity,
        "registrations": len(registrations),
        "checked_in": checked_in,
        "cancelled": cancelled,
        "no_show": no_show,
        "attendance_rate": attendance_rate,
        "revenue": (price * checked_in).quantize(CENT),
    }


def write_event_report(path, summaries):
    fields = ("event_id", "title", "capacity", "registrations", "checked_in",
              "cancelled", "no_show", "attendance_rate", "revenue")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in summaries:
            output = dict(row)
            output["attendance_rate"] = "{0:.1f}".format(row["attendance_rate"])
            output["revenue"] = "{0:.2f}".format(row["revenue"])
            writer.writerow(output)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  how many registered guests actually attended")
print("Q2  what fraction of registrations checked in")
print("Q3  how many guests cancelled or did not arrive")
print("Q4  how much ticket revenue did an event collect")
print("Q5  how do we compare several events consistently")
print("Q6  what data errors should a report reject")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  count check-in statuses")
print("Q2  checked-in divided by total registrations")
print("Q3  count cancelled and no-show statuses separately")
print("Q4  ticket price times checked-in guests")
print("Q5  use the same summary function for every event")
print("Q6  duplicate IDs, unknown statuses and over-capacity data")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - prepare several fixed event records")
print("TASK 2 - summarize attendance and capacity")
print("TASK 3 - calculate check-in rate and no-shows")
print("TASK 4 - calculate revenue from attended guests")
print("TASK 5 - reject duplicate and impossible records")
print("TASK 6 - export the event metrics to CSV")
print("TASK 7 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project80_")
REPORT = os.path.join(WORK, "event-performance.csv")
events = [
    {"event_id": "EV1", "title": "Python Evening", "capacity": 20, "ticket_price": "5.00",
     "registrations": [
         {"registration_id": "R1", "status": "checked-in"},
         {"registration_id": "R2", "status": "checked-in"},
         {"registration_id": "R3", "status": "checked-in"},
         {"registration_id": "R4", "status": "cancelled"},
         {"registration_id": "R5", "status": "no-show"},
     ]},
    {"event_id": "EV2", "title": "Book Club", "capacity": 10, "ticket_price": "3.50",
     "registrations": [
         {"registration_id": "R6", "status": "checked-in"},
         {"registration_id": "R7", "status": "cancelled"},
         {"registration_id": "R8", "status": "checked-in"},
         {"registration_id": "R9", "status": "no-show"},
     ]},
    {"event_id": "EV3", "title": "Quiet Reading", "capacity": 8, "ticket_price": "0.00", "registrations": []},
]

print("=" * 60)
print("TASK 1 - event fixtures")
print("=" * 60)
print("events ->", len(events))
print("total registrations ->", sum(len(event["registrations"]) for event in events))
print("known states ->", "checked-in, cancelled, no-show")
print()

print("=" * 60)
print("TASK 2 - attendance and capacity")
print("=" * 60)
summaries = [summarize_event(event) for event in events]
for row in summaries:
    print("{0}: {1}/{2} attended, {3} registrations".format(
        row["title"], row["checked_in"], row["capacity"], row["registrations"]
    ))
print("EV1 counts correct ->", check("EV1 attendance", summaries[0]["checked_in"] == 3 and summaries[0]["cancelled"] == 1 and summaries[0]["no_show"] == 1))
print()

print("=" * 60)
print("TASK 3 - attendance rate and no-shows")
print("=" * 60)
for row in summaries:
    print("{0}: attendance {1:.1f}%, no-shows {2}".format(
        row["event_id"], row["attendance_rate"], row["no_show"]
    ))
print("EV1 attendance rate ->", summaries[0]["attendance_rate"], "%")
print("empty event rate ->", summaries[2]["attendance_rate"], "%")
check("rates use registration count", summaries[0]["attendance_rate"] == 60.0 and summaries[2]["attendance_rate"] == 0.0)
print()

print("=" * 60)
print("TASK 4 - ticket revenue")
print("=" * 60)
for row in summaries:
    print("{0} revenue -> ${1:.2f}".format(row["title"], row["revenue"]))
total_revenue = sum((row["revenue"] for row in summaries), Decimal("0.00"))
print("total event revenue -> ${0:.2f}".format(total_revenue))
print("revenue calculation correct ->", check("ticket revenue", summaries[0]["revenue"] == Decimal("15.00") and summaries[1]["revenue"] == Decimal("7.00")))
print()

print("=" * 60)
print("TASK 5 - reject invalid event records")
print("=" * 60)
invalid_events = [
    {"event_id": "BAD", "title": "Bad", "capacity": 2, "ticket_price": "1", "registrations": [
        {"registration_id": "D1", "status": "checked-in"},
        {"registration_id": "D1", "status": "no-show"}]},
    {"event_id": "FULL", "title": "Full", "capacity": 1, "ticket_price": "1", "registrations": [
        {"registration_id": "F1", "status": "checked-in"},
        {"registration_id": "F2", "status": "checked-in"}]},
]
invalid_messages = []
for event in invalid_events:
    try:
        summarize_event(event)
    except EventReportError as error:
        invalid_messages.append(str(error))
    else:
        invalid_messages.append("accepted")
print("invalid records rejected ->", invalid_messages)
check("duplicate and over-capacity rejected", invalid_messages == ["duplicate registration ID", "registrations exceed capacity"])
print()

print("=" * 60)
print("TASK 6 - export performance CSV")
print("=" * 60)
fields = write_event_report(REPORT, summaries)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("event rows ->", len(report_text.splitlines()) - 1)
print("empty event included ->", "Quiet Reading" in report_text)
print("revenue field included ->", "revenue" in fields)
check("report includes each event", len(report_text.splitlines()) == len(events) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary performance report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
