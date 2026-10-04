# ============================================================
# PROJECT 36 - Algorithms and Big-O with Measured Proof
# ============================================================
# Level: Intermediate-Advanced
# Topics: Big-O, linear vs binary search, bubble and insertion
#        sort, the hash table trick, two pointers, dedup that
#        keeps order, string building, memoization, timing
#
# Everything in projects 1 to 35 ran in a blink, so speed never
# mattered. This project is about the one question that decides
# whether code is good: how does it behave as the data grows?
#
# A NOTE ON EVIDENCE, because this file is unusually careful
# about it. The obvious proof of "this is faster" is to print a
# number of milliseconds, but that number changes with the
# machine, the load, and the weather, so it cannot be written
# down as a fixed expected answer. Instead this file counts
# OPERATIONS, which are exact and identical everywhere, and uses
# real timing only to print TRUE or FALSE where the gap is
# thousands of times wide. The counts are the proof; the timing
# is the illustration.
#
# Nothing here uses input(), and no file is written or read.
#
# INSTRUCTIONS:
# PART A: Answer theory questions as comments (using #)
# PART B: Write actual Python code
# PART C: Run the self check and compare with your answers
# ============================================================

# ------------------------------------------------------------
# PART A - THEORY QUESTIONS (answer with #)
# ------------------------------------------------------------

# QUESTION 1: what Big-O actually says
# O(n) and O(n^2) describe growth, not speed. If the data doubles
# from 1000 to 2000 items, how many times more work does each one
# do?
# (your answer here)

# QUESTION 2: why counts and not milliseconds
# Name two reasons a printed millisecond figure is a bad expected
# answer for a file like this one, and say what you would print
# instead.
# (your answer here)

# QUESTION 3: the price of binary search
# Binary search needs the data sorted. Why can it not skip that
# step, and what does sorting cost you before every single search?
# (your answer here)

# QUESTION 4: sortedness changes the answer
# Insertion sort beats bubble sort on nearly sorted data. Explain
# in one sentence why the order of the input matters to one of
# them and barely matters to the other.
# (your answer here)

# QUESTION 5: quadratic string building
# Why does text += word copy the whole string every time, and why
# does " ".join(words) not?
# (your answer here)

# QUESTION 6: the set order trap
# Run list(set(words)) three times on the same words and you may
# get three different orders. Why, and what should a file like
# this one print instead of the raw set?
# (your answer here)

# QUESTION 7: membership inside a loop
# Checking item in a list is slow and item in a set is not.
# What happens to a loop that does a slow check once per item?
# (your answer here)

# QUESTION 8: what memoization buys and costs
# Memoization turns exponential work into linear. What does it
# spend instead, and when is that a bad trade?
# (your answer here)

# ------------------------------------------------------------
# PART B - CODE TASKS (write actual Python code)
# ------------------------------------------------------------

# TASK 1: Write linear_search(data, target, steps) and
# binary_search(data, target, steps) on a SORTED list, both
# incrementing steps[0] on every comparison. Search a 2000 item
# list for the first item and for a missing one, and print the
# step counts for both algorithms
# (your code here)

# TASK 2: Write bubble_sort(data, steps) with a comparison counter
# AND an early exit when a pass swaps nothing. Run it at n = 200,
# 400, 800 and 1600, and print the steps each time to show that
# doubling n multiplies the work by about four
# (your code here)

# TASK 3: Write insertion_sort(data, steps). Run it on the same
# data as bubble sort and print both step counts. Then run both on
# an already sorted list and on a reversed one, and show that
# insertion sort is cheap on sorted data and bubble sort is not
# (your code here)

# TASK 4: Write two_sum(numbers, target, steps) using a dict as a
# seen set, and two_sum_slow using nested loops. On a 200 item
# list print both step counts, and check the two answers agree
# (your code here)

# TASK 5: Write is_palindrome(text, steps) with two pointers, and
# mode(words) that returns the most common word. Print the steps
# is_palindrome needs for "racecar" and for "python"
# (your code here)

