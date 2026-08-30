# Lesson 22 - List Methods (Part 1)
# Source: Elzero Python Course (Arabic) - Lesson #022
# Topic: append(), extend(), remove(), sort(), reverse()
# Type: Theory + Practical Code

# ============================================================
# append() - ADD ONE ITEM AT THE END
# ============================================================
# Adds a new item at the end of the list.
# Can add any type: String, Float, Boolean, etc.

myFriends = ["Osama", "Ahmed", "Sayed"]
myFriends.append("Alaa")
myFriends.append(100)
myFriends.append(150.200)
myFriends.append(True)

print(myFriends)
# Output: ['Osama', 'Ahmed', 'Sayed', 'Alaa', 100, 150.2, True]

print("=" * 50)

# ============================================================
# append() WITH A LIST (NESTED LIST)
# ============================================================
# If you append a whole list, it is added as ONE nested item.
# To access an item inside it -> use Nested Indexing.

myOldFriends = ["Haytham", "Samah", "Ali"]
myFriends.append(myOldFriends)

print(myFriends)
# Output: ['Osama', 'Ahmed', 'Sayed', 'Alaa', 100, 150.2, True, ['Haytham', 'Samah', 'Ali']]

print(myFriends[2])
# Output: Sayed

print(myFriends[6])
# Output: True

print(myFriends[7])
# Output: ['Haytham', 'Samah', 'Ali']

print(myFriends[7][2])
# Output: Ali  (Nested Indexing)

print("=" * 50)

# ============================================================
# extend() - ADD ALL ITEMS (NOT AS A NESTED LIST)
# ============================================================
# Adds all items of another list as SEPARATE items
# (not as one nested list like append()).

a = [1, 2, 3, 4]
b = ["A", "B", "C"]
c = ["One", "Two"]

a.extend(b)
a.extend(c)

print(a)
# Output: [1, 2, 3, 4, 'A', 'B', 'C', 'One', 'Two']

print("=" * 50)

# ============================================================
# remove() - REMOVE THE FIRST MATCHING ITEM
# ============================================================
# Removes the FIRST occurrence of the given value only.

x = [1, 2, 3, 4, 5, "Osama", True, "Osama", "Osama"]
x.remove("Osama")
print(x)
# Output: [1, 2, 3, 4, 5, True, 'Osama', 'Osama']
# (only the FIRST "Osama" was removed)

print("=" * 50)

# ============================================================
# sort() - SORT THE LIST
# ============================================================
# sort() -> ascending (small to big)
# sort(reverse=True) -> descending (big to small)
# NOTE: Cannot sort a list with mixed types (int + str).

y = [1, 2, 100, 120, -10, 17, 29]
y.sort(reverse=True)
print(y)
# Output: [120, 100, 29, 17, 2, 1, -10]

# y = [1, 2, 100, 120, -10, 17, 29, "Osama"]
# y.sort(reverse=True)
# TypeError: '<' not supported between instances of 'int' and 'str'

y = ["A", "Z", "C"]
y.sort(reverse=True)
print(y)
# Output: ['Z', 'C', 'A']

print("=" * 50)

# ============================================================
# reverse() - REVERSE THE ORDER
# ============================================================
# Reverses the current order of the items (does NOT sort).
# The last item becomes first, and the first becomes last.

z = [10, 1, 9, 80, 100, "Osama", 100]
z.reverse()
print(z)
# Output: [100, 'Osama', 100, 80, 9, 1, 10]

print("=" * 50)

# ============================================================
# SUMMARY
# ============================================================
# [1] append(item)  -> add ONE item at the end
# [2] append(list)  -> add a whole list as ONE nested item
# [3] extend(list)  -> add all items as separate items
# [4] remove(value) -> remove the FIRST matching item
# [5] sort()        -> sort ascending
# [6] sort(reverse=True) -> sort descending
# [7] reverse()     -> reverse the order (not sorting)
# [8] Nested Indexing -> myList[7][2] to access nested item

# ============================================================
# NEXT LESSON: List Methods (Part 2)
# ============================================================
