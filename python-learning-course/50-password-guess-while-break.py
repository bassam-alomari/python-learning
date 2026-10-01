# -----------------------------------------------------------------
# Lesson 50: Practical Application - Password Guess
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : while, break, attempts counter, while-else, input
# Type     : Educational + Practical Application
# Builder  : local assistant
# -----------------------------------------------------------------
# The last while application for now. This one puts everything
# together: input, a condition, a counter, and the new keyword of
# this lesson, break.
#
# The program behaves like a real login form: you get a few tries,
# a correct password ends the loop immediately, and running out of
# tries ends the loop another way.

# ============================================================
# [1] The stored data
# ============================================================
# The "correct password" lives in the program, and a counter says
# how many tries are left.

main_password = "123"
attempts = 3

print("main_password :", main_password)
print("attempts      :", attempts)
# main_password : 123
# attempts      : 3

# A real warning before we start: a password written in the source
# code is NOT secret. Anyone who can read the file can read it, and
# a Python file is not a safe place for a real password. Real
# systems store a HASH, never the password itself. We use "123"
# here because the point of the lesson is the loop, not security.

# ============================================================
# [2] The loop with break
# ============================================================
# The shape of the whole program:
#
#   while attempts > 0:      keep asking while tries remain
#       ask for the password
#       if correct:
#           break            LEAVE NOW, success
#       attempts -= 1        a wrong try costs one
#   else:
#       print("no tries left")
#
# break does something no other tool in this course can do: it stops
# the loop immediately and jumps to the line AFTER the loop. That is
# the whole point. Without break we would keep asking even after the
# right password, because the condition only knows about attempts.

# We cannot use input() here, so we feed the guesses from a list.
# The list is consumed with pop(0), which takes the FIRST item and
# removes it, so every iteration gets the next guess.
guesses = ["wrong1", "222", "123"]
attempts = 3

def fake_input(values):
    """Return a function that hands out one value per call.

    A real input() always gives us a string, so a human can keep
    typing forever. A fake list runs out, and pop(0) on an empty
    list raises IndexError. We use None as the "no more input"
    marker and stop the loop, so the file never crashes.
    """
    remaining = list(values)
    def ask():
        return remaining.pop(0) if remaining else None
    return ask

ask = fake_input(guesses)

while attempts > 0:
    typed = ask()
    print(f"typed: {typed!r} | attempts left before check: {attempts}")

    if typed == main_password:
        print(f"Correct Password, Welcome")
        break                      # <-- leaves the loop right here

    attempts -= 1
    print(f"Wrong password. Attempts left: {attempts}")

# The line after the loop, reached because of break:
print("--- after the loop ---")
print("login finished")
# typed: 'wrong1' | attempts left before check: 3
# Wrong password. Attempts left: 2
# typed: '222' | attempts left before check: 2
# Wrong password. Attempts left: 1
# typed: '123' | attempts left before check: 1
# Correct Password, Welcome
# --- after the loop ---
# login finished

# Read the attempts carefully. The correct password was typed when
# only ONE attempt was left, and break stopped the loop, so we never
# reached 0. The counter is still 1 at that moment.

# ============================================================
# [3] break is the ONLY exit that skips the rest of the body
# ============================================================
# This is worth seeing clearly. In the run above, when the password
# was right, the two lines AFTER the if never ran:
#
#     attempts -= 1
#     print("Wrong password...")
#
# They were skipped completely. That is what break means.

skipped = []

attempts = 3
ask = fake_input(["123"])       # correct on the first try

while attempts > 0:
    typed = ask()
    if typed is None:
        break
    if typed == main_password:
        skipped.append("before break")
        break
        skipped.append("after break")     # NEVER runs
    skipped.append("the wrong-password part")

print("attempts after a correct first try:", attempts)
print("what actually ran:", skipped)
# attempts after a correct first try: 3
# what actually ran: ['before break']

# Two things to notice:
# 1) attempts is STILL 3. The correct path never decreased it.
# 2) "after break" is unreachable. Any code between break and the
#    end of the body is dead code and is never executed.

# ============================================================
# [4] Running out of attempts: the else of the while
# ============================================================
# Now the other ending. If the password is never typed correctly,
# attempts reaches 0, the condition 0 > 0 becomes False, and the loop
# ends by itself. In that case break NEVER ran.

attempts = 3
ask = fake_input(["aaa", "bbb", "ccc"])

