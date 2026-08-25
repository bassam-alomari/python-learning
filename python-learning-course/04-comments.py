# Lesson 04 - Comments
# Source: Elzero Python Course (Arabic)
# Topic: Comments - How to write them, when to use them
# Type: Code + Theory

# ============================================================
# WHAT IS A COMMENT?
# ============================================================
# A comment is text that Python IGNORES completely
# It is ONLY for humans to read
# Use # to write a comment

# This is a comment - Python skips this line
print("This runs")  # Python executes this

# ============================================================
# TYPES OF COMMENTS
# ============================================================

# [1] Single Line Comment
# This comment is on its own line

# [2] Inline Comment (same line as code)
print("Hello")  # This prints hello

# [3] Multi Line Comment (use # on each line)
# This is line 1 of the comment
# This is line 2 of the comment
# This is line 3 of the comment

# ============================================================
# FILE HEADER (Best Practice)
# ============================================================
# Always start your files with a header comment:
#
# # File: my_script.py
# # Author: Bassam Alomari
# # Date: 2026-08-25
# # Description: This script does XYZ

# ============================================================
# COMMENTING OUT CODE
# ============================================================
# You can "disable" code by turning it into a comment
# This is useful for debugging

# print("This line is commented out - will NOT run")
# x = 10
# print(x)

print("This line RUNS because it is NOT commented")

# ============================================================
# GOOD vs BAD Comments
# ============================================================

# BAD (useless comment - states the obvious):
# print("Hello")  # This prints Hello

# GOOD (useful comment - explains WHY):
# We use print here to show the result to the user
print("Hello")

# GOOD (warning comment - alert your team):
# WARNING: Do NOT change this function - it breaks the API
def get_data():
    return "important data"

# GOOD (explaining complex logic):
# This formula converts temperature from Celsius to Fahrenheit
# Formula: (C * 9/5) + 32
celsius = 100
fahrenheit = (celsius * 9/5) + 32

# ============================================================
# VS CODE SHORTCUTS
# ============================================================
# Windows/Linux: Ctrl + /  (toggle comment)
# Mac: Cmd + /  (toggle comment)
# Select multiple lines, then press the shortcut

# ============================================================
# KEY RULES
# ============================================================
# [1] Comments are ignored by Python
# [2] Use # for single line comments
# [3] Comment WHAT and WHY, not WHAT (the code already shows that)
# [4] Keep comments short and useful
# [5] Remove old comments that are no longer relevant
# [6] Comment complex logic for other developers

# ============================================================
# EXERCISE: Try commenting out code
# ============================================================
print("Line 1: This runs")
# print("Line 2: This is commented out")
print("Line 3: This runs too")
# x = 5
# print(x)
