# -----------------------------------------------------------------
# Lesson 65: file handling -- open() and the file modes
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : open(path, mode), modes r / w / a, relative vs
#            absolute paths, the os module, backslash paths and
#            raw strings, check-before-open discipline
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# File handling is the bridge between a program that forgets
# everything at exit and one that keeps its work. The transcript
# lists what this block of lessons covers: open an existing file,
# create a new one, read from it, write, edit, and delete its
# content. This lesson builds the foundation: the open()
# function, the three modes, and where files actually live.
#
#       open(file_path, mode)          (encoding added by habit)
#
#   r  read       -- file must exist; missing -> FileNotFoundError
#   w  write      -- creates if missing, and ERASES old content
#   a  append     -- creates if missing, adds at the END
#
# HOW THIS LESSON RUNS SAFELY: real files would litter the course
# tree, so everything below happens inside a fresh temporary
# folder (tempfile.mkdtemp) that we chdir into and -- guarded by
# try/finally -- delete again no matter what happens. The cleanup
# itself is part of the lesson: always leave the filesystem the
# way you found it.
#
# Only stable facts are printed (booleans, fixed names, file
# contents) -- never machine-specific paths, so the output is
# byte-identical on every run and on every machine.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

import os
import shutil
import tempfile

# ============================================================
# [0] The sandbox: a work folder we guarantee to clean up
# ============================================================
# Remember where we started, make a private folder, move into
# it -- so every RELATIVE path below means "inside the sandbox":

ORIGINAL_CWD = os.getcwd()
WORK_DIR = tempfile.mkdtemp(prefix="py65_")

