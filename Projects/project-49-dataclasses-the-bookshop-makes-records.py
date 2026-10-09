# ============================================================
# Project 49 - dataclasses: the bookshop makes records
# ============================================================
# What this lesson teaches:
#   @dataclass         __init__, __repr__ and __eq__ from the type hints
#   field order        a default cannot come before a required field
#   default_factory    a mutable default must be built per instance
#   frozen=True        immutable, and therefore hashable
#   __post_init__      refuse bad values while the object is being built
#   order=True         records become sortable
#   field()            tune one field: repr, compare, default
#   asdict / astuple   the record as a dict, or as a tuple
#
# Everything is the standard library. No input(), no random, no datetime.now.
# The output is deterministic. The file runs to completion and exits with 0.
# Nothing here touches the disk: a record is data, and data can just be data.
#
# Run it:  python project-49-dataclasses-the-bookshop-makes-records.py
# ============================================================

import dataclasses
import sys
from dataclasses import asdict, astuple, dataclass, field

CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what does @dataclass add to a class")
print("Q2  how does a dataclass decide equality")
print("Q3  why can a default field not come before a required one")
print("Q4  why is a plain [] default dangerous")
print("Q5  what does frozen=True buy you")
print("Q6  what does __post_init__ do")
print("Q7  what do asdict and astuple give you")
print("Q8  what does field(repr=False) change")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  __init__, __repr__ and __eq__, taken from the type hints")
print("Q2  it compares the fields, not the objects' identities")
print("Q3  because __init__ takes arguments in field order")
print("Q4  every instance would share that one list")
print("Q5  the record cannot change after it is built, and it hashes")
print("Q6  it runs right after __init__, so bad values are refused early")
print("Q7  the record as a dictionary, and as a tuple")
print("Q8  only that field is hidden from repr; it is still a real field")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - the class that writes itself")
print("T1  repr -> Book(title='Dune', author='Frank Herbert', copies=3)")
print("T1  so dataclass writes __init__ and __repr__ -> True")
print()

print("TASK 2 - equality compares the fields")
print("T2  same fields -> True")
print("T2  different fields -> False")
print("T2  so equality compares the fields -> True")
print()

print("TASK 3 - field order is not negotiable")
print("T3  a default before a required field -> TypeError")
print("T3  so fields run in a fixed order -> True")
print()

print("TASK 4 - a mutable default must be built")
print("T4  a plain [] default -> ValueError")
print("T4  default_factory gives each its own -> True")
print()

print("TASK 5 - frozen means frozen")
print("T5  changing it raises -> FrozenInstanceError")
print("T5  so frozen means frozen -> True")
print()

print("TASK 6 - refuse bad values while building")
print("T6  a zero-day loan -> ValueError")
print("T6  so validation happens at construction -> True")
print()

print("TASK 7 - the record as a dict and a tuple")
print("T7  asdict -> {'title': 'Dune', 'author': 'Frank Herbert', 'copies': 3}")
print("T7  astuple -> ('Dune', 'Frank Herbert', 3)")
print("T7  so the record is easy to ship -> True")
print()

print("TASK 8 - order=True makes them sortable")
print("T8  sorted first -> Dune")
print("T8  so order=True makes them sortable -> True")
print()

print("TASK 9 - field() tunes a single field")
print("T9  the repr -> Card(title='Dune', copies=3)")
print("T9  secret still there -> hidden")
print("T9  so field() tunes one field -> True")
print()

