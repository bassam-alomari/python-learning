# Lesson 19 - Numbers
# Source: Elzero Python Course (Arabic) - Lesson #019
# Topic: Integer (int), Float, Complex, Type Casting
# Type: Theory + Practical Code

# ============================================================
# INTEGER (int)
# ============================================================
# The normal number: positive, negative, or zero.
# Examples: 1, 100, 10, -10, -110

print(type(1))
print(type(100))
print(type(10))
print(type(-10))
print(type(-110))
# Output: <class 'int'> (all of them)

print("=" * 50)

# ============================================================
# FLOAT
# ============================================================
# A number with a decimal point (fraction).
# Examples: 1.500, 100.99, -10.99, 0.99, -0.99

print(type(1.500))
print(type(100.99))
print(type(-10.99))
print(type(0.99))
print(type(-0.99))
# Output: <class 'float'> (all of them)

print("=" * 50)

# ============================================================
# COMPLEX
# ============================================================
# Complex Number: has a Real part and an Imaginary part.
# Written like: 5 + 6j
# .real -> the Real part
# .imag -> the Imaginary part

myComplexNumber = 5+6j

print(type(myComplexNumber))
# Output: <class 'complex'>

print("Real Part Is: {}".format(myComplexNumber.real))
# Output: Real Part Is: 5.0

print("Imaginary Part Is: {}".format(myComplexNumber.imag))
# Output: Imaginary Part Is: 6.0

print("=" * 50)

# ============================================================
# TYPE CASTING (Converting Between Types)
# ============================================================
# [1] You Can Convert From Int To Float or Complex
# [2] You Can Convert From Float To Int or Complex
# [3] You Cannot Convert Complex To Any Type

# Int -> Float and Complex
print(100)
# Output: 100

print(float(100))
# Output: 100.0

print(complex(100))
# Output: (100+0j)

print("=" * 50)

# Float -> Int and Complex
print(10.50)
# Output: 10.5

print(int(10.50))
# Output: 10  (removes the decimal part)

print(complex(10.50))
# Output: (10.5+0j)

print("=" * 50)

# Complex -> Cannot convert (TypeError)
print(10+9j)
# Output: (10+9j)

# print(int(10+9j))
# TypeError: can't convert complex to int

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] int     -> normal number (positive, negative, zero)
# [2] float   -> number with decimal point
# [3] complex -> number with Real + Imaginary part (5+6j)
# [4] .real   -> get the Real part of a complex number
# [5] .imag   -> get the Imaginary part of a complex number
# [6] int()   -> convert to Integer (removes decimal part)
# [7] float() -> convert to Float
# [8] complex() -> convert to Complex
# [9] You CANNOT convert Complex to any other type

# ============================================================
# NEXT LESSON: Arithmetic Operators
# ============================================================
