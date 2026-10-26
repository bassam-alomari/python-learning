# -----------------------------------------------------------------
# Lesson 94: type hinting -- document expected types
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : parameter annotations with :, return
#            annotations with ->, dynamic typing,
#            runtime metadata, and clearer large projects
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: a small, useful Python feature --
# Type Hinting.
#
#   WHAT [00:13] -- annotate the data types expected for a
#   function's Parameters and its Return Value
#   PYTHON IS DYNAMIC -- hints guide the programmer and
#   editor (such as VS Code) with clarity, autocomplete
#   and early warnings; Python itself does NOT enforce
#   them at runtime
#   SYNTAX [00:45] -- a colon after each parameter name
#   and an arrow -> before the return type
#       def calculate(n1: int, n2: int) -> int:
#           return n1 + n2
#   WHY [02:52] -- especially useful in large-scale
#   projects: clearer, more organized, easier to maintain
#
# STABILITY: all outputs are derived from fixed values
# and annotations. No external editor or type checker
# required; no machine paths. Every expected line was
# produced by running this file.

# ============================================================
# [1] What Type Hinting means [00:13]
# ============================================================
# Hints document what types a function expects and
# returns -- a note for the people and tools reading it.

def calculate(n1: int, n2: int) -> int:
    """Add two integers and return their sum."""
    return n1 + n2


print(f"  calculate(3, 4): {calculate(3, 4)}")
print(f"  parameters carry hints: {calculate.__annotations__['n1'] is int and calculate.__annotations__['n2'] is int}")
print(f"  return hint is int: {calculate.__annotations__['return'] is int}")
#   calculate(3, 4): 7
#   parameters carry hints: True
#   return hint is int: True

# The colon marks each parameter's expected type; the
# arrow marks the expected return type.

# ============================================================
# [2] The syntax: colon and arrow [00:45]
# ============================================================
# Inspect the annotations Python stored on the function:

annotations = calculate.__annotations__
print(f"  n1 annotation: {annotations['n1'].__name__}")
print(f"  n2 annotation: {annotations['n2'].__name__}")
print(f"  return annotation: {annotations['return'].__name__}")
#   n1 annotation: int
#   n2 annotation: int
#   return annotation: int

# __annotations__ is metadata, separate from the
# function's calculation.

# ============================================================
# [3] Python remains dynamically typed [00:13]
# ============================================================
# The transcript stresses that Python does NOT force
# hints as runtime rules. This annotated function still
# accepts values of another type:

dynamic_result = calculate("Py", "thon")
print(f"  different types accepted: {dynamic_result}")
print(f"  result type: {type(dynamic_result).__name__}")
#   different types accepted: Python
#   result type: str

# The annotation is a promise/documentation, not a
# runtime guard. (A static type checker or editor can
# warn about the mismatch; Python itself still runs it.)

# ============================================================
# [4] Hints do not coerce values
# ============================================================
# An int hint does not convert a string to an int:

def describe_number(value: int) -> str:
    """Return a readable label for the supplied value."""
    return "value=" + str(value)


label = describe_number("12")
print(f"  string passed through: {label}")
print(f"  returned type: {type(label).__name__}")
print(f"  annotation remains int: {describe_number.__annotations__['value'] is int}")
#   string passed through: value=12
#   returned type: str
#   annotation remains int: True

# The hint did not coerce "12" to 12. It remains a str
# argument; str() inside the function explicitly formats
# it for the label.

# ============================================================
# [5] Annotations are available as metadata
# ============================================================
# Editors can inspect the same information exposed here:

print(f"  annotations are a dict: {isinstance(calculate.__annotations__, dict)}")
print(f"  parameter names listed: {set(calculate.__annotations__) == set(('n1', 'n2', 'return'))}")
print(f"  hint values are types: {all(isinstance(item, type) for item in calculate.__annotations__.values())}")
#   annotations are a dict: True
#   parameter names listed: True
#   hint values are types: True

# Parameter names plus "return" form the annotation
# keys. This is the metadata an editor can use for
# suggestions and early diagnostics.

# ============================================================
# [6] A mismatch is still executable
# ============================================================
# The call below disagrees with the int hints, but it
# still executes -- a visible proof of dynamic typing:

mismatch_result = calculate("2", "3")
print(f"  mismatched call result: {mismatch_result}")
print(f"  mismatched result type: {type(mismatch_result).__name__}")
#   mismatched call result: 23
#   mismatched result type: str

# No automatic TypeError: both strings concatenate even
# though the signature says int. The hint documents the
# intended contract; it does not enforce one.

# ============================================================
# [7] Static hints versus runtime checks
# ============================================================
print("  Python does not enforce annotations at runtime")
#   Python does not enforce annotations at runtime

