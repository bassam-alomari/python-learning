# -----------------------------------------------------------------
# Lesson 79: date and time (datetime)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : import datetime, datetime.datetime.now() (shape
#            only -- never its raw values), extracting
#            year/month/day, MINYEAR and MAXYEAR,
#            datetime.time for the clock alone,
#            building a custom datetime (1980, 10, 10,
#            10, 45, 55), and subtracting dates with
#            timedelta
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's headline [00:04]: one of the most
# important topics in programming -- DATE AND TIME.
#
# THE STABILITY RULE FOR THIS LESSON (course rule 4):
# datetime.datetime.now() returns a DIFFERENT value every
# run -- it is the opposite of a seed. So now() is called
# and CHECKED (types, attribute presence, ranges) but its
# raw numbers are NEVER printed. Every value this file
# prints comes from a FIXED date you can read right here:
#
#   datetime.datetime(1980, 10, 10, 10, 45, 55)
#
# The transcript itself uses exactly that construction
# [05:46]. The only exceptions are pure CONSTANTS
# (MINYEAR, MAXYEAR) and fixed differences (16071 days),
# which never change.
#
# Everything in this file runs by itself. Every expected
# output was produced by running the file, not written
# from memory.

import datetime

# ============================================================
# [1] import datetime [00:33]
# ============================================================
# The built-in library for dates and times, exactly as the
# transcript writes it. Inside sits the main class -- note
# the double name datetime.datetime (module . class):

print(f"  import worked: {type(datetime).__name__}")
print(f"  main class: {datetime.datetime.__name__}")
print(f"  also a time class: {datetime.time.__name__}")
print(f"  also a timedelta class: {datetime.timedelta.__name__}")
#   import worked: module
#   main class: datetime
#   also a time class: time
#   also a timedelta class: timedelta

# One module, three tools we will use: datetime (a moment
# in time), time (a clock reading), timedelta (a span
# between two moments).

# ============================================================
# [2] datetime.datetime.now() [01:28] -- shape only
# ============================================================
# The transcript's way to get the CURRENT date and time,
# complete down to microseconds. We call it for real --
# and print only facts that stay true on every run:

moment = datetime.datetime.now()

print(f"  now() type: {type(moment).__name__}")
print(f"  has year: {hasattr(moment, 'year')}")
print(f"  has month: {hasattr(moment, 'month')}")
print(f"  has day: {hasattr(moment, 'day')}")
print(f"  has hour: {hasattr(moment, 'hour')}")
print(f"  has minute: {hasattr(moment, 'minute')}")
print(f"  has second: {hasattr(moment, 'second')}")
print(f"  has microsecond: {hasattr(moment, 'microsecond')}")
print(f"  year within MINYEAR..MAXYEAR: {datetime.MINYEAR <= moment.year <= datetime.MAXYEAR}")
#   now() type: datetime
#   has year: True
#   has month: True
#   has day: True
#   has hour: True
#   has minute: True
#   has second: True
#   has microsecond: True
#   year within MINYEAR..MAXYEAR: True

# All seven fields the transcript lists -- year, month,
# day, hours, minutes, seconds, microseconds -- really are
# on the object. Their VALUES are not printed: printing
# this run's second or microsecond would make the file's
# output change every execution. Shape travels, values
# stay home. (Run `python -c "import datetime; print(datetime.datetime.now())"`
# in a terminal to watch the live clock yourself.)

# ============================================================
# [3] Extracting each element [02:06]
# ============================================================
# The transcript: reach into the object for ONE field at a
# time -- year, month, day. We do it on a FIXED date so
# the answers are readable and permanent:

project_start = datetime.datetime(2030, 6, 15, 18, 30, 0)

print(f"  year: {project_start.year}")
print(f"  month: {project_start.month}")
print(f"  day: {project_start.day}")
print(f"  hour: {project_start.hour}")
print(f"  minute: {project_start.minute}")
print(f"  second: {project_start.second}")
#   year: 2030
#   month: 6
#   day: 15
#   hour: 18
#   minute: 30
#   second: 0

# Plain attributes -- no parentheses, they are fields on
# the object, not calls. Same extraction works on the
# now() object from section [2]; only its numbers would
# be different every time.

# ============================================================
# [4] The supported range: MINYEAR and MAXYEAR [03:09]
# ============================================================
# The transcript's limits. Python datetime years run from
# 1 to 9999 -- both are CONSTANTS, so they print safely:

print(f"  datetime.MINYEAR: {datetime.MINYEAR}")
print(f"  datetime.MAXYEAR: {datetime.MAXYEAR}")

earliest = datetime.datetime(datetime.MINYEAR, 1, 1)
print(f"  earliest date: {earliest}")
#   datetime.MINYEAR: 1
#   datetime.MAXYEAR: 9999
#   earliest date: 0001-01-01 00:00:00

# And the floor really is a floor -- year 0 is rejected:

try:
    datetime.datetime(0, 1, 1)
except ValueError:
    print("  year 0 raises ValueError: True")
#   year 0 raises ValueError: True

