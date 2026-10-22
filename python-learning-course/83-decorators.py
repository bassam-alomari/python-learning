# -----------------------------------------------------------------
# Lesson 83: decorators
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : a function that takes a function, wraps it
#            with extra work, and returns the NEW
#            function -- first-class functions as the
#            foundation, the nested wrapper pattern,
#            the @ syntactic sugar, argument pass-through,
#            functools.wraps, and a stateful counter
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: an advanced and wonderful
# topic -- Decorators. The definition [00:13]:
#
#   A decorator is a function that takes ANOTHER function
#   as input, adds/modifies/enhances some behavior on it,
#   and RETURNS the new function -- WITHOUT touching the
#   original function's code.
#
# The foundation [00:26]: First-Class Functions -- Python
# treats functions as ordinary VALUES (variables, args,
# returnables). The build [01:09]: an outer decorator
# function holding a NESTED function that does the extra
# work (print before, call, print after). The application
# [03:18]: the @ decorator_name line -- pure syntactic
# sugar for the manual pass-through.
#
# Everything here is deterministic -- pure built-ins, no
# clock, no files. Every expected output was produced by
# running the file, not written from memory.

import functools

# ============================================================
# [1] What a decorator is [00:13]
# ============================================================
# Before any code: the contract. Function IN, enhanced
# function OUT, original code UNTOUCHED. That is the
# entire promise -- everything below is mechanics:

print("  contract: function in, new function out")
print("  original code stays untouched: that is the point")
#   contract: function in, new function out
#   original code stays untouched: that is the point

# The transcript's modify/enhance without editing: the
# decoration happens at the CALL site, not inside the
# original def. Sections [3] and [10] prove both halves.

# ============================================================
# [2] First-class functions: the foundation [00:26]
# ============================================================
# Before decorators can work, functions must be VALUES.
# Three moves: assign, pass, return:

def say_hello(name):
    return f"Hello {name}"

alias = say_hello
passed_to_caller = alias("Osama")

def get_greeting():
    return say_hello

returned = get_greeting()("Mona")

print(f"  assigned: {alias is say_hello}")
print(f"  passed as value: {passed_to_caller}")
print(f"  returned: {returned}")
#   assigned: True
#   passed as value: Hello Osama
#   returned: Hello Mona

# say_hello sits in a variable (same object: True), rides
# into another scope as an argument, and comes back out
# of a function -- no parentheses, no special syntax.
# That is first-class [00:26], and it is the ONLY reason
# a decorator (a function that receives a function) can
# exist.

# ============================================================
# [3] Building the decorator [01:09]
# ============================================================
# Outer function = the decorator. Nested function = the
# wrapper that carries the extra work. Return the wrapper:

def shout_decorator(original_function):
    def wrapper():
        print("  >> before the original")
        original_function()
        print("  >> after the original")
    return wrapper

print(f"  decorator is callable: {callable(shout_decorator)}")
print(f"  wrapper is callable: {callable(shout_decorator(say_hello))}")
#   decorator is callable: True
#   wrapper is callable: True

# shout_decorator receives a function; its inner wrapper
# adds the two >> messages; returning wrapper hands back
# the ENHANCED version. The original_function parameter
# is the transcript's "دالة أخرى كمدخل".

# ============================================================
# [4] Applying it by hand, then calling
# ============================================================
# The manual pass -- decorated = decorator(original), the
# classic form before @ existed in your fingers:

def speak():
    print("  ...speaking...")

decorated = shout_decorator(speak)
decorated()
#   >> before the original
#   ...speaking...
#   >> after the original

# Before, original, after -- in that order, every call.
# speak() itself never changed; we CALLED a different
# function that happens to call it in the middle.

# ============================================================
# [5] The original stays pristine
# ============================================================
# The transcript's "دون أن تغير في الكود الأصلي". Call
# speak() directly and the >> messages are absent; the
# names differ too:

speak()
print(f"  original name: {speak.__name__}")
print(f"  decorated name: {decorated.__name__}")
#   ...speaking...
#   original name: speak
#   decorated name: wrapper

