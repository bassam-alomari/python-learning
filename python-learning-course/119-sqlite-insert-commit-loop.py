# -----------------------------------------------------------------
# Lesson 119: SQLite -- insert rows, commit and loop
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : Cursor execution, INSERT INTO, parameterized
#            SQL, commit persistence, for/enumerate batch
#            inserts, and querying the saved rows
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: next step after creating a DB
# and tables -- insert data with Python and SQLite.
#
#   CURSOR [00:50] -- execute SQL commands through the
#   connection's cursor
#   INSERT INTO [02:17] -- insert user_id, name and age
#   COMMIT [04:30] -- persist changes to the database file
#   LOOP [05:49] -- use for + enumerate to insert records
#   from a prepared list efficiently
#
# A temporary database is used and removed at the end.

import os
import shutil
import sqlite3
import tempfile

# ============================================================
# [1] Create the database and users table
# ============================================================
# Prepare the same table structure from the previous lesson:

WORK_DIR = tempfile.mkdtemp(prefix="py119_")
db_path = os.path.join(WORK_DIR, "users.db")
db = sqlite3.connect(db_path)
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE users ("
    "user_id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL)"
)
db.commit()

print(f"  database connected: {isinstance(db, sqlite3.Connection)}")
print(f"  users table ready: {cursor.execute('SELECT name FROM sqlite_master WHERE name = ?', ('users',)).fetchone() == ('users',)}")
#   database connected: True
#   users table ready: True

# ============================================================
# [2] Cursor executes SQL [00:50]
# ============================================================
# Use the cursor to run all SQL statements:

print(f"  cursor belongs to db: {cursor.connection is db}")
print(f"  cursor can execute: {callable(cursor.execute)}")
#   cursor belongs to db: True
#   cursor can execute: True

# ============================================================
# [3] Insert one user with INSERT INTO [02:17]
# ============================================================
# Use placeholders so values remain separate from SQL:

cursor.execute(
    "INSERT INTO users (user_id, name, age) VALUES (?, ?, ?)",
    (1, "Amina", 29),
)

print(f"  first insert affected rows: {cursor.rowcount}")
#   first insert affected rows: 1

# ============================================================
# [4] Commit saves the insert [04:30]
# ============================================================
# Commit the transaction so the database records it:

db.commit()
first_user = cursor.execute(
    "SELECT user_id, name, age FROM users WHERE user_id = ?", (1,)
).fetchone()

print(f"  committed row: {first_user}")
#   committed row: (1, 'Amina', 29)

# ============================================================
# [5] Insert a prepared list with a loop [05:49]
# ============================================================
# Enumerate records to assign unique IDs and insert them:

users = [
    ("Omar", 34),
    ("Lina", 26),
    ("Rami", 41),
]

for user_id, (name, age) in enumerate(users, start=2):
    cursor.execute(
        "INSERT INTO users (user_id, name, age) VALUES (?, ?, ?)",
        (user_id, name, age),
    )

db.commit()
print(f"  list records inserted: {len(users)}")
#   list records inserted: 3

# ============================================================
# [6] Verify every row was saved
# ============================================================
# Query the table in ID order:

all_users = cursor.execute(
    "SELECT user_id, name, age FROM users ORDER BY user_id"
).fetchall()

print(f"  saved user rows: {all_users}")
print(f"  total rows: {len(all_users)}")
#   saved user rows: [(1, 'Amina', 29), (2, 'Omar', 34), (3, 'Lina', 26), (4, 'Rami', 41)]
#   total rows: 4

# ============================================================
# [7] enumerate provides stable row IDs [05:49]
# ============================================================
# The generated IDs start at 2 because ID 1 was inserted
# separately:

generated_ids = [row[0] for row in all_users[1:]]
print(f"  loop-generated IDs: {generated_ids}")
print(f"  IDs are sequential: {generated_ids == [2, 3, 4]}")
#   loop-generated IDs: [2, 3, 4]
#   IDs are sequential: True

# ============================================================
# [8] Commit makes rows persistent across connections
# ============================================================
# Close and reconnect to the same file, then query again:

cursor.close()
db.close()
reopened = sqlite3.connect(db_path)
reopened_count = reopened.execute("SELECT COUNT(*) FROM users").fetchone()[0]

print(f"  rows after reconnect: {reopened_count}")
print(f"  committed data persists: {reopened_count == 4}")
#   rows after reconnect: 4
#   committed data persists: True

# ============================================================
# [9] Query selected user fields
# ============================================================
# SQL can retrieve chosen fields from the inserted rows:

names = reopened.execute(
    "SELECT name FROM users ORDER BY user_id"
).fetchall()
print(f"  stored names: {[row[0] for row in names]}")
#   stored names: ['Amina', 'Omar', 'Lina', 'Rami']

# ============================================================
# [10] Count inserted records
# ============================================================
# COUNT(*) summarizes the number of stored user records:

count_row = reopened.execute("SELECT COUNT(*) FROM users").fetchone()
print(f"  COUNT(*) result: {count_row[0]}")
print(f"  one direct plus three loop inserts: {count_row[0] == 1 + len(users)}")
#   COUNT(*) result: 4
#   one direct plus three loop inserts: True

# ============================================================
# [11] SQL parameters keep values separate
# ============================================================
# The insert statements use ? placeholders and pass values
# as a tuple:

insert_sql = "INSERT INTO users (user_id, name, age) VALUES (?, ?, ?)"
print(f"  parameter placeholders: {insert_sql.count('?')}")
print(f"  parameterized insert shape: 'VALUES (?, ?, ?)' in insert_sql")
#   parameter placeholders: 3
#   parameterized insert shape: 'VALUES (?, ?, ?)' in insert_sql

# ============================================================
# [12] Close and clean the temporary database
# ============================================================
# Finish by closing the active connection and removing
# the temporary sandbox:

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
# SQLite inserts, from the transcript:
#
#   1. CURSOR [00:50] -- execute SQL through cursor.execute()
#   2. INSERT [02:17] -- add user_id, name, age with
#      INSERT INTO and parameter placeholders
#   3. COMMIT [04:30] -- save the transaction durably;
#      committed rows survive closing and reconnecting
#   4. LOOP [05:49] -- for + enumerate(users, start=2)
#      assigns IDs and inserts three records in a batch
#   5. VERIFY -- query rows back, check order and count
#   6. CLEANUP -- close the connection and remove the
#      temporary database after the demo
#
# Cursor executes; commit persists; query confirms what
# the database saved.