# Years 1..9999 (the transcript's الحد الأدنى والأقصى),
# and the year before MINYEAR does not exist. That range
# is why the datetime type always answers.

# ============================================================
# [5] Time alone: datetime.time [04:15]
# ============================================================
# The transcript: hours, minutes, seconds WITHOUT today's
# date -- datetime.time():

clock = datetime.time(10, 45, 55)

print(f"  time type: {type(clock).__name__}")
print(f"  clock: {clock}")
print(f"  hour: {clock.hour}")
print(f"  minute: {clock.minute}")
print(f"  second: {clock.second}")
print(f"  carries a date: {hasattr(clock, 'date')}")
#   time type: time
#   clock: 10:45:55
#   hour: 10
#   minute: 45
#   second: 55
#   carries a date: False

# A time object is the CLOCK ONLY -- it knows 10:45:55 but
# not which day that is (no date field: False above). The
# mirror of a datetime, which always carries both.

# ============================================================
# [6] Building a custom date [05:46]
# ============================================================
# The transcript's exact construction -- a birth date or a
# project start, hand-built from parts:

birthday = datetime.datetime(1980, 10, 10, 10, 45, 55)

print(f"  built: {birthday}")
print(f"  isoformat: {birthday.isoformat()}")
print(f"  just the date: {birthday.date()}")
print(f"  just the time: {birthday.time()}")
print(f"  weekday number: {birthday.weekday()}")
#   built: 1980-10-10 10:45:55
#   isoformat: 1980-10-10T10:45:55
#   just the date: 1980-10-10
#   just the time: 10:45:55
#   weekday number: 4

# Year, month, day, hour, minute, second -- positional, in
# that order, exactly as the transcript wrote them.
# isoformat() is the machine-friendly spelling (the T
# separates date from time), .date() and .time() split the
# object in half, and weekday() counts Monday=0 -- so 4 is
# Friday. From raw numbers to a full moment in six
# arguments.

# ============================================================
# [7] Subtracting dates: timedelta [07:00]
# ============================================================
# The transcript's core trick: subtract two dates to get
# the span between them -- days (and years) elapsed.
# Two FIXED dates, so the span is a fixed number:

start = datetime.datetime(1980, 10, 10)
milestone = datetime.datetime(2024, 10, 10)
gap = milestone - start

print(f"  gap type: {type(gap).__name__}")
print(f"  gap: {gap}")
print(f"  gap in days: {gap.days}")
print(f"  == 16071 days: {gap == datetime.timedelta(days=16071)}")
#   gap type: timedelta
#   gap: 16071 days, 0:00:00
#   gap in days: 16071
#   == 16071 days: True

# datetime minus datetime lands on a TIMESPAN
# (timedelta), not a date. 1980-10-10 to 2024-10-10 is
# 16071 days -- 44 years counting every leap day (11 of
# them). The days attribute is the plain integer; the
# equality check proves timedelta(16071) and the computed
# gap are the same object value.

# ============================================================
# [8] The anatomy of a timedelta
# ============================================================
# A timedelta holds days + seconds + microseconds
# internally; its string shows the friendly form:

span = datetime.timedelta(days=1, hours=2, minutes=3)

print(f"  span: {span}")
print(f"  its days: {span.days}")
print(f"  its seconds: {span.seconds}")
print(f"  hours kept in seconds: {span.seconds // 3600}")
#   span: 1 day, 2:03:00
#   its days: 1
#   its seconds: 7380
#   hours kept in seconds: 2

# 7380 seconds // 3600 -> 2 whole hours. 2 hours +
# 3 minutes = 7380 seconds, stored under days=1 +
# seconds=7380. timedelta does the carrying for you:
# build it in hours and minutes, read it back in days
# and seconds.

# ============================================================
# [9] Age until NOW -- booleans only
# ============================================================
# The transcript's [07:00] payoff: years elapsed from a
# date UNTIL TODAY. Today is now() -- so the exact day
# count would drift between runs. Print the CLAIMS, not
# the counter:

age = datetime.datetime.now() - birthday

print(f"  age is a timedelta: {isinstance(age, datetime.timedelta)}")
print(f"  age is positive: {age > datetime.timedelta(0)}")
print(f"  over 15000 days: {age.days > 15000}")
print(f"  over 40 full years: {age.days // 365 > 40}")
print(f"  birthday still in the past: {datetime.datetime.now() > birthday}")
#   age is a timedelta: True
#   age is positive: True
#   over 15000 days: True
#   over 40 full years: True
#   birthday still in the past: True

# now() minus 1980-10-10 -- a real subtraction against the
# live clock, with every printed answer a statement that
# stays true for decades. The transcript shows the exact
# numbers; this lesson shows how to hold them without
# freezing the clock.

# ============================================================
# [10] Checking the live clock, safely
# ============================================================
# More things provable about now() without leaking its
# values -- ranges and orderings that hold on any run:

print(f"  hour is 0..23: {0 <= datetime.datetime.now().hour <= 23}")
print(f"  minute is 0..59: {0 <= datetime.datetime.now().minute <= 59}")
print(f"  month is 1..12: {1 <= datetime.datetime.now().month <= 12}")
print(f"  now is after 1980: {datetime.datetime.now() > birthday}")
print(f"  now() and now() agree to the day: {datetime.datetime.now().date() == datetime.datetime.now().date()}")
#   hour is 0..23: True
#   minute is 0..59: True
#   month is 1..12: True
#   now is after 1980: True
#   now() and now() agree to the day: True

# Every rule the calendar promises, verified against the
# live object. (The last one could only ever fail at
# midnight between two calls -- a reminder that the clock
# moves while you read it.)

# ============================================================
# [11] Reassembling the parts: combine()
# ============================================================
# date + time back into one datetime -- the inverse of
# section [6]'s .date() / .time() split:

rejoined = datetime.datetime.combine(datetime.date(1980, 10, 10),
                                     datetime.time(10, 45, 55))
print(f"  rejoined: {rejoined}")
print(f"  equals the built birthday: {rejoined == birthday}")
#   rejoined: 1980-10-10 10:45:55
#   equals the built birthday: True

# The same moment, rebuilt from halves. split and
# recombine -- every part stays first class.

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- the import, the
# live shape, the fixed parts, the range, the clock, the
# custom date, and the span:

print(f"  module: {type(datetime).__name__}")
print(f"  live now() is a datetime: {type(datetime.datetime.now()).__name__}")
print(f"  fixed parts: {birthday.year}-{birthday.month}-{birthday.day}")
print(f"  MINYEAR..MAXYEAR: {datetime.MINYEAR}..{datetime.MAXYEAR}")
print(f"  clock alone: {clock}")
print(f"  custom: {birthday}")
print(f"  span to 2024-10-10: {gap.days} days")
print(f"  span in years: {gap.days // 365} full years")
#   module: module
#   live now() is a datetime: datetime
#   fixed parts: 1980-10-10
#   MINYEAR..MAXYEAR: 1..9999
#   clock alone: 10:45:55
#   custom: 1980-10-10 10:45:55
#   span to 2024-10-10: 16071 days
#   span in years: 44 full years

# The live clock announced (type only), the fixed date
# dissected, the limits quoted, the clock alone, the
# transcript's exact construction, and the 44-year span
# (16071 // 365 = 44 full years -- 44 x 365 = 16060, and
# the 11 leftover days are the leap days between the
# anniversaries).

# ============================================================
# [13] The summary
# ============================================================
# Date and time, from the transcript, complete:
#
#   1. IMPORT [00:33] -- `import datetime`; the module
#      carries datetime (a moment), time (a clock), and
#      timedelta (a span)
#   2. now() [01:28] -- datetime.datetime.now() returns
#      the current moment COMPLETE to microseconds;
#      course rule: its type and all seven fields are
#      checked (year..microsecond, each present), but
#      its raw values are never printed -- they change
#      every run
#   3. EXTRACTION [02:06] -- plain attributes, no
#      parentheses: .year .month .day .hour .minute
#      .second read one field at a time off any
#      datetime (shown on 2030-06-15 18:30:00)
#   4. THE RANGE [03:09] -- datetime.MINYEAR = 1,
#      datetime.MAXYEAR = 9999 (constants, safe to
#      print); datetime(1, 1, 1) builds the earliest
#      date, year 0 raises ValueError
#   5. TIME ALONE [04:15] -- datetime.time(10, 45, 55)
#      -> 10:45:55 with hour/minute/second fields and
#      NO date attached (hasattr(..., 'date') -> False)
#   6. CUSTOM DATE [05:46] -- the transcript's exact
#      datetime.datetime(1980, 10, 10, 10, 45, 55):
#      str -> '1980-10-10 10:45:55',
#      isoformat -> '1980-10-10T10:45:55', .date() and
#      .time() split it, .weekday() -> 4 (Friday)
#   7. SUBTRACTION [07:00] -- datetime minus datetime
#      gives a timedelta: 2024-10-10 - 1980-10-10 ->
#      16071 days (44 years with 11 leap days),
#      equal to timedelta(days=16071)
#   8. TIMEDLETA ANATOMY -- built as
#      timedelta(days=1, hours=2, minutes=3) -> '1 day,
#      2:03:00'; stored as days=1 + seconds=7380
#      (7380 // 3600 -> 2 hours)
#   9. AGE UNTIL NOW -- now() - birthday is a real
#      subtraction against the live clock; printed as
#      claims that hold forever: isinstance True,
#      positive True, > 15000 days True, > 40 years
#      True -- the exact numbers stay unprinted
#  10. LIVE CLOCK CHECKS -- hour 0..23, minute 0..59,
#      month 1..12, now() > 1980, now() agrees with
#      itself to the day -- all True on any run
#  11. COMBINE -- datetime.combine(date, time) rebuilds
#      1980-10-10 10:45:55 from halves: equals the
#      built birthday True
#  12. THE DISCIPLINE -- constants and fixed dates print
#      as values; the live clock prints only as facts.
#      That is how a lesson about NOW can be reproducible
#
# Dates are data; the clock is a stream. Read both.
