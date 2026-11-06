# -----------------------------------------------------------------
# Lesson 126: Skills App -- find, update or offer to add
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : user-scoped skill lookup, update existing
#            progress, detect missing skills, optionally add,
#            detect duplicate names, and confirm before changes
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript is noisy, but the practical flow appears to be:
#
#   1. Identify the current user and target skill.
#   2. Search only that user's rows by user_id + skill name.
#   3. If found, update that skill's progress.
#   4. If absent, offer to add it; don't silently duplicate.
#   5. Before inserting, check it isn't already present.
#   6. Confirm duplicate/previously existing data and ask
#      before changing it.
#
# This lesson demonstrates that flow using deterministic
# scripted answers instead of interactive input(). All SQL
# is parameterized and scoped by user_id.

import os
import shutil
import sqlite3
import tempfile

# ============================================================
# [1] Prepare an isolated user/skills database
# ============================================================
# Two users have similar data, so scoping is testable:

WORK_DIR = tempfile.mkdtemp(prefix="py126_")
DB_PATH = os.path.join(WORK_DIR, "skills.db")
db = sqlite3.connect(DB_PATH)
db.execute(
    "CREATE TABLE skills ("
    "skill_id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, "
    "name TEXT NOT NULL, progress INTEGER NOT NULL, "
    "UNIQUE(user_id, name))"
)
db.executemany(
    "INSERT INTO skills (user_id, name, progress) VALUES (?, ?, ?)",
    [(1, "python", 70), (1, "sql", 35), (2, "python", 90)],
)
db.commit()
db.close()


def connect_db():
    """Open the demo database."""
    return sqlite3.connect(DB_PATH)


def close_db(connection):
    """Close a live connection safely."""
    if connection is not None:
        connection.close()


print("  database prepared: True")
#   database prepared: True

# ============================================================
# [2] Find a skill for this user before editing
# ============================================================
# Always match both user_id and normalized skill name:

def find_skill(user_id, raw_name):
    """Return one user's matching skill row or None."""
    name = raw_name.strip().lower()
    connection = None
    try:
        connection = connect_db()
        return connection.execute(
            "SELECT skill_id, name, progress FROM skills "
            "WHERE user_id = ? AND name = ?",
            (user_id, name),
        ).fetchone()
    finally:
        close_db(connection)


found = find_skill(1, "  Python ")
print(f"  user 1 skill found: {found}")
print(f"  user 1 missing skill: {find_skill(1, 'rust')}")
#   user 1 skill found: (1, 'python', 70)
#   user 1 missing skill: None

# ============================================================
# [3] Update an existing skill after confirmation
# ============================================================
# Confirmed updates change only the selected user's row:

def update_existing(user_id, raw_name, new_progress, confirmed):
    """Update existing progress only after confirmation."""
    if not confirmed:
        return "cancelled"
    if not 0 <= new_progress <= 100:
        return "invalid progress"
    row = find_skill(user_id, raw_name)
    if row is None:
        return "not found"

    connection = None
    try:
        connection = connect_db()
        cursor = connection.execute(
            "UPDATE skills SET progress = ? WHERE user_id = ? AND name = ?",
            (new_progress, user_id, row[1]),
        )
        connection.commit()
        return "updated" if cursor.rowcount == 1 else "not found"
    finally:
        close_db(connection)


update_result = update_existing(1, "python", 85, confirmed=True)
print(f"  confirmed existing skill result: {update_result}")
print(f"  updated row: {find_skill(1, 'python')}")
#   confirmed existing skill result: updated
#   updated row: (1, 'python', 85)

# ============================================================
# [4] A missing skill is detected, not silently changed
# ============================================================
# Without an add choice, a missing name remains absent:

missing_update = update_existing(1, "rust", 20, confirmed=True)
print(f"  update missing skill: {missing_update}")
print(f"  still absent after update: {find_skill(1, 'rust') is None}")
#   update missing skill: not found
#   still absent after update: True

# ============================================================
# [5] Ask whether to add a missing skill
# ============================================================
# Simulate the user choosing Yes/No with a supplied value:

def add_if_missing(user_id, raw_name, progress, user_choice):
    """Offer an insert for a missing skill; honor user choice."""
    name = raw_name.strip().lower()
    existing = find_skill(user_id, name)
    if existing is not None:
        return "already exists"
    if not user_choice:
        return "not added"
    if not 0 <= progress <= 100:
        return "invalid progress"

    connection = None
    try:
        connection = connect_db()
        cursor = connection.execute(
            "INSERT OR IGNORE INTO skills (user_id, name, progress) "
            "VALUES (?, ?, ?)",
            (user_id, name, progress),
        )
        connection.commit()
        return "added" if cursor.rowcount == 1 else "already exists"
    finally:
        close_db(connection)


