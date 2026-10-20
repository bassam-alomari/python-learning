# -----------------------------------------------------------------
# Lesson 76: modules -- what they are and how to import them
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : a module is a file of functions, variables, and
#            classes you import instead of rewriting; Python
#            ships a huge library of ready modules (math, os,
#            random, sys); import basics, from-import of one
#            name, aliases with as, and from ... import *
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's headline: modules are one of the greatest,
# most important topics in Python. The definition [00:21]:
#
#   A MODULE is a FILE containing a group of functions,
#   variables, and classes that perform specific tasks --
#   import it, use it, and save the time of reinventing the
#   wheel.
#
# Every .py file is a module -- including the lesson files of
# this course. Python itself ships a vast library of ready
# modules [00:30] (the transcript's "Built-in Modules" -- in
# precise terms, the STANDARD LIBRARY that travels with every
# Python install): math, os, random, sys, and hundreds more.
# Nothing to pip-install; they are already there.
#
# The import styles this lesson teaches, in the transcript's
# order:
#
#   import module                          [01:40]
#   from module import function_name      [05:45]
#   import module as alias                [05:58]
#   from module import *                  [07:02]
#
# RANDOMNESS NOTE: random values change every run, so this
# lesson NEVER prints one. It proves random() works with a
# SEEDED equality check (same seed -> same number, True or
# False, version after version).
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

# ============================================================
# [1] What is a module? A file you import
# ============================================================
# The transcript's [00:21]. math is exactly such a file --
# functions and constants compiled into the language's
# standard library. `import math` loads the whole file into
# a NAME, and the dot accesses what is inside:

import math

print(f"  math is a module file: {type(math).__name__}")
print(f"  its name: {math.__name__}")
print(f"  math.pi: {math.pi}")
#   math is a module file: module
#   its name: math
#   math.pi: 3.141592653589793

# type is "module", __name__ is "math" -- the file's identity.
# math.pi is a VARIABLE living inside that file; the dot
# (math.pi) is how you reach into a module from outside. One
# import, and the library's contents are at your prompt.

# ============================================================
# [2] Inside math: functions ready to work
# ============================================================
# The module's FUNCTIONS do the heavy lifting -- square
# roots, ceilings, floors -- the kind of mathematics you
# would otherwise write (and debug) yourself:

print(f"  sqrt(16): {math.sqrt(16)}")
print(f"  ceil(2.1): {math.ceil(2.1)}")
print(f"  floor(2.9): {math.floor(2.9)}")
print(f"  e: {math.e}")
print(f"  sqrt(2) to 4 places: {math.sqrt(2):.4f}")
#   sqrt(16): 4.0
#   ceil(2.1): 3
#   floor(2.9): 2
#   e: 2.718281828459045
#   sqrt(2) to 4 places: 1.4142

# Five calls, zero formulas written. This is the transcript's
# توفير الوقت والجهد بدلاً من إعادة اختراع العجلة -- the
# wheel already came with the car.

# ============================================================
# [3] The standard library tour: os, random, sys
# ============================================================
# The transcript's [00:30]: the library is HUGE. Three more
# of its famous members, loaded the basic way -- and a look
# at what each file offers:

import os
import random
import sys

print(f"  os offers getcwd: {callable(os.getcwd)}")
print(f"  os offers remove: {callable(os.remove)}")
print(f"  random offers random: {callable(random.random)}")
print(f"  random offers choice: {callable(random.choice)}")
print(f"  sys offers exit: {callable(sys.exit)}")
#   os offers getcwd: True
#   os offers remove: True
#   random offers random: True
#   random offers choice: True
#   sys offers exit: True

# os has run this course's whole file-handling section (65 to
# 68); random generates numbers and picks items; sys inspects
# the interpreter itself. Three files, three jobs, all
# already installed -- the "مكتبة ضخمة جداً" in miniature.

# ============================================================
# [4] import random, safely: the seeded equality proof
# ============================================================
# random's VALUES change every run -- so this lesson shows
# reproducibility instead. A seed pins the generator: the
# same seed always produces the same number, which we prove
# by asking twice:

random.seed(42)
first = random.randint(1, 1000)
random.seed(42)
second = random.randint(1, 1000)

print(f"  same seed, same number: {first == second}")
print(f"  it is an int in range: {1 <= first <= 1000}")
#   same seed, same number: True
#   it is an int in range: True

# Two calls to random.seed(42) reset the generator to the
# same starting line, so both randint() calls MUST agree --
# and they do (True). The actual number stays unprinted; the
# BOOLEAN is the lesson: random is deterministic once you
# control the seed, which is exactly how tests and lessons
# use it.