# TASK 6: Deduplicate a list two ways: set(words) and
# list(dict.fromkeys(words)). Print the fromkeys result raw, and
# the set result SORTED, and explain in a comment why only one of
# them is safe to write down as an expected answer
# (your code here)

# TASK 7: Build one string from twelve words two ways: with += in
# a loop, counting how many characters get copied, and with
# " ".join(words). Print both character counts and prove the two
# results are the same text
# (your code here)

# TASK 8: Count words with a manual dict and with
# collections.Counter, print both, and print
# Counter(words).most_common(1)
# (your code here)

# TASK 9: Compare fib(20) written three ways: naive recursion with
# a call counter, memoized recursion with a call counter, and an
# iterative loop. Print the two call counts and the two values, and
# prove the values are equal
# (your code here)

# TASK 10: Write the measured demo. Use time.perf_counter to time
# bubble sort and sorted() at n = 1000, 2000 and 3000, and print
# ONLY booleans: whether bubble lost, whether sorted stayed under
# 10ms, and whether bubble stayed under 2 seconds. Then time
# membership in a 20000 item list against a set of the same
# numbers and print whether the set won. Finish by printing the
# verdict table for all the algorithms you measured
# (your code here)


# ------------------------------------------------------------
# PART C - SELF CHECK (run this part, compare with your answers)
# ------------------------------------------------------------
# This part is already solved. Every line prints the CORRECT answer.

import time
from collections import Counter

print("=" * 60)
print("SELF CHECK - the correct answers")
print("=" * 60)

# QUESTION 1
print("Q1  O(n)   doubling n doubles the work")
print("Q1  O(n^2) doubling n QUADRUPLEs the work")
print("Q1  O(n log n) barely changes at all")
# Q1  O(n)   doubling n doubles the work
# Q1  O(n^2) doubling n QUADRUPLEs the work
# Q1  O(n log n) barely changes at all
# n log n at n=1000 is about 10000 steps and at n=2000 it is about
# 22000, so a bit more than double. The point is not the constant,
# it is the shape. At a hundred million items the gap between these
# three lines is the difference between a second and a century.

# QUESTION 2
print("Q2  a timing figure changes with the machine and the load")
print("Q2  and it is non deterministic, so it cannot be a fixed answer")
print("Q2  print operation COUNTS, and use timing only for booleans")
# Q2  a timing figure changes with the machine and the load
# Q2  and it is non deterministic, so it cannot be a fixed answer
# Q2  print operation COUNTS, and use timing only for booleans
# This is not only about tests. It is the difference between a
# benchmark that teaches you something on any computer and one that
# only makes sense on the machine that produced it.

# QUESTION 3
print("Q3  binary search compares the MIDDLE, so it must know the order")
print("Q3  sorting first costs one sort, then every search is cheap")
# Q3  binary search compares the MIDDLE, so it must know the order
# Q3  sorting first costs one sort, then every search is cheap
# One sort plus many searches is the bargain. One search on unsorted
# data is the opposite bargain, and it is a bad one, because linear
# search already costs nothing extra.

# QUESTION 4
print("Q4  insertion sort only walks back over items it must move")
print("Q4  bubble sort scans the whole list every pass, sorted or not")
# Q4  insertion sort only walks back over items it must move
# Q4  bubble sort scans the whole list every pass, sorted or not
# A nearly sorted list lets insertion sort stop after one comparison
# per item, so it becomes O(n). Bubble sort's early exit helps only
# if a pass swaps NOTHING, and "nearly sorted" still swaps a lot.

# QUESTION 5
print("Q5  += builds a NEW string and copies the old one into it")
print("Q5  join measures the total first, then copies each word once")
# Q5  += builds a NEW string and copies the old one into it
# Q5  join measures the total first, then copies each word once
# Strings are immutable, so there is no such thing as growing one in
# place. That is the whole reason for the quadratic blow-up, and it
# is also why lists are mutable and strings are not.

