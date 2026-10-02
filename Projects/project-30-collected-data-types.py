# ============================================================
# PROJECT 30 - Collected Data Types (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01-32, plus the for loop from 47-51)
# Topics: All previous + choosing between list, tuple, set and
#        dict, hashable vs unhashable, converting between them,
#        and nested shapes (list of dicts, dict of lists)
#
# By project 29 you have used each of the four collection types on
# its own. Real code uses two or three of them TOGETHER, and the
# skill this project builds is choosing which one to reach for.
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: the one-line difference
# In your own words, what is the single difference that
# separates a tuple from a list? Prove your answer with code.
# (your answer here)

# QUESTION 2: duplicates
# I have [1, 1, 2, 2, 3]. Which of the four types keeps the
# duplicates, and which one throws them away automatically?
# (your answer here)

# QUESTION 3: hashable
# I want to use a list as a key in a dictionary. What error do I
# get, and what is the ONE property that decides whether a type
# can be a key?
# (your answer here)

# QUESTION 4: the order of a set
# I do set([3, 1, 2]) and print it. Will I always see [3, 1, 2]?
# What should I write instead when I want a readable print?
# (your answer here)

# QUESTION 5: the membership test
# The "in" operator works on all four types. What does it
# actually look for in a DICTIONARY, and why is that different
# from the other three?
# (your answer here)

# QUESTION 6: converting
# Write the one line that turns a list into a dict, and say what
# the list has to look like first.
# (your answer here)

# QUESTION 7: which shape
# I have many students, and each one has a name, an age and a
# city. Is a list of dicts or a dict of lists the better shape,
# and why?
# (your answer here)

# QUESTION 8: the reverse trap
# I build seen = set() to track duplicates, which is faster than a
# list. What do I LOSE by throwing the order away, and what do I
# have to add to get it back for printing?
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Take data = [3, 1, 3, 2, 1]. Print it as a list, as a
# tuple, as a set (sorted), and as a dict mapping each value to
# the position where it was LAST found. Print the length of each
# and explain in a comment why they are all different
# (your code here)

# TASK 2: Prove the tuple is immutable and the list is not. Try to
# change element 0 of each one, catch the TypeError for the tuple,
# and show that the list change worked
# (your code here)

# TASK 3: Try to use a list as a dict key, then a tuple as a dict
# key, then a dict as a dict key. Catch every TypeError and print
# which ones are allowed. Then prove that a frozenset works too
# (your code here)

# TASK 4: Start from nums = [3, 1, 3, 2, 1] and convert it five
# ways: to a set, to a tuple, from a set back to a list, and a
# list of (key, value) pairs into a dict, and a dict back into a
# list of its keys. Print every result
# (your code here)

# TASK 5: Build people = [{"name": "Omar", "age": 21}, {"name":
# "Mona", "age": 19}, {"name": "Ali", "age": 30}]. Loop with for
# and print each person's line, then build a list of just the
# names and print the average age to two decimals
# (your code here)

# TASK 6: Build groups = {"A": ["Omar", "Mona"], "B": ["Ali",
# "Sayed"]}. Print each group with its size, then collect EVERY
# member from EVERY group into one sorted list using a for loop
# nested inside another for loop
# (your code here)

# TASK 7: Loop over [1, 1, 2, 3, 3] twice. The first time use a
# list and the "if not in" check to collect unique values, the
# second time use a set with add(). Print both and explain the
# difference in how the work is done
# (your code here)

# TASK 8: Build records = [{"name": "Omar", "tag": "python"},
# {"name": "Mona", "tag": "python"}, {"name": "Ali", "tag":
# "web"}, {"name": "Sayed", "tag": "python"}]. Print every tag in
# order, print the unique tags sorted, then build a dict of
# tag -> how many records carry it, sorted by tag
# (your code here)

# TASK 9: Write a duplicate finder. Define
#   find_duplicates(items) -> the values that appear MORE THAN
#                            ONCE, sorted, as a LIST
# Test it on a list WITH duplicates and on one without, and on a
# list where EVERY value is duplicated
# (your code here)

# TASK 10: Write first_seen(records) where records is a list of
# dicts with a "name" key. It returns a TUPLE of the names in the
# order they first appeared, with no repeats. Explain in a comment
# why the return type is a tuple and not a set
# (your code here)

# TASK 11: Build a tiny library index. Use a dict of lists for the
# shelves, and a set for the borrowed books. Write and use:
#   lend(index, borrowed, book)   -> adds it if it is not already
#                                   borrowed, returns "lent" or
#                                   "already out"
#   return_book(borrowed, book)   -> removes it safely
#   available(index, borrowed)    -> a sorted list of the books
#                                   that are still on the shelf
# Lend two, try to lend a duplicate, return one, then print what
# is still available
# (your code here)

