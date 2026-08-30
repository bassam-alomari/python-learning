# Lesson 23 - List Methods (Part 2)
# Source: Elzero Python Course (Arabic) - Lesson #023
# Topic: clear(), copy(), count(), index(), insert(), pop()
# Type: Theory + Practical Code

# ============================================================
# clear() - EMPTY THE LIST
# ============================================================
# Removes ALL items from the list (makes it empty).
# Useful e.g. when clearing a shopping cart.

a = [1, 2, 3, 4]
a.clear()
print(a)
# Output: []

print("=" * 50)

# ============================================================
# copy() - COPY THE LIST
# ============================================================
# Creates a copy of the list so you can modify the copy
# WITHOUT affecting the original list.
# Very important when you need to edit a copy but keep
# the original data unchanged.

b = [1, 2, 3, 4]
c = b.copy()
c.append(5)

print(b)
# Output: [1, 2, 3, 4]  (original NOT changed)

print(c)
# Output: [1, 2, 3, 4, 5]  (copy was modified)

print("=" * 50)

# ============================================================
# count() - COUNT HOW MANY TIMES AN ITEM APPEARS
# ============================================================
# Counts how many times a specific value appears in the list.

d = [1, 2, 3, 4, 1, 1, 5, 1]
print(d.count(1))
# Output: 4  (the number 1 appears 4 times)

print("=" * 50)

# ============================================================
# index() - GET THE INDEX OF AN ITEM
# ============================================================
# Returns the index of the FIRST matching item.

e = ["Osama", "Ahmed", "Sayed", "Osama"]
print(e.index("Osama"))
# Output: 0  (first "Osama" is at index 0)

print("=" * 50)

# ============================================================
# insert() - ADD AN ITEM AT A SPECIFIC POSITION
# ============================================================
# Adds an item at a specific index (unlike append() which
# always adds at the end).
# insert(index, value) -> puts the value BEFORE that index.

f = [1, 2, 3, 4, 5]
f.insert(0, "Zero")   # add "Zero" at index 0 (before everything)
f.insert(-1, "Last")  # add "Last" before the last item

print(f)
# Output: ['Zero', 1, 2, 3, 4, 'Last', 5]

print("=" * 50)

# ============================================================
# pop() - REMOVE AND RETURN AN ITEM
# ============================================================
# Removes an item (by index) and RETURNS it.
# If no index is given, it removes the LAST item by default.

g = [10, 20, 30, 40, 50]
print(g.pop())       # removes & returns the last item
# Output: 50

print(g.pop(0))      # removes & returns the item at index 0
# Output: 10

print(g)
# Output: [20, 30, 40]

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] clear()            -> empty the whole list
# [2] copy()             -> make a copy (edit without affecting original)
# [3] count(value)       -> count how many times a value appears
# [4] index(value)       -> get the index of the first match
# [5] insert(index, val) -> add an item at a specific position
# [6] pop()              -> remove & return the last item
# [7] pop(index)         -> remove & return the item at that index

# ============================================================
# NEXT LESSON: List Methods (Part 3)
# ============================================================
