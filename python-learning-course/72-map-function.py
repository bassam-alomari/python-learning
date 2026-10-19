# -----------------------------------------------------------------
# Lesson 72: map() -- apply a function to every item
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : map(function, iterable) applies the function to
#            each element one by one; the result is a lazy map
#            OBJECT you read with a for loop or list(); it
#            pairs with def or a one-line lambda, and replaces
#            long traditional for loops
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's headline: map() is "من الحاجات العظيمة
# جداً" -- one of the greatest things in Python and programming
# in general, and you will use it constantly in the projects
# ahead.
#
# The shape:
#
#   map(function, iterable)
#
# One function, one iterable (list, tuple, ...). map() applies
# the function to EVERY element, one at a time. The result is
# not a list -- it is a map OBJECT, a lazy recipe: read it
# with a for loop, or convert it with list(map(...)).
#
# This lesson follows the transcript's own script: the names
# list my_all, cleaning with strip() + capitalize(), def or
# lambda inside the map, and the closing point that map()
# replaces long traditional loops with cleaner code.
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

# ============================================================
# [1] The idea: one function, one iterable, element by element
# ============================================================
# map(str.upper, words) asks str.upper() to run on each word
# in turn. First, WHAT comes back -- not a list, a map
# object:

words = ["cat", "dog"]
mapped = map(str.upper, words)
print(f"  type: {type(mapped).__name__}")
print(f"  is a list: {isinstance(mapped, list)}")
print(f"  as list: {list(mapped)}")
#   type: map
#   is a list: False
#   as list: ['CAT', 'DOG']

# type is "map" -- a dedicated object, not a list. It holds
# the PLAN (this function, that iterable), and list() is the
# switch that executes it.

# ============================================================
# [2] First real use: cleaning the names list (the transcript's)
# ============================================================
# The transcript's exact script: my_all holds names, a def
# function tidies each one -- strip the extra spaces, then
# capitalize the first letter:

my_all = ["  osama  ", "ahmed", "  sayed  "]

def clean_name(text):
    return text.strip().capitalize()

cleaned = map(clean_name, my_all)
print(list(cleaned))
#   ['Osama', 'Ahmed', 'Sayed']

# "  osama  ".strip() drops the padding, .capitalize() makes
# "Osama". One function call per element -- no append, no
# index, no loop on the screen. This is the transcript's
# تنظيف الأسماء in one line.

# ============================================================
# [3] Reading the map: with a for loop
# ============================================================
# The transcript names two ways to see the result. The first:
# a plain for loop -- a map object is iterable, so `for` walks
# it naturally:

for name in map(clean_name, my_all):
    print(f"  - {name}")
#   - Osama
#   - Ahmed
#   - Sayed

# No list() in sight -- the loop pulls one result at a time
# from the map object as it goes. Same data, second door.

# ============================================================
# [4] The map object is LAZY: nothing runs until you ask
# ============================================================
# A map object does NOT execute eagerly -- it stores the
# recipe, and the function fires only when something iterates
# over it. Watch the order of the output lines:

def shout(text):
    print(f"  applying to {text!r}")
    return text.upper()

pending = map(shout, ["aa", "bb"])      # built, NOT run
print("  nothing applied yet")
print(list(pending))                    # now it runs
#   nothing applied yet
#   applying to 'aa'
#   applying to 'bb'
#   ['AA', 'BB']

# "nothing applied yet" printed BEFORE any "applying to" line
# -- at creation, shout() had touched nothing. list() is what
# pulled the trigger. Laziness means a map over a million
# items costs you nothing until you read it.

# ============================================================
# [5] One pass only: the map object is consumed
# ============================================================
# Because each iteration RE-EXECUTES the plan, the second
# pass finds the object empty -- a map object is an iterator,
# and iterators run once:

same = map(clean_name, my_all)
print(f"  first pass: {list(same)}")
print(f"  second pass: {list(same)}")
#   first pass: ['Osama', 'Ahmed', 'Sayed']
#   second pass: []

