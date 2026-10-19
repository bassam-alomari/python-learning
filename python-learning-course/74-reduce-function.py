# -----------------------------------------------------------------
# Lesson 74: reduce() -- compress a list into one value
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : reduce(function, iterable) folds the iterable two
#            elements at a time -- result meets the next item,
#            over and over -- until ONE value remains; it
#            imports from functools (from functools import
#            reduce) and merges with lambda for one-line
#            accumulations
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's finale: reduce() is the LAST function of
# this famous built-in section, and it usually travels with
# map() and filter(). The pair of the trio's shapes:
#
#   map(...)     same length, transformed
#   filter(...)  shorter, selected
#   reduce(...)  ONE value, compressed
#
# The transcript's core image [00:30]: take TWO elements,
# apply the function, merge the RESULT with the THIRD, and
# keep going -- the list folds into itself step by step until
# a single final element comes out.
#
# Why the import? The transcript's [01:06]: in modern Python
# reduce() was MOVED into the functools module, so it must be
# brought in first:
#
#   from functools import reduce
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

import functools
from functools import reduce            # lesson point [3]

# ============================================================
# [1] The trio's shapes: map keeps length, filter shrinks,
#     reduce ends in ONE value
# ============================================================
# Before the mechanics, the position of reduce() beside its
# two companions (lessons 72 and 73), all on the same data:

my_nums = [2, 4, 6, 8, 10]

mapped = list(map(lambda n: n * 10, my_nums))
filtered = list(filter(lambda n: n > 5, my_nums))
folded = reduce(lambda a, b: a + b, my_nums)

print(f"  map:    {mapped} -> same length")
print(f"  filter: {filtered} -> shorter")
print(f"  reduce: {folded} -> one value")
#   map:    [20, 40, 60, 80, 100] -> same length
#   filter: [6, 8, 10] -> shorter
#   reduce: 30 -> one value

# Five in, five out; five in, three out; five in, ONE out.
# reduce() is the only one of the three that changes the
# SHAPE of the data into a single result -- that is the
# transcript's "تخرج بعنصر واحد نهائي".

# ============================================================
# [2] The fold, one merge at a time (the transcript's image)
# ============================================================
# [00:30] made concrete: watch each pairing happen. The
# function takes TWO numbers, returns their sum, and that
# sum becomes "num1" of the NEXT round:

def trace_add(num1, num2):
    result = num1 + num2
    print(f"  {num1} + {num2} = {result}")
    return result

total = reduce(trace_add, my_nums)
print(f"  final: {total}")
#   2 + 4 = 6
#   6 + 6 = 12
#   12 + 8 = 20
#   20 + 10 = 30
#   final: 30

# Round 1: 2 and 4 become 6. Round 2: that 6 meets the third
# element 6 -- 12. Then 12 + 8 = 20, then 20 + 10 = 30.
# Four merges, five elements, one answer. The accumulator
# (the running total) IS the first argument of the next call
# -- that is what "folding" means.

# ============================================================
# [3] The import: reduce() lives in functools
# ============================================================
# The transcript's [01:06] and [01:09]. reduce() is NOT a
# plain built-in anymore -- modern Python ships it inside the
# functools module, which the two lines at the top of this
# file already imported. Proof it arrived, and what kind of
# callable it is:

print(f"  type: {type(reduce).__name__}")
print(f"  functools.reduce is it: {functools.reduce is reduce}")
print(f"  first call: {reduce(lambda a, b: a + b, [2, 4, 6, 8, 10])}")
#   type: builtin_function_or_method
#   functools.reduce is it: True
#   first call: 30

# `from functools import reduce` puts the name in reach;
# `functools.reduce` would work too (and `functools.reduce is
# reduce` proves both names point at the same function). Its
# type name is builtin_function_or_method -- reduce() is
# compiled into the language, not written in Python; still,
# one import line and it behaves like any built-in.

# ============================================================
# [4] First practical: the transcript's sum of my_nums
# ============================================================
# [01:45] and [02:11], exact script: my_nums = [2, 4, 6, 8,
# 10], add them through repeated pairing. Then the built-in
# that does the same job, for a reality check:

total = reduce(lambda num1, num2: num1 + num2, my_nums)
print(f"  reduce total: {total}")
print(f"  sum() total:  {sum(my_nums)}")
print(f"  identical: {total == sum(my_nums)}")
#   reduce total: 30
#   sum() total:  30
#   identical: True

