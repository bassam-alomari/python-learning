# -----------------------------------------------------------------
# Lesson 37: Type Conversion
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : int, float, str, list, tuple, set, dict conversions
# Type     : Educational + Practical
# Builder  : local assistant
# -----------------------------------------------------------------
# Type conversion means changing a value from one data type into
# another one. It is one of the most useful basics in any language,
# because the type of a value decides which operations we can do.

value = 15

# ============================================================
# [1] The number conversions we already know
# ============================================================
# int()   makes a whole number
# float() makes a decimal number
# str()   makes text

print("int(15.9)   :", int(value + 0.9))
# int(15.9)   : 15
print("float(15)   :", float(value))
# float(15)   : 15.0
print("str(15)     :", str(value))
# str(15)     : 15

# int() CUTS the decimals, it does not round them.
print("int(15.99)  :", int(15.99))
# int(15.99)  : 15
print("round(15.99):", round(15.99))
# round(15.99): 16

# Text becomes a number only if it really looks like a number.
print("int('20') + 5:", int("20") + 5)
# int('20') + 5: 25

# A number becomes text so we can join it with other text.
print("'age = ' + str(22):", "age = " + str(22))
# 'age = ' + str(22): age = 22

# ============================================================
# [2] list()  -> convert a tuple, a set, a dict, or a string
# ============================================================

my_tuple = (1, 2, 3)
print("list((1, 2, 3))      :", list(my_tuple))
# list((1, 2, 3))      : [1, 2, 3]

my_string = "python"
print("list('python')       :", list(my_string))
# list('python')       : ['p', 'y', 't', 'h', 'o', 'n']

# CAREFUL: converting a SET to a list may change the order,
# because a set is not ordered in the first place.
my_set = {3, 1, 2}
print("set -> list          :", list(my_set))
# set -> list          : [1, 2, 3]     (the order is not guaranteed)

# The BIGGEST surprise: converting a DICTIONARY to a list gives
# only the KEYS, and it drops the values completely.
my_dict = {"a": 1, "b": 2}
print("dict -> list (keys!) :", list(my_dict))
# dict -> list (keys!) : ['a', 'b']
print("dict -> list items   :", list(my_dict.items()))
# dict -> list items   : [('a', 1), ('b', 2)]

# ============================================================
# [3] tuple()  -> the same data, now as a tuple
# ============================================================

my_list = [1, 2, 3]
print("tuple([1, 2, 3])     :", tuple(my_list))
# tuple([1, 2, 3])     : (1, 2, 3)

# A round trip shows the conversion is lossless both ways.
print("list(tuple([1, 2, 3])):", list(tuple(my_list)))
# list(tuple([1, 2, 3])): [1, 2, 3]

# ============================================================
# [4] set()  -> remove the duplicates automatically
# ============================================================

print("set([1, 2, 2, 3, 3]):", set([1, 2, 2, 3, 3]))
# set([1, 2, 2, 3, 3]): {1, 2, 3}
letters = set(("a", "a", "b"))
print("set(('a','a','b'))   :", letters, "| sorted:", sorted(letters))
# set(('a','a','b'))   : {'a', 'b'} | sorted: ['a', 'b']
# NOTE: the printed order can change between runs. That is the
# whole reason we say a set is unordered.

# The order of a set is not guaranteed, so never rely on it.
# Also note: converting a DICTIONARY to a set gives its keys.
dict_keys = set({"x": 1, "y": 2})
print("set(dict)            :", dict_keys, "| sorted:", sorted(dict_keys))
# set(dict)            : {'x', 'y'} | sorted: ['x', 'y']

# ============================================================
# [5] dict()  -> build a dictionary from PAIRS
# ============================================================
# To use dict() the data must already be a sequence of PAIRS,
# where each pair has exactly TWO parts: a key and a value.

pairs = [("name", "Bassam"), ("age", 22)]
print("dict(list of pairs)  :", dict(pairs))
# dict(list of pairs)  : {'name': 'Bassam', 'age': 22}

# The same thing with keyword arguments.
print("dict(name=..., age=...):", dict(name="Bassam", age=22))
# dict(name=..., age=...): {'name': 'Bassam', 'age': 22}

# A tuple of tuples works just as well.
print("dict(tuple of pairs) :", dict((("a", 1), ("b", 2))))
# dict(tuple of pairs) : {'a': 1, 'b': 2}

# Converting a zip result is the most common real pattern.
print("dict(zip(keys, vals)):", dict(zip(["id", "city"], [7, "Amman"])))
# dict(zip(keys, vals)): {'id': 7, 'city': 'Amman'}

