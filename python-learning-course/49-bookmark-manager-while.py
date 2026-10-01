# -----------------------------------------------------------------
# Lesson 49: Practical Application - Bookmark Manager
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : while, list, append, sort, input, strip, lower
# Type     : Educational + Practical Application
# Builder  : local assistant
# -----------------------------------------------------------------
# A small real program: the user types up to 5 websites, and the
# program keeps them in a list, then prints them sorted with numbers.
# The point of this lesson is the SHAPE of the while loop. Instead of
# counting UP to the list length, we count DOWN a counter of free
# places. That single change is what makes the loop stop.

# ============================================================
# [1] The empty list and the maximum
# ============================================================
# The list starts EMPTY, so there is nothing to print yet. We will
# fill it with append() while the loop runs.
#
# `maximum` is NOT a loop index. It is the number of FREE PLACES
# left. This is a different style from lesson 48, and it is the
# style you use when you do not know in advance how many items the
# user will give you.

my_websites = []
maximum = 5

print("my_websites :", my_websites)
print("maximum     :", maximum)
# my_websites : []
# maximum     : 5

# Why a maximum at all? Because this program asks a human, and a
# human can type forever. An unbounded while loop with input() is a
# guaranteed infinite loop. The counter is the brake.

# ============================================================
# [2] The input loop
# ============================================================
# The condition is "while there are still free places":
#
#   while maximum > 0:      keep going while places remain
#       website = input()   ask the user
#       append it           store it
#       maximum -= 1        one place is now taken
#
# We do NOT use len(my_websites) < 5 here, even though it would
# work. The counter is simpler, and it is what the lesson teaches.

maximum = 5

# We fake the input() with a list so the file runs by itself and we
# can check every printed line. In the real program this single line
# asks the user:
#
#   website = input("Please type your website: ")
#
fake_typing = ["  Google  ", "Python.org", "  GITHUB.com", "  Www.Example.COM", "  stackoverflow "]

# We store each answer in `answer`, and the while body copies it into
# `website`. A CAREFUL point: never write `for website in fake_typing`
# and then reuse that same name inside the loop, or the name will hold
# only the LAST value by the time the body runs again.
answer = ""

while maximum > 0:
    # ---- this is where the real input() goes ----
    answer = fake_typing[5 - maximum]       # take the next fake answer
    website = answer.strip().lower()        # clean it: strip + lower

    my_websites.append(website)             # store it in the list
    maximum -= 1                           # take one place

    print(f"Website Added, You Have {maximum} Places Left")
    # loop condition is re-checked here, and now maximum may be 0

# There is no `for` loop at all now. The while does everything, which
# is what the lesson asks for. The list indexing is only there to
# supply five answers without input().

print("--- the result of the loop ---")
print("my_websites :", my_websites)
print("maximum     :", maximum)
# Website Added, You Have 4 Places Left
# Website Added, You Have 3 Places Left
# Website Added, You Have 2 Places Left
# Website Added, You Have 1 Places Left
# Website Added, You Have 0 Places Left
# --- the result of the loop ---
# my_websites : ['google', 'python.org', 'github.com', 'www.example.com', 'stackoverflow']
# maximum     : 0

# The last message says "0 Places Left", and that is the moment the
# condition 0 > 0 became False, so the loop stopped. It ran exactly
# five times for five free places.

# ============================================================
# [3] Cleaning the text: why strip() AND lower()
# ============================================================
# Look at the first input above: "  Google  ".
#
#   .strip()  removes spaces at the START and the END only
#   .lower()  turns every capital letter into a small one
#
# Without them the list would be full of near duplicates:
#   "  Google  " , "github.com" , "GITHUB.com"
# would be THREE different strings, and sort() would put them in
# three different places.

messy = "  GITHUB.com  "
print("raw           :", repr(messy))
print("after strip() :", repr(messy.strip()))
print("after lower() :", repr(messy.strip().lower()))
# raw           : '  GITHUB.com  '
# after strip() : 'GITHUB.com'
# after lower() : 'github.com'

print("--- the trap: strip does NOT touch the middle ---")
print(repr("git hub.com".strip()))      # inner space survives
print(repr("GitHub.com".lower()))       # only the CAPITALS change
# 'git hub.com'
# 'github.com'

# strip() is not a "fix my text" tool. It only trims the edges. And
# lower() does not remove spaces, it only changes the letters. Each
# one does exactly one small job.

