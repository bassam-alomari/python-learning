# -----------------------------------------------------------------
# Lesson 53: nested loops - for inside for
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : outer loop, inner loop, list of dicts, two-dimensional data
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# In lesson 52 we looped over ONE dictionary. Real data is almost
# never one dictionary -- it is a LIST of dictionaries, or a
# dictionary of dictionaries, and to reach the inside you need a
# loop inside a loop.
#
# The transcript's warning is fair: nested loops look complex the
# first time. The rule that makes them simple is this: the outer
# loop picks the SUBJECT, the inner loop walks what the subject
# OWNS. One line per subject, then one line per detail.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] The data: a list of people, each with their own skills
# ============================================================
# This is the structure the transcript describes: several users,
# each one a dictionary of skills with a mastery percentage.

users = [
    {"name": "Osama", "skills": {"Python": 90, "JS": 80}},
    {"name": "Ahmed", "skills": {"HTML": 95, "CSS": 85, "Git": 70}},
    {"name": "Sayid", "skills": {"SQL": 88, "Python": 75}},
]

print("the outer list has", len(users), "people")
# the outer list has 3 people

# A list of dictionaries. Each dictionary has two keys: "name" for
# the person, and "skills" for ANOTHER dictionary that belongs to
# them. That second dictionary is the reason we need two loops.

# ============================================================
# [2] The trap: one loop is not enough
# ============================================================
# If you loop over users once, you get the three people, and
# nothing else. The skills are still hidden inside.

for user in users:
    print("one loop gives:", user["name"])
# one loop gives: Osama
# one loop gives: Ahmed
# one loop gives: Sayid

# We know WHO they are, but not WHAT they know. The skills
# dictionary is one level deeper, and a single for loop cannot
# reach it. Adding a second loop does.

# ============================================================
# [3] The shape: outer loop, then inner loop
# ============================================================
# The outer loop walks the list of people. The inner loop, written
# INSIDE the outer loop's body, walks one person's skills. The
# indentation is the structure.

for user in users:                      # outer: pick a person
    print(user["name"] + ":")           # their header line
    for skill, value in user["skills"].items():   # inner: their skills
        print("   ", skill, "=", value, "%")
# Osama:
#     Python = 90 %
#     JS = 80 %
# Ahmed:
#     HTML = 95 %
#     CSS = 85 %
#     Git = 70 %
# Sayid:
#     SQL = 88 %
#     Python = 75 %

# Read it in English: "FOR each user, print their name, THEN for
# each skill they own, print the skill." The inner loop starts
# from the top every time the outer loop takes a new person, which
# is why each person gets their own block of skill lines.

# ============================================================
# [4] Counting the work: the inner loop runs len(skills) times
# ============================================================
# The outer loop ran 3 times (three people). The inner loop ran
# 2 + 3 + 2 = 7 times (Osama has 2 skills, Ahmed 3, Sayid 2).
# Total printed detail lines: 7, plus the 3 header lines.

detail_lines = 0
for user in users:
    detail_lines += len(user["skills"])
print("detail lines:", detail_lines)
# detail lines: 7

print("header lines:", len(users))
# header lines: 3

print("total lines:", len(users) + detail_lines)
# total lines: 10

# The formula is: total = sum of the sizes of the inner
# collections. The outer loop's count is multiplied by however
# many times the inner loop runs, which is why nested loops grow
# fast: 3 people x 3 skills each would be 9 detail lines, not 6.

# ============================================================
# [5] A clean profile card: the transcript's goal
# ============================================================
# The transcript asks for a neat, professional display: the name
# on its own line, then every skill under it. The f-string and
# padding from lesson 52 do the alignment.

print()
for user in users:
    print(f"  {user['name']}'s Profile")
    print("  " + "-" * 16)
    for skill, value in user["skills"].items():
        print(f"  {skill:<8} {value}%")
    print("  " + "-" * 16)
    print()
#   Osama's Profile
#   ----------------
#   Python   90%
#   JS       80%
#   ----------------
#
#   Ahmed's Profile
#   ----------------
#   HTML     95%
#   CSS      85%
#   Git      70%
#   ----------------
#
#   Sayid's Profile
#   ----------------
#   SQL      88%
#   Python   75%
#   ----------------
#

# The blank print() after each person is what separates the cards.
# Without it the three profiles would run together into one long
# list. The outer loop decides WHERE the separator goes: after the
# whole inner loop finishes for one person.

# ============================================================
# [6] Nested loops over a 2D table: rows and columns
# ============================================================
# The list-of-dictionaries is one shape of nested data. The other
# classic shape is a table: a list of rows, each row a list of
# cells. Outer loop = row, inner loop = column.

table = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

for row in table:                # outer: one row at a time
    for cell in row:             # inner: one cell at a time
        print(cell, end=" ")
    print()                      # move to the next line
# 1 2 3
# 4 5 6
# 7 8 9

# The inner print(cell, end=" ") keeps the row on one line, and
# the outer print() after the inner loop ends starts the next row.
# That is the whole trick behind printing a table: the inner loop
# fills the line, the outer loop ends it.

# ============================================================
# [7] Walking a list of strings inside a list of rows
# ============================================================
# The same shape works for text: a list of lines, each line a list
# of words.

lines = [
    ["learn", "python", "daily"],
    ["write", "code", "every", "day"],
]

for line_no, words in enumerate(lines):
    for word in words:
        print(f"line {line_no}: {word}")
# line 0: learn
# line 0: python
# line 0: daily
# line 1: write
# line 1: code
# line 1: every
# line 1: day

# enumerate() on the OUTER loop gives the line number, and the
# inner loop does not need it -- each word belongs to whichever
# line the outer loop is currently on.

