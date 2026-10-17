# -----------------------------------------------------------------
# Lesson 66: file reading -- read(), readline(), readlines()
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : the file object (print, .name, .mode, .encoding),
#            read() and read(size), the cursor and the empty
#            second read, readline() / readline(size),
#            readlines() -> list, for line in file,
#            startswith() + break, close() as best practice
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lesson 65 opened files and switched modes. This lesson stays
# inside MODE r and asks the real question: HOW do you pull text
# out of a file? The transcript introduces the family, one
# method at a time:
#
#   read()        whole file as one string (or read(size) chars)
#   readline()    one line per call (or readline(size) chars)
#   readlines()   every line as a LIST of strings
#   for line in f the same lines, streamed -- no big list
#
# Plus the file object itself: print(f) shows an OBJECT, not
# the text; f.name / f.mode / f.encoding describe it; and
# f.close() ends the story (using a closed file raises).
#
# HOW THIS LESSON RUNS SAFELY: same sandbox as lesson 65 --
# temp folder, chdir in, try/finally, rmtree out. Only stable
# facts are printed (contents, counts, attributes, booleans),
# so the output is byte-identical on every run and machine.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

import os
import shutil
import tempfile

ORIGINAL_CWD = os.getcwd()
WORK_DIR = tempfile.mkdtemp(prefix="py66_")
FILE = "shapes.txt"
CONTENT = "red square\ngreen circle\nblue triangle\nred circle\n"