print("TASK 10 - the records carry the report")
print("T10  loans -> 2")
print("T10  the first row -> {'book': 'Dune', 'member': 'Sara', 'days': 7}")
print("T10  so a dataclass can carry the record -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)


# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - the class that writes itself")
print("-" * 60)


@dataclass
class Book:
    title: str
    author: str
    copies: int


book = Book("Dune", "Frank Herbert", 3)

check("the constructor took positional arguments",
      book.title == "Dune" and book.author == "Frank Herbert")
check("repr shows every field",
      repr(book) == "Book(title='Dune', author='Frank Herbert', copies=3)")
check("no __init__ was written by hand",
      Book("Dune", "Frank Herbert", 3).copies == 3)
check("the class knows its own name", type(book).__name__ == "Book")

print("T1  repr ->", book)
print("T1  so dataclass writes __init__ and __repr__ ->",
      repr(book) == "Book(title='Dune', author='Frank Herbert', copies=3)")
print()


# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - equality compares the fields")
print("-" * 60)
twin = Book("Dune", "Frank Herbert", 3)
other = Book("Dune Messiah", "Frank Herbert", 2)

check("same fields are equal", book == twin)
check("different fields are not equal", book != other)
check("equal does not mean identical", book is not twin)
check("every field counts", other.copies == 2 and other.title != book.title)

print("T2  same fields ->", book == twin)
print("T2  different fields ->", book == other)
print("T2  so equality compares the fields ->", book == twin)
print()


# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - field order is not negotiable")
print("-" * 60)
order_error = None
try:
    @dataclass
    class Backwards:
        a: str = "x"
        b: str
except TypeError as exc:
    order_error = exc


@dataclass
class Member:
    name: str
    fine: float = 0.0


check("the class refused to exist", order_error is not None)
check("it is a TypeError", isinstance(order_error, TypeError))
check("the message says which field",
      order_error is not None
      and "non-default argument" in str(order_error))
check("a well-ordered default works", Member("Sara").fine == 0.0)

print("T3  a default before a required field ->",
      type(order_error).__name__ if order_error else "no error")
print("T3  so fields run in a fixed order ->",
      order_error is not None and Member("Sara").fine == 0.0)
print()


# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - a mutable default must be built")
print("-" * 60)
shared_error = None
try:
    @dataclass
    class Broken:
        tags: list = []
except ValueError as exc:
    shared_error = exc


@dataclass
class Tagged:
    tags: list = field(default_factory=list)


first = Tagged()
second = Tagged()
first.tags.append("sci-fi")

check("the plain default was refused", shared_error is not None)
check("it is a ValueError", isinstance(shared_error, ValueError))
check("the message names default_factory",
      shared_error is not None
      and "default_factory" in str(shared_error))
check("the two instances do not share a list", second.tags == [])

print("T4  a plain [] default ->",
      type(shared_error).__name__ if shared_error else "no error")
print("T4  default_factory gives each its own ->", second.tags == [])
print()


# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - frozen means frozen")
print("-" * 60)


@dataclass(frozen=True)
class Shelf:
    name: str
    capacity: int


shelf = Shelf("A", 40)
set_error = None
try:
    shelf.name = "B"
except dataclasses.FrozenInstanceError as exc:
    set_error = exc

hash_error = None
try:
    hash(book)
except TypeError as exc:
    hash_error = exc

check("the assignment was refused", set_error is not None)
check("it is a FrozenInstanceError",
      isinstance(set_error, dataclasses.FrozenInstanceError))
check("frozen records hash", hash(shelf) is not None)
check("an ordinary dataclass does not", isinstance(hash_error, TypeError))

print("T5  changing it raises ->",
      type(set_error).__name__ if set_error else "no error")
print("T5  so frozen means frozen ->",
      set_error is not None and hash(shelf) is not None)
print()


# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - refuse bad values while building")
print("-" * 60)


@dataclass
class Loan:
    book: str
    member: str
    days: int

    def __post_init__(self):
        if self.days < 1:
            raise ValueError("a loan lasts at least one day")


fine_error = None
try:
    Loan("Dune", "Sara", 0)
except ValueError as exc:
    fine_error = exc

good_loan = Loan("Dune", "Sara", 7)

check("the zero-day loan was refused", fine_error is not None)
check("the message explains why",
      fine_error is not None
      and "at least one day" in str(fine_error))
check("a real loan was built", good_loan.days == 7)
check("the fields are all there",
      good_loan.book == "Dune" and good_loan.member == "Sara")

print("T6  a zero-day loan ->",
      type(fine_error).__name__ if fine_error else "no error")
print("T6  so validation happens at construction ->",
      fine_error is not None and good_loan.days == 7)
print()


# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - the record as a dict and a tuple")
print("-" * 60)
record = asdict(book)
row = astuple(book)

check("asdict returns a dict", isinstance(record, dict))
check("the keys are the field names",
      list(record) == ["title", "author", "copies"])
check("astuple returns a tuple", isinstance(row, tuple))
check("the values survived the trip",
      record["title"] == "Dune" and row[2] == 3)

print("T7  asdict ->", record)
print("T7  astuple ->", row)
print("T7  so the record is easy to ship ->",
      record == {"title": "Dune", "author": "Frank Herbert", "copies": 3})
print()


# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - order=True makes them sortable")
print("-" * 60)


@dataclass(order=True)
class Ranked:
    title: str
    copies: int


shelf_list = [Ranked("Zealot", 1), Ranked("Dune", 5)]
shelf_list.sort()

order_error_type = None
try:
    book < other
except TypeError as exc:
    order_error_type = exc

check("sort worked", shelf_list[0].title == "Dune")
check("there are two records", len(shelf_list) == 2)
check("an ordinary dataclass refuses <",
      isinstance(order_error_type, TypeError))
check("the sort did not lose a field",
      shelf_list[1].title == "Zealot" and shelf_list[1].copies == 1)

print("T8  sorted first ->", shelf_list[0].title)
print("T8  so order=True makes them sortable ->", shelf_list[0].title == "Dune")
print()


# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - field() tunes a single field")
print("-" * 60)


@dataclass
class Card:
    title: str
    secret: str = field(default="n/a", repr=False, compare=False)
    copies: int = field(default=1)


shown = Card("Dune", "hidden", 3)
twin_card = Card("Dune", "something else", 3)

check("secret is hidden from repr", "secret" not in repr(shown))
check("secret is still a real field", shown.secret == "hidden")
check("secret is excluded from equality", shown == twin_card)
check("copies still shows up", "copies=3" in repr(shown))

print("T9  the repr ->", shown)
print("T9  secret still there ->", shown.secret)
print("T9  so field() tunes one field ->",
      "secret" not in repr(shown) and shown == twin_card)
print()


# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the records carry the report")
print("-" * 60)
loans = [Loan("Dune", "Sara", 7), Loan("Messiah", "Omar", 14)]
rows = [asdict(one) for one in loans]

refused = None
try:
    Loan("Children", "Nadia", 0)
except ValueError as exc:
    refused = exc

check("two loans were recorded", len(loans) == 2)
check("the first row is a dict", isinstance(rows[0], dict))
check("the first row says Dune",
      rows[0] == {"book": "Dune", "member": "Sara", "days": 7})
check("the second row says Omar", rows[1]["member"] == "Omar")
check("bad rows never get made", refused is not None)

print("T10  loans ->", len(loans))
print("T10  the first row ->", rows[0])
print("T10  so a dataclass can carry the record ->",
      len(rows) == 2 and refused is not None)
print()


# ------------------------------------------------------------
# report
# ------------------------------------------------------------
failed = [name for name, ok in CHECKS if not ok]
print("=" * 60)
if failed:
    for name in failed:
        print("  FAILED:", name)
    print("CHECKS PASSED {0} of {1}".format(
        len(CHECKS) - len(failed), len(CHECKS)))
    sys.exit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
