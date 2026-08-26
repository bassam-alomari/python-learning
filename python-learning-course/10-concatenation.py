# Lesson 10 - String Concatenation
# Source: Elzero Python Course (Arabic)
# Topic: Joining Strings Together
# Type: Theory + Practical Code

# ============================================================
# WHAT IS CONCATENATION?
# ============================================================
# Concatenation = joining two or more strings together
# to create a bigger string.
#
# In Python, we use the + operator to concatenate strings.

# ============================================================
# BASIC CONCATENATION
# ============================================================

a = "Hello"
b = "World"

# Join them with +
c = a + b
print(c)    # HelloWorld (no space!)

# The result is a new string: "Hello" + "World" = "HelloWorld"

print("=" * 50)

# ============================================================
# ADDING SPACES BETWEEN STRINGS
# ============================================================
# The + operator does NOT add spaces automatically.
# You must add spaces yourself.

# Method 1: Space inside the string
a = "Hello "
b = "World"
print(a + b)    # Hello World

# Method 2: Space at the beginning of second string
a = "Hello"
b = " World"
print(a + b)    # Hello World

# Method 3: Add a space string between them
a = "Hello"
b = "World"
print(a + " " + b)    # Hello World

# Method 4: Store space in a variable
space = " "
a = "Hello"
b = "World"
print(a + space + b)  # Hello World

print("=" * 50)

# ============================================================
# CONCATENATION WITH MULTIPLE STRINGS
# ============================================================

first_name = "Bassam"
middle = " "
last_name = "Alomari"

full_name = first_name + middle + last_name
print(full_name)  # Bassam Alomari

# Building a sentence
greeting = "Hello"
name = "Bassam"
exclamation = "!"

message = greeting + " " + name + exclamation
print(message)  # Hello Bassam!

print("=" * 50)

# ============================================================
# CONCATENATION WITH VARIABLES ON MULTIPLE LINES
# ============================================================
# You can split long strings across multiple lines.

line1 = "This is line one. "
line2 = "This is line two. "
line3 = "This is line three."

full_text = line1 + line2 + line3
print(full_text)

print("=" * 50)

# ============================================================
# ERROR: Cannot Concatenate String with Number
# ============================================================
# You CANNOT use + to join a string and a number directly.

# This will cause a TypeError:
# print("Hello" + 1)    # TypeError: can only concatenate str to str

# To fix this, convert the number to string first using str()
print("Hello" + str(1))    # Hello1
print("Score: " + str(100))  # Score: 100

print("=" * 50)

# ============================================================
# CONCATENATION vs f-strings
# ============================================================
# f-strings are often EASIER than using + for combining
# variables with strings.

name = "Bassam"
age = 21

# Using concatenation (with +)
message1 = "My name is " + name + " and I am " + str(age) + " years old"
print(message1)

# Using f-string (easier!)
message2 = f"My name is {name} and I am {age} years old"
print(message2)

# Both produce the same output, but f-strings are cleaner.

print("=" * 50)

# ============================================================
# PRACTICE EXERCISES
# ============================================================

# Exercise 1: Build a full name
first = "Bassam"
last = "Alomari"
full = first + " " + last
print(f"Full Name: {full}")

# Exercise 2: Create an address
street = "123 Main St"
city = "Irbid"
country = "Jordan"
address = street + ", " + city + ", " + country
print(f"Address: {address}")

# Exercise 3: Build a URL
protocol = "https://"
domain = "github.com"
username = "/bassam-alomari"
url = protocol + domain + username
print(f"URL: {url}")

# ============================================================
# SUMMARY
# ============================================================
# [1] Concatenation = joining strings with + operator
# [2] + does NOT add spaces automatically
# [3] Add spaces manually: " " or variable
# [4] CANNOT concatenate string + number directly
#     Use str() to convert number to string first
# [5] f-strings are often easier than + for mixing variables

# ============================================================
# NEXT LESSON: Strings - Ways to Write
# ============================================================
