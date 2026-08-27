# Lesson 16 - Strings Methods (Part 4)
# Source: Elzero Python Course (Arabic) - Lesson #016
# Topic: replace(), join()
# Type: Theory + Practical Code

# ============================================================
# replace(Old Value, New Value, Count)
# ============================================================
# Replaces the Old Value with the New Value in the string.
# Count (optional) -> how many times to replace (from left).
# If Count is not given, it replaces ALL occurrences.

a = "Hello One Two Three One One"
print(a.replace("One", "1"))
# Output: Hello 1 Two Three 1 1

print(a.replace("One", "1", 1))
# Output: Hello 1 Two Three One One

print(a.replace("One", "1", 2))
# Output: Hello 1 Two Three 1 One

print("=" * 50)

# ============================================================
# join(Iterable)
# ============================================================
# Joins the elements of an Iterable (list, tuple, etc.)
# into ONE string, using the Separator (the string before .join)
# between each element.

myList = ["Osama", "Mohamed", "Elsayed"]

# Join with "-" separator
print("-".join(myList))
# Output: Osama-Mohamed-Elsayed

# Join with space separator
print(" ".join(myList))
# Output: Osama Mohamed Elsayed

# Join with ", " separator
print(", ".join(myList))
# Output: Osama, Mohamed, Elsayed

# Check the type of the result (it is a String)
print(type(", ".join(myList)))
# Output: <class 'str'>

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] replace(old, new, count) -> replace old value with new
#     value, count times (optional, default = all).
# [2] join(iterable) -> join list/tuple elements into one
#     string using the separator before .join().

# ============================================================
# NEXT LESSON: Format (String Formatting)
# ============================================================
