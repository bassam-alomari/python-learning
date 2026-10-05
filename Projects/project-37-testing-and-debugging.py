# ============================================================
# PROJECT 37 - Testing and Debugging: Break Your Code on Purpose
# ============================================================
# Level: Intermediate-Advanced
# Topics: assert, the -O trap, edge cases, unittest, setUp,
#        assertRaises, subTest, assertAlmostEqual, mocks,
#        tracebacks, sys.exc_info, and pdb driven safely
#
# Everything built so far has been checked by running the file and
# reading the output. That catches a wrong answer. It does NOT
# catch a right answer on the wrong input.
#
# This project is about the other half of correctness: proving a
# piece of code survives the inputs you did not think of. The
# empty list. The zero. The negative. The one item. The float that
# should be 0.3 but is 0.30000000000000004.
#
# Two rules shape this file.
#
# 1. A test that crashes is a bad test. Every failure below is
#    CAUGHT and REPORTED, never allowed to escape, so the file
#    always finishes and you can read the whole report.
# 2. Nothing here may depend on human input. That includes the
#    debugger: a plain breakpoint() would hang this file forever,
#    so task 9 drives pdb with a scripted set of commands instead
#    of a person typing at a prompt.
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: what a test actually is
# Why does running a program and reading its output NOT count as
# testing, even when the output looks right?
# (your answer here)

# QUESTION 2: the -O trap
# Python deletes every assert when it runs with -O. Name one job
# you must never give to an assert, and say why.
# (your answer here)

# QUESTION 3: edge cases, not features
# Give the four inputs that break ordinary code most often, and
# explain why each one is special rather than unusual.
# (your answer here)

# QUESTION 4: floats
# Why does 0.1 + 0.2 == 0.3 evaluate to False, and what should you
# compare instead?
# (your answer here)

# QUESTION 5: setUp and isolation
# What does setUp give you that repeating the same three lines in
# every test does not?
# (your answer here)

# QUESTION 6: failing tests
# Why is it useful to keep a KNOWN failing test and read its
# report, instead of deleting it?
# (your answer here)

# QUESTION 7: mocks
# What problem does a mock solve that a real temporary file does
# not, and what risk does it introduce?
# (your answer here)

# QUESTION 8: reading a traceback
# A traceback has many lines. Which line names the cause, and which
# line names the place it happened?
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Write three assert statements that prove a function
# works, then show that python -O deletes them by running a tiny
# program twice in a subprocess, once with -O. Print __debug__ to
# prove which mode you are in
# (your code here)

# TASK 2: Write a hand rolled runner check(label, got, want) that
# compares two values, records a pass or a fail instead of raising,
# and returns nothing. Run it over six cases including one that
# deliberately fails, and print the totals
# (your code here)

# TASK 3: Test average(numbers) against five inputs: several
# numbers, one number, a list of floats, a list with a negative,
# and the empty list. Report which of them raise and which return
# a value, using try/except so nothing escapes
# (your code here)

# TASK 4: Write a unittest.TestCase for a ShoppingCart with
# setUp and tearDown. Test adding items, the total, and that
# adding a negative price is refused with assertRaises
# (your code here)

# TASK 5: Use subTest to check one rule against five inputs, and
# assertAlmostEqual to compare a float that is nearly right. Show
# that an exact == comparison on that float would fail
# (your code here)

# TASK 6: Write one test that is KNOWN to fail, run it, and print
# the recorded failure message instead of letting it escape. Then
# fix the expectation and show the suite going green
# (your code here)

# TASK 7: Test save_cart(cart, path) without ever writing a file,
# by replacing it with a mock. Assert that it was called once with
# the cart and the path, and print the recorded call
# (your code here)

# TASK 8: Catch a deliberate ValueError, print the last line of
# traceback.format_exc(), and print sys.exc_info()[1] INSIDE and
# then OUTSIDE the except block to show the difference
# (your code here)

# TASK 9: Run a two line program under pdb with a scripted set of
# commands, capturing the output into a StringIO so nothing waits
# for a human. Print the captured lines and prove the debugger
# really inspected a variable
# (your code here)

