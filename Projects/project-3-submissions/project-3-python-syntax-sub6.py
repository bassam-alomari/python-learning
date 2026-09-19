# ============================================================
# PROJECT 3 - Python Syntax & First Program (ULTIMATE EXPANDED + BONUS)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04)
# Topics used: Introduction, Setup, print(), Comments, Indentation,
#              Errors, Semicolons
#
# INSTRUCTIONS:
# This project has BOTH theory questions (answer as comments with #)
# AND code tasks (write actual Python code).
#
# ULTIMATE EDITION (sub6): Expanded theory + BONUS + EXTRA challenges
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
#  4 - It has many libraries that save you time
#  5 - It has a huge community for support)

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

# QUESTION 7: Semicolons (Lesson 03)
# Does Python need semicolons at the end of lines?
# When can you use a semicolon?
# (No, Python does not need semicolons at the end of lines.
#  You can use a semicolon to write more than one statement
#  on the same line, for example: print("A"); print("B")
#  But it is better to write each statement on its own line,
#  because it makes the code cleaner and easier to read.)

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
# PART D - EXTRA BONUS CHALLENGES (advanced)
# ============================================================

# EXTRA 1: Print type() of all 8 data types
print(type(10))           # int
print(type(10.5))         # float
print(type(True))         # bool
print(type("text"))       # str
print(type([1,2,3]))      # list
print(type((1,2,3)))      # tuple
print(type({"a":1}))      # dict
print(type({1,2,3}))      # set

# EXTRA 2: Dynamic typing demonstration
x = 100
print(type(x))
x = "now a string"
print(type(x))

# EXTRA 3: Multiple assignment
a, b, c = 1, 2.5, "three"
print(a, b, c)

# EXTRA 4: Check more reserved keywords
import keyword
print(keyword.iskeyword("for"))
print(keyword.iskeyword("while"))
print(keyword.iskeyword("class"))
print(keyword.iskeyword("def"))

# EXTRA 5: Arithmetic operations
print(10 + 5)   # 15
print(10 - 5)   # 5
print(10 * 5)   # 50
print(10 / 5)   # 2.0
print(10 // 3)  # 3 (floor division)
print(10 % 3)   # 1 (modulo)
print(2 ** 3)   # 8 (power)

# EXTRA 6: String operations
name = "Bassam"
print(name.upper())
print(name.lower())
print(len(name))

# EXTRA 7: Semicolon usage (multiple statements on one line)
print("First"); print("Second"); print("Third")

# EXTRA 8: Function call with the fixed indentation
say_hello()

# ============================================================
# END OF PROJECT 3 - ULTIMATE EXPANDED EDITION (sub6)
# ============================================================