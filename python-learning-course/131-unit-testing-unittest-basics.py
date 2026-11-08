# -----------------------------------------------------------------
# Lesson 131: unit testing -- unittest basics
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : unit tests, expected vs actual results,
#              assertions, test cases and useful failure
#              messages with Python's unittest module
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript is noisy, but its clear thread is unit
# testing: check a small unit of behavior, compare the
# expected result with the actual result, and report
# whether it matches.
#
#     UNIT TESTS [00:50] -- many tools test one small unit
#     and report whether its result matches expectations
#     EXAMPLE [03:06] -- 3 * 8 should be 24; 5 * 10
#     should be 50
#     ASSERTIONS [03:36-05:43] -- a test passes when the
#     actual result equals the expected result; a wrong
#     expectation (250 instead of 240) is a failure
#     COMPARISONS [07:55-12:54] -- compare values such as
#     100 > 97 and 100 > 101; the assertion message helps
#     explain what was expected
#
# This lesson uses the standard-library unittest module,
# not pytest. It does not repeat project 40's pytest and
# coverage lesson: here we focus on writing small tests
# and reading expected/actual results. Tests are run in a
# sandbox and their time/path-specific report lines are
# normalized before printing.

import contextlib
import io
import os
import shutil
import tempfile
import textwrap
import unittest

# ============================================================
# [1] What a unit test checks
# ============================================================
# A unit test checks one small behavior against a known
# expectation. It answers: did the unit do what we meant?

print("  unit test: check one behavior against an expectation")
print("  result: expected value compared with actual value")
#   unit test: check one behavior against an expectation
#   result: expected value compared with actual value

# ============================================================
# [2] The function under test
# ============================================================
# Keep the tested unit small and easy to reason about.

def multiply(first, second):
    """Multiply two numbers."""
    return first * second

print(f"  multiply(3, 8): {multiply(3, 8)}")
print(f"  expected result: {24}")
print(f"  actual matches expected: {multiply(3, 8) == 24}")
#   multiply(3, 8): 24
#   expected result: 24
#   actual matches expected: True

# ============================================================
# [3] Use unittest.TestCase
# ============================================================
# TestCase groups test methods; assertEqual checks the
# expected value against the actual value.

class MultiplyTests(unittest.TestCase):
    """Tests for the multiplication unit."""

    def test_three_times_eight(self):
        self.assertEqual(multiply(3, 8), 24)

    def test_five_times_ten(self):
        self.assertEqual(multiply(5, 10), 50)

print(f"  TestCase available: {issubclass(MultiplyTests, unittest.TestCase)}")
print(f"  test methods: {len([name for name in dir(MultiplyTests) if name.startswith('test_')])}")
#   TestCase available: True
#   test methods: 2

# ============================================================
# [4] Run the tests without a command-line runner
# ============================================================
# unittest.TextTestRunner writes a report to a stream.
# Capture it so this lesson can print stable facts only.

def run_suite(test_case):
    """Run a TestCase and return its result and captured report."""
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
    report = io.StringIO()
    result = unittest.TextTestRunner(
        stream=report, verbosity=2
    ).run(suite)
    return result, report.getvalue()

passing_result, passing_report = run_suite(MultiplyTests)
print(f"  tests run: {passing_result.testsRun}")
print(f"  failures: {len(passing_result.failures)}")
print(f"  errors: {len(passing_result.errors)}")
print(f"  suite successful: {passing_result.wasSuccessful()}")
#   tests run: 2
#   failures: 0
#   errors: 0
#   suite successful: True

# The full runner report is captured; summary facts are
# stable and do not depend on terminal width.

# ============================================================
# [5] Expected versus actual
# ============================================================
# An assertion compares the two sides: actual first,
# expected second. unittest prints both if they disagree.

expected = 24
actual = multiply(3, 8)
print(f"  expected: {expected}")
print(f"  actual: {actual}")
print(f"  equal: {actual == expected}")
#   expected: 24
#   actual: 24
#   equal: True

# ============================================================
# [6] A wrong expectation produces a failing test
# ============================================================
# The transcript describes an expected 250 where the
# function correctly returns 240: the test should fail.

class WrongExpectationTests(unittest.TestCase):
    """Deliberately incorrect expectation for demonstration."""

    def test_wrong_expected_value(self):
        self.assertEqual(multiply(30, 8), 250)

wrong_result, wrong_report = run_suite(WrongExpectationTests)
print(f"  deliberately wrong test fails: {len(wrong_result.failures) == 1}")
print(f"  actual value is reported: {'240' in wrong_report}")
print(f"  expected value is reported: {'250' in wrong_report}")
#   deliberately wrong test fails: True
#   actual value is reported: True
#   expected value is reported: True

# A red test is useful information: it tells us the
# expectation or the code needs attention. This one is
# intentionally wrong, so the overall lesson still exits 0.

# ============================================================
# [7] Fix the expectation
# ============================================================
# Correct the expected result to 240, then the test is
# green. Same function, corrected requirement.

class CorrectExpectationTests(unittest.TestCase):
    """The corrected multiplication expectation."""

    def test_correct_expected_value(self):
        self.assertEqual(multiply(30, 8), 240)

