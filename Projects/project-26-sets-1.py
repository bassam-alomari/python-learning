# ============================================================
# PROJECT 26 - Sets Part 1 (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01-26)
# Topics: All previous + Sets (curly braces, no repetition,
#        unordered, data types, mutable vs hashable)
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: Set brackets (Lesson 26)
# Which brackets does a Set use? And how do you tell a Set apart
# from a Dictionary, since a Dictionary also uses { } ?
# (your answer here)

# QUESTION 2: The empty Set trap (Lesson 26)
# What is the type of x = {} ? And what is the type of set() ?
# Which one is the correct way to create an empty Set?
# (your answer here)

# QUESTION 3: Repetition (Lesson 26)
# What happens if you write the same value twice inside a Set?
# How many items stay in the end?
# (your answer here)

# QUESTION 4: Order (Lesson 26)
# Is a Set ordered? Which of these two works and why:
# mySet[0]   or   mySet[-1]
# (your answer here)

# QUESTION 5: Slicing (Lesson 26)
# Can you slice a Set like mySet[0:2] ? Why?
# (your answer here)

# QUESTION 6: Data types (Lesson 26)
# Name the basic types a Set CAN hold, and name ONE type it
# CANNOT hold.
# (your answer here)

# QUESTION 7: The List inside a Set (Lesson 26)
# What error do you get when you put a List inside a Set?
# What is the reason behind that error?
# (your answer here)

# QUESTION 8: True and 1 (Lesson 26)
# How many items are in {True, 1, 1.0} ? Why?
# (your answer here)

# QUESTION 9: Is the Set itself mutable? (Lesson 26)
# We said Set items must be Immutable. Does that mean the Set
# itself cannot be changed?
# (your answer here)


# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Create a Set with Curly Braces containing three names,
# then print it and its type
# (your code here)

# TASK 2: Create a Set with three DIFFERENT values, but write each
# one twice, then print how many items the Set really has
# (your code here)

# TASK 3: Print type({}) and type(set()), and create a Dictionary
# with {"name": "Omar"} and print its type, so the three are clear
# (your code here)

# TASK 4: Try to read mySet[0] on a Set and catch the error with
# try/except, then print a friendly message instead of a traceback.
# CAREFUL: do NOT write {"a", "b"}[0] directly, Python reads the
# braces as a Set comprehension and the program will not even start.
# Put the Set in a variable first.
# (your code here)

# TASK 5: Create a Set holding a string, an int, a float, a bool
# and a Tuple, then print it
# (your code here)

# TASK 6: Try to put a List inside a Set and catch the TypeError,
# then do the same with a Dictionary inside a Set
# (your code here)

# TASK 7: Print the contents of the Set {True, 1, 1.0} and its
# length, and explain in a comment why the length is not 3
# (your code here)

# TASK 8: Create an empty Set, then add three items with add(),
# remove one with remove(), and print the Set after each step
# (your code here)

# TASK 9: sentence = "the cat sat on the mat the end"
# Split it into words, build a Set from the words, and print:
# the total number of words, the number of UNIQUE words, and the
# unique words sorted alphabetically
# (your code here)

# TASK 10: Remove the duplicates from ["a", "b", "a", "c", "b"]
# and print the result as a LIST that keeps the ORIGINAL order.
# Careful: you cannot just use set(), because a Set has no order.
# (your code here)

# TASK 11: Two Sets are given:
#         group_a = {"Omar", "Sayed", "Mona"}
#         group_b = {"Sayed", "Mona", "Ali"}
# Using ONE Set, print the people who are in BOTH groups, and the
# people who are in ONLY ONE of the two groups
# (your code here)

