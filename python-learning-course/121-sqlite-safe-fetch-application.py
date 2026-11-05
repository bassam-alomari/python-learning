# -----------------------------------------------------------------
# Lesson 121: SQLite application -- safe fetch and display
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : integrate functions, loops, data processing,
#            try/except error handling, SELECT/fetch loop,
#            formatted output, and finally-close cleanup
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: practical integration of course
# skills -- functions, loops, exception handling and data
# processing -- with SQLite.
#
#   SAFE ERRORS [00:28] -- catch likely database failures
#   and show a helpful message instead of an abrupt crash
#   FETCH / PRINT [02:27] -- SELECT users, loop over rows,
#   format and display each one clearly
#   FINALLY [07:03] -- always close the database connection,
#   on success or error, to avoid leaking resources

import os
import shutil
import sqlite3
import tempfile

# ============================================================
# [1] Prepare a deterministic database
# ============================================================
# Use fixed rows in a temporary SQLite file:

WORK_DIR = tempfile.mkdtemp(prefix="py121_")
DB_PATH = os.path.join(WORK_DIR, "application.db")

db = sqlite3.connect(DB_PATH)
db.execute(
    "CREATE TABLE users (user_id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
)
db.executemany(
    "INSERT INTO users (user_id, name, age) VALUES (?, ?, ?)",
    [(1, "Amina", 29), (2, "Omar", 34), (3, "Lina", 26)],
)
db.commit()
db.close()

print(f"  demo database prepared: {os.path.exists(DB_PATH)}")
#   demo database prepared: True

# ============================================================
# [2] A function owns the database operation
# ============================================================
# Encapsulate connection, query and cleanup in one function:

def display_users(path):
    """Fetch users safely and always close the connection."""
    connection = None
    displayed_rows = []
    error_message = ""
    close_verified = False

    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT user_id, name, age FROM users ORDER BY user_id"
        )
        rows = cursor.fetchall()
        for user_id, name, age in rows:
            displayed_rows.append(
                f"ID {user_id} | Name: {name} | Age: {age}"
            )
    except sqlite3.Error as error:
        error_message = type(error).__name__
    finally:
        if connection is not None:
            connection.close()
            try:
                connection.execute("SELECT 1")
            except sqlite3.ProgrammingError:
                close_verified = True

    return displayed_rows, error_message, close_verified


rows, message, was_closed = display_users(DB_PATH)
print(f"  function returned rows: {len(rows)}")
print(f"  error message: {message or 'none'}")
print(f"  connection closed in finally: {was_closed}")
#   function returned rows: 3
#   error message: none
#   connection closed in finally: True

# ============================================================
# [3] SELECT fetch and formatted output [02:27]
# ============================================================
# The function formatted each row in its loop:

for formatted_row in rows:
    print(f"  {formatted_row}")
#   ID 1 | Name: Amina | Age: 29
#   ID 2 | Name: Omar | Age: 34
#   ID 3 | Name: Lina | Age: 26

# ============================================================
# [4] Handle a database error safely [00:28]
# ============================================================
# A path that does not exist produces a handled SQLite
# error, not an unhandled traceback:

missing_path = os.path.join(WORK_DIR, "missing.db")
missing_rows, missing_error, missing_closed = display_users(missing_path)

print(f"  missing database rows: {missing_rows}")
print(f"  error caught: {missing_error}")
print(f"  no connection leaked: {missing_closed}")
#   missing database rows: []
#   error caught: OperationalError
#   no connection leaked: True

# sqlite3.connect() creates absent files, but SELECT fails
# because the new database has no users table. The error
# is caught and reported by type; finally still closes.

# ============================================================
# [5] Make the error report user-friendly
# ============================================================
# Translate the technical error type into a clear message:

def user_facing_message(error_name):
    """Convert a database error label into a readable message."""
    if error_name:
        return "Could not read user records"
    return "User records loaded successfully"


print(f"  success message: {user_facing_message(message)}")
print(f"  error message: {user_facing_message(missing_error)}")
#   success message: User records loaded successfully
#   error message: Could not read user records

# ============================================================
# [6] Process rows with a loop [02:27]
# ============================================================
# Build a derived list of display names from fetched data:

display_names = []
for formatted_row in rows:
    name = formatted_row.split("Name: ", 1)[1].split(" |", 1)[0]
    display_names.append(name.upper())

print(f"  processed names: {display_names}")
#   processed names: ['AMINA', 'OMAR', 'LINA']

# ============================================================
# [7] Count and summarize retrieved records
# ============================================================
# The same loop-driven data can produce a short summary:

summary = {
    "records": len(rows),
    "names": display_names,
    "error": bool(message),
}
print(f"  summary: {summary}")
#   summary: {'records': 3, 'names': ['AMINA', 'OMAR', 'LINA'], 'error': False}

# ============================================================
# [8] Verify finally closes on the successful path
# ============================================================
# The normal fetch succeeded, and close_verified records
# that the connection was closed:

print(f"  successful path connection closed: {was_closed}")
print(f"  all users were formatted: {len(rows) == 3 and all(' | ' in row for row in rows)}")
#   successful path connection closed: True
#   all users were formatted: True

# ============================================================
# [9] Verify finally closes on the error path [07:03]
# ============================================================
# Missing-table failure was caught and the connection
# closed by the same finally clause:

print(f"  error path caught: {bool(missing_error)}")
print(f"  error path connection closed: {missing_closed}")
print(f"  error path did not crash: {missing_rows == [] and bool(missing_error)}")
#   error path caught: True
#   error path connection closed: True
#   error path did not crash: True

# ============================================================
# [10] One function handles multiple database files
# ============================================================
# Both calls follow the same result contract:

print(f"  success result shape: {len((rows, message, was_closed))}")
print(f"  error result shape: {len((missing_rows, missing_error, missing_closed))}")
print(f"  error and success paths both close: {was_closed and missing_closed}")
#   success result shape: 3
#   error result shape: 3
#   error and success paths both close: True

# ============================================================
# [11] The application workflow
# ============================================================
# Outline the integrated operation in order:

workflow = (
    "connect",
    "execute SELECT",
    "fetch rows",
    "format in a loop",
    "catch errors",
    "close in finally",
)
print(f"  workflow steps: {len(workflow)}")
print(f"  starts with: {workflow[0]}")
print(f"  ends with: {workflow[-1]}")
#   workflow steps: 6
#   starts with: connect
#   ends with: close in finally

# ============================================================
# [12] Close temporary artifacts [07:03]
# ============================================================
# The function closed every connection; remove the two
# temporary database files and their directory:

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  temporary databases removed: {not os.path.exists(WORK_DIR)}")
#   temporary databases removed: True

# ============================================================
# [13] The summary
# ============================================================
# SQLite safe fetch application, from the transcript:
#
#   1. INTEGRATION [00:04] -- functions, loops, data
#      processing and exception handling around SQLite
#   2. TRY/EXCEPT [00:28] -- catch sqlite3.Error, return a
#      readable status instead of an abrupt traceback
#   3. SELECT [02:27] -- fetch all user rows and loop
#      through them in stable ID order
#   4. FORMATTING -- each row prints as ID / name / age;
#      a second loop derives uppercase names and summary
#   5. FINALLY [07:03] -- connection closed on success and
#      on SQL error; both outcomes verified
#   6. ERROR DEMO -- missing table caught as
#      OperationalError; no leaked connection
#   7. CLEANUP -- temporary database files removed
#
# A practical database script should both explain errors
# and close its resources on every path.
