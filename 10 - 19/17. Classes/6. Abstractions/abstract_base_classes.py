"""
Deeper exploration of Abstract Base Classes.

This file demonstrates advanced ABC features:
abstract properties, abstract class methods,
and how Python tracks abstract methods internally.
"""

from abc import ABC, abstractmethod


# ----------------------------------------
# 1) ABSTRACT METHODS RECAP
# ----------------------------------------

# An abstract method is a method declared in an abstract class
# that must be implemented by subclasses.
#
# Python enforces this rule during class instantiation.
#
# If at least one abstract method remains unimplemented,
# Python will raise TypeError when attempting to create an instance.


# ----------------------------------------
# 2) ABSTRACT PROPERTY
# ----------------------------------------

class Shape(ABC):

    # Properties can also be abstract.
    # This means subclasses must implement the property.

    @property
    @abstractmethod
    def area(self) -> float:
        pass


class Square(Shape):

    def __init__(self, side: float) -> None:
        self.side = side

    @property
    def area(self) -> float:
        return self.side * self.side


def abstract_property_demo() -> None:
    print("=== abstract_property_demo ===")

    square = Square(4.0)

    print("Square area:", square.area)
    print()


# ----------------------------------------
# 3) ABSTRACT CLASS METHOD
# ----------------------------------------

class Animal(ABC):

    # Abstract class methods define behavior that subclasses
    # must implement at the class level rather than instance level.

    @classmethod
    @abstractmethod
    def species_name(cls) -> str:
        pass


class Dog(Animal):

    @classmethod
    def species_name(cls) -> str:
        return "Canis lupus familiaris"


def abstract_classmethod_demo() -> None:
    print("=== abstract_classmethod_demo ===")

    print("Dog species:", Dog.species_name())
    print()


# ----------------------------------------
# 4) MULTIPLE ABSTRACT METHODS
# ----------------------------------------
#
# Abstract classes may define multiple required methods.
# Subclasses must implement all of them.


# ----------------------------------------
# 5) INTERNAL ABC MECHANISM
# ----------------------------------------

# Python tracks abstract methods using the class attribute:
#
# __abstractmethods__
#
# This attribute contains a set of method names that are still abstract.
#
# When a subclass implements all abstract methods,
# the set becomes empty and the class becomes instantiable.


def abstractmethods_attribute_demo() -> None:
    print("=== abstractmethods_attribute_demo ===")

    print("Shape abstract methods:", Shape.__abstractmethods__)
    print("Square abstract methods:", Square.__abstractmethods__)

    print()


# ----------------------------------------
# 6) IMPORTANT DESIGN NOTES
# ----------------------------------------
#
# Abstract Base Classes should describe behavior,
# not implementation details.
#
# A good abstract class:
#
# - defines a clear interface
# - does not enforce unnecessary structure
# - allows multiple independent implementations
#
# Overusing abstract classes can make a system rigid.
#
# They are most useful in:
#
# - frameworks
# - extensible architectures
# - plugin systems
# - public APIs


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    abstract_property_demo()
    abstract_classmethod_demo()
    abstractmethods_attribute_demo()
