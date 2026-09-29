# -----------------------------------------------------------------
# Lesson 45: Membership Operators - in and not in
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : in, not in, membership in lists/tuples/sets/strings/dicts
# Type     : Educational + Practical Project
# Builder  : local assistant
# -----------------------------------------------------------------
# The membership operators answer ONE question: is this value a
# member of this collection, yes or no? They are the shortest and
# the clearest way to test many values at once.

# ============================================================
# [1] What does membership mean?
# ============================================================
# Is the item a member of the group, or not? That is all.
# The result is ALWAYS a boolean: True or False.

names = ["Ahmed", "Sayed", "Mahmoud"]

print("Ahmed in names   :", "Ahmed" in names)
print("Mahmoud in names :", "Mahmoud" in names)
print("Ali in names     :", "Ali" in names)
# Ahmed in names   : True
# Mahmoud in names : True
# Ali in names     : False

# Notice what the operator did NOT do: it did not print anything
# about where the item is, and it did not modify the list. It only
# answered yes or no.

# ============================================================
# [2] in works on strings too
# ============================================================
# A string is a collection of characters, so we can ask if a piece
# of text is inside it.

sentence = "Ahmed Sayed Mahmoud"
print('"Sayed" in sentence :', "Sayed" in sentence)
print('"ali" in sentence   :', "ali" in sentence)
# "Sayed" in sentence : True
# "ali" in sentence   : False

# This is substring searching, and it is case sensitive.

# ============================================================
# [3] The real application: country discounts
# ============================================================
# In lesson 42 we solved this with a long or chain:
#   if country == "Egypt" or country == "KSA" or country == "...":
# With in it becomes one short and readable line, and adding a
# new country means adding ONE name to a list.

PRICE_80 = ["Egypt", "KSA"]
PRICE_50 = ["Kuwait", "Bahrain", "Qatar", "UAE"]
DEFAULT_PRICE = 30

u_country = input("Input Your Country: ")

if u_country in PRICE_80:
    course_price = 80
    print("you are in the 80 dollars group")
elif u_country in PRICE_50:
    course_price = 50
    print("you are in the 50 dollars group")
else:
    course_price = DEFAULT_PRICE
    print("you get the standard price")

print(f"The Course Price Is ${course_price}")
# you are in the 80 dollars group
# The Course Price Is $80

# ============================================================
# [4] not in is the exact opposite
# ============================================================
# in      -> True when the value IS a member
# not in  -> True when the value is NOT a member

banned = ["Banned", "Fraud", "Spam"]

account = "Banned"
print('"Banned" in banned    :', "Banned" in banned)
print('"Banned" not in banned:', "Banned" not in banned)
# "Banned" in banned    : True
# "Banned" not in banned: False

account = "Normal"
print('"Normal" in banned    :', "Normal" in banned)
print('"Normal" not in banned:', "Normal" not in banned)
# "Normal" in banned    : False
# "Normal" not in banned: True

# The classic use of not in is a GUARD: let the good cases flow
# first, and deal with the bad ones at the end.
if account not in banned:
    print("welcome, your account is fine")
# welcome, your account is fine

# ============================================================
# Improvement (from me): four real traps
# ============================================================
# These are the mistakes that make in give a WRONG answer. Each
# one is tested below with its real output.

# ---------- TRAP 1: a string is NOT a list of countries ----------
# If you forget the brackets, Python treats the container as one
# long string and then matches SUBSTRINGS. "ypt" is not a country,
# but it is a piece of "Egypt", so it passes the test.
print("--- trap 1: string instead of list ---")
print('"ypt" in "Egypt KSA"     :', "ypt" in "Egypt KSA")
print('"ypt" in ["Egypt", "KSA"]:', "ypt" in ["Egypt", "KSA"])
# "ypt" in "Egypt KSA"     : True
# "ypt" in ["Egypt", "KSA"]: False

# Always use brackets, even for a single country.

# ---------- TRAP 2: the empty string is inside every string ----------
print("--- trap 2: the empty string ---")
print('"" in "cat"   :', "" in "cat")
print('"" in ["cat"] :', "" in ["cat"])
# "" in "cat"   : True
# "" in ["cat"] : False

# So a user who presses Enter without typing anything can pass a
# check that says: if "" in the_allowed_text. Clean the input first.

# ---------- TRAP 3: in a dict checks the KEYS, not the values ----
print("--- trap 3: dict keys vs values ---")
prices = {"egypt": 20, "ksa": 25}
print('"egypt" in prices       :', "egypt" in prices)
print('20 in prices            :', 20 in prices)
print('20 in prices.values()   :', 20 in prices.values())
# "egypt" in prices       : True
# 20 in prices            : False
# 20 in prices.values()   : True