correct_result, _ = run_suite(CorrectExpectationTests)
print(f"  corrected test passes: {correct_result.wasSuccessful()}")
print(f"  expected value: {240}")
#   corrected test passes: True
#   expected value: 240

# ============================================================
# [8] Comparison assertions
# ============================================================
# The transcript checks whether one number is greater
# than another, both when true and when false.

class ComparisonTests(unittest.TestCase):
    """Examples of comparison assertions."""

    def test_one_hundred_is_above_ninety_seven(self):
        self.assertGreater(100, 97)

    def test_one_hundred_is_not_above_one_hundred_one(self):
        self.assertFalse(100 > 101)

comparison_result, _ = run_suite(ComparisonTests)
print(f"  comparisons run: {comparison_result.testsRun}")
print(f"  comparisons pass: {comparison_result.wasSuccessful()}")
print(f"  100 > 97: {100 > 97}")
print(f"  100 > 101: {100 > 101}")
#   comparisons run: 2
#   comparisons pass: True
#   100 > 97: True
#   100 > 101: False

# ============================================================
# [9] More useful assertion messages
# ============================================================
# A custom message explains the requirement when a test
# fails; demonstrate the same failure safely and capture it.

class MessageTests(unittest.TestCase):
    """Show that assertion messages describe intent."""

    def test_custom_message(self):
        self.assertGreater(80, 100, "score must exceed 100")

message_result, message_report = run_suite(MessageTests)
print(f"  custom-message test fails: {len(message_result.failures) == 1}")
print(f"  message explains the rule: {'score must exceed 100' in message_report}")
#   custom-message test fails: True
#   message explains the rule: True

# ============================================================
# [10] A list of test cases
# ============================================================
# Several input/expected pairs can exercise one unit.

cases = [
    (3, 8, 24),
    (5, 10, 50),
    (30, 8, 240),
    (0, 99, 0),
]

class MultiplyCaseTableTests(unittest.TestCase):
    """Check a small table of multiplication examples."""

    def test_all_cases(self):
        for first, second, expected_value in cases:
            with self.subTest(first=first, second=second):
                self.assertEqual(multiply(first, second), expected_value)

table_result, _ = run_suite(MultiplyCaseTableTests)
print(f"  table cases: {len(cases)}")
print(f"  table suite passes: {table_result.wasSuccessful()}")
#   table cases: 4
#   table suite passes: True

# ============================================================
# [11] A failing test does not change the function
# ============================================================
# The wrong expectation failed because it disagreed with
# the result; multiply itself remains correct.

print(f"  multiply(30, 8) after wrong test: {multiply(30, 8)}")
print(f"  original function unchanged: {multiply(3, 8) == 24}")
#   multiply(30, 8) after wrong test: 240
#   original function unchanged: True

# ============================================================
# [12] Run tests from a separate sandbox module
# ============================================================
# A small test module makes the test/code separation
# explicit. This mini-runner filters volatile path lines.

WORK_DIR = tempfile.mkdtemp(prefix="py131_")
module_path = os.path.join(WORK_DIR, "lesson_math.py")
test_path = os.path.join(WORK_DIR, "test_lesson_math.py")

with open(module_path, "w", encoding="utf-8", newline="\n") as module_file:
    module_file.write(textwrap.dedent('''\
        def multiply(first, second):
            return first * second
    '''))
with open(test_path, "w", encoding="utf-8", newline="\n") as test_file:
    test_file.write(textwrap.dedent('''\
        import unittest
        from lesson_math import multiply

        class FileTests(unittest.TestCase):
            def test_product(self):
                self.assertEqual(multiply(3, 8), 24)
    '''))

# Load tests in-process from the sandbox, without printing
# runner paths or its timing-dependent summary line.
import sys
sys.path.insert(0, WORK_DIR)
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_lesson_math", test_path)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
    file_result, _ = run_suite(test_module.FileTests)
finally:
    sys.path.remove(WORK_DIR)
    sys.modules.pop("test_lesson_math", None)
    sys.modules.pop("lesson_math", None)

print(f"  separate test module passes: {file_result.wasSuccessful()}")
print(f"  test file exists: {os.path.isfile(test_path)}")
#   separate test module passes: True
#   test file exists: True

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# Unit testing in this lesson:
#
#   1. UNIT -- test one small behavior against an expected
#      result, separately from the rest of the program
#   2. unittest.TestCase groups named test methods
#   3. assertEqual(actual, expected) checks equality
#   4. 3 * 8 gives 24; 5 * 10 gives 50
#   5. A wrong expected value (250 instead of 240) gives
#      a failure that reports both values
#   6. Fix the expectation and the test passes
#   7. assertGreater checks 100 > 97; a false condition
#      (100 > 101) is tested as False
#   8. Custom messages explain the intended rule on failure
#   9. A table/subTest covers multiple input pairs
#  10. A deliberately failing example is captured, so the
#      lesson itself still exits successfully
#  11. The standard-library unittest is distinct from
#      pytest and its coverage report (project 40)
#  12. Sandbox test/code files are removed (True)
#
# Tests do not prove that a program is perfect. They give
# you repeatable evidence that selected expectations hold.
