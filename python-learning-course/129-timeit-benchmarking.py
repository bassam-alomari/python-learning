# -----------------------------------------------------------------
# Lesson 129: timeit -- benchmark Python code reliably
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : timeit for repeated timing, repeat() for several
#            batches, compare equivalent implementations,
#            report minimum and understand measurement noise
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript audio is partly unclear, but the repeated
# references to timing code a million times, running several
# trials, and reporting the fastest measurement strongly
# suggest Python's timeit module.
#
#   timeit -- executes a statement repeatedly and measures
#   elapsed time; repetition reduces timer/OS noise
#   repeat -- runs several timing batches and returns one
#   duration per batch
#   COMPARISON -- compare equivalent code that produces the
#   same result; smaller observed time is not a universal
#   guarantee because hardware and system load can vary

import statistics
import timeit

# ============================================================
# [1] Timing code needs repeated measurements
# ============================================================
# A single run can be affected by background activity.
# timeit provides a dedicated repeatable benchmarking API:

print(f"  timeit module imported: {timeit.__name__ == 'timeit'}")
print(f"  timeit callable available: {callable(timeit.timeit)}")
print(f"  repeat callable available: {callable(timeit.repeat)}")
#   timeit module imported: True
#   timeit callable available: True
#   repeat callable available: True

# ============================================================
# [2] Compare two equivalent implementations
# ============================================================
# Both functions make the same list of squares:

def squares_loop(size):
    """Build squares using a for loop."""
    result = []
    for value in range(size):
        result.append(value * value)
    return result


def squares_comprehension(size):
    """Build squares using a list comprehension."""
    return [value * value for value in range(size)]


loop_result = squares_loop(100)
comprehension_result = squares_comprehension(100)
print(f"  results are equal: {loop_result == comprehension_result}")
print(f"  result item count: {len(loop_result)}")
#   results are equal: True
#   result item count: 100

# Benchmark only equivalent work so the timing comparison
# is meaningful.

# ============================================================
# [3] timeit.timeit repeats one statement
# ============================================================
# Run a fixed small number of executions; do not display
# elapsed seconds because timing varies by machine:

single_batch = timeit.timeit(
    "squares_loop(100)",
    globals=globals(),
    number=1000,
)
print(f"  timeit ran the loop batch: {single_batch >= 0}")
print(f"  batch requested executions: {1000}")
#   timeit ran the loop batch: True
#   batch requested executions: 1000

# ============================================================
# [4] repeat() returns multiple batch timings
# ============================================================
# Run the same workload in three batches:

loop_times = timeit.repeat(
    "squares_loop(100)",
    globals=globals(),
    number=1000,
    repeat=3,
)

print(f"  repeat batch count: {len(loop_times)}")
print(f"  every timing is nonnegative: {all(value >= 0 for value in loop_times)}")
#   repeat batch count: 3
#   every timing is nonnegative: True

# ============================================================
# [5] Benchmark the second implementation
# ============================================================
# Use the same number of repeats and executions:

comprehension_times = timeit.repeat(
    "squares_comprehension(100)",
    globals=globals(),
    number=1000,
    repeat=3,
)

print(f"  second batch count: {len(comprehension_times)}")
print(f"  both use same run count: {len(loop_times) == len(comprehension_times)}")
#   second batch count: 3
#   both use same run count: True

# ============================================================
# [6] Summarize timing batches without raw seconds
# ============================================================
# Report a stable-shape comparison: each has a minimum and
# median, but values themselves depend on the machine:

loop_min = min(loop_times)
comp_min = min(comprehension_times)
loop_median = statistics.median(loop_times)
comp_median = statistics.median(comprehension_times)

print(f"  loop minimum timing exists: {loop_min >= 0}")
print(f"  comprehension minimum timing exists: {comp_min >= 0}")
print(f"  loop median timing exists: {loop_median >= 0}")
print(f"  comprehension median timing exists: {comp_median >= 0}")
#   loop minimum timing exists: True
#   comprehension minimum timing exists: True
#   loop median timing exists: True
#   comprehension median timing exists: True

