# Lesson 13 - Strings Methods (Part 1)
# Source: Elzero Python Course (Arabic)
# Topic: len(), strip(), rstrip(), lstrip(), title(),
#        capitalize(), zfill(), upper(), lower()
# Type: Theory + Practical Code

# ============================================================
# len() - GET STRING LENGTH
# ============================================================
# len() is a function that returns the number of items
# in a string (or any data).

a = "I Love Python"
b = "    I Love Python    "

print(len(a))   # 13
print(len(b))   # 22 (includes spaces)

print("=" * 50)

# ============================================================
# strip() rstrip() lstrip() - REMOVE SPACES
# ============================================================
# All three remove spaces, but from different sides:
# [1] strip()  -> removes spaces from BOTH sides
# [2] rstrip() -> removes spaces from RIGHT side only
# [3] lstrip() -> removes spaces from LEFT side only

a = "     I Love Python     "

print(a.strip())    # I Love Python (both sides)
print(a.rstrip())   #      I Love Python (right only)
print(a.lstrip())   # I Love Python      (left only)

print("=" * 50)

# ============================================================
# strip() WITH CUSTOM CHARACTERS
# ============================================================
# You can pass a character/string to strip() to remove
# those specific characters instead of spaces.

a = "######I Love Python####"
print(a.strip("#"))     # I Love Python
print(a.rstrip("#"))    # ######I Love Python
print(a.lstrip("#"))    # I Love Python####

# Multiple characters
a = "@#@#@#I Love Python@#@#@#"
print(a.strip("@#"))    # I Love Python
print(a.rstrip("@#"))   # @#@#@#I Love Python
print(a.lstrip("@#"))   # I Love Python@#@#@#

print("=" * 50)

# ============================================================
# title() - CAPITALIZE FIRST LETTER OF EVERY WORD
# ============================================================
# Makes the first letter of EACH word uppercase.
# Also capitalizes letters after numbers.

b = "I Love 2d Graphics and 3g Technology and python"
print(b.title())
# Output: I Love 2D Graphics And 3G Technology And Python

print("=" * 50)

# ============================================================
# capitalize() - CAPITALIZE FIRST LETTER ONLY
# ============================================================
# Makes ONLY the first letter of the sentence uppercase.
# Everything else becomes lowercase.

b = "I Love 2d Graphics and 3g Technology and python"
print(b.capitalize())
# Output: I love 2d graphics and 3g technology and python

print("=" * 50)

# ============================================================
# zfill() - ZERO FILL (Add Zeros at the Beginning)
# ============================================================
# Adds zeros to the LEFT of the string until it reaches
# the specified width (total number of characters).

c, d, e, f = "1", "11", "111", "1111"

print(c)  # 1
print(d)  # 11
print(e)  # 111
print(f)  # 1111

# With width 3
print(c.zfill(3))   # 001
print(d.zfill(3))   # 011
print(e.zfill(3))   # 111
print(f.zfill(3))   # 1111 (already 4 chars, no change)

# With width 4
print(c.zfill(4))   # 0001
print(d.zfill(4))   # 0011
print(e.zfill(4))   # 0111
print(f.zfill(4))   # 1111

print("=" * 50)

# ============================================================
# upper() and lower() - CHANGE CASE
# ============================================================

# upper() -> makes ALL letters uppercase
g = "osama"
print(g.upper())    # OSAMA

# lower() -> makes ALL letters lowercase
h = "OSama"
print(h.lower())    # osama

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] len()       -> number of characters
# [2] strip()     -> remove spaces from both sides
# [3] rstrip()    -> remove spaces from right
# [4] lstrip()    -> remove spaces from left
# [5] title()     -> capitalize first letter of every word
# [6] capitalize()-> capitalize first letter of sentence
# [7] zfill(n)    -> add zeros to reach width n
# [8] upper()     -> all uppercase
# [9] lower()     -> all lowercase

# ============================================================
# NEXT LESSON: Strings Methods (Part 2)
# ============================================================
