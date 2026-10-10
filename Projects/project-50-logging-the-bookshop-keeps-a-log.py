# ============================================================
# Project 50 - logging: the bookshop keeps a log
# ============================================================
# What this lesson teaches:
#   getLogger          one logger object per name, the same one every time
#   levels             DEBUG INFO WARNING ERROR CRITICAL, ranked by number
#   setLevel           the first gate: which records are allowed out
#   Handler            where a record goes: a buffer, a file, a stream
#   StreamHandler      by default it writes to sys.stderr - we never use that
#   Formatter          %(name)s %(levelname)s %(message)s filled per record
#   formatTime         asctime follows the real clock, so we fix it
#   propagate          a child logger hands records up to its parent
#   logger.exception   the traceback stays inside the record
#   handler level      the second gate, after the logger has already spoken
#
# Everything is the standard library. No input(), no random, no datetime.now.
# The output is deterministic. The file runs to completion and exits with 0.
# The default logging setup writes to sys.stderr, and this file never calls
# basicConfig(): every handler here writes into a StringIO.
#
# Run it:  python project-50-logging-the-bookshop-keeps-a-log.py
# ============================================================

import io
import logging
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
print("Q1  what does logging.getLogger return")
print("Q2  what are the levels")
print("Q3  what does a handler do")
print("Q4  what is a format string made of")
print("Q5  why must asctime be handled with care")
print("Q6  what does logger.setLevel change")
print("Q7  what does propagate mean")
print("Q8  where does logging write by default")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  one logger object per name, the same one every time you ask")
print("Q2  DEBUG, INFO, WARNING, ERROR, CRITICAL - numbers that rank urgency")
print("Q3  it takes a finished record and stores it somewhere, a buffer included")
print("Q4  field names like %(levelname)s and %(message)s, filled from the record")
print("Q5  because the real clock changes every run, and our output must not")
print("Q6  which records pass the first gate, and which are dropped")
print("Q7  a child logger hands its records up to its parent's handlers")
print("Q8  sys.stderr - which is why this course never uses the default setup")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - getLogger hands back one logger")
print("T1  the same logger -> True")
print("T1  so getLogger hands back one logger -> True")
print()

print("TASK 2 - levels are numbers")
print("T2  the level -> 10")
print("T2  so DEBUG lets everything through -> True")
print()

print("TASK 3 - a record reaches the handler")
print("T3  captured -> bookshop INFO the shelf was read")
print("T3  so a handler holds the record -> True")
print()

print("TASK 4 - the format is a template")
print("T4  formatted -> WARNING | late return")
print("T4  so the format is a template -> True")
print()

print("TASK 5 - the clock is ours to fix")
print("T5  with a fixed clock -> 12:00:00 opened")
print("T5  so asctime cannot change the output -> True")
print()

print("TASK 6 - the level gate drops what is below")
print("T6  after the gate -> bookshop WARNING spoken")
print("T6  so below the level never arrives -> True")
print()

print("TASK 7 - child loggers propagate upward")
print("T7  the child went up -> bookshop.stock INFO counted 12 books")
print("T7  so propagate hands the record to the parent -> True")
print()

print("TASK 8 - the traceback stays in the record")
print("T8  the record carries a traceback -> True")
print("T8  so exception logging keeps the detail -> True")
print()

print("TASK 9 - two gates must both be open")
print("T9  through both gates -> bookshop ERROR kept by handler")
print("T9  so a record passes two checks -> True")
print()

