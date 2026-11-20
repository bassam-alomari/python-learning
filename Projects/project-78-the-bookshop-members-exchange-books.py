# ============================================================
# Project 78 - the bookshop lets members exchange books
# ============================================================
# What this project teaches:
#   member listings      list books available to exchange
#   exchange request     request a listed copy from its owner
#   request guards       block self-requests and duplicate requests
#   acceptance           transfer ownership only after acceptance
#   cancellation         close an open request without transfer
#   inventory integrity each copy has one current owner
#   CSV audit            export listings and exchange history
#   cleanup              generated report stays in a temp folder
#
# Everything uses the standard library and fixed fixtures. No input(),
# random, network or clock is used.
#
# Run it:  python project-78-the-bookshop-members-exchange-books.py
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


class ExchangeError(ValueError):
    """Raised when a book exchange operation is invalid."""


class ExchangeDesk:
    """Manage book listings, requests and completed transfers."""

    def __init__(self, members, copies):
        self.members = set(members)
        self.copies = {}
        for copy in copies:
            copy_id = copy["copy_id"]
            if copy_id in self.copies:
                raise ExchangeError("duplicate copy ID")
            if copy["owner"] not in self.members:
                raise ExchangeError("copy owner is not a member")
            self.copies[copy_id] = dict(copy)
        self.requests = {}
        self.next_id = 1

    def request(self, requester, copy_id):
        """Create a request for an offered copy."""
        if requester not in self.members:
            raise ExchangeError("requester is not a member")
        copy = self._get_copy(copy_id)
        if copy["status"] != "listed":
            raise ExchangeError("copy is not available for exchange")
        if copy["owner"] == requester:
            raise ExchangeError("cannot request your own copy")
        duplicate = any(row["requester"] == requester and row["copy_id"] == copy_id
                        and row["status"] == "open" for row in self.requests.values())
        if duplicate:
            raise ExchangeError("duplicate open request")
        request_id = "X{0:03d}".format(self.next_id)
        self.next_id += 1
        row = {"request_id": request_id, "copy_id": copy_id,
               "title": copy["title"], "owner": copy["owner"],
               "requester": requester, "status": "open"}
        self.requests[request_id] = row
        return dict(row)

    def accept(self, request_id, owner):
        """Transfer the listed copy to the requester."""
        row = self._get_request(request_id)
        copy = self._get_copy(row["copy_id"])
        if row["status"] != "open":
            raise ExchangeError("request is not open")
        if owner != copy["owner"]:
            raise ExchangeError("only the current owner may accept")
        copy["owner"] = row["requester"]
        copy["status"] = "owned"
        row["status"] = "accepted"
        return dict(row)

    def cancel(self, request_id, member):
        row = self._get_request(request_id)
        if row["status"] != "open":
            raise ExchangeError("request is not open")
        if member not in (row["requester"], row["owner"]):
            raise ExchangeError("member is not part of this request")
        row["status"] = "cancelled"
        return dict(row)

    def _get_copy(self, copy_id):
        copy = self.copies.get(copy_id)
        if copy is None:
            raise ExchangeError("copy not found")
        return copy

    def _get_request(self, request_id):
        row = self.requests.get(request_id)
        if row is None:
            raise ExchangeError("request not found")
        return row

    def listing_rows(self):
        return [{
            "copy_id": copy_id,
            "title": copy["title"],
            "owner": copy["owner"],
            "status": copy["status"],
        } for copy_id, copy in sorted(self.copies.items())]

    def request_rows(self):
        return [dict(row) for _, row in sorted(self.requests.items())]


def export_exchange(path, listings, requests):
    fields = ("record_type", "record_id", "title", "owner", "requester", "status")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in listings:
            writer.writerow({"record_type": "copy", "record_id": row["copy_id"],
                             "title": row["title"], "owner": row["owner"],
                             "requester": "", "status": row["status"]})
        for row in requests:
            writer.writerow({"record_type": "request", "record_id": row["request_id"],
                             "title": row["title"], "owner": row["owner"],
                             "requester": row["requester"], "status": row["status"]})
    return fields


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  who may request a listed book")
print("Q2  why can an owner not request their own copy")
print("Q3  when does the book change ownership")
print("Q4  what happens when a request is cancelled")
print("Q5  how do we keep each copy assigned to one owner")
print("Q6  how can exchanges be audited")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  a known member other than the current owner")
print("Q2  self-requests do not create a meaningful exchange")
print("Q3  only after the owner accepts the open request")
print("Q4  close the request without changing ownership")
print("Q5  store one owner field per unique copy ID")
print("Q6  export copy listings and request statuses")
print()

# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)
print("TASK 1 - register members and their copies")
print("TASK 2 - list an available book for exchange")
print("TASK 3 - request another member's copy")
print("TASK 4 - prevent self and duplicate requests")
print("TASK 5 - accept a request and transfer ownership")
print("TASK 6 - cancel a request without transferring the book")
print("TASK 7 - export copy and request audit records")
print("TASK 8 - clean up the report")
print()
print("-" * 60)
print("PART C - the solution")
print("-" * 60)

WORK = tempfile.mkdtemp(prefix="project78_")
REPORT = os.path.join(WORK, "book-exchange.csv")
desk = ExchangeDesk(
    members=("M001", "M002", "M003"),
    copies=(
        {"copy_id": "C101", "title": "Dune", "owner": "M001", "status": "listed"},
        {"copy_id": "C102", "title": "Kindred", "owner": "M002", "status": "listed"},
        {"copy_id": "C103", "title": "The Hobbit", "owner": "M003", "status": "listed"},
    ),
)

print("=" * 60)
print("TASK 1 - members and listings")
print("=" * 60)
print("members ->", len(desk.members))
print("listed copies ->", len(desk.listing_rows()))
print("Dune owner ->", desk.copies["C101"]["owner"])
print()

print("=" * 60)
print("TASK 2 - request an exchange")
print("=" * 60)
request1 = desk.request("M002", "C101")
print("request ID ->", request1["request_id"])
print("request title ->", request1["title"])
print("owner ->", request1["owner"])
print("request status ->", request1["status"])
print()

print("=" * 60)
print("TASK 3 - block self and duplicate requests")
print("=" * 60)
try:
    desk.request("M001", "C101")
except ExchangeError as error:
    self_message = str(error)
else:
    self_message = "accepted"
try:
    desk.request("M002", "C101")
except ExchangeError as error:
    duplicate_message = str(error)
else:
    duplicate_message = "accepted"
print("self-request ->", self_message)
print("duplicate request ->", duplicate_message)
print("both guards work ->", check("self/duplicate guards", self_message == "cannot request your own copy" and duplicate_message == "duplicate open request"))
print()

print("=" * 60)
print("TASK 4 - owner accepts and title transfers")
print("=" * 60)
accepted = desk.accept(request1["request_id"], owner="M001")
print("accepted request ->", accepted["status"])
print("new owner ->", desk.copies["C101"]["owner"])
print("copy status ->", desk.copies["C101"]["status"])
check("ownership changed only on acceptance", accepted["status"] == "accepted" and desk.copies["C101"]["owner"] == "M002")
print()

print("=" * 60)
print("TASK 5 - cancel another request without transfer")
print("=" * 60)
request2 = desk.request("M001", "C102")
cancelled = desk.cancel(request2["request_id"], member="M001")
print("cancelled status ->", cancelled["status"])
print("owner unchanged ->", desk.copies["C102"]["owner"])
print("cancellation does not transfer ->", check("cancel leaves owner", desk.copies["C102"]["owner"] == "M002"))
print()

print("=" * 60)
print("TASK 6 - reject unauthorized actions")
print("=" * 60)
try:
    desk.accept(request1["request_id"], owner="M001")
except ExchangeError as error:
    closed_message = str(error)
else:
    closed_message = "accepted"
try:
    desk.cancel(request1["request_id"], member="M003")
except ExchangeError as error:
    stranger_message = str(error)
else:
    stranger_message = "accepted"
print("accept closed request ->", closed_message)
print("cancel as stranger ->", stranger_message)
check("closed/unauthorized actions rejected", closed_message == "request is not open" and stranger_message == "request is not open")
print()

print("=" * 60)
print("TASK 7 - export exchange history")
print("=" * 60)
fields = export_exchange(REPORT, desk.listing_rows(), desk.request_rows())
with open(REPORT, "r", encoding="utf-8", newline="") as handle:
    report_text = handle.read()
print("CSV header ->", report_text.splitlines()[0])
print("audit rows ->", len(report_text.splitlines()) - 1)
print("accepted state exported ->", "accepted" in report_text)
print("cancelled state exported ->", "cancelled" in report_text)
print("owner/requester fields included ->", "owner" in fields and "requester" in fields)
check("listings and requests exported", len(report_text.splitlines()) == len(desk.copies) + len(desk.requests) + 1)
print()

print("=" * 60)
print("TASK 8 - cleanup")
print("=" * 60)
shutil.rmtree(WORK)
check("workspace removed", not os.path.exists(WORK))
print("temporary exchange report removed ->", not os.path.exists(WORK))
print("=" * 60)

failed = [name for name, ok in CHECKS if not ok]
if failed:
    print("FAILED CHECKS ->", ", ".join(failed))
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    raise SystemExit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
