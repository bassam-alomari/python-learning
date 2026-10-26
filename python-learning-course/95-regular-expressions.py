# -----------------------------------------------------------------
# Lesson 95: regular expressions -- search text by pattern
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : re patterns for searching, validating and
#            extracting; metacharacters, repetitions,
#            email / phone / credit-card / IP examples,
#            and interactive tester workflow
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: Regular Expressions, commonly
# shortened to RegEx (التعابير النمطية).
#
#   WHAT [00:13] -- a pattern or template for searching
#   text, validating it, or extracting parts by rules
#   USES [00:13] -- validation examples: email, phone,
#   credit cards and IP addresses
#   METACHARACTERS [03:08] -- digits, upper/lowercase
#   letters, whitespace, and repetition (braces, stars)
#   TESTERS [06:25] -- try patterns in an interactive
#   tester and view matches quickly before using code
#
# Patterns here are teaching examples, not production
# security validators. All sample strings are fixed;
# outputs are booleans or deliberately extracted text.

import re

# ============================================================
# [1] What RegEx does [00:13]
# ============================================================
# One pattern can search for a rule inside a larger string:

message = "Order 482 is ready"
match = re.search(r"\d+", message)

print(f"  pattern found: {match is not None}")
print(f"  matched text: {match.group()}")
#   pattern found: True
#   matched text: 482

# \d means a digit; + means one or more. search() looks
# anywhere in the supplied text.

# ============================================================
# [2] Search, validate, extract
# ============================================================
# The three tasks named in the transcript, using one
# fixed input:

text = "Contact: team@example.com"
email_match = re.search(r"[\w.]+@[\w.]+", text)
is_email = re.fullmatch(r"[\w.]+@[\w.]+", "team@example.com")
all_words = re.findall(r"\w+", text)

print(f"  search found email-like text: {email_match is not None}")
print(f"  full input matches pattern: {is_email is not None}")
print(f"  extracted words: {all_words}")
#   search found email-like text: True
#   full input matches pattern: True
#   extracted words: ['Contact', 'team', 'example', 'com']

# search finds a piece; fullmatch checks the entire
# string; findall extracts every match.

# ============================================================
# [3] Digits and character classes [03:08]
# ============================================================
# Character classes describe which single characters
# are allowed:

sample = "A7 z"
print(f"  digits: {re.findall(r'\d', sample)}")
print(f"  uppercase letters: {re.findall(r'[A-Z]', sample)}")
print(f"  lowercase letters: {re.findall(r'[a-z]', sample)}")
print(f"  whitespace matches: {len(re.findall(r'\s', sample))}")
#   digits: ['7']
#   uppercase letters: ['A']
#   lowercase letters: ['z']
#   whitespace matches: 1

# \d digit, [A-Z] uppercase range, [a-z] lowercase
# range, \s whitespace.

# ============================================================
# [4] Useful shorthand metacharacters [03:08]
# ============================================================
# \w is a word character, \D is a non-digit,
# \S is a non-whitespace character:

code = "AB-29"
print(f"  word characters: {re.findall(r'\w', code)}")
print(f"  non-digits: {re.findall(r'\D', code)}")
print(f"  non-spaces: {re.findall(r'\S+', 'red blue')}")
#   word characters: ['A', 'B', '2', '9']
#   non-digits: ['A', 'B', '-']
#   non-spaces: ['red', 'blue']

# Complements are uppercase: \D means not a digit,
# \S means not whitespace.

# ============================================================
# [5] Repetition: +, *, ? and braces [03:08]
# ============================================================
# Repeat counts: + one-or-more, * zero-or-more,
# ? optional, {m,n} a bounded count:

sample = "a aa aaa b"
print(f"  a+ matches: {re.findall(r'a+', sample)}")
print(f"  a* matches: {re.findall(r'a*', 'ba')}")
print(f"  optional color: {bool(re.fullmatch(r'colou?r', 'color'))}")
print(f"  exactly three digits: {bool(re.fullmatch(r'\d{3}', '482'))}")
print(f"  two to four digits: {bool(re.fullmatch(r'\d{2,4}', '482'))}")
#   a+ matches: ['a', 'aa', 'aaa']
#   a* matches: ['', 'a', '']
#   optional color: True
#   exactly three digits: True
#   two to four digits: True

# * can match an empty string too; {3} means exactly
# three; {2,4} means at least two, at most four.

# ============================================================
# [6] Anchors and boundaries
# ============================================================
# ^ and $ mark the beginning and end; \b marks a word
# boundary:

print(f"  starts with Python: {bool(re.search(r'^Python', 'Python 3'))}")
print(f"  ends with 3: {bool(re.search(r'3$', 'Python 3'))}")
print(f"  whole word cat: {bool(re.search(r'\bcat\b', 'a cat naps'))}")
print(f"  not whole word cat: {bool(re.search(r'\bcat\b', 'catalog'))}")
#   starts with Python: True
#   ends with 3: True
#   whole word cat: True
#   not whole word cat: False

