# -----------------------------------------------------------------
# Lesson 103: OOP introduction -- classes and objects
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : Object-Oriented Programming as a paradigm,
#            objects with data and behavior, attributes,
#            methods, classes as blueprints, instantiation
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: begin a new Python section --
# Object-Oriented Programming (OOP). The concepts are
# broadly shared across programming languages.
#
#   WHAT [01:14-01:21] -- OOP is NOT a programming
#   language; it is a paradigm/design approach to organize
#   code and make large applications reusable and
#   maintainable
#   OBJECT [01:51] -- a program unit joining data and
#   behavior
#   ATTRIBUTES [01:51] -- data/variables belonging to an
#   object (name, age, color, model)
#   METHODS [01:51] -- functions describing what an object
#   can do (walk, start, stop)
#   CLASS [05:39-05:43] -- a blueprint used to create many
#   objects with the same kinds of attributes and methods
#   PRACTICE [06:29] -- the next lessons will make these
#   ideas concrete through code

# ============================================================
# [1] OOP is a paradigm, not a language [01:21]
# ============================================================
# A programming paradigm is a way to design and organize
# code. Python supports OOP; OOP itself is not Python:

print("  OOP is a programming paradigm")
print("  OOP is not a programming language")
print("  goal: organize reusable, maintainable applications")
#   OOP is a programming paradigm
#   OOP is not a programming language
#   goal: organize reusable, maintainable applications

# ============================================================
# [2] An object joins data and behavior [01:51]
# ============================================================
# A simple real-world model: a car has data (color,
# model) and actions (start, stop):

class Car:
    """A blueprint for a simple car object."""

    def __init__(self, model, color):
        self.model = model
        self.color = color
        self.running = False

    def start(self):
        """Start the car."""
        self.running = True
        return "started"

    def stop(self):
        """Stop the car."""
        self.running = False
        return "stopped"


car = Car("Civic", "blue")
print(f"  object model: {car.model}")
print(f"  object color: {car.color}")
print(f"  starts running: {car.running}")
#   object model: Civic
#   object color: blue
#   starts running: False

# The object is the unit that brings its attributes and
# methods together.

# ============================================================
# [3] Attributes: an object's data [01:51]
# ============================================================
# Attributes are values stored on the individual object:

print(f"  model attribute: {car.model}")
print(f"  color attribute: {car.color}")
print(f"  running attribute: {car.running}")
print(f"  object has its own attributes: {car.__dict__ == {'model': 'Civic', 'color': 'blue', 'running': False}}")
#   model attribute: Civic
#   color attribute: blue
#   running attribute: False
#   object has its own attributes: True

# Two objects from the same blueprint can hold different
# attribute values.

# ============================================================
# [4] Methods: an object's behavior [01:51]
# ============================================================
# Methods are functions attached to the class; called
# through an object they act on that object's state:

start_result = car.start()
print(f"  start method result: {start_result}")
print(f"  running after start: {car.running}")
stop_result = car.stop()
print(f"  stop method result: {stop_result}")
print(f"  running after stop: {car.running}")
#   start method result: started
#   running after start: True
#   stop method result: stopped
#   running after stop: False

# start and stop are behaviors; running is data that
# those behaviors update.

# ============================================================
# [5] Class: the blueprint [05:39-05:43]
# ============================================================
# A class is designed once; instantiate it to create
# objects from that blueprint:

print(f"  car is an instance of Car: {isinstance(car, Car)}")
print(f"  blueprint class name: {Car.__name__}")
print(f"  class has start method: {callable(Car.start)}")
#   car is an instance of Car: True
#   blueprint class name: Car
#   class has start method: True

# Class is the plan; instance/object is the built item.

# ============================================================
# [6] Instantiate more than one object [05:43]
# ============================================================
# One blueprint can create many similar objects:

car_two = Car("Corolla", "red")
car_three = Car("Civic", "green")

print(f"  first car: {car.model}, {car.color}")
print(f"  second car: {car_two.model}, {car_two.color}")
print(f"  third car: {car_three.model}, {car_three.color}")
print(f"  all share one class: {type(car) is type(car_two) is type(car_three)}")
#   first car: Civic, blue
#   second car: Corolla, red
#   third car: Civic, green
#   all share one class: True

# Same kinds of attributes and methods; distinct data
# belonging to each instance.

# ============================================================
# [7] Objects keep their own state
# ============================================================
# Starting one car does not start the other:

car_two.start()
print(f"  second car running: {car_two.running}")
print(f"  first car still stopped: {not car.running}")
print(f"  third car still stopped: {not car_three.running}")
#   second car running: True
#   first car still stopped: True
#   third car still stopped: True

# Each object stores its own attributes; a method call
# changes the object it was called on.

# ============================================================
# [8] The building blueprint analogy [05:43]
# ============================================================
# Like one building plan used for several houses:

blueprint = Car
houses_built = [blueprint("Model A", "white"),
                blueprint("Model B", "black")]

print(f"  blueprint reused: {len(houses_built)} objects")
print(f"  same class: {all(isinstance(item, Car) for item in houses_built)}")
print(f"  different colors: {houses_built[0].color != houses_built[1].color}")
#   blueprint reused: 2 objects
#   same class: True
#   different colors: True

# The transcript's blueprint analogy: design once,
# instantiate many similar objects.

# ============================================================
# [9] Identify attributes and methods
# ============================================================
# Inspect the class's interface without printing any
# machine-dependent representation:

print(f"  object has model attribute: hasattr(car, 'model') -> {hasattr(car, 'model')}")
print(f"  object has color attribute: hasattr(car, 'color') -> {hasattr(car, 'color')}")
print(f"  start is callable on object: {callable(car.start)}")
print(f"  stop is callable on object: {callable(car.stop)}")
#   object has model attribute: hasattr(car, 'model') -> True
#   object has color attribute: hasattr(car, 'color') -> True
#   start is callable on object: True
#   stop is callable on object: True

# Values describe attributes; callable actions are
# methods.

# ============================================================
# [10] Reuse behavior across instances
# ============================================================
# The same method implementation acts on different
# objects and their distinct states:

car.start()
car_three.start()

print(f"  first started: {car.running}")
print(f"  second started: {car_two.running}")
print(f"  third started: {car_three.running}")
print(f"  method reused for each object: {Car.start is type(car_two).start}")
#   first started: True
#   second started: True
#   third started: True
#   method reused for each object: True

# One method definition, many independent objects --
# reuse without copying the behavior.

# ============================================================
# [11] Why OOP helps larger applications [01:21]
# ============================================================
# Group related data and operations under one model:

car_state = (car.model, car.color, car.running)
print(f"  one object groups its state: {car_state}")
print(f"  objects created from blueprint: {len((car, car_two, car_three))}")
print(f"  reusable methods: {all(callable(getattr(car, name)) for name in ('start', 'stop'))}")
#   one object groups its state: ('Civic', 'blue', True)
#   objects created from blueprint: 3
#   reusable methods: True

# Modeling entities this way helps structure applications
# and keeps related state/behavior together.

# ============================================================
# [12] One session: class, objects, attributes, methods
# ============================================================
# The core terms from the lesson, demonstrated together:

print(f"  class: {Car.__name__}")
print(f"  object count: {len((car, car_two, car_three))}")
print(f"  each is a Car: {all(isinstance(item, Car) for item in (car, car_two, car_three))}")
print(f"  attributes hold data: {car.model}, {car.color}")
print(f"  methods describe actions: {car.start.__name__}, {car.stop.__name__}")
print(f"  objects have independent state: {car.running and car_two.running and car_three.running}")
#   class: Car
#   object count: 3
#   each is a Car: True
#   attributes hold data: Civic, blue
#   methods describe actions: start, stop
#   objects have independent state: True

# ============================================================
# [13] The summary: beginning the OOP section [06:29]
# ============================================================
# OOP, from the transcript:
#
#   1. OOP [00:04] -- a widely shared programming approach;
#      its ideas carry across languages
#   2. PARADIGM [01:14-01:21] -- not a language, but a
#      design method for organizing code, reuse and
#      maintenance in large applications
#   3. OBJECT [01:51] -- a program unit combining data
#      and behaviors
#   4. ATTRIBUTES [01:51] -- object data (model, color,
#      running); values can differ from instance to instance
#   5. METHODS [01:51] -- object actions (start, stop);
#      functions that can change that object's state
#   6. CLASS [05:39-05:43] -- a blueprint designed once
#      and used to instantiate many objects
#   7. INSTANTIATION -- three Car objects share one class
#      and behavior, while holding distinct attributes
#   8. REUSE -- one method definition works on each object
#      without copying its code
#   9. WHY -- related data and actions stay together,
#      helping code organization and maintainability
#  10. NEXT [06:29] -- practice and code in upcoming lessons
#      will make the theory clearer
#
# A class is the plan; an object is one built instance;
# attributes are its data, methods are its actions.
