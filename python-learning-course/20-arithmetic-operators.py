# Lesson 20 - Arithmetic Operators
# Source: Elzero Python Course (Arabic) - Lesson #020
# Topic: + - * / % ** //
# Type: Theory + Practical Code

# ============================================================
# ARITHMETIC OPERATORS
# ============================================================
# [+] Addition
# [-] Subtraction
# [*] Multiplication
# [/] Division
# [%] Modulus (Remainder)
# [**] Exponent (Power)
# [//] Floor Division (Integer Division)

print("=" * 50)

# ============================================================
# ADDITION (+)
# ============================================================

print(10 + 30)   # 40
print(-10 + 20)   # 10
print(1 + 2.66)   # 3.66
print(1.2 + 1.2)   # 2.4

print("=" * 50)

# ============================================================
# SUBTRACTION (-)
# ============================================================

print(60 - 30)  # 30
print(-30 - 20)  # -50
print(-30 - -20)  # -10
print(5.66 - 3.44)  # 2.22

print("=" * 50)

# ============================================================
# MULTIPLICATION (*)
# ============================================================
# NOTE: Multiplication happens BEFORE Addition
# (Operator Precedence). Use ( ) to change the order.

print(10 * 3)  # 30
print(5 + 10 * 100)  # 1005  (10*100=1000, then +5)
print((5 + 10) * 100)  # 1500  ((5+10)=15, then *100)

print("=" * 50)

# ============================================================
# DIVISION (/)
# ============================================================
# Always returns a Float number.

print(100 / 20)  # 5.0
print(int(100 / 20))  # 5  (convert to int)

print("=" * 50)

# ============================================================
# MODULUS (%) - REMAINDER
# ============================================================
# Returns the remainder of the division.

print(8 % 2)  # 0  (8 is divisible by 2)
print(9 % 2)  # 1  (9 / 2 = 4 remainder 1)
print(20 % 5)  # 0  (20 is divisible by 5)
print(22 % 5)  # 2  (22 / 5 = 4 remainder 2)

print("=" * 50)

# ============================================================
# EXPONENT (**) - POWER
# ============================================================
# 2 ** 5 = 2 * 2 * 2 * 2 * 2 = 32

print(2 ** 5)  # 32
print(2 * 2 * 2 * 2 * 2)  # 32

print(5 ** 4)  # 625
print(5 * 5 * 5 * 5)  # 625

print("=" * 50)

# ============================================================
# FLOOR DIVISION (//)
# ============================================================
# Returns the division result rounded DOWN to the nearest
# integer (removes the decimal part).

print(100 // 20)  # 5
print(119 // 20)  # 5  (119/20 = 5.95 -> 5)
print(120 // 20)  # 6
print(140 // 20)  # 7

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [+] Addition        -> 10 + 30 = 40
# [-] Subtraction     -> 60 - 30 = 30
# [*] Multiplication  -> 10 * 3 = 30
# [/] Division        -> 100 / 20 = 5.0 (always float)
# [%] Modulus         -> 9 % 2 = 1 (remainder)
# [**] Exponent       -> 2 ** 5 = 32 (power)
# [//] Floor Division -> 119 // 20 = 5 (round down)
#
# Operator Precedence: ( ) > ** > * / % // > + -

# ============================================================
# NEXT LESSON: Assignment Operators
# ============================================================
