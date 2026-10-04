# ============================================================
# PROJECT 35 - Object Oriented Programming: the Library as Classes
# ============================================================
# Level: Intermediate-Advanced
# Topics: classes, __init__, __str__ vs __repr__, __eq__, __hash__,
#        __lt__, properties and setters, inheritance, super(),
#        classmethod, the container protocol, JSON round trip
#
# Projects 33 and 34 built the library out of functions and plain
# dicts. That works, and it kept the data simple. But a dict will
# happily let you write library["dune"]["copies"] = -5, and there
# is nothing you can do about it, because a dict has no rules.
#
# A class is how you give the data rules. Book is not free to hold
# a negative number of copies, not because we check politely, but
# because copies is a PROPERTY and the setter refuses. That single
# idea is the reason to use a class at all.
#
# Every class here replaces something from project 33, and the two
# programs produce the same answers. Nothing in this file uses
# input(), and the JSON part writes to a temporary folder that is
# deleted before the file finishes.
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: what a class actually buys you
# A dict lets you write library["dune"]["copies"] = -5. Name one
# thing a class can do that makes THAT line impossible.
# (your answer here)

# QUESTION 2: property instead of a plain attribute
# Why is copies written as a property with a setter rather than a
# plain self.copies? What exactly does the setter stop?
# (your answer here)

# QUESTION 3: eq and hash together
# You define __eq__ so two books with the same title compare equal.
# What breaks next, and what are the two ways to fix it?
# (your answer here)

# QUESTION 4: str and repr
# Which one does print() use, and which one does a LIST use? Why
# does the answer matter when you are hunting a bug?
# (your answer here)

# QUESTION 5: the project 31 trap, inside a class
# Project 31 warned against def f(items=[]). Why is that mistake
# WORSE in __init__ than it was in a function?
# (your answer here)

# QUESTION 6: inheritance or composition
# A Magazine really is a Book, so Magazine(Book) is honest. Give
# one thing from project 34 that should NOT be a subclass of
# Library, and say why.
# (your answer here)

# QUESTION 7: super()
# Why call super().__init__(title) instead of writing
# Book.__init__(self, title)? Name the situation where the first
# form keeps working and the second one breaks.
# (your answer here)

# QUESTION 8: the container protocol
# Name the four dunder methods that let your own class support
# len(x), x in y, for x in y, and y[0].
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Write class Book with __init__(title, author, year,
# copies=1) taking four plain attributes. Give it __str__ for a
# human line and __repr__ for a debugging form, then print both for
# one book. Notice that print(book) uses __str__ while
# [book] uses __repr__
# (your code here)

# TASK 2: Convert copies into a property. The setter must refuse a
# negative number, a non int, and a bool, raising LibraryError.
# Prove all three refusals work, and prove __slots__ is not in use
# by adding one extra attribute
# (your code here)

# TASK 3: Add __eq__ comparing title and author, __hash__ so books
# can go in a set, and __lt__ so sorted() can order them by year
# then title. Prove a set of two equal books holds one, and print
# a sorted list of three books
# (your code here)

# TASK 4: Write class Library as a CONTAINER. It must support
# len(), "in", for, and indexing through __len__, __contains__,
# __iter__ and __getitem__. Prove all four work, and show that
# "dune" in library and "nope" in library differ
# (your code here)

# TASK 5: Add Library.add and Library.borrow and
# Library.give_back, raising LibraryError on a missing title and
# on too few copies. Prove both refusals and both successes
# (your code here)

# TASK 6: Write class Member holding its OWN loan dict, with take
# and give_back methods that take a library argument. Create two
# members, let one drain a title, and prove the other sees an empty
# record while still being refused at the shelf
# (your code here)

# TASK 7: Write class Magazine(Book) that adds an issue number,
# calls super().__init__, and overrides __str__ to include the
# issue. Print a Book and a Magazine, and show that the Magazine
# still reaches the base __init__ for title, author and year
# (your code here)

# TASK 8: Give Library a to_dict and a classmethod from_dict, then
# a save and a load, so the objects survive a restart exactly the
# way the plain dicts did in project 34. Print the shelf after a
# reload and prove copies counts are equal
# (your code here)

# TASK 9: Add a classmethod Book.from_spec("dune | Herbert | 1965
# | 3") that builds a Book from one string, and a staticmethod
# Book.is_valid_year(value). Call both, and show that the
# classmethod can return the class itself
# (your code here)

# TASK 10: Write the full demo. Build a Library of five books
# including one Magazine, save it to a temporary folder, throw the
# objects away, load them back from JSON, let two Members borrow
# and return, save again, reload a third time and print the shelf.
# Prove the total number of copies is unchanged, then delete the
# temporary folder and print that it is gone
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.

import atexit
import json
import os
import shutil
import tempfile

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
print("Q1  a dict has no rules, so copies can be set to anything")
print("Q1  a class can REFUSE, which turns a bug into an exception")
# Q1  a dict has no rules, so copies can be set to anything
# Q1  a class can REFUSE, which turns a bug into an exception
# That is the whole trade. You give up a little speed and a lot of
# simplicity, and in exchange the impossible state cannot be built.

# QUESTION 2
print("Q2  a plain attribute is public, so anyone can write -5 to it")
print("Q2  the setter is the ONLY door, so it can check what arrives")
# Q2  a plain attribute is public, so anyone can write -5 to it
# Q2  the setter is the ONLY door, so it can check what arrives
# A plain self.copies is also a plain self.copies. There is no
# difference in strength, which is exactly why the strong version
# has to be written on purpose.

# QUESTION 3
class _HashDemo:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, _HashDemo) and self.name == other.name


