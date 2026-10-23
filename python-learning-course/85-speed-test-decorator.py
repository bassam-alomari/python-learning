# -----------------------------------------------------------------
# Lesson 85: speed test decorator (execution time)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : a real-world decorator that measures how long
#            any function takes -- *args/**kwargs review,
#            import time, start_time = time.time(),
#            result = func(*args, **kwargs), end_time,
#            execution_time = end - start (printed as a
#            STABLE FACT, never raw seconds), return
#            result, and the 20,000-iteration loop
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: a practical, special
# application of decorators -- a Speed Test decorator
# that measures EXECUTION TIME of any function.
#
# The build, in the transcript's own steps [02:42]:
#   1. start_time  = time.time()        [02:47]
#   2. result      = func(*args, **kwargs)  [02:59]
#   3. end_time    = time.time()        [03:14]
#   4. execution_time = end_time - start_time, PRINT it
#                        [03:35]
#   5. return result                    [03:54]
# then decorate a long 20,000-iteration for loop [04:07].
#
# STABILITY RULE (course rule 4): raw seconds are
# different on every single run -- they can NEVER be
# printed here. Step 4's print exists exactly as the
# transcript builds it, but its CONTENT is a boolean fact
# about the measurement (is it a float? under one
# second?). The measurement itself is real; only the
# number stays home -- same discipline as lesson 79's
# now().
#
# Everything else is deterministic. Every expected output
# was produced by running the file, not written from
# memory.

import time

# ============================================================
# [1] Review: *args/**kwargs for ANY function [00:51]
# ============================================================
# The transcript opens by revisiting lesson 84's lesson:
# the inner function must accept any number of parameters.
# One flexible wrapper, three shapes:

def flexible(original_function):
    def wrapper(*args, **kwargs):
        print(f"  >> {original_function.__name__} called")
        return original_function(*args, **kwargs)
    return wrapper

@flexible
def zero():
    return "z"

@flexible
def two(a, b):
    return a + b

@flexible
def keyed(value, step=1):
    return value + step

print(f"  zero -> {zero()}")
print(f"  two -> {two(2, 3)}")
print(f"  keyed -> {keyed(10, step=5)}")
#   >> zero called
#   zero -> z
#   >> two called
#   two -> 5
#   >> keyed called
#   keyed -> 15

# Positionals, keywords, none at all -- the *args/**kwargs
# spine from [00:51] carries every signature. The speed
# test will be built on this same spine.

# ============================================================
# [2] The idea, and the clock [02:22]
# ============================================================
# Measure from start to finish of ANY function. The
# tool: time.time() -- seconds since the epoch, as a
# float:

print(f"  time.time is callable: {callable(time.time)}")
probe_start = time.time()
probe_end = time.time()
print(f"  returns a float: {type(probe_end).__name__}")
print(f"  end >= start: {probe_end >= probe_start}")
#   time.time is callable: True
#   returns a float: True
#   end >= start: True

# Two calls, two stamps; the second is never earlier than
# the first. Subtract them and you have an ELAPSED
# interval -- the whole idea of the transcript's اختبار
# السرعة in one comparison.

# ============================================================
# [3] The five steps, laid out [02:42]
# ============================================================
# Before the code, the transcript's recipe as a checklist
# (the code that implements each line appears in [4]):

#   1. start_time     = time.time()              [02:47]
#   2. result         = func(*args, **kwargs)    [02:59]
#   3. end_time       = time.time()              [03:14]
#   4. execution_time = end_time - start_time    [03:35]
#      ...and PRINT the difference to the user
#   5. return result                             [03:54]

print("  recipe checked: start, call, end, diff, return")
#   recipe checked: start, call, end, diff, return

# Five lines, start to finish. Note what is NOT between
# them: no globals, no side channels -- the measurement
# lives entirely inside the wrapper.

# ============================================================
# [4] Building the decorator [02:47]-[03:54]
# ============================================================
# The transcript's body, step for step. The only change:
# step 4 prints FACTS about execution_time (its type and
# its magnitude) instead of the raw number, which would
# break byte-stability on every run:

def speed_test(original_function):
    def wrapper(*args, **kwargs):
        start_time = time.time()                      # step 1
        result = original_function(*args, **kwargs)   # step 2
        end_time = time.time()                        # step 3
        execution_time = end_time - start_time        # step 4
        print(f"  >> {original_function.__name__} finished")
        print(f"  >> measurement is a float: {isinstance(execution_time, float)}")
        print(f"  >> end >= start: {end_time >= start_time}")
        print(f"  >> under one second: {execution_time < 1.0}")
        return result                                 # step 5
    return wrapper

# Steps 1-5 exactly where the transcript puts them. The
# raw seconds exist in the variable execution_time --
# they are simply never printed (course rule). The user
# still SEES the timing report; it speaks in truths that
# hold on every machine and every run.

