# -----------------------------------------------------------------
# Lesson 96: regular expressions -- quantifiers
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : *, +, ?, {n}, {n,m}; repetition counts,
#            greedy vs lazy matching, and a practical
#            phone-number pattern explained piece by piece
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: continue Regular Expressions
# with Quantifiers (المحددات الكمية).
#
#   WHAT [00:13] -- symbols that say how many times a
#   character or sub-pattern must repeat
#   COMMON FORMS [02:31] -- * zero or more, + one or more,
#   ? zero or one, {n} exactly n, {n,m} from n through m
#   PRACTICE [07:11] -- combine quantifiers into a complete
#   phone/data pattern and validate it in code
#   TESTERS [08:38] -- use a RegEx tester such as Regex101
#   to inspect each pattern part and practice interactively
#
# All samples are fixed and deterministic. These phone
# patterns validate a teaching format, not real phone
# assignment or reachability.

import re

# ============================================================
# [1] What a quantifier controls [00:13]
# ============================================================
# A quantifier follows a character or group and controls
# how many repetitions the pattern accepts:

print("  quantifier: controls how many repeats match")
print("  it follows a character or grouped pattern")
#   quantifier: controls how many repeats match
#   it follows a character or grouped pattern

# ============================================================
# [2] Star: zero or more [02:31]
# ============================================================
# * accepts none, one, or many copies:

pattern = r"ab*c"
samples = ("ac", "abc", "abbbc", "abbx")
results = [bool(re.fullmatch(pattern, item)) for item in samples]

print(f"  pattern ab*c: {results}")
print(f"  zero b accepted: {results[0]}")
print(f"  many b accepted: {results[2]}")
#   pattern ab*c: [True, True, True, False]
#   zero b accepted: True
#   many b accepted: True

# The b is repeated zero-or-more times between a and c.

# ============================================================
# [3] Plus: one or more [02:31]
# ============================================================
# + requires at least one repetition:

pattern = r"ab+c"
samples = ("ac", "abc", "abbbc")
results = [bool(re.fullmatch(pattern, item)) for item in samples]

print(f"  pattern ab+c: {results}")
print(f"  zero b rejected: {not results[0]}")
print(f"  one or more accepted: {results[1] and results[2]}")
#   pattern ab+c: [False, True, True]
#   zero b rejected: True
#   one or more accepted: True

# ============================================================
# [4] Question mark: optional [02:31]
# ============================================================
# ? accepts zero or one copy:

pattern = r"colou?r"
samples = ("color", "colour", "colouur")
results = [bool(re.fullmatch(pattern, item)) for item in samples]

print(f"  optional u: {results}")
print(f"  both spellings accepted: {results[0] and results[1]}")
print(f"  repeated u rejected: {not results[2]}")
#   optional u: [True, True, False]
#   both spellings accepted: True
#   repeated u rejected: True

# ============================================================
# [5] Exact count: {n} [02:31]
# ============================================================
# {3} means exactly three repetitions:

pattern = r"\d{3}"
samples = ("482", "48", "4821")
results = [bool(re.fullmatch(pattern, item)) for item in samples]

print(f"  exactly three digits: {results}")
print(f"  three accepted: {results[0]}")
print(f"  two rejected: {not results[1]}")
print(f"  four rejected: {not results[2]}")
#   exactly three digits: [True, False, False]
#   three accepted: True
#   two rejected: True
#   four rejected: True

# ============================================================
# [6] Range count: {n,m} [02:31]
# ============================================================
# {2,4} allows two, three, or four digits:

pattern = r"\d{2,4}"
samples = ("4", "42", "482", "4821", "48210")
results = [bool(re.fullmatch(pattern, item)) for item in samples]

print(f"  two-to-four digits: {results}")
print(f"  both ends accepted: {results[1] and results[3]}")
print(f"  outside range rejected: {not results[0] and not results[4]}")
#   two-to-four digits: [False, True, True, True, False]
#   both ends accepted: True
#   outside range rejected: True

# The lower and upper bounds are inclusive.

# ============================================================
# [7] Quantifiers apply to the preceding token
# ============================================================
# Parentheses group a whole sequence so its quantifier
# repeats that entire sequence:

pair_pattern = r"(ha){2,3}"
samples = ("haha", "hahaha", "ha", "hahahaha")
results = [bool(re.fullmatch(pair_pattern, item)) for item in samples]

print(f"  repeated (ha) pairs: {results}")
print(f"  group repeats two or three times: {results[0] and results[1]}")
#   repeated (ha) pairs: [True, True, False, False]
#   group repeats two or three times: True

# Without parentheses, the quantifier would apply only
# to the immediately preceding character.

# ============================================================
# [8] Greedy and lazy quantifiers
# ============================================================
# By default, repetition is greedy (takes as much as it
# can); adding ? makes it lazy (takes as little as it can):

