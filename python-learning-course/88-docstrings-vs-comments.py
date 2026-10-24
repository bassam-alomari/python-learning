# -----------------------------------------------------------------
# Lesson 88: docstrings (documenting vs commenting)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : what a docstring is (triple quotes under the
#            def line), comments (#) vs docstrings -- the
#            interpreter ignores one, the object KEEPS
#            the other in __doc__, reading it
#            programmatically, help(), multi-line
#            docstrings (summary / Parameters / Returns),
#            class and module docstrings
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: an important topic --
# Docstrings, and the difference between COMMENTING and
# DOCUMENTING.
#
#   DOCSTRING [00:31] -- explanatory text written INSIDE
#   functions, classes or modules, between triple quotes
#   (""" """), directly under the definition line
#   COMMENTS (#) [01:40] -- notes for developers while
#   writing code; the interpreter IGNORES them completely
#   THE DIFFERENCE [01:40] -- a comment vanishes at
#   runtime; a docstring stays stored on the object in
#   __doc__, readable programmatically (API docs)
#   READING IT [02:17] -- function_name.__doc__ or
#   help(function_name)
#   MULTI-LINE [03:00] -- summary, Parameters, Returns
#
# Everything here is deterministic -- pure built-ins, no
# clock, no files outside a cleaned sandbox. Every
# expected output was produced by running the file, not
# written from memory.

import contextlib
import io
import os
import shutil
import sys
import tempfile

# ============================================================
# [1] What a docstring is [00:31]
# ============================================================
# Triple quotes, first statement inside the def, nothing
# between them and the def line:

def add(num1, num2):
    """Add two numbers and return the total."""
    return num1 + num2

print(f"  docstring type: {type(add.__doc__).__name__}")
print(f"  exact text: {add.__doc__}")
print(f"  the function still works: {add(2, 3)}")
#   docstring type: str
#   exact text: Add two numbers and return the total.
#   the function still works: 5

# A plain string as the first statement -- Python does
# not throw it away, it hangs it on the function as
# __doc__. And the function runs normally: the docstring
# is data, not a statement to execute.

# ============================================================
# [2] Comments vs docstrings [01:40]
# ============================================================
# A comment lives in the SOURCE; a docstring lives in the
# OBJECT. Prove both halves -- this file contains '#'
# everywhere, but the function's __doc__ never will:

source_handle = open(__file__, encoding="utf-8")
source_text = source_handle.read()
source_handle.close()

print(f"  source has comments: {'#' in source_text}")
print(f"  add.__doc__ has a comment char: {'#' in add.__doc__}")
print(f"  interpreter ignores comments: True (it ran fine)")
#   source has comments: True
#   add.__doc__ has a comment char: False
#   interpreter ignores comments: True (it ran fine)

# '#' floods this file (thousands of characters) and
# __doc__ holds none of it. The comment was never
# delivered to the object -- the transcript's "يتم
# تجاهلها تماماً بواسطة المترجم". Two channels: source
# for humans, __doc__ for the machine.

# ============================================================
# [3] The docstring is a real attribute [01:40]
# ============================================================
# __doc__ is not a display trick -- it is a stored string
# you can slice, search and pass around:

doc = add.__doc__
print(f"  stored on the object: {hasattr(add, '__doc__')}")
print(f"  it is a str: {isinstance(doc, str)}")
print(f"  length: {len(doc)}")
print(f"  starts with 'Add': {doc.startswith('Add')}")
#   stored on the object: True
#   it is a str: True
#   length: 37
#   starts with 'Add': True

# hasattr, isinstance, len, startswith -- every string
# tool works on it because it IS a string, kept alive
# after the def line has finished executing. That is the
# transcript's "يبقى مخزناً داخل كائن الدالة".

# ============================================================
# [4] Reading it with help() [02:17]
# ============================================================
# The transcript's second route: help(function) renders
# the documentation nicely in the terminal. Capture the
# rendering (lesson 75's StringIO technique) and check
# what it contains -- the raw dump is never printed:

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    help(add)
rendered = buffer.getvalue()

print(f"  help produced output: {len(rendered) > 0}")
print(f"  mentions the function name: {'add' in rendered}")
print(f"  mentions the docstring text: {'Add two numbers' in rendered}")
print(f"  has the Help header: {'Help on function' in rendered}")
#   help produced output: True
#   mentions the function name: True
#   mentions the docstring text: True
#   has the Help header: True

# help() wraps __doc__ with a header and the signature --
# the "منظم وجميل" terminal view the transcript
# describes. Underneath, it read the SAME __doc__ from
# section [3].

# ============================================================
# [5] help() vs __doc__: wrapper vs raw
# ============================================================
# Two views of one truth -- compare their roles:

print(f"  __doc__ is the raw text: {add.__doc__.startswith('Add')}")
print(f"  help adds a header: {'Help on function' in rendered}")
print(f"  both carry the same sentence: {'Add two numbers and return the total.' in rendered}")
#   __doc__ is the raw text: True
#   help adds a header: True
#   both carry the same sentence: True

# __doc__ is the warehouse; help() is the showroom. API
# tools (and other programmers' code) read __doc__;
# humans at a terminal ask for help().

# ============================================================
# [6] Multi-line docstring [03:00]
# ============================================================
# The transcript's structure for bigger code: a short
# description, then Parameters, then Returns -- all in
# one triple-quoted block:

def area(width, height):
    """Calculate the area of a rectangle.

    Parameters:
        width (float): the rectangle's width.
        height (float): the rectangle's height.

    Returns:
        float: width multiplied by height.
    """
    return width * height

multi = area.__doc__
first_line = multi.strip().splitlines()[0]

print(f"  first line is the summary: {first_line}")
print(f"  has Parameters section: {'Parameters:' in multi}")
print(f"  has Returns section: {'Returns:' in multi}")
print(f"  spans multiple lines: {len(multi.strip().splitlines()) > 5}")
print(f"  area(3, 4) still works: {area(3, 4)}")
#   first line is the summary: Calculate the area of a rectangle.
#   has Parameters section: True
#   has Returns section: True
#   spans multiple lines: True
#   area(3, 4) still works: 12

# The transcript's three ingredients in one block: short
# description first, then the parameters it accepts, then
# the value it returns. The newlines are preserved
# verbatim inside __doc__ -- print it and you get the
# whole layout back.

# ============================================================
# [7] The first-line convention
# ============================================================
# Tooling convention (and the transcript's "وصف مختصر"):
# line one stands alone, then a blank line, then the
# details. Check the structure programmatically:

lines = multi.splitlines()
print(f"  line 1 is one sentence: {lines[0].endswith('.')}")
print(f"  line 2 is blank: {lines[1] == ''}")
print(f"  details follow: {lines[2].strip().startswith('Parameters')}")
#   line 1 is one sentence: True
#   line 2 is blank: True
#   details follow: True

# Summary, blank, details -- the shape every docstring
# reader (help(), Sphinx, IDEs) expects. Structure is
# part of the documentation.

# ============================================================
# [8] Docstrings on classes too [00:31]
# ============================================================
# The transcript: functions, CLASSES, or modules. A
# class carries __doc__ the same way:

class Counter:
    """Count things up and down.

    Attributes:
        value (int): the current count.
    """

    def __init__(self):
        self.value = 0

    def bump(self):
        """Increase the count by one."""
        self.value += 1
        return self.value

print(f"  class doc first line: {Counter.__doc__.splitlines()[0]}")
print(f"  method doc: {Counter.bump.__doc__}")
print(f"  instance works: {Counter().bump()}")
#   class doc first line: Count things up and down.
#   method doc: Increase the count by one.
#   instance works: 1

# The class has its own docstring, and each METHOD has
# its own -- nested documentation, each level stored on
# its own object. help(Counter) would show both.

# ============================================================
# [9] Docstrings on modules (a real second file) [00:31]
# ============================================================
# The third home the transcript names: MODULES. Build a
# tiny module in the sandbox, import it, read its
# __doc__ -- then destroy everything:

WORK_DIR = tempfile.mkdtemp(prefix="py88_")
module_path = os.path.join(WORK_DIR, "docmod.py")

module_handle = open(module_path, "w", encoding="utf-8", newline="")
module_handle.write('"""Tiny helper module for lesson 88."""\n\n\ndef greet(name):\n    """Greet someone by name."""\n    return f"Hello {name}"\n')
module_handle.close()

sys.path.insert(0, WORK_DIR)
import docmod
sys.path.remove(WORK_DIR)

print(f"  module doc: {docmod.__doc__}")
print(f"  its function doc: {docmod.greet.__doc__}")
print(f"  it runs: {docmod.greet('Ali')}")
#   module doc: Tiny helper module for lesson 88.
#   its function doc: Greet someone by name.
#   it runs: Hello Ali

# The module-level """...""" (first statement of the
# file) landed in docmod.__doc__ -- same rule as
# functions, one level up. The file lives in the temp
# sandbox and is removed at the end of this lesson.

# ============================================================
# [10] The difference, stated as data
# ============================================================
# Everything the transcript's [01:40] claims, as
# checkable facts:

print(f"  comment char in source: True (this file is full of them)")
print(f"  comment char in add.__doc__: {'#' in add.__doc__}")
print(f"  docstring survives at runtime: {hasattr(add, '__doc__')}")
print(f"  docstring is reachable: {isinstance(add.__doc__, str)}")
print(f"  help() can show it: {'Add two numbers' in rendered}")
#   comment char in source: True (this file is full of them)
#   comment char in add.__doc__: False
#   docstring survives at runtime: True
#   docstring is reachable: True
#   help() can show it: True

