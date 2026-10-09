# ============================================================
# Project 47 - re: the bookshop finds things in text
# ============================================================
# What this lesson teaches:
#   re.search          find the pattern anywhere in the text
#   re.match           anchored at the start only
#   re.fullmatch       the whole string, or nothing
#   re.findall         every match, as a list
#   re.sub / re.subn   rewrite the text, and count the changes
#   re.split           split on a pattern instead of a string
#   groups             parentheses carve the text, group() reads them back
#   named groups       (?P<name>...) read by name, not by number
#   re.IGNORECASE      flags change what counts as a match
#   raw strings        r"..." so Python does not eat the backslashes
#   re.compile         one pattern object, used again and again
#
# Everything is the standard library. No input(), no random, no datetime.now.
# The output is deterministic. The file runs to completion and exits with 0.
#
# Run it:  python project-47-re-the-bookshop-finds-things.py
# ============================================================

import re
import sys

CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what does re.search return")
print("Q2  how do match and fullmatch differ")
print("Q3  what does re.findall give you")
print("Q4  what does re.sub do")
print("Q5  what is a group")
print("Q6  what is a named group")
print("Q7  why raw strings for patterns")
print("Q8  what does fullmatch prove")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  a match object if the pattern is found anywhere, else None")
print("Q2  match anchors at the start, fullmatch needs the whole string")
print("Q3  a list of every piece the pattern matched")
print("Q4  it rewrites the text, replacing every match")
print("Q5  a piece inside parentheses, read back with group()")
print("Q6  a group with a name, read back by that name")
print("Q7  so backslashes reach the regex engine instead of Python")
print("Q8  that the entire string fits the pattern, not just part of it")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - search finds it anywhere")
print("T1  search found -> Dune")
print("T1  so search returns a match object -> True")
print()

print("TASK 2 - match anchors, fullmatch demands everything")
print("T2  match at the start -> 1965")
print("T2  fullmatch needs the whole string -> True")
print()

print("TASK 3 - findall returns every match")
print("T3  the years -> ['1965', '1969']")
print("T3  so findall returns every match -> True")
print()

print("TASK 4 - sub rewrites the text")
print("T4  collapsed -> Dune Frank Herbert")
print("T4  four space runs became one space -> True")
print("T4  so sub rewrites the text -> True")
print()

print("TASK 5 - groups pull pieces out")
print("T5  group 0 -> Herbert wrote Dune")
print("T5  group 1 -> Herbert")
print("T5  group 2 -> Dune")
print("T5  so groups pull pieces out -> True")
print()

print("TASK 6 - named groups read by name")
print("T6  named author -> Herbert")
print("T6  named title -> Dune")
print("T6  so a named group reads by name -> True")
print()

print("TASK 7 - flags change what counts")
print("T7  without the flag -> None")
print("T7  with re.IGNORECASE -> DUNE")
print("T7  so flags change what counts -> True")
print()

print("TASK 8 - escape the dot or it matches anything")
print("T8  the price -> $4.99")
print("T8  the unescaped dot matched -> 4x99")
print("T8  so escape the dot -> True")
print()

print("TASK 9 - compile once, use it again")
print("T9  the titles -> ['Dune', 'Dune Messiah', 'Children of Dune']")
print("T9  the count -> 3")
print("T9  so a compiled pattern is reused -> True")
print()

