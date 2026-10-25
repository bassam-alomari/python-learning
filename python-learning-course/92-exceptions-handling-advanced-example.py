# -----------------------------------------------------------------
# Lesson 92: exceptions handling -- advanced practical example
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : the file-open program with 5 tries: while
#            loop + try / except / else / finally,
#            FileNotFoundError caught and decremented,
#            read on success, close in finally, and
#            "All Tries Done" on exhaustion
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: an advanced, comprehensive
# practical example -- Exceptions Handling Advanced.
#
#   THE IDEA [00:20] -- a program that takes a file name
#   (File Path) to open and read; a fixed number of
#   tries (5); a wrong name -> catch FileNotFoundError,
#   decrement a try, warn about the tries left; a right
#   name -> open, read, and close safely with finally;
#   no tries left -> end with "All Tries Done"
#   THE STRUCTURE [01:23] -- while loop for the tries
#   left; try to open; except for FileNotFoundError (or
#   anything else); else for the successful read;
#   finally to close the file in ALL cases -- no
#   resource leaks, no memory problems
#   WHY IT MATTERS [09:55] -- this one example gathers
#   everything learned about exception handling into a
#   realistic, useful program
#
# STABILITY RULES: no input() -- the "user" is a
# scripted list of names, so every run is identical.
# The sandbox file is created with known content and
# destroyed at the end; only our messages, built-in
# type names and booleans are printed -- no tracebacks,
# no machine paths. All expected outputs came from
# running the file.

import inspect
import os
import shutil
import tempfile

# ============================================================
# [1] The program's idea [00:20]
# ============================================================
# The transcript's spec, as four lines:

print("  the program: open a file by name, with 5 tries")
print("  on miss: catch, decrement, warn remaining")
print("  on hit: read, then close in finally")
print("  on exhaustion: All Tries Done")
#   the program: open a file by name, with 5 tries
#   on miss: catch, decrement, warn remaining
#   on hit: read, then close in finally
#   on exhaustion: All Tries Done

# Four sentences, the whole contract. Now we build it.

# ============================================================
# [2] The structure: while + four clauses [01:23]
# ============================================================
# The transcript's mapping -- which clause does what:

print("  while: controls the remaining tries")
print("  try: attempts to open the file")
print("  except: catches FileNotFoundError and decrements")
print("  else: reads the file on success")
print("  finally: closes the file in all cases")
#   while: controls the remaining tries
#   try: attempts to open the file
#   except: catches FileNotFoundError and decrements
#   else: reads the file on success
#   finally: closes the file in all cases

# The loop owns the COUNT; the try family owns one
# attempt. Between them: the full handling model from
# lesson 91, applied to a real task.

# ============================================================
# [3] The sandbox: a real file to find
# ============================================================
# The target the "user" is trying to open:

WORK_DIR = tempfile.mkdtemp(prefix="py92_")
notes_path = os.path.join(WORK_DIR, "notes.txt")

handle = open(notes_path, "w", encoding="utf-8")
handle.write("lesson 92 notes")
handle.close()

print(f"  sandbox file created: {os.path.exists(notes_path)}")
print(f"  wrong names will miss: {not os.path.exists(os.path.join(WORK_DIR, 'ghost_a.txt'))}")
#   sandbox file created: True
#   wrong names will miss: True

# One real file, two guaranteed ghosts -- the stage for
# misses and a hit.

# ============================================================
# [4] The engine: while + try/except/else/finally
# ============================================================
# The transcript's structure in code. The "user input"
# is a scripted list (no input() -- determinism), and
# every attempt walks all four clauses:

def run_open_program(names, max_tries):
    """Open the first existing name; report every step."""
    tries_left = max_tries
    attempts = []
    else_runs = 0
    finally_runs = 0
    closed_flags = []
    content = ""
    outcome = "All Tries Done"
    index = 0

    while tries_left > 0 and index < len(names):
        name = names[index]
        index += 1
        handle = None
        try:
            handle = open(
                os.path.join(WORK_DIR, name),
                "r",
                encoding="utf-8",
            )
        except FileNotFoundError:
            tries_left -= 1
            attempts.append(
                (name, "FileNotFoundError", tries_left)
            )
        else:
            else_runs += 1
            content = handle.read()
            attempts.append((name, "read", tries_left))
            outcome = "success"
            break
        finally:
            finally_runs += 1
            if handle is not None:
                handle.close()
                closed_flags.append(handle.closed)

    return {
        "attempts": attempts,
        "else_runs": else_runs,
        "finally_runs": finally_runs,
        "closed_flags": closed_flags,
        "content": content,
        "outcome": outcome,
        "tries_left": tries_left,
    }