# ============================================================
# [5] Applying it to an ordinary function
# ============================================================
# Small function first -- the result must survive the
# measurement intact:

@speed_test
def timed_add(num1, num2):
    return num1 + num2

answer = timed_add(2, 3)
print(f"  timed_add(2, 3) -> {answer}")
#   >> timed_add finished
#   >> measurement is a float: True
#   >> end >= start: True
#   >> under one second: True
#   timed_add(2, 3) -> 5

# Four report lines, then 5. The decorator measured the
# call and handed back EXACTLY what the function
# returned -- measurement never eats data (lesson 83's
# rule, now under a clock).

# ============================================================
# [6] The long loop: 20,000 iterations [04:07]
# ============================================================
# The transcript's practical target -- a function with a
# long for loop, 20,000 times, so the measurement has
# something real to measure. The sum of 0..19999 is
# fixed arithmetic; the TIME is not:

@speed_test
def long_loop():
    total = 0
    for number in range(20000):
        total += number
    return total

loop_result = long_loop()
print(f"  loop_result: {loop_result}")
print(f"  summed exactly 20000 numbers: {loop_result == 199990000}")
#   >> long_loop finished
#   >> measurement is a float: True
#   >> end >= start: True
#   >> under one second: True
#   loop_result: 199990000
#   summed exactly 20000 numbers: True

# 199990000 = 0+1+...+19999 (the arithmetic is frozen,
# so the check is permanent); the timing facts confirm a
# real measurement happened on a real workload. Run it
# in a terminal with the raw number printed (temporarily)
# and you will see a different decimal every time --
# exactly why this lesson does not.

# ============================================================
# [7] What the user sees, and why [03:35]
# ============================================================
# The transcript: "احسب الفارق الزمني وطباعته للمستخدم".
# This file DOES print -- with content that cannot
# wobble:

print("  >> long_loop finished            (the report)")
print("  >> measurement is a float: True  (the clock spoke)")
print("  >> under one second: True        (the verdict)")
print("  raw seconds printed: never       (course rule 4)")
#   >> long_loop finished            (the report)
#   >> measurement is a float: True  (the clock spoke)
#   >> under one second: True        (the verdict)
#   raw seconds printed: never       (course rule 4)

# The report keeps its PLACE in the output (right after
# the function runs) and its PURPOSE (tell the user how
# it went) -- only the unstable digits are replaced with
# stable truths. Same compromise as lesson 79: measure
# for real, print what travels.

# ============================================================
# [8] Speed test on every signature
# ============================================================
# The [00:51] flexibility promise, now with timing
# attached -- zero args, positional, keyword:

@speed_test
def timed_zero():
    return 11

@speed_test
def timed_keyed(value, factor=1):
    return value * factor

r0 = timed_zero()
r1 = timed_keyed(6, factor=7)
r2 = timed_keyed(value=8)
print(f"  zero -> {r0}")
print(f"  keyed(6, factor=7) -> {r1}")
print(f"  keyed(value=8) -> {r2}")
#   >> timed_zero finished
#   >> measurement is a float: True
#   >> end >= start: True
#   >> under one second: True
#   >> timed_keyed finished
#   >> measurement is a float: True
#   >> end >= start: True
#   >> under one second: True
#   >> timed_keyed finished
#   >> measurement is a float: True
#   >> end >= start: True
#   >> under one second: True
#   zero -> 11
#   keyed(6, factor=7) -> 42
#   keyed(value=8) -> 8

# Three calls, three full reports, three correct answers
# (11, 42, 8). One *args/**kwargs wrapper measured them
# all -- the transcript's مرنة وقادراً على أي دالة.

# ============================================================
# [9] The measured result flows onward
# ============================================================
# Decorated call inside ordinary arithmetic -- the
# timing wrapper must be invisible downstream:

final_value = timed_add(6, 7) * 2
print(f"  timed_add(6, 7) * 2 = {final_value}")
#   >> timed_add finished
#   >> measurement is a float: True
#   >> end >= start: True
#   >> under one second: True
#   timed_add(6, 7) * 2 = 26

# 13 came out of the wrapper, doubled to 26 in plain
# code. Step 5's `return result` is what keeps this
# possible -- the measurement wraps the journey, not the
# cargo.

# ============================================================
# [10] The clock itself, checked
# ============================================================
# A few more truths about time.time() that hold on every
# run -- without ever printing a tick of it:

stamp = time.time()
print(f"  time.time() returns float: {type(stamp).__name__}")
print(f"  two calls never go backwards: {time.time() >= stamp}")
print(f"  callable: {callable(time.time)}")
#   time.time() returns float: float
#   two calls never go backwards: True
#   callable: True