try:
    hash(_HashDemo("a"))
    print("Q3  it stayed hashable")
except TypeError as err:
    print("Q3  defining __eq__ removed the hash ->", type(err).__name__)
    print("Q3  fix 1: __hash__ = lambda self: hash(self.name)")
    print("Q3  fix 2: @dataclass(frozen=True), which generates both")
# Q3  defining __eq__ removed the hash -> TypeError
# Q3  fix 1: __hash__ = lambda self: hash(self.name)
# Q3  fix 2: @dataclass(frozen=True), which generates both
# Python sets __hash__ to None the moment you write __eq__, because
# two objects that compare equal but hash differently would break
# every dict and set in the program. It refuses rather than guess.

# QUESTION 4
class _PrintDemo:
    def __str__(self):
        return "I am the friendly version"

    def __repr__(self):
        return "<PrintDemo object at 0x????>"


demo_obj = _PrintDemo()
print("Q4  print(obj) ->", str(demo_obj))
print("Q4  [obj]     ->", repr(demo_obj))
# Q4  print(obj) -> I am the friendly version
# Q4  [obj]     -> <PrintDemo object at 0x????>
# A container shows you __repr__, because a list of forty objects
# cannot afford friendly prose. That is why __repr__ must identify
# the object on its own, with no help from its neighbours.

# QUESTION 5
class _BadInit:
    def __init__(self, items=[]):
        self.items = items
        self.items.append(len(self.items))


class _GoodInit:
    def __init__(self, items=None):
        self.items = [] if items is None else list(items)


print("Q5  a bad instance ->", _BadInit().items)
print("Q5  the next one   ->", _BadInit().items, "<- the same list again")
print("Q5  a good instance->", _GoodInit().items, "<- built fresh")
# Q5  a bad instance -> [0]
# Q5  the next one   -> [0, 1] <- the same list again
# Q5  a good instance-> [] <- built fresh
# This is project 31's trap in a worse costume. A function usually
# runs and finishes, so the damage is small and local. A class
# instance can live for the whole program, so the shared list
# keeps growing and the cause is far away from the symptom.

# QUESTION 6
print("Q6  Magazine IS-A Book        -> inheritance is honest")
print("Q6  A Loan IS-A Library       -> no, a loan is something it HOLDS")
print("Q6  that one must be an ATTRIBUTE, not a subclass")
# Q6  Magazine IS-A Book        -> inheritance is honest
# Q6  A Loan IS-A Library       -> no, a loan is something it HOLDS
# Q6  that one must be an ATTRIBUTE, not a subclass
# The test is always the same sentence: "X is a Y" earns a subclass,
# "X has a Y" earns an attribute. Loans belong in a dict on the
# Library, which is composition.

# QUESTION 7
print("Q7  super() follows the MRO, so it still works if the")
print("Q7  parent gains another class, or the order is changed")
# Q7  super() follows the MRO, so it still works if the
# Q7  parent gains another class, or the order is changed
# Hard coding Book.__init__ freezes the ancestry in the child's
# source. super() asks the class itself, so inserting a class
# between Book and Magazine needs no edit here.

