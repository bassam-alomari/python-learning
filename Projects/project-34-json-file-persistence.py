# ============================================================
# PROJECT 34 - Saving and Loading Data with JSON
# ============================================================
# Level: Intermediate
# Topics: the json module, writing and reading files, UTF-8,
#        defensive parsing, validation of loaded data,
#        atomic writes, a file-backed version of project 33
#
# Project 33 built a library system that forgot everything the
# moment it stopped. This project gives it a MEMORY: the state is
# written to a real file and read back on the next run.
#
# That single change turns a demo into a program, and it brings a
# brand new problem. Project 33 never had to ask "what if the file
# is broken?", because there was no file. Now the data arrives from
# OUTSIDE your program, so it can be wrong, half-written, or
# hand-edited. Most of this project is about surviving that.
#
# Nothing here uses input(). The demo writes to a temporary folder
# that it deletes before it finishes, so running this file never
# leaves anything behind in your repository.
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: why json and not repr
# Project 33 could have saved its library with write(str(library)).
# Name one thing that breaks the moment you load that file back.
# (your answer here)

# QUESTION 2: json is NOT python
# Load {"year": "1965"} and you get the STRING "1965", not the
# number. What is the name for this whole category of surprise,
# and what single habit prevents it?
# (your answer here)

# QUESTION 3: keys become strings
# Save a dict whose key is the integer 5. Load it and print the
# key and its type. Why does json do this, and what would it break
# in project 33?
# (your answer here)

# QUESTION 4: the exception that disappears
# In try/except JSONDecodeError as err, the name err does not
# exist after the except block ends. Why, and what do you write
# if you need the message afterwards?
# (your answer here)

# QUESTION 5: an empty file
# A brand new file is zero bytes. What does json.load raise on it,
# and should your program treat that as corrupt or as a fresh
# start?
# (your answer here)

# QUESTION 6: trust nothing
# You validated the file before saving it, so why validate again
# on the way in? Name two things that can differ.
# (your answer here)

# QUESTION 7: atomic write
# Explain the two step save: write to library.json.tmp, then
# os.replace onto library.json. What does the reader see if the
# program crashes halfway through the first write?
# (your answer here)

# QUESTION 8: encoding
# Why pass encoding="utf-8" to every open()? What happens on a
# Windows machine that does not?
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Write save_library(library, path) that dumps the dict
# with indent=2 and returns the number of characters written.
# Save a two book library and print the count
# (your code here)

# TASK 2: Write load_library(path) that returns an EMPTY dict when
# the file does not exist, and the parsed dict when it does. Print
# both cases: a missing path and a real one
# (your code here)

# TASK 3: Write load_library_safe(path) that also survives a
# CORRUPT file by catching JSONDecodeError and returning an empty
# dict. Write a deliberately broken file and show that it is
# refused without crashing
# (your code here)

# TASK 4: Write looks_like_library(data) returning (True, "ok") or
# (False, reason). Test it against a good dict, a list, a record
# missing "copies", and a record whose copies is a string
# (your code here)

# TASK 5: Write a save that is ATOMIC: dump to path + ".tmp",
# then os.replace it onto path. Prove the temporary file no longer
# exists afterwards
# (your code here)

# TASK 6: Write a counter that survives a restart with
# read_id(path) and write_id(path, value). Load it, add one, save
# it, load it again and print all three numbers to prove the state
# survived the file
# (your code here)

# TASK 7: Take project 33's borrow, give_back and make_member and
# make them work on a SAVED library: load it, run the actions,
# save it, then load it fresh and print what the shelf looks like
# after a restart
# (your code here)

# TASK 8: Write merge_saved(library, path) that loads what is on
# disk and adds only the titles that are missing from the passed
# library, without overwriting anything. Prove that a title already
# on disk keeps its copies
# (your code here)

# TASK 9: Write a corrupt_file_repair(path) that reads a broken
# file, moves it aside to path + ".bak" using os.replace, and
# returns a fresh empty dict, so the operator still has the
# evidence. Show the backup existing afterwards
# (your code here)