# TASK 12: Build a summary report function. Define
#   summarize(records) -> a tuple of THREE things:
#        (number_of_records, sorted_unique_tags, oldest_name)
# It must NOT modify the list it receives. Test it on two
# different lists and print every part of the result
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
print("Q1  a tuple cannot be changed after it is created:")
t = (1, 2, 3)
try:
    t[0] = 99
except TypeError as err:
    print("Q1  tuple[0] = 99 -> TypeError:", err)
l = [1, 2, 3]
l[0] = 99
print("Q1  list[0] = 99  -> worked, now", l)
# Q1  a tuple cannot be changed after it is created:
# Q1  tuple[0] = 99 -> TypeError: 'tuple' object does not support item assignment
# Q1  list[0] = 99  -> worked, now [99, 2, 3]

# QUESTION 2
print("Q2  len([1, 1, 2, 2, 3]) ->", len([1, 1, 2, 2, 3]), "(the list keeps them)")
print("Q2  len({1, 1, 2, 2, 3}) ->", len({1, 1, 2, 2, 3}), "(the set drops them)")
# Q2  len([1, 1, 2, 2, 3]) -> 5 (the list keeps them)
# Q2  len({1, 1, 2, 2, 3}) -> 3 (the set drops them)

# QUESTION 3
try:
    {[1, 2]: "a"}
except TypeError as err:
    print("Q3  a list as a key -> TypeError:", err)
print("Q3  so the deciding property is: can this type be CHANGED?")
print("Q3  mutable -> unhashable, immutable -> hashable")
# Q3  a list as a key -> TypeError: unhashable type: 'list'
# Q3  so the deciding property is: can this type be CHANGED?
# Q3  mutable -> unhashable, immutable -> hashable

# QUESTION 4
print("Q4  set([3, 1, 2]) ->", set([3, 1, 2]), "(sorted here, but not guaranteed)")
print("Q4  for a stable print use ->", "sorted(set([3, 1, 2]))")
# Q4  set([3, 1, 2]) -> {1, 2, 3} (sorted here, but not guaranteed)
# Q4  for a stable print use -> sorted(set([3, 1, 2]))

# QUESTION 5
print("Q5  2 in [1, 2, 3] ->", 2 in [1, 2, 3], "(looking for a VALUE)")
print("Q5  2 in {'a': 1} ->", 2 in {"a": 1}, "(looking for a KEY, and 2 is not one)")
# Q5  2 in [1, 2, 3] -> True (looking for a VALUE)
# Q5  2 in {'a': 1} -> False (looking for a KEY, and 2 is not one)

# QUESTION 6
print("Q6  list of pairs -> dict ->", dict([("a", 1), ("b", 2)]))
# Q6  list of pairs -> dict -> {'a': 1, 'b': 2}

# QUESTION 7
print("Q7  many students, many fields each -> a LIST of dicts.")
print("Q7  reason: the number of students changes, and each one")
print("Q7  carries its own fields. A dict keyed by name would also")
print("Q7  work, but only if the names are guaranteed unique.")
# Q7  many students, many fields each -> a LIST of dicts.
# Q7  reason: the number of students changes, and each one
# Q7  carries its own fields. A dict keyed by name would also
# Q7  work, but only if the names are guaranteed unique.

# QUESTION 8
print("Q8  what you lose with a set -> the ORDER you first saw them in.")
print("Q8  what you add back     -> sorted(), or a list of the keys.")
# Q8  what you lose with a set -> the ORDER you first saw them in.
# Q8  what you add back     -> sorted(), or a list of the keys.

print("-" * 60)

# TASK 1
data = [3, 1, 3, 2, 1]
positions = {}
for index, value in enumerate(data):
    positions[value] = index
print("T1  as a list       ->", data, "| length", len(data))
print("T1  as a tuple      ->", tuple(data), "| length", len(tuple(data)))
print("T1  as a set        ->", sorted(set(data)), "| length", len(set(data)))
print("T1  as a dict       ->", positions, "| length", len(positions))
# T1  as a list       -> [3, 1, 3, 2, 1] | length 5
# T1  as a tuple      -> (3, 1, 3, 2, 1) | length 5
# T1  as a set        -> [1, 2, 3] | length 3
# T1  as a dict       -> {3: 2, 1: 4, 2: 3} | length 3
# The list and the tuple keep the 3 twice. The set cannot, and the
# dict cannot either, because a dict key must be unique.

# TASK 2
t = (1, 2, 3)
try:
    t[0] = 99
except TypeError as err:
    print("T2  tuple is immutable -> TypeError:", err)
