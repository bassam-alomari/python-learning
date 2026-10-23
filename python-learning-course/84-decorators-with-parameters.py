# -----------------------------------------------------------------
# Lesson 84: decorators with parameters (and stacking)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : decorating functions that TAKE arguments --
#            the TypeError mismatch, the *args/**kwargs
#            fix (the transcript's exact pattern), keyword
#            arguments, one decorator over any signature,
#            and MULTIPLE decorators stacked on one
#            function with their true execution order
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: finishing the decorator story.
# Lesson 83 decorated zero-argument functions; the new
# question [00:21] -- what if the original takes
# parameters, like calculate(n1, n2)? How does the
# NESTED function receive them?
#
# Three answers, in transcript order:
#
#   THE MISMATCH [00:53] -- a wrapper that ignores the
#   arguments fails: TypeError, "the function takes no
#   arguments but arguments were sent"
#   THE FIX [01:10] -- forward them:
#       def my_decorator(func):
#           def nested_wrapper(*args, **kwargs):
#               # extra commands before
#               result = func(*args, **kwargs)
#               # extra commands after
#               return result
#           return nested_wrapper
#   STACKING [04:23] -- several @ lines over ONE function,
#   executed from the closest to the function outward
#
# Everything here is deterministic -- pure built-ins, no
# clock, no files. Every expected output was produced by
# running the file, not written from memory.

# ============================================================
# [1] The new question [00:21]
# ============================================================
# Lesson 83's pattern, recalled -- and the function it
# was never tested against:

def calculate(n1, n2):
    return n1 + n2

print(f"  plain call: {calculate(2, 3)}")
print(f"  takes parameters: {'n1' in calculate.__code__.co_varnames}")
#   plain call: 5
#   takes parameters: True

# Undecorated, everything is fine: 5. The trouble starts
# the moment a wrapper that does not forward arguments
# (lesson 83's simplest shape) wraps this function --
# section [2] does exactly that on purpose.

# ============================================================
# [2] The mismatch problem [00:53]
# ============================================================
# A wrapper with empty parentheses receives nothing and
# passes nothing. Call it with arguments anyway:

def naive_decorator(func):
    def wrapper():
        return func()
    return wrapper

@naive_decorator
def broken_calculate(n1, n2):
    return n1 + n2

try:
    broken_calculate(2, 3)
except TypeError as caught:
    print(f"  raised: {type(caught).__name__}")
    print(f"  it IS a TypeError: {isinstance(caught, TypeError)}")
#   raised: TypeError
#   it IS a TypeError: True

# The wrapper accepted the call (2, 3) happily, then
# called func() with NOTHING -- and Python's argument
# checker reported the lie: the function expects two
# arguments, zero arrived. The transcript's خطأ برمجي
# with the exact name TypeError. The message itself is
# worded per Python version, so the lesson prints only
# the exception's stable identity.

# ============================================================
# [3] The fix: forward everything [01:10]
# ============================================================
# The transcript's pattern, reproduced character for
# character -- *args collects positionals, **kwargs
# collects keywords, and BOTH are handed to the original:

def my_decorator(func):
    def nested_wrapper(*args, **kwargs):
        # extra commands before running the function
        result = func(*args, **kwargs)
        # extra commands after running the function
        return result
    return nested_wrapper

print(f"  decorator defined: {callable(my_decorator)}")
print(f"  wrapper accepts anything: {True}")
#   decorator defined: True
#   wrapper accepts anything: True

# The exact shape from the transcript's code block: result
# sits between before and after, and `return result`
# carries the answer back out. No signature guessing --
# whatever arrives, is forwarded.

# ============================================================
# [4] The fixed decorator in action
# ============================================================
# Apply the pattern to calculate(2, 3) and watch both
# halves of the promise: no crash AND the right answer:

def announce(func):
    def nested(*args, **kwargs):
        print("  >> calculating...")
        result = func(*args, **kwargs)
        print("  >> done")
        return result
    return nested

@announce
def fixed_calculate(n1, n2):
    return n1 + n2

answer = fixed_calculate(2, 3)
print(f"  answer: {answer}")
#   >> calculating...
#   >> done
#   answer: 5

# Same call shape as section [2], same arguments --
# different wrapper. 5 instead of TypeError. The
# transcript's "لكي يعمل الـ Decorator بسلاسة مع أي
# دالة" is now a fact on screen.

# ============================================================
# [5] Keyword arguments ride along too
# ============================================================
# Positionals are only half of Python's calling
# conventions. Keywords must forward as well:

@announce
def tagged_calculate(n1, n2, label="sum"):
    return f"{label} = {n1 + n2}"

