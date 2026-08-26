# Lesson 07 - Variables (Fundamentals)
# Source: Elzero Python Course (Arabic)
# Topic: What are Variables + Naming Rules + Naming Conventions
# Type: Theory + Practical Code

# ============================================================
# WHAT IS A VARIABLE?
# ============================================================
# Imagine a game that asks for your name and shows it
# throughout the game (welcome message, score, etc.)
#
# The VARIABLE is what STORES your name.
# It changes based on who is playing.
#
# In programming:
# When you write code, the computer reserves a BOX in memory
# to store data. The variable is the NAME (reference/pointer)
# that takes you to that box.
#
# Think of it like:
# - Memory = a shelf with many boxes
# - Data = what is inside a box
# - Variable = a label on the box that tells you what is inside
#
# The variable does NOT hold the data directly.
# It is just a REFERENCE that points to where the data lives
# in the computer's memory.

# ============================================================
# CREATING A VARIABLE (Assignment)
# ============================================================
# Syntax: variable_name = value
#
# Python makes this very easy compared to other languages.
# Just write the name and assign a value directly.

name = "Bassam"
age = 21
height = 1.75
is_student = True

print(name)        # Bassam
print(age)         # 21
print(height)      # 1.75
print(is_student)  # True

print("=" * 50)

# ============================================================
# NAMING RULES (5 Rules - MUST Follow)
# ============================================================

# RULE 1: Must start with a LETTER (a-z, A-Z) or UNDERSCORE (_)
#         CANNOT start with a NUMBER

my_name = "Ahmad"    # Valid
_name = "Sara"       # Valid
__name = "Ali"       # Valid (double underscore)
# 2age = 25          # INVALID - starts with number

print(my_name)  # Ahmad
print(_name)    # Sara

# RULE 2: Cannot start with a SPACE or certain symbols
#         Will cause a SyntaxError

# my name = "Ali"    # INVALID - contains space
# my-name = "Ali"    # INVALID - contains dash
# my@name = "Ali"    # INVALID - contains @

# RULE 3: Can use NUMBERS (0-9) and UNDERSCORE in the MIDDLE or END
#         But NOT at the beginning

name2 = "Ahmad"     # Valid - number at the end
na_me = "Sara"      # Valid - underscore in the middle
name_2 = "Ali"      # Valid - number after underscore

print(name2)  # Ahmad
print(na_me)  # Sara
print(name_2) # Ali

# RULE 4: Cannot use SPECIAL SYMBOLS (@, $, %, #, etc.)

# my$name = "Ali"    # INVALID
# my%name = "Ali"    # INVALID
# my#name = "Ali"    # INVALID

# RULE 5: Python is CASE-SENSITIVE
#         name, Name, and NAME are THREE DIFFERENT variables

name = "Bassam"
Name = "Ahmad"
NAME = "Sara"

print(name)  # Bassam
print(Name)  # Ahmad
print(NAME)  # Sara

print("=" * 50)

# ============================================================
# IMPORTANT: Assign BEFORE Using
# ============================================================
# You MUST create (assign) a variable BEFORE you use it.
# Otherwise, Python will give you a NameError.

greeting = "Hello"
print(greeting)  # Hello

# print(unknown_variable)  # NameError: name 'unknown_variable' is not defined

print("=" * 50)

# ============================================================
# NAMING CONVENTIONS (Multi-Word Variables)
# ============================================================
# When a variable name has more than one word,
# use one of these two styles:

# Style 1: snake_case (RECOMMENDED in Python)
# Separate words with underscore _
first_name = "Bassam"
last_name = "Alomari"
my_full_name = "Bassam Alomari"

print(first_name)   # Bassam
print(last_name)    # Alomari
print(my_full_name) # Bassam Alomari

# Style 2: camelCase (used in some other languages)
# First word lowercase, next words start with capital
firstName = "Ahmad"
lastName = "Ali"
myFullName = "Ahmad Ali"

print(firstName)   # Ahmad
print(lastName)    # Ali
print(myFullName)  # Ahmad Ali

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] Variable = a NAME that refers to data in memory
# [2] Create with: variable_name = value
# [3] Naming Rules:
#     - Start with letter or _
#     - Can use numbers and _ in middle/end
#     - No special symbols (@, $, %, etc.)
#     - Case-sensitive (name != Name != NAME)
#     - Assign before using
# [4] Naming Conventions:
#     - snake_case (Python recommended): first_name
#     - camelCase (other languages): firstName

# ============================================================
# NEXT LESSON: Strings (Part 1)
# ============================================================