# A dict can be built from an existing dict too.
print("dict(existing dict)  :", dict(my_dict))
# dict(existing dict)  : {'a': 1, 'b': 2}

# ============================================================
# [6] When the data does NOT fit, Python tells us why
# ============================================================
# These failures are not random; each one has a clear reason.

# Problem 1: single values are not pairs.
try:
    dict([1, 2, 3])
except (TypeError, ValueError) as err:
    print("dict([1, 2, 3]) ->", err)
# dict([1, 2, 3]) -> cannot convert dictionary update sequence element #0 to a sequence

# Problem 2: the pairs must have exactly two parts.
try:
    dict([("a", 1, 2)])
except ValueError as err:
    print("dict([('a', 1, 2)]) ->", err)
# dict([('a', 1, 2)]) -> dictionary update sequence element #0 has length 3; 2 is required

# Problem 3: text that is not a number cannot become one.
try:
    int("abc")
except ValueError as err:
    print("int('abc') ->", err)
# int('abc') -> invalid literal for int() with base 10: 'abc'

# ============================================================
# [7] The HASHABLE rule blocks some conversions
# ============================================================
# A dictionary needs its keys to be HASHABLE (unchangeable).
# That is why a list can never be a key, and why a set cannot
# contain a list at all.

try:
    {1, [2, 3]}
except TypeError as err:
    print("{1, [2, 3]} ->", err)
# {1, [2, 3]} -> unhashable type: 'list'

# The same rule applies to the ** unpacking, which only accepts
# string keys.
try:
    dict(**{1: "a"})
except TypeError as err:
    print("dict(**{1: 'a'}) ->", err)
# dict(**{1: 'a'}) -> keywords must be strings

# But list, tuple, and set keys are perfectly fine.
print("{(1, 2): 'a tuple key'}:", {(1, 2): "a tuple key"})
# {(1, 2): 'a tuple key'}: {(1, 2): 'a tuple key'}

# ============================================================
# Improvement (from me): a conversion helper that never crashes
# ============================================================
# Conversions fail often in real programs, because the input is
# not always what we expect. This helper turns any failure into a
# readable message instead of a stack trace.

def try_convert(func, data, label=None):
    """Run a conversion and report the result OR the reason it failed."""
    name = label or getattr(func, "__name__", "convert")
    try:
        result = func(data)
    except Exception as err:
        return f"{name}({data!r}) -> ERROR {type(err).__name__}: {err}"
    return f"{name}({data!r}) -> {result!r} ({type(result).__name__})"


print("--- safe conversions ---")
for func, data, label in [
    (list, (1, 2, 3), "list"),
    (tuple, [1, 2, 3], "tuple"),
    (set, [1, 2, 2, 3], "set"),
    (dict, [("a", 1), ("b", 2)], "dict"),
    (int, "20", "int"),
    (int, "abc", "int"),
    (dict, [1, 2, 3], "dict"),
    (set, [[1, 2]], "set"),
]:
    print(try_convert(func, data, label))

# And a round-trip helper that reports whether the data survived
# the trip out and back. We compare with the original data AFTER
# coming back, because comparing a list with a tuple is always
# False and would tell us nothing.
def round_trip(data, to_type, back_type):
    """Convert to a type and back, then tell us if the data survived."""
    forward = to_type(data)
    backward = back_type(forward)
    return to_type.__name__, forward, backward, backward == data

print("--- round trips ---")
for data, to_type, back_type in [
    ([1, 2, 3], tuple, list),
    ((1, 2, 3), list, tuple),
    ("python", list, "".join),
    ([1, 2, 2, 3], set, list),
]:
    name, forward, backward, intact = round_trip(data, to_type, back_type)
    print(f"{data!r} -> {name} -> {forward!r} -> {backward!r} | intact = {intact}")

# ============================================================
# SUMMARY
# ============================================================
# - int(), float(), str() convert between numbers and text.
# - int() cuts the decimals; use round() if you want rounding.
# - list(), tuple(), set(), dict() convert between containers.
# - list(dict) gives the KEYS only. Use list(dict.items()) for pairs.
# - A set has no guaranteed order, never rely on the output order.
# - set() removes duplicates automatically.
# - dict() needs PAIRS: use a list of tuples, kwargs, or zip().
# - Failures are informative: TypeError, ValueError, and the
#   unhashable rule tell us exactly what was wrong.
# - A dict or a set can never hold a list, because lists are not
#   hashable.

# ============================================================
# NEXT LESSON: Control Flow - the if / elif / else statements
# ============================================================
