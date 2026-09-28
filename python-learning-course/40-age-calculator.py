# -----------------------------------------------------------------
# Lesson 40: Practical Application - Age Calculator
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : input, int, multiplication, f-string, thousands commas
# Type     : Educational + Practical Project
# Builder  : local assistant
# -----------------------------------------------------------------
# A small program that asks for an age and then calculates every
# time unit the person has already lived. It is a perfect review
# of input, int(), the multiplication operators, and formatting.

# ============================================================
# [1] Getting the age from the user
# ============================================================
# input() always returns text, so we wrap it in int() to be able
# to do the arithmetic. This is the step people forget.

age_text = input("Please enter your age in years: ")
age = int(age_text)
print("age =", age)
# age = 22

# ============================================================
# [2] The chain of calculations
# ============================================================
# Every unit is built from the one before it, step by step.

months = age * 12              # 12 months in a year
weeks = months * 4             # about 4 weeks in a month
days = age * 365               # 365 days in a year
hours = days * 24              # 24 hours in a day
minutes = hours * 60           # 60 minutes in an hour
seconds = minutes * 60         # 60 seconds in a minute

print("months  :", months)
print("weeks   :", weeks)
print("days    :", days)
print("hours   :", hours)
print("minutes :", minutes)
print("seconds :", seconds)
# months  : 264
# weeks   : 1056
# days    : 8030
# hours   : 192720
# minutes : 11563200
# seconds : 693792000

# ============================================================
# [3] Formatting with f-strings and the thousands separator
# ============================================================
# Big numbers are hard to read without separators. Putting a comma
# inside the braces, {value:,}, makes Python add them for us.
# The value stays a real number; only the PRINTING changes.

print(f"{seconds:,} seconds")
# 693,792,000 seconds

print(f"you have lived {days:,} days and {hours:,} hours")
# you have lived 8,030 days and 192,720 hours

# The alignment symbols inside the braces control the columns:
#   :<15  -> pad on the RIGHT (text style, left aligned)
#   :>15  -> pad on the LEFT  (numbers look tidy on the right)
print(f"{'Unit':<10}{'Total':>15}")
# Unit                Total

# ============================================================
# [4] The final report
# ============================================================
# This is the presentation version of the same calculations.

age = 22                                     # a fixed value for the report
months = age * 12
weeks = months * 4
days = age * 365
hours = days * 24
minutes = hours * 60
seconds = minutes * 60

print("=" * 44)
print("        HOW MUCH TIME HAS PASSED?")
print("=" * 44)
print(f"  Age       : {age} years")
print(f"  Months    : {months:,}")
print(f"  Weeks     : {weeks:,}")
print(f"  Days      : {days:,}")
print(f"  Hours     : {hours:,}")
print(f"  Minutes   : {minutes:,}")
print(f"  Seconds   : {seconds:,}")
print("=" * 44)

# ============================================================
# [5] Why the thousands comma matters so much
# ============================================================
# The comma changes NOTHING about the number itself. It is only a
# display trick, so we can safely use it everywhere.

raw = seconds
with_commas = f"{raw:,}"

print("without the comma:", raw)
print("with    the comma:", with_commas)
print("same object?      :", str(raw) == str(raw).replace(",", ""))
# without the comma: 693792000
# with    the comma: 693,792,000
# same object?      : True

# We can also ask Python for a readable size: K, M, and B.
print("short version     :", f"{seconds / 1_000_000:.2f} million seconds")
# short version     : 693.79 million seconds

# ============================================================
# Improvement (from me): a precise version plus a fact sheet
# ============================================================
# The lesson used months * 4 for the weeks, which is an
# approximation. We can do much better, and we can add some fun.

def age_facts(age_in_years):
    """Return every time unit, calculated as precisely as we can."""
    if age_in_years < 0:
        raise ValueError("the age cannot be negative")

    days_total = age_in_years * 365
    # A leap year adds one day. There is roughly one every 4 years.
    leap_days = age_in_years // 4
    days_total += leap_days

    hours_total = days_total * 24
    minutes_total = hours_total * 60
    seconds_total = minutes_total * 60

    return {
        "age": age_in_years,
        "months": age_in_years * 12,
        "weeks_rough": age_in_years * 12 * 4,
        "weeks_exact": days_total // 7,
        "days": days_total,
        "hours": hours_total,
        "minutes": minutes_total,
        "seconds": seconds_total,
        "heartbeats": minutes_total * 72,      # 72 beats per minute
        "sleep_nights": days_total // 3,        # roughly a third of life
    }


def plural(count, singular, plural_form):
    """Return the singular word when the count is exactly 1."""
    return singular if count == 1 else plural_form


def show_report(facts):
    """Print the whole time sheet as a clean two column table."""
    years_word = plural(facts["age"], "year", "years")
    rows = [
        ("Age", f"{facts['age']} {years_word}"),
        ("Months", f"{facts['months']:,}"),
        ("Weeks (rough)", f"{facts['weeks_rough']:,}"),
        ("Weeks (exact)", f"{facts['weeks_exact']:,}"),
        ("Days", f"{facts['days']:,}"),
        ("Hours", f"{facts['hours']:,}"),
        ("Minutes", f"{facts['minutes']:,}"),
        ("Seconds", f"{facts['seconds']:,}"),
    ]
    lines = ["=" * 40, "        TIME SHEET", "=" * 40]
    lines += [f"  {label:<16}{value:>18}" for label, value in rows]
    lines += ["-" * 40, "  FUN FACTS", "-" * 40]
    lines += [
        f"  {'Heartbeats':<16}{facts['heartbeats']:,}",
        f"  {'Nights slept':<16}{facts['sleep_nights']:,}",
    ]
    lines += ["=" * 40]
    return "\n".join(lines)


# We run it for several ages and we also check the error case.
for sample_age in (1, 10, 22, 65):
    print(show_report(age_facts(sample_age)))
    print()

try:
    age_facts(-5)
except ValueError as err:
    print("age_facts(-5) ->", err)
# age_facts(-5) -> the age cannot be negative

# ============================================================
# SUMMARY
# ============================================================
# - input() returns text, so use int(input(...)) for calculations.
# - Each time unit is built from the one before it: months, weeks,
#   days, hours, minutes, then seconds.
# - f-strings let us insert values directly: f"{value}".
# - The comma inside the braces, {value:,}, adds thousands
#   separators for a readable output without changing the number.
# - Align the columns with :<15 and :>15 inside the f-string.
# - For real precision use days // 7 for the weeks and add the
#   leap days instead of multiplying by 365 only.

# ============================================================
# NEXT LESSON: Control Flow - the if / elif / else statements
# ============================================================
