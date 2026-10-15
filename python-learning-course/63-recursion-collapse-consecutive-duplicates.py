# -----------------------------------------------------------------
# Lesson 63: recursion (a function that calls itself)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : base case + smaller step, a practical example
#            (collapse consecutive duplicate letters), tracing
#            prints, missing base case -> RecursionError,
#            call counting with global (lesson 62)
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# Recursion is one of the ideas that separates people who can
# read code from people who can write it: a function that calls
# ITSELF to do the same job on a smaller piece of the input,
# until the piece is small enough to answer directly.
#
# The two ingredients, always the same two:
#
#   base case       -- "when the input is this small, answer
#                      immediately, no more calls"
#   smaller step    -- "otherwise, do one slice of the work and
#                      hand the REST to myself"
#
# The transcript deliberately avoids the usual factorial demo
# and builds a practical tool instead: a function that removes
# consecutive duplicate letters -- WWWOORLLD becomes WORLD.
# The tracing prints in section 7 exist for one reason: to watch
# every call and every return exactly as the transcript asks, so
# you understand each line rather than memorize it.
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] The shape of recursion, in the smallest possible example
# ============================================================
# Before the real tool: what does a self-call LOOK like? Here is
# a function that counts down by calling itself one smaller each
# time -- base case first, smaller step second:

def echo_back(n):
    if n == 0:                      # base case: stop here
        print("  done")
        return
    print(f"  tick {n}")            # one slice of the work
    echo_back(n - 1)                # hand a SMALLER job to myself

echo_back(3)
#   tick 3
#   tick 2
#   tick 1
#   done

# Read the order: three self-calls opened, then the base case
# answered, then each call finished. The line `echo_back(n - 1)`
# is inside echo_back -- that is the whole trick. If the base
# case were missing, the calls would open forever (section 9
# shows exactly what Python says then).

# ============================================================
# [2] The practical problem: collapse consecutive duplicates
# ============================================================
# The transcript's example. The job: a word arrives with runs of
# repeated letters; the answer keeps ONE letter of each run and
# drops the rest. These are the targets this lesson builds to:

targets = [
    ("WWWOORLLD", "WORLD"),
    ("hellooo", "helo"),
    ("aaabbbccc", "abc"),
    ("aabc", "abc"),
]
for raw, expected in targets:
    print(f"  {raw:<10} -> {expected}")
#   WWWOORLLD  -> WORLD
#   hellooo    -> helo
#   aaabbbccc  -> abc
#   aabc       -> abc

# Note what the job is NOT: it does not remove every repeated
# letter, only ADJACENT ones. "aabc" loses the first extra a
# (they touch) and keeps every other letter. That distinction --
# "compare each letter with its RIGHT NEIGHBOR" -- is exactly
# what a recursive step over word[0] and word[1] does naturally.

# ============================================================
# [3] Ingredient one: the base case (written first, as in class)
# ============================================================
# The transcript writes the stop condition before anything else:
# if the word is one character long, it is already clean --
# return it and call nobody:

def squeeze(word):
    # The lecture's line is exactly:
    #     if len(word) == 1: return word
    # We write <= 1 so an empty string also returns safely. The
    # recursion itself never produces "" -- only a caller can
    # pass one.
    if len(word) <= 1:
        return word
    # the recursive branches arrive in the next section

print(f"  one char -> {squeeze('w')!r}")
print(f"  empty    -> {squeeze('')!r}")
#   one char -> 'w'
#   empty    -> ''

# The base case is the promise that makes recursion safe: the
# smallest inputs get answered with NO further call. Everything
# else in the function will be built to shrink the input toward
# this condition.

# ============================================================
# [4] Ingredient two: compare, then hand the rest to myself
# ============================================================
# Now the full function. Two branches after the base case --
# one for "these two letters are the same", one for "they are
# different":

def squeeze(word):                    # same name: Python just
    if len(word) <= 1:                # replaced the binding
        return word                   # (lesson 56 / lesson 62)
    if word[0] == word[1]:            # a duplicate at the front
        return squeeze(word[1:])      # drop one of the pair
    return word[0] + squeeze(word[1:])  # keep it, move on

# Branch by branch:
#
#   word[0] == word[1]  -- e.g. "WW..." The two letters are
#      identical, so ONE of them must disappear. Recursing on
#      word[1:] keeps the second and drops the first -- since
#      they are the same letter, "skipping the duplicate" is
#      exactly what that is.
#
#   otherwise           -- e.g. "WO...". The first letter is
#      finished: nothing ahead can merge with it. Keep it with
#      + and let the recursion handle the rest.
#
# Both branches recurse on a word that is exactly ONE character
# shorter, so the base case is always reached -- that is the
# "smaller step" requirement, satisfied by construction.

# ============================================================
# [5] The results
# ============================================================
# The targets from section 2, plus the two edges (no duplicates,
# single letter):

for word in ["WWWOORLLD", "hellooo", "aaabbbccc", "aabc", "world", "a"]:
    print(f"  {word:<10} -> {squeeze(word)}")
