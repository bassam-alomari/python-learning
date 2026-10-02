# ============================================================
# PROJECT 28 - Dictionaries Part 1 (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01-32, plus the for loop from 47-51)
# Topics: All previous + Dictionary Basics, keys(), values(),
#        items(), get(), pop(), popitem(), update(),
#        setdefault(), del, and the view trap
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: keys(), values(), items()
# What does each of these three methods return? Give the exact
# type name of what keys() returns, and say what items() puts
# inside the list it returns.
# (your answer here)

# QUESTION 2: the "in" operator
# If I write "city" in student, is Python looking for a KEY or
# for a VALUE? What happens if I write "Amman" in student?
# (your answer here)

# QUESTION 3: get() versus square brackets
# What does student["phone"] do when the key is missing? What
# does student.get("phone") do? And what does
# student.get("phone", "unknown") return?
# (your answer here)

# QUESTION 4: pop() versus popitem()
# Which one needs a key name? Which one takes no argument? What
# does popitem() remove, the first pair or the last one?
# (your answer here)

# QUESTION 5: update()
# If I call d.update({"age": 30}) and "age" already exists with
# the value 21, do I get two "age" keys, one "age" key with 30, or
# an error?
# (your answer here)

# QUESTION 6: setdefault()
# If the key ALREADY exists, does setdefault() overwrite the value
# or leave it alone? When exactly does it write?
# (your answer here)

# QUESTION 7: del versus pop()
# Both remove a key. What is the difference in what they give back
# to me, and what happens if the key is missing?
# (your answer here)

# QUESTION 8: the view trap
# I run view = student.keys(), then I add a new key to student.
# Does my old view still show the new key? Why?
# (your answer here)

# QUESTION 9: fromkeys()
# If I build d = dict.fromkeys(["a", "b"], []), do "a" and "b"
# point to two different empty lists, or to the SAME one?
# (your answer here)

