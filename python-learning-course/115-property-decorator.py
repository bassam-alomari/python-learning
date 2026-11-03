# -----------------------------------------------------------------
# Lesson 115: @property -- methods accessed like attributes
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : property decorator, method-call vs attribute
#            access, computed days lived from fixed dates,
#            read-only property and property getter behavior
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: a useful Python decorator --
# @property.
#
#   WHAT [00:23] -- turn a method into an attribute-like
#   property; access it without parentheses
#   METHOD vs PROPERTY [01:38] -- days_compute() vs
#   days_compute; same calculation, different interface
#   HOW [02:26] -- put @property directly above the method;
#   it becomes a getter property

from datetime import date

# ============================================================
# [1] A computed method needs parentheses [01:38]
# ============================================================
# Use fixed dates to make this example deterministic:

class MemberWithMethod:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

    def days_compute(self, today):
        return (today - self.birth_date).days


fixed_today = date(2026, 11, 3)
birth_date = date(2000, 1, 1)
method_member = MemberWithMethod("Amina", birth_date)
method_days = method_member.days_compute(fixed_today)

print(f"  method call with parentheses: {method_days}")
print(f"  method result type: {type(method_days).__name__}")
#   method call with parentheses: 9803
#   method result type: int

# ============================================================
# [2] A property is accessed without parentheses [00:23]
# ============================================================
# @property makes the computed value read like an
# attribute:

class MemberWithProperty:
    def __init__(self, name, birth_date, today):
        self.name = name
        self.birth_date = birth_date
        self.today = today

    @property
    def days_compute(self):
        return (self.today - self.birth_date).days


property_member = MemberWithProperty("Amina", birth_date, fixed_today)
property_days = property_member.days_compute
print(f"  property access without parentheses: {property_days}")
print(f"  property result type: {type(property_days).__name__}")
#   property access without parentheses: 9803
#   property result type: int

# ============================================================
# [3] Compare method and property results [01:38]
# ============================================================
# Both interfaces expose the same computed value:

print(f"  results are equal: {method_days == property_days}")
print(f"  property is not a bound method: {not callable(property_days)}")
#   results are equal: True
#   property is not a bound method: True

# A property is evaluated when accessed; the caller does
# not write parentheses.

# ============================================================
# [4] @property is a descriptor on the class [02:26]
# ============================================================
# The class stores a property descriptor; reading it on
# an instance invokes its getter:

print(f"  class attribute is property: {isinstance(MemberWithProperty.days_compute, property)}")
print(f"  property has a getter: {callable(MemberWithProperty.days_compute.fget)}")
#   class attribute is property: True
#   property has a getter: True

# ============================================================
# [5] A property can be computed from other attributes
# ============================================================
# It does not need to be stored separately; calculate it
# from the current object's data:

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height


rectangle = Rectangle(4, 5)
print(f"  computed area: {rectangle.area}")
rectangle.width = 6
print(f"  area after width changes: {rectangle.area}")
#   computed area: 20
#   area after width changes: 30

# The property always reflects the current width and height.

# ============================================================
# [6] Read-only by default
# ============================================================
# With no setter, assigning to a property raises
# AttributeError; handle it as an expected demonstration:

try:
    rectangle.area = 100
except AttributeError:
    assignment_rejected = True
else:
    assignment_rejected = False

print(f"  read-only property rejects assignment: {assignment_rejected}")
print(f"  computed area remains: {rectangle.area}")
#   read-only property rejects assignment: True
#   computed area remains: 30

# ============================================================
# [7] A property can validate assignment with a setter
# ============================================================
# Add @area.setter to control the write path:

class Box:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    @area.setter
    def area(self, value):
        if value <= 0:
            raise ValueError("area must be positive")
        self.width = value / self.height


box = Box(4, 5)
box.area = 60
print(f"  area updated through setter: {box.area}")
print(f"  width adjusted: {box.width}")
#   area updated through setter: 60.0
#   width adjusted: 12.0

# ============================================================
# [8] Setter validation rejects bad values
# ============================================================
# Invalid assignment is caught and leaves the valid area:

try:
    box.area = 0
except ValueError as error:
    bad_area_rejected = str(error) == "area must be positive"
else:
    bad_area_rejected = False

print(f"  zero area rejected: {bad_area_rejected}")
print(f"  previous area preserved: {box.area}")
#   zero area rejected: True
#   previous area preserved: 60.0

# ============================================================
# [9] Property vs explicit getter syntax
# ============================================================
# Compare the direct property syntax with a conventional
# getter method:

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    def get_fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32


temperature = Temperature(20)
print(f"  getter method: {temperature.get_fahrenheit()}")
print(f"  property access: {temperature.fahrenheit}")
print(f"  values agree: {temperature.get_fahrenheit() == temperature.fahrenheit}")
#   getter method: 68.0
#   property access: 68.0
#   values agree: True

# ============================================================
# [10] Properties keep the public interface stable
# ============================================================
# A property lets the implementation compute a value
# while callers use simple attribute syntax:

print(f"  rectangle looks like attribute: {rectangle.area}")
print(f"  days lived looks like attribute: {property_member.days_compute}")
print(f"  neither access uses parentheses: True")
#   rectangle looks like attribute: 30
#   days lived looks like attribute: 9803
#   neither access uses parentheses: True

# ============================================================
# [11] Fixed-date arithmetic is repeatable
# ============================================================
# Expose the dates used by the example, without using
# today's live clock:

print(f"  fixed today: {fixed_today.isoformat()}")
print(f"  fixed birth date: {birth_date.isoformat()}")
print(f"  days calculation consistent: {property_days == (fixed_today - birth_date).days}")
#   fixed today: 2026-11-03
#   fixed birth date: 2000-01-01
#   days calculation consistent: True

# ============================================================
# [12] One session: methods and properties
# ============================================================
# The key examples together:

print(f"  method days_compute(): {method_member.days_compute(fixed_today)}")
print(f"  property days_compute: {property_member.days_compute}")
print(f"  rectangle area property: {rectangle.area}")
print(f"  Box area with setter: {box.area}")
print(f"  Fahrenheit property: {temperature.fahrenheit}")
#   method days_compute(): 9803
#   property days_compute: 9803
#   rectangle area property: 30
#   Box area with setter: 60.0
#   Fahrenheit property: 68.0

# ============================================================
# [13] The summary
# ============================================================
# @property, from the transcript:
#
#   1. WHAT [00:23] -- turns a method into an attribute-
#      like property; access without ()
#   2. METHOD [01:38] -- member.days_compute(today)
#      explicitly calls a method with parentheses
#   3. PROPERTY [01:38-02:26] -- @property above the
#      method lets member.days_compute read like a value
#   4. COMPUTED VALUES -- area and days lived derive from
#      other attributes and stay current when they change
#   5. GETTER -- @property supplies a read interface
#   6. READ-ONLY -- without a setter, assignment is rejected
#   7. SETTER -- @area.setter validates and updates through
#      attribute assignment
#   8. DETERMINISM -- fixed dates avoid live-clock output
#
# A property keeps convenient attribute syntax while
# allowing a method to compute or control the value.
