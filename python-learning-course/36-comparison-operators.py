# -----------------------------------------------------------------
# Lesson 36: Comparison Operators (Relational Operators)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : == != > < >= <=
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# Comparison operators are the ones that sit BETWEEN two values.
# They ask a question and answer with True or False.
# They are almost the same in every programming language.

# ============================================================
# [1] Equal to  ==
# ============================================================
# == checks whether the two values are EQUAL.
# Do not confuse it with = , which STORES a value.

print("100 == 100 :", 100 == 100)
# 100 == 100 : True
print("100 == 200 :", 100 == 200)
# 100 == 200 : False

# Text works the same way.
print("'python' == 'python':", "python" == "python")
# 'python' == 'python': True

# ============================================================
# [2] Not equal  !=
# ============================================================
# != is the opposite of ==. It is True when the values differ.

print("100 != 100 :", 100 != 100)
# 100 != 100 : False   (they ARE equal, so this is False)
print("100 != 200 :", 100 != 200)
# 100 != 200 : True

# ============================================================
# [3] Greater than  >   and  Less than  <
# ============================================================

print("100 > 200  :", 100 > 200)
# 100 > 200  : False
print("200 > 100  :", 200 > 100)
# 200 > 100  : True

print("100 < 200  :", 100 < 200)
# 100 < 200  : True
print("200 < 100  :", 200 < 100)
# 200 < 100  : False

# The direction matters: 100 > 200 is not the same as 100 < 200.

# ============================================================
# [4] Greater than or equal  >=   and  Less than or equal  <=
# ============================================================
# These are satisfied when ONE of the two situations happens:
# either strictly bigger/lower, or exactly the same.

print("100 >= 100 :", 100 >= 100)
# 100 >= 100 : True   (equal counts)
print("100 >= 200 :", 100 >= 200)
# 100 >= 200 : False
print("200 >= 100 :", 200 >= 100)
# 200 >= 100 : True

print("100 <= 100 :", 100 <= 100)
# 100 <= 100 : True
print("100 <= 200 :", 100 <= 200)
# 100 <= 200 : True
print("200 <= 100 :", 200 <= 100)
# 200 <= 100 : False

# ============================================================
# [5] The classic mistake:  =  versus  ==
# ============================================================
# = STORES a value, it cannot be used in a question.
# == ASKS a question and gives True or False.

x = 10        # this stores 10 inside x
print("x == 10   :", x == 10)
# x == 10   : True

# If you write this by mistake:
# if x = 10:        -> SyntaxError, because = cannot join a question
# The correct form is:
# if x == 10:

# ============================================================
# [6] Comparing strings: case matters, and order is alphabetical
# ============================================================
# String comparison is case SENSITIVE, and it follows the order of
# the letters, so it works like a dictionary.

print("'apple' == 'apple' :", "apple" == "apple")
# 'apple' == 'apple' : True
print("'apple' == 'Apple' :", "apple" == "Apple")
# 'apple' == 'Apple' : False   (only the capital A differs)

# Uppercase letters come before lowercase ones.
print("'Z' < 'a' :", "Z" < "a")
# 'Z' < 'a' : True

# So we usually normalize first:
print("'Apple'.lower() == 'apple':", "Apple".lower() == "apple")
# 'Apple'.lower() == 'apple': True

# ============================================================
# [7] Comparing different types
# ============================================================
# == and != are safe: they simply answer False or True.
print("100 == '100' :", 100 == "100")
# 100 == '100' : False   (an int is never equal to a str)

# But the ORDER comparisons cannot work between different types,
# so Python raises a TypeError.
try:
    print(100 < "100")
except TypeError as err:
    print("100 < '100' ->", err)
# 100 < '100' -> '<' not supported between instances of 'int' and 'str'

# ============================================================
# [8] Chained comparisons  (a Python speciality)
# ============================================================
# Python lets us chain two comparisons in a single expression,
# and it means: the first AND the second must be True.

print("10 < 20 < 30  :", 10 < 20 < 30)
# 10 < 20 < 30  : True
print("10 < 20 < 15  :", 10 < 20 < 15)
# 10 < 20 < 15  : False  (the second part fails)
print("30 < 20 < 10  :", 30 < 20 < 10)
# 30 < 20 < 10  : False

# This is much cleaner than writing 10 < 20 and 20 < 30
print("long way     :", 10 < 20 and 20 < 30)
# long way     : True

# The range check you need all the time:
score = 75
print("0 <= score <= 100:", 0 <= score <= 100)
# 0 <= score <= 100: True

# ============================================================
# [9] The complete operator table
# ============================================================
print("a = 100, b = 200")
a, b = 100, 200
print("a == b  ->", a == b)
print("a != b  ->", a != b)
print("a >  b  ->", a > b)
print("a <  b  ->", a < b)
print("a >= b  ->", a >= b)
print("a <= b  ->", a <= b)

# ============================================================
# Improvement (from me): a comparison report and a safe wrapper
# ============================================================
# A function that runs all six operators at once and prints the
# answers, plus a version that survives a type mismatch.

def compare_report(a, b):
    """Return a readable report of all six comparison operators."""
    rows = [
        ("a == b", a == b),
        ("a != b", a != b),
        ("a >  b", a > b),
        ("a <  b", a < b),
        ("a >= b", a >= b),
        ("a <= b", a <= b),
    ]
    return "\n".join(f"  {expr:<7} {result}" for expr, result in rows)


def safe_compare(a, b):
    """compare_report, but it explains the failure instead of crashing."""
    try:
        return compare_report(a, b)
    except TypeError as err:
        return f"  cannot order these types: {err}"


print("compare 100 and 200:")
print(compare_report(100, 200))

print("compare 100 and 100:")
print(compare_report(100, 100))

print("compare 100 and '100':")
print(safe_compare(100, "100"))

# compare 100 and 200:
#   a == b  False
#   a != b  True
#   a >  b  False
#   a <  b  True
#   a >= b  False
#   a <= b  True

# ============================================================
# SUMMARY
# ============================================================
# - ==  : equal
# - !=  : not equal
# - >   : greater than          <  : less than
# - >=  : greater than or equal <= : less than or equal
# - =   STORES a value, == ASKS a question. Never mix them up.
# - String comparison is case sensitive and follows letter order.
# - == between different types gives False, but < and > give TypeError.
# - Python chains comparisons: 0 <= score <= 100 is valid and clean.
# - These operators are the foundation of every if condition.

# ============================================================
# NEXT LESSON: Control Flow - the if / elif / else statements
# ============================================================
