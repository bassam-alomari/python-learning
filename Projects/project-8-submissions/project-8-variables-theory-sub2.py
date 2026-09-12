# ============================================================
# PROJECT 8 - Variables Theory & Concepts (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04 + 05 + 06 + 07 + 08)
# Topics: Introduction, Setup, print(), Comments, Data Types,
#         type(), Variables, Dynamic Typing, Keywords
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

# QUESTION 8: Variables (Lesson 07)
# What is a variable? List 3 naming rules.
# (A variable is something that points to a location in the memory
#  that holds the data.
#  Naming rules:
#  1 - Do not use spaces in the name
#  2 - Do not start the name with a number
#  3 - Only use letters, numbers and underscore _)

# QUESTION 9: Source Code (Lesson 08)
# What is Source Code?
# (Source Code is the code that you write in a programming language,
#  it is the text file that contains the instructions of the program.)

# QUESTION 10: Compilation vs Runtime (Lesson 08)
# What is Compilation? What is Runtime?
# How does Python execute code (all at once or step by step)?
# (Compilation is when the compiler reads all the code lines
#  and then executes them.
#  Runtime is when the program is actually running.
#  Python executes the code step by step (line by line),
#  because it is an interpreter language.)

# QUESTION 11: Dynamic Typing (Lesson 08)
# What does "Dynamically Typed" mean?
# Can a variable change its type in Python? Give an example.
# (Dynamically Typed means that the variable can change its type
#  after creation.
#  Yes, in Python a variable can change its type.
#  Example:
#  h = 1      # int
#  h = 1.1    # now it is float)

# QUESTION 12: Reserved Keywords (Lesson 08)
# What are Reserved Keywords?
# Can you use them as variable names? Name 3 of them.
# (Reserved Keywords are words that are reserved by the language
#  for special meanings.
#  No, you cannot use them as variable names.
#  Examples: if, else, for, while, def, return)

# QUESTION 13: Multiple Assignment (Lesson 08)
# How do you assign 3 values to 3 variables in ONE line?
# What error do you get if the counts don't match?
# (You write them separated by commas:
#  x, y, z = 1, 2, 3
#  If the counts do not match, you get a ValueError.)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Create a variable with your name and print it
my_name = "bassam alomari"
print(my_name)

# TASK 2: Create variables for age and height, print both
age = 21
height = 170
print(age)
print(height)

# TASK 3: Dynamic Typing - assign 10 to x, print type(x),
# then assign "Osama" to x, print type(x) again
x = 10
print(type(x))
x = "Osama"
print(type(x))

# TASK 4: Multiple Assignment - assign 1, 2, 3 to x, y, z
# in one line and print all three
x, y, z = 1, 2, 3
print(x)
print(y)
print(z)

# TASK 5: Print type() of a variable holding a float
f = 1.2
print(type(f))

# TASK 6: Print type() of a variable holding a boolean
b = True
print(type(b))

# TASK 7: Use the keyword module to print all reserved keywords
import keyword
print(keyword.kwlist)

# TASK 8: Use keyword.iskeyword() to check if "if" is reserved
import keyword
print(keyword.iskeyword("if"))

# TASK 9: Create a variable using snake_case (my_full_name)
my_full_name = "bassam alomari"

# ============================================================
# END OF PROJECT 8
# ============================================================