# ============================================================
# PROJECT 29 - Dictionaries Part 2 (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01-32, plus the for loop from 47-51)
# Topics: All previous + Dictionary Views, zip(), dictionary
#        comprehension, nested dicts, shallow vs deep copy,
#        sorting by value, inverting a dict
#
# This is the SECOND dictionary project. Project 28 covered the
# methods one at a time. This one uses them together the way real
# code does: build, transform, count, sort, and report.
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: the three views
# I write "name" in d.keys() and "name" in d.values(). What does
# each one look for? And what does d.items() give me inside, a key
# or a pair?
# (your answer here)

# QUESTION 2: zip()
# I build a dict with dict(zip(list_a, list_b)) and the two lists
# have different lengths. What happens to the extra items?
# (your answer here)

# QUESTION 3: dictionary comprehension
# What does {n: n * n for n in nums} do, and how do I add a
# condition so only SOME items become keys?
# (your answer here)

# QUESTION 4: nested dicts
# If d = {"a": {"b": 1}} and I want to read d["a"]["b"] without
# risking a crash when a key is missing, what do I write instead?
# (your answer here)

# QUESTION 5: .copy() versus a deep copy
# My dictionary holds another dictionary inside it. I call
# original.copy(), change the INNER value, and original changes
# too. Why, and what is the one-word fix?
# (your answer here)

# QUESTION 6: sorting by value
# A dict of name -> score. How do I get the names ordered from
# the highest score to the lowest, and why is plain sorted()
# not enough?
# (your answer here)

# QUESTION 7: the counting idiom
# Why does counts[word] = counts.get(word, 0) + 1 work on the
# very first time a word appears, when the key does not exist yet?
# (your answer here)

# QUESTION 8: inverting a dict
# I have {name: id} and I want {id: name}. What single line does
# it, and what breaks if two names share one id?
# (your answer here)

# QUESTION 9: set operations on keys
# I learned & | - on Sets in project 27. Do I get the same
# operations from d1.keys() and d2.keys()? What do I get back
# when I do?
# (your answer here)

# QUESTION 10: order after reassigning
# I write d["z"] = 1, then d["a"] = 2, then d["z"] = 3. Which
# order do the keys end up in, and where does "z" sit?
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: With d = {"name": "Omar", "age": 21}, test "name" in
# d.keys(), 21 in d.values(), and "name" in d.items(). Convert
# d.keys() to a set and d.items() to a list, and print all of it
# (your code here)

# TASK 2: Build a dict from names = ["Omar", "Mona", "Ali"] and
# scores = [90, 75, 88] with zip(). Then build one more where the
# two lists have different lengths, and explain in a comment which
# items survived
# (your code here)

# TASK 3: Use a dictionary comprehension to build
#   {n: n * n} for n in [1, 2, 3, 4, 5], and then the same but
# keeping only the ODD numbers. Print both
# (your code here)

# TASK 4: Build lengths = {"a": 1, "bb": 2, "ccc": 3}, then use
# a dictionary comprehension to INVERT it into {1: "a", 2: "bb",
# 3: "ccc"}. Print both and say in a comment why this inversion is
# only safe when the values are unique
# (your code here)

# TASK 5: Loop over lengths with a for loop and UNPACK the pair
# inside the loop line, printing "key has value". Then swap two
# variables with a single assignment and print them
# (your code here)

# TASK 6: Create original = {"a": {"x": 1}, "b": 2}. Make
# shallow = original.copy(), change shallow["a"]["x"] to 999, and
# print original to show it changed. Then set shallow["b"] = 222
# and print original again to show the top level was safe.
# Finally fix it with copy.deepcopy and prove the original is
# untouched
# (your code here)

# TASK 7: Create user = {"name": "Sara", "address": {"city":
# "Amman", "street": "Main"}}. Print the city with square
# brackets, then with a get() chain for a key that exists, then
# with a get() chain for a path that does NOT exist at all
# (your code here)

# TASK 8: With marks = {"Omar": 55, "Mona": 91, "Ali": 73}, print
# the pairs sorted from the highest mark down, and the names in
# alphabetical order. Do NOT modify marks itself
# (your code here)

# TASK 9: Count the letters in "a b a c b a" with a dict, then
# print every letter that appears EXACTLY twice, sorted
# (your code here)

