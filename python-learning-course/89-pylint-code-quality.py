# -----------------------------------------------------------------
# Lesson 89: pylint -- code quality checking
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : what a Linter is (bugs + PEP 8 violations),
#            pip install pylint, running pylint
#            my_file.py, the rating out of 10, the
#            detailed report (unused variables, bad
#            names, missing docstrings), the fix-until-
#            10/10 workflow -- all on SANDBOX files
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: an important tool for clean,
# professional code -- Pylint.
#
#   WHAT [00:13] -- a Linter: it analyzes your .py files,
#   hunts for potential errors and violations of the
#   clean-code standards (PEP 8)
#   WHY [00:13] -- code can RUN and still break the
#   globally agreed style; Pylint unifies style and
#   matches what big companies require
#   INSTALL [01:00] -- pip install pylint
#   RUN [02:18] -- pylint my_file.py: line-by-line review,
#   a rating out of 10, and a detailed report (unused
#   variables, non-standard names, ...)
#   THE GOAL [04:42] -- follow the report, fix the notes,
#   reach the full 10/10
#
# STABILITY RULES: pylint's raw output contains absolute
# machine paths -- it is NEVER printed; only parsed
# facts are (exit codes, booleans, symbol names). The
# sample files are built in a temp sandbox with Python
# (newline="" so line endings stay pure LF -- mixed
# endings would earn a C0327 of their own) and destroyed
# afterwards.
#
# Every expected output was produced by running the file,
# not written from memory.

import os
import re
import shutil
import subprocess
import sys
import tempfile

# ============================================================
# [1] What Pylint is [00:13]
# ============================================================
# The transcript's definition: a Linter -- a checker that
# analyzes Python files, looks for potential errors and
# clean-code (PEP 8) violations. First, is it here?

import importlib.util

pylint_present = importlib.util.find_spec("pylint") is not None
print(f"  pylint installed: {pylint_present}")
#   pylint installed: True

# (The transcript's install command is `pip install
# pylint` [01:00] -- run it in a terminal if this line
# says False.) A linter reads code WITHOUT running it --
# static analysis, like a spell-checker for programs.

# ============================================================
# [2] Why: running is not the same as clean [00:13]
# ============================================================
# The transcript's point: Python may show NO errors while
# your code quietly violates the agreed standards. A
# demonstration file that RUNS perfectly but is written
# badly -- built in the sandbox:

WORK_DIR = tempfile.mkdtemp(prefix="py89_")
messy_path = os.path.join(WORK_DIR, "messy_sample.py")
clean_path = os.path.join(WORK_DIR, "clean_sample.py")

messy_source = (
    "import os\n"
    "\n"
    "def badFunction(Data):\n"
    "    X = 42\n"
    "    return Data\n"
)
clean_source = (
    '"""A tiny clean module for lesson 89."""\n'
    "\n"
    "\n"
    "def add_numbers(first, second):\n"
    '    """Add two numbers and return the total."""\n'
    "    return first + second\n"
    "\n"
    "\n"
    "def double_number(value):\n"
    '    """Return the value multiplied by two."""\n'
    "    return value * 2\n"
)

for path, text in ((messy_path, messy_source), (clean_path, clean_source)):
    handle = open(path, "w", encoding="utf-8", newline="")
    handle.write(text)
    handle.close()

# The messy file RUNS (import os, a function, a return --
# nothing crashes) while carrying four style sins:
# an unused import, an unused variable, camelCase names,
# and no docstrings. Pylint will see them all.

# ============================================================
# [3] Running it: pylint my_file.py [02:18]
# ============================================================
# The transcript's command form. We invoke it through
# `python -m pylint` (the lesson 78 reliability trick)
# and capture EVERYTHING -- the raw report holds machine
# paths, so only parsed facts escape:

messy_run = subprocess.run(
    [sys.executable, "-m", "pylint", messy_path],
    capture_output=True,
    text=True,
)
messy_out = messy_run.stdout

