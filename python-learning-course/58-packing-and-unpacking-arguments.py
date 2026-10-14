# -----------------------------------------------------------------
# Lesson 58: packing and unpacking arguments
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : *args packing, *list unpacking at the call, fixed +
#            variable parameters, loops over the packed tuple
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The star (*) has ONE meaning in function arguments -- "spread or
# gather" -- but it appears on two different SIDES of the call,
# and that is what confuses people:
#
#   in the def    def show(*skills):    PACK   gather values in
#   in the call   show(*skills):        UNPACK spread values out
#
# Lesson 57 used *args once and promised the full story. Here it
# is: gathering any number of values into a tuple, looping over
# that tuple inside the function, unpacking a list or tuple at the
# call site, and mixing a fixed parameter with a packed one
# (def show_skills(name, *skills)) -- the transcript's final form.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] The star in two places, at a glance
# ============================================================
# Same symbol, opposite directions. Seeing both in one screen is
# the fastest way to stop mixing them up.

def collect(*items):                 # DEF side: gather into a tuple
    print("gathered:", items)

collect(1, 2, 3)
# gathered: (1, 2, 3)

values = [4, 5, 6]
collect(*values)                     # CALL side: spread the list
# gathered: (4, 5, 6)

# First call: three separate arguments were PACKED into the tuple
# (1, 2, 3). Second call: the list [4, 5, 6] was UNPACKED into
# three separate arguments, which the def then packed again. Two
# stars, one round trip, and the function body never noticed any
# difference.

# ============================================================
# [2] Packing: any number of arguments, one tuple
# ============================================================
# The transcript's core: when you do NOT know how many values the
# user will send, put a star before the parameter name. Python
# collects everything into a TUPLE, automatically.

def welcome_all(*people):
    print("  count:", len(people))
    print("  tuple:", people)

welcome_all("Osama", "Mona", "Ahmed")
#   count: 3
#   tuple: ('Osama', 'Mona', 'Ahmed')

welcome_all("Sayid")
#   count: 1
#   tuple: ('Sayid',)

welcome_all()
#   count: 0
#   tuple: ()

# Three cases, one def:
#
#   many values  -> a full tuple
#   ONE value    -> a tuple with a trailing comma: ('Sayid',)
#   NO values    -> the empty tuple ()
#
# The single-value case is the one to remember. A tuple with one
# element needs the comma, and Python writes it for you -- people
# expect 'Sayid' (a string) and get ('Sayid',) (a tuple). The
# TYPE never changes with the count: packed always means tuple.

# ============================================================
# [3] Loop over the packed tuple inside the function
# ============================================================
# The transcript's next step: a for loop inside the body, walking
# whatever arrived. The tuple is an ordinary tuple (lesson 24),
# so every loop rule from lessons 51 to 55 applies unchanged.

def print_skills(*skills):
    print("  skills received:")
    for skill in skills:                 # a normal loop
        print("   -", skill)

print_skills("Python", "JS")
#   skills received:
#    - Python
#    - JS

print_skills("HTML", "CSS", "Git", "SQL")
#   skills received:
#    - HTML
#    - CSS
#    - Git
#    - SQL

# Two calls, two lengths, zero edits to the function. The loop
# runs len(skills) times and stops when the tuple runs out --
# the same guarantee every for loop has.

# ============================================================
# [4] Arithmetic over an unknown count
# ============================================================
# The transcript's "sum of a number of values". Lesson 57 used
# sum(); here we walk the tuple by hand to show the packed value
# is just data:

def total(*numbers):
    running = 0
    for n in numbers:
        running += n
    return running                      # give it back (lesson 56)

print("total(10, 20, 30) =", total(10, 20, 30))
# total(10, 20, 30) = 60

print("total(5, 5, 5, 5, 5) =", total(5, 5, 5, 5, 5))
# total(5, 5, 5, 5, 5) = 25

print("total() =", total())
# total() = 0

# Empty packing sums to 0 because the loop body never runs --
# running starts at 0 and nothing changes it. No special case for
# "no numbers" was needed; the loop handled it by simply not
# looping. That is what makes *numbers the right design here.

# ============================================================
# [5] Unpacking: spread a list or tuple at the call site
# ============================================================
# The other direction. You HAVE a collection; the function wants
# separate arguments; the star at the call site does the split.

def show_three(a, b, c):
    print(f"  {a} | {b} | {c}")

langs = ["HTML", "CSS", "JS"]
show_three(*langs)
#   HTML | CSS | JS

grades = (80, 90, 100)
show_three(*grades)
#   80 | 90 | 100

