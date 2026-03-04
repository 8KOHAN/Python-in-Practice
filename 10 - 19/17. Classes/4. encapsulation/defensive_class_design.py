"""
Demonstrates defensive class design in Python:
- enforcing invariants
- fail-fast principles
- controlled access to internal state
- preventing inconsistent object states
"""

from __future__ import annotations


# ----------------------------------------
# 1) FAIL-FAST PRINCIPLE
# ----------------------------------------

def fail_fast_demo() -> None:
    print("=== fail_fast_demo ===")

    # Fail-fast means detecting invalid state as early as possible.
    # This prevents propagation of invalid objects through the system.

    class Person:
        def __init__(self, name: str, age: int) -> None:
            if not name:
                raise ValueError("Name cannot be empty")
            if age < 0:
                raise ValueError("Age cannot be negative")

            self.name: str = name
            self.age: int = age

    # Instantiation with invalid data immediately raises an error.
    try:
        invalid_person: Person = Person("", -1)
    except ValueError as e:
        print("Caught error:", e)

    print()


# ----------------------------------------
# 2) ENFORCING INVARIANTS
# ----------------------------------------

def invariants_demo() -> None:
    print("=== invariants_demo ===")

    # Invariants are conditions that must always hold true
    # for the object to remain valid.

    class BankAccount:
        def __init__(self, balance: float) -> None:
            self._balance: float = 0.0
            self.balance = balance  # Routed through setter

        @property
        def balance(self) -> float:
            return self._balance

        @balance.setter
        def balance(self, value: float) -> None:
            if value < 0:
                raise ValueError("Balance cannot be negative")
            self._balance = value

    account: BankAccount = BankAccount(100.0)
    print(account.balance)

    # account.balance = -50.0  # Would violate invariant
    # The setter prevents it (fail-fast)

    print()


# ----------------------------------------
# 3) IMMUTABLE OBJECTS
# ----------------------------------------

def immutable_object_demo() -> None:
    print("=== immutable_object_demo ===")

    # Making an object immutable prevents accidental mutation
    # and protects invariants.

    class Point:
        __slots__ = ("_x", "_y")

        def __init__(self, x: float, y: float) -> None:
            self._x: float = x
            self._y: float = y

        @property
        def x(self) -> float:
            return self._x

        @property
        def y(self) -> float:
            return self._y

    p: Point = Point(1.0, 2.0)
    print(p.x, p.y)

    # p.x = 5.0  # AttributeError, object is effectively immutable

    print()


# ----------------------------------------
# 4) DEFENSIVE SETTERS
# ----------------------------------------

def defensive_setters_demo() -> None:
    print("=== defensive_setters_demo ===")

    # Defensive setters enforce constraints on object state.
    # Any attempt to break invariants immediately raises an error.

    class Rectangle:
        def __init__(self, width: float, height: float) -> None:
            self._width: float = 0.0
            self._height: float = 0.0
            self.width = width
            self.height = height

        @property
        def width(self) -> float:
            return self._width

        @width.setter
        def width(self, value: float) -> None:
            if value <= 0:
                raise ValueError("Width must be positive")
            self._width = value

        @property
        def height(self) -> float:
            return self._height

        @height.setter
        def height(self, value: float) -> None:
            if value <= 0:
                raise ValueError("Height must be positive")
            self._height = value

        @property
        def area(self) -> float:
            return self._width * self._height

    rect: Rectangle = Rectangle(3.0, 4.0)
    print(rect.area)

    # rect.width = -2.0  # Raises ValueError immediately

    print()


# ----------------------------------------
# 5) DESIGN NOTES
# ----------------------------------------

# Defensive class design principles:
#
# - Enforce invariants in constructors and setters
# - Fail fast on invalid input
# - Consider making objects immutable where possible
# - Protect internal state from direct modification
# - Keep the public API minimal and consistent
# - Use properties to control access and validation
#
# The goal is to maintain object consistency,
# reduce bugs, and make code easier to reason about.


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    fail_fast_demo()
    invariants_demo()
    immutable_object_demo()
    defensive_setters_demo()
