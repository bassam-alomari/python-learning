# ============================================================
# Project 56 - the bookshop reorders low-stock titles
# ============================================================
# What this project teaches:
#   reorder threshold   identify titles at or below a stock limit
#   purchase orders     build a supplier request from low-stock books
#   duplicate guard     do not open a second order for the same title
#   receiving stock     add delivered copies and close the order
#   value calculation   estimate reorder cost from unit price
#   validation          reject unknown titles and invalid quantities
#   deterministic flow all fixtures are local and repeatable
#   cleanup             temporary order export is removed at the end
#
# This continues the bookshop transaction projects. No network, input(),
# random, or clock is used. Supplier orders are represented as data.
#
# Run it:  python project-56-the-bookshop-reorders-low-stock.py
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


class ReorderError(ValueError):
    """Raised when an inventory or purchase-order operation is invalid."""


class ReorderDesk:
    """Track stock and open supplier orders for a small bookshop."""

    def __init__(self, books, supplier, threshold=2, target_stock=5):
        if threshold < 0 or target_stock < 1:
            raise ReorderError("invalid reorder policy")
        self.books = {book["title"].casefold(): dict(book) for book in books}
        self.supplier = supplier
        self.threshold = threshold
        self.target_stock = target_stock
        self.orders = {}
        self.next_order = 1

    def low_stock(self):
        """Return titles at/below threshold, in stable title order."""
        return sorted(
            (book for book in self.books.values() if book["copies"] <= self.threshold),
            key=lambda book: book["title"].casefold(),
        )

    def create_orders(self):
        """Open one purchase order per low-stock title unless already open."""
        created = []
        for book in self.low_stock():
            existing = next((
                order for order in self.orders.values()
                if order["title"].casefold() == book["title"].casefold()
                and order["status"] == "open"
            ), None)
            if existing is not None:
                continue
            quantity = self.target_stock - book["copies"]
            order_id = "PO{0:03d}".format(self.next_order)
            self.next_order += 1
            order = {
                "id": order_id,
                "title": book["title"],
                "supplier": self.supplier,
                "quantity": quantity,
                "unit_price": book["price"],
                "estimated_total": round(quantity * book["price"], 2),
                "status": "open",
            }
            self.orders[order_id] = order
            created.append(order)
        return created

    def receive(self, order_id, quantity=None):
        """Receive an open order and update stock exactly once."""
        order = self.orders.get(order_id)
        if order is None:
            raise ReorderError("purchase order not found")
        if order["status"] != "open":
            raise ReorderError("purchase order is already closed")
        delivered = order["quantity"] if quantity is None else quantity
        if not isinstance(delivered, int) or delivered <= 0:
            raise ReorderError("received quantity must be positive")
        if delivered > order["quantity"]:
            raise ReorderError("received quantity exceeds ordered quantity")
        book = self.books[order["title"].casefold()]
        book["copies"] += delivered
        order["status"] = "received"
        order["received"] = delivered
        return book["copies"]

    def export_orders(self, path):
        """Write purchase orders as a CSV report."""
        fields = ("id", "title", "supplier", "quantity", "unit_price",
                  "estimated_total", "status", "received")
        with open(path, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows({key: order.get(key, "") for key in fields}
                             for order in self.orders.values())
        return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  when should the shop consider reordering a title")
print("Q2  how many copies should a purchase order request")
print("Q3  how do we avoid duplicate open orders")
print("Q4  what changes when a delivery arrives")
print("Q5  how do we prevent receiving the same order twice")
print("Q6  how can the supplier request be exported")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  when copies are at or below the reorder threshold")
print("Q2  target stock minus copies currently on hand")
print("Q3  skip a title that already has an open order")
print("Q4  increase on-hand stock and close the purchase order")
print("Q5  only receive orders with open status")
print("Q6  write a CSV purchase-order report")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - identify low-stock books")
print("TASK 2 - open purchase orders up to target stock")
print("TASK 3 - skip duplicate open orders")
print("TASK 4 - estimate order cost")
print("TASK 5 - receive a delivery and update inventory")
print("TASK 6 - reject duplicate or excessive receipts")
print("TASK 7 - export orders as CSV")
print("TASK 8 - clean up the temporary report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project56_")
ORDER_REPORT = os.path.join(WORK, "purchase-orders.csv")
books = [
    {"title": "Dune", "price": 12.50, "copies": 4},
    {"title": "Neuromancer", "price": 9.99, "copies": 1},
    {"title": "Café Society", "price": 7.25, "copies": 2},
    {"title": "The Hobbit", "price": 8.50, "copies": 0},
]
desk = ReorderDesk(books, supplier="North Star Books", threshold=2, target_stock=5)

print("=" * 60)
print("TASK 1 - find low stock")
print("=" * 60)
low = desk.low_stock()
print("low-stock titles ->", ", ".join(book["title"] for book in low))
print("low-stock count ->", len(low))
print("Dune is above threshold ->", check("in-stock book skipped", all(book["title"] != "Dune" for book in low)))
print()

print("=" * 60)
print("TASK 2 - create purchase orders")
print("=" * 60)
created = desk.create_orders()
print("orders created ->", len(created))
print("order IDs ->", ", ".join(order["id"] for order in created))
print("Neuromancer quantity ->", next(order["quantity"] for order in created if order["title"] == "Neuromancer"))
print("Café Society quantity ->", next(order["quantity"] for order in created if order["title"] == "Café Society"))
print("The Hobbit quantity ->", next(order["quantity"] for order in created if order["title"] == "The Hobbit"))
check("target stock quantity", all(order["quantity"] == 5 - next(book["copies"] for book in books if book["title"] == order["title"]) for order in created))
print()

print("=" * 60)
print("TASK 3 - duplicate open orders are skipped")
print("=" * 60)
second_batch = desk.create_orders()
print("second batch created ->", len(second_batch))
print("open orders remain unique ->", check("one open order per title", len(desk.orders) == len(created)))
print()

print("=" * 60)
print("TASK 4 - estimate supplier cost")
print("=" * 60)
order_total = round(sum(order["estimated_total"] for order in created), 2)
print("supplier ->", desk.supplier)
print("estimated purchase total -> ${0:.2f}".format(order_total))
print("all orders use same supplier ->", check("supplier assigned", all(order["supplier"] == desk.supplier for order in created)))
print()

print("=" * 60)
print("TASK 5 - receive a delivery")
print("=" * 60)
neuromancer_order = next(order for order in created if order["title"] == "Neuromancer")
new_stock = desk.receive(neuromancer_order["id"])
print("received order ->", neuromancer_order["id"])
print("Neuromancer stock now ->", new_stock)
print("order status ->", neuromancer_order["status"])
check("received quantity added", new_stock == 5)
print()

print("=" * 60)
print("TASK 6 - invalid receipt is rejected")
print("=" * 60)
try:
    desk.receive(neuromancer_order["id"])
except ReorderError as error:
    duplicate_receipt = str(error)
else:
    duplicate_receipt = "accepted"
print("duplicate receipt ->", duplicate_receipt)
print("stock not counted twice ->", check("no duplicate receipt", desk.books["neuromancer"]["copies"] == 5))
try:
    desk.receive(next(order["id"] for order in created if order["title"] == "The Hobbit"), 99)
except ReorderError as error:
    excessive_receipt = str(error)
else:
    excessive_receipt = "accepted"
print("excess delivery ->", excessive_receipt)
print("excess quantity rejected ->", check("reject more than ordered", excessive_receipt.startswith("received quantity exceeds")))
print()

print("=" * 60)
print("TASK 7 - export the order report")
print("=" * 60)
fields = desk.export_orders(ORDER_REPORT)
with open(ORDER_REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("rows in report ->", len(report_text.splitlines()) - 1)
print("report includes supplier ->", desk.supplier in report_text)
print("expected columns ->", ", ".join(fields))
check("report row count", len(report_text.splitlines()) == len(created) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary order report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
