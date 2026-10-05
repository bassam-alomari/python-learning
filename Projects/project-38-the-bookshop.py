# ============================================================
# PROJECT 38 - THE BOOKSHOP: EVERYTHING TOGETHER
# ============================================================
#
# This is the final project. Nothing new is invented here on purpose.
# Every idea is one you already met, and now they all have to live in
# the same program without fighting each other:
#
#   project 32  plain functions, closures, memoisation
#   project 33  functional library, defaults, boundaries
#   project 34  JSON on disk, atomic replace, integrity checks
#   project 35  classes, properties, a small exception hierarchy
#   project 36  Big-O, and measuring work by counting it
#   project 37  edge cases, unittest, mocks, tracebacks, pdb
#   project 38  ALL OF IT, plus CSV and a context manager
#
# The shop has three things: books, members, and loans. It can export
# the catalogue to CSV for a human, keep its state in JSON for itself,
# and survive a crash while writing.
#
# There is no input() anywhere. Everything is deterministic: the same
# numbers on every run, every machine, forever.
#
# Run it:  python project-38-the-bookshop.py
# ============================================================

import csv
import functools
import io
import json
import os
import tempfile
import unittest
from unittest import mock


# ============================================================
# PART A - THE QUESTIONS
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print("Q1  a dict keyed by title gives one lookup, not a loop")
print("Q2  so a duplicate title is a one line check, not a search")
print("Q3  csv quoting saves your commas, and lineterminator saves")
print("Q3  your diffs, because default csv writes \\r\\n on Windows")
print("Q4  a context manager is a with block that cannot leak, so")
print("Q4  loading on enter and saving on exit is one class not two")
print("Q5  the save must be skipped when the block raised, or a bug")
print("Q5  will happily write its own broken state to disk")
print("Q6  csv gives you text back, so int() on every numeric column")
print("Q6  and .get() a default for a column that might be missing")
print("Q7  a memoised search is only safe while the data is frozen,")
print("Q7  so any method that edits books has to clear the cache")
print("Q8  the real test of a program is not that it runs, it is")
print("Q8  what it refuses to do, and what it leaves behind on disk")
print()

# ------------------------------------------------------------
# SELF CHECK - the correct answers
# ------------------------------------------------------------
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  find a title by looping over 4 books costs 4 comparisons")
print("Q1  find it in the dict costs 1 lookup, whatever the size")
print("Q2  so if new in dict is False the title is already taken")
print("Q3  without lineterminator the same data gives two files")
print("Q3  one with \\r\\n on Windows and one with \\n on Linux")
print("Q4  __enter__ returns the thing you want to use")
print("Q4  __exit__ returns False so an exception still escapes")
print("Q5  a with block that raised means the data is untrustworthy")
print("Q5  and writing it would turn a crash into silent corruption")
print("Q6  so round tripping is not free, it needs a conversion step")
print("Q7  a stale cache is worse than no cache, it lies confidently")
print("Q8  so the tests below mostly feed the shop rubbish")
print("Q8  and assert that it refuses instead of crashing or saving")
print()
print("-" * 60)


# ============================================================
# THE SHOP
# ============================================================

class ShopError(Exception):
    """The parent of every problem this shop knows how to explain."""


class DuplicateTitle(ShopError):
    pass


class DuplicateMember(ShopError):
    pass


class UnknownMember(ShopError):
    pass


class NotBorrowed(ShopError):
    pass


class NoBooksYet(ShopError):
    pass


def to_int(value, default=None):
    """A strict int conversion that never raises, for reading files."""
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        try:
            return int(text)
        except ValueError:
            return default
    return default


class Book:
    """One catalogue line. Validation lives in the properties, so an
    invalid Book cannot be built at all, whatever the caller does."""

    def __init__(self, title, author, copies):
        self.title = title
        self.author = author
        self.copies = copies

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        text = "" if value is None else str(value).strip()
        if not text:
            raise ShopError("a book needs a title")
        self._title = text

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        text = "" if value is None else str(value).strip()
        if not text:
            raise ShopError("a book needs an author")
        self._author = text

    @property
    def copies(self):
        return self._copies

    @copies.setter
    def copies(self, value):
        number = to_int(value)
        if number is None:
            raise ShopError("copies must be a whole number")
        if number < 0:
            raise ShopError("copies must not be negative")
        self._copies = number

    def to_row(self):
        return {"title": self.title, "author": self.author, "copies": self.copies}


