# -----------------------------------------------------------------
# Lesson 73: filter() -- keep what passes the test
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : filter(function, iterable) keeps only the elements
#            whose condition returns truthy and discards the
#            falsy/False ones; the condition can be a def or a
#            one-line lambda; startswith() filters names; and
#            filter() replaces long loops with complex
#            conditions
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's pairing: map() applies a function to EVERY
# element and returns all the results -- filter() is the sieve.
# It runs each element through a CONDITION that answers
# True/False:
#
#   truthy  -> kept
#   falsy / False -> discarded, gone from the final result
#
# The shape, same as map:
#
#   filter(function, iterable)
#
# This lesson follows the transcript's script: the number list
# my_numbers = [1, 19, 10, 20, 100, 5] filtered to numbers
# greater than 10, names filtered with startswith(), the
# lambda merge, and the closing point about replacing long
# loops with complex conditions.
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

# ============================================================
# [1] The idea: map tests everyone, filter keeps a few
# ============================================================
# The transcript's [00:46] contrast, side by side on the same
# list. map() answers a question for EVERY element; filter()
# uses the same question as a gate:

my_numbers = [1, 19, 10, 20, 100, 5]

print(f"  map tests all:     {list(map(lambda n: n > 10, my_numbers))}")
print(f"  filter keeps some: {list(filter(lambda n: n > 10, my_numbers))}")
#   map tests all:     [False, True, False, True, True, False]
#   filter keeps some: [19, 20, 100]

# map() kept six answers -- six booleans, the verdict on each
# element. filter() used the same verdict to CUT the list:
# only 19, 20, and 100 passed. One transforms, the other
# selects. Same function slot, opposite jobs.

# ============================================================
# [2] First practical: numbers greater than 10 (the transcript's)
# ============================================================
# The transcript's [01:45] and [01:57], exact script: my_numbers
# holds [1, 19, 10, 20, 100, 5], and the condition is
# "bigger than 10":

def is_big(n):
    return n > 10

kept = filter(is_big, my_numbers)
print(list(kept))
#   [19, 20, 100]

# 1 fails (too small), 19 passes, **10 fails too** -- the
# condition is >, not >=, so exactly-10 is excluded, exactly
# as the transcript's "أكبر من 10 فقط" demands. 20 and 100
# pass, 5 fails. Six in, three out.

# ============================================================
# [3] The rule: the condition only needs a truthy/falsy answer
# ============================================================
# The transcript's [03:00]: the passed function must return a
# logical True or False so filter() can decide. The honest
# detail: any TRUTHY value keeps the element, any FALSY value
# discards it -- bool() runs underneath. Proof with modulo,
# which returns 1 or 0, not True/False:

print(f"  odd via %: {list(filter(lambda n: n % 2, [1, 2, 3, 4, 5]))}")
#   odd via %: [1, 3, 5]

# n % 2 gives 1 (truthy) for odd, 0 (falsy) for even -- no
# explicit True/False written anywhere, and filter() had all
# it needed. The transcript's "قيمة منطقية" is the DECISION
# being decidable: bool(1) is True, bool(0) is False. Write
# a condition that clearly answers "yes or no" and you are
# always right.

# ============================================================
# [4] filter(None, ...): the condition IS the truth itself
# ============================================================
# The falsy rule stated in its purest form. Pass NO function
# -- None is the default -- and filter() keeps every truthy
# element, drops every falsy one, from the transcript's
# Falsy family (0, "", None, empty containers):

messy = [0, 1, "", "x", None, [7]]
print(f"  filter(None): {list(filter(None, messy))}")
#   filter(None): [1, 'x', [7]]

# 0, "", and None are falsy -- gone. 1, "x", and [7] are
# truthy -- kept. filter(None, ...) is the "remove the empty
# ones" button, and it is built into the language.

# ============================================================
# [5] The filter object: lazy, one pass, not a list
# ============================================================
# Like map() (lesson 72), filter() returns its own OBJECT --
# type "filter", a lazy recipe that executes on read and runs
# out after one full pass:

kept = filter(lambda n: n > 10, my_numbers)
print(f"  type: {type(kept).__name__}")
print(f"  is a list: {isinstance(kept, list)}")
print(f"  as list: {list(kept)}")
#   type: filter
#   is a list: False
#   as list: [19, 20, 100]

# Lazy: the test does not run at creation, only when read.
# Watch the order:

def mark(n):
    print(f"  testing {n}")
    return n > 10

pending = filter(mark, [1, 19])          # built, NOT run
print("  nothing tested yet")
print(list(pending))                     # now it runs
#   nothing tested yet
#   testing 1
#   testing 19
#   [19]

