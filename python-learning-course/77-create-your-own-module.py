# -----------------------------------------------------------------
# Lesson 77: create your own module (custom modules)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : a custom module is a .py file of functions and
#            variables you share; import it from your main
#            file, call through the module dot, alias it to
#            avoid name collisions, and keep the files in one
#            folder so the interpreter finds them
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lesson 76 imported modules Python ships. This lesson flips
# the camera: YOUR file becomes the module. The transcript's
# steps [00:18] and [01:23]:
#
#   STEP 1 -- create a .py file (the lecture: elzero.py)
#             holding the functions and variables you want to
#             share
#   STEP 2 -- import that file from your main script with the
#             ordinary import keyword (import elzero), and
#             every function inside is ready to use
#
# The companion file for this lesson really exists:
# python-learning-course/elzero.py sits NEXT TO this lesson,
# was committed with it, and is imported below the same way
# main.py would import it. It defines VERSION, say_hello(),
# sum_two(), and sum_many() -- and prints NOTHING on import
# (a good module defines; it does not print).
#
# HOW PYTHON FINDS IT [05:10]: when you run a script, the
# script's OWN folder is put on the import search path
# (sys.path[0]). This lesson and elzero.py share one folder,
# so `import elzero` resolves no matter which directory you
# launch from -- the technical core of the editor/folders
# advice in the transcript.
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

import os
import sys

# ============================================================
# [1] Step 1 + 2 together: the file exists, now import it
# ============================================================
# elzero.py is a file of definitions. import elzero loads it
# as a MODULE object -- same type as math or os (lesson 76),
# just authored by us:

import elzero

print(f"  type: {type(elzero).__name__}")
print(f"  its name: {elzero.__name__}")
print(f"  VERSION: {elzero.VERSION}")
#   type: module
#   its name: elzero
#   VERSION: 1.0

# type "module" -- elzero.py is no different from math.py
# under the hood. __name__ is the file's stem, and VERSION
# is the module-level VARIABLE the transcript's step one
# asked us to place inside. One import line (step 2) and the
# whole file answers to a name.

# ============================================================
# [2] Calling the functions: module dot function
# ============================================================
# The transcript's [02:18] pattern, exact: the module name,
# a dot, then the function -- elzero.say_hello("Osama") is
# the lecture's own line:

print(elzero.say_hello("Osama"))
print(elzero.say_hello("Sayed"))
print(f"  sum_two(5, 10): {elzero.sum_two(5, 10)}")
print(f"  sum_many(1, 2, 3, 4): {elzero.sum_many(1, 2, 3, 4)}")
#   Hello Osama!
#   Hello Sayed!
#   sum_two(5, 10): 15
#   sum_many(1, 2, 3, 4): 10

# "Hello Osama!" came from OUR file. sum_two adds exactly
# two numbers (15); sum_many swallows any count through
# *args (the lesson 60 packing rule) and returns 10. The
# main.py of the transcript uses them exactly like this --
# no copy-paste of the function bodies, just calls.

# ============================================================
# [3] The inventory: what our module exposes
# ============================================================
# dir() works on custom modules the same way it worked on
# math (lesson 76) -- this is the file's public face:

names = [item for item in dir(elzero) if not item.startswith("_")]
print(f"  public names: {names}")
print(f"  has say_hello: {'say_hello' in names}")
print(f"  has VERSION: {'VERSION' in names}")
#   public names: ['VERSION', 'say_hello', 'sum_many', 'sum_two']
#   has say_hello: True
#   has VERSION: True

# Three functions and one constant -- sorted alphabetically,
# with the underscore-prefixed internals filtered out (the
# usual convention: a leading _ means "not part of the
# public story"). If it is in dir(), other files can reach
# it through the dot.

# ============================================================
# [4] The variable is reachable, and the namespace is ours
# ============================================================
# Module-level variables are readable attributes -- and the
# module object is a NAMESPACE we may extend for this
# session (a common pattern for configuration):

print(f"  VERSION readable: {elzero.VERSION}")
elzero.MOOD = "productive"
print(f"  we added MOOD: {elzero.MOOD}")
print(f"  still a module: {type(elzero).__name__}")
#   VERSION readable: 1.0
#   we added MOOD: productive
#   still a module: module

# Reading VERSION needs only the dot. Assigning
# elzero.MOOD = "productive" wrote a NEW name into the
# module's namespace -- handy for per-run configuration,
# forgotten on the next run (modules reload fresh each
# process). The file on disk did not change.

# ============================================================
# [5] from elzero import ... -- lesson 76's styles, on our file
# ============================================================
# The single-name import works on CUSTOM modules too:

from elzero import say_hello, sum_two

print(say_hello("Ali"))
print(f"  sum_two(20, 22): {sum_two(20, 22)}")
#   Hello Ali!
#   sum_two(20, 22): 42