#   WWWOORLLD  -> WORLD
#   hellooo    -> helo
#   aaabbbccc  -> abc
#   aabc       -> abc
#   world      -> world
#   a          -> a

# Every target hits. "world" comes back untouched because every
# adjacent pair differs, so the function just walks down the
# letters one call at a time -- recursion used as a scanner, not
# only as a reducer.

# ============================================================
# [6] The hand walkthrough: every call of WWWOORLLD
# ============================================================
# The transcript's point at the end: understand every call, not
# just the code. Here is what really happens, call by call --
# the calls go DOWN first:
#
#   call 1  squeeze("WWWOORLLD")  W==W -> drop one W, recurse
#   call 2  squeeze("WWOORLLD")   W==W -> drop one W, recurse
#   call 3  squeeze("WOORLLD")    W!=O -> keep W,  recurse
#   call 4  squeeze("OORLLD")     O==O -> drop one O, recurse
#   call 5  squeeze("ORLLD")      O!=R -> keep O,  recurse
#   call 6  squeeze("RLLD")       R!=L -> keep R,  recurse
#   call 7  squeeze("LLD")        L==L -> drop one L, recurse
#   call 8  squeeze("LD")         L!=D -> keep L,  recurse
#   call 9  squeeze("D")          base case -> returns "D"
#
# then the answers climb back UP, one return per frame:
#
#   call 8  'L' + "D"   = "LD"
#   call 7  dropped L   -> "LD"
#   call 6  'R' + "LD"  = "RLD"
#   call 5  'O' + "RLD" = "ORLD"
#   call 4  dropped O   -> "ORLD"
#   call 3  'W' + "ORLD"= "WORLD"
#   call 2  dropped W   -> "WORLD"
#   call 1  dropped W   -> "WORLD"
#
# Nine characters, nine calls, nine returns. Every line of the
# function ran exactly as written -- nothing was magic, and the
# + operators all executed on the way back up, which is why the
# answer assembles itself in reverse order of the calls.

# ============================================================
# [7] Tracing prints: watch it move, as in the lecture
# ============================================================
# The transcript adds print statements inside the function so
# the data flow is visible "behind the scenes". This is the same
# algorithm with an entry print and an exit print per branch:

def squeeze_traced(word):
    print(f"  -> call   {word!r}")
    if len(word) <= 1:
        print(f"  == base   {word!r}")
        return word
    if word[0] == word[1]:
        result = squeeze_traced(word[1:])
        print(f"  <- skip   drop {word[0]!r}, answer {result!r}")
        return result
    result = squeeze_traced(word[1:])
    print(f"  <- keep   {word[0]!r} + {result!r} = {word[0] + result!r}")
    return word[0] + result

answer = squeeze_traced("woorld")
#   -> call   'woorld'
#   -> call   'oorld'
#   -> call   'orld'
#   -> call   'rld'
#   -> call   'ld'
#   -> call   'd'
#   == base   'd'
#   <- keep   'l' + 'd' = 'ld'
#   <- keep   'r' + 'ld' = 'rld'
#   <- keep   'o' + 'rld' = 'orld'
#   <- skip   drop 'o', answer 'orld'
#   <- keep   'w' + 'orld' = 'world'

# Six calls down, six lines up. The arrows tell you which half
# of the story you are reading: -> is a call opening, <- is a
# call returning its answer to its caller.

# ============================================================
# [8] Reading the trace: what it proves
# ============================================================
# Look at the trace from section 7 in order and three facts jump
# out -- these are the "behind the scenes" facts the transcript
# wants internalized:

print(f"  final answer: {answer}")
#   final answer: world

# 1. THE CALLS DESCEND BY ONE LETTER EACH LINE.
#    'woorld' -> 'oorld' -> 'orld' -> 'rld' -> 'ld' -> 'd'.
#    Every arrow line is one character shorter than the one
#    above it -- that IS the smaller step, visible.
#
# 2. THE BASE CASE FIRES EXACTLY ONCE, AT THE BOTTOM.
#    The == line appears a single time, when len(word) is 1.
#    One stop for six calls: the promise from section 3 kept.
#
# 3. THE ANSWERS ASSEMBLE ON THE WAY UP.
#    'd' exists first, then 'ld', 'rld', 'orld', and finally
#    'world'. Each <- line shows one frame adding (or dropping)
#    its own letter and handing the result to the frame above.
#    The final print matches the last <- line, character for
#    character -- nothing else could have produced it.

# ============================================================
# [9] No base case -> RecursionError
# ============================================================
# The failure mode, worth seeing exactly once. A self-call that
# never shrinks the input (or has no stop condition) opens frames
# forever, and Python stops it at its recursion limit:

def runaway(n):
    return runaway(n + 1)            # never smaller, never stops

try:
    runaway(0)
except RecursionError as error:
    print("no base case ->", type(error).__name__)
# no base case -> RecursionError

