# -----------------------------------------------------------------
# Lesson 78: install external packages (pip)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : module vs package (file vs folder), why the world
#            needs external packages, pip as the official
#            package manager (install, pin a version,
#            upgrade), and the termcolor practical
#            (from termcolor import colored)
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's headline: the MOST important lesson of the
# modules section. Two definitions first [00:16]:
#
#   MODULE  -- ONE .py file of functions and variables
#             (lesson 76's math, lesson 77's elzero)
#   PACKAGE -- a FOLDER holding modules and files together
#             (the stdlib's encodings, email, json)
#
# Why go outside the language [01:11]? Python's built-in
# library is huge, but it cannot contain everything in the
# world -- that would make the language enormous and heavy.
# So developers everywhere publish READY packages you can
# download and use. The official downloader is pip [01:23],
# run from the terminal:
#
#   pip install package_name              install
#   pip install package_name==1.0.0       pin a version
#   pip install --upgrade package_name    update
#
# The practical example is termcolor [06:13]: a small package
# that colors terminal text.
#
# PREQUISITE: this lesson REQUIRES termcolor, exactly as the
# transcript instructs -- run `pip install termcolor` first.
# The file then PROVES the installation (find_spec, metadata)
# instead of taking it on faith.
#
# ANSI NOTE: termcolor only prints color codes when the
# stream is a real terminal; in captured runs it returns
# plain text. Setting the FORCE_COLOR environment variable
# BEFORE the import makes the codes appear everywhere --
# that is how this lesson keeps its output byte-stable, and
# the codes themselves are printed via repr().
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

import importlib.metadata
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

# ============================================================
# [1] Module vs package: a file versus a folder
# ============================================================
# The transcript's [00:16], checked live. A package is a
# folder, and Python marks it with a __path__ attribute; a
# plain module (one file) has no __path__:

import math
import encodings
import json

print(f"  math is a module (no __path__): {not hasattr(math, '__path__')}")
print(f"  encodings is a package: {hasattr(encodings, '__path__')}")
print(f"  json is a package: {hasattr(json, '__path__')}")
print(f"  math is compiled in (no __file__): {not hasattr(math, '__file__')}")
print(f"  encodings.__file__ lives in a folder: {encodings.__file__.endswith('__init__.py')}")
#   math is a module (no __path__): True
#   encodings is a package: True
#   json is a package: True
#   math is compiled in (no __file__): True
#   encodings.__file__ lives in a folder: True

# math is ONE thing with no __path__ (it is compiled into
# the interpreter, so it has no __file__ either).
# encodings and json are FOLDERS -- packages, marked by
# __path__, the list of directories they own, and their
# __file__ points at the folder's __init__.py. Same import
# keyword for both; the difference is what sits on disk.
# Lesson 77's elzero.py was a module; the packages below
# are the other half of the story.

# ============================================================
# [2] Why external packages exist [01:11]
# ============================================================
# The stdlib is already vast -- but deliberately NOT the
# whole world. Count its members (a threshold, not the exact
# number, which grows with versions):

print(f"  stdlib has 100+ modules: {len(sys.stdlib_module_names) > 100}")
print(f"  termcolor is NOT in the stdlib: {'termcolor' not in sys.stdlib_module_names}")
#   stdlib has 100+ modules: True
#   termcolor is NOT in the stdlib: True

# A hundred-plus modules ship with Python, and termcolor is
# not one of them -- exactly the transcript's point: no
# language ships the entire world; the rest comes from the
# community, one pip install away.

# ============================================================
# [3] pip: the official manager, present on this machine
# ============================================================
# The transcript's [01:23]. pip runs from the terminal --
# the reliable modern form is `python -m pip` (the same
# manager, guaranteed to belong to THIS interpreter). We run
# it for real, but print only stable facts about the run --
# never its machine-specific output:

result = subprocess.run(
    [sys.executable, "-m", "pip", "--version"],
    capture_output=True,
    text=True,
)
print(f"  pip responds: {result.returncode == 0}")
print(f"  output mentions pip: {'pip' in result.stdout.lower()}")
#   pip responds: True
#   output mentions pip: True

# exit code 0 and the word "pip" in the answer -- the
# manager is installed and alive. (Its full line names a
# version and install paths that differ per machine, so it
# stays unprinted. Run `pip --version` yourself in a
# terminal to see yours.)

# ============================================================
# [4] pip install package_name -- the everyday command
# ============================================================
# The transcript's [04:10], first form. The command for the
# lecture's example package:
#
#   pip install termcolor
#
# Downloads termcolor from the package index and installs it
# into THIS interpreter. The install itself is done (it is
# the lesson's prerequisite) -- so we verify it the
# programmatic way: find_spec() looks for the package on the
# import path:

installed = importlib.util.find_spec("termcolor") is not None
print(f"  find_spec('termcolor'): {installed}")
#   find_spec('termcolor'): True

