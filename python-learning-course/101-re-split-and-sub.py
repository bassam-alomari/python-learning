# -----------------------------------------------------------------
# Lesson 101: Python re -- split and substitute text
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : re.split() into a list, split by whitespace
#            or punctuation, maxsplit, re.sub() replacement,
#            and the count limit
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: two useful functions from re --
# re.split() and re.sub().
#
#   split() [00:15-00:26] -- divide text into a list of
#   strings wherever a pattern matches
#   maxsplit [01:27] -- limit how many splits occur
#   sub() [06:35-06:46] -- replace pattern matches with
#   replacement text; count limits replacements
#
# Samples are fixed for deterministic output. split and
# sub work on text patterns, not literal separators only.

import re

# ============================================================
# [1] re.split(): split at a pattern [00:15-00:26]
# ============================================================
# Split a sentence on whitespace:

sentence = "split this sentence"
words = re.split(r"\s+", sentence)

print(f"  split result: {words}")
print(f"  result type: {type(words).__name__}")
print(f"  parts count: {len(words)}")
#   split result: ['split', 'this', 'sentence']
#   result type: list
#   parts count: 3

# re.split returns a list of strings between matches.

# ============================================================
# [2] Split on whitespace runs
# ============================================================
# \s+ treats one or many spaces as one delimiter:

messy_spaces = "red   green\tblue"
clean_parts = re.split(r"\s+", messy_spaces)

print(f"  whitespace split: {clean_parts}")
print(f"  three words: {len(clean_parts) == 3}")
#   whitespace split: ['red', 'green', 'blue']
#   three words: True

# A tab is whitespace too; the plus quantifier groups
# consecutive whitespace into one separator.

# ============================================================
# [3] Split on punctuation [01:27]
# ============================================================
# A character class can treat comma, semicolon or pipe
# as separators:

record = "red,green;blue|gold"
items = re.split(r"[,;|]", record)

print(f"  punctuation split: {items}")
print(f"  item count: {len(items)}")
#   punctuation split: ['red', 'green', 'blue', 'gold']
#   item count: 4

# Inside the class, each listed punctuation character
# is an alternative separator.

# ============================================================
# [4] maxsplit: cap the number of splits [01:27]
# ============================================================
# maxsplit=1 splits only at the first matching space:

text = "one two three four"
one_split = re.split(r"\s+", text, maxsplit=1)
two_splits = re.split(r"\s+", text, maxsplit=2)

print(f"  maxsplit 1: {one_split}")
print(f"  maxsplit 2: {two_splits}")
print(f"  remaining text preserved: {one_split[1] == 'two three four'}")
#   maxsplit 1: ['one', 'two three four']
#   maxsplit 2: ['one', 'two', 'three four']
#   remaining text preserved: True

# maxsplit limits splits, not the length of the result;
# the unsplit remainder stays together as the last part.

# ============================================================
# [5] maxsplit=0 means no limit
# ============================================================
# The default is zero, which means split at every match:

default_split = re.split(r"-", "a-b-c")
zero_split = re.split(r"-", "a-b-c", maxsplit=0)

print(f"  default split: {default_split}")
print(f"  maxsplit zero: {zero_split}")
print(f"  same result: {default_split == zero_split}")
#   default split: ['a', 'b', 'c']
#   maxsplit zero: ['a', 'b', 'c']
#   same result: True

# ============================================================
# [6] re.sub(): replace matches [06:35-06:46]
# ============================================================
# Replace every digit with a star:

masked = re.sub(r"\d", "*", "Order 482")

print(f"  substituted text: {masked}")
print(f"  original unchanged: {'Order 482'}")
#   substituted text: Order ***
#   original unchanged: Order 482

# re.sub returns a new string; it does not mutate the
# original string.

# ============================================================
# [7] Replace a pattern, not just one character
# ============================================================
# Replace one-or-more whitespace characters with a
# single space:

