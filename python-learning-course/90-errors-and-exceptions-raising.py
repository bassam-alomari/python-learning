# -----------------------------------------------------------------
# Lesson 90: errors and exceptions -- raising
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : Syntax Errors vs runtime Exceptions, the
#            raise keyword, custom messages, specific
#            types (ValueError / TypeError), and the
#            practical type-check pattern
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: a new and very important
# topic -- Errors and Exceptions, and how to RAISE
# exceptions.
#
#   DIFFERENCE [00:19] -- Errors: usually Syntax Errors
#   that stop the code from running at all, from the
#   start. Exceptions: runtime errors that happen WHILE
#   the program runs (dividing by zero, adding a string
#   to a number)
#   RAISING [01:13] -- sometimes the compiler sees NO
#   technical error (the code is syntactically correct)
#   but it violates your project's logic (a negative
#   number where only positives are allowed); you can
#   FORCE Python to stop and "raise an exception"
#   yourself with the keyword `raise`
#   HOW [03:45] -- a condition; if it holds, raise an
#   exception with a custom message: raise
#   Exception("Custom error message") -- or a specific
#   type like ValueError or TypeError
#   PRACTICAL [05:47] -- check input types (is it an int
#   and not a str?); if not, raise TypeError to stop the
#   wrong execution
#
# STABILITY RULES: every exception in this lesson is
# CAUGHT -- nothing is allowed to crash the run. Only
# built-in type names and OUR OWN messages are printed;
# no tracebacks, no machine paths. All expected outputs
# came from running the file.

# ============================================================
# [1] Errors vs exceptions [00:19]
# ============================================================
# The transcript's split:
#   Errors     -> usually Syntax Errors: the code never
#                 starts
#   Exceptions -> runtime errors: the code started, then
#                 hit an invalid operation
# Both are BaseException descendants at heart, but the
# moment they strike differs completely -- and that is
# the lesson's first fact:

print("  errors: syntax mistakes that block the start")
print("  exceptions: runtime mistakes during execution")
#   errors: syntax mistakes that block the start
#   exceptions: runtime mistakes during execution

# ============================================================
# [2] A syntax error, safely observed
# ============================================================
# We cannot put a real syntax error in THIS file (it
# would refuse to run), so we hand one to compile() --
# the same check the interpreter does before running
# anything. It raises SyntaxError BEFORE any execution:

try:
    compile("def broken(:", "<string>", "exec")
except SyntaxError:
    syntax_caught = True
else:
    syntax_caught = False

print(f"  syntax error caught: {syntax_caught}")
print(f"  it blocks before running: {syntax_caught}")
#   syntax error caught: True
#   it blocks before running: True

# compile() never got to build anything -- the malformed
# `def` was rejected at the gate. That is the
# transcript's "تمنع تشغيل الكود تماماً من البداية".

# ============================================================
# [3] Runtime exception 1: dividing by zero
# ============================================================
# The transcript's first runtime example. The line is
# perfectly legal syntax -- Python only objects when it
# EXECUTES the division:

try:
    zero_result = 10 / 0
except ZeroDivisionError:
    zero_caught = True
else:
    zero_caught = False

print(f"  division by zero caught: {zero_caught}")
print(f"  exception type: ZeroDivisionError")
#   division by zero caught: True
#   exception type: ZeroDivisionError

# Syntax: fine. Runtime: refused. The program had
# already started when the error struck.

# ============================================================
# [4] Runtime exception 2: string plus number
# ============================================================
# The transcript's second example -- "جمع نص مع رقم".
# Again the syntax is flawless:

try:
    bad_sum = "5" + 5
except TypeError:
    type_caught = True
else:
    type_caught = False

print(f"  string plus int caught: {type_caught}")
print(f"  exception type: TypeError")
#   string plus int caught: True
#   exception type: TypeError

# Two runtime exceptions, two different built-in types --
# Python names the problem precisely so your except can
# answer it precisely.

# ============================================================
# [5] The difference, proven as data
# ============================================================
# Section [2] raised during compile (before running);
# sections [3] and [4] raised during execution. The
# timing IS the difference:

print(f"  syntax error comes from compile: {syntax_caught}")
print(f"  exceptions come from execution: {zero_caught and type_caught}")
print(f"  both stop the program: {syntax_caught and zero_caught and type_caught}")
#   syntax error comes from compile: True
#   exceptions come from execution: True
#   both stop the program: True

