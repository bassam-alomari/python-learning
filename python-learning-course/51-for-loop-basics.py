# -----------------------------------------------------------------
# Lesson 51: for loop - the loop you will use the most
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : for, in, range(), enumerate(), iterating a string
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# In lesson 50 we finished the while loop. Now we start the loop
# that you will write ten times more often than while.
#
# while asks: "how many times?"     -> you keep a counter by hand
# for   asks: "over WHAT?"          -> Python handles the count
#
# Everything in this file runs by itself. Every expected output was
# produced by running the file, not written from memory.

# ============================================================
# [1] The shape of a for loop
# ============================================================
# Four parts, and the order never changes:
#
#     for   item   in   something:
#       body
#
# item       a temporary variable that holds the current element
# in         a keyword, it is not a name you can change
# something  any iterable: list, tuple, set, dict, or a string

numbers = [10, 20, 30, 40]

for number in numbers:
    print("number is:", number)
# number is: 10
# number is: 20
# number is: 30
# number is: 40

# Read it in English: "FOR each number IN numbers, do this."
#
# The important part: there is no counter and no number += 1.
# Python moves to the next element and stops by itself when the
# list runs out. You cannot run past the end of a list, which
# means you cannot get the IndexError that a hand-written
# counter can produce.

# ============================================================
# [2] The same job with while, to see what for saves you
# ============================================================
# The while version needs three extra things: an index, the
# increase, and a condition that can go wrong.

index = 0
while index < len(numbers):
    print("number is:", numbers[index])
    index += 1
# number is: 10
# number is: 20
# number is: 30
# number is: 40

# Same output, and the for version is shorter and safer. This is
# why for is the default choice, and while is kept for the cases
# where you genuinely need a counter or a condition.

# ============================================================
# [3] range(): a for loop over numbers
# ============================================================
# range() does not need a list. It produces numbers as the loop
# asks for them, so range(1_000_000) costs no memory.

for n in range(5):
    print("n is:", n)
# n is: 0
# n is: 1
# n is: 2
# n is: 3
# n is: 4

# range(5) starts at 0. That is the single most common surprise
# for a beginner: you ask for five numbers and you get 0 to 4,
# not 1 to 5. The stop value is never included.

# The three arguments are start, stop, step:

print(list(range(2, 6)))
# [2, 3, 4, 5]

print(list(range(0, 10, 2)))
# [0, 2, 4, 6, 8]

print(list(range(5, 0, -1)))
# [5, 4, 3, 2, 1]

# A negative step counts backwards. range(5, 0, -1) starts at 5
# and stops BEFORE 0, so 0 is not printed. The same "stop is never
# included" rule applies in both directions.

# You never need list() around range() in a for loop. It is only
# used above so we can see the numbers all at once:

for n in range(1, 11, 3):
    print("stepped n is:", n)
# stepped n is: 1
# stepped n is: 4
# stepped n is: 7
# stepped n is: 10

# ============================================================
# [4] Conditions inside a for loop
# ============================================================
# The transcript's example: tell even numbers from odd numbers.
# n % 2 is the remainder, so n % 2 == 0 means "divides by 2 with
# nothing left over", which is the definition of even.

for n in range(1, 11):
    if n % 2 == 0:
        print(f"{n} is even")
    else:
        print(f"{n} is odd")
# 1 is odd
# 2 is even
# 3 is odd
# 4 is even
# 5 is odd
# 6 is even
# 7 is odd
# 8 is even
# 9 is odd
# 10 is even

# A warning about %, because it surprises people twice:
#
#     -3 % 2   ->  1     (not -1)
#      3 % 2   ->  1
#
# Python's % follows the sign of the DIVISOR, so it never returns
# a negative remainder. That is convenient for even/odd tests: the
# odd branch is always n % 2 == 1, no matter the sign of n.

# ============================================================
# [5] More than one condition: elif
# ============================================================
# A for loop with if / elif / else is the most common shape in
# real grading and validation code.

for score in [95, 80, 73, 60, 40]:
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "F"
    print(f"score {score:3} -> {grade}")
# score  95 -> A
# score  80 -> B
# score  73 -> C
# score  60 -> F
# score  40 -> F

# Note the ORDER of the tests. Python runs them from the top and
# stops at the first match, so >= 90 must come before >= 80. If
# you reverse them, a score of 95 reaches the >= 80 test first and
# is called a B. The chain only works from strict to loose.

# ============================================================
# [6] Looping over a string
# ============================================================
# A string is a sequence of characters, so a for loop can walk it
# one character at a time with no extra work.

name = "Ahmed"

for ch in name:
    print("char is:", repr(ch))
# char is: 'A'
# char is: 'h'
# char is: 'm'
# char is: 'e'
# char is: 'd'

# repr() puts quotes around the value, which is how you can see
# that each ch is a separate one-character string and not a word.

# Calling a string method on each character, as the transcript does
# with upper(). Adding end="" keeps everything on one line, because
# print() would add a newline after every character otherwise.

print("upper:", end=" ")
for ch in name:
    print(ch.upper(), end=" ")
print()
# upper: A H M E D

# ============================================================
# [7] The position of each character: enumerate()
# ============================================================
# When you need the index as well, enumerate() gives you both, and
# it is shorter and safer than counting by hand.

for i, ch in enumerate(name):
    print(f"{i} -> {ch}")
