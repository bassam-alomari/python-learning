# -----------------------------------------------------------------
# Lesson 106: instance methods -- self, full names and greetings
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : instance methods receive self, read instance
#            attributes, build a full name, branch on
#            gender, and call one method from another
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: continue instance attributes;
# now focus on instance methods and how to use them.
#
#   self [00:25-00:35] -- every method belonging to an
#   instance takes self first to access that object's data
#   FULL NAME [01:01] -- combine first, middle and last
#   names and return the result
#   GENDER [04:32-04:45] -- an extra attribute; if/else
#   changes the title/message (Mr or Mrs)
#   METHOD CALLS [08:00] -- call another method of the
#   same object through self

# ============================================================
# [1] Instance methods receive self [00:25-00:35]
# ============================================================
# A method uses self to work with the current instance:

class Member:
    def __init__(self, fname, mname, lname):
        self.fname = fname
        self.mname = mname
        self.lname = lname

    def full_name(self):
        return " ".join((self.fname, self.mname, self.lname))


member = Member("Osama", "Mohamed", "Elsayed")
print(f"  method name: {member.full_name.__name__}")
print(f"  method belongs to this instance: {member.full_name.__self__ is member}")
#   method name: full_name
#   method belongs to this instance: True

# When called as member.full_name(), Python supplies
# member as self automatically.

# ============================================================
# [2] Full-name method [01:01]
# ============================================================
# The method reads the three attributes and returns a
# combined string:

print(f"  full name: {member.full_name()}")
print(f"  return type: {type(member.full_name()).__name__}")
#   full name: Osama Mohamed Elsayed
#   return type: str

# The name parts remain separate attributes; the method
# provides a convenient combined view.

# ============================================================
# [3] Another member, another full name
# ============================================================
# The same method works with every instance:

member_two = Member("Mona", "Ali", "Hassan")
print(f"  first member: {member.full_name()}")
print(f"  second member: {member_two.full_name()}")
print(f"  same method works on both: {member.full_name.__func__ is member_two.full_name.__func__}")
#   first member: Osama Mohamed Elsayed
#   second member: Mona Ali Hassan
#   same method works on both: True

# Same method implementation, different self and data.

# ============================================================
# [4] Add a gender attribute [04:32-04:45]
# ============================================================
# Store gender along with the name during initialization:

class GreetingMember:
    def __init__(self, fname, mname, lname, gender):
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.gender = gender

    def full_name(self):
        return " ".join((self.fname, self.mname, self.lname))


male_member = GreetingMember("Omar", "Khaled", "Nasser", "male")
female_member = GreetingMember("Lina", "Ali", "Hassan", "female")
print(f"  male gender stored: {male_member.gender}")
print(f"  female gender stored: {female_member.gender}")
#   male gender stored: male
#   female gender stored: female

# ============================================================
# [5] Use if/else to select a title [04:45]
# ============================================================
# A method can branch on the object's gender attribute:

class TitledMember:
    def __init__(self, fname, gender):
        self.fname = fname
        self.gender = gender

    def title(self):
        if self.gender == "male":
            return "Mr"
        else:
            return "Mrs"


titled_male = TitledMember("Omar", "male")
titled_female = TitledMember("Lina", "female")
print(f"  male title: {titled_male.title()}")
print(f"  female title: {titled_female.title()}")
#   male title: Mr
#   female title: Mrs

# ============================================================
# [6] Gender changes the greeting [04:45]
# ============================================================
# Use the title and name to form a complete message:

class PersonGreeting:
    def __init__(self, fname, gender):
        self.fname = fname
        self.gender = gender

    def greeting(self):
        if self.gender == "male":
            return "Hello Mr " + self.fname
        else:
            return "Hello Mrs " + self.fname


person_male = PersonGreeting("Omar", "male")
person_female = PersonGreeting("Lina", "female")
print(f"  male greeting: {person_male.greeting()}")
print(f"  female greeting: {person_female.greeting()}")
#   male greeting: Hello Mr Omar
#   female greeting: Hello Mrs Lina

# ============================================================
# [7] Call a method from another method [08:00]
# ============================================================
# greet() calls full_name() through self:

class CompleteMember:
    def __init__(self, fname, mname, lname, gender):
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.gender = gender

    def full_name(self):
        return " ".join((self.fname, self.mname, self.lname))

    def greeting(self):
        if self.gender == "male":
            title = "Mr"
        else:
            title = "Mrs"
        return "Hello " + title + " " + self.full_name()


