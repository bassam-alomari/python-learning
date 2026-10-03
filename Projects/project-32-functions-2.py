# ============================================================
# PROJECT 32 - Functions Part 2 (Theory + Code)
# ============================================================
# Level: Beginner (Lessons 01-32, plus the for loop from 47-51)
# Topics: All previous + scope in depth, global, nonlocal,
#        closures, recursion, lambda, functions as values,
#        map/filter, recursion cost
#
# Project 31 introduced def and return. This one goes further:
# where names live, how a function can remember something, how a
# function can call itself, and how a function becomes a VALUE
# you can pass around.
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: reading a global
# I read a module level variable inside a function without
# writing global. Is that allowed? Which keyword is only needed
# when you want to REPLACE it?
# (your answer here)

# QUESTION 2: assignment makes a new local
# A function assigns to a name that also exists outside it. Does
# the outside value change? Why does Python let this happen
# instead of raising an error?
# (your answer here)

# QUESTION 3: nonlocal
# I have a variable in an OUTER function and I want to change it
# from an inner function. Which keyword does that, and which
# keyword is the WRONG one to use?
# (your answer here)

# QUESTION 4: what is a closure
# An inner function uses a variable from the function around it.
# The outer function has already RETURNED. Where does that value
# live now?
# (your answer here)

# QUESTION 5: recursion
# What are the two things EVERY recursive function must have to
# avoid running forever, and what error do you get if one is
# missing?
# (your answer here)

# QUESTION 6: recursion is expensive
# Calling a naive fib(15) makes far more calls than fib(10).
# Roughly how many times bigger is it, and what is the normal fix?
# (your answer here)

# QUESTION 7: lambda
# When is a lambda BETTER than a def, and when is it worse? Name
# one clear advantage and one clear disadvantage.
# (your answer here)

# QUESTION 8: functions as values
# I pass a function into another function as an argument. What
# term describes that, and which two builtins use it heavily?
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Write read_global() that RETURNS a module level
# variable, and write_global() that REPLACES it using global.
# Print the value before, the result of reading, and the value
# after writing. Then write write_local() that assigns the same
# name WITHOUT global and show that the real value survives
# (your code here)

# TASK 2: Write make_counter() returning an inner function that
# counts 1, 2, 3 and uses nonlocal. Call the same counter four
# times, then make a SECOND counter and call it twice, printing
# everything. Explain in a comment why the two counters do not
# interfere
# (your code here)

# TASK 3: Write a three level nest: outer -> middle -> inner,
# where the inner READS a variable from the outer, then ASSIGNS
# to it using nonlocal. Print the value at each level so the
# effect is visible
# (your code here)

# TASK 4: Write factorial(n) recursively and factorial_loop(n)
# with a for loop. Print both for 1, 5 and 0. Then write
# forever(n) that calls itself with no base case, and catch the
# RecursionError
# (your code here)

# TASK 5: Write fib(n) recursively and print fib from 0 to 8 in
# one list comprehension. Then write counted_fib(n, counter)
# that increments a counter list on every call, and print how
# many calls fib(10) needs
# (your code here)

# TASK 6: Write search(numbers, target) with a for loop that
# returns the index of the target or -1, then write the same
# thing recursively with an index parameter. Print all four
# results and confirm they agree
# (your code here)

# TASK 7: Write double() with def and triple() with lambda. Pass
# BOTH into list(map(...)) over [1, 2, 3] and print the two
# results. Do NOT print a map object on its own
# (your code here)

# TASK 8: Use lambda with filter() to keep only the even numbers
# of [1, 2, 3, 4, 5, 6], and with sorted() to order a list of
# (score, name) pairs from the highest score down. Print both
# (your code here)

# TASK 9: Write apply_twice(function, value) that calls the
# function on the value twice. Test it with a times_two function,
# and then with add_tax from TASK 11 below. Print both results
# (your code here)

# TASK 10: Write a counter that PROVES the project-31 trap is
# about the DEFAULT ARGUMENT and not about closures. Make two
# separate default-argument accumulators and show they share one
# list, then make two separate closure accumulators and show they
# do NOT share. Print everything
# (your code here)

