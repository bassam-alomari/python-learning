# -----------------------------------------------------------------
# Lesson 35: Assignment Operators
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : = += -= *= /= %= **= //=
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# The assignment operator stores a value inside a variable.
# Once you know the first one, the rest are all the same story.

# ============================================================
# [1] The basic assignment operator  =
# ============================================================
# = means: take the value on the right, store it in the name on
# the left. It does NOT mean "equal to" the way maths uses it.

x = 10
y = 20

print("x =", x)
print("y =", y)
# x = 10
# y = 20

# Here we store a NEW variable z that holds the sum of x and y.
z = x + y
print("z = x + y :", z)
# z = x + y : 30

# IMPORTANT: z is a new variable. x and y did not change at all.
print("x is still:", x, "| y is still:", y)
# x is still: 10 | y is still: 20

# ============================================================
# [2] Updating the SAME variable
# ============================================================
# Now we want x itself to become the sum. We write the name on
# both sides of the =.

x = 10
y = 20
x = x + y            # the long way
print("x = x + y :", x)
# x = x + y : 30

# Python reads the right side first (using the old value of x),
# then assigns the result to x. This is why it works.

# ============================================================
# [3] The compound assignment  +=
# ============================================================
# The long way is wordy, so Python gives us a shortcut that means
# exactly the same thing: "x equals its current value plus y".

x = 10
y = 20
x += y               # the short way
print("x += y :", x)
# x += y : 30

# x += y  is exactly the same as  x = x + y
# This is called a COMPOUND ASSIGNMENT OPERATOR.

# The most common use in the whole language: the counter.
score = 0
score += 10
score += 5
print("score:", score)
# score: 15

# ============================================================
# [4] The same idea for every arithmetic operation
# ============================================================
# -= subtracts, *= multiplies, and so on. Each one is the long
# form written in a single token.

# Subtraction: num -= value  means  num = num - value
num = 10
num -= 4
print("num -= 4  :", num)
# num -= 4  : 6

# Multiplication: num *= value  means  num = num * value
num = 10
num *= 4
print("num *= 4  :", num)
# num *= 4  : 40

# Division: num /= value  means  num = num / value
num = 10
num /= 4
print("num /= 4  :", num)
# num /= 4  : 2.5

# Floor division: num //= value  means  num = num // value
num = 10
num //= 4
print("num //= 4 :", num)
# num //= 4 : 2

# Modulo (remainder): num %= value  means  num = num % value
num = 10
num %= 4
print("num %= 4  :", num)
# num %= 4  : 2

# Power: num **= value  means  num = num ** value
num = 2
num **= 5
print("num **= 5 :", num)
# num **= 5 : 32

# ============================================================
# [5] A complete comparison table
# ============================================================
# The long form and the short form, side by side.

print("Long form            Short form   Result")
pairs = [
    ("n = n + 3",          "n += 3",    10),
    ("n = n - 3",          "n -= 3",    4),
    ("n = n * 3",          "n *= 3",    21),
    ("n = n / 3",          "n /= 3",    2.3333333333333335),
    ("n = n // 3",         "n //= 3",   2),
    ("n = n % 3",          "n %= 3",    1),
    ("n = n ** 3",         "n **= 3",   343),
]
for long_form, short_form, expected in pairs:
    n = 7
    exec(long_form)
    got = n
    n = 7
    exec(short_form)
    same = "same" if got == n == expected else "CHECK"
    print(f"n = 7 ->  {long_form:<14} = {got!r:<20} | {short_form:<10} = {n!r:<20} {same}")

# ============================================================
# [6] Two gotchas worth knowing
# ============================================================
# Gotcha 1: / and /= always produce a FLOAT, even on a clean number.

total = 10
total /= 4
print("10 /= 4 :", total)
# 10 /= 4 : 2.5

# If you want a whole number, use //= instead.
whole = 10
whole //= 4
print("10 //= 4:", whole)
# 10 //= 4: 2

# Gotcha 2: you must define a variable BEFORE you use += on it.
# counter += 1 without counter = 0 first gives a NameError.

counter = 0
counter += 1
counter += 1
print("counter after two increments:", counter)
# counter after two increments: 2

# ============================================================
# [7] Chain assignment
# ============================================================
# One value can be assigned to several names in a single line.
# The right side is evaluated once, then the names are bound to it.

a = b = c = 0
print("a, b, c :", a, b, c)
# a, b, c : 0 0 0

# They are three separate names. Changing one does not change the
# others, because the object here is an immutable int.
a = 10
print("after a = 10 -> b is still:", b)
# after a = 10 -> b is still: 0

# ============================================================
# Improvement (from me): a real shopping cart with += and -=
# ============================================================
# A practical example that uses the operators the way a real
# application does: accumulate a total, then adjust it.

def cart_total(items):
    """Return the total price of a list of (name, price, quantity)."""
    total = 0
    names = []
    for name, price, quantity in items:
        total += price * quantity        # accumulating with +=
        names.append(f"{name} x{quantity}")
    return names, total


def apply_discount(total, percent):
    """Return the total after a percent discount, without floats."""
    total *= 100 - percent              # *= then //= to stay exact
    total //= 100
    return total


shopping = [("Notebook", 12, 2), ("Pen", 3, 4), ("Bag", 40, 1)]

names, total = cart_total(shopping)
print("items  :", names)
# items  : ['Notebook x2', 'Pen x4', 'Bag x1']
print("total  :", total)
# total  : 76

print("after 10% off:", apply_discount(total, 10))
# after 10% off: 68

# The reverse operation: return one item and take it off the total.
refund_price, refund_qty = 12, 2
total -= refund_price * refund_qty
print("total after the refund:", total)
# total after the refund: 52

# ============================================================
# SUMMARY
# ============================================================
# - = stores a value in a variable; it is not a comparison.
# - z = x + y creates a NEW variable and leaves x alone.
# - x = x + y updates x itself with its own old value.
# - += is the short form of x = x + y, and it is the same for all
#   the other arithmetic operators:
#       -=   -= sub      /=  divide      **=  power
#       *=   *= mul      %=  remainder  //=  floor divide
# - / and /= always give a float; use //= for a whole number.
# - Always create the variable before the first += on it.
# - a = b = c = 0 assigns one value to several names.

# ============================================================
# NEXT LESSON: Control Flow - the if / elif / else statements
# ============================================================
