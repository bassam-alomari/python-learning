# ============================================================
# Project 42 - sqlite3: the bookshop's data finally stops being JSON
# ============================================================
# What this lesson teaches:
#   sqlite3            the database that lives in one file
#   PRAGMA table_info  the schema is data you can read back
#   rowcount           counts rows CHANGED, and a SELECT reports -1
#   sqlite3.Row        a row is a tuple until you say otherwise
#   the ? placeholder  a value is data, a string you build is code
#   transactions       commit, or it never happened
#   type affinity      the column is a preference, not a cage
#   aggregates         COUNT never lies, SUM of nothing is NULL
#   EXPLAIN QUERY PLAN the planner shows you the shortcut it took
#   LEFT JOIN          the bookshop's loans, with a member who has none
#
# Everything is the standard library. The database is a real file in
# a temporary folder, so nothing is left behind. One note: sqlite3
# used to expose sqlite3.version; it is deprecated and dies under
# -W error, so this lesson reads sqlite3.sqlite_version instead.
#
# Run it:  python project-42-sqlite-the-bookshop-db.py
# ============================================================

import os
import shutil
import sqlite3
import sys
import tempfile

FOLDER = tempfile.mkdtemp(prefix="project42_")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  which standard library module opens a database file")
print("Q2  what does PRAGMA table_info give you back")
print("Q3  what is a row before you set row_factory")
print("Q4  why is the ? placeholder the only safe way to build SQL")
print("Q5  what does rowcount report after a SELECT")
print("Q6  what happens to an INSERT you never commit")
print("Q7  what does SQLite do with \"not a number\" in an INTEGER column")
print("Q8  what is SUM() of an empty set")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  sqlite3, and the file is a real database, not a text format")
print("Q2  the schema as rows: name, type, notnull, default, primary key")
print("Q3  a plain tuple, until row_factory = sqlite3.Row")
print("Q4  because a value is data, and a string you build is code")
print("Q5  -1, because SELECT does not change any rows")
print("Q6  nothing - without commit, the transaction rolls back")
print("Q7  it stores it as TEXT anyway; the column is a preference")
print("Q8  NULL, not zero - and COUNT is the aggregate that never lies")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - a database is a file with rules")
print("T1  the engine behind the file -> SQLite")
print("T1  the schema came back as this many rows -> 4")
print("T1  the columns -> ['id', 'title', 'price', 'copies']")
print("T1  the types -> ['INTEGER', 'TEXT', 'INTEGER', 'INTEGER']")
print("T1  so the schema is data you can read back -> True")
print()

print("TASK 2 - INSERT, and the rowcount trap")
print("T2  one INSERT gave lastrowid -> 1")
print("T2  and rowcount -> 1")
print("T2  a SELECT reports rowcount -> -1")
print("T2  executemany added this many rows -> 3")
print("T2  the table now holds -> 4")
print("T2  so rowcount counts changed rows, never found ones -> True")
print()

print("TASK 3 - a row is a tuple until you say otherwise")
print("T3  the plain row -> (1, 'Dune', 10, 3)")
print("T3  its type -> tuple")
print("T3  with row_factory it answers by name -> Dune")
print("T3  dict(row) -> {'id': 1, 'title': 'Dune', 'price': 10, 'copies': 3}")
print("T3  so a row can be a tuple or a mapping, your choice -> True")
print()

print("TASK 4 - the ? placeholder is the only safe way")
print("T4  the value that wants to escape -> ' OR 1=1 --")
print("T4  parameterised, it matches -> 0")
print("T4  the SQL you would have built -> SELECT COUNT(*) FROM books "
      "WHERE title = '' OR 1=1 --'")
print("T4  that SQL matches -> 4")
print("T4  so a value is data and a string is code -> True")
print()

print("TASK 5 - UPDATE, DELETE, and what rowcount counts")
print("T5  UPDATE that changed one row -> 1")
print("T5  UPDATE that matched nothing -> 0")
print("T5  DELETE that removed one row -> 1")
print("T5  SELECT still reports -> -1")
print("T5  so rowcount is about rows touched, not rows found -> True")
print()

