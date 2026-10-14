# -----------------------------------------------------------------
# Lesson 60: packing and unpacking keyword arguments (**kwargs)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : ** in the def -> dict, ** at the call -> spread,
#            *args + **kwargs together, identifier trap, collisions
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lesson 58 gave the star one meaning: gather or spread POSITIONAL
# arguments, always as a tuple. This lesson adds the second star:
#
#   in the def    def show(**skills):    PACK   gather keywords
#   in the call   show(**skills):        UNPACK spread a dict
#
# One star collects unnamed values into a TUPLE. Two stars collect
# named values into a DICT. The transcript's example is the whole
# idea in one line -- def show_skills(**skills) receiving
# html=90, css=80, js=70 -- and the rest of this file is that
# idea, the rules that keep it legal, and the traps that break it.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] Two stars in the def: any keywords, one dictionary
# ============================================================
# A parameter starting with ** collects every keyword argument
# the caller sends, into a DICT. Any number of them, any names.

def show_skills(**skills):
    print("packed type:", type(skills).__name__)
    print("packed dict:", skills)

show_skills(html=90, css=80, js=70)
# packed type: dict
# packed dict: {'html': 90, 'css': 80, 'js': 70}

show_skills(python=95)
# packed type: dict
# packed dict: {'python': 95}

show_skills()
# packed type: dict
# packed dict: {}

# Three calls, three dict lengths, one def. The empty call gives
# {} -- the same emptiness lesson 58 saw with the empty tuple.
# Note what the caller wrote: html=90 is a keyword argument,
# exactly like verbose=False in lesson 59, except now there is no
# named slot waiting for it -- the ** collects the overflow.

# ============================================================
# [2] Loop over the packed dict: keys and values
# ============================================================
# The transcript's practical step. The packed value is an
# ordinary dictionary (lessons 30 to 32, 52 to 55), so items()
# works exactly as taught:

def print_skills(**skills):
    for skill, value in skills.items():
        print(f"  {skill:<8} {value}%")

print_skills(html=90, css=80, js=70)
#   html     90%
#   css      80%
#   js       70%

print_skills(python=95, sql=88)
#   python   95%
#   sql      88%

# The loop does not know or care that the data arrived as keyword
# arguments. It sees a dict, it walks a dict. That is the payoff
# of packing into a real data structure instead of a loose list:
# every dictionary tool from earlier lessons is now a keyword
# tool.

# ============================================================
# [3] Unpacking at the call: **my_dict spreads the keys
# ============================================================
# The other direction. You HAVE a dictionary; the function wants
# keyword arguments; two stars at the call site do the split.

def show_pair(skill, value):
    print(f"  {skill:<8} {value}%")

one_skill = {"skill": "html", "value": 90}
show_pair(**one_skill)
#   html     90%

# The dict's two KEYS become the two PARAMETER names. This only
# works because the keys match the def exactly: skill= and value=.
# Section 7 shows what happens when they do not.

# A dict can also be unpacked into a **kwargs function, where the
# keys need no matching names at all:

def collect(**items):
    print("  collected:", items)

my_scores = {"html": 90, "css": 80}
collect(**my_scores)
#   collected: {'html': 90, 'css': 80}

# Spreading my_scores sent html=90 and css=80 as separate keyword
# arguments; collect's ** gathered them back into a dict. One
# star round trip, same values, same order (dictionaries keep
# insertion order -- lesson 30).

# ============================================================
# [4] Two stars together: *args and **kwargs in one def
# ============================================================
# The classic pair. Positional leftovers go to the tuple, keyword
# leftovers go to the dict, and both can be absent:

def order(item, *extras, **options):
    print(f"  item:    {item}")
    print(f"  extras:  {extras}")
    print(f"  options: {options}")

order("Dune")
#   item:    Dune
#   extras:  ()
#   options: {}

order("Dune", "bookmark", "poster")
#   item:    Dune
#   extras:  ('bookmark', 'poster')
#   options: {}

order("Dune", "bookmark", rush=True, gift=True)
#   item:    Dune
#   extras:  ('bookmark',)
#   options: {'rush': True, 'gift': True}

# The boundary is clean: anything UNNAMED after "Dune" lands in
# extras; anything NAMED lands in options. The caller decides
# which bucket by how they write the argument. This pair is what
# built-in functions like print() use (print(*objects, sep=" ",
# end="\n", ...) is the same shape), which is why print accepts
# any number of values AND named switches.

# ============================================================
# [5] Order rule: **kwargs goes last
# ============================================================
# Same law as lesson 58's star, now for the double star. In the
# positional-parameter zone, **kwargs (and *args) close the list:

def ok_order(a, b, *rest, **options):     # legal, and usual
    pass

def ok_order2(a, b=0, **options):         # defaults before ** is fine
    pass

# Both are legal. What is NOT legal is trying to put a plain
# positional parameter after **kwargs -- it would have no
# position to fill:
#
# def bad(**options, a):     <-- SyntaxError
#     pass
#
# And a keyword-only parameter after **kwargs is also SyntaxError
# (there is nothing left for it to be "only" after). The zone
# layout, from lesson 58 onward:
#
#   positional required -> positional defaults -> *args
#   -> keyword-only required -> keyword-only defaults -> **kwargs

# ============================================================
# [6] Trap: keyword names must be usable as identifiers
# # ============================================================
# You cannot write html-90= as a keyword in source -- the hyphen
# breaks the syntax. The same rule applies to what ** unpacking
# SENDS to a function with named parameters:

def needs_html(html):
    print(f"  html is {html}")

needs_html(html=90)
#   html is 90

# That call is fine. But a dict with an invalid identifier as a
# key cannot be unpacked into a function that expects a REAL
# parameter name:

bad_dict = {"html-90": 1}
try:
    needs_html(**bad_dict)
except TypeError as error:
    print("invalid name ->", error)
# invalid name -> needs_html() got an unexpected keyword argument 'html-90'

# The string "html-90" is a perfectly legal dict key -- it just
# cannot name a Python parameter. If the function collects **kwargs
# instead, the odd key is accepted, because no named slot needs
# to match it:

def collect_anything(**items):
    print("  got:", items)

collect_anything(**bad_dict)
#   got: {'html-90': 1}

# Rule of thumb: keys destined for NAMED parameters must be
# valid identifiers (letters, digits, underscore, not starting
# with a digit). Keys destined only for **kwargs can be any
# string.

# ============================================================
# [7] Trap: duplicate keyword -> TypeError
# ============================================================
# If you send a keyword the normal way AND via **dict, Python
# refuses to guess which one wins:

def greet(name):
    print(f"  Hello, {name}!")

try:
    greet(name="Osama", **{"name": "Mona"})
except TypeError as error:
    print("duplicate ->", error)
# duplicate -> __main__.greet() got multiple values for keyword argument 'name'

# Same rule as sending two positionals into one parameter: one
# slot, one value. The error names the parameter, so the fix is
# obvious -- send it one way, not both. The same check applies to
# a **kwargs function if a named keyword collides with a key in
# the dict you unpack:

def collect(name="default", **rest):
    print(f"  name: {name}  rest: {rest}")

try:
    collect(name="Osama", **{"name": "Mona"})
except TypeError as error:
    print("duplicate in kwargs ->", error)
# duplicate in kwargs -> __main__.collect() got multiple values for keyword argument 'name'

# The fix, both times: drop the duplicate from one side. (The
# __main__. prefix in the messages is just the module name -- this
# file is running as a script, so its functions live there.)

# ============================================================
# [8] Realistic: a settings record the page can place anywhere
# ============================================================
# The transcript's "any keywords you want" becomes a record
# builder -- the lesson 56 and 59 pattern, now with unlimited
# fields:

def build_settings(user, **options):
    """Fixed user, then any extra options as a record."""
    record = {"user": user, "theme": "dark"}
    for key, value in options.items():
        record[key] = value
    return record                        # give it back (lesson 56)

settings = build_settings("Osama", language="ar", notifications=True)
print("settings:", settings)
# settings: {'user': 'Osama', 'theme': 'dark', 'language': 'ar', 'notifications': True}

print("theme:", settings["theme"])
# theme: dark

print("language:", settings["language"])
# language: ar

# The function fixed what it must control (user, theme) and let
# the caller pour in whatever else the application needs. No
# parameter list to edit when a new option appears -- the **kwargs
# absorbed it. That is the flexibility the transcript describes,
# in the same direction as lesson 59's defaults but for an
# UNLIMITED tail instead of a fixed few.

# ============================================================
# [9] Transcript's shape, finished: scores card
# ============================================================
# show_skills from section 1, now doing real work: totals,
# sorting by value, and a formatted card -- everything a dict
# loop can do (lessons 52 to 55):

def skills_card(name, **skills):
    """Print one person's skills, highest first."""
    print(f"  {name}")
    if not skills:
        print("    (none listed)")
        return
    for skill, value in sorted(skills.items(), key=lambda kv: kv[1], reverse=True):
        print(f"    {skill:<8} {value}%")

skills_card("Osama", html=90, css=80, js=70)
#   Osama
#     html     90%
#     css      80%
#     js       70%