# Anchors constrain position; boundaries distinguish a
# whole word from the same letters inside a longer word.

# ============================================================
# [7] Email-like validation [00:13]
# ============================================================
# A teaching pattern for a simple address shape. Real
# email standards are much broader:

email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
emails = ("learner@example.com", "not-an-email")

for address in emails:
    print(f"  {address}: {bool(re.fullmatch(email_pattern, address))}")
#   learner@example.com: True
#   not-an-email: False

# fullmatch means the entire address must fit the pattern;
# this is illustrative, not a complete email-spec parser.

# ============================================================
# [8] Phone-like validation [00:13]
# ============================================================
# A simplified North-American-style phone example:

phone_pattern = r"\d{3}-\d{3}-\d{4}"
phones = ("555-123-4567", "55-123-4567")

for phone in phones:
    print(f"  {phone}: {bool(re.fullmatch(phone_pattern, phone))}")
#   555-123-4567: True
#   55-123-4567: False

# The exact count in braces checks the shape, not whether
# the number is assigned or reachable.

# ============================================================
# [9] Credit-card-shaped text and IP addresses [00:13]
# ============================================================
# Simple shape checks only -- not payment validation or
# a complete IPv4 parser:

card_pattern = r"\d{4}-\d{4}-\d{4}-\d{4}"
ip_pattern = r"\d{1,3}(?:\.\d{1,3}){3}"

print(f"  card-shaped: {bool(re.fullmatch(card_pattern, '1234-5678-9012-3456'))}")
print(f"  IP-shaped: {bool(re.fullmatch(ip_pattern, '192.168.1.10'))}")
print(f"  malformed IP shape: {bool(re.fullmatch(ip_pattern, '192.168.1'))}")
#   card-shaped: True
#   IP-shaped: True
#   malformed IP shape: False

# A shape match does not check card validity, nor whether
# each IPv4 octet is in the 0..255 range. Production
# validation needs more than this starter pattern.

# ============================================================
# [10] Groups: extract structured parts
# ============================================================
# Parentheses capture sub-parts; findall returns them:

date_text = "Meeting: 2026-10-26"
date_parts = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_text)

print(f"  year: {date_parts.group(1)}")
print(f"  month: {date_parts.group(2)}")
print(f"  day: {date_parts.group(3)}")
print(f"  full date: {date_parts.group(0)}")
#   year: 2026
#   month: 10
#   day: 26
#   full date: 2026-10-26

# Capturing groups turn a match into useful fields.

# ============================================================
# [11] Replace text with sub()
# ============================================================
# sub(pattern, replacement, text) replaces each match:

masked = re.sub(r"\d", "*", "Card 4821")
cleaned = re.sub(r"\s+", " ", "one   two\nthree")

print(f"  digits masked: {masked}")
print(f"  whitespace normalized: {cleaned}")
#   digits masked: Card ****
#   whitespace normalized: one two three

# The same pattern language can find, validate, extract
# and transform text.

# ============================================================
# [12] RegEx testers [06:25]
# ============================================================
# The transcript recommends trying patterns in a live
# tester before putting them in code. These checks model
# that workflow locally and reproducibly:

tester_pattern = r"\d{3}-\d{2}"
tester_samples = ("482-19", "48-219")
tester_results = [
    bool(re.fullmatch(tester_pattern, item))
    for item in tester_samples
]

print(f"  tester pattern: {tester_pattern}")
print(f"  tester results: {tester_results}")
print(f"  first sample matches: {tester_results[0]}")
print(f"  second sample rejected: {not tester_results[1]}")
#   tester pattern: \d{3}-\d{2}
#   tester results: [True, False]
#   first sample matches: True
#   second sample rejected: True

# A web tester visualizes matches interactively; the
# local loop gives the same pattern/sample iteration
# without relying on an external website.

# ============================================================
# [13] The summary
# ============================================================
# Regular Expressions, from the transcript:
#
#   1. WHAT [00:13] -- a pattern for searching,
#      validating and extracting text by rules
#   2. USES [00:13] -- email, phone, credit-card and IP
#      examples; the lesson's patterns check shape only
#   3. METACHARACTERS [03:08] -- \d digits, [A-Z]
#      uppercase, [a-z] lowercase, \s whitespace,
#      \w word characters and complements \D / \S
#   4. REPETITION [03:08] -- + one-or-more, * zero-or-
#      more, ? optional, {n} exact count, {m,n} range
#   5. POSITION -- ^ start, $ end, \b word boundary
#   6. FIND -- search() locates a match within text;
#      findall() returns all matches
#   7. VALIDATE -- fullmatch() requires all input to fit
#      the pattern
#   8. EXTRACT -- parentheses capture groups for fields
#   9. TRANSFORM -- sub() replaces matched text
#  10. TESTERS [06:25] -- try a pattern against sample
#      strings interactively before using it in code
#  11. LIMITS -- a shape match is not full validation:
#      email syntax, card authorization and IP ranges
#      need stronger domain-specific checks
#
# A RegEx is a compact rule for text; test the rule
# against both matching and non-matching examples.