print("TASK 10 - the audit, and the stderr that stayed empty")
print("T10  the audit lines -> 3")
print("T10  the root logger has no handlers -> True")
print("T10  so the log never touched stderr -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)

# One logger, one buffer, and no basicConfig() anywhere: the default
# StreamHandler would write to sys.stderr, and stderr must stay empty.
buf = io.StringIO()
logger = logging.getLogger("bookshop")
logger.setLevel(logging.DEBUG)
logger.propagate = False
handler = logging.StreamHandler(buf)
handler.setFormatter(logging.Formatter("%(name)s %(levelname)s %(message)s"))
logger.addHandler(handler)


def emitted():
    """Everything the main handler has taken so far, as lines."""
    return buf.getvalue().splitlines()


def clear():
    """Empty the buffer without touching the handlers."""
    buf.seek(0)
    buf.truncate(0)


# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - getLogger hands back one logger")
print("-" * 60)
one = logging.getLogger("bookshop")
two = logging.getLogger("bookshop")

check("it is the same object", one is two)
check("the name is the key", one.name == "bookshop")
check("it is a real Logger", isinstance(one, logging.Logger))
check("exactly one handler so far", len(one.handlers) == 1)

print("T1  the same logger ->", one is two and one.name == "bookshop")
print("T1  so getLogger hands back one logger ->", one is two)
print()


# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - levels are numbers")
print("-" * 60)
check("the level is DEBUG", logger.level == logging.DEBUG)
check("the ranks ascend",
      logging.DEBUG < logging.INFO < logging.WARNING < logging.ERROR)
check("DEBUG lets everything through",
      logger.isEnabledFor(logging.DEBUG))
check("the effective level matches",
      logger.getEffectiveLevel() == logging.DEBUG)

print("T2  the level ->", logger.level)
print("T2  so DEBUG lets everything through ->",
      logger.isEnabledFor(logging.DEBUG))
print()


# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - a record reaches the handler")
print("-" * 60)
clear()
logger.info("the shelf was read")
lines = emitted()

check("one line arrived", len(lines) == 1)
check("the level is in there", lines and "INFO" in lines[0])
check("the message is intact",
      lines and lines[0].endswith("the shelf was read"))
check("the name came from the logger",
      lines and lines[0].startswith("bookshop "))

print("T3  captured ->", lines[0])
print("T3  so a handler holds the record ->", len(lines) == 1)
print()


# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - the format is a template")
print("-" * 60)
audit_buf = io.StringIO()
audit = logging.getLogger("bookshop.audit")
audit.setLevel(logging.DEBUG)
audit.propagate = False
audit_handler = logging.StreamHandler(audit_buf)
audit_handler.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
audit.addHandler(audit_handler)

audit.warning("late return")
audit_line = audit_buf.getvalue().splitlines()[0]

check("the template was filled", audit_line == "WARNING | late return")
check("levelname and message both landed",
      audit_line.startswith("WARNING")
      and audit_line.endswith("late return"))
check("the separator is ours", " | " in audit_line)
check("the formatter is a Formatter",
      isinstance(audit_handler.formatter, logging.Formatter))

print("T4  formatted ->", audit_line)
print("T4  so the format is a template ->",
      audit_line == "WARNING | late return")
print()


# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - the clock is ours to fix")
print("-" * 60)


class FixedTimeFormatter(logging.Formatter):
    """asctime is a real timestamp, so this course pins it down."""

    def formatTime(self, record, datefmt=None):
        return "12:00:00"


clock_buf = io.StringIO()
clock = logging.getLogger("bookshop.clock")
clock.setLevel(logging.DEBUG)
clock.propagate = False
clock_handler = logging.StreamHandler(clock_buf)
clock_handler.setFormatter(FixedTimeFormatter("%(asctime)s %(message)s"))
clock.addHandler(clock_handler)

clock.info("opened")
clock_line = clock_buf.getvalue().splitlines()[0]

check("the time is the fixed one", clock_line == "12:00:00 opened")
check("the override was used",
      isinstance(clock_handler.formatter, FixedTimeFormatter))
check("the record still knows the real clock", clock_handler is not None)
check("no real timestamp leaked", "20" not in clock_line.split()[0])

print("T5  with a fixed clock ->", clock_line)
print("T5  so asctime cannot change the output ->",
      clock_line == "12:00:00 opened")
print()


# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - the level gate drops what is below")
print("-" * 60)
clear()
logger.setLevel(logging.WARNING)
logger.debug("quiet")
logger.info("also quiet")
logger.warning("spoken")
kept = emitted()

check("only the warning arrived", len(kept) == 1)
check("nothing below the level got through",
      "quiet" not in buf.getvalue())
check("INFO is below the gate now", not logger.isEnabledFor(logging.INFO))
check("WARNING opens the gate", logger.isEnabledFor(logging.WARNING))

print("T6  after the gate ->", kept[0])
print("T6  so below the level never arrives ->",
      len(kept) == 1 and "quiet" not in buf.getvalue())
print()


# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - child loggers propagate upward")
print("-" * 60)
clear()
logger.setLevel(logging.DEBUG)
stock = logging.getLogger("bookshop.stock")
stock.info("counted 12 books")
went_up = emitted()

before = len(went_up)
stock.propagate = False
stock.info("this one stays home")
after = emitted()

check("the child has no handlers of its own", len(stock.handlers) == 0)
check("the parent took the record",
      went_up and went_up[0].startswith("bookshop.stock INFO"))
check("the name shows the whole path",
      went_up and went_up[0].startswith("bookshop.stock "))
check("propagate=False stops the climb", len(after) == before)

print("T7  the child went up ->", went_up[0])
print("T7  so propagate hands the record to the parent ->",
      went_up[0].startswith("bookshop.stock INFO"))
print()


# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - the traceback stays in the record")
print("-" * 60)
clear()
try:
    raise ValueError("bad shelf count")
except ValueError:
    logger.exception("the audit stopped")
text = buf.getvalue()

check("the traceback is in the buffer",
      "Traceback (most recent call last)" in text)
check("the exception type and message are there",
      "ValueError: bad shelf count" in text)
check("the log message is there once", text.count("the audit stopped") == 1)
check("the traceback is several lines, all captured",
      len(text.splitlines()) > 3)

print("T8  the record carries a traceback ->",
      "Traceback (most recent call last)" in text)
print("T8  so exception logging keeps the detail ->",
      "ValueError: bad shelf count" in text)
print()


# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - two gates must both be open")
print("-" * 60)
clear()
handler.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)
logger.warning("dropped by handler")
logger.error("kept by handler")
through = emitted()

check("the handler kept the error", len(through) == 1)
check("the handler dropped the warning",
      "dropped by handler" not in buf.getvalue())
check("the logger gate was wide open", logger.level == logging.DEBUG)
check("the handler gate was at ERROR", handler.level == logging.ERROR)

print("T9  through both gates ->", through[-1])
print("T9  so a record passes two checks ->",
      len(through) == 1 and "dropped by handler" not in buf.getvalue())
print()


# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the audit, and the stderr that stayed empty")
print("-" * 60)
clear()
handler.setLevel(logging.NOTSET)
logger.setLevel(logging.DEBUG)
for message in ("opened", "sold Dune", "closed"):
    logger.info(message)
audit_lines = emitted()
root = logging.getLogger()
streams = [each.stream for each in logger.handlers]

check("three lines were logged", len(audit_lines) == 3)
check("in the order they happened",
      audit_lines[0].endswith("opened")
      and audit_lines[1].endswith("sold Dune")
      and audit_lines[2].endswith("closed"))
check("the root logger has no handlers", root.handlers == [])
check("our handler writes to a StringIO",
      all(isinstance(each, io.StringIO) for each in streams))
check("nothing is pointed at stderr",
      all(each is not sys.stderr for each in streams))

print("T10  the audit lines ->", len(audit_lines))
print("T10  the root logger has no handlers ->", root.handlers == [])
print("T10  so the log never touched stderr ->",
      all(each is not sys.stderr for each in streams))
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
