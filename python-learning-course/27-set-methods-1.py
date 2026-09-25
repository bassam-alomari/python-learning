# -----------------------------------------------------------------
# Lesson 27: Set Methods Part 1
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : set methods - union, add, copy, remove, discard, pop, update
# Type     : Educational + Practical
# Builder  : local assistant (safe rewrite, no broken chars)
# -----------------------------------------------------------------
# In this lesson we use the built-in methods that a set object gives us.
# A set is already a powerful unordered collection with unique items,
# and its methods let us modify it and combine it with other sets.

# ============================================================
# [1] union()  or  the | operator  -> combine two sets
# ============================================================
# union returns a NEW set that has all items from both sets.
# Duplicated items appear only once.

group_a = {1, 2, 3, 4}
group_b = {3, 4, 5, 6}

combined = group_a.union(group_b)
print("union():", combined)
# union(): {1, 2, 3, 4, 5, 6}

combined_pipe = group_a | group_b
print("pipe |  :", combined_pipe)
# pipe |  : {1, 2, 3, 4, 5, 6}

# The original sets did NOT change.
print("group_a after union:", group_a)
# group_a after union: {1, 2, 3, 4}

# ============================================================
# [2] add()  -> add ONE item to the set (in place)
# ============================================================
numbers = {10, 20}
numbers.add(30)
print("after add(30):", numbers)
# after add(30): {10, 20, 30}

# Adding an existing item changes nothing.
numbers.add(10)
print("after add(10) again:", numbers)
# after add(10) again: {10, 20, 30}

# ============================================================
# [3] copy()  -> return a shallow copy of the set
# ============================================================
original = {5, 6, 7}
cloned = original.copy()
print("cloned:", cloned)
# cloned: {5, 6, 7}

# Changing the clone does not touch the original.
cloned.add(99)
print("original untouched:", original)
# original untouched: {5, 6, 7}

# ============================================================
# [4] remove() vs discard()  -> delete an item
# ============================================================
# remove() raises KeyError when the item does NOT exist.
# discard() silently does NOTHING when the item does NOT exist.

colors = {"red", "green", "blue"}

# remove an existing item -> OK
colors.remove("green")
print("after remove(green):", colors)
# after remove(green): {'red', 'blue'}

# discard an existing item -> OK
colors.discard("blue")
print("after discard(blue):", colors)
# after discard(blue): {'red'}

# discard a MISSING item -> no error, nothing happens
colors.discard("yellow")
print("after discard(missing yellow):", colors)
# after discard(missing yellow): {'red'}

# remove a MISSING item -> KeyError (we catch it to keep the script clean)
try:
    colors.remove("yellow")
except KeyError as err:
    print("remove() raised:", err)
# remove() raised: 'yellow'

# ============================================================
# [5] pop()  -> remove and return an ARBITRARY item
# ============================================================
# Sets are unordered, so pop() cannot tell us WHICH item comes out.
snacks = {"chips", "nuts", "juice"}
popped = snacks.pop()
print("popped:", popped)
print("set after pop():", snacks)
# popped: (any one of the three)
# set after pop(): (the remaining two)

# ============================================================
# [6] update()  -> add MANY items from an iterable (in place)
# ============================================================
nums = {1, 2}
nums.update([3, 4, 5])
print("after update([3,4,5]):", nums)
# after update([3, 4, 5]): {1, 2, 3, 4, 5}

# update also accepts another set.
nums.update({10, 20})
print("after update({10,20}):", nums)
# after update({10, 20}): {1, 2, 3, 4, 5, 10, 20}

# ============================================================
# Improvement (from me): safe membership-checked modification
# ============================================================
# Instead of guessing, always check membership BEFORE removing,
# and prefer discard() when the item may already be absent.
def safe_toggle(target, item):
    """If the item is present -> remove it, otherwise -> add it."""
    if item in target:
        target.discard(item)
        return "removed"
    target.add(item)
    return "added"

flags = {"A", "B"}
result_1 = safe_toggle(flags, "B")   # present -> removed
result_2 = safe_toggle(flags, "Z")   # absent  -> added
print("toggle B   ->", result_1)
print("toggle Z   ->", result_2)
print("flags now :", flags)
# toggle B   -> removed
# toggle Z   -> added
# flags now : {'A', 'Z'}

# ============================================================
# SUMMARY
# ============================================================
# - union() / |  : new set with all items of both sets (no duplicates)
# - add(x)       : add one item in place
# - copy()       : new independent copy
# - remove(x)    : delete x, raises KeyError if missing
# - discard(x)   : delete x, does nothing if missing
# - pop()        : remove + return an arbitrary item
# - update(iter) : add many items in place
# Prefer discard() + membership checks for safe, non-crashing code.

# ============================================================
# NEXT LESSON: Set Methods (Part 2) - difference, difference_update,
#              intersection, intersection_update, symmetric_difference,
#              symmetric_difference_update, isdisjoint, issubset
# ============================================================
