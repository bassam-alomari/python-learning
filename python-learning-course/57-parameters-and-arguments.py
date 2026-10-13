# -----------------------------------------------------------------
# Lesson 57: parameters and arguments, in detail
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : def parameters, call arguments, count matching, TypeError,
#            cleaning inputs with strip() and capitalize()
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lesson 56 introduced def and return. This lesson slows down on
# the arrow between the two halves of a function call:
#
#   def say_hello(name):        name is a PARAMETER (the slot)
#   say_hello("Osama")          "Osama" is an ARGUMENT (the value)
#
# The transcript's advanced example finishes the lesson: a full
# name (first, middle, last) cleaned with strip() and formatted
# with capitalize(), printed properly. That example needs multiple
# parameters and correct argument counts, which is exactly what
# the first two-thirds of this file builds toward.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] The two words, defined once
# ============================================================
# Parameters live in the def. Arguments live in the call. The
# function never sees the arguments -- it only ever sees the
# parameters, holding whatever was passed.

def say_hello(name):          # "name" is a parameter: a slot
    print(f"Hello, {name}!")

say_hello("Osama")           # "Osama" is an argument: a value
# Hello, Osama!

# Inside the body, name IS "Osama" for the duration of the call.
# The word "argument" never appears in the function. Think of a
# function as a machine with labeled slots (parameters); you put
# things in the slots (arguments); the machine works on what it
# finds in the slots.

# ============================================================
# [2] One parameter, many arguments: the slot is refilled
# ============================================================
# The same def, called three times with three values. Each call
# starts the function fresh -- name does not remember the last
# value.

say_hello("Osama")
# Hello, Osama!

say_hello("Mona")
# Hello, Mona!

say_hello("Ahmed")
# Hello, Ahmed!

# Nothing is kept between calls. A function is a fresh workspace
# every time, which is why lesson 56 could call greet() twice
# with no cleanup in between.

# ============================================================
# [3] Multiple parameters: fill every slot
# ============================================================
# The transcript's next step: more than one parameter. They are
# declared in the def, comma-separated, and the call must supply
# a matching number of arguments, in order.

def full_name(first, middle, last):
    print(f"  first:  {first}")
    print(f"  middle: {middle}")
    print(f"  last:   {last}")

full_name("Osama", "Ali", "Smith")
#   first:  Osama
#   middle: Ali
#   last:   Smith

# Three parameters, three arguments. The first argument fills the
# first parameter, the second fills the second, and so on --
# positionally, left to right. The names do NOT have to match:
#
#   full_name("A", "B", "C")   works exactly the same
#
# The parameter names only matter INSIDE the function. At the
# call site, only the order and the count matter.

# ============================================================
# [4] Arithmetic with parameters: the calculation version
# ============================================================
# Numbers work the same way. The transcript's "several numeric
# values" case:

def average3(a, b, c):
    return (a + b + c) / 3

print("average3(80, 90, 100) =", average3(80, 90, 100))
# average3(80, 90, 100) = 90.0

print("average3(10, 20, 30) =", average3(10, 20, 30))
# average3(10, 20, 30) = 20.0

# The function does not care whether the numbers are grades,
# prices, or temperatures. It knows only "three slots, add them,
# divide by three". That ignorance is a feature: the same function
# serves every three-number average in the program.

# ============================================================
# [5] Trap: wrong argument count -> TypeError
# ============================================================
# The transcript's central warning. Python checks the count at
# CALL time, not at def time. Too few or too many, and you get a
# TypeError with a message that names the function.

# Too few:
try:
    full_name("Osama", "Ali")          # last is missing
except TypeError as error:
    print("too few ->", error)
# too few -> full_name() missing 1 required positional argument: 'last'

# Too many:
try:
    full_name("Osama", "Ali", "Smith", "Jr")   # one extra
except TypeError as error:
    print("too many ->", error)
# too many -> full_name() takes 3 positional arguments but 4 were given

# The def itself never complained -- Python only validates when
# you CALL. The two messages are worth reading once each:
#
#   missing 1 required positional argument   you sent too few
#   takes 3 ... but 4 were given             you sent too many
#
# "positional" here means "matched by position", which is the
# default matching mode. Section 8 shows the other mode.

