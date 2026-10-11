# -----------------------------------------------------------------
# Lesson 55: advanced dictionary loops - nested dictionaries
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : dict inside dict, outer items(), inner items(), formatting
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lesson 52 looped over one flat dictionary. Lesson 53 put people
# in a list and looped two levels. This lesson closes the set: a
# dictionary whose VALUES are themselves dictionaries, and the two
# nested for loops that read it.
#
# The transcript's shape: a main technology (HTML, CSS) with an
# inner dictionary of sub-skills and their percentages. Outer loop
# walks the technologies, inner loop walks each technology's
# details.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] Quick review: one flat dictionary, one items() loop
# ============================================================
# Everything from lesson 52, in ten lines, because the nested
# version is this loop with one more layer on top.

my_skills = {"HTML": 90, "CSS": 80, "JS": 70, "Python": 90}

for skill, value in my_skills.items():
    print(f"{skill} => {value}%")
# HTML => 90%
# CSS => 80%
# JS => 70%
# Python => 90%

# One level: key is a string, value is a number. Now imagine each
# value were a dictionary instead of a number. That single change
# is the whole lesson.

# ============================================================
# [2] Two ways to read a value: brackets vs unpacking
# ============================================================
# The transcript compares the two. Both print the same number,
# but only one works inside a loop without knowing the key first.

skill = "CSS"

print("brackets:", my_skills[skill])       # you must have the key
# brackets: 80

for key, value in my_skills.items():
    if key == "CSS":
        print("unpacking:", value)          # the loop hands it over
# unpacking: 80

# brackets   my_skills[skill]   fast, but YOU supply the key
# unpacking  for key, value     the loop supplies both halves
#
# When you are walking the dictionary yourself, unpacking wins:
# one pass, no lookups, no KeyError risk. When you already hold a
# specific key outside any loop, brackets win: direct and short.
#
# The KeyError trap with brackets:

missing = my_skills["SQL"] if "SQL" in my_skills else "absent"
print("missing key handled:", missing)
# missing key handled: absent

# brackets on a key that does not exist raises KeyError. The
# unpacking loop cannot hit that bug -- it only ever sees keys
# that are really there. (Dictionary .get() is the other guard,
# covered in the lesson files for dictionary methods.)

# ============================================================
# [3] The nested data: my_ultimate_skills
# ============================================================
# The transcript's structure. Each MAIN key (HTML, CSS) maps to an
# INNER dictionary of sub-skills: "Main" for the core, plus a
# framework or preprocessor per technology.

my_ultimate_skills = {
    "HTML": {"Main": 80, "Pugs": 50},
    "CSS":  {"Main": 90, "Sass": 70},
}

print("top-level keys:", list(my_ultimate_skills.keys()))
# top-level keys: ['HTML', 'CSS']

# Two levels deep:
#
#   "HTML"                     the main key
#       {"Main": 80, ...}      the value IS a dictionary
#           "Main"  ->  80     the child key and child value
#
# A flat loop over this gives you the main keys and the inner
# dictionaries as opaque blobs -- it cannot see the percentages.

for main_key in my_ultimate_skills:
    print("flat loop sees:", main_key, "->", my_ultimate_skills[main_key])
# flat loop sees: HTML -> {'Main': 80, 'Pugs': 50}
# flat loop sees: CSS -> {'Main': 90, 'Sass': 70}

# That printed the inner dictionaries raw. The percentages are in
# there, but not readable yet. Two loops fix that.

# ============================================================
# [4] The shape: outer items(), inner items()
# ============================================================
# The transcript's two steps: the outer loop takes the main key
# and the inner dictionary, the inner loop takes the child key and
# the child number.

for main_key, main_value in my_ultimate_skills.items():     # outer
    print(main_key + ":")
    for child_key, child_value in main_value.items():       # inner
        print(f"   {child_key} = {child_value}%")
# HTML:
#    Main = 80%
#    Pugs = 50%
# CSS:
#    Main = 90%
#    Sass = 70%