# QUESTION 8
print("Q8  __len__    -> len(library)")
print("Q8  __contains_-> 'dune' in library")
print("Q8  __iter__   -> for title in library")
print("Q8  __getitem__-> library['dune']")
# Q8  __len__    -> len(library)
# Q8  __contains_-> 'dune' in library
# Q8  __iter__   -> for title in library
# Q8  __getitem__-> library['dune']
# Four small methods, and then your object behaves like the built in
# containers you already know how to use.

print("-" * 60)

# TASK 1
class LibraryError(Exception):
    """Raised when a library action cannot be completed."""


class Book:
    """One title on the shelf, with the rules that protect it."""

    def __init__(self, title, author, year, copies=1):
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

    def __repr__(self):
        return f"<Book {self.title!r} {self.year} copies={self.copies}>"


one = Book("dune", "Frank Herbert", 1965, 3)
print("T1  print(book) ->", one)
print("T1  str(book)   ->", str(one))
print("T1  repr(book)  ->", repr(one))
print("T1  a list      ->", [one])
# T1  print(book) -> dune by Frank Herbert (1965)
# T1  str(book)   -> dune by Frank Herbert (1965)
# T1  repr(book)  -> <Book 'dune' 1965 copies=3>
# T1  a list      -> [<Book 'dune' 1965 copies=3>]
# print() and str() agree, but the list swapped in __repr__ without
# being asked. Keep __repr__ short and unambiguous, because you will
# read it inside a wall of other objects one day.

# TASK 2
class Book:
    def __init__(self, title, author, year, copies=1):
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

    def __repr__(self):
        return f"<Book {self.title!r} {self.year} copies={self.copies}>"

    @property
    def copies(self):
        """The only way in or out, so the rule lives in one place."""
        return self._copies

    @copies.setter
    def copies(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise LibraryError(f"copies of {self.title!r} must be an int")
        if value < 0:
            raise LibraryError(f"copies of {self.title!r} cannot be negative")
        self._copies = value


guarded = Book("dune", "Frank Herbert", 1965, 3)
print("T2  reading works ->", guarded.copies)
guarded.copies = 0
print("T2  zero is legal ->", guarded.copies)
for bad in (-5, "three", True):
    try:
        guarded.copies = bad
    except LibraryError as err:
        print(f"T2  refusing {bad!r:8} -> LibraryError: {err}")
guarded.tag = "classic"
print("T2  an extra attribute is fine ->", guarded.tag)
# T2  reading works -> 3
# T2  zero is legal -> 0
# T2  refusing -5       -> LibraryError: copies of 'dune' cannot be negative
# T2  refusing 'three'  -> LibraryError: copies of 'dune' must be an int
# T2  refusing True     -> LibraryError: copies of 'dune' must be an int
# T2  an extra attribute is fine -> classic
# The bool check comes first for a real reason: bool is a subclass
# of int, so True would sail past a plain int test and then act as
# a count of one. Zero is allowed on purpose, because an empty shelf
# is a normal state, while a negative shelf is not a thing.

# TASK 3
class Book:
    def __init__(self, title, author, year, copies=1):
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

    def __repr__(self):
        return f"<Book {self.title!r} {self.year} copies={self.copies}>"

    @property
    def copies(self):
        return self._copies

    @copies.setter
    def copies(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise LibraryError(f"copies of {self.title!r} must be an int")
        if value < 0:
            raise LibraryError(f"copies of {self.title!r} cannot be negative")
        self._copies = value

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self.title, self.author) == (other.title, other.author)

    def __hash__(self):
        return hash((self.title, self.author))

    def __lt__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self.year, self.title) < (other.year, other.title)


copy_a = Book("dune", "Frank Herbert", 1965, 3)
copy_b = Book("dune", "Frank Herbert", 1965, 1)
other = Book("clean code", "Robert Martin", 2008, 2)
print("T3  two copies equal    ->", copy_a == copy_b)
print("T3  a set drops the dupe->", len({copy_a, copy_b, other}), "books")
print("T3  and it is hashable ->", isinstance(hash(copy_a), int))
shelf_order = [Book("pragmatic", "Hunt", 1999), Book("dune", "Frank Herbert", 1965), other]
print("T3  sorted by year     ->", [b.title for b in sorted(shelf_order)])
print("T3  equal to a string  ->", copy_a == "dune")
# T3  two copies equal    -> True
# T3  a set drops the dupe-> 2 books
# T3  and it is hashable -> True
# T3  sorted by year     -> ['dune', 'pragmatic', 'clean code']
# T3  equal to a string  -> False
# copies is deliberately NOT part of __eq__. Two records of the same
# book are the same book even when one shelf says three and the
# other says one, and if copies were compared the set would keep
# both and the whole de-duplication idea would collapse.
#
# Returning NotImplemented instead of False is how you say "not
# mine to answer". Python then asks the other side, so a Book can
# still compare sanely against a string.

