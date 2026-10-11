# -----------------------------------------------------------------
# Lesson 54: loop control - continue, break, pass
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : skip an iteration, leave the loop, and the placeholder
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# In lessons 51 to 53 we walked collections. Now we learn the three
# words that control the walk itself: continue says "skip this
# one", break says "I am done, leave", and pass says "nothing to
# do here, but stay syntactically legal".
#
# continue and break are about FLOW -- they change where the loop
# goes next. pass is about SHAPE -- it changes nothing, it only
# keeps the syntax valid. Mixing them up wastes an afternoon, so
# this lesson keeps them apart.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] continue: skip THIS iteration only
# ============================================================
# The transcript's first keyword. When the condition fires,
# continue throws away the rest of this iteration and the loop
# moves to the next element as if this one never happened.

for n in range(1, 11):
    if n % 2 == 0:
        continue                      # even numbers are skipped
    print("odd:", n)
# odd: 1
# odd: 3
# odd: 5
# odd: 7
# odd: 9

# The loop still visited 10 numbers. It only PRINTED five. The
# even ones hit continue, the rest of the iteration body was
# abandoned, and the loop moved on. Nothing after continue in the
# same iteration ever runs:

for n in [10, 15, 20]:
    if n > 10:
        continue
    print("kept:", n)                 # unreachable for 15, 20
# kept: 10

# Rule: continue affects exactly one iteration. The loop itself
# is untouched, and the next element is processed normally.

# ============================================================
# [2] break: leave the loop entirely
# ============================================================
# The second keyword. break abandons the whole loop, not just the
# current element. Every remaining element is never visited.

for n in range(1, 100):
    if n == 4:
        print("reached 4, stopping")
        break
    print("n =", n)
# n = 1
# n = 2
# n = 3
# reached 4, stopping

# range(1, 100) would have produced 99 numbers. We printed three
# and stopped. The difference from continue could not be bigger:
#
#   continue  -> skip this element, keep looping
#   break     -> this element ends the loop, no more elements

# ============================================================
# [3] continue vs break, the same loop side by side
# ============================================================
# One loop skips even numbers, the other stops at the first even
# number. The condition is identical in both.

print("continue version:")
for n in range(1, 8):
    if n % 2 == 0:
        continue
    print("  ", n)
# continue version:
#    1
#    3
#    5
#    7

print("break version:")
for n in range(1, 8):
    if n % 2 == 0:
        break
    print("  ", n)
# break version:
#    1

# continue saw all four odd numbers. break met the first even
# number (2) and left after printing one line. The condition is
# identical in both loops -- only the keyword differs, and that
# one word changes the whole outcome. If you can name which one
# your loop needs, you have understood the lesson.

# ============================================================
# [4] break only leaves the INNERMOST loop
# ============================================================
# This is the detail that trips people up in nested loops
# (lesson 53). break exits one level, the loop it is written in.
# The outer loop keeps going.

for person in ["Osama", "Ahmed"]:
    print(person + ":")
    for skill in ["Python", "JS", "SQL"]:
        if skill == "JS":
            break                      # only leaves the INNER loop
        print("   ", skill)
# Osama:
#     Python
# Ahmed:
#     Python

# The inner loop ran twice per person (Python, then JS hit break).
# The outer loop still visited both people. To leave BOTH loops
# you need a flag, or -- better -- a function with return:

def first_match(people):
    """Return the first person who knows SQL, or None."""
    knows = {"Osama": ["Python", "JS"],
             "Ahmed": ["Python", "SQL"]}
    for person in people:
        for skill in knows[person]:
            if skill == "SQL":
                return person          # leaves the FUNCTION
    return None

print("found:", first_match(["Osama", "Ahmed"]))
# found: Ahmed

# return exits the whole function, which ends both loops at once.
# That is the clean way to break out of several levels: put the
# loops in a function and return.

# ============================================================
# [5] break and for-else: the else runs only if NOT broken
# ============================================================
# Lesson 51 touched this. The else clause of a for loop runs when
# the loop finished WITHOUT a break -- i.e. the search failed.

