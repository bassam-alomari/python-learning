# -----------------------------------------------------------------
# Lesson 61: packing and unpacking in action (full practice)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : one def with name + *skills + **progress,
#            walking the tuple, walking the dict, every call shape,
#            unpacking lists and dicts at the call site,
#            the double-nesting trap
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# This lesson is the practice drill for lessons 58 to 60. The
# transcript's idea is one function that collects a fixed name,
# an unlimited list of plain skills (*skills), and an unlimited
# set of keyword skills with progress (**progress). Everything
# else in this file is that function, exercised from every angle
# -- different call shapes, unpacking lists and dicts into it,
# and the two traps that catch people who forget the stars at
# the call site.
#
# If you can read every section here without surprise, the
# packing/unpacking half of the functions block is done.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] The full signature: fixed + star + double-star
# ============================================================
# One required positional (name), then *skills to gather plain
# values into a tuple, then **progress to gather keywords into a
# dict. That is the complete shape from lessons 58 and 60,
# combined exactly as the transcript describes:

def profile(name, *skills, **progress):
    print(f"  name:     {name}")
    print(f"  skills:   {skills}")
    print(f"  progress: {progress}")

profile("Osama")
#   name:     Osama
#   skills:   ()
#   progress: {}

# Nothing extra was passed, so both collectors came back empty --
# the same emptiness seen in lesson 60's inventory. The function
# still runs; no TypeError, because nothing was actually required
# beyond the name.

profile("Osama", "html", "css", "js")
#   name:     Osama
#   skills:   ('html', 'css', 'js')
#   progress: {}

# Four positionals after the name: the first fills nothing else,
# the rest are gathered -- same rule as lesson 58. One name, one
# tuple, one dict. That is the whole machine.

# ============================================================
# [2] Walk the tuple: for loop over *skills
# ============================================================
# The transcript's first practical step. The tuple is ordinary
# (lessons 12, 22, 25), so the same for loop works:

def show_skills(name, *skills):
    print(f"  {name}'s skills:")
    if not skills:
        print("    (none listed)")
        return
    for skill in skills:
        print(f"    - {skill}")

show_skills("Osama", "html", "css", "js")
#   Osama's skills:
#     - html
#     - css
#     - js

show_skills("Mona")
#   Mona's skills:
#     (none listed)

# The guard `if not skills:` is the same empty-collection guard
# from lesson 58 -- empty tuple is falsy, so one line covers the
# "no skills at all" case before the loop ever starts.

# ============================================================
# [3] Walk the dict: for loop over **progress
# ============================================================
# The transcript's second practical step. Keys and values, same
# items() loop as lessons 52 to 55 and 60:

def show_progress(name, **progress):
    print(f"  {name}'s progress:")
    if not progress:
        print("    (no progress recorded)")
        return
    for skill, value in progress.items():
        print(f"    {skill:<8} {value}%")

show_progress("Osama", html=90, css=80, js=70)
#   Osama's progress:
#     html     90%
#     css      80%
#     js       70%

show_progress("Mona")
#   Mona's progress:
#     (no progress recorded)

# Identical structure to section 2 -- the only difference is the
# data shape: a tuple walked by value, a dict walked by
# key, value. Same loop syntax, same guard pattern.

# ============================================================
# [4] Both collectors in one def: the transcript's full shape
# ============================================================
# Now combine sections 2 and 3 into the single function the
# transcript asks for. Plain skills print as a list; keyword
# skills print as a percentage table:

def full_profile(name, *skills, **progress):
    print(f"  {name}")
    if skills:
        print("    known:")
        for skill in skills:
            print(f"      - {skill}")
    else:
        print("    known: (nothing listed)")
    if progress:
        print("    measured:")
        for skill, value in progress.items():
            print(f"      {skill:<8} {value}%")
    else:
        print("    measured: (nothing measured)")

full_profile("Osama", "html", "css", html=90, css=80)
#   Osama
#     known:
#       - html
#       - css
#     measured:
#       html     90%
#       css      80%

full_profile("Mona", "python", python=95)
#   Mona
#     known:
#       - python
#     measured:
#       python   95%

full_profile("Sayid")
#   Sayid
#     known: (nothing listed)
#     measured: (nothing measured)

# Three calls, three shapes, zero errors. The name is fixed;
# everything after it lands in exactly one of the two buckets,
# decided by whether the caller wrote it with an `=` or not.
# That boundary -- unnamed goes to the tuple, named goes to the
# dict -- is the single rule that makes the whole system work.

