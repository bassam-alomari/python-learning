# -----------------------------------------------------------------
# Lesson 31: Dictionary Methods - Part 1
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : dictionary methods - clear, update, copy, keys, values
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# In this lesson we start the dictionary methods. They are the same
# idea we already used with lists and sets, but they work on a
# key: value structure.

# ============================================================
# [1] clear()  -> remove ALL items from the dictionary
# ============================================================
# clear() empties the dictionary completely and returns None.

my_dict = {"name": "Bassam", "age": 22, "city": "Amman"}
print("before clear:", my_dict)
# before clear: {'name': 'Bassam', 'age': 22, 'city': 'Amman'}

result = my_dict.clear()
print("after clear :", my_dict)
# after clear : {}
print("clear() returns:", result)
# clear() returns: None

# The dictionary still exists, it is just empty now.
print("is empty?", len(my_dict) == 0)
# is empty? True

# ============================================================
# [2] update()  -> update old values AND add new items
# ============================================================
# update() takes another dictionary and merges it into ours.
# Existing keys get the NEW value, new keys simply get added.

settings = {"theme": "dark", "font": 14}
settings.update({"theme": "light", "language": "Arabic"})
print("after update:", settings)
# after update: {'theme': 'light', 'font': 14, 'language': 'Arabic'}

# The 'theme' key existed before and its value changed from dark to light.
# The 'language' key is completely new.

# We can also pass key=value directly as keyword arguments.
settings.update(font=16)
print("after update(font=16):", settings)
# after update(font=16): {'theme': 'light', 'font': 16, 'language': 'Arabic'}

# ============================================================
# [3] Adding an item directly WITHOUT update()
# ============================================================
# Assigning to a key that does NOT exist simply creates it.
# So this is a valid alternative to update() for a single item.

profile = {"name": "Bassam"}
profile["age"] = 22
profile["city"] = "Amman"
print("built by direct assignment:", profile)
# built by direct assignment: {'name': 'Bassam', 'age': 22, 'city': 'Amman'}

# Both ways are fine:
#   a) my_dict["age"] = 22        -> one item
#   b) my_dict.update({"age": 22}) -> one item or many at once

# ============================================================
# [4] copy()  -> take a copy so the original stays safe
# ============================================================
# copy() returns a NEW dictionary with the same items, so we can
# modify the copy without touching the original.

original = {"name": "Bassam", "age": 22}
cloned = original.copy()

cloned["name"] = "Ahmad"
cloned["age"] = 30

print("original:", original)
# original: {'name': 'Bassam', 'age': 22}
print("cloned  :", cloned)
# cloned  : {'name': 'Ahmad', 'age': 30}

# The original was NOT affected. This is the whole point of copy().

# IMPORTANT: copy() is a SHALLOW copy.
# If a value is a list, both dictionaries point to the SAME list.

team = {"lead": "Bassam", "skills": ["Python"]}
team_copy = team.copy()
team_copy["skills"].append("Git")

print("team_copy skills:", team_copy["skills"])
# team_copy skills: ['Python', 'Git']
print("team skills too :", team["skills"])
# team skills too : ['Python', 'Git']   <- the original list changed too!

# ============================================================
# [5] keys() and values()  -> a quick review
# ============================================================
# keys() gives us all the keys, values() gives us all the values.

user = {"name": "Bassam", "age": 22, "city": "Amman"}

print("keys()  :", user.keys())
# keys()  : dict_keys(['name', 'age', 'city'])

print("values():", user.values())
# values(): dict_values(['Bassam', 22, 'Amman'])

# Convert them to lists when we need to work with them normally.
print("keys as list  :", list(user.keys()))
# keys as list  : ['name', 'age', 'city']
print("values as list:", list(user.values()))
# values as list: ['Bassam', 22, 'Amman']

# count the items without calling len() on a list
print("how many keys:", len(user.keys()))
# how many keys: 3

# ============================================================
# Improvement (from me): filter a record and make a safe template
# ============================================================
# Two helpers that turn these methods into practical code.

def filter_items(record, minimum):
    """Return a NEW dict keeping only the integer values >= minimum."""
    return {
        key: value
        for key, value in record.items()
        if type(value) is int and value >= minimum
    }


def make_template(base, **overrides):
    """Copy base, then apply the updates; base is never modified."""
    result = base.copy()
    result.update(overrides)
    return result


scores = {"bassam": 90, "ahmad": 65, "sara": 78}
print("scores >= 70:", filter_items(scores, 70))
# scores >= 70: {'bassam': 90, 'sara': 78}

default_config = {"theme": "dark", "font": 14, "language": "English"}
custom_config = make_template(default_config, font=20, language="Arabic")
print("default:", default_config)
# default: {'theme': 'dark', 'font': 14, 'language': 'English'}
print("custom :", custom_config)
# custom : {'theme': 'dark', 'font': 20, 'language': 'Arabic'}

# ============================================================
# SUMMARY
# ============================================================
# - clear()      : deletes every item; the dict stays empty, returns None
# - update()     : merges a dict, replacing old values and adding new keys
# - d[key] = v   : creates or replaces ONE key without update()
# - copy()       : returns a copy; changing it does not affect the original
# - copy() is SHALLOW: nested lists and dicts are shared between copies
# - keys()       : all the keys
# - values()     : all the values

# ============================================================
# NEXT LESSON: Dictionary Methods - Part 2
#              pop, popitem, fromkeys, setdefault
# ============================================================