# The source itself, checked against the transcript's
# blueprint [01:23]:

engine_source = inspect.getsource(run_open_program)
print(f"  engine uses while: {'while ' in engine_source}")
print(f"  engine has try/except/else/finally: "
      f"{all(key in engine_source for key in ('try:', 'except FileNotFoundError', 'else:', 'finally:'))}")
#   engine uses while: True
#   engine has try/except/else/finally: True

# The five pieces the transcript names are all really
# there -- verified from the function's own source.

# ============================================================
# [5] Run 1: two misses, then the hit
# ============================================================
# The scripted user: two wrong names, then the right
# one -- exactly the transcript's flow:

run_one = run_open_program(
    ["ghost_a.txt", "ghost_b.txt", "notes.txt"],
    max_tries=5,
)

for step, (name, kind, left) in enumerate(run_one["attempts"], start=1):
    if kind == "FileNotFoundError":
        print(f"  try {step}: {name} -> {kind}, tries left: {left}")
    else:
        print(f"  try {step}: {name} -> opened and read")
#   try 1: ghost_a.txt -> FileNotFoundError, tries left: 4
#   try 2: ghost_b.txt -> FileNotFoundError, tries left: 3
#   try 3: notes.txt -> opened and read

# Two catches, two decrements (5 -> 4 -> 3), then the
# file appeared. The warning about remaining tries is
# right there in the log -- the transcript's "تنبيهه
# بالمحاولات المتبقية".

# ============================================================
# [6] The successful read [00:20]
# ============================================================
# The else clause did its job on the hit:

print(f"  content read: {run_one['content']}")
print(f"  outcome: {run_one['outcome']}")
print(f"  else ran on the hit: {run_one['else_runs']}")
#   content read: lesson 92 notes
#   outcome: success
#   else ran on the hit: 1

# The content matches what section [3] wrote -- the
# read happened through the else, never through the
# try (the transcript's clean separation).

# ============================================================
# [7] finally closed the file [01:23]
# ============================================================
# The transcript's hard requirement: file.close() in
# every case. Three attempts, three finally visits, and
# the opened file is closed:

print(f"  finally ran per attempt: {run_one['finally_runs']}")
print(f"  file closed in finally: {run_one['closed_flags'] == [True]}")
print(f"  no resource leaked: {all(run_one['closed_flags'])}")
#   finally ran per attempt: 3
#   file closed in finally: True
#   no resource leaked: True

# One visit per attempt -- misses included (their
# handle was None, nothing to close) and the hit
# (handle closed, flag True). "لضمان عدم تسريب
# الموارد" -- proven, not promised.

# ============================================================
# [8] else ran ONLY on success
# ============================================================
# Three attempts, one else -- the misses never reached
# it, because their except answered first:

misses_one = sum(
    1 for _, kind, _ in run_one["attempts"]
    if kind == "FileNotFoundError"
)
print(f"  attempts: {len(run_one['attempts'])}")
print(f"  misses: {misses_one}")
print(f"  else runs: {run_one['else_runs']}")
print(f"  else skipped on misses: {run_one['else_runs'] == 1 and misses_one == 2}")
#   attempts: 3
#   misses: 2
#   else runs: 1
#   else skipped on misses: True

# 3 attempts, 2 misses, exactly 1 else -- the ratio
# that proves the clause's rule from lesson 91, now
# inside a real program.

# ============================================================
# [9] Run 2: all tries exhausted [00:20]
# ============================================================
# The other ending: five wrong names, no hit -- the
# program must stop with the transcript's message:

run_two = run_open_program(
    ["ghost_1.txt", "ghost_2.txt", "ghost_3.txt",
     "ghost_4.txt", "ghost_5.txt"],
    max_tries=5,
)

misses_two = len(run_two["attempts"])
print(f"  misses recorded: {misses_two}")
print(f"  tries left: {run_two['tries_left']}")
print(f"  final message: {run_two['outcome']}")
print(f"  loop stopped by tries: {run_two['tries_left'] == 0}")
#   misses recorded: 5
#   tries left: 0
#   final message: All Tries Done
#   loop stopped by tries: True

# Five misses, counter at zero, outcome exactly "All
# Tries Done" -- the transcript's ending, word for
# word. The while condition (tries_left > 0) is what
# ended the loop, not a crash.

# ============================================================
# [10] The exhausted run's hygiene
# ============================================================
# Even the failure path must be clean: finally visited
# every attempt, no file was ever opened, nothing to
# close, nothing leaked:

print(f"  finally ran in exhausted run: {run_two['finally_runs']}")
print(f"  else never ran: {run_two['else_runs'] == 0}")
print(f"  no file was opened: {run_two['closed_flags'] == []}")
print(f"  content stays empty: {run_two['content'] == ''}")
#   finally ran in exhausted run: 5
#   else never ran: True
#   no file was opened: True
#   content stays empty: True

# finally kept its promise five times with nothing to
# close -- the clause costs nothing when there is no
# resource, and saves you when there is one.

# ============================================================
# [11] Both endings, side by side
# ============================================================
# The transcript's two terminal states, compared:

print(f"  run 1 outcome: {run_one['outcome']}")
print(f"  run 2 outcome: {run_two['outcome']}")
print(f"  run 1 attempts: {len(run_one['attempts'])} of 5")
print(f"  run 2 attempts: {len(run_two['attempts'])} of 5")
#   run 1 outcome: success
#   run 2 outcome: All Tries Done
#   run 1 attempts: 3 of 5
#   run 2 attempts: 5 of 5

# One program, two honest endings: success after three
# tries, exhaustion after five. No traceback in either
# -- handling all the way down.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block:

print(f"  engine blueprint complete: "
      f"{all(key in engine_source for key in ('while ', 'try:', 'except FileNotFoundError', 'else:', 'finally:'))}")
print(f"  run 1 misses: {misses_one}")
print(f"  run 1 content: {run_one['content']}")
print(f"  run 1 file closed: {run_one['closed_flags'] == [True]}")
print(f"  run 1 else runs: {run_one['else_runs']}")
print(f"  run 1 finally runs: {run_one['finally_runs']}")
print(f"  run 2 outcome: {run_two['outcome']}")
print(f"  run 2 tries left: {run_two['tries_left']}")
print(f"  run 2 misses: {misses_two}")
print(f"  run 2 else runs: {run_two['else_runs']}")
print(f"  run 2 finally runs: {run_two['finally_runs']}")

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   engine blueprint complete: True
#   run 1 misses: 2
#   run 1 content: lesson 92 notes
#   run 1 file closed: True
#   run 1 else runs: 1
#   run 1 finally runs: 3
#   run 2 outcome: All Tries Done
#   run 2 tries left: 0
#   run 2 misses: 5
#   run 2 else runs: 0
#   run 2 finally runs: 5
#   sandbox removed: True

# Twelve facts, two complete runs, zero crashes, zero
# leaked files -- the transcript's advanced example,
# executed end to end.

# ============================================================
# [13] The summary
# ============================================================
# The advanced example, from the transcript:
#
#   1. THE IDEA [00:20] -- take a file name, allow 5
#      tries, catch a wrong name, read a right one,
#      finish with "All Tries Done" if all fail
#   2. THE STRUCTURE [01:23] -- while owns the tries
#      left; try opens; except catches
#      FileNotFoundError and decrements; else reads on
#      success; finally closes in all cases (all five
#      verified present in the engine's own source)
#   3. THE SANDBOX -- a real notes.txt with known
#      content, plus guaranteed ghosts: created True,
#      ghosts missing True
#   4. RUN 1 -- two misses with warnings (tries left 4
#      then 3), then the hit: opened and read
#   5. THE READ -- content "lesson 92 notes", outcome
#      success, else ran exactly once on the hit
#   6. FINALLY'S DUTY -- 3 attempts, 3 finally visits,
#      the opened file closed (True), no resource
#      leaked (all closed flags True): the transcript's
#      "file.close() in all cases", proven
#   7. ELSE'S RULE -- 3 attempts, 2 misses, 1 else:
#      the misses never reached it (True) -- the
#      lesson 91 ratio, inside a real program
#   8. RUN 2 -- five misses, tries left 0, final
#      message exactly "All Tries Done", loop ended by
#      the while condition (True), not by a crash
#   9. EXHAUSTED HYGIENE -- finally ran 5 times with
#      nothing to close, else never ran (True), no file
#      opened (True), content empty (True): the failure
#      path is as clean as the success path
#  10. BOTH ENDINGS -- success (3 of 5 attempts) and
#       All Tries Done (5 of 5): one program, two
#       honest terminals, no traceback in either
#  11. THE DISCIPLINE -- no input(): the user is a
#       scripted list, so every run is byte-identical;
#       sandbox destroyed (removed True); only our
#       messages, type names and booleans printed
#  12. WHY IT MATTERS [09:55] -- while + try + except +
#       else + finally in one realistic task: the whole
#       handling course, gathered into a program you
#       would actually ship
#
# One attempt is a guess; five handled attempts are a
# program. The difference is the structure around them.
