# -----------------------------------------------------------------
# Lesson 68: file handling part 4 -- important info
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : tell() and the cursor position, read(size) while
#            watching tell() climb, seek(offset) to rewind or
#            jump, in-place edit with seek + r+, deleting files
#            with os.remove(), and what os can do with no
#            external packages
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lessons 65 to 67 opened, read, and wrote files. This one adds
# the instruments that make file handling PRECISE -- knowing
# where the cursor is and putting it where you want:
#
#   f.tell()      where is the cursor right now?
#   f.seek(n)     move the cursor to position n (0 = start)
#
# Plus the transcript's other half: deleting files with
# os.remove(), and the observation that the os module handles
# operating systems, folders, and files with zero packages to
# install.
#
# A note on "bytes": in BINARY mode ("rb") tell() is a true
# byte offset. In TEXT mode it is an opaque handle that seek()
# understands -- for pure-ASCII files (all of this lesson) the
# numbers happen to match byte counts, which is exactly what
# the transcript describes.
#
# HOW THIS LESSON RUNS SAFELY: same sandbox as lessons 65 to
# 67 -- temp folder, chdir in, try/finally, rmtree out. Only
# stable facts are printed, so the output is byte-identical on
# every run and on every machine.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

import os
import shutil
import tempfile

ORIGINAL_CWD = os.getcwd()
WORK_DIR = tempfile.mkdtemp(prefix="py68_")
FILE = "sample.txt"
CONTENT = "Hello World!\n"              # 13 ASCII characters

