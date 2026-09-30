# -----------------------------------------------------------------
# Lesson 46: Practical Application - Membership Control
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : in / not in, input, strip/capitalize, list, index, remove, append
# Type     : Educational + Practical Project
# Builder  : local assistant
# -----------------------------------------------------------------
# This application combines everything we learned so far: input,
# string cleaning, lists, conditions, and the membership operators.
# The program asks for a name and then lets the user update it,
# delete it, or apply to join the admins list.

# ============================================================
# [1] The admins list
# ============================================================
# A plain Python list holding the names that are allowed in.

admins = ["Ahmed", "Osama", "Mahmoud", "Anas"]

print("current admins:", admins)
# current admins: ['Ahmed', 'Osama', 'Mahmoud', 'Anas']

# ============================================================
# [2] Cleaning the name: a real trap with capitalize()
# ============================================================
# The lesson uses .capitalize(). Watch what it really does to a
# name that has more than ONE word:
#
#   "MOHAMED AHMED".capitalize()  ->  "Mohamed ahmad"   <- the A is lost!
#   "MOHAMED AHMED".title()      ->  "Mohamed Ahmed"   <- correct
#
# capitalize() uppercases the FIRST letter and LOWERCASES every
# other letter, including the first letter of the other words. It
# is fine for a single word like "ahmed", and wrong for a full
# name. title() is the right tool for a person.

print("'MOHAMED AHMED'.capitalize() ->", "MOHAMED AHMED".capitalize())
print("'MOHAMED AHMED'.title()     ->", "MOHAMED AHMED".title())
# 'MOHAMED AHMED'.capitalize() -> Mohamed ahmad
# 'MOHAMED AHMED'.title()     -> Mohamed Ahmed


def clean_name(raw):
    """Return a tidy person name: trimmed, single spaced, title case."""
    return " ".join(str(raw).strip().split()).title()


# Let us check the cleaner against the tricky inputs.
print("--- checking clean_name ---")
for messy in ["  ahmed  ", "AHMED", "mohamed   ahmed", " Osama  "]:
    print(f"  {messy!r:<22} -> {clean_name(messy)!r}")
#   '  ahmed  '          -> 'Ahmed'
#   'AHMED'              -> 'Ahmed'
#   'mohamed   ahmed'    -> 'Mohamed Ahmed'
#   ' Osama  '           -> 'Osama'

# ============================================================
# [3] index() and remove() can crash
# ============================================================
# Both index() and remove() raise a ValueError when the item is
# NOT in the list. This is the single most common crash in a
# program like this one, and the reason we always test membership
# FIRST with in before calling them.

print("--- why we must check with in first ---")
print('"Anas" in admins      :', "Anas" in admins)
try:
    admins.index("Anas")
    print("index found it")
except ValueError as err:
    print("index crashed:", err)
# "Anas" in admins      : True
# index found it

try:
    admins.index("Sayed")
    print("index found it")
except ValueError as err:
    print("index('Sayed') crashed ->", err)
# index('Sayed') crashed -> 'Sayed' is not in list

# ============================================================
# [4] The real program
# ============================================================
# The whole flow, exactly as the application works.

name = clean_name(input("Enter your name: "))

if name in admins:
    # -----------------------------------------------
    # BRANCH 1: the name is already an admin
    # -----------------------------------------------
    position = admins.index(name) + 1
    print(f"Welcome back, {name}! You are admin number {position}.")

    op = " ".join(input("Choose [Update, Delete]: ").strip().split()).capitalize()

    if op == "Update":
        new_name = clean_name(input("Please enter your new name: "))
        # index() gives the position, and we put the new name there
        admins[admins.index(name)] = new_name
        print(f"Updated: '{name}' became '{new_name}'")

    elif op == "Delete":
        # remove() deletes the first match and shifts the rest
        admins.remove(name)
        print(f"Deleted: '{name}' is no longer an admin")

    else:
        print(f"'{op}' is not Update or Delete, so nothing changed")

