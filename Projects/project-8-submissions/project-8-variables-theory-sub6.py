# ============================================================
# PROJECT 8 - Variables Theory & Reserved Keywords (ULTIMATE EXPANDED + BONUS)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04 + 05 + 06 + 07 + 08)
# Topics: Introduction, Setup, print(), Comments, Data Types,
#         type(), Variables, Dynamic Typing, Reserved Keywords,
#         Multiple Assignment, Source Code, Compilation vs Runtime
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C (BONUS): Challenge code that runs for extra marks
# PART D (EXTRA): Advanced bonus challenges
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
#  4 - It has many libraries that save you time
#  5 - It has a huge community for support)

# QUESTION 2: Interpreter vs Compiler (Lesson 01)
# What is the difference? Which one is Python?
# (An interpreter reads the code line by line and executes it line by line;
#  if there is an error in a line, the program stops at that line.
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
#  from the terminal from anywhere on your computer,
#  without going to the Python folder every time.)

# QUESTION 5: Indentation (Lesson 03)
# What does Python use instead of curly braces {} ?
# What error do you get if you indent wrong?
# (Python uses spaces instead of curly braces {}.
#  You should use 4 spaces for indentation.
#  If you indent wrong, you get a syntax error:
#  for example: IndentationError: expected an indented block)

# QUESTION 6: Comments (Lesson 04)
# What are the 3 types of comments in Python?
# (1 - Single line comment: # comment
#  2 - Inline comment: code # comment
#  3 - Multi line comment: multiple # lines)

# QUESTION 7: Data Types (Lesson 05)
# Name the 4 main data types in Python with an example of each.
# (1 - int: 10
#  2 - float: 12.2
#  3 - string: "bassam"
#  4 - bool: True)

# QUESTION 8: type() Function (Lesson 06)
# What does type() do? Give an example.
# (type() shows the data type of the value.
#  Example: type(15) returns <class 'int'>)

# QUESTION 9: Variables (Lesson 07)
# What is a variable? Does it hold the data directly?
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
#  camelCase: first word lowercase, next words start with capital,
#  example: myName
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

# QUESTION 14: Source Code (Lesson 08)
# What is Source Code?
# (Source Code is the code that you write in the editor,
#  the code that the computer will read and execute.)

# QUESTION 15: Compilation vs Runtime (Lesson 08)
# What is Compilation? What is Runtime?
# How does Python execute code (all at once or step by step)?
# (Compilation is the process of converting the source code
#  into machine code that the computer understands.
#  Runtime is the time when the program is actually running
#  and executing the code.
#  Python executes the code step by step, line by line.)

# QUESTION 16: Dynamic Typing (Lesson 08)
# What does "Dynamically Typed" mean?
# Can a variable change its type in Python? Give an example.
# (Dynamically Typed means that the variable type is not fixed,
#  it can change while the program is running.
#  Yes, a variable can change its type in Python.
#  Example: x = 10 (int), then x = "bassam" (string).)

# QUESTION 17: Multiple Assignment (Lesson 08)
# How do you assign 3 values to 3 variables in ONE line?
# What error do you get if the counts don't match?
# (You write: x, y, z = 1, 2, 3
#  If the counts don't match, you get a ValueError,
#  for example: ValueError: not enough values to unpack)

# QUESTION 18: Reserved Keywords (Lesson 08)
# What are Reserved Keywords?
# Can you use them as variable names? Name 3 of them.
# (Reserved Keywords are words that Python keeps for itself,
#  they have a special meaning in the language.
#  No, you cannot use them as variable names.
#  Examples: if, else, for)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Create a variable with your name and print it
my_name = "bassam alomari"
print(my_name)

# TASK 2: Create variables for age and height, print both
age = 21
height = 175
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
a = 1.1
print(type(a))

# TASK 6: Print type() of a variable holding a boolean
b = True
print(type(b))

# TASK 7: Use the keyword module to print all reserved keywords
import keyword
print(keyword.kwlist)

# TASK 8: Use keyword.iskeyword() to check if "if" is reserved
print(keyword.iskeyword("if"))

# TASK 9: Create a variable using snake_case (my_full_name)
# and print the result of type() on it
my_full_name = "bassam alomari"
print(type(my_full_name))

# ============================================================
# PART C - BONUS CHALLENGE CODE (extra marks - makes it 100%)
# ============================================================

# BONUS 1: Print type() of a set and a frozenset
print(type({1, 2, 3}))
print(type(frozenset([1, 2, 3])))

# BONUS 2: Print type() of a complex number
print(type(3 + 4j))

# BONUS 3: Use keyword module to check if "class" is reserved
print(keyword.iskeyword("class"))

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

# BONUS 7: Show that variables are references (same object)
x = [1, 2, 3]
y = x
y.append(4)
print(x)  # [1, 2, 3, 4] - x changed too!

# BONUS 8: ValueError demonstration - unpack mismatch
# Uncomment to see the error:
# x, y = 1, 2, 3  # ValueError: too many values to unpack

# BONUS 9: NameError demonstration - use before assign
# Uncomment to see the error:
# print(undefined_variable)  # NameError: name 'undefined_variable' is not defined

# BONUS 10: IndentationError demonstration
# Uncomment to see the error:
# def test():
# print("bad indent")  # IndentationError: expected an indented block

# ============================================================
# PART D - EXTRA BONUS CHALLENGES (advanced)
# ============================================================

# EXTRA 1: Print type() of all 8 data types
print(type(10))           # int
print(type(10.5))         # float
print(type(True))         # bool
print(type("text"))       # str
print(type([1,2,3]))      # list
print(type((1,2,3)))      # tuple
print(type({"a":1}))      # dict
print(type({1,2,3}))      # set

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

# EXTRA 7: Print type() of frozenset and complex
print(type(frozenset([1,2,3])))
print(type(3 + 4j))

# EXTRA 8: Reference demonstration
x = [1, 2, 3]
y = x
y.append(4)
print(x)  # [1, 2, 3, 4] - x changed too!

# EXTRA 9: Variable swapping (Pythonic way)
a, b = 10, 20
a, b = b, a
print(a, b)  # 20 10

# EXTRA 10: Augmented assignment operators
x = 10
x += 5   # x = x + 5
print(x)  # 15
x -= 3   # x = x - 3
print(x)  # 12
x *= 2   # x = x * 2
print(x)  # 24
x //= 4  # x = x // 4
print(x)  # 6

# EXTRA 11: Error demonstrations (uncomment to see)
# ValueError: too many values to unpack
# x, y = 1, 2, 3

# NameError: name 'undefined_variable' is not defined
# print(undefined_variable)

# IndentationError: expected an indented block
# def test():
# print("bad indent")

# ============================================================
# END OF PROJECT 8 - ULTIMATE EXPANDED EDITION (sub6)
# ============================================================