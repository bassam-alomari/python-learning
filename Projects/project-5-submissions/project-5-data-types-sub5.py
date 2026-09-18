# ============================================================
# PROJECT 5 - Data Types & Variables (FINAL EXPANDED + BONUS)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04 + 05 + 06)
# Topics: Introduction, Setup, print(), Comments, Data Types,
#         type(), Variables, Dynamic Typing, Multiple Assignment
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C (BONUS): Challenge code that runs for extra marks
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
# What is the difference? Which one is Python?
# (An interpreter reads the code line by line and executes it line by line;
#  if there is an error, the program stops at the line that has the error.
#  A compiler reads all the code first and then executes it;
#  if there is an error in any line, the whole code is not executed.
#  Python is an interpreter, and C/C++ are compiled languages.)

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
# (Python uses 4 spaces instead of curly braces {}.
#  You should use 4 spaces for indentation.
#  If you indent wrong, you get a syntax error,
#  for example: IndentationError: expected an indented block.)

# QUESTION 6: Comments (Lesson 04)
# What are the 3 types of comments in Python?
# (1 - Single line comment: # comment
#  2 - Inline comment: code # comment
#  3 - Multi line comment: multiple # lines)

# QUESTION 7: Data (Lesson 05)
# In any application, what are the TWO main parts?
# (1 - Code
#  2 - Data)

# QUESTION 8: Data Types (Lesson 05)
# Name the 4 main data types in Python with an example of each.
# (1 - int: 10
#  2 - float: 12.2
#  3 - string: "bassam"
#  4 - bool: True)

# QUESTION 9: What is a Variable? (Lesson 05)
# Is a variable the data itself or something else? Explain.
# (A variable is something that points to a place in memory
#  that holds the data. It is NOT the data itself,
#  it is a reference to the data.)

# QUESTION 10: What is a String? (Lesson 05)
# What happens when you put text inside quotes?
# What type of data is it?
# (When you put text inside single or double quotes,
#  it becomes a string data type, it is not code anymore.)

# ------------------------------------------------------------
# PART B - EXPANDED CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Print the type() of an integer
print(type(10))

# TASK 2: Print the type() of a float
print(type(12.2))

# TASK 3: Print the type() of a boolean
print(type(True))

# TASK 4: Print the type() of a string
print(type("This is a string"))

# TASK 5: Create a variable with your name and print it
my_name = "bassam omari"
print(my_name)

# TASK 6: Create TWO variables (age + height) and print both
age = 20
height = 170
print(age)
print(height)

# TASK 7: Create a variable, print type(), then change it to
# a different data type and print type() again (Dynamic Typing)
x = 10
print(type(x))
x = "bassam"
print(type(x))

# TASK 8: Assign multiple variables in one line (z, f, s)
z, f, s = 3, 10.8, "bassam"
print(z)
print(f)
print(s)

# TASK 9: Write the result of 2 == 2 as a comment below,
# then print the actual comparison in code.
# 2 == 2 returns True
print(2 == 2)

# TASK 10: Print the result of a comparison that is False
print(1 == 10)

# ============================================================
# PART C - BONUS CHALLENGE CODE (extra marks - makes it 100%)
# ============================================================

# BONUS 1: Print type() of a list and a tuple
print(type([1, 2, 3]))
print(type((1, 2, 3)))

# BONUS 2: Print type() of a dictionary
print(type({"name": "bassam", "age": 20}))

# BONUS 3: Use keyword module to check if "for" is reserved
import keyword
print(keyword.iskeyword("for"))

# BONUS 4: Print all reserved keywords
print(keyword.kwlist)

# BONUS 5: Create a variable, then reassign it to a different
# type and print both types (dynamic typing proof)
var = 100
print(type(var))
var = "now a string"
print(type(var))

# BONUS 6: Multiple assignment with different types
a, b, c = 1, 2.5, "three"
print(a, b, c)

# ============================================================
# END OF PROJECT 5 - FINAL EXPANDED (sub5)
# ============================================================