# TASK 10: Two dicts share some keys:
#         d1 = {"x": 1, "y": 2}
#         d2 = {"y": 9, "z": 3}
# Print the shared keys with &, all keys with |, and the keys
# only in d1 with -, each sorted
# (your code here)

# TASK 11: Build a small grades database on ONE dict where each
# key is a student name and each value is another dict of
# subject -> mark. Write and use:
#   add_mark(db, name, subject, mark)  -> creates the student if
#                                        needed, then sets the
#                                        subject
#   average(db, name)                  -> the mean mark, or
#                                        "no record" when the
#                                        student is unknown
#   top_student(db)                    -> the (name, average)
#                                        pair with the best
#                                        average
# Test with two students and three subjects, and print every
# result
# (your code here)

# TASK 12: Write report(cards) where cards is a list of dicts
# like {"name": "Omar", "subject": "math", "mark": 90}. It must
# return a NEW dict mapping each subject to a list of the marks in
# it, sorted from the highest down. Print the report, and print
# the number of subjects it found
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.
#
# Nothing here modifies a dictionary while looping over its keys.
# That mistake raised RuntimeError in project 28, and it is the
# single rule to remember from both projects.

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
d = {"name": "Omar", "age": 21}
print("Q1  'name' in d.keys()   ->", "name" in d.keys(), "(the KEY)")
print("Q1  21 in d.values()     ->", 21 in d.values(), "(the VALUE)")
print("Q1  'name' in d.items()  ->", "name" in d.items(), "(items holds PAIRS)")
# Q1  'name' in d.keys()   -> True (the KEY)
# Q1  21 in d.values()     -> True (the VALUE)
# Q1  'name' in d.items()  -> False (items holds PAIRS)

# QUESTION 2
print("Q2  zip with a longer key list ->", dict(zip(["a", "b", "c"], [1, 2])))
print("Q2  so the extra key 'c' is silently DROPPED")
# Q2  zip with a longer key list -> {'a': 1, 'b': 2}
# Q2  so the extra key 'c' is silently DROPPED

# QUESTION 3
nums = [1, 2, 3, 4, 5]
print("Q3  squares           ->", {n: n * n for n in nums})
print("Q3  odd squares only  ->", {n: n * n for n in nums if n % 2 == 1})
# Q3  squares           -> {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
# Q3  odd squares only  -> {1: 1, 3: 9, 5: 25}

# QUESTION 4
user = {"address": {"city": "Amman"}}
print("Q4  safe chain        ->", user.get("phone", {}).get("model", "unknown"))
# Q4  safe chain        -> unknown

# QUESTION 5
import copy
original = {"a": {"x": 1}}
shallow = original.copy()
shallow["a"]["x"] = 999
print("Q5  after .copy() and a nested change ->", original, "(the INNER dict is shared)")
deep = copy.deepcopy(original)
deep["a"]["x"] = 7
print("Q5  after deepcopy and a nested change ->", original, "(now it is safe)")
# Q5  after .copy() and a nested change -> {'a': {'x': 999}} (the INNER dict is shared)
# Q5  after deepcopy and a nested change -> {'a': {'x': 999}} (now it is safe)

# QUESTION 6
marks = {"Omar": 55, "Mona": 91}
print("Q6  by value, highest first ->", sorted(marks.items(), key=lambda p: -p[1]))
# Q6  by value, highest first -> [('Mona', 91), ('Omar', 55)]

# QUESTION 7
counts = {}
counts["a"] = counts.get("a", 0) + 1
print("Q7  the first 'a' ->", counts, "(get returned 0, the default)")
# Q7  the first 'a' -> {'a': 1} (get returned 0, the default)

# QUESTION 8
print("Q8  inverted ->", {v: k for k, v in {"Omar": 1, "Mona": 2}.items()})
# Q8  inverted -> {1: 'Omar', 2: 'Mona'}

# QUESTION 9
d1 = {"x": 1, "y": 2}
d2 = {"y": 9, "z": 3}
print("Q9  d1 & d2 ->", sorted(d1.keys() & d2.keys()), "(a SET of keys)")
# Q9  d1 & d2 -> ['y'] (a SET of keys)

