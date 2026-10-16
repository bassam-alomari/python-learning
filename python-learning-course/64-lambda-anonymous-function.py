# -----------------------------------------------------------------
# Lesson 64: lambda functions (anonymous functions)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : what lambda is, syntax lambda parameters: expression,
#            the auto-return rule, one-expression limit,
#            def vs lambda and when to prefer each,
#            multiple parameters, temporary functions,
#            lambdas returned from def (small factories)
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# A lambda is a function with no name -- an ANONYMOUS function.
# Where def builds a full, named, reusable tool, lambda builds a
# one-line expression that evaluates to a result, usually for
# one job in one place:
#
#       lambda parameters: expression
#
# Two properties define it, and every section below is one of
# them made concrete:
#
#   1. single expression -- evaluated and returned AUTOMATICALLY,
#      no return keyword, no statements, no blocks
#   2. anonymous        -- no def, no stored name required; the
#      object is a normal function you can hold, call, pass
#      around, or throw away after one use
#
# The transcript's examples (greeting, add two numbers, square)
# appear in sections 3 and 4; the def-vs-lambda comparison in
# sections 7 and 8; multiple parameters in section 9; and the
# "temporary function inside another function" habitat -- the
# reason lambda exists -- in section 10.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] What a lambda IS: a function, just nameless
# ============================================================
# Before writing any lambda logic, look at what one is at the
# object level. Bind a lambda to a variable and inspect it:

speak = lambda: "Hi"
print("type:   ", type(speak).__name__)
print("callable:", callable(speak))
# type:    function
# callable: True

# type() says function -- not some special lambda type. A lambda
# IS a function; the keyword only describes how it was BUILT
# (one expression, no def). callable() says you can invoke it,
# exactly like any function from lesson 56. The word
# "anonymous" will show up as a string in section 8.

# ============================================================
# [2] The syntax, and the automatic return
# ============================================================
# The general form the transcript gives:
#
#       lambda parameters: expression
#
# The expression is evaluated and its value becomes the
# function's answer -- NO return keyword, because there is no
# statement position to put one in:

triple = lambda n: n * 3        # expression: n * 3
print("triple(4) ->", triple(4))
# triple(4) -> 12

# Read it as: "a one-line function taking n, whose entire body
# is n * 3, whose result is that value." The assignment on the
# left is ordinary Python -- triple is simply a NAME holding the
# function, the same way a def statement would create one. Only
# the right side is lambda's territory.

# ============================================================
# [3] Transcript example one: a greeting
# ============================================================
# "دالة لامدا تستقبل اسماً وترجع رسالة ترحيبية" -- a lambda that
# takes a name and returns a welcome message:

greeting = lambda name: f"Hello, {name}!"
print(greeting("Osama"))
print(greeting("Mona"))
# Hello, Osama!
# Hello, Mona!

# One line, one parameter, one f-string expression, and the
# result came back without writing return. The transcript's
# first practical example, exactly.

# ============================================================
# [4] Transcript example two: arithmetic
# ============================================================
# "عملية حسابية بسيطة (مثل جمع رقمين أو تربيع رقم)" -- add two
# numbers, square a number:

add = lambda a, b: a + b
square = lambda n: n ** 2
print(f"  add(3, 4)   -> {add(3, 4)}")
print(f"  square(5)   -> {square(5)}")
#   add(3, 4)   -> 7
#   square(5)   -> 25

# Two parameters in one lambda (the transcript saves this for
# [04:03] -- section 9 restates it), and ** for the square,
# both just expressions. This is lambda's sweet spot: an
# arithmetic one-liner you would otherwise define a whole def
# to hold.

# ============================================================
# [5] The value is a function you can hold or call at once
# ============================================================
# Because a lambda evaluates to a function OBJECT (section 1),
# you can keep it in a variable and call it later -- or wrap it
# in parentheses and call it immediately, with no variable at
# all:

print(f"  stored then called -> {triple(2)}")
print(f"  called at once     -> {(lambda x: x + 1)(4)}")
#   stored then called -> 6
#   called at once     -> 5

