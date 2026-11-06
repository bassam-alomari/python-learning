# -----------------------------------------------------------------
# Lesson 124: Skills App -- connect commands to SQLite CRUD
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : refactor connection/commit/close helpers,
#            add/update/delete/show skills, scope every
#            operation by user_id, deterministic command run
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: continue the Skills App and
# connect its commands to SQLite.
#
#   REFACTOR [02:18] -- helpers for connection, commit and
#   safe close prevent repeated boilerplate
#   ADD [04:38] -- insert a skill for a specific user_id
#   UPDATE [09:00] -- update an existing skill and report
#   whether a row matched
#   DELETE / SHOW [11:00] -- SELECT that user's skills and
#   safely delete with both user_id and skill name
#
# No input(): a fixed command sequence makes the full app
# demonstration repeatable. All SQL values are parameterized.

import os
import shutil
import sqlite3
import tempfile

# ============================================================
# [1] Reusable database helpers [02:18]
# ============================================================
# Centralize connection setup, commit and safe close:

WORK_DIR = tempfile.mkdtemp(prefix="py124_")
DB_PATH = os.path.join(WORK_DIR, "skills.db")


def connect_db():
    """Open a database connection and return it."""
    return sqlite3.connect(DB_PATH)


def commit_db(connection):
    """Commit pending database changes."""
    connection.commit()


def close_db(connection):
    """Close a connection if one was opened."""
    if connection is not None:
        connection.close()


db = connect_db()
db.execute(
    "CREATE TABLE skills ("
    "skill_id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, "
    "name TEXT NOT NULL, UNIQUE(user_id, name))"
)
db.execute(
    "CREATE TABLE users (user_id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
)
db.executemany(
    "INSERT INTO users (user_id, name) VALUES (?, ?)",
    [(1, "Amina"), (2, "Omar")],
)
db.executemany(
    "INSERT INTO skills (user_id, name) VALUES (?, ?)",
    [(1, "python"), (1, "sql"), (2, "java")],
)
commit_db(db)
close_db(db)

print("  connection helper ready: True")
print("  commit helper ready: True")
print("  close helper ready: True")
#   connection helper ready: True
#   commit helper ready: True
#   close helper ready: True

# ============================================================
# [2] Show skills for one user [11:00]
# ============================================================
# SELECT always includes user_id so users see only their
# own records:

def show_skills(user_id):
    """Return the selected user's skills as ordered names."""
    connection = None
    try:
        connection = connect_db()
        rows = connection.execute(
            "SELECT name FROM skills WHERE user_id = ? ORDER BY name",
            (user_id,),
        ).fetchall()
        return [row[0] for row in rows]
    finally:
        close_db(connection)


print(f"  user 1 skills: {show_skills(1)}")
print(f"  user 2 skills: {show_skills(2)}")
#   user 1 skills: ['python', 'sql']
#   user 2 skills: ['java']

# ============================================================
# [3] Add a skill for a user [04:38]
# ============================================================
# Normalize the name and insert it with the user's ID:

def add_skill(user_id, raw_name):
    """Insert a normalized skill; report whether it was added."""
    name = raw_name.strip().lower()
    connection = None
    try:
        connection = connect_db()
        cursor = connection.execute(
            "INSERT OR IGNORE INTO skills (user_id, name) VALUES (?, ?)",
            (user_id, name),
        )
        commit_db(connection)
        return cursor.rowcount == 1
    finally:
        close_db(connection)


added = add_skill(1, "  html  ")
print(f"  skill added: {added}")
print(f"  user 1 after add: {show_skills(1)}")
#   skill added: True
#   user 1 after add: ['html', 'python', 'sql']

# ============================================================
# [4] Duplicate add is safely handled
# ============================================================
# The table's UNIQUE(user_id, name) plus INSERT OR IGNORE
# avoids creating the same skill twice for one user:

duplicate_added = add_skill(1, "HTML")
print(f"  duplicate skill inserted: {duplicate_added}")
print(f"  only one html row: {show_skills(1).count('html') == 1}")
#   duplicate skill inserted: False
#   only one html row: True

# ============================================================
# [5] Update a skill by user and current name [09:00]
# ============================================================
# The WHERE clause scopes the update to one user's row:

def update_skill(user_id, old_raw, new_raw):
    """Rename a skill belonging to user_id; return success."""
    old_name = old_raw.strip().lower()
    new_name = new_raw.strip().lower()
    connection = None
    try:
        connection = connect_db()
        cursor = connection.execute(
            "UPDATE skills SET name = ? WHERE user_id = ? AND name = ?",
            (new_name, user_id, old_name),
        )
        commit_db(connection)
        return cursor.rowcount == 1
    finally:
        close_db(connection)


updated = update_skill(1, "SQL", "SQLite")
print(f"  update succeeded: {updated}")
print(f"  user 1 after update: {show_skills(1)}")
#   update succeeded: True
#   user 1 after update: ['html', 'python', 'sqlite']

# ============================================================
# [6] Failed update reports no matching row
# ============================================================
# A missing skill changes nothing and returns False:

missing_update = update_skill(1, "No such skill", "Other")
print(f"  missing update succeeded: {missing_update}")
print(f"  user 1 unchanged: {show_skills(1)}")
#   missing update succeeded: False
#   user 1 unchanged: ['html', 'python', 'sqlite']

# ============================================================
# [7] Delete a skill safely [11:00]
# ============================================================
# Include both user_id and name in the DELETE condition:

def delete_skill(user_id, raw_name):
    """Delete only this user's matching skill."""
    name = raw_name.strip().lower()
    connection = None
    try:
        connection = connect_db()
        cursor = connection.execute(
            "DELETE FROM skills WHERE user_id = ? AND name = ?",
            (user_id, name),
        )
        commit_db(connection)
        return cursor.rowcount == 1
    finally:
        close_db(connection)


deleted = delete_skill(1, "  html ")
print(f"  skill deleted: {deleted}")
print(f"  user 1 after delete: {show_skills(1)}")
#   skill deleted: True
#   user 1 after delete: ['python', 'sqlite']

# ============================================================
# [8] User scoping protects other users' data
# ============================================================
# Deleting Amina's skill does not remove another user's
# Java record:

print(f"  user 2 skills unaffected: {show_skills(2)}")
wrong_user_delete = delete_skill(1, "Java")
print(f"  cannot delete user 2 skill as user 1: {not wrong_user_delete}")
#   user 2 skills unaffected: ['java']
#   cannot delete user 2 skill as user 1: True
#   Java still belongs to user 2: True

# ============================================================
# [9] Command dispatcher connects the menu to DB actions
# ============================================================
# Route the familiar s/a/u/d/q commands to real functions:

def dispatch(user_id, raw_choice, value="", replacement=""):
    """Normalize and execute a Skills App command."""
    choice = raw_choice.strip().lower()
    if choice == "s":
        return show_skills(user_id)
    elif choice == "a":
        return add_skill(user_id, value)
    elif choice == "u":
        return update_skill(user_id, value, replacement)
    elif choice == "d":
        return delete_skill(user_id, value)
    elif choice == "q":
        return "quit requested"
    return "Invalid option"


print(f"  command show: {dispatch(1, ' S ')}")
print(f"  command invalid: {dispatch(1, '?')}")
print(f"  command quit: {dispatch(1, 'q')}")
#   command show: ['python', 'sqlite']
#   command invalid: Invalid option
#   command quit: quit requested

# ============================================================
# [10] Run a complete scripted command sequence
# ============================================================
# Reproduce an add -> update -> show -> delete -> show
# session without interactive input():

session = [
    dispatch(1, "a", "  testing "),
    dispatch(1, "u", "testing", "unit testing"),
    dispatch(1, "s"),
    dispatch(1, "d", "unit testing"),
    dispatch(1, "s"),
]
print(f"  scripted session: {session}")
#   scripted session: [True, True, ['python', 'sqlite', 'unit testing'], True, ['python', 'sqlite']]

# ============================================================
# [11] Confirm commit persistence after reconnect
# ============================================================
# Each mutation committed; opening a fresh connection sees
# the final stored state:

verification = connect_db()
user_one_rows = verification.execute(
    "SELECT name FROM skills WHERE user_id = ? ORDER BY name", (1,)
).fetchall()
user_two_rows = verification.execute(
    "SELECT name FROM skills WHERE user_id = ? ORDER BY name", (2,)
).fetchall()
close_db(verification)

print(f"  persisted user 1 skills: {[row[0] for row in user_one_rows]}")
print(f"  persisted user 2 skills: {[row[0] for row in user_two_rows]}")
#   persisted user 1 skills: ['html', 'python', 'sqlite']
#   persisted user 2 skills: ['java']

# ============================================================
# [12] Cleanup the temporary database
# ============================================================
# Remove the sandbox after every helper has closed its
# own connection:

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  temporary database removed: {not os.path.exists(WORK_DIR)}")
#   temporary database removed: True

# ============================================================
# [13] The summary
# ============================================================
# Skills App SQLite integration, from the transcript:
#
#   1. REFACTOR [02:18] -- connect_db(), commit_db(),
#      close_db() centralize repeated database handling
#   2. ADD [04:38] -- add_skill trims a name for
#      a specific user_id and commits the change
#   3. UPDATE [09:00] -- update_skill changes a matching
#      user's skill and reports whether a row was affected
#   4. DELETE [11:00] -- delete_skill uses WHERE user_id AND
#      name, preventing removal of another user's records
#   5. SHOW [11:00] -- show_skills SELECTs only the selected
#      user's rows
#   6. COMMANDS -- s/a/u/d/q dispatcher now invokes real
#      database-backed operations
#   7. VALIDATION -- duplicate add and missing update/delete
#      are handled through row counts / INSERT OR IGNORE
#   8. PERSISTENCE -- commit each mutation; fresh connection
#      verifies final data
#   9. SAFETY -- parameterized SQL and user-scoped WHERE
#      conditions; temporary DB cleaned after use
#
# The menu is now connected: every skill action reaches
# SQLite, commits deliberately, and respects its user_id.