skills_card("Mona", python=95, sql=88)
#   Mona
#     python   95%
#     sql      88%

skills_card("Sayid")
#   Sayid
#     (none listed)

# Three calls, three shapes: three keywords, two keywords, none.
# The card fixed the person's name (a required positional), took
# any number of scores (**skills), sorted them by value with the
# same key= trick used elsewhere in the course, and handled the
# empty dict with the same if not skills: guard from lesson 58.
# The transcript's promise -- "any number of keywords, packed
# into one dictionary" -- fulfilled end to end.

# ============================================================
# [10] Merging dictionaries with {**a, **b}
# ============================================================
# The unpacking syntax works OUTSIDE function calls too. Two
# dicts merge into one new dict in a single expression:

base = {"theme": "dark", "language": "ar"}
overrides = {"language": "en", "notifications": True}

merged = {**base, **overrides}
print("merged:", merged)
# merged: {'theme': 'dark', 'language': 'en', 'notifications': True}

# Read it left to right: start with base's pairs, then add
# overrides' pairs on top. When a key exists in BOTH, the one
# unpacked LATER wins -- language came out as "en", not "ar".
# That last-wins rule is exactly how configuration files layer
# defaults under user choices, and it is the same star you have
# been using, now doing data work instead of argument work.

# ============================================================
# [11] Passing a whole record to a function with named slots
# ============================================================
# Unpacking into named parameters (section 3) scales to any
# function, not just **kwargs collectors:

def register(username, email, role="member"):
    print(f"  {username} <{email}> as {role}")

record = {"username": "Mona", "email": "mona@example.com", "role": "admin"}
register(**record)
#   Mona <mona@example.com> as admin

# The dict's keys matched all three parameter names, so the call
# spread cleanly. Miss one key and Python raises the usual
# missing-argument TypeError; send an extra key and it raises
# unexpected-keyword. The dict must be a KEYED COPY of the
# signature -- which is why this pattern shines when the record
# came from JSON, a database row, or section 8's builder.

# ============================================================
# [12] The full inventory: four stars, two sides
# ============================================================
# Everything the last three lessons covered, in one screen:

def inventory(*args, **kwargs):
    print(f"  args:   {args}")
    print(f"  kwargs: {kwargs}")

print("no arguments:")
inventory()
# no arguments:
#   args:   ()
#   kwargs: {}

print("positional only:")
inventory(1, 2, 3)
# positional only:
#   args:   (1, 2, 3)
#   kwargs: {}

print("keyword only:")
inventory(a=1, b=2)
# keyword only:
#   args:   ()
#   kwargs: {'a': 1, 'b': 2}

print("both:")
inventory(1, 2, a=3)
# both:
#   args:   (1, 2)
#   kwargs: {'a': 3}

print("unpacked both:")
inventory(*[1, 2], **{"a": 3})
# unpacked both:
#   args:   (1, 2)
#   kwargs: {'a': 3}

# One def, five call shapes, and the last line is the whole
# lesson compressed: *list spreads positionals into args, **dict
# spreads keywords into kwargs. Two stars at the call, two stars
# in the def, and a tuple and a dict holding everything.

# ============================================================
# [13] The summary
# ============================================================
# Two stars, one extra meaning each:
#
#   def f(*args):        positional overflow -> tuple
#   def f(**kwargs):     keyword overflow    -> dict
#   f(*collection):      spread positionals from any iterable
#   f(**dict):           spread keywords from a dict's keys
#
# The rules that keep it predictable:
#
#   1. **kwargs goes last in the parameter list; after it, no
#      plain positional parameters (SyntaxError at def time)
#   2. keyword names that must match NAMED parameters have to be
#      valid identifiers -- "html-90" fails for a named slot but
#      is fine inside **kwargs-only collection
#   3. one slot, one value: greet(name=..., **{"name": ...}) is
#      a TypeError, never a silent overwrite
#   4. unpacking into named parameters requires the dict's keys
#      to be an exact keyed copy of the signature
#   5. {**a, **b} merges dicts outside function calls; later
#      keys win -- defaults first, overrides second
#   6. *args and **kwargs combine cleanly: unnamed goes to the
#      tuple, named goes to the dict, the boundary is the = sign
#      and the keyword syntax itself
#
# The transcript's def show_skills(**skills) receiving html=90,
# css=80, js=70 is the picture to keep: any number of named
# values, one dictionary, a for loop over items(), and -- when
# you already hold the dict -- **my_dict to send it all back out
# again. With this lesson, packing and unpacking are complete for
# both kinds of arguments, and every function in the projects to
# come can accept exactly the shape its caller has.
