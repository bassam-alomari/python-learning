# Lesson 25 - Tuples (Part 2) - Tuple Methods
# Source: Elzero Python Course (Arabic) - Lesson #025
# Topic: count(), index(), Concatenation (+), Repetition (*),
#        Unpacking (Destructuring)
# Type: Theory + Practical Code

# ============================================================
# SINGLE ITEM TUPLE - MUST ADD A TRAILING COMMA ( , )
# ============================================================
# If a Tuple has only ONE item, you MUST add a comma ( , )
# after it. Otherwise Python will treat it as a String /
# Number / etc. (NOT as a Tuple).

mySingleTuple = ("Osama",)   # correct  -> Tuple
mySingleNumber = (100,)      # correct  -> Tuple

# myBadTuple1 = ("Osama")    # <class 'str'>
# myBadTuple2 = (100)        # <class 'int'>

print(type(mySingleTuple))
# Output: <class 'tuple'>

print(type(mySingleNumber))
# Output: <class 'tuple'>

print("=" * 70)

# ============================================================
# len() - COUNT THE ITEMS
# ============================================================
# len(tuple) -> total number of items.
# Works the SAME as it does with Lists & Strings.

myTupleCount = (10, 20, 30, 40, 50)
print(len(myTupleCount))
# Output: 5

print("=" * 70)

# ============================================================
# CONCATENATION ( + ) - JOIN TWO TUPLES
# ============================================================
# Tuples are IMMUTABLE: we CANNOT modify them directly.
# BUT we CAN create a NEW Tuple by joining others with ( + ).

tuple1 = (1, 2, 3, 4)
tuple2 = (5, 6)

tuple3 = tuple1 + tuple2
print(tuple3)
# Output: (1, 2, 3, 4, 5, 6)

print("=" * 70)

# ============================================================
# REPETITION ( * ) - REPEAT THE TUPLE
# ============================================================
# tuple * N -> repeats the WHOLE Tuple N times
#             concatenated into ONE big Tuple.

tuple4 = ("A", "B", "C")
tuple5 = tuple4 * 3
print(tuple5)
# Output: ('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C')

print("=" * 70)

# ============================================================
# count() - HOW MANY TIMES A VALUE APPEARS
# ============================================================
# tuple.count(value) -> how many times (value) appears.

myTupleCount2 = (1, 5, 7, 5, 0, 10, 5, 5)
print(myTupleCount2.count(5))
# Output: 4

print("=" * 70)

# ============================================================
# index() - GET THE INDEX OF THE FIRST MATCH
# ============================================================
# tuple.index(value) -> index of the FIRST occurrence.

myTupleIndex = (1, 5, 9, 5, 0, 10, 5, 5)
print(myTupleIndex.index(5))
# Output: 1   (the FIRST "5" is at index 1)

print("=" * 70)

# ============================================================
# UNPACKING / DESTRUCTURING
# ============================================================
# Unpacking = put ALL items into SEPARATE variables
#             in ONE line.
# The number of variables MUST equal the number of items,
# otherwise -> ValueError.

myUnpack = ("Osama", "Ahmed", "Sayed")
x, y, z = myUnpack

print(x)
# Output: Osama

print(y)
# Output: Ahmed

print(z)
# Output: Sayed

print("=" * 70)

# ============================================================
# SUMMARY
# ============================================================
# [1] Single-item Tuple   -> MUST have a trailing comma ( , )
# [2] len(tuple)          -> number of items
# [3] tuple + tuple       -> concatenation (new Tuple)
# [4] tuple * N           -> repetition
# [5] tuple.count(value)  -> how many times value appears
# [6] tuple.index(value)  -> first index of value
# [7] Unpacking           -> a, b, c = myTuple
# [8] Cannot modify Tuple -> IMMUTABLE

# ============================================================
# NEXT LESSON: Dictionaries (What Are Dictionaries?)
# ============================================================
