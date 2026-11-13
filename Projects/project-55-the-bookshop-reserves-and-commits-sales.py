# ============================================================
# Project 55 - the bookshop reserves stock and commits sales
# ============================================================
# What this project teaches:
#   reservation        hold copies temporarily without selling yet
#   confirmation       commit a reservation and issue a receipt
#   cancellation       release a hold with no stock loss
#   availability       on-hand minus active reservations
#   transaction safety reject overbooking before changing state
#   idempotence        reject duplicate confirmation/cancellation
#   persistence        atomically save final inventory as JSON
#   cleanup            all files live in a temporary workspace
#
# This continues project 54's inventory/snapshot workflow. It uses only
# the standard library, no input(), no random, and no wall-clock values.
#
# Run it:  python project-55-the-bookshop-reserves-and-commits-sales.py
# ============================================================

import json
import os
import shutil
import tempfile

CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


class ReservationError(ValueError):
    """Raised when a reservation operation is invalid."""


class Bookshop:
    """Small in-memory inventory with reservation transactions."""

    def __init__(self, books):
        self.books = {book["title"].casefold(): dict(book) for book in books}
        self.reservations = {}
        self.next_id = 1

    def available(self, title):
        """Return copies not currently held by open reservations."""
        key = title.casefold()
        if key not in self.books:
            raise ReservationError("book not found")
        held = sum(
            reservation["quantity"]
            for reservation in self.reservations.values()
            if reservation["title"].casefold() == key
            and reservation["status"] == "open"
        )
        return self.books[key]["copies"] - held

    def reserve(self, title, quantity):
        """Place a temporary hold after checking availability."""
        if not isinstance(quantity, int) or quantity <= 0:
            raise ReservationError("quantity must be a positive integer")
        available = self.available(title)
        if quantity > available:
            raise ReservationError("not enough available copies")
        reservation_id = "R{0:03d}".format(self.next_id)
        self.next_id += 1
        self.reservations[reservation_id] = {
            "title": self.books[title.casefold()]["title"],
            "quantity": quantity,
            "status": "open",
        }
        return reservation_id

    def confirm(self, reservation_id):
        """Commit a hold: reduce stock and return a receipt."""
        reservation = self._open_reservation(reservation_id)
        book = self.books[reservation["title"].casefold()]
        quantity = reservation["quantity"]
        book["copies"] -= quantity
        reservation["status"] = "confirmed"
        return {
            "id": reservation_id,
            "title": book["title"],
            "quantity": quantity,
            "total": round(book["price"] * quantity, 2),
            "remaining": book["copies"],
        }

    def cancel(self, reservation_id):
        """Release a hold without changing on-hand inventory."""
        reservation = self._open_reservation(reservation_id)
        reservation["status"] = "cancelled"
        return reservation["quantity"]

    def _open_reservation(self, reservation_id):
        reservation = self.reservations.get(reservation_id)
        if reservation is None:
            raise ReservationError("reservation not found")
        if reservation["status"] != "open":
            raise ReservationError("reservation is already closed")
        return reservation

    def snapshot(self):
        """Return a deterministic JSON-compatible state document."""
        return {
            "format": "bookshop-reservations",
            "version": 1,
            "books": sorted(self.books.values(), key=lambda book: book["title"].casefold()),
            "reservations": [
                {"id": reservation_id, **reservation}
                for reservation_id, reservation in sorted(self.reservations.items())
            ],
        }


