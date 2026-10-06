# ============================================================
# Project 40 - pytest and line coverage
# ============================================================
# What this lesson teaches:
#   pytest.main()      run the whole runner inside your own process
#   pytest.raises      the exception IS the assertion
#   parametrize        four cases, one function
#   fixtures + tmp_path  setup and cleanup you did not write
#   the exit code      0 green, 1 red, 5 nothing to run, 4 bad flag
#   ast + trace        what could run, and what did run
#   and the blind spot 100% covered, and the function still breaks
#
# The measurement uses only the standard library (ast + trace), so this
# file runs anywhere. coverage.py is the industry tool for the same
# job; if you install it, `python -m coverage run -m pytest` prints the
# same two lists this lesson computes by hand.
#
# Run it:  python project-40-pytest-and-coverage.py
# ============================================================

import ast
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile
import textwrap
import trace

try:
    import pytest
except ImportError:
    raise SystemExit("project 40 needs pytest: python -m pip install pytest")

FOLDER = tempfile.mkdtemp(prefix="project40_")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


def write(name, source):
    """Every scenario gets its own file name. See TASK 8 for why."""
    path = os.path.join(FOLDER, name)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(textwrap.dedent(source).lstrip("\n"))
    return path


def tidy(text):
    """Strip the two things that change from run to run: paths and times."""
    text = text.replace(FOLDER + os.sep, "").replace(FOLDER, "")
    return re.sub(r" in \d+\.\d+s", "", text)


def run_pytest(*args):
    """Run pytest in THIS process, quietly, from inside our own folder.

    pytest.main() returns an exit code instead of exiting, which is the
    only reason a lesson file can print its own test results.
    """
    argv = ["-q", "--no-header", "-p", "no:cacheprovider"] + list(args)
    buffer = io.StringIO()
    here = os.getcwd()
    os.chdir(FOLDER)
    try:
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            code = pytest.main(argv)
    finally:
        os.chdir(here)
    return int(code), tidy(buffer.getvalue())


def last_line(output):
    lines = [line for line in output.splitlines() if line.strip()]
    return lines[-1] if lines else ""


def counts(output):
    """pytest's own numbers, read back out of its summary line."""
    found = {}
    for value, word in re.findall(
            r"(\d+) (passed|failed|deselected|errors|warnings|skipped)", output):
        found[word.rstrip("s")] = int(value)
    return found


def failure(output):
    """pytest's one-line explanation, with no path attached to it."""
    for line in output.splitlines():
        if line.startswith("E   "):
            return line[4:].strip()
    return ""


def collect(path):
    """--collect-only: the ids pytest would run, grouped by class."""
    _, output = run_pytest("--collect-only", os.path.basename(path))
    ids, classes = [], {}
    for line in output.splitlines():
        if "::" in line:
            parts = line.split("::")
            ids.append(parts[-1])
            if len(parts) == 3:
                classes.setdefault(parts[1], []).append(parts[-1])
    return ids, classes


def collected_count(output):
    match = re.search(r"(\d+) tests? collected", output)
    return int(match.group(1)) if match else 0


def folder_contents():
    """Our scratch folder, minus the cache Python keeps for itself."""
    return sorted(name for name in os.listdir(FOLDER) if name != "__pycache__")


# ------------------------------------------------------------
# The code we are going to measure
# ------------------------------------------------------------

UNDER_TEST = textwrap.dedent('''
    def average(nums):
        total = 0
        for n in nums:
            total += n
        return total / len(nums)


    def price(qty, unit, member):
        total = qty * unit
        if member:
            total = total * 0.9
        if qty >= 10:
            total = total - 5
        return total
''').strip("\n")

UNDER_TEST_PATH = os.path.join(FOLDER, "under_test.py")


def executable_lines(source):
    """What ast says could run: every statement, taken branch or not."""
    tree = ast.parse(source)
    return sorted({node.lineno for node in ast.walk(tree)
                   if isinstance(node, ast.stmt)})


def lines_of(tree, name):
    node = next(node for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef) and node.name == name)
    return list(range(node.lineno, node.end_lineno + 1))


