# ============================================================
# PROJECT 2 - Python Setup & Introduction (ULTIMATE EXPANDED + BONUS)
# ============================================================
# Level: Beginner (Lessons 01 + 02 - Theory + Practical BONUS)
# Topics: What is Python, Why Python, Setup, Installation, IDE,
#         PATH, Python 2 vs 3, Career Paths, Key Terms
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B (BONUS): Write actual Python code that RUNS
# PART C (EXTRA): Advanced bonus challenges
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: What is Python? (Lesson 01)
# Write 3 things that make Python special.
# (Python is an interpreter programming language. It is special because:
#  1 - It is easy to learn and read (the code reads like English)
#  2 - It is easy to setup (install + start coding the same day)
#  3 - It works on any platform (Windows, Mac, Linux)
#  4 - It has many libraries that save you time and effort
#  5 - It has a huge community for support)

# QUESTION 2: Interpreter vs Compiler (Lesson 01)
# What is the difference? Which one is Python?
# Give an example of a compiled language.
# (An interpreter reads the code line by line and executes it
#  line by line; if there is an error, the program stops at
#  the line that has the error.
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

# QUESTION 4: Python Installation - IMPORTANT (Lesson 02)
# On Windows, what is the IMPORTANT option you MUST check?
# Why is it important?
# (You MUST check "Add Python to PATH".
#  It is important because it lets you run the python command
#  from the terminal from anywhere on your computer,
#  without going to the Python folder every time.)

# QUESTION 5: IDE (Lesson 02)
# What does IDE stand for? Name 2 IDEs/editors.
# Which one is recommended in the course?
# (IDE stands for Integrated Development Environment.
#  It is a text editor for writing code with helpful tools.
#  Examples: 1 - VS Code  2 - PyCharm
#  The recommended one in the course is VS Code,
#  because it is free, light and supports many languages.)

# QUESTION 6: Python Version (Lesson 02)
# Should you use Python 2 or Python 3? Why?
# (You should use Python 3,
#  because Python 2 is no longer supported
#  and stopped getting updates.
#  So all new code and libraries work with Python 3.)

# QUESTION 7: Career Paths (Lesson 02)
# Name 4 career paths that Python can lead to.
# Which one interests you the most? Why?
# (1 - Web Development
#  2 - Data Science / Artificial Intelligence
#  3 - Game Development
#  4 - Automation / Scripting
#  Web Development interests me the most,
#  because I want to build real websites
#  that people use every day.)

# QUESTION 8: Key Terms (Lesson 01)
# Explain these 3 terms in your own words:
#   1) Garbage Collection
#   2) OOP (Object-Oriented Programming)
#   3) Modules & Packages
# (1 - Garbage Collection:
#     Python cleans the memory automatically.
#     When data is no longer used, Python removes it,
#     so you do not need to delete it yourself.
#  2 - OOP (Object-Oriented Programming):
#     A way of organizing code using objects
#     that have data and actions. We will learn it later.
#  3 - Modules & Packages:
#     Ready-made code that you import and use,
#     like a toolbox. You do not write everything
#     from scratch, you reuse what others built.)

# QUESTION 9: Companies that use Python (Lesson 01)
# Name 4 companies that use Python.
# (1 - NASA
#  2 - Google
#  3 - Instagram
#  4 - Spotify)

# ============================================================
# PART B - BONUS CODE (write code that actually RUNS)
# ============================================================
# These bonus tasks prove that your Python setup works.
# If these run, your setup is 100% correct!
# ============================================================

# BONUS 1: Hello World
print("Hello World")

# BONUS 2: Print a string with your name
print("Bassam Alomari")

# BONUS 3: Print the result of 20 + 30
print(20 + 30)

# BONUS 4: Print the result of 10 / 3
print(10 / 3)

# BONUS 5: Print a boolean value (True)
print(True)

# BONUS 6: Use type() to print the type of 15
print(type(15))

# BONUS 7: Print the type of a string "Hello"
print(type("Hello"))

# BONUS 8: Create a variable with your name and print it
my_name = "Bassam Alomari"
print(my_name)

# BONUS 9: Use the keyword module to print all reserved keywords
import keyword
print(keyword.kwlist)

# BONUS 10: Check if "if" is a reserved keyword
import keyword
print(keyword.iskeyword("if"))

# ============================================================
# PART C - EXTRA BONUS CHALLENGES (advanced)
# ============================================================

# EXTRA 1: Print type() of different data types
print(type(10))        # int
print(type(10.5))      # float
print(type(True))      # bool
print(type("text"))    # str
print(type([1,2,3]))   # list
print(type((1,2,3)))   # tuple
print(type({"a":1}))   # dict
print(type({1,2,3}))   # set

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

# ============================================================
# END OF PROJECT 2 - ULTIMATE EXPANDED EDITION (sub6)
# ============================================================