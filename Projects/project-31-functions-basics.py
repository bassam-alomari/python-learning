# ============================================================
# PROJECT 31 - Functions Basics (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01-32, plus the for loop from 47-51)
# Topics: All previous + def, return, parameters, arguments,
#        default values, keyword arguments, scope, *args,
#        **kwargs, and the mutable default trap
#
# This project opens the FUNCTIONS arc. Everything so far was
# data: lists, tuples, sets, dicts. A function turns data into
# BEHAVIOUR, and it is the single biggest jump in the course.
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: return versus print
# What does print() do that return() does NOT do, and what does
# return() do that print() cannot do at all?
# (your answer here)

# QUESTION 2: parameters versus arguments
# In def total(price, count): what are "price" and "count"
# called? And in the call total(10, 3), what are 10 and 3 called?
# (your answer here)

# QUESTION 3: default values
# In def greet(name, greeting="Hello"), can I call greet("Ali",
# "Hi")? Can I call greet(greeting="Hi")? Which one works, and
# why the difference?
# (your answer here)

# QUESTION 4: what return None means
# A function ends without a return. What comes back, and is that
# the same as an empty string or an empty list?
# (your answer here)

# QUESTION 5: scope
# I create a variable inside a function and then use it outside.
# What error do I get, and why does it exist at all?
# (your answer here)

# QUESTION 6: the argument trap
# I pass a list to a function, and the function appends to it.
# Does MY list change? What about a string argument instead, and
# why is the answer different?
# (your answer here)

# QUESTION 7: the mutable default trap
# def add(item, target=[]): ... is called twice. What does the
# second call's target contain, and why? What is the fix?
# (your answer here)

# QUESTION 8: *args and **kwargs
# What type does *numbers give you inside the function, and what
# type does **details give you? Name both.
# (your answer here)

# QUESTION 9: why return a tuple
# Why does min_max() below return (min, max) instead of printing
# the two numbers?
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Write greet(name) that RETURNS "Hello <name>" instead of
# printing it. Call it twice, store both results in a list, then
# print that list. Print the length of the list too
# (your code here)

# TASK 2: Write announce(message) that PRINTS inside the function
# and returns nothing. Store the result and print it, so you can
# see that a missing return produces None and not an empty string
# (your code here)

# TASK 3: Write describe(name, age=0, country="unknown") that
# returns a joined string of all three. Call it with one, two and
# three arguments, then call it by keyword while skipping age.
# Print all four
# (your code here)

# TASK 4: Write need_name(name) with no default, then call it with
# NO argument and catch the TypeError. Print the error message
# (your code here)

# TASK 5: Write check(value, limit) that returns "over" or
# "under". Then write first_even(numbers) that returns the first
# even number it meets, or None when there is none. Test
# first_even on a list with one and on a list with none
# (your code here)

# TASK 6: Write local_test() that creates a variable inside itself
# and returns it. Call it successfully, then try to use the same
# name outside the function and catch the NameError
# (your code here)

# TASK 7: Prove the argument trap. Write append_item(items,
# value) that appends and returns, pass it a LIST, then print the
# original list to show it changed. Then pass it a STRING and
# show that the string argument behaves differently
# (your code here)

# TASK 8: Write total(*numbers) that adds every argument. Test it
# with three numbers and with no numbers at all. Also write
# tags(*words, **extra) and print what each one collects
# (your code here)

# TASK 9: THE TRAP. Write add_bad(item, target=[]) exactly as
# shown, call it three times with "a", "b" and "c", and print
# each result so the growing list is visible. Then write
# add_good(item, target=None) with the None guard and call it the
# same three times. Print both sets of results
# (your code here)

# TASK 10: Write profile(name, **details) that returns a string
# with the name and whatever extras arrived. Call it with no
# extras and with two extras, and print both
# (your code here)

# TASK 11: Write min_max(numbers) that RETURNS the smallest and
# the largest as a tuple. Unpack it into two variables, then call
# it again and keep the tuple whole. Print both forms
# (your code here)

# TASK 12: Build a tiny money app. Write and use:
#   add_tax(amount, rate=0.16)  -> the amount plus tax, rounded
#                                  to 2 decimals
#   receipt(items, rate=0.16)   -> takes a list of (name, price)
#                                 pairs and returns a dict with
#                                 "count", "subtotal", "tax" and
#                                 "total"
# The tax rate must have a default AND still be overridable.
# Test the default, then override it, and print every result
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.
#
# Never print a function on its own. Python shows its memory
# address, and that address is different on every run, so it can
# never appear in an expected output.

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
def greet(name):
    return f"Hello {name}"


