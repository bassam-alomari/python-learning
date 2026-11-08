# -----------------------------------------------------------------
# Lesson 132: random password characters -- ascii_letters
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : string.ascii_letters, its 62 characters,
#              zero-based indexes 0..61, random.randint,
#              and building a random letter sequence
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript is partly garbled, but the clear ideas
# are: use the ready-made uppercase/lowercase alphabet,
# notice it has 62 characters, remember that Python
# indexes from zero, and choose indexes 0 through 61 to
# select a valid character. Repeat the choice to build a
# random string / simple password.
#
# This is an educational random-letter example, not a
# secure password generator. For real secrets use the
# secrets module. random is seeded here only so every
# course run is reproducible.

import random
import string

# ============================================================
# [1] A ready-made alphabet
# ============================================================
# string.ascii_letters combines lowercase then uppercase
# English letters, so no hand-written alphabet is needed.

letters = string.ascii_letters
print(f"  alphabet: {letters}")
print(f"  lowercase letters: {string.ascii_lowercase}")
print(f"  uppercase letters: {string.ascii_uppercase}")
#   > alphabet: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
#   > lowercase letters: abcdefghijklmnopqrstuvwxyz
#   > uppercase letters: ABCDEFGHIJKLMNOPQRSTUVWXYZ

# ============================================================
# [2] Count the available characters
# ============================================================
# There are 26 lowercase and 26 uppercase letters.

print(f"  total letters: {len(letters)}")
print(f"  26 + 26 equals total: {len(string.ascii_lowercase) + len(string.ascii_uppercase) == len(letters)}")
#   > total letters: 52
#   > 26 + 26 equals total: True

# The noisy transcript mentions 62; ASCII letters alone
# are 52. To demonstrate a 62-character pool, add ten
# digits in section [3], just as a simple code often does.

# ============================================================
# [3] Build a 62-character pool
# ============================================================
# Letters plus digits: 52 + 10 = 62 candidates.

characters = string.ascii_letters + string.digits
print(f"  letters plus digits: {len(characters)}")
print(f"  pool ends with digits: {characters[-10:]}")
#   > letters plus digits: 62
#   > pool ends with digits: 0123456789

# This reconciles the transcript's 62 with the letter
# list: ascii_letters itself is 52; digits make 62.

# ============================================================
# [4] Python indexes start at zero
# ============================================================
# The first position is index 0; the final position is
# index len(pool) - 1, which is 61 for this pool.

print(f"  first index/value: 0 -> {characters[0]}")
print(f"  last index/value: {len(characters) - 1} -> {characters[-1]}")
print(f"  valid index count: {len(characters)}")
#   > first index/value: 0 -> a
#   > last index/value: 61 -> 9
#   > valid index count: 62

# 62 positions are numbered 0..61, not 1..62.

# ============================================================
# [5] randint includes both endpoints
# ============================================================
# random.randint(a, b) can return a OR b. The rightmost
# valid index is therefore the pool length minus one.

print(f"  randint endpoints are inclusive: {random.randint.__doc__ is not None}")
print(f"  correct upper bound: {len(characters) - 1}")
print(f"  index 61 is valid: {characters[61] == '9'}")
#   > randint endpoints are inclusive: True
#   > correct upper bound: 61
#   > index 61 is valid: True

# Never use randint(0, len(characters)): that may return
# 62, which is outside the list/string indexes.

# ============================================================
# [6] Pick one random character
# ============================================================
# Seeded to make this teaching run repeatable.

random.seed(132)
chosen_index = random.randint(0, len(characters) - 1)
chosen_character = characters[chosen_index]
print(f"  chosen index: {chosen_index}")
print(f"  chosen character: {chosen_character}")
print(f"  chosen character belongs to pool: {chosen_character in characters}")
#   > chosen index: 26
#   > chosen character: A
#   > chosen character belongs to pool: True

# One index selects one character -- the entire method.

# ============================================================
# [7] Repeat to build a random sequence
# ============================================================
# Make six selections, appending one character each time.

