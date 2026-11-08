# -----------------------------------------------------------------
# Lesson 130: logging -- write, read, format and filter a log
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : logging events to a file, reading its tail,
#            severity levels, fixed timestamps, and
#            custom log formatting
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript is noisy, but its repeated examples point
# to Python's logging module:
#
#     PURPOSE [00:04-00:52] -- keep a record of what happened
#     in a program / website: page visits, errors, conflicts,
#     uploads rejected for exceeding 25 MB
#     FILE [00:52-01:24] -- timestamped lines; inspect the
#     whole file or only its last lines for newest events
#     LEVELS [04:31-07:17] -- choose which events to record
#     and how important they are
#     FORMATTING [08:08-11:46] -- arrange time/date, logger
#     name, level and message; strftime directives control
#     the date/time layout
#
# The middle is unclear, so this lesson demonstrates the
# concepts using a FileHandler and fixed LogRecord times.
# Every file lives in a temporary sandbox; no wall clock
# or machine path is printed. All outputs were run.

import datetime
import io
import logging
import os
import shutil
import tempfile

# ============================================================
# [1] Why programs keep a log
# ============================================================
# A log is a durable diary of events -- page opened,
# upload rejected, server conflict. It can be inspected
# after the visitor has left.

print("  logging: a program's event diary")
print("  examples: page visit, error, rejected upload")
#   logging: a program's event diary
#   examples: page visit, error, rejected upload

# ============================================================
# [2] The logging module
# ============================================================
# The standard library provides loggers and handlers.

print(f"  module name: {logging.__name__}")
print(f"  logger factory available: {callable(logging.getLogger)}")
print(f"  file handler available: {callable(logging.FileHandler)}")
#   module name: logging
#   logger factory available: True
#   file handler available: True

# A Logger creates records; a Handler sends them to a
# destination. Here the destination will be a file.

# ============================================================
# [3] Write events to a real file
# ============================================================
# Fixed timestamps keep output repeatable, independent
# of the clock on the computer running this file.

WORK_DIR = tempfile.mkdtemp(prefix="py130_")
log_path = os.path.join(WORK_DIR, "site.log")
logger = logging.getLogger("lesson130.site")
logger.setLevel(logging.DEBUG)
logger.propagate = False
handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
handler.setFormatter(logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))
logger.addHandler(handler)


def log_at(active_logger, level, message, when):
    """Write a log record with an explicitly fixed time."""
    record = active_logger.makeRecord(
        active_logger.name, level, "lesson.py", 1, message, (), None
    )
    record.created = when.timestamp()
    active_logger.handle(record)


log_at(logger, logging.INFO, "home page opened",
       datetime.datetime(2020, 3, 31, 13, 20, 10))
log_at(logger, logging.WARNING, "upload exceeds 25 MB",
       datetime.datetime(2020, 3, 31, 13, 21, 5))
handler.flush()

print(f"  log file created: {os.path.isfile(log_path)}")
print(f"  log file basename: {os.path.basename(log_path)}")
#   log file created: True
#   log file basename: site.log

# ============================================================
# [4] Read the whole log file
# ============================================================
# A log is ordinary text. Read it like any other file.

with open(log_path, "r", encoding="utf-8") as log_file:
    all_lines = log_file.read().splitlines()

print(f"  whole log line count: {len(all_lines)}")
print(f"  first line: {all_lines[0]}")
print(f"  second line: {all_lines[1]}")
#   whole log line count: 2
#   first line: 2020-03-31 13:20:10 | INFO | lesson130.site | home page opened
#   second line: 2020-03-31 13:21:05 | WARNING | lesson130.site | upload exceeds 25 MB

# Each row records when, how serious, where from and
# what happened -- the useful shape of a log line.

# ============================================================
# [5] Read only the tail of a longer log
# ============================================================
# Add three more events using an append handler. The
# first two could represent earlier traffic and the
# final one the newest record.

handler.flush()
handler.close()
logger.removeHandler(handler)
append_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
append_handler.setFormatter(logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))
logger.addHandler(append_handler)
for index in range(3, 6):
    log_at(logger, logging.INFO, f"event {index}",
           datetime.datetime(2020, 3, 31, 13, 20, index))
append_handler.flush()

with open(log_path, "r", encoding="utf-8") as log_file:
    expanded_lines = log_file.read().splitlines()
tail_lines = expanded_lines[-2:]

print(f"  expanded log line count: {len(expanded_lines)}")
print(f"  tail line count: {len(tail_lines)}")
print(f"  tail last line: {tail_lines[-1]}")
#   expanded log line count: 5
#   tail line count: 2
#   tail last line: 2020-03-31 13:20:05 | INFO | lesson130.site | event 5

# The slice lines[-2:] means "the last two lines".
# Close and detach this handler before changing setup.
append_handler.close()
logger.removeHandler(append_handler)

# ============================================================
# [6] Severity levels
# ============================================================
# Standard levels, from least to most severe:

levels = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL,
]
level_names = [logging.getLevelName(level) for level in levels]
print(f"  level names: {level_names}")
print(f"  levels increase: {levels == sorted(levels)}")
#   level names: ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
#   levels increase: True

# ============================================================
# [7] A level threshold filters records
# ============================================================
# A WARNING threshold excludes DEBUG and INFO records.