# TASK 11: Build a small cart app using functions only. Write:
#   add_tax(amount, rate=0.16)      -> amount plus tax, 2 dp
#   line_total(item)                -> takes (name, price,
#                                       quantity) and returns
#                                       the total for that line
#   cart_total(items, rate=0.16)    -> takes a list of lines and
#                                       returns (subtotal, total)
# Test with three lines and print every part. Then test
# apply_twice with add_tax on a single amount
# (your code here)

# TASK 12: Write memoize(fib) that wraps a slow recursive fib and
# remembers the answers in a dict, so the SECOND call does almost
# no work. Count the real calls of both and print both counts
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.
#
# A map object and a function both carry a memory address, so
# neither is ever printed on its own here.

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
value = "global value"


def read_global():
    return value


def write_global():
    global value
    value = "changed by the function"


print("Q1  before the write ->", value)
print("Q1  read_global()    ->", read_global())
write_global()
print("Q1  after the write  ->", value)
# Q1  before the write -> global value
# Q1  read_global()    -> global value
# Q1  after the write  -> changed by the function
# READING a global needs no keyword at all. The global keyword is
# only required when you want to REPLACE the name, because an
# assignment inside a function creates a local by default.

# QUESTION 2
def write_local():
    value = "local copy"
    return value


returned = write_local()
print("Q2  write_local() returned ->", returned)
print("Q2  the real value         ->", value, "(survived)")
# Q2  write_local() returned -> local copy
# Q2  the real value         -> changed by the function (survived)
# Python does not raise here on purpose. If a function could not
# create its own local, then any name it used for scratch work
# would risk overwriting something outside it. Two functions can
# both use "i" as a loop counter and never meet.

# QUESTION 3
def outer():
    count = 0

    def middle():
        def inner():
            nonlocal count
            count += 1
            return count

        return inner()

    return middle()


print("Q3  after the inner ran ->", outer())
# Q3  after the inner ran -> 1
# nonlocal reaches UP to the nearest enclosing function that owns
# the name. global reaches all the way to the module, and would be
# the WRONG keyword here: count does not live at module level.

# QUESTION 4
def make_counter():
    count = 0

    def bump():
        nonlocal count
        count += 1
        return count

    return bump


survivor = make_counter()
print("Q4  three calls later   ->", survivor(), survivor(), survivor())
print("Q4  the outer function ended, but count is still alive inside")
# Q4  three calls later   -> 1 2 3
# Q4  the outer function ended, but count is still alive inside
# This is a CLOSURE. The inner function keeps a reference to the
# cell that holds count, so the value outlives the function that
# made it. That is how a function gets memory without a class.

print("-" * 60)

# QUESTION 5
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def forever(n):
    return forever(n + 1)


print("Q5  factorial(5) ->", factorial(5), "(the base case stops it)")
try:
    forever(0)
except RecursionError as err:
    print("Q5  forever(0)   -> RecursionError:", err)
# Q5  factorial(5) -> 120 (the base case stops it)
# Q5  forever(0)   -> RecursionError: maximum recursion depth exceeded
# A recursive function needs a BASE CASE and a call that moves
# TOWARD it. Without one, the calls never end and Python stops
# them at its recursion limit instead of letting the machine run
# out of memory.

# QUESTION 6
calls = [0]


def slow_fib(n):
    calls[0] += 1
    if n <= 1:
        return n
    return slow_fib(n - 1) + slow_fib(n - 2)


for n in (10, 15):
    calls[0] = 0
    slow_fib(n)
    print(f"Q6  slow_fib({n}) made ->", calls[0], "calls")
# Q6  slow_fib(10) made -> 177 calls
# Q6  slow_fib(15) made -> 1973 calls
# Five more inputs produced about ELEVEN times the work. The normal
# fixes are memoization (remember the answers) or a plain loop.

# QUESTION 7
def triple_def(n):
    return n * 3


triple_lambda = lambda n: n * 3
print("Q7  def    ->", triple_def(4))
print("Q7  lambda ->", triple_lambda(4))
print("Q7  lambda is shorter, but it has no name to reuse or trace")
# Q7  def    -> 12
# Q7  lambda -> 12
# Q7  lambda is shorter, but it has no name to reuse or trace
# A lambda is good as a quick argument, for example inside
# sorted(key=...). It is bad for anything you need to read later,
# because there is no name in the traceback and no docstring.