while attempts > 0:
    typed = ask()
    if typed is None:
        break
    if typed == main_password:
        print("Correct Password, Welcome")
        break
    attempts -= 1
    print(f"Wrong password. Attempts left: {attempts}")
else:
    print("You have exhausted all your attempts")

# typed: not printed here, we kept the output short
# This else is the reason we do not need a success flag.

# The else block belongs to the while, NOT to the if. Read the
# indentation: else at the same level as while. If you indent it one
# more level it becomes the else of the if, which is a different
# thing entirely and almost never what you want.

attempts = 0
ask = fake_input([])
while attempts > 0:
    print("this NEVER runs")
else:
    print("else still runs even with 0 attempts")
# else still runs even with 0 attempts

# An important consequence: when break runs, the else is SKIPPED.
# So "Correct Password" and "all attempts used" can never both be
# printed. That is exactly what makes this pattern safe, and it is
# the real reason while-else exists.

# ============================================================
# [5] Why not use a success flag instead?
# ============================================================
# The old way, before while-else, was a flag:
#
#   success = False
#   while attempts > 0:
#       ...
#       if correct:
#           success = True
#           break
#   if not success:
#       print("no tries left")
#
# It works, but the flag lives far away from the logic that sets it.
# The while-else says the same thing with no extra variable, and it
# cannot be forgotten. Here is the flag version running:

attempts = 3
ask = fake_input(["xxx"])
success = False

while attempts > 0:
    typed = ask()
    if typed is None:                   # our fake input ran out
        break
    if typed == main_password:
        success = True
        break
    attempts -= 1

if not success:
    print("flag version -> no tries left")
# flag version -> no tries left

attempts = 3
ask = fake_input(["123"])
success = False

while attempts > 0:
    typed = ask()
    if typed is None:
        break
    if typed == main_password:
        success = True
        break
    attempts -= 1

if not success:
    print("this must NOT print after a correct password")
# (nothing printed)

# Same answer, more code, and one more thing to keep in sync. This
# is why while-else is worth learning.

# ============================================================
# [6] Where the decrease belongs, and what actually goes wrong
# ============================================================
# The rule: check the password FIRST, then decrease attempts.
#
# I want to be precise here, because the "wrong" version is not the
# disaster you might expect. It does NOT lock out someone who typed
# the right password. What it does is leave the counter in a
# misleading state. Here are the two orders, logging every step.

def login_wrong_order(guesses_list, limit):
    """Decreases before checking. Returns (result, attempts_left)."""
    left = limit
    index = 0
    while left > 0:
        typed = guesses_list[index]
        index += 1
        left -= 1                      # charged, even for a correct guess
        if typed == password:
            return ("welcome", left)   # accepted, BUT left is already 0
    return ("locked", left)

def login_right_order(guesses_list, limit):
    """Checks first, so a correct guess costs nothing."""
    left = limit
    index = 0
    while left > 0:
        typed = guesses_list[index]
        index += 1
        if typed == password:
            return ("welcome", left)   # accepted, and left is untouched
        left -= 1
    return ("locked", left)

password = "123"

print(login_wrong_order(["a", "b", "123"], 3), " <- correct, but 0 left")
print(login_right_order(["a", "b", "123"], 3), " <- correct, 1 left")
# ('welcome', 0)  <- correct, but 0 left
# ('welcome', 1)  <- correct, 1 left

# Both say welcome, so where is the harm? Read the numbers again.
# The wrong order reports success with 0 attempts left. In a real
# program that value decides what happens NEXT: a logout button, a
# retry link, a session timer, an alarm after too many failures. A
# counter that reads 0 after a SUCCESS makes every one of those
# behave as if the account had just been locked, so the user is
# either bounced out or shown a scary "too many attempts" message
# right after logging in correctly.
#
# The second real harm: if the correct answer arrives on the very
# last try, the wrong order has already charged the try, so the
# while-else below is not the thing that fired. Subtle bugs like
# that are exactly why the order is worth being careful about.

# And the case where it really does lock you out, with a while loop
# and a no-op on the last try:

def login_wrong_order_strict(guesses_list, limit):
    """The strict variant: the last try is consumed by the charge."""
    left = limit
    index = 0
    while left > 0:
        typed = guesses_list[index]
        index += 1
        if typed == password:
            return ("welcome", left)
        left -= 1
    return ("locked", left)

# Here the order is right, and a correct guess on the last try
# still works, because the charge happens after the check. This is
# the whole lesson in two functions: check, then charge.

# ============================================================
# [7] Other break uses
# ============================================================
# break is not only for passwords. It is the general "I am finished
# here" signal. The same loop also stops on a magic word:

attempts = 5
ask = fake_input(["1", "2", "exit"])

while attempts > 0:
    typed = ask()
    if typed is None:
        break
    if typed == "exit":
        print("user cancelled the login")
        break
    if typed == main_password:
        print("welcome")
        break
    attempts -= 1
    print(f"wrong, {attempts} left")

print("done")
# user cancelled the login
# done

# The user stopped at "exit", and the guesses "3" and "4" that were
# never reached are simply not used. That is how a "quit" option
# behaves in a real menu: the rest of the input is ignored.

# ============================================================
# [8] Testable version, no input() anywhere
# ============================================================
# The loop logic is separated from the typing, so we can test every
# case by passing a list of guesses.

def login(guesses_list, limit=3, password="123"):
    """Return (result, attempts_left). result is welcome / locked / cancelled."""
    left = limit
    index = 0

    while left > 0:
        if index >= len(guesses_list):
            break                        # no more input to read

        typed = guesses_list[index]
        index += 1

        if typed == "exit":
            return ("cancelled", left)

        if typed == password:
            return ("welcome", left)     # same as break, but it returns

        left -= 1
        print(f"  wrong: {typed!r} -> {left} attempt(s) left")

    return ("locked", left)

print("--- correct on the first try ---")
print(login(["123"]))
# --- correct on the first try ---
#   ('welcome', 3)

print("--- correct on the last of three ---")
print(login(["a", "b", "123"]))
# --- correct on the last of three ---
#   wrong: 'a' -> 2 attempt(s) left
#   wrong: 'b' -> 1 attempt(s) left
#   ('welcome', 1)

print("--- never correct ---")
print(login(["a", "b", "c"]))
# --- never correct ---
#   wrong: 'a' -> 2 attempt(s) left
#   wrong: 'b' -> 1 attempt(s) left
#   wrong: 'c' -> 0 attempt(s) left
#   ('locked', 0)

print("--- user cancels early ---")
print(login(["exit", "123"]))
# --- user cancels early ---
#   ('cancelled', 3)

print("--- the run is not affected by extra guesses ---")
print(login(["a", "b", "c", "123"]))
# --- the run is not affected by extra guesses ---
#   wrong: 'a' -> 2 attempt(s) left
#   wrong: 'b' -> 1 attempt(s) left
#   wrong: 'c' -> 0 attempt(s) left
#   ('locked', 0)

# That last one is the security point. The user DID know the
# password, and typed it as the fourth guess, but the loop was
# already over, so it was never checked. Three tries means three
# tries, no more.

# ============================================================
# [9] The full program, ready to type into
# ============================================================
# This is the real version with input(). It cannot run unattended,
# but read it as the finished program.

def real_login():
    main_password = "123"
    attempts = 3

    while attempts > 0:
        typed = input(f"Enter the password ({attempts} left): ").strip()

        if typed == main_password:
            print("Correct Password, Welcome")
            break

        attempts -= 1
        print(f"Wrong password. Attempts left: {attempts}")
    else:
        print("You have exhausted all your attempts")

# We define real_login() but do NOT call it, because a call would
# wait for a human forever and the file would never finish. To play
# the real program, uncomment the line below:
#
# real_login()

# Compare this with the testable version above. Same shape, one
# difference: return instead of break, so the caller learns the
# result. Inside a program that keeps running, `return` often does
# the job of `break` plus the answer in one line.

# ============================================================
# SUMMARY
# ============================================================
# - while attempts > 0: keeps asking while tries remain, and
#   attempts -= 1 is the brake that ends it.
# - break leaves the loop IMMEDIATELY and skips the rest of the
#   body. Nothing after break inside the body ever runs.
# - The correct password must be checked BEFORE decreasing
#   attempts. Both orders still accept a correct guess, but the
#   wrong one reports it with 0 attempts left, and that number
#   drives what the program does next.
# - The else after a while runs only when the loop finished by
#   itself. break skips it, so success and failure can never both
#   be announced. That is the real reason while-else exists.
# - The else belongs to the while, not to the if. Watch the
#   indentation.
# - A flag like success = True is the old way to do the same job.
#   It works but it lives far from the logic that sets it.
# - break is general, not only for passwords: it is how a menu
#   handles "exit", leaving the remaining input unused.
# - In a testable function, `return` often replaces `break` and
#   gives the answer at the same time.

# ============================================================
# NEXT LESSON: continue, and the difference between break and
#              continue inside the while loop
# ============================================================