# Read the left sides carefully:
#
#   main_key, main_value       from the OUTER items()
#                              main_value is a dict
#   child_key, child_value     from main_value.items()
#                              child_value is the number
#
# The inner loop is written against main_value -- the VALUE the
# outer loop just unpacked. That handoff is the entire trick: the
# outer loop's value becomes the inner loop's dictionary.

# ============================================================
# [5] The formatted card the transcript asks for
# ============================================================
# Same two loops, with the alignment and separators from lessons
# 52 and 53.

print()
for main_key, main_value in my_ultimate_skills.items():
    print(f"  {main_key}")
    print("  " + "-" * 14)
    for child_key, child_value in main_value.items():
        print(f"    {child_key:<8} {child_value}%")
    print()
#   HTML
#   --------------
#     Main     80%
#     Pugs     50%
#
#   CSS
#   --------------
#     Main     90%
#     Sass     70%
#

# One header per main key, one line per child, a blank line to
# separate the cards. The structure of the OUTPUT mirrors the
# structure of the DATA: two levels in the dictionary, two levels
# of indentation on screen.

# ============================================================
# [6] Counting the work: 2 main keys x 2 children = 4 lines
# ============================================================
# The multiplication rule from lesson 53 still holds, one level
# deeper: total detail lines = sum over main keys of
# len(their inner dictionary).

detail = 0
for main_key, main_value in my_ultimate_skills.items():
    detail += len(main_value)
print("detail lines:", detail)
# detail lines: 4

print("header lines:", len(my_ultimate_skills))
# header lines: 2

print("total:", len(my_ultimate_skills) + detail)
# total: 6

# Grow one inner dictionary to 5 children and the detail count
# jumps without touching a single loop line. The loops describe
# the SHAPE, the nested dictionary supplies the content -- the
# same data-driven rule as lesson 52, now with two shapes stacked.

# ============================================================
# [7] Reaching one level with brackets, and why loops are better
# ============================================================
# You CAN pull a single nested value without any loop:

sass = my_ultimate_skills["CSS"]["Sass"]
print("one value:", sass)
# one value: 70

# Two bracket pairs = two levels of keys, each one must be
# spelled exactly right, and either one missing raises KeyError.
# That is fine for a known path (you are certain CSS has Sass).
# It does not scale to WALKING everything:

total = 0
for main_value in my_ultimate_skills.values():       # only 1 loop
    for child_value in main_value.values():          # this is the 2nd
        total += child_value
print("sum of all percentages:", total)
# sum of all percentages: 290

# Even "just the numbers" needs both loops: the outer .values()
# gives inner dictionaries, the inner .values() gives numbers.
# You never write a single key name, so a renamed or added key
# cannot break this code.

# ============================================================
# [8] A deeper nest: three levels, same pattern
# ============================================================
# Nothing new appears at three levels. One more indentation, one
# more items().

report = {
    "frontend": {
        "HTML": {"Main": 80, "Pugs": 50},
        "CSS":  {"Main": 90, "Sass": 70},
    },
    "backend": {
        "Python": {"Main": 95},
    },
}

for area, technologies in report.items():                # level 1
    print(area + ":")
    for tech, details in technologies.items():           # level 2
        print(f"   {tech}")
        for child_key, child_value in details.items():   # level 3
            print(f"        {child_key} = {child_value}")
# frontend:
#    HTML
#         Main = 80
#         Pugs = 50
#    CSS
#         Main = 90
#         Sass = 70
# backend:
#    Python
#         Main = 95

# Each level unpacks items() into two names, and the inner loop
# iterates over whichever name holds the next dictionary. The
# variable names (area, technologies, tech, details) are chosen to
# say WHERE you are in the tree -- that readability is free, and
# it is what keeps three-level nests readable.

# ============================================================
# [9] Trap: confusing main_value with child_value
# ============================================================
# The classic nested-loop bug: using the outer value inside the
# inner loop as if it were the number.

# WRONG -- main_value is a dict, not a percentage:
# for main_key, main_value in my_ultimate_skills.items():
#     print(main_key, main_value + 1)      # TypeError: unsupported