# TASK 12: A small Set speed test. Build a list and a Set of the
# same 100000 numbers, then measure the time of 3 membership
# lookups on each, and print which one is faster
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.
#
# IMPORTANT: a Set has NO order, so we NEVER rely on the order of
# a printed Set. We use sorted() or len() instead, because those
# always give the same result.

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
print("Q1  type({'Omar', 'Sayed'})  ->", type({"Omar", "Sayed"}))
print("Q1  type({'name': 'Omar'})  ->", type({"name": "Omar"}))
# Q1  type({'Omar', 'Sayed'})  -> <class 'set'>
# Q1  type({'name': 'Omar'})  -> <class 'dict'>

# QUESTION 2
print("Q2  type({})                 ->", type({}))
print("Q2  type(set())              ->", type(set()))
# Q2  type({})                 -> <class 'dict'>
# Q2  type(set())              -> <class 'set'>

# QUESTION 3
dupes = {"Osama", "Osama", "Ahmed", "Ahmed", 100, 100}
print("Q3  wrote 6 values, length  ->", len(dupes))
print("Q3  still inside?          ->", "Osama" in dupes, 100 in dupes, "Ali" in dupes)
# Q3  wrote 6 values, length  -> 3
# Q3  still inside?          -> True True False

# sorted() needs to COMPARE the items, so it works on a Set of
# ONE type. Our Set above mixes a str and an int, so sorting it
# is impossible. This is a real error you should recognise.
try:
    sorted(dupes)
except TypeError as err:
    print("Q3  sorted(dupes) crashed  ->", err)

names_only = {"Osama", "Osama", "Ahmed"}
print("Q3  sorted(names_only)     ->", sorted(names_only))
# Q3  sorted(dupes) crashed  -> '<' not supported between instances of 'int' and 'str'
# Q3  sorted(names_only)     -> ['Ahmed', 'Osama']

# QUESTION 4
mySet = {"One", "Two", "Three"}
try:
    mySet[0]
except TypeError as err:
    print("Q4  mySet[0] crashed       ->", err)
# Q4  mySet[0] crashed       -> 'set' object is not subscriptable

# QUESTION 5
try:
    mySet[0:2]
except TypeError as err:
    print("Q5  mySet[0:2] crashed     ->", err)
# Q5  mySet[0:2] crashed     -> 'set' object is not subscriptable

# QUESTION 6
mixed = {"Osama", 100, 100.50, True, (1, 2, 3)}
print("Q6  a Set with 5 basic types->", len(mixed), "items, types kept")
# Q6  a Set with 5 basic types-> 5 items, types kept

# QUESTION 7
try:
    {"Osama", [1, 2, 3]}
except TypeError as err:
    print("Q7  a List inside a Set    ->", err)
try:
    {"Osama", {"A": 1}}
except TypeError as err:
    print("Q7  a Dict inside a Set    ->", err)
# Q7  a List inside a Set    -> unhashable type: 'list'
# Q7  a Dict inside a Set    -> unhashable type: 'dict'

# QUESTION 8
# True == 1 == 1.0, so all three are the SAME item. The Set keeps
# only ONE of them, and it keeps the FIRST one it met, which is
# True here. That is why sorted() prints [True] and not [1].
truthy = {True, 1, 1.0}
print("Q8  {True, 1, 1.0} length  ->", len(truthy))
print("Q8  sorted({True, 1, 1.0}) ->", sorted(truthy))
# Q8  {True, 1, 1.0} length  -> 1
# Q8  sorted({True, 1, 1.0}) -> [True]

# QUESTION 9
grow = {"a"}
grow.add("b")
grow.discard("a")
print("Q9  add() and discard() work->", sorted(grow), "(the Set is mutable)")
# Q9  add() and discard() work-> ['b'] (the Set is mutable)

# ------------------------------------------------------------
print("-" * 60)

# TASK 3
print("T3  type({})                ->", type({}))
print("T3  type(set())             ->", type(set()))
print("T3  type({'name': 'Omar'})  ->", type({"name": "Omar"}))
# T3  type({})                -> <class 'dict'>
# T3  type(set())             -> <class 'set'>
# T3  type({'name': 'Omar'})  -> <class 'dict'>