try:
    os.chdir(WORK_DIR)

    # ============================================================
    # [1] A file object in a variable: my_file = open(...)
    # ============================================================
    # The transcript's opening move. Make the sample file with
    # w first (lesson 65), then open it for reading -- note that
    # MODE r is the default when you pass nothing:

    f = open(FILE, "w", encoding="utf-8")
    f.write(CONTENT)
    f.close()

    my_file = open(FILE)                 # no mode given: r is default
    print(f"  default mode is r: {my_file.mode == 'r'}")
    my_file.close()
    #   default mode is r: True

    # open() returned an OBJECT -- a live connection to the
    # file on disk -- and we put it in a variable. Everything
    # in this lesson happens through that object.

    # ============================================================
    # [2] print(the object) shows the OBJECT, not the text
    # ============================================================
    # The transcript's first trap at [00:50]: print(my_file)
    # does NOT dump the file's contents -- it shows what the
    # object IS:

    f = open(FILE, encoding="utf-8")
    print(f"  object: {f}")
    f.close()
    #   object: <_io.TextIOWrapper name='shapes.txt' mode='r' encoding='utf-8'>

    # Read the parts: TextIOWrapper is the object type (a text
    # stream wrapping the raw file), name='shapes.txt' is the
    # file it holds, mode='r' is how it was opened, encoding is
    # the text encoding. No file CONTENT appears anywhere --
    # contents only come from the reading methods below.

    # ============================================================
    # [3] The file object's basic attributes
    # ============================================================
    # The transcript's [01:13]: three properties that describe
    # the connection without reading a single byte:

    f = open(FILE, encoding="utf-8")
    print(f"  name: {f.name}")
    print(f"  mode: {f.mode}")
    print(f"  encoding: {f.encoding}")
    f.close()
    #   name: shapes.txt
    #   mode: r
    #   encoding: utf-8

    # name is the path you passed in (here, just the filename);
    # mode is the one-letter (or longer) mode string; encoding
    # is what we asked for. Handy for logging "which file am I
    # in?" without touching the data.

    # ============================================================
    # [4] read(): the whole file -- and the cursor behind it
    # ============================================================
    # read() with no argument returns EVERYTHING as one string.
    # Then the transcript's favorite demonstration of how
    # reading works: call read() a second time on the same open
    # file and you get '' -- a "cursor" sits at the end after
    # the first read, and there is nothing left:

    f = open(FILE)
    whole = f.read()
    print(f"  whole file: {whole!r}")
    again = f.read()
    print(f"  second read: {again!r}")
    f.close()
    #   whole file: 'red square\ngreen circle\nblue triangle\nred circle\n'
    #   second read: ''

    # One string, newlines and all (shown with !r so you can
    # SEE them as \n). The empty second read is not a bug --
    # it is the file position. Every open() starts a fresh
    # cursor at the beginning, which is why each section here
    # reopens the file.

    # ============================================================
    # [5] read(size): take a bite, not the meal
    # ============================================================
    # The transcript's [01:36]: pass a number and read() stops
    # after that many CHARACTERS, leaving the cursor where it
    # stopped:

    f = open(FILE)
    chunk1 = f.read(10)
    chunk2 = f.read(10)
    chunk3 = f.read()                     # no number: the rest
    f.close()
    print(f"  chunk1: {chunk1!r}")
    print(f"  chunk2: {chunk2!r}")
    print(f"  chunk3: {chunk3!r}")
    #   chunk1: 'red square'
    #   chunk2: '\ngreen cir'
    #   chunk3: 'cle\nblue triangle\nred circle\n'

    # Ten, ten, then everything: the three chunks glue back
    # into the exact file text. chunk2 even STARTS with the
    # newline that ended line one -- characters do not care
    # about lines; that is what readline() is for.

    # ============================================================
    # [6] readline(): one line per call (or size chars of it)
    # ============================================================
    # The transcript's [02:03]. Each call returns the next line
    # INCLUDING its trailing newline; past the end, '' forever:

    f = open(FILE)
    line1 = f.readline()
    line2 = f.readline()
    line3 = f.readline()
    line4 = f.readline()
    line5 = f.readline()
    f.close()
    print(f"  line1: {line1!r}")
    print(f"  line2: {line2!r}")
    print(f"  line3: {line3!r}")
    print(f"  line4: {line4!r}")
    print(f"  line5: {line5!r}")
    #   line1: 'red square\n'
    #   line2: 'green circle\n'
    #   line3: 'blue triangle\n'
    #   line4: 'red circle\n'
    #   line5: ''

    # Four calls, four lines, one empty -- the same cursor
    # story as read(), stepped one LINE at a time. And the size
    # version cuts mid-line, exactly like read(size):

    f = open(FILE)
    partial = f.readline(4)
    rest_of_line = f.readline()
    f.close()
    print(f"  readline(4): {partial!r}")
    print(f"  then readline(): {rest_of_line!r}")
    #   readline(4): 'red '
    #   then readline(): 'square\n'

    # readline(4) took "red " (four characters); the next
    # readline() finished THAT line before moving on -- the
    # cursor remembers it was mid-line.

    # ============================================================
    # [7] readlines(): every line, as a list
    # ============================================================
    # The transcript's [03:06]: one call, a LIST of line
    # strings (newlines included), ready for a loop or index:

    f = open(FILE)
    all_lines = f.readlines()
    f.close()
    print(f"  count: {len(all_lines)}")
    print(f"  list: {all_lines}")
    #   count: 4
    #   list: ['red square\n', 'green circle\n', 'blue triangle\n', 'red circle\n']

    # A list is convenient -- len(), indexing, membership --
    # but it loads the WHOLE file into memory at once. For a
    # novel that is wasteful; for a database export it can be
    # fatal. The next method avoids exactly that.

    # ============================================================
    # [8] for line in my_file: the streaming loop
    # ============================================================
    # The transcript's [03:50]. A file object IS its own
    # iterator: one line at a time, nothing extra held in
    # memory:

    f = open(FILE)
    for line in f:
        print(f"  | {line.rstrip()}")
    f.close()
    #   | red square
    #   | green circle
    #   | blue triangle
    #   | red circle

    # Same four lines as readlines() -- rstrip() just drops the
    # trailing newline for printing. The difference is
    # mechanical: readlines() built a list first and THEN the
    # loop walked it; this loop received each line the moment
    # the file produced it. Big-file rule of thumb: prefer the
    # loop.

    # ============================================================
    # [9] startswith() + break: find a line, stop reading
    # ============================================================
    # The transcript's [04:24]: scan until you have what you
    # want, then break -- the file never has to finish:

    f = open(FILE)
    lines_read = 0
    for line in f:
        lines_read += 1
        if line.startswith("blue"):
            break
    f.close()
    print(f"  stopped on line: {lines_read}")
    print(f"  matched: {line.rstrip()}")
    #   stopped on line: 3
    #   matched: blue triangle

    # Three lines were pulled, not four -- the break cut the
    # scan short, which is the "توفير الموارد" (resource
    # saving) the transcript mentions. startswith() tested the
    # START of each line; line still holds the match because
    # loop variables survive their loop (lesson 25).

    # ============================================================
    # [10] close(): best practice, and what happens without it
    # ============================================================
    # The transcript's [04:52]. Every successful open() above
    # ended in close(); here is what that bought us -- the
    # object KNOWS it is closed, and reading it again is an
    # error instead of a mystery:

    f = open(FILE)
    f.close()
    print(f"  closed: {f.closed}")

    try:
        f.read()
    except ValueError as error:
        print(f"  read after close -> {type(error).__name__}")
    #   closed: True
    #   read after close -> ValueError

    # closed is a boolean flag on the object; ValueError
    # ("I/O operation on closed file") is Python refusing to
    # serve data from a connection you already tore down. An
    # UNclosed file is worse than a crash -- it holds system
    # resources until the program ends (and leaks them under
    # -W error or long-running servers). close() is not
    # optional hygiene; the with-statement form of the same
    # discipline arrives in the next lesson.

    # ============================================================
    # [11] Three methods, one answer
    # ============================================================
    # The same file read three ways -- whole-string + split,
    # readlines() + strip, and the for loop -- producing the
    # identical normalized list:

    f = open(FILE)
    style_a = f.read().splitlines()
    f.close()

    f = open(FILE)
    style_b = [item.strip() for item in f.readlines()]
    f.close()

    f = open(FILE)
    style_c = [item.rstrip() for item in f]
    f.close()

    print(f"  read+splitlines: {style_a}")
    print(f"  readlines strip: {style_b}")
    print(f"  for-loop rstrip: {style_c}")
    print(f"  all identical: {style_a == style_b == style_c}")
    #   read+splitlines: ['red square', 'green circle', 'blue triangle', 'red circle']
    #   readlines strip: ['red square', 'green circle', 'blue triangle', 'red circle']
    #   for-loop rstrip: ['red square', 'green circle', 'blue triangle', 'red circle']
    #   all identical: True

    # Three routes, one destination: choosing a method is about
    # MEMORY and CONTROL, not about getting different data.
    # splitlines() (lesson 22) cut on line boundaries; strip()
    # and rstrip() only trimmed the newline; the loop never
    # held more than one line.

    # ============================================================
    # [12] In practice: collect every match with its number
    # ============================================================
    # The for loop plus enumerate (lesson 26) plus startswith:
    # a tiny search tool -- which lines mention "red", and
    # where:

    f = open(FILE)
    hits = []
    for number, line in enumerate(f, start=1):
        if line.startswith("red"):
            hits.append(f"{number}: {line.rstrip()}")
    f.close()

    print("  red lines:")
    for hit in hits:
        print(f"    {hit}")
    #   red lines:
    #     1: red square
    #     4: red circle

    # Streaming iteration (never more than one line in memory),
    # line numbers from enumerate, matching from startswith,
    # results collected for later -- the whole lesson combined
    # into twelve lines that would work on a file a million
    # times larger.

