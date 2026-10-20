# -----------------------------------------------------------------
# Lesson 75: enumerate(), help(), and reversed()
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : enumerate() adds an automatic counter to any
#            iterable (with a configurable start=), help()
#            prints the built-in manual for any function,
#            module, or object, and reversed() returns a
#            reversed-object you read with a loop or list()
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Three more built-ins the transcript calls easy, useful, and
# something you will use constantly:
#
#   enumerate(iterable, start=)   (index, value) pairs
#   help(object)                  the usage manual, on the spot
#   reversed(iterable)            the elements, backwards
#
# enumerate() removes the manual counter you would otherwise
# write by hand; help() ends the "search the internet" habit;
# reversed() is the polite way to walk a list backwards. All
# three return objects you read with a for loop or list() --
# the same reading rules as map/filter (lessons 72-73).
#
# ONE SAFETY NOTE: help(print) in a real terminal prints the
# FULL manual page -- far too big (and version-dependent) to
# sit in this lesson's stable output. So help() here is
# CAPTURED into a string, and only stable facts about the
# capture are printed (length > 0, contains a word, returns
# None). The comments say what a live terminal would show.
#
# Everything in this file runs by itself. Every expected output
# was produced by running the file, not written from memory.

import contextlib
import io

# ============================================================
# [1] enumerate(): the manual counter, retired
# ============================================================
# The transcript's [00:15]: instead of building a counter by
# hand, enumerate() attaches the index to every element --
# each iteration gives the number AND the value. Side by
# side, the old way and the new way:

names = ["osama", "ahmed", "sayed"]

manual = []
counter = 0
for name in names:
    manual.append((counter, name))
    counter += 1

print(f"  manual pairs:  {manual}")
print(f"  enumerate:     {list(enumerate(names))}")
print(f"  identical: {manual == list(enumerate(names))}")
#   manual pairs:  [(0, 'osama'), (1, 'ahmed'), (2, 'sayed')]
#   enumerate:     [(0, 'osama'), (1, 'ahmed'), (2, 'sayed')]
#   identical: True

# Six lines of bookkeeping against one call. The pairs are
# tuples -- (index, value) -- ready to unpack or print. The
# counter is the transcript's "عداد تلقائي" and it starts at
# 0 by default.

# ============================================================
# [2] The daily form: unpack the pair in a for loop
# ============================================================
# The shape you will actually write every week -- one name
# for the index, one for the value, both from the same
# pair:

for index, name in enumerate(names):
    print(f"  {index}: {name}")
#   0: osama
#   1: ahmed
#   2: sayed

# No range(len(names)), no manual += 1 -- enumerate() hands
# both halves of the tuple over, and the loop unpacks them.
# This is the "دون الحاجة لإنشاء عداد يدوي منفصل" of the
# transcript, in its final form.

# ============================================================
# [3] The start parameter: begin at 1, or at 10
# ============================================================
# The transcript's [01:11]: the counter's first value is
# yours to choose -- enumerate(iterable, start=1) for human
# counting, or any other number at all:

print(list(enumerate(names, start=1)))
print(list(enumerate(names, start=10)))
#   [(1, 'osama'), (2, 'ahmed'), (3, 'sayed')]
#   [(10, 'osama'), (11, 'ahmed'), (12, 'sayed')]

# start=1 is what humans mean by "first"; start=10 shows the
# parameter takes ANY seed. The default (0) is only a
# default, never a rule.

# ============================================================
# [4] In practice: numbered menus and ranked lists
# ============================================================
# Numbering is the everyday job of enumerate(): menus,
# instructions, leaderboards. Two, straight from the
# pattern:

menu = ["coffee", "tea", "cake"]
for number, item in enumerate(menu, start=1):
    print(f"  {number}. {item}")
#   1. coffee
#   2. tea
#   3. cake

scores = [88, 95, 72]
for place, score in enumerate(sorted(scores, reverse=True), start=1):
    print(f"  place {place}: {score}")
#   place 1: 95
#   place 2: 88
#   place 3: 72

# A menu with items 1, 2, 3 -- and a podium: sorted the
# scores high-to-low, then let enumerate() do the places.
# Zero manual indices anywhere.