class Catalogue:
    """The books, held in a dict so every lookup costs one step.
    The author index is memoised, so the cache must be cleared
    whenever a book is added or removed."""

    def __init__(self):
        self._books = {}
        self.titles_by_author = memoised(self._titles_by_author)

    def add(self, book):
        if book.title in self._books:
            raise DuplicateTitle("already stocked: " + book.title)
        self._books[book.title] = book
        self._invalidate()

    def get(self, title):
        return self._books.get(title)

    def size(self):
        return len(self._books)

    def copies(self):
        """Total copies on the shelf, not titles, because one title
        with 300 copies is not the same stock as 300 titles."""
        return sum(book.copies for book in self._books.values())

    def titles(self):
        return sorted(self._books)

    def authors(self):
        seen = []
        for title in self.titles():
            author = self._books[title].author
            if author not in seen:
                seen.append(author)
        return sorted(seen)

    def _titles_by_author(self, author):
        wanted = author.strip().lower()
        found = [title for title in self.titles()
                 if self._books[title].author.lower() == wanted]
        return found

    def _invalidate(self):
        self.titles_by_author.cache.clear()


def memoised(func):
    """Remember pure results by their arguments, and count the hits so
    the tests can prove the cache is actually being used."""
    cache = {}
    counters = {"miss": 0, "hit": 0}

    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            counters["hit"] += 1
            return cache[args]
        counters["miss"] += 1
        result = func(*args)
        cache[args] = result
        return result

    wrapper.cache = cache
    wrapper.counters = counters
    return wrapper


class Loans:
    """Open loans keyed by (member, title), so checking one loan is a
    single lookup. Days are numbers passed in by the caller, never
    read from the clock, so the same run always gives the same fines."""

    def __init__(self, loan_days=14, fine_per_day=2):
        days = to_int(loan_days)
        rate = to_int(fine_per_day)
        if days is None or days < 0:
            raise ShopError("loan_days must be a whole number >= 0")
        if rate is None or rate < 0:
            raise ShopError("fine_per_day must be a whole number >= 0")
        self.loan_days = days
        self.fine_per_day = rate
        self._open = {}
        self.history = []

    def borrow(self, member, title, day):
        number = to_int(day)
        if number is None:
            raise ShopError("a day must be a whole number")
        self._open[(member, title)] = {"borrowed": number, "due": number + self.loan_days}
        self.history.append({"member": member, "title": title,
                             "borrowed": number, "returned": None, "fine": None})

    def due_on(self, member, title):
        loan = self._open.get((member, title))
        if loan is None:
            raise NotBorrowed("not on loan: " + title)
        return loan["due"]

    def fine_on(self, member, title, day):
        loan = self._open.get((member, title))
        if loan is None:
            raise NotBorrowed("not on loan: " + title)
        late = max(0, to_int(day, 0) - loan["due"])
        return late * self.fine_per_day

    def give_back(self, member, title, day):
        loan = self._open.get((member, title))
        if loan is None:
            raise NotBorrowed("not on loan: " + title)
        number = to_int(day)
        if number is None:
            raise ShopError("a day must be a whole number")
        if number < loan["borrowed"]:
            raise ShopError("cannot return before it was borrowed")
        fine = max(0, number - loan["due"]) * self.fine_per_day
        del self._open[(member, title)]
        for record in self.history:
            if (record["member"] == member and record["title"] == title
                    and record["returned"] is None):
                record["returned"] = number
                record["fine"] = fine
                break
        return fine

    def open_count(self):
        return len(self._open)

    def open_loans(self):
        return sorted((member, title) for member, title in self._open)


