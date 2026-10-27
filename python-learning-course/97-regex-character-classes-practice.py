# -----------------------------------------------------------------
# Lesson 97: RegEx character classes -- practice drills
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : [ ... ] character sets and ranges, negation
#            with ^, combined classes, custom punctuation
#            and whitespace, challenge then explained solution
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: practical exercises on
# Regular Expression Character Classes.
#
#   REVIEW [00:10] -- square brackets [...] define a set
#   or range of allowed characters: [a-z], [A-Z], [0-9]
#   NEGATION [01:49] -- ^ at the START inside brackets
#   complements the class: [^a-z] means not lowercase
#   COMBINE [02:40] -- mix ranges, custom characters and
#   whitespace to describe a more precise text format
#   CHALLENGE [03:45] -- try the pattern before reading
#   its solution; then explain every component [03:51]
#
# All examples use fixed strings. Character classes
# match one character at a time; repetition is added
# when the exercise needs more than one.

import re

# ============================================================
# [1] Character classes: one allowed character [00:10]
# ============================================================
# A class in [...] matches one character from its set:

lower = re.findall(r"[a-z]", "Hi, Python 3!")
upper = re.findall(r"[A-Z]", "Hi, Python 3!")
digits = re.findall(r"[0-9]", "Hi, Python 3!")

print(f"  lowercase letters: {lower}")
print(f"  uppercase letters: {upper}")
print(f"  digits: {digits}")
#   lowercase letters: ['i', 'y', 't', 'h', 'o', 'n']
#   uppercase letters: ['H', 'P']
#   digits: ['3']

# The range endpoints are included: a-z, A-Z, 0-9.

# ============================================================
# [2] A class can list chosen characters
# ============================================================
# [aeiou] matches any one of the five listed vowels:

vowels = re.findall(r"[aeiou]", "regular expressions")
print(f"  vowels found: {vowels}")
print(f"  vowel count: {len(vowels)}")
#   vowels found: ['e', 'u', 'a', 'e', 'e', 'i', 'o']
#   vowel count: 7

# The bracket means OR among its members: one character
# matching a, e, i, o or u.

# ============================================================
# [3] Combine ranges in one class [02:40]
# ============================================================
# A single class can combine lowercase, uppercase and
# digits; + requires one or more allowed characters:

alphanumeric = re.fullmatch(r"[a-zA-Z0-9]+", "Py3thon")
mixed = re.fullmatch(r"[a-zA-Z0-9]+", "Py-thon")

print(f"  letters and digits accepted: {alphanumeric is not None}")
print(f"  hyphen rejected: {mixed is None}")
#   letters and digits accepted: True
#   hyphen rejected: True

# Classes allow exactly their listed characters --
# punctuation needs to be added explicitly.

# ============================================================
# [4] Negation with ^ [01:49]
# ============================================================
# ^ as the first character inside [...] means "not one
# of these". Here, find every non-lowercase character:

non_lower = re.findall(r"[^a-z]", "abC 7!")
print(f"  not lowercase: {non_lower}")
print(f"  uppercase, space, digit, punctuation: {len(non_lower) == 4}")
#   not lowercase: ['C', ' ', '7', '!']
#   uppercase, space, digit, punctuation: True

# Position matters: ^ inside a class at the beginning
# negates; outside a class it anchors the start of text.

# ============================================================
# [5] Negated class plus repetition
# ============================================================
# [^,]+ captures one or more characters up to a comma:

fields = re.findall(r"[^,]+", "red,green,blue")
print(f"  comma-separated fields: {fields}")
print(f"  field count: {len(fields)}")
#   comma-separated fields: ['red', 'green', 'blue']
#   field count: 3

# The negated class consumes any non-comma character;
# + consumes the run. The delimiter is excluded.

# ============================================================
# [6] Include a literal special character [02:40]
# ============================================================
# Inside a class, a hyphen at the end is literal. Add it
# to letters and digits for a simple ID format:

id_pattern = r"[a-zA-Z0-9-]+"
ids = ("AB-12", "room-7", "bad_id")
id_results = [bool(re.fullmatch(id_pattern, item)) for item in ids]

print(f"  ID format results: {id_results}")
print(f"  hyphen allowed: {id_results[0]}")
print(f"  underscore rejected: {not id_results[2]}")
#   ID format results: [True, True, False]
#   hyphen allowed: True
#   underscore rejected: True

# A hyphen can define a range when between characters;
# at the end of this class it is treated literally.

# ============================================================
# [7] Whitespace in a custom class [02:40]
# ============================================================
# A literal space inside [...] is an allowed character.
# This pattern accepts letters and spaces, but not digits:

name_pattern = r"[A-Za-z ]+"
names = ("Ada Lovelace", "Grace", "Grace 2")
name_results = [bool(re.fullmatch(name_pattern, item)) for item in names]

print(f"  names with spaces: {name_results}")
print(f"  space accepted: {name_results[0]}")
print(f"  digit rejected: {not name_results[2]}")
#   names with spaces: [True, True, False]
#   space accepted: True
#   digit rejected: True

