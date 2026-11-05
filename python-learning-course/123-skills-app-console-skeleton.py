# -----------------------------------------------------------------
# Lesson 123: Skills App -- console structure and commands
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : project skeleton, welcome/options menu, input
#            normalization, command validation, dispatch
#            to skill actions, preparing for SQLite wiring
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: begin a practical Skills App,
# combining Python fundamentals, functions and SQLite.
#
#   APP IDEA [00:32] -- manage personal skills: show, add,
#   update, delete, quit
#   INPUT [01:05] -- strip whitespace and normalize case
#   MENU [03:37] -- s/a/u/d/q commands
#   VALIDATION [06:44] -- if/elif/else routes valid commands
#   and warns on invalid input
#   PART ONE [10:04] -- establish the app's structure;
#   fully connect actions to the database in the next lesson
#
# To keep output deterministic and avoid input(), this
# skeleton runs a fixed sequence of sample commands.
# Database-backed functionality is intentionally left as
# the next installment; this lesson demonstrates the app flow.

# ============================================================
# [1] Welcome and options menu [03:37]
# ============================================================
# Present the commands clearly to the user:

MENU = (
    "s - show skills",
    "a - add a skill",
    "u - update a skill",
    "d - delete a skill",
    "q - quit",
)

print("  Welcome to the Skills App")
for option in MENU:
    print(f"  {option}")
#   Welcome to the Skills App
#   s - show skills
#   a - add a skill
#   u - update a skill
#   d - delete a skill
#   q - quit

# ============================================================
# [2] Normalize command input [01:05]
# ============================================================
# Trim spaces and lowercase commands before checking them:

raw_command = "  S  "
command = raw_command.strip().lower()
print(f"  raw command: {raw_command!r}")
print(f"  normalized command: {command}")
#   raw command: '  S  '
#   normalized command: s

# ============================================================
# [3] Normalize skill names [01:05]
# ============================================================
# Trim accidental spaces and capitalize consistently:

raw_skill = "  python basics  "
skill_name = raw_skill.strip().capitalize()
print(f"  raw skill: {raw_skill!r}")
print(f"  normalized skill: {skill_name}")
#   raw skill: '  python basics  '
#   normalized skill: Python basics

# ============================================================
# [4] Define action functions [00:32]
# ============================================================
# These are the command targets; database work will be
# connected in the next project part:

def show_skills():
    """Show the current skills (DB integration follows)."""
    return "show skills action selected"


def add_skill(name):
    """Prepare to add a cleaned skill name."""
    return "add skill: " + name


def update_skill(name):
    """Prepare to update a cleaned skill name."""
    return "update skill: " + name


def delete_skill(name):
    """Prepare to delete a cleaned skill name."""
    return "delete skill: " + name


print(f"  show function ready: {callable(show_skills)}")
print(f"  add function ready: {callable(add_skill)}")
print(f"  update function ready: {callable(update_skill)}")
print(f"  delete function ready: {callable(delete_skill)}")
#   show function ready: True
#   add function ready: True
#   update function ready: True
#   delete function ready: True

# ============================================================
# [5] Validate and dispatch a show command [06:44]
# ============================================================
# if/elif/else selects the function for a valid command:

def dispatch(raw_choice, raw_value=""):
    """Normalize a command, validate it, and return its action."""
    choice = raw_choice.strip().lower()
    value = raw_value.strip().capitalize()

    if choice == "s":
        return show_skills()
    elif choice == "a":
        return add_skill(value)
    elif choice == "u":
        return update_skill(value)
    elif choice == "d":
        return delete_skill(value)
    elif choice == "q":
        return "quit requested"
    else:
        return "Invalid option: choose s, a, u, d or q"


print(f"  dispatch show: {dispatch(' S ')}")
#   dispatch show: show skills action selected

# ============================================================
# [6] Dispatch add, update and delete choices
# ============================================================
# Each command reaches its matching function:

print(f"  dispatch add: {dispatch('a', '  python basics ')}")
print(f"  dispatch update: {dispatch('u', '  sql ')}")
print(f"  dispatch delete: {dispatch('d', '  old skill ')}")
#   dispatch add: add skill: Python basics
#   dispatch update: update skill: Sql
#   dispatch delete: delete skill: Old skill

# ============================================================
# [7] Invalid choices receive a helpful message [06:44]
# ============================================================
# Unknown input follows the final else branch:

print(f"  invalid option: {dispatch('x')}")
#   invalid option: Invalid option: choose s, a, u, d or q

# ============================================================
# [8] Quit command
# ============================================================
# q selects the exit path rather than a skill operation:

print(f"  quit option: {dispatch(' Q ')}")
#   quit option: quit requested

# ============================================================
# [9] Run a predictable command session
# ============================================================
# A fixed command list simulates user choices without
# input(), keeping the lesson repeatable:

sample_commands = (
    ("s", ""),
    ("a", "  python basics "),
    ("u", "  sql "),
    ("d", "  old skill "),
    ("?", ""),
    ("q", ""),
)
responses = [dispatch(choice, value) for choice, value in sample_commands]

print(f"  simulated commands: {len(sample_commands)}")
print(f"  command responses: {responses}")
#   simulated commands: 6
#   command responses: ['show skills action selected', 'add skill: Python basics', 'update skill: Sql', 'delete skill: Old skill', 'Invalid option: choose s, u, a, d or q', 'quit requested']

# ============================================================
# [10] Validate menu commands systematically
# ============================================================
# All menu entries have a defined route:

valid_commands = {"s", "a", "u", "d", "q"}
valid_results = [dispatch(choice) for choice in sorted(valid_commands)]
print(f"  valid command count: {len(valid_commands)}")
print(f"  all valid commands have responses: {len(valid_results) == len(valid_commands)}")
#   valid command count: 5
#   all valid commands have responses: True

# ============================================================
# [11] Show the app boundary for this part [10:04]
# ============================================================
# This installment establishes menu flow and function
# dispatch; persistence wiring comes next:

database_wired = False
print(f"  menu and dispatch ready: {dispatch('s') == 'show skills action selected'}")
print(f"  database operations connected in this part: {database_wired}")
print("  next part: connect these actions to SQLite")
#   menu and dispatch ready: True
#   database operations connected in this part: False
#   next part: connect these actions to SQLite

# ============================================================
# [12] One session: clean, validate, route
# ============================================================
# Main flow facts together:

print(f"  command cleanup: {command}")
print(f"  skill cleanup: {skill_name}")
print(f"  add route: {dispatch('a', skill_name)}")
print(f"  invalid route warns: {dispatch('bad').startswith('Invalid option')}")
print(f"  quit route works: {dispatch('q') == 'quit requested'}")
#   command cleanup: s
#   skill cleanup: Python basics
#   add route: add skill: Python basics
#   invalid route warns: True
#   quit route works: True

# ============================================================
# [13] The summary
# ============================================================
# Skills App structure, from the transcript:
#
#   1. APP [00:05-00:32] -- manage personal skills using
#      show, add, update, delete and quit commands
#   2. INPUT [01:05] -- strip whitespace; normalize command
#      with lower() and skill labels with capitalize()
#   3. MENU [03:37] -- s/a/u/d/q displayed clearly
#   4. FUNCTIONS -- each action has a dedicated function
#      ready to receive SQLite-backed implementation next
#   5. VALIDATION [06:44] -- if/elif/else routes valid
#      choices and gives a helpful warning for invalid ones
#   6. DETERMINISM -- fixed sample commands demonstrate
#      flow without interactive input()
#   7. PART ONE [10:04] -- establishes the program skeleton;
#      database integration follows in the next lesson
#
# A menu is the app's front door; normalization and
# validation decide which function handles each request.
