"""
Demonstration of multiple inheritance in Python.

This file explains:
- how a class can inherit from multiple parents
- how attributes and methods are resolved
- method conflicts between parents
- cooperative use of super() in multiple inheritance
"""

# ----------------------------------------
# 1) BASIC MULTIPLE INHERITANCE
# ----------------------------------------

# Python allows a class to inherit from multiple base classes.
#
# This means the child class receives attributes and methods
# from all parent classes.
#
# Syntax:
#
# class Child(ParentA, ParentB):
#     ...
#
# The order of parents is important. Python will search them
# in the order defined by the inheritance list.


class Flyable:
    def fly(self) -> None:
        print("Flying through the air")


class Swimmable:
    def swim(self) -> None:
        print("Swimming in water")


class Duck(Flyable, Swimmable):
    pass


def basic_multiple_inheritance_demo() -> None:
    print("=== basic_multiple_inheritance_demo ===")

    duck = Duck()

    duck.fly()
    duck.swim()

    print()


# ----------------------------------------
# 2) METHOD NAME CONFLICT
# ----------------------------------------

# A conflict happens when multiple parent classes define
# a method with the same name.
#
# Python must decide which implementation to use.
#
# The rule is simple:
#
# Python searches parent classes from left to right.


class LoggerA:
    def log(self) -> None:
        print("Log from LoggerA")


class LoggerB:
    def log(self) -> None:
        print("Log from LoggerB")


class CombinedLogger(LoggerA, LoggerB):
    pass


def method_conflict_demo() -> None:
    print("=== method_conflict_demo ===")

    logger = CombinedLogger()

    # LoggerA appears first in the inheritance list
    # so its method will be used.
    logger.log()

    print()


# ----------------------------------------
# 3) DIAMOND INHERITANCE STRUCTURE
# ----------------------------------------

# The diamond inheritance structure appears when
# two classes inherit from the same base class
# and another class inherits from both of them.
#
#        Base
#       /    \
#   Left    Right
#       \    /
#        Child
#
# This structure can cause problems if parent
# constructors are called multiple times.


class Base:
    def greet(self) -> None:
        print("Hello from Base")


class Left(Base):
    pass


class Right(Base):
    pass


class Child(Left, Right):
    pass


def diamond_structure_demo() -> None:
    print("=== diamond_structure_demo ===")

    child = Child()

    # Even though Base appears twice in the hierarchy,
    # Python ensures it is only used once during lookup.
    child.greet()

    print()


# ----------------------------------------
# 4) COOPERATIVE MULTIPLE INHERITANCE
# ----------------------------------------

# In complex hierarchies, classes must cooperate.
#
# This means:
# every class should use super() instead of calling
# a specific parent class directly.
#
# This allows Python to follow the correct method
# resolution order across the entire hierarchy.


class A:
    def process(self) -> None:
        print("A.process start")
        super().process()
        print("A.process end")


class B:
    def process(self) -> None:
        print("B.process start")
        super().process()
        print("B.process end")


class C:
    def process(self) -> None:
        print("C.process (final method)")


class Combined(A, B, C):
    pass


def cooperative_super_demo() -> None:
    print("=== cooperative_super_demo ===")

    obj = Combined()
    obj.process()

    print()


# ----------------------------------------
# 5) INSPECTING THE INHERITANCE TREE
# ----------------------------------------

# Python exposes the inheritance chain through
# the __mro__ attribute.
#
# MRO means:
# Method Resolution Order
#
# It defines the exact order Python uses to search
# for attributes and methods.


def mro_inspection_demo() -> None:
    print("=== mro_inspection_demo ===")

    for cls in Combined.__mro__:
        print(cls)

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_multiple_inheritance_demo()
    method_conflict_demo()
    diamond_structure_demo()
    cooperative_super_demo()
    mro_inspection_demo()