def shout(name):
    print(f"Hello {name}")


stored = greet("Omar")
print("Q1  greet returns    ->", repr(stored), "(a value I can keep)")
print("Q1  that value works ->", stored.upper())
shout("Omar")
nothing = shout("Mona")
print("Q1  shout returned   ->", repr(nothing), "(only printed)")
# Q1  greet returns    -> 'Hello Omar' (a value I can keep)
# Q1  that value works -> HELLO OMAR
# Q1  shout returned   -> None (only printed)
# print() writes to the screen and forgets. return() hands the value
# back, so it can be stored, compared, changed or printed LATER.

# QUESTION 2
def total(price, count):
    return price * count


print("Q2  price and count are the PARAMETERS")
print("Q2  10 and 3 are the ARGUMENTS ->", total(10, 3))
# Q2  price and count are the PARAMETERS
# Q2  10 and 3 are the ARGUMENTS -> 30

# QUESTION 3
def greet_it(name, greeting="Hello"):
    return f"{greeting} {name}"


print("Q3  greet_it('Ali', 'Hi')   ->", greet_it("Ali", "Hi"))
print("Q3  greet_it(name='Ali')    ->", greet_it(name="Ali"))
print("Q3  skipping 'greeting' is fine, because it HAS a default")
try:
    greet_it(greeting="Hi")
except TypeError as err:
    print("Q3  but skipping 'name' fails -> TypeError:", err)
# Q3  greet_it('Ali', 'Hi')   -> Hi Ali
# Q3  greet_it(name='Ali')    -> Hello Ali
# Q3  skipping 'greeting' is fine, because it HAS a default
# Q3  but skipping 'name' fails -> TypeError: greet_it() missing 1 required positional argument: 'name'
# A parameter with a default may be skipped. A parameter WITHOUT
# one must always be given, either by position or by keyword.

print()
print("Q3  a default must be the LAST parameter")
try:
    exec("def bad_order(age=0, name): pass")
except SyntaxError as err:
    print("Q3  def bad_order(age=0, name) -> SyntaxError:", err)
# Q3  a default must be the LAST parameter
# Q3  def bad_order(age=0, name) -> SyntaxError: parameter without a default follows parameter with a default (<string>, line 1)
# Python cannot tell whether the value you passed is for age or for
# name, so it refuses the order. Write def good_order(name,
# age=0) instead.

# QUESTION 4
def announce(message):
    print(f"Q4  inside announce: {message}")


got = announce("hi")
print("Q4  it returned     ->", repr(got))
print("Q4  None == '' ?", got == "", "| None == [] ?", got == [])
# Q4  inside announce: hi
# Q4  it returned     -> None
# Q4  None == '' ? False | None == [] ? False
# A function without a return gives back None. That is NOT an empty
# string and NOT an empty list, and `if not result` will be True for
# all three, which is a classic source of bugs.

# QUESTION 5
def local_test():
    secret = "inside"
    return secret


print("Q5  inside the function ->", local_test())
try:
    print(secret)
except NameError as err:
    print("Q5  outside it         -> NameError:", err)
# Q5  inside the function -> inside
# Q5  outside it         -> NameError: name 'secret' is not defined
# The function has its own private world. Names made inside it die
# when it ends, so two functions can both use "i" without ever
# meeting. That is why scope exists.

# QUESTION 6
def append_item(items, value):
    items.append(value)
    return items


def touch_text(text, suffix):
    return text + suffix


original = ["a"]
append_item(original, "b")
print("Q6  a list argument  ->", original, "(changed in the caller)")
word = "hi"
touched = touch_text(word, "!")
print("Q6  a string argument->", repr(word), "and", repr(touched))
# Q6  a list argument  -> ['a', 'b'] (changed in the caller)
# Q6  a string argument-> 'hi' and 'hi!'
# A list is a real object, so the function and the caller are
# holding the SAME list. append() edited it in place. A string
# cannot be edited in place, so "hi" stays untouched and the
# function had to build a NEW string. Mutability, again.

# QUESTION 7
def add_bad(item, target=[]):
    target.append(item)
    return target


print("Q7  add_bad('a') ->", add_bad("a"))
print("Q7  add_bad('b') ->", add_bad("b"), "<- 'a' came back!")
print("Q7  add_bad('c') ->", add_bad("c"))