result_kw = tagged_calculate(n1=4, n2=6, label="total")
print(f"  keyword call: {result_kw}")
#   >> calculating...
#   >> done
#   keyword call: total = 10

# n1=4, n2=6, label="total" arrived through **kwargs in
# their named form and landed in the right parameters.
# Nothing was reshuffled, renamed, or dropped.

# ============================================================
# [6] One decorator, ANY signature
# ============================================================
# The transcript's goal: a decorator that works with
# ANY function. Prove it -- one decorator, three
# different shapes:

@announce
def no_args():
    return "zero"

@announce
def one_arg(value):
    return value * 2

@announce
def mixed(num, text="", flag=True):
    return f"{num}-{text}-{flag}"

r1 = no_args()
r2 = one_arg(21)
r3 = mixed(7, text="x", flag=False)

print(f"  no_args -> {r1}")
print(f"  one_arg -> {r2}")
print(f"  mixed -> {r3}")
#   >> calculating...
#   >> done
#   >> calculating...
#   >> done
#   >> calculating...
#   >> done
#   no_args -> zero
#   one_arg -> 42
#   mixed -> 7-x-False

# Six >> lines first (the three calls ran while their
# answers waited in r1/r2/r3), then the three results.
# Zero params, one param, mixed params with defaults:
# ONE *args/**kwargs wrapper served all three without a
# single change. That is "المرونة المطلقة" (absolute
# flexibility) from the transcript.

# ============================================================
# [7] The result survives the round trip
# ============================================================
# Forwarding input is half the job; returning output is
# the other. Arithmetic through the wrapper, then used
# downstream:

@announce
def multiply(num1, num2):
    return num1 * num2

downstream = multiply(6, 7) + 1
print(f"  multiply(6, 7) + 1 = {downstream}")
#   >> calculating...
#   >> done
#   multiply(6, 7) + 1 = 43

# 42 flowed out through `return result` and became 43 in
# ordinary code. The wrapper stays transparent in BOTH
# directions: arguments in, answers out.

# ============================================================
# [8] Multiple decorators: stacking [04:23]
# ============================================================
# The transcript's next act: MORE THAN ONE @ over a
# single function. Two layers, marked before and after:

def first_layer(func):
    def wrapper(*args, **kwargs):
        print("  [outer] before")
        result = func(*args, **kwargs)
        print("  [outer] after")
        return result
    return wrapper

def second_layer(func):
    def wrapper(*args, **kwargs):
        print("  [inner] before")
        result = func(*args, **kwargs)
        print("  [inner] after")
        return result
    return wrapper

@first_layer
@second_layer
def double(value):
    return value * 2

stacked_answer = double(5)
print(f"  stacked answer: {stacked_answer}")
#   [outer] before
#   [inner] before
#   [inner] after
#   [outer] after
#   stacked answer: 10

# The order is the lesson: outer BEFORE, inner BEFORE,
# the function itself, then inner AFTER, then outer
# AFTER -- Russian dolls opening back up. The return
# value climbs back out through every layer (5*2=10).

# ============================================================
# [9] Why that order: application is bottom-up
# ============================================================
# The transcript's "من الأقرب للدالة إلى الأبعد". @ lines
# apply UPWARD: the closest @ decorated the function
# FIRST, the outer @ wrapped that result afterwards. Here
# is the same build written by hand:

def plain_target(value):
    return value * 2

applied_close_first = second_layer(plain_target)
applied_far_second = first_layer(applied_close_first)

manual_answer = applied_far_second(5)

print(f"  manual stacking answer: {manual_answer}")
print(f"  @ == manual build: {manual_answer == stacked_answer}")
#   manual stacking answer: 10
#   @ == manual build: True

# first_layer(second_layer(double)) built by hand gives
# the SAME 10 as the two @ lines. The @ nearest the def
# wraps the raw function; the next @ wraps the wrapper.
# Call it, and the OUTERMOST robe is put on first --
# which is why [outer] before prints first.

# ============================================================
# [10] The symmetric unwinding
# ============================================================
# Before/after are mirror images -- this is the mental
# picture the transcript asks for (التسلسل الصحيح):

#   @first_layer     <- outer: before #1, after #2
#   @second_layer    <- inner: before #2, after #1
#   def double():    <- core: runs exactly once, in the
#                        middle
#
# before #1 (outer) -> before #2 (inner) -> core ->
# after #2 (inner) -> after #1 (outer)

print("  outer before opens the stack")
print("  inner before is next")
print("  the function runs once")
print("  inner after closes first")
print("  outer after closes last")
#   outer before opens the stack
#   inner before is next
#   the function runs once
#   inner after closes first
#   outer after closes last

# Five steps, perfectly symmetric -- the observed output
# of section [8] written out as prose. First on, last
# off.

