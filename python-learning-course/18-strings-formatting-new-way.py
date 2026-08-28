# Lesson 18 - Strings Formatting (New Way)
# Source: Elzero Python Course (Arabic) - Lesson #018
# Topic: New Way Formatting with .format() and f-string
# Type: Theory + Practical Code

# ============================================================
# NEW WAY FORMATTING WITH .format()
# ============================================================
# Instead of % (old way), we use {} as placeholders
# and .format() to pass the values.

name = "Osama"
age = 36
rank = 10

print("My Name is: {}".format("Osama"))
# Output: My Name is: Osama

print("My Name is: {}".format(name))
# Output: My Name is: Osama

print("My Name is: {} My Age: {}".format(name, age))
# Output: My Name is: Osama My Age: 36

# With types inside the placeholder
print("My Name is: {:s} Age: {:d} & Rank is: {:f}".format(name, age, rank))
# Output: My Name is: Osama Age: 36 & Rank is: 10.000000

print("=" * 50)

# ============================================================
# TYPES INSIDE THE PLACEHOLDER
# ============================================================
# {:s} => String
# {:d} => Number (Integer)
# {:f} => Float

n = "Osama"
l = "Python"
y = 10

print("My Name is {} Iam {} Developer With {:d} Years Exp".format(n, l, y))
# Output: My Name is Osama Iam Python Developer With 10 Years Exp

print("=" * 50)

# ============================================================
# CONTROL FLOATING POINT NUMBER
# ============================================================

myNumber = 10
print("My Number is: {:d}".format(myNumber))
# Output: My Number is: 10

print("My Number is: {:f}".format(myNumber))
# Output: My Number is: 10.000000

print("My Number is: {:.2f}".format(myNumber))
# Output: My Number is: 10.00

print("=" * 50)

# ============================================================
# FORMAT MONEY (Thousands Separator)
# ============================================================
# {:_d} -> underscore separator
# {:,d} -> comma separator

myMoney = 500162350198

print("My Money in Bank Is: {:d}".format(myMoney))
# Output: My Money in Bank Is: 500162350198

print("My Money in Bank Is: {:_d}".format(myMoney))
# Output: My Money in Bank Is: 500_162_350_198

print("My Money in Bank Is: {:,d}".format(myMoney))
# Output: My Money in Bank Is: 500,162,350,198

# print("My Money in Bank Is: {:&d}".format(myMoney))  # Wrong
# ValueError: Invalid format specifier

print("=" * 50)

# ============================================================
# REARRANGE ITEMS (Change Order with Index)
# ============================================================
# {} -> in order (0, 1, 2)
# {1} {2} {0} -> change the order using index

a, b, c = "One", "Two", "Three"
print("Hello {} {} {}".format(a, b, c))
# Output: Hello One Two Three

print("Hello {1} {2} {0}".format(a, b, c))
# Output: Hello Two Three One

print("Hello {2} {0} {1}".format(a, b, c))
# Output: Hello Three One Two

print("=" * 50)

# ============================================================
# REARRANGE NUMBERS WITH INDEX + TYPE
# ============================================================

x, y, z = 10, 20, 30
print("Hello {} {} {}".format(x, y, z))
# Output: Hello 10 20 30

print("Hello {1:d} {2:d} {0:d}".format(x, y, z))
# Output: Hello 20 30 10

print("Hello {2:f} {0:f} {1:f}".format(x, y, z))
# Output: Hello 30.000000 10.000000 20.000000

print("Hello {2:.2f} {0:.4f} {1:.5f}".format(x, y, z))
# Output: Hello 30.00 10.0000 20.00000

print("=" * 50)

# ============================================================
# FORMAT IN VERSION 3.6+ (f-string)
# ============================================================
# The easiest way: put f before the string and use {variable}
# directly inside the string.

myName = "Osama"
myAge = 36

# Without f -> prints the placeholders as text (not replaced)
print("My Name is : {myName} and My Age is : {myAge}")
# Output: My Name is : {myName} and My Age is : {myAge}

# With f -> replaces the variables with their values
print(f"My Name is : {myName} and My Age is : {myAge}")
# Output: My Name is : Osama and My Age is : 36

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] .format() -> new way, uses {} placeholders
# [2] {:s} -> String, {:d} -> Integer, {:f} -> Float
# [3] {:.2f} -> Float with 2 decimal places
# [4] {:_d} -> underscore separator, {:,d} -> comma separator
# [5] {1} {2} {0} -> change order using index
# [6] f-string (Python 3.6+) -> easiest way, use f before string
#     and {variable} directly inside.

# ============================================================
# NEXT LESSON: Numbers (int, float)
# ============================================================
