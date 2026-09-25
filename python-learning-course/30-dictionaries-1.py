# -----------------------------------------------------------------
# Lesson 30: Dictionary - Part 1 (The Basics)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : dictionary concept, key/value rules, access, keys, values,
#           nested dictionary, assignment
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# A Dictionary stores data as KEY : VALUE pairs.
# Think of a real dictionary: each word (the key) has a meaning (the value).
# The key is the label you use to find the data quickly.

# ============================================================
# [1] How to create a Dictionary
# ============================================================
# We use curly braces {} and write each item as key: value,
# separating the items with a comma.

my_dict = {"name": "Bassam", "age": 22, "city": "Amman"}
print("my_dict:", my_dict)
# my_dict: {'name': 'Bassam', 'age': 22, 'city': 'Amman'}

# An empty dictionary is created with dict() or {}.
empty = dict()
print("empty dictionary:", empty)
# empty dictionary: {}

# The type of a dictionary is <class 'dict'>.
print("type:", type(my_dict))
# type: <class 'dict'>

# ============================================================
# [2] The rules of the KEYS
# ============================================================
# A key MUST be an IMMUTABLE type (a value that cannot be changed):
# strings, integers, floats, booleans, and tuples are all allowed keys.

valid_keys = {"name": "Bassam", 10: "ten", 3.5: "three point five", True: "yes"}
print("valid keys:", valid_keys)
# valid keys: {'name': 'Bassam', 10: 'ten', 3.5: 'three point five', True: 'yes'}

# A MUTABLE type such as a LIST can never be a key.
try:
    {["a", "b"]: 1}          # a list key -> TypeError
except TypeError as err:
    print("list as key ->", err)
# list as key -> unhashable type: 'list'

# Why? A dictionary finds its value by hashing the key, and a list
# can change its content, so its hash would not be stable.

# ============================================================
# [3] The rules of the VALUES
# ============================================================
# A value has NO restriction: it can be any data type, even another
# container. This is the big difference between keys and values.

mixed_values = {
    "text": "hello",
    "number": 100,
    "flag": True,
    "list": [1, 2, 3],
    "tuple": (4, 5),
}
print("values can be anything:", mixed_values)
# values can be anything: {'text': 'hello', 'number': 100, 'flag': True,
#                          'list': [1, 2, 3], 'tuple': (4, 5)}

# ============================================================
# [4] Keys must be UNIQUE
# ============================================================
# If the same key is written twice, Python keeps the LAST value
# and silently drops the first one. No error is raised.

duplicated = {"color": "red", "color": "blue"}
print("duplicated key:", duplicated)
# duplicated key: {'color': 'blue'}

# This is a common beginner trap: check your key spelling carefully.

# ============================================================
# [5] Accessing a value - method 1: square brackets
# ============================================================
user = {"name": "Bassam", "age": 22, "country": "Jordan"}

print("user['name']:", user["name"])
# user['name']: Bassam

# If the key does NOT exist, we get a KeyError.
try:
    print(user["phone"])
except KeyError as err:
    print("missing key ->", err)
# missing key -> 'phone'

# ============================================================
# [6] Accessing a value - method 2: get()
# ============================================================
# get() returns the value if the key exists, otherwise it returns
# the default, which is None unless we provide another default.

print("get('name')    :", user.get("name"))
# get('name')    : Bassam
print("get('phone')   :", user.get("phone"))
# get('phone')   : None
print("get('phone','N/A'):", user.get("phone", "N/A"))
# get('phone','N/A'): N/A

# get() is the SAFE way when the key is optional.

# ============================================================
# [7] Getting all keys and all values
# ============================================================
# keys() returns a view of the keys, values() returns a view of the values.

print("keys()  :", user.keys())
# keys()  : dict_keys(['name', 'age', 'country'])

print("values():", user.values())
# values(): dict_values(['Bassam', 22, 'Jordan'])

# We can convert them to real lists to work with them normally.
all_keys = list(user.keys())
all_values = list(user.values())
print("as list keys  :", all_keys)
# as list keys  : ['name', 'age', 'country']
print("as list values:", all_values)
# as list values: ['Bassam', 22, 'Jordan']

# A quick loop over keys to print each pair.
for key in user:
    print(key, "->", user[key])

# ============================================================
# [8] Nested Dictionary (a dictionary inside a dictionary)
# ============================================================
# Very often our data is structured in groups, so a value can be
# another whole dictionary. This is called a nested dictionary.

main_dict = {
    "dict1": {
        "name": "Python",
        "version": 3,
    },
    "dict2": {
        "name": "JavaScript",
        "version": 2023,
    },
}

# To reach a nested value we chain the keys one after another.
print("main_dict['dict1']['name']:", main_dict["dict1"]["name"])
# main_dict['dict1']['name']: Python
print("main_dict['dict2']['version']:", main_dict["dict2"]["version"])
# main_dict['dict2']['version']: 2023

# A safe version of the same access using get() twice.
safe_name = main_dict.get("dict1", {}).get("name")
print("safe access:", safe_name)
# safe access: Python

# ============================================================
# [9] Building a big dictionary from separate small dictionaries
# ============================================================
# We can build one dictionary and then attach other dictionaries to it.
# This is the same idea as the nested dictionary above, just written apart.

lang_1 = {"name": "Python", "typed": True}
lang_2 = {"name": "JavaScript", "typed": False}

languages = {}
languages["lang_1"] = lang_1
languages["lang_2"] = lang_2

print("languages:", languages)
# languages: {'lang_1': {'name': 'Python', 'typed': True},
#              'lang_2': {'name': 'JavaScript', 'typed': False}}

print("languages['lang_2']['name']:", languages["lang_2"]["name"])
# languages['lang_2']['name']: JavaScript

# ============================================================
# Improvement (from me): safe reading and inverting a dictionary
# ============================================================
# Two small helpers that make dictionary code safer and more useful.

def read_field(record, key, default="unknown"):
    """Read one field safely; never raises KeyError."""
    return record.get(key, default)


def invert(mapping):
    """Return a NEW dictionary that swaps every key with its value."""
    return {value: key for key, value in mapping.items()}


person = {"name": "Bassam", "job": "Developer", "city": "Amman"}
print(read_field(person, "name"))          # Bassam
print(read_field(person, "salary"))        # unknown
print("inverted:", invert(person))
# inverted: {'Bassam': 'name', 'Developer': 'job', 'Amman': 'city'}

# ============================================================
# SUMMARY
# ============================================================
# - A dictionary stores data as key: value pairs and is created with {}.
# - Keys must be immutable (str, int, float, bool, tuple) and unique.
# - A list can never be a key -> TypeError: unhashable type.
# - Values have no restriction; they can be any type, even other dicts.
# - A repeated key keeps only the LAST value.
# - dict[key] gives KeyError when missing; get(key, default) is safe.
# - keys() and values() return the keys and the values.
# - Nested dictionaries are reached by chaining: main["a"]["b"].
# - Dictionary assignment lets us build a big dict piece by piece.

# ============================================================
# NEXT LESSON: Dictionary Methods - update, pop, popitem, clear,
#              copy, fromkeys, setdefault
# ============================================================
