# -----------------------------------------------------------------
# Lesson 100: Python re -- search, findall and finditer
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : standard re module, first Match object,
#            span/string/group details, email-like search,
#            all matches, iteration and capture groups
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: apply Regular Expressions in
# Python with its built-in re module.
#
#   IMPORT [00:36] -- import re
#   search() [00:51-01:17] -- first match only; returns a
#   Match object or None; inspect span(), string and group()
#   EMAIL [05:05-05:25] -- search for an email-shaped
#   address and use if/else to report the result
#   findall() / finditer() [07:26-08:04] -- find all
#   matches; findall returns a list (empty if none)
#   FILTER [08:49] -- scan supplied text entries and
#   collect valid-shaped addresses in a separate list
#   GROUPS [11:19] -- capturing groups change what
#   findall() returns
#
# No input() here: sample submissions are fixed for
# reproducible output. The email pattern is a simplified
# shape check, not a complete standards validator.

import re

# ============================================================
# [1] Import the standard re module [00:36]
# ============================================================
# re is part of the Python standard library:

print(f"  re module imported: {re.__name__ == 're'}")
print(f"  search available: {callable(re.search)}")
print(f"  findall available: {callable(re.findall)}")
#   re module imported: True
#   search available: True
#   findall available: True

# ============================================================
# [2] search(): first match only [00:51-01:17]
# ============================================================
# Search for digits in a string with several digit runs:

source_text = "Order 42, box 7"
first_match = re.search(r"\d+", source_text)

print(f"  first match found: {first_match is not None}")
print(f"  first matching text: {first_match.group()}")
#   first match found: True
#   first matching text: 42

# search() stops at the first match; it does not return
# every digit group.

# ============================================================
# [3] Match span(): where it matched [01:17]
# ============================================================
# span() returns (start, end), with end exclusive:

print(f"  match span: {first_match.span()}")
print(f"  start index: {first_match.start()}")
print(f"  end index: {first_match.end()}")
print(f"  slice equals match: {source_text[first_match.start():first_match.end()] == first_match.group()}")
#   match span: (6, 8)
#   start index: 6
#   end index: 8
#   slice equals match: True

# The matched substring is source_text[6:8]; the ending
# index points just after the match.

# ============================================================
# [4] Match string() and group() [01:17]
# ============================================================
# string is the original searched text; group() is the
# exact text that matched:

print(f"  original string: {first_match.string}")
print(f"  matched group: {first_match.group()}")
print(f"  group equals slice: {first_match.group() == source_text[6:8]}")
#   original string: Order 42, box 7
#   matched group: 42
#   group equals slice: True

# One Match object carries both the input and the match.

# ============================================================
# [5] search() returns None when absent
# ============================================================
# If no match exists, search() returns None -- check
# before calling group():

no_digits = re.search(r"\d+", "no numbers here")
print(f"  absent match is None: {no_digits is None}")

if no_digits is not None:
    absent_result = no_digits.group()
else:
    absent_result = "no match"

print(f"  if/else result: {absent_result}")
#   absent match is None: True
#   if/else result: no match

# ============================================================
# [6] Email-shaped search [05:05]
# ============================================================
# Reuse a teaching-level address pattern: search locates
# an address-shaped substring inside larger text:

email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"
message = "Please contact team@example.com today"
email_match = re.search(email_pattern, message)

if email_match:
    email_result = "email-shaped address found"
else:
    email_result = "no email-shaped address"

print(f"  if/else: {email_result}")
print(f"  extracted address: {email_match.group()}")
#   if/else: email-shaped address found
#   extracted address: team@example.com

# search() can find the address inside a sentence; unlike
# fullmatch(), the whole message need not be an address.

# ============================================================
# [7] Validate a whole supplied string
# ============================================================
# To check whether the entire entry has the email shape,
# use fullmatch() rather than search():

entries = ("name@domain.com", "prefix name@domain.com", "bad-address")
entry_results = [re.fullmatch(email_pattern, item) is not None for item in entries]

print(f"  whole-entry validation: {entry_results}")
print(f"  ordinary address accepted: {entry_results[0]}")
print(f"  surrounding text rejected: {not entry_results[1]}")
#   whole-entry validation: [True, False, False]
#   ordinary address accepted: True
#   surrounding text rejected: True

# search() finds a part; fullmatch() checks the entire
# value. That distinction matters for validation.

# ============================================================
# [8] findall(): every match as a list [07:26-08:04]
# ============================================================
# The same text, all digit runs:

all_matches = re.findall(r"\d+", source_text)
none_matches = re.findall(r"\d+", "nothing numeric")

print(f"  findall results: {all_matches}")
print(f"  list type: {type(all_matches).__name__}")
print(f"  no matches gives empty list: {none_matches == []}")
#   findall results: ['42', '7']
#   list type: list
#   no matches gives empty list: True

