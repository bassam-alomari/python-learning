# -----------------------------------------------------------------
# Lesson 59: default parameters
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : x=..., skipped arguments, order rule, mutable default
#            trap, None sentinel, defaults + *args + keyword-only
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lessons 56 and 57 made every argument mandatory: forget one and
# Python raises TypeError. Default parameters remove that pressure
# for the arguments you can reasonably guess:
#
#   def show_details(name, age=0, country="Unknown"):
#
# If the caller omits age or country, the function does not
# complain -- it uses the values written in the def. The caller
# sends only what they know; the def supplies the rest.
#
# This lesson also covers the one default-parameter bug every
# Python programmer meets exactly once: the mutable default. It
# is worth its own section, because the symptom (a list that
# remembers things between calls) looks like magic until you know
# that defaults are evaluated ONCE, at def time.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] The simplest default: one parameter that can be skipped
# ============================================================
# A parameter with = value in the def becomes optional at the
# call site. The caller may pass it -- or not.

def greet(name, greeting="Hello"):
    print(f"  {greeting}, {name}!")

greet("Osama")
#   Hello, Osama!

greet("Mona", "Hi")
#   Hi, Mona!

# First call: two arguments were not needed, greeting used its
# default. Second call: the caller overrode the default. The
# default is not a special mode -- it is simply "the value to use
# when this slot arrives empty".

# ============================================================
# [2] The transcript's example: show_details with all defaults
# ============================================================
# The transcript defines three parameters, all defaulted. Every
# one can be skipped, so a call with NO arguments still works:

def show_details(name="Unknown", age="Unknown", country="Unknown"):
    print(f"  name:    {name}")
    print(f"  age:     {age}")
    print(f"  country: {country}")

print("no arguments:")
show_details()
# no arguments:
#   name:    Unknown
#   age:     Unknown
#   country: Unknown

print("one argument:")
show_details("Osama")
# one argument:
#   name:    Osama
#   age:     Unknown
#   country: Unknown

print("all three:")
show_details("Mona", 28, "Egypt")
# all three:
#   name:    Mona
#   age:     28
#   country: Egypt

# Three call shapes, one def, zero TypeError. Positional
# arguments still fill left to right: "Osama" lands in name, and
# age and country keep their defaults.

# ============================================================
# [3] Partial defaults: required first, optional after
# ============================================================
# Real functions usually have SOME arguments you must know (a
# name) and some you can guess (a country). The transcript's
# order rule, in code:

def details(name, age=0, country="Unknown"):
    """name is required; age and country may be skipped."""
    print(f"  {name}, {age}, {country}")

details("Osama", 30, "Egypt")
#   Osama, 30, Egypt

details("Mona", 28)
#   Mona, 28, Unknown

details("Sayid")
#   Sayid, 0, Unknown

# Left to right: the first call filled all three slots, the
# second left country on its default, the third left both. The
# caller cannot skip the middle and send only the last without
# naming it (section 5) -- positional matching has no gaps.

# ============================================================
# [4] The order rule: defaults must come LAST
# # ============================================================
# The transcript states it as a law, and Python enforces it at
# DEF time with a SyntaxError. A required parameter after a
# defaulted one has no defined position, so the file refuses to
# start:

# This is a SyntaxError -- never define it:
# def bad_order(name="Unknown", age):    <-- default before required
#     pass

# Python cannot guess which call shape you meant:
#   bad_order("Osama", 30)   -- could be name+age, or just name?
# Positional matching needs a fixed boundary between "required
# zone" and "optional zone", and required-then-default is how you
# draw it.
#
# The legal shapes, in order of preference:

def ok1(name, age=0, country="Unknown"):      # all optional last
    pass

def ok2(name, age, country="Unknown"):        # one optional last
    pass

def ok3(name, age=0, country=0, *, city=""):  # keyword-only after
    pass

# ok3 ends with *, city="..." -- everything after the star is
# keyword-only (lesson 58), and defaults rule there too. The
# SyntaxError only applies to POSITIONAL parameters arriving in
# the wrong order.

# ============================================================
# [5] Skipping the middle: name the argument
# ============================================================
# You cannot positionally skip age and send country -- the first
# unnamed argument fills age, always. Naming the parameter fixes
# it:

details(age=40, name="Hassan")
#   Hassan, 40, Unknown

details(country="Jordan", name="Nadia", age=33)
#   Nadia, 33, Jordan

# Keyword arguments leap over slots. The call on the second line
# reads almost like the def itself -- the reader can see which
# value fills which parameter without counting positions. When
# only SOME parameters have defaults, this is the tool for
# reaching the later ones.

# ============================================================
# [6] The mutable default trap: a list that remembers
# ============================================================
# The famous bug. A default value that is a list (or dict, or
# set) is created ONCE -- when Python reads the def -- and the
# SAME object is reused on every call that skips the argument.

def add_skill_buggy(skills=[]):        # the trap, do not do this
    skills.append("Python")
    print("  buggy sees:", skills)

print("first call:")
add_skill_buggy()
# first call:
#   buggy sees: ['Python']

print("second call:")
add_skill_buggy()
# second call:
#   buggy sees: ['Python', 'Python']

# The second call did NOT start from []. It started from the same
# list the first call left behind -- ['Python'] -- and appended
# again. Call it a third time and you get three Pythons. The
# function has no memory of its own; the DEFAULT does, because
# the default was built once and never rebuilt.
#
# The rule that explains every case in this file:
#
#   the default expression runs ONCE, at def time,
#   and the result is stored on the function object forever

# ============================================================
# [7] The fix: None as the sentinel
# ============================================================
# The standard cure. Use None (or another unique marker) as the
# default, and build the real value INSIDE the body, fresh per
# call:

def add_skill(skills=None):
    """Append Python to a list the CALLER owns, safely."""
    if skills is None:
        skills = []                    # new list, every call
    skills.append("Python")
    return skills

print("first safe call:", add_skill())
# first safe call: ['Python']

print("second safe call:", add_skill())
# second safe call: ['Python']

# Both calls print one element, because each started from a new
# []. The symptom is gone -- but look at what None is doing. It
# does not stand for "no skills"; it stands for "the caller did
# not say". The actual empty list is built when that case is
# detected. That is the sentinel pattern:
#
#   default None means "not provided"
#   body turns "not provided" into a fresh value

# ============================================================
# [8] Why the sentinel pattern also lets the CALLER share data
# # ============================================================
# add_skill's None-sentinel does more than fix the trap: it lets
# a caller pass their OWN list and get it back extended. The
# buggy version could never do that safely.

mine = []
first = add_skill(mine)
second = add_skill(mine)
print("caller's list after two calls:", mine)
# caller's list after two calls: ['Python', 'Python']

print("same object:", first is mine)
# same object: True

# The caller passed a list, so skills was NOT None, the body
# skipped the fresh-list branch, and the append landed on the
# caller's object. One function, two behaviours, chosen by the
# argument:
#
#   add_skill()        -> builds and returns a new list
#   add_skill(mine)    -> extends and returns mine
#
# The buggy version (section 6) could never offer the second
# behaviour -- its default list was shared with EVERYONE.

# ============================================================
# [9] Defaults are evaluated once: watch the clock, not the call
# # ============================================================
# Section 6's rule has a second consequence that shows up even
# with immutable defaults, if you are curious what Python does
# at def time. Prove it with a value you can observe:

marks = []
def remember(mark, store=marks):       # default IS the list object
    store.append(mark)
    return store

remember(10)
print("store grew:", marks)
# store grew: [10]

# remember's default parameter and the name marks point at the
# SAME list. Appending through the parameter changed the outer
# variable, because there was only ever one list. Delete the
# default from your memory and use None:
#
#   def remember(mark, store=None):
#       if store is None:
#           store = []
#       store.append(mark)
#       return store
#
# Now store=None means "fresh list each time", and passing a real
# list still works. Same shape as add_skill -- because it IS the
# same shape. Every mutable-default bug in Python is this one
# bug.

# ============================================================
# [10] None is also the honest default for "no value yet"
# # ============================================================
# Sometimes None is not a workaround -- it is the RIGHT answer.
# "The user has not set a phone number" is None, not "" and not
# 0. Defaults that mean what they say:

def contact(name, phone=None, email=None):
    """Return a contact record; unset fields stay None."""
    return {"name": name, "phone": phone, "email": email}

osama = contact("Osama", phone="01000000000")
mona = contact("Mona", email="mona@example.com")
sayid = contact("Sayid")