# "nothing tested yet" came BEFORE both "testing" lines.
# And one pass only, exactly like map():

same = filter(lambda n: n > 10, my_numbers)
print(f"  first pass: {list(same)}")
print(f"  second pass: {list(same)}")
#   first pass: [19, 20, 100]
#   second pass: []

# The iterator exhausts itself. One object, one full read --
# then it is empty. (Same trap as lesson 72, same fix:
# filter again, or keep the converted list.)

# ============================================================
# [6] Second practical: names that start with a letter
# ============================================================
# The transcript's [06:08] and [06:29]: filter a name list
# with startswith() to keep only the names beginning with one
# chosen letter:

my_names = ["osama", "ahmed", "sayed", "ali", "mona"]

def starts_with_a(name):
    return name.startswith("a")

print(list(filter(starts_with_a, my_names)))
#   ['ahmed', 'ali']

# "osama" starts with o -- out. "ahmed" with a -- in.
# "sayed" s -- out. "ali" a -- in. "mona" m -- out. The
# condition is one method call that reads like English:
# name.startswith("a").

# ============================================================
# [7] startswith() is case sensitive (and how to fix it)
# ============================================================
# The letter must match exactly -- 'a' is not 'A'. A capital
# needle on the lowercase list finds NOTHING, and the fix
# stacks with last lesson's map():

print(f"  needle 'a': {list(filter(lambda n: n.startswith('a'), my_names))}")
print(f"  needle 'A': {list(filter(lambda n: n.startswith('A'), my_names))}")

cased = list(map(str.capitalize, my_names))
print(f"  needle 'A' after map(capitalize): {list(filter(lambda n: n.startswith('A'), cased))}")
#   needle 'a': ['ahmed', 'ali']
#   needle 'A': []
#   needle 'A' after map(capitalize): ['Ahmed', 'Ali']

# Empty list for 'A' -- startswith compares byte by byte, and
# lowercase osama does not begin with capital A. map()
# capitalized the names first, then the SAME filter found
# Ahmed and Ali. Two built-ins, one pipeline.

# ============================================================
# [8] filter + lambda: the transcript's one-liners
# ============================================================
# The transcript's [07:09]: skip the def, write the condition
# inline as a lambda -- clean and professional, one line each:

print(list(filter(lambda n: n > 10, my_numbers)))
print(list(filter(lambda n: n.startswith("a"), my_names)))
#   [19, 20, 100]
#   ['ahmed', 'ali']

# Both def versions' outputs, reproduced without a single
# named function. The condition lives where it is used --
# small test, short life, one line.

# ============================================================
# [9] Complex conditions: join tests with `and` / `or`
# ============================================================
# The transcript's [09:22] -- filter() shines when the
# condition gets COMPLEX, where a hand-written loop turns into
# nested mush. A range band, then a band plus parity:

print(f"  10 < n < 100: {list(filter(lambda n: n > 10 and n < 100, my_numbers))}")
print(f"  big and even: {list(filter(lambda n: n > 10 and n % 2 == 0, my_numbers))}")
print(f"  1 or n > 99: {list(filter(lambda n: n == 1 or n > 99, my_numbers))}")
#   10 < n < 100: [19, 20]
#   big and even: [20, 100]
#   1 or n > 99: [1, 100]

# Three rules, three lines: the band excludes 100 (not <
# 100) and excludes 10 (not > 10); "big and even" keeps 20
# and 100; "the tiny one or the huge one" keeps 1 and 100.
# Each condition is one boolean sentence -- in a for loop,
# each would be another indented if.

# ============================================================
# [10] The old way vs the filter way
# ============================================================
# The transcript's closing argument made visible -- the
# traditional loop with a condition, against the one-line
# filter. Both must agree:

kept = []
for n in my_numbers:
    if n > 10:
        kept.append(n)

filtered = list(filter(lambda n: n > 10, my_numbers))

print(f"  for loop result: {kept}")
print(f"  filter result:   {filtered}")
print(f"  same result: {kept == filtered}")
#   for loop result: [19, 20, 100]
#   filter result:   [19, 20, 100]
#   same result: True

# Empty list, for, if, append -- four moving parts that must
# stay in sync -- versus one filter() that states the job.
# The transcript's توفير أكواد طويلة وحلقات تكرار with
# شروط معقدة: the complexity moves INTO the condition, where
# it belongs, and the scaffolding disappears.

# ============================================================
# [11] Stacking: filter() feeds map(), or the reverse
# ============================================================
# Filter objects and map objects are both iterables -- so they
# compose. Select first, then transform; or transform first,
# then select:

as_text = list(map(str, filter(lambda n: n > 10, my_numbers)))
print(f"  filter then map: {as_text}")

messy_names = ["osama", "", "ahmed", "  ", "ali"]
kept_names = list(map(str.capitalize, filter(lambda n: n.strip() != "", messy_names)))
print(f"  drop blanks, then capitalize: {kept_names}")
#   filter then map: ['19', '20', '100']
#   drop blanks, then capitalize: ['Osama', 'Ahmed', 'Ali']

# First line: three big numbers survive the gate, then each
# becomes text. Second: filter() discarded "" and "  " (both
# strip to nothing), and map() capitalized what remained --
# the names never lost their original padding until map()
# rebuilt them. Readable pipelines beat nested loops every
# time.

# ============================================================
# [12] One session: everything together
# ============================================================
# The transcript's full coverage in one block -- numbers,
# names, parity, a count, a max, and the untouched source:

my_numbers = [1, 19, 10, 20, 100, 5]
my_names = ["osama", "ahmed", "sayed", "ali", "mona"]

big = list(filter(lambda n: n > 10, my_numbers))
a_names = list(filter(lambda n: n.startswith("a"), my_names))
odds = list(filter(lambda n: n % 2 == 1, my_numbers))

print(f"  > 10: {big}")
print(f"  a-names: {a_names}")
print(f"  odd: {odds}")
print(f"  count of big: {len(big)}")
print(f"  biggest of big: {max(big)}")
print(f"  old list intact: {my_numbers == [1, 19, 10, 20, 100, 5]}")
#   > 10: [19, 20, 100]
#   a-names: ['ahmed', 'ali']
#   odd: [1, 19, 5]
#   count of big: 3
#   biggest of big: 100
#   old list intact: True

# The three gates each answered from the transcript's own
# data. len() counted the survivors, max() (lesson 71)
# measured them -- filter objects convert to lists that
# ordinary built-ins understand -- and the original numbers
# list is exactly as it started: read, never modified.

# ============================================================
# [13] The summary
# ============================================================
# filter() in full:
#
#   1. THE IDEA -- where map() transforms EVERY element and
#      returns all results, filter() SIEVES: the condition's
#      truthy keeps an element, falsy/False discards it from
#      the final result (the transcript's [00:46])
#   2. THE SHAPE -- filter(function, iterable), identical
#      plumbing to map()
#   3. THE TRANSCRIPT'S FIRST PRACTICAL -- my_numbers =
#      [1, 19, 10, 20, 100, 5], condition n > 10 ->
#      [19, 20, 100]; remember 10 itself is excluded --
#      "larger than", not "larger or equal"
#   4. THE CONDITION RULE -- a logical yes/no decision is
#      required (the transcript's [03:00]); underneath,
#      any truthy keeps and any falsy drops: n % 2 giving
#      1/0 works without writing True/False at all
#   5. filter(None, ...) -- no function, truth IS the
#      condition: [0, 1, "", "x", None, [7]] -> [1, "x", [7]]
#   6. THE OBJECT -- type "filter", not a list; LAZY (the
#      test fires on read -- "nothing tested yet" prints
#      first), and ONE PASS (second list() -> []). Same
#      iterator rules as lesson 72's map
#   7. THE SECOND PRACTICAL -- names via startswith():
#      ["osama", "ahmed", "sayed", "ali", "mona"] with "a"
#      -> ['ahmed', 'ali']; case sensitive ('A' finds [] on
#      lowercase), fixed by map(str.capitalize, ...) stacked
#      before the filter
#   8. LAMBDA MERGE -- filter(lambda n: n > 10, my_numbers)
#      and filter(lambda n: n.startswith("a"), my_names):
#      the def disappears, one clean line remains
#   9. COMPLEX CONDITIONS -- `and` / `or` build bands and
#      combinations in one boolean sentence: 10 < n < 100 ->
#      [19, 20]; big and even -> [20, 100]; 1 or n > 99 ->
#      [1, 100]
#   10. VS THE FOR LOOP -- loop+if+append and filter() print
#       identical results (same result: True); the
#       scaffolding goes away, the condition stays -- the
#       transcript's savings in long codes and loops with
#       complex conditions
#   11. STACKING -- filter() feeds map() (big numbers ->
#       ['19', '20', '100']) and both read naturally left to
#       right: select, then transform
#   12. SOURCE SAFE -- the input list is never modified;
#       ordinary built-ins (len, max) consume the result
#
# One function. One condition. Keep the passers. That is
# filter().
