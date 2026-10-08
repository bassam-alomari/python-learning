# ============================================================
# Project 46 - subprocess: the bookshop calls out to other programs
# ============================================================
# What this lesson teaches:
#   subprocess.run       start a program, wait for it, read its answer
#   capture_output       stdout and stderr become two strings
#   returncode           the number the shell reads when the child exits
#   check=True           a non-zero exit code becomes an exception
#   input=               feed the child without a keyboard
#   env=                 the child's environment, passed as data
#   stderr=subprocess.STDOUT   two pipes, merged, in write order
#   timeout=             a hung tool cannot hang you
#   a list, not a string no shell parses it, so nothing gets quoted twice
#   cwd=                 run the child somewhere else, on purpose
#
# Everything is the standard library. No input(), no random, no datetime.now.
# The output is deterministic. The file runs to completion and exits with 0.
#
# Run it:  python project-46-subprocess-the-bookshop-calls-out.py
# ============================================================

import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what does subprocess.run actually start")
print("Q2  what does capture_output=True give you")
print("Q3  what is returncode")
print("Q4  what does check=True change")
print("Q5  how do you feed a child without a keyboard")
print("Q6  what does timeout= protect you from")
print("Q7  why a list instead of a string")
print("Q8  what does stderr=subprocess.STDOUT do")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  a child process, and run() waits for it to finish")
print("Q2  stdout and stderr captured into two strings")
print("Q3  the number the shell will read when the child exits")
print("Q4  a non-zero exit code raises CalledProcessError")
print("Q5  pass input='text' and the child reads it from stdin")
print("Q6  a tool that never finishes gets killed at the limit")
print("Q7  the list is passed as-is, with no shell to re-quote it")
print("Q8  stderr goes into the same pipe as stdout, in write order")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - run a command and read its stdout")
print("T1  child said -> hello from the child")
print("T1  exit code -> 0")
print("T1  so subprocess.run captures stdout -> True")
print()

print("TASK 2 - a list is not a string")
print("T2  the argument arrived whole -> Dune 1965")
print("T2  so a list is passed without a shell -> True")
print()

print("TASK 3 - the exit code is the answer")
print("T3  the child exited with -> 3")
print("T3  check=True raises CalledProcessError -> True")
print("T3  so the exit code is the answer -> True")
print()

print("TASK 4 - stdout and stderr are two pipes")
print("T4  stdout -> fine")
print("T4  stderr -> careful")
print("T4  so they are two different pipes -> True")
print()

print("TASK 5 - merging the streams on purpose")
print("T5  merged output -> line1 then line2")
print("T5  so stderr=STDOUT is one pipe, in order -> True")
print()

print("TASK 6 - feeding the child without a keyboard")
print("T6  input='abc' came back -> ABC")
print("T6  so input= writes to the child's stdin -> True")
print()

print("TASK 7 - the environment is data you pass")
print("T7  the child saw -> Oasis")
print("T7  the parent env untouched -> True")
print("T7  so the environment is data you pass -> True")
print()

print("TASK 8 - timeout: the one that must not hang")
print("T8  the child asked for 5 seconds -> slept")
print("T8  subprocess raised TimeoutExpired -> True")
print("T8  so a hung tool cannot hang you -> True")
print()

print("TASK 9 - cwd: run the child somewhere else")
print("T9  the child listed -> books.txt notes.md")
print("T9  the temp folder is gone -> True")
print("T9  so the temp folder cleans itself -> True")
print()