# QUESTION 8
print("Q8  map    ->", list(map(lambda n: n * 2, [1, 2, 3])))
print("Q8  filter ->", list(filter(lambda n: n % 2 == 0, [1, 2, 3, 4])))
# Q8  map    -> [2, 4, 6]
# Q8  filter -> [2, 4]
# Passing a function as an argument is "a function as a first class
# value". map() and filter() are built around it: map transforms
# every item, filter keeps only the items a test accepts.

print("-" * 60)

# TASK 1
value = "global value"


def read_global_t():
    return value


def write_global_t():
    global value
    value = "changed by the function"


def write_local_t():
    value = "local copy"
    return value


print("T1  before        ->", value)
print("T1  read_global   ->", read_global_t())
write_global_t()
print("T1  after global  ->", value)
print("T1  write_local   ->", write_local_t())
print("T1  the real one  ->", value, "(untouched by the local write)")
# T1  before        -> global value
# T1  read_global   -> global value
# T1  after global  -> changed by the function
# T1  write_local   -> local copy
# T1  the real one  -> changed by the function (untouched by the local write)

# TASK 2
def make_counter_t():
    count = 0

    def bump():
        nonlocal count
        count += 1
        return count

    return bump


first_counter = make_counter_t()
second_counter = make_counter_t()
print("T2  first, four calls  ->", first_counter(), first_counter(), first_counter(), first_counter())
print("T2  second, two calls  ->", second_counter(), second_counter())
# T2  first, four calls  -> 1 2 3 4
# T2  second, two calls  -> 1 2
# Each call to make_counter_t() runs the body again and makes a
# brand new count. So the two counters hold two separate numbers
# and can never interfere.

# TASK 3
def outer_t():
    total = "start"

    def middle_t():
        def inner_t():
            nonlocal total
            total = "changed by inner"
            return total

        before = total
        inner_result = inner_t()
        return before, inner_result, total

    return middle_t()


before, inside, after = outer_t()
print("T3  inside middle, before ->", before)
print("T3  inside inner          ->", inside)
print("T3  inside middle, after  ->", after)
# T3  inside middle, before -> start
# T3  inside inner          -> changed by inner
# T3  inside middle, after  -> changed by inner
# NONLOCAL, not global. total belongs to outer_t, and middle_t can
# see it but inner_t can only reach it through nonlocal. Using
# global here would create a different, module level variable.

# TASK 4
def factorial_t(n):
    if n <= 1:
        return 1
    return n * factorial_t(n - 1)


