# -----------------------------------------------------------------
# Lesson 70: built-in functions part 2 -- sum(), round(),
#            range(), and advanced print()
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : sum() adds the numbers of any iterable, round()
#            rounds floats (including Python's half-to-even
#            rule), range() generates number sequences from
#            start/stop/step, and print()'s sep and end
#            arguments control separators and line endings
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lesson 69 brought all(), any(), bin(), and id(). This one
# continues the built-in catalog with four more:
#
#   sum(iterable)              add every number in it
#   round(number[, ndigits])   round to int or to N decimals
#   range(start, stop, step)   generate a sequence of ints
#   print(..., sep=, end=)     advanced printing control
#
# The transcript's examples are used exactly where they appear
# -- sum([1, 10, 19, 70]) and print(1, 2, 3, sep=" - ") come
# straight from the lecture.
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

# ============================================================
# [1] sum(): add every number in an iterable
# ============================================================
# The transcript's [00:15] and [00:45]. sum() walks a list (or
# tuple, or any iterable of numbers) and returns the total.
# The lecture's exact example:

print(sum([1, 10, 19, 70]))            # 1 + 10 + 19 + 70
print(sum((5, 5, 5)))                  # tuples work too
print(sum([]))                         # nothing to add -> 0
#   100
#   15
#   0

# One call replaces the loop-and-accumulator pattern everyone
# writes first. The empty iterable sums to 0 -- the natural
# starting value.

# ============================================================
# [2] sum(): the start argument, and the text trap
# ============================================================
# sum() accepts a second argument: a number to begin adding
# from. And non-numbers are an error, not a silent skip:

print(sum([1, 2, 3], 10))              # start from 10 -> 16

try:
    sum([1, "2", 3])                   # "2" is text, not a number
except TypeError as error:
    print(f"  sum with text -> {type(error).__name__}")
#   16
#   sum with text -> TypeError

# 10 + (1 + 2 + 3) = 16. The start value joins the addition
# instead of replacing it. A string inside the list stops the
# call with TypeError -- sum() adds numbers, and "2" is not
# one.

# ============================================================
# [3] sum() meets range(): totals without writing the list
# ============================================================
# The two functions from this lesson combine perfectly --
# range() generates the numbers, sum() adds them:

print(sum(range(5)))                   # 0 + 1 + 2 + 3 + 4
print(sum(range(1, 6)))                # 1 + 2 + 3 + 4 + 5
#   10
#   15

# No list in memory, no loop on screen: range() feeds sum()
# directly. This is the idiomatic Python way to sum a span.

# ============================================================
# [4] round(): floats to the nearest integer
# ============================================================
# The transcript's [01:32] and [01:44]. round() with ONE
# argument rounds to the nearest whole number -- .5 and above
# goes up, below goes down (with one famous exception coming
# in [5]):

print(round(3.7))                      # above .5 -> up
print(round(3.2))                      # below .5 -> down
print(round(-3.7))                     # negative mirrors
print(round(-3.2))
#   4
#   3
#   -4
#   -3

# Distance decides: 3.7 is nearer to 4, 3.2 is nearer to 3.
# Negatives behave symmetrically -- -3.7 lands on -4.

# ============================================================
# [5] round(): the half-to-even rule (Python's famous quirk)
# ============================================================
# The transcript's [02:27] mentions how Python's rounding
# actually works. Exactly .5 does NOT always round up -- it
# rounds to the even neighbour. That is the official rule:

print(round(2.5))                      # half -> even -> 2
print(round(3.5))                      # half -> even -> 4
print(round(0.5))                      # half -> even -> 0
print(round(1.5))                      # half -> even -> 2
print(round(-2.5))                     # negatives too
#   2
#   4
#   0
#   2
#   -2

# 2.5 sits between 2 and 4's side -- the even answer is 2.
# 3.5 between 3 and 4 -- the even answer is 4. This is
# "banker's rounding", chosen so that long streams of .5s do
# not drift upward. Schoolbook rounding would give 3, 4, 1,
# 2; Python gives 2, 4, 0, 2. Know the rule and no float will
# surprise you again.

