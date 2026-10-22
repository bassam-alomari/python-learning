# -----------------------------------------------------------------
# Lesson 81: iterable vs iterator
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : what an Iterable is (list, tuple, dict, set,
#            string -- anything with __iter__), what an
#            Iterator is (the stateful cursor with
#            __next__), iter() to convert, next() to
#            advance, StopIteration as the end signal,
#            and what the for loop does behind the scenes
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: a lesson that REQUIRES focus --
# the difference between Iterable and Iterator. The
# transcript's own framing:
#
#   ITERABLE -- any container holding elements you can
#               visit one by one: list, tuple, dict, set,
#               string [00:13]
#   ITERATOR -- the object that TRACKS your place and
#               fetches the next element step by step
#               [02:50]; it knows where you stand now and
#               what comes next in line
#
# The conversion is iter() [03:11]; the fetching is
# next() [04:31]; the end signal is StopIteration; and
# the for loop [05:32] is nothing but those two calls on
# repeat, with the error swallowed for you.
#
# Everything here is deterministic -- pure built-ins, no
# clock, no files. Every expected output was produced by
# running the file, not written from memory.

# ============================================================
# [1] Iterable: the containers you can walk [00:13]
# ============================================================
# The transcript's five examples. Every one carries the
# __iter__ method -- the official mark of an iterable:

sample_list = [10, 20, 30]
sample_tuple = (10, 20, 30)
sample_dict = {"a": 1, "b": 2}
sample_set = {10, 20, 30}
sample_text = "python"

print(f"  list has __iter__: {hasattr(sample_list, '__iter__')}")
print(f"  tuple has __iter__: {hasattr(sample_tuple, '__iter__')}")
print(f"  dict has __iter__: {hasattr(sample_dict, '__iter__')}")
print(f"  set has __iter__: {hasattr(sample_set, '__iter__')}")
print(f"  str has __iter__: {hasattr(sample_text, '__iter__')}")
#   list has __iter__: True
#   tuple has __iter__: True
#   dict has __iter__: True
#   set has __iter__: True
#   str has __iter__: True

# Five containers, five Trues. __iter__ is the ticket to
# the party: if a thing has it, for loops work on it,
# map() works on it, the whole iteration family works on
# it.

# ============================================================
# [2] Testing iterable-or-not [01:47]
# ============================================================
# The transcript: strings and lists ARE iterable; plain
# integers are NOT -- you cannot loop over them directly.
# The probe is hasattr(__iter__); the proof is trying:

print(f"  text is iterable: {hasattr(sample_text, '__iter__')}")
print(f"  list is iterable: {hasattr(sample_list, '__iter__')}")
print(f"  int is iterable: {hasattr(42, '__iter__')}")

try:
    for x in 42:
        pass
except TypeError:
    print("  looping an int raises TypeError: True")
#   text is iterable: True
#   list is iterable: True
#   int is iterable: False
#   looping an int raises TypeError: True

# Two facts side by side: the probe says False, and the
# real for loop raises TypeError. Numbers are values,
# not containers -- exactly the transcript's warning.

# ============================================================
# [3] Iterator: the cursor that knows its place [02:50]
# ============================================================
# An iterable is the WAREHOUSE; an iterator is the
# WORKER holding your position. Make one and inspect it:

iterator = iter(sample_list)

print(f"  iterator type: {type(iterator).__name__}")
print(f"  has __next__: {hasattr(iterator, '__next__')}")
print(f"  the list itself has __next__: {hasattr(sample_list, '__next__')}")
#   iterator type: list_iterator
#   has __next__: True
#   the list itself has __next__: False

# list_iterator, not list. It carries __next__ -- the
# "give me the next one" button. The original list does
# NOT: the warehouse cannot fetch, only the worker can.
# That single difference (plus __iter__, which it also
# has) separates the two worlds.

# ============================================================
# [4] iter(): the conversion [03:11]
# ============================================================
# The transcript's exact move: my_iterator = iter(my_list)

converted = iter([1, 2, 3])
print(f"  iter() worked: {type(converted).__name__}")
print(f"  two calls, two iterators: {type(iter([1, 2, 3])) is type(iter([4, 5, 6]))}")
#   iter() worked: list_iterator
#   two calls, two iterators: True

# iter() is the only bridge between the worlds. Two calls
# make two INDEPENDENT cursors -- each with its own
# position (proof in section [7]).

# ============================================================
# [5] next(): fetching, one step at a time [04:15]
# ============================================================
# The transcript's print(next(my_iterator)). Each call
# hands over the NEXT element and advances the cursor:

walk = iter([10, 20, 30])

first = next(walk)
second = next(walk)
third = next(walk)

print(f"  first: {first}")
print(f"  second: {second}")
print(f"  third: {third}")
#   first: 10
#   second: 20
#   third: 30

# 10, then 20, then 30 -- in ORDER, one per call. The
# iterator remembers where it stopped between calls;
# that memory is the entire job the transcript assigns
# it ("يعرف أين يقف الآن وما هو العنصر التالي").

# ============================================================
# [6] StopIteration: the end of the road [04:31]
# ============================================================
# After the last element, next() does NOT return None --
# it RAISES StopIteration. Catch it, and the trip ends
# cleanly:

done = iter([10, 20, 30])
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
    print("  exhausted iterators stay exhausted: True")
#   fourth next() raises StopIteration: True
#   exhausted iterators stay exhausted: True

# Three elements, three successful fetches (unseen, they
# ran inside the try), then the fourth call trips the
# signal. A sixth call would trip it again -- exhaustion
# is permanent; no rewinding in an iterator.

# ============================================================
# [7] An iterator IS its own iterator
# ============================================================
# Ask an iterator for iter(itself) and you get... itself.
# That is the formal half of the definition:

it = iter([10, 20, 30])
print(f"  iter(it) is it: {iter(it) is it}")
print(f"  so the for loop needs no new cursor: {hasattr(it, '__iter__') and hasattr(it, '__next__')}")
#   iter(it) is it: True
#   so the for loop needs no new cursor: True

# The iterable's iter() makes a FRESH cursor each time
# (section [4]); the iterator's iter() returns the SAME
# cursor -- one worker, one position, forever.

# ============================================================
# [8] Every container breeds its own iterator breed
# ============================================================
# The type name tells you where the cursor came from:

print(f"  list -> {type(iter([1, 2])).__name__}")
print(f"  str -> {type(iter('abc')).__name__}")
print(f"  tuple -> {type(iter((1, 2))).__name__}")
print(f"  dict -> {type(iter({'a': 1})).__name__}")
print(f"  set -> {type(iter({1, 2})).__name__}")
#   list -> list_iterator
#   str -> str_ascii_iterator
#   tuple -> tuple_iterator
#   dict -> dict_keyiterator
#   set -> set_iterator

# Five breeds, five names. Note dict's: it walks the
# KEYS (dict_keyiterator) -- the same keys the for loop
# gives you when you for over a dict. And the string's
# name mentions ascii on this Python build; the behavior
# is the same: one CHARACTER per step.

# ============================================================
# [9] What the for loop does behind the scenes [05:32]
# ============================================================
# The transcript's reveal: for calls iter() once, then
# next() repeatedly, and catches StopIteration to exit
# "بأمان دون أن يشعر المستخدم". Here is the machinery,
# exposed:

collected = []
manual = iter([10, 20, 30])
while True:
    try:
        collected.append(next(manual))
    except StopIteration:
        break

print(f"  manual loop collected: {collected}")

looped = []
for value in [10, 20, 30]:
    looped.append(value)
print(f"  for loop collected: {looped}")
print(f"  both agree: {collected == looped}")
#   manual loop collected: [10, 20, 30]
#   for loop collected: [10, 20, 30]
#   both agree: True

# That while-try-except IS the for loop, written out.
# iter() once, next() forever, StopIteration -> break.
# The transcript's "خلف الكواليس" (behind the curtains)
# is exactly these five lines.

# ============================================================
# [10] The one-shot family you already met
# ============================================================
# Lessons 72, 73 and 75 introduced map, filter and
# reversed -- all three are ITERATORS, which is why they
# drain:

nums = [1, 2, 3]
doubled = map(lambda x: x * 2, nums)

print(f"  map is an iterator: {hasattr(doubled, '__next__')}")
print(f"  first pass: {list(doubled)}")
print(f"  second pass: {list(doubled)}")
#   map is an iterator: True
#   first pass: [2, 4, 6]
#   second pass: []

# __next__ present -> iterator -> one trip only. The
# empty second pass is the same StopIteration story as
# section [6]: the cursor finished, nothing rewinds it.
# (Lesson 75's reversed() behaves identically.)

# ============================================================
# [11] The recipe, generalized
# ============================================================
# The manual five lines work on ANY iterable -- try them
# on a string and a dict:

chars = []
char_walk = iter("py")
while True:
    try:
        chars.append(next(char_walk))
    except StopIteration:
        break
print(f"  string walked: {chars}")

keys = []
key_walk = iter({"x": 1, "y": 2})
while True:
    try:
        keys.append(next(key_walk))
    except StopIteration:
        break
print(f"  dict keys walked: {keys}")
#   string walked: ['p', 'y']
#   dict keys walked: ['x', 'y']

# Same cursor machinery, different cargo: characters
# from the string, keys from the dict. iterable feeds
# iterator; iterator feeds next(); next() feeds you.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- the two worlds,
# the bridge, the fetches, the signal, and the curtain:

print(f"  list iterable: {hasattr([1], '__iter__')}")
print(f"  int iterable: {hasattr(42, '__iter__')}")
print(f"  list_iterator has __next__: {hasattr(iter([1]), '__next__')}")
print(f"  list has __next__: {hasattr([1], '__next__')}")
final_walk = iter([10, 20, 30])
print(f"  next order: {next(final_walk)}, {next(final_walk)}, {next(final_walk)}")
try:
    next(final_walk)
except StopIteration:
    print(f"  end signal: StopIteration caught")
print(f"  for == while+next: {collected == looped}")
#   list iterable: True
#   int iterable: False
#   list_iterator has __next__: True
#   list has __next__: False
#   next order: 10, 20, 30
#   end signal: StopIteration caught
#   for == while+next: True

# A list that CAN be entered, a number that CANNOT, a
# cursor that fetches, a warehouse that cannot, the order
# 10-20-30, the closing signal, and the for loop proven
# to be nothing more than its own five-line recipe.

# ============================================================
# [13] The summary
# ============================================================
# Iterable vs iterator, from the transcript, complete:
#
#   1. ITERABLE [00:13] -- any container whose elements
#      can be visited in order: list, tuple, dict, set,
#      string -- marked by the __iter__ method (all five
#      probed: True)
#   2. THE TEST [01:47] -- hasattr(obj, '__iter__'):
#      strings and lists True, integers False; looping
#      an int raises TypeError -- numbers are values,
#      not containers
#   3. ITERATOR [02:50] -- the object that tracks the
#      walk and fetches one element per step; it knows
#      "where it stands now and what comes next"; marked
#      by __next__ (and it keeps __iter__ too)
#   4. iter() [03:11] -- the bridge: iter(my_list) ->
#      list_iterator; two calls make two independent
#      cursors with independent positions
#   5. next() [04:15] -- one fetch per call, in order:
#      10, then 20, then 30; the cursor REMEMBERS its
#      position between calls
#   6. StopIteration [04:31] -- next() past the end
#      RAISES it (not None, not a magic value); catch it
#      to end cleanly; exhausted iterators stay
#      exhausted -- no rewinding
#   7. SELF-HOSTING -- iter(iterator) is the iterator
#      itself (True): one worker, one position; the
#      iterable's iter() by contrast mints a FRESH
#      cursor every call
#   8. BREEDS -- list_iterator, str_ascii_iterator,
#      tuple_iterator, dict_keyiterator (dicts walk
#      their KEYS), set_iterator -- the type name names
#      the warehouse
#   9. THE FOR LOOP CURTAIN [05:32] -- for == iter() once
#      + next() forever + except StopIteration: break;
#      the five-line manual loop and the real for
#      collect [10, 20, 30] identically (both agree:
#      True)
#  10. THE ONE-SHOT FAMILY -- map/filter/reversed (lessons
#      72/73/75) carry __next__: first list() -> [2, 4, 6],
#      second -> [] -- the same drain the raw iterator
#      performs
#  11. GENERAL RECIPE -- the while-try-next-break pattern
#      walks strings ('p', 'y') and dicts (keys 'x', 'y')
#      unchanged: iterable in, elements out
#  12. THE DISCIPLINE -- print TYPE NAMES and BOOLEAN
#      facts, never object reprs that embed memory
#      addresses (course rule 1); everything else here
#      is pure built-ins, so the output is byte-stable
#
# Iterable = the warehouse. Iterator = the worker with
# a checklist. next() = one item. StopIteration = done.
