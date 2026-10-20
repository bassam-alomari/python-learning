# -----------------------------------------------------------------
# elzero.py -- the course's first CUSTOM MODULE (lesson 77)
# -----------------------------------------------------------------
# A module is just a .py file. This one holds two functions
# and one variable to share, exactly the transcript's step
# one: put the functions and variables you want to reuse
# into a file of its own.
#
# RULES a good module keeps:
#   * DEFINE things (functions, constants) -- do not PRINT
#     anything at import time; importing elzero should be
#     silent, and it is
#   * stay deterministic: no clocks, no randomness, no
#     machine paths in the values you hand out
# -----------------------------------------------------------------

VERSION = "1.0"


def say_hello(name):
    """Return a greeting for the given name."""
    return f"Hello {name}!"


def sum_two(num1, num2):
    """Return the sum of exactly two numbers."""
    return num1 + num2


def sum_many(*numbers):
    """Return the sum of any number of arguments."""
    total = 0
    for number in numbers:
        total += number
    return total