# The space is explicitly included; [A-Za-z] alone
# would not match it.

# ============================================================
# [8] Challenge: pause and solve [03:45]
# ============================================================
# The challenge: find tokens in this text that are made
# of one or more uppercase letters, digits, or hyphens.
#
# Before reading section [9], try to build the pattern:
#   - uppercase range?
#   - digits?
#   - literal hyphen?
#   - one-or-more?
#
# Stop here and solve it yourself first.

challenge_text = "AB-12 cd E9-X"
print(f"  challenge text ready: {challenge_text}")
print("  solve: one or more uppercase letters, digits, hyphens")
#   challenge text ready: AB-12 cd E9-X
#   solve: one or more uppercase letters, digits, hyphens

# ============================================================
# [9] Challenge solution: assemble the class [03:51]
# ============================================================
# Solution: [A-Z0-9-]+ -- allowed characters in brackets,
# then + for a run. Use findall to extract each token:

challenge_pattern = r"[A-Z0-9-]+"
tokens = re.findall(challenge_pattern, challenge_text)

print(f"  solution pattern: {challenge_pattern}")
print(f"  extracted tokens: {tokens}")
#   solution pattern: [A-Z0-9-]+
#   extracted tokens: ['AB-12', 'E9-X']

# The lowercase "cd" did not match, and the space split
# the two tokens -- both outcomes follow from the class.

# ============================================================
# [10] Explain the solution piece by piece [03:51]
# ============================================================
# The pattern has two components:

allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-")
print(f"  uppercase range included: all(letter in allowed for letter in 'AZ') -> {all(letter in allowed for letter in 'AZ')}")
print(f"  digits included: all(digit in allowed for digit in '09') -> {all(digit in allowed for digit in '09')}")
print(f"  hyphen included: {'-' in allowed}")
print(f"  plus means one-or-more: {len(tokens) == 2}")
#   uppercase range included: all(letter in allowed for letter in 'AZ') -> True
#   digits included: all(digit in allowed for digit in '09') -> True
#   hyphen included: True
#   plus means one-or-more: True

# [A-Z] uppercase range, [0-9] digits, - the literal
# hyphen, + one or more allowed characters. findall
# returns each non-overlapping run.

# ============================================================
# [11] A more complex class with a separator
# ============================================================
# Match a product code: two uppercase letters, a literal
# slash, then three digits. The class uses an explicit
# character set for the prefix:

product_pattern = r"[A-Z]{2}/[0-9]{3}"
products = ("AB/482", "A/482", "AB-482")
product_results = [bool(re.fullmatch(product_pattern, item)) for item in products]

print(f"  product code results: {product_results}")
print(f"  exact format accepted: {product_results[0]}")
print(f"  wrong length or separator rejected: {not product_results[1] and not product_results[2]}")
#   product code results: [True, False, False]
#   exact format accepted: True
#   wrong length or separator rejected: True

# Classes choose characters; quantifiers choose counts;
# the slash between them is a literal separator.

# ============================================================
# [12] One session: ranges, negation, challenge
# ============================================================
# The full practice set, condensed:

print(f"  [a-z] count: {len(lower)}")
print(f"  [A-Z] count: {len(upper)}")
print(f"  [0-9] count: {len(digits)}")
print(f"  negated class: {non_lower}")
print(f"  challenge solved: {tokens == ['AB-12', 'E9-X']}")
print(f"  product format solved: {product_results[0] and not any(product_results[1:])}")
#   [a-z] count: 6
#   [A-Z] count: 2
#   [0-9] count: 1
#   negated class: ['C', ' ', '7', '!']
#   challenge solved: True
#   product format solved: True

# The challenge is repeatable: each class and range has
# an accepted example and a rejected edge case.

# ============================================================
# [13] The summary
# ============================================================
# Character Classes practice, from the transcript:
#
#   1. REVIEW [00:10] -- [...] matches one character from
#      its allowed set; [a-z], [A-Z], [0-9] are ranges
#   2. LISTS -- [aeiou] lists chosen characters; ranges
#      can be combined with other characters in one class
#   3. NEGATION [01:49] -- ^ first inside brackets means
#      not these: [^a-z] matched C, space, 7, !
#   4. REPEAT -- add + to consume a run of allowed
#      characters; [^,]+ extracts comma-separated fields
#   5. CUSTOM CHARACTERS [02:40] -- include a literal
#      hyphen or space explicitly; then test both allowed
#      and rejected cases
#   6. CHALLENGE [03:45] -- uppercase/digit/hyphen tokens
#      from "AB-12 cd E9-X"; pause to solve before [9]
#   7. SOLUTION [03:51] -- [A-Z0-9-]+; uppercase range,
#      digits, literal hyphen, and + for one-or-more
#   8. COMBINE -- [A-Z]{2}/[0-9]{3} uses classes for
#      characters, quantifiers for counts, slash as
#      separator
#
# Build a class from allowed characters, negate it with
# ^ when needed, and always test what should NOT match.
