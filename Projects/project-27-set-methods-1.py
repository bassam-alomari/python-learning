# ============================================================
# PROJECT 27 - Set Methods Part 1 (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01-27)
# Topics: All previous + Set Methods (union, add, copy, remove,
#        discard, pop, update)
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: union() (Lesson 27)
# What does group_a.union(group_b) return? Does it MODIFY group_a,
# or does it build a new Set?
# (your answer here)

# QUESTION 2: the | operator (Lesson 27)
# Is a.union(b) exactly the same as a | b ? If yes, which one do
# you prefer to read, and why?
# (your answer here)

# QUESTION 3: add() (Lesson 27)
# What happens when you add an item that is ALREADY in the Set?
# Does the length go up? Is add() in place or does it return a
# new Set?
# (your answer here)

# QUESTION 4: copy() (Lesson 27)
# What does copy() return? If you add something to the copy, does
# the original change?
# (your answer here)

# QUESTION 5: remove() (Lesson 27)
# What error does remove() raise when the item is NOT in the Set?
# Give the exact name of the error.
# (your answer here)

# QUESTION 6: discard() (Lesson 27)
# What does discard() do when the item is NOT in the Set? How is
# that different from remove()?
# (your answer here)

# QUESTION 7: pop() (Lesson 27)
# Does pop() tell you WHICH item it removed? Why not? And does it
# GIVE you the item it removed?
# (your answer here)

# QUESTION 8: update() (Lesson 27)
# What kinds of values can update() accept? Is it in place or does
# it return a new Set?
# (your answer here)

# QUESTION 9: remove() or discard()? (Lesson 27)
# When would you choose remove() and when would you choose
# discard()? Which one should you use in code that must never
# crash?
# (your answer here)


# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Create group_a = {1, 2, 3, 4} and group_b = {3, 4, 5, 6},
# join them with union(), and print the result with sorted() plus
# the length of each original group
# (your code here)

# TASK 2: Do TASK 1 again but with the | operator instead, then
# print group_a AFTER the join to prove it was not modified
# (your code here)

# TASK 3: Create numbers = {10, 20}, add 30, then add 10 AGAIN.
# Print the Set and its length after each step, and explain in a
# comment why the second add() changed nothing
# (your code here)

# TASK 4: Create original = {5, 6, 7}, make cloned = original.copy(),
# add 99 to the clone, then print BOTH Sets and explain which one
# changed
# (your code here)

# TASK 5: Create colors = {"red", "green", "blue"}. Remove "green"
# (it exists), then try to remove "yellow" (it does NOT exist) and
# catch the KeyError with try/except
# (your code here)

# TASK 6: Do TASK 5 again but with discard() for the missing item,
# then explain in a comment why discard() needs no try/except
# (your code here)

# TASK 7: Create snacks = {"chips", "nuts", "juice"}, call pop(),
# store the result in a variable, then print that variable, the
# length of the Set before and after, and the remaining items with
# sorted(). Remember: you cannot know WHICH item pop() removes.
# (your code here)

# TASK 8: Create nums = {1, 2}, call update() with the LIST [3, 4, 5],
# then call update() again with the SET {10, 20}, printing after
# each call
# (your code here)

# TASK 9: Write safe_toggle(target, item) that REMOVES the item if
# it is inside target, otherwise ADDS it, and returns "removed" or
# "added". Test it with a present item and with a missing item.
# (your code here)

# TASK 10: Write three functions for an article tag system:
#   add_tag(tags, tag)    -> adds it only if it is not there
#   remove_tag(tags, tag) -> removes it safely, no error if missing
#   toggle_tag(tags, tag) -> adds it, or removes it if it is there
# Test all three and print the tags with sorted() after each call
# (your code here)

# TASK 11: Two classes share some students:
#         class_a = {"Omar", "Sayed", "Mona"}
#         class_b = {"Mona", "Ali", "Omar"}
# Using union(), print: how many SEATS there are in total, how many
# UNIQUE students there are, and how many students are in BOTH
# classes (found with count, not with the & operator yet)
# (your code here)

# TASK 12: Build a tiny guest list app. You have a Set called
#         guests, use add() to invite three people, use discard() to
#         cancel one who cannot come, use pop() when a guest arrives
#         early and no longer needs a seat, then print the final
#         guest list with sorted() and its length
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.
#
# IMPORTANT: a Set has NO order, so we never rely on the order of a
# printed Set. We use sorted() and len() instead.

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
group_a = {1, 2, 3, 4}
group_b = {3, 4, 5, 6}
combined = group_a.union(group_b)
print("Q1  union() result          ->", sorted(combined))
print("Q1  group_a AFTER the union ->", sorted(group_a), "(untouched)")
# Q1  union() result          -> [1, 2, 3, 4, 5, 6]
# Q1  group_a AFTER the union -> [1, 2, 3, 4] (untouched)

