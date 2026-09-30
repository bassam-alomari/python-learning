# -----------------------------------------------------------------
# Lesson 48: Practical Application - While Loop Over a List
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : while, len(), index, a += 1, numbering, zfill, f-string
# Type     : Educational + Practical Application
# Builder  : local assistant
# -----------------------------------------------------------------
# We know the while loop. Today we use it for something real:
# walking through a list of friends with an index, numbering each
# one, and printing a confirmation when the whole list is done.

# ============================================================
# [1] The friends list
# ============================================================
# A plain list of names. The Arabic names from the lesson are kept in
# the comments so the example stays easy to read for an Arabic user.

my_friends = ["Osama", "Ahmed", "Yehia", "Sayed", "Mona"]

#   my_friends[0] -> "Osama"
#   my_friends[1] -> "Ahmed"
#   my_friends[2] -> "Yehia"
#   my_friends[3] -> "Sayed"
#   my_friends[4] -> "Mona"
#
# The indices are 0, 1, 2, 3, 4. Python always starts counting from
# ZERO, and that is the single most important thing in this lesson.

print("my_friends     :", my_friends)
print("length of list :", len(my_friends))
# my_friends     : ['Osama', 'Ahmed', 'Yehia', 'Sayed', 'Mona']
# length of list : 5

# ============================================================
# [2] The wrong way: one print line per item
# ============================================================
# It works, and this is exactly the problem. If the list had 1000
# items we would need 1000 print lines, and nobody writes that.

print(my_friends[0])
print(my_friends[1])
print(my_friends[2])
print(my_friends[3])
print(my_friends[4])
# Osama
# Ahmed
# Yehia
# Sayed
# Mona

# 5 lines of code for 5 names. Add one friend and you must add one
# more line. That is the exact situation a loop removes.

# ============================================================
# [3] The while loop over the list
# ============================================================
# Four pieces, and all four are needed:
#
#   a = 0                    the counter, starts at 0
#   while a < len(friends)   the brake, stops at the end of the list
#   print(friends[a])        the body, uses the counter as an index
#   a += 1                   the advance, moves to the next index
#
# len(my_friends) is 5, so the condition a < 5 allows the indices
# 0,1,2,3,4 and nothing else. When a becomes 5 the loop stops.

a = 0

while a < len(my_friends):
    print(my_friends[a])     # take the item at position a
    a += 1                   # then go to the next position

# Osama
# Ahmed
# Yehia
# Sayed
# Mona

# WHY len() and not a hardcoded number? Because if we hardcode 5 and
# someone adds a 6th friend later, the loop keeps working but skips
# the new friend, or crashes if the list shrinks. len() always tells
# the truth about the list RIGHT NOW.

# ============================================================
# [4] Numbering the output, and the +1 offset trap
# ============================================================
# The lesson asks for numbers starting from 1, but the index starts
# from 0. So the printed number must be a + 1, NOT a.

b = 0

while b < len(my_friends):
    print(f"{b + 1}. {my_friends[b]}")
    b += 1

# 1. Osama
# 2. Ahmed
# 3. Yehia
# 4. Sayed
# 5. Mona

# Why? b is the index 0,1,2,3,4 and the human number is 1,2,3,4,5.
# Writing {b} alone would print 0.Osama ... 4.Mona, which is correct
# code but strange for a person reading a numbered list.

# ============================================================
# [5] Padding the number with zfill or f-string
# ============================================================
# The lesson wants 01, 02, 03 ... so the numbers line up in one
# column. There are two ways and they behave the same:

print("--- two ways to pad to two digits ---")
for number in (1, 9, 10, 100):
    print(f"  {number:3} | zfill -> {str(number).zfill(2)} | f-string -> {number:02d}")
#     1 | zfill -> 01 | f-string -> 01
#     9 | zfill -> 09 | f-string -> 09
#    10 | zfill -> 10 | f-string -> 10
#   100 | zfill -> 100 | f-string -> 100

print("--- the two are identical ---")
print("str(7).zfill(2) :", str(7).zfill(2))
print("f'{7:02d}'      :", f"{7:02d}")
# str(7).zfill(2) : 07
# f'{7:02d}'      : 07

# ============================================================
# [6] TWO REAL TRAPS about padding
# ============================================================
# TRAP 1: the width is a MINIMUM, not a fixed size.
# str(100).zfill(2) is "100", three characters. zfill never cuts a
# number, it only adds zeros on the left when the string is SHORTER
# than the width. So if the list grows past 99 items, the column
# widens and the alignment is lost. zfill(2) does not mean "2 wide".