print("TASK 10 - the pattern is the contract")
print("T10  the ISBN validates -> True")
print("T10  the broken ISBN is refused -> True")
print("T10  found inside a sentence -> 978-0-441-47812-3")
print("T10  so the pattern is the contract -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)


# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - search finds it anywhere")
print("-" * 60)
found = re.search(r"Dune", "Frank Herbert wrote Dune in 1965")
missing = re.search(r"Foundation", "Frank Herbert wrote Dune in 1965")

check("search found something", found is not None)
check("the match is Dune", found is not None and found.group() == "Dune")
check("it starts at the right place", found is not None and found.start() == 20)
check("the missing title really is missing", missing is None)

print("T1  search found ->", found.group())
print("T1  so search returns a match object ->", found is not None)
print()


# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - match anchors, fullmatch demands everything")
print("-" * 60)
anchored = re.match(r"\d+", "1965 and more")
whole = re.fullmatch(r"\d+", "1965 and more")

check("match anchored at the start", anchored is not None)
check("match stopped before the rest", anchored is not None
      and anchored.end() == 4)
check("fullmatch refused the rest", whole is None)
check("the difference is real", anchored is not None and whole is None)

print("T2  match at the start ->", anchored.group())
print("T2  fullmatch needs the whole string ->", whole is None)
print()


# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - findall returns every match")
print("-" * 60)
years = re.findall(r"\d{4}", "Dune 1965, Dune Messiah 1969")

check("findall returns a list", isinstance(years, list))
check("both years found", years == ["1965", "1969"])
check("every match, in order", len(years) == 2 and years[1] == "1969")

print("T3  the years ->", years)
print("T3  so findall returns every match ->", years == ["1965", "1969"])
print()


# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - sub rewrites the text")
print("-" * 60)
raw, replaced = re.subn(r"\s+", " ", "  Dune   Frank   Herbert  ")

check("the runs collapsed", raw.strip() == "Dune Frank Herbert")
check("four space runs became one space", replaced == 4)
check("the ends were space runs too",
      raw == " Dune Frank Herbert ")
check("nothing else changed", "Dune" in raw and "Herbert" in raw)

print("T4  collapsed ->", raw.strip())
print("T4  four space runs became one space ->", replaced == 4)
print("T4  so sub rewrites the text ->", raw == " Dune Frank Herbert ")
print()


# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - groups pull pieces out")
print("-" * 60)
piece = re.search(r"(\w+) wrote (\w+)", "Herbert wrote Dune")

check("there was a match", piece is not None)
check("group 0 is the whole match",
      piece is not None and piece.group(0) == "Herbert wrote Dune")
check("group 1 is the author",
      piece is not None and piece.group(1) == "Herbert")
check("group 2 is the title",
      piece is not None and piece.group(2) == "Dune")

print("T5  group 0 ->", piece.group(0))
print("T5  group 1 ->", piece.group(1))
print("T5  group 2 ->", piece.group(2))
print("T5  so groups pull pieces out ->",
      piece.group(1) == "Herbert" and piece.group(2) == "Dune")
print()


# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - named groups read by name")
print("-" * 60)
named = re.search(r"(?P<author>\w+) wrote (?P<title>\w+)",
                  "Herbert wrote Dune")

check("the named groups matched", named is not None)
check("author reads by name",
      named is not None and named.group("author") == "Herbert")
check("title reads by name",
      named is not None and named.group("title") == "Dune")
check("groupdict holds both",
      named is not None
      and named.groupdict() == {"author": "Herbert", "title": "Dune"})

print("T6  named author ->", named.group("author"))
print("T6  named title ->", named.group("title"))
print("T6  so a named group reads by name ->",
      named.group("author") == "Herbert")
print()


# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - flags change what counts")
print("-" * 60)
without = re.search(r"dune", "DUNE is on the shelf")
withflag = re.search(r"dune", "DUNE is on the shelf", re.IGNORECASE)

check("no flag, no match", without is None)
check("with the flag it matches", withflag is not None)
check("the matched text is the real text",
      withflag is not None and withflag.group() == "DUNE")
check("the string itself never changed",
      withflag is not None and withflag.string == "DUNE is on the shelf")

print("T7  without the flag ->", without)
print("T7  with re.IGNORECASE ->", withflag.group())
print("T7  so flags change what counts ->", withflag is not None)
print()


# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - escape the dot or it matches anything")
print("-" * 60)
price = re.search(r"\$\d+\.\d+", "the price is $4.99 today")
wild = re.search(r"4.99", "4x99 is not a price")

check("the escaped pattern found the price",
      price is not None and price.group() == "$4.99")
check("the unescaped dot matched anyway", wild is not None)
check("and it swallowed the x", wild is not None and wild.group() == "4x99")
check("escaped, it refuses the fake",
      re.fullmatch(r"4\.99", "4x99") is None)

print("T8  the price ->", price.group())
print("T8  the unescaped dot matched ->", wild.group())
print("T8  so escape the dot ->", wild.group() == "4x99")
print()


# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - compile once, use it again")
print("-" * 60)
titles_pattern = re.compile(r"\s*,\s*")
titles = titles_pattern.split("Dune, Dune Messiah ,Children of Dune")

check("compile returns a Pattern", isinstance(titles_pattern, re.Pattern))
check("split by pattern", titles
      == ["Dune", "Dune Messiah", "Children of Dune"])
check("three titles", len(titles) == 3)
check("the spaces around the commas went too",
      titles[1] == "Dune Messiah")

print("T9  the titles ->", titles)
print("T9  the count ->", len(titles))
print("T9  so a compiled pattern is reused ->",
      isinstance(titles_pattern, re.Pattern))
print()


# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the pattern is the contract")
print("-" * 60)
isbn = re.compile(r"\d{3}-\d-\d{3}-\d{5}-\d")
good = isbn.fullmatch("978-0-441-47812-3")
bad = isbn.fullmatch("978-0-441-47812")
inside = re.search(r"\d{3}-\d-\d{3}-\d{5}-\d",
                   "call 978-0-441-47812-3 now")

check("the real ISBN validates", good is not None)
check("the broken ISBN is refused", bad is None)
check("found inside a sentence",
      inside is not None and inside.group() == "978-0-441-47812-3")
check("thirteen digits inside it",
      good is not None
      and len([c for c in good.group() if c.isdigit()]) == 13)
check("one pattern, three jobs", good is not None and bad is None)

print("T10  the ISBN validates ->", good is not None)
print("T10  the broken ISBN is refused ->", bad is None)
print("T10  found inside a sentence ->", inside.group())
print("T10  so the pattern is the contract ->",
      good is not None and bad is None)
print()


# ------------------------------------------------------------
# report
# ------------------------------------------------------------
failed = [name for name, ok in CHECKS if not ok]
print("=" * 60)
if failed:
    for name in failed:
        print("  FAILED:", name)
    print("CHECKS PASSED {0} of {1}".format(
        len(CHECKS) - len(failed), len(CHECKS)))
    sys.exit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)
