# -----------------------------------------------------------------
# Lesson 113: encapsulation -- public, protected, private
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : access conventions, data hiding, underscore
#            naming, name mangling, getters/setters and
#            controlled updates
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: Encapsulation and data
# protection in OOP.
#
#   WHAT [00:10] -- limit direct access to some object data
#   to prevent accidental changes and keep the program stable
#   PUBLIC [00:22] -- ordinary names; accessible and
#   assignable from outside
#   PROTECTED -- one leading underscore (_name) signals a
#   convention: internal/subclass use; Python does not
#   strictly block outside access
#   PRIVATE -- two leading underscores (__name) trigger
#   name mangling; use methods (getters/setters) for
#   controlled access
#   PYTHON'S APPROACH [07:09] -- name mangling is not
#   absolute secrecy; encapsulation relies on conventions
#   and developer cooperation

# ============================================================
# [1] Encapsulation: control how data is changed [00:10]
# ============================================================
# A class can expose safe operations instead of inviting
# arbitrary edits to its internal state:

print("  encapsulation: control access to object data")
print("  goal: prevent accidental invalid changes")
#   encapsulation: control access to object data
#   goal: prevent accidental invalid changes

# ============================================================
# [2] Public attributes [00:22]
# ============================================================
# Public is the normal Python default:

class PublicMember:
    def __init__(self, name):
        self.name = name


public_member = PublicMember("Amina")
print(f"  public value: {public_member.name}")
public_member.name = "Mona"
print(f"  public value changed directly: {public_member.name}")
#   public value: Amina
#   public value changed directly: Mona

# ============================================================
# [3] Protected convention: one underscore
# ============================================================
# A leading underscore communicates intended internal
# use, but does not prevent access:

class ProtectedMember:
    def __init__(self, name):
        self._name = name


protected_member = ProtectedMember("Rami")
print(f"  protected convention value: {protected_member._name}")
print(f"  underscore attribute exists: {'_name' in protected_member.__dict__}")
#   protected convention value: Rami
#   underscore attribute exists: True

# The leading underscore is a convention, not a runtime
# access barrier.

# ============================================================
# [4] Protected attributes are still accessible
# ============================================================
# Python permits access from outside; the underscore
# asks code readers to treat it with care:

protected_member._name = "Rami updated"
print(f"  outside access still works: {protected_member._name}")
#   outside access still works: Rami updated

# ============================================================
# [5] Private-style name with double underscore
# ============================================================
# __name is transformed by name mangling inside the class:

class PrivateMember:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


private_member = PrivateMember("Salma")
print(f"  getter reads private-style value: {private_member.get_name()}")
print(f"  literal __name key stored: {'__name' in private_member.__dict__}")
print(f"  mangled key stored: {'_PrivateMember__name' in private_member.__dict__}")
#   getter reads private-style value: Salma
#   literal __name key stored: False
#   mangled key stored: True

# ============================================================
# [6] Direct private-style access is not the normal name
# ============================================================
# The original spelling is not present as an instance key;
# the class can provide a public getter instead:

print(f"  getter is callable: {callable(private_member.get_name)}")
print(f"  public getter result: {private_member.get_name()}")

try:
    private_member.__name
except AttributeError:
    direct_name_missing = True
else:
    direct_name_missing = False

print(f"  direct __name lookup fails: {direct_name_missing}")
#   getter is callable: True
#   public getter result: Salma
#   direct __name lookup fails: True

# ============================================================
# [7] Name mangling is not absolute secrecy [07:09]
# ============================================================
# Python rewrites __name to _ClassName__name. Knowing
# that transformed name can reach it:

print(f"  mangled access value: {private_member._PrivateMember__name}")
print(f"  mangling prefix: {'_PrivateMember__name'.startswith('_PrivateMember__')}")
#   mangled access value: Salma
#   mangling prefix: True

# Name mangling avoids accidental clashes and casual
# access; it is not encryption or a security boundary.

# ============================================================
# [8] Getter and setter for controlled access
# ============================================================
# A setter can validate before changing a private-style
# attribute:

class Account:
    def __init__(self, owner, balance):
        self.__owner = owner
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def set_balance(self, amount):
        if amount < 0:
            raise ValueError("balance cannot be negative")
        self.__balance = amount


account = Account("Amina", 50)
account.set_balance(75)
print(f"  balance after valid setter: {account.get_balance()}")
#   balance after valid setter: 75

# ============================================================
# [9] Setter rejects invalid changes
# ============================================================
# An invalid value is rejected; the old value survives:

try:
    account.set_balance(-10)
except ValueError as error:
    invalid_rejected = str(error) == "balance cannot be negative"
else:
    invalid_rejected = False

print(f"  negative balance rejected: {invalid_rejected}")
print(f"  balance remains unchanged: {account.get_balance()}")
#   negative balance rejected: True
#   balance remains unchanged: 75

# ============================================================
# [10] Compare access styles
# ============================================================
# Show the naming convention and access route together:

print(f"  public: {public_member.name}")
print(f"  protected convention: {protected_member._name}")
print(f"  private-style through getter: {private_member.get_name()}")
print(f"  controlled account balance: {account.get_balance()}")
#   public: Mona
#   protected convention: Rami updated
#   private-style through getter: Salma
#   controlled account balance: 75

# ============================================================
# [11] Why use a setter?
# ============================================================
# A controlled method can enforce an invariant; direct
# state access would skip that validation:

print(f"  accepted balance is nonnegative: {account.get_balance() >= 0}")
print(f"  invalid attempt left valid state: {account.get_balance() == 75}")
print(f"  data access goes through methods: {account.get_balance() == 75}")
#   accepted balance is nonnegative: True
#   invalid attempt left valid state: True
#   data access goes through methods: True

# ============================================================
# [12] One session: conventions and controlled access
# ============================================================
# Core facts from the lesson:

print(f"  public can be directly changed: {public_member.name == 'Mona'}")
print(f"  protected remains accessible: {protected_member._name == 'Rami updated'}")
print(f"  private spelling is mangled: {'_PrivateMember__name' in private_member.__dict__}")
print(f"  getter returns private-style value: {private_member.get_name()}")
print(f"  setter rejects invalid balance: {invalid_rejected}")
print(f"  Python mangling is reversible by convention: {private_member._PrivateMember__name == 'Salma'}")
#   public can be directly changed: True
#   protected remains accessible: True
#   private spelling is mangled: True
#   getter returns private-style value: Salma
#   setter rejects invalid balance: True
#   Python mangling is reversible by convention: True

# ============================================================
# [13] The summary
# ============================================================
# Encapsulation, from the transcript:
#
#   1. WHAT [00:10] -- control access to object data so
#      accidental edits do not break valid state
#   2. PUBLIC [00:22] -- ordinary names; freely accessible
#      and assignable through the object
#   3. PROTECTED -- _name signals intended class/subclass
#      use; Python still allows outside access
#   4. PRIVATE -- __name is name-mangled to
#      _ClassName__name; ordinary direct spelling fails
#   5. GETTERS / SETTERS -- methods can expose data and
#      validate updates (negative balance rejected)
#   6. NAME MANGLING [07:09] -- discourages accidental
#      access/name clashes; not strict secrecy or security
#   7. PYTHON CONVENTION -- "we are all consenting adults";
#      encapsulation relies on clear conventions and
#      cooperative code, with validation where needed
#
# Public is open; one underscore is a warning; two
# underscores trigger name mangling, not a vault.