# The second line created a function and used it inside the
# same expression: (lambda x: x + 1) builds it, (4) calls it.
# The parentheses around the lambda are required -- without
# them the (4) would try to index or call something else
# entirely. Temporary job, temporary function, gone after one
# use: that is the anonymous half of the definition.

# ============================================================
# [6] The one-expression rule (and what it refuses)
# ============================================================
# Lambda cannot hold statements -- no assignments, no loops, no
# if BLOCKS. What it CAN do is an expression that chooses, via
# the conditional expression form:

label = lambda n: "big" if n >= 10 else "small"
print(label(12))
print(label(3))
# big
# small

# That single line is the whole decision -- expression on both
# sides of the if, so it stays legal inside a lambda. Now watch
# Python REFUSE a statement in the same position. compile()
# checks the code WITHOUT running it, so the failure is pure
# syntax:

try:
    compile("lambda x: y = 1", "<test>", "eval")
except SyntaxError as error:
    print("statement inside lambda ->", type(error).__name__)
# statement inside lambda -> SyntaxError

# "y = 1" is an assignment STATEMENT; a lambda body must be an
# expression. The check happened before anything ran, which is
# exactly why you will never see a half-built lambda at
# runtime -- Python rejects it at parse time. If a job needs a
# statement, it needs a def (or a conditional expression like
# label's).

# ============================================================
# [7] def vs lambda, side by side
# ============================================================
# The same job, both ways, producing identical answers:

def add_def(a, b):
    return a + b

add_lam = lambda a, b: a + b

print(f"  def    -> {add_def(2, 3)}")
print(f"  lambda -> {add_lam(2, 3)}")
#   def    -> 5
#   lambda -> 5

# From OUTSIDE, there is no difference at all: same parameters,
# same result, same call syntax. The difference is only in how
# they were written -- def spans three lines with an explicit
# return; lambda is one line with an implicit one. Neither is
# "faster"; the choice is about readability and intent, which
# is the next section's whole subject.

# ============================================================
# [8] When to prefer which (and the anonymous proof)
# ============================================================
# The comparison the transcript asks for at [02:38]. First, the
# proof that lambda really is nameless -- inspect both objects'
# __name__:

def real_name():
    pass

just_a_lambda = lambda: None
print(f"  def's name:    {real_name.__name__}")
print(f"  lambda's name: {just_a_lambda.__name__}")
#   def's name:    real_name
#   lambda's name: <lambda>

# The def carried its name from the statement; every lambda
# reports the placeholder <lambda> -- it never had one. Now the
# guidelines:
#
#   prefer DEF when:               prefer LAMBDA when:
#   ------------------------------- ----------------------------
#   the body needs >1 expression   the whole job is one line
#   you use statements (return,    you need it ONCE, right here
#     loops, real if blocks)       it is being passed directly
#   it deserves a name/docstring     to another function
#   you will call it in many       it is a quick key/transform
#     places in the file             for sort, map, filter...
#
# The right column is why lambda exists: a TEMPORARY function.
# The transcript names the classic habitat -- functions like
# map() and filter(), which expect a function as an argument;
# those helpers arrive in the upcoming lessons, and section 10
# uses an ordinary function as their stand-in so the idea is
# clear before their syntax shows up.

# ============================================================
# [9] More than one parameter
# ============================================================
# Lambda takes any parameter list, exactly like def -- the
# transcript highlights this at [04:03]:

full_name = lambda first, last: f"{first} {last.capitalize()}"
print(f"  {full_name('osama', 'ali')}")
#   osama Ali

volume = lambda l, w, h: l * w * h
print(f"  volume(2, 3, 4) -> {volume(2, 3, 4)}")
#   volume(2, 3, 4) -> 24

# Three parameters, one expression each. The one-expression
# limit is about the BODY, not the parameter list -- as many
# inputs as the job needs, still one line of work. (capitalize()
# came from lesson 57; it is not lambda's doing.)

# ============================================================
# [10] The real habitat: a temporary function inside a def
# ============================================================
# This is the pattern lambda was built for. A function that
# takes ANOTHER function as a value, and callers who hand it a
# one-line job instead of defining a name:

def apply_operation(a, b, operation):
    return operation(a, b)                # call what we were given

print(f"  3 + 4 = {apply_operation(3, 4, lambda x, y: x + y)}")
print(f"  3 * 4 = {apply_operation(3, 4, lambda x, y: x * y)}")
print(f"  3 - 4 = {apply_operation(3, 4, lambda x, y: x - y)}")
#   3 + 4 = 7
#   3 * 4 = 12
#   3 - 4 = -1

# One def, three different behaviors, zero extra names in the
# file. Each lambda lives only inside its own print line --
# nobody needs add_two, multiply_two, or subtract_two sitting
# around afterward. apply_operation (a higher-order function:
# it accepts a function) is a miniature of map()/filter():
# loop over inputs, apply what was handed in. Section 8's right
# column, running.

# ============================================================
# [11] In the wild: a lambda as a sort key
# ============================================================
# A real one-liner doing real work -- you already met this shape
# in lesson 61 (sorted with key=lambda). The transcript's
# "temporary function inside other functions" claim, at normal
# size:

scores = [("Mona", 88), ("Osama", 95), ("Sayid", 72)]
ranked = sorted(scores, key=lambda pair: pair[1], reverse=True)
for name, score in ranked:
    print(f"  {name:<6} {score}")
#   Osama  95
#   Mona   88
#   Sayid  72

# sorted() needs to know how to COMPARE items; the lambda tells
# it "compare by the score" in the place and moment of the
# call. Writing a def named score_of for one use would add a
# name the file never uses again -- which is exactly the
# trade-off guideline from section 8.

# ============================================================
# [12] Lambdas returned from def: tiny factories
# ============================================================
# The advanced habit the transcript hints at for later lessons:
# a def whose JOB is to hand out lambdas. Each one arrives with
# its own captured value:

def multiplier(factor):
    return lambda x: x * factor           # a lambda, built here

double = multiplier(2)
treble = multiplier(3)
print(f"  double(5) -> {double(5)}")
print(f"  treble(5) -> {treble(5)}")
#   double(5) -> 10
#   treble(5) -> 15

# Both returned lambdas are the same one line of code, yet one
# doubles and one triples -- each remembers the factor that was
# current when it was created, even though multiplier had
# already returned (a story that builds directly on lesson 62:
# the lambda kept its own piece of data alive). This is how
# specialized one-liners get manufactured on demand, and it is
# the kind of "advanced application" the transcript promises
# for the lessons ahead.

# ============================================================
# [13] The summary
# ============================================================
# Lambda, complete:
#
#   1. DEFINITION -- an anonymous function: one expression, no
#      def, no name required
#   2. SYNTAX -- lambda parameters: expression; the expression
#      is evaluated and returned AUTOMATICALLY (no return)
#   3. IT IS A FUNCTION OBJECT -- type 'function', callable,
#      storable in a variable, callable immediately when
#      wrapped in parentheses: (lambda x: x + 1)(4)
#   4. ONE EXPRESSION ONLY -- statements are rejected at parse
#      time (SyntaxError); choices use the expression form
#      ("big" if n >= 10 else "small")
#   5. vs DEF -- identical behavior from the outside; def for
#      multi-line, named, reusable, documented work; lambda for
#      one-liners you need once, right where you use them
#   6. ANONYMOUS PROOF -- __name__ is '<lambda>' against the
#      def's real name
#   7. PARAMETERS -- as many as needed (name, name; a, b, c),
#      still one expression of body
#   8. THE HABITAT -- passing a temporary function to another
#      function: apply_operation(3, 4, lambda x, y: x * y), the
#      shape of the coming map()/filter() lessons, and sorted's
#      key=lambda you already know
#   9. RETURNED LAMBDAS -- a def can hand out one-line functions
#      that each capture their own values: multiplier(2)(5)
#      makes 10, multiplier(3)(5) makes 15
#
# The one question to ask before reaching for lambda: does the
# whole job fit in a single expression that nobody will need to
# call from anywhere else? If yes, lambda is shorter and
# clearer. If no, def is not bureaucracy -- it is the right
# tool.
