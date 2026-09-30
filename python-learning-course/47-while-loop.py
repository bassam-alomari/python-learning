# -----------------------------------------------------------------
# Lesson 47: While Loop - Repetition Until a Condition Breaks
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : loop, while, condition, iteration, infinite loop, break, else
# Type     : Educational + Practical Examples
# Builder  : local assistant
# -----------------------------------------------------------------
# Today we start the loop family. A loop saves us from writing the
# same line hundreds of times. Imagine a list with 1000 items: you
# cannot write one line per item, so you let the loop walk the data
# for you. The first loop we learn is while.

# ============================================================
# [1] The idea of repetition
# ============================================================
# A List with 1000 items, and we want to print every one of it.
# The wrong way is 1000 print lines. The right way is one loop.

names = ["Ahmed", "Sayed", "Mona", "Omar", "Hana"]

print("--- the loop prints all of them in 3 lines of code ---")
for name in names:                       # the loop itself
    print(name)                          # this line repeats 5 times
# Ahmed
# Sayed
# Mona
# Omar
# Hana

print("items in the list:", len(names))
# items in the list: 5

# Think of it this way: you write the body ONCE, and Python runs it
# once per item. That is the whole promise of a loop.

# ============================================================
# [2] while means "as long as" or "while"
# ============================================================
# Arabic: while = بينما, طالما أن
#
# The shape of every while loop:
#
#   while CONDITION:      <- checked FIRST
#       body              <- then the body runs
#
# The rule: while the condition is True, keep running the body.
# The loop stops ONLY when the condition turns False.

a = 0

while a < 10:              # "as long as a is smaller than 10"
    print("a is now:", a)   # this runs again and again
    a += 1                 # THIS LINE IS THE BRAKE

print("after the loop, a =", a)
# a is now: 0
# a is now: 1
# ...
# a is now: 9
# after the loop, a = 10

# Read it out loud: "while a is smaller than 10, print a, then make a
# bigger by one." When a becomes 10 the condition is False, so the
# loop stops. a ends at exactly 10.

# ============================================================
# [3] THE TRAP: forget the brake and you get an infinite loop
# ============================================================
# If we remove a += 1, then a stays 0 forever, and 0 < 10 is True
# forever. That is an Infinite Loop. The program never finishes and
# you have to force stop it (Ctrl+C in the terminal).
#
# WE WILL NOT RUN IT HERE, because it would freeze this lesson.
# We only write it as text to show the shape:

# while a < 10:            # DANGER: no a += 1 inside
#     print("forever")     # DANGER: a never changes, so this never stops

# The lesson's own sentence: if you do not change the variable inside
# the loop, it will run to infinity, because the condition stays true.

# The proof that the brake is what saves us:
counter = 0
while counter < 5:
    counter += 1            # brake
print("with the brake, counter =", counter)
# with the brake, counter = 5

# ============================================================
# [4] Iteration: one pass = one iteration
# ============================================================
# An iteration is ONE single run of the loop body. The word comes
# from "iterate" = to repeat.

total = 0
i = 1

while i <= 5:
    total += i              # add the current number to the total
    print(f"iteration {i}: added {i}, total = {total}")
    i += 1                  # advance to the next number

print("the sum of 1..5 =", total)
# iteration 1: added 1, total = 1
# iteration 2: added 2, total = 3
# iteration 3: added 3, total = 6
# iteration 4: added 4, total = 10
# iteration 5: added 5, total = 15
# the sum of 1..5 = 15

# ============================================================
# [5] Downwards loops: start big, shrink to the target
# ============================================================
# The condition does not have to count UP. It can count DOWN, and
# then the brake must DECREASE the variable.

remaining = 5

while remaining > 0:
    print(f"{remaining} tickets left, selling one...")
    remaining -= 1

print("sold out. remaining =", remaining)
# 5 tickets left, selling one...
# 4 tickets left, selling one...
# 3 tickets left, selling one...
# 2 tickets left, selling one...
# 1 tickets left, selling one...
# sold out. remaining = 0

# ============================================================
# [6] String repetition inside a loop
# ============================================================
# A while loop is also handy for building text step by step.

line = ""
stars = 4

while stars > 0:
    line += "*"            # the string GROWS every iteration
    stars -= 1             # the counter SHRINKS every iteration

print("built:", line)
# built: ****

# Two variables moving toward each other: one grows, one shrinks.
# This is a very common shape, and the danger is forgetting the
# shrink line, which turns it into an infinite loop again.

