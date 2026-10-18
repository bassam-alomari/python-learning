# -----------------------------------------------------------------
# Lesson 71: built-in functions part 3 -- abs(), pow(), min(),
#            max(), and slice()
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : abs() returns the absolute value, pow() raises a
#            base to an exponent (with an optional modulo),
#            min() and max() find the smallest and largest
#            elements (numbers or strings), and slice() builds
#            a slice object as an alternative to [a:b:c]
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lessons 69 and 70 covered all(), any(), bin(), id(), sum(),
# round(), range(), and print(). Five more join the catalog:
#
#   abs(number)                  absolute value (drop the sign)
#   pow(base, exp[, mod])        base ** exp, optionally % mod
#   min(iterable)                smallest element
#   max(iterable)                largest element
#   slice(start, stop, step)     a reusable [start:stop:step]
#
# The transcript's own examples are used where they appear --
# abs(-10), pow(2, 5), and slice(start, stop, step) come
# straight from the lecture.
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

# ============================================================
# [1] abs(): the absolute value
# ============================================================
# The transcript's [00:13] and [00:18]. abs() returns the
# distance from zero -- negatives become positive, positives
# stay as they are. The lecture's exact example first:

print(abs(-10))                        # the transcript's example
print(abs(10))                         # already positive
print(abs(-3.7))                       # floats too
print(abs(0))                          # zero stays zero
#   10
#   10
#   3.7
#   0

# One rule, no exceptions in daily use: strip the minus sign.
# -10 and 10 both become 10 -- the SIGN is lost, the SIZE
# remains.

# ============================================================
# [2] abs() in practice: distances and differences
# ============================================================
# abs() shines whenever direction does not matter, only
# magnitude -- How far? How cold? How much changed?

print(abs(20 - 50))                    # the gap, not the direction
print(abs(50 - 20))                    # same gap either way
temperature = -12
print(f"  outside is {abs(temperature)} degrees below zero")
#   30
#   30
#   outside is 12 degrees below zero

# abs(20 - 50) and abs(50 - 20) both give 30 -- subtraction
# has a direction, distance does not. That is the everyday
# job of abs(): turn a signed difference into a plain gap.

# ============================================================
# [3] pow(): base and exponent
# ============================================================
# The transcript's [01:06] and [01:13]. pow(base, exp)
# returns base raised to the power exp -- the same as
# base ** exp, in function form. The lecture's exact example:

print(pow(2, 5))                       # 2 * 2 * 2 * 2 * 2
print(pow(10, 3))                      # 10 * 10 * 10
print(pow(2, 0))                       # anything to the 0 is 1
print(pow(5, 1))                       # anything to the 1 is itself
#   32
#   1000
#   1
#   1

# pow(2, 5) = 32, exactly as the transcript says. The two
# edge rules appear in the last two lines: exponent 0 gives
# 1, exponent 1 gives the base unchanged.

# ============================================================
# [4] pow(base, exp, mod): the power, then the remainder
# ============================================================
# The transcript's [01:53]. A THIRD, optional argument turns
# the call into "raise to the power, THEN take the remainder
# when divided by mod" -- pow(base, exp, mod) ==
# (base ** exp) % mod, computed in one efficient step:

print(pow(2, 3, 5))                    # 2**3 = 8, 8 % 5 = 3
print(pow(5, 2, 13))                   # 5**2 = 25, 25 % 13 = 12
print(pow(2, 10, 1000))                # 1024 % 1000 = 24
print(pow(7, 0, 5))                    # 1 % 5 = 1
#   3
#   12
#   24
#   1

# Without the third argument Python would build the FULL
# power first -- 2 to the 1000th is a 300-digit number -- and
# only then divide. With mod, the size never explodes; the
# answer stays smaller than mod the whole way. This is why
# pow(base, exp, mod) is the workhorse of checksums and
# cryptography: enormous powers, tiny remainders, one call.

# ============================================================
# [5] min(): the smallest element (numbers)
# ============================================================
# The transcript's [03:38] and [03:44]. min() walks an
# iterable and returns its smallest element. Lists, tuples,
# or several plain arguments all work:

print(min([3, 1, 2]))                  # from a list
print(min((10, 5, 8)))                 # from a tuple
print(min(3, 1, 2))                    # several arguments
print(min(range(5)))                   # 0 is the smallest
#   1
#   5
#   1
#   0

# Same comparison < the loop you would write by hand, in one
# call. range(5) is [0, 1, 2, 3, 4], so its minimum is 0 --
# min() reads any iterable, not just lists.

# ============================================================
# [6] min() with text: alphabetical order
# ============================================================
# The transcript explicitly mentions comparing letters and
# words. Strings compare in dictionary (lexicographic)
# order -- min() returns the one that would come FIRST in a
# dictionary:

print(min(["banana", "apple", "cherry"]))   # a comes first
print(min("banana"))                        # smallest letter
print(min(["cat", "bat", "hat"]))           # b < c < h
#   apple
#   a
#   bat

# "apple" starts with a -- before b and c -- so it wins.
# Inside a single string, min() treats each character as an
# element: 'a', 'a', 'b', 'n', 'n', 'a' and the smallest is
# 'a'. Same rule, letters instead of numbers.

# ============================================================
# [7] max(): the largest element
# ============================================================
# The transcript's [05:40] and [05:47]. max() is min()'s
# twin with the opposite comparison:

print(max([3, 1, 2]))                  # from a list
print(max(3, 1, 2))                    # several arguments
print(max(range(5)))                   # 4 is the largest
print(max([-4, -8, -1]))               # works with negatives
#   3
#   3
#   4
#   -1

# The largest of [-4, -8, -1] is -1 -- remember, on the
# number line -1 is GREATER than -4. max() compares values,
# not magnitudes; for magnitude, wrap with abs() (section
# [2]).

# ============================================================
# [8] max() with text, and the scores report
# ============================================================
# The alphabetical twin of [6], then both functions in their
# natural habitat -- a score sheet:

print(max(["banana", "apple", "cherry"]))   # last in order
print(max("banana"))                        # furthest letter
#   cherry
#   n

scores = [88, 95, 72, 91]
highest = max(scores)
lowest = min(scores)
print(f"  highest: {highest}")
print(f"  lowest: {lowest}")
print(f"  spread: {highest - lowest}")
#   highest: 95
#   lowest: 72
#   spread: 23

# "cherry" comes last alphabetically; 'n' is the furthest
# letter in "banana". Then the report: highest 95, lowest
# 72, spread 23 -- two built-ins and one subtraction, the
# shape of every stats line you will ever need.

# ============================================================
# [9] slice(): the bracket notation, as an object
# ============================================================
# The transcript's [06:34] and [06:40]. slice(start, stop,
# step) builds a SLICE OBJECT -- the same recipe as
# data[start:stop:step], but stored in a variable you can
# reuse and inspect:

data = [0, 1, 2, 3, 4, 5]
s = slice(1, 4)
print(f"  data[s]: {data[s]}")
print(f"  data[1:4]: {data[1:4]}")        # identical result

text = "hello"
print(f"  text[s]: {text[s]!r}")
#   data[s]: [1, 2, 3]
#   data[1:4]: [1, 2, 3]
#   text[s]: 'ell'

# data[s] and data[1:4] return the SAME list -- the slice
# object is the bracket recipe, lifted out and named. It
# works on any sequence: lists, strings, tuples. One recipe,
# many containers.

# ============================================================
# [10] slice() with a step, and the full reverse
# ============================================================
# The third argument behaves exactly like the bracket step --
# including the famous negative step that walks backwards:

s = slice(0, 6, 2)
print(f"  every second: {data[s]}")

r = slice(None, None, -1)               # the whole reverse
print(f"  reversed: {data[r]}")
print(f"  bracket form: {data[::-1]}")   # same recipe
#   every second: [0, 2, 4]
#   reversed: [5, 4, 3, 2, 1, 0]
#   bracket form: [5, 4, 3, 2, 1, 0]

