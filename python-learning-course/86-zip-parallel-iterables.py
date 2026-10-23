# -----------------------------------------------------------------
# Lesson 86: zip() -- parallel iterables
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : merging several iterables element-by-element
#            into tuples, the golden shortest-list rule,
#            one for loop with tuple unpacking over
#            nums/names/skills, zip with dicts (and the
#            nested-loop it replaces), unzip with zip(*),
#            sets, and reading parallel sources cleanly
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: a practical and very important
# application -- iterating over MORE THAN ONE iterable at
# the same time with zip().
#
# The idea [00:13]: zip() accepts several iterables
# (lists, tuples, ...), merges the elements that FACE each
# other in matching order into TUPLES, and hands them out
# so one for loop can walk everything.
#
# The golden rule [00:20]: zip stops at the SHORTEST
# iterable -- a 10-element list beside a 3-element list
# yields 3 tuples; the extra elements in the long list
# are ignored.
#
# The practical [01:07]: for num, name, skill in
# zip(nums, names, skills) -- three lists, ONE loop, no
# index bookkeeping. Plus zip with dicts [02:10] and the
# best-practice verdict [07:20].
#
# Everything here is deterministic -- pure built-ins, no
# clock, no files. Every expected output was produced by
# running the file, not written from memory.

# ============================================================
# [1] What zip does [00:13]
# ============================================================
# Two lists, paired by position, delivered as tuples:

letters = ["a", "b", "c"]
marks = [1, 2, 3]

paired = list(zip(letters, marks))

print(f"  type of the pairing: {type(paired).__name__}")
print(f"  pairs: {paired}")
print(f"  first pair is a tuple: {type(paired[0]).__name__}")
#   type of the pairing: list
#   pairs: [('a', 1), ('b', 2), ('c', 3)]
#   first pair is a tuple: tuple

# ('a', 1), ('b', 2), ('c', 3) -- element facing element,
# in ORDER. The zip name itself pictures a zipper:
# tooth meets tooth, slider moves on.

# ============================================================
# [2] The golden rule: stop at the shortest [00:30]
# ============================================================
# The transcript's exact scenario: a long list beside a
# short one. 10 elements vs 3 -- zip ends at 3:

long_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
short_list = ["x", "y", "z"]

cut = list(zip(long_list, short_list))

print(f"  long has {len(long_list)} elements")
print(f"  short has {len(short_list)} elements")
print(f"  zip produced {len(cut)} pairs")
print(f"  stopped at the shortest: {len(cut) == len(short_list)}")
print(f"  pairs: {cut}")
#   long has 10 elements
#   short has 3 elements
#   zip produced 3 pairs
#   stopped at the shortest: True
#   pairs: [(1, 'x'), (2, 'y'), (3, 'z')]

# Three pairs, then silence -- elements 4..10 never even
# looked for partners. The transcript's القاعدة الذهبية:
# no error, no padding, no warning; the shortest list
# decides when the show is over.

# ============================================================
# [3] One pair per step (it is an iterator) [00:13]
# ============================================================
# Lesson 81/82 territory: zip() itself is an iterator --
# next() walks it pair by pair:

walker = zip(letters, marks)

print(f"  first: {next(walker)}")
print(f"  second: {next(walker)}")
print(f"  third: {next(walker)}")
#   first: ('a', 1)
#   second: ('b', 2)
#   third: ('c', 3)

# One tuple per call, in pairing order. (And lesson 81's
# rule applies: a drained zip stays drained -- call
# zip() again for a fresh walk.)

# ============================================================
# [4] The practical: three lists, ONE loop [01:07]
# ============================================================
# The transcript's for num, name, skill in zip(nums,
# names, skills) -- numbers, names, and skills side by
# side, printed by a single loop:

nums = [1, 2, 3]
names = ["Osama", "Mona", "Ali"]
skills = ["Python", "JavaScript", "SQL"]

for num, name, skill in zip(nums, names, skills):
    print(f"  {num}. {name} -> {skill}")
#   1. Osama -> Python
#   2. Mona -> JavaScript
#   3. Ali -> SQL

# THREE lists, ONE for header, THREE variables receiving
# each tuple's parts. The transcript's "طباعة واحدة"
# loop: no range(), no len(), no [i] anywhere.

# ============================================================
# [5] The unpacking is real
# ============================================================
# Each loop iteration hands a 3-element tuple; the three
# names on the left of `in` split it apart. Prove it
# outside the loop:

row = next(zip(nums, names, skills))
print(f"  a row is a tuple of three: {type(row).__name__} len {len(row)}")
print(f"  its parts: {row[0]}, {row[1]}, {row[2]}")
#   a row is a tuple of three: tuple len 3
#   its parts: 1, Osama, Python

# Same tuple shape the for loop unpacked -- the syntax
# `for a, b, c in ...` is plain tuple unpacking (lesson
# 25's skill) applied to zip's output.

# ============================================================
# [6] zip replaces the index machinery [01:07]
# ============================================================
# Before zip, parallel data meant range(len(...)) and
# [i] everywhere -- the "nested" bookkeeping the
# transcript wants gone. Build both ways, compare:

old_school = []
for i in range(len(nums)):
    old_school.append((nums[i], names[i], skills[i]))

new_school = list(zip(nums, names, skills))

print(f"  index way: {old_school}")
print(f"  zip way: {new_school}")
print(f"  both agree: {old_school == new_school}")
#   index way: [(1, 'Osama', 'Python'), (2, 'Mona', 'JavaScript'), (3, 'Ali', 'SQL')]
#   zip way: [(1, 'Osama', 'Python'), (2, 'Mona', 'JavaScript'), (3, 'Ali', 'SQL')]
#   both agree: True

# Identical output, one third of the code, zero index
# arithmetic. That is the transcript's توفير كتابة
# حلقات تكرار متداخلة معقدة -- the loop count lives in
# the SHORTEST list now, not in your head.

# ============================================================
# [7] zip with dicts: rebuilding pairs [02:10]
# ============================================================
# Dictionaries are iterables too (of their keys). Feed
# zip a key list and a value list and dict() snaps them
# back together:

keys = ["x", "y", "z"]
values = [10, 20, 30]

rebuilt = dict(zip(keys, values))

print(f"  rebuilt: {rebuilt}")
print(f"  equals the original: {rebuilt == {'x': 10, 'y': 20, 'z': 30}}")
#   rebuilt: {'x': 10, 'y': 20, 'z': 30}
#   equals the original: True

# zip pairs them, dict() consumes the pairs -- keys and
# values from two sources become ONE clean structure.
# The transcript's "ربط مفاتيح وقيم بطريقة نظيفة".

# ============================================================
# [8] Inside a dict: keys and values side by side
# ============================================================
# Walking a dict's keys AND values together without
# [key] lookups -- zip over the dict itself and its
# values:

inventory = {"pen": 3, "book": 5, "bag": 1}

side_by_side = list(zip(inventory, inventory.values()))
print(f"  zip(dict, dict.values()): {side_by_side}")
print(f"  same as items(): {side_by_side == list(inventory.items())}")
#   zip(dict, dict.values()): [('pen', 3), ('book', 5), ('bag', 1)]
#   same as items(): True

# Iterating a dict yields its KEYS -- so zip(keys_view,
# values) rebuilds every (key, value) pair, byte-for-byte
# what items() returns. Two roads, one destination.

# ============================================================
# [9] Unzipping: zip(*pairs) [02:10]
# ============================================================
# The reverse trick -- hand zip a pack of pairs (the *
# unpacks them) and the columns fall out:

pairs = [(1, "a"), (2, "b"), (3, "c")]
numbers_column, letters_column = zip(*pairs)

print(f"  numbers column: {numbers_column}")
print(f"  letters column: {letters_column}")
print(f"  round trip: {list(zip(numbers_column, letters_column)) == pairs}")
#   numbers column: (1, 2, 3)
#   letters column: ('a', 'b', 'c')
#   round trip: True

# Rows became columns in one expression. zip zips; zip(*)
# unzips -- the same tool working in both directions,
# which is why it survives in professional code.

# ============================================================
# [10] zip with sets (sorted for truth) [02:10]
# ============================================================
# Sets are iterables too -- but their order is not
# guaranteed, so this lesson sorts the pairs before
# printing (the discipline: never trust a set's order on
# screen):

left = {1, 2, 3}
right = {4, 5, 6}

set_pairs = sorted(zip(left, right))
print(f"  sorted pairs: {set_pairs}")
print(f"  shortest rule holds: {len(set_pairs) == min(len(left), len(right))}")
#   sorted pairs: [(1, 4), (2, 5), (3, 6)]
#   shortest rule holds: True

# Three pairs from two three-element sets -- and had one
# set been shorter, the golden rule from section [2]
# would cut it the same way. Sorting makes the printout
# permanent; zip's behavior underneath is unchanged.

# ============================================================
# [11] The best practice: parallel sources [07:20]
# ============================================================
# The transcript's verdict: zip is the way to read data
# coming from several sources AT THE SAME MOMENT --
# compare, print, or validate without nested loops.
# Three "sources" (lists from three places), one pass:

