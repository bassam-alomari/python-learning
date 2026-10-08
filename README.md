# Python Learning — 51 lessons, 45 projects

A course in Python that never asks you to type anything in. Every file runs to
completion on its own, prints its own result, and gives the same output on every
run, on every machine.

**Run anything:**

```bash
python Projects/project-38-the-bookshop.py          # a lesson
python Projects/project-39-the-bookshop-cli.py add-book Dune "Frank Herbert" --copies 3
python Projects/project-39-the-bookshop-cli.py report
python Projects/project-40-pytest-and-coverage.py   # runs pytest inside itself
python Projects/project-41-packaging-a-wheel.py      # builds a wheel, pip installs it
python Projects/project-42-sqlite-the-bookshop-db.py # a real database, in one file
python Projects/project-43-threading-concurrent-customers.py # the shop serves many at once
python Projects/project-44-http-the-bookshop-gets-a-web-api.py # the shop speaks HTTP
python Projects/project-45-argparse-the-bookshop-cli.py # a CLI you can test without a keyboard
echo $?
```

Nothing here uses `input()`. That is deliberate: a file you cannot run without a
keyboard is a file you cannot check automatically, and this course checks
everything it teaches.

---

## Why this course exists

Most Python tutorials stop at `print("Hello World")`. This one ends with a
program that has 44 predecessors behind it, and every earlier idea has to still
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
| 39 | an `argparse` CLI, exit codes, stdout vs stderr | driving it from words, and still testing it |
| 40 | `pytest` fixtures and `parametrize`, line coverage | knowing what you have not tested |
| 41 | `pyproject.toml`, a wheel built by hand, offline `pip` | shipping it, and proving it arrived intact |
| 42 | `sqlite3`, a database that is a real file | state that survives, and answers questions |
| 43 | `threading`, locks, daemons, the GIL | many customers at once, without losing an order |
| 44 | `http.server`, `http.client`, JSON over HTTP | the bookshop gets a web API |
| 45 | `argparse` subcommands, flags, exit codes | a CLI that tests itself without a keyboard |

---

## The projects worth reading

If you only read twelve files, read these.

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

### 39 — `the-bookshop-cli.py`
The same shop, driven from a terminal. Seven subcommands, three exit codes, data
on stdout and complaints on stderr — and a 25-test suite that runs in-process,
because `argv` is a list and a list is an ordinary argument.

### 40 — `pytest-and-coverage.py`
The file that runs the test runner. Fixtures, `parametrize`, and the four exit
codes that matter — then `ast` and `trace` measure what actually ran, using
nothing but the standard library. The answer comes back `100%` for a function
that still crashes, which is the whole point.

### 41 — `packaging-a-wheel.py`
The file that ships it. `pyproject.toml` parsed by `tomllib`, a `.whl` built
with `zipfile` and installed by `pip --no-index` with the network switched off,
and a `RECORD` of sha256 digests you recompute yourself — change one byte and
exactly one row breaks.