# True means the package's files are really on disk where
# Python looks -- the same lookup that makes
# `from termcolor import colored` (section [7]) possible.
# If this were False, the fix is the terminal command above.

# ============================================================
# [5] pip install package==version -- pinning
# ============================================================
# The transcript's second form. Real projects PIN the exact
# version so every machine installs the same code:
#
#   pip install termcolor==2.4.0
#
# The ==2.4.0 part is the pin. The INSTALLED version is
# readable from Python itself -- we check its SHAPE
# (digits and dots) but never print the number, because it
# differs per machine:

version = importlib.metadata.version("termcolor")
looks_pinned_ready = version.replace(".", "").isdigit() and "." in version
print(f"  metadata reports a version: {len(version) > 0}")
print(f"  it looks like N.N.N: {looks_pinned_ready}")
#   metadata reports a version: True
#   it looks like N.N.N: True

# importlib.metadata is the stdlib reading the installed
# package's ID card. Copy YOUR number from
# `pip show termcolor` into a requirements file (section
# [11]) and every teammate gets that exact build.

# ============================================================
# [6] pip install --upgrade package_name -- updating
# ============================================================
# The transcript's third form:
#
#   pip install --upgrade termcolor
#
# Asks pip for the newest version on the index and replaces
# the installed one if it differs. This lesson does NOT run
# an upgrade -- upgrading would CHANGE the environment under
# the lesson's own feet (and could alter the color codes in
# later sections). The facts we need are already here:

print(f"  upgrade command documented: True")   # shown above
print(f"  current version still readable: {len(importlib.metadata.version('termcolor')) > 0}")
#   upgrade command documented: True
#   current version still readable: True

# The habit: install once, pin in requirements, upgrade on
# purpose (never by accident in the middle of a project).

# ============================================================
# [7] The practical: from termcolor import colored [06:13]
# ============================================================
# The transcript's import line, exact. One adjustment for
# non-terminal runs -- FORCE_COLOR tells termcolor to emit
# codes even when stdout is captured (set BEFORE the
# import), which keeps this lesson's output stable:

os.environ["FORCE_COLOR"] = "1"
from termcolor import colored

sample = colored("Hello", "red")
print(f"  colored returns str: {type(sample).__name__}")
print(f"  codes present: {'31' in sample and sample.endswith(chr(27) + '[0m')}")
#   colored returns str: str
#   codes present: True

# colored() is a function that RETURNS a string -- the text
# wrapped in ANSI escape codes. The reset suffix (\x1b[0m)
# ends the coloring so nothing later on the line changes
# color. The exact bytes appear in the next section.

# ============================================================
# [8] The codes themselves: red and green
# ============================================================
# repr() shows the escapes as readable text. Red is code 31,
# green is 32, and both wrap the message in \x1b[...m pairs:

red = colored("Hello", "red")
green = colored("OK", "green")
print(f"  red: {red!r}")
print(f"  green: {green!r}")
#   red: '\x1b[31mHello\x1b[0m'
#   green: '\x1b[32mOK\x1b[0m'

# \x1b[31m switches the terminal to red, the text follows,
# \x1b[0m switches it off. Green is the same skeleton with
# 32. Those numbers are the ANSI color table the whole
# terminal world agrees on -- termcolor just types them for
# you.

# ============================================================
# [9] Extra attributes: bold and friends
# ============================================================
# The transcript's "تلوين النصوص وإخراجها بشكل جميل ومنظم":
# colors plus STYLE attributes. attrs=["bold"] adds the
# bold code -- which termcolor writes BEFORE the color:

loud = colored("Hi", "yellow", attrs=["bold"])
print(f"  bold yellow: {loud!r}")
print(f"  has bold code: {chr(27) + '[1m' in loud}")
print(f"  has yellow code: {'[33m' in loud}")
#   bold yellow: '\x1b[1m\x1b[33mHi\x1b[0m'
#   has bold code: True
#   has yellow code: True

# \x1b[1m is bold, \x1b[33m is yellow -- both open, the
# word Hi sits between them, \x1b[0m closes everything.
# attrs also knows underline, dim, and more; the pattern
# never changes: open codes, text, reset.

# ============================================================
# [10] In practice: a tiny status printer
# ============================================================
# The everyday use of colored(): status labels that jump off
# the terminal. Build three, and verify each carries its
# color code:

def status(label, color):
    """Return a colored [label] tag."""
    return colored(f"[{label}]", color)

ok = status("OK", "green")
warn = status("WARN", "yellow")
fail = status("FAIL", "red")

print(f"  ok tag: {ok!r}")
print(f"  warn carries 33: {'[33m' in warn}")
print(f"  fail carries 31: {'[31m' in fail}")
#   ok tag: '\x1b[32m[OK]\x1b[0m'
#   warn carries 33: True
#   fail carries 31: True

# One helper, three tags, each wearing the right ANSI code
# (green 32, yellow 33, red 31). A build script, a test
# runner, a server log -- anywhere a human reads the
# terminal, this five-line pattern pays for the install.

