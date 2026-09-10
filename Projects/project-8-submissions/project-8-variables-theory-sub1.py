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

# QUESTION 8: Variables (Lesson 07)
# What is a variable? List 3 naming rules.
# (it is the value that refers to a location in the memory that has a value // do not use spaces and it is case sensitive and not start with numbers and only use numbers and alphabetic and _ and do not include the !/@#$%)

# QUESTION 9: Source Code (Lesson 08)
# What is Source Code?
# (is the of program)

# QUESTION 10: Compilation vs Runtime (Lesson 08)
# What is Compilation? What is Runtime?
# How does Python execute code (all at once or step by step)?
# (Compilation is code read all lines and execute // Runtime code read and execute line by line)

# QUESTION 11: Dynamic Typing (Lesson 08)
# What does "Dynamically Typed" mean?
# Can a variable change its type in Python? Give an example.
# (the variable can change the type after creation)
h =1
h= 1.1
# QUESTION 12: Reserved Keywords (Lesson 08)
# What are Reserved Keywords?
# Can you use them as variable names? Name 3 of them.
# (Reserved Keywords are keywords that are reserved by the language and you cannot use them as variable names 1 - list 2 - print 3 - type)

# QUESTION 13: Multiple Assignment (Lesson 08)
# How do you assign 3 values to 3 variables in ONE line?
# What error do you get if the counts don't match?
# (syntax error)
name, Name, NAME = "bassam" , "adnan" , "alomari"
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
# TASK 3: Dynamic Typing - assign 10 to x, print type(x),
# then assign "Osama" to x, print type(x) again
# (your code here)
x = 10
print(type(x))
x = "Osama"
print(type(x))
# TASK 4: Multiple Assignment - assign 1, 2, 3 to x, y, z
# in one line and print all three
# (your code here)
x,y,z = 1,2,3
print(x);print(y);print(z)

# TASK 5: Print type() of a variable holding a float
# (your code here)
f= 1.2
print(type(f))
# TASK 6: Print type() of a variable holding a boolean
# (your code here)
b= True
print(type(b))
# TASK 7: Use the keyword module to print all reserved keywords
# (your code here)
import keyword
print(keyword.kwlist)
# TASK 8: Use keyword.iskeyword() to check if "if" is reserved
# (your code here)
import keyword
print(keyword.iskeyword("if"))
# TASK 9: Create a variable using snake_case (my_full_name)
# (your code here)
my_full_name= "bassam alomari"
# ============================================================
# END OF PROJECT 8
# ============================================================