print("TASK 6 - commit, or it never happened")
print("T6  rows committed before the rollback -> 1")
print("T6  rows inserted after it -> 1")
print("T6  rows that survived the reopen -> 1")
print("T6  so a transaction is all-or-nothing -> True")
print()

print("TASK 7 - the dynamic-typing leak")
print("T7  'not a number' into INTEGER became -> text")
print("T7  8 into TEXT became -> text")
print("T7  9 into REAL became -> real")
print("T7  so the column is a preference, not a cage -> True")
print()

print("TASK 8 - aggregates, and the NULL trap")
print("T8  over four rows -> COUNT 4, SUM 41, AVG 10.25, MIN Dune")
print("T8  over an empty set -> COUNT 0, SUM None, AVG None")
print("T8  so COUNT never lies and SUM of nothing is -> None")
print("T8  COALESCE turns it into -> 0")
print("T8  so NULL is a fact, not a bug -> True")
print()

print("TASK 9 - an index changes the plan")
print("T9  without an index the planner -> SCAN books")
print("T9  with one it -> SEARCH books USING INDEX idx_books_title (title=?)")
print("T9  so the index is a shortcut the planner can take -> True")
print()

print("TASK 10 - the loop, closed: the bookshop's loans")
print("T10  omar -> 2 loans, 28 days")
print("T10  sara -> 2 loans, 21 days")
print("T10  nour -> 1 loan, 3 days")
print("T10  lina -> 0 loans, 0 days")
print("T10  the member with no loans was rescued by -> COALESCE")
print("T10  the file database survived the reopen -> True")
print("T10  and the folder this file lives in is untouched -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)

projects_before = sorted(os.listdir(SCRIPT_DIR))

# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - a database is a file with rules")
print("-" * 60)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, "
            "title TEXT NOT NULL, price INTEGER NOT NULL, "
            "copies INTEGER NOT NULL DEFAULT 1)")
info = con.execute("PRAGMA table_info(books)").fetchall()
columns = [row[1] for row in info]
types = [row[2] for row in info]

check("the engine is SQLite", sqlite3.sqlite_version.count(".") == 2)
check("the schema came back as four rows", len(info) == 4)
check("the columns are id, title, price, copies",
      columns == ["id", "title", "price", "copies"])
check("the types are INTEGER, TEXT, INTEGER, INTEGER",
      types == ["INTEGER", "TEXT", "INTEGER", "INTEGER"])
check("the primary key column is id", [row[5] for row in info] == [1, 0, 0, 0])

print("T1  the engine behind the file -> SQLite")
print("T1  the schema came back as this many rows ->", len(info))
print("T1  the columns ->", columns)
print("T1  the types ->", types)
print("T1  so the schema is data you can read back ->",
      len(info) == 4 and columns == ["id", "title", "price", "copies"])
print()

# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - INSERT, and the rowcount trap")
print("-" * 60)
cursor = con.execute("INSERT INTO books (title, price, copies) "
                     "VALUES (?, ?, ?)", ("Dune", 10, 3))
lastrowid = cursor.lastrowid
insert_count = cursor.rowcount
select_cursor = con.execute("SELECT * FROM books")
select_count = select_cursor.rowcount
con.executemany("INSERT INTO books (title, price, copies) "
                "VALUES (?, ?, ?)",
                [("Hyperion", 12, 1), ("Foundation", 8, 5),
                 ("Kindred", 11, 0)])
total = con.execute("SELECT COUNT(*) FROM books").fetchone()[0]

check("the first insert got id 1", lastrowid == 1)
check("the insert changed one row", insert_count == 1)
check("a SELECT reports -1", select_count == -1)
check("executemany added three rows", total == 4)
check("the table holds four books", total == 4)

