# ============================================================
# PROJECT 6 - Data Types & type() Practical (ULTIMATE EXPANDED + BONUS)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04 + 05 + 06)
# Topics: Introduction, Setup, print(), Comments, Data Types,
#         type(), Variables, Dynamic Typing
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
# PART C - BONUS CHALLENGE CODE (extra marks - makes it 100%)
# ============================================================

# BONUS 1: Dynamic typing - change variable type and print both
x = 10
print(type(x))
x = "bassam"
print(type(x))

# BONUS 2: Print type() of a set
print(type({1, 2, 3}))

# BONUS 3: Print type() of None
print(type(None))

# BONUS 4: Use keyword module to check if "while" is reserved
import keyword
print(keyword.iskeyword("while"))

# BONUS 5: Multiple assignment with different types
a, b, c = 1, 2.5, "three"
print(a, b, c)

# BONUS 6: Compare strings with == and !=
print("hello" == "world")
print("hello" != "world")

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

# ============================================================
# END OF PROJECT 6 - ULTIMATE EXPANDED EDITION (sub6)
# ============================================================