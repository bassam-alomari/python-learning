# Lesson 09 - Escape Sequences Characters
# Source: Elzero Python Course (Arabic)
# Topic: Escape Sequences in Strings
# Type: Theory + Practical Code

# ============================================================
# WHAT ARE ESCAPE SEQUENCES?
# ============================================================
# In Python strings, we use the backslash (\) before
# certain special characters to give them special meanings.
# These are called Escape Sequences.

# ============================================================
# [1] \b - BACKSPACE (Delete Previous Character)
# ============================================================
# Deletes the character right before it.
# Like pressing the Backspace key on your keyboard.

print("Hello\b World")    # Hell World (deletes 'o')
print("Python\bPro")      # PythoPro (deletes 'n')

print("=" * 50)

# ============================================================
# [2] \n - NEW LINE (Move to Next Line)
# ============================================================
# Moves the cursor to a new line.

print("Line 1\nLine 2")
# Output:
# Line 1
# Line 2

print("Name: Bassam\nAge: 21")
# Output:
# Name: Bassam
# Age: 21

print("=" * 50)

# ============================================================
# [3] \\ - PRINT BACKSLASH ITSELF
# ============================================================
# To print a backslash, use double backslash (\\).

print("Hello\\World")    # Hello\World
print("Path: C:\\Users") # Path: C:\Users

print("=" * 50)

# ============================================================
# [4] \' and \" - ESCAPE QUOTES
# ============================================================
# If your string contains quotes, you need to escape them.

# Single quote inside double quotes (no escape needed)
print("I'm Bassam")

# Double quote inside single quotes (no escape needed)
print('He said "Hello"')

# But if you use the SAME quote inside:
# print("He said "Hello"")  # SyntaxError!
# print('It's a nice day')  # SyntaxError!

# Solution: escape the inner quotes
print("He said \"Hello\"")
print("It\'s a nice day")

print("=" * 50)

# ============================================================
# [5] \r - CARRIAGE RETURN (Go Back to Start of Line)
# ============================================================
# Moves cursor back to the START of the current line.
# Text after \r overwrites the beginning of the text before it.

print("Hello\rWorld")
# Output: World (overwrites "Hello")

print("Python\rJava")
# Output: Javaon (overwrites "Pyth")

print("=" * 50)

# ============================================================
# [6] \t - HORIZONTAL TAB (Big Space)
# ============================================================
# Adds a tab space between words.

print("Name:\tBassam")
print("Age:\t21")
print("City:\tIrbid")

# Output:
# Name:   Bassam
# Age:    21
# City:   Irbid

print("=" * 50)

# ============================================================
# [7] \x - HEXADECIMAL CHARACTER
# ============================================================
# Print a character using its hexadecimal (base-16) value.
# Syntax: \xHH (where HH is the hex code)

print("\x48\x65\x6C\x6C\x6F")  # Hello
print("\x41")                    # A (hex 41 = decimal 65)
print("\x61")                    # a (hex 61 = decimal 97)

print("=" * 50)

# ============================================================
# SUMMARY OF ESCAPE SEQUENCES
# ============================================================
# \b  -> Backspace (delete previous char)
# \n  -> New Line
# \\  -> Backslash itself
# \'  -> Single quote
# \"  -> Double quote
# \r  -> Carriage Return (back to start)
# \t  -> Tab (horizontal space)
# \x  -> Hex character code

# ============================================================
# PRACTICE EXERCISES
# ============================================================

# Exercise 1: Print a multi-line menu
print("=== MENU ===\n1. Start\n2. Settings\n3. Exit")

# Exercise 2: Use tab to align data
print("Item\tPrice\tQty")
print("Apple\t$1.50\t10")
print("Banana\t$0.75\t20")

# Exercise 3: Print a path
print("C:\\Users\\Bassam\\Documents")

# ============================================================
# NEXT LESSON: Strings (Part 1) - Indexing & Slicing
# ============================================================
