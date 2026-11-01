# -----------------------------------------------------------------
# Lesson 108: class methods and static methods
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : compare instance methods (self), class methods
#            (@classmethod, cls), and static methods
#            (@staticmethod); class data and helpers
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: two important OOP method types --
# Class Methods and Static Methods -- and how they differ
# from ordinary instance methods.
#
#   CLASS METHOD [00:35-00:46] -- decorated with
#   @classmethod; first parameter cls is the class itself;
#   can read/change class attributes and can often be
#   called without creating an instance
#   STATIC METHOD [05:12-05:23] -- decorated with
#   @staticmethod; no required self or cls; a helper that
#   needs neither instance nor class state

# ============================================================
# [1] The three method kinds
# ============================================================
# One class shows all three conventions together:

class Member:
    category = "learner"

    def __init__(self, name):
        self.name = name

    def instance_label(self):
        return self.name + " / " + self.category

    @classmethod
    def class_label(cls):
        return "category=" + cls.category

    @staticmethod
    def clean_name(name):
        return name.strip().title()


member = Member("amina")
print(f"  instance method: {member.instance_label()}")
print(f"  class method: {Member.class_label()}")
print(f"  static method: {Member.clean_name('  aMina  ')}")
#   instance method: amina / learner
#   class method: category=learner
#   static method: Amina

# ============================================================
# [2] Instance method receives self
# ============================================================
# It operates on one object's attributes:

print(f"  instance method is bound to member: {member.instance_label.__self__ is member}")
print(f"  instance name: {member.name}")
#   instance method is bound to member: True
#   instance name: amina

# ============================================================
# [3] Class method receives cls [00:46]
# ============================================================
# Called through the class, the bound method receives
# that class as its first argument:

bound_class_method = Member.class_label
print(f"  class method is bound to Member: {bound_class_method.__self__ is Member}")
print(f"  cls can read class attribute: {Member.class_label()}")
#   class method is bound to Member: True
#   cls can read class attribute: category=learner

# ============================================================
# [4] Call class method without an instance
# ============================================================
# No Member object is needed to call class_label():

print(f"  class call works without instance: {Member.class_label() == 'category=learner'}")
print(f"  class itself supplies cls: {Member.class_label.__self__ is Member}")
#   class call works without instance: True
#   class itself supplies cls: True

# ============================================================
# [5] Change class data through cls
# ============================================================
# A class method can update the shared class attribute:

class Catalog:
    item_count = 0

    @classmethod
    def add_item(cls):
        cls.item_count += 1
        return cls.item_count


print(f"  catalog starts: {Catalog.item_count}")
first_count = Catalog.add_item()
second_count = Catalog.add_item()
print(f"  first class update: {first_count}")
print(f"  second class update: {second_count}")
print(f"  shared class value: {Catalog.item_count}")
#   catalog starts: 0
#   first class update: 1
#   second class update: 2
#   shared class value: 2

# ============================================================
# [6] Instance can call a class method too
# ============================================================
# The decorator binds cls to the class even when the call
# is made through an instance:

catalog_object = Catalog()
catalog_object.add_item()
print(f"  called through instance: {Catalog.item_count}")
print(f"  instance call changed class data: {catalog_object.item_count == Catalog.item_count}")
#   called through instance: 3
#   instance call changed class data: True

# ============================================================
# [7] Static method: no implicit self or cls [05:23]
# ============================================================
# The helper is namespaced in the class, but receives
# only the explicit argument:

print(f"  static helper result: {Member.clean_name('  jO  ')}")
print(f"  static method is not bound: {not hasattr(Member.clean_name, '__self__')}")
print(f"  static access returns function: {type(Member.clean_name).__name__ == 'function'}")
#   static helper result: Jo
#   static method has no bound instance: True
#   static method has no bound class: True

# Unlike class_label, clean_name is not automatically
# passed either self or cls.

# ============================================================
# [8] Static helper does not need class state
# ============================================================
# A general formatting/validation helper can work only
# with the arguments it receives:

class TextTools:
    @staticmethod
    def is_long_enough(text, minimum):
        return len(text) >= minimum


print(f"  helper accepts long text: {TextTools.is_long_enough('Python', 4)}")
print(f"  helper rejects short text: {not TextTools.is_long_enough('Py', 4)}")
#   helper accepts long text: True
#   helper rejects short text: True

# It needs no object or class data -- only text and the
# minimum length provided by the caller.

# ============================================================
# [9] Static method can be called through an instance
# ============================================================
# Calling it through an object does not insert self:

text_tools = TextTools()
print(f"  class access: {TextTools.is_long_enough('hello', 5)}")
print(f"  instance access: {text_tools.is_long_enough('hi', 3)}")
#   class access: True
#   instance access: False

# It behaves as the same independent helper either way.

# ============================================================
# [10] Compare signatures and responsibilities
# ============================================================
# Instance method needs self; class method needs cls;
# static method has only explicit parameters:

print(f"  instance first parameter: {Member.instance_label.__code__.co_varnames[0]}")
print(f"  class method parameter: {Member.class_label.__func__.__code__.co_varnames[0]}")
print(f"  static helper first parameter: {Member.clean_name.__code__.co_varnames[0]}")
#   instance first parameter: self
#   class method parameter: cls
#   static helper first parameter: name

# ============================================================
# [11] Choose the method by what it needs
# ============================================================
# A quick responsibility check:

print(f"  instance method sees object data: {member.instance_label().startswith(member.name)}")
print(f"  class method sees shared data: {Member.class_label().endswith(Member.category)}")
print(f"  static method transforms argument only: {Member.clean_name('  lee ') == 'Lee'}")
#   instance method sees object data: True
#   class method sees shared data: True
#   static method transforms argument only: True

# ============================================================
# [12] One session: all three method types
# ============================================================
# Final comparison:

print(f"  instance / self: {member.instance_label()}")
print(f"  class / cls: {Catalog.item_count} items")
print(f"  static / explicit input: {Member.clean_name('  mIRA  ')}")
print(f"  class method no instance needed: {Member.class_label() == 'category=learner'}")
print(f"  static needs no class data: {TextTools.is_long_enough('OOP', 3)}")
#   instance / self: amina / learner
#   class / cls: 3 items
#   static / explicit input: Mira
#   class method no instance needed: True
#   static needs no class data: True

# ============================================================
# [13] The summary
# ============================================================
# Class and Static Methods, from the transcript:
#
#   1. INSTANCE METHOD -- first parameter self; works with
#      one object's attributes
#   2. CLASS METHOD [00:35-00:46] -- @classmethod; first
#      parameter cls is the class; can access/update class
#      attributes
#   3. CALLING -- class methods can often be called as
#      ClassName.method() without constructing an instance
#   4. CLASS UPDATE -- Catalog.add_item() changes the
#      shared item_count from 0 to 1 to 2 (and 3)
#   5. STATIC METHOD [05:12-05:23] -- @staticmethod; no
#      implicit self or cls; receives only explicit inputs
#   6. USE -- static methods are class-namespaced helpers
#      that need neither instance nor class state
#   7. ACCESS -- static helpers and class methods can also
#      be called through an instance, but their binding
#      behavior remains distinct
#
# Choose by dependency: self for object data, cls for
# class data, static for an independent helper.
