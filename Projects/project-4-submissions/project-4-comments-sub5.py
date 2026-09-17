# ============================================================
# PROJECT 4 - Python Comments & Syntax (FINAL EXPANDED + BONUS)
# ============================================================
# Level: Beginner (Lessons 01 + 02 + 03 + 04)
# Topics: Introduction, Setup, print(), Comments
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C (BONUS): Challenge code that runs for extra marks
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: What is Python? (Lesson 01)
# Write 3 things that make Python special.
# (Python is an interpreter programming language.
#  It is special because:
#  1 - It is easy to learn
#  2 - It is easy to setup
#  3 - It works on any platform
#  4 - It has many libraries that save you time)

# QUESTION 2: What is an Interpreter? How is it different
# from a Compiler? Which one is Python?
# (An interpreter reads the code line by line and executes it
#  line by line; if there is an error, the program stops at the
#  line that has the error.
#  A compiler reads all the code first and then executes it;
#  if there is an error in any line, the whole code is not executed.
#  Python is an interpreter, and C/C++ are compiled languages.)

# QUESTION 3: What do you need to start? (Lesson 02)
# List 4 things you need to start learning Python.
# (1 - Python itself (install it)
#  2 - An IDE / text editor (like VS Code)
#  3 - Knowledge of programming basics
#  4 - Practice and continuity)

# QUESTION 4: Python Installation (Lesson 02)
# On Windows, what is the IMPORTANT option you MUST check?
# Why? (from sub2 fixing - MUST be correct)
# (On Windows installation you MUST check
#  "Add Python to PATH".
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

# QUESTION 7: Comment Rules (Lesson 04)
# List 2 rules for writing good comments.
# (1 - Use # to write the comment.
#  2 - Start the file with a header comment
#      that explains what the file does.)

# QUESTION 8: Commenting Out (Lesson 04)
# How do you "disable" a line of code without deleting it?
# (Put # at the beginning of the line,
#  then the code will not run.
#  This is useful for testing and debugging.)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Hello World
print("Hello World")

# TASK 2: Print 20 + 30 = 50
print(20 + 30)

# TASK 3: Print your name
print("bassam alomari")

# TASK 4: Print a boolean value (True) with an inline comment
print(True) # this is an inline comment

# TASK 5: Comment out two lines of code so they do NOT run
# print(112)
# print(120)

# TASK 6: Fix the indentation error (missing spaces)
def say_hello():
    print("Hello from a function!")

# TASK 7: File header comment (already at the top of this file)

# ============================================================
# PART C - BONUS CHALLENGE CODE (extra marks - makes it 100%)
# ============================================================

# BONUS 1: Use type() to show the type of a string and an int
print(type("bassam"))
print(type(50))

# BONUS 2: Use type() to show the type of a float and a boolean
print(type(9.5))
print(type(True))

# BONUS 3: Comment line blocking - block a line with the keyword
# module to prove you understand reserved words
import keyword
print(keyword.iskeyword("if"))

# BONUS 4: Print the result of 10 / 3 (division)
print(10 / 3)

# BONUS 5: Compare two values (==) to prove booleans
print(5 == 5)

# ============================================================
# END OF PROJECT 4 - FINAL EXPANDED (sub5)
# ============================================================