# ============================================================
# [5] Call-shape matrix: every legal combination
# ============================================================
# The same function, called every legal way. This is the drill:
# read each shape and predict the two buckets before running:

def buckets(name, *a, **k):
    print(f"  {name:<8} a={a}  k={k}")

buckets("Osama")
#   Osama    a=()  k={}

buckets("Osama", "html")
#   Osama    a=('html',)  k={}

buckets("Osama", html=90)
#   Osama    a=()  k={'html': 90}

buckets("Osama", "html", html=90)
#   Osama    a=('html',)  k={'html': 90}

buckets("Osama", "html", "css", html=90, css=80)
#   Osama    a=('html', 'css')  k={'html': 90, 'css': 80}

# Five shapes, one signature. Note line four: the STRING "html"
# and the KEYWORD html=90 can coexist -- one is a positional
# (goes to the tuple), the other is a keyword (goes to the dict).
# They are different arguments even though they look related.
# The duplicate trap from lesson 60 only fires when the SAME
# keyword is sent twice, not when a string and a keyword share
# a name.

# ============================================================
# [6] Unpacking a list into *skills at the call
# ============================================================
# The transcript's final step: take a list you already hold and
# spread it into the positional collector with one star:

def list_profile(name, *skills):
    print(f"  {name}: {skills}")

my_list = ["html", "css", "js"]
list_profile("Osama", *my_list)
#   Osama: ('html', 'css', 'js')

# Without the star, the list itself would be ONE element of the
# tuple -- section 10 shows that trap. With the star, the three
# strings become three positionals, gathered back into a tuple
# exactly as if the caller had written them by hand. Same rule
# as lesson 58's `inner(*xs)`; the list can grow and the call
# stays correct.

# ============================================================
# [7] Unpacking a dict into **progress at the call
# ============================================================
# The other half: a dict you already hold, spread into the
# keyword collector with two stars:

def dict_profile(name, **progress):
    print(f"  {name}: {progress}")

my_dict = {"html": 90, "css": 80, "js": 70}
dict_profile("Osama", **my_dict)
#   Osama: {'html': 90, 'css': 80, 'js': 70}

# Without the stars, the dict would be ONE positional -- again,
# section 11. With them, its keys become keyword arguments and
# **progress gathers them back. The dict can gain or lose keys
# and the call still works -- that is the flexibility the
# transcript means by "any number of arguments, no errors."

# ============================================================
# [8] Both unpacked at once: the full call
# ============================================================
# One list, one dict, both spread into the same call. This is
# the complete picture the transcript builds toward:

def combined(name, *skills, **progress):
    print(f"  {name}")
    print(f"    skills:   {skills}")
    print(f"    progress: {progress}")

skills_list = ["html", "css", "js"]
progress_dict = {"html": 90, "css": 80, "js": 70}
combined("Osama", *skills_list, **progress_dict)
#   Osama
#     skills:   ('html', 'css', 'js')
#     progress: {'html': 90, 'css': 80, 'js': 70}

# Two stars at the call, two stars in the def, and the data
# arrived as two ordinary Python objects the caller built
# elsewhere -- a list from a loop, a dict from a JSON file, a
# database row, a settings screen. The function does not care
# where they came from; it only sees the unpacked arguments.

# ============================================================
# [9] Realistic: a report built from unpacked data
# ============================================================
# The same shape, doing real work. Data comes in as a list and a
# dict (the way an application would hold it), and the function
# produces a formatted report -- totals, sorted progress, and a
# summary line:

def report(name, *skills, **progress):
    """Build one person's skills report from unpacked data."""
    print(f"  === {name} ===")
    print(f"  plain skills ({len(skills)}):")
    if skills:
        for skill in skills:
            print(f"    - {skill}")
    else:
        print("    (none)")
    print(f"  measured ({len(progress)}):")
    if progress:
        for skill, value in sorted(progress.items(), key=lambda kv: kv[1], reverse=True):
            print(f"    {skill:<8} {value}%")
        average = sum(progress.values()) / len(progress)
        print(f"    average:  {average:.1f}%")
    else:
        print("    (none)")
    print()

report("Osama", *["html", "css", "js"], **{"html": 90, "css": 80, "js": 70})
#   === Osama ===
#   plain skills (3):
#     - html
#     - css
#     - js
#   measured (3):
#     html     90%
#     css      80%
#     js       70%
#     average:  80.0%

