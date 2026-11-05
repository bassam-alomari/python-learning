# -----------------------------------------------------------------
# Lesson 120: SQLite -- SELECT and cursor fetch methods
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : SELECT *, selected columns, fetchall(),
#            fetchone(), fetchmany(size), iterate and
#            display rows, close and clean up
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: retrieve stored table data
# with Python and SQLite.
#
#   SELECT [00:54] -- execute SELECT * or named columns
#   through cursor.execute()
#   FETCH [01:46] -- fetchall() gets all rows as a list of
#   tuples; fetchone() gets one row; fetchmany(size) gets
#   a requested batch
#   ITERATE [03:08] -- loop over returned rows and display
#   them in an organized way
#   NEXT [04:08] -- upcoming practical lesson combines
#   insert, query and data processing

import os
import shutil
import sqlite3
import tempfile

# ============================================================
# [1] Prepare a deterministic temporary database
# ============================================================
# Create a users table and insert fixed rows for retrieval:

WORK_DIR = tempfile.mkdtemp(prefix="py120_")
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

print(f"  records ready: {cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0]}")
#   records ready: 4

# ============================================================
# [2] SELECT * retrieves every column [00:54]
# ============================================================
# execute() runs SELECT; fetchall() returns all matching
# rows as a list of tuples:

cursor.execute("SELECT * FROM users ORDER BY user_id")
all_rows = cursor.fetchall()

print(f"  fetchall result: {all_rows}")
print(f"  result is a list: {isinstance(all_rows, list)}")
print(f"  each row is a tuple: {all(isinstance(row, tuple) for row in all_rows)}")
#   fetchall result: [(1, 'Amina', 29), (2, 'Omar', 34), (3, 'Lina', 26), (4, 'Rami', 41)]
#   result is a list: True
#   each row is a tuple: True

# ============================================================
# [3] SELECT named columns [00:54]
# ============================================================
# Retrieve only the name column:

cursor.execute("SELECT name FROM users ORDER BY user_id")
name_rows = cursor.fetchall()
names = [row[0] for row in name_rows]

print(f"  selected names: {names}")
#   selected names: ['Amina', 'Omar', 'Lina', 'Rami']

# ============================================================
# [4] fetchone(): one result [01:46]
# ============================================================
# Execute the query, then fetch its first matching row:

cursor.execute("SELECT user_id, name, age FROM users ORDER BY user_id")
first_row = cursor.fetchone()

print(f"  fetchone result: {first_row}")
#   fetchone result: (1, 'Amina', 29)

# ============================================================
# [5] fetchone() advances the cursor
# ============================================================
# Calling fetchone() again reads the next row from the
# same result set:

second_row = cursor.fetchone()
print(f"  next fetchone result: {second_row}")
#   next fetchone result: (2, 'Omar', 34)

# ============================================================
# [6] fetchmany(size): retrieve a batch [01:46]
# ============================================================
# Start a fresh query and fetch only the first two rows:

cursor.execute("SELECT user_id, name FROM users ORDER BY user_id")
first_two = cursor.fetchmany(2)

print(f"  fetchmany(2): {first_two}")
print(f"  batch size: {len(first_two)}")
#   fetchmany(2): [(1, 'Amina'), (2, 'Omar')]
#   batch size: 2

# ============================================================
# [7] fetchmany() continues from current position
# ============================================================
# A second batch continues after the first two rows:

next_two = cursor.fetchmany(2)
print(f"  next fetchmany(2): {next_two}")
#   next fetchmany(2): [(3, 'Lina'), (4, 'Rami')]

# ============================================================
# [8] Loop through retrieved rows [03:08]
# ============================================================
# A loop processes each tuple in order:

cursor.execute("SELECT user_id, name, age FROM users ORDER BY user_id")
loop_rows = cursor.fetchall()
displayed = []
for user_id, name, age in loop_rows:
    displayed.append(f"{user_id}: {name} ({age})")

print(f"  rows displayed by loop: {displayed}")
#   rows displayed by loop: ['1: Amina (29)', '2: Omar (34)', '3: Lina (26)', '4: Rami (41)']

# ============================================================
# [9] Fetch only rows matching a condition
# ============================================================
# SELECT can filter records; placeholders keep values
# separate from the SQL statement:

cursor.execute(
    "SELECT name, age FROM users WHERE age >= ? ORDER BY age",
    (30,),
)
older_rows = cursor.fetchall()
print(f"  age 30 or more: {older_rows}")
#   age 30 or more: [('Omar', 34), ('Rami', 41)]

# ============================================================
# [10] Empty result behavior
# ============================================================
# fetchall() returns an empty list when no rows match:

cursor.execute("SELECT name FROM users WHERE age > ?", (100,))
no_rows = cursor.fetchall()
print(f"  no results: {no_rows}")
print(f"  empty list returned: {no_rows == []}")
#   no results: []
#   empty list returned: True

# ============================================================
# [11] fetchone() returns None when no row matches
# ============================================================
# A no-match fetchone result is None:

cursor.execute("SELECT name FROM users WHERE user_id = ?", (99,))
missing_row = cursor.fetchone()
print(f"  missing fetchone is None: {missing_row is None}")
#   missing fetchone is None: True

# ============================================================
# [12] Close the database and clean the sandbox
# ============================================================
# Close resources after the retrieval work:

cursor.close()
db.close()
try:
    db.execute("SELECT 1")
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
# SQLite retrieval, from the transcript:
#
#   1. SELECT [00:54] -- execute SELECT * or named fields
#      through cursor.execute()
#   2. fetchall() [01:46] -- all rows as list[tuple]; no
#      matches returns []
#   3. fetchone() [01:46] -- one row, then advances; no
#      matching row returns None
#   4. fetchmany(size) [01:46] -- a batch of requested
#      rows; repeated calls continue from the cursor position
#   5. LOOP [03:08] -- iterate over retrieved rows and
#      format them in a readable order
#   6. FILTER -- SELECT WHERE returns only matching rows
#   7. NEXT [04:08] -- the practical follow-up combines
#      inserts, queries and processing
#   8. CLEANUP -- close cursor/connection and remove the
#      temporary database file
#
# SELECT asks the question; fetch methods decide how much
# of its result to retrieve at a time.
