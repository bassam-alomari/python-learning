# -----------------------------------------------------------------
# Lesson 44: Advanced Age Calculator V2 - choose your own unit
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : input, string cleaning, if/elif/else, user choice
# Type     : Educational + Practical Project
# Builder  : local assistant
# -----------------------------------------------------------------
# This is version two of the age calculator from lesson 40. The
# difference is that the USER picks which time unit he wants, and
# we accept both the full word and the short letter.

# ============================================================
# [1] The available units
# ============================================================
# Each unit is simply how many of it fit in ONE year, so the
# total is always age * the_factor.
#
#   months   : 12          hours   : 365 * 24
#   weeks    : 52          minutes : 365 * 24 * 60
#   days     : 365         seconds : 365 * 24 * 60 * 60

DAYS_PER_YEAR = 365
HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60

UNITS = {
    "months": 12,
    "weeks": 52,
    "days": DAYS_PER_YEAR,
    "hours": DAYS_PER_YEAR * HOURS_PER_DAY,
    "minutes": DAYS_PER_YEAR * HOURS_PER_DAY * MINUTES_PER_HOUR,
    "seconds": DAYS_PER_YEAR * HOURS_PER_DAY * MINUTES_PER_HOUR * SECONDS_PER_MINUTE,
}

print("--- the available units ---")
for name, factor in UNITS.items():
    print(f"  {name:<9} = {factor:>12,} per year")
#   months   =           12 per year
#   weeks    =           52 per year
#   days     =          365 per year
#   hours    =        8,760 per year
#   minutes  =      525,600 per year
#   seconds  =   31,536,000 per year

# ============================================================
# [2] Getting the name and the age
# ============================================================
# The name is text, so we clean it. The age is a number, so we
# convert it with int(). This is the exact same cleanup we used
# in the user input lesson.
#
# plural() is a tiny helper, the same idea we used in lesson 40:
# it returns the singular word when the count is exactly 1, so
# we never print "1 years". We need it here, so it comes first.
def plural(count, singular, plural_form):
    """Return the singular word when the count is exactly 1."""
    return singular if count == 1 else plural_form


raw_name = input("What is your name? ")
user_name = " ".join(raw_name.strip().split()).title()

raw_age = input("How old are you? ")
age = int(raw_age)

years_word = plural(age, "year", "years")
print(f"Hello {user_name}, you are {age} {years_word} old")
# Hello Sara, you are 1 year old
# Hello Mohamed Ahmed, you are 22 years old

# ============================================================
# [3] A REAL problem with the short letters
# ============================================================
# The idea is to accept the first letter as a shortcut:
#   m -> months    w -> weeks    d -> days
#   h -> hours     m -> minutes  s -> seconds
#
# Look at the m. It is used TWICE, for months AND for minutes.
# A user who types m has no way to know which one we picked, and
# so do we. This is a genuine design bug, and it is exactly the
# kind of thing you only notice by thinking carefully.

FIRST_LETTERS = {
    "w": "weeks",
    "d": "days",
    "h": "hours",
    "s": "seconds",
}

AMBIGUOUS_LETTERS = {
    "m": "months or minutes",
}

print("m means:", AMBIGUOUS_LETTERS["m"])
# m means: months or minutes

# ============================================================
# [4] Resolving whatever the user typed
# ============================================================
# We accept: the full word, a unique short letter, and we give a
# clear message for the ambiguous one and for anything invalid.

def resolve_unit(user_text):
    """Return (unit_key, error_message). unit_key is None on error."""
    key = " ".join(str(user_text).strip().split()).lower()

    if not key:
        return None, "you entered nothing"
    if key in UNITS:
        return key, ""
    if key in FIRST_LETTERS:
        return FIRST_LETTERS[key], ""
    if key in AMBIGUOUS_LETTERS:
        return None, f"'{key}' is not clear, did you mean {AMBIGUOUS_LETTERS[key]}?"
    return None, f"'{key}' is not one of the units we know"

# Let us test the resolver with the tricky cases first.
print("--- checking the resolver ---")
for test in ["months", "  MONTHS  ", "w", "d", "h", "s", "m", "years", ""]:
    unit, err = resolve_unit(test)
    print(f"  '{test}' -> {unit if unit else 'ERROR: ' + err}")
#   'months' -> months
#   '  MONTHS  ' -> months
#   'w' -> weeks
#   'd' -> days
#   'h' -> hours
#   's' -> seconds
#   'm' -> ERROR: 'm' is not clear, did you mean months or minutes?
#   'years' -> ERROR: 'years' is not one of the units we know
#   '' -> ERROR: you entered nothing