# Comment: present in source, absent from the object.
# Docstring: present in the object, reachable as a str,
# renderable by help(). The whole difference in five
# lines.

# ============================================================
# [11] Documenting is for the NEXT reader
# ============================================================
# The practical payoff -- a function whose docstring
# answers the three questions a stranger asks (what does
# it take, what does it give, what does it do) WITHOUT
# reading the body:

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit.

    Parameters:
        celsius (float): temperature in degrees Celsius.

    Returns:
        float: the same temperature in Fahrenheit.
    """
    return celsius * 9 / 5 + 32

doc_lines = celsius_to_fahrenheit.__doc__.strip().splitlines()
print(f"  answers 'what': {doc_lines[0]}")
print(f"  answers 'takes': {'celsius (float)' in celsius_to_fahrenheit.__doc__}")
print(f"  answers 'gives': {'same temperature' in celsius_to_fahrenheit.__doc__}")
print(f"  and it computes: {celsius_to_fahrenheit(100)}")
#   answers 'what': Convert Celsius to Fahrenheit.
#   answers 'takes': True
#   answers 'gives': True
#   and it computes: 212.0

# Read the first three lines, never open the body, know
# the contract -- that is API documentation working as
# the transcript promises.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- stored text,
# help(), structure, class, module, and the verdict:

print(f"  add.__doc__: {add.__doc__}")
print(f"  help mentions it: {'Add two numbers' in rendered}")
print(f"  multi-line sections: {'Parameters:' in multi and 'Returns:' in multi}")
print(f"  class documented: {Counter.__doc__.splitlines()[0]}")
print(f"  module documented: {docmod.__doc__}")
print(f"  comments ignored by interpreter: True")
print(f"  docstring reachable: {isinstance(add.__doc__, str)}")

sys.modules.pop("docmod", None)
shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   add.__doc__: Add two numbers and return the total.
#   help mentions it: True
#   multi-line sections: True
#   class documented: Count things up and down.
#   module documented: Tiny helper module for lesson 88.
#   comments ignored by interpreter: True
#   docstring reachable: True
#   sandbox removed: True

# The raw text, the help view, the multi-line structure,
# the class, the module, the interpreter's shrug at
# comments, and a clean directory. Docstrings, end to
# end.

# ============================================================
# [13] The summary
# ============================================================
# Docstrings, from the transcript, complete:
#
#   1. WHAT [00:31] -- explanatory text inside functions,
#      classes or modules, between triple quotes
#      (""" """), directly under the definition line; it
#      is a STRING expression, so the function still
#      runs normally (add(2, 3) -> 5)
#   2. COMMENTS [01:40] -- '#' notes for developers; the
#      interpreter ignores them completely: this file is
#      full of '#', add.__doc__ contains none (False)
#   3. DOCSTRINGS [01:40] -- stay STORED on the object in
#      __doc__: hasattr True, isinstance str True, len
#      and startswith work on it -- data, not decoration
#   4. help() [02:17] -- renders __doc__ with a header and
#      signature ("Help on function ..."); captured via
#      StringIO and checked by content (name, sentence,
#      header all present) -- the raw dump never printed
#   5. TWO VIEWS -- __doc__ is the warehouse (raw text),
#      help() is the showroom (formatted); tools read the
#      first, humans ask for the second
#   6. MULTI-LINE [03:00] -- the transcript's structure:
#      short description, Parameters:, Returns: -- all
#      preserved verbatim in __doc__ (area(3, 4) -> 12
#      alongside)
#   7. THE FIRST-LINE CONVENTION -- line one is a
#      complete sentence ending in '.', line two blank,
#      details after: the shape help() and IDEs expect
#   8. CLASSES [00:31] -- Counter.__doc__ and
#      Counter.bump.__doc__ both stored; each level
#      documents itself (instance bump() -> 1)
#   9. MODULES [00:31] -- a sandbox file whose first
#      statement is """...""" lands in docmod.__doc__;
#      its function has its own; it runs (Hello Ali);
#      the file is destroyed with the sandbox
#  10. THE DIFFERENCE AS DATA -- comment char in source
#       True / in __doc__ False; docstring survives
#       runtime True, reachable True, help()-able True
#  11. THE PAYOFF -- celsius_to_fahrenheit's docstring
#       answers what/takes/gives WITHOUT opening the
#       body, and still computes 100 -> 212.0: that is
#       API documentation
#  12. THE DISCIPLINE -- help() output captured and
#       checked by content (lesson 75's rule); the
#       sandbox module removed; no clock, no paths --
#       byte-stable on every run
#
# Comments explain the code to the writer. Docstrings
# explain the FUNCTION to everyone who comes after.
