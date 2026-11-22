# ============================================================
# Project 81 - the bookshop rebuilds inventory from its event log
# ============================================================
# What this project teaches:
#   event log          store checkout/return events as append-only records
#   replay              rebuild current copy state from history
#   state transitions   reject double checkout and return-without-loan
#   auditability        explain which event changed a copy
#   snapshots           compare replayed state with a saved snapshot
#   CSV export          write the event log for inspection
#   deterministic data fixed event sequence; no clock/network
#   cleanup             temporary audit report is removed
#
# Run it:  python project-81-the-bookshop-replays-inventory-events.py
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


class InventoryEventError(ValueError):
    """Raised when an event is invalid for the current copy state."""


def replay_events(copies, events):
    """Rebuild available/on-loan status by applying events in order."""
    state = {copy_id: {"title": title, "status": "available", "member": ""}
             for copy_id, title in copies.items()}
    for number, event in enumerate(events, start=1):
        required = ("event_id", "kind", "copy_id", "member")
        if any(key not in event for key in required):
            raise InventoryEventError("event " + str(number) + " missing fields")
        copy_id = event["copy_id"]
        if copy_id not in state:
            raise InventoryEventError("event references unknown copy")
        if event["kind"] == "checkout":
            if state[copy_id]["status"] != "available":
                raise InventoryEventError("copy already on loan")
            if not event["member"].strip():
                raise InventoryEventError("checkout member is required")
            state[copy_id]["status"] = "on loan"
            state[copy_id]["member"] = event["member"]
        elif event["kind"] == "return":
            if state[copy_id]["status"] != "on loan":
                raise InventoryEventError("copy is not on loan")
            if event["member"] != state[copy_id]["member"]:
                raise InventoryEventError("return member does not match checkout")
            state[copy_id]["status"] = "available"
            state[copy_id]["member"] = ""
        else:
            raise InventoryEventError("unknown event kind")
    return state


def export_events(path, events):
    fields = ("event_id", "kind", "copy_id", "member")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({key: event[key] for key in fields} for event in events)
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what is an append-only event log")
print("Q2  how can current inventory be rebuilt")
print("Q3  why must events be replayed in order")
print("Q4  what is a double checkout")
print("Q5  how can a snapshot be checked against history")
print("Q6  why keep an audit trail")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  a history of facts that is appended, not overwritten")
print("Q2  start from initial copies and apply each event")
print("Q3  later events depend on the state created by earlier ones")
print("Q4  checking out a copy that is already on loan")
print("Q5  compare the stored state to the replay result")
print("Q6  it shows who changed each copy and in what order")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - define initial copy inventory")
print("TASK 2 - build a checkout/return event history")
print("TASK 3 - replay events to rebuild current state")
print("TASK 4 - compare replay result to an expected snapshot")
print("TASK 5 - reject invalid event sequences")
print("TASK 6 - export the audit trail to CSV")
print("TASK 7 - clean up the audit file")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project81_")
REPORT = os.path.join(WORK, "inventory-events.csv")
initial_copies = {"C001": "Dune", "C002": "Neuromancer", "C003": "Kindred"}
events = [
    {"event_id": "E001", "kind": "checkout", "copy_id": "C001", "member": "M001"},
    {"event_id": "E002", "kind": "checkout", "copy_id": "C002", "member": "M002"},
    {"event_id": "E003", "kind": "return", "copy_id": "C001", "member": "M001"},
    {"event_id": "E004", "kind": "checkout", "copy_id": "C003", "member": "M003"},
]

print("=" * 60)
print("TASK 1 - initial copies and events")
print("=" * 60)
print("initial copies ->", len(initial_copies))
print("events ->", len(events))
print("event order ->", " -> ".join(event["kind"] for event in events))
print()

print("=" * 60)
print("TASK 2 - replay the event log")
print("=" * 60)
current = replay_events(initial_copies, events)
for copy_id in sorted(current):
    row = current[copy_id]
    owner_text = row["member"] if row["member"] else "none"
    print("{0} {1}: {2}, member {3}".format(copy_id, row["title"], row["status"], owner_text))
print("available copies ->", sum(row["status"] == "available" for row in current.values()))
print("copies on loan ->", sum(row["status"] == "on loan" for row in current.values()))
print()

print("=" * 60)
print("TASK 3 - compare replayed state with expected snapshot")
print("=" * 60)
expected = {
    "C001": {"title": "Dune", "status": "available", "member": ""},
    "C002": {"title": "Neuromancer", "status": "on loan", "member": "M002"},
    "C003": {"title": "Kindred", "status": "on loan", "member": "M003"},
}
print("snapshot matches replay ->", check("replay snapshot", current == expected))
print("C001 checkout then return ->", current["C001"]["status"])
print()

print("=" * 60)
print("TASK 4 - invalid history is rejected")
print("=" * 60)
invalid_histories = [
    events + [{"event_id": "E005", "kind": "checkout", "copy_id": "C002", "member": "M004"}],
    [{"event_id": "E006", "kind": "return", "copy_id": "C001", "member": "M001"}],
    [{"event_id": "E007", "kind": "checkout", "copy_id": "C001", "member": "M001"},
     {"event_id": "E008", "kind": "return", "copy_id": "C001", "member": "M999"}],
]
errors = []
for history in invalid_histories:
    try:
        replay_events(initial_copies, history)
    except InventoryEventError as error:
        errors.append(str(error))
    else:
        errors.append("accepted")
print("invalid history errors ->", errors)
print("all invalid histories rejected ->", check("bad event sequences blocked", all(error != "accepted" for error in errors)))
print()

print("=" * 60)
print("TASK 5 - event replay is deterministic")
print("=" * 60)
replayed_again = replay_events(initial_copies, list(events))
print("replay produces same state ->", check("repeat replay", replayed_again == current))
print("log has stable IDs ->", check("event IDs unique", len({event["event_id"] for event in events}) == len(events)))
print()

print("=" * 60)
print("TASK 6 - export audit CSV")
print("=" * 60)
fields = export_events(REPORT, events)
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    log_text = handle.read()
print("CSV header ->", log_text.splitlines()[0])
print("audit rows ->", len(log_text.splitlines()) - 1)
print("member column included ->", "member" in fields)
print("return event exported ->", "return" in log_text)
check("all events exported", len(log_text.splitlines()) == len(events) + 1)
print()

print("=" * 60)
print("TASK 7 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary event log removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
