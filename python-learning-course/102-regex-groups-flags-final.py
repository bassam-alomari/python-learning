# -----------------------------------------------------------------
# Lesson 102: RegEx groups and flags -- series finale
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : URL groups for protocol/domain/port/path,
#            extracting with group(), and IGNORECASE,
#            MULTILINE and DOTALL flags
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: final lesson in the Regular
# Expressions series -- group exercises and flags.
#
#   GROUPS [00:31] -- divide a complex URL into parts:
#   protocol, host/domain, port and path; extract each
#   part by its group number
#   FLAGS [07:26] -- options that modify matching:
#      re.IGNORECASE / re.I -- ignore letter case
#      re.MULTILINE / re.M -- ^ and $ work per line
#      re.DOTALL / re.S -- dot also matches newline
#   FINALE [10:31] -- close this Regex series
#
# Examples teach pattern mechanics, not URL validation
# standards or network reachability.

import re

# ============================================================
# [1] Groups divide a complex pattern [00:31]
# ============================================================
# Each capturing (...) stores one part of the match:

url_pattern = r"^(https?)://([A-Za-z0-9.-]+)(?::(\d+))?(/[^\s?#]*)?(?:\?[^\s#]*)?(?:#\S*)?$"
url = "https://docs.example.com:8443/guide/start?mode=full#top"
match = re.fullmatch(url_pattern, url)

print(f"  URL matched: {match is not None}")
print(f"  captured groups: {len(match.groups())}")
#   URL matched: True
#   captured groups: 4

# Captures are protocol, host, optional port, optional
# path. Query and fragment are accepted but not captured.

# ============================================================
# [2] Extract the protocol with group(1)
# ============================================================
# group(0) is the whole match; group(1) is the first
# parenthesized capture:

print(f"  whole URL: {match.group(0)}")
print(f"  protocol: {match.group(1)}")
#   whole URL: https://docs.example.com:8443/guide/start?mode=full#top
#   protocol: https

# ============================================================
# [3] Extract host and port with group(2), group(3)
# ============================================================
# The port group is optional; this URL includes one:

print(f"  host: {match.group(2)}")
print(f"  port: {match.group(3)}")
print(f"  port is numeric text: {match.group(3).isdigit()}")
#   host: docs.example.com
#   port: 8443
#   port is numeric text: True

# group() returns captured text, so the port is a string;
# convert it explicitly if numeric arithmetic is needed.

# ============================================================
# [4] Extract path with group(4)
# ============================================================
# The path is its own capture; query/fragment remain
# outside that group:

print(f"  path: {match.group(4)}")
print(f"  path starts with slash: {match.group(4).startswith('/')}")
#   path: /guide/start
#   path starts with slash: True

# ============================================================
# [5] Optional groups may be None
# ============================================================
# A short URL has no explicit port or path:

short_match = re.fullmatch(url_pattern, "http://example.org")
print(f"  short URL matched: {short_match is not None}")
print(f"  absent port group: {short_match.group(3) is None}")
print(f"  absent path group: {short_match.group(4) is None}")
#   short URL matched: True
#   absent port group: True
#   absent path group: True

# Optional capture groups return None when their part
# was not present.

# ============================================================
# [6] Filter a list and extract parts [00:31]
# ============================================================
# Use group() to store only host and path from matching
# entries; malformed entries are skipped:

addresses = (
    "https://shop.example.com:443/cart",
    "http://news.example.org/story",
    "not a URL",
)
extracted = []

for address in addresses:
    found = re.fullmatch(url_pattern, address)
    if found:
        extracted.append((found.group(2), found.group(4)))

print(f"  extracted host/path pairs: {extracted}")
print(f"  malformed entry skipped: {len(extracted) == 2}")
#   extracted host/path pairs: [('shop.example.com', '/cart'), ('news.example.org', '/story')]
#   malformed entry skipped: True

# Group numbers let the program keep exactly the fields
# needed and ignore the rest.

# ============================================================
# [7] IGNORECASE / re.I [07:26]
# ============================================================
# Ignore capitalization differences while matching:

case_text = "PyThOn"
case_sensitive = re.fullmatch(r"python", case_text)
case_ignored = re.fullmatch(r"python", case_text, re.IGNORECASE)
short_flag = re.fullmatch(r"python", case_text, re.I)

print(f"  default case-sensitive match: {case_sensitive is not None}")
print(f"  IGNORECASE match: {case_ignored is not None}")
print(f"  re.I equivalent: {short_flag is not None}")
#   default case-sensitive match: False
#   IGNORECASE match: True
#   re.I equivalent: True

