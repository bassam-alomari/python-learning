# Lesson 08 - Variables (Theory + More Concepts)
# Source: Elzero Python Course (Arabic)
# Topic: Source Code, Compilation, Runtime, Dynamic Typing,
#        Reserved Keywords, Multiple Assignment
# Type: Theory + Practical Code

# ============================================================
# SOURCE CODE
# ============================================================
# Any code you write in any programming language
# is called Source Code.
# The computer understands it after it is translated.

# ============================================================
# COMPILATION
# ============================================================
# Compilation = converting your Source Code into
# Machine Language (the language the computer understands).
# Some languages compile the entire code BEFORE running it.
# Example: C, C++, Java

# ============================================================
# RUNTIME
# ============================================================
# Runtime = the time period during which your program
# is executing (running) the commands you wrote.

# In Python:
# The code is translated and executed STEP BY STEP
# during runtime (not all at once like compiled languages).

# ============================================================
# PYTHON IS DYNAMICALLY TYPED
# ============================================================
# This is one of the most important features of Python.
#
# Dynamically Typed Language:
# - You do NOT need to declare the type of a variable
# - A variable's type CAN CHANGE during runtime
# - No errors when you change the type
#
# Example:

x = 10            # x is an integer (int)
print(type(x))    # <class 'int'>

x = "Osama"       # x is now a string (str) - NO ERROR!
print(type(x))    # <class 'str'>

x = 3.14          # x is now a float - NO ERROR!
print(type(x))    # <class 'float'>

x = True          # x is now a boolean - NO ERROR!
print(type(x))    # <class 'bool'>

# In Python, this is completely fine.
# The variable type follows the VALUE, not the name.

print("=" * 50)

# ============================================================
# COMPARISON: PYTHON vs C (Static Typing)
# ============================================================
# In languages like C, you MUST declare the type:
#
#   int x = 10;        // x is ALWAYS an integer
#   x = "Osama";       // COMPILATION ERROR! Cannot change type
#
# Python is more flexible - it allows type changes.

# ============================================================
# RESERVED KEYWORDS IN PYTHON
# ============================================================
# Just like operating systems have reserved folder names
# that you cannot use, programming languages have
# RESERVED KEYWORDS that are reserved for the system.
#
# You CANNOT use these words as variable names.
#
# When you type a reserved keyword in Python,
# the editor changes its color automatically to
# distinguish it from regular names.

# Examples of reserved keywords:
# if, else, elif, for, while, break, continue,
# return, def, class, import, from, True, False,
# None, and, or, not, in, is, try, except, etc.

# ============================================================
# HOW TO CHECK ALL RESERVED KEYWORDS
# ============================================================
# Use the keyword module to see all reserved words.

import keyword

print("All Python Reserved Keywords:")
print(keyword.kwlist)
print(f"\nTotal reserved keywords: {len(keyword.kwlist)}")

# You can also check if a specific word is reserved:
print(f"\nIs 'if' reserved? {keyword.iskeyword('if')}")      # True
print(f"\nIs 'name' reserved? {keyword.iskeyword('name')}")  # False
print(f"\nIs 'True' reserved? {keyword.iskeyword('True')}")  # True

print("=" * 50)

# ============================================================
# MULTIPLE VARIABLE ASSIGNMENT
# ============================================================
# In other languages, you might need multiple lines:
#   int x = 1;
#   int y = 2;
#   int z = 3;
#
# In Python, you can do it in ONE line:

x, y, z = 1, 2, 3

print(x)  # 1
print(y)  # 2
print(z)  # 3

# ============================================================
# ERROR: Mismatched Assignment Count
# ============================================================
# If you assign MORE or FEWER values than variables,
# Python gives a clear error message.

# Example of error (uncomment to see):
# x, y, z = 1, 2          # ValueError: not enough values to unpack
# x, y, z = 1, 2, 3, 4    # ValueError: too many values to unpack

# Python is like a strict teacher - it tells you exactly
# how many values it expected and how many you gave.

# ============================================================
# SUMMARY
# ============================================================
# [1] Source Code = the code you write
# [2] Compilation = converting code to machine language
# [3] Runtime = the time your program is executing
# [4] Python is DYNAMICALLY TYPED - type can change freely
# [5] Reserved Keywords = special words for the system
#     - Cannot be used as variable names
#     - Check with: keyword.kwlist
# [6] Multiple Assignment: x, y, z = 1, 2, 3
#     - Must match variable count with value count

# ============================================================
# NEXT LESSON: Strings (Part 1) - Full Details
# ============================================================