def factorial_loop_t(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def forever_t(n):
    return forever_t(n + 1)


for n in (1, 5, 0):
    print(f"T4  factorial({n})      ->", factorial_t(n), "| loop ->", factorial_loop_t(n))
try:
    forever_t(0)
except RecursionError as err:
    print("T4  forever_t(0)        -> RecursionError:", err)
# T4  factorial(1)      -> 1 | loop -> 1
# T4  factorial(5)      -> 120 | loop -> 120
# T4  factorial(0)      -> 1 | loop -> 1
# T4  forever_t(0)        -> RecursionError: maximum recursion depth exceeded
# Both versions agree. The loop uses no stack at all, so it can go
# deeper without ever meeting the recursion limit.

# TASK 5
def fib_t(n):
    if n <= 1:
        return n
    return fib_t(n - 1) + fib_t(n - 2)


print("T5  fib 0 to 8 ->", [fib_t(n) for n in range(9)])


def counted_fib_t(n, counter):
    counter[0] += 1
    if n <= 1:
        return n
    return counted_fib_t(n - 1, counter) + counted_fib_t(n - 2, counter)


box = [0]
fib_t(10)
counted_fib_t(10, box)
print("T5  fib(10) needs    ->", box[0], "calls, to produce", fib_t(10))
# T5  fib 0 to 8 -> [0, 1, 1, 2, 3, 5, 8, 13, 21]
# T5  fib(10) needs    -> 177 calls, to produce 55
# 177 calls to produce one number. Almost all of them recompute an
# answer that was already found, which is exactly what TASK 12 fixes.

# TASK 6
def search_t(numbers, target):
    for index, value in enumerate(numbers):
        if value == target:
            return index
    return -1


def search_recursive_t(numbers, target, index=0):
    if index >= len(numbers):
        return -1
    if numbers[index] == target:
        return index
    return search_recursive_t(numbers, target, index + 1)


data = [4, 9, 2]
print("T6  loop, found        ->", search_t(data, 9))
print("T6  loop, missing      ->", search_t(data, 7))
print("T6  recursion, found   ->", search_recursive_t(data, 9))
print("T6  recursion, missing ->", search_recursive_t(data, 7))
# T6  loop, found        -> 1
# T6  loop, missing      -> -1
# T6  recursion, found   -> 1
# T6  recursion, missing -> -1
# Same answers, two styles. The recursive one needs a second
# parameter to carry its position, and a check for running off the
# end. That extra bookkeeping is the usual price of recursion.

# TASK 7
def double_t(n):
    return n * 2


triple_t = lambda n: n * 3
print("T7  map with double ->", list(map(double_t, [1, 2, 3])))
print("T7  map with triple ->", list(map(triple_t, [1, 2, 3])))
# T7  map with double -> [2, 4, 6]
# T7  map with triple -> [3, 6, 9]
# map() walks the list and hands each item to your function. The
# lambda is perfect here because it is used once and needs no name.

# TASK 8
numbers = [1, 2, 3, 4, 5, 6]
print("T8  filter evens        ->", list(filter(lambda n: n % 2 == 0, numbers)))
scored = [(70, "Omar"), (95, "Mona"), (82, "Ali")]
ordered = sorted(scored, key=lambda pair: -pair[0])
print("T8  sorted by score      ->", ordered)
print("T8  names only           ->", [name for _score, name in ordered])
# T8  filter evens        -> [2, 4, 6]
# T8  sorted by score      -> [(95, 'Mona'), (82, 'Ali'), (70, 'Omar')]
# T8  names only           -> ['Mona', 'Ali', 'Omar']
# This is where a lambda earns its place: one line, used once, and
# it says exactly what it does. Sorting straight would have sorted
# by the score ASCENDING, so the - flips it.

# TASK 9
def apply_twice_t(function, value):
    return function(function(value))


def times_two_t(n):
    return n * 2


print("T9  apply_twice(times_two, 3) ->", apply_twice_t(times_two_t, 3))
print("T9  apply_twice(times_two, 0) ->", apply_twice_t(times_two_t, 0))
# T9  apply_twice(times_two, 3) -> 12
# T9  apply_twice(times_two, 0) -> 0
# apply_twice knows NOTHING about doubling. It only knows it may
# call whatever function it was handed. That is the whole idea of
# passing a function as an argument.

# TASK 10
def default_accumulator_t(item, target=[]):
    target.append(item)
    return target


def make_closure_accumulator_t():
    collected = []

    def add(item):
        collected.append(item)
        return collected

    return add


default_one = default_accumulator_t
print("T10 default, first  ->", default_accumulator_t("a"))
print("T10 default, second ->", default_accumulator_t("b"), "<- shared list")

closure_one = make_closure_accumulator_t()
closure_two = make_closure_accumulator_t()
first_in_one = closure_one("a")
second_in_one = closure_one("b")
print("T10 closure one, stored 'a' ->", first_in_one)
print("T10 closure one, stored 'b' ->", second_in_one)
print("T10 both show the SAME list ->", first_in_one is second_in_one)
print("T10 closure two             ->", closure_two("x"), "<- its OWN list")
print("T10 one is not two          ->", closure_one("c"))
print("T10 two unchanged           ->", closure_two("y"))
# T10 default, first  -> ['a']
# T10 default, second -> ['a', 'b'] <- shared list
# T10 closure one, stored 'a' -> ['a', 'b']
# T10 closure one, stored 'b' -> ['a', 'b']
# T10 both show the SAME list -> True
# T10 closure two             -> ['x'] <- its OWN list
# T10 one is not two          -> ['a', 'b', 'c']
# T10 two unchanged           -> ['x', 'y']
# TWO lessons here, and both come from the same one-line cause.
#
# First, the project 31 trap is NOT caused by closures. It is
# caused by a DEFAULT ARGUMENT, which Python builds ONCE at the
# def line, so every call to that one function shares it. A
# variable inside a closure is built FRESH on every call to the
# maker, so closure_one and closure_two never share.
#
# Second, "stored 'a'" and "stored 'b'" now print the SAME
# ['a', 'b'], and `is` says True. The closure returns its live
# list instead of a copy, so the first answer changed after the
# fact. If you need a snapshot, return list(collected) instead.

# the unused name below used to sit here and did nothing:
# default_one = default_accumulator_t

# TASK 11
def add_tax_t(amount, rate=0.16):
    """Return the amount plus its tax, rounded to 2 decimals."""
    return round(amount + amount * rate, 2)


def line_total_t(item):
    """Return the total for one (name, price, quantity) line."""
    name, price, quantity = item
    return round(price * quantity, 2)


def cart_total_t(items, rate=0.16):
    """Return (subtotal, total) for a list of cart lines."""
    subtotal = 0.0
    for item in items:
        subtotal += line_total_t(item)
    subtotal = round(subtotal, 2)
    return (subtotal, round(subtotal + subtotal * rate, 2))


cart = [
    ("pen", 2.50, 3),
    ("book", 12.00, 1),
    ("bag", 8.25, 2),
]
for item in cart:
    print(f"T11 line {item[0]:5} ->", line_total_t(item))
sub, total = cart_total_t(cart)
print("T11 subtotal       ->", sub)
print("T11 with tax       ->", total)
print("T11 with rate 0.05 ->", cart_total_t(cart, 0.05))
print("T11 apply_twice    ->", apply_twice_t(add_tax_t, 100))
print("T11 the cart after ->", cart, "(untouched)")
# T11 line pen   -> 7.5
# T11 line book  -> 12.0
# T11 line bag   -> 16.5
# T11 subtotal       -> 36.0
# T11 with tax       -> 41.76
# T11 with rate 0.05 -> (36.0, 37.8)
# T11 apply_twice    -> 134.56
# T11 the cart after -> [('pen', 2.5, 3), ('book', 12.0, 1), ('bag', 8.25, 2)] (untouched)
# apply_twice(tax) taxes the tax, which is NOT how real tax works.
# It is here to prove a point: add_tax_t has a DEFAULT rate, and a
# default on an immutable number is completely safe. Only a
# MUTABLE default is dangerous.

# TASK 12
def slow_fib_t(n):
    if n <= 1:
        return n
    return slow_fib_t(n - 1) + slow_fib_t(n - 2)


def memoize(function):
    """Wrap a function so it remembers answers it already computed."""
    cache = {}

    def wrapper(n):
        if n not in cache:
            cache[n] = function(n)
        return cache[n]

    return wrapper


real_calls = [0]


def counted_slow_fib_t(n):
    """The slow fib itself, counting every time it is entered."""
    real_calls[0] += 1
    if n <= 1:
        return n
    return counted_slow_fib_t(n - 1) + counted_slow_fib_t(n - 2)


def memoize(function):
    """Wrap a function so it remembers answers it already computed."""
    cache = {}

    def wrapper(n):
        if n not in cache:
            cache[n] = function(n)
        return cache[n]

    return wrapper


fast_fib = memoize(counted_slow_fib_t)
real_calls[0] = 0
first_answer = fast_fib(20)
first_calls = real_calls[0]
real_calls[0] = 0
second_answer = fast_fib(20)
second_calls = real_calls[0]

print("T12 the answer, both times ->", first_answer, "/", second_answer)
print("T12 real calls, first time ->", first_calls)
print("T12 real calls, second time->", second_calls)
print("T12 so the cache turned", first_calls, "calls into", second_calls)
# T12 the answer, both times -> 6765 / 6765
# T12 real calls, first time -> 21891
# T12 real calls, second time-> 0
# T12 so the cache turned 21891 calls into 0
# The second call did NO work at all, because the dict already held
# every answer. 21891 real calls became 0. Notice what the cache
# is NOT: it is not a default argument, so it is NOT shared with
# anything. It is a closure variable inside memoize, which means
# it belongs to this one wrapper and to nothing else in the program.

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 32")
print("=" * 60)
# ============================================================
# END OF PROJECT 32
# ============================================================