# TASK 10: Write the full demo. Create a temporary folder, build a
# four book library with project 33's helpers, save it, delete
# the in-memory copy, load it back, let two members borrow and
# return, save again, load a THIRD time and print the shelf. Show
# that the total number of copies is unchanged, then delete the
# temporary folder and print that it is gone
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.

import json
import os
import shutil
import tempfile

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
print("Q1  repr() has no quotes on the keys, so loads fails at once")
print("Q1  and it can even run code, which a data file must never do")
# Q1  repr() has no quotes on the keys, so loads fails at once
# Q1  and it can even run code, which a data file must never do
# repr({'dune': 1}) prints {'dune': 1} with no quotes anywhere, and
# eval()ing that is a security hole. json is not just prettier, it is
# the format that can only ever mean data.

# QUESTION 2
probe = json.loads('{"year": "1965"}')
print("Q2  loads keeps the type it was GIVEN ->", repr(probe["year"]), type(probe["year"]).__name__)
print("Q2  the habit: validate every loaded value, never trust it")
# Q2  loads keeps the type it was GIVEN -> '1965' str
# Q2  the habit: validate every loaded value, never trust it
# json never guesses. "1965" with quotes must stay a string, because
# the file could have meant a postcode. Guessing would be convenient
# and wrong.

# QUESTION 3
round_trip = json.loads(json.dumps({5: "int key"}))
only_key = list(round_trip)[0]
print("Q3  the key came back as", repr(only_key), type(only_key).__name__)
print("Q3  json only allows string keys, so numbers become text")
# Q3  the key came back as '5' str
# Q3  json only allows string keys, so numbers become text
# The JSON spec has no integer keys. Project 33 looks books up by a
# title, which is already a string, so it survives. An id keyed by
# int would not, and library[5] would raise KeyError after a reload.

# QUESTION 4
print("Q4  Python DELETES the exception name when the block ends")
print("Q4  so read err.msg INSIDE the block, or return it")
# Q4  Python DELETES the exception name when the block ends
# Q4  so read err.msg INSIDE the block, or return it
# This exists so a stale large traceback is not kept alive for the
# rest of the function. It deletes the name, not the exception, so
# keeping what you need is the fix:
#     except json.JSONDecodeError as err:
#         return {}, err.msg

# QUESTION 5
blank = os.path.join(tempfile.gettempdir(), "p34_question5.json")
with open(blank, "w", encoding="utf-8") as handle:
    handle.write("")
try:
    with open(blank, encoding="utf-8") as handle:
        json.load(handle)
    print("Q5  an empty file loaded fine")
except json.JSONDecodeError as err:
    print("Q5  an empty file raises ->", err.msg)
    print("Q5  treat it as a FRESH START, not as corruption")
os.remove(blank)
# Q5  an empty file raises -> Expecting value
# Q5  treat it as a FRESH START, not as corruption
# A file you just created with open(..., "w") is empty on purpose.
# Calling that corruption would make a first run impossible.

# QUESTION 6
print("Q6  the file may be older than this program, or hand edited")
print("Q6  so check the SHAPE on load, not just on save")
# Q6  the file may be older than this program, or hand edited
# Q6  so check the SHAPE on load, not just on save
# Save side validation only proves the file was good when it left.
# It says nothing about what happened in between.

# QUESTION 7
print("Q7  the reader sees the OLD file, because .tmp is never read")
print("Q7  a half written library.json would be unreadable json")
# Q7  the reader sees the OLD file, because .tmp is never read
# Q7  a half written library.json would be unreadable json
# os.replace is the atomic step. Readers only ever point at the real
# name, so they see either all of the new file or all of the old.

