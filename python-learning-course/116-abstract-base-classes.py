# -----------------------------------------------------------------
# Lesson 116: Abstract Base Classes -- contracts for subclasses
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : abc.ABC, @abstractmethod, abstract contracts,
#            instantiation restrictions, child implementation,
#            and metaclass inspection
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: Abstract Base Classes (ABCs),
# a more advanced OOP concept.
#
#   WHAT [00:15] -- an abstract class is a blueprint/
#   contract for child classes; it cannot be instantiated
#   directly and requires subclasses to implement methods
#   ABC MODULE [05:03] -- import ABC and @abstractmethod
#   from the standard abc module
#   IMPLEMENTATION -- a child missing required methods
#   cannot be instantiated; Python raises TypeError
#
# Python's ABC is a convenient base class using ABCMeta;
# a direct metaclass=ABCMeta declaration is also possible.

from abc import ABC, ABCMeta, abstractmethod

# ============================================================
# [1] Import ABC tools from the standard library [05:03]
# ============================================================
# Confirm the module and decorators are available:

print(f"  ABC base imported: {isinstance(ABC, type)}")
print(f"  ABCMeta imported: {isinstance(ABCMeta, type)}")
print(f"  abstractmethod is callable: {callable(abstractmethod)}")
#   ABC base imported: True
#   ABCMeta imported: True
#   abstractmethod is callable: True

# ============================================================
# [2] Define an abstract contract [00:15]
# ============================================================
# An abstract method names behavior every concrete child
# must provide:

class Notifier(ABC):
    @abstractmethod
    def send(self, message):
        """Send a message using a concrete transport."""
        raise NotImplementedError


print(f"  Notifier uses ABCMeta: {isinstance(Notifier, ABCMeta)}")
print(f"  send is marked abstract: {Notifier.send.__isabstractmethod__}")
#   Notifier uses ABCMeta: True
#   send is marked abstract: Notifier.send.__isabstractmethod__

# ============================================================
# [3] Abstract classes cannot be instantiated
# ============================================================
# Attempt construction and catch the expected TypeError:

try:
    Notifier()
except TypeError:
    abstract_creation_blocked = True
else:
    abstract_creation_blocked = False

print(f"  abstract instantiation blocked: {abstract_creation_blocked}")
#   abstract instantiation blocked: True

# ============================================================
# [4] A child must implement the abstract method
# ============================================================
# This child inherits the contract without implementing
# send(), so it remains abstract:

class IncompleteNotifier(Notifier):
    pass


try:
    IncompleteNotifier()
except TypeError:
    incomplete_creation_blocked = True
else:
    incomplete_creation_blocked = False

print(f"  incomplete child remains abstract: {IncompleteNotifier.__abstractmethods__ == frozenset({'send'})}")
print(f"  incomplete child instantiation blocked: {incomplete_creation_blocked}")
#   incomplete child remains abstract: True
#   incomplete child instantiation blocked: True

# ============================================================
# [5] Implement the contract in a concrete child
# ============================================================
# The child supplies the required method and becomes
# instantiable:

class EmailNotifier(Notifier):
    def send(self, message):
        return "email: " + message


email = EmailNotifier()
print(f"  child instance created: {isinstance(email, EmailNotifier)}")
print(f"  required method works: {email.send('Hello')}")
print(f"  no remaining abstract methods: {not EmailNotifier.__abstractmethods__}")
#   child instance created: True
#   required method works: email: Hello
#   no remaining abstract methods: True

# ============================================================
# [6] Another child provides a different implementation
# ============================================================
# The same contract supports a different transport:

class ConsoleNotifier(Notifier):
    def send(self, message):
        return "console: " + message


console = ConsoleNotifier()
print(f"  console implementation: {console.send('Hello')}")
print(f"  both satisfy contract: {isinstance(email, Notifier) and isinstance(console, Notifier)}")
#   console implementation: console: Hello
#   both satisfy contract: True

# ============================================================
# [7] One interface handles both implementations
# ============================================================
# The caller can use send() without branching on the
# concrete notifier class:

def announce(notifiers, message):
    return [item.send(message) for item in notifiers]