### 42 — `sqlite-the-bookshop-db.py`
The file that stops pretending. The bookshop's data finally leaves JSON for a
real database — one file, opened by the standard library. It teaches the traps
that cost real hours: a `SELECT` reports `rowcount == -1`, `SUM()` of an empty
set is `NULL` not `0`, a string you build into SQL is code while a `?` is data,
and SQLite will happily store `"not a number"` in an `INTEGER` column. Then it
shows the planner's own report — `SCAN books` becoming `SEARCH books USING
INDEX` — and closes the loop with a `LEFT JOIN` that rescues the member with no
loans via `COALESCE`.

### 43 — `threading-concurrent-customers.py`
The file that serves many customers at once. A `Thread` is a function running
in parallel, `join()` is the only way to wait for it, and threads share memory
— which is the danger. The lesson forces a real race with `Event`s: two
threads both read `0`, both write `1`, and one increment is silently lost,
because `counter += 1` is read, then write, and another thread can slip
between. A `Lock` makes the pair indivisible and the answer `2`. Daemons die
with the process — proven by a child process that starts a 5-second daemon and
finishes in under two seconds — and `ThreadPoolExecutor.map` hands results
back in submission order. The GIL means counting threads take turns, sleeping
threads overlap, and the database from project 42 serves five concurrent
customers through one locked connection.

### 44 — `http-the-bookshop-gets-a-web-api.py`
The file that makes the bookshop speak HTTP. `http.server` with
`BaseHTTPRequestHandler` answers requests: `GET /` returns plain text, `GET
/books` returns JSON, `GET /books?title=Dune` filters by query parameter, and
`POST /books` reads a JSON body to add a book. Status codes matter: `200`,
`404`, `405`, `500`. The server binds to port 0 so the OS picks a free port,
and `log_message` is redirected into a diary so stderr stays empty. Both
`urllib.request` and `http.client` are used to prove the same conversation,
and `server.shutdown()` plus `server_close()` releases the port. The diary
shows that an error request logs twice — a small but real detail of the
standard library.

### 45 — `argparse-the-bookshop-cli.py`
The file that closes the loop. `argparse` reads `sys.argv` and hands back an
object with attributes: `store_true` flips a boolean, `choices` refuses what
you did not plan for, `nargs='+'` collects a list, `type=int` turns text into
numbers, and the help text is part of the contract. Subcommands split the
verbs — `report`, `add-book`, `sell-book` — each with its own arguments. The
real lesson is the exit code: `0` worked, `1` the program refused the input,
`2` argparse did not understand it. So the CLI is tested by calling
`main(['unknown'])` with a list instead of a keyboard, and argparse's own
usage message is captured so even a failing run leaves stderr empty.

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

**a context manager makes "save only if nothing broke" a language feature.**
`__enter__` loads, `__exit__` saves — but only when `exc_type is None`, and it
returns `False` so the original exception still escapes. This is the `34` bug
solved structurally rather than by remembering.

**`argv` is just a list of strings.** That single fact is what makes a terminal
program testable: `main(["report", "--state", path])` is an ordinary function
call. Project 39 runs its entire suite with no subprocess, no keyboard, and no
flake. Never call `sys.exit()` inside `main()` — return the code, and let the
last line of the file do the exiting.

**The exit code is the part your shell actually reads.** Bash, `make` and every
CI system branch on it; none of them read your error message. A program that
prints an error and exits `0` is lying with a straight face. Convention here:
`0` worked, `1` your program understood the command and refused it, `2` argparse
could not understand the command at all.

**The one trap in project 39 that costs real money.** If a shared option lives
on the main parser *and* on every subparser, a value given before the command is
parsed correctly and then **silently overwritten** by the subparser's default:

```
bookshop --state given.json report   ->   exit 0, uses shop.json
```

No warning, wrong file. The fix is `default=argparse.SUPPRESS` on the shared
copy, so it only sets the attribute when it actually saw the flag. And never
golden-test argparse's help text — it re-wraps itself to the terminal width, so
assert on the exit code instead.

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

**pytest runs inside your own process.** `pytest.main([...])` returns an exit
code instead of exiting, so one process can run a dozen suites, capture their
output, and print its own results. Four codes cover everything: `0` green, `1`
red, `5` nothing to run, `4` a flag pytest never heard of. One trap follows
from running in-process: the test modules stay imported, so rewriting a file
and running it a second time runs the *old* tests. A fresh file name per
scenario — or a `sys.modules.pop()` — is the fix.

**Line coverage counts lines, never paths.** `ast` says what *could* run,
`trace` says what *did* run, and the difference is your homework list. Project
40 computes `10 of 12 = 83%` with the standard library alone, and the same
numbers come out of `coverage.py` — verified line for line, not approximately.

**One hundred percent is still compatible with a broken function.** Every line
of `average()` runs when you hand it a happy list, so it measures `5 of 5`.
Then `average([])` dies with `ZeroDivisionError` — on a line that was already
marked covered. A percentage is a spotlight, not a scoreboard.

**A wheel is a zip you are allowed to open.** `.whl` means nothing to Python
and everything to `zipfile`: your package plus a `name-version.dist-info`
folder holding `METADATA`, `WHEEL`, `entry_points.txt` and `RECORD`. Build one
by hand and `pip install --no-index` accepts it, because pip never needed a
server — it needed a file. One rule the zip will not forgive: entry names use
`/`, and `os.path.join` hands you `\` on Windows.

**`RECORD` is the difference between a file and a promise.** Every row is a
path, a sha256 and a size. Recompute them and the wheel proves it is unchanged;
edit one byte inside it and exactly one row goes red. Integrity that only
someone else can check is not integrity.

**The version lives in three places and one of them is the truth.**
`pyproject.toml`, `__version__` in the code, and
`importlib.metadata.version()` reading the installed `.dist-info`. They agree
in this lesson — and when they do not, the installed one is what every other
tool believes.

**A database is a file with rules, and the rules are data.** `sqlite3` opens a
real file, and `PRAGMA table_info` hands the schema back as ordinary rows —
name, type, `notnull`, default, primary key — so the structure of your data is
queryable like the data itself. Three traps follow from how SQLite actually
works. First, `rowcount` counts rows *changed*: an `INSERT` reports `1`, but a
`SELECT` reports `-1`, because it changed nothing. Second, aggregates over an
empty set are `NULL` — `COUNT()` returns `0`, but `SUM()`, `AVG()` and `MIN()`
return `None`, and `COALESCE` is the rescue. Third, columns are a preference,
not a cage: store `"not a number"` in an `INTEGER` column and SQLite keeps it
as `TEXT`, which `typeof()` will happily confess.

**A value is data, and a string you build is code.** `"SELECT ... WHERE title
= '" + guess + "'"` turns `' OR 1=1 --` into a query that matches every row.
The `?` placeholder sends the value separately, so the same string matches
nothing. This is the one rule with no exception: never build SQL by
concatenation.

