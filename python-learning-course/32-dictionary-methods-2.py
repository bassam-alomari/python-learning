# -----------------------------------------------------------------
# Lesson 32: Dictionary Methods - Part 2
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : setdefault, popitem, items, fromkeys
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# We finish the dictionary methods with four very useful tools.
# Each one answers a question we always ask: does the key exist,
# what is the last item, how do I loop over everything, and how do
# I build many keys at once.

# ============================================================
# [1] setdefault()  -> check the key, and create it if it is missing
# ============================================================
# Syntax: my_dict.setdefault(key, default_value)
# If the key EXISTS     -> return its value and change nothing.
# If the key is MISSING -> add it with the default value and return it.

user = {"name": "Bassam"}

# The key 'name' already exists, so we only READ it.
existing_value = user.setdefault("name", "Guest")
print("setdefault('name'):", existing_value)
# setdefault('name'): Bassam
print("user unchanged:", user)
# user unchanged: {'name': 'Bassam'}

# The key 'age' does NOT exist, so it gets created with 22.
new_value = user.setdefault("age", 22)
print("setdefault('age'):", new_value)
# setdefault('age'): 22
print("user now:", user)
# user now: {'name': 'Bassam', 'age': 22}

# If we call it again, the key exists so the value stays 22
# and our new default is simply ignored.
user.setdefault("age", 99)
print("age after second call:", user["age"])
# age after second call: 22

# ============================================================
# [2] popitem()  -> remove the LAST item and return it as a tuple
# ============================================================
# popitem() works on the LAST inserted pair and gives it back as
# a (key, value) tuple. In Python 3.7+ this is LIFO, exactly like
# popping from a list. Before 3.7 the order was random.

fruits = {"apple": 1, "banana": 2, "orange": 3}
print("fruits:", fruits)
# fruits: {'apple': 1, 'banana': 2, 'orange': 3}

last_item = fruits.popitem()
print("popitem():", last_item)
# popitem(): ('orange', 3)
print("fruits after popitem:", fruits)
# fruits after popitem: {'apple': 1, 'banana': 2}

# Calling popitem on an EMPTY dictionary raises a KeyError.
try:
    {}.popitem()
except KeyError as err:
    print("popitem on empty ->", err)
# popitem on empty -> 'popitem(): dictionary is empty'

# ============================================================
# [3] items()  -> get every key WITH its value as a tuple
# ============================================================
# items() returns a view of (key, value) tuples. This is the best
# way to loop over a dictionary because we get both parts at once.

settings = {"theme": "dark", "font": 14, "language": "Arabic"}

print("items():", settings.items())
# items(): dict_items([('theme', 'dark'), ('font', 14), ('language', 'Arabic')])

# Convert to a list to see the tuples clearly.
print("as list:", list(settings.items()))
# as list: [('theme', 'dark'), ('font', 14), ('language', 'Arabic')]

# The classic loop with unpacking.
for key, value in settings.items():
    print(key, "=", value)

# We can also read the whole tuple from a for loop.
for pair in settings.items():
    print("pair:", pair, "| key:", pair[0], "| value:", pair[1])

# ============================================================
# [4] fromkeys()  -> build many keys with ONE default value
# ============================================================
# Syntax: dict.fromkeys(keys, value)
# It takes any iterable of keys (list, tuple, set) and returns a
# NEW dictionary where every key has the same value.

fields = ["name", "email", "phone"]
new_user = dict.fromkeys(fields, "Not Filled")
print("fromkeys(list):", new_user)
# fromkeys(list): {'name': 'Not Filled', 'email': 'Not Filled', 'phone': 'Not Filled'}

# The value is optional; without it every value becomes None.
statuses = dict.fromkeys(["todo", "doing", "done"])
print("fromkeys(no value):", statuses)
# fromkeys(no value): {'todo': None, 'doing': None, 'done': None}

# A tuple of keys works the same way.
levels = dict.fromkeys(("low", "high"), 1)
print("fromkeys(tuple):", levels)
# fromkeys(tuple): {'low': 1, 'high': 1}

# ============================================================
# [5] The fromkeys() TRAP: mutable values are SHARED
# ============================================================
# fromkeys() assigns the SAME object to every key, so a mutable
# value (list/dict) is shared between all of them.

shared = dict.fromkeys(["a", "b"], [])
shared["a"].append(1)
print("shared:", shared)
# shared: {'a': [1], 'b': [1]}   <- 'b' changed too, and we never asked for that!

# The safe way is to build the dictionary with a comprehension
# so every key gets its own separate object.

safe = {key: [] for key in ["a", "b"]}
safe["a"].append(1)
print("safe  :", safe)
# safe  : {'a': [1], 'b': []}

# ============================================================
# Improvement (from me): a safe fromkeys plus a small data report
# ============================================================
# One helper to avoid the shared-mutable-value trap, and one
# helper to read a record nicely using items().

def safe_fromkeys(keys, value=None):
    """Like fromkeys, but a mutable value gets its OWN copy per key."""
    if hasattr(value, "copy"):
        return {key: value.copy() for key in keys}
    return {key: value for key in keys}


def data_report(record):
    """Return a readable multi-line report of key = value pairs."""
    return "\n".join(f"{key}: {value}" for key, value in record.items())


per_key = safe_fromkeys(["a", "b"], [])
per_key["a"].append("only for a")
print("safe_fromkeys:", per_key)
# safe_fromkeys: {'a': ['only for a'], 'b': []}

print("report:")
print(data_report({"name": "Bassam", "age": 22}))
# report:
# name: Bassam
# age: 22

# ============================================================
# SUMMARY
# ============================================================
# - setdefault(k, d) : returns the value if the key exists, otherwise
#                      creates the key with d and returns it
# - popitem()        : removes the LAST pair and returns it as a tuple;
#                      KeyError on an empty dictionary
# - items()          : returns all (key, value) tuples; best for loops
# - fromkeys(k, v)   : builds a new dict where every key gets the same v
# - WARNING: a mutable value in fromkeys() is SHARED between all keys,
#   so use a comprehension (or safe_fromkeys) when the value is a list

# ============================================================
# NEXT LESSON: Control Flow - if / elif / else and the comparison
#              and membership operators
# ============================================================
