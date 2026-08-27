# Lesson 15 - Strings Methods (Part 3)
# Source: Elzero Python Course (Arabic) - Lesson #015
# Topic: index(), find(), rjust(), ljust(), splitlines(),
#        partition(), rpartition(), istitle(), islower(),
#        isidentifier(), isalpha(), isalnum()
# Type: Theory + Practical Code

# ============================================================
# index(SubString, Start, End)
# ============================================================
# Returns the index (position) where the substring starts.
# NOTE: Raises ValueError if substring NOT found.

a = "I Love Python"
print(a.index("P"))  # Index Number 7
print(a.index("P", 0, 10))  # Index Number 7
# print(a.index("P", 0, 5))  # Through Error (ValueError)

print("=" * 50)

# ============================================================
# find(SubString, Start, End)
# ============================================================
# Same as index(), but returns -1 if NOT found
# (instead of raising an error).

b = "I Love Python"
print(b.find("P"))  # Index Number 7
print(b.find("P", 0, 10))  # Index Number 7
print(b.find("P", 0, 5))  # -1

print("=" * 50)

# ============================================================
# rjust(Width, Fill Char) and ljust(Width, Fill Char)
# ============================================================
# rjust() -> align text to the RIGHT
# ljust() -> align text to the LEFT

c = "Osama"
print(c.rjust(10))
print(c.rjust(10, "#"))

d = "Osama"
print(d.ljust(10))
print(d.ljust(10, "#"))

print("=" * 50)

# ============================================================
# splitlines() - SPLIT INTO LINES
# ============================================================
# Returns a list of all lines in the string.

e = """First Line
Second Line
Third Line"""
print(e.splitlines())
print(type(e.splitlines()))

print("=" * 50)

# ============================================================
# partition() and rpartition() - SPLIT INTO 3 PARTS
# ============================================================
# Returns a tuple of 3 elements:
# (before separator, separator, after separator)

f = "I Love Python and PHP"

# partition() - splits from the LEFT
print(f.partition("Python"))
# Output: ('I Love ', 'Python', ' and PHP')

# rpartition() - splits from the RIGHT
print(f.rpartition("and"))
# Output: ('I Love Python ', 'and', ' PHP')

print("=" * 50)

# ============================================================
# VALIDATION METHODS (Return True or False)
# ============================================================

# istitle() - Is every word's first letter uppercase?
g = "I Love Python"
print(g.istitle())
# Output: True

h = "I love python"
print(h.istitle())
# Output: False

print("=" * 50)

# islower() - Are all letters lowercase?
i = "hello world"
print(i.islower())
# Output: True

j = "Hello World"
print(j.islower())
# Output: False

print("=" * 50)

# isidentifier() - Is it a valid variable name?
seven = "osama_elzero"
eight = "OsamaElzero100"
nine = "Osama--Elzero100"

print(seven.isidentifier())
print(eight.isidentifier())
print(nine.isidentifier())

print("=" * 50)

# isalpha() - Are all characters letters (no numbers/symbols)?
x = "AaaaaBbbbbb"
y = "AaaaaBbbbbb111"
print(x.isalpha())
print(y.isalpha())

print("=" * 50)

# isalnum() - Are all characters letters AND/OR numbers?
m = "Hello123"
print(m.isalnum())
# Output: True

n = "Hello 123"
print(n.isalnum())
# Output: False (contains space)

o = "Hello!"
print(o.isalnum())
# Output: False (contains symbol)

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] index()      -> position of substring (error if not found)
# [2] find()       -> position of substring (-1 if not found)
# [3] rjust()      -> align right with fill
# [4] ljust()      -> align left with fill
# [5] splitlines() -> split into list of lines
# [6] partition()  -> split into 3-part tuple (from left)
# [7] rpartition() -> split into 3-part tuple (from right)
# [8] istitle()    -> is every word capitalized?
# [9] islower()    -> are all letters lowercase?
# [10] isidentifier() -> is it a valid variable name?
# [11] isalpha()   -> are all characters letters?
# [12] isalnum()   -> are all characters letters/numbers?

# ============================================================
# NEXT LESSON: Numbers (int, float)
# ============================================================