# Editors and static type checkers can report a mismatch
# before you run the program; plain Python does not.

# ============================================================
# [8] Hints improve editor assistance
# ============================================================
# The annotations make the intended call legible to a
# reader and to tools that understand Python hints:

print(f"  intended first argument: {calculate.__annotations__['n1'].__name__}")
print(f"  intended second argument: {calculate.__annotations__['n2'].__name__}")
print(f"  intended result: {calculate.__annotations__['return'].__name__}")
#   intended first argument: int
#   intended second argument: int
#   intended result: int

# In VS Code, these hints help display expected types,
# completion suggestions and potential mismatch warnings.

# ============================================================
# [9] Readability in a larger-style function
# ============================================================
# A longer signature can communicate its contract at a
# glance, before anyone reads the body:

def calculate_invoice(subtotal: float, tax_rate: float) -> float:
    """Return subtotal plus tax at the supplied rate."""
    return subtotal + subtotal * tax_rate


invoice_total = calculate_invoice(100.0, 0.08)
print(f"  invoice total: {invoice_total}")
print(f"  both inputs annotated: {'subtotal' in calculate_invoice.__annotations__ and 'tax_rate' in calculate_invoice.__annotations__}")
print(f"  output annotated: {calculate_invoice.__annotations__['return'] is float}")
#   invoice total: 108.0
#   both inputs annotated: True
#   output annotated: True

# The signature tells readers the intended contract
# immediately -- particularly valuable across a large
# project with many functions and contributors.

# ============================================================
# [10] Hints do not replace validation
# ============================================================
# If a program must enforce a rule, write a real check;
# do not rely on a hint alone:

def require_int(value: int) -> int:
    """Enforce an int at runtime and return it."""
    if not isinstance(value, int):
        raise TypeError("value must be an int")
    return value


print(f"  valid int returned: {require_int(8)}")
try:
    require_int("8")
except TypeError as error:
    validation_caught = str(error) == "value must be an int"
else:
    validation_caught = False

print(f"  explicit validation catches str: {validation_caught}")
#   valid int returned: 8
#   explicit validation catches str: True

# The hint informs; isinstance enforces. Distinct tools,
# distinct jobs.

# ============================================================
# [11] Why large projects benefit [02:52]
# ============================================================
# The transcript's benefits: clarity, organization and
# easier maintenance. These signatures expose a contract
# without opening the function body:

contracts = (
    calculate.__annotations__,
    describe_number.__annotations__,
    calculate_invoice.__annotations__,
)
print(f"  annotated functions: {len(contracts)}")
print(f"  each has a return hint: {all('return' in item for item in contracts)}")
print(f"  hints aid maintainability: {all(isinstance(item, dict) for item in contracts)}")
#   annotated functions: 3
#   each has a return hint: True
#   hints aid maintainability: True

# A consistent contract is easier to understand,
# review and maintain as the project grows.

# ============================================================
# [12] One session: syntax, metadata, dynamic behavior
# ============================================================
# The key facts together:

print(f"  example result: {calculate(3, 4)}")
print(f"  parameter hint: {annotations['n1'].__name__}")
print(f"  return hint: {annotations['return'].__name__}")
print(f"  runtime accepts other types: {dynamic_result == 'Python'}")
print(f"  editor metadata exists: {bool(annotations)}")
print(f"  explicit check enforces type: {validation_caught}")
#   example result: 7
#   parameter hint: int
#   return hint: int
#   runtime accepts other types: True
#   editor metadata exists: True
#   explicit check enforces type: True

# Hints describe intent; Python stays dynamic; explicit
# validation is how a program enforces a requirement.

# ============================================================
# [13] The summary
# ============================================================
# Type Hinting, from the transcript:
#
#   1. WHAT [00:13] -- annotate expected parameter types
#      and the return value
#   2. DYNAMIC TYPING -- Python does not force hints at
#      runtime; calculate("Py", "thon") runs and returns
#      "Python" (str), despite int annotations
#   3. SYNTAX [00:45] -- parameter colon (n1: int),
#      return arrow (-> int): calculate(n1: int,
#      n2: int) -> int
#   4. METADATA -- __annotations__ stores the hints for
#      tools and readers; parameter keys plus "return"
#   5. NO COERCION -- a hint does not convert a value;
#      str("12") remains str until code converts it
#   6. EDITOR HELP [00:13] -- editors such as VS Code
#      can use hints for completion and early warnings
#   7. LARGE PROJECTS [02:52] -- clearer contracts,
#      organization and maintainability
#   8. VALIDATION -- if runtime enforcement is required,
#      write isinstance checks; hints alone do not guard
#
# A type hint is a promise to the reader and the editor,
# not a rule Python enforces for you.
