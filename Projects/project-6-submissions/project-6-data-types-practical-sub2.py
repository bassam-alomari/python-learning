# ============================================================
# PROJECT 6 - Data Types Practical & type() (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04 + 05 + 06)
# Topics: Introduction, Setup, print(), Comments, Data Types, type()
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
#  3 - It works on any platform)

# QUESTION 2: Interpreter vs Compiler (Lesson 01)
# What is the difference? Which one is Python?
# (An interpreter reads the code line by line and executes it line by line;
#  if there is an error, the program stops at the line that has the error.
#  A compiler reads all the code first and then executes it;
#  if there is an error in any line, the whole code is not executed.
#  Python is an interpreter language, and C/C++ are compiled languages.)

# QUESTION 3: What do you need to start? (Lesson 02)
# List 4 things you need to start learning Python.
# (1 - Python itself (install it on your computer)
#  2 - An IDE / text editor (like VS Code)
#  3 - Knowledge of programming basics
#  4 - Practice and continuity)

# QUESTION 4: Indentation (Lesson 03)
# What does Python use instead of curly braces {} ?
# (Python uses spaces instead of curly braces {}.
#  You should use 4 spaces for indentation.
#  If you indent wrong, you get a syntax error.)

# QUESTION 5: Comments (Lesson 04)
# What are the 3 types of comments in Python?
# (1 - Single line comment: # comment
#  2 - Inline comment: code # comment
#  3 - Multi line comment: multiple # lines)

# QUESTION 6: Data Types (Lesson 05)
# Name the 3 main data types in Python with an example of each.
# (1 - int: 10
#  2 - float: 12.2
#  3 - string: "bassam")

# QUESTION 7: type() Function (Lesson 06)
# What does type() do? Give an example.
# (type() shows the data type of the value.
#  Example: type(15) returns <class 'int'>)

# QUESTION 8: Data Types Practical (Lesson 06)
# Name 7 data types in Python and describe each one briefly.
# (1 - int: a numeric value without fractions, example: 10
#  2 - float: a numeric value with fractions, example: 10.5
#  3 - bool: a boolean value that has two choices: True or False
#  4 - string: an alphabetic value with numbers or without, example: "bassam"
#  5 - list: a collection that has multiple values, example: [1, 2, 3]
#  6 - dict: a collection that has a key and a value, example: {"one": 1}
#  7 - tuple: like a list but you cannot modify it after creation, example: (1, 2, 3))

# QUESTION 9: Strings (Lesson 06)
# Can you use single quotes and double quotes for strings?
# What is the difference?
# (Yes, you can use both single quotes ' ' and double quotes " ".
#  There is no difference between them in Python.)

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
# Use type() to print the type of the number 10
print(type(10))

# TASK 2: Print type() of a string
# Use type() to print the type of "Hello"
print(type("Hello"))

# TASK 3: Print type() of a float
# Use type() to print the type of 9.5
print(type(9.5))

# TASK 4: Print type() of a boolean
# Use type() to print the type of True
print(type(True))

# TASK 5: Print type() of a list
# Use type() to print the type of [1, 2, 3]
print(type([1, 2, 3]))

# TASK 6: Print type() of a tuple
# Use type() to print the type of (1, 2, 3)
print(type((1, 2, 3)))

# TASK 7: Print type() of a dictionary
# Use type() to print the type of {"one": 1}
print(type({"one": 1}))

# TASK 8: Compare two numbers
# Use == and != to compare 5 and 10, print both results
print(5 == 10)
print(5 != 10)

# ============================================================
# END OF PROJECT 6
# ============================================================