# QUESTION 10
d10 = {}
d10["z"] = 1
d10["a"] = 2
d10["z"] = 3
print("Q10 the keys ->", list(d10), "('z' kept its FIRST position)")
# Q10 the keys -> ['z', 'a'] ('z' kept its FIRST position)

print("-" * 60)

# TASK 1
d = {"name": "Omar", "age": 21}
print("T1  'name' in d.keys()   ->", "name" in d.keys())
print("T1  21 in d.values()     ->", 21 in d.values())
print("T1  'name' in d.items()  ->", "name" in d.items())
# A Set has no order (project 27), so we sort it before printing.
# Printing the raw set would work but the order could change.
print("T1  sorted(d.keys())     ->", sorted(d.keys()))
print("T1  list(d.items())      ->", list(d.items()))
# T1  'name' in d.keys()   -> True
# T1  21 in d.values()     -> True
# T1  'name' in d.items()  -> False
# T1  sorted(d.keys())     -> ['age', 'name']
# T1  list(d.items())      -> [('name', 'Omar'), ('age', 21)]

# TASK 2
names = ["Omar", "Mona", "Ali"]
scores = [90, 75, 88]
print("T2  even lengths      ->", dict(zip(names, scores)))
print("T2  3 keys, 2 scores  ->", dict(zip(names, [90, 75])), "('Ali' was dropped)")
print("T2  2 keys, 3 scores  ->", dict(zip(["Omar", "Mona"], scores)), "(88 was dropped)")
# T2  even lengths      -> {'Omar': 90, 'Mona': 75, 'Ali': 88}
# T2  3 keys, 2 scores  -> {'Omar': 90, 'Mona': 75} ('Ali' was dropped)
# T2  2 keys, 3 scores  -> {'Omar': 90, 'Mona': 75} (88 was dropped)

# TASK 3
nums = [1, 2, 3, 4, 5]
print("T3  all squares   ->", {n: n * n for n in nums})
print("T3  odd squares   ->", {n: n * n for n in nums if n % 2 == 1})
# T3  all squares   -> {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
# T3  odd squares   -> {1: 1, 3: 9, 5: 25}

# TASK 4
lengths = {"a": 1, "bb": 2, "ccc": 3}
inverted = {value: key for key, value in lengths.items()}
print("T4  original     ->", lengths)
print("T4  inverted     ->", inverted)
print("T4  safe here because every value was unique")
# T4  original     -> {'a': 1, 'bb': 2, 'ccc': 3}
# T4  inverted     -> {1: 'a', 2: 'bb', 3: 'ccc'}
# T4  safe here because every value was unique

# TASK 5
lengths = {"a": 1, "bb": 2, "ccc": 3}
for key, value in lengths.items():
    print(f"T5  {key} has {value}")
first, second = "left", "right"
print("T5  before the swap ->", first, second)
first, second = second, first
print("T5  after the swap  ->", first, second)
# T5  a has 1
# T5  bb has 2
# T5  ccc has 3
# T5  before the swap -> left right
# T5  after the swap  -> right left

# TASK 6
import copy
original = {"a": {"x": 1}, "b": 2}
shallow = original.copy()
shallow["a"]["x"] = 999
print("T6  after a NESTED change ->", original, "(changed!)")
shallow["b"] = 222
print("T6  after a TOP change    ->", original, "(b is still 2, safe)")
deep = copy.deepcopy(original)
deep["a"]["x"] = 7
print("T6  after deepcopy        ->", original, "(untouched now)")
# T6  after a NESTED change -> {'a': {'x': 999}, 'b': 2} (changed!)
# T6  after a TOP change    -> {'a': {'x': 999}, 'b': 2} (b is still 2, safe)
# T6  after deepcopy        -> {'a': {'x': 999}, 'b': 2} (untouched now)

# TASK 7
user = {"name": "Sara", "address": {"city": "Amman", "street": "Main"}}
print("T7  brackets         ->", user["address"]["city"])
print("T7  get chain, there ->", user.get("address", {}).get("city", "unknown"))
print("T7  get chain, gone  ->", user.get("phone", {}).get("model", "unknown"))
# T7  brackets         -> Amman
# T7  get chain, there -> Amman
# T7  get chain, gone  -> unknown

