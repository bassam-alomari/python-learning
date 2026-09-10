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
# (easy to learn // easy to use // works on any platform)

# QUESTION 2: Interpreter vs Compiler (Lesson 01)
# What is the difference? Which one is Python?
# (Interpreter: e.g. Python reads code line by line and executes it line by line; if there is any error in the code, the code is interrupted at the line that has the error. Compiler: C++/C reads all the code and executes all the code; if there is an error in any line, all the code is interrupted)

# QUESTION 3: What do you need to start? (Lesson 02)
# List 4 things you need to start learning Python.
# (IDE and setup any version of Python and have a PC or laptop and mouse and keyboard)

# QUESTION 4: Indentation (Lesson 03)
# What does Python use instead of curly braces {} ?
# (indentation)

# QUESTION 5: Comments (Lesson 04)
# What are the 3 types of comments in Python?
# (inline//single line//multiple line)

# QUESTION 6: Data Types (Lesson 05)
# Name the 3 main data types in Python with an example of each.
# (int = 10 , string = "bassam" , float = 12.2)

# QUESTION 7: type() Function (Lesson 06)
# What does type() do? Give an example.
# (type() shows the data type that the variable refers to)
print(type(15)) # int
# QUESTION 8: What is a Variable? (Lesson 07)
# Explain what a variable is. Does it hold the data directly?
# (it is the value that refers to a location in the memory that has a value)

# QUESTION 9: Naming Rules (Lesson 07)
# List 4 rules for naming variables in Python.
# (do not use spaces and it is case sensitive and should be unique and not start with numbers and only use numbers and alphabetic and _ and do not include the !/@#$%)

# QUESTION 10: Naming Conventions (Lesson 07)
# What is snake_case? What is camelCase?
# Which one is recommended in Python?
# (your answer here)
my_name="bassam" # snake_case this is recommended
myName="bassam" # camelCase
# QUESTION 11: Case Sensitivity (Lesson 07)
# Are name, Name, and NAME the same variable? Why?
# (no, Python is case sensitive)

# QUESTION 12: Assign Before Using (Lesson 07)
# What error do you get if you use a variable before assigning it?
# (logical error)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Create a variable with your name and print it
# (your code here)
my_name="bassam alomari"
print(my_name)
# TASK 2: Create variables for age and height, print both
# (your code here)
age = 21
height = 170
print(age)
print(height)
# TASK 3: Create a boolean variable and print it
# (your code here)
b = True
print(b)
# TASK 4: Create a variable using snake_case (first_name)
# (your code here)
first_name="bassam"
# TASK 5: Create a variable using camelCase (firstName)
# (your code here)
firstName="bassam"
# TASK 6: Print type() of a variable holding a string
# (your code here)
print(type(first_name))
# TASK 7: Print type() of a variable holding a float
# (your code here)
a=1.1
print(type(a))
# TASK 8: Create 3 variables (name, Name, NAME) with different
# values and print all 3 to show case sensitivity
# (your code here)
name, Name, NAME = "bassam" , "adnan" , "alomari"
print(name);print(Name);print(NAME)
# TASK 9: Create a variable, then print it, then change its
# value and print it again
# (your code here)
h=1
print(h)
h=2
print(h)
# ============================================================
# END OF PROJECT 7
# ============================================================