# ============================================================
# [7] The else attached to while  (a real Elzero topic)
# ============================================================
# Once the while loop finishes NATURALLY, meaning the condition
# turned False and not because we used break, Python runs the
# else block that sits at the same level as the while.

x = 0

while x < 5:
    x += 1
    print("x =", x)
else:
    print("Loop Is Done")

# x = 1
# x = 2
# x = 3
# x = 4
# x = 5
# Loop Is Done

# Why is this useful? The else runs ONLY if the loop was not cut
# short by a break. So it is the perfect place for the message
# "we finished everything", because it will be skipped if we stopped
# early. We will see that power with break in the next lesson.

# ============================================================
# [8] While vs if: when do we use which?
# ============================================================
# if runs the block ONCE, if the condition is true.
# while runs the block AGAIN AND AGAIN, as long as it is true.

count = 0

if count < 3:               # ONE check
    count += 1
print("after if  ->", count)
# after if  -> 1

count = 0

while count < 3:            # MANY checks: 0 -> 1 -> 2 -> 3, then stop
    count += 1
print("after while ->", count)
# after while -> 3

# if: "maybe once". while: "keep going until I say stop".

# ============================================================
# [9] Real traps when writing a while loop
# ============================================================
# 1) Forgetting the update line is the #1 bug: infinite loop.
# 2) Using == instead of >= or <= makes the loop run ZERO times:
#      a = 0
#      while a == 5:      # we ask "is a exactly 5?"
#          a += 1
#    Here a starts at 0, so "a == 5" is False on the very first
#    check and the body never runs. And because the body never runs,
#    a stays 0 forever, so it can NEVER become 5. It is a deadlock,
#    not an infinite loop: it just quietly does nothing.
#    This is the trap that looks like a working loop but never runs.
d = 0
while d == 5:
    d += 1
print("with ==, the body ran", d, "times (it never started)")
# with ==, the body ran 0 times (it never started)
# 3) Writing the update line but at the TOP of the body changes the
#    result: it skips the first value.
# 4) A while loop with a False condition runs ZERO times, never once.

b = 0
while b < 3:
    print("this WILL print, b =", b)
    b += 1
# this WILL print, b = 0
# this WILL print, b = 1
# this WILL print, b = 2

c = 10
while c < 3:
    print("this will NEVER print")
    c += 1
print("a False condition means the body is skipped completely")
# a False condition means the body is skipped completely

# ============================================================
# [10] The same thing without input, so it is testable
# ============================================================
# In the next lessons we will read the loop limit with input().
# For now we hardcode it, so the file runs by itself and we can
# check every number in the printed output.

def count_up_to(limit):
    """Return how many numbers we printed from 1 up to limit."""
    n = 0
    while n < limit:
        n += 1
    return n

print("count_up_to(5)  ->", count_up_to(5))
print("count_up_to(0)  ->", count_up_to(0))
print("count_up_to(10) ->", count_up_to(10))
# count_up_to(5)  -> 5
# count_up_to(0)  -> 0
# count_up_to(10) -> 10

def sum_up_to(limit):
    """Return 1 + 2 + ... + limit using a while loop."""
    total = 0
    n = 1
    while n <= limit:
        total += n
        n += 1
    return total

print("sum_up_to(5)  ->", sum_up_to(5))
print("sum_up_to(10) ->", sum_up_to(10))
# sum_up_to(5)  -> 15
# sum_up_to(10) -> 55

# sum_up_to(0) is also 0, and that is the correct answer, not a bug:
# the loop never starts because n=1 already fails 1 <= 0.
print("sum_up_to(0)  ->", sum_up_to(0))
# sum_up_to(0)  -> 0

# ============================================================
# SUMMARY
# ============================================================
# - A loop repeats a block of code so you write it once, not 1000 times.
# - while means "as long as": it checks the condition, runs the body,
#   and repeats while the condition stays True.
# - The update line (a += 1) is the BRAKE. Forget it and you get an
#   infinite loop, which is exactly what the lesson warns about.
# - One pass of the body is called one iteration.
# - The loop can also count DOWN, then the update must decrease.
# - The else after a while runs only when the loop finished normally,
#   which makes it the right place for "Loop Is Done" messages.
# - if runs once; while runs as many times as the condition allows.
# - Use >= or <= in the condition, not ==, or the loop may run zero
#   times and you will be confused.

# ============================================================
# NEXT LESSON: break and continue inside the while loop
# ============================================================