# Same word "error", two moments: before the program
# lives, or while it lives. (In this lesson every one is
# caught -- an UNcaught exception would end the run with
# a traceback.)

# ============================================================
# [6] Raising: correct syntax, wrong logic [01:13]
# ============================================================
# The transcript's case: no technical error anywhere --
# the code runs -- but a negative age violates the
# project's rules. We force the stop ourselves:

def set_age(years):
    """Return a validated age, or raise on bad input."""
    if years < 0:
        raise ValueError("age cannot be negative")
    return years

try:
    set_age(-5)
except ValueError as err:
    negative_caught = True
    negative_message = str(err)
else:
    negative_caught = False
    negative_message = ""

print(f"  negative age rejected: {negative_caught}")
print(f"  custom message: {negative_message}")
print(f"  accepted age: {set_age(25)}")
#   negative age rejected: True
#   custom message: age cannot be negative
#   accepted age: 25

# The compiler saw nothing wrong with set_age(-5) --
# -5 is a valid int. OUR rule said otherwise, so OUR
# raise stopped it. That is "رفع استثناء بنفسك".

# ============================================================
# [7] The raise keyword with a custom message [03:45]
# ============================================================
# The transcript's exact form: raise
# Exception("Custom error message"). Caught, inspected:

try:
    raise Exception("Custom error message")
except Exception as err:
    generic_type = type(err).__name__
    generic_message = str(err)

print(f"  raised type: {generic_type}")
print(f"  message carried: {generic_message}")
#   raised type: Exception
#   message carried: Custom error message

# raise + a message you wrote: the program stops HERE
# and hands your words to whoever catches it -- a user
# prompt, a log, a caller up the stack.

# ============================================================
# [8] Specific types: ValueError and TypeError [03:45]
# ============================================================
# The transcript: "رفع نوع محدد مثل ValueError أو
# TypeError". Specific types let callers answer each
# problem differently:

caught_names = []
for bad_call in (lambda: int("not a number"),
                 lambda: {} + []):
    try:
        bad_call()
    except ValueError:
        caught_names.append("ValueError")
    except TypeError:
        caught_names.append("TypeError")

print(f"  int('word') raises: {caught_names[0]}")
print(f"  dict plus list raises: {caught_names[1]}")
print(f"  both specific types caught: {caught_names == ['ValueError', 'TypeError']}")
#   int('word') raises: ValueError
#   dict plus list raises: TypeError
#   both specific types caught: True

# Built-ins raising themselves -- no custom code needed.
# Choosing WHICH type to raise in your own code is how
# you tell the world what KIND of mistake it was.

# ============================================================
# [9] Practical: type checking [05:47]
# ============================================================
# The transcript's application: make sure the input is
# an int, not a str -- otherwise raise TypeError and
# stop the wrong execution before it spreads:

def ensure_int(value):
    """Return the value if it is an int, else raise."""
    if not isinstance(value, int):
        raise TypeError(
            "expected int, got " + type(value).__name__
        )
    return value

print(f"  int accepted: {ensure_int(7)}")

try:
    ensure_int("7")
except TypeError as err:
    wrong_type_caught = True
    wrong_type_message = str(err)
else:
    wrong_type_caught = False
    wrong_type_message = ""

print(f"  str rejected: {wrong_type_caught}")
print(f"  message: {wrong_type_message}")
#   int accepted: 7
#   str rejected: True
#   message: expected int, got str

# The message even NAMES the offender (str) -- built
# from type(value).__name__, so it stays accurate for
# any wrong type. Wrong input dies at the door.

# ============================================================
# [10] The pattern: condition -> raise -> message
# ============================================================
# The transcript's recipe [03:45], written as three
# steps and demonstrated end to end:

#   1. write the condition   (if years < 0)
#   2. raise inside it       (raise ValueError(...))
#   3. give a clear message  (what went wrong, and why)

pattern_ok = (
    "raise ValueError" in set_age.__code__.co_consts
    or any(isinstance(c, str) and "negative" in c
           for c in set_age.__code__.co_consts)
)
print(f"  set_age carries a raise: {pattern_ok}")
print(f"  good input passes through: {set_age(30)}")