try:
    os.chdir(WORK_DIR)          # from here on, cwd == sandbox

    # ============================================================
    # [1] open(): two basic arguments -- path and mode
    # ============================================================
    # The transcript's signature: a file path/name and a mode.
    # First contact: mode w creates the file, one write, then we
    # close it -- every open() gets its close() (the with
    # statement that pairs them automatically arrives next
    # lesson):

    f = open("notes.txt", "w", encoding="utf-8")   # w: create/write
    f.write("Hello, file!")                        # one string in
    f.close()                                      # always close

    print(f"  created: {os.path.exists('notes.txt')}")
    #   created: True

    f = open("notes.txt", "r", encoding="utf-8")   # r: read it back
    content = f.read()
    f.close()
    print(f"  content: {content}")
    #   content: Hello, file!

    # Two opens, two closes, one file on disk. encoding="utf-8"
    # names the text encoding explicitly -- the habit from
    # project 48 that keeps every machine reading the file the
    # same way.

    # ============================================================
    # [2] Mode w: creates -- and ERASES what was there
    # ============================================================
    # The transcript's warning: "احذر لأنه يحذف أي محتوى قديم".
    # Prove it: write content, then open with w AGAIN and watch
    # the old text vanish. A small reader (same open/read/close
    # the way section 1 showed it) keeps later sections about
    # MODES instead of about retyping mechanics:

    def read_text(name):
        """Whole file as one string, trailing blank lines trimmed."""
        reader = open(name, "r", encoding="utf-8")
        text = reader.read()
        reader.close()
        return text.strip()

    f = open("truncation.txt", "w", encoding="utf-8")
    f.write("old content that vanishes")
    f.close()

    f = open("truncation.txt", "w", encoding="utf-8")   # second w
    f.write("only this remains")
    f.close()

    print(f"  after second write: {read_text('truncation.txt')}")
    #   after second write: only this remains

    # The second open("...w") emptied the file the moment it
    # opened -- the first string never had a chance. That is the
    # trap the transcript warns about, and it is NOT a mistake
    # you get warned about: w silently does its job.

    # ============================================================
    # [3] Mode a: append -- creates, and never erases
    # ============================================================
    # a adds at the END. On a file that does not exist yet, it
    # creates it -- so log.txt is born from appends alone:

    print(f"  log existed before: {os.path.exists('log.txt')}")
    #   log existed before: False

    f = open("log.txt", "a", encoding="utf-8")     # a: creates too
    f.write("first entry\n")
    f.close()

    f = open("log.txt", "a", encoding="utf-8")     # adds after
    f.write("second entry\n")
    f.close()

    print("  after two appends:")
    print(read_text("log.txt"))
    #   after two appends:
    # first entry
    # second entry

    # Both entries survived because a never truncates. Had we
    # used w for the second line, the file would now say only
    # "second entry" -- section 9 runs that comparison side by
    # side.

    # ============================================================
    # [4] Mode r: read only -- and the missing-file error
    # ============================================================
    # r needs the file to already exist. Existing file: content
    # comes back. Missing file: Python raises at the open()
    # line itself -- no file object is ever created, so there is
    # nothing to close:

    f = open("notes.txt", "r", encoding="utf-8")
    existing = f.read()
    f.close()
    print(f"  read existing: {existing}")
    #   read existing: Hello, file!

    try:
        f = open("missing.txt", "r", encoding="utf-8")   # raises here
        f.close()
    except FileNotFoundError as error:
        print(f"  missing file -> {type(error).__name__}")
    #   missing file -> FileNotFoundError

    # FileNotFoundError (a subclass of OSError) is Python saying
    # "r refuses to invent a file." Modes r, w, a answer the
    # three questions from the transcript: what if it is missing?
    #   r -> error,  w -> create (and wipe),  a -> create (and
    #   add at the end).

    # ============================================================
    # [5] File paths: relative vs absolute
    # ============================================================
    # The transcript's [02:14]. A RELATIVE path ("notes.txt") is
    # resolved against the current working directory; an
    # ABSOLUTE path starts at the filesystem root and needs no
    # context. We are inside the sandbox, so look at the facts:

    print(f"  cwd is absolute: {os.path.isabs(os.getcwd())}")
    print(f"  notes.txt is absolute: {os.path.isabs('notes.txt')}")
    print(f"  abspath is absolute: {os.path.isabs(os.path.abspath('notes.txt'))}")
    print(f"  cwd is a directory: {os.path.isdir(os.getcwd())}")
    resolved = os.path.isfile(os.path.join(WORK_DIR, "notes.txt"))
    print(f"  relative resolved in cwd: {resolved}")
    #   cwd is absolute: True
    #   notes.txt is absolute: False
    #   abspath is absolute: True
    #   cwd is a directory: True
    #   relative resolved in cwd: True

    # os.path.abspath() answered "where would 'notes.txt' land
    # from here?" without printing a machine-specific path --
    # the last line checks that spot directly. Absolute paths
    # (built with os.path.join) always mean the same file no
    # matter what the cwd happens to be; section 10 proves that
    # from inside another directory.

    # ============================================================
    # [6] The os module: inspect and manage the filesystem
    # ============================================================
    # The transcript's [04:27]. os is Python's window onto the
    # operating system -- where you are, what exists, what to
    # make or remove:

    os.mkdir("data")
    print(f"  mkdir data isdir: {os.path.isdir('data')}")
    print(f"  notes.txt isfile: {os.path.isfile('notes.txt')}")
    print(f"  data isfile: {os.path.isfile('data')}")
    print(f"  getsize notes.txt: {os.path.getsize('notes.txt')}")

    f = open("trash.txt", "w", encoding="utf-8")
    f.write("throwaway")
    f.close()
    os.remove("trash.txt")
    print(f"  after os.remove: {os.path.exists('trash.txt')}")

    print(f"  listdir: {sorted(os.listdir())}")
    #   mkdir data isdir: True
    #   notes.txt isfile: True
    #   data isfile: False
    #   getsize notes.txt: 12
    #   after os.remove: False
    #   listdir: ['data', 'log.txt', 'notes.txt', 'truncation.txt']

    # The toolkit in one block: getcwd/isdir (where am I?),
    # isfile/exists (is it there?), mkdir (make a folder),
    # getsize (12 bytes for "Hello, file!"), remove (delete a
    # FILE -- folders need rmtree/shutil), and listdir -- sorted
    # here, because os.listdir() returns names in no promised
    # order and this lesson demands identical output every run.

    # ============================================================
    # [7] The backslash problem, and raw strings
    # ============================================================
    # The transcript's [09:02]: Windows paths are written with
    # backslashes, but inside a normal string some of those
    # pair up into escape sequences -- "reports\notes.txt"
    # hides a NEWLINE where the folder separator was meant:

    plain = "reports\notes.txt"    # \n became one newline char
    raw = r"reports\notes.txt"     # the r keeps it literal

    plain_lines = "\n" in plain
    raw_lines = "\n" in raw
    raw_slash = "\\" in raw
    print(f"  len(plain): {len(plain)}")
    print(f"  len(raw): {len(raw)}")
    print(f"  plain has newline: {plain_lines}")
    print(f"  raw has newline: {raw_lines}")
    print(f"  raw has backslash: {raw_slash}")
    #   len(plain): 16
    #   len(raw): 17
    #   plain has newline: True
    #   raw has newline: False
    #   raw has backslash: True

    # The plain string lost a character (the escape ate the n)
    # and gained a newline; the raw string kept all 17 as text.
    # Three defenses, in order of preference: (1) build paths
    # with os.path.join instead of typing separators, (2) write
    # paths with forward slashes -- Python accepts / on every
    # operating system, including Windows, (3) when you must
    # paste a real Windows path, prefix the string with r.

    # ============================================================
    # [8] The beginner's common error: opening blind
    # ============================================================
    # A wrong path and a missing file look identical from the
    # outside -- both end in FileNotFoundError. The os module
    # (transcript's toolkit) turns that into a clean decision:

    target = "missing.txt"
    if os.path.exists(target):
        f = open(target, "r", encoding="utf-8")
        f.close()
    else:
        print(f"  skipped {target}: not found (create with w or a)")
    #   skipped missing.txt: not found (create with w or a)

    # Existence checks belong where MISSING files are normal
    # (settings files, first runs) -- not everywhere: the
    # check-then-open pattern is a race in multi-process code,
    # and for required files, letting r raise its FileNotFoundError
    # IS the report you want.

    # ============================================================
    # [9] Choosing the mode: w regenerates, a accumulates
    # ============================================================
    # The decision rule, shown twice on real files. A report is
    # rebuilt from scratch every run -> w. A log keeps its
    # history -> a:

    f = open("report.txt", "w", encoding="utf-8")   # regenerate
    f.write("report for today")
    f.close()

    f = open("report.txt", "w", encoding="utf-8")   # tomorrow: w again
    f.write("report for tomorrow")
    f.close()
    print(f"  report.txt via w: {read_text('report.txt')}")

    f = open("log.txt", "a", encoding="utf-8")      # history grows
    f.write("third entry\n")
    f.close()
    print("  log.txt via a:")
    print(read_text("log.txt"))
    #   report.txt via w: report for tomorrow
    #   log.txt via a:
    # first entry
    # second entry
    # third entry

    # report.txt holds ONE line -- everything before "tomorrow"
    # was wiped by the second w. log.txt holds THREE -- every a
    # added without touching what came before. One question
    # decides the mode: should this open erase the file?

    # ============================================================
    # [10] Paths in practice: move cwd, watch where files land
    # ============================================================
    # Relative paths follow the working directory around;
    # absolute paths do not. Prove it by writing one of each
    # from INSIDE the data/ subfolder:

    os.chdir(os.path.join(WORK_DIR, "data"))        # cwd is now data/

    f = open("rel.txt", "w", encoding="utf-8")      # relative -> data/
    f.write("made by relative path")
    f.close()

    absolute_target = os.path.join(WORK_DIR, "abs.txt")   # absolute
    f = open(absolute_target, "w", encoding="utf-8")
    f.write("made by absolute path")
    f.close()

    rel_in_data = os.path.isfile(os.path.join(WORK_DIR, "data", "rel.txt"))
    abs_at_top = os.path.isfile(os.path.join(WORK_DIR, "abs.txt"))
    rel_at_top = os.path.isfile(os.path.join(WORK_DIR, "rel.txt"))
    print(f"  rel.txt inside data/: {rel_in_data}")
    print(f"  abs.txt at top level: {abs_at_top}")
    print(f"  rel.txt at top level: {rel_at_top}")
    os.chdir(WORK_DIR)                              # back to sandbox root
    #   rel.txt inside data/: True
    #   abs.txt at top level: True
    #   rel.txt at top level: False

    # rel.txt was written RELATIVELY while cwd was data/ -- so
    # it landed in data/ (True) and NOT at the top (False).
    # abs.txt was built from WORK_DIR and landed at the top no
    # matter where we stood. That is the whole difference: one
    # path answers "relative to WHERE?", the other never asks.

    # ============================================================
    # [11] The file lifecycle: create, use, delete
    # ============================================================
    # The transcript's opening promise includes deleting
    # content. os.remove() removes a FILE; after it, every
    # check agrees the file is gone:

    job = "tempjob.txt"
    f = open(job, "w", encoding="utf-8")
    f.write("scratch work")
    f.close()
    print(f"  exists after create: {os.path.exists(job)}")

    os.remove(job)
    print(f"  exists after remove: {os.path.exists(job)}")
    #   exists after create: True
    #   exists after remove: False

    # open -> write -> close -> remove, the full arc in six
    # lines. (For folders, os.remove fails -- folders need
    # shutil.rmtree, which the cleanup below uses on the whole
    # sandbox.)

    # ============================================================
    # [12] One small session, then guaranteed cleanup
    # ============================================================
    # Everything this lesson taught, in the order a real
    # program would use it: start fresh with w, extend with a,
    # read the result with r:

    f = open("session.txt", "w", encoding="utf-8")  # w: fresh start
    f.write("line one\n")
    f.close()

    f = open("session.txt", "a", encoding="utf-8")  # a: keep going
    f.write("line two\n")
    f.close()

    print("  session.txt:")
    print(read_text("session.txt"))
    #   session.txt:
    # line one
    # line two

    # The three modes, one file, no data lost that should have
    # stayed. Now the promise from [0] -- whatever happened
    # above, this runs:

finally:
    os.chdir(ORIGINAL_CWD)                       # leave the folder first
    shutil.rmtree(WORK_DIR, ignore_errors=True)  # then erase it all

# No print lives inside finally, so nothing here depends on how
# the try-block ended -- and the sandbox is gone either way:
print(f"  work folder removed: {not os.path.exists(WORK_DIR)}")
#   work folder removed: True

# ============================================================
# [13] The summary
# ============================================================
# File handling, as the transcript introduces it:
#
#   1. open(file_path, mode) takes two basics: WHERE the file
#      is and HOW to open it; we add encoding="utf-8" so every
#      machine decodes the same bytes the same way
#   2. MODE r -- read only; the file must exist, otherwise
#      FileNotFoundError is raised at the open() line (nothing
#      to close)
#   3. MODE w -- write: creates the file if missing AND ERASES
#      any old content the moment it opens; no warning, so use
#      it only when a fresh file is exactly what you want
#   4. MODE a -- append: creates if missing, otherwise adds at
#      the END; old content always survives -- the log mode
#   5. PATHS -- relative paths resolve against the current
#      working directory (os.getcwd()); absolute paths start
#      at the root and work from anywhere; os.path.isabs()
#      tells them apart, os.path.abspath() shows where a
#      relative name would land
#   6. THE os MODULE -- getcwd, exists, isfile, isdir, mkdir,
#      remove, listdir, getsize: the operating system behind
#      one import (sort listdir output when order matters)
#   7. BACKSLASHES -- "path\new" hides escape sequences; fix
#      with os.path.join first, forward slashes second (they
#      work on Windows too), raw strings third (r"path\...")
#   8. DISCIPLINE -- every open() gets a close(); check
#      existence when missing files are normal; delete files
#      with os.remove and folders with shutil.rmtree; clean up
#      what you create (our sandbox: try/finally, proven by
#      the final True)
#
# The transcript closes by promising the practical details --
# reading line by line, writing structures, the with statement
# that closes files automatically -- for the lessons ahead.
# With r / w / a and paths solid underneath, those lessons are
# all about WHAT goes into the file.