# ============================================================
# [6] Default values: a parameter that can be skipped
# ============================================================
# A parameter with = value in the def becomes OPTIONAL at the
# call site. The default is used when the caller leaves it out.

def greet_formal(name, title="Mr."):
    print(f"Hello, {title} {name}")

greet_formal("Osama")
# Hello, Mr. Osama

greet_formal("Mona", "Dr.")
# Hello, Dr. Mona

# One def, two call shapes. The rule that saves hours of
# debugging: parameters WITHOUT defaults must come BEFORE
# parameters WITH them.

# This is legal:
def good_order(a, b=2):
    print(f"good_order a={a} b={b}")

good_order(1)
# good_order a=1 b=2

# This is a SyntaxError at def time (default before required):
# def bad_order(a=1, b):     <-- never runs, file won't start
#     pass

# The interpreter refuses to define bad_order at all, so you see
# the error the moment you run the file, not at some later call.

# ============================================================
# [7] Keyword arguments: name the slot yourself
# ============================================================
# Section 3 said position decides which argument fills which
# parameter. Naming the parameter at the call site overrides
# that, and makes the call readable:

greet_formal(title="Prof.", name="Hassan")
# Hello, Prof. Hassan

# The order of the keywords does not matter -- the names carry
# the meaning. Mixing is allowed too: positional arguments still
# come first, keywords after:

def book(title, author, copies=1):
    print(f"  {title} by {author}, copies={copies}")

book("Dune", "Herbert")
#   Dune by Herbert, copies=1

book("Neuromancer", "Gibson", copies=3)
#   Neuromancer by Gibson, copies=3

book("Hyperion", author="Simmons", copies=2)
#   Hyperion by Simmons, copies=2

# Three valid shapes: positional, positional+keyword-default,
# keyword-only override. All three reach the same def without
# ever counting on the reader's memory of the parameter order.

# ============================================================
# [8] *args: "any number of numbers"
# ============================================================
# When the transcript says "several numeric values", sometimes
# you do not know HOW many. A parameter starting with * collects
# the leftovers into a tuple.

def total(*prices):
    print("  prices seen:", prices)
    return sum(prices)

print("total(10, 20) =", total(10, 20))
#   prices seen: (10, 20)
# total(10, 20) = 30

print("total(5, 5, 5, 5) =", total(5, 5, 5, 5))
#   prices seen: (5, 5, 5, 5)
# total(5, 5, 5, 5) = 20

# The name prices is arbitrary -- the STAR is what collects.
# Inside the body, prices is an ordinary tuple (lesson 24).
# A star-parameter must be LAST among positional parameters;
# after it you may still add keyword-only parameters, but that is
# a story for the deeper function lessons.

# ============================================================
# [9] The transcript's advanced example: clean full names
# ============================================================
# Everything above converges here. Three parameters, each one
# cleaned with strip() (remove surrounding spaces) and formatted
# with capitalize() (first letter upper, rest lower) from the
# string lessons.

def show_full_name(first, middle, last):
    """Clean and display a three-part name, properly."""
    first = first.strip().capitalize()
    middle = middle.strip().capitalize()
    last = last.strip().capitalize()
    print(f"  {first} {middle} {last}")

print("raw input:")
show_full_name("  osama   ", "aLI", "sMITH  ")
# raw input:
#   Osama Ali Smith

print("already clean:")
show_full_name("Mona", "Zaid", "Khalil")
# already clean:
#   Mona Zaid Khalil

# Trace one argument through:
#
#   "  osama   "   .strip()   -> "osama"
#                .capitalize() -> "Osama"
#
# strip() is what makes the function survive real input -- typed
# names carry stray spaces. capitalize() makes the display
# consistent regardless of how the name arrived (all caps, all
# lower, mixed). The parameters are reassigned, which is fine:
# they are local slots (lesson 58 covers scope properly), and the
# caller's original strings are untouched anyway, because strings
# are immutable.

