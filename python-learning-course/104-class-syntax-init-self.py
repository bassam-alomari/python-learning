# -----------------------------------------------------------------
# Lesson 104: class syntax, __init__ and self
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : define classes with PascalCase, initialize
#            objects with __init__, use self for current
#            instance attributes, compare class and dict
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: first practical OOP coding --
# define classes and instantiate objects.
#
#   CLASS SYNTAX [01:00] -- class Member:; PascalCase is
#   the usual class-name convention
#   CONSTRUCTOR [02:00] -- __init__ runs automatically
#   when a new object is instantiated
#   self [02:40] -- required first parameter for instance
#   methods; refers to the current instance and stores its
#   attributes on that object
#   DICTIONARIES vs CLASSES [06:50] -- classes organize
#   related data and behavior with a shared structure,
#   helping safer and clearer large applications

# ============================================================
# [1] Define a class [01:00]
# ============================================================
# A minimal class can use pass as its empty body:

class Member:
    pass


print(f"  class defined: {Member.__name__}")
print(f"  Member is a class: {isinstance(Member, type)}")
#   class defined: Member
#   Member is a class: True

# ============================================================
# [2] PascalCase naming [01:00]
# ============================================================
# Class names conventionally capitalize each word:

class CourseMember:
    pass


print(f"  class name: {CourseMember.__name__}")
print(f"  name uses PascalCase: {CourseMember.__name__ == 'CourseMember'}")
#   class name: CourseMember
#   name uses PascalCase: True

# ============================================================
# [3] __init__: runs on instantiation [02:00]
# ============================================================
# Python calls __init__ automatically when an instance
# is made; it sets up that instance's initial state:

class Learner:
    def __init__(self):
        self.ready = True


learner = Learner()
print(f"  instance created: {isinstance(learner, Learner)}")
print(f"  __init__ initialized ready: {learner.ready}")
#   instance created: True
#   __init__ initialized ready: True

# ============================================================
# [4] self is the current instance [02:40]
# ============================================================
# self receives the instance being initialized; assigning
# self.name creates an attribute on that particular object:

class Person:
    def __init__(self, name):
        self.name = name


person = Person("Rana")
print(f"  self stored name: {person.name}")
print(f"  attribute belongs to instance: {'name' in person.__dict__}")
#   self stored name: Rana
#   attribute belongs to instance: True

# ============================================================
# [5] __init__ accepts values
# ============================================================
# Arguments after self supply initial values to store:

class MemberProfile:
    def __init__(self, name, age):
        self.name = name
        self.age = age


profile = MemberProfile("Omar", 24)
print(f"  profile name: {profile.name}")
print(f"  profile age: {profile.age}")
#   profile name: Omar
#   profile age: 24

# ============================================================
# [6] Each instance has independent attributes [02:40]
# ============================================================
# The same class creates different instances with their
# own data:

profile_two = MemberProfile("Lina", 31)
print(f"  first member: {profile.name}, {profile.age}")
print(f"  second member: {profile_two.name}, {profile_two.age}")
print(f"  separate instance dictionaries: {profile.__dict__ is not profile_two.__dict__}")
#   first member: Omar, 24
#   second member: Lina, 31
#   separate instance dictionaries: True

# ============================================================
# [7] self in another instance method
# ============================================================
# Every instance method receives the current object as
# its first argument; self lets the method read its state:

class GreetingMember:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return "Hello " + self.name


greeter = GreetingMember("Maya")
print(f"  method uses current self: {greeter.greet()}")
#   method uses current self: Hello Maya

# Python supplies the instance to self when called as
# greeter.greet().

# ============================================================
# [8] The dictionary version [06:50]
# ============================================================
# A dictionary can hold the same member data:

member_record = {"name": "Omar", "age": 24}
print(f"  dict name: {member_record['name']}")
print(f"  dict age: {member_record['age']}")
print(f"  dict keys: {sorted(member_record)}")
#   dict name: Omar
#   dict age: 24
#   dict keys: ['age', 'name']

# Dictionaries are useful for flexible records; their
# keys and structure are not enforced by the dict itself.