# QUESTION 10: the order of a dictionary
# If I print {"z": 1, "a": 2, "m": 3}, do I get z, a, m or
# a, m, z? Do I need sorted() like I did with a Set?
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Create student = {"name": "Omar", "age": 21,
# "city": "Amman"}. Print the three keys, the three values, the
# three pairs from items(), and the length of the dictionary
# (your code here)

# TASK 2: Take the dictionary from TASK 1, store its keys() in a
# variable called view, then ADD a new key to the dictionary, then
# print the SAME view variable again. Explain in a comment why
# the new key shows up
# (your code here)

# TASK 3: With the dictionary from TASK 1, test membership with
# "in" for a key that exists, a value that does NOT exist as a
# key, and a key you never added. Then print the same three
# lookups with get() and a default message
# (your code here)

# TASK 4: Create settings = {"theme": "dark"}. Change the value
# of "theme" with square brackets, add a brand new key the same
# way, then merge two more pairs in ONE call with update().
# Print after every step
# (your code here)

# TASK 5: Create cart = {"pen": 2, "book": 5, "bag": 1}. Remove
# "bag" with del, remove "pen" with pop() and store what came
# back, then try to pop a key that is not there WITHOUT a default
# and catch the KeyError with try/except. Finally pop the same
# missing key WITH a default and print the default
# (your code here)

# TASK 6: Create a dictionary with four pairs. Call popitem()
# three times in a loop and print each removed pair, then print
# what is left. Explain in a comment which pair comes out first
# and WHY
# (your code here)

# TASK 7: Create prefs = {"theme": "dark"}. Call setdefault()
# with an existing key and a NEW value, then call it again with a
# key that does not exist. Print the dictionary after each call
# and explain both results
# (your code here)

# TASK 8: Build bad = dict.fromkeys(["a", "b"], []), then append
# a word to bad["a"] WITHOUT assigning it back. Print the whole
# dictionary and explain in a comment why "b" changed too
# (your code here)

# TASK 9: Create data = {"a": 1, "b": 2, "c": 3, "d": 4}. Try to
# delete the keys "a" and "b" while looping over data directly,
# and catch the RuntimeError. Then do the same deletion safely by
# looping over list(data) instead, and print the result
# (your code here)

# TASK 10: Count how many times each word appears in
# "the quick brown fox jumps over the lazy dog the fox". Use a
# for loop over the words and counts.get(word, 0) + 1. Print the
# full dictionary, then print the three most common words using
# sorted() with a key on the count
# (your code here)

# TASK 11: Build a tiny phone book app on a dict called contacts.
# Write and use these functions:
#   add_contact(book, name, phone)  -> adds it, or updates the
#                                     phone if the name exists
#   find_contact(book, name)        -> returns the phone, or
#                                     "not found" using get()
#   delete_contact(book, name)      -> removes it safely and
#                                     returns "deleted" or
#                                     "no such contact"
# Print the result of every call, including a second add_contact
# for a name that already exists
# (your code here)

# TASK 12: Two teams have members as a dict of name -> score.
# Print: the merged dict with update(), the SHARED names using
# the & operator on the two keys() views, the names only in the
# first team using -, and every name sorted using |. Then delete
# every name whose score is below 10 by looping over list(...)
# and print what is left
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.
#
# IMPORTANT: unlike a Set, a dictionary KEEPS the order you wrote
# the keys in, so we do not need sorted() to print it. We only
# use sorted() when we WANT alphabetical order.

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
student = {"name": "Omar", "age": 21, "city": "Amman"}
print("Q1  keys()   ->", list(student.keys()))
print("Q1  values() ->", list(student.values()))
print("Q1  items()  ->", list(student.items()))
print("Q1  len()    ->", len(student))
# Q1  keys()   -> ['name', 'age', 'city']
# Q1  values() -> ['Omar', 21, 'Amman']
# Q1  items()  -> [('name', 'Omar'), ('age', 21), ('city', 'Amman')]
# Q1  len()    -> 3

# QUESTION 2
print("Q2  'city' in student   ->", "city" in student, "(a KEY, found)")
print("Q2  'Amman' in student  ->", "Amman" in student, "(a VALUE, ignored)")
print("Q2  'phone' in student  ->", "phone" in student, "(not a key)")
# Q2  'city' in student   -> True (a KEY, found)
# Q2  'Amman' in student  -> False (a VALUE, ignored)
# Q2  'phone' in student  -> False (not a key)

# QUESTION 3
try:
    student["phone"]
except KeyError as err:
    print("Q3  student['phone']   -> KeyError", err)
print("Q3  get('phone')       ->", student.get("phone"))
print("Q3  get('phone', 'x')  ->", student.get("phone", "unknown"))
# Q3  student['phone']   -> KeyError 'phone'
# Q3  get('phone')       -> None
# Q3  get('phone', 'x')  -> unknown

# QUESTION 4
d4 = {"a": 1, "b": 2, "c": 3}
print("Q4  pop('b')      ->", d4.pop("b"), "(I chose the key)")
print("Q4  popitem()     ->", d4.popitem(), "(Python chose, the last pair)")
print("Q4  left          ->", d4)
# Q4  pop('b')      -> 2 (I chose the key)
# Q4  popitem()     -> ('c', 3) (Python chose, the last pair)
# Q4  left          -> {'a': 1}

# QUESTION 5
d5 = {"x": 1, "y": 2}
d5.update({"y": 20, "z": 30})
print("Q5  after update   ->", d5, "(one 'y' key, holding 20)")
# Q5  after update   -> {'x': 1, 'y': 20, 'z': 30} (one 'y' key, holding 20)

# QUESTION 6
d6 = {"theme": "dark"}
d6.setdefault("theme", "light")
d6.setdefault("lang", "ar")
print("Q6  after both     ->", d6)
# Q6  after both     -> {'theme': 'dark', 'lang': 'ar'}

# QUESTION 7
d7 = {"k": 1}
removed = d7.pop("k")
print("Q7  pop() gave back ->", repr(removed), "| left ->", d7)
try:
    d7.pop("k")
except KeyError as err:
    print("Q7  pop() a missing key -> KeyError", err)
# Q7  pop() gave back -> 1 | left -> {}
# Q7  pop() a missing key -> KeyError 'k'

# QUESTION 8
view = student.keys()
student["grade"] = "A"
print("Q8  the old view now ->", list(view), "(a live window, not a copy)")
# Q8  the old view now -> ['name', 'age', 'city', 'grade'] (a live window, not a copy)

# QUESTION 9
shared = dict.fromkeys(["a", "b"], [])
shared["a"].append("hit")
print("Q9  after touching a ->", shared, "(ONE list, shared by both keys)")
# Q9  after touching a -> {'a': ['hit'], 'b': ['hit']} (ONE list, shared by both keys)

# QUESTION 10
print("Q10 the order        ->", list({"z": 1, "a": 2, "m": 3}), "(written order, no sorted())")
# Q10 the order        -> ['z', 'a', 'm'] (written order, no sorted())

print("-" * 60)

# TASK 1
student = {"name": "Omar", "age": 21, "city": "Amman"}
print("T1  keys            ->", list(student.keys()))
print("T1  values          ->", list(student.values()))
print("T1  items           ->", list(student.items()))
print("T1  length          ->", len(student))
# T1  keys            -> ['name', 'age', 'city']
# T1  values          -> ['Omar', 21, 'Amman']
# T1  items           -> [('name', 'Omar'), ('age', 21), ('city', 'Amman')]
# T1  length          -> 3

# TASK 2
student = {"name": "Omar", "age": 21, "city": "Amman"}
view = student.keys()
student["grade"] = "A"
print("T2  before the add, the view held ->", 3, "keys")
print("T2  the SAME view after the add    ->", list(view))
print("T2  so view was a window, not a photo")
# T2  before the add, the view held -> 3 keys
# T2  the SAME view after the add    -> ['name', 'age', 'city', 'grade']
# T2  so view was a window, not a photo

# TASK 3
student = {"name": "Omar", "age": 21, "city": "Amman"}
print("T3  'city' in student          ->", "city" in student)
print("T3  'Amman' in student         ->", "Amman" in student)
print("T3  'grade' in student         ->", "grade" in student)
print("T3  get('city')                ->", student.get("city"))
print("T3  get('grade', 'unknown')    ->", student.get("grade", "unknown"))
print("T3  get('phone', 'unknown')    ->", student.get("phone", "unknown"))
# T3  'city' in student          -> True
# T3  'Amman' in student         -> False
# T3  'grade' in student         -> False
# T3  get('city')                -> Amman
# T3  get('grade', 'unknown')    -> unknown
# T3  get('phone', 'unknown')    -> unknown

# TASK 4
settings = {"theme": "dark"}
print("T4  start                 ->", settings)
settings["theme"] = "light"
print("T4  after [] on 'theme'   ->", settings, "(changed, not duplicated)")
settings["font"] = "mono"
print("T4  after [] on new key   ->", settings, "([] adds OR changes)")
settings.update({"font": "serif", "lang": "ar"})
print("T4  after update()        ->", settings, "(two pairs in one call)")
# T4  start                 -> {'theme': 'dark'}
# T4  after [] on 'theme'   -> {'theme': 'light'} (changed, not duplicated)
# T4  after [] on new key   -> {'theme': 'light', 'font': 'mono'} ([] adds OR changes)
# T4  after update()        -> {'theme': 'light', 'font': 'serif', 'lang': 'ar'} (two pairs in one call)

# TASK 5
cart = {"pen": 2, "book": 5, "bag": 1}
del cart["bag"]
print("T5  after del 'bag'      ->", cart, "(del gives nothing back)")
gave_back = cart.pop("pen")
print("T5  pop('pen') gave back ->", gave_back, "| left ->", cart)
try:
    cart.pop("phone")
except KeyError as err:
    print("T5  pop('phone')        -> KeyError", err)
print("T5  with a default       ->", cart.pop("phone", "no such item"))
# T5  after del 'bag'      -> {'pen': 2, 'book': 5} (del gives nothing back)
# T5  pop('pen') gave back -> 2 | left -> {'book': 5}
# T5  pop('phone')        -> KeyError 'phone'
# T5  with a default       -> no such item

# TASK 6
queue = {"first": 1, "second": 2, "third": 3, "fourth": 4}
removed_order = []
for _ in range(3):
    pair = queue.popitem()
    removed_order.append(pair)
    print("T6  popitem() removed   ->", pair)
print("T6  the removal order    ->", removed_order)
print("T6  what is left         ->", queue)
# T6  popitem() removed   -> ('fourth', 4)
# T6  popitem() removed   -> ('third', 3)
# T6  popitem() removed   -> ('second', 2)
# T6  the removal order    -> [('fourth', 4), ('third', 3), ('second', 2)]
# T6  what is left         -> {'first': 1}

# TASK 7
prefs = {"theme": "dark"}
prefs.setdefault("theme", "light")
print("T7  existing key kept    ->", prefs, "('dark' was NOT replaced)")
prefs.setdefault("lang", "ar")
print("T7  missing key written ->", prefs)
# T7  existing key kept    -> {'theme': 'dark'} ('dark' was NOT replaced)
# T7  missing key written -> {'theme': 'dark', 'lang': 'ar'}

# TASK 8
bad = dict.fromkeys(["a", "b"], [])
bad["a"].append("hit")
print("T8  after append to a    ->", bad)
print("T8  b changed too       ->", bad["b"] == bad["a"], "(same list object)")
# T8  after append to a    -> {'a': ['hit'], 'b': ['hit']}
# T8  b changed too       -> True (same list object)

# TASK 9
data = {"a": 1, "b": 2, "c": 3, "d": 4}
try:
    for key in data:
        if key in "ab":
            del data[key]
except RuntimeError as err:
    print("T9  direct loop         -> RuntimeError:", err)
safe = {"a": 1, "b": 2, "c": 3, "d": 4}
for key in list(safe):
    if key in "ab":
        del safe[key]
print("T9  looping list(data)  ->", safe, "(correct)")
# T9  direct loop         -> RuntimeError: dictionary changed size during iteration
# T9  looping list(data)  -> {'c': 3, 'd': 4} (correct)

# TASK 10
words = "the quick brown fox jumps over the lazy dog the fox".split()
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print("T10 all counts          ->", counts)
top_three = sorted(counts.items(), key=lambda pair: -pair[1])[:3]
print("T10 the top three      ->", top_three)
# T10 all counts          -> {'the': 3, 'quick': 1, 'brown': 1, 'fox': 2, 'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1}
# T10 the top three      -> [('the', 3), ('fox', 2), ('quick', 1)]

# TASK 11
def add_contact(book, name, phone):
    """Add a contact, or update the phone if the name is known."""
    if name in book:
        book[name] = phone
        return "updated"
    book[name] = phone
    return "added"

def find_contact(book, name):
    """Return the phone number, or a clear message when unknown."""
    return book.get(name, "not found")

def delete_contact(book, name):
    """Remove a contact safely, without raising on a missing name."""
    if name in book:
        del book[name]
        return "deleted"
    return "no such contact"

contacts = {}
print("T11 add Omar    ->", add_contact(contacts, "Omar", "0790"), "|", contacts)
print("T11 add Mona    ->", add_contact(contacts, "Mona", "0781"), "|", contacts)
print("T11 add Omar AGAIN ->", add_contact(contacts, "Omar", "0799"), "|", contacts)
print("T11 find Omar   ->", find_contact(contacts, "Omar"))
print("T11 find Sayed  ->", find_contact(contacts, "Sayed"))
print("T11 delete Omar ->", delete_contact(contacts, "Omar"), "|", contacts)
print("T11 delete Omar AGAIN ->", delete_contact(contacts, "Omar"), "|", contacts)
# T11 add Omar    -> added | {'Omar': '0790'}
# T11 add Mona    -> added | {'Omar': '0790', 'Mona': '0781'}
# T11 add Omar AGAIN -> updated | {'Omar': '0799', 'Mona': '0781'}
# T11 find Omar   -> 0799
# T11 find Sayed  -> not found
# T11 delete Omar -> deleted | {'Mona': '0781'}
# T11 delete Omar AGAIN -> no such contact | {'Mona': '0781'}

# TASK 12
team_a = {"Omar": 12, "Sayed": 8, "Mona": 20}
team_b = {"Mona": 15, "Ali": 9, "Omar": 11}

merged = team_a.copy()
merged.update(team_b)
print("T12 merged (b wins on ties) ->", merged)
print("T12 shared names (&)        ->", sorted(team_a.keys() & team_b.keys()))
print("T12 only in A (-)           ->", sorted(team_a.keys() - team_b.keys()))
print("T12 every name (|)          ->", sorted(team_a.keys() | team_b.keys()))

qualified = merged.copy()
for name in list(qualified):
    if qualified[name] < 10:
        del qualified[name]
print("T12 after dropping < 10     ->", qualified)
# T12 merged (b wins on ties) -> {'Omar': 11, 'Sayed': 8, 'Mona': 15, 'Ali': 9}
# T12 shared names (&)        -> ['Mona', 'Omar']
# T12 only in A (-)           -> ['Sayed']
# T12 every name (|)          -> ['Ali', 'Mona', 'Omar', 'Sayed']
# T12 after dropping < 10     -> {'Omar': 11, 'Mona': 15}

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 28")
print("=" * 60)
# ============================================================
# END OF PROJECT 28
# ============================================================
