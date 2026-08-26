# Lesson 03 - Python Syntax + First Program
# Source: Elzero Python Course (Arabic)
# Topic: print(), Running Code, Indentation, Errors
# Type: Code + Theory

# ============================================================
# THE print() FUNCTION
# ============================================================
# print() is the first function you learn
# It outputs/displays text on the screen
# You will use it everywhere until advanced lessons

# Hello World - your first Python program
print("Hello, World!")

# Print multiple things
print("Hello", "Bassam")
print("Hello" + "Bassam")  # concatenation

# ============================================================
# RUNNING CODE IN VS CODE
# ============================================================
# Method 1: Terminal
#   - Open terminal in VS Code
#   - Type: python filename.py
#
# Method 2: Green Play Button
#   - Click the green "Run" button in VS Code
#   - It runs the file automatically in the terminal
#
# Method 3: Keyboard Shortcut
#   - Press Ctrl + F5 to run without debugging

# ============================================================
# SEMICOLONS
# ============================================================
# Python does NOT need semicolons at end of lines
# But you CAN use semicolons to put two commands on one line

# These are the same:
print("Hello")
print("World")

# This also works (semicolons as separator):
print("Hello"); print("World")

# ============================================================
# INDENTATION (Very Important!)
# ============================================================
# Python uses SPACES (indentation) instead of curly braces {}
# This is how Python knows which code belongs to which block

# WRONG - will cause IndentationError:
# def greet():
# print("Hello")  # ERROR! Missing indentation

# CORRECT:
def greet():
    print("Hello")  # Indented with 4 spaces

# Indentation rules:
# - Use 4 spaces (recommended) or 1 tab
# - Be CONSISTENT - don't mix tabs and spaces
# - Wrong indentation = IndentationError

# ============================================================
# INDENTATION ERROR
# ============================================================
# If you indent wrong, Python gives you a clear error:
#
# IndentationError: expected an indented block
#
# The error tells you EXACTLY which line has the problem
# Python errors are very helpful - read them carefully!

# ============================================================
# KEY POINTS
# ============================================================
# [1] print() displays output on screen
# [2] Python does NOT need semicolons
# [3] Python uses INDENTATION (spaces) not curly braces
# [4] Wrong indentation = IndentationError
# [5] Always read error messages - they tell you the problem
# [6] Use 4 spaces for indentation (standard)

# ============================================================
# EXERCISE: Try these yourself!
# ============================================================
print("Exercise 1: Hello Python!")
print("Exercise 2:", 1 + 2)
print("Exercise 3: " + "Bassam" + " " + "Alomari")

# ============================================================
# NEXT LESSON: Comments
# ============================================================
