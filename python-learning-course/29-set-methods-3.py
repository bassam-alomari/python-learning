# -----------------------------------------------------------------
# Lesson 29: Set Methods Part 3
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : set methods - issubset, issuperset, isdisjoint
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# In this lesson we finish the set methods with three VALIDATION
# methods. They do NOT modify any set; they only answer a question
# about the relationship between two sets and return True or False.

# ============================================================
# [1] issubset()  -> is this set a SUBSET of the other set?
# ============================================================
# issubset() checks: are ALL items of the second set found
# inside the first set?
# The answer is True only if EVERY item is present.

a = {1, 2, 3, 4}
b = {1, 2, 3}

print("b.issubset(a):", b.issubset(a))
# b.issubset(a): True   -> every item of b exists in a

b2 = {1, 2, 9}   # 9 does NOT exist in a
print("b2.issubset(a):", b2.issubset(a))
# b2.issubset(a): False  -> 9 is missing from a

# A set is always a subset of itself.
print("a.issubset(a):", a.issubset(a))
# a.issubset(a): True

# ============================================================
# [2] issuperset()  -> does this set CONTAIN all items of the other?
# ============================================================
# issuperset() is the opposite of issubset().
# It checks: does the first set contain ALL the items of the second?

print("a.issuperset(b):", a.issuperset(b))
# a.issuperset(b): True   -> a has 1, 2, 3, 4 so it has all of b

print("b.issuperset(a):", b.issuperset(a))
# b.issuperset(a): False  -> b has no 4, so it cannot contain all of a

# Quick comparison: subset and superset are mirror images.
small = {10, 20}
big = {10, 20, 30, 40}
print("small is subset of big  :", small.issubset(big))   # True
print("big is superset of small:", big.issuperset(small)) # True

# ============================================================
# [3] isdisjoint()  -> are the two sets completely SEPARATED?
# ============================================================
# isdisjoint() checks: is there ANY shared item between the sets?
# If there is NO common item at all -> True (disjoint).
# If they share even ONE item     -> False.

x = {1, 2, 3}
y = {4, 5, 6}
print("x.isdisjoint(y):", x.isdisjoint(y))
# x.isdisjoint(y): True   -> no shared items, fully separated

z = {3, 7, 8}   # 3 exists in x
print("x.isdisjoint(z):", x.isdisjoint(z))
# x.isdisjoint(z): False  -> they share the item 3

# ============================================================
# [4] Comparing two sets without creating a temporary set
# ============================================================
# The < and > operators do the same job:
#   x < y   means  x.issubset(y)
#   x > y   means  x.issuperset(y)

print("b < a  (subset)   :", b < a)     # True
print("a > b  (superset) :", a > b)     # True
print("b2 < a (subset)   :", b2 < a)    # False

# ============================================================
# Improvement (from me): a friendly relationship reporter
# ============================================================
# Turn the three raw checks into one readable sentence.
# This is a nice touch for logging and teaching material.

def describe_relation(first, second):
    """Return a short text that explains how the two sets relate."""
    if first.isdisjoint(second):
        return "completely separate (no shared items)"
    if first.issuperset(second):
        return f"'{first}' fully contains '{second}'"
    if first.issubset(second):
        return f"'{first}' is fully inside '{second}'"
    return "they partially overlap (neither one contains the other)"

print(describe_relation(a, b))    # '{1, 2, 3, 4}' fully contains '{1, 2, 3}'
print(describe_relation(x, y))    # completely separate (no shared items)
print(describe_relation({1, 2}, {2, 3}))  # partially overlap

# ============================================================
# SUMMARY
# ============================================================
# - issubset()   : True if ALL items of this set exist in the other set
# - issuperset() : True if this set contains ALL items of the other set
# - isdisjoint() : True if there is NO shared item at all
# - Operators    : < behaves like issubset(), > behaves like issuperset()
# All of them return True / False and never modify the sets.

# ============================================================
# NEXT LESSON: Dictionary - what it is, how to create one, and how
#              it differs from lists, tuples, and sets
# ============================================================