# ============================================================
# [4] The empty input trap
# ============================================================
# A real user will press Enter without typing anything. Then
# input() returns "", and after strip() it is still "".
#
# Appending "" would put a BLANK line in the list, and the program
# would claim it added a website when it added nothing. Worse, the
# place would still be consumed, so the user silently loses a slot.

blank = "   "
print("empty input, before:", repr(blank))
print("empty input, after :", repr(blank.strip()), "-> length", len(blank.strip()))
# empty input, before: '   '
# empty input, after : '' -> length 0

# The lesson does not handle this, but a real program must check it
# BEFORE append(). We use `if not website:` which is True for an
# empty string, and also for "0" and 0, so be careful with numbers.

# ============================================================
# [5] The duplicate trap
# ============================================================
# Nothing stops the user from typing the same site twice. In real
# life you check with `in` first, exactly like lesson 45, so the
# list never holds the same address twice.

saved = ["google", "github.com"]

print("'github.com' in saved :", "github.com" in saved)
print("'twitter.com' in saved:", "twitter.com" in saved)
# 'github.com' in saved : True
# 'twitter.com' in saved: False

# So the honest version of the adding step is:
#
#   website = input(...).strip().lower()
#   if not website:
#       print("Nothing was typed, that place is not used")
#   elif website in my_websites:
#       print(f"{website} is already saved")
#   else:
#       my_websites.append(website)
#       maximum -= 1        # only a REAL new site uses a place
#
# Notice maximum -= 1 sits in the else branch. If the user types a
# duplicate and we still decreased the counter, the program would
# end early with empty places and no way to fill them.

# ============================================================
# [6] Sorting before printing
# ============================================================
# sort() puts the strings in alphabetical order and changes the
# list IN PLACE, it does not return a new list. So this works:
#
#   my_websites.sort()            <- no assignment!
#
# This is a real difference from sorted(), which returns a new list
# and leaves the original alone.

numbers = [3, 1, 2]
print("before sort() :", numbers)
result = numbers.sort()           # returns None, not a list!
print("after sort()  :", numbers)
print("what sort() returned:", result)
# before sort() : [3, 1, 2]
# after sort()  : [1, 2, 3]
# what sort() returned: None

print("--- sorted() instead: the original is NOT touched ---")
original = [3, 1, 2]
copy = sorted(original)
print("original :", original, "| copy :", copy)
# original : [3, 1, 2] | copy : [1, 2, 3]

names = ["Zaid", "ahmed", "Mona", "Bashar"]
print("--- sorting is CASE SENSITIVE ---")
print("as typed   :", names)
print("after sort :", sorted(names))
print("after lower first:", sorted(n.lower() for n in names))
# as typed   : ['Zaid', 'ahmed', 'Mona', 'Bashar']
# after sort : ['Bashar', 'Mona', 'Zaid', 'ahmed']
# after lower first: ['ahmed', 'bashar', 'mona', 'zaid']

# Look at the second line: "Zaid" comes BEFORE "ahmed", because in
# ASCII every capital letter has a smaller code than every small one.
# This is the SECOND reason we call lower() while reading the input.
# Cleaning at input time fixes the display AND the sorting at once.

# ============================================================
# [7] Printing the list with numbers
# ============================================================
# We use a SECOND while loop here, exactly as the lesson says. It
# walks the sorted list using an index, and the index is the brake.

sorted_websites = ["github.com", "google", "python.org", "stackoverflow", "www.example.com"]

index = 0

while index < len(sorted_websites):
    print(f"{index + 1}. {sorted_websites[index]}")
    index += 1
# 1. github.com
# 2. google
# 3. python.org
# 4. stackoverflow
# 5. www.example.com

print("All Bookmarks Printed Successfully")
# All Bookmarks Printed Successfully

# Why a while and not the one from section [2]? Because this loop
# counts UP through a list that already has a known length, which is
# the exact shape from lesson 48. Two loops, two different jobs:
# the first collects while counting DOWN free places, the second
# prints while counting UP through the list.

# ============================================================
# [8] The full program, ready to type into
# ============================================================
# This is the real program. It waits for input(), so it cannot be
# tested by running the file, but read it as the finished version.
# Every line above that used a fake list appears here for real.