# ============================================================
# [10] Cleaning with a return, not only a print
# ============================================================
# Lesson 56's rule applied to the same job: give the value back,
# let the caller decide.

def clean_name(part):
    """Return one name part, stripped and capitalized."""
    return part.strip().capitalize()

def full_name_tidy(first, middle, last):
    """Return a tidy full-name string."""
    return f"{clean_name(first)} {clean_name(middle)} {clean_name(last)}"

tidy = full_name_tidy("  osama   ", "aLI", "sMITH  ")
print("tidy:", tidy)
# tidy: Osama Ali Smith

print("upper for a header:", tidy.upper())
# upper for a header: OSAMA ALI SMITH

print("initials:", ". ".join(p[0] for p in tidy.split()))
# initials: O. A. S

# One cleaned value, three destinations: plain print, a header in
# caps, initials for a badge. The print-only version could serve
# exactly one of these. This is the transcript's "control where
# the data appears" point, now with string parts.

# ============================================================
# [11] The count check, collected
# ============================================================
# A compact recap of what raises TypeError and what does not:

def two(a, b):
    return a + b

# Wrong counts raise:
try:
    two(1)
except TypeError as error:
    print("one arg ->", error)
# one arg -> two() missing 1 required positional argument: 'b'

try:
    two(1, 2, 3)
except TypeError as error:
    print("three args ->", error)
# three args -> two() takes 2 positional arguments but 3 were given

# Correct counts do not, even with odd values:
print("two(1, 2) =", two(1, 2))
# two(1, 2) = 3

print('two("a", "b") =', two("a", "b"))
# two("a", "b") = ab

# Python checks SHAPE (how many), not CONTENT (what kind) --
# unless the function itself checks, or the operation fails
# inside (like "a" + 1). Argument count errors are caught before
# your code runs; type errors inside the body are caught when
# that line executes. Two different safety nets.

# ============================================================
# [12] A realistic pass: register a user, validated
# ============================================================
# Parameters, defaults, keyword arguments, cleaning, and a
# guard clause -- the whole lesson in one small function.

def register_user(username, email, role="member", active=True):
    """Return a clean user record, or None if invalid."""
    username = username.strip()
    email = email.strip().lower()
    if not username or not email:
        return None                      # empty input is rejected
    return {
        "username": username,
        "email": email,
        "role": role,
        "active": active,
    }

user = register_user("  Osama  ", "OSAMA@EXAMPLE.COM")
print("user:", user)
# user: {'username': 'Osama', 'email': 'osama@example.com', 'role': 'member', 'active': True}

admin = register_user("Mona", "MONA@EXAMPLE.COM", role="admin")
print("admin role:", admin["role"])
# admin role: admin

bad = register_user("   ", "")
print("rejected:", bad is None)
# rejected: True

# Watch each parameter do its job:
#
#   username    positional, cleaned with strip()
#   email       positional, cleaned with strip().lower()
#   role        keyword-default, overridable per call
#   active      keyword-default, left alone here
#   return      a record the caller stores, or None on bad input
#
# The function never prints. The caller printed three different
# answers from three calls -- which is the return habit from
# lesson 56, now with parameters that deserve the name "real".

# ============================================================
# [13] The summary
# ============================================================
# Parameters are the slots in the def. Arguments are the values
# in the call. The function only ever sees the slots.
#
#   positional matching     order decides, count must match
#   keyword matching        name decides, order does not matter
#   defaults (x=...)        the slot can be left empty
#   *args                   any number of extras, collected as a tuple
#
# Wrong counts fail loudly at call time with TypeError -- too few
# says "missing 1 required positional argument", too many says
# "takes N ... but M were given". The def never validates; the
# CALL does.
#
# The transcript's advanced example is the shape to keep: three
# name parameters, each passed through strip() and capitalize(),
# either printed once or -- better -- returned as a tidy string
# the caller can upper(), split, or store. Clean at the boundary,
# return the clean value, and every consumer downstream gets data
# it can trust.
#
# Scope (where the parameters live after the call) and deeper
# parameter forms are the next lessons. The count rule and the
# clean-at-the-boundary habit are already yours.