# ============================================================
# [5] import os: the filesystem file, again in context
# ============================================================
# os has been a working tool since lesson 65 -- here it
# appears as what it is: a standard-library MODULE. Two
# path helpers whose answers are identical on every
# platform:

print(f"  basename('/x/y.py'): {os.path.basename('/x/y.py')}")
print(f"  dirname('/x/y.py'): {os.path.dirname('/x/y.py')}")
print(f"  splitext('/a/b.txt'): {os.path.splitext('/a/b.txt')[0]}")
#   basename('/x/y.py'): y.py
#   dirname('/x/y.py'): /x
#   splitext('/a/b.txt'): /a/b

# basename keeps the file, dirname keeps the folder, and
# splitext cuts the extension (the [0] takes the name part).
# os.path is a module INSIDE the os module -- modules can
# nest, and the dot-map keeps working: os.path.basename.

# ============================================================
# [6] from module import function: just the one name
# ============================================================
# The transcript's [05:45]. Instead of loading the module
# and reaching through it every time, pull the ONE function
# you need and call it directly:

from math import sqrt, ceil

print(f"  sqrt(25): {sqrt(25)}")
print(f"  ceil(4.2): {ceil(4.2)}")
print(f"  no math. prefix needed: {type(sqrt).__name__}")
#   sqrt(25): 5.0
#   ceil(4.2): 5
#   no math. prefix needed: builtin_function_or_method

# sqrt(25) instead of math.sqrt(25) -- the transcript's
# "تجنب تحميل الموديول كاملاً واستدعاء الدالة مباشرة": one
# name arrives instead of the whole module, and the call
# shortens. (Under the hood the module still loaded; what
# changed is what sits in your namespace.)

# ============================================================
# [7] import ... as: the alias
# ============================================================
# The transcript's [05:58]. Long or frequent names get a
# short ALIAS -- same module object, friendlier handle. The
# classic example from the lecture, plus a check that the
# alias and the original are literally the same thing:

import random as rnd
import math as m

rnd.seed(42)
aliased_value = rnd.randint(1, 1000)

print(f"  rnd is random: {rnd is random}")
print(f"  m.pi == math.pi: {m.pi == math.pi}")
print(f"  aliased call worked: {1 <= aliased_value <= 1000}")
#   rnd is random: True
#   m.pi == math.pi: True
#   aliased call worked: True

# rnd is random -- True, because "as" only adds a second
# NAME on the same module object (the id() idea from lesson
# 69). m.pi equals math.pi for the same reason. The lecture's
# import random as rnd is the everyday form; scientific code
# favors import numpy as np the very same way.

# ============================================================
# [8] from module import *: everything at once
# ============================================================
# The transcript's [07:02]. The star grabs every public name
# in the module -- functions AND constants -- into your
# namespace in one line:

from math import *

print(f"  pi without prefix: {pi == math.pi}")
print(f"  e without prefix: {e == math.e}")
print(f"  sqrt without prefix: {sqrt(36)}")
print(f"  pow here is math's: {type(pow).__name__}")
#   pi without prefix: True
#   e without prefix: True
#   sqrt without prefix: 6.0
#   pow here is math's: builtin_function_or_method

# pi, e, and sqrt now answer without any prefix. The last
# line is the CAUTION printed as a fact: math.pow REPLACED
# the built-in pow() from lesson 71 in this namespace --
# that is the known risk of the star. It is quick in a
# scratch cell; in real projects, explicit imports (sections
# [6] and [7]) win, because no one can see what the star
# silently brought in.

# ============================================================
# [9] Looking inside a module: dir() and __name__
# ============================================================
# Curious what a module holds? dir() returns the list of
# names it exposes -- the inventory of the file:

inventory = dir(math)
print(f"  names in math: {len(inventory)}")
print(f"  has sqrt: {'sqrt' in inventory}")
print(f"  has pi: {'pi' in inventory}")
print(f"  has sin: {'sin' in inventory}")
#   names in math: 67
#   has sqrt: True
#   has pi: True
#   has sin: True

# Sixty-seven names -- functions, constants, and more,
# printed as booleans so the count stays the only number.
# dir() on ANY module (yours included) answers "what can I
# call or read here?" -- and __name__ (shown in [1]) names
# the file itself.

# ============================================================
# [10] sys: the module about Python itself
# ============================================================
# sys does not touch files or numbers -- it reports on the
# INTERPRETER running your code. Only stable, machine-
# independent facts are printed:

print(f"  major version is 3: {sys.version_info[0] == 3}")
print(f"  version is text: {type(sys.version).__name__}")
print(f"  import search path exists: {len(sys.path) > 0}")
print(f"  platform is text: {type(sys.platform).__name__}")
#   major version is 3: True
#   version is text: True
#   import search path exists: True
#   platform is text: True