for n in [1, 3, 5, 7]:
    if n == 4:
        print("found 4")
        break
else:
    print("4 was never found")          # runs: loop ended cleanly
# 4 was never found

for n in [1, 3, 4, 7]:
    if n == 4:
        print("found 4")
        break
else:
    print("4 was never found")          # skipped: break fired
# found 4

# The else is not tied to the if. It is tied to the loop. "If the
# loop completed all its iterations without break, do this." It
# replaces the flag variable people write in other languages:

found = False
for n in [1, 3, 5]:
    if n == 3:
        found = True
        break
if not found:
    print("the flag version says: not found")
# the flag version says: not found

# Same answer, more lines, and one more variable to keep in sync.
# for-else is the Pythonic version.

# ============================================================
# [6] pass: do nothing, legally
# ============================================================
# The third keyword. pass has no effect at all. It is a
# placeholder that satisfies the interpreter's need for a body.
# The transcript's exact case: an empty if, function, or loop
# would otherwise be a SyntaxError.

# These are ALL legal because of pass:

for n in [1, 2, 3]:
    pass                              # the body is empty for now

def coming_soon():
    pass                              # a stub, not an error yet

class Book:
    pass                              # a class with no members yet

# Without pass, each of those would be a SyntaxError, because
# Python needs an indented block after :, and it needs at least
# one statement inside it.

# The real use: you are building a program, and you know the shape
# but not the content yet.

def calculate_tax(price, rate):
    """Not implemented yet -- the signature is decided."""
    pass

def calculate_shipping(weight):
    """This one is done."""
    return weight * 0.5

print("shipping 4kg:", calculate_shipping(4))
# shipping 4kg: 2.0

print("tax is a stub:", calculate_tax(100, 0.15) is None)
# tax is a stub: True

# calculate_tax returns None because pass returns nothing. That
# is fine for a stub: the program runs, the name exists, and you
# can fill in the body later without touching every call site.

# ============================================================
# [7] pass vs continue vs break, the one-table summary
# ============================================================
# All three appear inside loops. They do completely different
# things to the loop's flow.

for n in [1, 2, 3, 4, 5]:
    if n == 1:
        continue                      # skip n=1 only
    if n == 5:
        break                         # leave at n=5
    if n == 3:
        pass                          # do nothing, fall through
    print("visited:", n)
# visited: 2
# visited: 3
# visited: 4

# Trace it: n=1 continue (nothing printed). n=2 prints. n=3 hits
# pass -- pass does nothing, execution continues to print, so 3
# IS printed. n=4 prints. n=5 break (never printed).
#
#   continue  -> jump to the next iteration NOW
#   break     -> jump out of the loop NOW
#   pass      -> do nothing, keep going line by line
#
# pass is not a "skip". It is a no-op. The loop body continues
# with the statement after it.

# ============================================================
# [8] continue in a while loop, same meaning
# ============================================================
# continue and break work in while exactly as they do in for.
# The transcript's keywords are not for-specific.

n = 0
while n < 6:
    n += 1
    if n % 2 == 0:
        continue
    print("odd n:", n)
# odd n: 1
# odd n: 3
# odd n: 5

n = 0
while n < 6:
    n += 1
    if n == 4:
        break
    print("stopped before:", n)
# stopped before: 1
# stopped before: 2
# stopped before: 3

# One warning that matters ONLY for while: if you continue before
# updating the counter, the loop spins forever. This file would
# hang without the n += 1 coming first. That is why the update is
# at the top here -- it runs on every path, including the one that
# continues.

# ============================================================
# [9] pass in real code: except, and placeholder branches
# ============================================================
# The transcript names if, function, and loop. The two other places
# beginners meet pass are except and elif, where you want to
# acknowledge a case without handling it yet.

def read_number(text):
    """Return an int, or None if text is not a number."""
    try:
        return int(text)
    except ValueError:
        pass                            # not a number: just stop
    return None

print("parsed:", read_number("42"))
# parsed: 42

print("failed:", read_number("forty-two"))
# failed: None