def bookmark_manager(maximum=5):
    """Collect websites one by one, then print them sorted."""

    my_websites = []

    while maximum > 0:
        website = input("Please type your website: ").strip().lower()

        if not website:
            print("Nothing typed, this place is not used")
            continue                      # does NOT use a place

        if website in my_websites:
            print(f"{website} is already saved")
            continue                      # does NOT use a place

        my_websites.append(website)
        maximum -= 1
        print(f"Website Added, You Have {maximum} Places Left")

    my_websites.sort()

    index = 0
    while index < len(my_websites):
        print(f"{index + 1}. {my_websites[index]}")
        index += 1

    print("All Bookmarks Printed Successfully")
    return my_websites

# `continue` is the important word in the two early exits above. It
# jumps straight to the next while check WITHOUT running the rest of
# the body, so maximum -= 1 and the "Website Added" message are both
# skipped. We cover continue properly in the next lesson.

# ============================================================
# [9] Testable version, no input() inside
# ============================================================
# Putting input() inside the function makes it impossible to test
# automatically. Moving the asking part out lets us check the real
# collecting logic with a plain list of answers.

def add_website(my_websites, maximum, raw_input):
    """Try to add one raw input. Return the new maximum."""
    website = raw_input.strip().lower()

    if not website:
        return maximum                      # nothing typed, no place used
    if website in my_websites:
        return maximum                      # duplicate, no place used

    my_websites.append(website)
    maximum -= 1
    return maximum

def collect(answers, maximum=5):
    """Run the collecting loop over a list of answers."""
    my_websites = []
    for raw in answers:
        if maximum <= 0:                    # belt and braces
            break
        maximum = add_website(my_websites, maximum, raw)
    my_websites.sort()
    return my_websites

print("--- the normal case ---")
print(collect(["  Google  ", "Python.org", "  GITHUB.com", "www.Example.com", "stackoverflow"]))
# ['github.com', 'google', 'python.org', 'stackoverflow', 'www.example.com']

print("--- a blank answer does NOT waste a place ---")
print(collect(["google", "   ", "python.org"]))
# ['google', 'python.org']

print("--- a duplicate does NOT waste a place ---")
print(collect(["google", "GOOGLE", "  google  ", "python.org"]))
# ['google', 'python.org']

print("--- only 3 places available, 5 answers given ---")
print(collect(["a.com", "b.com", "c.com", "d.com", "e.com"], maximum=3))
# ['a.com', 'b.com', 'c.com']

print("--- the exact same answers, without the cleaning rules ---")
naive = ["  Google  ", "GITHUB.com", "  google  "]
print("naive list keeps three near duplicates:", sorted(naive))
# naive list keeps three near duplicates: ['  Google  ', '  google  ', 'GITHUB.com']

# Read that last line carefully, because the ORDER is the lesson.
# sorted() compares character by character, and in ASCII:
#     space = 32   capital A = 65   small a = 97
# So a leading SPACE wins and comes first, and the capital 'G' beats
# the small 'g'. The result looks random to a person, but it is
# perfectly ordered by character code.
#
# The cleaned version of the same three answers gives ONE entry,
# 'github.com', because strip() removed the spaces and lower()
# made the letters match. Three messy strings became one real
# bookmark. That single difference is why both calls matter.

# ============================================================
# SUMMARY
# ============================================================
# - my_websites = [] starts empty, and append() fills it inside the
#   loop.
# - maximum is a count of FREE PLACES, not an index. `while maximum
#   > 0` is the brake, and maximum -= 1 is what makes it stop.
# - This is a different style from counting to len(list). Use it
#   when you do not know the number of items in advance, which is
#   exactly the case with input().
# - strip() trims the two ends only, lower() changes the case only.
#   Neither one fixes the middle of the string.
# - An empty input is not a website. Check `if not website:` before
#   append, or you will "save" a blank string and waste a place.
# - A duplicate is not a new bookmark either. Check `in` first, and
#   only decrease maximum when you really appended something.
# - sort() changes the list in place and returns None. sorted()
#   returns a NEW list and leaves the original alone.
# - Sorting is case sensitive: "Zaid" sorts before "ahmed". Cleaning
#   with lower() at input time fixes both the display and the order.
# - The printing loop counts UP with an index, the collecting loop
#   counts DOWN with free places. Two loops, two different jobs.
# - continue skips the rest of the body, which is how we reject a
#   bad input without spending a place. Full coverage next lesson.

# ============================================================
# NEXT LESSON: break and continue inside the while loop
# ============================================================