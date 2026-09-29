# -----------------------------------------------------------------
# Lesson 41: Control Flow - the if / elif / else statements
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : conditions, branching, country based pricing
# Type     : Educational + Practical Project
# Builder  : local assistant
# -----------------------------------------------------------------
# Until now our programs ran straight from top to bottom. Today we
# teach the program to DECIDE, so the same code can give a
# different result depending on the input. This is the single
# most important skill in programming.

# ============================================================
# [1] The first if
# ============================================================
# The if statement asks ONE yes/no question. If the answer is
# True, the indented block runs. If not, Python skips it.

course_price = 30
u_country = input("Input Your Country: ")

if u_country == "Egypt":
    print("Hello Egyptian, here is your special price")
    course_price = 20

print(f"The Course Price Is ${course_price}")
# The Course Price Is $20

# Look at the indentation. The four spaces are NOT decoration:
# they tell Python which lines belong to the if.
# Without them, Python raises IndentationError.

# ============================================================
# [2] Adding elif (else if) for the other countries
# ============================================================
# elif means: "IF the first condition failed, TRY this one".
# Python checks the branches from top to bottom and runs ONLY the
# first one that is True, then jumps straight to the end.

course_price = 30
u_country = input("Input Your Country: ")

if u_country == "Egypt":
    print("Hello Egyptian, here is your special price")
    course_price = 20
elif u_country == "KSA":
    print("Hello Saudi, you have a student discount")
    course_price = 25
elif u_country == "Kuwait":
    print("Hello Kuwaiti, you get 50% off")
    course_price = 15
else:
    print("Hello from the rest of the world, standard price")
    course_price = 30

print(f"The Course Price Is ${course_price}")
# The Course Price Is $20

# Why elif and NOT a second if?
# With elif, only ONE branch ever runs. With a second if, the
# program would keep checking and could change the price twice.
# That is exactly what "mutually exclusive" means.

# ============================================================
# [3] The order matters
# ============================================================
# The first True branch wins and stops the chain. So a specific
# condition must ALWAYS come before a general one.
#
#   GOOD:  if score == 100: ... elif score >= 90: ...
#   BAD:   if score >= 90: ... elif score == 100: ...   <- never reached

temperature = 100
if temperature >= 90:
    print("A: very hot")
elif temperature == 100:
    print("B: exactly boiling")   # this can never run
# A: very hot

# ============================================================
# [4] The real problem: a bug in the original idea
# ============================================================
# A real user will NEVER type the country name exactly right.
# They will type "egypt", " Egypt ", or "EGYPT", and == is
# case sensitive, so the comparison fails and the user pays the
# full price. That is a genuine bug, not a style problem.

messy = "  EGYPT  "
print("raw comparison  :", messy == "Egypt")
# raw comparison  : False
print("after cleaning  :", " ".join(messy.strip().split()).lower() == "egypt")
# after cleaning  : True

# ============================================================
# Improvement (from me): a pricing engine that never surprises
# ============================================================
# Instead of a long if/elif chain, we put the prices in a dict
# and let Python find the right one. The if/elif logic is still
# there, just written once and safely.

DEFAULT_PRICE = 30

COUNTRY_PRICES = {
    "egypt": 20,
    "ksa": 25,
    "kuwait": 15,      # 50% off the standard price
    "uae": 22,
    "qatar": 18,
}


def clean_country(country_input):
    """Normalise whatever the user typed into a safe lookup key."""
    return " ".join(str(country_input).strip().split()).lower()


def get_course_price(country_input):
    """Return (price, message) for the given country name."""
    key = clean_country(country_input)

    if key in COUNTRY_PRICES:
        return COUNTRY_PRICES[key], f"special price for '{key}'"
    if not key:
        return DEFAULT_PRICE, "no country entered, so the standard price"
    return DEFAULT_PRICE, f"no special deal for '{key}', standard price"


# We apply it to the user's real answer.
user_country = input("Input Your Country: ")
price, reason = get_course_price(user_country)

print()
print("=" * 46)
print("         COUNTRY PRICING")
print("=" * 46)
print(f"  You typed   : '{user_country}'")
print(f"  Cleaned key : '{clean_country(user_country)}'")
print(f"  Reason      : {reason}")
print(f"  Final price : ${price}")
print("=" * 46)

# Now we test many countries in one go, without more input().
print("--- testing a batch of countries ---")
for country in ["Egypt", "  eGYpt  ", "KSA", "ksa", "Kuwait", "UAE",
                "Qatar", "United States", "", "   ", "Sudan"]:
    p, r = get_course_price(country)
    print(f"  {clean_country(country) or '(empty)':<16} -> ${p:<3} | {r}")

# ============================================================
# [5] Several countries can share one branch
# ============================================================
# Sometimes a group of countries shares the same price, and then
# a tuple with in is cleaner than a long elif chain.

GULF = ("ksa", "kuwait", "qatar", "uae", "bahrain", "oman")

country_key = clean_country("  Kuwait ")
if country_key in GULF:
    print("this country is in the Gulf group")
# this country is in the Gulf group

# ============================================================
# [6] A compact way to build if / elif / else
# ============================================================
# The if/elif/else statement also works as an EXPRESSION, so it
# can return a value instead of running statements. This is handy
# for small choices.

age = 20
ticket = "free" if age < 10 else ("half" if age < 18 else "full")
print("ticket for", age, "->", ticket)
# ticket for 20 -> full

# ============================================================
# SUMMARY
# ============================================================
# - if runs its block only when the condition is True.
# - elif means "else if": it is checked ONLY if the previous
#   conditions were all False, and only the FIRST True branch runs.
# - else is the fallback that always catches everything left.
# - The order of the branches matters: specific first, general last.
# - Indentation is mandatory; it defines the block of each branch.
# - == is case sensitive, so always clean the input with
#   " ".join(raw.strip().split()).lower() before comparing.
# - The ternary form (a if cond else b) is a short if/else that
#   returns a value.

# ============================================================
# NEXT LESSON: Advanced if / elif / else - nested and combined
# ============================================================