# ============================================================
# [8] Trap: the inner loop's variable does not survive
# ============================================================
# Just like lesson 51's single loop, the inner loop variable is
# fresh each time. After the inner loop ends, only the LAST value
# it saw is still reachable, and it belongs to the LAST outer
# element.

last_seen = None
for user in users:
    for skill in user["skills"]:
        last_seen = skill
print("last skill seen:", last_seen)
# last skill seen: Python

# The final value is Python, because Sayid is the last person, and
# Python is the last key in Sayid's skills. The loop did not
# remember Osama's skills at all -- each inner loop started over.
# If you need EVERY skill after the loops end, collect them into a
# list as you go:

all_skills = []
for user in users:
    for skill in user["skills"]:
        all_skills.append(skill)
print("all_skills:", all_skills)
# all_skills: ['Python', 'JS', 'HTML', 'CSS', 'Git', 'SQL', 'Python']

# Note Python appears twice, because two different people know it.
# The list is a flat record of every skill line ever printed.

# ============================================================
# [9] Trap: changing the data while nested loops run
# ============================================================
# Lesson 51 warned about changing a list while a loop walks it.
# With nested loops the rule doubles: do not change the OUTER
# collection while the outer loop runs, and do not change an
# INNER collection while the inner loop runs. The safe habit is
# the same: build a new structure, or walk a snapshot.

snapshot = [dict(user["skills"]) for user in users]

for user in users:
    for skill in list(user["skills"]):        # snapshot the inner
        user["skills"][skill + "!"] = user["skills"][skill]

# The outer loop's dictionary objects were edited in place (their
# KEYS grew), which is allowed because the outer LIST -- users --
# never changed size. The inner keys grew too, and that is safe
# because we walked list(user["skills"]), a snapshot of the keys.

print("first person now:", users[0]["skills"])
# first person now: {'Python': 90, 'JS': 80, 'Python!': 90, 'JS!': 80}

# Restore for the next section, so the rest of the file sees the
# original data:
for user, original in zip(users, snapshot):
    user["skills"] = original

# The pattern to remember: mutating VALUES inside a loop is fine,
# changing the SIZE of the thing you are looping over is not.
# Snapshot what you walk, mutate what you keep.

# ============================================================
# [10] Practical: find the highest skill across everyone
# ============================================================
# Now the two loops work together for a real question: which skill,
# of any person, is the highest? One pass through everything.

best_person = None
best_skill = None
best_value = -1

for user in users:
    for skill, value in user["skills"].items():
        if value > best_value:
            best_value = value
            best_person = user["name"]
            best_skill = skill

print(f"best: {best_skill} ({best_value}%) by {best_person}")
# best: HTML (95%) by Ahmed

# The outer loop supplies WHO, the inner loop supplies WHAT, and
# the if keeps the running champion. If two skills tie, the first
# one found wins, because the test is strict >. That is a
# decision, not an accident -- change it to >= if you want the
# last one found to win instead.

# ============================================================
# [11] Practical: average skill per person
# ============================================================
# The same shape, but the sum resets for each person. That is what
# the placement of total = 0 does: it is OUTSIDE the inner loop,
# INSIDE the outer loop, so each person starts fresh.

for user in users:
    total = 0
    count = 0
    for value in user["skills"].values():
        total += value
        count += 1
    average = total / count
    print(f"  {user['name']:<6} average {average:.1f}%")
#   Osama  average 85.0%
#   Ahmed  average 83.3%
#   Sayid  average 81.5%

# If total = 0 had been placed BEFORE the outer loop, all three
# people would share one running total and the averages would be
# wrong. Indentation decides scope, and scope decides whether the
# number resets. This is the most common nested-loop bug: the
# accumulator in the wrong place.

# ============================================================
# [12] Three levels deep, just to show it scales
# ============================================================
# Nothing magical happens at three levels. A course has modules,
# each module has lessons, each lesson has sections: three loops,
# nested the same way.

course = [
    {"module": "basics", "lessons": ["variables", "strings"]},
    {"module": "loops",  "lessons": ["while", "for", "nested"]},
]

for module in course:                       # level 1: modules
    print(module["module"] + ":")
    for lesson in module["lessons"]:        # level 2: lessons
        print("   ", lesson)
        for part in ("theory", "practice"): # level 3: sections
            print("        -", part)
# loops:
#     while
#         - theory
#         - practice
#     for
#         - theory
#         - practice
#     nested
#         - theory
#         - practice

# (The "basics" module prints first, cut here to save space.)
# The cost multiplies: 2 modules x ~2-3 lessons x 2 parts. At
# three levels you can already print dozens of lines from three
# lines of loop. That power is exactly why the indentation rule
# matters: the deeper you nest, the more a wrong indent costs.

# ============================================================
# [13] The summary
# ============================================================
# A nested loop is two questions, not one:
#
#   outer loop   "WHICH subject?"   the person, the row, the module
#   inner loop   "WHICH detail?"    their skills, the cells, lessons
#
# The inner loop restarts from the top every time the outer loop
# advances, so each subject gets a fresh walk of its own details.
# Total work = outer count x inner count, which is why deep
# nesting explodes.
#
# The three rules that keep nested loops safe:
#
#   1. the accumulator resets INSIDE the outer loop (lesson 11)
#   2. never change the SIZE of what you are walking (lesson 9)
#   3. the inner loop variable does not survive the outer step
#      (lesson 8) -- collect results on purpose if you need them
#
# The transcript's people-and-skills example is the one to carry
# forward: a list of dictionaries on the outside, a dictionary of
# percentages on the inside, and one indented print per detail.
# Every table, every report, every profile page you will write is
# this shape, with different names for "person" and "skill".