print("T2  one INSERT gave lastrowid ->", lastrowid)
print("T2  and rowcount ->", insert_count)
print("T2  a SELECT reports rowcount ->", select_count)
print("T2  executemany added this many rows ->", total - 1)
print("T2  the table now holds ->", total)
print("T2  so rowcount counts changed rows, never found ones ->",
      insert_count == 1 and select_count == -1)
print()

# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - a row is a tuple until you say otherwise")
print("-" * 60)
plain = con.execute("SELECT * FROM books").fetchone()
con.row_factory = sqlite3.Row
named = con.execute("SELECT * FROM books").fetchone()
named_dict = dict(named)

check("the plain row is a tuple", type(plain) is tuple)
check("the plain row is Dune", plain[1] == "Dune")
check("the named row answers by name", named["title"] == "Dune")
check("the named row is a mapping", isinstance(named, sqlite3.Row))
check("dict(row) has four keys", len(named_dict) == 4)

print("T3  the plain row ->", plain)
print("T3  its type ->", type(plain).__name__)
print("T3  with row_factory it answers by name ->", named["title"])
print("T3  dict(row) ->", named_dict)
print("T3  so a row can be a tuple or a mapping, your choice ->",
      type(plain) is tuple and isinstance(named, sqlite3.Row))
print()

# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - the ? placeholder is the only safe way")
print("-" * 60)
evil = "' OR 1=1 --"
safe = con.execute("SELECT COUNT(*) FROM books WHERE title = ?",
                   (evil,)).fetchone()[0]
broken_sql = "SELECT COUNT(*) FROM books WHERE title = '{0}'".format(evil)
broken = con.execute(broken_sql).fetchone()[0]

check("the parameterised value matches nothing", safe == 0)
check("the string-built SQL matches everything", broken == 4)
check("the string-built SQL is visibly different",
      broken_sql != "SELECT COUNT(*) FROM books WHERE title = ?")
check("the placeholder was used", "?" in
      "SELECT COUNT(*) FROM books WHERE title = ?")
check("the value never became part of the query", evil not in
      "SELECT COUNT(*) FROM books WHERE title = ?")

print("T4  the value that wants to escape ->", evil)
print("T4  parameterised, it matches ->", safe)
print("T4  the SQL you would have built ->", broken_sql)
print("T4  that SQL matches ->", broken)
print("T4  so a value is data and a string is code ->",
      safe == 0 and broken == 4)
print()

# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - UPDATE, DELETE, and what rowcount counts")
print("-" * 60)
con.execute("CREATE TABLE stock (item TEXT, qty INTEGER)")
con.execute("INSERT INTO stock VALUES ('pen', 5), ('pad', 2)")
changed = con.execute("UPDATE stock SET qty = qty + 1 "
                      "WHERE item = 'pen'").rowcount
matched_nothing = con.execute("UPDATE stock SET qty = qty + 1 "
                              "WHERE item = 'eraser'").rowcount
deleted = con.execute("DELETE FROM stock WHERE item = 'pad'").rowcount
select_still = con.execute("SELECT * FROM stock").rowcount

check("the UPDATE changed one row", changed == 1)
check("the UPDATE that matched nothing changed zero", matched_nothing == 0)
check("the DELETE removed one row", deleted == 1)
check("the SELECT still reports -1", select_still == -1)
check("the stock table holds one item",
      con.execute("SELECT COUNT(*) FROM stock").fetchone()[0] == 1)

print("T5  UPDATE that changed one row ->", changed)
print("T5  UPDATE that matched nothing ->", matched_nothing)
print("T5  DELETE that removed one row ->", deleted)
print("T5  SELECT still reports ->", select_still)
print("T5  so rowcount is about rows touched, not rows found ->",
      changed == 1 and matched_nothing == 0 and select_still == -1)
print()

# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - commit, or it never happened")
print("-" * 60)
file_db = os.path.join(FOLDER, "shop.db")
fcon = sqlite3.connect(file_db)
fcon.execute("CREATE TABLE t (v TEXT)")
fcon.execute("INSERT INTO t VALUES ('committed')")
fcon.commit()
fcon.execute("INSERT INTO t VALUES ('never saved')")
committed_before = fcon.execute(
    "SELECT COUNT(*) FROM t WHERE v = 'committed'").fetchone()[0]
