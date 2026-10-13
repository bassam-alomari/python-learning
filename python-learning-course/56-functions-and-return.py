# -----------------------------------------------------------------
# Lesson 56: functions - def, calling, and return
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : def, parameters, calling, print vs return, returning data
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript calls functions "one of the most important topics
# in programming", and it is right. Everything from here on -- the
# projects, the tests, the libraries -- is built out of functions.
#
# The two ideas in this file:
#
#   def       write the block ONCE, call it ANYWHERE
#   return    hand a VALUE back to the caller, instead of printing
#
# print and return look similar on screen and could not be more
# different. Most of this lesson is about that difference, because
# confusing them is the number-one beginner bug in functions.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] What a function is: a block you write once, call forever
# ============================================================
# The transcript's definition, made concrete. Here is a block of
# code with a name. Nothing runs yet -- naming is not calling.

def greet():
    print("Hello from the function")

# Nothing printed. The file only READ the def. Now we call it --
# twice, because that is the whole point:

greet()
# Hello from the function

greet()
# Hello from the function

# One definition, two calls, two runs of the same body. If the
# message ever changes, you change it in ONE place. That is the
# first reason functions exist: no repetition of a block you have
# already written.

# ============================================================
# [2] The parts: def, name, parentheses, body
# ============================================================
# Four pieces, and the order never changes:
#
#   def   name   ( parameters ):
#       body
#
# def         the keyword that defines -- nothing before it runs
# name        what YOU choose to call the function later
# ( ... )     the parameter list, empty here, may hold names
# body        indented lines, the same indentation rule as loops

# The call is the name plus parentheses, even when there are no
# parameters. The parentheses ARE the call:
#
#   greet      -> the function object itself (not called)
#   greet()    -> a call, the body runs now

print("greet without () is a function:", callable(greet))
# greet without () is a function: True

# callable(greet) asks "is this something you CAN call?" -- True
# for functions. greet alone is a VALUE you could store in a
# variable; greet() is an ACTION that runs the body. We never
# print the raw function object here, because its repr contains a
# memory address that changes per machine, and this course keeps
# every output identical on every run.

# ============================================================
# [3] Built-in functions you already use
# ============================================================
# The transcript points out that print() and len() are functions
# too. You have been calling functions since lesson 1:

print(len("bookshop"))
# 8

print(type(42))
# <class 'int'>

# print, len, type, range, input, int, str, list -- all functions.
# The difference between them and greet() is only that Python
# shipped with those, and you wrote greet(). Same syntax, same
# rules, same calling.

# ============================================================
# [4] Parameters: the function's inputs
# ============================================================
# A function with parameters is a template. The def names what it
# needs; the call supplies what it gets.

def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Osama")
# Hello, Osama!

greet_person("Mona")
# Hello, Mona!

# name is a PARAMETER -- a placeholder name chosen in the def.
# "Osama" and "Mona" are ARGUMENTS -- the actual values passed in
# at each call. People use the two words interchangeably; the
# distinction only matters when you want to say which half you
# mean. Inside the body, name is just a normal variable that
# holds whatever the caller passed.

# ============================================================
# [5] return: hand a value back, do not print it
# ============================================================
# THE central idea of the lesson. print pushes text to the screen
# and the function keeps going with nothing in hand. return gives
# a VALUE to the caller and leaves the function immediately.

def add_print(a, b):
    print("the sum is:", a + b)        # shows it, returns None

def add_return(a, b):
    return a + b                       # shows nothing, returns 30

print("calling add_print:")
result = add_print(10, 20)
# calling add_print:
# the sum is: 30

print("result of add_print:", result)
# result of add_print: None

print("calling add_return:")
result = add_return(10, 20)
# calling add_return:

print("result of add_return:", result)
# result of add_return: 30

# Read the four lines of output slowly:
#
#   add_print   printed inside, returned None (the default)
#   add_return  printed NOTHING inside, returned 30
#
# A function with no return, or with return and nothing after it,
# returns None. None is not an error -- it is the answer "I have
# nothing to give back".

# ============================================================
# [6] Why return matters: store it, use it, print it LATER
# ============================================================
# The transcript's real-world point. Once the value is back in a
# variable, YOU decide where it goes: on screen, into another
# calculation, into a file, onto a web page.

total = add_return(10, 20)             # the value arrives here
doubled = total * 2                    # it works in arithmetic
message = f"Total is {total}"          # it works in text

print("doubled:", doubled)
# doubled: 60

print("message:", message)
# message: Total is 30

# add_print could not do any of this. Its answer went to the
# screen and vanished; nothing was left to multiply or format.
# The rule in one line:
#
#   print is for SHOWING. return is for GIVING.
#
# A function should return what the caller needs, and the caller
# decides whether to print it.

# ============================================================
# [7] return None, and the trap of "returning" a print
# ============================================================
# The trap the transcript warns about, in code:

def broken_add(a, b):
    return print(a + b)                # returns the result of print

value = broken_add(10, 20)
# 30

print("broken_add returned:", value)
# broken_add returned: None

# print() itself returns None, so return print(...) returns None
# and ALSO prints. You get the screen output you did not ask to
# depend on, and no usable value. If you want to both show and
# give, do them as two separate lines:

def working_add(a, b):
    result = a + b
    print("the sum is:", result)
    return result

value = working_add(10, 20)
# the sum is: 30

print("working_add returned:", value)
# working_add returned: 30