# sys.version_info confirms the 3.x line this course runs
# on; sys.path is the list Python searches when YOU write
# import -- the very mechanism this whole lesson uses;
# sys.platform names the OS (never printed raw here -- it
# differs per machine). sys.exit exists for ending programs
# (callable was checked in [3]; calling it would stop this
# lesson!).

# ============================================================
# [11] Why modules exist: the wheel you did not build
# ============================================================
# The transcript's core argument [00:21], made checkable.
# Each of these would be a project to write from scratch --
# and each arrived in one import line:

would_take_forever = [
    "precise square roots and pi to 17 digits",
    "a reproducible random generator",
    "filesystem paths on any operating system",
    "interpreter introspection",
]
print(f"  problems already solved: {len(would_take_forever)}")
print(f"  sqrt(2) precise value: {math.sqrt(2)}")
print(f"  os still handles paths: {os.path.basename('/a/b.py')}")
print(f"  random still seeded: {rnd is random}")
#   problems already solved: 4
#   sqrt(2) precise value: 1.4142135623730951
#   os still handles paths: b.py
#   random still seeded: True

# Four paragraphs of "implement it yourself" work, one
# list, zero effort. math gives IEEE-grade precision, os
# keeps working across sections, and the aliased random is
# the same module. This is the economics of modules: import
# is cheaper than invention, every single time.

# ============================================================
# [12] One session: all four import styles together
# ============================================================
# The transcript's complete syntax set in one block -- the
# basic import, the single-name import, the alias, and the
# star's namespace (checked, not trusted):

import math                            # style 1: the module
from math import sqrt                  # style 2: one function
import math as mm                      # style 3: an alias

root = sqrt(49)
print(f"  basic import: {math.sqrt(9)}")
print(f"  from-import: {root}")
print(f"  alias: {mm.floor(3.9)}")
print(f"  star brought pi: {pi == mm.pi}")
print(f"  all four agree: {math is mm}")
#   basic import: 3.0
#   from-import: 7.0
#   alias: 3
#   star brought pi: True
#   all four agree: True

# Four names (math, sqrt, mm, pi) pointing into the same
# file -- and math is mm proves the alias is not a copy.
# Every style reaches the same wheel; pick per situation:
# the module name for clarity, from-import for short calls,
# an alias for long or repeated use, and the star (knowing
# its risk) when you truly want the whole toolbox.

# ============================================================
# [13] The summary
# ============================================================
# Modules, from the transcript, complete:
#
#   1. A MODULE is a FILE of functions, variables, and
#      classes for specific tasks; import it and use it
#      instead of reinventing the wheel (the transcript's
#      [00:21]); every .py file is a module -- including
#      this course's own lesson files
#   2. THE STANDARD LIBRARY ships with Python (the
#      transcript's Built-in Modules, [00:30]): math, os,
#      random, sys, and hundreds more -- installed the
#      moment Python is
#   3. import module -- the basic style [01:40]: import
#      math, then math.pi (3.141592653589793), math.sqrt,
#      math.ceil, math.floor, math.e -- five jobs, zero
#      formulas
#   4. import os / random / sys -- three more library files:
#      os reaches the filesystem (basename, dirname,
#      splitext -- platform-stable on forward-slash paths),
#      random generates (NEVER printed raw here -- the
#      seeded equality check: same seed 42 twice -> same
#      number -> True), sys reports on the interpreter
#      (version_info, sys.path -- the import search list)
#   5. from module import name -- pull ONE function [05:45]:
#      from math import sqrt, ceil; call sqrt(25) with no
#      prefix; the module still loads, the namespace gets
#      shorter
#   6. import module as alias -- a shorter handle [05:58]:
#      import random as rnd, import math as m; "rnd is
#      random" -> True: an alias is a second name on the
#      SAME module object, not a copy (lesson 69's id rule)
#   7. from module import * -- everything at once [07:02]:
#      pi, e, sqrt answer without prefixes -- and math.pow
#      silently REPLACED the built-in pow(): the star's
#      documented risk; fine for scratch work, avoided in
#      real projects in favor of explicit imports
#   8. dir(module) -- the inventory: 67 names in math, with
#      sqrt and pi inside; __name__ names the file
#   9. WHY -- four solved problems (precision, randomness,
#      paths, introspection) in one import line each; the
#      economics: import is cheaper than invention
#   10. ALL FOUR STYLES in one session, all agreeing --
#        math is mm -> True
#
# One file. One import. Someone else's tested work.
# The next lesson builds our OWN modules (custom modules).
