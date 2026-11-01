# -----------------------------------------------------------------
# Lesson 110: inheritance -- parent, child, overriding, super()
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : base and derived classes, inherited attributes
#            and methods, method overriding, and super() to
#            reuse parent initialization and extend child data
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: one of the core OOP pillars --
# Inheritance.
#
#   WHAT [00:15] -- a Derived/Child class inherits
#   attributes and methods from an existing Base/Parent;
#   reuse behavior instead of repeating code
#   SYNTAX [01:21] -- class Food(Member):
#   OVERRIDING [03:14] -- a child can replace a parent's
#   method behavior to fit its own needs
#   super() [05:09-05:39] -- call parent behavior (often
#   __init__) from a child, then add child-specific data

# ============================================================
# [1] A base class provides shared behavior [00:15]
# ============================================================
# Define attributes and a method once in a parent:

class Member:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return "Member: " + self.name


member = Member("Amina")
print(f"  parent method: {member.describe()}")
#   parent method: Member: Amina

# ============================================================
# [2] Child class inherits from parent [01:21]
# ============================================================
# Pass the parent class in parentheses:

class Food(Member):
    pass


food = Food("Apple")
print(f"  Food is a Member: {isinstance(food, Member)}")
print(f"  inherited name: {food.name}")
print(f"  inherited method: {food.describe()}")
#   Food is a Member: True
#   inherited name: Apple
#   inherited method: Member: Apple

# Food inherits __init__ and describe() without
# redefining either one.

# ============================================================
# [3] Inheritance avoids duplicated code
# ============================================================
# Both parent and child share the same method:

print(f"  parent and child use same method: {Member.describe is Food.describe}")
print(f"  child class name: {Food.__name__}")
print(f"  parent class name: {Member.__name__}")
#   parent and child use same method: True
#   child class name: Food
#   parent class name: Member

# ============================================================
# [4] Add child-specific attributes [05:39]
# ============================================================
# A child can define its own initialization and extend
# the parent's setup with super():

class Apple(Food):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color


apple = Apple("Apple", "red")
print(f"  inherited name: {apple.name}")
print(f"  child color: {apple.color}")
print(f"  still a Food: {isinstance(apple, Food)}")
#   inherited name: Apple
#   child color: red
#   still a Food: True

# super().__init__(name) reuses the parent's name setup;
# the child adds only its own color attribute.

# ============================================================
# [5] super() calls parent methods [05:09]
# ============================================================
# The child can build on a parent method too:

class DescribedApple(Food):
    def describe(self):
        return super().describe() + " (fruit)"


described = DescribedApple("Apple")
print(f"  parent description extended: {described.describe()}")
#   parent description extended: Member: Apple (fruit)

# The parent part remains reusable; the child adds a
# suffix instead of copying the whole implementation.

# ============================================================
# [6] Override a method [03:14]
# ============================================================
# Redefine a method in a child to change its behavior:

class Vegetable(Food):
    def describe(self):
        return "Vegetable: " + self.name


carrot = Vegetable("Carrot")
print(f"  overridden method: {carrot.describe()}")
print(f"  parent method remains unchanged: {member.describe()}")
#   overridden method: Vegetable: Carrot
#   parent method remains unchanged: Member: Amina

# The child override is selected for Vegetable instances;
# Member's own method stays the same.

# ============================================================
# [7] Override and still reuse parent behavior
# ============================================================
# An override may call super() then add or change detail:

class NamedVegetable(Food):
    def describe(self):
        parent_text = super().describe()
        return parent_text.replace("Member", "Vegetable")


named_vegetable = NamedVegetable("Carrot")
print(f"  override uses parent method: {named_vegetable.describe()}")
#   override uses parent method: Vegetable: Carrot

# ============================================================
# [8] Check the inheritance chain [01:21]
# ============================================================
# Apple derives from Food, which derives from Member:

print(f"  Apple is Food: {isinstance(apple, Food)}")
print(f"  Apple is Member: {isinstance(apple, Member)}")
print(f"  Food subclasses Member: {issubclass(Food, Member)}")
print(f"  Apple subclasses Member: {issubclass(Apple, Member)}")
#   Apple is Food: True
#   Apple is Member: True
#   Food subclasses Member: True
#   Apple subclasses Member: True

# ============================================================
# [9] Child inherits then extends [05:39]
# ============================================================
# Inherited description plus child attribute in one
# formatted result:

class ColoredApple(Member):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def describe(self):
        return super().describe() + ", color " + self.color


green_apple = ColoredApple("Apple", "green")
print(f"  extended child description: {green_apple.describe()}")
print(f"  parent attribute preserved: {green_apple.name}")
#   extended child description: Member: Apple, color green
#   parent attribute preserved: Apple

# ============================================================
# [10] super() follows the class hierarchy
# ============================================================
# super() delegates to the next implementation in the
# method resolution order:

print(f"  ColoredApple MRO: {[cls.__name__ for cls in ColoredApple.__mro__[:3]]}")
print(f"  first MRO class: {ColoredApple.__mro__[0].__name__}")
print(f"  parent follows child: {ColoredApple.__mro__[1] is Member}")
#   ColoredApple MRO: ['ColoredApple', 'Member', 'object']
#   first MRO class: ColoredApple
#   parent follows child: True

# ============================================================
# [11] Several child types reuse one parent
# ============================================================
# A common parent provides shared identity; children
# specialize their descriptions:

foods = (Apple("Apple", "red"), Vegetable("Carrot"))
print(f"  child descriptions: {[item.describe() for item in foods]}")
print(f"  all are Members: {all(isinstance(item, Member) for item in foods)}")
#   child descriptions: ['Member: Apple', 'Vegetable: Carrot']
#   all are Members: True

# ============================================================
# [12] One session: inheritance, override, super()
# ============================================================
# Key behavior together:

print(f"  inherited child method: {food.describe()}")
print(f"  child-specific attribute: {apple.color}")
print(f"  overridden method: {carrot.describe()}")
print(f"  super-built description: {green_apple.describe()}")
print(f"  parent-child relation: {isinstance(green_apple, Member)}")
#   inherited child method: Member: Apple
#   child-specific attribute: red
#   overridden method: Vegetable: Carrot
#   super-built description: Member: Apple, color green
#   parent-child relation: True

# ============================================================
# [13] The summary
# ============================================================
# Inheritance, from the transcript:
#
#   1. WHAT [00:15] -- a child/derived class inherits
#      parent/base attributes and methods; less duplication
#   2. SYNTAX [01:21] -- class Food(Member):
#   3. INHERITED BEHAVIOR -- Food gets Member.__init__ and
#      describe() without writing them again
#   4. EXTENSION [05:39] -- Apple adds color while
#      super().__init__(name) keeps parent setup
#   5. OVERRIDING [03:14] -- Vegetable replaces describe()
#      for its own instances, without changing Member
#   6. super() [05:09] -- call a parent/next-class method
#      and build on its work rather than duplicate it
#   7. CHAIN -- Apple -> Food -> Member -> object; child
#      instances are instances of their ancestors too
#   8. REUSE -- multiple child types share Member's
#      attributes while tailoring their behavior
#
# Inheritance shares the common core; overriding and
# super() let a child specialize it without losing reuse.