# Unlike search(), findall() gathers every match, or []
# if there are none.

# ============================================================
# [9] finditer(): every match as Match objects [07:26]
# ============================================================
# finditer() returns an iterator of Match objects, each
# with group and span information:

digit_matches = list(re.finditer(r"\d+", source_text))
iter_texts = [item.group() for item in digit_matches]
iter_spans = [item.span() for item in digit_matches]

print(f"  finditer texts: {iter_texts}")
print(f"  finditer spans: {iter_spans}")
print(f"  each item is a Match: {all(isinstance(item, re.Match) for item in digit_matches)}")
#   finditer texts: ['42', '7']
#   finditer spans: [(6, 8), (14, 15)]
#   each item is a Match: True

# finditer combines all matches with the Match-object
# details taught in sections [3]-[4].

# ============================================================
# [10] Groups change findall() results [11:19]
# ============================================================
# With one capturing group, findall returns that group's
# text; with two, it returns tuples:

pair_text = "AB-12 CD-34"
one_group = re.findall(r"([A-Z]+)-\d+", pair_text)
two_groups = re.findall(r"([A-Z]+)-(\d+)", pair_text)
no_capture = re.findall(r"(?:[A-Z]+)-\d+", pair_text)

print(f"  one capturing group: {one_group}")
print(f"  two capturing groups: {two_groups}")
print(f"  non-capturing group: {no_capture}")
#   one capturing group: ['AB', 'CD']
#   two capturing groups: [('AB', '12'), ('CD', '34')]
#   non-capturing group: ['AB-12', 'CD-34']

# A capturing group changes what findall returns; (?:...)
# groups the pattern without changing the returned match.

# ============================================================
# [11] Filter a batch of email entries [08:49]
# ============================================================
# Model several supplied entries without input():
# search for an email-shaped substring, then store just
# the captured addresses in their own list:

submissions = (
    "name@domain.com",
    "bad entry",
    "Contact: support@example.org",
    "also@broken",
    "two: a@one.com and b@two.net",
)
valid_addresses = []

for submission in submissions:
    found = re.search(email_pattern, submission)
    if found:
        valid_addresses.append(found.group())

print(f"  submissions scanned: {len(submissions)}")
print(f"  first email per submission: {valid_addresses}")
print(f"  first-match count: {len(valid_addresses)}")
#   submissions scanned: 5
#   first email per submission: ['name@domain.com', 'support@example.org', 'a@one.com']
#   first-match count: 3

# The loop finds the first address in each entry; the
# last entry contains two, so use findall() to collect
# ALL addresses from each submission:

all_valid_addresses = []
for submission in submissions:
    all_valid_addresses.extend(re.findall(email_pattern, submission))

print(f"  all matches collected: {all_valid_addresses}")
#   all matches collected: ['name@domain.com', 'support@example.org', 'a@one.com', 'b@two.net']

# ============================================================
# [12] One session: choose the right tool
# ============================================================
# The main operations side by side:

print(f"  search first: {first_match.group()}")
print(f"  search span: {first_match.span()}")
print(f"  findall all: {all_matches}")
print(f"  finditer count: {len(digit_matches)}")
print(f"  captured group result: {one_group}")
print(f"  filtered emails: {len(all_valid_addresses)}")
#   search first: 42
#   search span: (6, 8)
#   findall all: ['42', '7']
#   finditer count: 2
#   captured group result: ['AB', 'CD']
#   filtered emails: 4

# First Match object -> search; all strings -> findall;
# all Match objects with spans -> finditer.

# ============================================================
# [13] The summary
# ============================================================
# Python's re module, from the transcript:
#
#   1. IMPORT [00:36] -- import re (built-in standard
#      library module)
#   2. search() [00:51-01:17] -- first match only; Match
#      object or None
#   3. MATCH DETAILS -- span() gives (start, end),
#      string is the original text, group() is the match
#   4. EMAIL [05:05-05:25] -- search() locates an
#      address-shaped substring; if/else reports it
#   5. fullmatch() -- checks the entire input; search()
#      only needs a matching substring
#   6. findall() [07:26-08:04] -- all matching strings
#      in a list; no matches -> []
#   7. finditer() -- all Match objects, retaining groups
#      and spans for each match
#   8. GROUPS [11:19] -- one capture returns strings;
#      multiple captures return tuples; (?:...) groups
#      without capturing
#   9. FILTER [08:49] -- loop over supplied entries and
#      store matching email-shaped strings separately
#  10. LIMIT -- this email regex checks shape only, not
#      full standards compliance or mailbox existence
#
# Search asks "where is the first?"; findall asks "what
# are all the matches?"; finditer asks "where is each?".
