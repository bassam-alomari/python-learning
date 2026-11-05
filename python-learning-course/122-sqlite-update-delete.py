# -----------------------------------------------------------------
# Lesson 122: SQLite -- UPDATE and DELETE rows safely
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : UPDATE with a precise WHERE, DELETE FROM a
#            selected row, commit persistence, and verify
#            unaffected records
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: two essential SQLite operations --
# update and delete data using Python.
#
#   UPDATE [00:28] -- UPDATE table SET column = value
#   WHERE condition; use a precise key such as user_id
#   DELETE [02:37] -- DELETE FROM table WHERE condition
#   COMMIT [03:00] -- save changes permanently in the DB file
#
# These examples use placeholders and a temporary database.
# The WHERE clause is deliberate: without it, all rows could
# be modified or deleted.

import os
import shutil
import sqlite3
import tempfile

# ============================================================
# [1] Prepare a temporary users table
# ============================================================
# Use fixed rows so the effect of each command is clear:

WORK_DIR = tempfile.mkdtemp(prefix="py122_")
db_path = os.path.join(WORK_DIR, "users.db")
db = sqlite3.connect(db_path)
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE users (user_id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
)
cursor.executemany(
    "INSERT INTO users (user_id, name, age) VALUES (?, ?, ?)",
    [(1, "Amina", 29), (2, "Omar", 34), (3, "Lina", 26), (4, "Rami", 41)],
)
db.commit()

before = cursor.execute(
    "SELECT user_id, name, age FROM users ORDER BY user_id"
).fetchall()
print(f"  initial users: {before}")
#   initial users: [(1, 'Amina', 29), (2, 'Omar', 34), (3, 'Lina', 26), (4, 'Rami', 41)]

# ============================================================
# [2] UPDATE a row with a precise WHERE [00:28]
# ============================================================
# Change only the age for user_id 2:

cursor.execute(
    "UPDATE users SET age = ? WHERE user_id = ?",
    (35, 2),
)
updated_count = cursor.rowcount
db.commit()

print(f"  rows updated: {updated_count}")
#   rows updated: 1

# ============================================================
# [3] Verify the update was committed [03:00]
# ============================================================
# Read the updated row and a neighboring row:

updated_user = cursor.execute(
    "SELECT user_id, name, age FROM users WHERE user_id = ?", (2,)
).fetchone()
untouched_user = cursor.execute(
    "SELECT user_id, name, age FROM users WHERE user_id = ?", (1,)
).fetchone()

print(f"  updated user: {updated_user}")
print(f"  other user unchanged: {untouched_user}")
#   updated user: (2, 'Omar', 35)
#   other user unchanged: (1, 'Amina', 29)

# ============================================================
# [4] Why WHERE matters [00:28]
# ============================================================
# The condition limited the change to one matching ID:

after_update_count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
print(f"  total users still present: {after_update_count}")
print(f"  only one row changed: {updated_count == 1 and after_update_count == 4}")
#   total users still present: 4
#   only one row changed: True

# Without WHERE user_id = ?, every row could receive the
# same new age; a precise condition prevents that mistake.

# ============================================================
# [5] DELETE one selected row [02:37]
# ============================================================
# Remove the user whose ID is 4:

cursor.execute("DELETE FROM users WHERE user_id = ?", (4,))
deleted_count = cursor.rowcount
db.commit()
print(f"  rows deleted: {deleted_count}")
#   rows deleted: 1

# ============================================================
# [6] Verify deletion and remaining records [03:00]
# ============================================================
# Query the deleted ID and the remaining table:

deleted_user = cursor.execute(
    "SELECT user_id, name, age FROM users WHERE user_id = ?", (4,)
).fetchone()
remaining = cursor.execute(
    "SELECT user_id, name, age FROM users ORDER BY user_id"
).fetchall()