def measure(path, source, calls):
    """What trace says did run, by actually running it.

    trace looks at frame.f_globals['__file__'], not at the code object,
    which is why the scope carries __file__ and the compile() uses the
    same path. Without that, the counts come back empty and quiet.
    """
    counter = trace.Trace(count=1, trace=0)
    scope = {"__name__": "under_test", "__file__": path}
    counter.runctx(compile(source, path, "exec"), scope, scope)
    for name, arguments in calls:
        counter.runfunc(scope[name], *arguments)
    ran = sorted({line for (filename, line) in counter.results().counts
                  if filename == path})
    return ran, scope


def percent(hits, wanted):
    return round(100 * len(hits) / len(wanted))


# ============================================================
# PART A - THE QUESTIONS
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print("Q1  pytest.main() runs the whole runner inside your own process")
print("Q2  so your process, your exit code, your captured output")
print("Q3  a fixture is setup and teardown handed to you, already cleaned up")
print("Q4  parametrize writes the four tests you did not want to type")
print("Q5  pytest tells the truth in exactly one place: the number it returns")
print("Q6  coverage counts lines that ran, and never once counts a path")
print("Q7  an uncovered line is a test you have not written yet")
print("Q8  and one hundred percent is still compatible with a broken function")
print()

print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  pytest.main([...]) returns an exit code instead of exiting")
print("Q1  which is why this file can print its own results at all")
print("Q2  and why one process can run a dozen suites in a row")
print("Q3  tmp_path is a folder pytest made and takes back when done")
print("Q4  four cases, one function, and every failure names its own id")
print("Q5  0 green, 1 red, 5 nothing to run, 4 for a flag it never heard")
print("Q6  ast says what could run, trace says what did run")
print("Q7  line 11 and line 13 were not bugs, they were homework")
print("Q8  every line of average() ran and average([]) still died")
print("Q8  because a line is not an input, and a number is not a test")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - pytest owns four exit codes")
print("T1  a suite that passes exits -> 0")
print("T1  and its last line -> 2 passed")
print("T1  a suite with a failure exits -> 1")
print("T1  and its last line -> 1 failed")
print("T1  a file holding no tests exits -> 5")
print("T1  and its last line -> no tests ran")
print("T1  an unknown flag is pytest's own mistake, exit -> 4")
print("T1  so 0, 1 and 5 are yours and 4 is usage -> True")
print()

print("TASK 2 - pytest.raises replaces the hand-made helper")
print("T2  expecting ValueError and getting it -> 1 passed")
print("T2  expecting KeyError while ValueError arrives -> 1 failed")
print("T2  and pytest names the exception it did get -> ValueError: something else")
print("T2  match= against words that differ -> 1 failed")
print("T2  and it says why -> AssertionError: Regex pattern did not match.")
print("T2  so the assertion is the exception and its words -> True")
print()

print("TASK 3 - one function, many cases")
print("T3  one function collected as this many cases -> 5")
print("T3  the ids the cases were given -> ['test_int[1-1]', 'test_int[2-2]', "
      "'test_int[-3--3]', 'test_int[7-7]']")
print("T3  and the case without parameters -> test_plain")
print("T3  a case that fails is named by its own id -> test_int[9-0]")
print("T3  so four cases cost one function, not four -> True")
print()

print("TASK 4 - a fixture and the folder pytest lends you")
print("T4  one fixture built the file, four tests read it -> 4 passed")
print("T4  so the folder it lent us really existed -> True")
print("T4  and no test wrote a byte outside it -> True")
print("T4  our own folder gained nothing from the run -> True")
print()

print("TASK 5 - -k narrows, -x stops")
print("T5  -k keeps one case out of five -> 1 passed, 4 deselected")
print("T5  -x stops at the first failure -> 1 failed, 1 passed")
print("T5  and it still exits -> 1")
print("T5  so -k narrows the run and -x shortens it -> True")
print()

print("TASK 6 - ast finds what could run")
print("T6  the file holds this many executable lines -> 12")
print("T6  their line numbers -> [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14]")
print("T6  lines belonging to average() -> 5")
print("T6  and to price() -> 7")
print("T6  an if-body nobody took still counts -> True")
print("T6  because ast reads what could run, never what did -> True")
print()

