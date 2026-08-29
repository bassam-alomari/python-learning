# Lesson 21 - Lists
# Source: Elzero Python Course (Arabic) - Lesson #021
# Topic: Lists - Index, Slicing, Step, Mutable
# Type: Theory + Practical Code

# ============================================================
# LISTS - THEORY
# ============================================================
# [1] List Items Are Enclosed in Square Brackets []
# [2] List Are Ordered, To Use Index To Access Item
# [3] List Are Mutable => Add, Delete, Edit
# [4] List Items Is Not Unique (can repeat)
# [5] List Can Have Different Data Types

myAwesomeList = ["One", "Two", "One", 1, 100.5, True]

print("=" * 50)

# ============================================================
# ACCESS ITEMS WITH INDEX
# ============================================================
# Index starts from 0 (first item).
# Negative index starts from the end (-1 = last item).

print(myAwesomeList)  # Whole List
# Output: ['One', 'Two', 'One', 1, 100.5, True]

print(myAwesomeList[1])  # "One"
# Output: Two

print(myAwesomeList[-1])  # True
# Output: True

print(myAwesomeList[-3])  # 1
# Output: 1

print("=" * 50)

# ============================================================
# SLICING
# ============================================================
# [start:end] -> from start to end (end NOT included)
# [:end]      -> from beginning to end
# [start:]    -> from start to the end

print(myAwesomeList[1:4])  # "Two", "One", 1
# Output: ['Two', 'One', 1]

print(myAwesomeList[:4])   # ['One', 'Two', 'One', 1]
# Output: ['One', 'Two', 'One', 1]

print(myAwesomeList[1:])   # ['Two', 'One', 1, 100.5, True]
# Output: ['Two', 'One', 1, 100.5, True]

print("=" * 50)

# ============================================================
# STEP
# ============================================================
# [::step] -> take every (step) item

print(myAwesomeList[::1])  # all items
# Output: ['One', 'Two', 'One', 1, 100.5, True]

print(myAwesomeList[::2])  # every 2nd item
# Output: ['One', 'One', 100.5]

print("=" * 50)

# ============================================================
# INDEX ERROR
# ============================================================
# If the index is out of range -> IndexError

# print(myAwesomeList[150])
# IndexError: list index out of range

print("=" * 50)

# ============================================================
# MUTABLE - EDIT ONE ITEM
# ============================================================
# Lists are Mutable: we can change an item directly
# using its index.

print(myAwesomeList)
# Output: ['One', 'Two', 'One', 1, 100.5, True]

myAwesomeList[1] = 2
myAwesomeList[-1] = False

print(myAwesomeList)
# Output: ['One', 2, 'One', 1, 100.5, False]

print("=" * 50)

# ============================================================
# MUTABLE - EDIT A RANGE OF ITEMS
# ============================================================
# We can replace a whole range of items with new values,
# or delete them by assigning an empty list [].

# Delete the first 2 items
myAwesomeList[0:2] = []
print(myAwesomeList)
# Output: ['One', 1, 100.5, False]

# Replace the first 3 items with new values
myAwesomeList[0:3] = ["A", "B", "C"]
print(myAwesomeList)
# Output: ['A', 'B', 'C', False]

# Replace the first 3 items with only 1 item
myAwesomeList[0:3] = ["A"]
print(myAwesomeList)
# Output: ['A', False]

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] List -> items in Square Brackets []
# [2] Index -> starts from 0, negative from the end
# [3] Slicing -> [start:end], [:end], [start:]
# [4] Step -> [::step]
# [5] Mutable -> can Add, Delete, Edit items
# [6] Edit one item -> myList[index] = value
# [7] Edit a range -> myList[start:end] = [values]
# [8] Delete a range -> myList[start:end] = []

# ============================================================
# NEXT LESSON: List Methods (Part 1)
# ============================================================