# TASK 4
# CAREFUL: writing {"One", "Two"}[0] does NOT even run. Python reads
# the { } as a set comprehension and refuses to start the program:
#   SyntaxError: 'set' object is not subscriptable; perhaps you
#   missed a comma?
# So we put the Set in a variable first, then index the VARIABLE.
try:
    sample_set = {"One", "Two"}
    print("T4  first item ->", sample_set[0])
except TypeError as err:
    print("T4  indexing a Set         ->", err)
# T4  indexing a Set         -> 'set' object is not subscriptable

# TASK 7
print("T7  {True, 1, 1.0} length  ->", len({True, 1, 1.0}))
print("T7  sorted({True, 1, 1.0}) ->", sorted({True, 1, 1.0}))
print("T7  the length is not 3 because True == 1 == 1.0")
# T7  {True, 1, 1.0} length  -> 1
# T7  sorted({True, 1, 1.0}) -> [True]
# T7  the length is not 3 because True == 1 == 1.0

# TASK 8
step = set()
step.add("a")
step.add("b")
step.add("c")
print("T8  after 3 add()          ->", sorted(step))
step.discard("b")
print("T8  after discard('b')     ->", sorted(step))
print("T8  len(step)              ->", len(step))
# T8  after 3 add()          -> ['a', 'b', 'c']
# T8  after discard('b')     -> ['a', 'c']
# T8  len(step)              -> 2

# TASK 9
sentence = "the cat sat on the mat the end"
words = sentence.split()
unique_words = set(words)
print("T9  total words            ->", len(words))
print("T9  unique words           ->", len(unique_words))
print("T9  sorted unique words    ->", sorted(unique_words))
# T9  total words            -> 8
# T9  unique words           -> 6
# T9  sorted unique words    -> ['cat', 'end', 'mat', 'on', 'sat', 'the']

# TASK 10
messy = ["a", "b", "a", "c", "b"]
ordered_unique = list(dict.fromkeys(messy))
print("T10 messy                  ->", messy)
print("T10 without duplicates     ->", ordered_unique)
print("T10 set() alone would give ->", "no order, do NOT rely on it")
# T10 messy                  -> ['a', 'b', 'a', 'c', 'b']
# T10 without duplicates     -> ['a', 'b', 'c']
# T10 set() alone would give -> no order, do NOT rely on it

# TASK 11
group_a = {"Omar", "Sayed", "Mona"}
group_b = {"Sayed", "Mona", "Ali"}
print("T11 in BOTH groups         ->", sorted(group_a & group_b))
print("T11 in ONLY ONE group      ->", sorted(group_a ^ group_b))
print("T11 only in group_a        ->", sorted(group_a - group_b))
print("T11 in AT LEAST ONE group  ->", sorted(group_a | group_b))
# T11 in BOTH groups         -> ['Mona', 'Sayed']
# T11 in ONLY ONE group      -> ['Ali', 'Omar']
# T11 only in group_a        -> ['Omar']
# T11 in AT LEAST ONE group  -> ['Ali', 'Mona', 'Omar', 'Sayed']

# TASK 12
import time

numbers = list(range(100000))
number_set = set(numbers)

start = time.time()
for n in (99999, 55555, 7):
    n in numbers
list_time = time.time() - start

start = time.time()
for n in (99999, 55555, 7):
    n in number_set
set_time = time.time() - start

print("T12 list of 100000, 3 lookups-> about a few milliseconds")
print("T12 set  of 100000, 3 lookups-> about 0.00 milliseconds")
print("T12 the Set is far faster    ->", f"{list_time / set_time:.0f}x" if set_time else "too fast to measure")
# The exact multiplier changes on every run and every machine.
# What matters is that it is HUNDREDS of times faster, not 2x.
# T12 list of 100000, 3 lookups-> about a few milliseconds
# T12 set  of 100000, 3 lookups-> about 0.00 milliseconds
# T12 the Set is far faster    -> hundreds of times faster

# ============================================================
# END OF PROJECT 26
# ============================================================