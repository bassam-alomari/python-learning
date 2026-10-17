# -----------------------------------------------------------------
# Lesson 67: file writing -- write() and writelines()
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : mode w (creates, ERASES) vs mode a (never erases),
#            write() and the newline you must add yourself,
#            writelines() adds no separators either,
#            the write cursor (w starts at 0, a starts at EOF),
#            write() returns the character count
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Lesson 66 read files; this one writes them. The transcript
# keeps it practical -- two modes, two methods, one cursor:
#
#   open(name, "w")   creates if missing, and ERASES old
#                     content first (the warning again, taken
#                     seriously)
#   open(name, "a")   creates if missing, appends at the END,
#                     never erases
#
#   f.write(text)         one string, as-is
#   f.writelines(list)    many strings, as-is, no separators
#
# The word as-is is the whole lesson: neither method adds
# newlines, spaces, or anything else -- what you hand them is
# what lands in the file, byte for byte. And behind both modes
# sits a write cursor that decides WHERE the next character
# goes: position 0 for w, the end of the file for a.
#
# HOW THIS LESSON RUNS SAFELY: same sandbox as lessons 65 and
# 66 -- temp folder, chdir in, try/finally, rmtree out. Only
# stable facts are printed, so the output is byte-identical on
# every run and on every machine.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

import os
import shutil
import tempfile

ORIGINAL_CWD = os.getcwd()
WORK_DIR = tempfile.mkdtemp(prefix="py67_")
FILE = "osama.txt"                     # the transcript's filename

