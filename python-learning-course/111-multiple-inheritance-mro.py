# -----------------------------------------------------------------
# Lesson 111: multiple inheritance, overriding and MRO
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : method overriding, method resolution order,
#            __mro__ and mro(), multiple inheritance,
#            multilevel inheritance, cooperative super()
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:05]: continue OOP with multiple
# inheritance, method overriding and MRO.
#
#   OVERRIDING [00:16] -- a child defines a same-named
#   method and replaces the parent's behavior
#   MRO [02:18-02:23] -- __mro__ / mro() gives Python's
#   ordered lookup path for methods and attributes
#   INHERITANCE [04:16-04:31] -- inherit from several
#   parents or along a chain (Grandparent -> Parent -> Child)

# ============================================================
# [1] Override a parent method [00:16]
# ============================================================
# A child method with the same name takes precedence:

class Parent:
    def speak(self):
        return "Parent speaking"


class Child(Parent):
    def speak(self):
        return "Child speaking"


parent = Parent()
child = Child()
print(f"  parent method: {parent.speak()}")
print(f"  overridden child method: {child.speak()}")
#   parent method: Parent speaking
#   overridden child method: Child speaking

# ============================================================
# [2] The parent method remains available via super()
# ============================================================
# An override can deliberately call the parent's version:

class PoliteChild(Parent):
    def speak(self):
        return super().speak() + "; child adds hello"


polite = PoliteChild()
print(f"  parent behavior reused: {polite.speak()}")
#   parent behavior reused: Parent speaking; child adds hello

# ============================================================
# [3] Inspect MRO with __mro__ [02:23]
# ============================================================
# Python records the lookup order on each class:

class Base:
    pass


class Left(Base):
    pass


class Right(Base):
    pass


class Combined(Left, Right):
    pass


order_names = [cls.__name__ for cls in Combined.__mro__]
print(f"  Combined __mro__: {order_names}")
#   Combined __mro__: ['Combined', 'Left', 'Right', 'Base', 'object']

# ============================================================
# [4] Inspect MRO with mro() [02:23]
# ============================================================
# The class method mro() returns the same ordered classes:

method_order = [cls.__name__ for cls in Combined.mro()]
print(f"  Combined.mro(): {method_order}")
print(f"  both forms agree: {Combined.__mro__ == tuple(Combined.mro())}")
#   Combined.mro(): ['Combined', 'Left', 'Right', 'Base', 'object']
#   both forms agree: True

# ============================================================
# [5] Method lookup follows MRO [02:23]
# ============================================================
# If both parents define a method, the first parent in
# the declared order is found first:

class FirstParent:
    def identify(self):
        return "FirstParent"


class SecondParent:
    def identify(self):
        return "SecondParent"


class ChildBoth(FirstParent, SecondParent):
    pass


both = ChildBoth()
print(f"  method selected: {both.identify()}")
print(f"  first parent in MRO: {ChildBoth.mro()[1].__name__}")
#   method selected: FirstParent
#   first parent in MRO: FirstParent

# ============================================================
# [6] Multiple inheritance [04:16-04:31]
# ============================================================
# A child can inherit distinct capabilities from two
# base classes:

class CanSwim:
    def swim(self):
        return "swimming"


class CanFly:
    def fly(self):
        return "flying"


class Duck(CanSwim, CanFly):
    pass


duck = Duck()
print(f"  duck can swim: {duck.swim()}")
print(f"  duck can fly: {duck.fly()}")
print(f"  duck has both parents: {isinstance(duck, CanSwim) and isinstance(duck, CanFly)}")
#   duck can swim: swimming
#   duck can fly: flying
#   duck has both parents: True

# ============================================================
# [7] Multilevel inheritance [04:31]
# ============================================================
# A chain accumulates methods: Grandparent -> Parent -> Child:

class Grandparent:
    def family_root(self):
        return "root"


class MiddleParent(Grandparent):
    def family_middle(self):
        return "middle"


class FinalChild(MiddleParent):
    def family_leaf(self):
        return "leaf"