# ============================================================
# [6] round(number, ndigits): control the decimal places
# ============================================================
# The transcript's second form. ndigits says how many places
# after the decimal point survive:

print(round(3.14159, 2))               # two places
print(round(3.14159, 3))               # three places
print(round(3.14159))                  # zero places -> int
print(round(2.675, 2))                 # the float trap
#   3.14
#   3.142
#   3
#   2.67

# The last line is a rite of passage. 2.675 LOOKS like it
# should become 2.68, but decimal 2.675 has no exact binary
# float representation -- it is stored as a hair under
# 2.675 -- so rounding sees 2.674999... and keeps 2.67.
# Same rule, different neighbor: the number inside the
# machine is what gets rounded, never the digits you typed.

# ============================================================
# [7] round() with negative ndigits: round the tens place
# ============================================================
# ndigits can go past the decimal point into the whole
# numbers -- -1 rounds to the tens, -2 to the hundreds (and
# banker's rounding still rules the halves):

print(round(87, -1))                   # nearest ten
print(round(85, -1))                   # half -> even -> 80
print(round(95, -1))                   # half -> even -> 100
print(round(1234, -2))                 # nearest hundred
#   90
#   80
#   100
#   1200

# 87 is nearest to 90; 85 is a half -- even neighbour is 80;
# 95's halves (90 and 100) are both even, and the rule picks
# 100. One function covers pennies and thousands alike.

# ============================================================
# [8] range(): one argument is the STOP (start defaults to 0)
# ============================================================
# The transcript's [04:00] and [05:07]. range() builds a
# sequence of integers. With ONE argument you give the STOP,
# and Python starts at 0 automatically. The result is a range
# OBJECT -- a lightweight recipe, not a list -- so list() and
# len() materialize or measure it:

r = range(5)
print(f"  type: {type(r).__name__}")
print(f"  as list: {list(r)}")
print(f"  length: {len(r)}")
print(f"  3 in range: {3 in r}")
print(f"  5 in range: {5 in r}")
#   type: range
#   as list: [0, 1, 2, 3, 4]
#   length: 5
#   3 in range: True
#   5 in range: False

# range(5) means "from 0 up to but NOT including 5" -- five
# numbers: 0, 1, 2, 3, 4. The stop is exclusive; 5 in the
# range is False. range objects remember only start, stop,
# and step -- they cost the same whether they hold five
# numbers or five million.

# ============================================================
# [9] range(start, stop): two arguments, your own start
# ============================================================
# Give TWO arguments and the first becomes the start. Still
# exclusive on the stop. And floats are refused -- range()
# counts whole numbers only:

r = range(2, 7)
print(f"  list(range(2, 7)): {list(r)}")
print(f"  length: {len(r)}")
print(f"  4 in range: {4 in r}")
print(f"  7 in range: {7 in r}")

try:
    list(range(2.5))                   # not an integer count
except TypeError as error:
    print(f"  range(2.5) -> {type(error).__name__}")
#   list(range(2, 7)): [2, 3, 4, 5, 6]
#   length: 5
#   4 in range: True
#   7 in range: False
#   range(2.5) -> TypeError

# 2, 3, 4, 5, 6 -- starts at 2, stops just before 7. The
# membership tests prove the exclusive edge: 7 is not inside.
# range() is an integer counter; 2.5 has no place in one.

# ============================================================
# [10] range(start, stop, step): the third argument
# ============================================================
# THREE arguments add the step -- the size of each jump.
# Positive steps climb; negative steps count DOWN:

print(f"  evens: {list(range(0, 10, 2))}")
print(f"  countdown: {list(range(5, 0, -1))}")
print(f"  by threes: {list(range(10, 0, -3))}")
#   evens: [0, 2, 4, 6, 8]
#   countdown: [5, 4, 3, 2, 1]
#   by threes: [10, 7, 4, 1]

