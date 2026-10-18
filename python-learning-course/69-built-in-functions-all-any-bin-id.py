# -----------------------------------------------------------------
# Lesson 69: built-in functions -- all(), any(), bin(), id()
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : all() checks that every element is truthy, any()
#            checks that at least one is, bin() converts a
#            number to its 0b-prefixed binary string, and id()
#            reports the unique memory address of every value
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lessons 52 to 58 covered variables, containers, loops,
# conditions, and functions. Today adds four ready-made tools
# the language hands you:
#
#   all(iterable)   True only when EVERY element is truthy
#   any(iterable)   True when AT LEAST ONE element is truthy
#   bin(number)     the binary string, always starting 0b
#   id(value)       the unique memory address (an int)
#
# The transcript opens by naming print(), len(), int(), float()
# as tools we already use without thinking -- these four join
# that list today.
#
# ONE RULE FOR THIS LESSON: id() values are machine addresses
# that change every run, so they are NEVER printed raw. Only
# id() COMPARISONS appear (True/False) -- the exact question
# the transcript asks: do these two names point at the same
# place, or different places?
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

# ============================================================
# [1] all(): every element must be truthy
# ============================================================
# The transcript's [00:35] and [00:50]. all() walks a list (or
# any iterable) and answers True only if nothing in it is
# false, empty, or zero:

print(all([1, 2, 3]))                  # True: every number is truthy
print(all([True, True, True]))         # True: every flag is on
print(all(["read", "write"]))          # True: every string is non-empty
#   True
#   True
#   True

# ============================================================
# [2] all(): ONE falsy element kills the result
# ============================================================
# The transcript's [01:13]. A single 0, "", None, or False --
# anything falsy -- turns the whole call to False:

print(all([1, 0, 3]))                  # 0 is falsy
print(all([1, "", 3]))                 # empty string is falsy
print(all([1, None, 3]))               # None is falsy
print(all([1, True, False]))           # one False is enough
#   False
#   False
#   False
#   False

# all() short-circuits: it stops at the first falsy element it
# meets. One rotten apple ends the inspection.

# ============================================================
# [3] all(): the empty container is True (vacuous truth)
# ============================================================
# The edge every interviewer loves. There is no falsy element
# in an empty list -- because there is no element at all -- so
# all() reports True. Same rule, opposite face, in [5]:

print(all([]))                         # True: nothing falsy found
print(all(["hello", "x"]))             # both non-empty
print(all(["hello", ""]))              # "" is falsy
#   True
#   True
#   False

# ============================================================
# [4] any(): one truthy element is enough
# ============================================================
# The transcript's [02:03] and [02:36]. any() is the opposite
# question -- does ANYTHING here qualify? A single truthy
# element returns True:

print(any([0, 0, 3]))                  # 3 saves the call
print(any([False, False, 1]))          # 1 saves the call
print(any(["", "x"]))                  # "x" saves the call
#   True
#   True
#   True

# ============================================================
# [5] any(): False only when EVERY element is falsy
# ============================================================
# The transcript's rule stated from the other side. If nothing
# qualifies -- not one -- any() answers False. And the mirror
# of [3]: an empty list contains no truthy element, so it is
# False here (it was True for all()):

print(any([0, False, "", None]))       # nothing truthy at all
print(any([]))                         # False: nothing at all
print(any([0, False, []]))             # an empty list is falsy too
#   False
#   False
#   False

# all([]) -> True, any([]) -> False: same emptiness, opposite
# questions. Memorize the pair once and never mix them again.

# ============================================================
# [6] In practice: permissions with all(), errors with any()
# ============================================================
# The two functions in their natural habitats. A permissions
# list must be COMPLETE (all), an error list must be EMPTY
# (any on errors == False means clean):

permissions = ["read", "write", "exec"]
print(f"  permissions complete: {all(permissions)}")

permissions_missing = ["read", "", "exec"]
print(f"  permissions complete: {all(permissions_missing)}")

errors = [0, 0, 0]
print(f"  any errors: {any(errors)}")

errors_found = [0, "file missing", 0]
print(f"  any errors: {any(errors_found)}")
#   permissions complete: True
#   permissions complete: False
#   any errors: False
#   any errors: True

# One all() says "everything is ready"; one any() says
# "something is wrong". Two lines of code, the shape of every
# checklist and health-check script you will write.

# ============================================================
# [7] bin(): the binary string, always with 0b
# ============================================================
# The transcript's [03:29] and [03:39]. bin() converts a
# number to base 2 -- the zeros-and-ones language the machine
# speaks -- and the result is a STRING that always starts with
# the two characters 0b:

print(bin(10))                         # the transcript's example
print(bin(0))                          # zero is just 0b0
print(bin(1))                          # one is 0b1
print(bin(255))                        # eight ones
#   0b1010
#   0b0
#   0b1
#   0b11111111

# bin() does not return a number -- it returns text with a
# label attached. The 0b prefix is how Python marks "this
# string is binary"; strip it when you want the bare digits.

# ============================================================
# [8] bin(): bare bits, and reading the last one
# ============================================================
# Drop the prefix with [2:] (two characters gone) and the
# digits are yours. The LAST digit tells odd from even -- 1
# means odd, 0 means even:

bits = bin(13)[2:]
print(f"  13 in binary: {bits}")
print(f"  digits: {len(bits)}")

print(f"  7 is odd: {bin(7)[-1] == '1'}")
print(f"  8 is odd: {bin(8)[-1] == '1'}")
#   13 in binary: 1101
#   digits: 4
#   7 is odd: True
#   8 is odd: False

# [-1] is Python's "last character" -- here the least
# significant bit, the parity digit itself. One bin(), one
# index, and the oldest trick in the book.

# ============================================================
# [9] bin() round trip: back to a number with int(x, 2)
# ============================================================
# bin() goes number -> string. The way home is int() with the
# base given as its second argument -- base 2 here:

print(int("1010", 2))                  # binary text -> 10
print(int("11111111", 2))              # eight ones -> 255
print(bin(int("1010", 2)))             # and back again
#   10
#   255
#   0b1010

# int("1010", 2) reads the string as base-2 digits -- the
# same idea as int("12", 10) for decimal. Round trip closed:
# 10 -> '0b1010' -> 10.

# ============================================================
# [10] id(): every value lives at a unique address
# ============================================================
# The transcript's [04:00] and [04:31]. Every variable or
# value Python stores has a place in memory, and id() returns
# that place as an integer. The raw numbers are machine
# addresses -- they change between runs, so this lesson prints
# COMPARISONS only. First fact: id() itself returns an int:

print(f"  id() returns: {type(id(1)).__name__}")

# Second fact: give a second name to the SAME object, and the
# addresses match:

a = [1, 2, 3]
b = a                               # same object, new name
print(f"  same address: {id(a) == id(b)}")
#   id() returns: int
#   same address: True

# b is not a copy -- it is a second label on one box. One
# object, two names, one address.

# ============================================================
# [11] id(): equal contents, different objects
# ============================================================
# Now build a SECOND list with the same contents. The == test
# says the contents match; the id() test says the objects do
# not. The `is` operator is exactly "same id?":

c = [1, 2, 3]                        # equal contents, NEW object
print(f"  a == c: {a == c}")         # contents equal
print(f"  a is c: {a is c}")         # different objects
print(f"  same address: {id(a) == id(c)}")

print(f"  a is b: {a is b}")         # the shared name from [10]
#   a == c: True
#   a is c: False
#   same address: False
#   a is b: True

# == asks "do these contain the same thing?"; is (and id()
# equality) asks "are these the SAME thing?". Two lists can
# hold identical numbers and still be two separate boxes in
# two separate places. (CPython quietly reuses some small
# immutable values internally -- an implementation detail, not
# a language rule. The reliable tool is always the id()
# comparison itself.)

# ============================================================
# [12] One session: all four functions together
# ============================================================
# Everything combined the way real code meets them -- checks,
# a conversion, and an identity question in one block:

flags = [True, True, True]
blocked = [False, 0, "", None, []]

print(f"  all flags on: {all(flags)}")
print(f"  any flag on: {any(flags)}")
print(f"  all blocked empty: {all(blocked)}")
print(f"  any blocked truthy: {any(blocked)}")

print(f"  bin(10): {bin(10)}")

saved = flags
fresh = [True, True, True]
print(f"  saved is flags: {saved is flags}")
print(f"  fresh is flags: {fresh is flags}")
#   all flags on: True
#   any flag on: True
#   all blocked empty: False
#   any blocked truthy: False
#   bin(10): 0b1010
#   saved is flags: True
#   fresh is flags: False

# Four calls on the same pair of lists -- all() sees every
# flag clean, any() sees the same, and on the blocked list
# (all falsy: False, 0, "", None, []) both answers flip:
# all() is False, any() is False. Then bin() labels its
# number, and `is` splits the shared name from the fresh copy.

# ============================================================
# [13] The summary
# ============================================================
# Four tools, four jobs:
#
#   1. all(iterable) -- True ONLY when every element is
#      truthy; one 0, "", None, or False ends it (and it
#      short-circuits at the first failure); all([]) is True
#      -- vacuous truth, nothing falsy was found
#   2. any(iterable) -- True when AT LEAST ONE element is
#      truthy; False only when everything is falsy; any([])
#      is False -- nothing qualifies. The all([])/any([]) pair
#      (True / False) is the emptiness rule memorized once
#   3. THE PRACTICE SHAPE -- all() on a permissions list
#      ("is everything ready?"), any() on an error list ("is
#      anything wrong?"): two lines, every checklist script
#   4. bin(number) -- the binary STRING, always 0b-prefixed:
#      bin(10) -> '0b1010', bin(255) -> '0b11111111'; [2:]
#      strips the label, [-1] reads the parity bit (odd if
#      '1'), and int(text, 2) walks back to a number
#   5. id(value) -- the unique memory address as an int; the
#      RAW numbers are machine-specific and never printed
#      here; id(a) == id(b) answers the transcript's real
#      question -- same place or different places -- and the
#      `is` operator is that comparison in operator form
#   6. == VERSUS is -- equal contents (a == c: True) can live
#      in different objects (a is c: False); one name on one
#      box (b = a) shares the address (a is b: True)
#
# all() and any() judge CONTENTS. bin() translates NUMBERS.
# id() names OBJECTS. Four built-ins, one lesson, ready to
# use.