responses = announce([email, console], "Update")
print(f"  uniform caller results: {responses}")
#   uniform caller results: ['email: Update', 'console: Update']

# ============================================================
# [8] Abstract methods can declare shared behavior
# ============================================================
# A second abstract contract requires both a name and
# a calculation:

class Measurement(ABC):
    @property
    @abstractmethod
    def label(self):
        """Return a measurement label."""
        raise NotImplementedError

    @abstractmethod
    def value(self):
        """Return a numeric measurement."""
        raise NotImplementedError


required_measurement_methods = frozenset(("label", "value"))
print(f"  two abstract requirements: {Measurement.__abstractmethods__ == required_measurement_methods}")
#   two abstract requirements: True

# ============================================================
# [9] Implement all requirements
# ============================================================
# A concrete measurement supplies the property and method:

class FixedMeasurement(Measurement):
    def __init__(self, amount):
        self.amount = amount

    @property
    def label(self):
        return "fixed"

    def value(self):
        return self.amount


measurement = FixedMeasurement(12)
print(f"  measurement label: {measurement.label}")
print(f"  measurement value: {measurement.value()}")
print(f"  requirements all implemented: {not FixedMeasurement.__abstractmethods__}")
#   measurement label: fixed
#   measurement value: 12
#   requirements all implemented: True

# ============================================================
# [10] ABCMeta can be specified explicitly [05:03]
# ============================================================
# ABC is a helper base whose metaclass is ABCMeta. The
# equivalent explicit style is shown here:

class ExplicitContract(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


print(f"  explicit class uses ABCMeta: {isinstance(ExplicitContract, ABCMeta)}")
print(f"  explicit class is abstract: {bool(ExplicitContract.__abstractmethods__)}")
#   explicit class uses ABCMeta: True
#   explicit class is abstract: bool(ExplicitContract.__abstractmethods__)

# ============================================================
# [11] ABC is the concise standard pattern
# ============================================================
# Both declaration styles share the same metaclass:

print(f"  ABC metaclass name: {type(Notifier).__name__}")
print(f"  explicit metaclass name: {type(ExplicitContract).__name__}")
print(f"  styles use same metaclass: {type(Notifier) is type(ExplicitContract)}")
#   ABC metaclass name: ABCMeta
#   explicit metaclass name: ABCMeta
#   styles use same metaclass: type(Notifier) is type(ExplicitContract)

# ============================================================
# [12] One session: contract and concrete children
# ============================================================
# The contract, failed construction and implementations:

print(f"  parent abstract: {bool(Notifier.__abstractmethods__)}")
print(f"  parent instantiation blocked: {abstract_creation_blocked}")
print(f"  missing method blocked: {incomplete_creation_blocked}")
print(f"  email child: {email.send('Done')}")
print(f"  console child: {console.send('Done')}")
print(f"  measurement child value: {measurement.value()}")
#   parent abstract: True
#   parent instantiation blocked: True
#   missing method blocked: True
#   email child: email: Done
#   console child: console: Done
#   measurement child value: 12

# ============================================================
# [13] The summary
# ============================================================
# Abstract Base Classes, from the transcript:
#
#   1. WHAT [00:15] -- abstract class is a strict blueprint
#      / contract; it cannot be instantiated directly
#   2. IMPORT [05:03] -- from abc import ABC, ABCMeta,
#      abstractmethod
#   3. DECORATOR -- @abstractmethod marks required
#      methods; a subclass must implement them
#   4. ENFORCEMENT -- Notifier() and an incomplete child
#      raise TypeError at construction time
#   5. CONCRETE CHILD -- EmailNotifier and ConsoleNotifier
#      implement send() differently but share the contract
#   6. UNIFORM USE -- announce() calls send() on mixed
#      children without checking their concrete types
#   7. MORE CONTRACTS -- abstract property label and
#      abstract value() are both required
#   8. METACLASS -- ABC uses ABCMeta; explicit
#      metaclass=ABCMeta is another valid declaration style
#
# An ABC defines what children must provide; concrete
# classes decide how to provide it.