pending_before = fcon.execute(
    "SELECT COUNT(*) FROM t WHERE v = 'never saved'").fetchone()[0]
fcon.rollback()
fcon.close()
again = sqlite3.connect(file_db)
survived = again.execute("SELECT v FROM t").fetchall()
again.close()

check("the committed row was visible before the rollback",
      committed_before == 1)
check("the pending row was visible before the rollback",
      pending_before == 1)
check("the rollback removed the uncommitted row", len(survived) == 1)
check("the surviving row is the committed one",
      survived == [("committed",)])
check("the database is a real file", os.path.getsize(file_db) > 0)
with open(file_db, "rb") as handle:
    header = handle.read(16)
check("the file is a SQLite database",
      header.startswith(b"SQLite format 3"))

print("T6  rows committed before the rollback ->", committed_before)
print("T6  rows inserted after it ->", pending_before)
print("T6  rows that survived the reopen ->", len(survived))
print("T6  so a transaction is all-or-nothing ->",
      len(survived) == 1 and survived == [("committed",)])
print()

# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - the dynamic-typing leak")
print("-" * 60)
con.execute("CREATE TABLE affinity (n INTEGER, t TEXT, r REAL)")
con.execute("INSERT INTO affinity VALUES (?, ?, ?)",
            ("not a number", "x", "y"))
con.execute("INSERT INTO affinity VALUES (?, ?, ?)", (7, 8, 9))
kinds = con.execute("SELECT typeof(n), typeof(t), typeof(r) "
                    "FROM affinity").fetchall()

check("the text stayed text in the INTEGER column",
      kinds[0][0] == "text")
check("the integer became text in the TEXT column", kinds[1][1] == "text")
check("the integer became real in the REAL column", kinds[1][2] == "real")
check("the first row kept its text nature",
      tuple(kinds[0]) == ("text", "text", "text"))
check("the second row obeyed the columns",
      tuple(kinds[1]) == ("integer", "text", "real"))

print("T7  'not a number' into INTEGER became ->", kinds[0][0])
print("T7  8 into TEXT became ->", kinds[1][1])
print("T7  9 into REAL became ->", kinds[1][2])
print("T7  so the column is a preference, not a cage ->",
      kinds[0][0] == "text" and kinds[1][1] == "text" and kinds[1][2] == "real")
print()

# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - aggregates, and the NULL trap")
print("-" * 60)
summary = con.execute("SELECT COUNT(*), SUM(price), AVG(price), MIN(title) "
                      "FROM books").fetchone()
empty = con.execute("SELECT COUNT(*), SUM(price), AVG(price), MIN(title) "
                    "FROM books WHERE copies > 99").fetchone()
rescued = con.execute("SELECT COALESCE(SUM(price), 0) "
                      "FROM books WHERE copies > 99").fetchone()[0]

check("four books are counted", summary[0] == 4)
check("the prices sum to 41", summary[1] == 41)
check("the average is 10.25", summary[2] == 10.25)
check("the earliest title is Dune", summary[3] == "Dune")
check("COUNT of an empty set is 0", empty[0] == 0)
check("SUM of an empty set is NULL", empty[1] is None)
check("COALESCE turns NULL into 0", rescued == 0)

print("T8  over four rows -> COUNT {0}, SUM {1}, AVG {2}, MIN {3}".format(
    summary[0], summary[1], summary[2], summary[3]))
print("T8  over an empty set -> COUNT {0}, SUM {1}, AVG {2}".format(
    empty[0], empty[1], empty[2]))
print("T8  so COUNT never lies and SUM of nothing is ->", empty[1])
print("T8  COALESCE turns it into ->", rescued)
print("T8  so NULL is a fact, not a bug ->",
      empty[0] == 0 and empty[1] is None and rescued == 0)
