# -----------------------------------------------------------------
# Lesson 38: User Input
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : input(), strip(), title(), capitalize(), upper(), lower(),
#           method chaining, slicing, and real formatting applications
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# Everything we learned so far finally comes together in this lesson.
# The program STOPS and WAITS while the user types on the keyboard.

# ============================================================
# [1] input()  -> the program pauses and waits for the user
# ============================================================
# Syntax: variable = input("the prompt that the user will see")
# The program cannot continue until the user presses Enter.
# VERY IMPORTANT: input() ALWAYS returns TEXT (a str), even when
# the user types a number. We convert it ourselves when we need it.

name = input("Please enter your full name: ")
print("Hello,", name)
print("type of the name:", type(name))
# type of the name: <class 'str'>   -> text, not an int

# The leading and trailing spaces problem. If the user types
# "   mohamed ahmed   " by mistake, the spaces travel with the
# value and break any formatting we do later.
age = int(input("Please enter your age: "))
print("age:", age, "| type:", type(age))
# age: 22 | type: <class 'int'>  -> now it is a real number

# ============================================================
# [2] Cleaning the input with strip()
# ============================================================
# strip() removes the spaces at the START and at the END only.
# It does NOT touch the spaces in the middle.

raw = "   Bassam   "
print("before strip:", repr(raw))
# before strip: '   Bassam   '
print("after  strip:", repr(raw.strip()))
# after  strip: 'Bassam'

# To remove ALL the extra spaces we split on them and join again.
messy = "   Bassam    Al-Omari  "
print("messy        :", repr(messy))
print("join(split()) :", repr(" ".join(messy.split())))
# join(split()) : 'Bassam Al-Omari'

# ============================================================
# [3] Formatting methods on user input
# ============================================================
# These are the string methods that shape how a name looks.

raw = "   bassam   al-omari  "
clean = " ".join(raw.split())     # first remove the extra spaces

print("clean    :", clean)
# clean    : bassam al-omari
print("title()  :", clean.title())
# title()  : Bassam Al-Omari      -> capital letter at the start of every word
print("capitalize():", clean.capitalize())
# capitalize(): Bassam al-omari   -> only the first letter becomes capital
print("upper()  :", clean.upper())
# upper()  : BASSAM AL-OMARI
print("lower()  :", clean.upper().lower())
# lower()  : bassam al-omari

# ============================================================
# [4] Method Chaining  -> many methods in one line
# ============================================================
# Instead of writing a long temporary variable for every step, we
# can call the methods one after another. This is called CHAINING.

typed = "   mohamed   ahmed   elsayed  "

cleaned = typed.strip().title()
print("chained  :", cleaned)
# chained  : Mohamed   Ahmed   Elsayed   (the inner spaces are still there)

perfect = " ".join(typed.split()).title()
print("perfect  :", perfect)
# perfect  : Mohamed Ahmed Elsayed

# Chaining is not only for formatting. It works anywhere:
print("chain on data:", "  10  ".strip().isdigit())
# chain on data: True

# ============================================================
# [5] A real application: the middle initial (M.)
# ============================================================
# Many websites show "Mohamed A. Elsayed" instead of the full name.
# We take the first letter of the middle name, upper case it, and
# add a dot.

full_name = "mohamed ahmed elsayed"
parts = full_name.strip().split()

first_name = parts[0].title()
middle_initial = parts[1][0].upper() + "."
last_name = parts[-1].title()

print("full     :", full_name)
# full     : mohamed ahmed elsayed
print("short    :", f"{first_name} {middle_initial} {last_name}")
# short    : Mohamed A. Elsayed

# The same result with slicing instead of an index.
print("by slicing:", f"{full_name.split()[0].title()} {full_name.split()[1][0].upper()}. {full_name.split()[-1].title()}")
# by slicing: Mohamed A. Elsayed

# ============================================================
# [6] Slicing and format inside the print
# ============================================================
# Slicing lets us take a PART of a string: text[start:end].

text = "Python Programming"
print("full      :", text)
# full      : Python Programming
print("text[:6]  :", text[:6])
# text[:6]  : Python
print("text[7:]  :", text[7:])
# text[7:]  : Programming
print("text[0:6] :", text[0:6], "|", text[7:11])
# text[0:6] : Python | Prog
print("every 2nd :", text[::2])
# every 2nd : Pto rgamn

# Old and new format styles with user input inside.
user = "bassam"
age_value = 22

print("old style: Hello %s, you are %d years old" % (user, age_value))
# old style: Hello bassam, you are 22 years old
print("new style: Hello {}, you are {} years old".format(user, age_value))
# new style: Hello bassam, you are 22 years old
print("f-string :", f"Hello {user}, you are {age_value} years old")
# f-string : Hello bassam, you are 22 years old

# ============================================================
# [7] Input combined with the operators we already know
# ============================================================
# The real power appears when the input meets the conditions and
# the calculations from the previous lessons.

a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))

print("sum     :", a + b)
# sum     : 75
print("is a > b:", a > b)
# is a > b: True

if a > b:
    print("the first number is bigger")
else:
    print("the second number is bigger or equal")

# ============================================================
# Improvement (from me): three helpers that make input safe
# ============================================================
# Real programs must survive messy human typing: empty fields,
# wrong spaces, and text where a number was expected.

def clean_name(raw):
    """Remove the extra spaces and give every word a capital letter."""
    return " ".join(raw.strip().split()).title()


def short_name(raw):
    """Turn a full name into 'First M. Last', and handle short names."""
    parts = raw.strip().split()
    if len(parts) == 0:
        return ""
    if len(parts) == 1:
        return parts[0].title()
    if len(parts) == 2:
        return f"{parts[0].title()} {parts[-1].title()}"
    return f"{parts[0].title()} {parts[1][0].upper()}. {parts[-1].title()}"


def read_int(prompt, attempts=3):
    """Ask until the user types a real number; None if they never do."""
    for _ in range(attempts):
        raw = input(prompt).strip()
        if not raw:
            return None                     # the user just pressed Enter
        try:
            return int(raw)
        except ValueError:
            print("   !! please type a whole number, try again")
    return None


# We use them on the name that the user typed at the top.
print("cleaned name :", clean_name(name))
# cleaned name : Mohamed Ahmed Elsayed
print("short name   :", short_name(name))
# short name   : Mohamed A. Elsayed

# And we check that the names are correct by trying other examples.
for sample in ["mohamed ahmed elsayed", "sara ali", "khaled", "   "]:
    print(f"{sample!r:>24} -> short: {short_name(sample)!r}")

#  'mohamed ahmed elsayed' -> short: 'Mohamed A. Elsayed'
#                'sara ali' -> short: 'Sara Ali'
#                  'khaled' -> short: 'Khaled'
#                     '   ' -> short: ''

# ============================================================
# SUMMARY
# ============================================================
# - input(prompt) pauses the program and returns what the user typed.
# - input() ALWAYS returns a str, so wrap it in int() for numbers.
# - strip() removes the spaces at both ends; " ".join(s.split())
#   removes ALL the extra spaces.
# - title(), capitalize(), upper(), and lower() shape the text.
# - Method chaining calls many methods in one clean line.
# - Slicing text[start:end] takes a part of the string.
# - The name, the age, and the conditions can all live together,
#   which is the whole point of this lesson.

# ============================================================
# NEXT LESSON: Control Flow - the if / elif / else statements
# ============================================================