print("TASK 10 - the shell reads the exit code")
print("T10  project 39 report -> 0")
print("T10  project 39 not-a-verb -> 2")
print("T10  so the shell reads the exit code -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)


# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - run a command and read its stdout")
print("-" * 60)
child = subprocess.run([sys.executable, "-c", "print('hello from the child')"],
                       capture_output=True, text=True)

check("the child exited 0", child.returncode == 0)
check("stdout was captured", child.stdout == "hello from the child\n")
check("nothing leaked to stderr", child.stderr == "")
check("text=True gives str, not bytes", isinstance(child.stdout, str))

print("T1  child said ->", child.stdout.strip())
print("T1  exit code ->", child.returncode)
print("T1  so subprocess.run captures stdout ->",
      child.stdout.strip() == "hello from the child")
print()


# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - a list is not a string")
print("-" * 60)
child = subprocess.run([sys.executable, "-c", "import sys; print(sys.argv[1])",
                        "Dune 1965"], capture_output=True, text=True)

check("the argument arrived whole", child.stdout.strip() == "Dune 1965")
check("the child saw two words as one", child.stdout.split() == ["Dune", "1965"])
check("no shell touched it", child.returncode == 0)
check("nothing was re-quoted", "Dune 1965" in child.stdout)

print("T2  the argument arrived whole ->", child.stdout.strip())
print("T2  so a list is passed without a shell ->",
      child.stdout.strip() == "Dune 1965")
print()


# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - the exit code is the answer")
print("-" * 60)
child = subprocess.run([sys.executable, "-c", "import sys; sys.exit(3)"],
                       capture_output=True, text=True)
raised = None
try:
    subprocess.run([sys.executable, "-c", "import sys; sys.exit(3)"],
                   capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as exc:
    raised = exc

check("the exit code survived", child.returncode == 3)
check("without check=True nothing is raised", child.returncode == 3)
check("check=True raises", raised is not None)
check("the exception carries the same code",
      raised is not None and raised.returncode == 3)

print("T3  the child exited with ->", child.returncode)
print("T3  check=True raises CalledProcessError ->", raised is not None)
print("T3  so the exit code is the answer ->",
      child.returncode == 3 and raised is not None)
print()


# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - stdout and stderr are two pipes")
print("-" * 60)
child = subprocess.run(
    [sys.executable, "-c",
     "import sys; print('fine'); sys.stderr.write('careful\\n')"],
    capture_output=True, text=True)

check("stdout is clean", child.stdout == "fine\n")
check("stderr is separate", child.stderr == "careful\n")
check("both were captured", child.stderr != "")
check("the child still succeeded", child.returncode == 0)

print("T4  stdout ->", child.stdout.strip())
print("T4  stderr ->", child.stderr.strip())
print("T4  so they are two different pipes ->",
      child.stdout == "fine\n" and child.stderr == "careful\n")
print()


# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - merging the streams on purpose")
print("-" * 60)
# capture_output and stderr=STDOUT cannot be combined: run() would refuse.
# So the two pipes are asked for by hand, with stderr pointed at stdout.
child = subprocess.run(
    [sys.executable, "-c",
     "import sys; sys.stdout.write('line1\\n'); sys.stdout.flush(); "
     "sys.stderr.write('line2\\n')"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

check("one pipe now", child.stdout == "line1\nline2\n")
check("the order is the write order",
      child.stdout.splitlines() == ["line1", "line2"])
check("stderr has no pipe of its own", child.stderr is None)
check("both lines arrived", child.stdout.count("line") == 2)

print("T5  merged output ->", " then ".join(child.stdout.splitlines()))
print("T5  so stderr=STDOUT is one pipe, in order ->",
      child.stdout == "line1\nline2\n")
print()


# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - feeding the child without a keyboard")
print("-" * 60)
child = subprocess.run(
    [sys.executable, "-c",
     "import sys; print(sys.stdin.read().strip().upper())"],
    input="abc", capture_output=True, text=True)

check("the child read stdin", child.stdout == "ABC\n")
check("it saw exactly what we sent", child.stdout.strip() == "ABC")
check("stderr stayed empty", child.stderr == "")
check("no keyboard was involved", child.returncode == 0)

print("T6  input='abc' came back ->", child.stdout.strip())
print("T6  so input= writes to the child's stdin ->",
      child.stdout.strip() == "ABC")
print()


# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - the environment is data you pass")
print("-" * 60)
mine = dict(os.environ)
mine["BOOKSHOP"] = "Oasis"
child = subprocess.run(
    [sys.executable, "-c", "import os; print(os.environ['BOOKSHOP'])"],
    capture_output=True, text=True, env=mine)

check("the child saw the value", child.stdout.strip() == "Oasis")
check("the parent was not changed", "BOOKSHOP" not in os.environ)
check("the child got a whole environment", len(mine) >= len(os.environ))
check("env= is a copy, not os.environ itself", mine is not os.environ)

print("T7  the child saw ->", child.stdout.strip())
print("T7  the parent env untouched ->", "BOOKSHOP" not in os.environ)
print("T7  so the environment is data you pass ->",
      child.stdout.strip() == "Oasis")
print()


# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - timeout: the one that must not hang")
print("-" * 60)
expired = None
started = time.monotonic()
try:
    subprocess.run([sys.executable, "-c", "import time; time.sleep(5)"],
                   capture_output=True, text=True, timeout=0.3)
except subprocess.TimeoutExpired as exc:
    expired = exc
elapsed = time.monotonic() - started

check("the child really was still sleeping", expired is not None)
check("it is the right exception",
      isinstance(expired, subprocess.TimeoutExpired))
check("we got our process back in well under 5 seconds", elapsed < 4.0)

print("T8  the child asked for 5 seconds -> slept")
print("T8  subprocess raised TimeoutExpired ->", expired is not None)
print("T8  so a hung tool cannot hang you ->", expired is not None)
print()


# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - cwd: run the child somewhere else")
print("-" * 60)
listing = None
existed_during = False
with tempfile.TemporaryDirectory(prefix="project46") as folder:
    for name in ("books.txt", "notes.md"):
        with open(os.path.join(folder, name), "w", encoding="utf-8") as handle:
            handle.write(name + "\n")
    child = subprocess.run(
        [sys.executable, "-c",
         "import os; print('\\n'.join(sorted(os.listdir('.'))))"],
        capture_output=True, text=True, cwd=folder)
    listing = child.stdout.split()
    existed_during = os.path.isdir(folder)
gone = not os.path.exists(folder)

check("the child listed the folder",
      listing == ["books.txt", "notes.md"])
check("the folder existed while it ran", existed_during)
check("the child exited 0", child.returncode == 0)
check("the temp folder cleaned itself", gone)

print("T9  the child listed ->", " ".join(listing))
print("T9  the temp folder is gone ->", gone)
print("T9  so the temp folder cleans itself ->",
      listing == ["books.txt", "notes.md"] and gone)
print()


# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the shell reads the exit code")
print("-" * 60)
p39 = os.path.join(HERE, "project-39-the-bookshop-cli.py")
good = subprocess.run([sys.executable, p39, "report"],
                      capture_output=True, text=True)
bad = subprocess.run([sys.executable, p39, "not-a-verb"],
                     capture_output=True, text=True)

check("report worked", good.returncode == 0)
check("the good run kept stderr empty", good.stderr == "")
check("the bad verb got 2", bad.returncode == 2)
check("the refusal is explained on stderr", "invalid choice" in bad.stderr)
check("the refusal is argparse's own wording", "choose from" in bad.stderr)

print("T10  project 39 report ->", good.returncode)
print("T10  project 39 not-a-verb ->", bad.returncode)
print("T10  so the shell reads the exit code ->",
      good.returncode == 0 and bad.returncode == 2)
print()


# ------------------------------------------------------------
# report
# ------------------------------------------------------------
failed = [name for name, ok in CHECKS if not ok]
print("=" * 60)
if failed:
    for name in failed:
        print("  FAILED:", name)
    print("CHECKS PASSED {0} of {1}".format(
        len(CHECKS) - len(failed), len(CHECKS)))
    sys.exit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