# The interpreter tells you immediately (dict + int), so this one
# fails loudly. The quieter version is naming:

for main_key, main_value in my_ultimate_skills.items():
    for child_key, child_value in main_value.items():
        pass
# here main_value is the inner dict, child_value is the number.
# Calling the number "main_value" anywhere below this point is
# how the confusion starts.

# The habit: main_* names live OUTSIDE the inner for line,
# child_* names live on or after it. The indentation tells you
# which scope you are in, and the names should agree with it.

# ============================================================
# [10] Practical: flatten the nest into rows
# ============================================================
# Real code often turns a nested dictionary into a flat list of
# rows -- one row per (technology, sub-skill, percentage) -- for a
# table, a CSV, or a chart. The two loops build it in one pass.

rows = []
for main_key, main_value in my_ultimate_skills.items():
    for child_key, child_value in main_value.items():
        rows.append((main_key, child_key, child_value))

for row in rows:
    print(row)
# ('HTML', 'Main', 80)
# ('HTML', 'Pugs', 50)
# ('CSS', 'Main', 90)
# ('CSS', 'Sass', 70)

print("rows:", len(rows))
# rows: 4

# The nested structure was convenient for storage and display; the
# flat structure is convenient for computation. The two loops are
# the converter between the two worlds, and it costs one pass.

# ============================================================
# [11] Practical: the best sub-skill across the whole nest
# ============================================================
# Same shape as lesson 53's "highest skill", one level deeper.
# The champion variables sit OUTSIDE the outer loop so they
# survive all iterations.

best_main = None
best_child = None
best_value = -1

for main_key, main_value in my_ultimate_skills.items():
    for child_key, child_value in main_value.items():
        if child_value > best_value:
            best_value = child_value
            best_main = main_key
            best_child = child_key

print(f"best: {best_main} / {best_child} = {best_value}%")
# best: CSS / Main = 90%

# If two sub-skills tie, the first found wins (strict >). Same
# decision as lesson 53: change to >= if you want the last one.
# The accumulation discipline is identical too: anything reset
# inside the outer loop belongs to ONE main key, anything outside
# belongs to the WHOLE run.

# ============================================================
# [12] Practical: average per main key
# ============================================================
# The accumulator placement rule, now with names that say which
# level they serve.

for main_key, main_value in my_ultimate_skills.items():
    total = 0                              # inside outer: resets per tech
    for child_value in main_value.values():
        total += child_value
    average = total / len(main_value)
    print(f"  {main_key:<6} average {average:.1f}%")
#   HTML   average 65.0%
#   CSS    average 80.0%

# total = 0 sits INSIDE the outer loop, so HTML's 130 and CSS's
# 160 never mix. Move it above the outer loop and you get one
# grand average of everything -- which is a different question,
# answered by different placement, not different code. Indentation
# is the query language here.

# ============================================================
# [13] The summary
# ============================================================
# Every loop-over-a-dictionary shape the course has now covered:
#
#   flat dict        for key, value in d.items()
#   list of dicts    for user in users:  for k, v in user.items()
#   dict of dicts    for main, inner in d.items():
#                        for child, value in inner.items()
#   three levels     add one more indentation, one more items()
#
# The two rules that make the nested version work:
#
#   1. the inner loop iterates over the VALUE the outer loop
#      unpacked -- main_value.items() is the handoff point
#   2. brackets answer KNOWN paths (d["CSS"]["Sass"]),
#      loops answer WALK-EVERYTHING questions; reaching for the
#      wrong one is most nested-dict bugs
#
# And the naming rule that keeps three-level code readable: the
# variable names should say which level they live on -- main_*
# outside the inner for, child_* on it. The transcript's
# my_ultimate_skills with HTML/Main/Pugs and CSS/Main/Sass is the
# picture to keep: two cards, two loops, one handoff line.
#
# With this lesson the loop-over-dictionaries set is complete --
# simple, listed, nested, and as deep as your data goes.