# The except block needs a body, pass gives it one, and the
# function falls through to return None. Compare with continue:
# pass here is inside except, not a loop, so "skip the iteration"
# does not even apply. pass is the universal "empty body needed".

# A placeholder branch in a decision tree:

status = "pending"
if status == "paid":
    print("ship it")
elif status == "refunded":
    print("restore stock")
elif status == "pending":
    pass                               # TODO: handle this later
# (nothing prints for pending)

# The branch exists, documents the intent, and does nothing. When
# you implement it, you replace pass with real code and no other
# line changes.

# ============================================================
# [10] Trap: continue/break inside a loop you MUTATE
# ============================================================
# Lesson 51's removal trap still applies, and break/continue make
# it easier to hit because you are already thinking about flow.

data = [10, 20, 30, 40, 50]

for item in data[:]:                   # walk a copy
    if item == 30:
        continue
    if item == 50:
        break
    data.remove(item)

print("data after:", data)
# data after: [30, 50]

# We walked a snapshot data[:], so removing inside is safe. The
# continue skipped removing 30, the break left before touching 50.
# Walking the LIVE list here would skip elements after each
# removal -- the exact bug from lesson 51, now with two more ways
# to lose your place.

# ============================================================
# [11] A practical search: first match, with a reason
# ============================================================
# Putting it together: search a list of records, skip irrelevant
# ones with continue, stop at the answer with break, and report
# with for-else if nothing matched.

records = [
    {"name": "Osama", "role": "admin"},
    {"name": "Ahmed", "role": "user"},
    {"name": "Sayid", "role": "user"},
    {"name": "Mona",  "role": "admin"},
]

target_role = "admin"
found = None
for record in records:
    if record["role"] != target_role:
        continue                        # not an admin: next record
    found = record["name"]
    print("admin found:", found)
    break                               # first admin is enough
else:
    print("no admin in the list")
# admin found: Osama

target_role = "guest"
for record in records:
    if record["role"] != target_role:
        continue
    found = record["name"]
    print("guest found:", found)
    break
else:
    print("no guest in the list")
# no guest in the list

# The same three keywords, three roles in one search:
#   continue  ignores records that cannot match
#   break     stops at the first record that does
#   for-else  reports the "nothing matched" case
#
# This is the shape of almost every lookup you will write.

# ============================================================
# [12] Trap: pass does NOT skip, and break does NOT continue
# ============================================================
# Two mental shortcuts that are wrong:
#
#   "pass skips the rest"  -> no, pass does nothing at all
#   "break skips to next"  -> no, break leaves entirely

for n in [1, 2, 3]:
    if n == 2:
        pass                            # NOT a skip
    print("pass prints:", n)
# pass prints: 1
# pass prints: 2
# pass prints: 3

for n in [1, 2, 3, 4]:
    if n == 2:
        break                           # NOT a skip
    print("break prints:", n)
# break prints: 1

# If you wanted "skip 2" you needed continue. If you wanted "stop
# at 4, print 2" you needed neither -- just no keyword at all.
# The keyword you reach for has to match the word you would use
# in English: skip (continue), stop (break), nothing (pass).

# ============================================================
# [13] The summary
# ============================================================
# Three keywords, three jobs, zero overlap:
#
#   continue  the loop keeps going, THIS element is dropped
#   break     the loop ends, ALL remaining elements are dropped
#   pass      nothing happens, the syntax stays valid
#
# continue and break are flow control -- they change where
# execution goes. pass is syntax control -- it only fills a
# required body when you have no code yet: an empty if, an
# unimplemented function, a stub class, an except you mean to
# ignore, a branch marked TODO.
#
# Two details to keep: break leaves only the innermost loop (use
# return from a function to leave several), and for-else reports
# "the loop never broke" without a flag variable. And remember
# pass is a no-op, not a skip -- the line after it still runs.
#
# The search pattern in lesson 11 is the one to carry forward:
# continue past the misses, break on the first hit, else report
# the miss. Skip, stop, nothing -- once the English word is
# settled, the keyword picks itself.
