# -----------------------------------------------------------------
# Lesson 93: debugging code -- follow execution step by step
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : debugging, variable inspection, breakpoints,
#            stepping over and into, continuing, and
#            fixing a logic bug with a trace
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: Debugging Code -- a key skill
# for professional programmers.
#
#   WHAT [00:11] -- follow execution step by step; watch
#   variable values; discover hidden causes of errors or
#   unexpected behavior in large projects
#   VS CODE [01:05] -- set a breakpoint by clicking beside
#   a line number (red dot); Start Debugging pauses there
#   so you can inspect memory and current variables
#   CONTROLS [02:42] -- Step Over / F10 executes this line
#   and goes to the next; Step Into / F11 follows a called
#   function inside; Continue / F5 runs to the next
#   breakpoint or program end
#   WHY [04:37] -- indispensable for understanding flow
#   and finding bugs precisely in large applications
#
# This lesson uses a deterministic trace as a stand-in
# for the debugger's variable panel -- the same values,
# one checkpoint at a time, without requiring VS Code
# or printing machine-specific debugger state.

# ============================================================
# [1] What debugging means [00:11]
# ============================================================
# Debugging is not guessing. It is watching a program's
# execution and its variables, step by step, until the
# unexpected result has an explanation.

print("  debugging: follow execution and inspect values")
print("  goal: find why the result is unexpected")
#   debugging: follow execution and inspect values
#   goal: find why the result is unexpected

# ============================================================
# [2] A small bug to investigate
# ============================================================
# A shop applies a 10% discount. The result looks wrong:

price = 100
discount_percent = 10
discount = discount_percent / 100
buggy_total = price - discount

print(f"  starting price: {price}")
print(f"  discount fraction: {discount}")
print(f"  buggy total: {buggy_total}")
#   starting price: 100
#   discount fraction: 0.1
#   buggy total: 99.9

# Expected 90, got 99.9. A breakpoint near the
# calculation lets us inspect each value before
# deciding which line is wrong.

# ============================================================
# [3] Breakpoint: pause and inspect [01:10]
# ============================================================
# In VS Code, click beside the line number to set the red
# dot, then Start Debugging. Here, named checkpoints give
# the same inspection in a reproducible text trace:

checkpoint_before = {
    "price": price,
    "discount_percent": discount_percent,
    "discount": discount,
}

print(f"  breakpoint values: {checkpoint_before}")
print(f"  expected discount amount: {price * discount}")
print(f"  actual subtraction amount: {discount}")
#   breakpoint values: {'price': 100, 'discount_percent': 10, 'discount': 0.1}
#   expected discount amount: 10.0
#   actual subtraction amount: 0.1

# The inspection exposes the mismatch: discount is a
# fraction, but the buggy line subtracts the fraction
# itself rather than the amount (price * discount).

# ============================================================
# [4] Step Over / F10 [02:42]
# ============================================================
# Step Over executes the current line without entering
# any called function, then pauses at the next line.
# Record the before/after values as if pressing F10:

step_values = []
running_total = price
step_values.append(running_total)
running_total = running_total - discount
step_values.append(running_total)

print(f"  F10 checkpoints: {step_values}")
print(f"  one line executed per step: {len(step_values) == 2}")
#   F10 checkpoints: [100, 99.9]
#   one line executed per step: True

# The debugger did not jump into a helper; it ran the
# current statement and paused at the next one.

# ============================================================
# [5] Step Into / F11 [02:42]
# ============================================================
# Step Into follows a called function's body. This helper
# makes the correct discount amount; F11 would enter it:

def calculate_discount(amount, fraction):
    """Return the monetary discount amount."""
    return amount * fraction


discount_amount = calculate_discount(price, discount)

print(f"  F11 enters calculate_discount: {discount_amount}")
print(f"  function result matches expected: {discount_amount == 10.0}")
#   F11 enters calculate_discount: 10.0
#   function result matches expected: True

# Step Into differs from Step Over: it follows the call
# into calculate_discount so you can inspect its inputs
# and return value.

# ============================================================
# [6] Find the logic error
# ============================================================
# Compare the intended operation with the buggy one:

buggy_subtraction = discount
correct_subtraction = calculate_discount(price, discount)

print(f"  buggy subtraction: {buggy_subtraction}")
print(f"  correct subtraction: {correct_subtraction}")
print(f"  values differ: {buggy_subtraction != correct_subtraction}")
#   buggy subtraction: 0.1
#   correct subtraction: 10.0
#   values differ: True

# The bug is not in the percentage or the price. The
# missing multiplication is the hidden cause.

# ============================================================
# [7] Fix the line and verify
# ============================================================
# Corrected calculation: subtract the amount, not the
# fraction:

fixed_total = price - calculate_discount(price, discount)

print(f"  fixed total: {fixed_total}")
print(f"  expected total: {90.0}")
print(f"  fix verified: {fixed_total == 90.0}")
#   fixed total: 90.0
#   expected total: 90.0
#   fix verified: True

# Debugging is complete when the observed values explain
# the bug AND the corrected output passes the expectation.

