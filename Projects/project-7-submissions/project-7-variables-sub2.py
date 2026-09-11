# ============================================================
# PROJECT 7 - Variables & Fundamentals (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04 + 05 + 06 + 07)
# Topics: Introduction, Setup, print(), Comments, Data Types,
#         type(), Variables
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

# QUESTION 8: What is a Variable? (Lesson 07)
# Explain what a variable is. Does it hold the data directly?
# (A variable is something that points to a location in the memory
#  that holds the data. It does NOT hold the data directly,
#  it is a reference to the data.)

# QUESTION 9: Naming Rules (Lesson 07)
# List 4 rules for naming variables in Python.
# (1 - Do not use spaces in the name
#  2 - Do not start the name with a number
#  3 - Only use letters, numbers and underscore _
#  4 - Do not use special characters like ! @ # $ %)

# QUESTION 10: Naming Conventions (Lesson 07)
# What is snake_case? What is camelCase?
# Which one is recommended in Python?
# (snake_case: words separated by underscore, example: my_name
#  camelCase: first word lowercase, next words start with capital,
#  example: myName
#  snake_case is the recommended one in Python.)

# QUESTION 11: Case Sensitivity (Lesson 07)
# Are name, Name, and NAME the same variable? Why?
# (No, they are NOT the same variable,
#  because Python is case sensitive,
#  so name, Name and NAME are three different variables.)

# QUESTION 12: Assign Before Using (Lesson 07)
# What error do you get if you use a variable before assigning it?
# (You get a NameError,
#  for example: NameError: name 'x' is not defined)

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
a = 1.1
print(type(a))

# TASK 8: Create 3 variables (name, Name, NAME) with different
# values and print all 3 to show case sensitivity
name, Name, NAME = "bassam", "adnan", "alomari"
print(name)
print(Name)
print(NAME)

# TASK 9: Create a variable, then print it, then change its
# value and print it again
h = 1
print(h)
h = 2
print(h)

# ============================================================
# END OF PROJECT 7
# ============================================================