**The planner will tell you what it did.** `EXPLAIN QUERY PLAN` reports
`SCAN books` before an index exists and `SEARCH books USING INDEX
idx_books_title (title=?)` after — the same query, a different plan, and the
proof that an index is a shortcut the planner can take, not a magic wand.

**A transaction is all-or-nothing.** Rows you `INSERT` and never `commit` are
gone after `rollback` — or after the connection closes. The file database
proves it: reopen the file and only the committed rows are there. And the
lesson's own database lives in a temporary folder that is deleted when the
file finishes, so the course still leaves nothing behind.

**A thread is a function running in parallel, and `join()` is the only way
to wait for it.** `start()` returns immediately; `is_alive()` tells you
whether the function is still running; `join()` blocks until it is done. A
thread that is never joined is a thread you cannot trust to have finished.

**Threads share memory, and that is the danger.** `counter += 1` is not one
step: it is read, then write, and another thread can slip between the two.
Project 43 forces that exact interleaving with `Event`s — both threads read
`0`, both write `1`, and one increment is silently lost. A `Lock` makes the
read-modify-write one indivisible step, and the answer becomes `2`. The race
is not a theory: it is reproduced on every run, on purpose.

**A daemon thread dies with the process.** It is a servant, not a partner:
if `main` finishes first, the daemon is killed without warning. The lesson
proves it with a child process that starts a 5-second daemon and finishes in
under two seconds — the process did not wait, because daemons are not waited
for. A daemon can still be woken and joined like any other thread, if someone
sets its event.

**`ThreadPoolExecutor.map` returns results in submission order.** The workers
finish in whatever order the scheduler chooses; the results come back in the
order you submitted them. That is the difference between a pool and a
free-for-all.

**The GIL lets exactly one thread run Python bytecode at a time.** Counting
threads take turns — which is why a `Lock` around a counter is cheap and
correct. Sleeping threads overlap, because `sleep` releases the GIL: two
0.2-second naps in parallel finish in about half the time of two in sequence.
I/O-bound threads do overlap; CPU-bound Python does not.

**A SQLite connection belongs to the thread that made it.**
`check_same_thread=False` says "I know better" — and the lock is exactly why
you do. Project 43's closing task serves five concurrent customers through
one connection, and every row lands.

**A server is a socket with manners.** `http.server` with
`BaseHTTPRequestHandler` turns a socket into an HTTP server: the request line
is `METHOD path VERSION`, status codes are the whole answer (`200`, `404`,
`405`, `500`), and JSON travels as `application/json`. Query parameters are
just text after `?`, a `POST` carries its data in the body with
`Content-Length`, and `http.client` proves the same conversation as
`urllib.request`. The server binds to port 0 so the OS picks a free port,
`log_message` is redirected into a diary to keep stderr empty, and
`server.shutdown()` plus `server_close()` releases the port. The diary also
shows that `send_error` logs twice — a real detail of the standard library.

---

## Layout

```
python-learning-course/   51 lesson files, in order
Projects/                 45 project files, in order
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
holds itself to 36 tests — none of which can tell you it passed unless it also
demonstrates that it can fail — and can then be driven entirely from a command
line, where the exit code is the part that actually tells the truth. Then you
measure it line by line, get `100%`, and watch one unmeasured input break it
anyway. Finally you build the `.whl` yourself, install it with the network
switched off, and check its sha256 digests by hand — so the program that
started as `print("Hello World")` is now something other people can install.
Then you move the bookshop's data into a real database file, watch a `SELECT`
report `-1` rows changed, rescue a `NULL` sum with `COALESCE`, and read the
planner's own report as it swaps a scan for an index — so the state that
survives is no longer a text file you have to trust, but a database that
answers questions. Finally the shop serves many customers at once: threads
share memory, one increment is lost to prove the race is real, a lock makes
it indivisible, daemons die with the process, and the database from the
previous lesson takes five concurrent orders through one locked connection.
Then it learns to speak HTTP: a tiny server answers `GET /books` with JSON,
filters with query parameters, accepts `POST /books` with a body, returns the
right status codes, and shuts down cleanly — so the program that started as
`print("Hello World")` is now a web API you can talk to with nothing but the
standard library.