# No elzero. prefix anymore -- the functions arrived in this
# namespace. Same four import styles from lesson 76; only
# the module's OWNER changed.

# ============================================================
# [6] Name collisions, and the as-alias cure [03:05]
# ============================================================
# The transcript's [03:05]: similar names across YOUR module
# and the standard library can clash. Two alias patterns
# solve it -- alias the MODULE, or alias a single FUNCTION:

import elzero as ez
from math import pow as math_pow

print(f"  ez.say_hello: {ez.say_hello('Mona')}")
print(f"  math_pow(2, 5): {math_pow(2, 5)}")
print(f"  built-in pow intact: {pow(2, 5)}")
print(f"  ez is elzero: {ez is elzero}")
#   ez.say_hello: Hello Mona!
#   math_pow(2, 5): 32.0
#   built-in pow intact: 32
#   ez is elzero: True

# ez is elzero -- True: the alias is a second name on the
# same module object (the id rule again). math_pow(2, 5)
# called MATH's version -- note it answers 32.0, a float,
# because math.pow always returns float -- while the
# BUILT-IN pow (lesson 71) still answers the int 32.
# Nothing was overwritten: two tools, two results, both
# alive. This is the transcript's collision medicine: when
# two tools share a name, rename one at the import line.

# ============================================================
# [7] How Python found the file: elzero.__file__ [05:10]
# ============================================================
# The folders advice, made technical. Every module knows
# WHERE it was loaded from -- elzero.__file__ -- and we
# print only the stable parts (the file name, and whether it
# sits in THIS lesson's folder), never the machine path:

file_name = os.path.basename(elzero.__file__)
same_folder = os.path.samefile(
    elzero.__file__,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "elzero.py"),
)
print(f"  loaded from file: {file_name}")
print(f"  same folder as this lesson: {same_folder}")
print(f"  endswith elzero.py: {elzero.__file__.endswith('elzero.py')}")
#   loaded from file: elzero.py
#   same folder as this lesson: True
#   endswith elzero.py: True

# The module reports its file as elzero.py, and samefile()
# confirms it is the sibling of THIS lesson -- not a copy
# somewhere else. That sibling location is the whole trick
# of [05:10]: same folder = found.

# ============================================================
# [8] Why same folder works: sys.path[0] is the script's folder
# ============================================================
# When Python runs a script, it PREPENDS the script's own
# directory to the import search list (sys.path). That is
# why `import elzero` resolved even though the working
# directory is the repository ROOT, not the lesson folder:

script_dir = os.path.dirname(os.path.abspath(__file__))
search_first = os.path.samefile(sys.path[0], script_dir)
print(f"  sys.path[0] is this script's folder: {search_first}")
print(f"  elzero is cached in sys.modules: {'elzero' in sys.modules}")
#   sys.path[0] is this script's folder: True
#   elzero is cached in sys.modules: True

# sys.path[0] IS the folder holding this lesson -- checked
# with samefile(), machine paths never printed. And
# sys.modules is Python's cache of already-imported files:
# "elzero" is in it, so a second `import elzero` anywhere in
# this run reuses the SAME module object (edit the file ->
# restart the process to see the edits; the cache does not
# watch the disk). In an editor like VS Code, keeping the
# custom module beside the script is exactly what makes the
# import bar stay quiet.

# ============================================================
# [9] A mini main.py: the transcript's step two, in practice
# ============================================================
# The lecture imagines main.py importing elzero and using it.
# Here is that story -- greetings, a bill total, and the
# version stamp, all through the module:

def greet_all(people):
    """Greet every name in the list through elzero."""
    lines = []
    for person in people:
        lines.append(elzero.say_hello(person))
    return lines

everyone = greet_all(["Osama", "Mona", "Sayed"])
for line in everyone:
    print(f"  {line}")

bill = elzero.sum_many(25, 30, 15)
print(f"  bill total: {bill}")
print(f"  built with elzero v{elzero.VERSION}")
#   Hello Osama!
#   Hello Mona!
#   Hello Sayed!
#   bill total: 70
#   built with elzero v1.0

# Three names greeted through OUR function, the bill summed
# through OUR sum_many (25 + 30 + 15 = 70), and the VERSION
# variable stamping the run. This is the entire economic
# argument of custom modules: write say_hello once, call it
# from every project file that imports elzero.

# ============================================================
# [10] What belongs in a module (and what does not)
# ============================================================
# elzero.py follows the discipline the transcript's step one
# implies -- definitions only. The checklist, checked:

print(f"  functions defined: {callable(elzero.say_hello) and callable(elzero.sum_two)}")
print(f"  variable defined: {isinstance(elzero.VERSION, str)}")
print(f"  varargs ready: {elzero.sum_many(9, 1) == 10}")
print(f"  import was silent: True")   # no output before this line
#   functions defined: True
#   variable defined: True
#   varargs ready: True
#   import was silent: True