captured = io.StringIO()
filter_logger = logging.getLogger("lesson130.filter")
filter_logger.setLevel(logging.DEBUG)
filter_logger.propagate = False
memory_handler = logging.StreamHandler(captured)
memory_handler.setLevel(logging.WARNING)
filter_logger.addHandler(memory_handler)
filter_logger.debug("debug detail")
filter_logger.info("ordinary visit")
filter_logger.warning("large upload")
filter_logger.error("page failed")
filter_logger.removeHandler(memory_handler)
memory_handler.close()
filtered = captured.getvalue().splitlines()

print(f"  threshold: {logging.getLevelName(memory_handler.level)}")
print(f"  captured messages: {filtered}")
print(f"  below-threshold messages excluded: {len(filtered) == 2}")
#   threshold: WARNING
#   captured messages: ['large upload', 'page failed']
#   below-threshold messages excluded: True

# ============================================================
# [8] Custom format: time, level, name, message
# ============================================================
# Arrange the fields with a format string.

format_text = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
formatter = logging.Formatter(
    fmt=format_text,
    datefmt="%d %B %Y %H:%M:%S",
)
record = logging.LogRecord(
    name="lesson130.custom",
    level=logging.INFO,
    pathname="lesson.py",
    lineno=1,
    msg="custom layout",
    args=(),
    exc_info=None,
)
record.created = datetime.datetime(2020, 3, 31, 13, 20, 0).timestamp()
custom_line = formatter.format(record)

print(f"  custom line: {custom_line}")
print(f"  layout order correct: {custom_line.endswith(' | lesson130.custom | custom layout')}")
#   custom line: 31 March 2020 13:20:00 | INFO | lesson130.custom | custom layout
#   layout order correct: True

# ============================================================
# [9] Date and time format directives
# ============================================================
# %d is day, %B full month, %Y full year; %H hour,
# %M minute, %S second. Combine them as desired.

moment = datetime.datetime(2020, 3, 31, 13, 20, 0)
old_style = moment.strftime("%d/%m/%Y %H:%M:%S")
new_style = moment.strftime("%d %B %Y %H:%M:%S")

print(f"  numeric date/time: {old_style}")
print(f"  readable date/time: {new_style}")
print(f"  same moment: {datetime.datetime.strptime(old_style, '%d/%m/%Y %H:%M:%S') == moment}")
#   numeric date/time: 31/03/2020 13:20:00
#   readable date/time: 31 March 2020 13:20:00
#   same moment: True

# ============================================================
# [10] Level and message are separate fields
# ============================================================
# A shorter format rearranges presentation without
# changing the underlying record fields.

record.levelname = "ERROR"
record.msg = "database connection failed"
record.args = ()
short_formatter = logging.Formatter("%(levelname)s: %(message)s")
short_line = short_formatter.format(record)
print(f"  short format: {short_line}")
print(f"  level field: {record.levelname}")
print(f"  message field: {record.getMessage()}")
#   short format: ERROR: database connection failed
#   level field: ERROR
#   message field: database connection failed

# ============================================================
# [11] Logger names identify the source
# ============================================================
# Hierarchical logger names can identify a component.

site_logger = logging.getLogger("lesson130.site.upload")
print(f"  parent logger: {site_logger.parent.name}")
print(f"  child logger: {site_logger.name}")
print(f"  child inherits hierarchy: {site_logger.name.startswith(site_logger.parent.name + '.')}")
#   parent logger: lesson130.site
#   child logger: lesson130.site.upload
#   child inherits hierarchy: True

# ============================================================
# [12] Final report and cleanup
# ============================================================
# Close/detach any live handler before removing the
# sandbox directory.

with open(log_path, "r", encoding="utf-8") as log_file:
    final_lines = log_file.read().splitlines()

print(f"  log lines at end: {len(final_lines)}")
print(f"  contains warning: {any('WARNING' in line for line in final_lines)}")
print(f"  contains first event: {any('home page opened' in line for line in final_lines)}")
print(f"  contains newest event: {any('event 5' in line for line in final_lines)}")

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   log lines at end: 5
#   contains warning: True
#   contains first event: True
#   contains newest event: True
#   sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# Logging as suggested by the transcript:
#
#   1. PURPOSE -- a program's diary of page visits,
#      errors, conflicts and rejected uploads
#   2. FILE -- FileHandler writes ordinary text; open()
#      and read() inspect it later
#   3. TAIL -- lines[-N:] reads only the newest N entries
#   4. LEVELS -- DEBUG < INFO < WARNING < ERROR < CRITICAL
#   5. THRESHOLD -- only records at/above the selected
#      level are emitted; WARNING excludes DEBUG and INFO
#   6. FORMAT -- %(asctime)s, %(levelname)s, %(name)s and
#      %(message)s can be arranged freely
#   7. DATEFMT -- strftime directives control appearance:
#      %d %B %Y %H:%M:%S
#   8. NAME -- logger hierarchy identifies the component
#      that produced an event
#   9. MESSAGE -- text stays distinct from level and
#      formatting; a handler controls the destination
#  10. DETERMINISM -- fixed datetimes, no machine clock,
#      no machine paths, no external dependencies
#  11. CLEANUP -- flush, close and detach handlers before
#      deleting the temporary log directory (removed True)
#  12. HONEST SCOPE -- the transcript is noisy; this
#      lesson demonstrates the concepts without claiming
#      unclear source code or exact settings
#
# A log turns "something happened" into a searchable
# record: when, where, how serious, and what.
