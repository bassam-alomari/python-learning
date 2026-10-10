# -----------------------------------------------------------------
# Lesson 52: for loop on dictionaries - keys, values, and items()
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : for + dict, .items(), .keys(), .values(), profile app
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# In lesson 51 we looped over lists, strings, and range(). The one
# collection we did not loop over yet is the dictionary, and it
# needs its own lesson because a dictionary is not a sequence of
# values -- it is a sequence of PAIRS, and a plain for loop over a
# dictionary gives you something surprising the first time.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] The data we will use: a skills dictionary
# ============================================================
# The transcript's example: a student records how well they know
# each technology. The key is the skill name, the value is the
# mastery percentage.

my_skills = {"HTML": 90, "CSS": 80, "JS": 70, "Python": 90}

print("the dictionary:")
print(my_skills)
# the dictionary:
# {'HTML': 90, 'CSS': 80, 'JS': 70, 'Python': 90}

# A dictionary has no indexes like 0, 1, 2. It has keys, and each
# key points to one value. That is why looping over it cannot work
# the same way a list loop works.

# ============================================================
# [2] Trap: a plain for loop over a dictionary gives you KEYS
# ============================================================
# This is the first surprise. When you write a for loop over a
# dictionary directly, Python does not give you the values, and it
# does not give you the pairs. It gives you the keys, one at a
# time.

for item in my_skills:
    print("plain for gives:", item)
# plain for gives: HTML
# plain for gives: CSS
# plain for gives: JS
# plain for gives: Python

# This is not a bug. It is the documented behaviour: iterating a
# dictionary iterates its keys. If you wanted the values, this loop
# is already wrong -- you have to ask for them on purpose.

# ============================================================
# [3] .keys(), .values(), and .items()
# ============================================================
# A dictionary has three methods that build the view you want, and
# the for loop then works on that view.

print("keys():  ", list(my_skills.keys()))
# keys():   ['HTML', 'CSS', 'JS', 'Python']

print("values():", list(my_skills.values()))
# values(): [90, 80, 70, 90]

print("items(): ", list(my_skills.items()))
# items():  [('HTML', 90), ('CSS', 80), ('JS', 70), ('Python', 90)]

# keys()   -> the keys only
# values() -> the values only
# items()  -> the pairs, each one a small tuple (key, value)
#
# You almost never need list() around them in real code. It is used
# here only so the whole view prints at once, the same trick we
# used with range() in lesson 51.

# ============================================================
# [4] Loop over keys only: for + .keys()
# ============================================================
# You can be explicit, even though the plain for loop already does
# this.

for skill in my_skills.keys():
    print("skill:", skill)
# skill: HTML
# skill: CSS
# skill: JS
# skill: Python

# The output is identical to section [2]. The explicit .keys() is
# sometimes used to remind the reader "I know this gives keys", but
# it adds nothing Python does not already do.

# ============================================================
# [5] Loop over values only: for + .values()
# ============================================================
# When you only care about the numbers -- for example, the average
# mastery -- the values view is what you want.

total = 0
for value in my_skills.values():
    total += value
print("sum of values:", total)
# sum of values: 330

print("average:", total / len(my_skills))
# average: 82.5

# You never touched the skill names in this loop. That is the
# point: .values() lets you work with the data and ignore the
# labels.

# ============================================================
# [6] Loop over pairs: for + .items()  <-- the one you want
# ============================================================
# The transcript's main line. .items() gives you the key and the
# value together, and Python unpacks them into two names in one
# step.

for skill, value in my_skills.items():
    print(f"{skill} => {value}%")
# HTML => 90%
# CSS => 80%
# JS => 70%
# Python => 90%

# Read it as: "for each skill, value pair in my_skills items, do
# this." The two names on the left of in are unpacking the tuple
# that .items() produced.

# If you use only ONE name on the left, you get the whole tuple:

for pair in my_skills.items():
    print("pair:", pair)
# pair: ('HTML', 90)
# pair: ('CSS', 80)
# pair: ('JS', 70)
# pair: ('Python', 90)

# Both loops walk the same data. The first one is shorter to write
# when you need both halves, and the second one is useful when you
# want to pass the pair around as a single object.

# ============================================================
# [7] A more formatted print, like a real profile page
# ============================================================
# The transcript formats the output to look like a skills card.
# The f-string from lesson 18 does the formatting, and the loop
# just repeats it once per skill.

print()
print("  --- My Skills ---")
for skill, value in my_skills.items():
    print(f"  {skill:<8} {value}%")
print("  -----------------")
#   --- My Skills ---
#   HTML     90%
#   CSS      80%
#   JS       70%
#   Python   90%
#   -----------------

# {skill:<8} means "print the skill name, padded to 8 characters,
# aligned left". Without it the percentages would not line up,
# because HTML is 4 letters and Python is 6.

# ============================================================
# [8] Change the dictionary, the loop follows automatically
# ============================================================
# This is the real-world point from the transcript: the loop does
# not hard-code four skills. It reads whatever the dictionary holds
# right now. Add a skill and the next run shows it, with no change
# to the loop code.

my_skills["Git"] = 85