# ---------- TRAP 4: case sensitivity ----------
print("--- trap 4: case sensitivity ---")
print('"EGYPT" in ["Egypt", "KSA"]      :', "EGYPT" in ["Egypt", "KSA"])
print('"egypt" in ["egypt", "ksa"]      :', "egypt" in ["egypt", "ksa"])
# "EGYPT" in ["Egypt", "KSA"]      : False
# "egypt" in ["egypt", "ksa"]      : True

# The fix: normalise the input AND the collection with the same
# .strip().lower() rule, so both sides speak the same language.

# ============================================================
# in works on EVERY container type
# ============================================================
print("--- membership in every container ---")
print("in list  :", 3 in [1, 2, 3])            # True
print("in tuple :", 3 in (1, 2, 3))            # True
print("in set   :", 3 in {1, 2, 3})            # True
print("in string:", "b" in "abc")               # True
print("in dict  :", "a" in {"a": 1, "b": 2})   # True  (key)
print("in range :", 5 in range(1, 10))         # True
print("not in   :", 9 not in [1, 2, 3])        # True
# in list  : True
# in tuple : True
# in set   : True
# in string: True
# in dict  : True  (key)
# in range : True
# not in   : True

# ============================================================
# A set is much faster than a list for membership
# ============================================================
# A list walks the items one by one until it finds a match, so a
# lookup can cost O(n). A set uses a hash table, so it costs about
# the same no matter how big it grows: O(1). For a short list the
# difference is invisible, for a huge one it is enormous.

import time

big_list = [f"country_{i}" for i in range(200000)]
big_set = set(big_list)
target = "country_199999"

start = time.time()
for _ in range(5):
    target in big_list
list_time = time.time() - start

start = time.time()
for _ in range(5):
    target in big_set
set_time = time.time() - start

print("--- 200000 items, 5 lookups ---")
# The exact numbers change on every run and on every machine, so
# do not memorise them. What matters is the SIZE of the gap.
print(f"list : {list_time * 1000:.2f} ms")
print(f"set  : {set_time * 1000:.2f} ms")
print(f"the set was {list_time / set_time:.0f} times faster")
# list : about 12 ms
# set  : about 0.01 ms
# the set was thousands of times faster

# So: keep the display list for reading, and build a set from it
# when the list is used for lookups on every request.

# ============================================================
# A safe, production ready version of the country app
# ============================================================
# Everything we learned above, applied to the same program.

PRICE_TIERS = [
    (80, ["Egypt", "KSA"]),
    (50, ["Kuwait", "Bahrain", "Qatar", "UAE"]),
]

# One clean lookup set, built from the tiers above, so the display
# names and the search keys never drift apart.
LOOKUP = {}
for tier_price, tier_countries in PRICE_TIERS:
    for tier_country in tier_countries:
        LOOKUP[tier_country.lower()] = tier_price


def get_price(country_input):
    """Return (price, message) with a safe default."""
    key = " ".join(str(country_input).strip().split()).lower()
    if not key:
        return DEFAULT_PRICE, "you typed nothing, so the standard price"
    if key in LOOKUP:
        return LOOKUP[key], f"'{key}' found in the tiers"
    return DEFAULT_PRICE, f"'{key}' is not in any tier"


print("--- the safe version ---")
for name in ["Egypt", "  kSA  ", "Kuwait", "Qatar", "Germany", "", "   "]:
    price, message = get_price(name)
    shown = " ".join(str(name).split()) or "(empty)"
    print(f"  {shown:<10} -> ${price:<3} | {message}")

# ============================================================
# SUMMARY
# ============================================================
# - in asks if a value is a member of a collection and returns
#   True or False; not in is its exact opposite.
# - in works on lists, tuples, sets, strings, dictionaries (keys)
#   and range.
# - Use in to replace long or chains: country in ["Egypt", "KSA"].
# - Use not in as a guard for the invalid cases, so the happy path
#   stays at the top of the function.
# - Beware: a string matches SUBSTRINGS, "" is inside every string,
#   a dict matches KEYS not values, and everything is case sensitive.
# - Normalise both sides with " ".join(x.strip().split()).lower().
# - For repeated lookups in a large collection, use a set: it is
#   O(1) instead of O(n).

# ============================================================
# NEXT LESSON: Advanced string formatting and multi-line output
# ============================================================
