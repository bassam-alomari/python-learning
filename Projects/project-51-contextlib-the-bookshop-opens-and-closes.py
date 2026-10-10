# ============================================================
# Project 51 - contextlib: the bookshop opens and closes
# ============================================================
# What this lesson teaches:
#   contextmanager    a generator becomes a with-statement: yield in, finally out
#   the body mutates  the yielded object is the real one, not a copy
#   teardown on error the close half runs even when the body raises
#   suppress          swallow exactly the exception types you name
#   redirect_stdout   point sys.stdout at a buffer for the block, then restore
#   redirect_stderr   the course rule, proved: stderr can be captured and checked
#   ExitStack         many managed resources in one block, closed last-in first-out
#   closing           a with-statement for objects that only have close()
#   nullcontext       a no-op manager that can still hand you a value
#   nesting           redirects + managers + suppress, and both streams restored
#
# Everything is the standard library. No input(), no random, no datetime.now.
# The output is deterministic. The file runs to completion and exits with 0.
# stdout and stderr are redirected only into StringIO buffers, never into
# each other, and both are restored before the file ends.
#
# Run it:  python project-51-contextlib-the-bookshop-opens-and-closes.py
# ============================================================

import contextlib
import io
import sys

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
print("Q1  what does a context manager promise")
print("Q2  what does @contextmanager turn into a manager")
print("Q3  what does suppress do")
print("Q4  what does redirect_stdout do")
print("Q5  what does redirect_stderr prove about stderr")
print("Q6  what is an ExitStack for")
print("Q7  what does closing give you")
print("Q8  what is nullcontext")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  the with-block always runs the cleanup half, even when the body raises")
print("Q2  a generator: code before yield runs on the way in, code after on the way out")
print("Q3  it swallows the exact exception types you name, and nothing else")
print("Q4  it points sys.stdout somewhere else for the block, then puts it back")
print("Q5  that stderr can be captured and asserted on instead of trusted")
print("Q6  it collects many managed resources in one block, closed last-in first-out")
print("Q7  a with-statement for objects that only have close() and no __enter__")
print("Q8  a context manager that does nothing, and can hand you a value")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - the with-statement always closes")
print("T1  opened and closed -> opened poetry then closed poetry")
print("T1  so the cleanup half is guaranteed -> True")
print()

print("TASK 2 - the yielded object is the real one")
print("T2  the books list grew -> 2")
print("T2  so mutations stick around -> True")
print()

print("TASK 3 - teardown runs even when the body raises")
print("T3  the close still ran -> True")
print("T3  so teardown is not optional -> True")
print()

print("TASK 4 - suppress swallows only what you name")
print("T4  nothing escaped -> True")
print("T4  so suppress is precise -> True")
print()

print("TASK 5 - redirect_stdout catches the prints")
print("T5  the prints landed -> sold Dune; sold Neuromancer")
print("T5  so redirect_stdout is a trap for text -> True")
print()

print("TASK 6 - redirect_stderr captures the stderr rule")
print("T6  the warning landed -> quiet failure")
print("T6  so stderr can be captured and inspected -> True")
print()

print("TASK 7 - ExitStack fans out one block")
print("T7  opened 3 shelves -> 3")
print("T7  so ExitStack manages them all -> True")
print()

print("TASK 8 - closing gives close() a with-statement")
print("T8  the shelf was closed -> True")
print("T8  so plain close() joins the with-world -> True")
print()

print("TASK 9 - nullcontext is a no-op with a value")
print("T9  the placeholder yielded -> 42")
print("T9  so nullcontext is always safe -> True")
print()