finally:
    os.chdir(ORIGINAL_CWD)
    shutil.rmtree(WORK_DIR, ignore_errors=True)

print(f"  work folder removed: {not os.path.exists(WORK_DIR)}")
#   work folder removed: True

# ============================================================
# [13] The summary
# ============================================================
# File reading, as the transcript lays it out:
#
#   1. my_file = open(path) -- the call returns a FILE OBJECT
#      (a live connection), not the text; mode r is the default
#   2. print(object) shows <_io.TextIOWrapper name=... mode=...
#      encoding=...> -- the connection's identity, never its
#      contents
#   3. ATTRIBUTES -- f.name (what it is), f.mode (how it was
#      opened), f.encoding (how text is decoded)
#   4. read() -> the whole file as one string; read(size) ->
#      exactly that many characters; a cursor remembers the
#      position, so a second read() on the same open file
#      returns ''
#   5. readline() -> one line per call, newline included;
#      readline(size) -> that many chars of the current line;
#      past the end -> ''
#   6. readlines() -> a LIST of all lines -- indexable, but it
#      loads everything into memory
#   7. for line in my_file: -> the same lines, streamed one at
#      a time -- the right default for large files
#   8. startswith() + break -> stop the scan the moment the
#      target line appears; unread lines are never pulled
#   9. close() -> every open() gets one; f.closed confirms it;
#      using a closed file raises ValueError instead of
#      returning stale data
#  10. SAME DATA, ANY METHOD -- read().splitlines(),
#      readlines() + strip, and the for loop all produced one
#      identical list; pick by memory and control needs
#
# The transcript's arc is deliberate: object -> whole file ->
# pieces of the file -> lines -> lists -> streams -> early
# stop -> close. Next lesson picks up the hygiene form (with)
# and starts WRITING; the reading half of the toolkit is now
# complete.
