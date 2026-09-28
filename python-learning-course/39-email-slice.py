# -----------------------------------------------------------------
# Lesson 39: Practical Application - Email Slice
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : input, strip, index, find, slicing, string formatting
# Type     : Educational + Practical Project
# Builder  : local assistant
# -----------------------------------------------------------------
# This is our first real mini program. It takes an email address
# and splits it into the username and the website, using only the
# tools we already learned: input, strip, index, find, and slicing.

# ============================================================
# [1] The idea
# ============================================================
# An email address is made of TWO parts separated by the @ sign:
#
#     bassam.alomari @ gmail.com
#     \_________/   \_________/
#       username        domain
#
# The username is the part BEFORE the @, and the domain (the
# website) is the part AFTER it.

email = "bassam.alomari@gmail.com"
print("the email:", email)
# the email: bassam.alomari@gmail.com

# ============================================================
# [2] Finding the @ sign: index() and find()
# ============================================================
# index() tells us the POSITION of the @, counting from zero.
at_position = email.index("@")
print("index('@') :", at_position)
# index('@') : 14

# The letter at that position is the @ itself.
print("email[14]  :", email[at_position])
# email[14]  : @

# find() gives the same number, BUT it does not crash when the
# character is missing. It simply returns -1.
print("find('@')  :", email.find("@"))
# find('@')  : 14
print("find('#')  :", email.find("#"))
# find('#')  : -1   -> not found

# This is the important difference:
try:
    email.index("#")
except ValueError as err:
    print("index('#') ->", err)
# index('#') -> substring not found

# find()   -> gives -1, safe
# index()  -> raises an error, dangerous but strict

# ============================================================
# [3] The slicing that does the whole job
# ============================================================
# email[:at_position]      -> everything BEFORE the @  = username
# email[at_position + 1:]  -> everything AFTER the @   = domain

username = email[:at_position]
domain = email[at_position + 1:]

print("username:", username)
# username: bassam.alomari
print("domain  :", domain)
# domain  : gmail.com

# We can even write it in one line without a temporary variable.
print("one line username:", email[:email.index("@")])
print("one line domain  :", email[email.index("@") + 1:])
# one line username: bassam.alomari
# one line domain  : gmail.com

# ============================================================
# [4] Going one step further: the site and the extension
# ============================================================
# partition() splits on the first dot and always returns THREE
# parts, even when there is no dot at all. That makes it safe.
# (split(".") would return a single item and break the unpacking.)

site, _, extension = domain.partition(".")
print("site      :", site)
# site      : gmail
print("extension :", "." + extension)
# extension : .com

# partition() is smarter than split() when there are extra dots.
mail = "bassam@mail.example.com"
_, _, user_domain = mail.partition("@")
print("mail      :", mail)
# mail      : bassam@mail.example.com
print("domain    :", user_domain, "-> rest kept whole")
# domain    : mail.example.com -> rest kept whole

# ============================================================
# [5] The REAL program: ask the user, then clean the input
# ============================================================
# The user may type spaces, so we clean the input with strip() and
# then we also remove the spaces in the middle. We lower the whole
# address because in practice nobody writes GMAIL.COM differently.

raw_email = input("Please enter your email address: ")

clean_email = " ".join(raw_email.strip().split()).lower()
print("cleaned email:", clean_email)
# cleaned email: mohamedahmed33@gmail.com

# Now we do the same slicing on the cleaned value.
at = clean_email.index("@")
user_name = clean_email[:at]
site_name = clean_email[at + 1:]
mail_site, _, mail_ext = site_name.partition(".")

print()
print("=" * 46)
print("         EMAIL SLICE REPORT")
print("=" * 46)
print(f"  Full email  : {clean_email}")
print(f"  Username    : {user_name}")
print(f"  Domain      : {site_name}")
print(f"  Site        : {mail_site}")
print(f"  Extension   : .{mail_ext}")
print(f"  First letter: {user_name[0].upper()}")
print("=" * 46)

# ============================================================
# [6] The output, nicely formatted
# ============================================================
# The three format styles from the previous lesson, all used here
# so the report always looks the same.

username_final = "mohamedahmed33"
domain_final = "gmail.com"

print("old style: %s uses %s" % (username_final, domain_final))
# old style: mohamedahmed33 uses gmail.com
print("new style: {} uses {}".format(username_final, domain_final))
# new style: mohamedahmed33 uses gmail.com
print("f-string :", f"{username_final} uses {domain_final}")
# f-string : mohamedahmed33 uses gmail.com

# A card built with chaining, so the name always looks tidy.
print("pretty name:", f"  @{' '.join(username_final.split()).title()}")
# pretty name:   @Mohamedahmed33

# ============================================================
# Improvement (from me): a validator that never crashes
# ============================================================
# Real users type bad emails, so we check the input first and give
# a helpful message instead of an ugly traceback.

def email_info(raw):
    """Return a dict describing the email, or the reason it failed."""
    email_value = " ".join(str(raw).strip().split()).lower()

    if not email_value:
        return {"ok": False, "error": "the email address is empty"}
    if email_value.count("@") != 1:
        return {"ok": False, "error": "an email needs exactly one @ sign"}
    if "." not in email_value:
        return {"ok": False, "error": "the domain needs a dot, like gmail.com"}

    username_value, domain_value = email_value.split("@")

    if not username_value:
        return {"ok": False, "error": "the username before @ is missing"}
    if not domain_value:
        return {"ok": False, "error": "the domain after @ is missing"}

    site_value, _, extension_value = domain_value.partition(".")
    if not extension_value:
        return {"ok": False, "error": "the domain needs something after the dot"}

    return {
        "ok": True,
        "email": email_value,
        "username": username_value,
        "domain": domain_value,
        "site": site_value,
        "extension": extension_value,
    }


def show_info(info):
    """Print a clean card for a good email, or a single clear error."""
    if not info["ok"]:
        return f"  INVALID -> {info['error']}"
    return (
        "  OK  email    : " + info["email"] + "\n"
        "      username : " + info["username"] + "\n"
        "      domain   : " + info["domain"] + "\n"
        "      site     : " + info["site"] + "\n"
        "      extension: ." + info["extension"]
    )


print("--- checking several emails ---")
samples = [
    "mohamedahmed33@gmail.com",
    "  Bassam.Alomari@Outlook.COM  ",
    "user@mail.example.com",
    "notanemail",
    "a@b@c.com",
    "@gmail.com",
    "user@nodots",
    "   ",
]
for sample in samples:
    print(show_info(email_info(sample)))

# ============================================================
# SUMMARY
# ============================================================
# - index() gives the position of @ but raises an error if missing.
# - find() gives the same position but returns -1 instead of crashing.
# - email[:email.index("@")]        -> the username
# - email[email.index("@") + 1:]    -> the domain
# - partition(".") splits on the first dot only and is always safe,
#   while split(".") can return one item and break unpacking.
# - Clean the input first: " ".join(raw.strip().split()).lower()
# - Always validate the email; a real user WILL type a wrong one.

# ============================================================
# NEXT LESSON: Control Flow - the if / elif / else statements
# ============================================================