print(f"  pylint responded: {len(messy_out) > 0}")
print(f"  mentions our file: {'messy_sample.py' in messy_out}")
print(f"  exit code signals findings: {messy_run.returncode != 0}")
#   pylint responded: True
#   mentions our file: True
#   exit code signals findings: True

# Output produced, our filename inside it, and a non-zero
# exit (pylint packs its verdict into an exit bitmask).
# The full text -- with C:\Users\... paths -- stays in
# the captured variable, never on screen.

# ============================================================
# [4] The rating out of 10 [02:18]
# ============================================================
# The transcript: "تقييم من 10 درجات (Rating out of 10)".
# Parse the score line and report it as FACTS:

score_match = re.search(r"rated at (\d+\.\d+)/10", messy_out)
messy_score = float(score_match.group(1)) if score_match else None

print(f"  rating line present: {score_match is not None}")
print(f"  messy rated under 10: {messy_score is not None and messy_score < 10}")
#   rating line present: True
#   messy rated under 10: True

# The line reads "Your code has been rated at X.XX/10".
# The exact number belongs to this pylint build and this
# file -- so the lesson prints the CLAIM (under 10) that
# stays true however the tool evolves. (Run it yourself
# in a terminal to watch YOUR number.)

# ============================================================
# [5] The detailed report [02:18]
# ============================================================
# The transcript's "تقريراً مفصلاً بالأخطاء والتحذيرات":
# every finding arrives as a line with a code, a message
# and a stable SYMBOL. Check the four kinds the
# transcript names (and one more):

print(f"  unused variable flagged: {'unused-variable' in messy_out}")
print(f"  unused import flagged: {'unused-import' in messy_out}")
print(f"  bad naming flagged: {'invalid-name' in messy_out}")
print(f"  missing docstring flagged: {'missing-function-docstring' in messy_out}")
print(f"  missing module docstring: {'missing-module-docstring' in messy_out}")
#   unused variable flagged: True
#   unused import flagged: True
#   bad naming flagged: True
#   missing docstring flagged: True
#   missing module docstring: True

# X is unused (W0612), os is unused (W0611), badFunction
# and Data and X break snake_case (C0103), and the
# docstrings are missing (C0114/C0116) -- exactly the
# transcript's "متغيرات غير مستخدمة" and "أسماء غير
# مطابقة للمعايير". The symbols in parentheses are the
# stable identifiers tools and humans quote.

# ============================================================
# [6] Counting the findings
# ============================================================
# How loud is the report? Count message lines (they all
# carry the filename) -- as a threshold, not a brittle
# exact number:

message_lines = [line for line in messy_out.splitlines()
                 if "messy_sample.py:" in line]

print(f"  message lines found: {len(message_lines)}")
print(f"  at least five findings: {len(message_lines) >= 5}")
#   message lines found: 7
#   at least five findings: True

# Seven lines of criticism for five lines of code -- the
# report is DENSE. (The exact count can shift with
# pylint versions; the claim "five or more" is the
# durable one.)

# ============================================================
# [7] The transcript's examples, mapped
# ============================================================
# The transcript lists typical findings: extra spaces,
# unused variables, non-standard names. Pylint's default
# checks cover the latter two directly (whitespace
# policing comes from style plugins like pycodestyle --
# noted honestly below):

print(f"  'متغيرات غير مستخدمة' -> unused-variable: {'unused-variable' in messy_out}")
print(f"  'أسماء غير مطابقة' -> invalid-name: {'invalid-name' in messy_out}")
print(f"  docstrings demanded: {'missing-function-docstring' in messy_out}")
#   'متغيرات غير مستخدمة' -> unused-variable: True
#   'أسماء غير مطابقة' -> invalid-name: True
#   docstrings demanded: True

# Each Arabic example from the transcript, tied to the
# exact symbol pylint prints. Whitespace checks (المسافات
# الزائدة) live in the pycodestyle family -- pylint
# focuses on structure, naming and dead code.

