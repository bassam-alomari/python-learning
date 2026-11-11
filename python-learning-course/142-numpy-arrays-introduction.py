# -----------------------------------------------------------------
# Lesson 142: NumPy arrays -- a first comparison
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : NumPy arrays, homogeneous element types,
# Topic continuation: shape and dtype, elementwise operations, and
# Topic continuation: differences from Python lists
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript introduces NumPy and its arrays, compares
# arrays with Python lists, notes that array elements share
# a data type, and creates arrays with matching dimensions.
# The exact examples are unclear, so this lesson uses small
# deterministic integer arrays.
#
# Install command if needed:
# Setup command: python -m pip install numpy
#
# NumPy is available in this environment. The lesson avoids
# printing version numbers or machine-specific information.

import numpy as np

# ============================================================
# [1] NumPy is for numerical arrays
# ============================================================
# NumPy supplies an ndarray type and array-oriented functions.

print(f"  NumPy imported: {np.__name__ == 'numpy'}")
#   NumPy imported: True
print(f"  ndarray available: {hasattr(np, 'ndarray')}")
#   ndarray available: True
print(f"  array constructor available: {callable(np.array)}")
#   array constructor available: True

# ============================================================
# [2] A Python list and a NumPy array
# ============================================================
# Both can store several values, but they have different
# types and operation rules.

values_list = [1, 2, 3]
values_array = np.array([1, 2, 3])
print(f"  list type: {type(values_list).__name__}")
#   list type: list
print(f"  array type: {type(values_array).__name__}")
#   array type: ndarray
print(f"  same values: {values_list == values_array.tolist()}")
#   same values: True

# ============================================================
# [3] Arrays have a shape and dtype
# ============================================================
# A one-dimensional array with three entries has shape (3,).

print(f"  array shape: {values_array.shape}")
#   array shape: (3,)
print(f"  array dimension count: {values_array.ndim}")
#   array dimension count: 1
print(f"  array data type kind: {values_array.dtype.kind}")
#   array data type kind: i

# ============================================================
# [4] Matching dimensions
# ============================================================
# Two arrays with three entries have matching shapes.

first = np.array([1, 2, 3])
second = np.array([10, 20, 30])
print(f"  first shape: {first.shape}")
#   first shape: (3,)
print(f"  second shape: {second.shape}")
#   second shape: (3,)
print(f"  shapes match: {first.shape == second.shape}")
#   shapes match: True

# ============================================================
# [5] NumPy adds element by element
# ============================================================
# The same-length arrays combine corresponding positions.

sum_array = first + second
print(f"  elementwise sum: {sum_array.tolist()}")
#   elementwise sum: [11, 22, 33]
print(f"  elementwise product: {(first * second).tolist()}")
#   elementwise product: [10, 40, 90]

# ============================================================
# [6] List plus and array plus differ
# ============================================================
# Python list + joins lists; ndarray + adds values.

joined_list = [1, 2, 3] + [10, 20, 30]
added_array = (np.array([1, 2, 3]) + np.array([10, 20, 30])).tolist()
print(f"  list plus: {joined_list}")
#   list plus: [1, 2, 3, 10, 20, 30]
print(f"  array plus: {added_array}")
#   array plus: [11, 22, 33]

# ============================================================
# [7] The * operator differs too
# ============================================================
# A list repeats; an array multiplies each entry by a scalar.

list_repeat = [1, 2, 3] * 2
array_scale = (np.array([1, 2, 3]) * 2).tolist()
print(f"  list times two: {list_repeat}")
#   list times two: [1, 2, 3, 1, 2, 3]
print(f"  array times two: {array_scale}")
#   array times two: [2, 4, 6]

# ============================================================
# [8] Array elements share a dtype
# ============================================================
# A NumPy array stores elements using one data type.

mixed = np.array([1, 2.5, 3])
print(f"  mixed array dtype kind: {mixed.dtype.kind}")
#   mixed array dtype kind: f
print(f"  mixed array values: {mixed.tolist()}")
#   mixed array values: [1.0, 2.5, 3.0]
print(f"  values use one dtype: {len({str(item.dtype) for item in [mixed]}) == 1}")
#   values use one dtype: True

# ============================================================
# [9] A two-dimensional array
# ============================================================
# Nested rows form a two-dimensional matrix-like array.

matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(f"  matrix shape: {matrix.shape}")
#   matrix shape: (2, 3)
print(f"  matrix dimension count: {matrix.ndim}")
#   matrix dimension count: 2
print(f"  second row: {matrix[1].tolist()}")
#   second row: [4, 5, 6]

# ============================================================
# [10] Arrays have fixed shape for elementwise operations
# ============================================================
# Equal-shaped arrays combine position by position.

left = np.array([2, 4, 6])
right = np.array([1, 3, 5])
difference = left - right
print(f"  elementwise difference: {difference.tolist()}")
#   elementwise difference: [1, 1, 1]
print(f"  result shape preserved: {difference.shape == left.shape}")
#   result shape preserved: True

# ============================================================
# [11] Useful aggregate operations
# ============================================================
# Arrays provide concise numerical reductions.

scores = np.array([70, 80, 90])
print(f"  sum: {int(scores.sum())}")
#   sum: 240
print(f"  mean: {scores.mean():.1f}")
#   mean: 80.0
print(f"  maximum: {int(scores.max())}")
#   maximum: 90

# ============================================================
# [12] The core distinction
# ============================================================
# Lists are general-purpose containers; arrays are designed
# for same-dtype numerical work.

print(f"  list is general container: {isinstance(values_list, list)}")
#   list is general container: True
print(f"  ndarray is NumPy array: {isinstance(values_array, np.ndarray)}")
#   ndarray is NumPy array: True
print(f"  array uses homogeneous dtype: {values_array.dtype.kind == 'i'}")
#   array uses homogeneous dtype: True

# ============================================================
# [13] The summary
# ============================================================
# NumPy basics from the transcript:
# NumPy provides ndarray arrays; arrays have shape and dtype;
# numerical operations usually work elementwise; Python list
# + concatenates and list * repeats, while ndarray + adds and
# ndarray * scalar scales. NumPy arrays store one dtype and
# are useful for numerical data. Example values here are small
# and deterministic; install with python -m pip install numpy.
#
# An ndarray is not merely another list: its shape and dtype
# define how numerical operations are interpreted.
