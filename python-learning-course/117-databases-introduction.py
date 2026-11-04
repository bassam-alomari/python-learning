# -----------------------------------------------------------------
# Lesson 117: databases -- introduction and persistence
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : what a database is, organized electronic data,
#            CRUD overview, application persistence, and
#            a small temporary SQLite demonstration
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: begin an important new Python
# section -- Databases.
#
#   WHAT [00:24] -- an organized electronic system to store,
#   retrieve, update and manage data safely, from users and
#   products to articles
#   WHY [01:07-01:51] -- modern apps/sites need persistent
#   state; a database keeps data beyond a temporary run
#   NEXT [02:18] -- prepare to connect Python to databases
#   and write practical code in upcoming lessons

import os
import sqlite3
import tempfile

# ============================================================
# [1] A database organizes electronic information [00:24]
# ============================================================
# A database keeps related records in a structured form:

print("  database: organized electronic data storage")
print("  examples: users, products, articles")
print("  operations: save, retrieve, update, manage")
#   database: organized electronic data storage
#   examples: users, products, articles
#   operations: save, retrieve, update, manage

# ============================================================
# [2] Why applications rely on databases [01:07-01:51]
# ============================================================
# App state should survive after the program exits:

print("  app data should outlive one program run")
print("  database provides persistent application state")
print("  database is a modern app's data backbone")
#   app data should outlive one program run
#   database provides persistent application state
#   database is a modern app's data backbone

# ============================================================
# [3] Create a temporary SQLite database
# ============================================================
# SQLite ships with Python and stores data in a file.
# Use a temporary directory so the lesson leaves no files:

WORK_DIR = tempfile.mkdtemp(prefix="py117_")
db_path = os.path.join(WORK_DIR, "app.db")
connection = sqlite3.connect(db_path)

print(f"  SQLite connection opened: {connection is not None}")
print(f"  database file created: {os.path.exists(db_path)}")
#   SQLite connection opened: True
#   database file created: True

# ============================================================
# [4] Create an organized table
# ============================================================
# A table describes the structure of stored records:

connection.execute(
    "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)"
)
connection.commit()
table_exists = connection.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
).fetchone() is not None

print(f"  users table exists: {table_exists}")
#   users table exists: True

# ============================================================
# [5] Save data (Create)
# ============================================================
# Insert a record with parameters rather than string
# concatenation:

connection.execute(
    "INSERT INTO users (name, role) VALUES (?, ?)",
    ("Amina", "admin"),
)
connection.commit()
saved_count = connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
print(f"  records saved: {saved_count}")
#   records saved: 1

# ============================================================
# [6] Retrieve data (Read)
# ============================================================
# Query the record back from the database:

saved_user = connection.execute(
    "SELECT name, role FROM users WHERE id = ?", (1,)
).fetchone()

print(f"  retrieved record: {saved_user}")
#   retrieved record: ('Amina', 'admin')

# ============================================================
# [7] Update data (Update)
# ============================================================
# Change a stored field and read it again:

connection.execute(
    "UPDATE users SET role = ? WHERE id = ?", ("editor", 1)
)
connection.commit()
updated_role = connection.execute(
    "SELECT role FROM users WHERE id = ?", (1,)
).fetchone()[0]

print(f"  updated role: {updated_role}")
#   updated role: editor

# ============================================================
# [8] Manage data (Delete)
# ============================================================
# Remove a record and confirm the table state:

connection.execute("DELETE FROM users WHERE id = ?", (1,))
connection.commit()
remaining_count = connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
print(f"  records after delete: {remaining_count}")
#   records after delete: 0

# ============================================================
# [9] Persistence across connections [01:51]
# ============================================================
# Close and reopen the database file; a new connection
# sees the committed table and current contents:

connection.close()
reopened = sqlite3.connect(db_path)
reopened_count = reopened.execute("SELECT COUNT(*) FROM users").fetchone()[0]
print(f"  reopened database sees table: {reopened_count == 0}")
print(f"  database file still exists: {os.path.exists(db_path)}")

#   reopened database sees table: True
#   database file still exists: True

# The table survives reconnecting because its schema and
# committed data live in the file, not only in memory.

# ============================================================
# [10] Persistence vs temporary in-memory state
# ============================================================
# A Python variable lasts only while the process runs;
# a committed database file can be opened later:

temporary_value = "only in this Python run"
stored_table_names = [
    row[0] for row in reopened.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
]
print(f"  Python variable is temporary: {temporary_value.endswith('run')}")
print(f"  table persists in database: {'users' in stored_table_names}")
#   Python variable is temporary: True
#   table persists in database: True

# ============================================================
# [11] A database helps manage many records
# ============================================================
# Store several products and query them as a collection:

reopened.execute("CREATE TABLE products (name TEXT, stock INTEGER)")
reopened.executemany(
    "INSERT INTO products (name, stock) VALUES (?, ?)",
    [("Book", 8), ("Pen", 20), ("Notebook", 5)],
)
reopened.commit()
products = reopened.execute(
    "SELECT name, stock FROM products ORDER BY name"
).fetchall()

print(f"  products managed: {len(products)}")
print(f"  ordered products: {products}")
#   products managed: 3
#   ordered products: [('Book', 8), ('Notebook', 5), ('Pen', 20)]

# ============================================================
# [12] Close connections and clean the demo database
# ============================================================
# A real application keeps or closes connections according
# to its lifecycle. This teaching sandbox cleans up fully:

reopened.close()
try:
    reopened.execute("SELECT 1")
except sqlite3.ProgrammingError:
    connection_closed = True
else:
    connection_closed = False
import shutil
shutil.rmtree(WORK_DIR, ignore_errors=True)

print(f"  connection closed: {connection_closed}")
print(f"  temporary database removed: {not os.path.exists(WORK_DIR)}")
#   connection closed: True
#   temporary database removed: True

# ============================================================
# [13] The summary: database section begins
# ============================================================
# Databases, from the transcript:
#
#   1. WHAT [00:24] -- organized electronic storage for
#      reliable saving, retrieval, updates and management
#   2. EXAMPLES -- user, product and article records
#   3. WHY [01:07-01:51] -- applications need persistent
#      state that lasts beyond one execution
#   4. PRACTICE -- SQLite table created; a user inserted,
#      retrieved, updated and deleted (CRUD)
#   5. PERSISTENCE -- closing and reopening the file-backed
#      database preserves its table and committed state
#   6. NEXT [02:18] -- upcoming lessons connect Python to
#      databases in more focused practical examples
#   7. CLEANUP -- this introductory demo uses a temporary
#      database and removes it after closing the connection
#
# Variables live in a run; a database is built to retain
# application data between runs.