# range(0, 10, 2) walks 0, 2, 4, 6, 8 -- stops before 10.
# range(5, 0, -1) walks 5, 4, 3, 2, 1 -- stops before 0
# because a negative step approaches from above. The step
# decides direction; the stop stays exclusive either way.

# ============================================================
# [11] print(): the sep argument (advanced print, part 1)
# ============================================================
# The transcript's [06:38] and [06:54]. print() can take
# MANY arguments, and sep says what goes BETWEEN them. The
# default separator is one space; the lecture's exact
# example replaces it:

print(1, 2, 3)                          # default sep: one space
print(1, 2, 3, sep=" - ")              # the transcript's example
print("2026", "10", "18", sep="-")     # a date, no spaces
#   1 2 3
#   1 - 2 - 3
#   2026-10-18

# Three arguments, one line, and sep decided the joints. The
# same trick builds CSV rows, tab-separated files, and any
# joined text you would otherwise build with string
# concatenation.

# ============================================================
# [12] print(): the end argument (advanced print, part 2)
# ============================================================
# The second advanced parameter. By default print() ends with
# a newline -- end changes what (if anything) is written
# AFTER the message. Stay on the line, or end it yourself:

print("Loading", end=" ")               # keep the cursor here
print("complete")                       # finishes the line
#   Loading complete

print("start", end=" -> ")
print("middle", end=" -> ")
print("end")
#   start -> middle -> end

print("a", "b", "c", sep="|", end="|")  # sep + end together
print("done")
#   a|b|c|done

# end=" " replaced the newline with a space, so the second
# print continued the same line -- "Loading complete". The
# chain builds "start -> middle -> end" from three calls.
# And the last pair proves sep and end cooperate: the parts
# join with | and the line closes with one final | before
# "done" lands. Progress bars, prompt lines, and live
# counters all live on these two arguments.

# ============================================================
# [13] The summary
# ============================================================
# Four built-ins, four jobs:
#
#   1. sum(iterable[, start]) -- adds every number: the
#      lecture's sum([1, 10, 19, 70]) -> 100; tuples work;
#      empty -> 0; start joins the total (sum([1,2,3], 10)
#      -> 16); text inside raises TypeError
#   2. sum() + range() -- sum(range(5)) -> 10 and
#      sum(range(1, 6)) -> 15: totals without a written list
#   3. round(number) -- nearest integer by distance, with
#      negatives mirroring; but EXACT halves follow the
#      half-to-EVEN rule (2.5 -> 2, 3.5 -> 4, 0.5 -> 0,
#      1.5 -> 2, -2.5 -> -2) -- banker's rounding, the
#      official behavior
#   4. round(number, ndigits) -- N places after the point
#      (3.14159 -> 3.14 / 3.142); negative ndigits round the
#      whole numbers (87 -> 90 tens, 85 -> 80, 1234 -> 1200
#      hundreds); and 2.675 -> 2.67 exposes the float trap --
#      binary storage rounds what is STORED, not what you
#      typed
#   5. range(stop) -- from 0 up to but not including stop;
#      a range OBJECT (type 'range', list()/len()/in work
#      on it); range(5) -> [0, 1, 2, 3, 4], 5 not inside
#   6. range(start, stop) -- your own start, stop still
#      exclusive; floats raise TypeError -- integers only
#   7. range(start, stop, step) -- the step sets the jump and
#      the direction: evens [0, 2, 4, 6, 8], countdown
#      [5, 4, 3, 2, 1], by threes [10, 7, 4, 1]
#   8. print(..., sep=...) -- the join between arguments
#      (default one space; " - " and "-" from the examples)
#   9. print(..., end=...) -- the trailer after the message
#      (default '\n'; a space keeps the line open, "-> "
#      chains calls); sep and end work together
#
# sum() adds, round() rounds (halves go even), range()
# counts, print() presents. Six lessons of built-ins now sit
# in one growing toolbox.