add_no = add_if_missing(1, "Rust", 20, user_choice=False)
add_yes = add_if_missing(1, "Rust", 20, user_choice=True)
print(f"  missing skill declined: {add_no}")
print(f"  missing skill accepted: {add_yes}")
print(f"  newly added row: {find_skill(1, 'rust')}")
#   missing skill declined: not added
#   missing skill accepted: added
#   newly added row: (4, 'rust', 20)

# ============================================================
# [6] Detect a duplicate before offering an insert
# ============================================================
# A case/space-normalized existing skill is not duplicated:

duplicate_result = add_if_missing(1, "  RUST ", 50, user_choice=True)
print(f"  duplicate insertion result: {duplicate_result}")
print(f"  only one Rust row: {find_skill(1, 'rust') is not None}")
#   duplicate insertion result: already exists
#   only one Rust row: True

# ============================================================
# [7] Existing skill: ask before overwriting [transcript]
# ============================================================
# A declined update preserves the existing value:

cancelled_update = update_existing(1, "sql", 99, confirmed=False)
print(f"  existing update declined: {cancelled_update}")
print(f"  SQL progress unchanged: {find_skill(1, 'sql')}")
#   existing update declined: cancelled
#   SQL progress unchanged: (2, 'sql', 35)

# ============================================================
# [8] Same skill name for a different user is separate
# ============================================================
# user 2's Python record does not collide with user 1's:

user_two_python = find_skill(2, "python")
print(f"  user 2 Python row: {user_two_python}")
print(f"  separate user-scoped record: {user_two_python[2] != find_skill(1, 'python')[2]}")
#   user 2 Python row: (3, 'python', 90)
#   separate user-scoped record: True

# ============================================================
# [9] Show a user's skills after all actions
# ============================================================
# Display only records belonging to the selected user:

def show_skills(user_id):
    """Return ordered names/progress for this user only."""
    connection = None
    try:
        connection = connect_db()
        return connection.execute(
            "SELECT name, progress FROM skills WHERE user_id = ? ORDER BY name",
            (user_id,),
        ).fetchall()
    finally:
        close_db(connection)


print(f"  user 1 skills: {show_skills(1)}")
print(f"  user 2 skills: {show_skills(2)}")
#   user 1 skills: [('python', 85), ('rust', 20), ('sql', 35)]
#   user 2 skills: [('python', 90)]

# ============================================================
# [10] Report CRUD results
# ============================================================
# Summarize the requested scenarios:

results = {
    "existing updated": update_result == "updated",
    "missing declined": add_no == "not added",
    "missing added": add_yes == "added",
    "duplicate blocked": duplicate_result == "already exists",
    "overwrite declined": cancelled_update == "cancelled",
}
print(f"  result checks: {results}")
print(f"  all scenarios handled: {all(results.values())}")
#   result checks: {'existing updated': True, 'missing declined': True, 'missing added': True, 'duplicate blocked': True, 'overwrite declined': True}
#   all scenarios handled: True

# ============================================================
# [11] Fresh connection verifies committed data
# ============================================================
# Reopen to confirm changes persisted to SQLite:

verification = connect_db()
verified_rows = verification.execute(
    "SELECT name, progress FROM skills WHERE user_id = ? ORDER BY name",
    (1,),
).fetchall()
close_db(verification)
print(f"  persisted user 1 rows: {verified_rows}")
#   persisted user 1 rows: [('python', 85), ('rust', 20), ('sql', 35)]

# ============================================================
# [12] Cleanup temporary database
# ============================================================
# Every helper closes its own connection; remove the file:

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  database sandbox removed: {not os.path.exists(WORK_DIR)}")
#   database sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# Smart skill update/add flow, from the transcript:
#
#   1. FIND -- search the selected user's skill by
#      user_id + normalized name before changing anything
#   2. FOUND -- offer/confirm update, then change only that
#      row's progress
#   3. MISSING -- report absent; if user declines, leave it
#      absent; if accepted, insert it
#   4. DUPLICATE -- check again before insert; do not create
#      a second same-named skill for that user
#   5. SCOPE -- same skill name can exist for another user;
#      every SELECT/UPDATE/INSERT uses user_id
#   6. VALIDATE -- progress restricted to 0..100; declined
#      changes do not overwrite existing values
#   7. PERSIST -- commit each accepted update/insert, then
#      verify using a fresh connection
#
# Find first, then ask; update if present, offer add if
# absent, and never overwrite or duplicate without consent.