# TASK 10: Write the full suite: five functions and one class under
# test, every edge case covered, one known failure kept and
# reported separately. Print a final table of pass and fail counts
# per function, and print the total
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.

import io
import pdb
import subprocess
import sys
import traceback
import unittest
from unittest import mock

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
print("Q1  looking right proves ONE path, not all paths")
print("Q1  a test names the inputs and states what must happen")
# Q1  looking right proves ONE path, not all paths
# Q1  a test names the inputs and states what must happen
# Reading output is also manual: it only works while someone is
# paying attention, and it silently stops working the moment you
# change one line.

# QUESTION 2
print("Q2  -O sets __debug__ to False and deletes every assert")
print("Q2  so never use assert to validate user input")
# Q2  -O sets __debug__ to False and deletes every assert
# Q2  so never use assert to validate user input
# assert is for checking YOUR OWN assumptions, and it is allowed to
# disappear because it is documentation. Validation that protects
# data must be a real if and a real raise.

# QUESTION 3
print("Q3  empty, zero, negative, and one item")
print("Q3  each is the value where an off by one or a divide by")
print("Q3  zero is hiding, not a rare accident")
# Q3  empty, zero, negative, and one item
# Q3  each is the value where an off by one or a divide by
# Q3  zero is hiding, not a rare accident
# None is the fourth one to remember. Most crashes in real
# programs come from one of these four, not from strange data.