# The first list() walked it to exhaustion; the second found
# nothing left. Need it twice? Call map() twice, or convert
# to a list ONCE and reuse that list. This one behavior
# explains most map() bugs in the wild.

# ============================================================
# [6] map() + lambda: the transcript's one-liner
# ============================================================
# The transcript's [mixing section]: instead of a separate
# def, write the function INLINE as a lambda, right inside
# the map -- the exact line from the lecture:

result = map(lambda text: text.strip().capitalize(), my_all)
print(list(result))
#   ['Osama', 'Ahmed', 'Sayed']

# Identical output to [2]'s def version -- but zero named
# functions, one statement. The lambda lives where it is
# used and disappears when the line ends. This is the
# transcript's "سطر برمجي واحد ومختصر": one short line.

# ============================================================
# [7] def vs lambda, and ready-made functions too
# ============================================================
# Side by side, then two surprises: functions you did NOT
# write work just as well -- map() only needs something
# callable:

def double(n):
    return n * 2

print(list(map(double, [1, 2, 3])))            # def version
print(list(map(lambda n: n * 2, [1, 2, 3])))   # lambda version
print(list(map(len, ["a", "bb", "ccc"])))       # a builtin
print(list(map(str, [1, 2, 3])))                # conversion
print(list(map(abs, [-4, 5, -6])))              # lesson 71's abs
#   [2, 4, 6]
#   [2, 4, 6]
#   [1, 2, 3]
#   ['1', '2', '3']
#   [4, 5, 6]

# def and lambda produce the same list -- pick whichever
# reads better (the transcript: lambda when the job is small
# and quick). Then len, str, and abs prove the point: ANY
# callable fits the first slot. map() does not care WHO
# defined the function.

# ============================================================
# [8] map() on numbers: math across a whole list
# ============================================================
# The pattern scales to arithmetic -- double, square, or
# round() (lesson 70) every element in one pass:

print(f"  doubled: {list(map(lambda n: n * 2, [1, 2, 3]))}")
print(f"  squared: {list(map(lambda n: n ** 2, [1, 2, 3, 4]))}")
print(f"  rounded: {list(map(round, [3.14, 2.71, 5.5]))}")
#   doubled: [2, 4, 6]
#   squared: [1, 4, 9, 16]
#   rounded: [3, 3, 6]

# Three list-builders with no building: no new list, no
# append, no range bookkeeping. And round() ran bare --
# map(round, floats) is the cleanest "round this column"
# line in Python (5.5 rounds to 6, the half-to-even rule
# from lesson 70 still applying).

# ============================================================
# [9] map() with TWO iterables: one function, paired items
# ============================================================
# The first slot can take more than one iterable. The
# function then receives them TOGETHER, one element from
# each -- and the run stops at the shortest:

prices = [10, 20, 30]
counts = [2, 1, 3]
totals = map(lambda p, c: p * c, prices, counts)
print(f"  totals: {list(totals)}")

full = map(lambda p, c: f"{p}x{c}", prices, counts)
print(f"  labels: {list(full)}")
#   totals: [20, 20, 90]
#   labels: ['10x2', '20x1', '30x3']

# lambda p, c takes price and count together: 10*2, 20*1,
# 30*3. The lists stay parallel (like zip, which you will
# meet later), and pairing is decided by POSITION. One
# function, two feeds.

# ============================================================
# [10] The old way vs the map way
# ============================================================
# The transcript's closing argument: map() spares you the
# long traditional loop and leaves the code cleaner. Here
# both, side by side, proving they agree:

raw = ["  omar ", " ali "]

old_way = []
for text in raw:
    old_way.append(text.strip().capitalize())

new_way = list(map(lambda text: text.strip().capitalize(), raw))

print(f"  for loop result: {old_way}")
print(f"  map result:      {new_way}")
print(f"  same result: {old_way == new_way}")
#   for loop result: ['Omar', 'Ali']
#   map result:      ['Omar', 'Ali']
#   same result: True

# Four lines of ceremony (empty list, for, append, call) versus
# one line of intention. Same output -- the difference is the
# sentence you must maintain. This is the transcript's
# "كود أكثر نظافة واحترافية" made visible.