# QUESTION 2
print("Q2  a | b                   ->", sorted(group_a | group_b))
print("Q2  a.union(b) == a | b     ->", group_a.union(group_b) == (group_a | group_b))
# Q2  a | b                   -> [1, 2, 3, 4, 5, 6]
# Q2  a.union(b) == a | b     -> True

# QUESTION 3
numbers = {10, 20}
numbers.add(30)
print("Q3  after add(30)           ->", sorted(numbers), "length", len(numbers))
numbers.add(10)
print("Q3  after add(10) again     ->", sorted(numbers), "length", len(numbers))
# Q3  after add(30)           -> [10, 20, 30] length 3
# Q3  after add(10) again     -> [10, 20, 30] length 3

# QUESTION 4
original = {5, 6, 7}
cloned = original.copy()
cloned.add(99)
print("Q4  the clone               ->", sorted(cloned))
print("Q4  the original            ->", sorted(original))
print("Q4  same object?            ->", original is cloned)
# Q4  the clone               -> [5, 6, 7, 99]
# Q4  the original            -> [5, 6, 7]
# Q4  same object?            -> False

# QUESTION 5
colors = {"red", "green", "blue"}
colors.remove("green")
print("Q5  after remove('green')   ->", sorted(colors))
try:
    colors.remove("yellow")
except KeyError as err:
    print("Q5  remove('yellow') raised ->", type(err).__name__, "->", err)
# Q5  after remove('green')   -> ['blue', 'red']
# Q5  remove('yellow') raised -> KeyError -> 'yellow'

# QUESTION 6
colors.discard("yellow")
print("Q6  discard('yellow')       -> no error, sorted:", sorted(colors))
print("Q6  the length              ->", len(colors))
# Q6  discard('yellow')       -> no error, sorted: ['blue', 'red']
# Q6  the length              -> 2

# QUESTION 7
snacks = {"chips", "nuts", "juice"}
print("Q7  the length BEFORE pop() ->", len(snacks))
popped = snacks.pop()
print("Q7  pop() GAVE back          ->", repr(popped), "(WHICH ONE IS ARBITRARY)")
print("Q7  the length AFTER pop()  ->", len(snacks))
print("Q7  what is left, sorted     ->", sorted(snacks))
# Q7  the length BEFORE pop() -> 3
# Q7  pop() GAVE back          -> one of the three strings. Which one
#                                depends on your Python version, so
#                                do NOT compare it with the sheet.
# Q7  the length AFTER pop()  -> 2
# Q7  what is left, sorted     -> the other two strings

# QUESTION 8
nums = {1, 2}
nums.update([3, 4, 5])
print("Q8  after update([3, 4, 5]) ->", sorted(nums))
nums.update({10, 20})
print("Q8  after update({10, 20})  ->", sorted(nums))
# Q8  after update([3, 4, 5]) -> [1, 2, 3, 4, 5]
# Q8  after update({10, 20})  -> [1, 2, 3, 4, 5, 10, 20]

# QUESTION 9
print("Q9  use discard() in code that must never crash")
print("Q9  use remove() when a missing item is a real bug")
# Q9  use discard() in code that must never crash
# Q9  use remove() when a missing item is a real bug

# ------------------------------------------------------------
print("-" * 60)

# TASK 3
n = {10, 20}
n.add(30)
print("T3  after add(30)           ->", sorted(n), "| length", len(n))
n.add(10)
print("T3  after add(10) again     ->", sorted(n), "| length", len(n))
# T3  after add(30)           -> [10, 20, 30] | length 3
# T3  after add(10) again     -> [10, 20, 30] | length 3

# TASK 4
o = {5, 6, 7}
c = o.copy()
c.add(99)
print("T4  original ->", sorted(o), "| clone ->", sorted(c))
# T4  original -> [5, 6, 7] | clone -> [5, 6, 7, 99]

# TASK 5
colors5 = {"red", "green", "blue"}
colors5.remove("green")
print("T5  after remove('green')   ->", sorted(colors5))
try:
    colors5.remove("yellow")
except KeyError as err:
    print("T5  remove('yellow')       -> KeyError:", err)
# T5  after remove('green')   -> ['blue', 'red']
# T5  remove('yellow')       -> KeyError: 'yellow'

