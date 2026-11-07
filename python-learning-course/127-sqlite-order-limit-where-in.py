# -----------------------------------------------------------------
# Lesson 127: SQLite queries -- order, limit, filter and IN
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : ORDER BY name/user_id, ASC/DESC, LIMIT/OFFSET,
#            WHERE comparisons, IN / NOT IN, parameterized SQL
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: useful SQLite information before
# closing the database section.
#
#   ORDER BY [03:22] -- sort by user_id or name; ASC is
#   ascending, DESC descending
#   LIMIT / OFFSET [04:27-05:51] -- cap rows and skip a
#   number of ordered rows before returning results
#   WHERE [06:33] -- filter using comparisons and AND/OR
#   IN / NOT IN [07:24] -- match values in a supplied set
#   SECURITY [01:42-03:13] -- bind values with placeholders,
#   never concatenate user input into SQL text

import os
import shutil
import sqlite3
import tempfile

# ============================================================
# [1] Prepare the Skills table with stable data
# ============================================================
# Multiple users and skill names illustrate sorting/filtering:

WORK_DIR = tempfile.mkdtemp(prefix="py127_")
DB_PATH = os.path.join(WORK_DIR, "skills.db")
db = sqlite3.connect(DB_PATH)
db.execute(
    "CREATE TABLE skills (skill_id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, level INTEGER)"
)
db.executemany(
    "INSERT INTO skills (user_id, name, level) VALUES (?, ?, ?)",
    [
        (1, "Python", 80),
        (1, "SQL", 60),
        (2, "Java", 70),
        (2, "Bash", 40),
        (3, "Go", 90),
        (4, "Pascal", 50),
    ],
)
db.commit()
cursor = db.cursor()

print(f"  skills rows prepared: {cursor.execute('SELECT COUNT(*) FROM skills').fetchone()[0]}")
#   skills rows prepared: 6

# ============================================================
# [2] ORDER BY user_id ascending [03:22]
# ============================================================
# ASC is the default, but write it explicitly for clarity:

ascending_ids = cursor.execute(
    "SELECT user_id, name FROM skills ORDER BY user_id ASC, name ASC"
).fetchall()
print(f"  ordered by user_id ASC: {ascending_ids}")
#   ordered by user_id ASC: [(1, 'Python'), (1, 'SQL'), (2, 'Bash'), (2, 'Java'), (3, 'Go'), (4, 'Pascal')]

# ============================================================
# [3] ORDER BY name descending [03:45]
# ============================================================
# DESC reverses the alphabetical order:

descending_names = cursor.execute(
    "SELECT name FROM skills ORDER BY name DESC"
).fetchall()
print(f"  names DESC: {[row[0] for row in descending_names]}")
#   names DESC: ['SQL', 'Python', 'Pascal', 'Java', 'Go', 'Bash']

# ============================================================
# [4] ORDER BY supports multiple keys
# ============================================================
# Sort by user_id, then skill name within each user:

ordered_pairs = cursor.execute(
    "SELECT user_id, name FROM skills ORDER BY user_id, name"
).fetchall()
print(f"  user then name: {ordered_pairs}")
#   user then name: [(1, 'Python'), (1, 'SQL'), (2, 'Bash'), (2, 'Java'), (3, 'Go'), (4, 'Pascal')]

# ============================================================
# [5] LIMIT returns only the first n rows [04:27]
# ============================================================
# Order first, then apply the limit:

first_two = cursor.execute(
    "SELECT name FROM skills ORDER BY name LIMIT ?", (2,)
).fetchall()
print(f"  first two names: {[row[0] for row in first_two]}")
#   first two names: ['Bash', 'Go']

# ============================================================
# [6] OFFSET skips ordered rows [04:57-05:51]
# ============================================================
# OFFSET 2 skips the first two ordered names; LIMIT 3
# returns the following three:

page = cursor.execute(
    "SELECT name FROM skills ORDER BY name LIMIT ? OFFSET ?",
    (3, 2),
).fetchall()
print(f"  names after OFFSET 2, LIMIT 3: {[row[0] for row in page]}")
#   names after OFFSET 2, LIMIT 3: ['Java', 'Pascal', 'Python']

# ============================================================
# [7] WHERE comparison and AND [06:33]
# ============================================================
# Filter skills by level and one user:

strong_user_one = cursor.execute(
    "SELECT name, level FROM skills WHERE user_id = ? AND level >= ? ORDER BY level DESC",
    (1, 60),
).fetchall()
print(f"  user 1 skills at level >= 60: {strong_user_one}")
#   user 1 skills at level >= 60: [('Python', 80), ('SQL', 60)]

# ============================================================
# [8] WHERE with OR
# ============================================================
# OR accepts rows matching either condition:

user_one_or_high = cursor.execute(
    "SELECT user_id, name FROM skills WHERE user_id = ? OR level >= ? ORDER BY user_id, name",
    (1, 90),
).fetchall()
print(f"  user 1 OR level >= 90: {user_one_or_high}")
#   user 1 OR level >= 90: [(1, 'Python'), (1, 'SQL'), (3, 'Go')]

# ============================================================
# [9] IN matches values from a set [07:24]
# ============================================================
# IN is convenient when a field may equal one of several
# supplied values:

in_rows = cursor.execute(
    "SELECT user_id, name FROM skills WHERE user_id IN (?, ?, ?) ORDER BY user_id, name",
    (1, 3, 4),
).fetchall()
print(f"  user IDs IN (1, 3, 4): {in_rows}")
#   user IDs IN (1, 3, 4): [(1, 'Python'), (1, 'SQL'), (3, 'Go'), (4, 'Pascal')]

# ============================================================
# [10] NOT IN excludes selected values [07:41]
# ============================================================
# NOT IN returns rows whose user_id is outside the list:

not_in_rows = cursor.execute(
    "SELECT DISTINCT user_id FROM skills WHERE user_id NOT IN (?, ?) ORDER BY user_id",
    (1, 2),
).fetchall()
print(f"  user IDs NOT IN (1, 2): {[row[0] for row in not_in_rows]}")
#   user IDs NOT IN (1, 2): [3, 4]

# ============================================================
# [11] Parameterized query avoids SQL injection [01:42]
# ============================================================
# Values are passed separately from SQL syntax:

safe_value = "Python' OR 1=1 --"
safe_result = cursor.execute(
    "SELECT name FROM skills WHERE name = ?", (safe_value,)
).fetchall()
print(f"  injected-looking value treated as data: {safe_result == []}")
print(f"  query uses a placeholder: {'name = ?' in 'SELECT name FROM skills WHERE name = ?'}")
#   injected-looking value treated as data: True
#   query uses a placeholder: True

# ============================================================
# [12] Close and clean the demo database
# ============================================================
# End the session and remove temporary files:

cursor.close()
db.close()
shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  database sandbox removed: {not os.path.exists(WORK_DIR)}")
#   database sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# SQLite query tools, from the transcript:
#
#   1. ORDER BY [03:22] -- sort user_id or name; ASC
#      ascending, DESC descending
#   2. LIMIT [04:27] -- return at most n ordered rows
#   3. OFFSET [04:57-05:51] -- skip rows before the limited
#      page; always pair with a deterministic ORDER BY
#   4. WHERE [06:33] -- comparison operators and AND/OR
#   5. IN / NOT IN [07:24] -- include or exclude a list of
#      parameterized values
#   6. SECURITY [01:42] -- ? placeholders treat supplied
#      values as data, not executable SQL
#   7. CLOSE -- cursor/connection closed, temporary DB removed
#
# Sort, page and filter in SQL; bind every user-supplied
# value rather than composing query text.