report("Mona", *["python"], **{"python": 95})
#   === Mona ===
#   plain skills (1):
#     - python
#   measured (1):
#     python   95%
#     average:  95.0%

report("Sayid")
#   === Sayid ===
#   plain skills (0):
#     (none)
#   measured (0):
#     (none)

# Three calls, three data shapes, one function. The sorted-by-
# value loop and the average line are the same tools from
# lessons 52 to 55 and 60 -- packing did not replace them, it
# just changed how the data arrives.

# ============================================================
# [10] Trap: a list WITHOUT the star becomes one element
# ============================================================
# This is the mistake the transcript warns against at the end.
# Passing a list into *skills without unpacking it:

def trap_positional(name, *skills):
    print(f"  {skills}")

trap_positional("Osama", my_list)
#   (['html', 'css', 'js'],)

# One element: the list itself, nested inside the tuple. The
# for loop from section 2 would then iterate once and print the
# whole list as a single "skill." The fix is one character --
# the star:

trap_positional("Osama", *my_list)
#   ('html', 'css', 'js')

# Same function, same list, different call. The star is not
# decoration; it is the instruction to spread.

# ============================================================
# [11] Trap: a dict WITHOUT the stars lands in the tuple
# ============================================================
# Same class of mistake on the keyword side. Passing a dict into
# a function without **:

def trap_keyword(name, *skills, **progress):
    print(f"  skills:   {skills}")
    print(f"  progress: {progress}")

trap_keyword("Osama", my_dict)
#   skills:   ({'html': 90, 'css': 80, 'js': 70},)
#   progress: {}

# The dict became ONE positional -- it went into the tuple, not
# the dict. progress is empty because no keyword arguments were
# sent at all. The fix, again, is the stars:

trap_keyword("Osama", **my_dict)
#   skills:   ()
#   progress: {'html': 90, 'css': 80, 'js': 70}

# One pair of stars moved the same object from the wrong bucket
# to the right one. If you ever see a dict sitting inside a tuple
# in your output, this is the bug -- and this is the fix.

# ============================================================
# [12] The full inventory: every shape in one screen
# ============================================================
# One function, every call shape from this lesson and the two
# before it, side by side:

def inventory(name, *args, **kwargs):
    print(f"  {name:<10} args={args}  kwargs={kwargs}")

inventory("empty")
#   empty      args=()  kwargs={}

inventory("pos", "a", "b")
#   pos        args=('a', 'b')  kwargs={}

inventory("kw", x=1, y=2)
#   kw         args=()  kwargs={'x': 1, 'y': 2}

inventory("both", "a", x=1)
#   both       args=('a',)  kwargs={'x': 1}

inventory("spread-list", *["a", "b"])
#   spread-list args=('a', 'b')  kwargs={}

inventory("spread-dict", **{"x": 1})
#   spread-dict args=()  kwargs={'x': 1}

inventory("spread-both", *["a"], **{"x": 1})
#   spread-both args=('a',)  kwargs={'x': 1}

inventory("nested-trap", ["a", "b"])
#   nested-trap args=(['a', 'b'],)  kwargs={}

# Eight lines, eight shapes, one signature. The last line is the
# trap from section 10, kept visible next to its correct form on
# the line above it. The difference between `*["a", "b"]` and
# `["a", "b"]` is one character and an entirely different tuple.

# ============================================================
# [13] The summary
# ============================================================
# This lesson was one function and every way to call it. The
# rules that made all of it work:
#
#   1. def f(name, *skills, **progress):  -- required first,
#      then the positional collector, then the keyword
#      collector, and nothing plain after either star
#   2. unnamed arguments land in the tuple; named arguments
#      land in the dict; the `=` sign is the boundary
#   3. walk the tuple with `for x in skills`; walk the dict
#      with `for k, v in progress.items()` -- both are ordinary
#      loops on ordinary collections
#   4. *my_list at the call spreads a list into positionals;
#      **my_dict spreads a dict into keywords; without the
#      stars, each becomes ONE element in the wrong bucket
#   5. empty collectors are fine: () and {} are legal values,
#      so a function with collectors can be called with nothing
#      extra at all
#   6. a string and a keyword can share a name without
#      conflict -- "html" as a positional and html=90 as a
#      keyword are two different arguments
#
# The transcript's closing claim is the right one: once this
# shape is comfortable, every function in the projects to come
# that needs "some fixed things, plus anything else the caller
# has" is a variation of what you just practiced. Packing and
# unpacking for both kinds of arguments are now complete.
