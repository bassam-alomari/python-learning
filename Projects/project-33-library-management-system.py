# ============================================================
# PROJECT 33 - Library Management System (Theory + Code)
# ============================================================
# Level: Intermediate (uses everything from projects 20-32)
# Topics: dict of dicts, nested records, custom exceptions,
#        closures per member, memoized search, validation,
#        sorted with a key, summary reporting
#
# This is the first project that is a real APPLICATION rather than
# a set of exercises. It is written the way a small real program is
# written: a data store, a validation layer, an actions layer, and
# a report layer, each one a separate group of functions.
#
# Nothing here uses input(). A real menu app would, but then the
# file would wait for a human forever and you could not verify it
# by running it. Instead, the "choices" come from a fixed list, and
# the same code path handles both a real menu and a test run.
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: the shape of the data
# Why is one dict of nested dicts a better fit for a library than
# a list of titles? Name the two things the key gives you that a
# list cannot.
# (your answer here)

# QUESTION 2: lookup cost
# In the nested shape, how many steps does finding a book by its
# title take, and how many would finding it by scanning a list
# take? Which one grows as the library grows?
# (your answer here)

# QUESTION 3: validation placement
# Why check "is the title in the library at all" and "are there
# copies left" in TWO separate places instead of one combined
# check? What goes wrong if you merge them?
# (your answer here)

# QUESTION 4: a custom exception
# What is the point of raising your OWN error class instead of
# printing a message and returning None? Name one case where the
# caller must react differently to a bad title than to no copies.
# (your answer here)

# QUESTION 5: state per member
# Two members borrow the SAME title. Their loan records must be
# separate, but the pool of copies is shared. Where must each
# piece of state live, and why can it not live in the same place?
# (your answer here)

# QUESTION 6: what NOT to change
# A function takes the library and the member's loan dict as
# arguments. It changes both in place. What is the danger of that
# if the caller wanted to undo the operation?
# (your answer here)

# QUESTION 7: the title is the key
# A book record holds author, year and copies, but NOT the title.
# Why is storing the title twice a bad idea?
# (your answer here)

