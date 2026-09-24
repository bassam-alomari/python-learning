# Lesson 28 - Set Methods (Part 2)
# Source: Elzero Python Course (Arabic) - Lesson #028
# Topic: difference, difference_update, intersection,
#        intersection_update, symmetric_difference,
#        symmetric_difference_update
# Type: Theory + Practical Code

# ============================================================
# [1] difference()  -  ITEMS IN SET1 BUT NOT IN SET2
# ============================================================
# set1.difference(set2) -> returns a NEW Set holding the
#                          items that EXIST in set1 and
#                          do NOT exist in set2.
# Shortcut:  you can use the Minus ( - ) operator instead:
#                      "set1 - set2"

mySetDiffA = {1, 2, 3, 4}
mySetDiffB = {1, 2, 3, 7, 8}

print(mySetDiffA.difference(mySetDiffB))
# Output: {4}
# (4 is in A && NOT in B)

print(mySetDiffA - mySetDiffB)
# Output: {4}   <-- same result with the ( - ) operator

print("=" * 50)

# ============================================================
# [2] difference_update()  -  KEEP ONLY NON-SHARED IN SET1
# ============================================================
# set1.difference_update(set2) -> does NOT create a new Set,
# it MODIFIES set1 DIRECTLY, deleting from it every item
# that also exists in set2.

mySetDiffUpA = {1, 2, 3, 4}
mySetDiffUpB = {1, 2, 3, 7, 8}

mySetDiffUpA.difference_update(mySetDiffUpB)
print(mySetDiffUpA)
# Output: {4}   <-- set1 changed IN PLACE

print("=" * 50)

# ============================================================
# [3] intersection()  -  ITEMS SHARED BY BOTH SETS
# ============================================================
# set1.intersection(set2) -> returns a NEW Set with ONLY
#                            the items that exist in BOTH.
# Shortcut:  the ( & ) Ampersand operator.

mySetInterA = {1, 2, 3, 4, 5}
mySetInterB = {4, 5, 6, 7}

print(mySetInterA.intersection(mySetInterB))
# Output: {4, 5}

print(mySetInterA & mySetInterB)
# Output: {4, 5}   <-- same result with ( & )

print("=" * 50)

# ============================================================
# [4] intersection_update()  -  KEEP ONLY SHARED, IN PLACE
# ============================================================
# set1.intersection_update(set2) -> modifies set1 DIRECTLY,
# keeping only the items shared with set2.

mySetInterUpA = {1, 2, 3, 4, 5}
mySetInterUpB = {4, 5, 6, 7}

mySetInterUpA.intersection_update(mySetInterUpB)
print(mySetInterUpA)
# Output: {4, 5}   <-- set1 changed IN PLACE

print("=" * 50)

# ============================================================
# [5] symmetric_difference()  -  ITEMS NOT SHARED (A+B)
# ============================================================
# set1.symmetric_difference(set2) -> returns a NEW Set with
# the items that are in set1 OR in set2, but NOT in both.
# Shortcut:  the ( ^ ) Caret operator.

mySetSymA = {1, 2, 3, 4, 5}
mySetSymB = {4, 5, 6, 7}

print(mySetSymA.symmetric_difference(mySetSymB))
# Output: {1, 2, 3, 6, 7}
# (1,2,3 only in A | 6,7 only in B | 4,5 shared -> dropped)

print(mySetSymA ^ mySetSymB)
# Output: {1, 2, 3, 6, 7}   <-- same result with ( ^ )

print("=" * 50)

# ============================================================
# [6] symmetric_difference_update()  -  IN PLACE
# ============================================================
# set1.symmetric_difference_update(set2) -> modifies set1
# DIRECTLY, keeping only the items NOT shared with set2.

mySetSymUpA = {1, 2, 3, 4, 5}
mySetSymUpB = {4, 5, 6, 7}

mySetSymUpA.symmetric_difference_update(mySetSymUpB)
print(mySetSymUpA)
# Output: {1, 2, 3, 6, 7}   <-- set1 changed IN PLACE

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] difference()                set1 - set2     (new Set)
# [2] difference_update()         (modify set1)
# [3] intersection()              set1 & set2     (new Set)
# [4] intersection_update()       (modify set1)
# [5] symmetric_difference()      set1 ^ set2     (new Set)
# [6] symmetric_difference_update()(modify set1)

# ============================================================
# NEXT LESSON: Dictionary (Part 1) - What is a Dictionary
# ============================================================