# ============================================================
# [5] Asking the user, and asking again if needed
# ============================================================
# One if/else that prints an error and gives up is not friendly.
# Real programs re-ask the user until the answer is usable.

MAX_TRIES = 3
chosen_unit = None
attempts = 0

while chosen_unit is None and attempts < MAX_TRIES:
    raw_choice = input("Which unit do you want? (months/weeks/days/hours/minutes/seconds): ")
    chosen_unit, problem = resolve_unit(raw_choice)
    attempts += 1

    if chosen_unit is None:
        print(f"  sorry: {problem}")
        print("  valid units: " + ", ".join(UNITS.keys()))

if chosen_unit is None:
    print("too many wrong tries, I will show you the full table instead")
    chosen_unit = None

# ============================================================
# [6] The if/elif/else version, exactly as the lesson taught it
# ============================================================
# We keep the if/elif/else style on purpose, so the logic is
# visible, but the branches are chosen by the unit KEY now.

if chosen_unit == "months":
    result = age * UNITS["months"]
    label = "months"
elif chosen_unit == "weeks":
    result = age * UNITS["weeks"]
    label = "weeks"
elif chosen_unit == "days":
    result = age * UNITS["days"]
    label = "days"
elif chosen_unit == "hours":
    result = age * UNITS["hours"]
    label = "hours"
elif chosen_unit == "minutes":
    result = age * UNITS["minutes"]
    label = "minutes"
elif chosen_unit == "seconds":
    result = age * UNITS["seconds"]
    label = "seconds"
else:
    result = 0
    label = "unknown"

# ============================================================
# [7] The final report
# ============================================================
# If the user gave up, we print the whole table so they still get
# an answer instead of an empty screen.

if chosen_unit is None:
    print()
    print("=" * 42)
    print(f"  {user_name}, here is everything for {age} {years_word}")
    print("=" * 42)
    for name, factor in UNITS.items():
        total = age * factor
        word = plural(total, name[:-1], name)
        print(f"  {name:<9}{total:>16,} {word}")
    print("=" * 42)
else:
    # label[:-1] turns "minutes" into "minute" and "days" into "day"
    unit_word = plural(result, label[:-1], label)
    print()
    print("=" * 42)
    print(f"  HELLO, {user_name}!")
    print(f"  You have lived {result:,} {unit_word}")
    print("=" * 42)
    # We also show the neighbouring units for a bit of context.
    print("  for reference, the same age in other units:")
    for name, factor in UNITS.items():
        mark = ">>" if name == chosen_unit else "  "
        print(f"  {mark} {name:<9}{age * factor:>16,}")
    print("=" * 42)

# ============================================================
# Improvement (from me): the whole if/elif chain is not needed
# ============================================================
# Six branches that do exactly ONE thing are a sign that a dict is
# a better tool. One line replaces all of them, and adding a new
# unit becomes a single new entry in UNITS instead of a new branch.

def total_for(age_in_years, unit_key):
    """Return the total, or None if the unit is unknown."""
    factor = UNITS.get(unit_key)
    return None if factor is None else age_in_years * factor


print("--- the dict version gives the same answers ---")
for key in UNITS:
    old_way = {"months": age * 12, "weeks": age * 52, "days": age * 365,
               "hours": age * 8760, "minutes": age * 525600,
               "seconds": age * 31536000}[key]
    new_way = total_for(age, key)
    print(f"  {key:<9} if/elif={old_way:>12,}   dict={new_way:>12,}   same={old_way == new_way}")
print("  unknown unit ->", total_for(age, "years"))
# unknown unit -> None

# ============================================================
# SUMMARY
# ============================================================
# - Every time unit is age * a_factor, and the factor is fixed
#   (12, 52, 365, 8760, 525600, 31536000).
# - Clean the name with " ".join(raw.strip().split()).title() and
#   convert the age with int().
# - Use if/elif/else to react to the unit the user chose.
# - The else branch must explain what the valid choices are, not
#   just say "wrong".
# - The first letter is NOT always unique: m means both months and
#   minutes, so detect the ambiguous letters and ask again.
# - Ask again in a loop instead of giving up after one mistake.
# - When many branches do the same single thing, replace the chain
#   with a dict and get(key).

# ============================================================
# NEXT LESSON: Advanced string formatting and multi-line output
# ============================================================