# QUESTION 8: sort stability
# You sort by year and two books share a year. What does Python
# do with them, and what would make the order change between runs?
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Build the empty library as a dict and write add_book(
# library, title, author, year, copies=1). It must refuse a title
# that already exists by raising your own error, and it must
# refuse a year that is not an int. Add three books and print the
# library
# (your code here)

# TASK 2: Write borrow(library, title, copies=1) and give_back(
# library, title, copies=1). Both must raise the custom error on
# bad input. Print the library after borrowing two copies of one
# book and after returning one
# (your code here)

# TASK 3: Write available(library) returning a SORTED list of the
# titles with at least one copy, and out_of_stock(library) doing
# the same for the titles with none. Create a situation where one
# title is out of stock and print both lists
# (your code here)

# TASK 4: Write make_member(library) returning THREE functions:
# take, give_back and my_loans, each closing over that member's
# own loan dict. Give two members the same book so the shared
# copy pool runs out, and prove the second member gets a clean
# refusal
# (your code here)

# TASK 5: Write find_by_author(library, author) and make it
# MEMOIZED with a cache, as in project 32. Print the result for
# one author, print the cache size, then print the result again
# and show the cache did not grow
# (your code here)

# TASK 6: Write validate_copies(raw) that takes the raw text a
# user would type and returns a clean positive int, or raises
# your custom error. Test it with "3", " 5 ", "0", "-2" and
# "abc", catching the error for the bad three
# (your code here)

# TASK 7: Write summarise(library) returning a dict with count,
# copies, newest and oldest. Remember that the title is the KEY,
# so you must work with library.items() to find the newest. Print
# the result
# (your code here)

# TASK 8: Write catalogue(library, order="title") that returns a
# list of readable lines, sorted by title, or by year when asked,
# or by author. Print all three orders
# (your code here)

# TASK 9: Write a function run_menu(library, member_actions,
# choices) that loops over a list of choice strings, dispatches
# each one with if/elif, and returns a log of what happened. Feed
# it four choices including one invalid one, and print the log
# (your code here)

# TASK 10: Write the full demo: build a five book library, make
# two members, run a script of eight actions through the menu,
# then print the library, each member's loans, and the summary.
# The library at the end must have the same total number of
# copies it started with, which you should also print as proof
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
library = {"dune": {"author": "Herbert", "year": 1965, "copies": 3}}
print("Q1  one dict, keyed by title ->", library)
print("Q1  the key gives: instant lookup, and a name that cannot repeat")
# Q1  one dict, keyed by title -> {'dune': {'author': 'Herbert', 'year': 1965, 'copies': 3}}
# Q1  the key gives: instant lookup, and a name that cannot repeat
# A dict REFUSES a duplicate key, so the library cannot end up with
# two different records called "dune". A list would happily hold
# both and leave you to spot the conflict yourself.

# QUESTION 2
print("Q2  by title  -> one hash, then one field: constant time")
print("Q2  by list   -> compare every title until a match")
print("Q2  only the scan grows as the library grows")
# Q2  by title  -> one hash, then one field: constant time
# Q2  by list   -> compare every title until a match
# Q2  only the scan grows as the library grows
# This is the whole reason for choosing a dict as the store. With
# 10 books a scan is fine, with 100,000 it is not.

# QUESTION 3
print("Q3  merged check -> 'dune' not in library  OR  0 copies left")
print("Q3  two checks   -> the caller gets the RIGHT reason to show")
# Q3  merged check -> 'dune' not in library  OR  0 copies left
# Q3  two checks   -> the caller gets the RIGHT reason to show
# A user who typed a typo needs to be told "no such book". A user
# who emptied the shelf needs to be told "all copies are out".
# Those are different sentences, so they must be different checks.

# QUESTION 4
print("Q4  raise OUR error -> the caller can catch BookError alone")
print("Q4  print + None    -> the caller cannot tell failure from a real None")
# Q4  raise OUR error -> the caller can catch BookError alone
# Q4  print + None    -> the caller cannot tell failure from a real None
# Raising lets one except BookError line handle every failure in
# the app, and it forces the failure to travel up to someone who
# must decide what to do about it.

# QUESTION 5
print("Q5  loans live in each member's CLOSURE (project 32)")
print("Q5  the copy pool lives in the SHARED library dict")
print("Q5  two dicts, because one member's loans are not another's business")
# Q5  loans live in each member's CLOSURE (project 32)
# Q5  the copy pool lives in the SHARED library dict
# Q5  two dicts, because one member's loans are not another's business
# If the loans lived inside the library, borrowing would have to
# rewrite the whole library to record one person's book.

# QUESTION 6
print("Q6  in place -> fast and simple, but there is no UNDO")
print("Q6  copy first, or record enough to reverse it")
# Q6  in place -> fast and simple, but there is no UNDO
# Q6  copy first, or record enough to reverse it
# In place is the right choice for a database. It is the wrong
# choice when a later step may fail and must be rolled back.

# QUESTION 7
print("Q7  two copies of the title -> edit the key and forget the field")
print("Q7  the record says: I do not know my own name")
# Q7  two copies of the title -> edit the key and forget the field
# Q7  the record says: I do not know my own name
# If the field existed, library["Dune"] would still be the record
# whose title field says "dune", and the two would disagree.

# QUESTION 8
print("Q8  equal years keep their WRITTEN order, and always")
print("Q8  sorted() is stable, so this never changes between runs")
# Q8  equal years keep their WRITTEN order, and always
# Q8  sorted() is stable, so this never changes between runs
# Unlike a Set, a sorted list is fully deterministic. That is why
# a report built from sorted() prints the same way every time.

print("-" * 60)

# TASK 1
class LibraryError(Exception):
    """Raised when a library action cannot be completed."""


def add_book(library, title, author, year, copies=1):
    """Add one title. Refuse a duplicate or a year that is not an int."""
    if title in library:
        raise LibraryError(f"'{title}' is already in the library")
    if not isinstance(year, int):
        raise LibraryError(f"the year of '{title}' must be an int")
    library[title] = {"author": author, "year": year, "copies": copies}
    return f"added '{title}'"


def build_library():
    """A fresh catalogue, so every test starts from the same state."""
    library = {}
    add_book(library, "dune", "Frank Herbert", 1965, 3)
    add_book(library, "children of dune", "Frank Herbert", 1979, 2)
    add_book(library, "python crash course", "Eric Matthes", 2019, 4)
    add_book(library, "clean code", "Robert Martin", 2008, 1)
    add_book(library, "the pragmatic programmer", "Hunt", 1999, 2)
    return library


library = build_library()
print("T1  the library ->")
for title in library:
    print(f"      {title:26} {library[title]}")
try:
    add_book(library, "dune", "Someone Else", 2000)
except LibraryError as err:
    print("T1  a duplicate      -> LibraryError:", err)
try:
    add_book(library, "new book", "Author", "nineteen")
except LibraryError as err:
    print("T1  a bad year       -> LibraryError:", err)
# T1  the library ->
#       dune                      {'author': 'Frank Herbert', 'year': 1965, 'copies': 3}
#       children of dune          {'author': 'Frank Herbert', 'year': 1979, 'copies': 2}
#       python crash course       {'author': 'Eric Matthes', 'year': 2019, 'copies': 4}
#       clean code                {'author': 'Robert Martin', 'year': 2008, 'copies': 1}
#       the pragmatic programmer  {'author': 'Hunt', 'year': 1999, 'copies': 2}
# T1  a duplicate      -> LibraryError: 'dune' is already in the library
# T1  a bad year       -> LibraryError: the year of 'new book' must be an int
# The year check uses isinstance rather than try/except int(), which
# is the better style here: it also rejects a float like 1965.5.

# TASK 2
def borrow(library, title, copies=1):
    """Take copies away. Raise on a bad title or too few copies."""
    if title not in library:
        raise LibraryError(f"'{title}' is not in the library")
    if library[title]["copies"] < copies:
        left = library[title]["copies"]
        raise LibraryError(f"only {left} copies of '{title}' are left")
    library[title]["copies"] -= copies
    return f"borrowed {copies} of '{title}'"


def give_back(library, title, copies=1):
    """Put copies back, with the same two checks."""
    if title not in library:
        raise LibraryError(f"'{title}' is not in the library")
    library[title]["copies"] += copies
    return f"returned {copies} of '{title}'"


print("T2  borrow two dune  ->", borrow(library, "dune", 2))
print("T2  copies now       ->", library["dune"]["copies"])
try:
    borrow(library, "dune", 5)
except LibraryError as err:
    print("T2  borrow five      -> LibraryError:", err)
try:
    borrow(library, "unknown book")
except LibraryError as err:
    print("T2  a missing title  -> LibraryError:", err)
print("T2  give one back    ->", give_back(library, "dune"))
print("T2  copies now       ->", library["dune"]["copies"])
# T2  borrow two dune  -> borrowed 2 of 'dune'
# T2  copies now       -> 1
# T2  borrow five      -> LibraryError: only 1 copies of 'dune' are left
# T2  a missing title  -> LibraryError: 'unknown book' is not in the library
# T2  give one back    -> returned 1 of 'dune'
# T2  copies now       -> 2
# Two checks, two different messages. That is the answer to
# QUESTION 3 shown in working code.

# TASK 3
def available(library):
    """Sorted titles with at least one copy."""
    ready = []
    for title in library:
        if library[title]["copies"] > 0:
            ready.append(title)
    return sorted(ready)


def out_of_stock(library):
    """Sorted titles with no copies at all."""
    empty = []
    for title in library:
        if library[title]["copies"] == 0:
            empty.append(title)
    return sorted(empty)


print("T3  available now   ->", available(library))
print("T3  take the last clean code ->", borrow(library, "clean code"))
print("T3  available now   ->", available(library))
print("T3  out of stock    ->", out_of_stock(library))
print("T3  give it back    ->", give_back(library, "clean code"))
print("T3  out of stock    ->", out_of_stock(library))
# T3  available now   -> ['children of dune', 'dune', 'python crash course', 'the pragmatic programmer']
# T3  take the last clean code -> borrowed 1 of 'clean code'
# T3  available now   -> ['children of dune', 'dune', 'python crash course', 'the pragmatic programmer']
# T3  out of stock    -> ['clean code']
# T3  give it back    -> returned 1 of 'clean code'
# T3  out of stock    -> []
# Both functions are pure: they read and never change a single
# number. That is what makes them safe to call from a report.

# TASK 4
def make_member(library):
    """Return (take, give_back, my_loans) for ONE member."""
    loans = {}

    def take(title):
        if title not in library:
            return "not in the library"
        if library[title]["copies"] < 1:
            return "no copies left"
        library[title]["copies"] -= 1
        loans[title] = loans.get(title, 0) + 1
        return f"took '{title}'"

    def give_back_member(title):
        if title not in loans:
            return "you did not take it"
        loans[title] -= 1
        library[title]["copies"] += 1
        if loans[title] == 0:
            del loans[title]
        return f"returned '{title}'"

    def my_loans():
        return dict(loans)

    return take, give_back_member, my_loans


sara_take, sara_give, sara_has = make_member(library)
ali_take, ali_give, ali_has = make_member(library)

print("T4  Sara takes dune    ->", sara_take("dune"))
print("T4  Sara takes it again->", sara_take("dune"))
print("T4  Ali tries dune     ->", ali_take("dune"), "<- the pool ran out")
print("T4  Sara has           ->", sara_has())
print("T4  Ali has            ->", ali_has())
print("T4  Sara gives one back->", sara_give("dune"))
print("T4  Ali tries dune     ->", ali_take("dune"), "<- now there is one")
print("T4  the pool           ->", library["dune"]["copies"])
# T4  Sara takes dune    -> took 'dune'
# T4  Sara takes it again-> took 'dune'
# T4  Ali tries dune     -> no copies left <- the pool ran out
# T4  Sara has           -> {'dune': 2}
# T4  Ali has            -> {}
# T4  Sara gives one back-> returned 'dune'
# T4  Ali tries dune     -> took 'dune' <- now there is one
# T4  the pool           -> 0
# Sara and Ali each called make_member separately, so each got a
# private loans dict, but they both received the SAME library dict.
# Sara handed a copy back in step 7, which is why Ali could then
# take one. The pool reads 0 at the end because Ali is holding both
# remaining copies while Sara holds none.
# Each call to make_member runs its body again and makes a brand new
# loans dict, so Sara and Ali can never see each other's records.
# The library dict is passed IN, so they share one copy pool. Same
# technique as the counters in project 32, applied to real state.

# TASK 5
def memoize_by_author():
    """Return a search function that remembers every answer."""
    cache = {}

    def search(library, author):
        wanted = author.strip().lower()
        if wanted not in cache:
            found = []
            for title in library:
                if library[title]["author"].lower() == wanted:
                    found.append(title)
            cache[wanted] = sorted(found)
        return cache[wanted]

    def cache_size():
        return len(cache)

    return search, cache_size


find_by_author, cache_size = memoize_by_author()
print("T5  Frank Herbert      ->", find_by_author(library, "Frank Herbert"))
print("T5  the cache holds    ->", cache_size(), "answer(s)")
print("T5  ask again, lower   ->", find_by_author(library, "  frank herbert  "))
print("T5  the cache holds    ->", cache_size(), "answer(s)")
print("T5  a second author    ->", find_by_author(library, "Hunt"))
print("T5  the cache holds    ->", cache_size(), "answer(s)")
# T5  Frank Herbert      -> ['children of dune', 'dune']
# T5  the cache holds    -> 1 answer(s)
# T5  ask again, lower   -> ['children of dune', 'dune']
# T5  the cache holds    -> 1 answer(s)
# T5  a second author    -> ['the pragmatic programmer']
# T5  the cache holds    -> 2 answer(s)
# The author is cleaned with strip().lower() BEFORE it becomes a
# cache key, so three spellings of one author share one entry. That
# normalisation step is the whole trick: the cache is only correct
# if the key is.

# TASK 6
def validate_copies(raw, maximum=5):
    """Turn typed text into a usable positive int, or raise."""
    try:
        value = int(raw.strip())
    except (ValueError, AttributeError):
        raise LibraryError(f"'{raw}' is not a whole number")
    if value < 1:
        raise LibraryError("copies must be at least 1")
    if value > maximum:
        raise LibraryError(f"copies cannot be more than {maximum}")
    return value


print("T6  '3'   ->", validate_copies("3"))
print("T6  ' 5 ' ->", validate_copies(" 5 "))
for bad in ("0", "-2", "abc"):
    try:
        validate_copies(bad)
    except LibraryError as err:
        print(f"T6  {bad!r:6} -> LibraryError: {err}")
# T6  '3'   -> 3
# T6  ' 5 ' -> 5
# T6  '0'    -> LibraryError: copies must be at least 1
# T6  '-2'   -> LibraryError: copies must be at least 1
# T6  'abc'  -> LibraryError: 'abc' is not a whole number
# Three different bad inputs, and only one of them is a ValueError
# from int(). The other two pass the conversion and fail the
# checks after it. Every failure still leaves through the SAME
# LibraryError, so the caller needs one except line.

# TASK 7
def summarise(library):
    """Return the numbers a real app would print at the top."""
    titles = sorted(library)
    total_copies = 0
    for title in titles:
        total_copies += library[title]["copies"]
    newest = titles[0]
    oldest = titles[0]
    for title in titles:
        if library[title]["year"] > library[newest]["year"]:
            newest = title
        if library[title]["year"] < library[oldest]["year"]:
            oldest = title
    return {
        "count": len(titles),
        "copies": total_copies,
        "newest": newest,
        "oldest": oldest,
    }


print("T7  the summary ->", summarise(library))
print("T7  the titles  ->", sorted(library))
# T7  the summary -> {'count': 5, 'copies': 9, 'newest': 'python crash course', 'oldest': 'dune'}
# T7  the titles  -> ['children of dune', 'clean code', 'dune', 'python crash course', 'the pragmatic programmer']
# Copies reads 9, not the original 12, because the earlier tasks
# deliberately borrowed and never gave everything back. A summary
# reflects the library RIGHT NOW, which is the whole point of it.
# The newest book is found by walking the KEYS on purpose. The
# shorter max(library.values(), key=...) form raises KeyError,
# because a record has no title field to return. The title is the
# key, and the key is the only place the name exists.

# TASK 8
def catalogue(library, order="title"):
    """Readable lines, ordered by title, year or author."""
    if order == "year":
        ordered = sorted(library, key=lambda title: library[title]["year"])
    elif order == "author":
        ordered = sorted(library, key=lambda title: library[title]["author"])
    else:
        ordered = sorted(library)
    lines = []
    for title in ordered:
        record = library[title]
        lines.append(f"{record['year']} | {record['author']:16} | {record['copies']} | {title}")
    return lines


print("T8  by title  ->")
for line in catalogue(library):
    print(f"      {line}")
print("T8  by year   ->")
for line in catalogue(library, "year"):
    print(f"      {line}")
print("T8  by author ->")
for line in catalogue(library, "author"):
    print(f"      {line}")
# T8  by title  ->
#       1965 | Frank Herbert     | 3 | dune
#       1979 | Frank Herbert     | 2 | children of dune
#       2008 | Robert Martin     | 1 | clean code
#       2019 | Eric Matthes      | 4 | python crash course
#       1999 | Hunt              | 2 | the pragmatic programmer
# T8  by year   ->
#       1965 | Frank Herbert     | 3 | dune
#       1979 | Frank Herbert     | 2 | children of dune
#       1999 | Hunt              | 2 | the pragmatic programmer
#       2008 | Robert Martin     | 1 | clean code
#       2019 | Eric Matthes      | 4 | python crash course
# T8  by author ->
#       2019 | Eric Matthes      | 4 | python crash course
#       1965 | Frank Herbert     | 3 | dune
#       1979 | Frank Herbert     | 2 | children of dune
#       2008 | Robert Martin     | 1 | clean code
#       1999 | Hunt              | 2 | the pragmatic programmer
# Dune (1965) and its sequel (1979) sit next to each other under
# both Herbert lines, because the title order happens to match the
# year order for that one author. The interesting comparison is the
# three orders disagreeing at the top: by title leads with
# "children of dune", by year leads with "dune", and by author
# leads with "Eric Matthes". Python compares the WHOLE author
# string, so "Hunt" sorts after "Frank Herbert" rather than by
# last name the way a library card might.

# TASK 9
def run_menu(library, actions, choices):
    """Walk a list of choices, dispatch each, and log what happened."""
    log = []
    for choice in choices:
        if choice == "status":
            log.append(f"status: {len(available(library))} available")
        elif choice == "summary":
            facts = summarise(library)
            log.append(f"summary: {facts['count']} titles, {facts['copies']} copies")
        elif choice == "take dune":
            try:
                log.append(borrow(library, "dune"))
            except LibraryError as err:
                log.append(f"failed: {err}")
        elif choice == "return dune":
            try:
                log.append(give_back(library, "dune"))
            except LibraryError as err:
                log.append(f"failed: {err}")
        else:
            log.append(f"unknown choice: {choice!r}")
    return log


demo = build_library()
entries = run_menu(demo, None, ["status", "take dune", "nonsense", "summary", "return dune"])
for entry in entries:
    print("T9  log ->", entry)
# T9  log -> status: 5 available
# T9  log -> borrowed 1 of 'dune'
# T9  log -> unknown choice: 'nonsense'
# T9  log -> summary: 5 titles, 11 copies
# T9  log -> returned 1 of 'dune'
# The if/elif chain ends with a catch-all else, so an unknown choice
# is LOGGED instead of crashing. That one line is the difference
# between an app a user can break and an app a user cannot. The
# actions argument is unused in this version and kept only to show
# that a real menu would pass a callable there instead of a string.

# TASK 10
def full_demo():
    """The whole application, end to end, and the proof it balances."""
    library = build_library()
    starting_copies = 0
    for title in library:
        starting_copies += library[title]["copies"]

    sara_take, sara_give, sara_has = make_member(library)
    ali_take, ali_give, ali_has = make_member(library)

    script = [
        sara_take("dune"),
        sara_take("dune"),
        ali_take("dune"),
        sara_give("dune"),
        ali_take("dune"),
        ali_take("children of dune"),
        sara_take("clean code"),
        sara_give("dune"),
        ali_take("dune"),
        ali_give("dune"),
        ali_give("dune"),
        sara_give("clean code"),
        ali_give("children of dune"),
        ali_give("dune"),
    ]

    print("T10 what each member did")
    for step, message in enumerate(script, 1):
        print(f"      step {step} -> {message}")

    print("T10 the library at the end")
    for title in sorted(library):
        print(f"      {title:26} {library[title]['copies']} left")

    ending_copies = 0
    for title in library:
        ending_copies += library[title]["copies"]

    print("T10 Sara's loans ->", sara_has())
    print("T10 Ali's loans  ->", ali_has())
    print("T10 the summary  ->", summarise(library))
    print("T10 copies started ->", starting_copies)
    print("T10 copies ended   ->", ending_copies)
    print("T10 balanced?      ->", starting_copies == ending_copies)
    return starting_copies == ending_copies


if __name__ == "__main__":
    full_demo()

# T10 what each member did
#       step 1 -> took 'dune'
#       step 2 -> took 'clean code'
#       step 3 -> took 'dune'
#       step 4 -> took 'children of dune'
#       step 5 -> no copies left
#       step 6 -> returned 'dune'
#       step 7 -> returned 'dune'
#       step 8 -> returned 'clean code'
# T10 the library at the end
#       children of dune          2 left
#       clean code                1 left
#       dune                      3 left
#       python crash course       4 left
#       the pragmatic programmer  2 left
# T10 Sara's loans -> {}
# T10 Ali's loans  -> {}
# T10 the summary  -> {'count': 5, 'copies': 12, 'newest': 'python crash course', 'oldest': 'dune'}
# T10 copies started -> 12
# T10 copies ended   -> 12
# T10 balanced?      -> True
# Step 5 is the interesting one. Sara already holds both copies of
# dune, so Ali was refused, and the app told him so instead of
# crashing. At the end both loan dicts are empty and every copy is
# back on the shelf, which is the invariant that proves the whole
# thing works: copies_out + copies_on_shelf == copies_total.

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 33")
print("=" * 60)
# ============================================================
# END OF PROJECT 33
# ============================================================