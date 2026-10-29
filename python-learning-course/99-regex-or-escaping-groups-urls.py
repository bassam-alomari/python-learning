# -----------------------------------------------------------------
# Lesson 99: RegEx OR, escaping and groups -- URL patterns
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : alternation with |, literal metacharacters
#            with backslash escaping, groups/subgroups,
#            and a flexible URL-shape example
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: continue RegEx with two key
# topics -- Logical OR and Escaping.
#
#   OR [00:10] -- pipe | allows one alternative or another
#   (apple|orange)
#   GROUPS [00:55] -- parentheses organize alternatives,
#   apply quantifiers and capture sub-parts
#   ESCAPING [01:38] -- backslash makes a metacharacter
#   literal, e.g. \., \*, \?, \(, \)
#   URL PRACTICE [04:44] -- optional http/https and www
#   using OR, escaping and groups
#
# The URL expression below validates an illustrative
# shape only. It does not prove that a URL resolves or
# that a server exists.

import re

# ============================================================
# [1] Logical OR with pipe | [00:10]
# ============================================================
# (apple|orange) matches either word:

fruit_pattern = r"^(apple|orange)$"
fruits = ("apple", "orange", "pear")
fruit_results = [bool(re.fullmatch(fruit_pattern, item)) for item in fruits]

print(f"  OR results: {fruit_results}")
print(f"  apple or orange accepted: {fruit_results[0] and fruit_results[1]}")
print(f"  third option rejected: {not fruit_results[2]}")
#   OR results: [True, True, False]
#   apple or orange accepted: True
#   third option rejected: True

# The pipe separates alternatives; parentheses make the
# alternatives one grouped choice.

# ============================================================
# [2] More than two alternatives
# ============================================================
# Add more choices to the same group:

color_pattern = r"^(red|green|blue)$"
colors = ("red", "green", "blue", "yellow")
color_results = [bool(re.fullmatch(color_pattern, item)) for item in colors]

print(f"  color alternatives: {color_results}")
print(f"  accepted color count: {sum(color_results)}")
#   color alternatives: [True, True, True, False]
#   accepted color count: 3

# ============================================================
# [3] Escaping: special vs literal [01:38]
# ============================================================
# A dot normally means any character. Escaped \.
# matches a literal period:

any_char = re.fullmatch(r"a.b", "a-b")
literal_dot = re.fullmatch(r"a\.b", "a.b")
wrong_literal = re.fullmatch(r"a\.b", "a-b")

print(f"  dot wildcard matches a-b: {any_char is not None}")
print(f"  escaped dot matches a.b: {literal_dot is not None}")
print(f"  escaped dot rejects a-b: {wrong_literal is None}")
#   dot wildcard matches a-b: True
#   escaped dot matches a.b: True
#   escaped dot rejects a-b: True

# ============================================================
# [4] Escape other metacharacters
# ============================================================
# Escape *, ?, and parentheses to find them literally:

literal_pattern = r"\*\?\(\)"
literal_text = "*?()"
literal_match = re.fullmatch(literal_pattern, literal_text)

print(f"  literal symbols match: {literal_match is not None}")
print(f"  pattern escapes four specials: {literal_pattern}")
#   literal symbols match: True
#   pattern escapes four specials: \*\?\(\)

# Without the backslashes, these symbols would act as
# quantifiers or group syntax instead of plain characters.

# ============================================================
# [5] Groups and subgroups [00:55]
# ============================================================
# Parentheses organize a pattern AND capture the text:

contact_pattern = r"(Mr|Ms)\.? ([A-Z][a-z]+)"
contact = re.fullmatch(contact_pattern, "Ms. Jones")

print(f"  complete contact matched: {contact is not None}")
print(f"  title subgroup: {contact.group(1)}")
print(f"  name subgroup: {contact.group(2)}")
#   complete contact matched: True
#   title subgroup: Ms
#   name subgroup: Jones

# (Mr|Ms) is a subgroup: either title; the second group
# captures the name. The escaped dot after the title is
# optional because of ?.

# ============================================================
# [6] Non-capturing groups
# ============================================================
# (?:...) groups alternatives without storing a capture:

prefix_pattern = r"(?:http|https)://"
prefixes = ("http://", "https://", "ftp://")
prefix_results = [bool(re.fullmatch(prefix_pattern, item)) for item in prefixes]

print(f"  protocol alternatives: {prefix_results}")
print(f"  no capture groups stored: {re.fullmatch(prefix_pattern, 'https://').groups() == ()}")
#   protocol alternatives: [True, True, False]
#   no capture groups stored: True

# ?: keeps the grouping behavior but says "do not capture
# this part".

# ============================================================
# [7] URL plan: optional parts [04:44]
# ============================================================
# The requested flexibility: http/https may appear or
# not; www may appear or not; a domain and suffix follow:

url_pattern = r"^(?:(?:https?)://)?(?:www\.)?[A-Za-z0-9-]+\.[A-Za-z]{2,}(?:/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?$"