print(f"  deleted ID returns None: {deleted_user is None}")
print(f"  remaining users: {remaining}")
#   deleted ID returns None: True
#   remaining users: [(1, 'Amina', 29), (2, 'Omar', 35), (3, 'Lina', 26)]

# ============================================================
# [7] DELETE with an unmatched condition
# ============================================================
# A WHERE condition that matches no row deletes nothing:

cursor.execute("DELETE FROM users WHERE user_id = ?", (99,))
no_delete_count = cursor.rowcount
db.commit()
print(f"  unmatched delete count: {no_delete_count}")
print(f"  rows remain: {cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0]}")
#   unmatched delete count: 0
#   rows remain: 3

# ============================================================
# [8] Commit persists UPDATE and DELETE [03:00]
# ============================================================
# Close and reconnect to verify saved state:

cursor.close()
db.close()
reopened = sqlite3.connect(db_path)
persisted = reopened.execute(
    "SELECT user_id, name, age FROM users ORDER BY user_id"
).fetchall()

print(f"  after reconnect: {persisted}")
print(f"  committed update persisted: {persisted[1][2] == 35}")
print(f"  committed delete persisted: {all(row[0] != 4 for row in persisted)}")

#   after reconnect: [(1, 'Amina', 29), (2, 'Omar', 35), (3, 'Lina', 26)]
#   committed update persisted: True
#   committed delete persisted: True

# ============================================================
# [9] Confirm commit results as booleans
# ============================================================
# The database state after reconnect:

print(f"  update persisted: {persisted[1][2] == 35}")
print(f"  deleted row absent: {all(row[0] != 4 for row in persisted)}")
print(f"  row count after changes: {len(persisted)}")
#   update persisted: True
#   deleted row absent: True
#   row count after changes: 3

# ============================================================
# [10] SQL safety: values are parameters
# ============================================================
# Use ? placeholders instead of building SQL with string
# concatenation:

update_sql = "UPDATE users SET age = ? WHERE user_id = ?"
delete_sql = "DELETE FROM users WHERE user_id = ?"
print(f"  update placeholders: {update_sql.count('?')}")
print(f"  delete placeholders: {delete_sql.count('?')}")
#   update placeholders: 2
#   delete placeholders: 1

# ============================================================
# [11] The safe sequence
# ============================================================
# A repeatable data-change routine:

sequence = ("choose WHERE key", "execute parameterized SQL", "commit", "SELECT to verify")
print(f"  safe steps: {len(sequence)}")
print(f"  first: {sequence[0]}")
print(f"  last: {sequence[-1]}")
#   safe steps: 4
#   first: choose WHERE key
#   last: SELECT to verify

# ============================================================
# [12] Close and clean the database
# ============================================================
# Release the connection and remove the temporary file:

reopened.close()
try:
    reopened.execute("SELECT 1")
except sqlite3.ProgrammingError:
    connection_closed = True
else:
    connection_closed = False
shutil.rmtree(WORK_DIR, ignore_errors=True)

print(f"  connection closed: {connection_closed}")
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   connection closed: True
#   sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# SQLite UPDATE and DELETE, from the transcript:
#
#   1. UPDATE [00:28] -- SET a new value and use WHERE
#      user_id = ? to target exactly one row
#   2. VERIFY -- rowcount is 1; the chosen age changes,
#      unrelated user remains unchanged
#   3. DELETE [02:37] -- DELETE FROM users WHERE user_id = ?
#      removes only the selected row
#   4. VERIFY -- deleted ID returns None; an unmatched
#      ID deletes zero rows
#   5. COMMIT [03:00] -- commit after each change; close
#      and reconnect to prove UPDATE/DELETE persisted
#   6. SAFETY -- parameterized SQL and precise WHERE
#      conditions help avoid accidental whole-table changes
#   7. CLEANUP -- close connection and remove temp database
#
# UPDATE changes; DELETE removes; WHERE chooses; commit
# makes the result durable.