# ============================================================
# [8] One fix, measured [04:42]
# ============================================================
# The workflow the transcript describes: read the report,
# fix a note, re-run. Fix ONE thing (drop the unused
# import) and watch the report shrink:

fixed_once_source = (
    "def badFunction(Data):\n"
    "    X = 42\n"
    "    return Data\n"
)
fixed_once_path = os.path.join(WORK_DIR, "fixed_once.py")
handle = open(fixed_once_path, "w", encoding="utf-8", newline="")
handle.write(fixed_once_source)
handle.close()

fixed_run = subprocess.run(
    [sys.executable, "-m", "pylint", fixed_once_path],
    capture_output=True,
    text=True,
)
fixed_lines = [line for line in fixed_run.stdout.splitlines()
               if "fixed_once.py:" in line]

print(f"  before fix: {len(message_lines)} findings")
print(f"  after one fix: {len(fixed_lines)} findings")
print(f"  the report shrank: {len(fixed_lines) < len(message_lines)}")
#   before fix: 7 findings
#   after one fix: 6 findings
#   the report shrank: True

# One deleted import, one fewer complaint. The loop the
# transcript promises works: run -> read -> fix -> run
# again -> fewer notes.

# ============================================================
# [9] The goal: 10/10 [04:42]
# ============================================================
# The clean file -- docstrings everywhere, snake_case
# names, nothing unused -- run through the same tool:

clean_run = subprocess.run(
    [sys.executable, "-m", "pylint", clean_path],
    capture_output=True,
    text=True,
)
clean_out = clean_run.stdout
clean_match = re.search(r"rated at (\d+\.\d+)/10", clean_out)
clean_score = float(clean_match.group(1)) if clean_match else None

print(f"  clean exit code: {clean_run.returncode}")
print(f"  clean rated 10/10: {clean_score == 10.0}")
print(f"  the transcript's goal reached: {clean_score == 10.0}")
#   clean exit code: 0
#   clean rated 10/10: True
#   the transcript's goal reached: True

# Exit 0 (pylint's "no complaints at all") and the full
# 10.00/10 -- the transcript's التقييم النهائي الكامل,
# reached by following the report instead of guessing.

# ============================================================
# [10] What the clean file did right
# ============================================================
# Reverse-engineer the 10/10 -- zero message lines, and
# the properties that earned them:

clean_messages = [line for line in clean_out.splitlines()
                  if "clean_sample.py:" in line]

print(f"  zero findings: {len(clean_messages) == 0}")
print(f"  module docstring present: {clean_source.startswith(chr(34) * 3)}")
print(f"  every function documented: {clean_source.count(chr(34) * 3) == 6}")
print(f"  snake_case names: {'badFunction' not in clean_source}")
#   zero findings: True
#   module docstring present: True
#   every function documented: True
#   snake_case names: True

# One module docstring + two function docstrings = six
# triple-quote markers; names in snake_case; no dead
# imports or variables. The clean file is the messy
# file's opposite in every dimension Pylint measures.

# ============================================================
# [11] The workflow, stated [04:42]
# ============================================================
# The transcript's loop, as a checklist you can run on
# any project:

#   1. pylint my_file.py            (run it)
#   2. read the report              (symbols + messages)
#   3. fix what it names            (one note at a time)
#   4. re-run                       (count goes down)
#   5. repeat until 10/10           (exit code 0)

print("  workflow: run -> read -> fix -> re-run -> repeat")
print(f"  shrinking proven: {len(fixed_lines) < len(message_lines)}")
print(f"  10/10 proven: {clean_score == 10.0}")
#   workflow: run -> read -> fix -> re-run -> repeat
#   shrinking proven: True
#   10/10 proven: True

# Both endpoints of the loop demonstrated on real runs:
# the count fell 7 -> 6 after one fix, and the finished
# file sits at 10/10. The transcript's path from messy
# to professional, walked end to end.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- presence, the
# run, the rating, the report, the fix, the goal:

version_run = subprocess.run(
    [sys.executable, "-m", "pylint", "--version"],
    capture_output=True,
    text=True,
)

print(f"  pylint installed: {pylint_present}")
print(f"  version command works: {'pylint' in version_run.stdout.lower()}")
print(f"  messy responded: {messy_run.returncode != 0}")
print(f"  rating parsed: {score_match is not None}")
print(f"  unused variable: {'unused-variable' in messy_out}")
print(f"  invalid name: {'invalid-name' in messy_out}")
print(f"  findings >= 5: {len(message_lines) >= 5}")
print(f"  one fix shrank it: {len(fixed_lines) < len(message_lines)}")
print(f"  clean exit 0: {clean_run.returncode == 0}")
print(f"  clean 10/10: {clean_score == 10.0}")

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   pylint installed: True
#   version command works: True
#   messy responded: True
#   rating parsed: True
#   unused variable: True
#   invalid name: True
#   findings >= 5: True
#   one fix shrank it: True
#   clean exit 0: True
#   clean 10/10: True
#   sandbox removed: True

# Installed, versioned, run, parsed, diagnosed, improved
# and finished at 10/10 -- with the sandbox gone and not
# one machine path printed. Pylint, end to end.

# ============================================================
# [13] The summary
# ============================================================
# Pylint, from the transcript, complete:
#
#   1. WHAT [00:13] -- a Linter: analyzes .py files for
#      potential errors and clean-code (PEP 8) violations
#      WITHOUT running them (static analysis)
#   2. WHY [00:13] -- code can run and still break the
#      globally agreed style; Pylint unifies style to
#      what big companies require
#   3. INSTALL [01:00] -- `pip install pylint`; verified
#      here by find_spec (installed True) and by running
#      `python -m pylint --version` (works True)
#   4. RUN [02:18] -- `pylint my_file.py`; invoked as
#      `python -m pylint <file>` for interpreter
#      reliability; output captured, filename confirmed,
#      non-zero exit signals findings
#   5. THE RATING -- "Your code has been rated at
#      X.XX/10"; parsed with a regex and reported as the
#      durable claim (messy under 10 -> True); the raw
#      number belongs to the tool build, so it stays in
#      the terminal, not in this file
#   6. THE REPORT [02:18] -- one line per finding with a
#      code, message and stable symbol: unused-variable,
#      unused-import, invalid-name,
#      missing-function-docstring,
#      missing-module-docstring -- all five True on the
#      messy sample (the transcript's unused variables
#      and non-standard names, named exactly)
#   7. DENSITY -- 7 message lines for 5 lines of code
#      (>= 5 -> True); exact counts may drift with
#      versions, thresholds do not
#   8. ONE FIX, MEASURED -- dropping the unused import
#      shrank the report 7 -> 6 (shrank -> True): the
#      run/read/fix loop really reduces findings
#   9. THE GOAL [04:42] -- the clean sample (docstrings,
#      snake_case, no dead code) scores exit 0 and
#      10.00/10 (both True): the transcript's full
#      rating, reached by following the report
#  10. THE CLEAN FILE'S SECRETS -- zero findings, module
#       and function docstrings (six triple-quote
#       markers), snake_case names: the mirror image of
#       every sin in section [2]
#  11. THE WORKFLOW -- run -> read -> fix -> re-run ->
#       repeat until 10/10; both endpoints proven on
#       real subprocess runs
#  12. THE DISCIPLINE -- pylint's raw output contains
#       absolute machine paths and is NEVER printed;
#       sample files are written with newline="" (pure
#       LF -- mixed endings would earn a C0327 of their
#       own) and destroyed with the sandbox; only exit
#       codes, symbols and booleans escape
#
# The interpreter asks "does it run?". Pylint asks
# "would you sign your name under it?".