text = "<one><two>"
greedy = re.search(r"<.*>", text).group()
lazy = re.search(r"<.*?>", text).group()

print(f"  greedy match: {greedy}")
print(f"  lazy match: {lazy}")
print(f"  greedy is longer: {len(greedy) > len(lazy)}")
#   greedy match: <one><two>
#   lazy match: <one>
#   greedy is longer: True

# The extra ? modifies the * quantifier's preference;
# it does not mean optional in this combined form.

# ============================================================
# [9] Build a phone-format pattern [07:11]
# ============================================================
# Example format: three digits, hyphen, three digits,
# hyphen, four digits:

phone_pattern = r"\d{3}-\d{3}-\d{4}"
phones = ("555-123-4567", "55-123-4567", "555-123-456")
results = [bool(re.fullmatch(phone_pattern, item)) for item in phones]

print(f"  phone pattern: {phone_pattern}")
print(f"  phone format results: {results}")
#   phone pattern: \d{3}-\d{3}-\d{4}
#   phone format results: [True, False, False]

# Three quantifiers define each digit group precisely;
# the literal hyphens define separators.

# ============================================================
# [10] Explain the phone pattern part by part [07:11]
# ============================================================
# Break the complete pattern into readable components:

parts = (r"\d{3}", "-", r"\d{3}", "-", r"\d{4}")
print(f"  part 1: {parts[0]} means three digits")
print(f"  part 2: {parts[1]} is a literal hyphen")
print(f"  part 3: {parts[2]} means three digits")
print(f"  part 4: {parts[3]} is a literal hyphen")
print(f"  part 5: {parts[4]} means four digits")
#   part 1: \d{3} means three digits
#   part 2: - is a literal hyphen
#   part 3: \d{3} means three digits
#   part 4: - is a literal hyphen
#   part 5: \d{4} means four digits

# Read left to right: a digit group, separator, group,
# separator, final group.

# ============================================================
# [11] Optional country code and whitespace
# ============================================================
# Combine ? and * with bounded digit groups for a
# teaching format that accepts an optional +1 prefix:

international_pattern = r"(?:\+1 )?\d{3}-\d{3}-\d{4}"
numbers = ("555-123-4567", "+1 555-123-4567", "+44 555-123-4567")
results = [bool(re.fullmatch(international_pattern, item)) for item in numbers]

print(f"  optional +1 prefix: {results}")
print(f"  no prefix and +1 accepted: {results[0] and results[1]}")
print(f"  other country code rejected: {not results[2]}")
#   optional +1 prefix: [True, True, False]
#   no prefix and +1 accepted: True
#   other country code rejected: True

# (?:...) groups without capturing; ? makes the whole
# prefix optional. The fixed digit groups stay exact.

# ============================================================
# [12] Regex tester workflow [08:38]
# ============================================================
# The transcript mentions Regex101 and similar testers:
# enter a pattern, try examples, inspect why they match.
# Reproduce that practice as a fixed local test table:

tester_cases = (
    ("555-123-4567", True),
    ("555-12-4567", False),
    ("555-123-456", False),
)
tester_passed = [
    bool(re.fullmatch(phone_pattern, sample)) == expected
    for sample, expected in tester_cases
]

print(f"  tester cases: {len(tester_cases)}")
print(f"  each expected result matched: {all(tester_passed)}")
print(f"  matches / rejects shown: {tester_passed}")
#   tester cases: 3
#   each expected result matched: True
#   matches / rejects shown: [True, True, True]

# In an online tester you can see match highlights and
# pattern explanations live; this table makes the same
# matching/non-matching checks repeatable in the lesson.

# ============================================================
# [13] The summary
# ============================================================
# Quantifiers, from the transcript:
#
#   1. WHAT [00:13] -- operators that set how many times
#      a character or grouped pattern repeats
#   2. * [02:31] -- zero or more (ab*c accepts ac)
#   3. + [02:31] -- one or more (ab+c rejects ac)
#   4. ? [02:31] -- zero or one (colou?r accepts both
#      color and colour, but not colouur)
#   5. {n} [02:31] -- exactly n (\d{3})
#   6. {n,m} [02:31] -- inclusive range (\d{2,4})
#   7. GROUPS -- parentheses make the quantifier repeat
#      a complete sequence, as in (ha){2,3}
#   8. GREEDY / LAZY -- .* takes the longest match;
#      .*? takes the shortest match
#   9. PRACTICE [07:11] -- phone format \d{3}-\d{3}-\d{4};
#      each quantifier and literal separator explained
#  10. OPTIONAL PREFIX -- (?:\+1 )? makes the country
#      prefix optional while preserving fixed groups
#  11. TESTERS [08:38] -- Regex101 and similar tools let
#      you try patterns and inspect matches live; local
#      test cases prove both accepted and rejected inputs
#
# Quantifiers answer "how many?"; test the boundary
# cases as carefully as the ordinary match.
