# ============================================================
# Project 48 - pathlib: the bookshop organises its shelf
# ============================================================
# What this lesson teaches:
#   Path                a path as an object, not a string
#   name, stem, suffix   the pieces a path is made of
#   parent, parts        where it lives, and the whole chain
#   /                   join a piece, the readable way
#   with_suffix, with_name  rewrite a path, touch nothing
#   PureWindowsPath     the logic, with the Windows separator
#   PurePosixPath       the same logic, with the POSIX separator
#   read_text/write_text   text in and out, with an explicit encoding
#   is_file, is_dir, exists   questions the filesystem can answer
#   glob                select files by pattern
#   rename              move the bytes, keep the content
#
# Everything is the standard library. No input(), no random, no datetime.now.
# The output is deterministic. The file runs to completion and exits with 0.
# Nothing here ever prints an absolute path: a path on this machine is not
# the same path on yours.
#
# Run it:  python project-48-pathlib-the-bookshop-organises-its-shelf.py
# ============================================================

import pathlib
import shutil
import sys
import tempfile

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
print("Q1  what is a Path")
print("Q2  what do name, stem, and suffix give you")
print("Q3  what does the / operator do on a Path")
print("Q4  what is a pure path")
print("Q5  what do with_suffix and with_name change")
print("Q6  why pass encoding= to read_text and write_text")
print("Q7  what does glob do")
print("Q8  why never print resolve()")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  an object that holds the path and knows how to take it apart")
print("Q2  the file name, the name without its extension, and the extension")
print("Q3  it joins a piece onto the path, like os.path.join but readable")
print("Q4  a path with the logic but no filesystem, so it behaves the same")
print("Q5  they return a new path with that piece changed, and touch nothing")
print("Q6  so the bytes become text the same way on every machine")
print("Q7  it selects files by pattern, like *.txt, inside a folder")
print("Q8  because it prints this machine's absolute path, which is not yours")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - a path is made of pieces")
print("T1  the name -> dune.txt")
print("T1  the stem -> dune")
print("T1  so a path is made of pieces -> True")
print()

print("TASK 2 - the / operator joins")
print("T2  joined -> data/books/dune.txt")
print("T2  so / builds a path -> True")
print()

print("TASK 3 - rewrite a path, touch nothing")
print("T3  with_suffix(.md) -> data/books/dune.md")
print("T3  with_name(messiah.txt) -> data/books/messiah.txt")
print("T3  so a path can be rewritten without touching disk -> True")
print()

print("TASK 4 - pure paths pick the separator")
print("T4  windows -> C:\\shop\\books\\dune.txt")
print("T4  posix -> shop/books/dune.txt")
print("T4  so pure paths pick the separator -> True")
print()

print("TASK 5 - parts and absolute, without a filesystem")
print("T5  parts -> ('/', 'srv', 'books', 'dune.txt')")
print("T5  so parts splits the path -> True")
print()

print("TASK 6 - text in, text out, encoding named")
print("T6  the shelf -> Dune | Dune Messiah")
print("T6  so write_text and read_text round-trip -> True")
print()

print("TASK 7 - the filesystem answers questions")
print("T7  shelf.txt is a file -> True")
print("T7  covers is a directory -> True")
print("T7  missing.txt exists -> False")
print("T7  so the filesystem answers questions -> True")
print()

print("TASK 8 - glob selects by pattern")
print("T8  the txt files -> ['dune.txt', 'messiah.txt']")
print("T8  so glob selects by pattern -> True")
print()

print("TASK 9 - rename moves the bytes")
print("T9  after rename -> True")
print("T9  the old name is gone -> True")
print("T9  so rename keeps the bytes -> True")
print()

