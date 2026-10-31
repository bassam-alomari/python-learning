# -----------------------------------------------------------------
# Lesson 107: class attributes -- shared data and user counts
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : class vs instance attributes, a shared blocked
#            first-name list, validation in __init__, class
#            user counter, and instance deletion behavior
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: move from instance attributes
# to class attributes and learn where each is used.
#
#   CLASS ATTRIBUTE [00:20] -- defined directly in the
#   class body, not inside __init__; shared by instances,
#   useful for common data that does not vary per object
#   BLOCKED NAMES [00:45] -- common list checked during
#   construction; reject Abuse, Admin and Root
#   USER COUNTER [04:39] -- class-level users_num starts at
#   zero and increments once per successfully created object
#   DELETE [06:58] -- del removes a reference; __del__ may
#   update the counter when an object is actually finalized
#
# Important Python detail: del does not itself guarantee
# immediate object destruction if other references remain.
# The deterministic example uses one reference per object.

# ============================================================
# [1] Class attribute vs instance attribute [00:20]
# ============================================================
# A class attribute is written in the class body; an
# instance attribute is usually assigned through self:

class Example:
    shared_kind = "member"

    def __init__(self, name):
        self.name = name


item = Example("Amin")
print(f"  class attribute: {Example.shared_kind}")
print(f"  instance attribute: {item.name}")
print(f"  shared value visible on instance: {item.shared_kind}")
#   class attribute: member
#   instance attribute: Amin
#   shared value visible on instance: member

# ============================================================
# [2] Class attributes are shared [00:20]
# ============================================================
# Instances read the same class-level value:

item_two = Example("Salma")
print(f"  same class value: {item.shared_kind == item_two.shared_kind}")
print(f"  class owns shared_kind: {'shared_kind' in Example.__dict__}")
print(f"  instance stores its name: {'name' in item.__dict__}")
#   same class value: True
#   class owns shared_kind: True
#   instance stores its name: True

# The shared attribute lives on the class; each name
# lives on its own instance.

# ============================================================
# [3] Shared list of blocked names [00:45]
# ============================================================
# Define the common blocked list directly in the class:

class Member:
    not_allowed_first_names = ["Abuse", "Admin", "Root"]

    def __init__(self, fname):
        if fname in Member.not_allowed_first_names:
            raise ValueError("first name is not allowed")
        self.fname = fname


print(f"  blocked names: {Member.not_allowed_first_names}")
print(f"  list belongs to class: 'not_allowed_first_names' in Member.__dict__")
#   blocked names: ['Abuse', 'Admin', 'Root']
#   list belongs to class: 'not_allowed_first_names' in Member.__dict__

# ============================================================
# [4] Accept permitted names
# ============================================================
# A permitted instance is created and stores its own name:

member_one = Member("Amin")
member_two = Member("Salma")
print(f"  first member: {member_one.fname}")
print(f"  second member: {member_two.fname}")
print(f"  shared blocked list: {member_one.not_allowed_first_names is member_two.not_allowed_first_names}")
#   first member: Amin
#   second member: Salma
#   shared blocked list: True

# ============================================================
# [5] Reject a blocked name in __init__ [00:45]
# ============================================================
# The name is rejected at construction time with a clear
# exception message:

try:
    Member("Admin")
except ValueError as error:
    blocked_rejected = str(error) == "first name is not allowed"
else:
    blocked_rejected = False

print(f"  Admin rejected: {blocked_rejected}")
print(f"  Root is in blocked list: 'Root' in Member.not_allowed_first_names")
#   Admin rejected: True
#   Root is in blocked list: 'Root' in Member.not_allowed_first_names

# ============================================================
# [6] A shared users_num class attribute [04:39]
# ============================================================
# Start a separate class counter at zero:

class CountedMember:
    users_num = 0

    def __init__(self, name):
        self.name = name
        CountedMember.users_num += 1


print(f"  initial counter: {CountedMember.users_num}")
#   initial counter: 0

# ============================================================
# [7] Increment once per new instance [04:39]
# ============================================================
# Every successful construction increments the class
# attribute, visible through the class and its instances:

counted_one = CountedMember("Amin")
print(f"  after one instance: {CountedMember.users_num}")
counted_two = CountedMember("Salma")
print(f"  after two instances: {CountedMember.users_num}")
print(f"  visible through instance: {counted_one.users_num}")
#   after one instance: 1
#   after two instances: 2
#   visible through instance: 2

# ============================================================
# [8] Do not shadow the class counter
# ============================================================
# Assigning through an instance creates an instance
# attribute and hides the class attribute for that object:

counted_one.users_num = 99
print(f"  shadowed instance value: {counted_one.users_num}")
print(f"  class counter unchanged: {CountedMember.users_num}")
print(f"  other instance sees class counter: {counted_two.users_num}")
#   shadowed instance value: 99
#   class counter unchanged: 2
#   other instance sees class counter: 2

# For a shared counter, update CountedMember.users_num,
# not counted_one.users_num.

# ============================================================
# [9] Decrement when an object is finalized [06:58]
# ============================================================
# __del__ runs when an object is finalized. This demo
# keeps one reference per object and observes del safely:

class ActiveMember:
    users_num = 0

    def __init__(self, name):
        self.name = name
        ActiveMember.users_num += 1

    def __del__(self):
        ActiveMember.users_num -= 1


active_one = ActiveMember("One")
active_two = ActiveMember("Two")
print(f"  active before del: {ActiveMember.users_num}")
del active_one
print(f"  active after del: {ActiveMember.users_num}")
#   active before del: 2
#   active after del: 1

# CPython finalizes an unreferenced object immediately in
# this simple case. Other Python implementations may
# defer finalization; production resource cleanup should
# use context managers, not depend on __del__ timing.

# ============================================================
# [10] Delete the remaining instance [06:58]
# ============================================================
# With no other reference to active_two, deleting its
# name leaves one active object fewer:

del active_two
print(f"  active after second del: {ActiveMember.users_num}")
#   active after second del: 0

# del removes the reference; when that was the last one,
# the object was finalized and the counter decremented.

# ============================================================
# [11] Blocked names and user counter side by side
# ============================================================
# One class attribute is shared policy; another shared
# class attribute tracks the count:

print(f"  blocked names shared: {member_one.not_allowed_first_names is Member.not_allowed_first_names}")
print(f"  registration counter: {CountedMember.users_num}")
print(f"  accepted members created: {member_one.fname}, {member_two.fname}")
#   blocked names shared: True
#   registration counter: 2
#   accepted members created: Amin, Salma

# ============================================================
# [12] One session: shared vs per-object data
# ============================================================
# Final comparison of class state and instance state:

print(f"  class policy: {Member.not_allowed_first_names}")
print(f"  per-object names: {member_one.fname}, {member_two.fname}")
print(f"  counted instances: {CountedMember.users_num}")
print(f"  independent member data: {member_one.__dict__ is not member_two.__dict__}")
print(f"  deletion counter reached zero: {ActiveMember.users_num == 0}")
#   class policy: ['Abuse', 'Admin', 'Root']
#   per-object names: Amin, Salma
#   counted instances: 2
#   independent member data: True
#   deletion counter reached zero: True

# ============================================================
# [13] The summary
# ============================================================
# Class Attributes, from the transcript:
#
#   1. CLASS ATTRIBUTE [00:20] -- declared in the class
#      body, outside __init__; shared by instances
#   2. INSTANCE ATTRIBUTE -- assigned through self;
#      each object owns its own value
#   3. BLOCKED NAMES [00:45] -- shared list
#      not_allowed_first_names; __init__ rejects Admin
#      with ValueError, and includes Abuse/Root too
#   4. COUNTER [04:39] -- users_num starts at zero and
#      increments through ClassName.users_num per instance
#   5. SHADOWING -- assigning instance.users_num creates
#      an instance attribute and does not change the class
#      counter; update the class directly instead
#   6. DELETE [06:58] -- __del__ can decrement when the
#      object is finalized; del removes a reference and
#      does not guarantee immediate destruction if other
#      references remain
#   7. PRACTICAL CAUTION -- finalizer timing may vary;
#      prefer context managers for reliable resource cleanup
#
# Shared policy/count belongs on the class; personal
# values belong on each instance.
