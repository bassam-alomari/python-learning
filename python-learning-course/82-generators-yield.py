# -----------------------------------------------------------------
# Lesson 82: generators (yield)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : a function that LOOKS normal but uses yield
#            instead of return -- values produced one at a
#            time, the call body deferred until the first
#            next(), state kept between fetches (resume
#            where it left off), for-looping generators,
#            and the one-line generator expression
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: an ADVANCED and important
# topic -- Generators. The definition [00:11]:
#
#   A generator is a function that appears normal, but
#   instead of `return` (which hands back ALL the data at
#   once and finishes), it uses `yield` to GENERATE and
#   hand back one value at a time, KEEPING its standing
#   place in memory.
#
# The payoff [00:35]: unbelievable memory savings (nothing
# is stored all at once -- a value is produced when it is
# NEEDED) and total control of the flow (you decide when
# the next piece arrives).
#
# The mechanics: call the function -> get a generator
# object (the body does NOT run yet) -> next() fetches
# values, each call RESUMING exactly where the last yield
# paused [02:31] -> a for loop walks the rest [03:44].
#
# Everything here is deterministic -- pure built-ins, no
# clock, no files. Every expected output was produced by
# running the file, not written from memory.

# ============================================================
# [1] What a generator is [00:11]
# ============================================================
# The transcript's shape, spelled out: same def keyword,
# yield instead of return. Three yields, three values --
# written as a function, used as a stream:

def my_generator():
    yield 1
    yield 2
    yield 3

print(f"  defined with def: {type(my_generator).__name__}")

source_handle = open(__file__, encoding="utf-8")
source_text = source_handle.read()
source_handle.close()
print(f"  uses yield: {'yield' in source_text}")
#   defined with def: function
#   uses yield: True

# It really is a function type -- nothing exotic in the
# DEFINITION. The magic appears at the CALL, next
# section. (The self-inspection above reads this very
# file to confirm a yield lives in it -- proof, not
# assumption.)

# ============================================================
# [2] The call returns an object, not the values [02:31]
# ============================================================
# Calling my_generator() does NOT run the body and does
# NOT return 1. It returns a GENERATOR object -- the
# transcript's "تحصل على كائن Generator":

gen = my_generator()

print(f"  call result type: {type(gen).__name__}")
print(f"  values already out: False (nothing yielded yet)")
print(f"  has __next__: {hasattr(gen, '__next__')}")
#   call result type: generator
#   values already out: False (nothing yielded yet)
#   has __next__: True

# generator -- a brand new type, not list, not tuple. It
# carries __next__ like every cursor from lesson 81:
# generators ARE iterators, built from functions.

# ============================================================
# [3] next(): one yield per call [02:14]
# ============================================================
# The transcript's print(next(my_gen)). Three calls, three
# yields, in the order they were written:

walk = my_generator()

print(f"  first: {next(walk)}")
print(f"  second: {next(walk)}")
print(f"  third: {next(walk)}")
#   first: 1
#   second: 2
#   third: 3

# 1, 2, 3 -- exactly the transcript's my_generator with
# yield 1; yield 2; yield 3. One call per value; you
# control the pace.

# ============================================================
# [4] End of the stream: StopIteration [04:31]
# ============================================================
# Lesson 81's closing signal applies here too -- a
# generator runs out of yields and raises:

done = my_generator()
try:
    next(done)
    next(done)
    next(done)
    next(done)
except StopIteration:
    print("  fourth next() raises StopIteration: True")

try:
    next(done)
except StopIteration:
    print("  exhausted stays exhausted: True")
#   fourth next() raises StopIteration: True
#   exhausted stays exhausted: True

# Generators are iterators (section [2]); iterators die
# when their source is spent. The for loop knows this
# signal by heart -- section [7] relies on it.

# ============================================================
# [5] Resumes where it left off [02:31]
# ============================================================
# The transcript's key sentence: "يبدأ الـ Generator من
# النقطة التي توقف عندها تمامًا وليس من البداية". A
# generator with INTERNAL STATE proves it -- a running
# total that keeps counting between fetches:

def running_total():
    total = 0
    for number in (10, 20, 30):
        total += number
        yield total

steps = running_total()
print(f"  first yield: {next(steps)}")
print(f"  second yield: {next(steps)}")
print(f"  third yield: {next(steps)}")
#   first yield: 10
#   second yield: 30
#   third yield: 60

# 10, then 10+20=30, then 30+30=60. Each next() walks the
# for loop ONE more step, carrying the local variable
# `total` across the pauses. The state lives in the
# generator between calls -- the "مكان وقوفها الحالي في
# الذاكرة" the transcript promises.

# ============================================================
# [6] Proof the body waits: a spy in the works
# ============================================================
# If the call really does NOT run the body until the
# first next(), a side effect placed at the top of the
# function will stay silent until then:

trail = []

def spy():
    trail.append("ran")
    yield 1

sleeper = spy()
before = len(trail)
first_value = next(sleeper)
after = len(trail)

print(f"  silent before first next(): {before == 0}")
print(f"  first value: {first_value}")
print(f"  body ran after next(): {after == 1}")
#   silent before first next(): True
#   first value: 1
#   body ran after next(): True

# The list was empty until next() pressed START. Calling
# a generator is buying a TICKET; next() is boarding.
# Memory efficiency follows directly: nothing is
# produced -- and nothing is stored -- until you ask.

# ============================================================
# [7] Walking a generator with for [03:44]
# ============================================================
# The transcript's [03:44]: a plain for loop drains the
# remaining values "بكل سهولة واحترافية". No next(), no
# try/except -- the loop knows StopIteration:

collected = []
fresh = my_generator()
for value in fresh:
    collected.append(value)

print(f"  for collected: {collected}")
#   for collected: [1, 2, 3]

# The whole stream, in order. Lesson 81's five-line
# recipe (iter once, next forever, break on the signal)
# is running invisibly underneath -- generators were
# built to walk this way.

# ============================================================
# [8] One-shot, just like every iterator
# ============================================================
# Lesson 81's map/filter/reversed rule: the cursor
# finished, so a second walk finds nothing:

drained = my_generator()
first_pass = []
for value in drained:
    first_pass.append(value)

second_pass = []
for value in drained:
    second_pass.append(value)

print(f"  first pass: {first_pass}")
print(f"  second pass: {second_pass}")
#   first pass: [1, 2, 3]
#   second pass: []

# [1, 2, 3] then [] -- the transcript's memory economy
# has a price: a generator is consumed, not re-read. Need
# it again? Call the function again (section [9]).

# ============================================================
# [9] Two calls, two independent streams
# ============================================================
# Like lesson 81's two cursors: each call mints a fresh
# generator with its own position:

a = my_generator()
b = my_generator()

print(f"  a first: {next(a)}")
print(f"  b first: {next(b)}")
print(f"  a second: {next(a)}")
print(f"  they are different objects: {a is not b}")
#   a first: 1
#   b first: 1
#   a second: 2
#   they are different objects: True

# a is at 2 while b is still at its first 1 -- two
# positions, two copies of the state, no interference.
# (And a fresh call is the official way to "rewind".)

# ============================================================
# [10] The one-line generator: a generator expression
# ============================================================
# Bonus beyond the transcript, completing the picture:
# parentheses instead of a def -- the same lazy object,
# built from any iterable:

squares = (x * x for x in range(4))

print(f"  genexp type: {type(squares).__name__}")
print(f"  first fetch: {next(squares)}")
print(f"  drained by for: {[value for value in squares]}")
#   genexp type: generator
#   first fetch: 0
#   drained by for: [1, 4, 9]

# Same type as section [2]'s object. next() got 0
# (0*0); the for loop finished 1, 4, 9 -- and the
# generator is spent. List comprehension syntax in
# parentheses = values on demand, not values in memory.

# ============================================================
# [11] The whole transcript's recipe, once more
# ============================================================
# Define with yield, call to get the object, next() to
# step, for to drain -- the four moves in order:

def countdown(start):
    yield start
    yield start - 1
    yield start - 2

stream = countdown(5)
print(f"  step 1: {next(stream)}")
print(f"  step 2: {next(stream)}")

rest = []
for value in stream:
    rest.append(value)
print(f"  for finishes the rest: {rest}")
#   step 1: 5
#   step 2: 4
#   for finishes the rest: [3]

# next() twice, then for -- MIXING the two styles on the
# same generator works because they share one cursor. The
# loop picks up exactly where the last next() paused:
# value 3, the last yield.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- the type, the
# stepping, the resume, the for walk, the drain, and the
# one-liner:

final = my_generator()
print(f"  call -> generator: {type(final).__name__}")
print(f"  next order: {next(final)}, {next(final)}, {next(final)}")

stateful = running_total()
print(f"  resumed totals: {next(stateful)}, {next(stateful)}, {next(stateful)}")

for_each = []
for value in my_generator():
    for_each.append(value)
print(f"  for walk: {for_each}")

once = my_generator()
list(once)
print(f"  drained after for: {list(once)}")

oneliner = (x * 10 for x in range(3))
print(f"  genexp: {next(oneliner)} then {list(oneliner)}")
#   call -> generator: generator
#   next order: 1, 2, 3
#   resumed totals: 10, 30, 60
#   for walk: [1, 2, 3]
#   drained after for: []
#   genexp: 0 then [10, 20]

# Call returns generator; next() walks 1-2-3; the
# stateful one proves the resume (10, 30, 60); for walks
# the stream; a drained generator stays drained; and the
# one-line expression behaves identically. Generators,
# end to end.

# ============================================================
# [13] The summary
# ============================================================
# Generators, from the transcript, complete:
#
#   1. WHAT [00:11] -- a function that uses `yield`
#      instead of `return`: values are GENERATED one at
#      a time and the function KEEPS its standing place
#      in memory; the def itself looks ordinary
#      (type(my_generator) -> 'function')
#   2. THE CALL [02:31] -- calling it returns a
#      GENERATOR OBJECT (type -> 'generator') and does
#      NOT run the body; the object carries __next__
#      (and __iter__) -- generators ARE iterators
#   3. next() STEPPING [02:14] -- one yield per call, in
#      source order: 1, 2, 3 from the transcript's shape
#   4. THE END -- the last yield is followed by
#      StopIteration, same as lesson 81; fourth next()
#      catches it True; exhausted stays exhausted True
#   5. RESUME [02:31] -- the key sentence, proved with a
#      running total: yields 10, then 30, then 60 -- the
#      local `total` survives every pause; state lives
#      in the generator, not in your hands
#   6. LAZY BODY -- a spy appended before the first yield
#      stays silent until next() is called (trail empty
#      before True, ran after True): calling is buying a
#      ticket, next() is boarding -- that IS the memory
#      economy [00:35]
#   7. FOR WALKING [03:44] -- a plain for drains the
#      stream ([1, 2, 3]) with no next()/try needed --
#      the loop knows StopIteration
#   8. ONE-SHOT -- like map/filter/reversed: first for
#      -> [1, 2, 3], second for -> []; to replay, call
#      the function again (a fresh object every call)
#   9. INDEPENDENT STREAMS -- two calls make two
#      generators, each with its own position (a at 2
#      while b still at 1)
#  10. GENERATOR EXPRESSION (bonus) -- (x * x for x in
#      range(4)) builds the same 'generator' type in one
#      line; next() 0, for drains [1, 4, 9] -- list
#      syntax in parentheses, values on demand
#  11. MIXING STYLES -- next() twice then for on the
#      SAME generator works (countdown: 5, 4 by hand,
#      [3] by loop) -- one cursor, two drivers
#  12. THE DISCIPLINE -- no raw reprs, no addresses, no
#      clock: only type names, values from fixed
#      sources, and boolean facts -- byte-stable like
#      every lesson before it
#
# return gives you the whole loaf. yield hands you one
# slice at a time -- and remembers the knife.