def save_snapshot(path, state):
    """Write JSON atomically so a partial write cannot replace good state."""
    temporary = path + ".tmp"
    try:
        with open(temporary, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(state, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what is the difference between reserving and selling")
print("Q2  how do two customers avoid reserving the same last copy")
print("Q3  what happens when a reservation is cancelled")
print("Q4  what does confirming a reservation change")
print("Q5  why reject a second confirmation")
print("Q6  what state should be persisted")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  reserve holds availability; confirm performs the sale")
print("Q2  availability subtracts all active holds")
print("Q3  the hold is released and stock stays unchanged")
print("Q4  on-hand copies decrease and a receipt is returned")
print("Q5  a closed transaction must not apply twice")
print("Q6  inventory plus reservation statuses")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - create an inventory with limited stock")
print("TASK 2 - reserve copies and calculate available stock")
print("TASK 3 - reject an over-reservation without mutation")
print("TASK 4 - cancel one hold and release availability")
print("TASK 5 - confirm a hold and issue a receipt")
print("TASK 6 - reject duplicate confirmation")
print("TASK 7 - persist the final transaction state")
print("TASK 8 - clean up the temporary workspace")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project55_")
SNAPSHOT_PATH = os.path.join(WORK, "shop-state.json")
shop = Bookshop([
    {"title": "Dune", "price": 12.50, "copies": 3},
    {"title": "Neuromancer", "price": 9.99, "copies": 2},
])

check("starting Dune stock", shop.available("dune") == 3)
print("=" * 60)
print("TASK 1 - starting inventory")
print("=" * 60)
print("Dune on hand ->", shop.books["dune"]["copies"])
print("Dune available ->", shop.available("Dune"))
print("unknown titles rejected ->", end="")
try:
    shop.available("Foundation")
except ReservationError as error:
    unknown_message = str(error)
else:
    unknown_message = "accepted"
print(unknown_message)
print()

print("=" * 60)
print("TASK 2 - reserve and calculate availability")
print("=" * 60)
r1 = shop.reserve("Dune", 2)
print("reservation id ->", r1)
print("Dune available after hold ->", shop.available("Dune"))
print("stock still on hand ->", shop.books["dune"]["copies"])
check("hold changes availability only", shop.available("Dune") == 1 and shop.books["dune"]["copies"] == 3)
print()

print("=" * 60)
print("TASK 3 - over-reservation is rejected")
print("=" * 60)
available_before = shop.available("Dune")
try:
    shop.reserve("Dune", 2)
except ReservationError as error:
    overbook_message = str(error)
else:
    overbook_message = "accepted"
print("overbook result ->", overbook_message)
print("availability unchanged ->", check("overbook does not mutate", shop.available("Dune") == available_before))
print("open reservation count ->", sum(item["status"] == "open" for item in shop.reservations.values()))
print()

print("=" * 60)
print("TASK 4 - cancel a hold")
print("=" * 60)
r2 = shop.reserve("Dune", 1)
cancelled_quantity = shop.cancel(r2)
print("cancelled reservation ->", r2)
print("released quantity ->", cancelled_quantity)
print("availability after cancel ->", shop.available("Dune"))
print("on-hand stock unchanged ->", check("cancel preserves stock", shop.books["dune"]["copies"] == 3))
print()

print("=" * 60)
print("TASK 5 - confirm a reservation")
print("=" * 60)
receipt = shop.confirm(r1)
print("receipt id ->", receipt["id"])
print("receipt title ->", receipt["title"])
print("receipt quantity ->", receipt["quantity"])
print("receipt total -> ${0:.2f}".format(receipt["total"]))
print("remaining Dune copies ->", receipt["remaining"])
print("sale committed ->", check("confirm reduces stock", shop.books["dune"]["copies"] == 1))
print()

print("=" * 60)
print("TASK 6 - duplicate confirmation is rejected")
print("=" * 60)
try:
    shop.confirm(r1)
except ReservationError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
print("second confirmation ->", duplicate_message)
print("stock remains one ->", check("duplicate confirm is idempotently rejected", shop.books["dune"]["copies"] == 1))
print()

print("=" * 60)
print("TASK 7 - persist inventory and reservation states")
print("=" * 60)
state = shop.snapshot()
save_snapshot(SNAPSHOT_PATH, state)
with open(SNAPSHOT_PATH, "r", encoding="utf-8") as handle:
    saved_state = json.load(handle)
print("snapshot format ->", saved_state["format"])
print("books in snapshot ->", len(saved_state["books"]))
print("reservations in snapshot ->", len(saved_state["reservations"]))
print("confirmed status saved ->", check("confirmed transaction persisted", any(item["id"] == r1 and item["status"] == "confirmed" for item in saved_state["reservations"])))
print("cancelled status saved ->", check("cancelled transaction persisted", any(item["id"] == r2 and item["status"] == "cancelled" for item in saved_state["reservations"])))
print("temporary file gone ->", not os.path.exists(SNAPSHOT_PATH + ".tmp"))
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary transaction workspace removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