ids = [101, 102, 103]
cities = ["Amman", "Cairo", "Doha"]
active = [True, False, True]

records = list(zip(ids, cities, active))
matched = [r for r in records if r[2]]

print(f"  total records: {len(records)}")
print(f"  active records: {matched}")
print(f"  all rows aligned: {all(len(r) == 3 for r in records)}")
#   total records: 3
#   active records: [(101, 'Amman', True), (103, 'Doha', True)]
#   all rows aligned: True

# One pass, one condition, zero nested loops -- the
# comparison the transcript promises (مقارنة أو قراءة
# البيانات من عدة مصادر في نفس اللحظة) in six lines.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- pairing, the
# golden rule, the three-list loop, dict rebuilding, and
# the round trip:

print(f"  pairs: {list(zip(letters, marks))}")
print(f"  shortest cut: {len(list(zip(long_list, short_list)))}")
for num, name, skill in zip(nums, names, skills):
    print(f"  row: {num} {name} {skill}")
print(f"  rebuilt dict: {dict(zip(keys, values))}")
print(f"  unzip round trip: {list(zip(*pairs))}")
print(f"  index way == zip way: {old_school == new_school}")
#   pairs: [('a', 1), ('b', 2), ('c', 3)]
#   shortest cut: 3
#   row: 1 Osama Python
#   row: 2 Mona JavaScript
#   row: 3 Ali SQL
#   rebuilt dict: {'x': 10, 'y': 20, 'z': 30}
#   unzip round trip: [(1, 2, 3), ('a', 'b', 'c')]
#   index way == zip way: True

# Pairing, cutting at the shortest, one-loop rows, dict
# rebuilding, columns falling out of zip(*), and the old
# way surrendered to the new -- zip() end to end.

# ============================================================
# [13] The summary
# ============================================================
# zip(), from the transcript, complete:
#
#   1. THE IDEA [00:13] -- zip() takes several iterables
#      (lists, tuples, dicts, sets...), merges elements
#      that face each other in matching order into
#      TUPLES, and makes them walkable in ONE for loop
#   2. THE GOLDEN RULE [00:20] -- it stops at the
#      SHORTEST iterable: 10 elements vs 3 -> 3 pairs,
#      the rest ignored (produced 3 pairs -> True);
#      no error, no padding -- the short list ends the
#      show
#   3. IT IS AN ITERATOR -- next() yields one pair at a
#      time: ('a', 1), ('b', 2), ('c', 3); drained zips
#      stay drained (lesson 81's rule)
#   4. THE PRACTICAL [01:07] -- for num, name, skill in
#      zip(nums, names, skills): three lists, ONE loop
#      header, three variables per row (1. Osama ->
#      Python, etc.); no range(), no len(), no [i]
#   5. UNPACKING IS REAL -- a row is a tuple of len 3;
#      `for a, b, c in ...` is plain tuple unpacking
#      applied to zip's output
#   6. INDEX MACHINERY RETIRED -- range(len()) + [i]
#      produces byte-identical rows to zip (both agree:
#      True) with a third of the code; the loop count
#      lives in the shortest list, not in your head
#   7. DICT REBUILDING [02:10] -- dict(zip(keys,
#      values)) snaps two lists into
#      {'x': 10, 'y': 20, 'z': 30} (equals original ->
#      True): keys and values from two sources, one
#      clean structure
#   8. DICT INTERNALS -- zip(dict, dict.values()) pairs
#      every key with its value and matches list(items())
#      exactly: iterating a dict yields its keys, so the
#      two roads meet
#   9. UNZIPPING -- zip(*pairs) with * unpacks the rows:
#      [(1, 'a'), (2, 'b')] -> columns (1, 2) and
#      ('a', 'b'); round trip back to the pairs -> True
#  10. SETS -- iterables too, but their screen order is
#       not guaranteed, so pairs are sorted before
#       printing: [(1, 4), (2, 5), (3, 6)]; the shortest
#       rule still applies (min length -> True)
#  11. BEST PRACTICE [07:20] -- reading several parallel
#       sources in one pass (ids + cities + active ->
#       records, filter active -> 2 matches, all rows
#       aligned True) is the professional case for zip:
#       no nested loops, no index bookkeeping
#  12. THE DISCIPLINE -- every printed pair comes from
#       fixed sources; set pairs are sorted; no addresses,
#       no clock -- byte-stable on every run
#
# Several lists enter; one aligned stream of tuples
# leaves; the shortest list holds the scissors.