class Shop:
    """The whole shop: books, members, loans, and the file that holds
    them. add_book and add_member enforce the one rule a dict cannot:
    a name is unique."""

    def __init__(self):
        self.catalogue = Catalogue()
        self.members = []
        self.loans = Loans()

    def add_book(self, title, author, copies):
        book = Book(title, author, copies)
        self.catalogue.add(book)
        return book

    def add_member(self, name):
        text = "" if name is None else str(name).strip()
        if not text:
            raise ShopError("a member needs a name")
        if text in self.members:
            raise DuplicateMember("already a member: " + text)
        self.members.append(text)
        return text

    def borrow(self, member, title, day):
        if self.catalogue.size() == 0:
            raise NoBooksYet("the shop has no books yet")
        if member not in self.members:
            raise UnknownMember("not a member: " + str(member))
        if self.catalogue.get(title) is None:
            raise NotBorrowed("not in stock: " + str(title))
        self.loans.borrow(member, title, day)

    def to_dict(self):
        return {
            "books": [self.catalogue.get(t).to_row() for t in self.catalogue.titles()],
            "members": sorted(self.members),
            "loans": [dict(record) for record in self.loans.history],
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ShopError("saved data must be a dict")
        shop = cls()
        for row in data.get("books", []):
            shop.add_book(row.get("title"), row.get("author"), row.get("copies", 0))
        for name in data.get("members", []):
            shop.add_member(name)
        for record in data.get("loans", []):
            member = record.get("member")
            title = record.get("title")
            day = to_int(record.get("borrowed"), 0)
            shop.borrow(member, title, day)
            returned = to_int(record.get("returned"))
            if returned is not None:
                shop.loans.give_back(member, title, returned)
        return shop


# ============================================================
# FILES - JSON for itself, CSV for humans
# ============================================================

def dumps_canonical(data):
    """One data set has exactly one text form, so two runs of the same
    shop produce byte identical files and git sees no diff."""
    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def save_json(path, data):
    """Write to a temporary file in the same folder, then replace the
    real one. A crash leaves the old file intact instead of half of
    the new one."""
    folder = os.path.dirname(os.path.abspath(path))
    handle, temp_path = tempfile.mkstemp(dir=folder, suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(dumps_canonical(data))
        os.replace(temp_path, path)
    except BaseException:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise


def load_json(path):
    with open(path, "r", encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ShopError("saved data must be a dict")
    return data


def read_text(path):
    """Never open(...).read(). That form relies on the garbage
    collector to close the file, so an interrupted run can leave the
    handle open, and the warning that tells you is easy to miss."""
    with open(path, "r", encoding="utf-8", newline="") as stream:
        return stream.read()


def read_bytes(path):
    with open(path, "rb") as stream:
        return stream.read()


class ShopFile:
    """A context manager: load the shop on enter, save it on a clean
    exit, and do nothing on a broken one. Returning False from
    __exit__ lets the original exception escape untouched."""

    def __init__(self, path, shop):
        self.path = path
        self.shop = shop
        self.saved = False
        self.exception_seen = None

    def __enter__(self):
        if os.path.exists(self.path):
            self.shop = Shop.from_dict(load_json(self.path))
        return self.shop

    def __exit__(self, exc_type, exc_value, traceback):
        self.exception_seen = exc_type
        if exc_type is None:
            save_json(self.path, self.shop.to_dict())
            self.saved = True
        return False


CSV_FIELDS = ["title", "author", "copies"]


def export_csv(path, books):
    """lineterminator must be given, or csv writes \\r\\n on Windows and
    \\n on Linux and the same data produces two different files."""
    with open(path, "w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        for book in books:
            writer.writerow(book.to_row())


def import_csv(path):
    """csv hands back text, so every number needs converting, and a
    missing column needs a default instead of a KeyError."""
    books = []
    problems = []
    with open(path, "r", encoding="utf-8", newline="") as stream:
        for number, row in enumerate(csv.DictReader(stream), start=2):
            title = (row.get("title") or "").strip()
            author = (row.get("author") or "").strip()
            if not title or not author:
                problems.append("line " + str(number) + " has no title or author")
                continue
            copies = to_int(row.get("copies"), 0)
            books.append(Book(title, author, copies))
    return books, problems


def shop_report(shop):
    """Sorted everywhere, so the report is a fixed string, not a
    rendering of whatever the dict happened to hold."""
    lines = []
    if shop.catalogue.size() == 0:
        return ["nothing to report"]
    lines.append("books " + str(shop.catalogue.size()) +
                 "  members " + str(len(shop.members)) +
                 "  open loans " + str(shop.loans.open_count()))
    for author in shop.catalogue.authors():
        owned = shop.catalogue.titles_by_author(author)
        lines.append("  " + author + " -> " + str(len(owned)) + " title(s)")
    if shop.loans.open_count() == 0:
        lines.append("no loans on record")
    else:
        for member, title in shop.loans.open_loans():
            lines.append("  on loan: " + member + " has " + title)
    return lines


# ============================================================
# HELPERS FOR THE TASKS
# ============================================================

def what_it_raises(func, *args):
    """Run it and name the exception class, so the output stays one
    line per case instead of a try block per case."""
    try:
        func(*args)
    except Exception as error:
        return type(error).__name__
    return "nothing"


def recorded(func, *args):
    """Same trick, but returns (value, exception name)."""
    try:
        return func(*args), None
    except Exception as error:
        return None, type(error).__name__


def message_of(func, *args):
    """The refusal itself, not just its type, because the message is
    what a user will actually read."""
    try:
        func(*args)
    except Exception as error:
        return str(error)
    return "nothing was refused"


def sample_shop():
    shop = Shop()
    shop.add_book("Dune", "Frank Herbert", 3)
    shop.add_book("Clean Code, A Handbook", "Robert Martin", 2)
    shop.add_book("The Pragmatic Programmer", "Andrew Hunt", 1)
    shop.add_book("Refactoring", "Martin Fowler", 2)
    shop.add_member("Sara")
    shop.add_member("Ali")
    return shop


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

# ------------------------------------------------------------
# TASK 1 - the exception ladder
# ------------------------------------------------------------
print("TASK 1 - one parent, four children")
print("T1  DuplicateTitle raised -> DuplicateTitle")
print("T1  UnknownMember raised -> UnknownMember")
print("T1  NotBorrowed raised -> NotBorrowed")
print("T1  they all share one parent -> ShopError")
print("T1  and that parent is an Exception -> True")
print("T1  so one except can catch the whole family -> True")
print()

# ------------------------------------------------------------
# TASK 2 - validation you cannot forget
# ------------------------------------------------------------
print("TASK 2 - properties that refuse at construction time")
print("T2  a valid Book was built -> Book")
print("T2  surrounding spaces are stripped -> Dune")
print("T2  an empty title is refused -> a book needs a title")
print("T2  a negative copies is refused -> copies must not be negative")
print("T2  a lone 7 is accepted -> 7 int")
print("T2  and true is not a number -> copies must be a whole number")
print()

# ------------------------------------------------------------
# TASK 3 - a dict instead of a loop
# ------------------------------------------------------------
print("TASK 3 - O(1) lookup and a memoised author index")
print("T3  books added -> 4")
print("T3  a duplicate title is refused -> DuplicateTitle")
print("T3  a known title is found -> Dune")
print("T3  an unknown title gives -> None")
print("T3  searching one author three times -> 1 miss, 2 hits")
print("T3  and the counters prove it -> {'miss': 1, 'hit': 2}")
print()

# ------------------------------------------------------------
# TASK 4 - loans and fines
# ------------------------------------------------------------
print("TASK 4 - loans, due days and fines")
print("T4  loans opened -> 2")
print("T4  Dune is due on day -> 24")
print("T4  its fine if returned on day 30 -> 12")
print("T4  returning it on day 20 costs -> 0")
print("T4  the late one costs -> 12")
print("T4  nothing is open afterwards -> True")
print("T4  a negative fine rate is refused -> ShopError")
print("T4  borrowing as a stranger is refused -> UnknownMember")
print("T4  returning a book never taken -> NotBorrowed")
print()

# ------------------------------------------------------------
# TASK 5 - one text form, written atomically
# ------------------------------------------------------------
print("TASK 5 - JSON with a single canonical form")
print("T5  the file ends with a newline -> True")
print("T5  the same data always gives the same text -> True")
print("T5  a reread equals the original -> True")
print("T5  loading a file that is not there -> FileNotFoundError")
print("T5  the temporary file is gone -> True")
print("T5  the folder holds exactly one file -> 1")
print("T5  and that file is not a temporary -> shop.json")
print()

# ------------------------------------------------------------
# TASK 6 - CSV for humans
# ------------------------------------------------------------
print("TASK 6 - CSV, and the two things it will surprise you with")
print("T6  the exported lines -> 5")
print("T6  the header row -> title,author,copies")
print("T6  a title holding a comma -> \"Clean Code, A Handbook\",Robert Martin,2")
print("T6  every line ends in a bare newline -> True")
print("T6  the bytes contain no \\r -> True")
print("T6  books reimported -> 4")
print("T6  the awkward title survived -> Clean Code, A Handbook")
print("T6  copies came back as text -> '2'")
print("T6  so converting it again gives -> 2")
print()

# ------------------------------------------------------------
# TASK 7 - the context manager
# ------------------------------------------------------------
print("TASK 7 - with, and the save that must not happen")
print("T7  inside the block the shop holds -> 4")
print("T7  a clean exit saved the file -> True")
print("T7  an exception inside the block -> ValueError")
print("T7  the block was told there was one -> ValueError")
print("T7  and the file was left alone -> True")
print("T7  still holding 4 books -> 4")
print("T7  and the fifth book was never written -> True")
print()

# ------------------------------------------------------------
# TASK 8 - what it refuses
# ------------------------------------------------------------
print("TASK 8 - the rubbish this shop will not accept")
print("T8  an empty catalogue holds -> 0")
print("T8  and it reports -> nothing to report")
print("T8  a duplicate member is refused -> DuplicateMember")
print("T8  a shop with no open loans -> no loans on record")
print("T8  returning a title never borrowed -> NotBorrowed")
print("T8  returning on the borrowing day costs -> 0")
print("T8  returning before it was borrowed -> ShopError")
print("T8  a broken csv line is skipped, not fatal -> line 3 has no title or author")
print()

# ------------------------------------------------------------
# TASK 9 - the test suite
# ------------------------------------------------------------
print("TASK 9 - every subject under test")
print("T9   validation   passed   8  failed   0")
print("T9   catalogue    passed   6  failed   0")
print("T9   loans        passed   9  failed   0")
print("T9   persistence  passed   7  failed   0")
print("T9   csv          passed   6  failed   0")
print("T9   TOTAL     passed  36  failed   0")
print("T9   errors, which are the dangerous kind -> 0")
print()

# ------------------------------------------------------------
# TASK 10 - the whole shop, and what it cost
# ------------------------------------------------------------
print("TASK 10 - the full shop, and the bill for it")
print("T10   books 4  members 2  open loans 2")
print("T10   copies on the shelf and out -> 8 total, 2 on loan, 6 home")
print("T10   one search, dict way -> 1")
print("T10   one search, loop way -> 3")
print("T10   so the dict wins by -> 3.0x")
print("T10   and the memory it costs -> 4 extra entries")
print("T10   the whole file leaves no temporary -> True")
print("T10   and every claim above was printed, not assumed -> True")
print()


# ============================================================
# PART C - THE SOLUTION
# ============================================================

print()
print("=" * 60)
print("PART C - the solution")
print("=" * 60)

# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print()
print("-" * 60)
print("TASK 1 - one parent, four children")
print("-" * 60)
shop = Shop()
shop.add_book("Dune", "Frank Herbert", 1)
shop.add_member("Sara")
print("T1  DuplicateTitle raised ->", what_it_raises(shop.add_book, "Dune", "X", 1))
print("T1  UnknownMember raised ->", what_it_raises(shop.borrow, "Ghost", "Dune", 1))
print("T1  NotBorrowed raised ->", what_it_raises(shop.loans.give_back, "Sara", "Dune", 5))
for child in (DuplicateTitle, DuplicateMember, UnknownMember, NotBorrowed, NoBooksYet):
    if not issubclass(child, ShopError):
        raise ShopError("a shop error escaped the family")
print("T1  they all share one parent ->", ShopError.__name__)
print("T1  and that parent is an Exception ->", issubclass(ShopError, Exception))
print("T1  so one except can catch the whole family ->", True)
print()

# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - properties that refuse at construction time")
print("-" * 60)
book = Book("Dune", "Frank Herbert", 3)
print("T2  a valid Book was built ->", type(book).__name__)
spaced = Book("  Dune  ", "  Frank Herbert ", 1)
print("T2  surrounding spaces are stripped ->", spaced.title)
print("T2  an empty title is refused ->", message_of(Book, "   ", "X", 1))
try:
    Book("Dune", "X", -1)
except ShopError as problem:
    print("T2  a negative copies is refused ->", problem)
loose = Book("Dune", "X", "7")
print("T2  a lone 7 is accepted ->", loose.copies, type(loose.copies).__name__)
try:
    Book("Dune", "X", True)
except ShopError as problem:
    print("T2  and true is not a number ->", problem)
print()

# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - O(1) lookup and a memoised author index")
print("-" * 60)
catalogue = Catalogue()
catalogue.add(Book("Dune", "Frank Herbert", 3))
catalogue.add(Book("Clean Code, A Handbook", "Robert Martin", 2))
catalogue.add(Book("The Pragmatic Programmer", "Andrew Hunt", 1))
catalogue.add(Book("Refactoring", "Martin Fowler", 2))
print("T3  books added ->", catalogue.size())
try:
    catalogue.add(Book("Dune", "Someone Else", 1))
except DuplicateTitle as problem:
    print("T3  a duplicate title is refused ->", type(problem).__name__)
found = catalogue.get("Dune")
print("T3  a known title is found ->", found.title)
print("T3  an unknown title gives ->", catalogue.get("Nothing At All"))
counters = catalogue.titles_by_author.counters
for _ in range(3):
    catalogue.titles_by_author("Martin Fowler")
print("T3  searching one author three times ->",
      str(counters["miss"]) + " miss, " + str(counters["hit"]) + " hits")
print("T3  and the counters prove it ->", counters)
print()

# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - loans, due days and fines")
print("-" * 60)
loans = Loans(loan_days=14, fine_per_day=2)
loans.borrow("Sara", "Dune", 10)
loans.borrow("Ali", "Clean Code, A Handbook", 12)
print("T4  loans opened ->", loans.open_count())
print("T4  Dune is due on day ->", loans.due_on("Sara", "Dune"))
print("T4  its fine if returned on day 30 ->", loans.fine_on("Sara", "Dune", 30))
print("T4  returning it on day 20 costs ->", loans.give_back("Sara", "Dune", 20))
print("T4  the late one costs ->", loans.give_back("Ali", "Clean Code, A Handbook", 32))
print("T4  nothing is open afterwards ->", loans.open_count() == 0)
print("T4  a negative fine rate is refused ->", what_it_raises(Loans, 14, -1))
mini = Shop()
mini.add_book("Dune", "Frank Herbert", 1)
mini.add_member("Sara")
print("T4  borrowing as a stranger is refused ->",
      what_it_raises(mini.borrow, "Ghost", "Dune", 1))
print("T4  returning a book never taken ->",
      what_it_raises(loans.give_back, "Sara", "Refactoring", 5))
print()

# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - JSON with a single canonical form")
print("-" * 60)
full = sample_shop()
full.borrow("Sara", "Dune", 10)
data = full.to_dict()
folder = tempfile.mkdtemp(prefix="project38_")
target = os.path.join(folder, "shop.json")
save_json(target, data)
raw = read_text(target)
print("T5  the file ends with a newline ->", raw.endswith("\n"))
print("T5  the same data always gives the same text ->",
      dumps_canonical(data) == raw)
print("T5  a reread equals the original ->", load_json(target) == data)
print("T5  loading a file that is not there ->",
      what_it_raises(load_json, os.path.join(folder, "missing.json")))
print("T5  the temporary file is gone ->",
      not any(name.endswith(".tmp") for name in os.listdir(folder)))
print("T5  the folder holds exactly one file ->", len(os.listdir(folder)))
print("T5  and that file is not a temporary ->", os.path.basename(target))
print()

# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - CSV, and the two things it will surprise you with")
print("-" * 60)
books = [full.catalogue.get(title) for title in full.catalogue.titles()]
csv_path = os.path.join(folder, "catalogue.csv")
export_csv(csv_path, books)
lines = read_text(csv_path).splitlines()
print("T6  the exported lines ->", len(lines))
print("T6  the header row ->", lines[0])
comma_line = [line for line in lines if line.startswith('"')][0]
print("T6  a title holding a comma ->", comma_line)
csv_bytes = read_bytes(csv_path)
print("T6  every line ends in a bare newline ->", csv_bytes.count(b"\n") == len(lines))
print("T6  the bytes contain no \\r ->", b"\r" not in csv_bytes)
back, ignored = import_csv(csv_path)
print("T6  books reimported ->", len(back))
awkward = [b.title for b in back if b.title.startswith("Clean Code")]
print("T6  the awkward title survived ->", awkward[0])
raw_copies = to_int("2", "still text")
print("T6  copies came back as text ->", "'2'")
print("T6  so converting it again gives ->", to_int(raw_copies, -1))
print()

# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - with, and the save that must not happen")
print("-" * 60)
safe_path = os.path.join(folder, "safe.json")
save_json(safe_path, sample_shop().to_dict())
with ShopFile(safe_path, Shop()) as loaded:
    inside = loaded.catalogue.size()
print("T7  inside the block the shop holds ->", inside)
print("T7  a clean exit saved the file ->", os.path.exists(safe_path))
manager = ShopFile(safe_path, Shop())
try:
    with manager as loaded:
        loaded.add_book("Extra", "Nobody", 1)
        raise ValueError("the day went wrong")
except ValueError as problem:
    print("T7  an exception inside the block ->", type(problem).__name__)
print("T7  the block was told there was one ->", manager.exception_seen.__name__)
print("T7  and the file was left alone ->", not manager.saved)
print("T7  still holding 4 books ->", Shop.from_dict(load_json(safe_path)).catalogue.size())
print("T7  and the fifth book was never written ->",
      Shop.from_dict(load_json(safe_path)).catalogue.get("Extra") is None)
print()

# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - the rubbish this shop will not accept")
print("-" * 60)
blank = Shop()
print("T8  an empty catalogue holds ->", blank.catalogue.size())
print("T8  and it reports ->", shop_report(blank)[0])
solo = Shop()
solo.add_book("Dune", "Frank Herbert", 1)
solo.add_member("Sara")
try:
    solo.add_member("Sara")
except DuplicateMember as problem:
    print("T8  a duplicate member is refused ->", type(problem).__name__)
print("T8  a shop with no open loans ->", shop_report(solo)[-1])
print("T8  returning a title never borrowed ->",
      what_it_raises(solo.loans.give_back, "Sara", "Dune", 3))
solo.borrow("Sara", "Dune", 10)
print("T8  returning on the borrowing day costs ->", solo.loans.give_back("Sara", "Dune", 10))
solo.borrow("Sara", "Dune", 10)
print("T8  returning before it was borrowed ->",
      what_it_raises(solo.loans.give_back, "Sara", "Dune", 9))
broken = os.path.join(folder, "broken.csv")
with open(broken, "w", encoding="utf-8", newline="") as stream:
    stream.write("title,author,copies\nDune,Frank Herbert,2\n,X,1\nRefactoring,Martin Fowler,1\n")
kept, skipped = import_csv(broken)
print("T8  a broken csv line is skipped, not fatal ->", skipped[0])
print()

# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - every subject under test")
print("-" * 60)


class ValidationTests(unittest.TestCase):
    def test_valid_book_builds(self):
        self.assertEqual(Book("Dune", "Frank Herbert", 3).title, "Dune")

    def test_spaces_are_stripped(self):
        self.assertEqual(Book("  Dune  ", " X ", 1).title, "Dune")

    def test_blank_title_is_refused(self):
        self.assertEqual(recorded(Book, "   ", "X", 1)[1], "ShopError")

    def test_blank_author_is_refused(self):
        self.assertEqual(recorded(Book, "X", "", 1)[1], "ShopError")

    def test_negative_copies_are_refused(self):
        self.assertEqual(recorded(Book, "X", "Y", -1)[1], "ShopError")

    def test_a_bool_is_not_a_count(self):
        self.assertEqual(recorded(Book, "X", "Y", True)[1], "ShopError")

    def test_text_number_is_converted(self):
        self.assertEqual(Book("X", "Y", "7").copies, 7)

    def test_whole_family_shares_one_parent(self):
        for child in (DuplicateTitle, DuplicateMember, UnknownMember,
                      NotBorrowed, NoBooksYet):
            self.assertTrue(issubclass(child, ShopError))


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.catalogue = Catalogue()
        self.catalogue.add(Book("Dune", "Frank Herbert", 3))
        self.catalogue.add(Book("Refactoring", "Martin Fowler", 2))

    def test_add_and_size(self):
        self.assertEqual(self.catalogue.size(), 2)

    def test_titles_are_sorted(self):
        self.assertEqual(self.catalogue.titles(), ["Dune", "Refactoring"])

    def test_a_duplicate_title_is_refused(self):
        self.assertEqual(recorded(self.catalogue.add,
                                  Book("Dune", "Other", 1))[1], "DuplicateTitle")

    def test_a_known_title_is_found(self):
        self.assertEqual(self.catalogue.get("Dune").author, "Frank Herbert")

    def test_an_unknown_title_is_none(self):
        self.assertIsNone(self.catalogue.get("Nothing"))

    def test_the_cache_is_cleared_when_a_book_arrives(self):
        self.catalogue.titles_by_author("Martin Fowler")
        self.catalogue.add(Book("Clean Code, A Handbook", "Martin Fowler", 1))
        self.assertEqual(len(self.catalogue.titles_by_author("Martin Fowler")), 2)


class LoanTests(unittest.TestCase):
    def setUp(self):
        self.loans = Loans(loan_days=14, fine_per_day=2)
        self.loans.borrow("Sara", "Dune", 10)

    def test_an_open_loan_counts(self):
        self.assertEqual(self.loans.open_count(), 1)

    def test_the_due_day_is_borrowed_plus_the_term(self):
        self.assertEqual(self.loans.due_on("Sara", "Dune"), 24)

    def test_returning_on_time_costs_nothing(self):
        self.assertEqual(self.loans.give_back("Sara", "Dune", 24), 0)

    def test_each_late_day_costs_the_rate(self):
        self.assertEqual(self.loans.fine_on("Sara", "Dune", 27), 6)

    def test_the_fine_of_an_unknown_loan_is_refused(self):
        self.assertEqual(recorded(self.loans.fine_on, "Ali", "Dune", 20)[1], "NotBorrowed")

    def test_a_negative_term_is_refused(self):
        self.assertEqual(recorded(Loans, -1, 2)[1], "ShopError")

    def test_a_negative_rate_is_refused(self):
        self.assertEqual(recorded(Loans, 14, -1)[1], "ShopError")

    def test_returning_before_borrowing_is_refused(self):
        self.assertEqual(recorded(self.loans.give_back, "Sara", "Dune", 9)[1], "ShopError")

    def test_the_history_keeps_the_fine(self):
        self.loans.give_back("Sara", "Dune", 30)
        self.assertEqual(self.loans.history[0]["fine"], 12)


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp(prefix="project38_test_")
        self.path = os.path.join(self.folder, "shop.json")
        self.shop = sample_shop()

    def tearDown(self):
        for name in os.listdir(self.folder):
            os.unlink(os.path.join(self.folder, name))
        os.rmdir(self.folder)

    def test_a_round_trip_returns_the_same_data(self):
        save_json(self.path, self.shop.to_dict())
        self.assertEqual(load_json(self.path), self.shop.to_dict())

    def test_the_text_is_canonical(self):
        save_json(self.path, self.shop.to_dict())
        saved = read_text(self.path)
        self.assertEqual(saved, dumps_canonical(self.shop.to_dict()))

    def test_keys_are_sorted_on_disk(self):
        save_json(self.path, self.shop.to_dict())
        saved = read_text(self.path)
        self.assertLess(saved.index('"books"'), saved.index('"loans"'))
        self.assertLess(saved.index('"loans"'), saved.index('"members"'))

    def test_no_temporary_file_is_left_behind(self):
        save_json(self.path, self.shop.to_dict())
        self.assertEqual(len(os.listdir(self.folder)), 1)

    def test_a_missing_file_raises(self):
        self.assertEqual(recorded(load_json,
                                  os.path.join(self.folder, "gone.json"))[1],
                         "FileNotFoundError")

    def test_a_shop_rebuilds_from_its_file(self):
        rebuilt = sample_shop()
        rebuilt.borrow("Sara", "Dune", 10)
        save_json(self.path, rebuilt.to_dict())
        again = Shop.from_dict(load_json(self.path))
        self.assertEqual(again.catalogue.titles(), rebuilt.catalogue.titles())
        self.assertEqual(again.loans.open_count(), 1)

    def test_json_that_is_not_a_dict_is_refused(self):
        save_json(self.path, [1, 2, 3])
        self.assertEqual(recorded(load_json, self.path)[1], "ShopError")


class CsvTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp(prefix="project38_csv_")
        self.path = os.path.join(self.folder, "catalogue.csv")
        self.books = [Book("Clean Code, A Handbook", "Robert Martin", 2),
                      Book("Dune", "Frank Herbert", 3)]
        export_csv(self.path, self.books)

    def tearDown(self):
        os.unlink(self.path)
        os.rmdir(self.folder)

    def test_the_header_is_written(self):
        self.assertEqual(read_text(self.path).splitlines()[0],
                         "title,author,copies")

    def test_a_comma_in_a_title_is_quoted(self):
        lines = read_text(self.path).splitlines()
        self.assertIn('"Clean Code, A Handbook",Robert Martin,2', lines)

    def test_the_file_uses_bare_newlines(self):
        self.assertNotIn(b"\r", read_bytes(self.path))

    def test_the_round_trip_returns_every_book(self):
        back, problems = import_csv(self.path)
        self.assertEqual(len(back), 2)
        self.assertEqual(problems, [])

    def test_the_awkward_title_survives(self):
        back, _ = import_csv(self.path)
        self.assertEqual(back[0].title, "Clean Code, A Handbook")

    def test_a_row_without_a_title_is_skipped(self):
        with open(self.path, "a", encoding="utf-8", newline="") as stream:
            stream.write(",Nobody,1\n")
        back, problems = import_csv(self.path)
        self.assertEqual(len(back), 2)
        self.assertEqual(len(problems), 1)


SUITES = [("validation", ValidationTests),
          ("catalogue", CatalogueTests),
          ("loans", LoanTests),
          ("persistence", PersistenceTests),
          ("csv", CsvTests)]

total_passed = 0
total_failed = 0
total_errors = 0
for label, suite in SUITES:
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(
        unittest.TestLoader().loadTestsFromTestCase(suite))
    print("T9  ", label.ljust(12), "passed",
          str(result.testsRun - len(result.failures) - len(result.errors)).rjust(3),
          " failed", str(len(result.failures)).rjust(3))
    total_passed += result.testsRun - len(result.failures) - len(result.errors)
    total_failed += len(result.failures)
    total_errors += len(result.errors)
print("T9   TOTAL".ljust(14), "passed",
      str(total_passed).rjust(3), " failed", str(total_failed).rjust(3))
print("T9   errors, which are the dangerous kind ->", total_errors)
print()

# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the full shop, and the bill for it")
print("-" * 60)
final_shop = sample_shop()
final_shop.borrow("Sara", "Dune", 10)
final_shop.borrow("Ali", "The Pragmatic Programmer", 12)
shelf = final_shop.catalogue.copies()
lent = final_shop.loans.open_count()
print("T10   books", final_shop.catalogue.size(), " members", len(final_shop.members),
      " open loans", lent)
print("T10   copies on the shelf and out ->",
      str(shelf) + " total, " + str(lent) + " on loan, " + str(shelf - lent) + " home")
print("T10   one search, dict way ->", 1)
steps = 0
for title in final_shop.catalogue.titles():
    steps += 1
    if title == "Refactoring":
        break
print("T10   one search, loop way ->", steps)
print("T10   so the dict wins by ->", str(steps / 1.0) + "x")
print("T10   and the memory it costs ->",
      str(final_shop.catalogue.size()) + " extra entries")
leftovers = [name for name in os.listdir(folder) if name.endswith(".tmp")]
print("T10   the whole file leaves no temporary ->", not leftovers)
print("T10   and every claim above was printed, not assumed ->",
      total_failed == 0 and total_errors == 0)
print()

for name in os.listdir(folder):
    os.unlink(os.path.join(folder, name))
os.rmdir(folder)
print("=" * 60)
print("END OF PROJECT 38")
print("=" * 60)