# ============================================================
# [5] help(): the manual, on demand
# ============================================================
# The transcript's [03:19] and [03:47]: pass ANY function,
# module, or object to help() and Python prints its complete
# usage guide -- no internet search needed. In a live
# terminal, help(print) fills the screen with the print()
# manual. Here the output is CAPTURED so the lesson stays
# stable, and we print facts about it instead:

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    help(print)                         # the full manual, captured
captured = buffer.getvalue()

print(f"  produced text: {len(captured) > 0}")
print(f"  mentions print: {'print' in captured}")

with contextlib.redirect_stdout(io.StringIO()):
    returned = help(str)
print(f"  help() returns: {returned}")
#   produced text: True
#   mentions print: True
#   help() returns: None

# help(print) really did write a full manual into the buffer
# (a live terminal would have shown it); help(str) the same
# for strings; and every help() call returns None -- it
# prints as its side effect and hands nothing back. The
# habit to build: stuck on any tool? help(tool) first, search
# engine second.

# ============================================================
# [6] help() works on YOUR functions too
# ============================================================
# Anything with a docstring gets a proper manual page. Write
# a tiny function, ask help() for it, and the docstring
# comes back inside the guide:

def greet(name):
    """Return a friendly greeting for the given name."""
    return f"Hello, {name}!"

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    help(greet)
page = buffer.getvalue()

print(f"  docstring shows: {'Return a friendly greeting' in page}")
print(f"  signature shows: {'greet(name)' in page}")
#   docstring shows: True
#   signature shows: True

# The docstring you wrote appears in the help() page, next
# to the signature greet(name). Your documentation and the
# built-in manual are the same pipeline -- write the
# docstring once, help() (and every reader) gets it forever.

# ============================================================
# [7] reversed(): the elements, backwards
# ============================================================
# The transcript's [03:52] and [04:15]. reversed() walks an
# iterable from the end -- a list, a tuple, a string's
# characters -- and returns a reversed OBJECT, not a list:

nums = [1, 2, 3, 4]
backwards = reversed(nums)
print(f"  type: {type(backwards).__name__}")
print(f"  as list: {list(backwards)}")
print(f"  original: {nums}")
#   type: list_reverseiterator
#   as list: [4, 3, 2, 1]
#   original: [1, 2, 3, 4]

# type is list_reverseiterator -- the transcript calls it a
# "reversed object", and that is exactly what it is: an
# iterator dedicated to walking backwards. list()
# materializes it into [4, 3, 2, 1], and the source list is
# untouched: reversed() reads, never rewrites.

# ============================================================
# [8] reversed() with a loop, on text, and vs [::-1]
# ============================================================
# Three doors to the same room: a for loop, a string's
# letters, and the slice spelling:

seen = []
for value in reversed(nums):
    seen.append(value)
print(f"  loop collected: {seen}")

letters = list(reversed("hello"))
print(f"  reversed string: {''.join(letters)!r}")
print(f"  slice way: {'hello'[::-1]!r}")
print(f"  same result: {''.join(reversed('hello')) == 'hello'[::-1]}")
#   loop collected: [4, 3, 2, 1]
#   reversed string: 'olleh'
#   slice way: 'olleh'
#   same result: True

# The loop pulled 4, 3, 2, 1 one at a time; "hello" turned
# into its letters backwards ('olleh'); and reversed() and
# [::-1] agree -- pick reversed() when you want the OBJECT
# (lazy, reusable as an iterator), the slice when you want
# the reversed COPY immediately.

# ============================================================
# [9] The reversed object runs once (the map/filter rule)
# ============================================================
# Like map objects (72) and filter objects (73), a reversed
# object is an iterator: read it fully once and it is spent:

same = reversed(nums)
print(f"  first pass: {list(same)}")
print(f"  second pass: {list(same)}")
#   first pass: [4, 3, 2, 1]
#   second pass: []

# First walk: all four numbers. Second walk: nothing left.
# The three iterator families of this course -- map, filter,
# reversed -- share one rule: one full read per object.
# Need it twice? Call reversed() twice, or keep the list.

# ============================================================
# [10] Stacked: enumerate() over reversed()
# ============================================================
# Both return iterables, so they compose -- count the
# backwards walk, numbering from 1 exactly where humans
# would:

for index, value in enumerate(reversed(nums), start=1):
    print(f"  #{index}: {value}")
#   #1: 4
#   #2: 3
#   #3: 2
#   #4: 1

# reversed() flipped the order, enumerate() numbered the
# flipped order -- "first" is now 4 because that is what
# comes first from the end. Two built-ins, one loop, zero
# bookkeeping.

# ============================================================
# [11] Stacked the other way: reversed() over enumerate()
# ============================================================
# Order of stacking changes the story. Number first (0-up),
# then reverse the PAIRS -- the last item now wears index 0:

pairs = list(enumerate(names))
flipped = list(reversed(pairs))
print(f"  numbered: {pairs}")
print(f"  pairs reversed: {flipped}")
#   numbered: [(0, 'osama'), (1, 'ahmed'), (2, 'sayed')]
#   pairs reversed: [(2, 'sayed'), (1, 'ahmed'), (0, 'osama')]

# The PAIRS reversed -- sayed's tuple comes first, carrying
# its original index 2. Same objects, different arrival
# order. Which stacking you want depends on whether the
# NUMBER should flip with the data or count the flip.

# ============================================================
# [12] One session: everything together
# ============================================================
# The transcript's three functions in one block -- numbered,
# reversed, documented, source intact:

names = ["osama", "ahmed", "sayed"]

numbered = list(enumerate(names, start=1))
backwards = list(reversed(names))

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    help(len)
doc_ok = "Return the number of items" in buffer.getvalue()

print(f"  numbered: {numbered}")
print(f"  backwards: {backwards}")
print(f"  help(len) has a docstring: {doc_ok}")
print(f"  source intact: {names == ['osama', 'ahmed', 'sayed']}")
#   numbered: [(1, 'osama'), (2, 'ahmed'), (3, 'sayed')]
#   backwards: ['sayed', 'ahmed', 'osama']
#   help(len) has a docstring: True
#   source intact: True

# enumerate(start=1) gave human counting; reversed() flipped
# the names without touching the list; help(len) proved the
# manual knows the len() docstring ("Return the number of
# items in a sequence."); and the source list is exactly as
# it started. Three easy functions, one tidy session.

# ============================================================
# [13] The summary
# ============================================================
# Three tools, three jobs:
#
#   1. enumerate(iterable) -- the automatic counter: each
#      iteration yields (index, value) pairs; default start
#      is 0; the manual alternative (append + counter += 1)
#      produces IDENTICAL pairs -- the transcript's "دون
#      الحاجة لإنشاء عداد يدوي منفصل"
#   2. THE DAILY FORM -- for index, name in enumerate(names):
#      unpack both halves in the loop; no range(len(...)),
#      no manual += 1
#   3. start= -- the first value is yours: start=1 for human
#      counting ("1. coffee"), start=10 when you need
#      another seed (the transcript's [01:11])
#   4. PRACTICE -- numbered menus and ranked scoreboards:
#      enumerate(sorted(scores, reverse=True), start=1)
#      writes the podium by itself
#   5. help(object) -- the complete usage manual for any
#      function, module, or object, printed on the spot
#      (the transcript's [03:19]: no internet search
#      needed); it returns None -- printing IS the effect;
#      here the pages were CAPTURED to keep output stable
#      (a live terminal shows the full page)
#   6. help() ON YOUR CODE -- a docstring becomes part of
#      the manual: greet(name) and its docstring both show
#      up in help(greet)'s page
#   7. reversed(iterable) -- a reversed OBJECT (the type
#      name is list_reverseiterator), read with a for loop
#      or list(); works on lists and on string letters
#      ('hello' -> 'olleh'); equals the [::-1] slice
#      result; the source is never modified
#   8. ONE PASS -- like map and filter objects, a reversed
#      object exhausts itself: first list() -> everything,
#      second -> []
#   9. STACKING -- enumerate(reversed(nums), start=1)
#      numbers the backwards walk; reversed(list(enumerate
#      (...))) flips the pairs while keeping their original
#      indices -- stacking order changes the story
#   10. SOURCE SAFE -- every function here reads without
#        rewriting; the input list survives every combination
#
# Count it (enumerate), learn it (help), flip it (reversed).