l = [1, 2, 3]
l[0] = 99
print("T2  list is mutable    ->", l, "changed with no error")
# T2  tuple is immutable -> TypeError: 'tuple' object does not support item assignment
# T2  list is mutable    -> [99, 2, 3] changed with no error

# TASK 3
try:
    {[1, 2]: "a"}
except TypeError as err:
    print("T3  a list as a key   -> TypeError:", err)
print("T3  a tuple as a key  ->", {(1, 2): "a"}, "allowed")
try:
    {{"x": 1}: "a"}
except TypeError as err:
    print("T3  a dict as a key   -> TypeError:", err)
print("T3  frozenset as a key->", {frozenset([1, 2]): "a"}, "allowed")
# T3  a list as a key   -> TypeError: unhashable type: 'list'
# T3  a tuple as a key  -> {(1, 2): 'a'} allowed
# T3  a dict as a key   -> TypeError: unhashable type: 'dict'
# T3  frozenset as a key-> {frozenset({1, 2}): 'a'} allowed
# The list and the dict can change, so Python refuses to hash
# them. The tuple and the frozenset cannot change, so they are
# safe to use as keys.

# TASK 4
nums = [3, 1, 3, 2, 1]
print("T4  list -> set        ->", sorted(set(nums)))
print("T4  list -> tuple      ->", tuple(nums))
print("T4  set  -> list       ->", sorted(list(set(nums))))
print("T4  pairs -> dict      ->", dict([("a", 1), ("b", 2)]))
print("T4  dict -> its keys   ->", sorted({"a": 1, "b": 2}.keys()))
# T4  list -> set        -> [1, 2, 3]
# T4  list -> tuple      -> (3, 1, 3, 2, 1)
# T4  set  -> list       -> [1, 2, 3]
# T4  pairs -> dict      -> {'a': 1, 'b': 2}
# T4  dict -> its keys   -> ['a', 'b']

# TASK 5
people = [
    {"name": "Omar", "age": 21},
    {"name": "Mona", "age": 19},
    {"name": "Ali", "age": 30},
]
for person in people:
    print(f"T5  {person['name']} is {person['age']}")
names = [p["name"] for p in people]
ages = [p["age"] for p in people]
print("T5  the names  ->", names)
print("T5  the ages   ->", ages, "| average", round(sum(ages) / len(ages), 2))
# T5  Omar is 21
# T5  Mona is 19
# T5  Ali is 30
# T5  the names  -> ['Omar', 'Mona', 'Ali']
# T5  the ages   -> [21, 19, 30] | average 23.33

# TASK 6
groups = {"A": ["Omar", "Mona"], "B": ["Ali", "Sayed"]}
for group, members in groups.items():
    print(f"T6  group {group} has {len(members)}: {members}")
everyone = []
for members in groups.values():
    for member in members:
        everyone.append(member)
print("T6  every member ->", sorted(everyone), "| total", len(everyone))
# T6  group A has 2: ['Omar', 'Mona']
# T6  group B has 2: ['Ali', 'Sayed']
# T6  every member -> ['Ali', 'Mona', 'Omar', 'Sayed'] | total 4

# TASK 7
items = [1, 1, 2, 3, 3]
seen_list = []
for item in items:
    if item not in seen_list:
        seen_list.append(item)
seen_set = set()
for item in items:
    seen_set.add(item)
print("T7  with a list ->", seen_list, "| length", len(seen_list))
print("T7  with a set  ->", sorted(seen_set), "| length", len(seen_set))
# T7  with a list -> [1, 2, 3] | length 3
# T7  with a set  -> [1, 2, 3] | length 3
# The list version must ASK "is it in there?" on every item, and
# that check walks the list. The set version never asks, because
# add() cannot store the same value twice. The list also happens
# to keep the original order, which the set threw away.

# TASK 8
records = [
    {"name": "Omar", "tag": "python"},
    {"name": "Mona", "tag": "python"},
    {"name": "Ali", "tag": "web"},
    {"name": "Sayed", "tag": "python"},
]
tags = [r["tag"] for r in records]
unique_tags = sorted(set(tags))
per_tag = {}
for tag in unique_tags:
    per_tag[tag] = tags.count(tag)
print("T8  every tag in order ->", tags)
print("T8  the unique ones    ->", unique_tags)
print("T8  how many each      ->", per_tag)
# T8  every tag in order -> ['python', 'python', 'web', 'python']
# T8  the unique ones    -> ['python', 'web']
# T8  how many each      -> {'python': 3, 'web': 1}
# The list kept all three "python" entries, the set reduced them to
# one name, and the dict turned each name into a number.

# TASK 9
def find_duplicates(items):
    """Return the values that appear more than once, sorted."""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    repeated = []
    for item in sorted(counts):
        if counts[item] > 1:
            repeated.append(item)
    return repeated