print("TASK 7 - trace finds what did run")
print("T7  the lines that actually ran -> [1, 2, 3, 4, 5, 8, 9, 10, 12, 14]")
print("T7  that is this many of the twelve -> 10")
print("T7  so the file sits at -> 83%")
print("T7  the lines still missing -> [11, 13]")
print("T7  they are the bodies of the two ifs nobody took -> True")
print("T7  so an uncovered line is a test you have not written -> True")
print()

print("TASK 8 - one hundred percent, and it still breaks")
print("T8  average() on a happy input -> 5 of 5 lines, 100%")
print("T8  average([]) -> ZeroDivisionError: division by zero")
print("T8  and the crashing line was already marked covered -> True")
print("T8  so 100% said every line ran, never every input -> True")
print("T8  a percentage is a spotlight, not a scoreboard -> True")
print()

print("TASK 9 - the suite")
print("T9   TestAverage    collected   3")
print("T9   TestPrice      collected   5")
print("T9   TestRaises     collected   4")
print("T9   TestFixtures   collected   4")
print("T9   TOTAL      passed  16  failed   0")
print("T9   errors -> 0")
print()

print("TASK 10 - the loop, closed")
print("T10   the clean suite exits -> 0")
print("T10   the tests it ran -> 16")
print("T10   add the one test the percentage could not see -> 1 failed, 16 passed")
print("T10   and the exit code flips to -> 1")
print("T10   across these two runs the only non-zero -> [1]")
print("T10   and the folder this file lives in is untouched -> True")
print()

print("=" * 60)


# ============================================================
# PART C - THE SOLUTION
# ============================================================

print()
print("=" * 60)
print("PART C - the solution")
print("=" * 60)

# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print()
print("-" * 60)
print("TASK 1 - pytest owns four exit codes")
print("-" * 60)
green = write("test_01_pass.py", '''
    def test_one():
        assert 1 + 1 == 2


    def test_two():
        assert "a".upper() == "A"
''')
red = write("test_02_fail.py", '''
    def test_two():
        assert 2 + 2 == 5
''')
empty = write("test_03_none.py", "")

code_green, out_green = run_pytest(os.path.basename(green))
code_red, out_red = run_pytest(os.path.basename(red))
code_empty, out_empty = run_pytest(os.path.basename(empty))
code_usage, out_usage = run_pytest("--this-flag-was-never-real")

check("a green suite exits 0", code_green == 0)
check("a red suite exits 1", code_red == 1)
check("a file with no tests exits 5", code_empty == 5)
check("a flag pytest never heard exits 4", code_usage == 4)
check("the green summary counts two", counts(out_green).get("passed") == 2)
check("the red summary counts one", counts(out_red).get("failed") == 1)
check("nothing leaked to stderr", out_usage.count("Traceback") == 0)

print("T1  a suite that passes exits ->", code_green)
print("T1  and its last line ->", last_line(out_green))
print("T1  a suite with a failure exits ->", code_red)
print("T1  and its last line ->", last_line(out_red))
print("T1  a file holding no tests exits ->", code_empty)
print("T1  and its last line ->", last_line(out_empty))
print("T1  an unknown flag is pytest's own mistake, exit ->", code_usage)
print("T1  so 0, 1 and 5 are yours and 4 is usage ->",
      check("all four exit codes were seen",
            [code_green, code_red, code_empty, code_usage] == [0, 1, 5, 4]))
print()

# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - pytest.raises replaces the hand-made helper")
print("-" * 60)
right = write("test_04_raise.py", '''
    import pytest


    def test_int_refuses_text():
        with pytest.raises(ValueError):
            int("x")
''')
wrong = write("test_05_wrong.py", '''
    import pytest


    def test_it_thinks_keyerror():
        with pytest.raises(KeyError):
            raise ValueError("something else")
''')
words = write("test_06_match.py", '''
    import pytest


    def test_the_words_must_match():
        with pytest.raises(ValueError, match="declined"):
            raise ValueError("accepted")
''')

code_right, out_right = run_pytest(os.path.basename(right))
code_wrong, out_wrong = run_pytest("--tb=line", os.path.basename(wrong))
code_words, out_words = run_pytest("--tb=line", os.path.basename(words))

check("the exception it expected arrives", code_right == 0)
check("the exception it did not expect fails", code_wrong == 1)
check("a wrong message fails too", code_words == 1)
check("pytest names the exception it got",
      failure(out_wrong) == "ValueError: something else")