normalized = re.sub(r"\s+", " ", "red   green\tblue")
print(f"  normalized spacing: {normalized}")
print(f"  tabs removed: {'\t' not in normalized}")
#   normalized spacing: red green blue
#   tabs removed: True

# The pattern describes what is replaced; the second
# argument supplies the replacement text.

# ============================================================
# [8] sub() count: limit replacements [06:46]
# ============================================================
# count=1 replaces only the first matching digit:

text = "7 cats, 8 dogs, 9 birds"
first_only = re.sub(r"\d", "#", text, count=1)
all_digits = re.sub(r"\d", "#", text)

print(f"  count one: {first_only}")
print(f"  default count: {all_digits}")
#   count one: # cats, 8 dogs, 9 birds
#   default count: # cats, # dogs, # birds

# count=0 (the default) replaces all matches.

# ============================================================
# [9] Split and keep delimiters with a capture
# ============================================================
# Capturing the delimiter includes it in the split list:

parts_with_separators = re.split(r"([,;])", "a,b;c")
print(f"  captured separators: {parts_with_separators}")
#   captured separators: ['a', ',', 'b', ';', 'c']

# Parentheses capture delimiters in split(); a
# non-capturing group would not include them.

# ============================================================
# [10] Build a readable cleanup pipeline
# ============================================================
# Normalize whitespace, then split into fields:

raw_line = "  Ada   Lovelace,  analyst  "
normalized_line = re.sub(r"\s+", " ", raw_line).strip()
fields = re.split(r"\s*,\s*", normalized_line)

print(f"  normalized line: {normalized_line}")
print(f"  fields: {fields}")
#   normalized line: Ada Lovelace, analyst
#   fields: ['Ada Lovelace', 'analyst']

# sub() cleans spacing; split() separates on the comma
# and any adjacent whitespace.

# ============================================================
# [11] Practical: redact selected information
# ============================================================
# Replace a simple phone-shaped number, but only once:

contact_text = "Call 555-123-4567 or 555-987-6543"
redacted = re.sub(r"\d{3}-\d{3}-\d{4}", "[PHONE]", contact_text, count=1)

print(f"  first number redacted: {redacted}")
print(f"  second number remains: {'555-987-6543' in redacted}")
#   first number redacted: Call [PHONE] or 555-987-6543
#   second number remains: True

# This shows count limiting a multi-character pattern;
# real privacy redaction needs a complete data policy.

# ============================================================
# [12] One session: split vs substitute
# ============================================================
# split divides; sub replaces. Same source text, two jobs:

source = "north|south|east"
split_result = re.split(r"\|", source, maxsplit=1)
sub_result = re.sub(r"\|", ", ", source, count=1)

print(f"  split: {split_result}")
print(f"  substitute: {sub_result}")
print(f"  split returns list: {isinstance(split_result, list)}")
print(f"  sub returns string: {isinstance(sub_result, str)}")
#   split: ['north', 'south|east']
#   substitute: north, south|east
#   split returns list: True
#   sub returns string: True

# ============================================================
# [13] The summary
# ============================================================
# re.split() and re.sub(), from the transcript:
#
#   1. split() [00:15-00:26] -- divide text into a list
#      wherever the regex pattern matches
#   2. WHITESPACE -- \s+ splits on one or many spaces;
#      tabs are included
#   3. PUNCTUATION [01:27] -- [,;|] treats listed
#      punctuation as alternative delimiters
#   4. maxsplit [01:27] -- caps how many divisions occur;
#      remainder stays together; zero means no limit
#   5. sub() [06:35-06:46] -- replace pattern matches
#      with the replacement string; original is unchanged
#   6. count -- sub count=1 replaces only the first match;
#      default zero replaces all
#   7. CAPTURED DELIMITERS -- a capturing group in split
#      inserts the delimiter into the result list
#   8. PIPELINE -- sub() can normalize text before split()
#   9. PRACTICAL -- count can limit redaction of a
#      multi-character pattern too
#
# split() turns matches into boundaries; sub() turns
# matches into replacement text.
