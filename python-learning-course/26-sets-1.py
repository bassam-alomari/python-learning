# Lesson 26 - Sets (Part 1)
# Source: Elzero Python Course (Arabic) - Lesson #026
# Topic: What is a Set, Curly Braces, No Repetition, Unordered
# Type: Theory + Practical Code

# ============================================================
# WHAT IS A SET?
# ============================================================
# A Set is a collection of items written with
# Curly Braces { }  (not [ ] like Lists, not ( ) like Tuples).

mySet = {"Osama", "Ahmed", "Sayed"}
print(mySet)
# Output: {'Osama', 'Ahmed', 'Sayed'}   (order may differ)

print("=" * 50)

# ============================================================
# [1] SET DOES NOT ALLOW REPETITION (No Duplicates)
# ============================================================
# If the same value is written more than once,
# the Set keeps it ONLY ONCE (no duplicates).

mySet2 = {"Osama", "Osama", "Ahmed", "Ahmed", "Sayed", 100, 100}
print(mySet2)
# Output: {'Osama', 'Ahmed', 'Sayed', 100}

print("=" * 50)

# ============================================================
# [2] SET IS UNORDERED -> NO INDEXING / SLICING
# ============================================================
# Items have NO fixed order, so you CANNOT access an item
# with an index (there is no index at all).

mySetData = {"One", "Two", "Three", 1, 100.50, True}

# print(mySetData[0])
# TypeError: 'set' object is not subscriptable
# (A Set has NO order -> there is no index -> no indexing/slicing)

print("=" * 50)

# ============================================================
# [3] SET CAN HOLD DIFFERENT DATA TYPES  (Basic Types)
# ============================================================
# A Set can store: Strings, Numbers, Floats, Booleans, Tuples.
# BUT it CANNOT hold Mutable types (Lists / Dictionaries)
# because Set items MUST be Immutable (Hashable).

mySetTypes = {"Osama", 100, 100.50, True, (1, 2, 3)}
print(mySetTypes)
# Output: {(1, 2, 3), 'Osama', 100, 100.5, True}

# mySetBad = {"Osama", 100, [1, 2, 3]}   # List inside -> ERROR
# TypeError: unhashable type: 'list'

# mySetBad2 = {"Osama", 100, {"A": 1}}   # Dict inside -> ERROR
# TypeError: unhashable type: 'dict'

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] Set -> written with Curly Braces { }
# [2] Set -> does NOT allow Repetition (no duplicates)
# [3] Set -> is UNORDERED -> no Indexing, no Slicing
# [4] Set -> items can be any BASIC type (str/int/float/bool/tuple)
# [5] Set -> items CANNOT be Mutable (list/dict) -> TypeError
# [6] Set -> itself is Mutable (you CAN add/remove items later)

# ============================================================
# NEXT LESSON: Set Methods (Part 1)
# ============================================================