check("pytest explains a mismatched message",
      failure(out_words) == "AssertionError: Regex pattern did not match.")

print("T2  expecting ValueError and getting it ->", last_line(out_right))
print("T2  expecting KeyError while ValueError arrives ->",
      last_line(out_wrong))
print("T2  and pytest names the exception it did get ->", failure(out_wrong))
print("T2  match= against words that differ ->", last_line(out_words))
print("T2  and it says why ->", failure(out_words))
print("T2  so the assertion is the exception and its words ->",
      check("both forms of raises did their job",
            code_right == 0 and code_wrong == 1 and code_words == 1))
print()

# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - one function, many cases")
print("-" * 60)
param = write("test_07_param.py", '''
    import pytest


    @pytest.mark.parametrize("value,expected", [
        ("1", 1),
        ("2", 2),
        ("-3", -3),
        ("7", 7),
    ])
    def test_int(value, expected):
        assert int(value) == expected


    def test_plain():
        assert 1 == 1
''')
broken = write("test_08_param_fail.py", '''
    import pytest


    @pytest.mark.parametrize("value,expected", [
        ("1", 1),
        ("2", 2),
        ("-3", -3),
        ("7", 7),
        ("9", 0),
    ])
    def test_int(value, expected):
        assert int(value) == expected
''')

param_ids, _ = collect(param)
code_broken, out_broken = run_pytest("--tb=no", os.path.basename(broken))
named = ""
for line in out_broken.splitlines():
    match = re.search(r"FAILED \S+::(\S+)", line)
    if match:
        named = match.group(1)
        break

check("one function collected five cases", len(param_ids) == 5)
check("the ids name every case", param_ids[:4] == [
    "test_int[1-1]", "test_int[2-2]", "test_int[-3--3]", "test_int[7-7]"])
check("the last case has no parameters", param_ids[4] == "test_plain")
check("a failing case is named by its id", named == "test_int[9-0]")

print("T3  one function collected as this many cases ->", len(param_ids))
print("T3  the ids the cases were given ->", param_ids[:4])
print("T3  and the case without parameters ->", param_ids[4])
print("T3  a case that fails is named by its own id ->", named)
print("T3  so four cases cost one function, not four ->",
      check("the four cases were one function",
            len([i for i in param_ids if i.startswith("test_int")]) == 4))
print()

# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - a fixture and the folder pytest lends you")
print("-" * 60)
fixture = write("test_09_fixture.py", '''
    import json
    import os

    import pytest


    @pytest.fixture
    def shop(tmp_path):
        path = tmp_path / "shop.json"
        path.write_text(json.dumps({"books": 2}), encoding="utf-8")
        return path


    def test_the_fixture_handed_us_a_file(shop):
        assert shop.exists()


    def test_the_content_survives_a_round_trip(shop):
        assert json.loads(shop.read_text(encoding="utf-8")) == {"books": 2}


    def test_the_folder_holds_only_what_we_put_there(shop):
        assert sorted(os.listdir(shop.parent)) == ["shop.json"]


    def test_the_name_is_ours(shop):
        assert shop.name == "shop.json"
''')

before = folder_contents()
code_fixture, out_fixture = run_pytest(os.path.basename(fixture))
after = folder_contents()

check("the fixture suite is green", code_fixture == 0)
check("four tests read one fixture", counts(out_fixture).get("passed") == 4)
check("our own folder gained nothing", before == after)

print("T4  one fixture built the file, four tests read it ->",
      last_line(out_fixture))
print("T4  so the folder it lent us really existed ->",
      check("the four tests really ran", code_fixture == 0))
print("T4  and no test wrote a byte outside it ->", before == after)
print("T4  our own folder gained nothing from the run ->",
      check("pytest wrote nothing here either", before == after))
print()

# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - -k narrows, -x stops")
print("-" * 60)
stopping = write("test_10_stop.py", '''
    def test_one():
        assert 1 == 1


    def test_two():
        assert 1 == 2
''')

code_k, out_k = run_pytest(os.path.basename(param), "-k", "plain")
code_x, out_x = run_pytest(os.path.basename(stopping), "-x")

