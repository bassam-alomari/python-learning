# -----------------------------------------------------------------
# Lesson 91: exceptions handling -- try, except, else, finally
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : the full handling structure, catching
#            without crashing, specific except blocks
#            per error type, else on success only,
#            finally always (resource cleanup)
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: full control and handling of
# errors and exceptions with Try, Except, Else and
# Finally.
#
#   STRUCTURE [01:05] -- the basic try ... except form
#   TRY [01:24] -- the code that MIGHT fail while
#   running (like reading user input typed wrongly)
#   EXCEPT [01:37] -- activates immediately if an
#   exception hits inside try: it prevents the crash
#   and shows a suitable message instead
#   SPECIFIC [06:00] -- more than one except block to
#   catch different types precisely (ZeroDivisionError
#   for division by zero, ValueError for bad values),
#   each handled its own way
#   ELSE [03:04] -- runs ONLY if try finished with no
#   exception at all
#   FINALLY [04:13] -- runs in ALL cases (error or not,
#   caught or not); typically closes files, connections
#   and databases -- resource cleanup
#
# STABILITY RULES: every exception here is caught; the
# file sandbox is created with tempfile and destroyed at
# the end; only our own messages, built-in type names
# and booleans are printed -- no tracebacks, no machine
# paths. All expected outputs came from running the file.

import os
import tempfile
import shutil

# ============================================================
# [1] The structure [01:05]
# ============================================================
# Four keywords, four jobs -- the transcript's basic
# form before any code runs:

print("  the four parts: try, except, else, finally")
print("  order in source: try first, finally last")
#   the four parts: try, except, else, finally
#   order in source: try first, finally last

# try holds the risky code; except answers a failure;
# else rewards success; finally keeps its promise either
# way. The interpreter reads them as one unit.

# ============================================================
# [2] try: the code that might fail [01:24]
# ============================================================
# The transcript's example: user input read wrongly.
# We simulate a user who typed "42" -- int() succeeds:

user_value = "42"
try:
    parsed = int(user_value)
except ValueError:
    parse_ok = False
else:
    parse_ok = True

print(f"  user value parsed: {parse_ok}")
print(f"  parsed result: {parsed}")
#   user value parsed: True
#   parsed result: 42

# The try block held the conversion; nothing failed, so
# the except stayed silent and the value arrived. Now
# the user types "forty-two":

# ============================================================
# [3] except: catch instead of crashing [01:13 -> 01:37]
# ============================================================
# Same conversion, wrong input. The transcript: except
# activates "فوراً" and prevents the Crash:

try:
    parsed_bad = int("forty-two")
except ValueError:
    bad_input_caught = True
else:
    bad_input_caught = False

print(f"  bad input caught: {bad_input_caught}")
print(f"  crash prevented: {bad_input_caught}")
#   bad input caught: True
#   crash prevented: True

# Without except, this line would never print -- the
# program would be dead. With it, the failure became a
# fact we can use.

# ============================================================
# [4] Proof: execution continues
# ============================================================
# The strongest evidence that no crash happened: this
# section exists at all, AFTER the failure in [3]:

continued = bad_input_caught  # we reached this line
print(f"  execution continued after except: {continued}")
#   execution continued after except: True

# The program walked past the error and kept going --
# that is the whole promise of handling: a suitable
# message instead of a tombstone.

# ============================================================
# [5] Specific exceptions [06:00]
# ============================================================
# The transcript: more than one except block, each type
# answered precisely. One classifier, four outcomes:

def classify(work):
    """Run work and name the exception it raises."""
    try:
        work()
    except ZeroDivisionError:
        return "ZeroDivisionError"
    except ValueError:
        return "ValueError"
    except TypeError:
        return "TypeError"
    return "no error"

print(f"  10 / 0 -> {classify(lambda: 10 / 0)}")
print(f"  int('x') -> {classify(lambda: int('x'))}")
print(f"  'a' + 1 -> {classify(lambda: 'a' + 1)}")
print(f"  2 + 2 -> {classify(lambda: 2 + 2)}")
#   10 / 0 -> ZeroDivisionError
#   int('x') -> ValueError
#   'a' + 1 -> TypeError
#   2 + 2 -> no error