for skill, value in my_skills.items():
    print(f"{skill} => {value}%")
# HTML => 90%
# CSS => 80%
# JS => 70%
# Python => 90%
# Git => 85%

# Five lines now, because the dictionary has five pairs. The for
# loop code is unchanged. This is why data-driven loops matter:
# the code describes the SHAPE of the output, and the dictionary
# supplies the content.

# Update an existing value the same way:

my_skills["JS"] = 95

for skill, value in my_skills.items():
    if skill == "JS":
        print(f"updated: {skill} => {value}%")
# updated: JS => 95%

# The dictionary is the single source of truth. The loop reads it.
# Change the data, and every loop over it sees the change.

# ============================================================
# [9] A profile-page simulation: data in, display out
# ============================================================
# Now we put the idea into a small function. The function does not
# know or care how many skills exist. It receives a dictionary and
# prints whatever is in it. This is exactly how a profile page
# works: the page template has one loop, and the database supplies
# the dictionary.

def show_profile(name, skills):
    """Print a skills card for one user."""
    print()
    print(f"  {name}'s Profile")
    print("  " + "-" * 18)
    for skill, value in skills.items():
        print(f"  {skill:<8} {value}%")
    print("  " + "-" * 18)

show_profile("Ahmed", {"HTML": 90, "CSS": 80})
# Ahmed's Profile
#   ------------------
#   HTML     90%
#   CSS      80%
#   ------------------

show_profile("Mona", {"Python": 95, "SQL": 88, "Git": 76})
# Mona's Profile
#   ------------------
#   Python   95%
#   SQL      88%
#   Git      76%
#   ------------------

# Two calls, two different dictionaries, one loop inside the
# function. Ahmed has two skills and Mona has three. The function
# was never edited.

# ============================================================
# [10] Nested dictionaries: a list of profiles
# ============================================================
# Real applications rarely hold one dictionary. They hold a
# dictionary of dictionaries, or a list of dictionaries, and the
# loop nests the same way loops nest over lists.

users = {
    "ahmed": {"HTML": 90, "CSS": 80},
    "mona":  {"Python": 95, "SQL": 88},
}

for username, skills in users.items():
    print(f"{username}:")
    for skill, value in skills.items():
        print(f"  {skill} => {value}%")
# ahmed:
#   HTML => 90%
#   CSS => 80%
# mona:
#   Python => 95%
#   SQL => 88%

# The outer loop unpacks (username, skills). The inner loop
# unpacks (skill, value) from the dictionary that username points
# to. The pattern scales: add a third user to the dictionary and
# the outer loop prints them too, no code change.

# ============================================================
# [11] Trap: looping and adding keys at the same time
# ============================================================
# This is the dictionary version of the list trap from lesson 51.
# If you add a key to a dictionary while a for loop is walking it,
# Python raises RuntimeError: dictionary changed size during
# iteration. The list trap silently skipped items; this one fails
# loudly, which is better, but it is still a crash.

# The wrong way:
# for skill in my_skills:
#     my_skills[skill + "!"] = my_skills[skill]   # RuntimeError

# The safe way, same idea as the list: walk a snapshot of the
# items, and write into the real dictionary.

for skill, value in list(my_skills.items()):
    my_skills[skill + " (mastered)"] = value

# The snapshot list(my_skills.items()) is a fixed list of pairs.
# Adding keys to my_skills does not change that list, so the loop
# finishes safely, and the dictionary now contains the original
# four plus the four new keys.

# Rule, same as lesson 51: never change the SIZE of the collection
# while a for loop is walking it. Walk a copy instead.

# ============================================================
# [12] Which view should you use? A quick guide
# ============================================================
# for item in dict:            -> keys only (the default)
# for key in dict.keys():      -> keys only (explicit)
# for value in dict.values():  -> values only
# for key, value in dict.items():  -> both, unpacked
# for pair in dict.items():    -> both, as a tuple
#
# Pick the view that matches what you need:
#
#   - need the names only        -> keys / plain for
#   - need the numbers only      -> values
#   - need name AND number       -> items() with two names
#   - need to pass the pair on   -> items() with one name
#
# The default (plain for) gives keys. If you catch yourself
# writing dict[key] inside the loop, you probably wanted items():
#
#   # works, but clumsy:
#   for skill in my_skills:
#       print(skill, my_skills[skill])
#
#   # shorter, and what you meant:
#   for skill, value in my_skills.items():
#       print(skill, value)

# ============================================================
# [13] The summary
# ============================================================
# A dictionary loop is a pair loop, not a value loop.
#
#   plain for           -> keys
#   .keys()             -> keys
#   .values()           -> values
#   .items()            -> (key, value) tuples
#
# for skill, value in my_skills.items():   is the line to
# remember. It unpacks each pair into two names, and the loop body
# can use both. The f-string does the formatting, the dictionary
# holds the data, and the loop connects them.
#
# The profile-page idea is the one to carry forward: one loop in
# the display code, all the content in the dictionary. Change the
# dictionary -- add a skill, update a score, add a whole user --
# and the display follows without a single edit to the loop. That
# is what "data-driven" means, and it is the same idea behind
# every table, chart, and profile page you will ever build.
