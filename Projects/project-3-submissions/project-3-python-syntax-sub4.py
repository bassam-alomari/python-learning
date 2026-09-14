# ============================================================
# PROJECT 3 - Python Syntax & First Program (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03)
# Topics used: Introduction, Setup, print(), Indentation, Errors
#
# INSTRUCTIONS:
# This project has BOTH theory questions (answer as comments)
# AND code tasks (write actual Python code).
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer as comments with #)
# ------------------------------------------------------------

# QUESTION 1: What is Python? (from Lesson 01)
# In your own words, write what Python is.
# Mention at least 3 things that make Python special.
#
# Write your answer below:

# (Python is an interpreter programming language
#  that was created to be simple and powerful.
#  It is special because:
#  1 - It is easy to learn, even for beginners
#  2 - It is easy to setup: install it and start coding
#  3 - It works on any platform: Windows, Mac, Linux
#  4 - It has many libraries that save you time)


# QUESTION 2: Interpreter vs Compiler (from Lesson 01)
# Explain the difference between an Interpreter and a Compiler.
# Which one is Python?
#
# Write your answer below:

# (Interpreter:
#  - Reads the code line by line and executes it line by line.
#  - If there is an error in a line, the program stops
#    at that line and does not continue.
#
#  Compiler:
#  - Reads all the code first, then executes it.
#  - If there is an error in any line,
#    the whole code is not executed.
#
#  Python is an interpreter language,
#  and C/C++ are compiled languages.)


# QUESTION 3: What do you need to start? (from Lesson 02)
# List the 4 MOST IMPORTANT things you need to start
# learning Python.
#
# Write your answer below:

# (1 - Python itself: install it on your computer
#  2 - An IDE / text editor: like VS Code
#  3 - Knowledge of programming basics
#  4 - Practice and continuity: code every day)


# QUESTION 4: Python Installation (from Lesson 02)
# When installing Python on Windows, what is the IMPORTANT
# option you MUST check? Why is it important?
#
# Write your answer below:

# (You MUST check "Add Python to PATH".
#  It is important because it lets you run the python command
#  from the terminal from anywhere on your computer,
#  without going to the Python folder every time.)


# QUESTION 5: Indentation (from Lesson 03)
# What does Python use instead of curly braces {} ?
# How many spaces should you use for indentation?
# What error do you get if you indent wrong?
#
# Write your answer below:

# (Python uses spaces instead of curly braces {}.
#  You should use 4 spaces for indentation.
#  If you indent wrong, you get a syntax error,
#  for example: IndentationError: expected an indented block)


# QUESTION 6: Semicolons (from Lesson 03)
# Does Python need semicolons at the end of lines?
# When can you use a semicolon?
#
# Write your answer below:

# (No, Python does not need semicolons at the end of lines.
#  You can use a semicolon to write more than one statement
#  on the same line, for example: print("A"); print("B")
#  But it is better to write each statement on its own line,
#  because it makes the code cleaner and easier to read.)


# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Hello World
# Write a print() statement that prints: Hello, World!
# Write your code below:

print("Hello, World!")


# TASK 2: Print your name
# Write a print() statement that prints your full name.
# Write your code below:

print("Bassam Alomari")


# TASK 3: Print multiple things
# Use print() to print your first name and last name
# as TWO separate arguments (separated by a comma).
# Write your code below:

print("Bassam", "Alomari")


# TASK 4: Print a number
# Use print() to print the result of 10 + 5.
# Write your code below:

print(10 + 5)


# TASK 5: Semicolons
# Write TWO print() statements on ONE line using a semicolon.
# Write your code below:

print("Bassam"); print("Alomari")


# TASK 6: Fix the indentation
# The code below has an indentation error.
# Fix it so it runs correctly (add the missing spaces).
# Write your fixed code below:

# def say_hello():
# print("Hello from a function!")   # <-- this line needs indentation

def say_hello():
    print("Hello from a function!")


# ============================================================
# END OF PROJECT 3
# ============================================================