print("TASK 10 - the shelf writes its own index")
print("T10  indexed -> 2")
print("T10  the index says -> dune.txt,messiah.txt")
print("T10  so pathlib can build a report -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)


# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - a path is made of pieces")
print("-" * 60)
book = pathlib.Path("data/books/dune.txt")

check("name is the whole file name", book.name == "dune.txt")
check("stem drops the suffix", book.stem == "dune")
check("suffix keeps the dot", book.suffix == ".txt")
check("parent is the folder", book.parent.as_posix() == "data/books")

print("T1  the name ->", book.name)
print("T1  the stem ->", book.stem)
print("T1  so a path is made of pieces ->",
      book.name == "dune.txt" and book.stem == "dune")
print()


# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - the / operator joins")
print("-" * 60)
joined = pathlib.Path("data") / "books" / "dune.txt"

check("it is a Path", isinstance(joined, pathlib.Path))
check("joined without any concatenation",
      joined.as_posix() == "data/books/dune.txt")
check("the name survived", joined.name == "dune.txt")
check("parts are in order",
      joined.parts == ("data", "books", "dune.txt"))

print("T2  joined ->", joined.as_posix())
print("T2  so / builds a path ->",
      joined.as_posix() == "data/books/dune.txt")
print()


# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - rewrite a path, touch nothing")
print("-" * 60)
new_suffix = book.with_suffix(".md")
new_name = book.with_name("messiah.txt")
no_suffix = book.with_suffix("")

check("with_suffix swapped the extension",
      new_suffix.as_posix() == "data/books/dune.md")
check("with_name swapped the file name",
      new_name.as_posix() == "data/books/messiah.txt")
check("with_suffix('') drops it", no_suffix.as_posix() == "data/books/dune")
check("the original is untouched",
      book.as_posix() == "data/books/dune.txt")

print("T3  with_suffix(.md) ->", new_suffix.as_posix())
print("T3  with_name(messiah.txt) ->", new_name.as_posix())
print("T3  so a path can be rewritten without touching disk ->",
      book.as_posix() == "data/books/dune.txt")
print()


# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - pure paths pick the separator")
print("-" * 60)
windows = pathlib.PureWindowsPath("C:/shop/books") / "dune.txt"
posix = pathlib.PurePosixPath("shop/books") / "dune.txt"

check("windows joins with a backslash",
      str(windows) == "C:\\shop\\books\\dune.txt")
check("posix joins with a slash", str(posix) == "shop/books/dune.txt")
check("both keep the same file name", windows.name == posix.name)
check("the separators really differ", str(windows) != str(posix))

print("T4  windows ->", str(windows))
print("T4  posix ->", str(posix))
print("T4  so pure paths pick the separator ->", str(windows) != str(posix))
print()


# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - parts and absolute, without a filesystem")
print("-" * 60)
pure = pathlib.PurePosixPath("/srv/books/dune.txt")

check("parts splits every piece",
      pure.parts == ("/", "srv", "books", "dune.txt"))
check("an absolute path says so", pure.is_absolute())
check("a relative path says so too",
      not pathlib.PurePosixPath("srv/books").is_absolute())
check("no folder was opened", pure.name == "dune.txt")

print("T5  parts ->", pure.parts)
print("T5  so parts splits the path ->",
      pure.parts == ("/", "srv", "books", "dune.txt"))
print()


# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - text in, text out, encoding named")
print("-" * 60)
with tempfile.TemporaryDirectory(prefix="project48") as folder:
    shelf = pathlib.Path(folder) / "shelf.txt"
    shelf.write_text("Dune\nDune Messiah\n", encoding="utf-8")
    text = shelf.read_text(encoding="utf-8")

    cafe = pathlib.Path(folder) / "cafe.txt"
    cafe.write_text("Café\n", encoding="utf-8")
    round_trip = cafe.read_text(encoding="utf-8")
    shelf_exists = shelf.exists()

check("the text came back whole", text == "Dune\nDune Messiah\n")
check("utf-8 round-tripped a non-ascii character", round_trip == "Café\n")
check("the file really exists", shelf_exists)
check("encoding was never guessed", shelf.name == "shelf.txt")

print("T6  the shelf ->", " | ".join(text.splitlines()))
print("T6  so write_text and read_text round-trip ->",
      text == "Dune\nDune Messiah\n")
print()


# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - the filesystem answers questions")
print("-" * 60)
with tempfile.TemporaryDirectory(prefix="project48") as folder:
    base = pathlib.Path(folder)
    (base / "shelf.txt").write_text("Dune\n", encoding="utf-8")
    (base / "covers").mkdir()
    missing = base / "missing.txt"

    is_file = (base / "shelf.txt").is_file()
    is_dir = (base / "covers").is_dir()
    missing_exists = missing.exists()
    base_exists = base.exists()

check("the file answers is_file", is_file)
check("the folder answers is_dir", is_dir)
check("the missing file answers False", not missing_exists)
check("the folder itself exists", base_exists)

print("T7  shelf.txt is a file ->", is_file)
print("T7  covers is a directory ->", is_dir)
print("T7  missing.txt exists ->", missing_exists)
print("T7  so the filesystem answers questions ->",
      is_file and is_dir and not missing_exists)
print()


# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - glob selects by pattern")
print("-" * 60)
with tempfile.TemporaryDirectory(prefix="project48") as folder:
    base = pathlib.Path(folder)
    for name in ("dune.txt", "messiah.txt", "notes.md"):
        (base / name).write_text(name + "\n", encoding="utf-8")

    txt_files = sorted(p.name for p in base.glob("*.txt"))
    everything = sorted(p.name for p in base.iterdir())

check("only the txt files came back",
      txt_files == ["dune.txt", "messiah.txt"])
check("the markdown file stayed out", "notes.md" not in txt_files)
check("iterdir sees all three", len(everything) == 3)
check("sorted, so the order is stable",
      everything == ["dune.txt", "messiah.txt", "notes.md"])

print("T8  the txt files ->", txt_files)
print("T8  so glob selects by pattern ->",
      txt_files == ["dune.txt", "messiah.txt"])
print()


# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - rename moves the bytes")
print("-" * 60)
with tempfile.TemporaryDirectory(prefix="project48") as folder:
    base = pathlib.Path(folder)
    old = base / "old.txt"
    old.write_text("Dune\n", encoding="utf-8")
    new = base / "new.txt"
    old.rename(new)

    new_exists = new.exists()
    old_gone = not old.exists()
    moved = new.read_text(encoding="utf-8")
    left = len(list(base.iterdir()))

check("the new name exists", new_exists)
check("the old name is gone", old_gone)
check("the bytes came with it", moved == "Dune\n")
check("only one file left", left == 1)

print("T9  after rename ->", new_exists)
print("T9  the old name is gone ->", old_gone)
print("T9  so rename keeps the bytes ->", moved == "Dune\n")
print()


# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the shelf writes its own index")
print("-" * 60)
with tempfile.TemporaryDirectory(prefix="project48") as folder:
    base = pathlib.Path(folder)
    (base / "dune.txt").write_text("Dune\n", encoding="utf-8")
    (base / "messiah.txt").write_text("Messiah\n", encoding="utf-8")
    (base / "notes.md").write_text("notes\n", encoding="utf-8")

    names = sorted(p.name for p in base.glob("*.txt"))
    index = base / "index.txt"
    index.write_text("\n".join(names) + "\n", encoding="utf-8")
    back = index.read_text(encoding="utf-8")
    index_is_file = index.is_file()

check("two books were indexed", len(names) == 2)
check("the markdown was left out", "notes.md" not in names)
check("the index file exists", index_is_file)
check("the index says what we wrote",
      back == "dune.txt\nmessiah.txt\n")
check("one glob, one write, one read",
      names == ["dune.txt", "messiah.txt"])

print("T10  indexed ->", len(names))
print("T10  the index says ->", ",".join(names))
print("T10  so pathlib can build a report ->",
      back == "dune.txt\nmessiah.txt\n")
print()


# ------------------------------------------------------------
# report
# ------------------------------------------------------------
failed = [name for name, ok in CHECKS if not ok]
for leftovers in pathlib.Path(tempfile.gettempdir()).glob("project48*"):
    shutil.rmtree(leftovers, ignore_errors=True)
print("=" * 60)
if failed:
    for name in failed:
        print("  FAILED:", name)
    print("CHECKS PASSED {0} of {1}".format(
        len(CHECKS) - len(failed), len(CHECKS)))
    sys.exit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
