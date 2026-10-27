# -----------------------------------------------------------------
# Lesson 98: RegEx assertions -- anchors and email patterns
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : ^ start and $ end assertions, whole-string
#            validation, email components, pattern tests,
#            and a part-by-part tester-style explanation
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: continue Regular Expressions
# with Assertions and Email Pattern design.
#
#   ASSERTIONS [00:08] -- boundaries that check WHERE a
#   pattern occurs in a string
#   CARET ^ [03:31] -- beginning of the string/line
#   DOLLAR $ [03:31] -- end of the string/line; no extra
#   characters after the match
#   EMAIL [06:00] -- username @ domain . extension
#   TESTERS [10:50] -- inspect each pattern part and try
#   accepted and rejected examples in an online tester
#
# The email regex below is a teaching-level shape check,
# not a full implementation of every valid email syntax,
# and does not prove that an address exists.

import re

# ============================================================
# [1] Assertions check position [00:08]
# ============================================================
# Anchors don't consume characters; they assert a
# position where the match must begin or end:

print("  assertions check where a pattern matches")
print("  anchors assert positions, not extra characters")
#   assertions check where a pattern matches
#   anchors assert positions, not extra characters

# ============================================================
# [2] Caret ^: the beginning [03:31]
# ============================================================
# Without ^, search finds a match anywhere; with ^, it
# must begin at the start:

text = "prefix: cat"
anywhere = re.search(r"cat", text)
at_start = re.search(r"^cat", text)

print(f"  unanchored search finds cat: {anywhere is not None}")
print(f"  ^cat matches at start: {at_start is not None}")
print(f"  ^cat matches a starting string: {re.search(r'^cat', 'cat nap') is not None}")
#   unanchored search finds cat: True
#   ^cat matches at start: False
#   ^cat matches a starting string: True

# ============================================================
# [3] Dollar $: the end [03:31]
# ============================================================
# $ requires the match to end at the end of the string:

ends_here = re.search(r"cat$", "nap cat")
extra_after = re.search(r"cat$", "cat nap")

print(f"  cat$ at end: {ends_here is not None}")
print(f"  cat$ rejects trailing text: {extra_after is None}")
print(f"  unanchored cat finds prefix: {re.search(r'cat', 'cat nap') is not None}")
#   cat$ at end: True
#   cat$ rejects trailing text: True
#   unanchored cat finds prefix: True

# ============================================================
# [4] Anchor both ends for full input
# ============================================================
# ^...$ checks the whole string; fullmatch() is the
# direct Python API equivalent for whole-input matching:

pattern = r"^\d{3}$"
samples = ("482", "x482", "482x")
anchored = [bool(re.search(pattern, item)) for item in samples]
whole = [bool(re.fullmatch(r"\d{3}", item)) for item in samples]

print(f"  anchored results: {anchored}")
print(f"  fullmatch results: {whole}")
print(f"  both methods agree: {anchored == whole}")
#   anchored results: [True, False, False]
#   fullmatch results: [True, False, False]
#   both methods agree: True

# Anchors reject any prefix or suffix; only exactly three
# digits survive.

# ============================================================
# [5] Newline detail: string vs line anchors
# ============================================================
# By default, ^ and $ refer to the whole string. With
# MULTILINE, they can refer to each line:

multiline_text = "first\nsecond"
whole_start = re.findall(r"^\w+", multiline_text)
each_line_start = re.findall(r"^\w+", multiline_text, re.MULTILINE)

print(f"  default start matches: {whole_start}")
print(f"  MULTILINE start matches: {each_line_start}")
#   default start matches: ['first']
#   MULTILINE start matches: ['first', 'second']

# This clarifies the transcript's "line/string" wording:
# MULTILINE changes anchors to work per line.

# ============================================================
# [6] Email pattern: begin with the local part [06:00]
# ============================================================
# A teaching pattern, assembled from username, @,
# domain and extension components:

email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$"
print(f"  pattern: {email_pattern}")
print(f"  begins with ^: {email_pattern.startswith('^')}")
print(f"  ends with $: {email_pattern.endswith('$')}")
#   pattern: ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$
#   begins with ^: True
#   ends with $: True

# ^ locks the beginning; $ locks the end. The pieces
# between them must account for the entire address.

# ============================================================
# [7] Email part 1: username
# ============================================================
# [A-Za-z0-9._%+-]+ means one or more allowed username
# characters in this simplified pattern:

username_pattern = r"[A-Za-z0-9._%+-]+"
usernames = ("first.last+tag", "", "bad name")
username_results = [bool(re.fullmatch(username_pattern, item)) for item in usernames]

print(f"  username component matches: {username_results}")
print(f"  allowed punctuation included: {username_results[0]}")
#   username component matches: [True, False, False]
#   allowed punctuation included: True

