# Python Learning — 51 lessons, 38 projects

A course in Python that never asks you to type anything in. Every file runs to
completion on its own, prints its own result, and gives the same output on every
run, on every machine.

**Run anything:**

```bash
python Projects/project-38-the-bookshop.py
```

Nothing here uses `input()`. That is deliberate: a file you cannot run without a
keyboard is a file you cannot check automatically, and this course checks
everything it teaches.

---

## Why this course exists

Most Python tutorials stop at `print("Hello World")`. This one ends with a
program that has 38 predecessors behind it, and every earlier idea has to still
be true inside it.

The progression is deliberate, and each project is where the previous idea
becomes load-bearing:

| Projects | What is added | Why it matters later |
|---|---|---|
| 1–10 | setup, syntax, comments, variables, escape sequences | the alphabet |
| 11–19 | strings, indexing, slicing, formatting | text is most real data |
| 20–23 | arithmetic, lists, list methods | collections |
| 24–30 | tuples, sets, dictionaries | choosing the right container |
| 31–32 | functions, defaults, closures, memoisation | breaking a problem apart |
| 33 | a functional library app | composing functions into a program |
| 34 | JSON file persistence | state that survives the process |
| 35 | classes, properties, an exception hierarchy | validation that cannot be skipped |
| 36 | algorithms and Big-O | knowing what your code costs |
| 37 | edge cases, `unittest`, mocks, tracebacks, `pdb` | trusting your own code |
| 38 | the capstone: all of it at once | the ideas have to live together |

---

## The projects worth reading

If you only read five files, read these.

### 33 — `library-management-system.py`
Functions only: defaults, immutability, boundary checks. The discipline of
refusing bad input before it spreads.

### 34 — `json-file-persistence.py`
The real lesson: **an exception does not stop you.** A `try` block that catches
the error and then falls through to the next line will happily save a corrupted
state to disk. Use `try/except/else`, and write atomically.

### 35 — `oop-library-classes.py`
Validation in `property` setters, so an invalid object cannot be constructed at
all. Plus a small exception hierarchy, so one `except` catches a whole family of
problems without swallowing unrelated ones.

### 36 — `algorithms-and-big-o.py`
Timing is noise on a modern laptop; **operation counts are not.** This project
measures work by counting steps, and it is the only kind of benchmark you should
trust on your own machine.

### 38 — `the-bookshop.py`
The capstone. Classes, atomic JSON, CSV, a context manager, a memoised lookup,
and a 36-test suite — in one file, working together.

---

## What each project is built to teach

**Determinism is a design decision.** No `datetime.now()`, no `random`, no
`input()`. Days are numbers passed into the program, so a fine of 12 is 12
every time you run it.

**Atomic writes.** Write to a temporary file in the same folder, then
`os.replace()` the real one. A crash leaves the old file intact rather than half
of the new one. The capstone proves it: it asserts that no `.tmp` file survives.

**One text form per data set.** `json.dumps(..., sort_keys=True, indent=2)` means
the same shop always produces a byte-identical file, so `git diff` shows a real
change instead of reordering noise.

**CSV has two traps, and both are silent.**
1. It writes `\r\n` on Windows and `\n` on Linux by default, so the same data
   produces two different files. Pass `lineterminator="\n"`.
2. It hands every value back as **text**. `int()` your numbers, or your
   arithmetic quietly breaks. And a missing column is not a `KeyError` waiting
   to happen — the key is simply absent, so use `.get()`.

**`open(...).read()` is a bug waiting for a busy machine.** It relies on the
garbage collector to close the handle. Use `with`, and run `python -W error` on
your files to prove you have no leaks.

**A context manager makes "save only if nothing broke" a language feature.**
`__enter__` loads, `__exit__` saves — but only when `exc_type is None`, and it
returns `False` so the original exception still escapes. This is the `34` bug
solved structurally rather than by remembering.

**`assert` is documentation, not validation.** `python -O` deletes every `assert`
in your program and your exit code becomes `0` while your check silently
disappears. Verified, not assumed:

```
plain exit: 1   → AssertionError
-O exit:    0   → ran straight past it
```

Validate user input with `raise`. Use `assert` to state an invariant.

**Money and floats do not mix.** `0.1 + 0.2 == 0.3` is `False`. For money, count
integer units. If you must use floats, compare with `assertAlmostEqual`.

**An exception does not stop you, it hands you a value.** Miss the `except` and
the variable survives the block as `None`, and your program keeps running with
it. Read what you need before the block ends.

**A test suite that has never failed has never been tested.** Project 37 kills a
deliberate test on purpose, records the red report, then repairs it and records
the green one. Otherwise you cannot tell a working harness from a broken one.

**Most of the interesting tests feed the program rubbish.** Empty input, zero,
negative numbers, duplicates, unknown names, a half-written file. What a program
*refuses* tells you more than what it accepts.

**There are two kinds of test failure.** An **assertion** failure is a bug you
were hunting. An **error** is a test that blew up before it could check anything
— far more dangerous, because it counts as neither pass nor failure.

---

## Layout

```
python-learning-course/   51 lesson files, in order
Projects/                 38 project files, in order
```

Each project follows one shape:

```
PART A   the questions
PART B   the task, with the output it must produce
PART C   the solution, which actually produces it
```

---

## The course in one paragraph

You start by learning that `print` is a function, and you finish by shipping a
bookshop that refuses to save a corrupted state, exports a file that opens
identically on Windows and Linux, proves a lookup is one step instead of four,
and holds itself to 36 tests — none of which can tell you it passed unless it
also demonstrates that it can fail.