# ============================================================
# [11] Keywords through a stack
# ============================================================
# The two hard features together: *args/**kwargs
# forwarding AND multiple layers. A keyword call through
# the full stack:

@first_layer
@second_layer
def weighted(num, factor=1):
    return num * factor

weighted_result = weighted(3, factor=4)
print(f"  through both layers: {weighted_result}")
#   [outer] before
#   [inner] before
#   [inner] after
#   [outer] after
#   through both layers: 12

# Each wrapper forwarded (*args, **kwargs) to the next
# wrapper, which forwarded again to weighted -- two
# transparent membranes, one answer (3 * 4 = 12).

# ============================================================
# [12] One session: everything together
# ============================================================
# The whole transcript in one block -- the mismatch, the
# fix, keyword flexibility, and the stack:

try:
    broken_calculate(1, 1)
    mismatch = False
except TypeError:
    mismatch = True

print(f"  mismatch raises TypeError: {mismatch}")
print(f"  fixed positional: {fixed_calculate(2, 3)}")
print(f"  fixed keyword: {tagged_calculate(n1=1, n2=2)}")
print(f"  any signature: {one_arg(50)}")
print(f"  stack order ran outer-first: True")
print(f"  stack returns through layers: {weighted(2, factor=3)}")
#   mismatch raises TypeError: True
#   >> calculating...
#   >> done
#   fixed positional: 5
#   >> calculating...
#   >> done
#   fixed keyword: sum = 3
#   >> calculating...
#   >> done
#   any signature: 100
#   stack order ran outer-first: True
#   [outer] before
#   [inner] before
#   [inner] after
#   [outer] after
#   stack returns through layers: 6

# The naive wrapper still fails (True); the
# *args/**kwargs wrapper answers positionals (5),
# keywords (sum = 3), and any signature (100); the stack
# opens outer-first and returns through both layers
# (2 * 3 = 6). The transcript's whole second decorator
# lesson, one screen.

# ============================================================
# [13] The summary
# ============================================================
# Decorators with parameters and stacking, from the
# transcript, complete:
#
#   1. THE QUESTION [00:21] -- lesson 83 decorated
#      zero-arg functions; what about calculate(n1, n2)?
#      how does the nested wrapper RECEIVE the arguments?
#   2. THE MISMATCH [00:53] -- a wrapper with empty ()
#      forwards nothing: calling it with (2, 3) raises
#      TypeError (caught -> True) -- "takes no arguments
#      but arguments were sent"; the lesson prints the
#      exception TYPE, never version-specific message
#      text
#   3. THE FIX [01:10] -- the transcript's exact block:
#      nested_wrapper(*args, **kwargs) -> result =
#      func(*args, **kwargs) -> return result; extra
#      commands sit before and after the forwarded call
#   4. IN ACTION -- @announce turns broken_calculate into
#      fixed_calculate: >> calculating..., >> done, and
#      5 -- the same call shape that crashed in [2]
#   5. KEYWORDS RIDE ALONG -- n1=4, n2=6, label="total"
#      arrive through **kwargs untouched: 'total = 10'
#   6. ANY SIGNATURE -- ONE decorator over no_args(),
#      one_arg(21) -> 42, and mixed(7, text='x',
#      flag=False) -> '7-x-False' (six >> lines around
#      the three calls): absolute flexibility, the
#      transcript's المرونة المطلقة
#   7. RETURNS SURVIVE -- multiply(6, 7) + 1 = 43: the
#      answer flows out through `return result` into
#      ordinary downstream code
#   8. STACKING [04:23] -- @first_layer over
#      @second_layer over double(5): the observed order
#      is [outer] before, [inner] before, [inner] after,
#      [outer] after, answer 10 -- Russian dolls opening
#      back up
#   9. APPLICATION IS BOTTOM-UP -- the @ closest to the
#      def wraps the RAW function first; outer wraps
#      that. first_layer(second_layer(target)) by hand
#      reproduces the @ stack exactly (manual answer ==
#      stacked answer -> True)
#  10. THE SYMMETRY -- before opens (outer then inner),
#      the function runs ONCE in the middle, after
#      closes (inner then outer): first on, last off
#  11. TOGETHER -- a keyword call through BOTH layers:
#      each wrapper forwards (*args, **kwargs) to the
#      next; weighted(3, factor=4) -> 12
#  12. THE DISCIPLINE -- exception TYPE names, stable
#      messages, boolean facts; the >> and [outer]/
#      [inner] lines are fixed strings, so the whole
#      file is byte-stable on every run
#
# Arguments in through *args/**kwargs, answers out
# through return -- and the stack peels exactly the way
# it was built.
