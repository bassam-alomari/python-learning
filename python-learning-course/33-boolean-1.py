# -----------------------------------------------------------------
# Lesson 33: Boolean - Part 1 (True, False, bool(), Truthy, Falsy)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : boolean values, bool(), truthy values, falsy values
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# A Boolean can only be one of two things: True or False.
# We use it to ask a question in the code and let the answer decide
# what runs and what does not.

# ============================================================
# [1] The two Boolean values
# ============================================================
# There is no third option. A boolean is either True or False,
# and we write them with a capital first letter.

is_open = True
is_closed = False

print("is_open :", is_open)
# is_open : True
print("is_closed:", is_closed)
# is_closed: False

# Their type is bool.
print("type of True:", type(True))
# type of True: <class 'bool'>

# Useful detail: a boolean is also a number under the hood.
# True behaves like 1 and False behaves like 0.
print("int(True) =", int(True))
# int(True) = 1
print("int(False) =", int(False))
# int(False) = 0
print("True + True =", True + True)
# True + True = 2

# But they are not the same object as the numbers 1 and 0.
one = 1
print("True == one  :", True == one)   # True  -> same value
print("True is one  :", True is one)   # False -> but not the same object
print("True == True :", True == True)
# True is one  : False
# True == True : True

# ============================================================
# [2] Booleans come from asking a question
# ============================================================
# Every comparison gives us a boolean answer.

print("100 > 200 :", 100 > 200)   # False
print("100 > 90  :", 100 > 90)    # True
print("100 == 100:", 100 == 100)  # True
print("100 != 100:", 100 != 100)  # False

# Real life examples, like a bouncer checking an age limit.
age = 22
print("age >= 18 :", age >= 18)
# age >= 18 : True

password = "12345"
print("password == '12345':", password == "12345")
# password == '12345': True

# ============================================================
# [3] bool()  -> ask Python: is this value True or False?
# ============================================================
# bool() returns the boolean version of any value.
# Most of the time we never call it directly, because if, while,
# and not already use it for us. But it is very useful to see
# the rule clearly.

print("bool(100)       :", bool(100))        # True  -> non-zero number
print("bool(-5)        :", bool(-5))         # True  -> negative is still non-zero
print("bool(0)         :", bool(0))          # False -> zero
print("bool(0.0)       :", bool(0.0))        # False -> zero point zero
print("bool('Osama')   :", bool("Osama"))    # True  -> a non-empty string
print("bool('')        :", bool(""))         # False -> an empty string
print("bool([1, 2, 3]):", bool([1, 2, 3]))  # True  -> a non-empty list
print("bool([])        :", bool([]))         # False -> an empty list
print("bool(())        :", bool(()))         # False -> an empty tuple
print("bool({})        :", bool({}))         # False -> an empty dictionary
print("bool(set())     :", bool(set()))      # False -> an empty set
print("bool(True)      :", bool(True))       # True
print("bool(False)     :", bool(False))      # False
print("bool(None)      :", bool(None))       # False -> None means no value

# ============================================================
# [4] TRUTHY values  -> bool() gives True
# ============================================================
# Any non-zero number (positive or negative)
# Any non-empty string
# Any non-empty list, tuple, dictionary, or set
# The boolean True itself

# ============================================================
# [5] FALSY values  -> bool() gives False
# ============================================================
# The number zero (0 or 0.0)
# The empty string ""
# The empty containers [] , () , {} , set()
# The boolean False itself
# None  -> the special value that means "there is no value"

# A small table that shows the difference clearly.
samples = [
    ("100", 100), ("-5", -5), ("0", 0), ("0.0", 0.0),
    ("'Osama'", "Osama"), ("''", ""),
    ("[1, 2, 3]", [1, 2, 3]), ("[]", []),
    ("{}", {}), ("None", None), ("False", False), ("True", True),
]
for label, value in samples:
    print(f"{label:>10}  ->  bool() = {bool(value)}")

# ============================================================
# [6] The `not` keyword  -> flip the boolean
# ============================================================
# not True  becomes False, and not False becomes True.
print("not True :", not True)
# not True : False
print("not False:", not False)
# not False: True

# We can also use not with a value directly.
print("not 0      :", not 0)
# not 0      : True
print("not 'hello':", not "hello")
# not 'hello': False

# ============================================================
# Improvement (from me): explain WHY a value is truthy or falsy
# ============================================================
# Instead of just printing True or False, we can say the reason.
# This is very handy when you debug a condition that surprises you.

def describe(value):
    """Return a readable report explaining the truthy/falsy result."""
    if value is None:
        return "falsy  -> None means there is no value at all"
    if isinstance(value, bool):
        return f"falsy  -> the boolean {value}" if not value else "truthy -> the boolean True"
    if isinstance(value, (int, float)) and value == 0:
        return "falsy  -> zero has no truth in it"
    if isinstance(value, (str, list, tuple, dict, set)) and len(value) == 0:
        return f"falsy  -> an empty {type(value).__name__}"
    if isinstance(value, (int, float)):
        return f"truthy -> the non-zero number {value}"
    if isinstance(value, (str, list, tuple, dict, set)):
        return f"truthy -> a {type(value).__name__} that is not empty"
    return f"truthy -> {value!r}"


for value in [0, -3, "", "Osama", [], [1], None, True]:
    print(f"{value!r:>8}  ->  {describe(value)}")

# And a helper that behaves like a careful, explicit "has content" check.
def is_filled(value):
    """Return True only when the value carries real content."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, (str, list, tuple, dict, set)):
        return len(value) > 0
    return bool(value)


form = {"name": "Bassam", "phone": "", "age": 0, "city": None}
for field, value in form.items():
    print(f"{field:>6} -> is_filled = {is_filled(value)}")

# ============================================================
# SUMMARY
# ============================================================
# - A boolean has only two values: True and False.
# - Comparisons and conditions produce booleans.
# - bool(value) tells us if a value is truthy or falsy.
# - TRUTHY: any non-zero number, any non-empty string or container, True
# - FALSY : 0, 0.0, "", [], (), {}, set(), False, and None
# - not flips a boolean to its opposite.
# - In conditions, Python already applies bool() for you.

# ============================================================
# NEXT LESSON: Control Flow - if / elif / else conditions
# ============================================================
