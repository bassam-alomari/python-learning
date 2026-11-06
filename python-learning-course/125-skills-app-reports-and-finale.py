# -----------------------------------------------------------------
# Lesson 125: Skills App -- polished display and project finale
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : formatted per-user skills with progress percent,
#            friendly empty-state message, SQLite CRUD recap,
#            summary statistics and complete scripted flow
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: final Skills App installment --
# improve the display and add useful progress/reporting.
#
#   SHOW [02:10] -- fetch only one user's skills (WHERE
#   user_id = ?) and display name plus completion percent
#   EMPTY STATE [06:12] -- show a friendly message if no
#   skills are registered instead of a blank screen
#   FINALE [07:30] -- add, update, delete and show are all
#   connected to SQLite in the completed project
#
# A deterministic command sequence replaces input(); the
# database is temporary and removed after the demonstration.

import os
import shutil
import sqlite3
import tempfile

# ============================================================
# [1] Create a temporary multi-user skills database
# ============================================================
# Each skill has a name and progress percentage:

WORK_DIR = tempfile.mkdtemp(prefix="py125_")
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
    [(1, "python", 80), (1, "sql", 45), (2, "java", 30)],
)
db.commit()
db.close()

print(f"  skills database prepared: {os.path.exists(DB_PATH)}")
#   skills database prepared: True

# ============================================================
# [2] Reusable connect and close helpers
# ============================================================
# Keep connection management consistent across operations:

def connect_db():
    """Open a connection to the temporary Skills database."""
    return sqlite3.connect(DB_PATH)


def close_db(connection):
    """Close a connection if it was opened."""
    if connection is not None:
        connection.close()


print(f"  connection helper ready: {callable(connect_db)}")
print(f"  close helper ready: {callable(close_db)}")
#   connection helper ready: True
#   close helper ready: True

# ============================================================
# [3] Show skills for one user with progress [02:10]
# ============================================================
# WHERE user_id = ? prevents showing other users' data:

def show_skills(user_id):
    """Return formatted progress rows for just this user."""
    connection = None
    try:
        connection = connect_db()
        rows = connection.execute(
            "SELECT name, progress FROM skills "
            "WHERE user_id = ? ORDER BY name",
            (user_id,),
        ).fetchall()
        if not rows:
            return ["No skills registered yet."]
        return [f"{name}: {progress}%" for name, progress in rows]
    finally:
        close_db(connection)


user_one_display = show_skills(1)
for line in user_one_display:
    print(f"  {line}")
#   python: 80%
#   sql: 45%

# ============================================================
# [4] Empty-state message [06:12]
# ============================================================
# A user with no saved skills receives a helpful notice:

empty_display = show_skills(3)
print(f"  empty user display: {empty_display}")
print(f"  friendly empty message: {empty_display == ['No skills registered yet.']}")
#   empty user display: ['No skills registered yet.']
#   friendly empty message: True

# ============================================================
# [5] Add a skill with progress
# ============================================================
# Normalize the skill name and save its starting progress:

def add_skill(user_id, raw_name, progress=0):
    """Add one skill for a user; return whether it was inserted."""
    name = raw_name.strip().lower()
    if not 0 <= progress <= 100:
        return False
    connection = None
    try:
        connection = connect_db()
        cursor = connection.execute(
            "INSERT OR IGNORE INTO skills (user_id, name, progress) "
            "VALUES (?, ?, ?)",
            (user_id, name, progress),
        )
        connection.commit()
        return cursor.rowcount == 1
    finally:
        close_db(connection)


added = add_skill(1, "  Regex ", 20)
print(f"  skill added: {added}")
print(f"  updated user 1 display: {show_skills(1)}")
#   skill added: True
#   updated user 1 display: ['python: 80%', 'regex: 20%', 'sql: 45%']

# ============================================================
# [6] Update progress safely
# ============================================================
# The update is scoped by both user_id and skill name:

def update_progress(user_id, raw_name, progress):
    """Set progress in the 0..100 range for one user's skill."""
    if not 0 <= progress <= 100:
        return False
    name = raw_name.strip().lower()
    connection = None
    try:
        connection = connect_db()
        cursor = connection.execute(
            "UPDATE skills SET progress = ? WHERE user_id = ? AND name = ?",
            (progress, user_id, name),
        )
        connection.commit()
        return cursor.rowcount == 1
    finally:
        close_db(connection)