# TASK 6
colors6 = {"red", "green", "blue"}
colors6.discard("yellow")
print("T6  discard a missing item -> no error:", sorted(colors6))
# T6  discard a missing item -> no error: ['blue', 'green', 'red']

# TASK 7
snacks7 = {"chips", "nuts", "juice"}
before = len(snacks7)
popped7 = snacks7.pop()
print("T7  before ->", before, "| popped ->", repr(popped7), "| after ->", len(snacks7))
print("T7  the remaining two, sorted ->", sorted(snacks7))
# T7  before -> 3 | popped -> one of the three, WHICH ONE IS
#                          ARBITRARY | after -> 2
# T7  the remaining two, sorted -> the other two items

# TASK 8
nums8 = {1, 2}
nums8.update([3, 4, 5])
print("T8  after update([3,4,5])  ->", sorted(nums8))
nums8.update({10, 20})
print("T8  after update({10,20})  ->", sorted(nums8))
# T8  after update([3,4,5])  -> [1, 2, 3, 4, 5]
# T8  after update({10,20})  -> [1, 2, 3, 4, 5, 10, 20]

# TASK 9
def safe_toggle(target, item):
    """If the item is present remove it, otherwise add it."""
    if item in target:
        target.discard(item)
        return "removed"
    target.add(item)
    return "added"


flags = {"A", "B"}
print("T9  toggle 'B' (it is inside) ->", safe_toggle(flags, "B"))
print("T9  toggle 'Z' (it is missing)->", safe_toggle(flags, "Z"))
print("T9  flags now ->", sorted(flags))
# T9  toggle 'B' (it is inside) -> removed
# T9  toggle 'Z' (it is missing)-> added
# T9  flags now -> ['A', 'Z']

# TASK 10
def add_tag(tags, tag):
    if tag not in tags:
        tags.add(tag)
        return "added"
    return "already there"


def remove_tag(tags, tag):
    if tag in tags:
        tags.discard(tag)
        return "removed"
    return "was not there"


def toggle_tag(tags, tag):
    # CAREFUL: returning the word "removed" is NOT enough, we must
    # ACTUALLY call discard(). A function that only reports and does
    # not do the job is the worst kind of bug, because it looks right.
    if tag in tags:
        tags.discard(tag)
        return "removed"
    tags.add(tag)
    return "added"


article = {"python", "beginner"}
print("T10 the article starts as ->", sorted(article))
print("T10 toggle 'python'  ->", toggle_tag(article, "python"), "->", sorted(article))
print("T10 toggle 'data'    ->", toggle_tag(article, "data"), "->", sorted(article))
print("T10 remove 'missing' ->", remove_tag(article, "nope"), "->", sorted(article))
print("T10 add 'python'     ->", add_tag(article, "python"), "->", sorted(article))
# T10 the article starts as -> ['beginner', 'python']
# T10 toggle 'python'  -> removed -> ['beginner']
# T10 toggle 'data'    -> added -> ['beginner', 'data']
# T10 remove 'missing' -> was not there -> ['beginner', 'data']
# T10 add 'python'     -> added -> ['beginner', 'data', 'python']

# TASK 11
class_a = {"Omar", "Sayed", "Mona"}
class_b = {"Mona", "Ali", "Omar"}
everyone = class_a.union(class_b)
seats = len(class_a) + len(class_b)
in_both = sum(1 for student in class_a if student in class_b)
print("T11 total seats          ->", seats)
print("T11 unique students      ->", len(everyone))
print("T11 in BOTH classes      ->", in_both)
print("T11 the shared names     ->", sorted(class_a & class_b))
# T11 total seats          -> 6
# T11 unique students      -> 4
# T11 in BOTH classes      -> 2
# T11 the shared names     -> ['Mona', 'Omar']

# TASK 12
guests = set()
for guest in ["Omar", "Sayed", "Mona"]:
    guests.add(guest)
print("T12 after three add()      ->", sorted(guests))
guests.discard("Mona")
print("T12 after discard('Mona')  ->", sorted(guests))
arrived_early = guests.pop()
print("T12 pop() freed a seat for ->", repr(arrived_early), "(we cannot choose which)")
print("T12 the final guest list   ->", sorted(guests), "| length", len(guests))
# T12 after three add()      -> ['Mona', 'Omar', 'Sayed']
# T12 after discard('Mona')  -> ['Omar', 'Sayed']
# T12 pop() freed a seat for -> one of 'Omar' or 'Sayed', randomly
# T12 the final guest list   -> the other one | length 1

# ============================================================
# END OF PROJECT 27
# ============================================================