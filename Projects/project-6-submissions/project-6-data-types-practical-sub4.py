# ============================================================
# PROJECT 6 - Data Types & type() Practical (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04 + 05 + 06)
# Topics: Introduction, Setup, print(), Comments, Data Types,
#         type()
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: What is Python? (Lesson 01)
# Write 3 things that make Python special.
# (Python is an interpreter programming language. It is special because:
#  1 - It is easy to learn
#  2 - It is easy to setup
#  3 - It works on any platform
#  4 - It has many libraries that save you time)

# QUESTION 2: Interpreter vs Compiler (Lesson 01)
# What is the difference? Which one is Python?
# (An interpreter reads the code line by line and executes it line by line;
#  if there is an error in a line, the program stops at that line.
#  A compiler reads all the code first and then executes it;
#  if there is an error in any line, the whole code is not executed.
#  Python is an interpreter language, and C/C++ are compiled languages.)

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
#  It is important because it lets you run the "python" command
#  from the terminal from anywhere on your computer,
#  without going to the Python folder every time.)

# QUESTION 5: Indentation (Lesson 03)
# What does Python use instead of curly braces {} ?
# What error do you get if you indent wrong?
# (Python uses spaces instead of curly braces {}.
#  You should use 4 spaces for indentation.
#  If you indent wrong, you get a syntax error.)

# QUESTION 6: Comments (Lesson 04)
# What are the 3 types of comments in Python?
# (1 - Single line comment: # comment
#  2 - Inline comment: code # comment
#  3 - Multi line comment: multiple # lines)

# QUESTION 7: Data Types (Lesson 05)
# Name 3 main data types in Python with an example of each.
# (1 - int: 10
#  2 - float: 12.2
#  3 - string: "bassam")

# QUESTION 8: type() Function (Lesson 06)
# What does type() do? Give an example.
# (type() shows the data type of the value.
#  Example: type(15) returns <class 'int'>)

# QUESTION 9: Practical Data Types (Lesson 06)
# List 7 data types in Python with an example of each.
# (1 - int: 10
#  2 - float: 10.5
#  3 - bool: True
#  4 - string: "bassam"
#  5 - list: [1, 2, 3]
#  6 - tuple: (1, 2, 3)
#  7 - dict: {"one": 1})

# QUESTION 10: Booleans (Lesson 06)
# What are the only two values of a Boolean?
# What does 2 == 2 return? What does 2 != 2 return?
# (The only two values are True and False.
#  2 == 2 returns True.
#  2 != 2 returns False.)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Print type() of an integer
print(type(10))

# TASK 2: Print type() of a string
print(type("Hello"))

# TASK 3: Print type() of a float
print(type(9.5))

# TASK 4: Print type() of a boolean
print(type(True))

# TASK 5: Print type() of a list
print(type([1, 2, 3]))

# TASK 6: Print type() of a tuple
print(type((1, 2, 3)))

# TASK 7: Print type() of a dictionary
print(type({"one": 1}))

# TASK 8: Compare two numbers
# Use == and != to compare 5 and 10, print both results
print(5 == 10)
print(5 != 10)

# ============================================================
# END OF PROJECT 6
# ============================================================