else:
    # -----------------------------------------------
    # BRANCH 2: a brand new member
    # -----------------------------------------------
    print(f"This name is not admin: '{name}'")

    add = " ".join(input("Would you like to be added? [Y/N]: ").strip().split()).lower()

    if add in ("y", "yes"):          # membership, just like lesson 45
        admins.append(name)
        print(f"Added: '{name}' is now admin number {len(admins)}")
    elif add in ("n", "no"):
        print("No problem, you were not added")
    else:
        print(f"'{add}' is not yes or no, so nothing changed")

# ============================================================
# [5] The final list
# ============================================================
print("final admins:", admins)
# final admins: ['Mohamed Ahmed', 'Osama', 'Mahmoud', 'Anas']

# ============================================================
# Improvement (from me): the same app with testable functions
# ============================================================
# The program above is fine, but its logic is trapped inside the
# if/else chain, so it cannot be tested without typing into it.
# Moving each job into a small function makes every case checkable.

def find_index(items, wanted):
    """Return the position of wanted, or -1. Never raises."""
    return items.index(wanted) if wanted in items else -1


def update_admin(items, old_name, new_name):
    """Replace a name in place. Return True if it worked."""
    position = find_index(items, old_name)
    if position == -1:
        return False
    items[position] = new_name
    return True


def remove_admin(items, name):
    """Delete a name. Return True if it worked."""
    if name not in items:
        return False
    items.remove(name)
    return True


def add_admin(items, name):
    """Add a name, but never add the same one twice."""
    if name in items:
        return False
    items.append(name)
    return True


# Now we can test every operation without any typing.
print("--- testing the functions ---")
sandbox = ["Ahmed", "Osama", "Mahmoud", "Anas"]

print("find_index Ahmed      :", find_index(sandbox, "Ahmed"))
print("find_index Sayed      :", find_index(sandbox, "Sayed"))
print("update Ahmed -> Ali   :", update_admin(sandbox, "Ahmed", "Ali"))
print("update Sayed -> Omar  :", update_admin(sandbox, "Sayed", "Omar"))
print("remove Anas           :", remove_admin(sandbox, "Anas"))
print("remove Anas again     :", remove_admin(sandbox, "Anas"))
print("add Sayed             :", add_admin(sandbox, "Sayed"))
print("add Sayed again       :", add_admin(sandbox, "Sayed"))
print("sandbox now           :", sandbox)
# find_index Ahmed      : 0
# find_index Sayed      : -1
# update Ahmed -> Ali   : True
# update Sayed -> Omar  : False
# remove Anas           : True
# remove Anas again     : False
# add Sayed             : True
# add Sayed again       : False
# sandbox now           : ['Ali', 'Osama', 'Mahmoud', 'Sayed']

# ============================================================
# [6] Two real notes about this kind of program
# ============================================================
# 1) update() keeps the POSITION, while remove() + append() moves the
#    name to the end. Which one you want is a real decision.
sandbox2 = ["Ahmed", "Osama", "Mahmoud", "Anas"]
sandbox2[sandbox2.index("Osama")] = "Osman"
print("with index assignment :", sandbox2)
sandbox2.remove("Mahmoud")
sandbox2.append("Mahmoud")
print("with remove + append :", sandbox2)
# with index assignment : ['Ahmed', 'Osman', 'Mahmoud', 'Anas']
# with remove + append : ['Ahmed', 'Osman', 'Anas', 'Mahmoud']

# 2) This is a SIMULATION for learning. A real system never asks
#    "are you an admin?" with input(), because anyone can type any
#    name. Real permissions come from a password, a session token,
#    and a server side check. Never trust what the user typed.

# ============================================================
# SUMMARY
# ============================================================
# - in tells us if a name is already an admin, and it is the gate
#   for every other operation.
# - index() and remove() raise ValueError when the item is missing,
#   so always test with in first, or wrap the work in functions
#   that return False instead of crashing.
# - Use title() for a person name, not capitalize(), which lowercases
#   the rest of the string.
# - admins[index(name)] = new_name updates in place; remove() then
#   append() moves the name to the end of the list.
# - "y" in ("y", "yes") is a neat way to accept two spellings.
# - Always give the else branch a real message, and never add the
#   same name twice.

# ============================================================
# NEXT LESSON: Advanced string formatting and multi-line output
# ============================================================