print("osama:", osama)
# osama: {'name': 'Osama', 'phone': '01000000000', 'email': None}

print("mona:", mona)
# mona: {'name': 'Mona', 'phone': None, 'email': 'mona@example.com'}

print("sayid:", sayid)
# sayid: {'name': 'Sayid', 'phone': None, 'email': None}

# Three records, each missing a different field, and every field
# still present in the dict with a truthful None. A caller doing
# `if record["email"]:` gets False for sayid without any special
# string to remember ("", "N/A", "-"). The transcript's point
# about flexibility lands here: the function accepts one argument
# or three, and never crashes on the ones you left out.

# ============================================================
# [11] Defaults combined with *args and keyword-only
# # ============================================================
# Lesson 58's three shapes, now with defaults where they belong:

def order(item, *extras, rush=False, note=""):
    """Fixed item, any extras, two keyword-only switches."""
    print(f"  item:  {item}")
    print(f"  extras: {extras}")
    print(f"  rush:  {rush}  note: {note!r}")

order("Dune")
#   item:  Dune
#   extras: ()
#   rush:  False  note: ''

order("Dune", "bookmark", "poster")
#   item:  Dune
#   extras: ('bookmark', 'poster')
#   rush:  False  note: ''

order("Dune", "bookmark", rush=True, note="gift wrap")
#   item:  Dune
#   extras: ('bookmark',)
#   rush:  True  note: 'gift wrap'

# Read the def left to right: item has no default (required,
# section 4's rule); *extras gathers any number of positional
# leftovers into a tuple; rush and note are keyword-only with
# defaults. The caller can omit rush and note entirely, send one,
# or send both by name -- the defaults fill any gap. {note!r}
# shows the empty string as '' so you can see it is a string,
# not None.

# ============================================================
# [12] The transcript's protection angle, proved
# # ============================================================
# The transcript closes on why defaults matter: they protect the
# program from forgotten input. Prove it with the two defs side
# by side:

def rigid(name, age):
    print(f"  rigid: {name}, {age}")

def flexible(name, age=0, country="Unknown"):
    print(f"  flexible: {name}, {age}, {country}")

rigid("Osama", 30)
#   rigid: Osama, 30

try:
    rigid("Osama")                      # forget age -> boom
except TypeError as error:
    print("rigid forgot age ->", error)
# rigid forgot age -> rigid() missing 1 required positional argument: 'age'

flexible("Osama")                       # forget both -> fine
#   flexible: Osama, 0, Unknown

# Same caller mistake -- one argument missing. rigid dies with
# TypeError; flexible quietly uses its defaults and returns a
# usable line. That is the flexibility the transcript describes,
# and it is a DESIGN choice, not luck: you decide per parameter
# which failures are recoverable (give it a default) and which
# are bugs worth crashing on (leave it required). A name with no
# default cannot silently become "Unknown" in production data --
# and that is exactly why name stayed required in section 3.

# ============================================================
# [13] The summary
# ============================================================
# A default parameter is a value written into the def that fills
# the slot when the caller sends nothing:
#
#   def f(name, age=0, country="Unknown"):    required, then defaults
#   f("Osama")                age and country use their defaults
#   f("Osama", 30, "Egypt")   all three filled positionally
#   f(country="Jordan", name="Nadia")    names skip slots
#
# The rules, in the order you will need them:
#
#   1. defaults come AFTER required parameters, or SyntaxError
#   2. positional calls fill left to right -- no gaps; use a
#      keyword to reach a later defaulted parameter
#   3. the default is evaluated ONCE at def time, so a list or
#      dict default is one shared object (the trap in section 6)
#   4. the cure is always the same: default None, build the real
#      value fresh inside the body -- the sentinel pattern
#   5. None is also the honest default for "not provided": it
#      keeps every key present and truthful in the record
#   6. after *args, defaults still work -- those parameters are
#      keyword-only, which is where defaults shine brightest
#
# Defaults are the function's way of saying "I can continue
# without that". Used on the right parameters, they turn
# TypeErrors into graceful calls; used on the wrong ones (a
# shared list, a name that should never be silent), they hide
# bugs. The transcript's show_details shape -- required what you
# must know, defaulted what you can guess -- is the line to walk.
