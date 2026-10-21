# -----------------------------------------------------------------
# Lesson 80: format date (strftime)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : rendering dates YOUR way -- strftime() and the
#            %Y %y %m %d %B %b %A %a directives,
#            combining them into custom formats, full
#            date+time stamps, and the reverse trip with
#            strptime()
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:13]: projects and countries want
# dates DIFFERENT ways -- day first, then month, then
# year; month names as WORDS instead of numbers. strftime()
# [00:41] is the tool: String Format Time -- it turns a
# datetime object into a STRING in exactly the shape you
# ask for.
#
# Every directive starts with %, the transcript's table
# [01:32]:
#
#   %Y  year, 4 digits        %y  year, 2 digits
#   %m  month as a number     %d  day as a number
#   %B  month name, full      %b  month name, short
#   %A  weekday name, full    %a  weekday name, short
#
# Every date printed here is lesson 79's fixed moment --
# 1980-10-10 10:45:55, a FRIDAY -- so every formatted
# string is permanent. No now() anywhere in this file.
#
# Everything runs by itself. Every expected output was
# produced by running the file, not written from memory.

import datetime

# ============================================================
# [1] The date we will dress up
# ============================================================
# The transcript formats DATE objects -- so we need one.
# Lesson 79's construction, rebuilt exactly:

birthday = datetime.datetime(1980, 10, 10, 10, 45, 55)

print(f"  raw object: {birthday}")
print(f"  raw type: {type(birthday).__name__}")
#   raw object: 1980-10-10 10:45:55
#   raw type: datetime

# That is the DEFAULT rendering -- Python's own fixed
# style. The rest of this lesson is about asking for
# something else.

# ============================================================
# [2] strftime(): string format time [00:41]
# ============================================================
# The method exists on every datetime object, and it
# RETURNS a str (that is the "string" in its name):

formatted = birthday.strftime("%Y")

print(f"  strftime is callable: {callable(birthday.strftime)}")
print(f"  returns str: {type(formatted).__name__}")
print(f"  with %Y: {formatted}")
#   strftime is callable: True
#   returns str: str
#   with %Y: 1980

# One call, two parts: the METHOD (strftime) and a
# FORMAT STRING ("%Y") that names the shape you want.
# Everything the transcript teaches is choosing format
# strings.

# ============================================================
# [3] The year: %Y and %y [01:32]
# ============================================================
# Full year, or the two-digit short form:

print(f"  %Y: {birthday.strftime('%Y')}")
print(f"  %y: {birthday.strftime('%y')}")
#   %Y: 1980
#   %y: 80

# 1980 in four digits, 80 in two -- the transcript's
# أربعة أرقام vs رقمان أخوان. %y is for compact display
# only; store and compare with %Y.

# ============================================================
# [4] Numbered month and day: %m and %d
# ============================================================
# The month and day as NUMBERS -- exactly the transcript's
# "%m: الشهر كرقْم" and "%d: اليوم كرقْم":

print(f"  %m: {birthday.strftime('%m')}")
print(f"  %d: {birthday.strftime('%d')}")
#   %m: 10
#   %d: 10

# October is month 10, the 10th day is 10 -- both zero
# padded to two digits (so March shows as 03, never 3).
# Sorting-friendly by construction.

# ============================================================
# [5] Month as a word: %B and %b
# ============================================================
# The transcript's "اسم الشهر بالحروف بدلاً من الأرقام":

print(f"  %B: {birthday.strftime('%B')}")
print(f"  %b: {birthday.strftime('%b')}")
#   %B: October
#   %b: Oct

# Full name and abbreviation. 10 means nothing to a
# reader; October says it instantly -- the whole reason
# the transcript calls this a "beautiful" format.

# ============================================================
# [6] Day names: %A and %a
# ============================================================
# Weekday names, full and short. 1980-10-10 was a Friday
# (lesson 79's weekday() -> 4, Monday=0):

print(f"  %A: {birthday.strftime('%A')}")
print(f"  %a: {birthday.strftime('%a')}")
#   %A: Friday
#   %a: Fri

# %A/%a answer "which day of the WEEK" -- derived from
# the date itself, never stored on the object.

# ============================================================
# [7] Combining directives [02:49]
# ============================================================
# The transcript's practical line, exactly:
# my_date.strftime("%d %B %Y") -- day, word-month, year:

custom = birthday.strftime("%d %B %Y")
print(f"  %d %B %Y: {custom}")
#   %d %B %Y: 10 October 1980

# (The transcript writes 25 October 1980 as the sample
# shape -- our date is the 10th, so ours reads 10 October
# 1980. Same recipe, our ingredients.) The spaces between
# directives are copied into the output LITERALLY --
# arrange them however your project or country needs.

# ============================================================
# [8] More recipes from the same pantry
# ============================================================
# Day-first, ISO (machine) style, and comma style -- the
# directive set from sections [3]-[6] in new orders:

print(f"  %A, %d %b %Y: {birthday.strftime('%A, %d %b %Y')}")
print(f"  %Y-%m-%d: {birthday.strftime('%Y-%m-%d')}")
#   %A, %d %b %Y: Friday, 10 Oct 1980
#   %Y-%m-%d: 1980-10-10

# Weekday, short month, full year -- a date a human reads
# in a header. And %Y-%m-%d -- the ISO shape, the one
# SORTS correctly as text. Same eight directives, three
# personalities.

