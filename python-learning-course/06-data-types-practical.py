# Lesson 06 - Data Types (Practical)
# Source: Elzero Python Course (Arabic)
# Topic: Data Types Overview with type() Function
# Type: Theory + Practical Code

# ============================================================
# KEY FACT: ALL DATA IN PYTHON IS AN OBJECT
# ============================================================
# Every piece of data in Python is an Object.
# We will see how we interact with their properties
# throughout this course.

# ============================================================
# THE type() FUNCTION
# ============================================================
# type() is a built-in function that tells you
# what data type you are working with.

# Example:
print(type(10))        # <class 'int'>
print(type(9.5))       # <class 'float'>
print(type("Hello"))   # <class 'str'>
print(type([1, 2, 3])) # <class 'list'>
print(type((1, 2, 3))) # <class 'tuple'>
print(type({"one": 1}))# <class 'dict'>
print(type(True))      # <class 'bool'>

print("=" * 50)

# ============================================================
# [1] INTEGER (int) - Whole Numbers
# ============================================================
# Positive or negative numbers WITHOUT decimal points.

a = 10
b = 100
c = -50

print(type(a))  # <class 'int'>
print(type(b))  # <class 'int'>
print(type(c))  # <class 'int'>
print(a)        # 10
print(b)        # 100
print(c)        # -50

print("=" * 50)

# ============================================================
# [2] FLOAT - Decimal Numbers
# ============================================================
# Numbers that HAVE a decimal point.

x = 9.5
y = 1.5
z = -100.5

print(type(x))  # <class 'float'>
print(type(y))  # <class 'float'>
print(type(z))  # <class 'float'>
print(x)        # 9.5
print(y)        # 1.5
print(z)        # -100.5

print("=" * 50)

# ============================================================
# [3] STRING (str) - Text
# ============================================================
# Anything inside quotes (single or double).

name = "Bassam"
greeting = 'Hello World'
empty = ""

print(type(name))      # <class 'str'>
print(type(greeting))  # <class 'str'>
print(type(empty))     # <class 'str'>
print(name)            # Bassam
print(greeting)        # Hello World

print("=" * 50)

# ============================================================
# [4] LIST - Mutable Collection []
# ============================================================
# A group of items inside square brackets [].
# Can be modified after creation (add, remove, change items).

my_list = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "Hello", 3.5, True]

print(type(my_list))  # <class 'list'>
print(type(fruits))   # <class 'list'>
print(type(mixed))    # <class 'list'>
print(my_list)        # [1, 2, 3, 4, 5]
print(fruits)         # ['apple', 'banana', 'cherry']
print(mixed)          # [1, 'Hello', 3.5, True]

print("=" * 50)

# ============================================================
# [5] TUPLE - Immutable Collection ()
# ============================================================
# Similar to list but inside normal parentheses ().
# CANNOT be modified after creation.

my_tuple = (1, 2, 3, 4, 5)
colors = ("red", "green", "blue")

print(type(my_tuple))  # <class 'tuple'>
print(type(colors))    # <class 'tuple'>
print(my_tuple)        # (1, 2, 3, 4, 5)
print(colors)          # ('red', 'green', 'blue')

print("=" * 50)

# ============================================================
# [6] DICTIONARY (dict) - Key:Value Pairs {}
# ============================================================
# Uses curly braces {} with key-value pairs.
# Like a real dictionary: word (key) -> meaning (value).

my_dict = {"one": 1, "two": 2, "three": 3}
person = {"name": "Bassam", "age": 21, "major": "CS"}

print(type(my_dict))  # <class 'dict'>
print(type(person))   # <class 'dict'>
print(my_dict)        # {'one': 1, 'two': 2, 'three': 3}
print(person)         # {'name': 'Bassam', 'age': 21, 'major': 'CS'}

print("=" * 50)

# ============================================================
# [7] BOOLEAN (bool) - True or False
# ============================================================
# Only two possible values: True or False
# Result of comparison operations.

x = True
y = False

print(type(x))  # <class 'bool'>
print(type(y))  # <class 'bool'>
print(x)        # True
print(y)        # False

# Comparisons produce booleans:
print(2 == 2)   # True
print(2 == 4)   # False
print(2 > 1)    # True
print(2 < 1)    # False
print(2 != 2)   # False

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] int      -> whole numbers: 10, -50, 100
# [2] float    -> decimal numbers: 9.5, -100.5
# [3] str      -> text: "Hello", 'World'
# [4] list     -> mutable collection: [1, 2, 3]
# [5] tuple    -> immutable collection: (1, 2, 3)
# [6] dict     -> key-value pairs: {"one": 1}
# [7] bool     -> True or False
#
# Use type() to check any data type at any time.
# Each type will be covered in detail in future lessons.

# ============================================================
# NEXT LESSON: Strings (Part 1) - Full Details
# ============================================================
