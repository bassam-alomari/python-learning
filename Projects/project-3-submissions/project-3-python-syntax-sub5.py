# ============================================================
# PROJECT 3 - Python Syntax & First Program (FINAL EXPANDED)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04)
# Topics used: Introduction, Setup, print(), Comments, Indentation,
#              Errors, Semicolons
#
# INSTRUCTIONS:
# This project has BOTH theory questions (answer as comments with #)
# AND code tasks (write actual Python code).
#
# FINAL EDITION (sub5): Expanded theory answers + BONUS code
# ============================================================

# ------------------------------------------------------------
# PART A - EXPANDED THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: What is Python? (Lesson 01)
# Write 3 things that make Python special.
# (Python is an interpreter programming language. It is special because:
#  1 - It is easy to learn
#  2 - It is easy to setup
#  3 - It works on any platform
#  4 - It has many libraries that save you time)

# QUESTION 2: Interpreter vs Compiler (Lesson 01)
# Explain the difference. Which one is Python?
# (An interpreter reads the code line by line and executes it line by line;
#  if there is an error, the program stops at the line that has the error.
#  A compiler reads all the code first and then executes it;
#  if there is an error in any line, the whole code is not executed.
#  Python is an interpreter language.
#  C and C++ are examples of compiled languages.)

# QUESTION 3: What do you need to start? (Lesson 02)
# List 4 things you need to start learning Python.
# (1 - Python itself (install it on your computer)
#  2 - An IDE / text editor (like VS Code)
#  3 - Knowledge of programming basics
#  4 - Practice and continuity)

# QUESTION 4: Python Installation (Lesson 02)
# When installing Python on Windows, what is the IMPORTANT
# option you MUST check? Why is it important?
# (You MUST check "Add Python to PATH".
#  It is important because it lets you run the python command
#  from the terminal from anywhere on your computer.)

# QUESTION 5: Indentation (Lesson 03)
# What does Python use instead of curly braces {} ?
# What error do you get if you indent wrong?
# (Python uses spaces instead of curly braces {}.
#  You should use 4 spaces for indentation.
#  If you indent wrong, you get a syntax error,
#  for example: IndentationError: expected an indented block)

# QUESTION 6: Comments (Lesson 04)
# What are the 3 types of comments in Python?
# (1 - Single line comment: # comment
#  2 - Inline comment: code # comment
#  3 - Multi line comment: multiple # lines)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Hello World
print("Hello, World!")

# TASK 2: Print your name
print("Bassam Alomari")

# TASK 3: Print the result of 10 + 6
print(10 + 6)

# TASK 4: Print the result of 10 / 4
print(10 / 4)

# TASK 5: Fixed indentation - correct the indentation error below

# def say_hello():
# print("Hello")   # <-- this line needs indentation

def say_hello():
    print("Hello")

# ------------------------------------------------------------
# PART C - BONUS PRACTICAL CODE (final edition bonus)
# ------------------------------------------------------------
# These extra tasks run real code to prove you understand
# the setup, print(), type() and reserved keywords.

# BONUS 1: Print type() of an integer
print(type(10))

# BONUS 2: Print type() of a float
print(type(10.7))

# BONUS 3: Print type() of a string
print(type("Bassam"))

# BONUS 4: Print type() of a boolean
print(type(True))

# BONUS 5: Use the keyword module to print all reserved words
import keyword
print(keyword.kwlist)

# BONUS 6: Check if "if" is a reserved keyword
print(keyword.iskeyword("if"))

# ============================================================
# END OF PROJECT 3 - FINAL EXPANDED EDITION (sub5)
# ============================================================