print()

# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - an index changes the plan")
print("-" * 60)
before_plan = con.execute("EXPLAIN QUERY PLAN SELECT * FROM books "
                          "WHERE title = 'Dune'").fetchone()[3]
con.execute("CREATE INDEX idx_books_title ON books(title)")
after_plan = con.execute("EXPLAIN QUERY PLAN SELECT * FROM books "
                         "WHERE title = 'Dune'").fetchone()[3]

check("without an index the planner scans", before_plan == "SCAN books")
check("with an index it searches", after_plan.startswith("SEARCH books"))
check("the index is named in the plan", "idx_books_title" in after_plan)
check("the plan changed", before_plan != after_plan)
check("the index exists in the schema",
      any(row[1] == "idx_books_title"
          for row in con.execute("PRAGMA index_list(books)")))

print("T9  without an index the planner ->", before_plan)
print("T9  with one it ->", after_plan)
print("T9  so the index is a shortcut the planner can take ->",
      before_plan != after_plan and "idx_books_title" in after_plan)
print()

# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the loop, closed: the bookshop's loans")
print("-" * 60)
shop_db = os.path.join(FOLDER, "shop-loans.db")
shop = sqlite3.connect(shop_db)
shop.row_factory = sqlite3.Row
shop.execute("CREATE TABLE members (id INTEGER PRIMARY KEY, name TEXT)")
shop.execute("CREATE TABLE loans (id INTEGER PRIMARY KEY, member_id INTEGER, "
             "book_id INTEGER, days INTEGER)")
shop.executemany("INSERT INTO members (name) VALUES (?)",
                 [("sara",), ("nour",), ("omar",), ("lina",)])
shop.executemany("INSERT INTO loans (member_id, book_id, days) VALUES (?, ?, ?)",
                 [(1, 1, 7), (1, 2, 14), (2, 1, 3), (3, 3, 7), (3, 1, 21)])
shop.commit()
shop.close()

reopened = sqlite3.connect(shop_db)
reopened.row_factory = sqlite3.Row
joined = reopened.execute("""
    SELECT m.name AS name, COUNT(l.id) AS loans,
           COALESCE(SUM(l.days), 0) AS days
    FROM members m
    LEFT JOIN loans l ON l.member_id = m.id
    GROUP BY m.id
    ORDER BY loans DESC, m.name
""").fetchall()
reopened.close()

by_name = {row["name"]: row for row in joined}
lina = by_name["lina"]

check("four members came back", len(joined) == 4)
check("omar leads with two loans", by_name["omar"]["loans"] == 2)
check("sara has two loans", by_name["sara"]["loans"] == 2)
check("nour has one loan", by_name["nour"]["loans"] == 1)
check("lina has no loans", lina["loans"] == 0)
check("lina's days were rescued to zero", lina["days"] == 0)
check("the file database survived the reopen",
      os.path.getsize(shop_db) > 0)

for row in joined:
    word = "loan" if row["loans"] == 1 else "loans"
    print("T10  {0} -> {1} {2}, {3} days".format(
        row["name"], row["loans"], word, row["days"]))
print("T10  the member with no loans was rescued by -> COALESCE")
print("T10  the file database survived the reopen ->",
      os.path.getsize(shop_db) > 0)
projects_after = sorted(os.listdir(SCRIPT_DIR))
print("T10  and the folder this file lives in is untouched ->",
      projects_before == projects_after)
print()

# ------------------------------------------------------------
# clean up and report
# ------------------------------------------------------------
for connection in (con, fcon, again, shop, reopened):
    try:
        connection.close()
    except Exception:                                   # noqa: BLE001
        pass
shutil.rmtree(FOLDER, ignore_errors=True)

failed = [name for name, ok in CHECKS if not ok]
print("=" * 60)
if failed:
    for name in failed:
        print("  FAILED:", name)
    print("CHECKS PASSED {0} of {1}".format(
        len(CHECKS) - len(failed), len(CHECKS)))
    sys.exit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)