# ============================================================
# [8] Continue / F5 [02:42]
# ============================================================
# Continue resumes normal execution until the next
# breakpoint or the end. A two-checkpoint run illustrates
# that the debugger can pause, inspect, then continue:

breakpoints = ("before calculation", "after calculation")
print(f"  breakpoint count: {len(breakpoints)}")
print(f"  first breakpoint: {breakpoints[0]}")
print(f"  continue reaches: {breakpoints[1]}")
#   breakpoint count: 2
#   first breakpoint: before calculation
#   continue reaches: after calculation

# In VS Code, F5 continues to the next red dot (or ends
# the program if there are no more breakpoints).

# ============================================================
# [9] The three controls compared
# ============================================================
# F10, F11 and F5 -- compact reference from the lecture:

print("  F10 Step Over: run this line, pause at next")
print("  F11 Step Into: enter the called function")
print("  F5 Continue: run to next breakpoint or end")
#   F10 Step Over: run this line, pause at next
#   F11 Step Into: enter the called function
#   F5 Continue: run to next breakpoint or end

# Each control changes how far execution advances;
# variable inspection is what makes the pause useful.

# ============================================================
# [10] Watch values change over time
# ============================================================
# A small watch history makes the hidden change visible:

watch = []
remaining = price
watch.append(("start", remaining))
remaining -= discount
watch.append(("buggy", remaining))
remaining = price - calculate_discount(price, discount)
watch.append(("fixed", remaining))

print(f"  watched values: {watch}")
print(f"  final watch value: {watch[-1][1]}")
#   watched values: [('start', 100), ('buggy', 99.9), ('fixed', 90.0)]
#   final watch value: 90.0

# Watching a variable at multiple checkpoints answers
# "when did it become wrong?" -- the core debugging
# habit from the transcript.

# ============================================================
# [11] A repeatable debugging routine
# ============================================================
# Turn the lecture into a process:

routine = (
    "reproduce the unexpected result",
    "set a breakpoint before it",
    "inspect current variable values",
    "step over or into the relevant code",
    "fix the cause and verify the result",
)

print(f"  routine steps: {len(routine)}")
print(f"  first: {routine[0]}")
print(f"  last: {routine[-1]}")
#   routine steps: 5
#   first: reproduce the unexpected result
#   last: fix the cause and verify the result

# Reproducible, deliberate, and evidence-led -- not
# random edits until the symptom disappears.

# ============================================================
# [12] One session: the bug, the investigation, the fix
# ============================================================
# The complete example in a compact set of facts:

print(f"  buggy result: {buggy_total}")
print(f"  inspected fraction: {discount}")
print(f"  correct discount amount: {discount_amount}")
print(f"  fixed result: {fixed_total}")
print(f"  breakpoint controls taught: {len(breakpoints)}")
print(f"  F10 / F11 / F5 covered: {len(routine) == 5}")
print(f"  expected result reached: {fixed_total == 90.0}")
#   buggy result: 99.9
#   inspected fraction: 0.1
#   correct discount amount: 10.0
#   fixed result: 90.0
#   breakpoint controls taught: 2
#   F10 / F11 / F5 covered: True
#   expected result reached: True

# One hidden logic error, traced to the exact value,
# corrected, then verified -- the debugging loop.

# ============================================================
# [13] The summary
# ============================================================
# Debugging, from the transcript:
#
#   1. WHAT [00:11] -- follow execution step by step;
#      watch variable values; discover why behavior is
#      wrong instead of guessing
#   2. BREAKPOINT [01:10] -- VS Code: click beside a line
#      number for a red dot; Start Debugging pauses there
#      to inspect current memory and variables
#   3. THE INVESTIGATION -- price 100, discount 10%;
#      expected amount 10.0, buggy line subtracted 0.1;
#      the breakpoint values exposed the mismatch
#   4. STEP OVER / F10 [02:42] -- execute this line,
#      pause at the next; checkpoints [100, 99.9]
#   5. STEP INTO / F11 [02:42] -- follow the call inside
#      calculate_discount; inputs and result inspected,
#      correct amount 10.0
#   6. CONTINUE / F5 [02:42] -- run to the next
#      breakpoint or program end; the two checkpoints
#      demonstrate the pause/resume plan
#   7. THE FIX -- subtract price * fraction (10.0), not
#      the fraction itself (0.1); fixed total 90.0,
#      verified True
#   8. WATCH HISTORY -- start 100 -> buggy 99.9 -> fixed
#      90.0; the value history shows exactly when and how
#      the result went wrong
#   9. THE ROUTINE -- reproduce -> breakpoint -> inspect
#      -> step over/into -> fix and verify (five steps)
#  10. WHY IT MATTERS [04:37] -- indispensable in large
#      applications for understanding flow and finding
#      causes precisely
#  11. THE DISCIPLINE -- deterministic trace stands in
#      for the GUI debugger; no VS Code dependency, no
#      machine paths, and each checkpoint is reproducible
#
# A breakpoint asks the program to wait. A good question
# at that pause is what makes debugging work.