# ============================================================
# [7] Compare using the minimum observed batch
# ============================================================
# The minimum is commonly used as a lower-noise estimate;
# no machine-specific winner is assumed in expected output:

faster_min = "loop" if loop_min < comp_min else "comprehension or tie"
print(f"  measured winner label is valid: {faster_min in ('loop', 'comprehension or tie')}")
print(f"  same outputs before timing: {loop_result == comprehension_result}")
#   measured winner label is valid: True
#   same outputs before timing: True

# ============================================================
# [8] More repetitions help reveal variability
# ============================================================
# A small summary compares spread within each set of runs:

loop_spread = max(loop_times) - min(loop_times)
comp_spread = max(comprehension_times) - min(comprehension_times)
print(f"  loop spread is nonnegative: {loop_spread >= 0}")
print(f"  comprehension spread is nonnegative: {comp_spread >= 0}")
print(f"  multiple batches captured noise: {len(loop_times) > 1}")
#   loop spread is nonnegative: True
#   comprehension spread is nonnegative: True
#   multiple batches captured noise: True

# ============================================================
# [9] timeit.Timer interface
# ============================================================
# Timer offers the same API as module-level timeit/repeat:

timer = timeit.Timer("squares_loop(10)", globals=globals())
timer_runs = timer.repeat(repeat=2, number=10)
print(f"  Timer repeat count: {len(timer_runs)}")
print(f"  Timer results valid: {all(value >= 0 for value in timer_runs)}")
#   Timer repeat count: 2
#   Timer results valid: True

# ============================================================
# [10] Keep benchmark setup separate from the statement
# ============================================================
# setup runs before the timed statement; the code being
# measured should be clear and equivalent:

setup_example = timeit.timeit(
    "sum(values)",
    setup="values = list(range(100))",
    number=100,
)
print(f"  setup benchmark completed: {setup_example >= 0}")
print(f"  setup separated from timed expression: True")
#   setup benchmark completed: True
#   setup separated from timed expression: True

# ============================================================
# [11] Timing best practices
# ============================================================
# A benchmark checklist:

guidelines = (
    "compare equivalent results",
    "repeat multiple batches",
    "keep setup outside the timed statement when appropriate",
    "avoid drawing conclusions from one run",
    "remember machine and system-load differences",
)
print(f"  benchmark guidelines: {len(guidelines)}")
print(f"  first guideline: {guidelines[0]}")
print(f"  last guideline: {guidelines[-1]}")
#   benchmark guidelines: 5
#   first guideline: compare equivalent results
#   last guideline: remember machine and system-load differences

# ============================================================
# [12] One session: repeat, compare, interpret
# ============================================================
# Summary facts for both implementations:

print(f"  loop batches: {len(loop_times)}")
print(f"  comprehension batches: {len(comprehension_times)}")
print(f"  same output: {loop_result == comprehension_result}")
print(f"  comparison has valid minimums: {loop_min >= 0 and comp_min >= 0}")
print(f"  benchmark is not a universal guarantee: {True}")
#   loop batches: 3
#   comprehension batches: 3
#   same output: True
#   comparison has valid minimums: True
#   benchmark is not a universal guarantee: True

# ============================================================
# [13] The summary
# ============================================================
# Benchmarking, from the transcript:
#
#   1. timeit -- time a statement many times to reduce the
#      influence of one-off timing noise
#   2. timeit() -- runs a chosen number of executions
#   3. repeat() -- returns several batch durations; inspect
#      minimum/median and spread, not one lucky run
#   4. COMPARISON -- benchmark implementations only after
#      confirming they produce the same result
#   5. ENVIRONMENT -- hardware, interpreter, OS and other
#      processes affect timings; fastest observed is not a
#      universal guarantee
#   6. SETUP -- keep preparation separate when measuring
#      only the operation of interest
#
# Measure repeatedly, compare equal work, and treat a
# benchmark as evidence for this environment, not a promise.