try:
    os.chdir(WORK_DIR)

    def read_text(name):
        """Whole file as one string, trailing blank lines trimmed."""
        reader = open(name, "r", encoding="utf-8")
        text = reader.read()
        reader.close()
        return text.strip()

    # NEWLINE NOTE: every file in this lesson is created with
    # newline="" so each "\n" lands on disk as ONE byte. The
    # default text-mode translation would write "\r\n" on
    # Windows (14 bytes for a 13-character string) and tell()
    # would report the raw byte count -- correct per the
    # transcript, but different across operating systems.
    # newline="" pins the byte math to the simple version:
    # 13 characters, 13 bytes, tell() == len(read()).

    f = open(FILE, "w", encoding="utf-8", newline="")
    f.write(CONTENT)
    f.close()

    # ============================================================
    # [1] tell(): where is the cursor right now?
    # ============================================================
    # A fresh file starts at position 0. Reading moves the
    # cursor forward; tell() reports where it stands:

    f = open(FILE)
    start = f.tell()
    all_text = f.read()
    end = f.tell()
    f.close()
    print(f"  tell at start: {start}")
    print(f"  tell after full read: {end}")
    print(f"  characters read: {len(all_text)}")
    #   tell at start: 0
    #   tell after full read: 13
    #   characters read: 13

    # 0 -> 13, and the file has 13 characters ("Hello World!"
    # plus its newline). The cursor sits just past the last
    # character the read consumed -- which is why lesson 66's
    # second read() returned '': there was nothing after it.

    # ============================================================
    # [2] read(size) with tell(): watch the position climb
    # ============================================================
    # The transcript's [00:29]: bite the file in pieces and
    # check the cursor after every bite:

    f = open(FILE)
    c1 = f.read(5)
    t1 = f.tell()
    c2 = f.read(5)
    t2 = f.tell()
    c3 = f.read()
    t3 = f.tell()
    f.close()
    print(f"  chunk {c1!r} -> tell {t1}")
    print(f"  chunk {c2!r} -> tell {t2}")
    print(f"  chunk {c3!r} -> tell {t3}")
    #   chunk 'Hello' -> tell 5
    #   chunk ' Worl' -> tell 10
    #   chunk 'd!\n' -> tell 13

    # Each read() advanced the cursor by exactly the number of
    # characters it returned: 5, then 10, then the end. The
    # chunks glue back into the whole file -- tell() is the
    # running total.

    # ============================================================
    # [3] seek(0): rewind, and the empty read gets a second life
    # ============================================================
    # The transcript's [02:21]. Lesson 66 showed that reading
    # twice returns '' -- because the cursor stayed at the end.
    # seek(0) sends it home:

    f = open(FILE)
    f.read()                             # exhaust the file
    again = f.read()
    print(f"  second read without seek: {again!r}")
    f.seek(0)                            # rewind!
    rewound = f.read()
    print(f"  after seek(0): {rewound!r}")
    f.close()
    #   second read without seek: ''
    #   after seek(0): 'Hello World!\n'

    # Same open file, same methods -- the only new power is
    # control of the cursor. seek(0) is the "read it again"
    # button; no reopen required.

    # ============================================================
    # [4] seek(offset): start reading from the middle
    # ============================================================
    # seek() takes any position, not just 0. Position 6 is
    # where "World!" begins ("Hello " is six characters):

    f = open(FILE)
    f.seek(6)
    from_middle = f.read()
    f.close()
    print(f"  seek(6) then read: {from_middle!r}")
    #   seek(6) then read: 'World!\n'

    # One seek, one read, and the first six characters were
    # never touched -- random access instead of sequential.
    # That is what makes index files, fixed-width records, and
    # "jump to line N" tools possible.

    # ============================================================
    # [5] seek + write: edit a file in place (r+ mode)
    # ============================================================
    # The transcript says seek serves "القراءة أو الكتابة" --
    # reading OR writing. Mode r+ opens one file for both; a
    # seek then decides where the write lands. Replace one word
    # with another of the SAME length -- nothing else moves:

    f = open("word.txt", "w", encoding="utf-8", newline="")
    f.write("hello world\n")
    f.close()

    f = open("word.txt", "r+", encoding="utf-8")   # read + write
    f.seek(6)                                      # "world" starts here
    f.write("there")
    f.seek(0)                                      # look at the result
    print(f"  in-place edit: {f.read().strip()!r}")
    f.close()
    #   in-place edit: 'hello there'

    # seek(6) put the write cursor on "world"; "there" (five
    # characters) replaced it exactly; seek(0) + read() proved
    # it. Writing the same number of characters keeps every
    # later byte where it was -- the cheapest kind of edit there
    # is.

    # ============================================================
    # [6] Deleting files: os.remove()
    # ============================================================
    # The transcript's [03:28]. The file goes away -- really
    # away, no recycle bin in between:

    doomed = "doomed.txt"
    f = open(doomed, "w", encoding="utf-8", newline="")
    f.write("delete me")
    f.close()
    print(f"  exists: {os.path.exists(doomed)}")
    os.remove(doomed)                                   # gone
    print(f"  after os.remove: {os.path.exists(doomed)}")
    #   exists: True
    #   after os.remove: False

    # os.remove takes a path (relative or absolute) and deletes
    # the FILE at that path. It does not ask twice, and it does
    # not work on folders (those need shutil.rmtree -- our
    # sandbox cleanup uses exactly that).

    # ============================================================
    # [7] Removing what is not there: FileNotFoundError
    # ============================================================
    # A missing file is an error, not a silent success:

    try:
        os.remove("never-existed.txt")
    except FileNotFoundError as error:
        print(f"  removing missing -> {type(error).__name__}")
    #   removing missing -> FileNotFoundError

    # Same error as opening a missing file with mode r (lesson
    # 65) -- os.remove does not pretend it succeeded. If
    # "might already be gone" is a normal case, wrap the
    # remove in os.path.exists() or catch the error.

    # ============================================================
    # [8] The os module: folders and renames, no packages
    # ============================================================
    # The transcript's [04:11]: os handles the operating
    # system, folders, and files -- all of it already in the
    # standard library. Two more powers worth having:

    os.makedirs("deep/nested/folder")
    print(f"  makedirs created: {os.path.isdir('deep/nested/folder')}")

    f = open("before-rename.txt", "w", encoding="utf-8", newline="")
    f.write("content travels")
    f.close()
    os.rename("before-rename.txt", "after-rename.txt")
    print(f"  old name gone: {not os.path.exists('before-rename.txt')}")
    print(f"  new name there: {os.path.exists('after-rename.txt')}")
    print(f"  content kept: {read_text('after-rename.txt')!r}")
    #   makedirs created: True
    #   old name gone: True
    #   new name there: True
    #   content kept: 'content travels'

    # makedirs built three nested folders in one call (mkdir
    # only makes one level); rename moved the file under a new
    # name with its content untouched. os.remove, os.rename,
    # os.makedirs, os.listdir, os.path.* -- one import, the
    # whole filesystem.

    # ============================================================
    # [9] The cursor dance: half, rewind, whole, tail
    # ============================================================
    # tell() and seek() together, the way real code uses them:

    f = open(FILE)
    first_half = f.read(6)
    pos = f.tell()
    f.seek(0)
    whole = f.read()
    f.seek(6)
    second_half = f.read()
    f.close()
    print(f"  first 6: {first_half!r} at pos {pos}")
    print(f"  whole: {whole!r}")
    print(f"  from 6: {second_half!r}")
    print(f"  parts join to whole: {first_half + second_half == whole}")
    #   first 6: 'Hello ' at pos 6
    #   whole: 'Hello World!\n'
    #   from 6: 'World!\n'
    #   parts join to whole: True

    # Read the head, jump home, read everything, jump to the
    # middle, read the tail -- and the two pieces prove they
    # reconstruct the whole. Cursor control, verified.

    # ============================================================
    # [10] In practice: create files, then delete every one
    # ============================================================
    # os.remove's real job -- batch cleanup. A scratch folder,
    # three files, then nothing:

    os.mkdir("scratch")
    os.chdir("scratch")
    for name in ("one.txt", "two.txt", "three.txt"):
        f = open(name, "w", encoding="utf-8", newline="")
        f.write("temp")
        f.close()
    print(f"  created: {sorted(os.listdir())}")

    for name in ("one.txt", "two.txt", "three.txt"):
        os.remove(name)
    print(f"  after removing all: {sorted(os.listdir())}")
    os.chdir("..")
    #   created: ['one.txt', 'three.txt', 'two.txt']
    #   after removing all: []

    # Listdir sorted (lesson 65's habit) showed the three
    # names; after three removes it shows an empty list -- the
    # folder itself survives, its contents do not. This is the
    # shape of every "clear the output directory" script you
    # will ever write.

    # ============================================================
    # [11] Binary mode: tell() as a true byte offset
    # ============================================================
    # The transcript's "بالبايتس" is exact in binary mode --
    # "rb" reads raw bytes, and tell() counts them:

    f = open(FILE, "rb")                    # binary: no encoding
    first = f.read(3)
    position = f.tell()
    f.seek(0)
    again = f.read(3)
    f.close()
    print(f"  binary read(3): {first!r}")
    print(f"  tell in binary: {position}")
    print(f"  seek(0) read(3): {again!r}")
    #   binary read(3): b'Hel'
    #   tell in binary: 3
    #   seek(0) read(3): b'Hel'

    # b'Hel' -- three raw bytes, and tell() says 3, no
    # interpretation at all. In text mode the same numbers
    # appear for ASCII files, but only binary mode PROMISES
    # byte counting. When the exact bytes matter, open "rb".

    # ============================================================
    # [12] One session, then guaranteed cleanup
    # ============================================================
    # Everything combined: write, track, rewind, read lines,
    # delete, and let the sandbox go:

    f = open("session.txt", "w", encoding="utf-8", newline="")
    f.write("alpha\n")
    f.write("beta\n")
    f.close()

    f = open("session.txt")
    f.readline()                           # consume line one
    mid = f.tell()
    f.seek(0)                              # rewind
    lines = f.readlines()
    f.close()
    print(f"  after one readline, tell: {mid}")
    print(f"  rewound lines: {lines}")

    os.remove("session.txt")
    print(f"  session removed: {not os.path.exists('session.txt')}")
    #   after one readline, tell: 6
    #   rewound lines: ['alpha\n', 'beta\n']
    #   session removed: True

    # readline() moved the cursor past "alpha\n" (six
    # characters -- tell agrees), seek(0) restored the start,
    # readlines() got both lines, and os.remove erased the
    # evidence. The sandbox erases the rest:

finally:
    os.chdir(ORIGINAL_CWD)
    shutil.rmtree(WORK_DIR, ignore_errors=True)

print(f"  work folder removed: {not os.path.exists(WORK_DIR)}")
#   work folder removed: True

# ============================================================
# [13] The summary
# ============================================================
# The precision tools, complete:
#
#   1. f.tell() -- the cursor's current position; 0 at a fresh
#      open, the file's length after reading it all; in binary
#      mode it is a true byte offset, in text mode an opaque
#      handle that seek() understands (identical numbers for
#      ASCII)
#   2. read(size) + tell() -- each read advances the cursor by
#      the characters it returned; tell() is the running total
#   3. f.seek(0) -- rewind: the same open file becomes
#      readable again (fixes lesson 66's '' second read)
#   4. f.seek(n) -- jump anywhere: seek(6) started the next
#      read exactly at "World!" -- random access, not just
#      sequential
#   5. seek + WRITE -- mode r+ opens for reading AND writing;
#      seek(6) + write("there") changed "hello world" into
#      "hello there" in place, same-length replacement
#   6. os.remove(path) -- deletes one FILE, for real;
#      FileNotFoundError if it is not there; folders need
#      shutil.rmtree instead
#   7. os POWERS, NO PACKAGES -- makedirs (nested folders in
#      one call), rename (new name, same content), remove,
#      listdir, exists, isdir: one import covers the
#      filesystem
#   8. THE PRACTICE -- create three files, remove three files,
#      listdir shows []: cleanup scripts are just loops over
#      os.remove
#
# The transcript's four parts now sit together: positions you
# can read (tell), positions you can set (seek), files you can
# delete (os.remove), and a standard library that needs no
# installation for any of it. File handling's foundation is
# complete; the next lessons build structure on top of it.