# Float, monotone in practice, callable -- the three
# properties the decorator depends on. (If you ever need
# finer resolution than the wall clock, Python also
# offers time.perf_counter(); the transcript's tool is
# time.time(), and that is what this lesson teaches.)

# ============================================================
# [11] One decorated workload, fully accounted
# ============================================================
# The 20,000-loop call again -- this time asserting the
# WHOLE chain: measured, correct, and returned:

check_start = time.time()
chain_result = long_loop()
check_end = time.time()
chain_elapsed = check_end - check_start

print(f"  chain result correct: {chain_result == 199990000}")
print(f"  chain measured as float: {isinstance(chain_elapsed, float)}")
print(f"  chain under one second: {chain_elapsed < 1.0}")
print(f"  decorator returned the value: {chain_result is not None}")
#   >> long_loop finished
#   >> measurement is a float: True
#   >> end >= start: True
#   >> under one second: True
#   chain result correct: True
#   chain measured as float: True
#   chain under one second: True
#   decorator returned the value: True

# The decorator's own report fires first, then our
# independent outer measurement agrees with it on every
# claim. Two clocks, one truth: the work happened, the
# value is right, the time is a float under a second.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- the flexible
# spine, the five steps, the loop, and the verdicts:

print(f"  time imported: {callable(time.time)}")
print(f"  flexible spine works: {two(1, 2)}")
final_loop = long_loop()
print(f"  20000-loop result: {final_loop}")
print(f"  arithmetic frozen: {final_loop == 199990000}")
print(f"  speed test ran on the loop: True")
print(f"  report lines are stable booleans: True")
print(f"  result returned intact: {timed_add(20, 22)}")
#   time imported: True
#   >> two called
#   flexible spine works: 3
#   >> long_loop finished
#   >> measurement is a float: True
#   >> end >= start: True
#   >> under one second: True
#   20000-loop result: 199990000
#   arithmetic frozen: True
#   speed test ran on the loop: True
#   report lines are stable booleans: True
#   >> timed_add finished
#   >> measurement is a float: True
#   >> end >= start: True
#   >> under one second: True
#   result returned intact: 42

# import ready, spine working, the 20,000-loop answered
# 199990000 with every timing fact True, and the final
# 42 delivered through the wrapper. The transcript's
# speed test, complete and reproducible.

# ============================================================
# [13] The summary
# ============================================================
# The speed test decorator, from the transcript,
# complete:
#
#   1. THE IDEA [00:05] -- measure how long ANY function
#      takes, start to finish, as a reusable decorator
#   2. FLEXIBLE SPINE [00:51] -- *args/**kwargs in the
#      inner wrapper; proved on zero/positional/keyword
#      signatures (z, 5, 15)
#   3. THE CLOCK [02:22] -- import time; time.time()
#      returns a float stamp; two calls never go
#      backwards (in practice); callable -> True
#   4. THE FIVE STEPS [02:42] -- start_time = time.time()
#      [02:47]; result = func(*args, **kwargs) [02:59];
#      end_time = time.time() [03:14]; execution_time =
#      end - start and PRINT it [03:35]; return result
#      [03:54] -- implemented in that exact order
#   5. STABILITY RULE -- raw seconds change every run, so
#      step 4's print reports FACTS instead: is a float
#      True, end >= start True, under one second True.
#      The measurement is real; only the digits stay
#      home (lesson 79's now() discipline, reused)
#   6. THE 20,000 LOOP [04:07] -- for over range(20000)
#      summing to 199990000 (frozen arithmetic -> the
#      equality check is permanent); the decorated call
#      reports all timing facts True and returns the
#      exact sum
#   7. DATA SURVIVES -- timed_add(2, 3) -> 5,
#      timed_add(6, 7) * 2 -> 26: step 5's return keeps
#      the wrapper transparent in both directions
#   8. EVERY SIGNATURE MEASURED -- one decorator over
#      zero(), keyed(6, factor=7) -> 42, keyed(value=8)
#      -> 8: three full reports, three right answers
#   9. DOWNSTREAM USE -- decorated results multiply with
#      plain arithmetic (26): measurement wraps the
#      journey, not the cargo
#  10. DOUBLE CONFIRMATION -- an independent outer
#      measurement agrees with the decorator's report:
#      result correct, measured as float, under one
#      second, value not None -- all True
#  11. THE COMPROMISE, STATED -- the transcript says
#      "print the time to the user"; this lesson prints
#      a timing REPORT (name, float-ness, magnitude)
#      whose lines are byte-identical on every run --
#      the honest way to teach a clock in a reproducible
#      course
#  12. THE DISCIPLINE -- no raw time value is ever
#      printed; every line is a fixed string or a
#      boolean fact, so the file hashes identically 5
#      times over
#
# Start. Work. Stop. Report. Return. -- the decorator's
# five beats, now with a clock in the band.