# 2+4=6, +6=12, +8=20, +10=30 -- the transcript's "المجموع
# النهائي المخفض في قيمة واحدة". sum() agrees because sum()
# IS a reduce with + as its rule: reduce() is the general
# machinery underneath such shortcuts.

# ============================================================
# [5] reduce + lambda: the transcript's one-liner
# ============================================================
# [02:40]: no def, no trace -- the merge rule written inline,
# exactly as the lecture's line:

total = reduce(lambda num1, num2: num1 + num2, my_nums)
print(f"  {total}")
#   30

# lambda takes the two current elements, returns their sum,
# reduce() handles the sequencing. One line, full stop --
# the transcript's "سطر برمجي واحد بكفاءة عالية".

# ============================================================
# [6] The rule is yours: multiply instead of add
# ============================================================
# reduce() does not care WHAT the function does -- only that
# it eats two values and returns one. Product, with the same
# trace treatment:

def trace_mul(num1, num2):
    result = num1 * num2
    print(f"  {num1} * {num2} = {result}")
    return result

product = reduce(trace_mul, [1, 2, 3, 4])
print(f"  product: {product}")
#   1 * 2 = 2
#   2 * 3 = 6
#   6 * 4 = 24
#   product: 24

# Same folding shape, different operator: 1*2=2, the 2 meets
# 3 (6), the 6 meets 4 (24). Factorial, running totals,
# any accumulation -- swap the lambda, keep the machinery.

# ============================================================
# [7] Beyond numbers: reduce() over strings
# ============================================================
# The "logic you define" from [04:47] is not necessarily
# arithmetic -- joining text is the same fold with + on
# strings:

joined = reduce(lambda a, b: a + b, ["py", "thon", "!"])
print(f"  joined: {joined!r}")

spaced = reduce(lambda a, b: a + " " + b, ["elzero", "python", "fun"])
print(f"  spaced: {spaced!r}")
#   joined: 'python!'
#   spaced: 'elzero python fun'

# "py" + "thon" = "python", then + "!" -- one value out of
# three. With a space as the rule, three words become one
# line. reduce() reads the data type from ITS elements: + on
# numbers adds, + on strings concatenates.

# ============================================================
# [8] reduce() finding the max (the pattern to remember)
# ============================================================
# "Keep the bigger one" is a fold too -- the running value
# only ever holds the champion (the ternary lambda from
# lesson 64 does the comparing):

biggest = reduce(lambda a, b: a if a > b else b, my_nums)
print(f"  reduce finds max: {biggest}")
print(f"  max() agrees: {max(my_nums)}")
#   reduce finds max: 10
#   max() agrees: 10

# 2 vs 4 keeps 4; 4 vs 6 keeps 6; ... 8 vs 10 keeps 10.
# The accumulator never forgets the winner -- same reason
# loop-with-running-max works, stated as one expression.

# ============================================================
# [9] The function must take EXACTLY two arguments
# ============================================================
# The transcript's mechanics made checkable: every call
# passes (accumulator, next_element). A function wanting a
# different count refuses:

def show_pair(first, second):
    return first + second

print(f"  two params accepted: {show_pair(3, 4)}")

try:
    reduce(lambda only_one: only_one, [1, 2])
except TypeError as error:
    print(f"  one-param function -> {type(error).__name__}")
#   two params accepted: 7
#   one-param function -> TypeError

# reduce() will always call with TWO values -- where would a
# third come from? The signature of the rule is fixed:
# (what came before, what comes now).

# ============================================================
# [10] The edges: one element, and no elements
# ============================================================
# What folds down when there is nothing to fold? A single
# element needs no merge -- it IS the result. An empty
# iterable has no pair to start with, and no start value to
# fall back on:

single = reduce(lambda a, b: a + b, [42])
print(f"  single element: {single}")

try:
    reduce(lambda a, b: a + b, [])
except TypeError as error:
    print(f"  empty, no start -> {type(error).__name__}")
#   single element: 42
#   empty, no start -> TypeError

# One item: no pairing happened, the answer is the item --
# same rule as sum([42]) and max([42]). Zero items with no
# initializer: there is nothing to return, so reduce()
# raises, exactly as sum([]) with no start would be 0 by
# design but reduce has NO default rule to guess.

