# Lesson 17 - Strings Formatting (Old Way)
# Source: Elzero Python Course (Arabic) - Lesson #017
# Topic: Old Way Formatting with % (like C Language)
# Type: Theory + Practical Code

# ============================================================
# THE PROBLEM WITH CONCATENATION
# ============================================================
# Concatenation (+) fails when mixing String with Number.

name = "Osama"
age = 36
rank = 10

print("My Name is: " + name)
# Output: My Name is: Osama

# print("My Name is: " + name + " and My Age is: " + age)
# Type Error: can only concatenate str (not "int") to str

print("=" * 50)

# ============================================================
# OLD WAY FORMATTING WITH % (Like C Language)
# ============================================================
# %s -> String
# %d -> Integer (Decimal)
# %f -> Float
# %.2f -> Float with 2 decimal places
# %.5s -> Truncate String to 5 characters

# %s (String)
print("My Name is: %s" % "Osama")
# Output: My Name is: Osama

print("My Name is: %s" % name)
# Output: My Name is: Osama

# Multiple values -> put them in a tuple ( )
print("My Name is: %s and My Age is: %s" % (name, age))
# Output: My Name is: Osama and My Age is: 36

print("=" * 50)

# %s and %d together
n = "Osama"
l = "Python"
y = 10

print("My Name is %s Iam %s Developer With %d Years Exp" % (n, l, y))
# Output: My Name is Osama Iam Python Developer With 10 Years Exp

print("=" * 50)

# ============================================================
# CONTROL FLOATING POINT NUMBER
# ============================================================

myNumber = 10
print("My Number is: %d" % myNumber)
# Output: My Number is: 10

print("My Number is: %f" % myNumber)
# Output: My Number is: 10.000000

print("My Number is: %.2f" % myNumber)
# Output: My Number is: 10.00

print("=" * 50)

# ============================================================
# TRUNCATE STRING
# ============================================================
# %.5s -> take only the first 5 characters

myLongString = "Hello Peoples of Elzero Web School I Love You All"
print("Message is %.5s" % myLongString)
# Output: Message is Hello

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] %s  -> String
# [2] %d  -> Integer (Decimal)
# [3] %f  -> Float (default 6 decimal places)
# [4] %.2f -> Float with 2 decimal places
# [5] %.5s -> Truncate String to 5 characters
# [6] Multiple values -> use a tuple ( ) after %
# [7] Formatting is better than Concatenation because it
#     avoids the Type Error when mixing String + Number.

# ============================================================
# NEXT LESSON: Format (New Way - String Formatting)
# ============================================================
