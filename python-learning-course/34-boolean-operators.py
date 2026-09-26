# -----------------------------------------------------------------
# Lesson 34: Boolean Operators - and, or, not
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : combining conditions with and, or, and not
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# In real applications we rarely check ONE condition. We usually
# need two or more at the same time, and these three operators are
# the tool for joining them together.

# ============================================================
# The situation: a real app rule
# ============================================================
# To unlock a feature, the user must be OLD ENOUGH and must come
# from an ALLOWED country. This is exactly the shape of the rule.

age = 36
country = "Egypt"

# ============================================================
# [1] and  -> EVERY condition must be True
# ============================================================
# and gives True only when all its conditions are True.
# One single False is enough to make the whole result False.

print("age > 16 and country == 'Egypt':", age > 16 and country == "Egypt")
# age > 16 and country == 'Egypt': True

print("age > 40 and country == 'Egypt':", age > 40 and country == "Egypt")
# age > 40 and country == 'Egypt': False   (only the age failed)

print("age > 40 and country == 'USA'  :", age > 40 and country == "USA")
# age > 40 and country == 'USA'  : False   (both failed)

# Three conditions work exactly the same way.
has_id = True
print("three conditions:", age > 16 and country == "Egypt" and has_id)
# three conditions: True

# ============================================================
# [2] or  -> AT LEAST ONE condition must be True
# ============================================================
# or gives True when any single condition is True.
# It gives False ONLY when every condition is False.

print("age > 40 or country == 'Egypt':", age > 40 or country == "Egypt")
# age > 40 or country == 'Egypt': True   (the country matched)

print("age > 40 or country == 'USA'  :", age > 40 or country == "USA")
# age > 40 or country == 'USA'  : False  (nothing matched)

# A realistic or-rule: give access if the user is a member,
# or if they used a coupon code.
is_member = False
coupon = "SAVE10"
print("member or coupon:", is_member or coupon == "SAVE10")
# member or coupon: True

# ============================================================
# [3] not  -> flip the logical state
# ============================================================
# not turns True into False and False into True.
# It is a NEGATION operator.

print("not (age > 40):", not (age > 40))
# not (age > 40): True   (age is 36, so the condition was False)

print("not (age > 16):", not (age > 16))
# not (age > 16): False  (the condition was True)

print("not True :", not True)
# not True : False
print("not False:", not False)
# not False: True

# ============================================================
# [4] The complete truth table
# ============================================================
# This is the best way to memorize the three operators.
# Only four rows exist, because there are only two booleans.

print("A      B      A and B   A or B    not A")
for a in (True, False):
    for b in (True, False):
        print(f"{a!s:<6} {b!s:<6} {str(a and b):<9} {str(a or b):<9} {str(not a)}")

# A True   True   True      True      False
# A True   False  False     True      False
# A False  True   False     True      True
# A False  False  False     False     True

# ============================================================
# [5] Operator precedence: not > and > or
# ============================================================
# not is evaluated first, then and, then or.
# This is why the parentheses really matter here.

# Without parentheses: not binds first -> (not True) and False
print("not True and False   :", not True and False)
# not True and False   : False

# With parentheses we ask a different question
print("not (True and False) :", not (True and False))
# not (True and False) : True

# and binds tighter than or
print("True or True and False:", True or True and False)
# True or True and False: True   -> True or (True and False) = True or False

# A safe habit: always write the parentheses you mean.
print("(True or True) and False:", (True or True) and False)
# (True or True) and False: False

# ============================================================
# [6] SHORT CIRCUIT: and and or do not always check everything
# ============================================================
# Python stops as soon as the answer is already known. This is a
# very useful behaviour, so never put an expensive or dangerous
# call on the wrong side of and / or.

def second_check(value):
    print("   second_check() was called")
    return value

# With and: the first side is False, so the answer is already
# False and the right side is NEVER evaluated.
print("False and second_check(True):", False and second_check(True))
# False and second_check(True): False
# (note: "second_check() was called" was NOT printed)

# With or: the first side is True, so the answer is already
# True and the right side is NEVER evaluated.
print("True or second_check(True)  :", True or second_check(True))
# True or second_check(True)  : True
# (note: again the function was NOT called)

# This is exactly how we protect risky code safely.
# The expensive message is only built when debug is turned on.
debug = False
if debug and second_check("build this expensive message"):
    pass

# ============================================================
# [7] and / or return an OPERAND, not always True/False
# ============================================================
# This surprises almost every beginner. These operators return one
# of their operands, and we use that in real code all the time.

print("5 and 3          :", 5 and 3)        # 3   -> 5 is truthy, so the right side wins
print("0 and 3          :", 0 and 3)        # 0   -> 0 is falsy, so it wins
print("5 or 3           :", 5 or 3)         # 5   -> 5 is truthy, so it wins
print("0 or 'default'   :", 0 or "default") # default

# The classic "safe default" pattern built on the same rule.
name = ""
print("display name:", name or "Anonymous")
# display name: Anonymous
count = 0
print("display count:", count or 1)
# display count: 1

# ============================================================
# Improvement (from me): a validator that explains itself
# ============================================================
# Instead of returning a bare boolean, we return the reason too.
# A boolean alone never tells you WHY something failed.

ALLOWED_COUNTRIES = {"Egypt", "Jordan", "Saudi Arabia", "UAE"}


def check_access(age, country, min_age=18):
    """Return (allowed: bool, reason: str) for the access rule."""
    old_enough = age >= min_age
    country_ok = country in ALLOWED_COUNTRIES

    if old_enough and country_ok:
        return True, f"access granted for {country} (age {age})"
    if not old_enough:
        return False, f"age {age} is below the minimum age {min_age}"
    return False, f"country '{country}' is not in the allowed list"


tests = [
    (36, "Egypt"),
    (12, "Egypt"),
    (30, "USA"),
    (17, "Jordan"),
]
for person_age, person_country in tests:
    allowed, reason = check_access(person_age, person_country)
    label = "ALLOW" if allowed else "DENY"
    print(f"[{label}] age={person_age} country={person_country} -> {reason}")

# [ALLOW] age=36 country=Egypt -> access granted for Egypt (age 36)
# [DENY ] age=12 country=Egypt -> age 12 is below the minimum age 18
# [DENY ] age=30 country=USA   -> country 'USA' is not in the allowed list
# [DENY ] age=17 country=Jordan -> age 17 is below the minimum age 18

# ============================================================
# SUMMARY
# ============================================================
# - and  : True only when EVERY condition is True
# - or   : True when AT LEAST ONE condition is True
# - not  : flips True to False and False to True
# - Precedence order: not, then and, then or. Use parentheses!
# - Short circuit: and skips the right side on False,
#   or skips the right side on True. Use it to guard risky code.
# - and / or return one of their operands, which gives us the
#   `value or "default"` pattern.

# ============================================================
# NEXT LESSON: Control Flow - the if / elif / else statements
# ============================================================
