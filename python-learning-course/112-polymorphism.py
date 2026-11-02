# -----------------------------------------------------------------
# Lesson 112: polymorphism -- one interface, many behaviors
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : polymorphism, built-in + and len() across types,
#            shared parent interface, child overrides,
#            and processing mixed objects uniformly
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: an important OOP principle --
# Polymorphism (تعدد الأوجه).
#
#   WHAT [00:10] -- the same operation/name can perform
#   different behavior depending on the object or type
#   BUILT-INS [00:35] -- + adds numbers, concatenates
#   strings and joins lists; len() counts items, characters
#   or dictionary keys
#   OOP [02:45] -- a parent defines a common interface;
#   child classes override it with behavior suited to each
#   object, so callers can use one interface uniformly

# ============================================================
# [1] Polymorphism: one operation, different forms [00:10]
# ============================================================
# The plus operator's meaning depends on operand types:

number_result = 10 + 20
text_result = "Py" + "thon"
list_result = [1, 2] + [3, 4]

print(f"  int + int: {number_result}")
print(f"  str + str: {text_result}")
print(f"  list + list: {list_result}")
#   int + int: 30
#   str + str: Python
#   list + list: [1, 2, 3, 4]

# Same operator symbol, arithmetic or concatenation
# depending on the operands.

# ============================================================
# [2] len() works across different types [00:35]
# ============================================================
# The same function asks each object for its length:

print(f"  len(list): {len(['red', 'blue', 'green'])}")
print(f"  len(str): {len('Python')}")
print(f"  len(dict): {len({'name': 'Amina', 'age': 29})}")
#   len(list): 3
#   len(str): 6
#   len(dict): 2

# len() counts items, characters or mapping keys
# according to the object's type.

# ============================================================
# [3] Define a common parent interface [02:45]
# ============================================================
# The parent names the behavior every child should expose:

class Shape:
    def describe(self):
        raise NotImplementedError("child must describe itself")


print(f"  parent defines interface: callable(Shape.describe)")
#   parent defines interface: callable(Shape.describe)

# ============================================================
# [4] Child classes override the same method
# ============================================================
# Each shape gives describe() its own behavior:

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def describe(self):
        return f"Circle with radius {self.radius}"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def describe(self):
        return f"Rectangle {self.width} by {self.height}"


circle = Circle(3)
rectangle = Rectangle(4, 5)
print(f"  circle override: {circle.describe()}")
print(f"  rectangle override: {rectangle.describe()}")
#   circle override: Circle with radius 3
#   rectangle override: Rectangle 4 by 5

# ============================================================
# [5] Same call works on both [02:45]
# ============================================================
# The caller uses describe() without branching on class:

shapes = (circle, rectangle)
descriptions = [shape.describe() for shape in shapes]
print(f"  shared interface results: {descriptions}")
print(f"  each is a Shape: {all(isinstance(shape, Shape) for shape in shapes)}")
#   shared interface results: ['Circle with radius 3', 'Rectangle 4 by 5']
#   each is a Shape: True

# Same method name; each object's class supplies its
# specific implementation.

# ============================================================
# [6] One function processes mixed objects
# ============================================================
# A function can rely on the interface, not concrete type:

def print_descriptions(objects):
    return [item.describe() for item in objects]


mixed_descriptions = print_descriptions([rectangle, circle])
print(f"  mixed objects: {mixed_descriptions}")
#   mixed objects: ['Rectangle 4 by 5', 'Circle with radius 3']

# ============================================================
# [7] A third type joins without changing the caller
# ============================================================
# Add a Triangle with its own describe() method:

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def describe(self):
        return f"Triangle base {self.base}, height {self.height}"


triangle = Triangle(6, 4)
all_shapes = [circle, rectangle, triangle]
print(f"  three child behaviors: {print_descriptions(all_shapes)}")
#   three child behaviors: ['Circle with radius 3', 'Rectangle 4 by 5', 'Triangle base 6, height 4']

# The processing function did not need editing when a
# new Shape subtype appeared.

# ============================================================
# [8] Polymorphism with built-in len() and custom objects
# ============================================================
# A custom object can implement __len__ and join the same
# built-in protocol:

class Playlist:
    def __init__(self, tracks):
        self.tracks = tracks

    def __len__(self):
        return len(self.tracks)


playlist = Playlist(["Intro", "Song", "Outro"])
print(f"  len(custom Playlist): {len(playlist)}")
print(f"  same len function for list and custom object: {len(['x'])}, {len(playlist)}")
#   len(custom Playlist): 3
#   same len function for list and custom object: 1, 3

# ============================================================
# [9] Duck typing: behavior matters
# ============================================================
# A class need not inherit Shape if it offers describe():

class Report:
    def describe(self):
        return "Daily report"


report = Report()
print(f"  unrelated object accepted by interface function: {print_descriptions([report])}")
#   unrelated object accepted by interface function: ['Daily report']

# Python often cares that the needed method exists,
# rather than requiring a particular parent class.

# ============================================================
# [10] Contrast with type-specific branching
# ============================================================
# Polymorphism keeps callers simple; compare one shared
# call against explicit type checks:

def describe_all(objects):
    return [obj.describe() for obj in objects]


uniform = describe_all([circle, rectangle, triangle])
print(f"  one uniform call handles all: {len(uniform) == 3}")
print(f"  each behavior differs: {len(set(uniform)) == 3}")
#   one uniform call handles all: True
#   each behavior differs: True

# ============================================================
# [11] Same function name, per-object result
# ============================================================
# Collect each object's class name and its response:

responses = [(type(obj).__name__, obj.describe()) for obj in all_shapes]
print(f"  class-specific responses: {responses}")
#   class-specific responses: [('Circle', 'Circle with radius 3'), ('Rectangle', 'Rectangle 4 by 5'), ('Triangle', 'Triangle base 6, height 4')]

# The caller invokes describe() uniformly; dispatch selects
# the override based on the actual object.

# ============================================================
# [12] One session: operator, built-in and OOP
# ============================================================
# Three familiar forms of polymorphism together:

print(f"  plus on numbers: {10 + 20}")
print(f"  plus on strings: {'Py' + 'thon'}")
print(f"  len on dict: {len({'a': 1, 'b': 2})}")
print(f"  OOP dispatch: {print_descriptions(all_shapes)}")
print(f"  custom len: {len(playlist)}")
#   plus on numbers: 30
#   plus on strings: Python
#   len on dict: 2
#   OOP dispatch: ['Circle with radius 3', 'Rectangle 4 by 5', 'Triangle base 6, height 4']
#   custom len: 3

# ============================================================
# [13] The summary
# ============================================================
# Polymorphism, from the transcript:
#
#   1. WHAT [00:10] -- same function/operator name,
#      behavior varies with object or data type
#   2. + [00:35] -- numbers add; strings and lists
#      concatenate
#   3. len() [00:35] -- count list elements, string
#      characters or dictionary keys
#   4. OOP [02:45] -- Shape supplies describe(); Circle,
#      Rectangle and Triangle override it differently
#   5. UNIFORM CALL -- print_descriptions() handles mixed
#      child objects without knowing their concrete types
#   6. EXTENSIBLE -- adding Triangle did not require
#      changing the processing function
#   7. PROTOCOL -- Playlist implements __len__ and works
#      with built-in len(); Report works by having describe()
#
# One interface; many object-specific behaviors -- that's
# polymorphism in action.