# ============================================================
# [11] The third argument: a start value (initializer)
# ============================================================
# reduce() accepts an optional initial accumulator -- the
# running value's FIRST value before any element is seen.
# It answers the empty-list problem too:

with_start = reduce(lambda a, b: a + b, my_nums, 100)
print(f"  sum with start 100: {with_start}")

empty_ok = reduce(lambda a, b: a + b, [], 0)
print(f"  empty with start: {empty_ok}")
#   sum with start 100: 130
#   empty with start: 0

# 100 + 2 + 4 + 6 + 8 + 10 = 130 -- the start JOINS the
# addition (the same behavior as sum's second argument from
# lesson 70). And an empty list with start 0 now has an
# answer: 0. With an initializer, reduce() never has to
# guess -- the seed decides.

# ============================================================
# [12] One session: everything together
# ============================================================
# The transcript's whole section in one block -- four folds,
# two agreement checks, the untouched source:

my_nums = [2, 4, 6, 8, 10]
names = ["elzero", "python", "fun"]

summed = reduce(lambda a, b: a + b, my_nums)
product = reduce(lambda a, b: a * b, my_nums)
joined = reduce(lambda a, b: a + " " + b, names)
biggest = reduce(lambda a, b: a if a > b else b, my_nums)

print(f"  sum: {summed}")
print(f"  product: {product}")
print(f"  joined: {joined!r}")
print(f"  biggest: {biggest}")
print(f"  agrees with sum(): {summed == sum(my_nums)}")
print(f"  source intact: {my_nums == [2, 4, 6, 8, 10]}")
#   sum: 30
#   product: 3840
#   joined: 'elzero python fun'
#   biggest: 10
#   agrees with sum(): True
#   source intact: True

# Four different rules on one list (and one word list): add
# -> 30, multiply -> 3840 (2*4*6*8*10), join with spaces ->
# 'elzero python fun', keep-the-bigger -> 10. The built-in
# sum() confirms the first, and the source list never
# changed -- reduce() reads, folds, and leaves.

# ============================================================
# [13] The summary
# ============================================================
# reduce() in full:
#
#   1. THE POSITION -- the LAST function of this famous
#      built-in section, traveling with map() and filter();
#      their shapes: map keeps length, filter shrinks,
#      reduce ends in ONE value
#   2. THE MECHANISM -- take TWO elements, run the function,
#      merge the RESULT with the THIRD, continue until the
#      whole iterable folds into a single final element (the
#      transcript's [00:30]); the running result is called
#      the accumulator and becomes the first argument of
#      every next round
#   3. THE IMPORT -- modern Python moved reduce() into the
#      functools module: `from functools import reduce` (the
#      transcript's [01:06]); `functools.reduce is reduce`
#      confirms the alias
#   4. THE SHAPE -- reduce(function, iterable); a trace on
#      [2, 4, 6, 8, 10] shows 2+4=6, 6+6=12, 12+8=20,
#      20+10=30 -- four merges, one answer
#   5. THE TRANSCRIPT'S PRACTICAL -- my_nums = [2, 4, 6, 8,
#      10] summed to 30; sum() returns the same 30 because
#      sum() IS a reduce-with-plus -- reduce() is the general
#      machinery under such shortcuts
#   6. LAMBDA MERGE -- reduce(lambda num1, num2: num1 + num2,
#      my_nums) -> 30: the lecture's exact one-liner
#   7. YOUR RULE -- multiply folds [1, 2, 3, 4] to 24;
#      strings fold too ("py" + "thon" + "!" -> 'python!',
#      words with a space -> 'elzero python fun'); keep-the-
#      bigger folds my_nums to 10, agreeing with max() --
#      the logic is whatever YOU write (the transcript's
#      [04:47])
#   8. TWO ARGUMENTS EXACTLY -- every call is (accumulator,
#      next_element); a one-parameter function raises
#      TypeError -- that is the contract
#   9. THE EDGES -- one element returns itself (42); empty
#      with no start raises TypeError -- reduce() has no
#      default rule to guess
#   10. THE INITIALIZER -- the optional third argument seeds
#       the accumulator: start 100 -> 130 (the seed joins
#       the sum, like sum's start), and empty + start 0 ->
#       0; with a seed, reduce() never guesses
#   11. SOURCE SAFE -- the input list is untouched; four
#       folds, one session, `source intact: True`
#
# Two in. One out. Repeat. That is reduce().
