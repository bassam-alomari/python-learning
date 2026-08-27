# Lesson 14 - Strings Methods (Part 2)
# Source: Elzero Python Course (Arabic)
# Topic: split(), rsplit(), center(), count(),
#        swapcase(), startswith(), endswith()
# Type: Theory + Practical Code

# ============================================================
# split() - SPLIT STRING INTO A LIST
# ============================================================
# Splits a string into a list of items.
# By default, splits on spaces.

a = "I Love Python and PHP"
print(a.split())
# Output: ['I', 'Love', 'Python', 'and', 'PHP']

# Split on a specific character
b = "I-Love-Python-and-PHP"
print(b.split("-"))
# Output: ['I', 'Love', 'Python', 'and', 'PHP']

# Split with maxsplit (only split N times)
c = "I-Love-Python-and-PHP-and-MySQL"
print(c.split("-", 2))
# Output: ['I', 'Love', 'Python-and-PHP-and-MySQL']

print("=" * 50)

# ============================================================
# rsplit() - SPLIT FROM THE RIGHT
# ============================================================
# Splits from the right side, with a max number of splits.
# Syntax: rsplit(separator, maxsplit)

d = "I-Love-Python-and-PHP-and-MySQL"

# Split from right, max 2 splits
print(d.rsplit("-", 2))
# Output: ['I-Love-Python-and-PHP', 'and', 'MySQL']

# Split from right, max 3 splits
print(d.rsplit("-", 3))
# Output: ['I-Love-Python-and', 'PHP', 'and', 'MySQL']

print("=" * 50)

# ============================================================
# center() - CENTER THE STRING
# ============================================================
# Centers the string within a given width.
# Syntax: center(width, fillchar)
# NOTE: width is REQUIRED (error if missing)

e = "Osama"

# Center with spaces (default fill)
print(e.center(9))
# Output: '  Osama  '

# Center with # fill
print(e.center(9, "#"))
# Output: '##Osama##'

# Center with @ fill
print(e.center(15, "@"))
# Output: '@@@@@Osama@@@@@'

print("=" * 50)

# ============================================================
# count() - COUNT OCCURRENCES
# ============================================================
# Counts how many times a substring appears.
# Syntax: count(substring, start, end)

f = "I Love Python and PHP Because PHP is Easy"

# Count all occurrences
print(f.count("PHP"))
# Output: 2

# Count within a specific range
print(f.count("PHP", 0, 25))
# Output: 1 (only one PHP in first 25 chars)

print("=" * 50)

# ============================================================
# swapcase() - SWAP UPPER/LOWER CASE
# ============================================================
# Uppercase becomes lowercase, lowercase becomes uppercase.

g = "I Love Python"
h = "i lOVE pYTHON"

print(g.swapcase())
# Output: i lOVE pYTHON

print(h.swapcase())
# Output: I Love Python

print("=" * 50)

# ============================================================
# startswith() - CHECK IF STRING STARTS WITH
# ============================================================
# Returns True if the string starts with the given prefix.
# Syntax: startswith(prefix, start, end)

i = "I Love Python"

print(i.startswith("I"))
# Output: True

print(i.startswith("S"))
# Output: False

# Check within a specific range
print(i.startswith("P", 7, 12))
# Output: True (from index 7 to 12, it starts with "P")

print("=" * 50)

# ============================================================
# endswith() - CHECK IF STRING ENDS WITH
# ============================================================
# Returns True if the string ends with the given suffix.
# Syntax: endswith(suffix, start, end)

j = "I Love Python"

print(j.endswith("n"))
# Output: True

print(j.endswith("S"))
# Output: False

# Check within a specific range
print(j.endswith("e", 2, 6))
# Output: True (from index 2 to 6, it ends with "e")

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] split()      -> split string into list (on separator)
# [2] rsplit()     -> split from right with maxsplit
# [3] center()     -> center string within width (width required)
# [4] count()      -> count occurrences of substring
# [5] swapcase()   -> swap upper/lower case
# [6] startswith() -> check if string starts with prefix
# [7] endswith()   -> check if string ends with suffix

# ============================================================
# NEXT LESSON: Strings Methods (Part 3)
# ============================================================