# TASK 8
marks = {"Omar": 55, "Mona": 91, "Ali": 73}
by_mark = sorted(marks.items(), key=lambda pair: -pair[1])
by_name = sorted(marks.items())
print("T8  highest first    ->", [name for name, _ in by_mark])
print("T8  alphabetical    ->", [name for name, _ in by_name])
print("T8  marks untouched  ->", marks)
# T8  highest first    -> ['Mona', 'Ali', 'Omar']
# T8  alphabetical    -> ['Ali', 'Mona', 'Omar']
# T8  marks untouched  -> {'Omar': 55, 'Mona': 91, 'Ali': 73}

# TASK 9
counts = {}
for ch in "a b a c b a".split():
    counts[ch] = counts.get(ch, 0) + 1
print("T9  the counts       ->", counts)
twice = sorted(k for k, v in counts.items() if v == 2)
print("T9  seen exactly 2x  ->", twice)
# T9  the counts       -> {'a': 3, 'b': 2, 'c': 1}
# T9  seen exactly 2x  -> ['b']

# TASK 10
d1 = {"x": 1, "y": 2}
d2 = {"y": 9, "z": 3}
print("T10 shared keys (&)  ->", sorted(d1.keys() & d2.keys()))
print("T10 all keys   (|)  ->", sorted(d1.keys() | d2.keys()))
print("T10 only in d1 (-)  ->", sorted(d1.keys() - d2.keys()))
# T10 shared keys (&)  -> ['y']
# T10 all keys   (|)  -> ['x', 'y', 'z']
# T10 only in d1 (-)  -> ['x']

# TASK 11
def add_mark(db, name, subject, mark):
    """Store one mark, creating the student's record if needed."""
    if name not in db:
        db[name] = {}
    db[name][subject] = mark
    return "saved"

def average(db, name):
    """Return the mean mark for a student, or a clear message."""
    if name not in db:
        return "no record"
    marks = list(db[name].values())
    if not marks:
        return "no marks"
    return round(sum(marks) / len(marks), 2)

def top_student(db):
    """Return the (name, average) pair with the best average."""
    best_name = None
    best_average = -1
    for name in db:
        current = average(db, name)
        if current > best_average:
            best_name = name
            best_average = current
    if best_name is None:
        return "empty database"
    return (best_name, best_average)

db = {}
print("T11 add Omar math  ->", add_mark(db, "Omar", "math", 90))
print("T11 add Omar eng   ->", add_mark(db, "Omar", "english", 70))
print("T11 add Mona math  ->", add_mark(db, "Mona", "math", 95))
print("T11 add Mona sci   ->", add_mark(db, "Mona", "science", 88))
print("T11 the database   ->", db)
print("T11 average Omar   ->", average(db, "Omar"))
print("T11 average Mona   ->", average(db, "Mona"))
print("T11 average Sayed  ->", average(db, "Sayed"))
print("T11 top student    ->", top_student(db))
print("T11 top of empty   ->", top_student({}))
# T11 add Omar math  -> saved
# T11 add Omar eng   -> saved
# T11 add Mona math  -> saved
# T11 add Mona sci   -> saved
# T11 the database   -> {'Omar': {'math': 90, 'english': 70}, 'Mona': {'math': 95, 'science': 88}}
# T11 average Omar   -> 80.0
# T11 average Mona   -> 91.5
# T11 average Sayed  -> no record
# T11 top student    -> ('Mona', 91.5)
# T11 top of empty   -> empty database

# TASK 12
def report(cards):
    """Map each subject to its marks, highest first."""
    grouped = {}
    for card in cards:
        subject = card["subject"]
        grouped.setdefault(subject, []).append(card["mark"])
    for subject in grouped:
        grouped[subject].sort(reverse=True)
    return grouped

cards = [
    {"name": "Omar", "subject": "math", "mark": 90},
    {"name": "Mona", "subject": "math", "mark": 95},
    {"name": "Ali", "subject": "english", "mark": 70},
    {"name": "Sayed", "subject": "math", "mark": 82},
]
result = report(cards)
print("T12 the report     ->", result)
print("T12 subject count  ->", len(result))
print("T12 the input list ->", "still", len(cards), "cards, untouched")
# T12 the report     -> {'math': [95, 90, 82], 'english': [70]}
# T12 subject count  -> 2
# T12 the input list -> still 4 cards, untouched

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 29")
print("=" * 60)
# ============================================================
# END OF PROJECT 29
# ============================================================