# Same information on screen AND a real value in hand. The print
# is optional decoration; the return is the function's answer.

# ============================================================
# [8] Practical: a user profile, print version vs return version
# ============================================================
# The transcript's "fetch user data" example, both ways. The
# return version lets the caller put the data ANYWHERE.

def show_profile_print(name, role):
    """Print a card immediately. Gives the caller nothing."""
    print(f"  {name} - {role}")

def make_profile(name, role):
    """Build and RETURN a ready-to-use dictionary."""
    return {"name": name, "role": role, "active": True}

print("print version:")
show_profile_print("Osama", "admin")
# print version:
#   Osama - admin

print("return version, stored first:")
profile = make_profile("Mona", "user")
print("stored:", profile)
# return version, stored first:
# stored: {'name': 'Mona', 'role': 'user', 'active': True}

# The stored dictionary is now an ordinary variable. It can go to
# a card, a JSON file, an HTTP response, or a test -- wherever the
# application needs it. The print version already decided FOR the
# caller that the destination is the screen, and that is exactly
# the control the transcript says you lose.

# ============================================================
# [9] Returning different types: not just numbers
# ============================================================
# A function can return anything: numbers, text, lists,
# dictionaries, other functions.

def average(values):
    return sum(values) / len(values)     # a float

def shout(text):
    return text.upper()                  # a string

def top_two(values):
    return sorted(values, reverse=True)[:2]   # a list

def make_multiplier(factor):
    def multiply(n):                     # a function inside
        return n * factor
    return multiply

print("average:", average([80, 90, 100]))
# average: 90.0

print("shout:", shout("bookshop"))
# shout: BOOKSHOP

print("top_two:", top_two([5, 9, 1, 7]))
# top_two: [9, 7]

double = make_multiplier(2)
print("double(21):", double(21))
# double(21): 42

# The last one deserves a second look: make_multiplier RETURNS a
# function, and that returned function is then called like any
# other. Nothing magical -- if a value can be stored in a
# variable, and a function is a value (section 2), then a function
# can be returned. Deep waters, but the same shallow rules.

# ============================================================
# [10] return leaves immediately: early exit
# ============================================================
# return does not only end the function -- it ends it FROM WHERE
# IT STANDS. Anything after it in the function never runs. That
# makes it the tool for "already answered, stop here".

def safe_divide(a, b):
    if b == 0:
        return None                      # stop here, no crash
    return a / b                         # only reached if b != 0

print("5 / 2 =", safe_divide(5, 2))
# 5 / 2 = 2.5

print("5 / 0 =", safe_divide(5, 0))
# 5 / 0 = None

# The second call never reached the division line. One function,
# two exit doors, and the caller got None instead of a
# ZeroDivisionError crash. Multiple returns like this are
# Pythonic when each one answers a different case, as long as the
# reader can see which case is which -- one guard clause per line
# is usually enough.

# ============================================================
# [11] Parameters by position, and why order matters
# ============================================================
# Arguments are matched to parameters in ORDER, left to right.

def power(base, exponent):
    return base ** exponent

print("power(2, 10) =", power(2, 10))
# power(2, 10) = 1024

print("power(10, 2) =", power(10, 2))
# power(10, 2) = 100

# Same two numbers, different order, different answer. The first
# argument fills base, the second fills exponent, always. If you
# want the order to not matter at the call site, name the
# arguments explicitly:

print("named:", power(exponent=2, base=10))
# named: 100

# Keyword arguments make the call self-documenting and immune to
# reordering. Lesson files for functions go deeper on defaults and
# *args; this file keeps to the core the transcript asks for.

# ============================================================
# [12] A realistic piece: settings the page can place anywhere
# ============================================================
# Tying section 8 to something that looks like real code. The
# function prepares data. Nothing about WHERE it appears is baked
# in.

def site_settings(user):
    """Return the settings dict a page would need."""
    return {
        "user": user,
        "theme": "dark",
        "language": "ar",
        "notifications": True,
    }

settings = site_settings("Osama")

# A header might show only the name:
print("header shows:", settings["user"])
# header shows: Osama

# A footer might show only the language:
print("footer shows:", settings["language"])
# footer shows: ar

# A test might check the whole thing:
print("theme is dark:", settings["theme"] == "dark")
# theme is dark: True

# One function, three destinations, zero edits to the function.
# Had it printed a fixed card, all three destinations would need
# their own copy of the logic -- or the function would have to
# grow a parameter for "where to print", which is how programs
# rot. return keeps the function small and the caller free.

# ============================================================
# [13] The summary
# ============================================================
# def name(parameters):      write once
# name(arguments):           call anywhere, any number of times
# return value:              give a value back, leave now
#
# A function with no return gives back None -- not a crash, just
# nothing usable. print() itself returns None, so return print(x)
# prints AND gives None: the trap to delete from muscle memory.
#
# The transcript's rule, in its shortest form:
#
#   print is for showing. return is for giving.
#
# Show when the destination is genuinely the screen and nobody
# needs the value. Return when the caller might store it, compute
# with it, format it, test it, or send it across a network --
# which is almost always. A function that returns is a function
# you can build on; a function that only prints is a function you
# can only watch.
#
# Lessons ahead go deeper: default values, multiple parameters,
# scope, and functions as the unit tests that project 40 was
# already running. The shape you learned here -- def, call,
# return -- is the one every one of them keeps.