# ============================================================
# [8] Email part 2: @, domain, extension
# ============================================================
# @ is literal; the domain has dot-separated labels;
# escaped dots \.; the final suffix has at least 2 letters:

print(f"  @ is literal in pattern: {'@' in email_pattern}")
print(f"  escaped dot before extension: {r'\.' in email_pattern}")
print(f"  extension uses {2} or more letters: {'{2,}' in email_pattern}")
#   @ is literal in pattern: True
#   escaped dot before extension: True
#   extension uses 2 or more letters: True

# Escaped dot means an actual period, not the regex
# wildcard that matches any character. The domain supports
# dot-separated labels, followed by a final letter suffix.

# ============================================================
# [9] Validate addresses with both anchors [06:00]
# ============================================================
# Try accepted and rejected shapes:

addresses = (
    "name@domain.com",
    "user+tag@mail.example.org",
    "missing-at-sign.example.com",
    "name@domain",
    "name@domain.c",
    "name@domain.com.extra",
)
email_results = [bool(re.fullmatch(email_pattern, item)) for item in addresses]

for address, accepted in zip(addresses, email_results):
    print(f"  {address}: {accepted}")
#   name@domain.com: True
#   user+tag@mail.example.org: True
#   missing-at-sign.example.com: False
#   name@domain: False
#   name@domain.c: False
#   name@domain.com.extra: True

# The last form is accepted as a multi-label domain
# (domain.com) plus a final suffix (extra). The regex checks
# shape; it does not decide whether a domain is sensible.

# ============================================================
# [10] Capturing the email components
# ============================================================
# Add groups to see the local part, domain and suffix:

parts_pattern = r"^([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+)\.([A-Za-z]{2,})$"
parts_match = re.fullmatch(parts_pattern, "name@domain.com")

print(f"  username: {parts_match.group(1)}")
print(f"  domain: {parts_match.group(2)}")
print(f"  extension: {parts_match.group(3)}")
#   username: name
#   domain: domain
#   extension: com

# Capturing groups make the pattern useful for extracting
# pieces, not just returning True or False.

# ============================================================
# [11] Tester workflow [10:50]
# ============================================================
# As in Regex101: inspect each component and challenge
# the pattern with boundary examples:

test_cases = (
    ("a@b.co", True),
    ("a@b.c", False),
    ("a@b.co!", False),
)
test_results = [
    bool(re.fullmatch(email_pattern, sample)) == expected
    for sample, expected in test_cases
]

print(f"  tester cases: {len(test_cases)}")
print(f"  all expected results: {all(test_results)}")
print(f"  tests passed: {test_results}")
#   tester cases: 3
#   all expected results: True
#   tests passed: [True, True, True]

# Online testers show matches and explain a pattern in
# real time; these local boundary tests make the same
# practice reproducible without a network dependency.

# ============================================================
# [12] Important limit: shape is not proof
# ============================================================
# A pattern can check a format, but cannot prove that a
# mailbox exists or that the user can receive mail:

format_match = bool(re.fullmatch(email_pattern, "name@domain.com"))
mailbox_verified = False

print(f"  address shape matches: {format_match}")
print(f"  mailbox existence proven by regex: {mailbox_verified}")
print(f"  use confirmation for ownership: {format_match and not mailbox_verified}")
#   address shape matches: True
#   mailbox existence proven by regex: False
#   use confirmation for ownership: True

# Production systems typically normalize input, use a
# standards-aware parser, and confirm ownership by sending
# a verification message.

# ============================================================
# [13] The summary
# ============================================================
# Assertions and email patterns, from the transcript:
#
#   1. ASSERTIONS [00:08] -- check match position without
#      consuming characters
#   2. CARET ^ [03:31] -- requires the match at the start;
#      ^cat rejected the prefix example
#   3. DOLLAR $ [03:31] -- requires the match at the end;
#      cat$ rejected trailing text
#   4. WHOLE INPUT -- ^...$ (or fullmatch()) rejects
#      both prefixes and suffixes
#   5. MULTILINE -- by default anchors address the string;
#      re.MULTILINE lets them address each line
#   6. EMAIL [06:00] -- username @ domain . extension,
#      with anchors around the entire sample
#   7. USERNAME -- [A-Za-z0-9._%+-]+, one or more of the
#      simplified allowed characters
#   8. DOMAIN / SUFFIX -- literal @, escaped dot \.,
#      and an extension of at least two letters
#   9. TEST CASES -- correct shapes match; missing @,
#      missing suffix and short suffix reject; tests show
#      where a simplified pattern's limits appear
#  10. CAPTURES -- groups extract name, domain, com
#  11. TESTERS [10:50] -- use an online tester to inspect
#      each part and compare matching/nonmatching samples
#  12. LIMIT -- a regex checks shape, not mailbox
#      existence or ownership; confirm with a message
#
# ^ says where to start; $ says where to stop; the pattern
# between them describes the whole shape to check.
