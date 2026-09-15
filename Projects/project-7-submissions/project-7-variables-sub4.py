# ============================================================
# PROJECT 7 - Variables & Fundamentals (EXPANDED Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04 + 05 + 06 + 07)
# Topics: Introduction, Setup, print(), Comments, Data Types,
#         type(), Variables
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# ============================================================
# Student: Bassam Alomari
# Date: 2026/9/8
# ============================================================

# ------------------------------------------------------------
# PART A - EXPANDED THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: What is Python? (Lesson 01)
# Write 3 things that make Python special.
# (Python is an interpreter programming language. It is special because:
#  1 - It is easy to learn: the syntax is simple and clear
#  2 - It is easy to setup: install it and start coding the same day
#  3 - It works on any platform: Windows, Mac and Linux
#  4 - It has a huge community and many libraries that save you time)

# QUESTION 2: Interpreter vs Compiler (Lesson 01)
# What is the difference? Which one is Python?
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
# Name the 8 main data types in Python with an example of each.
# (1 - int: 10
#  2 - float: 12.2
#  3 - bool: True
#  4 - string: "bassam"
#  5 - list: [1, 2, 3]
#  6 - tuple: (1, 2, 3)
#  7 - dict: {"one": 1, "two": 2}
#  8 - set: {1, 2, 3})

# QUESTION 8: type() Function (Lesson 06)
# What does type() do? Give an example.
# (type() shows the data type of the value.
#  Example: type(15) returns <class 'int'>)

# QUESTION 9: What is a Variable? (Lesson 07)
# Explain what a variable is. Does it hold the data directly?
# (A variable is something that points to a place in memory
#  that holds the data. It is NOT the data itself,
#  it is a reference to the data.)

# QUESTION 10: Naming Rules (Lesson 07)
# List 4 rules for naming variables in Python.
# (1 - Do not use spaces in the name
#  2 - Do not start the name with a number
#  3 - Only use letters, numbers and underscore _
#  4 - Do not use special characters like ! @ # $ %)

# QUESTION 11: Naming Conventions (Lesson 07)
# What is snake_case? What is camelCase?
# Which one is recommended in Python?
# (snake_case: words separated by underscore, example: my_name
#  camelCase: first word lowercase, then the next words start
#  with a capital letter, example: myName
#  snake_case is the recommended one in Python.)

# QUESTION 12: Case Sensitivity (Lesson 07)
# Are name, Name, and NAME the same variable? Why?
# (No, they are NOT the same variable,
#  because Python is case sensitive,
#  so name, Name and NAME are three different variables.)

# QUESTION 13: Assign Before Using (Lesson 07)
# What error do you get if you use a variable before assigning it?
# (You get a NameError,
#  for example: NameError: name 'x' is not defined)

# ------------------------------------------------------------
# PART B - EXPANDED CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Create a variable with your name and print it
my_name = "bassam alomari"
print(my_name)

# TASK 2: Create variables for age and height, print both
age = 21
height = 170
print(age)
print(height)

# TASK 3: Create a boolean variable and print it
b = True
print(b)

# TASK 4: Create a variable using snake_case (first_name)
first_name = "bassam"

# TASK 5: Create a variable using camelCase (firstName)
firstName = "bassam"

# TASK 6: Print type() of a variable holding a string
print(type(first_name))

# TASK 7: Print type() of a variable holding a float
my_float = 1.1
print(type(my_float))

# TASK 8: Create 3 variables (name, Name, NAME) with different
# values and print all 3 to show case sensitivity
name, Name, NAME = "bassam", "adnan", "alomari"
print(name)
print(Name)
print(NAME)

# TASK 9: Create a variable, then print it, then change its
# value and print it again
x = 1
print(x)
x = 2
print(x)

# TASK 10: Dynamic Typing - assign an int to a variable,
# print type(), then assign a string to the SAME variable,
# print type() again
v = 10
print(type(v))
v = "bassam"
print(type(v))

# TASK 11: Multiple assignment in ONE line
a, b, c = 1, 2, 3
print(a)
print(b)
print(c)

# ============================================================
# END OF PROJECT 7 - SUBMISSION 4
# ============================================================