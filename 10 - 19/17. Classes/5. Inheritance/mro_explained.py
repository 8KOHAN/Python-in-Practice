"""
Explanation of Python's Method Resolution Order (MRO).

This file demonstrates:
- what MRO is
- how Python resolves attributes in inheritance hierarchies
- how the C3 linearization algorithm influences class lookup
- how super() relies on MRO
"""

# ----------------------------------------
# 1) WHAT IS MRO
# ----------------------------------------

# MRO stands for Method Resolution Order.
#
# It defines the exact order Python follows when searching
# for attributes and methods in a class hierarchy.
#
# When we access:
#
#   obj.method()
#
# Python must decide where that method is defined.
#
# The search follows a deterministic order stored in:
#
#   Class.__mro__
#
# This attribute is a tuple of classes representing
# the lookup path Python will follow.


class A:
    def greet(self) -> None:
        print("Hello from A")


class B(A):
    pass


class C(B):
    pass


def simple_mro_demo() -> None:
    print("=== simple_mro_demo ===")

    obj = C()

    # greet is defined in A
    # Python finds it by walking the MRO chain
    obj.greet()

    print("MRO:")
    for cls in C.__mro__:
        print(cls)

    print()


# ----------------------------------------
# 2) ATTRIBUTE LOOKUP ORDER
# ----------------------------------------

# When Python resolves an attribute access like:
#
#     obj.attribute
#
# it follows a well-defined lookup order.
#
# 1) data descriptors defined on the class
#    (objects implementing __get__ AND __set__)
#
# 2) instance dictionary
#    obj.__dict__
#
# 3) non-data descriptors and regular class attributes
#
# 4) parent classes according to the MRO


class Parent:
    value: int = 10


class Child(Parent):
    value: int = 20


def attribute_lookup_demo() -> None:
    print("=== attribute_lookup_demo ===")

    obj = Child()

    # The value defined in Child overrides Parent
    print("Resolved value:", obj.value)

    print("MRO:")
    for cls in Child.__mro__:
        print(cls)

    print()


# ----------------------------------------
# 3) MRO IN MULTIPLE INHERITANCE
# ----------------------------------------

# With multiple inheritance, Python must determine
# a consistent order across all parent classes.
#
# Python uses an algorithm called:
#
#   C3 linearization
#
# The algorithm ensures:
#
# - a consistent order
# - parents appear before their children
# - the declared inheritance order is respected


class X:
    def identify(self) -> None:
        print("X.identify")


class Y:
    def identify(self) -> None:
        print("Y.identify")


class Z(X, Y):
    pass


def multiple_inheritance_mro_demo() -> None:
    print("=== multiple_inheritance_mro_demo ===")

    obj = Z()

    # X appears before Y in the class definition
    # so X.identify is used
    obj.identify()

    print("MRO:")
    for cls in Z.__mro__:
        print(cls)

    print()


# ----------------------------------------
# 4) DIAMOND STRUCTURE AND MRO
# ----------------------------------------

# Diamond inheritance creates a situation where
# a base class appears multiple times in the hierarchy.
#
#        Base
#       /    \
#    Left   Right
#       \    /
#        Child
#
# Without a well-defined algorithm, Python might call
# the same method multiple times or follow inconsistent paths.
#
# C3 linearization ensures that Base appears only once
# in the final resolution order.


class Base:
    def greet(self) -> None:
        print("Hello from Base")


class Left(Base):
    pass


class Right(Base):
    pass


class Diamond(Left, Right):
    pass


def diamond_mro_demo() -> None:
    print("=== diamond_mro_demo ===")

    obj = Diamond()
    obj.greet()

    print("MRO:")
    for cls in Diamond.__mro__:
        print(cls)

    print()


# ----------------------------------------
# 5) HOW super() USES MRO
# ----------------------------------------

# The super() function does not simply call the parent class.
#
# Instead, it calls the next class in the MRO sequence.
#
# This is why cooperative multiple inheritance works.
#
# Each class delegates work to the next class in the chain.


class BaseProcessor:
    def process(self) -> None:
        print("BaseProcessor.process")


class LoggingProcessor(BaseProcessor):
    def process(self) -> None:
        print("LoggingProcessor.process start")
        super().process()
        print("LoggingProcessor.process end")


class ValidationProcessor(BaseProcessor):
    def process(self) -> None:
        print("ValidationProcessor.process start")
        super().process()
        print("ValidationProcessor.process end")


class ApplicationProcessor(LoggingProcessor, ValidationProcessor):
    pass


def super_mro_demo() -> None:
    print("=== super_mro_demo ===")

    processor = ApplicationProcessor()
    processor.process()

    print("MRO:")
    for cls in ApplicationProcessor.__mro__:
        print(cls)

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    simple_mro_demo()
    attribute_lookup_demo()
    multiple_inheritance_mro_demo()
    diamond_mro_demo()
    super_mro_demo()
