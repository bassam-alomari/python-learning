# -----------------------------------------------------------------
# Lesson 118: SQLite -- connect, cursor and create a table
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : built-in sqlite3, connect to a database file,
#            create a Cursor, execute CREATE TABLE IF NOT
#            EXISTS with user_id/name/age, close connection
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: first practical SQLite lesson --
# a lightweight database included with Python.
#
#   IMPORT [00:24] -- import sqlite3
#   CONNECT [01:35] -- sqlite3.connect() creates a database
#   file or opens it if it already exists
#   CURSOR / execute() -- issue SQL commands through a cursor
#   TABLE [04:22] -- users fields: user_id, name, age
#   CLOSE [05:40] -- close the database connection when done
#
# To keep this lesson repeatable and leave no artifacts,
# the .db file lives in a temporary directory and is
# removed after the connection is closed.

import os
import shutil
import sqlite3
import tempfile

# ============================================================
# [1] sqlite3 is built into Python [00:24]
# ============================================================
# Import the standard library module and inspect it:

print(f"  module name: {sqlite3.__name__}")
print(f"  connect available: {callable(sqlite3.connect)}")
print(f"  Cursor type available: {hasattr(sqlite3, 'Cursor')}")
#   module name: sqlite3
#   connect available: True
#   Cursor type available: True

# ============================================================
# [2] Connect to a .db file [01:35]
# ============================================================
# connect() creates a database file if absent, or opens
# it if present. Use a sandbox path rather than the
# workspace:

WORK_DIR = tempfile.mkdtemp(prefix="py118_")
db_path = os.path.join(WORK_DIR, "app.db")
db = sqlite3.connect(db_path)

print(f"  connection opened: {isinstance(db, sqlite3.Connection)}")
print(f"  database file created: {os.path.exists(db_path)}")
#   connection opened: True
#   database file created: True

# ============================================================
# [3] Create a Cursor [01:35]
# ============================================================
# A cursor executes SQL statements on the connection:

cursor = db.cursor()
print(f"  cursor created: {isinstance(cursor, sqlite3.Cursor)}")
print(f"  cursor belongs to connection: {cursor.connection is db}")
#   cursor created: True
#   cursor belongs to connection: True

# ============================================================
# [4] Execute CREATE TABLE IF NOT EXISTS [04:22]
# ============================================================
# Define the users table with an id, name and age:

cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )"""
)
db.commit()

print(f"  table command executed: {cursor.rowcount == -1}")
#   table command executed: True

# ============================================================
# [5] Inspect the created table
# ============================================================
# Read SQLite's schema catalog to confirm the table:

table_row = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type = ? AND name = ?",
    ("table", "users"),
).fetchone()

print(f"  users table created: {table_row == ('users',)}")
#   users table created: True

# ============================================================
# [6] Verify the table columns [04:22]
# ============================================================
# PRAGMA table_info reports the field names and types:

columns = cursor.execute("PRAGMA table_info(users)").fetchall()
column_names = [column[1] for column in columns]
column_types = [column[2] for column in columns]

print(f"  column names: {column_names}")
print(f"  column types: {column_types}")
#   column names: ['user_id', 'name', 'age']
#   column types: ['INTEGER', 'TEXT', 'INTEGER']

# ============================================================
# [7] IF NOT EXISTS makes creation repeatable
# ============================================================
# Running the same CREATE statement again is safe:

cursor.execute(
    "CREATE TABLE IF NOT EXISTS users "
    "(user_id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL)"
)
db.commit()
columns_after_repeat = cursor.execute("PRAGMA table_info(users)").fetchall()

print(f"  repeated create did not duplicate columns: {len(columns_after_repeat) == 3}")
#   repeated create did not duplicate columns: True

# ============================================================
# [8] Connection and Cursor are distinct objects
# ============================================================
# The connection represents the database session; the
# cursor issues statements through it:

print(f"  connection and cursor are different objects: {db is not cursor}")
print(f"  cursor connection is current db: {cursor.connection is db}")
#   connection and cursor are different objects: True
#   cursor connection is current db: True

# ============================================================
# [9] Close the database connection [05:40]
# ============================================================
# Close cursor and connection explicitly after the work:

cursor.close()
db.close()

try:
    db.execute("SELECT 1")
except sqlite3.ProgrammingError:
    connection_closed = True
else:
    connection_closed = False

print(f"  connection closed: {connection_closed}")
print(f"  database file remains until cleanup: {os.path.exists(db_path)}")
#   connection closed: True
#   database file remains until cleanup: True

# ============================================================
# [10] A closed cursor rejects further work
# ============================================================
# Closing the cursor ends its use too:

try:
    cursor.execute("SELECT 1")
except sqlite3.ProgrammingError:
    cursor_closed = True
else:
    cursor_closed = False

print(f"  cursor closed: {cursor_closed}")
#   cursor closed: True

# ============================================================
# [11] Clean the temporary database file
# ============================================================
# The lesson's database is disposable; remove its sandbox:

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
print(f"  database file removed: {not os.path.exists(db_path)}")
#   sandbox removed: True
#   database file removed: True

# ============================================================
# [12] The steps in order
# ============================================================
# A concise checklist of this SQLite workflow:

steps = (
    "import sqlite3",
    "connect to app.db",
    "create a cursor",
    "execute CREATE TABLE IF NOT EXISTS",
    "commit and close",
)
print(f"  workflow steps: {len(steps)}")
print(f"  first: {steps[0]}")
print(f"  last: {steps[-1]}")
#   workflow steps: 5
#   first: import sqlite3
#   last: commit and close

# ============================================================
# [13] The summary: SQLite setup
# ============================================================
# SQLite, from the transcript:
#
#   1. IMPORT [00:24] -- sqlite3 is included with Python
#   2. CONNECT [01:35] -- connect(path) opens or creates
#      the .db file
#   3. CURSOR -- connection.cursor() creates an executor
#      for SQL commands; cursor.execute(...) runs them
#   4. TABLE [04:22] -- CREATE TABLE IF NOT EXISTS users
#      (user_id, name, age); PRAGMA verified all columns
#   5. REPEATABILITY -- IF NOT EXISTS permits safe reruns
#   6. CLOSE [05:40] -- close cursor and db connection
#      explicitly after completing database work
#   7. CLEANUP -- temporary database file removed so the
#      lesson leaves no workspace or temp artifacts
#
# Next lessons can build on this connection/cursor/table
# foundation to insert and query application data.
