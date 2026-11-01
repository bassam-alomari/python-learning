# -----------------------------------------------------------------
# Lesson 109: magic (dunder) methods -- __str__ and __len__
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : double-underscore methods called by Python,
#            readable object display with __str__, custom
#            len() behavior with __len__, and built-in objects
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: Magic / Dunder Methods -- an
# important OOP concept.
#
#   WHAT [00:30] -- special methods with double underscores
#   at both ends (__init__, __str__, __len__); Python calls
#   them in response to ordinary operations
#   __str__ [01:37] -- controls the readable text from
#   str(object) and print(object)
#   EVERYTHING IS AN OBJECT [02:00] -- str, int and list
#   are instances of types/classes with their own behavior
#   __len__ [06:33] -- controls len(object), such as the
#   number of items or skills in a custom object

# ============================================================
# [1] Dunder methods have double underscores [00:30]
# ============================================================
# Common examples are __init__, __str__ and __len__:

print(f"  __init__ is present on object type: {hasattr(object, '__init__')}")
print(f"  __str__ is present on object type: {hasattr(object, '__str__')}")
print(f"  __len__ is a special method name: {'__len__'.startswith('__') and '__len__'.endswith('__')}")
#   __init__ is present on object type: True
#   __str__ is present on object type: True
#   __len__ is a special method name: True

# Python's ordinary syntax can trigger these special
# methods for you.

# ============================================================
# [2] Everything is an object [02:00]
# ============================================================
# Basic values are instances of built-in types:

text = "Python"
number = 42
items = ["a", "b", "c"]

print(f"  str value type: {type(text).__name__}")
print(f"  int value type: {type(number).__name__}")
print(f"  list value type: {type(items).__name__}")
print(f"  each has a type/class: {all(isinstance(value, type(value)) for value in (text, number, items))}")
#   str value type: str
#   int value type: int
#   list value type: list
#   each has a type/class: True

# Each value is an object created by its class/type.

# ============================================================
# [3] Python calls __str__ for str() and print() [01:37]
# ============================================================
# Define a readable representation instead of a default
# object address-like display:

class Member:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Member: {self.name}, age {self.age}"


member = Member("Amina", 29)
print(f"  str(member): {str(member)}")
print(f"  print representation: {member}")
#   str(member): Member: Amina, age 29
#   print representation: Member: Amina, age 29

# str() and print() use the same __str__ result.

# ============================================================
# [4] __str__ must return a string
# ============================================================
# The method gives a clear summary assembled from the
# object's own attributes:

summary = str(member)
print(f"  __str__ result type: {type(summary).__name__}")
print(f"  includes member name: {'Amina' in summary}")
print(f"  includes member age: {'29' in summary}")
#   __str__ result type: str
#   includes member name: True
#   includes member age: True

# ============================================================
# [5] __len__ customizes len(object) [06:33]
# ============================================================
# A skills profile reports its skill count:

class Profile:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

    def __len__(self):
        return len(self.skills)


profile = Profile("Amina", ["Python", "SQL", "Testing"])
print(f"  profile skill count: {len(profile)}")
print(f"  matches stored skills: {len(profile) == len(profile.skills)}")
#   profile skill count: 3
#   matches stored skills: True

# len(profile) triggers profile.__len__() automatically.

# ============================================================
# [6] Add __str__ and __len__ to one class
# ============================================================
# Both special methods can make an object natural to use:

class SkillSet:
    def __init__(self, owner, skills):
        self.owner = owner
        self.skills = skills

    def __str__(self):
        return f"{self.owner}: {', '.join(self.skills)}"

    def __len__(self):
        return len(self.skills)


skill_set = SkillSet("Omar", ["Python", "Regex"])
print(f"  readable skill set: {skill_set}")
print(f"  skill count: {len(skill_set)}")
#   readable skill set: Omar: Python, Regex
#   skill count: 2

# ============================================================
# [7] Built-in objects use their own behavior [02:00]
# ============================================================
# str, int and list have string representations and
# lengths where supported:

print(f"  str() on text: {str(text)}")
print(f"  str() on int: {str(number)}")
print(f"  str() on list: {str(items)}")
print(f"  len() on list: {len(items)}")
#   str() on text: Python
#   str() on int: 42
#   str() on list: ['a', 'b', 'c']
#   len() on list: 3

# int has a string form but no length; asking len(42)
# would raise TypeError, so we don't do that here.

# ============================================================
# [8] __len__ supports truth testing too
# ============================================================
# Python treats an object with length zero as false in
# a Boolean context:

empty_profile = Profile("Nobody", [])
filled_profile = Profile("Amina", ["Python"])
print(f"  empty profile is false: {not bool(empty_profile)}")
print(f"  filled profile is true: {bool(filled_profile)}")
#   empty profile is false: True
#   filled profile is true: True

# bool(object) can consult __len__ when __bool__ is not
# defined.

# ============================================================
# [9] Inspect special methods on classes
# ============================================================
# These methods live on the class and are invoked by
# Python's protocol operations:

print(f"  Member defines __str__: '__str__' in Member.__dict__")
print(f"  Profile defines __len__: '__len__' in Profile.__dict__")
print(f"  str(member) uses readable text: str(member) == 'Member: Amina, age 29'")
#   Member defines __str__: '__str__' in Member.__dict__
#   Profile defines __len__: '__len__' in Profile.__dict__
#   str(member) uses readable text: str(member) == 'Member: Amina, age 29'

# ============================================================
# [10] A method call and the protocol call
# ============================================================
# Direct calls are possible, but normal Python syntax is
# clearer:

print(f"  direct __str__ call: {member.__str__()}")
print(f"  normal str call: {str(member)}")
print(f"  direct __len__ call: {profile.__len__()}")
print(f"  normal len call: {len(profile)}")
#   direct __str__ call: Member: Amina, age 29
#   normal str call: Member: Amina, age 29
#   direct __len__ call: 3
#   normal len call: 3

# The transcript notes these methods are usually invoked
# implicitly by Python, not called by hand.

# ============================================================
# [11] The required return behavior
# ============================================================
# __str__ returns text; __len__ returns a non-negative
# integer. Confirm the examples follow those contracts:

print(f"  __str__ returns str: {isinstance(member.__str__(), str)}")
print(f"  __len__ returns int: {isinstance(profile.__len__(), int)}")
print(f"  __len__ non-negative: {profile.__len__() >= 0}")
#   __str__ returns str: True
#   __len__ returns int: True
#   __len__ non-negative: True

# ============================================================
# [12] One session: objects and magic methods
# ============================================================
# Summary facts together:

print(f"  built-in types: {type(text).__name__}, {type(number).__name__}, {type(items).__name__}")
print(f"  custom str: {member}")
print(f"  custom len: {len(profile)}")
print(f"  custom object truth from len: {bool(filled_profile)}")
print(f"  skill set text and count: {skill_set} / {len(skill_set)}")
#   built-in types: str, int, list
#   custom str: Member: Amina, age 29
#   custom len: 3
#   custom object truth from len: True
#   skill set text and count: Omar: Python, Regex / 2

# ============================================================
# [13] The summary
# ============================================================
# Magic / Dunder Methods, from the transcript:
#
#   1. DUNDER [00:30] -- methods begin and end with two
#      underscores: __init__, __str__, __len__
#   2. AUTOMATIC -- ordinary operations trigger them:
#      print/str calls __str__; len calls __len__
#   3. __str__ [01:37] -- return a readable string for
#      the object instead of a default representation
#   4. __len__ [06:33] -- return a meaningful item count;
#      len(profile) reports its skill count
#   5. EVERYTHING IS AN OBJECT [02:00] -- str, int and
#      list values are instances of their built-in types
#   6. TRUTH TESTING -- if __bool__ is absent, __len__ can
#      make an empty object false and a nonempty one true
#   7. PROTOCOLS -- __str__ should return str; __len__ a
#      non-negative int; use str()/print()/len() normally
#
# Magic methods are ordinary methods with special names;
# Python gives them meaning through common operations.