print("T9  with duplicates      ->", find_duplicates([1, 2, 2, 3, 3, 3]))
print("T9  without duplicates   ->", find_duplicates([1, 2, 3]))
print("T9  everything repeated  ->", find_duplicates([5, 5, 5]))
# T9  with duplicates      -> [2, 3]
# T9  without duplicates   -> []
# T9  everything repeated  -> [5]
# Note the return is a LIST, not a set, because the caller asked
# for a sorted result and a set would not keep the order.

# TASK 10
def first_seen(records):
    """Return the names in first-appearance order, without repeats."""
    names = []
    for record in records:
        name = record["name"]
        if name not in names:
            names.append(name)
    return tuple(names)

test_records = [
    {"name": "Omar"},
    {"name": "Mona"},
    {"name": "Omar"},
    {"name": "Ali"},
]
print("T10 the result   ->", first_seen(test_records))
print("T10 the type     ->", type(first_seen(test_records)).__name__)
# T10 the result   -> ('Omar', 'Mona', 'Ali')
# T10 the type     -> tuple
# A set would give the same three names but in NO order, which is
# the one thing this function exists to preserve. A tuple cannot
# be changed by the caller, so the result stays trustworthy.

# TASK 11
def lend(index, borrowed, book):
    """Move a book to the borrowed set, unless it is already out."""
    if book in borrowed:
        return "already out"
    borrowed.add(book)
    return "lent"

def return_book(borrowed, book):
    """Put a book back, safely, even if it was never borrowed."""
    if book in borrowed:
        borrowed.remove(book)
        return "returned"
    return "was not borrowed"

def available(index, borrowed):
    """Sorted list of the books still on the shelf."""
    on_shelf = []
    for shelf_books in index.values():
        for book in shelf_books:
            if book not in borrowed:
                on_shelf.append(book)
    return sorted(on_shelf)

index = {"fiction": ["dune", "solaris"], "tech": ["python", "git"]}
borrowed = set()
print("T11 lend dune      ->", lend(index, borrowed, "dune"))
print("T11 lend python    ->", lend(index, borrowed, "python"))
print("T11 lend dune again->", lend(index, borrowed, "dune"))
print("T11 borrowed now   ->", sorted(borrowed))
print("T11 return dune    ->", return_book(borrowed, "dune"))
print("T11 return ghost   ->", return_book(borrowed, "ghost"), "(no error)")
print("T11 available now  ->", available(index, borrowed))
# T11 lend dune      -> lent
# T11 lend python    -> lent
# T11 lend dune again-> already out
# T11 borrowed now   -> ['dune', 'python']
# T11 return dune    -> returned
# T11 return ghost   -> was not borrowed (no error)
# T11 available now  -> ['dune', 'git', 'solaris']
# "dune" is on the list again because we returned it above, so only
# "python" is still out. "ghost" was never borrowed, so remove()
# was never called and nothing could crash.
# The set answers "is it already out?" in one step, which is the
# whole reason for storing borrowed books in a set and not a list.

# TASK 12
def summarize(records):
    """Return (how many, the sorted unique tags, the oldest name)."""
    tags = []
    for record in records:
        tags.append(record["tag"])
    unique_tags = tuple(sorted(set(tags)))
    oldest_name = ""
    oldest_age = -1
    for record in records:
        if record["age"] > oldest_age:
            oldest_age = record["age"]
            oldest_name = record["name"]
    return (len(records), unique_tags, oldest_name)

batch_one = [
    {"name": "Omar", "tag": "python", "age": 21},
    {"name": "Mona", "tag": "web", "age": 30},
    {"name": "Ali", "tag": "python", "age": 25},
]
batch_two = [
    {"name": "Sayed", "tag": "web", "age": 44},
]
result_one = summarize(batch_one)
result_two = summarize(batch_two)
print("T12 batch one count ->", result_one[0])
print("T12 batch one tags  ->", result_one[1])
print("T12 batch one oldest->", result_one[2])
print("T12 batch two count ->", result_two[0])
print("T12 batch two tags  ->", result_two[1])
print("T12 batch two oldest->", result_two[2])
print("T12 batch one after ->", len(batch_one), "records, untouched")
# T12 batch one count -> 3
# T12 batch one tags  -> ('python', 'web')
# T12 batch one oldest-> Mona
# T12 batch two count -> 1
# T12 batch two tags  -> ('web',)
# T12 batch two oldest-> Sayed
# T12 batch one after -> 3 records, untouched
# summarize() only READS the list it was given, so calling it twice
# is safe. The result is a tuple because the three parts belong
# together and must not be changed by accident.

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 30")
print("=" * 60)
# ============================================================
# END OF PROJECT 30
# ============================================================