# ============================================================
# [11] Good habit: the source list is never touched
# ============================================================
# map() READS the iterable and produces new values -- it does
# not modify the original. The messy input stays messy, ready
# for the next job:

tidy = list(map(clean_name, my_all))
print(f"  results: {tidy}")
print(f"  source unchanged: {my_all == ['  osama  ', 'ahmed', '  sayed  ']}")
#   results: ['Osama', 'Ahmed', 'Sayed']
#   source unchanged: True

# Transformation without mutation -- the input list is exactly
# as it was. Old values in, new values out, and nothing
# destroyed. That separation is what makes map() safe to
# reuse anywhere in a bigger pipeline.

# ============================================================
# [12] One session: everything together
# ============================================================
# The transcript's full script, end to end -- def pass,
# lambda pass, agreement, untouched source, and a measure of
# the results:

names = ["  osama  ", " ahmed ", "  sayed  ", "MONA "]

def tidy(text):
    return text.strip().capitalize()

pass_one = list(map(tidy, names))
pass_two = list(map(lambda text: text.strip().capitalize(), names))

print(f"  def pass:    {pass_one}")
print(f"  lambda pass: {pass_two}")
print(f"  identical: {pass_one == pass_two}")
print(f"  source untouched: {names == ['  osama  ', ' ahmed ', '  sayed  ', 'MONA ']}")
print(f"  longest name: {max(map(len, pass_one))} chars")
#   def pass:    ['Osama', 'Ahmed', 'Sayed', 'Mona']
#   lambda pass: ['Osama', 'Ahmed', 'Sayed', 'Mona']
#   identical: True
#   source untouched: True
#   longest name: 5 chars

# Two routes, one destination: def and lambda build the SAME
# list. The source list survived untouched. And the last line
# feeds map()'s result straight into max() (lesson 71) --
# map objects are iterables, so built-ins stack: map(len, ...)
# inside max() with no intermediate list at all.

# ============================================================
# [13] The summary
# ============================================================
# map() in full:
#
#   1. THE SHAPE -- map(function, iterable): one function,
#      one iterable; the function is applied to EVERY element,
#      one at a time. The transcript's headline: a great,
#      powerful tool you will use constantly
#   2. THE RESULT -- a map OBJECT, not a list (type name
#      "map"); two reading styles: `for item in map(...)` or
#      list(map(...)) -- both demonstrated on the names list
#   3. THE TRANSCRIPT'S SCRIPT -- my_all = ["  osama  ",
#      "ahmed", "  sayed  "]; clean_name(text) does
#      strip().capitalize(); map(clean_name, my_all) ->
#      ['Osama', 'Ahmed', 'Sayed']
#   4. LAZY -- at creation NOTHING runs (the recipe is only
#      stored); list() pulls the trigger and the function
#      fires element by element, in order
#   5. ONE PASS -- an iterator exhausts itself: first
#      list(same) -> the results, second -> []. Need it
#      twice? Map again, or keep the converted list -- this
#      is the classic map() trap
#   6. LAMBDA INSIDE -- the exact lecture line:
#      map(lambda text: text.strip().capitalize(), my_all);
#      same output as the def version, no named function, one
#      short line (the transcript's مختصر)
#   7. ANY CALLABLE FITS -- def, lambda, or a ready-made:
#      map(len, ...), map(str, ...), map(abs, ...), map(round,
#      ...) -- the first slot does not care who wrote the
#      function
#   8. NUMBERS WORK THE SAME -- double, square, round whole
#      columns without one append
#   9. TWO ITERABLES -- map(lambda p, c: ..., prices, counts)
#      feeds both lists pairwise, stopping at the shortest
#   10. VS THE FOR LOOP -- the append version and the map
#       version print identical results; four lines of
#       ceremony become one line of intention -- the
#       transcript's cleaner, more professional code
#   11. SOURCE SAFE -- the input list is never modified; new
#       values out, old values intact
#   12. STACKS WITH THE REST -- max(map(len, pass_one))
#       chains map() into max() with no intermediate list
#
# One function. One iterable. Every element. That is map().