def add_good(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target


print("Q7  add_good('a') ->", add_good("a"))
print("Q7  add_good('b') ->", add_good("b"), "<- clean")
# Q7  add_bad('a') -> ['a']
# Q7  add_bad('b') -> ['a', 'b'] <- 'a' came back!
# Q7  add_bad('c') -> ['a', 'b', 'c']
# Q7  add_good('a') -> ['a']
# Q7  add_good('b') -> ['b'] <- clean
# The list in the default value is built ONCE, when Python reaches
# the def line. Every later call reuses that same list, so it keeps
# growing forever. The fix is None, because None means "no list
# yet" and the body then builds a fresh one each time.

# QUESTION 8
def total(*numbers):
    return sum(numbers)


def collect(*numbers):
    return numbers


print("Q8  *numbers is a", type(collect(1, 2)).__name__, "->", collect(1, 2, 3))
print("Q8  no numbers at all  ->", total())


def tags(*words, **extra):
    return (words, extra)


print("Q8  both together      ->", tags("a", "b", color="red"))
# Q8  *numbers is a tuple -> (1, 2, 3)
# Q8  no numbers at all  -> 0
# Q8  both together      -> (('a', 'b'), {'color': 'red'})
# *args collects the extra positional arguments into a TUPLE.
# **kwargs collects the extra keyword arguments into a DICT.
# The small collect() above exists only to show the type clearly:
# total() gives back a number, so its own type tells us nothing.

# QUESTION 9
def min_max(numbers):
    return min(numbers), max(numbers)


smallest, largest = min_max([4, 9, 2])
print("Q9  unpacked    ->", smallest, largest)
print("Q9  kept whole  ->", min_max([4, 9, 2]))
# Q9  unpacked    -> 2 9
# Q9  kept whole  -> (2, 9)
# print() gives you two lines of text and nothing to work with.
# Returning a tuple gives the caller BOTH values, and they can
# either unpack them or keep the tuple. This is exactly why
# top_student() in project 29 returned (name, average).

print("-" * 60)

# TASK 1
def greet_t(name):
    return f"Hello {name}"


both = [greet_t("Omar"), greet_t("Mona")]
print("T1  the two results ->", both)
print("T1  the list length ->", len(both))
# T1  the two results -> ['Hello Omar', 'Hello Mona']
# T1  the list length -> 2

# TASK 2
def announce_t(message):
    print(f"T2  inside the function: {message}")


returned = announce_t("hi")
print("T2  what came back    ->", repr(returned))
print("T2  is it an empty str ->", returned == "")
# T2  inside the function: hi
# T2  what came back    -> None
# T2  is it an empty str -> False

# TASK 3
def describe_t(name, age=0, country="unknown"):
    return f"{name} | {age} | {country}"


print("T3  one argument      ->", describe_t("Omar"))
print("T3  two arguments     ->", describe_t("Omar", 21))
print("T3  three arguments   ->", describe_t("Omar", 21, "Jordan"))
print("T3  by keyword        ->", describe_t(name="Omar", country="Jordan"))
# T3  one argument      -> Omar | 0 | unknown
# T3  two arguments     -> Omar | 21 | unknown
# T3  three arguments   -> Omar | 21 | Jordan
# T3  by keyword        -> Omar | 0 | Jordan

# TASK 4
def need_name(name):
    return name


try:
    need_name()
except TypeError as err:
    print("T4  with no argument -> TypeError:", err)
# T4  with no argument -> TypeError: need_name() missing 1 required positional argument: 'name'

# TASK 5
def check(value, limit):
    if value > limit:
        return "over"
    return "under"


def first_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            return n
    return None


print("T5  check(10, 5)     ->", check(10, 5))
print("T5  check(1, 5)      ->", check(1, 5))
print("T5  first even found ->", first_even([1, 3, 4, 6]))
print("T5  nothing found    ->", first_even([1, 3, 5]))
# T5  check(10, 5)     -> over
# T5  check(1, 5)      -> under
# T5  first even found -> 4
# T5  nothing found    -> None
# return gives the function TWO exits here. The loop also exits at
# the first even number, which is why a list can be searched in one
# line instead of a loop written by hand.

# TASK 6
def local_test_t():
    secret = "inside"
    return secret


print("T6  from inside      ->", local_test_t())
try:
    print(secret)
except NameError as err:
    print("T6  from outside     -> NameError:", err)
# T6  from inside      -> inside
# T6  from outside     -> NameError: name 'secret' is not defined

# TASK 7
def append_t(items, value):
    items.append(value)
    return items


def touch_text_t(text, suffix):
    return text + suffix


original_list = ["a"]
append_t(original_list, "b")
print("T7  a list, after    ->", original_list, "(the caller sees it)")
original_text = "hi"
touched_text = touch_text_t(original_text, "!")
print("T7  a string, after  ->", repr(original_text), "| result", repr(touched_text))
# T7  a list, after    -> ['a', 'b'] (the caller sees it)
# T7  a string, after  -> 'hi' | result 'hi!'
# If a function should NOT be able to change what you passed it,
# take a copy first: append_t(original_list[:], "b").

# TASK 8
def total_t(*numbers):
    return sum(numbers)


def tags_t(*words, **extra):
    return (words, extra)


print("T8  three numbers    ->", total_t(1, 2, 3))
print("T8  no numbers       ->", total_t())
print("T8  words and extras ->", tags_t("a", "b", color="red"))
# T8  three numbers    -> 6
# T8  no numbers       -> 0
# T8  words and extras -> (('a', 'b'), {'color': 'red'})
# total_t() with nothing works because sum() of an empty tuple is 0.

# TASK 9
def add_bad_t(item, target=[]):
    target.append(item)
    return target


print("T9  bad, first call  ->", add_bad_t("a"))
print("T9  bad, second call ->", add_bad_t("b"))
print("T9  bad, third call  ->", add_bad_t("c"))


def add_good_t(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target


print("T9  good, first call ->", add_good_t("a"))
print("T9  good, second call->", add_good_t("b"))
print("T9  good, third call ->", add_good_t("c"))
# T9  bad, first call  -> ['a']
# T9  bad, second call -> ['a', 'b']
# T9  bad, third call  -> ['a', 'b', 'c']
# T9  good, first call -> ['a']
# T9  good, second call-> ['b']
# T9  good, third call -> ['c']
# The bad version never forgets, because the default list is built
# once at the def line and then shared by every call. The good
# version builds a new list each time, because None cannot grow.

# TASK 10
def profile_t(name, **details):
    return f"{name} -> {details}"


print("T10 with no extras   ->", profile_t("Omar"))
print("T10 with two extras  ->", profile_t("Omar", city="Amman", age=21))
# T10 with no extras   -> Omar -> {}
# T10 with two extras  -> Omar -> {'city': 'Amman', 'age': 21}
# With no extras, details is still a dict, just an empty one.

# TASK 11
def min_max_t(numbers):
    return min(numbers), max(numbers)


small, large = min_max_t([4, 9, 2])
print("T11 unpacked         ->", small, large)
print("T11 kept as a tuple  ->", min_max_t([4, 9, 2]))
# T11 unpacked         -> 2 9
# T11 kept as a tuple  -> (2, 9)

# TASK 12
def add_tax(amount, rate=0.16):
    """Return the amount plus its tax, rounded to 2 decimals."""
    return round(amount + (amount * rate), 2)


def receipt(items, rate=0.16):
    """Return a summary dict for a list of (name, price) pairs."""
    subtotal = 0.0
    for _name, price in items:
        subtotal += price
    tax = round(subtotal * rate, 2)
    return {
        "count": len(items),
        "subtotal": round(subtotal, 2),
        "tax": tax,
        "total": round(subtotal + tax, 2),
    }


basket = [("pen", 2.50), ("book", 12.00), ("bag", 8.25)]
print("T12 add_tax(100)          ->", add_tax(100))
print("T12 add_tax(100, 0.10)    ->", add_tax(100, 0.10))
print("T12 the basket            ->", basket)
print("T12 with the default rate ->", receipt(basket))
print("T12 with rate 0.05        ->", receipt(basket, 0.05))
print("T12 the basket afterwards ->", basket, "(untouched)")
# T12 add_tax(100)          -> 116.0
# T12 add_tax(100, 0.10)    -> 110.0
# T12 the basket            -> [('pen', 2.5), ('book', 12.0), ('bag', 8.25)]
# T12 with the default rate -> {'count': 3, 'subtotal': 22.75, 'tax': 3.64, 'total': 26.39}
# T12 with rate 0.05        -> {'count': 3, 'subtotal': 22.75, 'tax': 1.14, 'total': 23.89}
# T12 the basket afterwards -> [('pen', 2.5), ('book', 12.0), ('bag', 8.25)] (untouched)
# The default rate can be replaced because rate is a normal
# parameter with a default, which is the safe kind from TASK 9: the
# number 0.16 cannot change, so sharing it is harmless.

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 31")
print("=" * 60)
# ============================================================
# END OF PROJECT 31
# ============================================================