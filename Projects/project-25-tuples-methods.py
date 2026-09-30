# ============================================================
# PROJECT 25 - Tuples Part 2 (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01-25)
# Topics: All previous + Tuple Methods (single item, len, + , *,
#        count(), index(), Unpacking, Immutability)
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare your answers with it
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: Single-item Tuple (Lesson 25)
# What happens if you write myTuple = ("Osama") WITHOUT a comma?
# What is type(myTuple)?
# (your answer here)

# QUESTION 2: len() (Lesson 25)
# What does len() return for a Tuple? Does it work the same as Lists?
# (your answer here)

# QUESTION 3: Concatenation (Lesson 25)
# Since a Tuple is immutable, can ( + ) modify the original Tuple
# or does it create a new one?
# (your answer here)

# QUESTION 4: Repetition (Lesson 25)
# What does ("A", "B") * 3 return? How many items are in the result?
# (your answer here)

# QUESTION 5: count() (Lesson 25)
# What does (1, 5, 7, 5, 0, 5).count(5) return?
# (your answer here)

# QUESTION 6: index() (Lesson 25)
# What does (1, 5, 9, 5, 0).index(5) return? And what happens if
# the value is NOT in the Tuple at all?
# (your answer here)

# QUESTION 7: Unpacking (Lesson 25)
# What happens with x, y, z = ("A", "B", "C", "D")?
# Why does Python complain about the number of variables?
# (your answer here)

# QUESTION 8: Immutability (Lesson 25)
# What error do you get if you try t[0] = 99 on a Tuple?
# (your answer here)

# QUESTION 9: sorted() (Lesson 25)
# Why can NOT you call t.sort() on a Tuple, and what do you use
# instead when you need a sorted version?
# (your answer here)


# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Create two single-item Tuples, one with a name and one
# with a number, then print type() of each
# (your code here)

# TASK 2: Create myTupleCount = (10, 20, 30, 40, 50) and print its
# length with len()
# (your code here)

# TASK 3: Create tuple1 = (1, 2, 3, 4) and tuple2 = (5, 6), join
# them with ( + ), then print the result
# (your code here)

# TASK 4: Create tuple = ("A", "B", "C"), repeat it 3 times with
# ( * ), then print the result and its length
# (your code here)

# TASK 5: Create myTuple = (1, 5, 7, 5, 0, 10, 5, 5) and print how
# many times the value 5 appears using count()
# (your code here)

# TASK 6: Create myTuple = (1, 5, 9, 5, 0, 10, 5, 5) and print the
# index of the FIRST 5 using index()
# (your code here)

# TASK 7: Create myTuple = (1, 5, 9, 5, 0, 10, 5, 5), then use
# index(0) to find where the zero is and print the value AFTER it
# (your code here)

# TASK 8: Unpack myUnpack = ("Osama", "Ahmed", "Sayed") into x, y, z
# and print each variable on its own line
# (your code here)

# TASK 9: Catch the two errors from this lesson using try/except:
#  - calling index() with a value that does not exist
#  - trying to assign to an item of a Tuple
# print a friendly message for each one instead of a traceback
# (your code here)

# TASK 10: scores = (88, 92, 75, 88, 100, 88)
# Print: the number of scores, how many 88s, the index of the first
# 88, the highest, the lowest, and the average
# (your code here)

# TASK 11: A student is stored as ONE Tuple:
#         student = ("Omar", 21, 88)
# Unpack it into name, age, score, then print a card that looks like:
#         Name : Omar
#         Age  : 21
#         Score: 88
# (your code here)

# TASK 12: You cannot call sort() on a Tuple. Use sorted() to get a
# sorted version of the scores Tuple from TASK 10, print BOTH the
# original and the sorted one, and explain in a comment why the
# original did not change
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer,
# so after you finish PART A and PART B, run the file and check that
# your results match these values.

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
myBadTuple = ("Osama")
print("Q1  ('Osama') type          ->", type(myBadTuple))
print("Q1  ('Osama',) type         ->", type(("Osama",)))
# Q1  ('Osama') type          -> <class 'str'>
# Q1  ('Osama',) type         -> <class 'tuple'>

# QUESTION 2
print("Q2  len((10, 20, 30))       ->", len((10, 20, 30)))
# Q2  len((10, 20, 30))       -> 3