# A list unpacks, a tuple unpacks -- ANY iterable can be spread
# into arguments, as long as the count matches the parameters
# (section 7 shows what happens when it does not). The function
# sees three plain arguments and has no idea a collection was
# ever involved.

# ============================================================
# [6] Packing and unpacking side by side
# ============================================================
# One function, called four ways, to fix the vocabulary:

def collect(*items):
    print("   items =", items)

print("separate arguments (packed by the def):")
collect(1, 2, 3)
# items = (1, 2, 3)

print("a list, unpacked at the call:")
collect(*[1, 2, 3])
# items = (1, 2, 3)

print("a tuple, unpacked at the call:")
collect(*(1, 2, 3))
# items = (1, 2, 3)

print("one list, NOT unpacked:")
collect([1, 2, 3])
# items = ([1, 2, 3],)

# The first three produce the SAME tuple -- separate values, a
# spread list, and a spread tuple are indistinguishable by the
# time they reach the def. The fourth call forgot the star: the
# list arrived as ONE argument, so items holds a one-element
# tuple containing the list. Compare:
#
#   collect(*[1, 2, 3])   ->  (1, 2, 3)     three numbers
#   collect([1, 2, 3])    ->  ([1, 2, 3],)  one list
#
# Forgetting the star is the packing/unpacking bug you will
# actually hit. The printed tuple tells you immediately which one
# you wrote.

# ============================================================
# [7] Trap: unpacking must match the parameter count
# ============================================================
# Unpacking sends SEPARATE arguments, so the normal count rule
# from lesson 57 applies to the spread too:

try:
    show_three(*[1, 2])
except TypeError as error:
    print("too few ->", error)
# too few -> show_three() missing 1 required positional argument: 'c'

try:
    show_three(*[1, 2, 3, 4])
except TypeError as error:
    print("too many ->", error)
# too many -> show_three() takes 3 positional arguments but 4 were given

# The star does not relax the count check -- it only changes HOW
# the arguments arrive. Whether you type three values by hand or
# spread a four-element list, Python matches positions and
# complains with the same TypeError when they disagree.

# ============================================================
# [8] The transcript's form: one fixed parameter, then packing
# ============================================================
# def show_skills(name, *skills): -- a name you always expect,
# plus any number of skills you do not. This is the shape the
# whole lesson has been building toward.

def show_skills(name, *skills):
    """Print one person's card: fixed name, variable skills."""
    print(f"  {name}")
    if not skills:
        print("    (no skills listed)")
    for skill in skills:
        print(f"    - {skill}")

show_skills("Osama", "Python", "JS", "SQL")
#   Osama
#     - Python
#     - JS
#     - SQL

show_skills("Mona", "HTML", "CSS")
#   Mona
#     - HTML
#     - CSS

show_skills("Sayid")
#   Sayid
#     (no skills listed)

# Read the def left to right: the FIRST argument (any single
# value) fills name; EVERYTHING else is gathered into the skills
# tuple. The function separates the constant from the variable
# automatically, no matter which side you look at it from:
#
#   call site   "Osama", "Python", "JS", "SQL"   looks flat
#   def side    name = "Osama"
#               skills = ("Python", "JS", "SQL")  split cleanly
#
# The empty case prints its own line because an empty tuple is
# falsy (if not skills:) -- the same truthiness rule as empty
# lists from the early lessons.

# ============================================================
# [9] Order rules: fixed first, star last, keywords after
# ============================================================
# Two rules keep the def legal and readable:
#
#   1. positional parameters come BEFORE the packed one
#   2. anything AFTER the packed one is keyword-only (must be
#      named at the call site)

def report(title, *rows, verbose=True):
    """Fixed title, any rows, one keyword-only switch."""
    print(f"  {title} ({len(rows)} rows)")
    if verbose:
        for row in rows:
            print("    -", row)

report("Skills", "Python", "JS")
#   Skills (2 rows)
#     - Python
#     - JS

report("Skills")                       # rows simply empty
#   Skills (0 rows)

report("Audit", "checked", verbose=False)
#   Audit (1 rows)

# verbose can ONLY be sent by name -- there is no position left
# for it, because every unnamed argument after "Audit" would land
# in rows. That is what "keyword-only" buys you: the caller
# cannot accidentally shove a boolean into your tuple, and the
# call reads as an instruction (verbose=False) instead of a
# mystery position.
#
# Illegal shapes (both fail BEFORE the file runs, at def time):
#
#   def bad(*rows, title):            positional after star names
#   def bad2(title=1, *rows):         default before required

# ============================================================
# [10] Packed values are ordinary data: dicts, pairs, numbers
# ============================================================
# The tuple holds whatever you send -- including the pairs from
# lessons 52 to 55. Unpacking each pair back OUT for processing
# is the same star, now on a tuple inside a tuple:

def show_pair(skill, value):
    print(f"    {skill:<8} {value}%")

def show_card(name, *pairs):
    print(f"  {name}")
    for pair in pairs:
        show_pair(*pair)                # unpack ONE pair per pass

show_card("Mona", ("Python", 95), ("SQL", 88))
#   Mona
#     Python   95%
#     SQL      88%

# Tracing the second loop pass: pair is ("SQL", 88), show_pair
# receives skill="SQL", value=88. The star at the call site of
# show_pair is doing exactly what show_three(*langs) did in
# section 5 -- splitting a collection into positional arguments.
# Packing gathered them in; unpacking hands them back out.

# ============================================================
# [11] Practical: greet any number of people
# ============================================================
# The transcript's first application, with the loop and a return
# so the caller can reuse the result (lesson 56's rule):

def greet_many(*names):
    """Return one greeting line per person."""
    lines = []
    for name in names:
        lines.append(f"Hello, {name}!")
    return lines                        # give the list back

for line in greet_many("Osama", "Mona", "Ahmed"):
    print(line)
# Hello, Osama!
# Hello, Mona!
# Hello, Ahmed!

print("---")
# ---

for line in greet_many("Sayid", "Hassan", "Khalil", "Nadia", "Ali"):
    print(line)
# Hello, Sayid!
# Hello, Hassan!
# Hello, Khalil!
# Hello, Nadia!
# Hello, Ali!

# Three names, then five -- same def, different tuple lengths.
# The function BUILT the lines and returned them; this loop
# decided they print right now. Had greet_many printed inside,
# the "---" separator between the groups would have been
# impossible to place: the printing function would own the
# output's order, not the caller.

# ============================================================
# [12] Trap: pack once, do not double-wrap
# ============================================================
# The subtle one. If a packed parameter is used as a whole, and
# you pass it on to ANOTHER packed parameter without unpacking,
# you get nesting:

def inner(*xs):
    print("   inner sees:", xs)

def outer(*xs):
    inner(xs)                           # WRONG: whole tuple as one
    inner(*xs)                          # right: spread it back out

print("outer(1, 2, 3):")
outer(1, 2, 3)
# outer(1, 2, 3):
#    inner sees: ((1, 2, 3),)
#    inner sees: (1, 2, 3)

# The first inner call received ONE argument -- the whole tuple
# -- so its own packing wrapped it AGAIN: (1, 2, 3) became a
# one-element tuple containing that tuple: ((1, 2, 3),). The
# second call spread the values back out, and inner saw the flat
# (1, 2, 3) it expected. Two extra parentheses, one real bug:
# a loop over the first result walks ONE item (a tuple), not
# three numbers. Watch the count instead:

def count_args(*xs):
    return len(xs)

def passthrough_broken(*xs):
    return count_args(xs)               # 1: the tuple itself

def passthrough_fixed(*xs):
    return count_args(*xs)              # 3: the three values

print("broken:", passthrough_broken(1, 2, 3))
# broken: 1

print("fixed:", passthrough_fixed(1, 2, 3))
# fixed: 3

# That is the real diagnostic. Broken says the next function saw
# ONE argument; fixed says it saw three. Rule: when forwarding a
# packed tuple to another function that also packs, UNPACK it
# again with the star -- or let the inner function accept the
# tuple directly, without a star on its parameter.

# ============================================================
# [13] The summary
# ============================================================
# One symbol, two positions, one meaning: spread it out or gather
# it in.
#
#   def f(*args):        PACK    any number of arguments arrive,
#                                collected as a tuple
#   f(*collection):      UNPACK  a list/tuple is spread into
#                                separate arguments
#
# The rules that make it predictable:
#
#   - packed always means TUPLE, whatever the count: full,
#     one element (('Sayid',)), or empty ()
#   - a for loop over the packed tuple works like every loop
#     from lessons 51 to 55
#   - fixed parameters go BEFORE the star; after the star,
#     parameters become keyword-only (verbose=True)
#   - unpacking at the call still obeys the count rule --
#     wrong count, same TypeError
#   - the trap to memorise: collect([1, 2, 3]) packs ONE list;
#     collect(*[1, 2, 3]) packs three numbers -- the printed
#     tuple tells you which you wrote
#   - when forwarding packed values onward, star them AGAIN
#     (inner(*xs)), or you nest tuples by accident
#
# The transcript's def show_skills(name, *skills) is the shape
# to keep: a fixed head the caller always names, and a variable
# tail that stretches to any length. That shape shows up
# everywhere -- print-style helpers, greeting builders, score
# collectors -- and the ** form for keyword arguments follows the
# same idea in a later lesson.
