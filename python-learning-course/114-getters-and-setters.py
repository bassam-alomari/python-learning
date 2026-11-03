# -----------------------------------------------------------------
# Lesson 114: getters and setters -- controlled attributes
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : getter to read private-style data, setter to
#            validate and update it, name mangling, and
#            preserving an object's valid state
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: continue Encapsulation with
# Getters and Setters.
#
#   WHY [00:10] -- Python does not strictly prevent access
#   to private-style data; methods provide a standard,
#   organized way to control reading and updating
#   GETTER -- returns a property's value to the caller
#   SETTER -- accepts a new value, validates it, then
#   updates the private-style attribute
#   PRACTICE [01:34] -- get_name() and set_name(new_name)
#   operate on self.__name

# ============================================================
# [1] Private-style attribute and getter [00:10]
# ============================================================
# __name is name-mangled; get_name() exposes it in a
# controlled, readable way:

class Member:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


member = Member("Amina")
print(f"  getter result: {member.get_name()}")
print(f"  getter returns text: {isinstance(member.get_name(), str)}")
#   getter result: Amina
#   getter returns text: True

# ============================================================
# [2] Getter reads the current object's value
# ============================================================
# Each instance has its own private-style name:

member_two = Member("Omar")
print(f"  first getter: {member.get_name()}")
print(f"  second getter: {member_two.get_name()}")
print(f"  values belong to different objects: {member.get_name() != member_two.get_name()}")
#   first getter: Amina
#   second getter: Omar
#   values belong to different objects: True

# ============================================================
# [3] Setter: update under class control [01:34]
# ============================================================
# set_name(new_name) changes the current object's
# private-style attribute:

class EditableMember:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        self.__name = new_name


editable = EditableMember("Lina")
editable.set_name("Lina Noor")
print(f"  after setter: {editable.get_name()}")
#   after setter: Lina Noor

# ============================================================
# [4] Validate before assigning
# ============================================================
# A setter can enforce rules before changing the stored
# value; this one rejects blank/non-string names:

class ValidatedMember:
    def __init__(self, name):
        self.__name = ""
        self.set_name(name)

    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        if not isinstance(new_name, str):
            raise TypeError("name must be text")
        cleaned = new_name.strip()
        if not cleaned:
            raise ValueError("name cannot be empty")
        self.__name = cleaned


validated = ValidatedMember("  Sara  ")
print(f"  initial value trimmed: {validated.get_name()}")
validated.set_name("  Sara Ali  ")
print(f"  updated value trimmed: {validated.get_name()}")
#   initial value trimmed: Sara
#   updated value trimmed: Sara Ali

# ============================================================
# [5] Reject an invalid value and preserve old data
# ============================================================
# A failed validation raises before assignment, so the
# existing name remains intact:

try:
    validated.set_name("   ")
except ValueError as error:
    empty_rejected = str(error) == "name cannot be empty"
else:
    empty_rejected = False

print(f"  blank name rejected: {empty_rejected}")
print(f"  old value preserved: {validated.get_name()}")
#   blank name rejected: True
#   old value preserved: Sara Ali

# ============================================================
# [6] Setter can validate the type too
# ============================================================
# Reject a non-string value with a specific exception:

try:
    validated.set_name(123)
except TypeError as error:
    wrong_type_rejected = str(error) == "name must be text"
else:
    wrong_type_rejected = False

print(f"  non-text rejected: {wrong_type_rejected}")
print(f"  value still valid: {validated.get_name() == 'Sara Ali'}")
#   non-text rejected: True
#   value still valid: True

# ============================================================
# [7] Getter and setter operate per instance
# ============================================================
# Updating one object leaves another untouched:

validated_two = ValidatedMember("Nour")
validated.set_name("Sara")
print(f"  first member updated: {validated.get_name()}")
print(f"  second member unchanged: {validated_two.get_name()}")
#   first member updated: Sara
#   second member unchanged: Nour

# ============================================================
# [8] The private-style spelling is name-mangled
# ============================================================
# The getter/setter use __name inside the class; Python
# stores it with a class-specific name:

print(f"  original __name key absent: {'__name' not in validated.__dict__}")
print(f"  mangled key present: {'_ValidatedMember__name' in validated.__dict__}")
print(f"  public getter still works: {validated.get_name()}")
#   original __name key absent: True
#   mangled key present: True
#   public getter still works: Sara

# This is name mangling, not encryption; the methods
# define the intended interface.

# ============================================================
# [9] A setter reports successful updates
# ============================================================
# Returning a status can make the result explicit:

class StatusMember:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        if not isinstance(new_name, str) or not new_name.strip():
            return False
        self.__name = new_name.strip()
        return True


status_member = StatusMember("Rami")
accepted = status_member.set_name("Rami Saleh")
rejected = status_member.set_name("")
print(f"  valid setter reports success: {accepted}")
print(f"  invalid setter reports failure: {not rejected}")
print(f"  stored value after both calls: {status_member.get_name()}")
#   valid setter reports success: True
#   invalid setter reports failure: True
#   stored value after both calls: Rami Saleh

# ============================================================
# [10] Compare direct update and controlled update
# ============================================================
# Public data can be overwritten directly; a getter/setter
# pair keeps an update path in one place:

class DirectRecord:
    def __init__(self, name):
        self.name = name


direct = DirectRecord("Amina")
direct.name = ""
status_member.set_name("")
print(f"  direct public value can become blank: {direct.name == ''}")
print(f"  validated value remains nonblank: {bool(status_member.get_name())}")
#   direct public value can become blank: True
#   validated value remains nonblank: True

# ============================================================
# [11] Use the accessor methods as an interface
# ============================================================
# Callers need only the public methods, not internal
# storage details:

def rename_and_read(obj, new_name):
    changed = obj.set_name(new_name)
    return changed, obj.get_name()


rename_result = rename_and_read(status_member, "  Dana  ")
print(f"  accessor result: {rename_result}")
#   accessor result: (True, 'Dana')

# ============================================================
# [12] One session: get, set, validate
# ============================================================
# The complete flow in compact form:

session_member = ValidatedMember("Huda")
before = session_member.get_name()
session_member.set_name("Huda Khaled")
after = session_member.get_name()

print(f"  before: {before}")
print(f"  after valid setter: {after}")
print(f"  type and blank checks protect data: {wrong_type_rejected and empty_rejected}")
print(f"  per-instance storage: {session_member.get_name() != validated_two.get_name()}")
#   before: Huda
#   after valid setter: Huda Khaled
#   type and blank checks protect data: True
#   per-instance storage: True

# ============================================================
# [13] The summary
# ============================================================
# Getters and Setters, from the transcript:
#
#   1. WHY [00:10] -- Python privacy is not an absolute
#      access barrier; methods provide a controlled API
#   2. GETTER -- get_name() returns the private-style value
#      without exposing the storage name to normal callers
#   3. SETTER [01:34] -- set_name(new_name) updates
#      self.__name in one organized place
#   4. VALIDATION -- require a string, trim whitespace,
#      reject blank values before assigning
#   5. SAFETY -- rejected updates preserve the previous
#      valid value
#   6. PER-INSTANCE -- each object's getter/setter uses
#      that instance's own name
#   7. NAME MANGLING -- __name becomes
#      _ClassName__name; a convention/tooling feature,
#      not secrecy or encryption
#   8. INTERFACE -- callers use get_name()/set_name()
#      while implementation details remain organized
#
# A getter reads; a setter validates then writes. Put
# rules at the update boundary to protect valid state.