print("TASK 10 - the audit, nested and restored")
print("T10  stdout lines -> 2")
print("T10  stderr lines -> 1")
print("T10  both streams were restored -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)

# The real streams, captured before anything redirects them.
REAL_STDOUT = sys.stdout
REAL_STDERR = sys.stderr

# Every shelf event the managers below record, in order.
shelf_events = []


@contextlib.contextmanager
def open_shelf(name):
    """Open a shelf on the way in, close it on the way out."""
    shelf_events.append("opened " + name)
    try:
        yield {"name": name, "books": []}
    finally:
        shelf_events.append("closed " + name)


# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - the with-statement always closes")
print("-" * 60)
shelf_events.clear()
with open_shelf("poetry") as shelf:
    inside = shelf["name"]
after = list(shelf_events)

check("opened first", after[0] == "opened poetry")
check("closed last", after[-1] == "closed poetry")
check("exactly two events", len(after) == 2)
check("the body saw the shelf", inside == "poetry")

print("T1  opened and closed ->", " then ".join(after))
print("T1  so the cleanup half is guaranteed ->",
      after == ["opened poetry", "closed poetry"])
print()


# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - the yielded object is the real one")
print("-" * 60)
shelf_events.clear()
with open_shelf("crime") as shelf:
    shelf["books"].append("Dune")
    shelf["books"].append("Neuromancer")

check("the mutation stuck", shelf["books"] == ["Dune", "Neuromancer"])
check("a real dict came back", isinstance(shelf, dict))
check("the shelf still closed", shelf_events[-1] == "closed crime")
check("two books", len(shelf["books"]) == 2)

print("T2  the books list grew ->", len(shelf["books"]))
print("T2  so mutations stick around ->",
      shelf["books"] == ["Dune", "Neuromancer"])
print()


# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - teardown runs even when the body raises")
print("-" * 60)
shelf_events.clear()
caught = None
try:
    with open_shelf("broken"):
        raise RuntimeError("spill on aisle 3")
except RuntimeError as error:
    caught = error

check("the teardown still ran", "closed broken" in shelf_events)
check("the error reached us", str(caught) == "spill on aisle 3")
check("the type survived", type(caught) is RuntimeError)
check("opened before the crash", shelf_events[0] == "opened broken")

print("T3  the close still ran ->", "closed broken" in shelf_events)
print("T3  so teardown is not optional ->",
      str(caught) == "spill on aisle 3")
print()


# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - suppress swallows only what you name")
print("-" * 60)
manager = contextlib.suppress(FileNotFoundError)
try:
    with manager:
        open(r"C:\definitely\not\here\book.txt", encoding="utf-8")
    missing_escaped = False
except FileNotFoundError:
    missing_escaped = True

try:
    with contextlib.suppress(ZeroDivisionError):
        1 / 0
    zero_escaped = False
except ZeroDivisionError:
    zero_escaped = True

try:
    with contextlib.suppress(FileNotFoundError):
        1 / 0
    other_escaped = True
except ZeroDivisionError:
    other_escaped = False

check("the missing file did not escape", not missing_escaped)
check("suppress handles any named type", not zero_escaped)
check("only the named error is swallowed", other_escaped is False)
check("it is a suppress instance",
      isinstance(manager, contextlib.suppress))

print("T4  nothing escaped ->",
      not missing_escaped and not zero_escaped)
print("T4  so suppress is precise ->", other_escaped is False)
print()


# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - redirect_stdout catches the prints")
print("-" * 60)
sink = io.StringIO()
with contextlib.redirect_stdout(sink):
    print("sold Dune")
    print("sold Neuromancer")
lines = sink.getvalue().splitlines()

check("both prints were caught",
      lines == ["sold Dune", "sold Neuromancer"])
check("stdout was restored", sys.stdout is REAL_STDOUT)
check("the buffer is a StringIO", isinstance(sink, io.StringIO))
check("the trailing newline was kept", sink.getvalue().endswith("\n"))

print("T5  the prints landed ->", "; ".join(lines))
print("T5  so redirect_stdout is a trap for text ->",
      lines == ["sold Dune", "sold Neuromancer"])
print()


# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - redirect_stderr captures the stderr rule")
print("-" * 60)
err = io.StringIO()
with contextlib.redirect_stderr(err):
    print("quiet failure", file=sys.stderr)

check("the warning was caught", err.getvalue() == "quiet failure\n")
check("stderr was restored", sys.stderr is REAL_STDERR)
check("stdout never moved", sys.stdout is REAL_STDOUT)
check("the newline is intact", err.getvalue().endswith("\n"))

print("T6  the warning landed ->", err.getvalue().strip())
print("T6  so stderr can be captured and inspected ->",
      err.getvalue() == "quiet failure\n")
print()


# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - ExitStack fans out one block")
print("-" * 60)
shelf_events.clear()
entered = []
with contextlib.ExitStack() as stack:
    for name in ("history", "science", "art"):
        current = stack.enter_context(open_shelf(name))
        entered.append(current["name"])
closed_order = [each for each in shelf_events if each.startswith("closed")]

check("three shelves opened", entered == ["history", "science", "art"])
check("six events total", len(shelf_events) == 6)
check("opened in order", shelf_events[0] == "opened history")
check("closed last-in first-out",
      closed_order == ["closed art", "closed science", "closed history"])

print("T7  opened 3 shelves ->", len(entered))
print("T7  so ExitStack manages them all ->",
      closed_order[0] == "closed art")
print()


# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - closing gives close() a with-statement")
print("-" * 60)


class Shelf:
    """A plain object: close(), but no __enter__ or __exit__."""

    def __init__(self, name):
        self.name = name
        self.closed = False

    def close(self):
        self.closed = True


plain = Shelf("maps")
with contextlib.closing(plain):
    was_open = not plain.closed

check("the body saw it open", was_open)
check("closing() called close()", plain.closed)
check("the object is the same", plain.name == "maps")
check("Shelf has no with methods", not hasattr(plain, "__enter__"))

print("T8  the shelf was closed ->", plain.closed)
print("T8  so plain close() joins the with-world ->",
      plain.closed and was_open)
print()


# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - nullcontext is a no-op with a value")
print("-" * 60)
seen = None
with contextlib.nullcontext(42) as value:
    seen = value
with contextlib.nullcontext() as empty:
    seen_empty = empty

check("the value came through", seen == 42)
check("without a value it yields None", seen_empty is None)
check("it is a nullcontext",
      isinstance(contextlib.nullcontext(1), contextlib.nullcontext))
check("it is a real manager", hasattr(contextlib.nullcontext(), "__enter__"))

print("T9  the placeholder yielded ->", seen)
print("T9  so nullcontext is always safe ->", seen == 42)
print()


# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the audit, nested and restored")
print("-" * 60)
shelf_events.clear()
out = io.StringIO()
err = io.StringIO()

with contextlib.ExitStack() as stack:
    stack.enter_context(contextlib.redirect_stdout(out))
    stack.enter_context(contextlib.redirect_stderr(err))
    stack.enter_context(open_shelf("audit"))
    with contextlib.suppress(KeyError):
        {}["missing"]
    print("audit start")
    print("quiet warning", file=sys.stderr)
    print("audit end")

stdout_lines = out.getvalue().splitlines()
stderr_lines = err.getvalue().splitlines()

check("two stdout lines", stdout_lines == ["audit start", "audit end"])
check("one stderr line", stderr_lines == ["quiet warning"])
check("the shelf opened and closed",
      shelf_events == ["opened audit", "closed audit"])
check("stdout was restored", sys.stdout is REAL_STDOUT)
check("stderr was restored", sys.stderr is REAL_STDERR)

print("T10  stdout lines ->", len(stdout_lines))
print("T10  stderr lines ->", len(stderr_lines))
print("T10  both streams were restored ->",
      sys.stdout is REAL_STDOUT and sys.stderr is REAL_STDERR)
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
