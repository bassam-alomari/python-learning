# -----------------------------------------------------------------
# Lesson 128: run Python files from the terminal
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : run with python file.py, path/name resolution,
#            current directory, script arguments, direct
#            execution and the shebang/executable distinction
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript audio is partly unclear, but repeatedly
# refers to running a Python file from a command/terminal,
# entering the file name, and the difference between running
# through Python and executing the file directly. This lesson
# demonstrates those concepts reproducibly without changing
# system permissions or PATH.
#
#   INTERPRETER [00:39-00:54] -- python path/to/file.py
#   runs the file through the Python interpreter
#   LOCATION [01:03-01:37] -- from another directory, use
#   a path to the script; the current working directory is
#   not necessarily the script's directory
#   DIRECT RUN -- requires an executable launcher/association
#   (commonly a shebang plus execute permission on Unix); the
#   portable command is always python script.py

import os
import shutil
import subprocess
import sys
import tempfile

# ============================================================
# [1] A Python file is text until run
# ============================================================
# The terminal command names both the interpreter and file:

print("  command form: python path/to/script.py")
print("  interpreter: Python reads and runs the source file")
#   command form: python path/to/script.py
#   interpreter: Python reads and runs the source file

# ============================================================
# [2] Create a small script in a temporary folder
# ============================================================
# Use a temporary script so the lesson is self-contained:

WORK_DIR = tempfile.mkdtemp(prefix="py128_")
script_path = os.path.join(WORK_DIR, "hello_script.py")
script_source = (
    "import sys\n"
    "print('script says hello')\n"
    "print('argument count:', len(sys.argv) - 1)\n"
    "if len(sys.argv) > 1:\n"
    "    print('first argument:', sys.argv[1])\n"
)

with open(script_path, "w", encoding="utf-8", newline="") as handle:
    handle.write(script_source)

print(f"  script file created: {os.path.isfile(script_path)}")
#   script file created: True

# ============================================================
# [3] Run through the current Python interpreter [00:39]
# ============================================================
# subprocess receives an argument list, not a shell string:

run_result = subprocess.run(
    [sys.executable, script_path],
    capture_output=True,
    text=True,
    check=True,
)
run_lines = run_result.stdout.splitlines()

print(f"  script exit code: {run_result.returncode}")
print(f"  script output: {run_lines}")
#   script exit code: 0
#   script output: ['script says hello', 'argument count: 0']

# sys.executable selects the same interpreter running this
# lesson; this is the robust equivalent of `python file.py`.

# ============================================================
# [4] Pass command-line arguments
# ============================================================
# Words after the script path become sys.argv entries:

arg_result = subprocess.run(
    [sys.executable, script_path, "Amina", "extra"],
    capture_output=True,
    text=True,
    check=True,
)
arg_lines = arg_result.stdout.splitlines()

print(f"  argument run output: {arg_lines}")
#   argument run output: ['script says hello', 'argument count: 2', 'first argument: Amina']

# ============================================================
# [5] Current directory versus script location [01:03]
# ============================================================
# The shell's current directory is separate from the file's
# directory. A full script path works from another cwd:

other_dir = os.path.join(WORK_DIR, "other")
os.mkdir(other_dir)
other_run = subprocess.run(
    [sys.executable, script_path],
    cwd=other_dir,
    capture_output=True,
    text=True,
    check=True,
)

print(f"  run from another directory succeeds: {other_run.returncode == 0}")
print(f"  script output preserved: {other_run.stdout.splitlines() == run_lines}")
#   run from another directory succeeds: True
#   script output preserved: True

# ============================================================
# [6] Why a path matters
# ============================================================
# A relative filename is resolved from the current working
# directory. Confirm the two directories differ:

print(f"  script is in temp work folder: {os.path.dirname(script_path) == WORK_DIR}")
print(f"  run cwd differs from script folder: {other_dir != os.path.dirname(script_path)}")
#   script is in temp work folder: True
#   run cwd differs from script folder: True

# The full path avoids ambiguity when the terminal is elsewhere.

# ============================================================
# [7] Direct execution is platform-dependent
# ============================================================
# Running `script.py` directly depends on OS file
# associations or an executable launcher; `python script.py`
# explicitly selects the interpreter and is portable:

print("  portable choice: invoke the Python interpreter explicitly")
print("  direct execution: depends on OS association or executable permission")
#   portable choice: invoke the Python interpreter explicitly
#   direct execution: depends on OS association or executable permission

# On Unix-like systems a shebang (#!/usr/bin/env python3)
# and executable permission are typically needed. Windows
# may use file associations/launchers. No permission or PATH
# settings are changed by this lesson.

# ============================================================
# [8] Script name and extension
# ============================================================
# A .py suffix is a convention that identifies Python source:

print(f"  script basename: {os.path.basename(script_path)}")
print(f"  Python extension: {os.path.splitext(script_path)[1]}")
print(f"  script exists before cleanup: {os.path.exists(script_path)}")
#   script basename: hello_script.py
#   Python extension: .py
#   script exists before cleanup: True

# ============================================================
# [9] Handle a script failure without crashing the caller
# ============================================================
# A failing child process returns a nonzero status; capture
# it and inspect the result:

failure_path = os.path.join(WORK_DIR, "failure_script.py")
with open(failure_path, "w", encoding="utf-8", newline="") as handle:
    handle.write("raise ValueError('demo failure')\n")

failure_run = subprocess.run(
    [sys.executable, failure_path],
    capture_output=True,
    text=True,
)
failure_lines = failure_run.stderr.splitlines()

print(f"  failing script nonzero exit: {failure_run.returncode != 0}")
print(f"  error captured from child: {any('ValueError' in line for line in failure_lines)}")
#   failing script nonzero exit: True
#   error captured from child: True

# ============================================================
# [10] Reproducible command recipe
# ============================================================
# A safe recipe for a terminal:

recipe = (
    "open terminal",
    "locate the script or use its path",
    "run python script.py",
    "add arguments after the script name if needed",
    "check output and exit status",
)
print(f"  recipe steps: {len(recipe)}")
print(f"  run command: {recipe[2]}")
#   recipe steps: 5
#   run command: run python script.py

# ============================================================
# [11] Interpreter path used by this process
# ============================================================
# Use a boolean rather than printing a machine-specific path:

print(f"  interpreter path is a file: {os.path.isfile(sys.executable)}")
print(f"  interpreter basename has python: {'python' in os.path.basename(sys.executable).lower()}")
#   interpreter path is a file: True
#   interpreter basename has python: True

# ============================================================
# [12] Clean temporary scripts
# ============================================================
# Remove all lesson-created files and directories:

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  temp work directory removed: {not os.path.exists(WORK_DIR)}")
#   temp work directory removed: True

# ============================================================
# [13] The summary
# ============================================================
# Running Python files from a terminal:
#
#   1. PORTABLE COMMAND [00:39-00:54] -- python file.py
#      runs the file through the Python interpreter
#   2. SCRIPT NAME -- supply the .py filename; include a
#      path when it is outside the current directory
#   3. CURRENT DIRECTORY [01:03-01:37] -- relative paths
#      resolve from the terminal's cwd, not automatically
#      from the script's folder
#   4. ARGUMENTS -- values after file.py appear in sys.argv
#   5. DIRECT RUN -- depends on OS association/launcher;
#      Unix commonly needs shebang and execute permission
#   6. ERRORS -- subprocess can capture output and inspect
#      the child's nonzero exit status
#   7. SAFETY -- this lesson does not change PATH, file
#      associations or permissions; temp files are removed
#
# Tell the interpreter which file to run; use a path when
# the shell is not already in the file's directory.
