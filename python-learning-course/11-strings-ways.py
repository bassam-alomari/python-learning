# Lesson 10 - Strings (Ways to Write)
# Source: Elzero Python Course (Arabic)
# Topic: Different Ways to Create Strings in Python
# Type: Theory + Practical Code

# ============================================================
# DIFFERENT WAYS TO WRITE STRINGS
# ============================================================
# Python gives you multiple ways to create strings.
# All of them produce the same result - strings.

# ============================================================
# [1] SINGLE QUOTES
# ============================================================

myStringOne = 'This is Single Quote'
print(myStringOne)  # This is Single Quote

# ============================================================
# [2] DOUBLE QUOTES
# ============================================================

myStringTwo = "This is Double Quotes"
print(myStringTwo)  # This is Double Quotes

print("=" * 50)

# ============================================================
# [3] QUOTES INSIDE STRINGS
# ============================================================
# Use single quotes outside when you have double quotes inside.
# Use double quotes outside when you have single quotes inside.

# Double quotes inside single quotes
myStringThree = 'This is Single Quote "Test"'
print(myStringThree)  # This is Single Quote "Test"

# Single quotes inside double quotes
myStringFour = "This is Double Quotes 'Test'"
print(myStringFour)  # This is Double Quotes 'Test'

print("=" * 50)

# ============================================================
# [4] TRIPLE QUOTES - MULTI-LINE STRINGS
# ============================================================
# Use three single quotes ''' or three double quotes """
# for strings that span multiple lines.

# Triple single quotes
myStringFive = '''First
Second
Third'''
print(myStringFive)
# Output:
# First
# Second
# Third

# Triple double quotes
myStringSix = """First
Second
Third"""
print(myStringSix)
# Output:
# First
# Second
# Third

print("=" * 50)

# ============================================================
# [5] QUOTES INSIDE TRIPLE QUOTES
# ============================================================
# You can use BOTH single and double quotes inside
# triple quotes without any problems.

# Single and double quotes inside triple single quotes
myStringSeven = '''First
Second 'Test' "Test"
Third'''
print(myStringSeven)
# Output:
# First
# Second 'Test' "Test"
# Third

# Single and double quotes inside triple double quotes
myStringEight = """First
Second "Test" 'Test'
Third"""
print(myStringEight)
# Output:
# First
# Second "Test" 'Test'
# Third

print("=" * 50)

# ============================================================
# [6] ESCAPE CHARACTERS IN TRIPLE QUOTES
# ============================================================
# You can use backslash \ to escape quotes inside triple quotes.

# Escaping with backslash
myStringNine = '''First
Second 'Test' "Test"
Third'''
print(myStringNine)

# Using double backslash to print actual backslash
myStringTen = """First
Second "Test" \\ 'Test'
Third"""
print(myStringTen)
# Output:
# First
# Second "Test" \ 'Test'
# Third

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] Single quotes: 'text'
# [2] Double quotes: "text"
# [3] Quotes inside: 'text "inner"' or "text 'inner'"
# [4] Triple single quotes: '''multi-line'''
# [5] Triple double quotes: """multi-line"""
# [6] Quotes inside triple: '''both ' and " work'''
# [7] Escape with backslash: \ to print special chars

# ============================================================
# NEXT LESSON: String Methods
# ============================================================