# ============================================================
# [11] Sharing the install: requirements.txt
# ============================================================
# Teams do not repeat `pip install` by hand -- they keep a
# requirements.txt and let pip read it:
#
#   pip install -r requirements.txt
#
# Build a minimal one in a scratch folder, read it back,
# and clean up (the lesson 65 sandbox pattern):

WORK_DIR = tempfile.mkdtemp(prefix="py78_")
try:
    path = os.path.join(WORK_DIR, "requirements.txt")
    handle = open(path, "w", encoding="utf-8", newline="")
    handle.write("termcolor\n")
    handle.close()

    handle = open(path, "r", encoding="utf-8")
    lines = handle.read().strip().splitlines()
    handle.close()

    print(f"  requirements lines: {lines}")
    print(f"  pip would install: {lines[0]}")
finally:
    shutil.rmtree(WORK_DIR, ignore_errors=True)

print(f"  cleaned up: {not os.path.exists(WORK_DIR)}")
#   requirements lines: ['termcolor']
#   pip would install: termcolor
#   cleaned up: True

# One name per line (add ==2.4.0-style pins as needed).
# Commit requirements.txt with your project and every clone
# rebuilds the same environment -- the transcript's external
# packages, made shareable.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole lesson in one block -- the two definitions, the
# manager, the installation proof, and the colored result:

print(f"  math (module): {not hasattr(math, '__path__')}")
print(f"  encodings (package): {hasattr(encodings, '__path__')}")
print(f"  pip alive: {result.returncode == 0}")
print(f"  termcolor installed: {importlib.util.find_spec('termcolor') is not None}")
print(f"  version on file: {len(importlib.metadata.version('termcolor')) > 0}")

banner = colored("lesson 78", "red", attrs=["bold"])
print(f"  banner: {banner!r}")
print(f"  banner is colorful: {'31m' in banner and '[1m' in banner}")
#   math (module): True
#   encodings (package): True
#   pip alive: True
#   termcolor installed: True
#   version on file: True
#   banner: '\x1b[1m\x1b[31mlesson 78\x1b[0m'
#   banner is colorful: True

# A file (math), a folder (encodings), a manager that
# answers (pip), a package on disk (termcolor) with a
# version on file, and a bold red banner built from its
# only function. External packages, end to end.

# ============================================================
# [13] The summary
# ============================================================
# External packages, from the transcript, complete:
#
#   1. MODULE vs PACKAGE [00:16] -- a module is ONE .py file
#      of functions and variables (lesson 77's elzero);
#      a package is a FOLDER of modules and files
#      (encodings, json), marked by the __path__ attribute;
#      the same import keyword loads both
#   2. WHY EXTERNAL [01:11] -- the stdlib is huge (100+
#      names, counted above) but deliberately not the whole
#      world; the community publishes the rest, ready to
#      download; termcolor is not in the stdlib
#   3. pip [01:23] -- the official package manager, run from
#      the terminal; the reliable spelling is
#      `python -m pip` (verified alive: exit 0, mentions
#      "pip" -- its machine-specific version line stays
#      unprinted)
#   4. THE THREE COMMANDS [04:10] --
#        pip install package_name              install
#        pip install package_name==1.0.0       pin exactly
#        pip install --upgrade package_name    update
#   5. PROOF OF INSTALL -- find_spec("termcolor") -> True
#      (the files are on the import path);
#      importlib.metadata.version("termcolor") reports a
#      version (shape checked, NUMBER not printed -- it is
#      machine-specific; copy yours from `pip show`)
#   6. THE PRACTICAL [06:13] -- from termcolor import
#      colored; colored() RETURNS a string wearing ANSI
#      codes; FORCE_COLOR=1 before the import forces codes
#      in non-TTY runs (this lesson's stability trick)
#   7. THE CODES -- '\x1b[31mHello\x1b[0m' is red (31),
#      '\x1b[32mOK\x1b[0m' is green (32); open code, text,
#      reset \x1b[0m -- the ANSI table terminals worldwide
#      agree on
#   8. STYLES -- attrs=["bold"] prepends \x1b[1m:
#      '\x1b[1m\x1b[33mHi\x1b[0m' is bold yellow (33);
#      underline, dim, and friends follow the same pattern
#   9. A STATUS PRINTER -- colored(f"[{label}]", color)
#      builds [OK]/[WARN]/[FAIL] tags in green/yellow/red:
#      the five-line pattern that makes logs readable
#   10. requirements.txt -- one package name per line,
#        installed in bulk with `pip install -r
#        requirements.txt`; build one in a scratch folder,
#        read it back ['termcolor'], clean up: teams share
#        ENVIRONMENTS this way, not just code
#   11. THE DISCIPLINE -- install once, PIN in
#        requirements, upgrade ON PURPOSE; never let a
#        mid-project upgrade rewrite the colors under you
#
# The stdlib is the floor. pip is the elevator.