print(f"  URL pattern starts anchored: {url_pattern.startswith('^')}")
print(f"  URL pattern ends anchored: {url_pattern.endswith('$')}")
print(f"  protocol group optional: {'(?:https?)://' in url_pattern}")
print(f"  www dot escaped: {'www\\.' in url_pattern}")
#   URL pattern starts anchored: True
#   URL pattern ends anchored: True
#   protocol group optional: True
#   www dot escaped: True

# (?:https?):// accepts http or https; the outer ? makes
# the whole protocol optional. www\. is optional too.

# ============================================================
# [8] Test URLs with different optional parts [04:44]
# ============================================================
# Four common shapes: neither prefix, protocol only,
# www only, both protocol and www:

urls = (
    "example.com",
    "https://example.com",
    "www.example.com",
    "http://www.example.com",
    "https://www.example.com/path?q=1",
)
url_results = [bool(re.fullmatch(url_pattern, item)) for item in urls]

for address, accepted in zip(urls, url_results):
    print(f"  {address}: {accepted}")
#   example.com: True
#   https://example.com: True
#   www.example.com: True
#   http://www.example.com: True
#   https://www.example.com/path?q=1: True

# The last optional group accepts a simple path/query
# character run after the domain.

# ============================================================
# [9] URL pattern: protocol and www groups
# ============================================================
# Explain the beginning of the expression:

protocol_group = r"(?:(?:https?)://)?"
www_group = r"(?:www\.)?"

print(f"  protocol group: {protocol_group}")
print(f"  www group: {www_group}")
print(f"  both prefixes optional: {protocol_group.endswith('?') and www_group.endswith('?')}")
#   protocol group: (?:(?:https?)://)?
#   www group: (?:www\.)?
#   both prefixes optional: True

# Inner (?:https?) chooses http or https; the outer group
# plus ? makes that entire protocol optional. www\.? is
# actually the literal www. prefix, optional as a group.

# ============================================================
# [10] Capturing domain and extension subgroups
# ============================================================
# A simpler grouped URL pattern can extract its core:

domain_pattern = r"^(?:https?://)?(?:www\.)?([A-Za-z0-9-]+)\.([A-Za-z]{2,})$"
domain_match = re.fullmatch(domain_pattern, "https://www.example.org")

print(f"  captured domain label: {domain_match.group(1)}")
print(f"  captured extension: {domain_match.group(2)}")
print(f"  protocol and www are not captured: {len(domain_match.groups()) == 2}")
#   captured domain label: example
#   captured extension: org
#   protocol and www are not captured: True

# Capturing parentheses give useful subgroups; (?:...)
# organizes optional choices without capturing them.

# ============================================================
# [11] Reject malformed URL shapes
# ============================================================
# Anchors and required separators reject incomplete
# examples; this remains format-only validation:

bad_urls = ("https:///example.com", "www.", "example", "example.c")
bad_results = [bool(re.fullmatch(url_pattern, item)) for item in bad_urls]

print(f"  malformed URL results: {bad_results}")
print(f"  all malformed samples rejected: {not any(bad_results)}")
#   malformed URL results: [False, False, False, False]
#   all malformed samples rejected: True

# ============================================================
# [12] Tester workflow [04:44]
# ============================================================
# Try alternatives and escaped literals against a small
# expected-results table, as in an online tester:

test_cases = (
    ("https://www.example.com", True),
    ("example.com", True),
    ("https:///example.com", False),
    ("https://.example.com", False),
)
tester_results = [
    bool(re.fullmatch(url_pattern, sample)) == expected
    for sample, expected in test_cases
]

print(f"  tester case count: {len(test_cases)}")
print(f"  all expected: {all(tester_results)}")
print(f"  test results: {tester_results}")
#   tester case count: 4
#   all expected: True
#   test results: [True, True, True, True]

# Online testers visualize matches and explain each part;
# these deterministic examples cover both accepted and
# rejected shapes without an external dependency.

# ============================================================
# [13] The summary
# ============================================================
# OR, escaping, groups and URLs, from the transcript:
#
#   1. OR [00:10] -- | chooses alternatives; (apple|orange)
#      accepts either and rejects pear
#   2. GROUPS [00:55] -- (...) groups choices and captures
#      subgroups; (Mr|Ms) plus a name extracted both parts
#   3. NON-CAPTURING -- (?:...) groups without recording
#      a capture, useful for optional URL prefixes
#   4. ESCAPING [01:38] -- \., \*, \?, \( and \) mean
#      literal characters instead of regex instructions
#   5. URL [04:44] -- optional (?:https?)://, optional
#      www\., domain, escaped dot, suffix, optional path
#   6. ANCHORS -- ^ and $ make the whole example fit the
#      URL pattern rather than a substring
#   7. TESTS -- bare domain, protocol, www, both, and a
#      path/query accepted; malformed forms rejected
#   8. TESTER [04:44] -- compare examples in an online
#      tester to understand how each group contributes
#   9. LIMIT -- matching shape does not establish that
#      a URL is reachable or safe
#
# OR chooses; parentheses organize; backslash escapes;
# anchors require the whole URL-shaped string.