check("-k keeps only the case it matched", counts(out_k).get("passed") == 1)
check("-k deselected the other four", counts(out_k).get("deselected") == 4)
check("-x stops after the failure", code_x == 1)
check("-x still reports what it did run", counts(out_x).get("passed") == 1)

print("T5  -k keeps one case out of five ->", last_line(out_k))
print("T5  -x stops at the first failure ->", last_line(out_x))
print("T5  and it still exits ->", code_x)
print("T5  so -k narrows the run and -x shortens it ->",
      check("both switches changed the run",
            counts(out_k).get("deselected") == 4 and code_x == 1))
print()

# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - ast finds what could run")
print("-" * 60)
with open(UNDER_TEST_PATH, "w", encoding="utf-8", newline="\n") as handle:
    handle.write(UNDER_TEST + "\n")

tree = ast.parse(UNDER_TEST)
could = executable_lines(UNDER_TEST)
average_lines = lines_of(tree, "average")
price_lines = lines_of(tree, "price")

check("ast finds twelve executable lines", len(could) == 12)
check("average is five lines", len(average_lines) == 5)
check("price is seven lines", len(price_lines) == 7)
check("the untaken if-body is still counted", 11 in could and 13 in could)

print("T6  the file holds this many executable lines ->", len(could))
print("T6  their line numbers ->", could)
print("T6  lines belonging to average() ->", len(average_lines))
print("T6  and to price() ->", len(price_lines))
print("T6  an if-body nobody took still counts ->", 11 in could and 13 in could)
print("T6  because ast reads what could run, never what did ->",
      check("ast never looked at a running program", len(could) == 12))
print()

# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - trace finds what did run")
print("-" * 60)
ran, scope = measure(UNDER_TEST_PATH, UNDER_TEST, [
    ("average", ([2, 4],)),
    ("price", (3, 10, False)),
])
hits = [line for line in could if line in ran]
missing = [line for line in could if line not in ran]

check("ten of twelve lines ran", len(hits) == 10)
check("the file measures 83%", percent(hits, could) == 83)
check("exactly two lines are missing", missing == [11, 13])
check("both missing lines are if-bodies",
      missing == [11, 13] and UNDER_TEST.splitlines()[10].strip()
      == "total = total * 0.9")

print("T7  the lines that actually ran ->", hits)
print("T7  that is this many of the twelve ->", len(hits))
print("T7  so the file sits at ->", "{0}%".format(percent(hits, could)))
print("T7  the lines still missing ->", missing)
print("T7  they are the bodies of the two ifs nobody took ->",
      missing == [11, 13])
print("T7  so an uncovered line is a test you have not written ->",
      check("the gap is a homework list, not a bug", missing == [11, 13]))
print()

# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - one hundred percent, and it still breaks")
print("-" * 60)
happy_runs, happy_scope = measure(UNDER_TEST_PATH, UNDER_TEST, [
    ("average", ([2, 4],)),
])
happy_hits = [line for line in average_lines if line in happy_runs]

crash = ""
try:
    happy_scope["average"]([])
except ZeroDivisionError as error:
    crash = "{0}: {1}".format(type(error).__name__, error)

check("average() alone measures 100%", percent(happy_hits, average_lines) == 100)
check("the crashing line was already counted", 5 in happy_hits)
check("averaging nothing really does crash", crash.startswith("ZeroDivisionError"))

print("T8  average() on a happy input -> {0} of {1} lines, {2}%".format(
    len(happy_hits), len(average_lines), percent(happy_hits, average_lines)))
print("T8  average([]) ->", crash)
print("T8  and the crashing line was already marked covered ->", 5 in happy_hits)
print("T8  so 100% said every line ran, never every input ->",
      check("the perfect score and the crash coexist",
            percent(happy_hits, average_lines) == 100 and crash != ""))
print("T8  a percentage is a spotlight, not a scoreboard ->",
      check("the number did not find the bug", crash != ""))
print()

# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - the suite")
print("-" * 60)
SUITE = '''
    import json
    import os

    import pytest

    from under_test import average, price


    @pytest.fixture
    def shop(tmp_path):
        path = tmp_path / "shop.json"
        path.write_text(json.dumps({"books": 2}), encoding="utf-8")
        return path


    class TestAverage:
        def test_several_numbers(self):
            assert average([2, 4]) == 3

        def test_a_single_number(self):
            assert average([7]) == 7

        def test_negatives(self):
            assert average([-1, -3]) == -2


    class TestPrice:
        def test_plain(self):
            assert price(3, 10, False) == 30

        def test_member(self):
            assert price(3, 10, True) == 27

        def test_bulk(self):
            assert price(11, 10, False) == 105

        def test_bulk_member(self):
            assert price(11, 10, True) == 94

        def test_exactly_ten(self):
            assert price(10, 10, False) == 95


    class TestRaises:
        def test_text_is_not_a_number(self):
            with pytest.raises(ValueError):
                int("x")

        def test_none_is_not_a_number(self):
            with pytest.raises(TypeError):
                int(None)

        def test_a_message_can_be_checked(self):
            with pytest.raises(ValueError, match="denied"):
                raise ValueError("access denied")

        def test_a_missing_key(self):
            with pytest.raises(KeyError):
                {}["nothing"]


    class TestFixtures:
        def test_the_fixture_handed_us_a_file(self, shop):
            assert shop.exists()

        def test_the_content_survives_a_round_trip(self, shop):
            assert json.loads(shop.read_text(encoding="utf-8")) == {"books": 2}

        def test_the_folder_holds_only_ours(self, shop):
            assert sorted(os.listdir(shop.parent)) == ["shop.json"]

        def test_the_name_is_ours(self, shop):
            assert shop.name == "shop.json"
'''
suite_path = write("test_11_suite.py", SUITE)

suite_ids, group = collect(suite_path)
code_suite, out_suite = run_pytest("--tb=no", os.path.basename(suite_path))
suite_counts = counts(out_suite)

for name in ("TestAverage", "TestPrice", "TestRaises", "TestFixtures"):
    check("the suite collected " + name, name in group)

check("the suite is green", code_suite == 0)
check("the suite ran sixteen tests", suite_counts.get("passed") == 16)
check("the suite had no errors", suite_counts.get("error", 0) == 0)

for name, expected in (("TestAverage", 3), ("TestPrice", 5),
                       ("TestRaises", 4), ("TestFixtures", 4)):
    print("T9   {0:<14} collected {1:>3}".format(name, len(group.get(name, []))))
print("T9   TOTAL      passed {0:>3}  failed {1:>3}".format(
    suite_counts.get("passed", 0), suite_counts.get("failed", 0)))
print("T9   errors ->", suite_counts.get("error", 0))
print()

# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the loop, closed")
print("-" * 60)
final_path = write("test_12_final.py", SUITE + '''

    class TestTheBlindSpot:
        def test_averaging_nothing_is_zero(self):
            assert average([]) == 0
''')
projects_before = sorted(os.listdir(SCRIPT_DIR))

code_final, out_final = run_pytest("--tb=no", os.path.basename(final_path))
final_counts = counts(out_final)
codes = [code_suite, code_final]
projects_after = sorted(os.listdir(SCRIPT_DIR))

check("the clean suite exits 0", code_suite == 0)
check("the extra test makes it exit 1", code_final == 1)
check("sixteen still pass", final_counts.get("passed") == 16)
check("exactly one fails", final_counts.get("failed") == 1)
check("the only non-zero code is 1", [c for c in codes if c] == [1])
check("this folder is untouched", projects_before == projects_after)

print("T10   the clean suite exits ->", code_suite)
print("T10   the tests it ran ->", suite_counts.get("passed", 0))
print("T10   add the one test the percentage could not see ->",
      last_line(out_final))
print("T10   and the exit code flips to ->", code_final)
print("T10   across these two runs the only non-zero ->",
      [c for c in codes if c])
print("T10   and the folder this file lives in is untouched ->",
      projects_before == projects_after)
print()

# ------------------------------------------------------------
# clean up and report
# ------------------------------------------------------------
shutil.rmtree(FOLDER, ignore_errors=True)
if FOLDER in sys.path:
    sys.path.remove(FOLDER)

failed = [name for name, ok in CHECKS if not ok]
print("=" * 60)
if failed:
    for name in failed:
        print("  FAILED:", name)
    print("CHECKS PASSED {0} of {1}".format(len(CHECKS) - len(failed), len(CHECKS)))
    sys.exit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
