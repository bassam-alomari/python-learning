# -----------------------------------------------------------------
# Lesson 62: variable scope (global vs local)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : global scope, local scope, local priority over global,
#            the global keyword (modify and create),
#            assignment vs mutation, execution-flow order
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Scope answers one question: WHERE was this variable defined,
# and therefore WHO can see it?
#
#   Global scope  -- defined outside every function, visible
#                    anywhere in the file
#   Local scope   -- defined inside one function, visible only
#                    inside that function, and only while it runs
#
# The transcript adds the two rules that make scope predictable:
# a local with the same name WINS inside its function without
# touching the global, and the global keyword is how you say
# "I mean the outer one" when you really need to change it.
# Section 12 adds the distinction that saves the most debugging:
# mutation does not need global, assignment does.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] Global scope: defined at the top, readable from anywhere
# ============================================================
# This variable is written at module level -- outside every
# def. That makes it global: any function may READ it.

course = "Python"

def show_course():
    print(f"  studying: {course}")

show_course()
#   studying: Python

show_course()
#   studying: Python

# Two calls, same answer. Reading a global needs no special
# keyword at all -- show_course simply looks up course, does not
# find it locally, and falls back to the global. The lookup
# happens at CALL time, which section 11 explores.

# ============================================================
# [2] Local scope: defined inside, invisible outside
# ============================================================
# A name born inside a function belongs to that function alone.
# It exists only while the function runs:

def greet():
    message = "Hello"          # local: created here
    print(f"  inside: {message}")

greet()
#   inside: Hello

# The call worked -- message existed for the duration of the
# call. But the function has returned now, and message was
# created inside it, so outside knows nothing about it:

try:
    print(message)
except NameError as error:
    print("outside ->", type(error).__name__)
# outside -> NameError

# Same story as section 1, opposite result: course lives at the
# top so everyone sees it; message lives inside greet so only
# greet ever saw it. Scope is just that -- the border around a
# function's private names.

# ============================================================
# [3] Local scope is created per call and destroyed after it
# ============================================================
# Each call gets its OWN locals, and they are gone when the call
# ends. Nothing from call one survives into call two:

def scratch():
    note = "first call"
    print(f"  {note}")

scratch()
scratch()
scratch()
#   first call
#   first call
#   first call

# Three fresh locals named note, three independent prints, no
# memory of the previous call. That is why locals cannot carry
# information between calls -- if you want something to last,
# it has to live outside the function (a global) or be handed
# back with return (lesson 56).

# ============================================================
# [4] Priority: a local with the same name wins inside
# ============================================================
# The transcript's first rule. Same name, two scopes -- the
# function always sees ITS OWN first:

level = "global"

def shadow():
    level = "local"
    print(f"  inside: {level}")

print("before:", level)
shadow()
print("after: ", level)
# before: global
#   inside: local
# after:  global

# Inside shadow, level means the local one. Outside, level
# still means the global one, and it never changed -- shadow's
# assignment touched only its private copy. Two variables, one
# name, zero interference. That isolation is the point of local
# scope: a function can reuse common names (result, data, i,
# value) without trashing anything at the top of the file.

# ============================================================
# [5] The priority shown from both sides
# ============================================================
# The same rule, with the global printed BEFORE the function is
# called and the local printed inside it -- two values, one
# name, and only the function's view differs:

count = 100

def both_views():
    count = 1                       # local, shadows the global
    print(f"  local sees:  {count}")

print("global sees:", count)
both_views()
print("global sees:", count)
# global sees: 100
#   local sees:  1
# global sees: 100

# Read the three lines in order: the global is 100, the
# function's private count is 1, the global is still 100. The
# function did not "edit the global quietly" -- it never touched
# it. If you WANTED it to touch it, that is exactly what the
# global keyword is for (sections 7 and 8).

# ============================================================
# [6] Reading a global never needs the keyword
# ============================================================
# A subtle but important split: a function may READ a global
# with no ceremony at all -- the keyword is only required to
# ASSIGN to it:

theme = "dark"

def show_theme():
    print(f"  theme: {theme}")      # read: no global keyword needed

show_theme()
#   theme: dark

theme = "light"                     # reassign at the top level
show_theme()
#   theme: light

# The second call printed "light" because show_theme looks the
# name up when it RUNS, not when it is defined. Reading is
# always safe: Python checks the local scope first, then the
# global. Only the act of ASSIGNING flips the meaning -- that
# is the trap in section 9.

# ============================================================
# [7] global keyword: modify the global from inside
# ============================================================
# Now the transcript's second rule. To CHANGE a global inside a
# function, announce it first:

score = 0

def gain(points):
    global score                    # announce: I mean the OUTER one
    score += points

gain(10)
gain(5)
print("score:", score)
# score: 15

# Without the global line, `score += points` would have created
# a local score, thrown it away at return, and the global would
# still be 0 (and Python would actually refuse to run it --
# section 9 shows that error). With the announcement, the
# addition happens to the one everyone can see, so both calls
# stacked onto the same variable: 0 + 10 + 5 = 15.

# ============================================================
# [8] global keyword: CREATE a global from inside
# ============================================================
# The same keyword also works when the name does not exist yet --
# the function brings it into the global scope:

def boot():
    global ready                    # announce a name that is new
    ready = True

print("before boot, ready exists?", "ready" in globals())
boot()
print("after boot,  ready =", ready)
# before boot, ready exists? False
# after boot,  ready = True

# Nothing named ready existed until boot ran. Because of the
# global line, the assignment landed at the top level instead of
# inside the function, so the line after boot() can see it.
# globals() is the dict of every global name -- a handy probe
# that keeps this check deterministic.

# ============================================================
# [9] The classic trap: assignment silently means local
# ============================================================
# The transcript warns about execution order; this is the trap
# that falls out of it. A counter written WITHOUT the global
# keyword does not count -- it explodes:

calls = 0

def broken():
    calls = calls + 1               # assignment => calls is LOCAL

try:
    broken()
except UnboundLocalError as error:
    print("broken ->", type(error).__name__)
# broken -> UnboundLocalError

print("global calls still:", calls)
# global calls still: 0

# Read it carefully: because `calls` is assigned inside broken,
# Python marks it LOCAL for the whole function -- so the right-
# hand side `calls + 1` tries to read a local that has no value
# yet. UnboundLocalError (a subclass of NameError) is Python
# saying "you assigned it, so you own it, but you never gave it
# a value." The global is untouched: still 0. The fix is one
# line.

# ============================================================
# [10] The fix: announce it, then it counts
# ============================================================
# Same function, one global line added:

calls = 0

def fixed():
    global calls                    # the one missing line
    calls += 1

fixed()
fixed()
fixed()
print("calls:", calls)
# calls: 3

# Three calls, three increments, one variable. Compare with
# section 9: the ONLY difference is the announcement. This is
# the smallest complete example of the transcript's rule --
# tell Python which variable you mean, and the modification
# reflects on the whole program.

# ============================================================
# [11] Execution flow: order decides what you see
# ============================================================
# Python reads the file top to bottom, one line at a time. A
# function body runs when it is CALLED, not when it is defined,
# and a global must exist before anything reads it:

def announce():
    print(f"  status: {status}")

try:
    announce()                       # called BEFORE status exists
except NameError as error:
    print("too early ->", type(error).__name__)
# too early -> NameError

status = "ready"                     # defined now
announce()                           # called AFTER status exists
#   status: ready

# Same function, two calls, opposite results -- nothing in
# announce changed; only WHERE the call sat in the file changed.
# The transcript's point about paying attention to line order
# is exactly this: define before use, call after the data it
# reads exists. The second half of flow is mutation timing:

total = 0

def add(amount):
    global total
    total += amount

add(5)
print("after add(5): ", total)
# after add(5):  5
add(3)
print("after add(3): ", total)
# after add(3):  8

# Each call sees the total left behind by the previous call,
# because the global survives between calls while locals do not
# (section 3). Order of calls = order of mutations = the number
# you read at the end.

# ============================================================
# [12] Mutation needs no global; assignment does
# ============================================================
# The distinction that prevents most scope bugs. Appending to a
# list CHANGES the object in place -- it is not an assignment,
# so no global keyword is required:

seen = []

def note(item):
    seen.append(item)               # mutation of a global object

note("alpha")
note("beta")
print("seen:", seen)
# seen: ['alpha', 'beta']

# The lookup of seen still fell back to the global (section 6),
# and append() mutated the one list everyone shares. But try to
# REBIND the name inside a function without global and you get a
# different result entirely:

def reset():
    seen = []                        # this is a NEW local list

reset()
print("after reset():", seen)
# after reset(): ['alpha', 'beta']

# reset() built an empty local, threw it away on return, and
# never touched the outer list -- so seen is unchanged, with no
# error to warn you. Rule of thumb the whole lesson hangs on:
#   * mutate (append, update, sort, item assignment) -> shared
#     object changes, no keyword
#   * assign (name = ...) -> a brand-new local unless you write
#     global first

# ============================================================
# [13] The summary
# ============================================================
# Scope is the border around a name that decides who can see it:
#
#   1. GLOBAL -- defined outside every function; anyone may
#      read it; it lives as long as the file runs
#   2. LOCAL  -- defined inside one function; only that function
#      sees it; a fresh copy per call, destroyed when the call
#      returns
#   3. PRIORITY -- when both exist, the local wins inside its
#      function and the global is left completely untouched
#   4. READING a global needs no keyword; LOOKUP order is local
#      first, then global, resolved when the call runs
#   5. ASSIGNING inside a function makes the name local by
#      default -- reading it back raises UnboundLocalError
#   6. `global name` announces your intent: assign to the outer
#      variable (creating it if needed), and the change is
#      visible to the whole program
#   7. MUTATION of a shared object (append, update, ...) needs
#      no keyword -- only rebinding the name does
#   8. EXECUTION FLOW -- Python reads top to bottom; define a
#      global before any call reads it, and remember each call
#      sees the mutations left by the calls before it
#
# The two halves of the transcript fit together: locals give
# functions privacy (priority rule, no accidental damage), and
# the global keyword is the explicit door between that privacy
# and the rest of the program -- to be opened only when a value
# is genuinely meant to be shared.