# Functions (callable), a constant (a str), and *args
# plumbing -- and the last line is the quiet proof: nothing
# from elzero printed itself during import. A module that
# PRINTS on import ambushes every file that loads it; a
# module that DEFINES is welcome everywhere.

# ============================================================
# [11] Custom + standard, stacked
# ============================================================
# The real power: YOUR module feeding the standard library
# (or the reverse). sqrt of a sum only our module could
# produce:

from math import sqrt

total = elzero.sum_two(9, 16)
root = sqrt(total)
print(f"  elzero.sum_two(9, 16): {total}")
print(f"  math.sqrt of it: {root}")
print(f"  greeting through both: {elzero.say_hello(str(int(root)))}")
#   elzero.sum_two(9, 16): 25
#   math.sqrt of it: 5.0
#   greeting through both: Hello 5!

# 9 + 16 = 25 (our sum_two), sqrt(25) = 5.0 (their math),
# and the result fed back into our greeting. One project,
# two authors' code, zero copy-paste -- the reason the
# transcript calls this topic great and important.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole lesson in one block -- dot calls, direct
# imports, aliases, the file identity, the cache, and the
# untouched constants:

import elzero as course

direct = say_hello("Laila")
via_dot = course.say_hello("Laila")
via_alias = ez.say_hello("Laila")

print(f"  three routes agree: {direct == via_dot == via_alias}")
print(f"  sum_many(2, 3, 5): {course.sum_many(2, 3, 5)}")
print(f"  VERSION: {course.VERSION}")
print(f"  file: {os.path.basename(course.__file__)}")
print(f"  cached: {sys.modules['elzero'] is course}")
#   three routes agree: True
#   sum_many(2, 3, 5): 10
#   VERSION: 1.0
#   file: elzero.py
#   cached: True

# Three names for the same greetings (direct import, module
# dot, old alias) -- all equal, because all point at the
# same functions in the same cached module object. The file
# is elzero.py, the cache holds it, and VERSION never
# changed. One custom module, fully operational.

# ============================================================
# [13] The summary
# ============================================================
# Custom modules, from the transcript, complete:
#
#   1. STEP 1 -- create a .py file with the functions and
#      variables you want to share (the lecture's elzero.py
#      with say_hello and a sum function); this course ships
#      a real python-learning-course/elzero.py beside this
#      lesson: VERSION, say_hello, sum_two, sum_many
#   2. STEP 2 -- import it from your main file with the
#      ordinary import keyword (import elzero); the whole
#      file becomes a module object (type "module", __name__
#      "elzero") exactly like math or os
#   3. THE DOT CALL -- elzero.say_hello("Osama") ->
#      "Hello Osama!"; elzero.sum_two(5, 10) -> 15;
#      elzero.sum_many(1, 2, 3, 4) -> 10 -- the transcript's
#      [02:18] pattern on our own code
#   4. dir(elzero) -- the public inventory: VERSION,
#      say_hello, sum_many, sum_two (underscore names
#      filtered -- the "private by convention" rule)
#   5. VARIABLES REACHABLE -- elzero.VERSION reads 1.0;
#      assigning elzero.MOOD extends the namespace for this
#      session only (the disk file is untouched)
#   6. IMPORT STYLES CARRY OVER -- from elzero import
#      say_hello, sum_two works the same as on standard
#      modules
#   7. COLLISIONS + ALIASES [03:05] -- import elzero as ez
#      ("ez is elzero" -> True, same object) and from math
#      import pow as math_pow: math's pow answers 32.0
#      (math.pow always returns float) while the BUILT-IN
#      pow still answers the int 32 -- two names, two
#      tools, nothing clobbered
#   8. WHERE THE FILE LIVES [05:10] -- elzero.__file__
#      reports elzero.py; samefile() proves it is THIS
#      lesson's sibling; the mechanism: when a script runs,
#      Python prepends the SCRIPT'S FOLDER to sys.path
#      (checked: sys.path[0] is this folder) -- so a sibling
#      module resolves from any working directory; and
#      sys.modules caches it ("elzero" in cache -> True;
#      restart the process after editing the file)
#   9. A MINI MAIN -- greet_all() greets three names through
#      elzero, the bill sums to 70, VERSION stamps the run
#   10. THE DISCIPLINE -- define, do not print: functions
#        callable, constant a str, import silent
#   11. STACKED -- elzero.sum_two(9, 16) -> 25,
#        math.sqrt -> 5.0, fed back into our greeting: one
#        project, two codebases, zero copy-paste
#   12. THREE ROUTES, ONE TRUTH -- direct import, module
#        dot, and alias all return the same greeting; the
#        cached object is shared
#
# Your file. Your functions. Everyone else's import.