try:
    os.chdir(WORK_DIR)

    def read_text(name):
        """Whole file as one string, trailing blank lines trimmed."""
        reader = open(name, "r", encoding="utf-8")
        text = reader.read()
        reader.close()
        return text.strip()

    # ============================================================
    # [1] Mode w: creates the file, first write()
    # ============================================================
    # The transcript's opening: open("osama.txt", "w") on a file
    # that does not exist yet -- Python creates it -- then
    # write() puts the text in:

    print(f"  existed before: {os.path.exists(FILE)}")
    #   existed before: False

    f = open(FILE, "w", encoding="utf-8")     # creates it
    f.write("Hello From Python")              # transcript's string
    f.close()
    print(f"  content: {read_text(FILE)}")
    #   content: Hello From Python

    # w answered the missing file by inventing it, and write()
    # put one string inside. No \n was needed here because the
    # file is meant to hold exactly that one line.

    # ============================================================
    # [2] The critical point: w ERASES what was there
    # ============================================================
    # The transcript's "نقطة بالغة الأهمية". Same file, opened
    # with w a second time -- watch the first string die:

    f = open(FILE, "w", encoding="utf-8")
    f.write("first version")
    f.close()

    f = open(FILE, "w", encoding="utf-8")     # second w
    f.write("second version")
    f.close()
    print(f"  after rewrite: {read_text(FILE)!r}")
    #   after rewrite: 'second version'

    # The file was NOT "updated" -- it was emptied and refilled.
    # w means "this file's content should become exactly what I
    # am about to write." When that is your intent (a regenerated
    # report), w is perfect; when it is not, w is how lines of
    # history disappear without an error.

    # ============================================================
    # [3] write() adds nothing -- not even newlines
    # ============================================================
    # The transcript's [03:25]: to get a new line you must
    # WRITE a new line. Three writes without \n glue into one
    # continuous string:

    f = open("lines.txt", "w", encoding="utf-8")
    f.write("one")
    f.write("two")
    f.write("three")
    f.close()
    print(f"  glued together: {read_text('lines.txt')!r}")
    #   glued together: 'onetwothree'

    # Now the same three writes with explicit newlines:

    f = open("lines.txt", "w", encoding="utf-8")
    f.write("one\n")
    f.write("two\n")
    f.write("three\n")
    f.close()
    print("  with \\n added:")
    print(read_text("lines.txt"))
    #   with \n added:
    # one
    # two
    # three

    # write() is not print() -- there is no automatic newline,
    # no separator, no formatting. The string you pass is the
    # bytes (well, characters) the file receives. That is
    # precision, and it is also the most common beginner
    # surprise in writing files.

    # ============================================================
    # [4] writelines(): a whole list in one call
    # ============================================================
    # The transcript's [02:48]: write a list of strings at once.
    # Same "as-is" contract as write() -- the list's strings
    # are concatenated with NOTHING between them, so each one
    # should carry its own \n:

    my_list = ["python\n", "is\n", "fun\n"]
    f = open("list.txt", "w", encoding="utf-8")
    f.writelines(my_list)
    f.close()
    print("  writelines with \\n:")
    print(read_text("list.txt"))
    #   writelines with \n:
    # python
    # is
    # fun

    # And the same call on a list WITHOUT newlines:

    f = open("list.txt", "w", encoding="utf-8")
    f.writelines(["python", "is", "fun"])
    f.close()
    print(f"  writelines without \\n: {read_text('list.txt')!r}")
    #   writelines without \n: 'pythonisfun'

    # writelines is not print(list) and not "write LINES" in
    # the automatic sense -- it is write-many, one string at a
    # time, buffered. The name promises lines; the contract
    # delivers only what you prepared.

    # ============================================================
    # [5] Mode a: creates a missing file, like w does
    # ============================================================
    # Append mode answers a missing file the same way w does --
    # by creating it -- but with completely different manners
    # afterward:

    fresh = "journal.txt"
    print(f"  existed before: {os.path.exists(fresh)}")
    #   existed before: False

    f = open(fresh, "a", encoding="utf-8")    # creates it
    f.write("day one\n")
    f.close()
    print(f"  after first append: {read_text(fresh)!r}")
    #   after first append: 'day one'

    # Identical outcome to section 1 for this ONE write --
    # because there was nothing yet to preserve. The difference
    # shows up on the next open.

    # ============================================================
    # [6] Mode a: never erases -- it grows the file
    # ============================================================
    # Two more appends; every earlier line survives:

    f = open(fresh, "a", encoding="utf-8")
    f.write("day two\n")
    f.close()

    f = open(fresh, "a", encoding="utf-8")
    f.write("day three\n")
    f.close()

    print("  after more appends:")
    print(read_text(fresh))
    #   after more appends:
    # day one
    # day two
    # day three

    # Three opens, three writes, three lines. Where section 2's
    # second w left ONE version, section 6's appends left ALL
    # versions. That is the fundamental difference the
    # transcript builds the whole lesson around.

    # ============================================================
    # [7] The write cursor: a starts at the END, automatically
    # ============================================================
    # The transcript's [04:28]. Nobody called seek(); nobody
    # read anything first. The fourth append still landed AFTER
    # the third line, because mode a places the write cursor at
    # the end of the file the moment the file opens:

    f = open(fresh, "a", encoding="utf-8")
    f.write("day four\n")
    f.close()

    lines = read_text(fresh).splitlines()
    print(f"  line count: {len(lines)}")
    print(f"  last line: {lines[-1]}")
    #   line count: 4
    #   last line: day four

    # The new line is the LAST line -- the cursor started at
    # EOF (end of file). Mode w places the same cursor at
    # position 0 of a file it has just emptied -- which is why
    # w overwrites from the first character and a extends from
    # the last. Same write() call, two different destinations,
    # decided entirely by the mode letter.

    # ============================================================
    # [8] What write() gives back: the character count
    # ============================================================
    # A small fact with real uses (progress bars, logging,
    # knowing a write succeeded): write() RETURNS the number of
    # characters it wrote:

    f = open("count.txt", "w", encoding="utf-8")
    n1 = f.write("abc")
    n2 = f.write("\n")
    f.close()
    print(f"  write('abc') returned: {n1}")
    print(f"  write('\\n') returned: {n2}")
    #   write('abc') returned: 3
    #   write('\n') returned: 1

    # Two writes, two counts: three characters, then one. The
    # counts add up to the file's length -- nothing was lost,
    # and the file itself confirms it (next section's habit).

    # ============================================================
    # [9] Three styles, one identical file
    # ============================================================
    # Several write() calls, one write() with embedded \n, or
    # writelines() with a prepared list -- the content is
    # whatever the strings say, no matter how they arrived:

    f = open("styles.txt", "w", encoding="utf-8")
    f.write("alpha\n")
    f.write("beta\n")
    f.write("gamma\n")
    f.close()
    style_a = read_text("styles.txt")

    f = open("styles.txt", "w", encoding="utf-8")
    f.write("alpha\nbeta\ngamma\n")
    f.close()
    style_b = read_text("styles.txt")

    f = open("styles.txt", "w", encoding="utf-8")
    f.writelines(["alpha\n", "beta\n", "gamma\n"])
    f.close()
    style_c = read_text("styles.txt")

    print(f"  three writes: {style_a!r}")
    print(f"  one write:    {style_b!r}")
    print(f"  writelines:   {style_c!r}")
    print(f"  identical: {style_a == style_b == style_c}")
    #   three writes: 'alpha\nbeta\ngamma'
    #   one write:    'alpha\nbeta\ngamma'
    #   writelines:   'alpha\nbeta\ngamma'
    #   identical: True

    # Same result -- the methods differ in SHAPE (many calls vs
    # one string vs a list), not in what the file becomes.
    # Choose writelines() when you already hold a list; choose
    # repeated write() when lines are built as you go.

    # ============================================================
    # [10] In practice: a task file that can grow or restart
    # ============================================================
    # The workflow both modes exist for. Start a list with
    # writelines(), extend it with a, and -- when the day is
    # done -- wipe the slate with a single w:

    todo = "todo.txt"

    f = open(todo, "w", encoding="utf-8")     # fresh list
    f.writelines(["buy milk\n", "write lesson\n", "push repo\n"])
    f.close()

    f = open(todo, "a", encoding="utf-8")     # one more task
    f.write("answer messages\n")
    f.close()

    print("  todo after adding:")
    print(read_text(todo))
    #   todo after adding:
    # buy milk
    # write lesson
    # push repo
    # answer messages

    f = open(todo, "w", encoding="utf-8")     # new day: restart
    f.write("all tasks done\n")
    f.close()
    print(f"  regenerated: {read_text(todo)!r}")
    #   regenerated: 'all tasks done'

    # Four writes accumulated; one w replaced everything. Both
    # were correct because the file's PURPOSE changed between
    # the two operations -- growing list, then fresh state.

    # ============================================================
    # [11] The writing habit: read back and check
    # ============================================================
    # Writing is a claim; reading it back is the proof. The
    # lesson-66 toolkit verifies exactly what was written:

    f = open("check.txt", "w", encoding="utf-8")
    f.write("expected line\n")
    f.write("second expected\n")
    f.close()

    f = open("check.txt")
    lines = f.read().splitlines()
    f.close()
    print(f"  line count ok: {len(lines) == 2}")
    print(f"  first ok: {lines[0] == 'expected line'}")
    print(f"  last ok: {lines[1] == 'second expected'}")
    #   line count ok: True
    #   first ok: True
    #   last ok: True

    # Three booleans, no trust required. This pattern -- write,
    # close, reopen, compare -- is how the projects to come
    # test their own file handling without printing full
    # contents everywhere.

    # ============================================================
    # [12] One full session, then guaranteed cleanup
    # ============================================================
    # The transcript's file, both modes, both methods, end to
    # end:

    f = open(FILE, "w", encoding="utf-8")     # w: start over
    f.write("Hello From Python\n")
    f.close()

    f = open(FILE, "a", encoding="utf-8")     # a: extend safely
    f.write("append is safe\n")
    f.writelines(["writelines works\n", "lesson done\n"])
    f.close()

    print("  osama.txt final:")
    print(read_text(FILE))
    #   osama.txt final:
    # Hello From Python
    # append is safe
    # writelines works
    # lesson done

    # w set the opening line; a and writelines() added the
    # rest without touching it. Now the promise from the top:

finally:
    os.chdir(ORIGINAL_CWD)
    shutil.rmtree(WORK_DIR, ignore_errors=True)

print(f"  work folder removed: {not os.path.exists(WORK_DIR)}")
#   work folder removed: True

# ============================================================
# [13] The summary
# ============================================================
# File writing, as the transcript teaches it:
#
#   1. MODE w -- creates the file if missing, and ERASES all
#      old content first; the new write becomes the file's
#      entire content. Use it when a fresh file is the goal;
#      fear it when it is not (no warning is coming)
#   2. MODE a -- creates the file if missing, otherwise writes
#      at the END; old content always survives -- the log mode
#   3. f.write(text) -- puts ONE string in exactly as given;
#      write() is not print(): no automatic newline, no
#      separator; add "\n" yourself for each new line
#   4. f.writelines(list_of_strings) -- many strings in one
#      call, concatenated as-is; the list must carry its own
#      "\n" per line or the file gets one long line
#   5. THE WRITE CURSOR -- w starts at position 0 (of the
#      emptied file); a starts at EOF automatically (no seek
#      needed); that placement alone explains overwrite vs
#      append
#   6. write() RETURNS the number of characters written --
#      3 for "abc", 1 for "\n" -- a built-in success signal
#   7. SAME FILE, THREE SHAPES -- repeated write(), one big
#      write(), and writelines() produced byte-identical
#      content; pick by how the strings are produced
#   8. THE HABIT -- after writing, close, reopen, and verify
#      (line count, first line, last line): claims become
#      booleans
#
# With lessons 65 to 67 together, the core is complete: open()
# with the right mode, reading by every method, writing by both
# methods, and the cursor that decides where the next character
# lands. The remaining file lessons build on exactly this
# foundation -- safer patterns (with) and structured data.