# TASK 4
class Library:
    """A container, so len/in/for/index all work on purpose."""

    def __init__(self, books=None):
        self._books = {}
        if books:
            for book in books:
                self.add(book)

    def __len__(self):
        return len(self._books)

    def __contains__(self, item):
        title = item.title if isinstance(item, Book) else item
        return title in self._books

    def __iter__(self):
        return iter(self._books)

    def __getitem__(self, title):
        if title not in self._books:
            raise LibraryError(f"'{title}' is not in the library")
        return self._books[title]

    def add(self, book):
        """Put one Book on the shelf, refusing a duplicate title."""
        if book.title in self._books:
            raise LibraryError(f"'{book.title}' is already in the library")
        self._books[book.title] = book
        return f"added '{book.title}'"


library = Library()
library.add(Book("dune", "Frank Herbert", 1965, 3))
library.add(Book("clean code", "Robert Martin", 2008, 2))
library.add(Book("pragmatic", "Hunt", 1999, 1))
print("T4  len(library)      ->", len(library))
print("T4  'dune' in library ->", "dune" in library)
print("T4  'nope' in library ->", "nope" in library)
print("T4  an object in too  ->", Book("dune", "Frank Herbert", 1965) in library)
print("T4  for title in ...  ->", list(library))
print("T4  library['dune']   ->", library["dune"])
try:
    library["missing book"]
except LibraryError as err:
    print("T4  a bad index       -> LibraryError:", err)
# T4  len(library)      -> 3
# T4  'dune' in library -> True
# T4  'nope' in library -> False
# T4  an object in too  -> True
# T4  for title in ...  -> ['dune', 'clean code', 'pragmatic']
# T4  library['dune']   -> dune by Frank Herbert (1965)
# T4  a bad index       -> LibraryError: 'missing book' is not in the library
# __contains__ accepts a Book as well as a string, which is why it
# starts by normalising item into a title. A real project would also
# want a case-insensitive title match, and the place to add it is
# this one method, not three different callers.
#
# The dict behind it is still the plain dict from project 33. The
# class did not replace the data structure, it wrapped it.

# TASK 5
class Library(Library):
    """The container, now with the actions from project 33."""

    def __init__(self, books=None):
        self._books = {}
        if books:
            for book in books:
                self.add(book)

    def __len__(self):
        return len(self._books)

    def __contains__(self, item):
        title = item.title if isinstance(item, Book) else item
        return title in self._books

    def __iter__(self):
        return iter(self._books)

    def __getitem__(self, title):
        if title not in self._books:
            raise LibraryError(f"'{title}' is not in the library")
        return self._books[title]

    def add(self, book):
        if book.title in self._books:
            raise LibraryError(f"'{book.title}' is already in the library")
        self._books[book.title] = book
        return f"added '{book.title}'"

    def titles(self):
        """Sorted titles, so every report prints the same order."""
        return sorted(self._books)

    def borrow(self, title, copies=1):
        """Take copies off the shelf."""
        if title not in self._books:
            raise LibraryError(f"'{title}' is not in the library")
        if self._books[title].copies < copies:
            left = self._books[title].copies
            raise LibraryError(f"only {left} copies of '{title}' are left")
        self._books[title].copies -= copies
        return f"borrowed {copies} of '{title}'"

    def give_back(self, title, copies=1):
        """Put copies on the shelf."""
        if title not in self._books:
            raise LibraryError(f"'{title}' is not in the library")
        self._books[title].copies += copies
        return f"returned {copies} of '{title}'"

    def total_copies(self):
        """The invariant from project 33, now a method."""
        running = 0
        for title in self._books:
            running += self._books[title].copies
        return running