# Each failure fell into ITS OWN block -- division by
# zero never pretends to be a bad value, and the clean
# call fell through to "no error". Precise diagnosis,
# precise answer: exactly the transcript's design.

# ============================================================
# [6] else: only when try succeeds [03:04]
# ============================================================
# The transcript: else runs "فقط إذا لم تحدث أي أخطاء".
# Two paths, one flag each:

try:
    ok_value = 5 * 4
except Exception:
    else_on_success = False
else:
    else_on_success = True

try:
    raise ValueError("no else for you")
except ValueError:
    else_on_failure = False
else:
    else_on_failure = True

print(f"  else ran on success: {else_on_success}")
print(f"  else skipped on failure: {not else_on_failure}")
print(f"  else result: {ok_value}")
#   else ran on success: True
#   else skipped on failure: True
#   else result: 20

# Success earns the else; failure never reaches it --
# the except already answered. Keep "what to do when it
# WORKED" out of the try block itself.

# ============================================================
# [7] finally: runs in all cases [04:13]
# ============================================================
# The transcript: finally executes "في جميع الأحوال".
# Two scenarios -- clean and failing -- one counter:

finally_runs = 0
for scenario in ("clean", "failing"):
    try:
        if scenario == "failing":
            raise ValueError("scenario failure")
    except ValueError:
        pass
    finally:
        finally_runs += 1

print(f"  finally ran in both scenarios: {finally_runs == 2}")
print(f"  count: {finally_runs}")
#   finally ran in both scenarios: True
#   count: 2

# Success and failure both paid their visit to finally.
# (An UNcaught exception would run finally too, then
# propagate -- we never demo that here, because this
# lesson never crashes.)

# ============================================================
# [8] The execution order, proven
# ============================================================
# What actually runs, in what order -- recorded as a
# trace for both paths:

order_ok = []
try:
    order_ok.append("try")
except ValueError:
    order_ok.append("except")
else:
    order_ok.append("else")
finally:
    order_ok.append("finally")

order_bad = []
try:
    order_bad.append("try")
    raise ValueError("force the failure path")
except ValueError:
    order_bad.append("except")
else:
    order_bad.append("else")
finally:
    order_bad.append("finally")

print(f"  success order: {' -> '.join(order_ok)}")
print(f"  failure order: {' -> '.join(order_bad)}")
#   success order: try -> else -> finally
#   failure order: try -> except -> finally

# The two canonical sequences: success skips except,
# failure skips else -- and finally is in BOTH. The
# transcript's four blocks, timed exactly.

# ============================================================
# [9] Resource cleanup: files [04:13]
# ============================================================
# The transcript's main use for finally: closing files.
# A write that FAILS mid-way -- the file must still be
# closed, or the resource leaks:

WORK_DIR = tempfile.mkdtemp(prefix="py91_")
notes_path = os.path.join(WORK_DIR, "notes.txt")

handle = open(notes_path, "w", encoding="utf-8")
try:
    handle.write("lesson 91")
    raise ValueError("simulated failure after write")
except ValueError:
    cleanup_failure_caught = True
finally:
    handle.close()

print(f"  failure caught: {cleanup_failure_caught}")
print(f"  file closed despite failure: {handle.closed}")

# And the clean path -- finally closes just the same:

handle_two = open(notes_path, "r", encoding="utf-8")
try:
    content = handle_two.read()
finally:
    handle_two.close()

print(f"  clean path also closed: {handle_two.closed}")
print(f"  content survived: {content}")
#   failure caught: True
#   file closed despite failure: True
#   clean path also closed: True
#   content survived: lesson 91

# Two opens, two closes, zero leaks -- the failure did
# not stop the cleanup, because cleanup does not live
# in the happy path. That is the transcript's "لضمان
# تنظيف الموارد".

# ============================================================
# [10] The full structure in one block
# ============================================================
# All four clauses around one operation, one run:

full_trace = []
try:
    full_trace.append("try")
    value = int("12")