complete_male = CompleteMember("Omar", "Khaled", "Nasser", "male")
complete_female = CompleteMember("Lina", "Ali", "Hassan", "female")
print(f"  greeting calls full_name: {complete_male.greeting()}")
print(f"  second method call: {complete_female.greeting()}")
#   greeting calls full_name: Hello Mr Omar Khaled Nasser
#   second method call: Hello Mrs Lina Ali Hassan

# self.full_name() invokes the same object's method and
# uses its own attributes.

# ============================================================
# [8] A method can return data for later use
# ============================================================
# full_name() returns a string; the caller can store,
# inspect or format it:

stored_name = complete_male.full_name()
print(f"  stored full name: {stored_name}")
print(f"  name has three parts: {len(stored_name.split()) == 3}")
#   stored full name: Omar Khaled Nasser
#   name has three parts: True

# ============================================================
# [9] self keeps behavior instance-specific
# ============================================================
# Changing one object's gender affects only its greeting:

before = complete_male.greeting()
complete_male.gender = "female"
after = complete_male.greeting()
print(f"  before gender change: {before}")
print(f"  after gender change: {after}")
print(f"  other member unchanged: {complete_female.greeting()}")
#   before gender change: Hello Mr Omar Khaled Nasser
#   after gender change: Hello Mrs Omar Khaled Nasser
#   other member unchanged: Hello Mrs Lina Ali Hassan

# ============================================================
# [10] Inspect method signatures
# ============================================================
# Instance methods declare self first; other parameters
# follow it:

print(f"  full_name parameter count: {CompleteMember.full_name.__code__.co_argcount}")
print(f"  greeting parameter count: {CompleteMember.greeting.__code__.co_argcount}")
print(f"  self is first parameter: {CompleteMember.full_name.__code__.co_varnames[0] == 'self'}")
#   full_name parameter count: 1
#   greeting parameter count: 1
#   self is first parameter: True

# Accessed from the class, the function explicitly takes
# self; accessed from an instance, Python binds it.

# ============================================================
# [11] Reuse one method design across several objects
# ============================================================
# Three instances, same greeting behavior:

roster = (
    CompleteMember("Omar", "Khaled", "Nasser", "male"),
    CompleteMember("Lina", "Ali", "Hassan", "female"),
    CompleteMember("Rami", "Samir", "Saleh", "male"),
)
greetings = [item.greeting() for item in roster]

print(f"  greetings: {greetings}")
print(f"  all use one greeting method: {all(type(item).greeting is CompleteMember.greeting for item in roster)}")
#   greetings: ['Hello Mr Omar Khaled Nasser', 'Hello Mrs Lina Ali Hassan', 'Hello Mr Rami Samir Saleh']
#   all use one greeting method: True

# ============================================================
# [12] One session: self, full name, gender, method call
# ============================================================
# The lesson's main path in a handful of facts:

print(f"  full name: {complete_female.full_name()}")
print(f"  gender: {complete_female.gender}")
print(f"  gender-based greeting: {complete_female.greeting()}")
print(f"  method uses current self: {complete_female.greeting().endswith(complete_female.full_name())}")
print(f"  instance methods shared: {type(complete_male).greeting is type(complete_female).greeting}")
#   full name: Lina Ali Hassan
#   gender: female
#   gender-based greeting: Hello Mrs Lina Ali Hassan
#   method uses current self: True
#   instance methods shared: True

# ============================================================
# [13] The summary
# ============================================================
# Instance Methods, from the transcript:
#
#   1. self [00:25-00:35] -- first parameter for an
#      instance method; accesses the current object's data
#   2. FULL NAME [01:01] -- combine fname, mname, lname
#      and return the full-name string
#   3. INSTANCE DATA -- the same method works on member
#      objects with different names because self differs
#   4. GENDER [04:32-04:45] -- store gender as an
#      attribute and branch with if/else for Mr or Mrs
#   5. METHOD INSIDE METHOD [08:00] -- use
#      self.full_name() inside greeting() to reuse the
#      same object's name-building behavior
#   6. RETURN VALUES -- methods return strings that can
#      be saved, inspected and formatted by the caller
#   7. REUSE -- one method implementation serves all
#      instances while each uses its own attributes
#
# self is the bridge: it lets an instance method read the
# current object's attributes and call its other methods.