# 0 -> A
# 1 -> h
# 2 -> m
# 3 -> e
# 4 -> d

# The old way, for comparison. It works, but it repeats name[i],
# and it breaks the moment the loop variable is not an index.

for i in range(len(name)):
    print(f"{i} -> {name[i]}")
# 0 -> A
# 1 -> h
# 2 -> m
# 3 -> e
# 4 -> d

# If you ever need the index, use enumerate(). If you do not need
# it, loop over the sequence directly and keep the code simple.

# ============================================================
# [8] split() then loop over the words
# ============================================================
# The string loop above gave us characters. When you want WORDS,
# split() cuts the sentence into a list first, and the same for
# loop works on it unchanged.

sentence = "learn python every day"

words = sentence.split()
print("words:", words)
# words: ['learn', 'python', 'every', 'day']

for w in words:
    print(f"  {w.upper()} (len {len(w)})")
#   LEARN (len 5)
#   PYTHON (len 6)
#   EVERY (len 5)
#   DAY (len 3)

# This is the pattern for almost every text program: split, then
# loop. Character access and word access are both just a for loop
# over a different sequence.

# ============================================================
# [9] break and for-else, the same as lesson 50
# ============================================================
# break leaves a for loop exactly the way it left a while loop, and
# for-else still runs only when the loop finished without a break.

for ch in "abcdef":
    if ch == "d":
        print("found d, leaving the loop now")
        break
else:
    print("this prints only if the loop was never broken")
# found d, leaving the loop now

# The else did NOT print, because break fired. This is the same
# idea from lesson 50: success and failure end a loop differently,
# and for-else lets you handle the failure without a flag
# variable.

# ============================================================
# [10] continue: skip the rest of THIS element
# ============================================================
# break leaves the loop. continue only skips the rest of the
# current element, and the loop moves on to the next one.

for n in range(1, 11):
    if n % 3 != 0:
        continue                    # ignore this n, try the next
    print(f"{n} is a multiple of 3")
# 3 is a multiple of 3
# 6 is a multiple of 3
# 9 is a multiple of 3

# The order of continue and break inside the same loop matters.
# Whichever test comes first decides the element's fate.

# ============================================================
# [11] Trap: changing the loop variable does nothing
# ============================================================
# The loop variable is a temporary copy. Rebinding it does not
# touch the list behind it.

names = ["ahmed", "mona"]

for n in names:
    n = n.upper()
print("names:", names)
# names: ['ahmed', 'mona']

# The list is unchanged. Each n was a fresh string, and strings
# cannot be edited in place anyway. If you want a new list, build
# one on purpose:

upper_names = []
for n in names:
    upper_names.append(n.upper())
print("upper_names:", upper_names)
# upper_names: ['AHMED', 'MONA']

# The rule: to change data inside a loop, either mutate the object
# in place (list.append, dict update) or collect the results into
# a new list. Assigning to the loop variable alone is a no-op.

# ============================================================
# [12] Trap: removing items while looping over the list
# ============================================================
# This one silently gives the wrong answer. The loop holds a
# position, and remove() shifts the remaining items left into that
# position, so the element after the removed one is skipped.

def remove_direct(data, should_remove):
    """Remove while walking the live list. Unsafe."""
    for item in data:
        if should_remove(item):
            data.remove(item)
    return data

def remove_on_copy(data, should_remove):
    """Remove while walking a snapshot. Safe."""
    for item in data[:]:
        if should_remove(item):
            data.remove(item)
    return data

# A case where the two really do disagree:
print(remove_direct([10, 20, 30, 40], lambda x: x > 15))
# [10, 30]

print(remove_on_copy([10, 20, 30, 40], lambda x: x > 15))
# [10]

# Direct removed 20, the list became [10, 30, 40], and the loop
# jumped to the next position, which held 40. So 30 was never
# examined and survived. The copy version examined every item and
# correctly left only 10.

# This is worth understanding properly, because the bug is
# invisible in the example from lesson 50:

print(remove_direct([1, 2, 3, 4], lambda x: x % 2 == 0))
# [1, 3]

print(remove_on_copy([1, 2, 3, 4], lambda x: x % 2 == 0))
# [1, 3]

# Both print [1, 3], so this looks safe. It is a coincidence: the
# skipped element was 3, and 3 is odd, so not removing it changed
# nothing. Change the data slightly and the two versions disagree,
# as we saw above with [10, 20, 30, 40].

# The safe habits, in order of preference:
#
#   1. build a new list     kept = [x for x in data if keep_it(x)]
#   2. loop over data[:]   the second function above
#   3. use while + index   only when you truly need the position
#
# Rule of thumb: never change the LENGTH of a list while a for
# loop is walking it. Changing an item's VALUE is fine.

# ============================================================
# [13] The summary
# ============================================================
# for item in something:      walk every element, count handled
# for i in range(a, b, c):    walk numbers, b excluded
# for i, value in enumerate(): walk with the position
# for key, value in dict.items():  walk a dictionary
#
# Use for when you loop over data. Use while when you loop until
# a condition changes: a countdown, a retry limit, input that must
# keep asking.
#
# The while loop from lessons 47 to 50 is not obsolete. It is the
# tool for "keep going until something happens". The for loop is
# the tool for "go through this collection". Reaching for the
# right one is most of what choosing a loop means.