except ValueError:
    full_trace.append("except")
else:
    full_trace.append("else")
finally:
    full_trace.append("finally")

print(f"  full block trace: {' -> '.join(full_trace)}")
print(f"  value parsed: {value}")
#   full block trace: try -> else -> finally
#   value parsed: 12

# try did the work, else reported the success, finally
# kept its promise -- the complete transcript structure
# in six lines.

# ============================================================
# [11] The checklist: which clause when
# ============================================================
# The four jobs, as one screen you can keep:

print("  try: the code that might fail")
print("  except: the answer to a specific failure")
print("  else: the reward for success")
print("  finally: the promise that always runs")
#   try: the code that might fail
#   except: the answer to a specific failure
#   else: the reward for success
#   finally: the promise that always runs

# Risk, answer, reward, promise -- four sentences, the
# whole handling model.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block:

print(f"  clean try parsed: {parse_ok}")
print(f"  bad input caught: {bad_input_caught}")
print(f"  execution continued: {continued}")
print(f"  specific types: {classify(lambda: 10 / 0)} / {classify(lambda: int('x'))}")
print(f"  else on success: {else_on_success}")
print(f"  else skipped on failure: {not else_on_failure}")
print(f"  finally always: {finally_runs == 2}")
print(f"  success order: {' -> '.join(order_ok)}")
print(f"  failure order: {' -> '.join(order_bad)}")
print(f"  file closed on failure: {handle.closed}")

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   clean try parsed: True
#   bad input caught: True
#   execution continued: True
#   specific types: ZeroDivisionError / ValueError
#   else on success: True
#   else skipped on failure: True
#   finally always: True
#   success order: try -> else -> finally
#   failure order: try -> except -> finally
#   file closed on failure: True
#   sandbox removed: True

# Eleven facts, zero crashes, zero leaked files --
# handling, demonstrated end to end.

# ============================================================
# [13] The summary
# ============================================================
# try / except / else / finally, from the transcript:
#
#   1. STRUCTURE [01:05] -- the basic try ... except
#      form; four keywords, four jobs, one unit
#   2. TRY [01:24] -- holds the code that might fail
#      while running (user input typed wrongly: "42"
#      parsed True, result 42)
#   3. EXCEPT [01:37] -- activates immediately on a
#      failure inside try: "forty-two" caught True,
#      crash prevented True -- a suitable message
#      instead of a program death
#   4. CONTINUATION -- execution continued after except
#      (True): the sections after [3] exist only because
#      handling kept the program alive
#   5. SPECIFIC EXCEPTIONS [06:00] -- one classifier,
#      four except outcomes: 10/0 ->
#      ZeroDivisionError, int('x') -> ValueError,
#      'a' + 1 -> TypeError, 2 + 2 -> no error -- each
#      type answered by its own block
#   6. ELSE [03:04] -- runs ONLY when try succeeds:
#      ran on success True, skipped on failure True,
#      result 20 -- success logic stays out of try
#   7. FINALLY [04:13] -- runs in ALL cases: both
#      scenarios visited it (count 2, True); an uncaught
#      exception would visit it too, then propagate --
#      never demonstrated, because this lesson never
#      crashes
#   8. THE ORDER -- success: try -> else -> finally;
#      failure: try -> except -> finally -- recorded by
#      trace lists, not assumed
#   9. RESOURCE CLEANUP [04:13] -- a write that fails
#      mid-way still closes its file in finally (closed
#      True); the clean path closes too (True); content
#      survived: lesson 91 -- no leaks on either path
#  10. THE FULL BLOCK -- all four clauses in one run:
#       trace try -> else -> finally, value 12
#  11. THE CHECKLIST -- try: the risky code; except: the
#       specific answer; else: the reward; finally: the
#       promise -- four sentences, the whole model
#  12. THE DISCIPLINE -- every exception caught, sandbox
#       destroyed (removed True); only our messages,
#       built-in type names and booleans printed -- no
#       tracebacks, no machine paths
#
# Unhandled, an exception is a verdict. Handled, it is
# information -- and finally is where you put the things
# that must happen no matter which.