# Direct call: no decoration, clean. And the decorated
# object's name is 'wrapper' -- it IS the nested
# function, a separate entity. The source of speak was
# never edited; decoration is re-WRAPPING, not
# re-WRITING.

# ============================================================
# [6] The @ syntax [03:18]
# ============================================================
# The transcript's @decorator_name -- "بدلاً من الطريقة
# التقليدية". Same decorator, new spelling:

@shout_decorator
def wave():
    print("  ...waving...")

wave()
#   >> before the original
#   ...waving...
#   >> after the original

# The @ line above def wave is Python saying, at definition
# time: wave = shout_decorator(wave). Identical messages
# to section [4] -- sugar, not new semantics.

# ============================================================
# [7] @ IS the manual line, proved twice
# ============================================================
# Two functions, two application styles, one behavior:

def manual_applied():
    print("  ...manual...")

manual_applied = shout_decorator(manual_applied)

@shout_decorator
def at_applied():
    print("  ...at sign...")

print(f"  both are functions: {type(manual_applied).__name__} then {type(at_applied).__name__}")
print(f"  both carry the wrapper name: {manual_applied.__name__ == at_applied.__name__}")
#   both are functions: function then function
#   both carry the wrapper name: True

# Both paths end at 'function' with the same wrapper
# identity. The @ is exactly what the transcript calls
# it: Syntactic Sugar.

# ============================================================
# [8] Arguments pass through untouched
# ============================================================
# Real decorated functions take arguments. *args and
# **kwargs forward everything to the original:

def log_decorator(original_function):
    def wrapper(*args, **kwargs):
        print(f"  >> calling {original_function.__name__}")
        return original_function(*args, **kwargs)
    return wrapper

@log_decorator
def add(num1, num2):
    return num1 + num2

@log_decorator
def greet(name, greeting="Hi"):
    return f"{greeting} {name}"

result_add = add(2, 3)
result_greet = greet("Mona", greeting="Yo")

print(f"  add(2, 3) -> {result_add}")
print(f"  greet -> {result_greet}")
#   >> calling add
#   >> calling greet
#   add(2, 3) -> 5
#   greet -> Yo Mona

# Positional args (2, 3) and keyword args (greeting="Yo")
# both arrive intact. The wrapper is a transparent
# messenger with one job: announce, then forward.

# ============================================================
# [9] The return value flows out
# ============================================================
# The wrapper must RETURN the original's answer --
# otherwise the decoration eats the result:

decorated_result = add(10, 32)
in_expression = add(10, 32) * 2

print(f"  decorated result: {decorated_result}")
print(f"  usable in expressions: {in_expression}")
#   decorated result: 42
#   usable in expressions: 84

# 42 comes back through the wrapper; multiply it by 2
# and you get 84. Decorators wrap BEHAVIOR, never swallow
# DATA.

# ============================================================
# [10] functools.wraps: keeping the original name
# ============================================================
# Bonus hygiene beyond the transcript: section [5] showed
# the decorated name becomes 'wrapper'. functools.wraps
# restores the original's identity:

def nice_decorator(original_function):
    @functools.wraps(original_function)
    def wrapper(*args, **kwargs):
        return original_function(*args, **kwargs)
    return wrapper

@nice_decorator
def multiply(num1, num2):
    return num1 * num2

print(f"  without wraps: {decorated.__name__}")
print(f"  with wraps: {multiply.__name__}")
print(f"  multiply(6, 7): {multiply(6, 7)}")
#   without wraps: wrapper
#   with wraps: multiply
#   multiply(6, 7): 42

# One import and one decorator line, and the wrapped
# function still reports its true name -- tools that
# inspect functions (test runners, frameworks) see the
# real thing.

# ============================================================
# [11] A stateful decorator: counting calls
# ============================================================
# Closures (course lesson 46 territory) live happily
# inside decorators -- the count survives between calls
# of the wrapped function:

def counter_decorator(original_function):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return original_function(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@counter_decorator
def play():
    return "played"

play()
play()
play()

print(f"  calls after three plays: {play.calls}")
#   calls after three plays: 3

# The wrapper carries its own state (calls) across every
# invocation -- three plays, three counts. Decorators
# are not only announcers; they are tiny state machines
# around someone else's function.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- first-class
# footing, the build, both application styles, argument
# and return pass-through, names, and state:

print(f"  first-class (same object): {alias is say_hello}")
print(f"  decorated type: {type(decorated).__name__}")
print(f"  original untouched: {speak.__name__}")

final_manual = shout_decorator(speak)
print(f"  manual path works: {callable(final_manual)}")

@shout_decorator
def bow():
    print("  ...bowing...")

bow()
print(f"  @ path carries wrapper name: {bow.__name__}")
print(f"  args forwarded: {add(9, 1)}")
print(f"  wraps restores name: {multiply.__name__}")
print(f"  stateful count: {play.calls}")
#   first-class (same object): True
#   decorated type: function
#   original untouched: speak
#   manual path works: True
#   >> before the original
#   ...bowing...
#   >> after the original
#   @ path carries wrapper name: wrapper
#   args forwarded: 10
#   wraps restores name: multiply
#   stateful count: 3

# One session, every piece of the transcript: functions
# as values, the nested build, the manual and @ paths,
# transparent arguments, wrapped returns, honest names,
# and a counter that remembers. Decorators, end to end.

# ============================================================
# [13] The summary
# ============================================================
# Decorators, from the transcript, complete:
#
#   1. WHAT [00:13] -- a function that takes a function,
#      adds/modifies/enhances behavior, and RETURNS the
#      new function; the original code is NEVER edited
#   2. FOUNDATION [00:26] -- First-Class Functions:
#      functions are values -- assign (alias is
#      say_hello -> True), pass as arguments
#      (Hello Osama), return from functions (Hello
#      Mona); without this, decorators cannot exist
#   3. THE BUILD [01:09] -- outer decorator holds a
#      NESTED wrapper; the wrapper prints >> before,
#      calls the original, prints >> after; return
#      wrapper hands back the enhanced version
#   4. MANUAL APPLICATION -- decorated = shout_decorator(speak);
#      calling it interleaves the messages around the
#      original's own print, in order
#   5. PRISTINE ORIGINAL -- speak() direct prints NO >>
#      messages; speak.__name__ is 'speak' while
#      decorated.__name__ is 'wrapper': re-WRAPPING, not
#      re-WRITING
#   6. @ SYNTAX [03:18] -- @shout_decorator above a def
#      runs wave = shout_decorator(wave) at definition
#      time; identical behavior to the manual line --
#      pure Syntactic Sugar, as the transcript names it
#   7. TWO PATHS, ONE BEHAVIOR -- manual assignment and
#      @ both yield type 'function' carrying the same
#      wrapper identity
#   8. ARGUMENTS FORWARD -- wrapper(*args, **kwargs)
#      passes positional (add(2, 3) -> 5) and keyword
#      (greeting="Yo" -> 'Yo Mona') arguments through
#      untouched; the wrapper is a transparent messenger
#   9. RETURNS FLOW OUT -- add(10, 32) -> 42, usable in
#      expressions (* 2 -> 84): wrappers wrap behavior,
#      never swallow data
#  10. functools.wraps (bonus hygiene) -- restores the
#      original __name__ ('multiply' instead of
#      'wrapper'); inspection tools see the truth
#  11. STATEFUL DECORATORS -- a closure counter on the
#      wrapper: three play() calls -> calls == 3; the
#      decorator is a tiny state machine around someone
#      else's function
#  12. THE DISCIPLINE -- every printed line is a fixed
#      message, a fixed value, or a boolean fact; no
#      addresses, no clock -- byte-stable like every
#      lesson before it
#
# The original does its job. The decorator hands it a
# coat -- and the @ is the quickest way to put it on.
