# Lesson 12 - Strings Indexing & Slicing
# Source: Elzero Python Course (Arabic)
# Topic: Access Characters by Index + Slice Strings
# Type: Theory + Practical Code

# ============================================================
# KEY CONCEPTS
# ============================================================
# [1] All Data in Python is an Object
# [2] Objects contain Elements
# [3] Every Element has its own Index
# [4] Python uses Zero-Based Indexing (starts from 0)
# [5] Use Square Brackets [] to access elements
# [6] Enable accessing parts of Strings, Tuples, or Lists

# ============================================================
# INDEXING (Access Single Item)
# ============================================================

myString = "I Love Python"

# Positive Index (start from 0)
print(myString[0])   # Index 0 => I
print(myString[9])   # Index 9 => t

# Negative Index (start from end, -1 is last)
print(myString[-1])  # Index -1 => n (last character)
print(myString[-6])  # Index -6 => P (6th from end)

print("=" * 50)

# ============================================================
# SLICING (Access Multiple Items)
# ============================================================
# Syntax: string[start:end]
# End is NOT included in the result.
# Syntax: string[start:end:step]

# Basic slicing
print(myString[8:11])   # yth (index 8, 9, 10)
print(myString[3:5])    # ov (index 3, 4)

# If start is missing, starts from 0
print(myString[:10])    # I Love Pyt

# If end is missing, goes to the end
print(myString[5:])     # e Python

# Full string
print(myString[:])      # I Love Python

print("=" * 50)

# ============================================================
# SLICING WITH STEP
# ============================================================
# Step determines how many characters to skip.

# Step = 1 (default, every character)
print(myString[0::1])   # I Love Python
print(myString[::1])    # I Love Python

# Step = 2 (every 2nd character)
print(myString[::2])    # ILv yhn

# Step = 3 (every 3rd character)
print(myString[::3])    # Io tn

print("=" * 50)

# ============================================================
# PRACTICAL EXAMPLES
# ============================================================

text = "Hello World"

# Get first character
print(text[0])          # H

# Get last character
print(text[-1])         # d

# Get "World"
print(text[6:11])       # World

# Get "Hello"
print(text[:5])         # Hello

# Get "orld"
print(text[7:])         # orld

# Reverse the string
print(text[::-1])       # dlroW olleH

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] Indexing: string[index] - access single character
# [2] Positive index: starts from 0
# [3] Negative index: starts from end (-1 is last)
# [4] Slicing: string[start:end] - end NOT included
# [5] Omit start: begins from 0
# [6] Omit end: goes to the end
# [7] Step: string[start:end:step] - skip characters
# [8] Reverse: string[::-1]

# ============================================================
# NEXT LESSON: String Methods
# ============================================================