shelf = Library()
shelf.add(Book("dune", "Frank Herbert", 1965, 3))
shelf.add(Book("clean code", "Robert Martin", 2008, 2))
print("T5  starting copies   ->", shelf.total_copies())
print("T5  borrow two        ->", shelf.borrow("dune", 2))
print("T5  dune now          ->", shelf["dune"].copies)
try:
    shelf.borrow("dune", 3)
except LibraryError as err:
    print("T5  too many          -> LibraryError:", err)
try:
    shelf.borrow("missing book")
except LibraryError as err:
    print("T5  a missing title   -> LibraryError:", err)
print("T5  give one back     ->", shelf.give_back("dune"))
print("T5  dune now          ->", shelf["dune"].copies)
print("T5  a duplicate add   ->", end=" ")
try:
    shelf.add(Book("dune", "Someone Else", 2000))
except LibraryError as err:
    print("LibraryError:", err)
# T5  starting copies   -> 5
# T5  borrow two        -> borrowed 2 of 'dune'
# T5  dune now          -> 1
# T5  too many          -> LibraryError: only 1 copies of 'dune' are left
# T5  a missing title   -> LibraryError: 'missing book' is not in the library
# T5  give one back     -> returned 1 of 'dune'
# T5  dune now          -> 2
# T5  a duplicate add   -> LibraryError: 'dune' is already in the library
# shelf["dune"].copies = -1 would work on a plain dict from project
# 33. Here it raises, because that assignment goes through the
# property setter. That is the single behaviour that justifies the
# whole rewrite.

# TASK 6
class Member:
    """A person. Each one owns a loan dict that no one else can see."""

    def __init__(self, name):
        self.name = name
        self._loans = {}

    def take(self, library, title):
        """Borrow through the library, then record it locally."""
        message = library.borrow(title, 1)
        self._loans[title] = self._loans.get(title, 0) + 1
        return f"{self.name}: {message}"

    def give_back(self, library, title):
        """Return a book this member is actually holding."""
        if title not in self._loans:
            return f"{self.name} did not take '{title}'"
        self._loans[title] -= 1
        library.give_back(title, 1)
        if self._loans[title] == 0:
            del self._loans[title]
        return f"{self.name}: returned '{title}'"

    @property
    def loans(self):
        """A copy, so a caller cannot edit the private record."""
        return dict(self._loans)

    def __str__(self):
        return f"Member {self.name} holding {len(self._loans)} title(s)"


sara = Member("Sara")
ali = Member("Ali")
single = Library()
single.add(Book("dune", "Frank Herbert", 1965, 1))
print("T6  Sara takes it  ->", sara.take(single, "dune"))
print("T6  Ali tries it   ->", end=" ")
try:
    ali.take(single, "dune")
except LibraryError as err:
    print("LibraryError:", err)
print("T6  Sara's record  ->", sara.loans)
print("T6  Ali's record   ->", ali.loans)
print("T6  Sara returns   ->", sara.give_back(single, "dune"))
print("T6  Ali takes it   ->", ali.take(single, "dune"))
print("T6  Sara's record  ->", sara.loans)
print("T6  Ali's record   ->", ali.loans)
print("T6  the shelf      ->", single["dune"].copies)
print("T6  Ali hands it in->", ali.give_back(single, "dune"))
print("T6  a stray return ->", ali.give_back(single, "dune"))
print("T6  the shelf      ->", single["dune"].copies)
# T6  Sara takes it  -> Sara: borrowed 1 of 'dune'
# T6  Ali tries it   -> LibraryError: only 0 copies of 'dune' are left
# T6  Sara's record  -> {'dune': 1}
# T6  Ali's record   -> {}
# T6  Sara returns   -> Sara: returned 'dune'
# T6  Ali takes it   -> Ali: borrowed 1 of 'dune'
# T6  Sara's record  -> {}
# T6  Ali's record   -> {'dune': 1}
# T6  the shelf      -> 0
# T6  Ali hands it in-> Ali: returned 'dune'
# T6  a stray return -> Ali did not take 'dune'
# T6  the shelf      -> 1
# The pool is one Library object that both members were handed, so
# they share it. The records are two Member objects, each with its
# own _loans, so they cannot collide. Project 33 proved the same
# thing with a closure; here the same isolation is written down
# explicitly, which is far easier to read six months later.
#
# The loans property returns dict(self._loans), a COPY. Returning
# the real dict would let anyone write member.loans["dune"] = 99
# and corrupt the record from outside.