descendant = FinalChild()
print(f"  inherited grandparent: {descendant.family_root()}")
print(f"  inherited parent: {descendant.family_middle()}")
print(f"  own child method: {descendant.family_leaf()}")
#   inherited grandparent: root
#   inherited parent: middle
#   own child method: leaf

# ============================================================
# [8] Multilevel lookup order
# ============================================================
# MRO follows the chain from the child upward:

chain_names = [cls.__name__ for cls in FinalChild.__mro__]
print(f"  FinalChild MRO: {chain_names}")
print(f"  grandparent is in chain: {Grandparent in FinalChild.__mro__}")
#   FinalChild MRO: ['FinalChild', 'MiddleParent', 'Grandparent', 'object']
#   grandparent is in chain: True

# ============================================================
# [9] Cooperative super() in multiple inheritance
# ============================================================
# Each implementation calls super(); MRO lets each class
# contribute once in a predictable order:

class Root:
    def route(self):
        return ["Root"]


class BranchA(Root):
    def route(self):
        return ["BranchA"] + super().route()


class BranchB(Root):
    def route(self):
        return ["BranchB"] + super().route()


class Leaf(BranchA, BranchB):
    def route(self):
        return ["Leaf"] + super().route()


leaf = Leaf()
print(f"  cooperative route: {leaf.route()}")
print(f"  route follows MRO: {leaf.route() == [cls.__name__ for cls in Leaf.__mro__[:-1]]}")
#   cooperative route: ['Leaf', 'BranchA', 'BranchB', 'Root']
#   route follows MRO: True

# ============================================================
# [10] MRO avoids ambiguous lookup
# ============================================================
# The consistent order also determines which shared
# ancestor is visited once by cooperative super():

leaf_route = leaf.route()
print(f"  Root appears once: {leaf_route.count('Root') == 1}")
print(f"  object is final MRO entry: {Leaf.__mro__[-1] is object}")
#   Root appears once: True
#   object is final MRO entry: True

# ============================================================
# [11] Overriding and multiple parents together
# ============================================================
# A child can override its own method while still
# inheriting independent parent methods:

class SmartDuck(CanSwim, CanFly):
    def fly(self):
        return "flying with a flap"


smart_duck = SmartDuck()
print(f"  overridden fly: {smart_duck.fly()}")
print(f"  inherited swim: {smart_duck.swim()}")
#   overridden fly: flying with a flap
#   inherited swim: swimming

# ============================================================
# [12] One session: override, MRO and inheritance
# ============================================================
# The main concepts together:

print(f"  child override: {child.speak()}")
print(f"  multiple inheritance: {duck.swim()} + {duck.fly()}")
print(f"  multilevel child gets root: {descendant.family_root()}")
print(f"  Combined lookup order: {' -> '.join(order_names)}")
print(f"  cooperative super order: {' -> '.join(leaf_route)}")
#   child override: Child speaking
#   multiple inheritance: swimming + flying
#   multilevel child gets root: root
#   Combined lookup order: Combined -> Left -> Right -> Base -> object
#   cooperative super order: Leaf -> BranchA -> BranchB -> Root

# ============================================================
# [13] The summary
# ============================================================
# Multiple Inheritance, overriding and MRO:
#
#   1. OVERRIDING [00:16] -- child method with same name
#      takes precedence for child instances
#   2. super() -- an override can reuse parent behavior
#      and extend its result
#   3. MRO [02:18-02:23] -- __mro__ and mro() show the
#      ordered method/attribute lookup path
#   4. MULTIPLE INHERITANCE [04:16-04:31] -- Duck inherits
#      independent swim and fly methods from two parents
#   5. MULTILEVEL -- FinalChild -> MiddleParent ->
#      Grandparent; attributes/methods accumulate upward
#   6. LOOKUP -- ChildBoth(FirstParent, SecondParent)
#      finds FirstParent.identify first
#   7. COOPERATIVE super() -- Leaf -> BranchA -> BranchB
#      -> Root follows MRO; each class contributes once
#
# Overriding chooses child behavior; MRO explains lookup;
# super() cooperates with that order.