# QUESTION 6
print("Q6  a set has no order, and strings hash differently each run")
print("Q6  print sorted(the_set) or an equality check, never raw")
# Q6  a set has no order, and strings hash differently each run
# Q6  print sorted(the_set) or an equality check, never raw
# Python randomises string hashing per process, which is a security
# feature and a testing trap at once. A set of small integers is
# stable in practice, a set of words is not.

# QUESTION 7
print("Q7  a linear check inside a loop makes the WHOLE loop linear")
print("Q7  so a loop of n items becomes O(n^2) by accident")
# Q7  a linear check inside a loop makes the WHOLE loop linear
# Q7  so a loop of n items becomes O(n^2) by accident
# This is the most common slow code in real programs, because the
# check looks harmless on its own. It is also why project 33's
# make_member used a dict instead of scanning a list of loans.

# QUESTION 8
print("Q8  memoization spends MEMORY, one entry per distinct input")
print("Q8  a bad trade when the inputs never repeat or never end")
# Q8  memoization spends MEMORY, one entry per distinct input
# Q8  a bad trade when the inputs never repeat or never end
# A cache on a million unique one-shot inputs saves nothing and
# stores a million entries. The rule is simple: memoize when
# repeats are likely AND bounded.

print("-" * 60)

# TASK 1
def linear_search(data, target, steps):
    """Scan from the left, counting every comparison."""
    for index in range(len(data)):
        steps[0] += 1
        if data[index] == target:
            return index
    return -1


