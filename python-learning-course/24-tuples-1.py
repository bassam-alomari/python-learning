# Lesson 24 - Tuples (Part 1)
# Source: Elzero Python Course (Arabic) - Lesson #024
# Topic: What is a Tuple, Indexing, Immutability
# Type: Theory + Practical Code

# ============================================================
# WHAT IS A TUPLE?
# ============================================================
# A Tuple is like a List, but it is written with
# Parentheses ( ) instead of Square Brackets [ ].
# It is used to store a collection of items.

# Tuple with Parentheses
myTuple = ("Osama", "Ahmed", "Sayed")
print(myTuple)
# Output: ('Osama', 'Ahmed', 'Sayed')

print("=" * 50)

# ============================================================
# TUPLE WITHOUT PARENTHESES
# ============================================================
# You can create a Tuple WITHOUT the parentheses.
# Python still treats it as a Tuple.

myTuple2 = "Osama", "Ahmed", "Sayed"
print(myTuple2)
# Output: ('Osama', 'Ahmed', 'Sayed')

print("=" * 50)

# ============================================================
# CHECK THE TYPE
# ============================================================
# In both cases the type is "tuple".

print(type(myTuple))
# Output: <class 'tuple'>

print(type(myTuple2))
# Output: <class 'tuple'>

print("=" * 50)

# ============================================================
# TUPLE IS ORDERED + INDEXING
# ============================================================
# A Tuple is Ordered, so you can access items by Index
# exactly like a List (including negative indexes).

myTuple3 = (1, 2, 3, 4, 5)
print(myTuple3[0])
# Output: 1

print(myTuple3[-1])
# Output: 5  (last item)

print(myTuple3[-2])
# Output: 4  (second from the end)

print("=" * 50)

# ============================================================
# TUPLE IS IMMUTABLE (CANNOT BE MODIFIED)
# ============================================================
# In Lists we can assign a new value and change items freely
# (Mutable). But in Tuples we CANNOT change items after
# creation (Immutable).
# If you try to change an item -> TypeError.

myTuple4 = (1, 2, 3, 4, 5)

# myTuple4[0] = "One"
# TypeError: 'tuple' object does not support item assignment

print(myTuple4)
# Output: (1, 2, 3, 4, 5)

print("=" * 50)

# ============================================================
# TUPLE CAN HOLD ANY DATA TYPE
# ============================================================
# Like Lists, a Tuple can hold any type of data:
# numbers, strings, booleans, etc.

myTuple5 = (1, 2.5, "Osama", True, [10, 20])
print(myTuple5)
# Output: (1, 2.5, 'Osama', True, [10, 20])

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] Tuple is written with ( ) instead of [ ]
# [2] You can create a Tuple WITHOUT parentheses
# [3] The type is always "tuple"
# [4] Tuple is Ordered -> use Index (including negative)
# [5] Tuple is IMMUTABLE -> cannot change items (TypeError)
# [6] Tuple can hold any data type

# ============================================================
# NEXT LESSON: Tuple Methods (Part 2)
# ============================================================