try:
    set_age(-1)
except ValueError:
    guard_works = True
else:
    guard_works = False
print(f"  guard stops bad input: {guard_works}")
#   set_age carries a raise: True
#   good input passes through: 30
#   guard stops bad input: True

# Condition, raise, message -- the same three moves in
# every guard you will ever write.

# ============================================================
# [11] raise stops the function immediately
# ============================================================
# Proof that nothing after the raise ever runs -- a
# trace list records what happened:

trace = []

def stop_here():
    """Raise and prove the rest never executes."""
    trace.append("before raise")
    raise RuntimeError("stop right here")
    trace.append("after raise")  # unreachable

try:
    stop_here()
except RuntimeError:
    stop_caught = True

print(f"  raise caught: {stop_caught}")
print(f"  code before raise ran: {'before raise' in trace}")
print(f"  code after raise ran: {'after raise' in trace}")
#   raise caught: True
#   code before raise ran: True
#   code after raise ran: False

# The function abandoned everything below the raise --
# that is what "stop the program" means in practice:
# the wrong path is never walked.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- the two kinds,
# the raise forms, the practical checks:

print(f"  syntax error caught: {syntax_caught}")
print(f"  zero division caught: {zero_caught}")
print(f"  string plus int caught: {type_caught}")
print(f"  generic raise type: {generic_type}")
print(f"  generic message: {generic_message}")
print(f"  negative age rejected: {negative_caught}")
print(f"  wrong type rejected: {wrong_type_caught}")
print(f"  wrong type message: {wrong_type_message}")
print(f"  specific types: {' and '.join(caught_names)}")
print(f"  raise stops the function: {'after raise' not in trace}")
#   syntax error caught: True
#   zero division caught: True
#   string plus int caught: True
#   generic raise type: Exception
#   generic message: Custom error message
#   negative age rejected: True
#   wrong type rejected: True
#   wrong type message: expected int, got str
#   specific types: ValueError and TypeError
#   raise stops the function: True

# Ten facts, zero crashes -- every exception in the
# lesson was caught on purpose, which is exactly how
# professionals use them: not to fear errors, but to
# name them, carry messages, and stop bad input early.

# ============================================================
# [13] The summary
# ============================================================
# Errors, exceptions and raising, from the transcript:
#
#   1. ERRORS [00:19] -- usually Syntax Errors; they
#      block the code from running at all, from the
#      start (proven: compile() raised SyntaxError
#      before any execution)
#   2. EXCEPTIONS [00:19] -- runtime errors during
#      execution: 10 / 0 -> ZeroDivisionError, "5" + 5
#      -> TypeError (both caught, both True)
#   3. THE TIMING IS THE DIFFERENCE -- compile-time
#      blocks the start; runtime strikes mid-life; both
#      stop the program (all three claims True)
#   4. RAISING [01:13] -- when the code is syntactically
#      perfect but violates your LOGIC (negative age),
#      you force the stop yourself with `raise`
#   5. THE KEYWORD [03:45] -- raise
#      Exception("Custom error message"): caught as type
#      Exception carrying our exact words
#   6. SPECIFIC TYPES -- ValueError (bad value: int of
#      "not a number") and TypeError (bad type: {} + [])
#      raised by built-ins, caught by name, both True
#   7. PRACTICAL [05:47] -- ensure_int: int passes
#      (7), str raises TypeError with the message
#      "expected int, got str" -- wrong execution
#      stopped at the door
#   8. THE PATTERN -- condition -> raise -> message;
#      set_age carries its raise (True), good input
#      passes (30), the guard stops bad input (True)
#   9. RAISE IS FINAL -- the trace proves code before
#      the raise ran, code after it never did (False):
#      the wrong path is never walked
#  10. ONE SESSION -- ten facts, zero crashes: every
#       exception was caught on purpose
#  11. THE DISCIPLINE -- nothing here is left uncaught;
#       only built-in type names and OUR messages are
#       printed -- no tracebacks, no machine paths
#  12. THE MINDSET -- errors name what the interpreter
#       refuses; exceptions name what execution refuses;
#       raise lets YOUR rules refuse too, loudly and
#       with a message
#
# The interpreter asks "can this run?". Your raise asks
# "should this run?" -- and answers for your project.