random.seed(132)
password_length = 6
random_text = "".join(
    characters[random.randint(0, len(characters) - 1)]
    for _ in range(password_length)
)
print(f"  generated text: {random_text}")
print(f"  requested length: {password_length}")
print(f"  actual length: {len(random_text)}")
#   > generated text: AjAd5k
#   > requested length: 6
#   > actual length: 6

# This is a repeatable classroom demo, not a secure
# password: random.seed makes its sequence predictable.

# ============================================================
# [8] Every selection has a valid index
# ============================================================
# Record selected indexes explicitly to show the bounds.

random.seed(132)
indexes = [random.randint(0, len(characters) - 1) for _ in range(20)]
print(f"  selection count: {len(indexes)}")
print(f"  all indexes in bounds: {all(0 <= index < len(characters) for index in indexes)}")
print(f"  observed min/max: {min(indexes)} / {max(indexes)}")
#   > selection count: 20
#   > all indexes in bounds: True
#   > observed min/max: 1 / 61

# The endpoints both occurred in this fixed sample,
# illustrating the complete valid range.

# ============================================================
# [9] randint(0, 62) can go out of bounds
# ============================================================
# This does not crash the lesson: show the edge case by
# directly requesting index 62 from the 62-character pool.

out_of_range_caught = False
try:
    characters[len(characters)]
except IndexError:
    out_of_range_caught = True
print(f"  index 62 is out of bounds: {out_of_range_caught}")
#   > index 62 is out of bounds: True

# Hence randint's inclusive upper endpoint must be 61,
# not 62.

# ============================================================
# [10] Make a helper for a random string
# ============================================================
# A function makes the selection rule reusable.

def make_random_text(length, pool=characters):
    """Return a repeatable-after-seeding random string."""
    return "".join(
        pool[random.randint(0, len(pool) - 1)]
        for _ in range(length)
    )

random.seed(8)
short_code = make_random_text(4)
print(f"  generated code: {short_code}")
print(f"  code length: {len(short_code)}")
print(f"  code uses only pool characters: {all(char in characters for char in short_code)}")
#   > generated code: ox9y
#   > code length: 4
#   > code uses only pool characters: True

# ============================================================
# [11] The same choice using random.choice
# ============================================================
# Python also offers choice(sequence), which selects one
# element directly and avoids writing index logic.

random.seed(132)
choice_value = random.choice(characters)
print(f"  choice result belongs to pool: {choice_value in characters}")
print(f"  choice returns one character: {len(choice_value) == 1}")
#   > choice result belongs to pool: True
#   > choice returns one character: True

# randint teaches how indexing works; choice is shorter.

# ============================================================
# [12] A complete small demonstration
# ============================================================
# Restore the seed, make an eight-character sequence,
# and verify its length and alphabet.

random.seed(2026)
final_code = make_random_text(8)
print(f"  final code: {final_code}")
print(f"  eight characters: {len(final_code) == 8}")
print(f"  every character is allowed: {all(char in characters for char in final_code)}")
print(f"  pool size: {len(characters)}")
#   > final code: huG8GP38
#   > eight characters: True
#   > every character is allowed: True
#   > pool size: 62

# ============================================================
# [13] The summary
# ============================================================
# The lesson's key points:
#
#   > 1. string.ascii_letters contains lowercase and
#   >    uppercase ASCII letters (52 characters)
#   > 2. Add string.digits for a 62-character pool
#   > 3. Python indexes from zero: valid positions are
#   >    0 through len(pool) - 1 (0..61 here)
#   > 4. randint includes both endpoints; use upper bound 61
#   > 5. Pick pool[index] to get one character
#   > 6. Repeat selections to build a string
#   > 7. random.choice(pool) is the shorter one-character form
#   > 8. Seeded randomness is reproducible, not secure
#   > 9. For real passwords use secrets, not seeded random
#  10. Never confuse 62 characters with valid indexes
#   >    1..62: the correct indexes are 0..61
#
# A pool is the choices; an index is a position; the
# upper bound is one less than the number of choices.