updated = update_progress(1, "regex", 65)
invalid_progress = update_progress(1, "regex", 120)
print(f"  progress updated: {updated}")
print(f"  invalid progress rejected: {not invalid_progress}")
print(f"  display after update: {show_skills(1)}")
#   progress updated: True
#   invalid progress rejected: True
#   display after update: ['python: 80%', 'regex: 65%', 'sql: 45%']

# ============================================================
# [7] Delete one user's skill
# ============================================================
# DELETE uses user_id and skill name together:

def delete_skill(user_id, raw_name):
    """Delete only the named skill belonging to user_id."""
    name = raw_name.strip().lower()
    connection = None
    try:
        connection = connect_db()
        cursor = connection.execute(
            "DELETE FROM skills WHERE user_id = ? AND name = ?",
            (user_id, name),
        )
        connection.commit()
        return cursor.rowcount == 1
    finally:
        close_db(connection)


deleted = delete_skill(1, "sql")
print(f"  skill deleted: {deleted}")
print(f"  user 1 after delete: {show_skills(1)}")
#   skill deleted: True
#   user 1 after delete: ['python: 80%', 'regex: 65%']

# ============================================================
# [8] User scoping keeps other skills private
# ============================================================
# User 2's Java record is not included in user 1's display:

print(f"  user 2 display: {show_skills(2)}")
wrong_owner_delete = delete_skill(1, "java")
print(f"  user 1 cannot delete user 2 skill: {not wrong_owner_delete}")
print(f"  user 2 still has Java: {show_skills(2) == ['java: 30%']}")
#   user 2 display: ['java: 30%']
#   user 1 cannot delete user 2 skill: True
#   user 2 still has Java: True

# ============================================================
# [9] Summary statistics for a user
# ============================================================
# Compute count and average from the displayed progress:

def skill_report(user_id):
    """Return a count and average progress for one user."""
    connection = None
    try:
        connection = connect_db()
        row = connection.execute(
            "SELECT COUNT(*), COALESCE(AVG(progress), 0) FROM skills "
            "WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return row[0], row[1]
    finally:
        close_db(connection)


count, average = skill_report(1)
print(f"  user 1 skill count: {count}")
print(f"  user 1 average progress: {average:.1f}%")
#   user 1 skill count: 2
#   user 1 average progress: 72.5%

# ============================================================
# [10] Empty user report
# ============================================================
# Empty lists produce a zero count and safe zero average:

empty_count, empty_average = skill_report(3)
print(f"  empty user count: {empty_count}")
print(f"  empty user average: {empty_average:.1f}%")
#   empty user count: 0
#   empty user average: 0.0%

# ============================================================
# [11] Full scripted app flow [07:30]
# ============================================================
# A concise add -> show -> update -> show -> delete -> show
# sequence, all against the same database:

scripted = []
scripted.append(add_skill(1, "Testing", 10))
scripted.append(show_skills(1))
scripted.append(update_progress(1, "testing", 50))
scripted.append(show_skills(1))
scripted.append(delete_skill(1, "testing"))
scripted.append(show_skills(1))
print(f"  scripted operation count: {len(scripted)}")
print(f"  add/update/delete succeeded: {scripted[0] and scripted[2] and scripted[4]}")
print(f"  final user skills: {scripted[-1]}")
#   scripted operation count: 6
#   add/update/delete succeeded: True
#   final user skills: ['python: 80%', 'regex: 65%']

# ============================================================
# [12] Cleanup the complete Skills App demo
# ============================================================
# Each helper closes its connection; remove the temp DB:

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  temporary database removed: {not os.path.exists(WORK_DIR)}")
#   temporary database removed: True

# ============================================================
# [13] The summary: Skills App completed [07:30]
# ============================================================
# Skills App display and reports, from the transcript:
#
#   1. SHOW [02:10] -- query only WHERE user_id = ? and
#      format each skill name with its progress percentage
#   2. EMPTY CHECK [06:12] -- users with no skills get a
#      friendly "No skills registered yet." message
#   3. ADD -- normalized skill name and progress saved to DB
#   4. UPDATE -- progress changed only for the matching
#      user and skill; values outside 0..100 rejected
#   5. DELETE -- user-scoped WHERE avoids cross-user removal
#   6. REPORT -- count and average progress; empty account
#      safely reports zero
#   7. FULL APP [07:30] -- add/update/delete/show all work
#      against SQLite and commit changes
#   8. CLEANUP -- temporary database removed after demo
#
# A polished app shows useful progress, explains empty
# states, and scopes every database operation to its user.