# ============================================================
# [8] MULTILINE / re.M [07:26]
# ============================================================
# With MULTILINE, ^ and $ match each line boundary:

lines = "start first\nmiddle\nstart second"
whole_text_starts = re.findall(r"^start.*", lines)
every_line_start = re.findall(r"^start.*", lines, re.MULTILINE)
short_flag_lines = re.findall(r"^start.*", lines, re.M)

print(f"  default start matches: {whole_text_starts}")
print(f"  MULTILINE start matches: {every_line_start}")
print(f"  re.M equivalent: {short_flag_lines == every_line_start}")
#   default start matches: ['start first']
#   MULTILINE start matches: ['start first', 'start second']
#   re.M equivalent: True

# By default, ^ starts the whole string; re.M lets it
# start each line. (With ., newline still needs DOTALL.)

# ============================================================
# [9] MULTILINE also changes $ [07:26]
# ============================================================
# $ can now mark the end of each line, not only the
# entire string:

line_ends = "one end\ntwo end\nthree"
default_ends = re.findall(r"end$", line_ends)
multiline_ends = re.findall(r"end$", line_ends, re.M)

print(f"  default end matches: {default_ends}")
print(f"  MULTILINE end matches: {multiline_ends}")
#   default end matches: []
#   MULTILINE end matches: ['end', 'end']

# No line ends with "end" in the whole string because
# "three" follows the newline; re.M finds the two lines.

# ============================================================
# [10] DOTALL / re.S [07:26]
# ============================================================
# By default, dot matches any character EXCEPT newline;
# DOTALL makes it include newline:

multi_text = "top\nbottom"
default_dot = re.search(r"top.bottom", multi_text)
dotall_match = re.search(r"top.bottom", multi_text, re.DOTALL)
short_dotall = re.search(r"top.bottom", multi_text, re.S)

print(f"  default dot crosses newline: {default_dot is not None}")
print(f"  DOTALL crosses newline: {dotall_match is not None}")
print(f"  re.S equivalent: {short_dotall is not None}")
#   default dot crosses newline: False
#   DOTALL crosses newline: True
#   re.S equivalent: True

# ============================================================
# [11] Flags can be combined
# ============================================================
# Combine IGNORECASE and DOTALL with bitwise OR:

combined_text = "BEGIN\npython\nEND"
combined_match = re.search(
    r"begin.*end",
    combined_text,
    re.IGNORECASE | re.DOTALL,
)

print(f"  combined flags match across lines and case: {combined_match is not None}")
print(f"  matched text has newline: {'\n' in combined_match.group()}")
#   combined flags match across lines and case: True
#   matched text has newline: True

# Pass combined flags as one third argument using |.

# ============================================================
# [12] One session: groups and flags
# ============================================================
# The groups and the three flags together:

print(f"  URL protocol: {match.group(1)}")
print(f"  URL host: {match.group(2)}")
print(f"  URL port: {match.group(3)}")
print(f"  URL path: {match.group(4)}")
print(f"  IGNORECASE works: {case_ignored is not None}")
print(f"  MULTILINE lines: {len(every_line_start)}")
print(f"  DOTALL newline: {dotall_match is not None}")
#   URL protocol: https
#   URL host: docs.example.com
#   URL port: 8443
#   URL path: /guide/start
#   IGNORECASE works: True
#   MULTILINE lines: 2
#   DOTALL newline: True

# ============================================================
# [13] The summary: Regex series finale [10:31]
# ============================================================
# Groups and flags, from the final transcript:
#
#   1. GROUPS [00:31] -- parentheses divide a complex URL
#      into protocol, host, optional port and path
#   2. group(0) -- the full match; group(1..4) -- protocol,
#      host, port, path respectively
#   3. OPTIONAL CAPTURES -- absent port/path groups return
#      None; check before converting or using them
#   4. FILTER -- extract host/path pairs from valid-shaped
#      samples; skip malformed entries
#   5. IGNORECASE / re.I [07:26] -- case-insensitive match
#   6. MULTILINE / re.M [07:26] -- ^ and $ address each
#      line boundary instead of only whole text
#   7. DOTALL / re.S [07:26] -- dot matches newline too
#   8. COMBINE -- flags can be ORed together with |
#   9. LIMIT -- URL matching here demonstrates structure;
#      it does not check network existence or safety
#  10. SERIES FINALE [10:31] -- RegEx groups, matching
#      flags, and the end of this Regex sequence
#
# Groups say which part; flags say how matching behaves.