# TRAP 2: zfill(1) adds nothing at all.
# The width must be larger than the longest number you expect.
print("zfill(1) on 5   :", repr(str(5).zfill(1)))      # '5'  <- no zero
print("f'{5:01d}'      :", f"{5:01d}")                # 5   <- no zero
# zfill(1) on 5   : '5'
# f'{5:01d}'      : 5

# Both are correct, both add no padding, because 1 is already the
# minimum width. If you want 05, you must ask for 2: zfill(2).

# ============================================================
# [7] The final message after the loop
# ============================================================
# The lesson prints one line at the end to confirm that every item
# was shown. It must sit AFTER the loop, at the same indentation,
# otherwise it would print on every single iteration.

c = 0

while c < len(my_friends):
    print(f"{str(c + 1).zfill(2)}. {my_friends[c]}")
    c += 1

print("All Friends Printed Successfully")
# 01. Osama
# 02. Ahmed
# 03. Yehia
# 04. Sayed
# 05. Mona
# All Friends Printed Successfully

# This file uses zfill here, and section [5] shows the f-string way,
# so you can see they are the same thing written two styles.

# ============================================================
# [8] The same loop with a for loop, for comparison
# ============================================================
# A for loop does this in ONE line with no counter and no len(),
# because Python counts the indices for us. We are still on while
# today, but you should see what you are writing by hand.

print("--- the while version ---")
d = 0
while d < len(my_friends):
    print(f"{str(d + 1).zfill(2)}. {my_friends[d]}")
    d += 1

print("--- the for version, same output, 2 lines ---")
for index, friend in enumerate(my_friends, start=1):
    print(f"{str(index).zfill(2)}. {friend}")

# Both blocks print exactly the same five lines. That is the honest
# truth about this lesson: while works, but for is the shorter tool
# for walking a list. We master while first so we understand for.

# ============================================================
# [9] The mistake that breaks the loop
# ============================================================
# Forgetting a += 1 gives an infinite loop. Forgetting a += 1 but
# writing a = a + 1 in the condition area, or using a > 0 instead of
# a < len(), gives other wrong answers. Let us test the boundary.

e = 0
while e <= len(my_friends) - 1:   # the long, safe way
    print("safe:", my_friends[e])
    e += 1
# safe: Osama
# safe: Ahmed
# safe: Yehia
# safe: Sayed
# safe: Mona

# e <= len(my_friends) - 1 is the same as e < len(my_friends), and it
# is clearer for a beginner because it shows where the last valid
# index is: len() - 1. Getting this wrong is the #1 crash here,
# because my_friends[5] does not exist and raises IndexError.

try:
    my_friends[len(my_friends)]
except IndexError as err:
    print("IndexError ->", err)
# IndexError -> list index out of range

# ============================================================
# [10] Testable version, no printing inside the logic
# ============================================================
# Printing inside the loop makes the code hard to test. Building the
# lines first and returning them lets us check the result directly.

def numbered_friends(friends):
    """Return the friends as zero-padded numbered lines."""
    lines = []
    position = 0
    while position < len(friends):
        lines.append(f"{str(position + 1).zfill(2)}. {friends[position]}")
        position += 1
    return lines

def total_characters(friends):
    """Return the number of letters in all the names."""
    count = 0
    position = 0
    while position < len(friends):
        count += len(friends[position])
        position += 1
    return count

print("--- checking the helper ---")
print("numbered_friends ->", numbered_friends(my_friends))
print("total characters ->", total_characters(my_friends))
print("empty list       ->", numbered_friends([]))
# numbered_friends -> ['01. Osama', '02. Ahmed', '03. Yehia', '04. Sayed', '05. Mona']
# total characters -> 24
# empty list       -> []

# An empty list is worth testing: the condition 0 < 0 is False, so the
# loop runs zero times and we get an empty list, not a crash.

# ============================================================
# SUMMARY
# ============================================================
# - len(my_friends) gives the number of items, and it is the honest
#   brake for the loop. Never hardcode the number.
# - The counter starts at 0 because indices start at 0, and the
#   condition a < len(friends) stops it at exactly the right place.
# - a += 1 is mandatory. Without it the loop never ends.
# - For human numbering use a + 1, otherwise the list starts at 0.
# - zfill(2) or f"{n:02d}" both give 01, 02, 03. The width is a
#   MINIMUM, so 100 stays "100", and zfill(1) adds nothing.
# - The final message must be OUTSIDE the loop, at the same level.
# - A for loop with enumerate does the same job in two lines. while
#   is worth mastering first, but for is the right tool for a list.
# - my_friends[len(my_friends)] raises IndexError, which is why the
#   condition must use < and not <=.

# ============================================================
# NEXT LESSON: break and continue inside the while loop
# ============================================================