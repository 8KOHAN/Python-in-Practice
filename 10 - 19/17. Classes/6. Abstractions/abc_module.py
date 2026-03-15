"""
Demonstration of the abc module from the Python standard library.

This file explains how abstract base classes are defined,
how abstract methods work, and how Python prevents
instantiation of incomplete subclasses.
"""

from abc import ABC, abstractmethod


# ----------------------------------------
# 1) WHAT IS THE abc MODULE
# ----------------------------------------

# The abc module provides infrastructure for defining
# Abstract Base Classes (ABCs).
#
# An Abstract Base Class is a class that cannot be instantiated
# directly and exists only to define a required interface.
#
# Python differs from many languages:
#
# - abstract classes may contain implemented methods
# - abstract classes may contain abstract methods
#
# A class becomes abstract when:
#
# - it inherits from ABC
# - at least one method is marked with @abstractmethod


# ----------------------------------------
# 2) DEFINING A SIMPLE ABSTRACT BASE CLASS
# ----------------------------------------

class Shape(ABC):

    # This method must be implemented by subclasses.
    # The decorator marks it as required.

    @abstractmethod
    def area(self) -> float:
        pass


# Shape is now an abstract class.
#
# Python prevents direct instantiation because
# the abstract method has no implementation.
#
# Attempting this would raise:
#
# TypeError:
# Can't instantiate abstract class Shape
# with abstract method area


# ----------------------------------------
# 3) IMPLEMENTING A CONCRETE SUBCLASS
# ----------------------------------------

class Rectangle(Shape):

    def __init__(self, width: float, height: float) -> None:
        self.width: float = width
        self.height: float = height

    # Concrete implementation of the required method

    def area(self) -> float:
        return self.width * self.height


def concrete_subclass_demo() -> None:
    print("=== concrete_subclass_demo ===")

    rectangle = Rectangle(10.0, 5.0)

    # Now the class is concrete because the abstract
    # method has been implemented.

    print("Rectangle area:", rectangle.area())
    print()


# ----------------------------------------
# 4) INCOMPLETE SUBCLASS
# ----------------------------------------

class BrokenShape(Shape):
    pass


# BrokenShape inherits from Shape but does not implement
# the required abstract method.
#
# Python still treats this class as abstract.
#
# Instantiating it would raise:
#
# TypeError:
# Can't instantiate abstract class BrokenShape
# with abstract method area


# ----------------------------------------
# 5) ABSTRACT CLASSES CAN HAVE NORMAL METHODS
# ----------------------------------------

class PrintableShape(ABC):

    @abstractmethod
    def area(self) -> float:
        pass

    # Abstract classes can contain fully implemented methods.
    # Subclasses inherit them automatically.

    def describe(self) -> str:
        return "Shape object with measurable area"


class Circle(PrintableShape):

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius * self.radius


def abstract_class_with_methods_demo() -> None:
    print("=== abstract_class_with_methods_demo ===")

    circle = Circle(3.0)

    print(circle.describe())
    print("Circle area:", circle.area())
    print()


# ----------------------------------------
# 6) WHY ABC EXISTS
# ----------------------------------------

# Without abstract base classes Python relies on duck typing.
#
# Duck typing detects errors only at runtime
# when a required method is missing.
#
# Abstract Base Classes allow detecting design mistakes
# earlier because subclasses must implement required methods.
#
# This is especially useful for:
#
# - frameworks
# - plugin systems
# - large architectures
# - extensible APIs


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    concrete_subclass_demo()
    abstract_class_with_methods_demo()