# slice(0, 6, 2) steps by 2: positions 0, 2, 4. And
# slice(None, None, -1) -- start at the beginning, stop at
# the end, step backwards -- is the textbook one-line
# reverse, spelled with None where "leave it default"
# belongs. data[r] and data[::-1] agree, as they must.

# ============================================================
# [11] slice() attributes: read the recipe back
# ============================================================
# A slice object is not just usable -- it is INSPECTABLE.
# The three parts live on named attributes:

s = slice(1, 5, 2)
print(f"  start: {s.start}")
print(f"  stop: {s.stop}")
print(f"  step: {s.step}")
print(f"  as brackets: [{s.start}:{s.stop}:{s.step}]")

open_ended = slice(3)                   # only a stop
print(f"  only stop -> {open_ended.stop}")
#   start: 1
#   stop: 5
#   step: 2
#   as brackets: [1:5:2]
#   only stop -> 3

# The brackets you write by hand carry no name and cannot be
# passed around; the object can. Store a recipe once, reuse
# it on twenty lists, and read its parts when you need them.
# slice(3) with one argument behaves like [:3] -- stop
# exclusive, start at zero.

# ============================================================
# [12] One session: all five together
# ============================================================
# The five functions combined the way real code meets them --
# a small temperature report:

temps = [-3, 8, -11, 5]
coldest = min(temps)
warmest = max(temps)
print(f"  coldest: {coldest}, warmest: {warmest}")
print(f"  coldest magnitude: {abs(coldest)}")
print(f"  warmest in binary: {bin(warmest)}")
print(f"  spread squared: {pow(warmest - coldest, 2)}")
print(f"  middle pair: {temps[slice(1, 3)]}")
#   coldest: -11, warmest: 8
#   coldest magnitude: 11
#   warmest in binary: 0b1000
#   spread squared: 361
#   middle pair: [8, -11]

# min() found -11, max() found 8; abs() turned the coldest
# into its magnitude 11; bin() (lesson 69) labeled the
# warmest 0b1000; pow() squared the spread -- (8 - -11)**2
# = 19**2 = 361; and slice(1, 3) cut out the middle pair.
# Five built-ins, one block, no invented loops.

# ============================================================
# [13] The summary
# ============================================================
# Five tools, five jobs:
#
#   1. abs(number) -- the distance from zero: abs(-10) -> 10
#      (the lecture's example), positives unchanged, floats
#      too; the everyday use is a direction-free GAP:
#      abs(20 - 50) == abs(50 - 20) == 30
#   2. pow(base, exp) -- base ** exp in function form:
#      pow(2, 5) -> 32, pow(10, 3) -> 1000; exponent 0
#      gives 1, exponent 1 gives the base
#   3. pow(base, exp, mod) -- raise, then remainder:
#      pow(2, 3, 5) -> 3 (8 % 5), pow(5, 2, 13) -> 12,
#      pow(2, 10, 1000) -> 24; the full power is never
#      built, so giant exponents stay tiny -- the engine of
#      checksums and cryptography
#   4. min(iterable) -- smallest element; lists, tuples,
#      plain arguments, even range(); with STRINGS it
#      compares alphabetically: min(["banana", "apple",
#      "cherry"]) -> "apple", min("banana") -> "a"
#   5. max(iterable) -- the twin: largest element; remember
#      -1 is GREATER than -4; max of scores 95, min 72,
#      spread highest - lowest = 23; with text,
#      "cherry" / 'n'
#   6. slice(start, stop, step) -- the [a:b:c] recipe as a
#      REUSABLE OBJECT: data[slice(1, 4)] == data[1:4] ->
#      [1, 2, 3] on lists AND strings; slice(0, 6, 2) steps
#      by two, slice(None, None, -1) is the one-line reverse
#      (== data[::-1]); the parts read back through .start,
#      .stop, .step -- a recipe you can store, pass, and
#      inspect
#
# abs() strips signs, pow() raises (and mods), min()/max()
# find extremes (numbers or letters), slice() names the
# cut. The built-in catalog keeps growing.