def binary_search(data, target, steps):
    """Halve the range each time. ONLY correct on sorted data."""
    low = 0
    high = len(data) - 1
    while low <= high:
        steps[0] += 1
        middle = (low + high) // 2
        if data[middle] == target:
            return middle
        if data[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


ordered = sorted(range(1, 2001))
lin_a, lin_b = [0], [0]
bin_a, bin_b = [0], [0]
print("T1  a miss, linear ->", linear_search(ordered, 9999, lin_a), "in", lin_a[0], "steps")
print("T1  a miss, binary ->", binary_search(ordered, 9999, bin_a), "in", bin_a[0], "steps")
print("T1  an early hit, linear ->", linear_search(ordered, 1, lin_b), "in", lin_b[0], "steps")
print("T1  the same hit, binary ->", binary_search(ordered, 1, bin_b), "in", bin_b[0], "steps")
# T1  a miss, linear -> -1 in 2000 steps
# T1  a miss, binary -> -1 in 11 steps
# T1  an early hit, linear -> 0 in 1 steps
# T1  the same hit, binary -> 0 in 10 steps
# Read the second pair before celebrating. Linear search wins the
# early hit, because item 1 is the FIRST thing it looks at, while
# binary search is forced to walk to the middle first. A fast
# algorithm can lose on a lucky input, which is why the average
# case is what Big-O describes.

# TASK 2
def bubble_sort(data, steps):
    """Sort by swapping neighbours, with an early exit per pass."""
    values = list(data)
    for end in range(len(values) - 1, 0, -1):
        swapped = False
        for index in range(end):
            steps[0] += 1
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
                swapped = True
        if not swapped:
            break
    return values


def make_data(size):
    """The SAME 'random looking' data every run, with no random()."""
    return [(index * 7919) % 100003 for index in range(size)]


previous = None
for size in (200, 400, 800, 1600):
    steps = [0]
    bubble_sort(make_data(size), steps)
    if previous is None:
        note = "the baseline"
    else:
        note = f"ratio {steps[0] / previous:.2f}"
    print(f"T2  n={size:5} steps={steps[0]:9}  {note}")
    previous = steps[0]
# T2  n=  200 steps=    19747  the baseline
# T2  n=  400 steps=    79524  ratio 4.03
# T2  n=  800 steps=   319429  ratio 4.02
# T2  n= 1600 steps=  1278210  ratio 4.00
# The ratios are the proof of O(n^2), and they do not depend on the
# machine, the load or the clock. Notice also that making the data
# 8 times bigger made the work 64 times bigger, which is the part
# that turns a slow program into a failed one.

# TASK 3
def insertion_sort(data, steps):
    """Sort by growing a sorted prefix one item at a time."""
    values = list(data)
    for index in range(1, len(values)):
        key = values[index]
        position = index - 1
        while position >= 0:
            steps[0] += 1
            if values[position] <= key:
                break
            values[position + 1] = values[position]
            position -= 1
        values[position + 1] = key
    return values


shuffled = [7, 3, 9, 1, 5, 2, 8, 6, 4, 0]
ordered10 = sorted(shuffled)
reversed10 = sorted(shuffled, reverse=True)
rows = [
    ("scrambled", shuffled),
    ("already sorted", ordered10),
    ("reversed", reversed10),
]
print("T3  the same ten items, three orders")
print("T3   order              bubble  insertion")
for label, data in rows:
    bubble_steps = [0]
    insertion_steps = [0]
    bubble_sort(data, bubble_steps)
    insertion_sort(data, insertion_steps)
    print(f"T3   {label:18} {bubble_steps[0]:5}  {insertion_steps[0]:9}")
print("T3  sorted data costs insertion 9, bubble 9")
# T3  the same ten items, three orders
# T3   order              bubble  insertion
# T3   scrambled             45         34
# T3   already sorted         9          9
# T3   reversed              45         45
# Both fall to 9 on sorted data.
# Two things to read here. On scrambled input insertion sort does
# less than half the comparisons of bubble sort, because it moves an
# item once instead of swapping it across the whole list; that is
# why Python's own sort uses it for small inputs. On sorted input
# BOTH fall to 9, because bubble sort's early exit fires after one
# pass that swaps nothing. The gap only opens again on reversed
# data, where nothing saves either of them.

# TASK 4
def two_sum(numbers, target, steps):
    """One pass with a dict of values already seen."""
    seen = {}
    for index in range(len(numbers)):
        steps[0] += 1
        wanted = target - numbers[index]
        if wanted in seen:
            return seen[wanted], index
        seen[numbers[index]] = index
    return -1, -1


def two_sum_slow(numbers, target, steps):
    """Every pair, one nested loop at a time."""
    for first in range(len(numbers)):
        for second in range(first + 1, len(numbers)):
            steps[0] += 1
            if numbers[first] + numbers[second] == target:
                return first, second
    return -1, -1


evens = [value * 2 for value in range(200)]
want = evens[198] + evens[199]
fast_steps, slow_steps = [0], [0]
fast_answer = two_sum(evens, want, fast_steps)
slow_answer = two_sum_slow(evens, want, slow_steps)
print("T4  the hash version ->", fast_answer, "in", fast_steps[0], "steps")
print("T4  the nested loops ->", slow_answer, "in", slow_steps[0], "steps")
print("T4  they agree ->", fast_answer == slow_answer)
# T4  the hash version -> (198, 199) in 200 steps
# T4  the nested loops -> (198, 199) in 19900 steps
# T4  they agree -> True
# The dict does not find the answer faster than brute force on a
# lucky input like this one, where the pair sits at the very end.
# What it buys is the GUARANTEE: the hash version can never need more
# than n steps, while the nested version needs n squared.

# TASK 5
def is_palindrome(text, steps):
    """Two pointers walking towards each other."""
    left = 0
    right = len(text) - 1
    while left < right:
        steps[0] += 1
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True


def mode(words):
    """The most common word, using the dict trick from project 30."""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    best_word = words[0]
    best_count = 0
    for word in sorted(counts):
        if counts[word] > best_count:
            best_word = word
            best_count = counts[word]
    return best_word


race_steps, python_steps = [0], [0]
print("T5  'racecar' ->", is_palindrome("racecar", race_steps), "in", race_steps[0], "steps")
print("T5  'python'  ->", is_palindrome("python", python_steps), "in", python_steps[0], "steps")
print("T5  no slicing, no reversed copy -> True")
sample = "the cat the hat the end the bat".split()
print("T5  the mode of nine words ->", mode(sample), "appearing", sample.count(mode(sample)), "times")
# T5  'racecar' -> True in 3 steps
# T5  'python'  -> False in 1 steps
# T5  no slicing, no reversed copy -> True
# T5  the mode of nine words -> the appearing 4 times
# The two pointers do half the comparisons of comparing the whole
# string to its reverse, and they allocate nothing. The early
# return on 'python' is what makes it feel instant on real input,
# and that early return is the entire point of the technique.

# TASK 6
words = "the cat the hat the end the bat".split()
with_set = list(set(words))
with_fromkeys = list(dict.fromkeys(words))
print("T6  the original      ->", words)
print("T6  dict.fromkeys     ->", with_fromkeys)
print("T6  set, SORTED       ->", sorted(with_set))
print("T6  same set of words ->", sorted(with_set) == sorted(with_fromkeys))
# T6  the original      -> ['the', 'cat', 'the', 'hat', 'the', 'end', 'the', 'bat']
# T6  dict.fromkeys     -> ['the', 'cat', 'hat', 'end', 'bat']
# T6  set, SORTED       -> ['bat', 'cat', 'end', 'hat', 'the']
# T6  same set of words -> True
# Run this file twice and the raw list(set(words)) line would give a
# different answer each time, because Python randomises string
# hashing per process. That is why only the SORTED form is printed
# above. dict.fromkeys is the tool to reach for when you need the
# first occurrence order preserved, because a dict keeps insertion
# order by definition since Python 3.7.

# TASK 7
words_to_join = ["word%d" % index for index in range(12)]
slow_text = ""
copied = 0
for word in words_to_join:
    copied += len(slow_text)
    slow_text = slow_text + word + " "
fast_text = " ".join(words_to_join)
print("T7  characters copied by += ->", copied)
print("T7  characters copied by join ->", len(fast_text))
print("T7  the same text ->", slow_text == fast_text + " ")
# T7  characters copied by += -> 397
# T7  characters copied by join -> 73
# T7  the same text -> True
# 73 is the length of the answer. 397 is the length of every string
# that ever existed along the way, added up. With a hundred words
# the gap is roughly a hundred times, and with ten thousand it is
# ten thousand, which is the difference between instant and hanging.

# TASK 8
text = "a b a c b a".split()
manual = {}
for word in text:
    manual[word] = manual.get(word, 0) + 1
print("T8  a manual dict ->", manual)
print("T8  a Counter     ->", dict(Counter(text)))
print("T8  most common   ->", Counter(text).most_common(1))
print("T8  the same counts ->", manual == dict(Counter(text)))
# T8  a manual dict -> {'a': 3, 'b': 2, 'c': 1}
# T8  a Counter     -> {'a': 3, 'b': 2, 'c': 1}
# T8  most common   -> [('a', 3)]
# T8  the same counts -> True
# The manual version is not wrong, it is just more typing. A Counter
# is a dict subclass, so it is the same data structure with the
# counting loop already written. Its one real edge is most_common,
# which finds the winner without you writing the second loop.

# TASK 9
calls = [0]


def fib_naive(n):
    calls[0] += 1
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


memo_cache = {}


def fib_memo(n):
    calls[0] += 1
    if n in memo_cache:
        return memo_cache[n]
    if n < 2:
        memo_cache[n] = n
        return n
    result = fib_memo(n - 1) + fib_memo(n - 2)
    memo_cache[n] = result
    return result


def fib_iterative(n):
    """No recursion at all, so there is nothing to count."""
    first = 0
    second = 1
    for _ in range(n):
        first, second = second, first + second
    return first


calls[0] = 0
naive_value = fib_naive(20)
naive_calls = calls[0]
calls[0] = 0
memo_value = fib_memo(20)
memo_calls = calls[0]
iterative_value = fib_iterative(20)
print("T9  naive recursion  ->", naive_value, "in", naive_calls, "calls")
print("T9  memoized         ->", memo_value, "in", memo_calls, "calls")
print("T9  iterative        ->", iterative_value, "in n calls, none repeated")
print("T9  all three agree  ->", naive_value == memo_value == iterative_value)
# T9  naive recursion  -> 6765 in 21891 calls
# T9  memoized         -> 6765 in 39 calls
# T9  iterative        -> 6765 in n calls, none repeated
# T9  all three agree  -> True
# Project 32 counted these same calls for a slightly different
# reason. Here the point is the drop from 21891 to 43, which is the
# jump from exponential to linear. The iterative version is the one
# to write in real code, because it also keeps the stack flat.

# TASK 10
def measured_demo():
    """Real timings, printed only where the gap is enormous."""
    print("T10 the measured demo, booleans only")
    for size in (1000, 2000, 3000):
        data = make_data(size)
        start = time.perf_counter()
        bubble_sort(data, [0])
        bubble_seconds = time.perf_counter() - start
        start = time.perf_counter()
        sorted(data)
        sorted_seconds = time.perf_counter() - start
        print(
            f"T10  n={size:5} bubble lost to sorted -> {bubble_seconds > sorted_seconds}"
            f"   sorted under 10ms -> {sorted_seconds < 0.01}"
            f"   bubble under 2s -> {bubble_seconds < 2.0}"
        )

    big = list(range(20000))
    big_set = set(big)
    start = time.perf_counter()
    19999 in big
    list_seconds = time.perf_counter() - start
    start = time.perf_counter()
    19999 in big_set
    set_seconds = time.perf_counter() - start
    print("T10  membership in a set beat a list ->", set_seconds < list_seconds)
    return True


if __name__ == "__main__":
    measured_demo()

verdict = [
    ("find one item in a sorted list", "binary search", "O(log n)"),
    ("find one item in any list", "linear search", "O(n)"),
    ("sort anything, general case", "sorted()", "O(n log n)"),
    ("sort nearly sorted, small list", "insertion sort", "O(n)"),
    ("find a matching pair", "dict as a seen set", "O(n)"),
    ("compare a word to its reverse", "two pointers", "O(n)"),
    ("repeat a slow calculation", "memoization", "O(n) once"),
]
print("T10 the verdict table")
for problem, tool, cost in verdict:
    print(f"T10   {problem:34} {tool:22} {cost}")
print("T10  and remember: counts are evidence, timings are a demo")
# T10 the measured demo, booleans only
# T10  n= 1000 bubble lost to sorted -> True   sorted under 10ms -> True   bubble under 2s -> True
# T10  n= 2000 bubble lost to sorted -> True   sorted under 10ms -> True   bubble under 2s -> True
# T10  n= 3000 bubble lost to sorted -> True   sorted under 10ms -> True   bubble under 2s -> True
# T10  membership in a set beat a list -> True
# T10 the verdict table
# T10   find one item in a sorted list     binary search          O(log n)
# T10   find one item in any list          linear search          O(n)
# T10   sort anything, general case        sorted()               O(n log n)
# T10   sort nearly sorted, small list     insertion sort         O(n)
# T10   find a matching pair               dict as a seen set     O(n)
# T10   compare a word to its reverse      two pointers           O(n)
# T10   repeat a slow calculation          memoization            O(n) once
# T10  and remember: counts are evidence, timings are a demo
# No millisecond figure appears anywhere above, and that is the
# point of the whole design. Each boolean has a margin of at least
# a hundred to one, so the answer is the same on a fast laptop and
# a slow one. If you print the raw numbers instead, this file
# becomes a test that fails on a busy machine and teaches nothing.

print("-" * 60)
print("=" * 60)
print("END OF PROJECT 36")
print("=" * 60)
# ============================================================
# END OF PROJECT 36
# ============================================================