# QUESTION 3
t1 = (1, 2)
t2 = (3, 4)
t3 = t1 + t2
print("Q3  t1 + t2                ->", t3, "| t1 is still", t1)
# Q3  t1 + t2                -> (1, 2, 3, 4) | t1 is still (1, 2)

# QUESTION 4
print("Q4  ('A', 'B') * 3         ->", ("A", "B") * 3)
# Q4  ('A', 'B') * 3         -> ('A', 'B', 'A', 'B', 'A', 'B')

# QUESTION 5
print("Q5  (1,5,7,5,0,5).count(5) ->", (1, 5, 7, 5, 0, 5).count(5))
# Q5  (1,5,7,5,0,5).count(5) -> 3

# QUESTION 6
print("Q6  (1,5,9,5,0).index(5)   ->", (1, 5, 9, 5, 0).index(5))
try:
    (1, 2, 3).index(99)
except ValueError as err:
    print("Q6  index(99) crashed      ->", err)
# Q6  (1,5,9,5,0).index(5)   -> 1
# Q6  index(99) crashed      -> tuple.index(x): x not in tuple

# QUESTION 7
try:
    x, y, z = ("A", "B", "C", "D")
except ValueError as err:
    print("Q7  4 values into 3 vars  ->", err)
# Q7  4 values into 3 vars  -> too many values to unpack (expected 3)

# The other direction fails too, when there are FEWER values than
# variables, and the message is different:
try:
    a, b, c = ("A", "B")
except ValueError as err:
    print("Q7  2 values into 3 vars  ->", err)
# Q7  2 values into 3 vars  -> not enough values to unpack (expected 3, got 2)

# QUESTION 8
try:
    bad_tuple = (1, 2, 3)
    bad_tuple[0] = 99
except TypeError as err:
    print("Q8  t[0] = 99 crashed     ->", err)
# Q8  t[0] = 99 crashed     -> 'tuple' object does not support item assignment

# QUESTION 9
unsorted = (3, 1, 2)
print("Q9  unsorted.sort() exists ->", hasattr(unsorted, "sort"))
print("Q9  sorted(unsorted)       ->", sorted(unsorted))
print("Q9  unsorted after         ->", unsorted)
# Q9  unsorted.sort() exists -> False
# Q9  sorted(unsorted)       -> [1, 2, 3]
# Q9  unsorted after         -> (3, 1, 2)

# ------------------------------------------------------------
print("-" * 60)

# TASK 5
print("T5  count(5) of (1,5,7,5,0,10,5,5) ->", (1, 5, 7, 5, 0, 10, 5, 5).count(5))
# T5  count(5) of (1,5,7,5,0,10,5,5) -> 4

# TASK 6
print("T6  index(5) of (1,5,9,5,0,10,5,5) ->", (1, 5, 9, 5, 0, 10, 5, 5).index(5))
# T6  index(5) of (1,5,9,5,0,10,5,5) -> 1

# TASK 7
myTuple = (1, 5, 9, 5, 0, 10, 5, 5)
print("T7  index(0) ->", myTuple.index(0), "-> the value after it:", myTuple[myTuple.index(0) + 1])
# T7  index(0) -> 4 -> the value after it: 10

# TASK 10
scores = (88, 92, 75, 88, 100, 88)
print("T10 how many scores         ->", len(scores))
print("T10 how many 88s            ->", scores.count(88))
print("T10 index of the first 88   ->", scores.index(88))
print("T10 highest                 ->", max(scores))
print("T10 lowest                  ->", min(scores))
print("T10 average                 ->", sum(scores) / len(scores))
# T10 how many scores         -> 6
# T10 how many 88s            -> 3
# T10 index of the first 88   -> 0
# T10 highest                 -> 100
# T10 lowest                  -> 75
# T10 average                 -> 88.5

# TASK 11
student = ("Omar", 21, 88)
name, age, score = student
print("T11 Name :", name)
print("T11 Age  :", age)
print("T11 Score:", score)
# T11 Name : Omar
# T11 Age  : 21
# T11 Score: 88

# TASK 12
print("T12 original ->", scores)
print("T12 sorted   ->", tuple(sorted(scores)))
print("T12 original ->", scores, "(unchanged, Tuples are immutable)")
# T12 original -> (88, 92, 75, 88, 100, 88)
# T12 sorted   -> (75, 88, 88, 88, 92, 100)
# T12 original -> (88, 92, 75, 88, 100, 88) (unchanged, Tuples are immutable)

# ============================================================
# END OF PROJECT 25
# ============================================================