# QUESTION 8
print("Q8  utf-8 is the json default, so omitting it is a real risk")
print("Q8  on Windows the default may be cp1252 and mangle the names")
# Q8  utf-8 is the json default, so omitting it is a real risk
# Q8  on Windows the default may be cp1252 and mangle the names
# json writes UTF-8 by default when you give it a file you opened
# yourself, but open() decides the encoding, not json. Omit it and
# Windows may hand back cp1252 instead, and then no error is raised
# at all: the title simply comes back as something else.
# A title like "Cafe" written as UTF-8 and read back as cp1252
# comes out as "CafÃ©", and nothing raises. Silent corruption is
# the worst kind, because the file still loads.

print("-" * 60)

# TASK 1
def save_library(library, path):
    """Write the library to path as pretty JSON. Return the length."""
    text = json.dumps(library, indent=2, ensure_ascii=False, sort_keys=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return len(text)


work = tempfile.mkdtemp(prefix="p34_")
shelf = os.path.join(work, "library.json")

small = {
    "dune": {"author": "Frank Herbert", "year": 1965, "copies": 3},
    "python crash course": {"author": "Eric Matthes", "year": 2019, "copies": 2},
}
written = save_library(small, shelf)
print("T1  characters written ->", written)
print("T1  the file is now  ->")
with open(shelf, encoding="utf-8") as handle:
    for line in handle.read().splitlines():
        print("      " + line)
# T1  characters written -> 180
# T1  the file is now  ->
#       {
#         "dune": {
#           "author": "Frank Herbert",
#           "copies": 3,
#           "year": 1965
#         },
#         "python crash course": {
#           "author": "Eric Matthes",
#           "copies": 2,
#           "year": 2019
#         }
#       }
# indent=2 makes a diff readable, sort_keys=True keeps the order
# stable so a save that changed nothing produces no diff at all,
# and ensure_ascii=False keeps a title like "Café" as itself
# instead of the escape CafÃ©.

# TASK 2
def load_library(path):
    """Return the parsed dict, or an empty dict when absent."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


print("T2  a missing file   ->", load_library(os.path.join(work, "nope.json")))
print("T2  the real file    ->", sorted(load_library(shelf)))
# T2  a missing file   -> {}
# T2  the real file    -> ['dune', 'python crash course']
# Returning {} for a missing file is what lets a first run simply
# start empty instead of crashing on step one.

# TASK 3
def load_library_safe(path):
    """Survive both a missing file and a corrupt one."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as err:
        # err only exists INSIDE this block, so read it here.
        print(f"      refused the file: {err.msg} (line {err.lineno})")
        return {}


broken = os.path.join(work, "broken.json")
with open(broken, "w", encoding="utf-8") as handle:
    handle.write("{ this is not json")
print("T3  a corrupt file   ->", load_library_safe(broken))
print("T3  the good file    ->", sorted(load_library_safe(shelf)))
# T3  a corrupt file   -> {}
#       refused the file: Expecting property name enclosed in double quotes (line 1)
# T3  the good file    -> ['dune', 'python crash course']
# Notice the refusal is REPORTED and then the program carries on with
# an empty library. Swallowing the error silently would be worse than
# the crash, because the user would never learn their data is gone.

# TASK 4
def looks_like_library(data):
    """Return (True, 'ok') or (False, the first reason it failed)."""
    if not isinstance(data, dict):
        return False, "the top level must be a dict"
    for title in sorted(data):
        record = data[title]
        if not isinstance(record, dict):
            return False, f"the record of {title!r} must be a dict"
        for field in ("author", "year", "copies"):
            if field not in record:
                return False, f"{title!r} is missing {field}"
        if not isinstance(record["copies"], int):
            return False, f"{title!r} has a non-int copies"
        if isinstance(record["copies"], bool):
            return False, f"{title!r} has a bool copies"
    return True, "ok"


cases = [
    ("good", small),
    ("a list", [1, 2, 3]),
    ("missing copies", {"dune": {"author": "H", "year": 1965}}),
    ("copies is text", {"dune": {"author": "H", "year": 1965, "copies": "two"}}),
]
for label, data in cases:
    ok, reason = looks_like_library(data)
    print(f"T4  {label:16} -> {ok}, {reason}")
# T4  good             -> True, ok
# T4  a list           -> False, the top level must be a dict
# T4  missing copies   -> False, 'dune' is missing copies
# T4  copies is text   -> False, 'dune' has a non-int copies
# The bool check comes last on purpose, because bool is a subclass
# of int in Python, so isinstance(True, int) is True. A file holding
# true would slip past a plain int check and then behave like a
# count of 1, which is exactly the kind of quiet bug to catch at the
# door instead of three functions later.

# TASK 5
def save_atomic(library, path):
    """Write to path + '.tmp', then swap it onto path in one step."""
    text = json.dumps(library, indent=2, ensure_ascii=False, sort_keys=True)
    temporary = path + ".tmp"
    with open(temporary, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(temporary, path)
    return len(text)


atomic_path = os.path.join(work, "atomic.json")
save_atomic(small, atomic_path)
print("T5  the real file exists   ->", os.path.isfile(atomic_path))
print("T5  the .tmp is gone       ->", not os.path.exists(atomic_path + ".tmp"))
print("T5  it still loads         ->", sorted(load_library(atomic_path)))
# T5  the real file exists   -> True
# T5  the .tmp is gone       -> True
# T5  it still loads         -> ['dune', 'python crash course']
# If the program died between the two lines, the old file is still
# intact and only a .tmp is left over. That leftover is harmless, and
# a crash DURING os.replace cannot happen, because it is a single
# rename inside the operating system.

# TASK 6
def write_id(path, value):
    save_atomic({"last_id": value}, path)


def read_id(path):
    """Return the stored counter, or 0 when there is nothing yet."""
    if not os.path.exists(path):
        return 0
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError:
        return 0
    value = data.get("last_id")
    if not isinstance(value, int):
        return 0
    return value


counter_path = os.path.join(work, "counter.json")
before = read_id(counter_path)
value = before + 1
write_id(counter_path, value)
after = read_id(counter_path)
print("T6  before   ->", before)
print("T6  saved    ->", value)
print("T6  reloaded ->", after)
print("T6  it survived the file ->", after == value)
# T6  before   -> 0
# T6  saved    -> 1
# T6  reloaded -> 1
# T6  it survived the file -> True
# A missing file, a corrupt file and a wrong type all give 0 rather
# than an exception, so this one helper can sit at the top of any
# program that needs a starting value.

# TASK 7
class LibraryError(Exception):
    """Raised when a library action cannot be completed."""


def borrow(library, title, copies=1):
    """Take copies out of a library dict that is already in memory."""
    if title not in library:
        raise LibraryError(f"'{title}' is not in the library")
    if library[title]["copies"] < copies:
        raise LibraryError(f"only {library[title]['copies']} copies of '{title}' are left")
    library[title]["copies"] -= copies
    return f"borrowed {copies} of '{title}'"


def give_back(library, title, copies=1):
    """Put copies back."""
    if title not in library:
        raise LibraryError(f"'{title}' is not in the library")
    library[title]["copies"] += copies
    return f"returned {copies} of '{title}'"


def make_member(library):
    """Return (take, give_back, my_loans) closing over one member."""
    loans = {}

    def take(title):
        if title not in library:
            return "not in the library"
        if library[title]["copies"] < 1:
            return "no copies left"
        library[title]["copies"] -= 1
        loans[title] = loans.get(title, 0) + 1
        return f"took '{title}'"

    def give_back_member(title):
        if title not in loans:
            return "you did not take it"
        loans[title] -= 1
        library[title]["copies"] += 1
        if loans[title] == 0:
            del loans[title]
        return f"returned '{title}'"

    def my_loans():
        return dict(loans)

    return take, give_back_member, my_loans


def total_copies(library):
    """The invariant that proves nothing was lost."""
    running = 0
    for title in library:
        running += library[title]["copies"]
    return running


saved_path = os.path.join(work, "saved_library.json")
save_library(small, saved_path)

restarted = load_library(saved_path)
print("T7  loaded after a restart ->", sorted(restarted))
sara_take, sara_give, sara_has = make_member(restarted)
ali_take, ali_give, ali_has = make_member(restarted)
print("T7  Sara ->", sara_take("dune"))
print("T7  Ali  ->", ali_take("dune"))
save_library(restarted, saved_path)

fresh = load_library(saved_path)
print("T7  the shelf now         ->", {t: fresh[t]["copies"] for t in sorted(fresh)})
print("T7  the file remembers    ->", fresh["dune"]["copies"] == 1)
# T7  loaded after a restart -> ['dune', 'python crash course']
# T7  Sara -> took 'dune'
# T7  Ali  -> took 'dune'
# T7  the shelf now         -> {'dune': 1, 'python crash course': 2}
# T7  the file remembers    -> True
# borrow and give_back did not change at all. They already worked on
# a plain dict, so making the program persistent needed no new logic
# here, only load before and save after. That is the payoff of
# keeping the data in a plain dict in project 33.

# TASK 8
def merge_saved(library, path):
    """Add only the titles that are missing from the file."""
    on_disk = load_library_safe(path)
    added = []
    for title in sorted(library):
        if title not in on_disk:
            on_disk[title] = library[title]
            added.append(title)
    if added:
        save_atomic(on_disk, path)
    return added


merging = os.path.join(work, "merge.json")
save_atomic(small, merging)
incoming = {
    "dune": {"author": "Frank Herbert", "year": 1965, "copies": 99},
    "clean code": {"author": "Robert Martin", "year": 2008, "copies": 2},
}
added = merge_saved(incoming, merging)
after_merge = load_library(merging)
print("T8  the titles added ->", added)
print("T8  dune kept its own copies ->", after_merge["dune"]["copies"])
print("T8  the shelf now    ->", {t: after_merge[t]["copies"] for t in sorted(after_merge)})
# T8  the titles added -> ['clean code']
# T8  dune kept its own copies -> 3
# T8  the shelf now    -> {'clean code': 2, 'dune': 3, 'python crash course': 2}
# The incoming dune claimed 99 copies and was ignored completely,
# because the title already exists. An upsert that overwrites would
# have invented 99 books out of nothing.

# TASK 9
def corrupt_file_repair(path):
    """Move a broken file aside and start fresh, keeping the evidence."""
    if not os.path.exists(path):
        return {}, "nothing to repair"
    try:
        with open(path, encoding="utf-8") as handle:
            json.load(handle)
    except json.JSONDecodeError as err:
        reason = err.msg
        backup = path + ".bak"
        os.replace(path, backup)
        return {}, f"moved the broken file to {os.path.basename(backup)} ({reason})"
    return load_library_safe(path), "the file was already fine"


damaged = os.path.join(work, "damaged.json")
with open(damaged, "w", encoding="utf-8") as handle:
    handle.write('{"dune": {"copies": 2},')
recovered, note = corrupt_file_repair(damaged)
print("T9  the note ->", note)
print("T9  recovered ->", recovered)
with open(damaged + ".bak", encoding="utf-8") as handle:
    print("T9  the backup holds the evidence ->", handle.read())
print("T9  the original path is now free ->", not os.path.exists(damaged))
# T9  the note -> moved the broken file to damaged.json.bak (Expecting property name enclosed in double quotes)
# T9  recovered -> {}
# T9  the backup holds the evidence -> {"dune": {"copies": 2},
# T9  the original path is now free -> True
# Deleting a file the user cannot recover is rude and unsafe. Moving
# it aside means the program can start immediately AND the owner can
# still open the broken file in a text editor to see what happened.

# TASK 10
def full_demo():
    """Persistence end to end, in a folder we clean up afterwards."""
    room = tempfile.mkdtemp(prefix="p34demo_")
    print("T10 a private folder was created ->", os.path.isdir(room))
    try:
        path = os.path.join(room, "library.json")

        start = {
            "dune": {"author": "Frank Herbert", "year": 1965, "copies": 3},
            "children of dune": {"author": "Frank Herbert", "year": 1979, "copies": 2},
            "clean code": {"author": "Robert Martin", "year": 2008, "copies": 2},
            "python crash course": {"author": "Eric Matthes", "year": 2019, "copies": 1},
        }
        opening_total = total_copies(start)
        save_atomic(start, path)
        print("T10 saved 4 titles, copies ->", opening_total)

        # Throw the in-memory copy away. Everything below must come
        # back from the file alone.
        start = None
        library = load_library_safe(path)
        print("T10 after a restart      ->", sorted(library))
        print("T10 copies read back     ->", total_copies(library))

        sara_take, sara_give, sara_has = make_member(library)
        ali_take, ali_give, ali_has = make_member(library)

        actions = [
            sara_take("dune"),
            sara_take("dune"),
            ali_take("dune"),
            ali_take("dune"),
            sara_give("dune"),
            sara_give("dune"),
            ali_take("dune"),
            ali_take("clean code"),
            ali_give("dune"),
            ali_give("clean code"),
            ali_give("dune"),
        ]
        for step, message in enumerate(actions, 1):
            print(f"T10   step {step} -> {message}")

        save_atomic(library, path)
        print("T10 Sara's loans ->", sara_has())
        print("T10 Ali's loans  ->", ali_has())

        third_read = load_library_safe(path)
        shelf = {title: third_read[title]["copies"] for title in sorted(third_read)}
        print("T10 the shelf after restart ->", shelf)
        print("T10 copies at the end       ->", total_copies(third_read))
        print("T10 unchanged?              ->", total_copies(third_read) == opening_total)

        # Prove the file is real by showing its first line.
        with open(path, encoding="utf-8") as handle:
            print("T10 the file starts with    ->", handle.readline().rstrip())
    finally:
        shutil.rmtree(room, ignore_errors=True)
    print("T10 the folder is gone      ->", not os.path.isdir(room))


if __name__ == "__main__":
    full_demo()
shutil.rmtree(work, ignore_errors=True)

# T10 a private folder was created -> True
# T10 saved 4 titles, copies -> 8
# T10 after a restart      -> ['children of dune', 'clean code', 'dune', 'python crash course']
# T10 copies read back     -> 8
# T10   step 1 -> took 'dune'
# T10   step 2 -> took 'dune'
# T10   step 3 -> took 'dune'
# T10   step 4 -> no copies left
# T10   step 5 -> returned 'dune'
# T10   step 6 -> returned 'dune'
# T10   step 7 -> took 'dune'
# T10   step 8 -> took 'clean code'
# T10   step 9 -> returned 'dune'
# T10   step 10 -> returned 'clean code'
# T10   step 11 -> returned 'dune'
# T10 Sara's loans -> {}
# T10 Ali's loans  -> {}
# T10 the shelf after restart -> {'children of dune': 2, 'clean code': 2, 'dune': 3, 'python crash course': 1}
# T10 copies at the end       -> 8
# T10 unchanged?              -> True
# T10 the file starts with    -> {
# T10 the folder is gone      -> True
# The three dunes go out in steps 1 to 3, so step 4 is refused with a
# clean message instead of a crash. Steps 5 and 6 hand them all back,
# and the last four steps borrow and return again. Every book ends
# on the shelf, which is the same invariant that closed project 33,
# now surviving a restart from disk.
#
# The try/finally matters: even if an action raised, shutil.rmtree
# still runs, so the demo never leaves a folder in your temp
# directory. The copy count returns to 8, which is the same
# invariant that closed project 33, now surviving a restart.

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 34")
print("=" * 60)
# ============================================================
# END OF PROJECT 34
# ============================================================