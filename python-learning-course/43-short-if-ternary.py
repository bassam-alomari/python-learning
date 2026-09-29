# -----------------------------------------------------------------
# Lesson 43: Short If - the Ternary Conditional Operator
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : ternary operator, one-liner conditions, expressions
# Type     : Educational + Practical Project
# Builder  : local assistant
# -----------------------------------------------------------------
# Sometimes an if/else is so simple that writing it on four lines
# is a waste. Python gives us a short form that fits on ONE line.
# It is the same logic, exactly the same logic, just compressed.

# ============================================================
# [1] The long way, for comparison
# ============================================================
# This is what we learned in the previous lesson.

country = "Egypt"

if country == "Egypt":
    price = 20
else:
    price = 30

print("price =", price)
# price = 20

# ============================================================
# [2] The one-liner version
# ============================================================
# The formula is:
#
#     [value if True]  if  [condition]  else  [value if False]
#
# Read it like a sentence in English: "20 IF country is Egypt,
# ELSE 30".

country = "Egypt"
price = 20 if country == "Egypt" else 30
print("price =", price)
# price = 20

# Watch the order! The CONDITION goes in the MIDDLE, between the
# two values. This is the part everyone mixes up at first.

country = "Sudan"
price = 20 if country == "Egypt" else 30
print("price =", price)
# price = 30

# ============================================================
# [3] The real example: a movie rating by age
# ============================================================
# if the person is 18 or older, print one message, otherwise print
# another one. The long version first, then the short version.

age = 21

# the long version
if age >= 18:
    message = "suitable for you, enjoy the movie"
else:
    message = "not suitable for your age"

# the short version, same result, one line
message_short = "suitable for you, enjoy the movie" if age >= 18 else "not suitable for your age"

print("long  :", message)
print("short :", message_short)
# long  : suitable for you, enjoy the movie
# short : suitable for you, enjoy the movie

# ============================================================
# [4] A rating table built with the ternary
# ============================================================
# We rate the movie for every age and print the right level.

def movie_rating(age):
    """Return the age rating of a movie for this age."""
    if age < 13:
        return "G       - safe for everyone"
    if age < 18:
        return "PG-13   - with a parent"
    return "R       - adults only"


for person_age in (5, 12, 13, 16, 18, 40):
    print(f"  age {person_age:>3} -> {movie_rating(person_age)}")
#   age   5 -> G       - safe for everyone
#   age  12 -> G       - safe for everyone
#   age  13 -> PG-13   - with a parent
#   age  16 -> PG-13   - with a parent
#   age  18 -> R       - adults only
#   age  40 -> R       - adults only

# ============================================================
# [5] The real strength: it is an EXPRESSION
# ============================================================
# A normal if statement is a STATEMENT: it does something.
# A ternary is an EXPRESSION: it PRODUCES a value. So it can go
# anywhere a value is expected, which a normal if cannot.

country = "KSA"
price = 25 if country in ("Egypt", "KSA") else 30

# 1) straight inside an f-string
print(f"the price for {country} is ${price}")
# the price for KSA is $25

# 2) inside a list
countries = ["Egypt", "KSA", "Sudan", "Kuwait", "UAE"]
flags = [c if c in ("Egypt", "KSA") else c.lower() for c in countries]
print("flags:", flags)
# flags: ['Egypt', 'KSA', 'sudan', 'kuwait', 'uae']

# 3) as a return value
def is_local(country):
    return True if country in ("Egypt", "KSA") else False


print("is_local('Egypt') ->", is_local("Egypt"))
# is_local('Egypt') -> True

# ============================================================
# [6] It only evaluates the side it picks
# ============================================================
# This is a very useful detail. A ternary is lazy: the branch that
# is not chosen is never executed at all.

def expensive_task():
    print("  -> the expensive task RAN")
    return 42


def cheap_task():
    print("  -> the cheap task ran")
    return 7


flag = False
result = expensive_task() if flag else cheap_task()
print("result =", result)
#   -> the cheap task ran
# result = 7

# The expensive task printed NOTHING, because it was on the side
# that was not selected. A normal if would skip it too, but the
# ternary makes it very obvious here.

# ============================================================
# [7] The DANGER: nested ternaries
# ============================================================
# You can chain ternaries, and it works, but do not abuse it.

age = 15

# chained, one line, correct but hard to read
level = "child" if age < 13 else ("teen" if age < 18 else "adult")

# the same logic written properly with if/elif/else
if age < 13:
    level_clear = "child"
elif age < 18:
    level_clear = "teen"
else:
    level_clear = "adult"

print("nested  :", level)
print("if/elif :", level_clear)
print("same?   :", level == level_clear)
# nested  : teen
# if/elif : teen
# same?   : True

# Rule of thumb: if you need more than ONE else in a ternary,
# write a real if/elif/else instead.

# ============================================================
# Improvement (from me): the most practical ternary of all
# ============================================================
# For a simple lookup, dict.get() with a ternary default beats both
# a long if/elif chain and a nested ternary.

COUNTRY_PRICES = {"egypt": 20, "ksa": 25, "kuwait": 15, "uae": 22}
DEFAULT_PRICE = 30


def final_price(country_input):
    """Return the price for a country, with a safe default."""
    key = " ".join(str(country_input).strip().split()).lower()
    return COUNTRY_PRICES.get(key, DEFAULT_PRICE)


print("--- final prices ---")
for name in ["Egypt", "  EGYPT  ", "KSA", "kuwait", "United States", ""]:
    print(f"  {final_price(name):>3} <- {name if name.strip() else '(empty)'}")

# The difference between the three styles for the SAME task:
#   if/elif chain : 8 lines, easy to read, one line per country
#   nested ternary: 1 unreadable line
#   dict.get()    : 1 short line, scales to a hundred countries
# This is the pattern you will use most in real projects.

# ============================================================
# SUMMARY
# ============================================================
# - The ternary is: [value_if_true] if [condition] else [value_if_false]
# - The condition sits in the MIDDLE, between the two values.
# - It is the same logic as if/else, written on one line.
# - A ternary is an EXPRESSION, so it can be used inside an
#   f-string, inside a list, or as a return value.
# - Only the chosen side runs; the other one is never evaluated.
# - Never nest more than one else inside a ternary; use if/elif.
# - For a lookup table, prefer dict.get(key, default) over any chain.

# ============================================================
# NEXT LESSON: Advanced string formatting and multi-line output
# ============================================================