# RecursionError is a subclass of RuntimeError, raised before
# the machine runs out of real memory. It is the interpreter
# saying "these calls will never come back." Both halves of the
# recipe are load-bearing: the base case stops the descent, and
# the smaller step GUARANTEES you reach it. squeeze() has both,
# so its depth is never a surprise (next section proves the
# exact bound).

# ============================================================
# [10] Edge cases, one line each
# ============================================================
# The corners of the contract -- each answer is what a careful
# reader predicts:

print(f"  {''!r:8} -> {squeeze('')!r}")
print(f"  {'q'!r:8} -> {squeeze('q')!r}")
print(f"  {'aaaa'!r:8} -> {squeeze('aaaa')!r}")
print(f"  {'abc'!r:8} -> {squeeze('abc')!r}")
print(f"  {'aabbcc'!r:8} -> {squeeze('aabbcc')!r}")
#   ''       -> ''
#   'q'      -> 'q'
#   'aaaa'   -> 'a'
#   'abc'    -> 'abc'
#   'aabbcc' -> 'abc'

# Empty in, empty out (the <= 1 guard); a single letter is its
# own answer; four identical letters collapse to one; untouched
# letters pass through; and a run of pairs collapses cleanly.
# An edge case is not a special favor -- it is the base case
# doing its normal job.

# ============================================================
# [11] Counting the calls: recursion depth is measurable
# ============================================================
# Lesson 62's global keyword, used as an instrument. How many
# calls does squeeze actually make? Count them:

calls_seen = 0

def squeeze_counted(word):
    global calls_seen                # announce the shared counter
    calls_seen += 1
    if len(word) <= 1:
        return word
    if word[0] == word[1]:
        return squeeze_counted(word[1:])
    return word[0] + squeeze_counted(word[1:])

squeeze_counted("world")
print(f"  {'world'!r:10} -> {calls_seen} calls")
calls_seen = 0
squeeze_counted("WWWOORLLD")
print(f"  {'WWWOORLLD'!r:10} -> {calls_seen} calls")
calls_seen = 0
squeeze_counted("a")
print(f"  {'a'!r:10} -> {calls_seen} calls")
#   'world'    -> 5 calls
#   'WWWOORLLD' -> 9 calls
#   'a'        -> 1 calls

# The pattern: every call removes exactly one character, so the
# number of calls EQUALS the length of the word. That is the
# depth bound promised in section 9 -- recursion depth here is
# tied to the input size, not to anything infinite. A 5-letter
# word opens 5 frames; a 9-letter word opens 9. (The last line
# says "1 calls" because the label is mechanical -- one frame
# is the base case itself.)

# ============================================================
# [12] In practice: cleaning stuttered text
# ============================================================
# The tool, doing the job it was designed for -- a line of text
# with keyboard-stutter typos, cleaned word by word:

messy = ["heyyyyyy", "weeeeelcome", "niice", "yeeees", "goooood"]
print(f"  messy:   {' '.join(messy)}")
cleaned = [squeeze(word) for word in messy]
print(f"  cleaned: {' '.join(cleaned)}")
#   messy:   heyyyyyy weeeeelcome niice yeeees goooood
#   cleaned: hey welcome nice yes god

# One squeeze per word inside a list comprehension (lesson 25's
# pattern), then join the results back into a sentence. The
# function never knew what a "typo" was -- it only ever looked
# at a letter and its neighbor, which is exactly why it composes
# into anything.

# ============================================================
# [13] The summary
# ============================================================
# Recursion, complete:
#
#   1. DEFINITION -- a function that calls itself, each time on
#      a SMALLER piece of the same problem
#   2. TWO INGREDIENTS, both required: a base case (answer the
#      smallest input directly) and a smaller step (shrink the
#      input every call so the base case is reached)
#   3. THE PRACTICAL EXAMPLE -- squeeze(word):
#        len(word) <= 1       -> return it (base case)
#        word[0] == word[1]   -> squeeze(word[1:]) drops one
#                                of the duplicate pair
#        otherwise            -> word[0] + squeeze(word[1:])
#                                keeps the letter and moves on
#   4. THE FLOW -- calls descend one character at a time, the
#      base case fires once at the bottom, and the + operators
#      assemble the answer on the way back up
#   5. TRACING PRINTS -- an entry line and an exit line per
#      branch turn invisible frames into readable output; this
#      is how you study code instead of memorizing it
#   6. THE FAILURE MODE -- no base case (or no shrinking) ends
#      in RecursionError at the recursion limit
#   7. THE BOUND -- here every call drops one character, so
#      depth == len(word), which a global counter (lesson 62)
#      proves in three lines
#   8. COMPOSITION -- one letter-and-neighbor rule cleaned a
#      whole sentence of stuttered text, because a correct
#      small function is a correct part of any larger one
#
# The transcript's closing advice is the real lesson: reading a
# recursive function line by line -- knowing which call opened,
# which returned, and why -- is the difference between having
# memorized the code and being an engineer who understands it.