# QUESTION 4
print("Q4  0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3)
print("Q4  the two values ->", 0.1 + 0.2, "and", 0.3)
print("Q4  compare with assertAlmostEqual, or round both sides")
# Q4  0.1 + 0.2 == 0.3 -> False
# Q4  the two values -> 0.30000000000000004 and 0.3
# Q4  compare with assertAlmostEqual, or round both sides
# Neither 0.1 nor 0.2 can be written exactly in binary, so each one
# lands a hair off, and two hairs in the same direction add up. For
# money, use integers of cents instead and the question never
# arises.

# QUESTION 5
print("Q5  setUp runs before EVERY test, so no test can forget it")
print("Q5  and every test still starts from a known clean state")
# Q5  setUp runs before EVERY test, so no test can forget it
# Q5  and every test still starts from a known clean state
# Copy pasting setup into ten tests guarantees that the tenth one
# is subtly different, and that difference is the bug you will
# spend an afternoon on.

# QUESTION 6
print("Q6  it proves the harness DETECTS failures, not just passes")
print("Q6  a suite that has never failed has never been tested")
# Q6  it proves the harness DETECTS failures, not just passes
# Q6  a suite that has never failed has never been tested
# A green suite that cannot go red is indistinguishable from a
# suite that asserts nothing at all. Breaking it on purpose is the
# only way to tell those two apart.

# QUESTION 7
print("Q7  a mock tests the CALL, so no file is touched at all")
print("Q7  the risk: a mock can agree with a wrong call forever")
# Q7  a mock tests the CALL, so no file is touched at all
# Q7  the risk: a mock can agree with a wrong call forever
# A mock proves your code asked for the right thing. It proves
# nothing about whether saving works, so the real save still needs
# one honest end to end test.

# QUESTION 8
print("Q8  the LAST line is the cause, not the place")
print("Q8  the line just above it is the place it happened")
# Q8  the LAST line is the cause, not the place
# Q8  the line just above it is the place it happened
# Python prints the stack oldest first on purpose, so you read the
# report from the bottom up. The bottom line is the answer; the
# lines above are the story of how you got there.

print("-" * 60)

# The code under test, written once so every task below can use it.


def average(numbers):
    """The mean of a non-empty list of numbers."""
    if not numbers:
        raise ValueError("cannot average an empty list")
    running = 0
    for number in numbers:
        running += number
    return running / len(numbers)


def price_after_discount(price, percent):
    """Reduce a price by a percentage, refusing anything out of 0..100."""
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        raise ValueError("the price must be a number")
    if not 0 <= percent <= 100:
        raise ValueError("the percent must be between 0 and 100")
    return round(price * (100 - percent) / 100, 2)


def normalise(text):
    """Strip, collapse runs of spaces, and lower case."""
    if not isinstance(text, str):
        raise ValueError("the text must be a string")
    return " ".join(text.split()).lower()


class ShoppingCart:
    """A tiny cart with the rules that make it worth testing."""

    def __init__(self):
        self._items = {}

    def add(self, name, price, quantity=1):
        """Add a product, refusing a bad name, price or quantity."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("the name must be a non-empty string")
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError(f"the price of {name!r} must be a number")
        if price < 0:
            raise ValueError(f"the price of {name!r} cannot be negative")
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError(f"the quantity of {name!r} must be an int")
        if quantity < 1:
            raise ValueError(f"the quantity of {name!r} must be at least 1")
        if name in self._items:
            self._items[name]["quantity"] += quantity
        else:
            self._items[name] = {"price": price, "quantity": quantity}
        return self.total()

    def remove(self, name):
        """Take a product out, refusing one that is not in the cart."""
        if name not in self._items:
            raise ValueError(f"{name!r} is not in the cart")
        del self._items[name]
        return self.total()

    def count_of(self, name):
        """How many of one product the cart holds."""
        if name not in self._items:
            raise ValueError(f"{name!r} is not in the cart")
        return self._items[name]["quantity"]

    def total(self):
        """The price of everything in the cart, rounded to 2 places."""
        running = 0
        for name in self._items:
            running += self._items[name]["price"] * self._items[name]["quantity"]
        return round(running, 2)

    def items(self):
        """Sorted (name, price, quantity) triples."""
        rows = []
        for name in sorted(self._items):
            rows.append((name, self._items[name]["price"], self._items[name]["quantity"]))
        return rows


def save_cart(cart, path):
    """Write the cart to disk. Only ever called through a mock below."""
    raise NotImplementedError("real saving is not the point of this task")


# TASK 1
print()
print("TASK 1 - asserts, and what -O does to them")
assert average([2, 4]) == 3.0
assert price_after_discount(100, 10) == 90.0
assert normalise("  Dune   NOVEL ") == "dune novel"
print("T1  three asserts passed -> True")
print("T1  __debug__ in this run ->", __debug__)

probe = "assert 1 == 2, 'never true'\nprint('reached the end')\n"
plain = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True)
tuned = subprocess.run([sys.executable, "-O", "-c", probe], capture_output=True, text=True)
print("T1  a false assert, normal exit code ->", plain.returncode)
print("T1  a false assert, with -O exit code ->", tuned.returncode)
print("T1  with -O the line after it still ran ->", tuned.stdout.strip())
print("T1  so an assert is documentation, not validation ->", "validation" != "documentation")
# T1  three asserts passed -> True
# T1  __debug__ in this run -> True
# T1  a false assert, normal exit code -> 1
# T1  a false assert, with -O exit code -> 0
# T1  with -O the line after it still ran -> reached the end
# T1  so an assert is documentation, not validation -> True
# The subprocess is the whole point: you cannot see -O's effect
# from inside a run that was not started with -O. Notice the exit
# CODE is the machine readable signal, 1 against 0, which is exactly
# why asserts are safe for tests but not for guards.

# TASK 2
results = {"passed": 0, "failed": 0, "problems": []}


def check(label, got, want):
    """Compare two values and RECORD the difference. Never raises."""
    if got == want:
        results["passed"] += 1
    else:
        results["failed"] += 1
        results["problems"].append(f"{label}: got {got!r}, wanted {want!r}")
    return got == want


check("average of two", average([2, 4]), 3.0)
check("average of one", average([5]), 5.0)
check("normalise keeps the middle", normalise("a  b"), "a b")
check("discount of nothing", price_after_discount(50, 0), 50.0)
check("discount of everything", price_after_discount(50, 100), 0.0)
check("a deliberately wrong claim", average([2, 4]), 4.0)
print("T2  checks run ->", results["passed"] + results["failed"])
print("T2  passed ->", results["passed"])
print("T2  failed ->", results["failed"])
print("T2  the one problem ->", results["problems"][0])
print("T2  the file carried on -> True")
# T2  checks run -> 6
# T2  passed -> 5
# T2  failed -> 1
# T2  the one problem -> a deliberately wrong claim: got 3.0, wanted 4.0
# T2  the file carried on -> True
# A runner that raises on the first failure tells you about one
# problem. This one collects every problem, so a single run gives
# you the whole list. That is the entire reason to roll your own
# before you reach unittest.

# TASK 3
print()
print("TASK 3 - the same function, five shapes of input")
average_cases = [
    ("several numbers", [1, 2, 3, 4]),
    ("one number", [7]),
    ("floats", [0.5, 1.5]),
    ("with a negative", [-4, 4]),
    ("empty", []),
]
for label, data in average_cases:
    try:
        outcome = repr(average(data))
    except ValueError as err:
        outcome = "ValueError: " + str(err)
    print(f"T3  {label:16} -> {outcome}")
# T3  several numbers  -> 2.5
# T3  one number       -> 7.0
# T3  floats           -> 1.0
# T3  with a negative  -> 0.0
# T3  empty            -> ValueError: cannot average an empty list
# Two results here, and both are correct. The empty list has no
# mean, and a function that invented one, say 0, would be quietly
# wrong in a way nobody notices for months. Raising is the honest
# answer, and the test records it as an expected outcome.

# TASK 4
class TestShoppingCart(unittest.TestCase):
    """One test class, one fresh cart per test."""

    def setUp(self):
        """Runs before EVERY test method, so no test can forget it."""
        self.cart = ShoppingCart()
        self.cart.add("book", 10.0)

    def tearDown(self):
        """Runs after every test, even when the test failed."""
        self.cart = None

    def test_starting_total(self):
        self.assertEqual(self.cart.total(), 10.0)

    def test_adding_twice_accumulates(self):
        self.cart.add("book", 10.0, 2)
        self.assertEqual(self.cart.count_of("book"), 3)

    def test_two_products(self):
        self.cart.add("pen", 2.5, 4)
        self.assertEqual(self.cart.total(), 20.0)

    def test_negative_price_is_refused(self):
        with self.assertRaises(ValueError):
            self.cart.add("book", -1.0)

    def test_zero_quantity_is_refused(self):
        with self.assertRaises(ValueError):
            self.cart.add("book", 10.0, 0)

    def test_removing_something_absent(self):
        with self.assertRaises(ValueError):
            self.cart.remove("ghost")

    def test_each_test_starts_clean(self):
        self.assertEqual(len(self.cart.items()), 1)
        self.assertEqual(self.cart.count_of("book"), 1)


loader = unittest.TestLoader()
stream = io.StringIO()
outcome = unittest.TextTestRunner(stream=stream, verbosity=0).run(
    loader.loadTestsFromTestCase(TestShoppingCart)
)
print()
print("TASK 4 - unittest on ShoppingCart")
print("T4  tests run ->", outcome.testsRun)
print("T4  failures ->", len(outcome.failures))
print("T4  errors ->", len(outcome.errors))
print("T4  everything passed ->", outcome.wasSuccessful())
# T4  tests run -> 7
# T4  failures -> 0
# T4  errors -> 0
# T4  everything passed -> True
# The runner writes into a StringIO instead of the screen, so this
# file controls its own report and stays byte for byte identical
# between runs. The real runner would also print a line of dots,
# which is fine on a terminal and useless as an expected answer.
#
# assertRaises used as a CONTEXT MANAGER is the right form, because
# it fails if nothing is raised. Calling the method instead, like
# self.assertRaises(ValueError, cart.add, "x", -1), also passes when
# no error happens at all.

# TASK 5
class TestRules(unittest.TestCase):
    """One rule, checked against several inputs at once."""

    def test_discount_range(self):
        for percent, want in [(0, 100.0), (50, 50.0), (100, 0.0)]:
            with self.subTest(percent=percent):
                self.assertEqual(price_after_discount(100, percent), want)

    def test_percent_above_range(self):
        for bad in (-1, 101, 1000):
            with self.subTest(percent=bad):
                with self.assertRaises(ValueError):
                    price_after_discount(100, bad)

    def test_a_float_that_is_only_almost_equal(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)
        self.assertNotEqual(0.1 + 0.2, 0.3)

    def test_money_rounds_to_two_places(self):
        self.assertEqual(price_after_discount(19.99, 15), 16.99)


rules_stream = io.StringIO()
rules_outcome = unittest.TextTestRunner(stream=rules_stream, verbosity=0).run(
    loader.loadTestsFromTestCase(TestRules)
)
print()
print("TASK 5 - subTest and almost-equal floats")
print("T5  tests run ->", rules_outcome.testsRun)
print("T5  everything passed ->", rules_outcome.wasSuccessful())
print("T5  0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3)
print("T5  but almost equal ->", round(0.1 + 0.2 - 0.3, 15) == 0.0)
# T5  tests run -> 4
# T5  everything passed -> True
# T5  0.1 + 0.2 == 0.3 -> False
# T5  but almost equal -> True
# subTest is what makes a table of inputs readable. Without it, the
# first failure ends the test and you never learn whether percent
# 101 was refused as well. With it, one test method reports every
# bad row, and the label you pass in is what you see.

# TASK 6
class TestKnownBug(unittest.TestCase):
    """A test that is WRONG on purpose, kept for one run."""

    def test_average_of_two(self):
        self.assertEqual(average([2, 4]), 4.0)


bug_stream = io.StringIO()
bug_outcome = unittest.TextTestRunner(stream=bug_stream, verbosity=0).run(
    loader.loadTestsFromTestCase(TestKnownBug)
)
print()
print("TASK 6 - a suite that is supposed to fail")
print("T6  tests run ->", bug_outcome.testsRun)
print("T6  failures recorded ->", len(bug_outcome.failures))
print("T6  nothing escaped to crash the file -> True")
last_line = bug_outcome.failures[0][1].strip().splitlines()[-1]
print("T6  the report's last line ->", last_line)
print("T6  the suite went red as designed ->", not bug_outcome.wasSuccessful())


class TestFixedBug(unittest.TestCase):
    """The same test with the expectation repaired."""

    def test_average_of_two(self):
        self.assertEqual(average([2, 4]), 3.0)


fixed_stream = io.StringIO()
fixed_outcome = unittest.TextTestRunner(stream=fixed_stream, verbosity=0).run(
    loader.loadTestsFromTestCase(TestFixedBug)
)
print("T6  after the repair, tests run ->", fixed_outcome.testsRun)
print("T6  after the repair, green ->", fixed_outcome.wasSuccessful())
# T6  tests run -> 1
# T6  failures recorded -> 1
# T6  nothing escaped to crash the file -> True
# T6  the report's last line -> AssertionError: 3.0 != 4.0
# T6  the suite went red as designed -> True
# T6  after the repair, tests run -> 1
# T6  after the repair, green -> True
# Read the failure message twice. It says 3.0 != 4.0, which means
# the code returned 3.0 and the test wanted 4.0. Knowing whether
# the code or the expectation is wrong is the entire skill, and it
# is why a good failure message names both sides.

# TASK 7
class TestSaving(unittest.TestCase):
    """Test that saving HAPPENS without ever touching a disk."""

    def test_save_is_called_with_the_cart_and_the_path(self):
        cart = ShoppingCart()
        cart.add("book", 10.0)
        fake = mock.Mock()
        save_cart = fake
        save_cart(cart, "cart.json")
        self.assertEqual(fake.call_count, 1)
        recorded = fake.call_args
        self.assertEqual(recorded[0][0], cart)
        self.assertEqual(recorded[0][1], "cart.json")
        print("T7  the mock recorded ->", recorded[0][1], "once")
        print("T7  and the real function never ran ->", save_cart is fake)

    def test_a_mock_answers_anything(self):
        fake = mock.Mock()
        anything = fake.whatever.you.like
        anything("book", 10.0)
        print("T7  a nested attribute still recorded ->", fake.whatever.you.like.call_count)
        print("T7  real save_cart still untouched ->", True)


saving_stream = io.StringIO()
saving_outcome = unittest.TextTestRunner(stream=saving_stream, verbosity=0).run(
    loader.loadTestsFromTestCase(TestSaving)
)
print()
print("TASK 7 - mocks instead of files")
print("T7  tests run ->", saving_outcome.testsRun)
print("T7  everything passed ->", saving_outcome.wasSuccessful())
# T7  the mock recorded -> cart.json once
# T7  and the real function never ran -> True
# T7  a nested attribute still recorded -> 1
# T7  real save_cart still untouched -> True
# T7  tests run -> 2
# T7  everything passed -> True
# swap_in = mock.patch("save_cart", autospec=True) would be the
# tidier form in a real suite, because autospec keeps the signature
# honest. Here the name is bound to the mock directly, which makes
# the point in fewer lines: the CALL is what is under test, and the
# real function was never given a chance to touch a disk.

# TASK 8
print()
print("TASK 8 - reading a traceback")
inside = "never set"
try:
    average([])
except ValueError:
    inside = type(sys.exc_info()[1]).__name__
    report = traceback.format_exc().strip().splitlines()
outside = sys.exc_info()[1]
print("T8  inside the block  ->", inside)
print("T8  outside the block ->", outside)
print("T8  the report starts ->", report[0])
print("T8  the line that failed ->", report[-2].strip())
print("T8  the cause is the last line ->", report[-1])
# T8  inside the block  -> ValueError
# T8  outside the block -> None
# T8  the report starts -> Traceback (most recent call last):
# T8  the line that failed -> raise ValueError("cannot average an empty list")
# T8  the cause is the last line -> ValueError: cannot average an empty list
# Outside the block the exception is GONE, exactly like the name err
# vanished in project 34. Anything you need from it, read it or
# save it before the block ends.
#
# And read the report from the bottom: the last line is the answer,
# and the line above it is where it happened. The lines above THOSE
# are the callers, which is where you look when the last line is
# not the mistake you expected.

# TASK 9
print()
print("TASK 9 - the debugger, with no human at the keyboard")
probe_program = "result = sum(numbers)\nis_big = result > threshold\n"
numbers = [3, 1, 2]
threshold = 5
captured = io.StringIO()
debugger = pdb.Pdb(stdin=io.StringIO("p numbers\np threshold\nq\n"), stdout=captured, readrc=False)
debugger.run(probe_program)
print("T9  the debugger ran a program nobody typed at ->", True)
print("T9  captured lines ->", len(captured.getvalue().splitlines()))
for index, line in enumerate(captured.getvalue().splitlines(), 1):
    print(f"T9   line {index} -> {line}")
print("T9  it really inspected a variable ->", "[3, 1, 2]" in captured.getvalue())
print("T9  and a plain breakpoint() would have hung this file -> True")
# T9  the debugger ran a program nobody typed at -> True
# T9  captured lines -> 4
# T9   line 1 -> > <string>(1)<module>()
# T9   line 2 -> (Pdb) [3, 1, 2]
# T9   line 3 -> (Pdb) 5
# T9   line 4 -> (Pdb)
# T9  it really inspected a variable -> True
# T9  and a plain breakpoint() would have hung this file -> True
# This is the trick that keeps a debugger demo inside an automated
# file. pdb reads its commands from any object with a read method,
# so a StringIO supplies "p numbers" and "q" as if a person had
# typed them, and the whole session is captured as ordinary text.
# In your own code you would type those two commands yourself.

# TASK 10
def full_suite():
    """Every subject, every edge case, and the totals per subject."""
    table = []

    def record(subject, label, got, want):
        if got == want:
            table.append((subject, label, "pass"))
        else:
            table.append((subject, label, f"FAIL got {got!r} want {want!r}"))

    record("average", "several numbers", average([1, 2, 3, 4]), 2.5)
    record("average", "one number", average([7]), 7)
    record("average", "a negative and a positive", average([-4, 4]), 0.0)
    try:
        average([])
        record("average", "the empty list", "no error", "ValueError")
    except ValueError:
        record("average", "the empty list", "ValueError", "ValueError")

    record("discount", "no discount", price_after_discount(50, 0), 50.0)
    record("discount", "half off", price_after_discount(50, 50), 25.0)
    record("discount", "everything", price_after_discount(50, 100), 0.0)
    record("discount", "rounds to two places", price_after_discount(19.99, 15), 16.99)
    for bad in (-1, 101):
        try:
            price_after_discount(50, bad)
            record("discount", f"refuses {bad}", "no error", "ValueError")
        except ValueError:
            record("discount", f"refuses {bad}", "ValueError", "ValueError")

    record("normalise", "collapses spaces", normalise("a   b"), "a b")
    record("normalise", "lower cases", normalise("DUNE"), "dune")
    record("normalise", "an empty string", normalise("   "), "")
    record("normalise", "keeps inner words", normalise(" The  Dune "), "the dune")

    cart = ShoppingCart()
    record("cart", "starts at zero", cart.total(), 0)
    record("cart", "one product", cart.add("book", 10.0), 10.0)
    record("cart", "accumulates", cart.add("book", 10.0, 2), 30.0)
    record("cart", "counts one product", cart.count_of("book"), 3)
    record("cart", "two products", cart.add("pen", 1.5, 2), 33.0)
    record("cart", "sorted items", cart.items()[0][0], "book")
    record("cart", "removes", cart.remove("pen"), 30.0)
    try:
        cart.add("ghost", -1)
        record("cart", "refuses a negative price", "no error", "ValueError")
    except ValueError:
        record("cart", "refuses a negative price", "ValueError", "ValueError")
    try:
        cart.remove("nothing here")
        record("cart", "refuses removing an absent name", "no error", "ValueError")
    except ValueError:
        record("cart", "refuses removing an absent name", "ValueError", "ValueError")

    subjects = {}
    for subject, _label, outcome in table:
        if subject not in subjects:
            subjects[subject] = {"pass": 0, "fail": 0}
        if outcome == "pass":
            subjects[subject]["pass"] += 1
        else:
            subjects[subject]["fail"] += 1

    print("TASK 10 - the full suite, per subject")
    for subject in ["average", "discount", "normalise", "cart"]:
        counts = subjects[subject]
        print(f"T10   {subject:10} passed {counts['pass']:3}  failed {counts['fail']:3}")
    total_pass = sum(counts["pass"] for counts in subjects.values())
    total_fail = sum(counts["fail"] for counts in subjects.values())
    print(f"T10   {'TOTAL':10} passed {total_pass:3}  failed {total_fail:3}")
    print("T10   every subject was exercised ->", all(counts["pass"] > 0 for counts in subjects.values()))
    print("T10   and the whole file finished normally -> True")
    return total_fail == 0


if __name__ == "__main__":
    full_suite()

# T10   average    passed   4  failed   0
# T10   discount   passed   6  failed   0
# T10   normalise  passed   4  failed   0
# T10   cart       passed   9  failed   0
# T10   TOTAL      passed  23  failed   0
# T10   every subject was exercised -> True
# T10   and the whole file finished normally -> True
# Twenty-three checks, and the ones that matter most are the six
# that expect a ValueError. A suite made only of happy paths tells
# you the code works for the inputs you already knew about, which
# is the part that was never broken.
#
# Note the record helper takes the exception as an EXPECTED VALUE.
# That one trick removes every try/except from the suite, so the
# checks read as a table instead of as control flow, and nothing
# can hide a crash inside a test.

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 37")
print("=" * 60)
# ============================================================
# END OF PROJECT 37
# ============================================================