# ============================================================
# [9] Class and dict side by side [06:50]
# ============================================================
# Both store the same information, with different access:

class AccountMember:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def label(self):
        return self.name + " (" + str(self.age) + ")"


account_member = AccountMember("Omar", 24)
account_dict = {"name": "Omar", "age": 24}

print(f"  class data: {account_member.name}, {account_member.age}")
print(f"  dict data: {account_dict['name']}, {account_dict['age']}")
print(f"  class provides behavior: {account_member.label()}")
#   class data: Omar, 24
#   dict data: Omar, 24
#   class provides behavior: Omar (24)

# The class keeps a domain action (label) beside the
# member's data; a plain dict only stores the values.

# ============================================================
# [10] Structure and typo safety
# ============================================================
# A class consistently initializes expected attributes;
# a dict permits misspelled keys to be added silently:

structured = MemberProfile("Sara", 28)
loose = {"name": "Sara", "age": 28}
loose["agge"] = 28

print(f"  structured attributes: {sorted(structured.__dict__)}")
print(f"  dict has accidental extra key: {'agge' in loose and 'age' in loose}")
print(f"  class contract is visible: {AccountMember.__init__.__code__.co_argcount == 3}")
#   structured attributes: ['age', 'name']
#   dict has accidental extra key: True
#   class contract is visible: True

# A class makes intended fields and operations explicit;
# classes can also add validation (introduced later).
# A normal class does not automatically forbid every
# extra attribute unless further controls are used.

# ============================================================
# [11] Reuse the blueprint [05:43]
# ============================================================
# One definition, many records with the same interface:

members = [
    MemberProfile("Omar", 24),
    MemberProfile("Lina", 31),
    MemberProfile("Sara", 28),
]

print(f"  member count: {len(members)}")
print(f"  all share MemberProfile: {all(isinstance(item, MemberProfile) for item in members)}")
print(f"  names: {[item.name for item in members]}")
#   member count: 3
#   all share MemberProfile: True
#   names: ['Omar', 'Lina', 'Sara']

# Consistent shape and behavior, distinct per-instance
# state -- useful as applications grow.

# ============================================================
# [12] One session: class, constructor, self, comparison
# ============================================================
# All core terms together:

print(f"  class: {MemberProfile.__name__}")
print(f"  constructor set attributes: {profile.__dict__ == {'name': 'Omar', 'age': 24}}")
print(f"  self identifies current data: {person.name}")
print(f"  class method: {account_member.label()}")
print(f"  dictionary stores values: {member_record['name']}, {member_record['age']}")
print(f"  instances independent: {profile.__dict__ is not profile_two.__dict__}")
#   class: MemberProfile
#   constructor set attributes: True
#   self identifies current data: Rana
#   class method: Omar (24)
#   dictionary stores values: Omar, 24
#   instances independent: True

# ============================================================
# [13] The summary: first practical OOP lesson
# ============================================================
# Class syntax, __init__ and self, from the transcript:
#
#   1. CLASS [01:00] -- `class Member:` defines a class;
#      `pass` is a valid empty body
#   2. PASCALCASE [01:00] -- names such as Member,
#      CourseMember and Car capitalize each word
#   3. __init__ [02:00] -- called automatically when a
#      new instance is created; initializes its state
#   4. self [02:40] -- required first parameter for an
#      instance method; it refers to the current object
#   5. ATTRIBUTES -- `self.name = name` stores data on
#      that particular instance
#   6. INSTANCES -- one class can create many objects
#      with independent attribute dictionaries
#   7. METHODS -- functions such as greet() and label()
#      use self to act on their instance
#   8. DICTS vs CLASSES [06:50] -- a dict flexibly stores
#      key/value data; a class describes expected fields
#      and can keep related behavior alongside them
#   9. LARGE APPS -- named structure and reusable methods
#      help organization and maintenance; extra validation
#      or restrictions can be added when needed
#  10. NEXT [06:29] -- continued practical coding makes
#      the OOP theory more familiar
#
# `class` draws the blueprint; `__init__` sets up the
# instance; `self` writes to the current object's data.
