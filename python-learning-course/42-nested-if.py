# -----------------------------------------------------------------
# Lesson 42: Nested if - conditions inside conditions
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : nested if, or, and, not, grouping countries
# Type     : Educational + Practical Project
# Builder  : local assistant
# -----------------------------------------------------------------
# Today we put an if INSIDE another if. The inner condition is only
# checked when the outer one is True, and that is exactly how real
# programs make two decisions in a row.

# ============================================================
# [1] The simplest nested if
# ============================================================
# The inner if is indented one level deeper, so it belongs to the
# outer if. Python checks the inner one ONLY if the outer is True.

age = 22
country = "Egypt"

if country == "Egypt":
    print("welcome, you are in the first group")
    if age >= 18:
        print("and you are an adult")
    else:
        print("but you are still a minor")
# welcome, you are in the first group
# and you are an adult

# Change the country and the inner block never runs at all.
country = "Sudan"
if country == "Egypt":
    print("welcome, you are in the first group")
    if age >= 18:
        print("and you are an adult")
# (nothing is printed here)

# ============================================================
# [2] The problem we want to solve
# ============================================================
# Egypt and KSA get the SAME price. The lazy way is to duplicate
# the whole block, once per country.

BASE_PRICE = 100
GROUP_PRICE = 80

country = "KSA"
price = BASE_PRICE

if country == "Egypt":
    print("special price for the first group")
    price = GROUP_PRICE
if country == "KSA":
    print("special price for the second group")
    price = GROUP_PRICE
# special price for the second group

# It works, but it repeats the body. Add two more countries and you
# will have copied the block four times. That is bad maintenance.

# ============================================================
# [3] The fix: merge the conditions with or
# ============================================================
# or means: True if AT LEAST ONE side is True.

country = "Egypt"
price = BASE_PRICE

if country == "Egypt" or country == "KSA":
    print("special price for the first group")
    price = GROUP_PRICE
# special price for the first group

# The same works with more countries. The condition gets long, but
# the body is written only once.

country = "Kuwait"
price = BASE_PRICE

if country == "Egypt" or country == "KSA" or country == "Kuwait" or country == "Bahrain":
    print("special price for the first group")
    price = 65
# special price for the first group

# ============================================================
# [4] Even cleaner: the in operator
# ============================================================
# When a condition lists many values, "in" is shorter and safer.
# You cannot forget a comma, and it is easier to maintain.

FIRST_GROUP = ["Egypt", "KSA", "Kuwait", "Bahrain"]
SECOND_GROUP = ["UAE", "Qatar", "Oman"]

country = "Bahrain"
price = BASE_PRICE

if country in FIRST_GROUP:
    price = GROUP_PRICE
elif country in SECOND_GROUP:
    price = 70
else:
    price = BASE_PRICE
print("Bahrain ->", price)
# Bahrain -> 80

# ============================================================
# [5] The real exercise: country AND student
# ============================================================
# Egypt and KSA share one price. On top of that, a student gets an
# extra discount. That is two decisions, so the second one is nested
# inside the first.

country = "Egypt"
is_student = "yes"

if country == "Egypt" or country == "KSA":
    print("Hello from the first group")
    course_price = 80

    if is_student == "yes":
        print("and you are a student, extra discount applied")
        course_price -= 10
else:
    print("Hello from the rest of the world")
    course_price = BASE_PRICE

print(f"The Course Price Is ${course_price}")
# Hello from the first group
# and you are a student, extra discount applied
# The Course Price Is $70

# The outer if is the GATE. No matter what, the student discount
# can only be reached if the country passed the outer test.

# ============================================================
# [6] The same program with real user input
# ============================================================
u_country = input("Input Your Country: ")
u_student = input("Are you a student? (yes/no): ")

if u_country == "Egypt" or u_country == "KSA":
    print("Hello from the first group")
    course_price = 80
    if u_student == "yes":
        print("and you are a student, extra discount applied")
        course_price -= 10
else:
    print("Hello from the rest of the world")
    course_price = BASE_PRICE

print(f"The Course Price Is ${course_price}")

# ============================================================
# Improvement (from me): nesting is fine, deep nesting is not
# ============================================================
# Three levels of indentation start to hurt the eye. Whenever we
# can, we flatten the logic instead of digging deeper.

# BAD: four levels deep, hard to follow and hard to edit.
def bad_price(country, student, coupon):
    if country in FIRST_GROUP:
        if student:
            if coupon:
                return 60
            else:
                return 70
        else:
            return 80
    else:
        return 100


# BETTER: combine the checks with and, so the depth stays at one.
def good_price(country, student, coupon):
    if country in FIRST_GROUP and student and coupon:
        return 60
    if country in FIRST_GROUP and student:
        return 70
    if country in FIRST_GROUP:
        return 80
    return 100


# EVEN BETTER: walk the rules in order and stop at the first match.
PRICE_RULES = [
    (("group", "student", "coupon"), 60),
    (("group", "student"), 70),
    (("group",), 80),
]


def apply_rules(has_group, is_student_flag, has_coupon):
    state = {
        "group": has_group,
        "student": is_student_flag,
        "coupon": has_coupon,
    }
    for needed, price in PRICE_RULES:
        if all(state[flag] for flag in needed):
            return price
    return BASE_PRICE


# We check the three versions agree with each other.
print("--- comparing the three designs ---")
for country, student, coupon in [("Egypt", True, True), ("Egypt", True, False),
                                 ("Egypt", False, True), ("Kuwait", False, False),
                                 ("Sudan", True, True)]:
    b = bad_price(country, student, coupon)
    g = good_price(country, student, coupon)
    r = apply_rules(country in FIRST_GROUP, student, coupon)
    print(f"  {country:<6} student={str(student):<5} coupon={str(coupon):<5}"
          f" -> bad={b} good={g} rules={r} same={b == g == r}")

# ============================================================
# [7] Other useful boolean tools
# ============================================================
# and  -> both sides must be True
# or   -> at least one side must be True
# not  -> flips True into False and the other way around
# in   -> is the value inside a list or a tuple or a string?

value = 15
print("and  :", value > 10 and value < 20)
# and  : True
print("or   :", value > 100 or value < 20)
# or   : True
print("not  :", not (value > 100))
# not  : True
print("in   :", "KSA" in FIRST_GROUP)
# in   : True
print("in str:", "at" in "cat")
# in str: True

# ============================================================
# SUMMARY
# ============================================================
# - A nested if is simply an if written inside the block of
#   another if, with one extra level of indentation.
# - The inner if runs ONLY if the outer condition was True.
# - To give several countries the same price, merge them with or
#   instead of copying the same block again and again.
# - When a condition lists many values, "x in [a, b, c]" is much
#   easier to read and to maintain than a long chain of or.
# - Use and when both conditions must be true, not to negate one.
# - Avoid more than two or three levels of nesting; flatten with and
#   or with a list of rules, otherwise the program becomes unreadable.

# ============================================================
# NEXT LESSON: Advanced string formatting and multi-line output
# ============================================================
