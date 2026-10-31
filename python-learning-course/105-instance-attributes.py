# -----------------------------------------------------------------
# Lesson 105: instance attributes -- each object has its own data
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : instance attributes, bind values with self
#            in __init__, instantiate with arguments,
#            access with dot notation, combine full names
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: focus on Instance Attributes
# and how each object receives and stores its own data.
#
#   INSTANCE ATTRIBUTES [01:10] -- per-object values,
#   independent from other instances (e.g. each user has
#   a separate name and description)
#   self [02:07] -- inside __init__, bind values to the
#   current instance: self.fname = fname, etc.
#   INSTANTIATION [03:09] -- pass values in the class call
#   ACCESS [06:24] -- read values with dot notation and
#   combine them to display a full name

# ============================================================
# [1] Define a Member class with instance attributes
# ============================================================
# Each input becomes an attribute on the new object:

class Member:
    def __init__(self, fname, mname, lname, description):
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.description = description


print(f"  class has initializer: {callable(Member.__init__)}")
print(f"  four fields are initialized: {Member.__init__.__code__.co_argcount == 5}")
#   class has initializer: True
#   four fields are initialized: True

# self is the new current instance; each assignment
# creates a value attached to that object.

# ============================================================
# [2] Instantiate and pass values [03:09]
# ============================================================
# Values go inside the parentheses in the order the
# initializer expects:

member1 = Member("Osama", "Mohamed", "Elsayed", "Python learner")

print(f"  first name stored: {member1.fname}")
print(f"  middle name stored: {member1.mname}")
print(f"  last name stored: {member1.lname}")
print(f"  description stored: {member1.description}")
#   first name stored: Osama
#   middle name stored: Mohamed
#   last name stored: Elsayed
#   description stored: Python learner

# ============================================================
# [3] Access attributes with dot notation [06:24]
# ============================================================
# Each attribute is read from the object with a dot:

print(f"  member1.fname: {member1.fname}")
print(f"  member1.mname: {member1.mname}")
print(f"  member1.lname: {member1.lname}")
#   member1.fname: Osama
#   member1.mname: Mohamed
#   member1.lname: Elsayed

# The dot selects a specific attribute from this object.

# ============================================================
# [4] Combine attributes into a full name
# ============================================================
# Join the first, middle and last names for display:

full_name = member1.fname + " " + member1.mname + " " + member1.lname
print(f"  full name: {full_name}")
#   full name: Osama Mohamed Elsayed

# The pieces remain separately available even when
# displayed together.

# ============================================================
# [5] Create a second independent member [01:10]
# ============================================================
# Same class, different data for a different object:

member2 = Member("Mona", "Ali", "Hassan", "Data analyst")

print(f"  member2 first name: {member2.fname}")
print(f"  member2 description: {member2.description}")
print(f"  first member unchanged: {member1.fname == 'Osama'}")
#   member2 first name: Mona
#   member2 description: Data analyst
#   first member unchanged: True

# ============================================================
# [6] The instance dictionaries show ownership
# ============================================================
# Each instance stores its own attributes:

print(f"  member1 data: {member1.__dict__}")
print(f"  member2 data: {member2.__dict__}")
print(f"  separate dictionaries: {member1.__dict__ is not member2.__dict__}")
#   member1 data: {'fname': 'Osama', 'mname': 'Mohamed', 'lname': 'Elsayed', 'description': 'Python learner'}
#   member2 data: {'fname': 'Mona', 'mname': 'Ali', 'lname': 'Hassan', 'description': 'Data analyst'}
#   separate dictionaries: True

# The stored fields are similar; the values belong to
# their own instances.

# ============================================================
# [7] Same attribute names, separate values
# ============================================================
# Assigning a new value on member2 does not change member1:

member2.description = "Python instructor"
print(f"  member2 updated description: {member2.description}")
print(f"  member1 description unchanged: {member1.description}")
print(f"  values remain independent: {member1.description != member2.description}")
#   member2 updated description: Python instructor
#   member1 description unchanged: Python learner
#   values remain independent: True

# ============================================================
# [8] Build a full-name helper using self
# ============================================================
# A method can use the current instance's own attributes:

class NamedMember:
    def __init__(self, fname, mname, lname):
        self.fname = fname
        self.mname = mname
        self.lname = lname

    def full_name(self):
        return " ".join((self.fname, self.mname, self.lname))


named = NamedMember("Osama", "Mohamed", "Elsayed")
print(f"  method full name: {named.full_name()}")
print(f"  method uses current instance: {named.full_name() == full_name}")
#   method full name: Osama Mohamed Elsayed
#   method uses current instance: True

# ============================================================
# [9] Instantiate several objects from the same class
# ============================================================
# Each one receives its own values at construction:

members = (
    NamedMember("Osama", "Mohamed", "Elsayed"),
    NamedMember("Mona", "Ali", "Hassan"),
    NamedMember("Rami", "Khaled", "Nasser"),
)
names = [item.full_name() for item in members]

print(f"  member names: {names}")
print(f"  each object has separate data: {len({id(item.__dict__) for item in members}) == 3}")
#   member names: ['Osama Mohamed Elsayed', 'Mona Ali Hassan', 'Rami Khaled Nasser']
#   each object has separate data: True

# ============================================================
# [10] Attributes are available individually or together
# ============================================================
# Read individual fields or build a formatted display:

display = f"{member2.fname} {member2.mname} {member2.lname} — {member2.description}"
print(f"  individual first name: {member2.fname}")
print(f"  combined display: {display}")
#   individual first name: Mona
#   combined display: Mona Ali Hassan — Python instructor

# ============================================================
# [11] Check the instance's stored fields
# ============================================================
# The class creates the expected attribute names for
# each constructed member:

expected_fields = {"fname", "mname", "lname", "description"}
print(f"  member1 has all fields: {set(member1.__dict__) == expected_fields}")
print(f"  member2 has all fields: {set(member2.__dict__) == expected_fields}")
print(f"  member1 and member2 are distinct objects: {member1 is not member2}")
#   member1 has all fields: True
#   member2 has all fields: True
#   member1 and member2 are distinct objects: True

# ============================================================
# [12] One session: pass, store, access and display
# ============================================================
# The lesson's complete cycle in a compact summary:

print(f"  instance count: {len(members)}")
print(f"  first full name: {members[0].full_name()}")
print(f"  second full name: {members[1].full_name()}")
print(f"  member1 description: {member1.description}")
print(f"  member2 description: {member2.description}")
print(f"  independent data verified: {member1.fname != member2.fname and member1.description != member2.description}")
#   instance count: 3
#   first full name: Osama Mohamed Elsayed
#   second full name: Mona Ali Hassan
#   member1 description: Python learner
#   member2 description: Python instructor
#   independent data verified: True

# ============================================================
# [13] The summary
# ============================================================
# Instance Attributes, from the transcript:
#
#   1. INSTANCE ATTRIBUTES [01:10] -- values belonging to
#      one object, independent from other instances
#   2. self [02:07] -- bind each incoming value in
#      __init__: self.fname = fname, self.mname = mname,
#      and so on
#   3. INSTANTIATION [03:09] -- pass arguments when
#      constructing: Member("Osama", "Mohamed", ...)
#   4. DOT ACCESS [06:24] -- member1.fname, mname, lname,
#      description; read each field directly
#   5. COMBINE -- join the separate name parts to display
#      a full name while retaining each attribute
#   6. INDEPENDENCE -- member2's data and edits do not
#      change member1; distinct instance dictionaries prove it
#   7. REUSE -- a method uses self to build a full name
#      for any instance of the class
#
# self stores the data on the current object; the dot
# retrieves that object's own value.
