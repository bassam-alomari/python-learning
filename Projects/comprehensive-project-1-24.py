# ============================================================
# COMPREHENSIVE PROJECT - Student Records Manager
# ============================================================
# Level: Beginner (Lessons 01-24 - ALL topics)
#
# This project combines EVERYTHING you learned:
#   [L01-02] Python Intro + Setup
#   [L03]    print() + Indentation
#   [L04]    Comments
#   [L05-06] Data Types + type()
#   [L07-08] Variables + Dynamic Typing + Keywords
#   [L09]    Escape Sequences
#   [L10]    Concatenation
#   [L11]    Strings Ways
#   [L12]    Indexing & Slicing
#   [L13-16] String Methods (len, strip, title, upper, lower,
#            split, join, replace, count, index, ...)
#   [L17-18] Formatting (% , .format(), f-string)
#   [L19]    Numbers (int, float, complex, casting)
#   [L20]    Arithmetic Operators
#   [L21-23] Lists + List Methods
#   [L24]    Tuples
#
# INSTRUCTIONS:
# Build a complete "Student Records Manager" program.
# Follow the steps and write your code in each section.
# At the end, run the program - it should work as ONE program.
# ============================================================

# ------------------------------------------------------------
# SECTION 1: STUDENT DATA (Variables + Tuples) [L07, L24]
# ------------------------------------------------------------
# Create a Tuple for the course info (fixed data - cannot change):
#   course_name, course_hours, course_level
# Example: ("Python Basics", 40, "Beginner")
#
# Create variables for YOUR student info:
#   student_name (string), student_age (int),
#   student_grade (float), is_active (bool)
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# SECTION 2: STUDENTS LIST (Lists) [L21]
# ------------------------------------------------------------
# Create a list called "students" that contains 3 student names.
# Then print:
#   - The whole list
#   - The first student (index 0)
#   - The last student (negative index)
#   - The first 2 students (slicing)
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# SECTION 3: ADD & REMOVE STUDENTS (List Methods) [L22-23]
# ------------------------------------------------------------
# Use append() to add a 4th student to the list.
# Use insert() to add a student at index 1.
# Use remove() to remove one student.
# Use pop() to remove the last student and print what was removed.
# Print the final list.
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# SECTION 4: SORT & REVERSE (List Methods) [L22]
# ------------------------------------------------------------
# Create a list of grades: [85, 90, 78, 92, 88]
# Use sort() to sort them ascending, print.
# Use sort(reverse=True) to sort descending, print.
# Use reverse() to reverse the order, print.
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# SECTION 5: CALCULATIONS (Arithmetic Operators) [L20]
# ------------------------------------------------------------
# Using the grades list from Section 4:
#   - Calculate the total (sum) using +
#   - Calculate the average using / (total / number of grades)
#   - Use len() to get the number of grades [L13]
#   - Use % to check if the total is even or odd
#   - Use ** to calculate the square of the average
#   - Use // to get the integer part of the average
# Print all results.
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# SECTION 6: CLEAN & FORMAT NAMES (String Methods) [L13-16]
# ------------------------------------------------------------
# Create a variable: raw_name = "   bassam alomari   "
# Use strip() to remove the spaces.
# Use title() to capitalize each word.
# Use upper() to make it all uppercase.
# Use lower() to make it all lowercase.
# Use len() to print the length of the cleaned name.
# Use replace() to replace "bassam" with "Bassam".
# Print all results.
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# SECTION 7: SPLIT & JOIN (String Methods) [L14, L16]
# ------------------------------------------------------------
# Create a variable: full_name = "Bassam Alomari"
# Use split() to split it into a list of 2 words.
# Use "-".join() to join the words with a dash.
# Use count() to count how many "a" letters are in the name.
# Use index() to find the position of "Alomari".
# Print all results.
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# SECTION 8: INDEXING & SLICING (Strings) [L12]
# ------------------------------------------------------------
# Create a variable: text = "I Love Python Programming"
# Print:
#   - The first character (index 0)
#   - The last character (negative index)
#   - The word "Python" (slicing)
#   - The word "Programming" (slicing)
#   - The whole string reversed
#   - Every 2nd character
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# SECTION 9: FORMATTING (%, .format(), f-string) [L17-18]
# ------------------------------------------------------------
# Using your student info from Section 1, print 3 messages:
#   [1] Old way with %:
#       "My Name is: %s and My Age is: %d"
#   [2] New way with .format():
#       "My Name is: {} and My Grade is: {:.2f}"
#   [3] f-string:
#       f"My Name is: {name} and I am {age} years old"
# Also format a big number with {:,d} (comma separator).
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# SECTION 10: ESCAPE SEQUENCES + FINAL OUTPUT [L09]
# ------------------------------------------------------------
# Print a final summary report using \n and \t:
#   ===== STUDENT REPORT =====
#   Name:    <your name>
#   Age:     <your age>
#   Grade:   <your grade>
#   Course:  <course name>
#   ==========================
# Use \t for alignment and \n for new lines.
# Use concatenation (+) or f-string to build it.
#
# Write your code below:

# (your code here)


# ------------------------------------------------------------
# BONUS: TYPE CHECKING (type()) [L06, L19]
# ------------------------------------------------------------
# Print the type of:
#   - Your student_name (should be str)
#   - Your student_age (should be int)
#   - Your student_grade (should be float)
#   - Your is_active (should be bool)
#   - The students list (should be list)
#   - The course tuple (should be tuple)
# Also convert your grade to int using int() and print it.
#
# Write your code below:

# (your code here)


# ============================================================
# END OF COMPREHENSIVE PROJECT
# ============================================================
# CHECKLIST - Did you use ALL of these?
# [ ] Variables (L07)          [ ] Tuples (L24)
# [ ] Lists (L21)              [ ] List Methods (L22-23)
# [ ] Arithmetic (L20)         [ ] Numbers/Casting (L19)
# [ ] String Methods (L13-16)  [ ] Indexing/Slicing (L12)
# [ ] Formatting (L17-18)      [ ] Escape Sequences (L09)
# [ ] Concatenation (L10)      [ ] type() (L06)
# ============================================================