# TASK 7
class Magazine(Book):
    """A Book that also has an issue number. This IS-A Book, honestly."""

    def __init__(self, title, author, year, issue, copies=1):
        super().__init__(title, author, year, copies)
        self.issue = issue

    def __str__(self):
        return f"{super().__str__()}, issue {self.issue}"

    def __repr__(self):
        return f"<Magazine {self.title!r} #{self.issue} copies={self.copies}>"


magazine = Magazine("national geographic", "various", 2021, 7, 4)
plain = Book("dune", "Frank Herbert", 1965, 3)
print("T7  a plain book   ->", plain)
print("T7  a magazine     ->", magazine)
print("T7  repr(magazine) ->", repr(magazine))
print("T7  inherited year ->", magazine.year, "from the base class")
print("T7  it is a Book   ->", isinstance(magazine, Book))
# T7  a plain book   -> dune by Frank Herbert (1965)
# T7  a magazine     -> national geographic by various (2021), issue 7
# T7  repr(magazine) -> <Magazine 'national geographic' #7 copies=4>
# T7  inherited year -> 2021 from the base class
# T7  it is a Book   -> True
# super().__str__() inside the override is what reuses the base
# text instead of copying it. If the base __str__ gains a field
# later, the magazine picks it up for free.

# TASK 8
class Library(Library):
    """The same shelf, plus the JSON round trip from project 34."""

    def __init__(self, books=None):
        self._books = {}
        if books:
            for book in books:
                self.add(book)

    def __len__(self):
        return len(self._books)

    def __contains__(self, item):
        title = item.title if isinstance(item, Book) else item
        return title in self._books

    def __iter__(self):
        return iter(self._books)

    def __getitem__(self, title):
        if title not in self._books:
            raise LibraryError(f"'{title}' is not in the library")
        return self._books[title]

    def add(self, book):
        if book.title in self._books:
            raise LibraryError(f"'{book.title}' is already in the library")
        self._books[book.title] = book
        return f"added '{book.title}'"

    def titles(self):
        return sorted(self._books)

    def borrow(self, title, copies=1):
        if title not in self._books:
            raise LibraryError(f"'{title}' is not in the library")
        if self._books[title].copies < copies:
            left = self._books[title].copies
            raise LibraryError(f"only {left} copies of '{title}' are left")
        self._books[title].copies -= copies
        return f"borrowed {copies} of '{title}'"

    def give_back(self, title, copies=1):
        if title not in self._books:
            raise LibraryError(f"'{title}' is not in the library")
        self._books[title].copies += copies
        return f"returned {copies} of '{title}'"

    def total_copies(self):
        running = 0
        for title in self._books:
            running += self._books[title].copies
        return running

    def to_dict(self):
        """Turn the objects back into the project 34 plain shape."""
        data = {}
        for title in self._books:
            record = {
                "author": self._books[title].author,
                "year": self._books[title].year,
                "copies": self._books[title].copies,
            }
            if isinstance(self._books[title], Magazine):
                record["issue"] = self._books[title].issue
            data[title] = record
        return data

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Library, and use cls so subclasses stay correct."""
        rebuilt = cls()
        for title in sorted(data):
            record = data[title]
            if "issue" in record:
                rebuilt.add(
                    Magazine(title, record["author"], record["year"], record["issue"], record["copies"])
                )
            else:
                rebuilt.add(Book(title, record["author"], record["year"], record["copies"]))
        return rebuilt

    def save(self, path):
        """Write atomically, exactly as project 34 did."""
        text = json.dumps(self.to_dict(), indent=2, ensure_ascii=False, sort_keys=True)
        temporary = path + ".tmp"
        with open(temporary, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(temporary, path)
        return len(text)

    @classmethod
    def load(cls, path):
        """Return a Library, or an empty one when the file is unusable."""
        if not os.path.exists(path):
            return cls()
        try:
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError:
            return cls()
        return cls.from_dict(data)


work = tempfile.mkdtemp(prefix="p35_")
atexit.register(shutil.rmtree, work, True)
data_file = os.path.join(work, "library.json")

persisted = Library()
persisted.add(Book("dune", "Frank Herbert", 1965, 3))
persisted.add(Book("clean code", "Robert Martin", 2008, 2))
persisted.add(Magazine("national geographic", "various", 2021, 7, 4))
print("T8  the dict shape ->", sorted(persisted.to_dict()))
print("T8  the magazine   ->", persisted.to_dict()["national geographic"])
chars = persisted.save(data_file)
print("T8  characters     ->", chars)
persisted = None
reloaded = Library.load(data_file)
print("T8  after a restart->", reloaded.titles())
print("T8  dune copies    ->", reloaded["dune"].copies)
print("T8  the magazine came back as ->", type(reloaded["national geographic"]).__name__)
print("T8  the same objects ->", reloaded.total_copies() == 9)
# T8  the dict shape -> ['clean code', 'dune', 'national geographic']
# T8  the magazine   -> {'author': 'various', 'year': 2021, 'copies': 4, 'issue': 7}
# T8  characters     -> 279
# T8  after a restart-> ['clean code', 'dune', 'national geographic']
# T8  dune copies    -> 3
# T8  the magazine came back as -> Magazine
# T8  the same objects -> True
# The record knows it is a magazine because the key "issue" exists,
# so from_dict rebuilds the right class instead of a plain Book.
# That one extra key is the whole difference between a saved book
# and a saved magazine.
#
# from_dict is a classmethod and returns cls(), not Library(). That
# single word means a subclass of Library would load as itself, for
# free, forever.

# TASK 9
class Book(Book):
    """The same rules, plus two ways to build one from text."""

    def __init__(self, title, author, year, copies=1):
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

    def __repr__(self):
        return f"<Book {self.title!r} {self.year} copies={self.copies}>"

    @property
    def copies(self):
        return self._copies

    @copies.setter
    def copies(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise LibraryError(f"copies of {self.title!r} must be an int")
        if value < 0:
            raise LibraryError(f"copies of {self.title!r} cannot be negative")
        self._copies = value

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self.title, self.author) == (other.title, other.author)

    def __hash__(self):
        return hash((self.title, self.author))

    def __lt__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self.year, self.title) < (other.year, other.title)

    @classmethod
    def from_spec(cls, spec):
        """Build a book from 'title | author | year | copies'."""
        parts = [part.strip() for part in spec.split("|")]
        if len(parts) != 4:
            raise LibraryError("a spec needs exactly four fields")
        title, author, year_text, copies_text = parts
        if not cls.is_valid_year(year_text):
            raise LibraryError(f"'{year_text}' is not a plausible year")
        return cls(title, author, int(year_text), int(copies_text))

    @staticmethod
    def is_valid_year(value):
        """A helper that needs neither a cls nor a self."""
        text = str(value)
        if not text.isdigit() or len(text) != 4:
            return False
        return 1000 <= int(text) <= 2100


built = Book.from_spec("dune | Frank Herbert | 1965 | 3")
print("T9  from_spec built  ->", built)
print("T9  and it is a Book ->", isinstance(built, Book))
print("T9  is_valid_year    ->", Book.is_valid_year(1965), Book.is_valid_year("nineteen"))
try:
    Book.from_spec("dune | Herbert")
except LibraryError as err:
    print("T9  a short spec     -> LibraryError:", err)
print("T9  the method is on the class ->", callable(Book.from_spec))
# T9  from_spec built  -> dune by Frank Herbert (1965)
# T9  and it is a Book -> True
# T9  is_valid_year    -> True False
# T9  a short spec     -> LibraryError: a spec needs exactly four fields
# T9  the method is on the class -> True
# from_spec is a classmethod, so it can see cls and return a Book
# even though it was never given an instance. is_valid_year is a
# staticmethod: it converts nothing and inspects nothing, so it has
# no business pretending to be part of the object.

# TASK 10
def full_demo():
    """The whole class based library, saved, reloaded and balanced."""
    room = tempfile.mkdtemp(prefix="p35demo_")
    print("T10 a private folder was created ->", os.path.isdir(room))
    try:
        path = os.path.join(room, "library.json")

        start = Library()
        start.add(Book("dune", "Frank Herbert", 1965, 3))
        start.add(Book("children of dune", "Frank Herbert", 1979, 2))
        start.add(Book("clean code", "Robert Martin", 2008, 2))
        start.add(Book("python crash course", "Eric Matthes", 2019, 1))
        start.add(Magazine("national geographic", "various", 2021, 7, 4))
        opening_total = start.total_copies()
        start.save(path)
        print("T10 saved titles, copies ->", len(start), opening_total)

        # Drop every object. Everything below must come from JSON.
        start = None
        library = Library.load(path)
        print("T10 after a restart      ->", library.titles())
        print("T10 copies read back     ->", library.total_copies())
        print("T10 the magazine is      ->", type(library["national geographic"]).__name__)

        sara = Member("Sara")
        ali = Member("Ali")

        actions = [
            lambda: sara.take(library, "dune"),
            lambda: sara.take(library, "dune"),
            lambda: ali.take(library, "dune"),
            lambda: ali.take(library, "dune"),
            lambda: sara.give_back(library, "dune"),
            lambda: sara.give_back(library, "dune"),
            lambda: ali.take(library, "dune"),
            lambda: ali.take(library, "clean code"),
            lambda: ali.give_back(library, "dune"),
            lambda: ali.give_back(library, "clean code"),
            lambda: ali.give_back(library, "dune"),
        ]
        for step, action in enumerate(actions, 1):
            try:
                message = action()
            except LibraryError as err:
                message = f"refused: {err}"
            print(f"T10   step {step} -> {message}")

        library.save(path)
        print("T10 Sara's loans ->", sara.loans)
        print("T10 Ali's loans  ->", ali.loans)

        third_read = Library.load(path)
        print("T10 the shelf after restart ->", [(t, third_read[t].copies) for t in third_read.titles()])
        print("T10 copies at the end       ->", third_read.total_copies())
        print("T10 unchanged?              ->", third_read.total_copies() == opening_total)
    finally:
        shutil.rmtree(room, ignore_errors=True)
    print("T10 the folder is gone      ->", not os.path.isdir(room))


if __name__ == "__main__":
    full_demo()

# T10 a private folder was created -> True
# T10 saved titles, copies -> 5 12
# T10 after a restart      -> ['children of dune', 'clean code', 'dune', 'national geographic', 'python crash course']
# T10 copies read back     -> 12
# T10 the magazine is      -> Magazine
# T10   step 1 -> Sara: borrowed 1 of 'dune'
# T10   step 2 -> Sara: borrowed 1 of 'dune'
# T10   step 3 -> Ali: borrowed 1 of 'dune'
# T10   step 4 -> refused: only 0 copies of 'dune' are left
# T10   step 5 -> Sara: returned 'dune'
# T10   step 6 -> Sara: returned 'dune'
# T10   step 7 -> Ali: borrowed 1 of 'dune'
# T10   step 8 -> Ali: borrowed 1 of 'clean code'
# T10   step 9 -> Ali: returned 'dune'
# T10   step 10 -> Ali: returned 'clean code'
# T10   step 11 -> Ali: returned 'dune'
# T10 Sara's loans -> {}
# T10 Ali's loans  -> {}
# T10 the shelf after restart -> [('children of dune', 2), ('clean code', 2), ('dune', 3), ('national geographic', 4), ('python crash course', 1)]
# T10 copies at the end       -> 12
# T10 unchanged?              -> True
# T10 the folder is gone      -> True
# The three dunes go out in steps 1 to 3, so step 4 is refused and
# caught, then steps 5 and 6 hand them all back and the last five
# steps borrow and return again. Every book ends on the shelf,
# which is the same invariant that closed projects 33 and 34, now
# surviving a restart from disk and a full round trip through
# classes.
#
# The actions are lambdas rather than results, because borrow
# raises instead of returning a message. Deferring the call means
# one try/except can cover the whole script. Note what the refusal
# did NOT do: nothing moved. borrow checks first and only then
# subtracts, so a refused step leaves the shelf untouched and the
# script stays trustworthy.
#
# The Magazine came back as a Magazine, not as a plain Book, and
# that is something the flat dict of project 34 could not carry on
# its own. The file only says "issue": 7, and it is from_dict that
# knows the key means "build the subclass instead".
#
# This is the payoff of the whole rewrite. Try
# library["dune"].copies = -1 anywhere in this file and you get a
# LibraryError instead of a corrupt shelf.
#
# One last cleanup lesson sits in the import line at the top. The
# folder used by tasks 1 to 9 is registered with atexit rather than
# deleted on the final line, because a delete on the final line does
# not run when something in the middle raises. An earlier draft of
# this file proved it by crashing and leaving a folder behind in
# temp. atexit runs on the way out even then.

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 35")
print("=" * 60)
# ============================================================
# END OF PROJECT 35
# ============================================================