# ============================================================
# [9] Formatting the CLOCK: %H, %M, %S, %I, %p
# ============================================================
# Time directives follow the same % pattern -- 24-hour
# clock, then the 12-hour with AM/PM:

print(f"  %H:%M:%S: {birthday.strftime('%H:%M:%S')}")
print(f"  %I:%M:%S %p: {birthday.strftime('%I:%M:%S %p')}")
#   %H:%M:%S: 10:45:55
#   %I:%M:%S %p: 10:45:55 AM

# %H is hour 00-23, %I is hour 01-12, %p answers AM or
# PM (10:45 in the morning is AM). %M minutes, %S
# seconds -- the transcript's time symbols carry the same
# % prefix as every date directive.

# ============================================================
# [10] Date AND time in one stamp
# ============================================================
# Put both halves together -- the everyday log line, with
# a day/month/year order swapped at will:

stamp = birthday.strftime("%d/%m/%Y %H:%M:%S")
print(f"  full stamp: {stamp}")
print(f"  reads day first: {stamp.startswith('10/10/')}")
#   full stamp: 10/10/1980 10:45:55
#   reads day first: True

# One format string, one strftime() call, one line that
# says everything. (Whether YOUR project wants
# %d/%m/%Y or %m/%d/%Y is the [00:13] point: strftime
# follows YOUR convention, not Python's.)

# ============================================================
# [11] The reverse trip: strptime()
# ============================================================
# Bonus beyond the transcript, because it completes the
# circle: when a date arrives AS A STRING (a file, an
# API), strptime() parses it back -- same directives,
# spelled backwards (string PARSE time):

parsed = datetime.datetime.strptime("10 October 1980 10:45:55",
                                    "%d %B %Y %H:%M:%S")
print(f"  parsed: {parsed}")
print(f"  full round trip equals the original: {parsed == birthday}")
#   parsed: 1980-10-10 10:45:55
#   full round trip equals the original: True

# Format out, parse in: the string we built in section
# [7] (plus the clock) parses back to the EXACT object
# this lesson started with. Every directive works on
# both sides of the trip.

# ============================================================
# [12] One session: every directive at once
# ============================================================
# The transcript's table [01:32], all eight, against one
# fixed date -- then the custom format that combines
# them:

print(f"  %Y: {birthday.strftime('%Y')}")
print(f"  %y: {birthday.strftime('%y')}")
print(f"  %m: {birthday.strftime('%m')}")
print(f"  %B: {birthday.strftime('%B')}")
print(f"  %b: {birthday.strftime('%b')}")
print(f"  %d: {birthday.strftime('%d')}")
print(f"  %A: {birthday.strftime('%A')}")
print(f"  %a: {birthday.strftime('%a')}")
print(f"  %d %B %Y: {birthday.strftime('%d %B %Y')}")
print(f"  round trip: {parsed == birthday}")
#   %Y: 1980
#   %y: 80
#   %m: 10
#   %B: October
#   %b: Oct
#   %d: 10
#   %A: Friday
#   %a: Fri
#   %d %B %Y: 10 October 1980
#   round trip: True

# The whole table in order -- four-digit year, two-digit
# year, numbered month, full month, short month, numbered
# day, full weekday, short weekday -- and the custom
# combination the transcript asked for. One date, ten
# faces.

# ============================================================
# [13] The summary
# ============================================================
# Formatting dates, from the transcript, complete:
#
#   1. WHY [00:13] -- projects and countries display dates
#      differently (day first? month first? month as a
#      word?); strftime() gives every project ITS shape
#   2. strftime() [00:41] -- String Format Time: a method
#      on datetime objects that RETURNS str, driven by a
#      format string like "%Y"
#   3. THE DIRECTIVES [01:32], all % -led --
#        %Y  1980 (4 digits)   %y  80 (2 digits)
#        %m  10 (number)       %d  10 (number)
#        %B  October (full)    %b  Oct (short)
#        %A  Friday (full)     %a  Fri (short)
#      every number zero-padded (03, not 3); %A/%a are
#      DERIVED from the date, never stored on it
#   4. COMBINING [02:49] -- the transcript's
#      strftime("%d %B %Y") -> '10 October 1980'; the
#      text BETWEEN directives is copied literally --
#      spaces, slashes, commas are yours to choose
#   5. RECIPES -- '%A, %d %b %Y' -> 'Friday, 10 Oct 1980'
#      (human header) and '%Y-%m-%d' -> '1980-10-10'
#      (ISO: sorts correctly as text); same eight
#      directives, different orders
#   6. THE CLOCK -- %H:%M:%S -> '10:45:55' (24-hour),
#      %I:%M:%S %p -> '10:45:55 AM' (12-hour + AM/PM)
#   7. FULL STAMP -- '%d/%m/%Y %H:%M:%S' ->
#      '10/10/1980 10:45:55': date and time in one line,
#      in YOUR convention (that freedom is the lesson)
#   8. THE REVERSE (bonus) -- strptime(string, format)
#      parses a date string BACK into an object:
#      '10 October 1980 10:45:55' with
#      '%d %B %Y %H:%M:%S' rebuilds the original object
#      exactly (round trip -> True)
#   9. THE DISCIPLINE -- every date here is fixed
#      (1980-10-10 10:45:55, a Friday); no now() and no
#      locale surprises, so the formatted strings are
#      byte-stable on every run
#
# Directives in, beautiful strings out; strings in,
# objects back.
