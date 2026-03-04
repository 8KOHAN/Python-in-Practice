"""
Demonstrates @property, setters, validation logic,
and controlled attribute access in Python classes.
"""

from __future__ import annotations


# ----------------------------------------
# 1) WHY PROPERTIES EXIST
# ----------------------------------------

def property_basics_demo() -> None:
    print("=== property_basics_demo ===")

    # Direct public attributes are simple and transparent.
    # However, sometimes we need:
    # - validation
    # - lazy computation
    # - derived values
    # - controlled mutation
    #
    # A property allows attribute-like access
    # while executing method logic internally.

    class Rectangle:
        def __init__(self, width: float, height: float) -> None:
            self.width: float = width
            self.height: float = height

        @property
        def area(self) -> float:
            return self.width * self.height

    rect: Rectangle = Rectangle(3.0, 4.0)

    # Access looks like attribute access,
    # but internally it is a method call.
    print(rect.area)

    print()


# ----------------------------------------
# 2) SETTERS AND VALIDATION
# ----------------------------------------

def setter_validation_demo() -> None:
    print("=== setter_validation_demo ===")

    # A property becomes powerful when combined with a setter.
    # The setter allows validation before state mutation.
    #
    # This protects class invariants.
    # Invariants are conditions that must always remain true
    # for the object to be valid.

    class BankAccount:
        def __init__(self, initial_balance: float) -> None:
            self._balance: float = 0.0
            self.balance = initial_balance  # Routed through setter

        @property
        def balance(self) -> float:
            return self._balance

        @balance.setter
        def balance(self, value: float) -> None:
            # Validation logic is centralized here.
            if value < 0:
                raise ValueError("Balance cannot be negative")

            self._balance = value

    account: BankAccount = BankAccount(100.0)
    print(account.balance)

    # account.balance = -50.0  # Would raise ValueError

    account.balance = 250.0
    print(account.balance)

    print()


# ----------------------------------------
# 3) READ-ONLY PROPERTIES
# ----------------------------------------

def readonly_property_demo() -> None:
    print("=== readonly_property_demo ===")

    # If no setter is defined,
    # the property becomes read-only.

    class Circle:
        def __init__(self, radius: float) -> None:
            self._radius: float = radius

        @property
        def radius(self) -> float:
            return self._radius

        @property
        def diameter(self) -> float:
            return self._radius * 2

    circle: Circle = Circle(5.0)

    print(circle.radius)
    print(circle.diameter)

    # circle.radius = 10.0  # AttributeError

    print()


# ----------------------------------------
# 4) VALIDATION VS DIRECT ATTRIBUTE ACCESS
# ----------------------------------------

def validation_design_demo() -> None:
    print("=== validation_design_demo ===")

    # Without properties, validation must be repeated manually.
    # That leads to duplication and fragile code.
    #
    # With properties:
    # - All validation logic lives in one place.
    # - External code cannot bypass it accidentally
    #   (unless it deliberately accesses protected fields).

    class Temperature:
        def __init__(self, celsius: float) -> None:
            self._celsius: float = 0.0
            self.celsius = celsius

        @property
        def celsius(self) -> float:
            return self._celsius

        @celsius.setter
        def celsius(self, value: float) -> None:
            if value < -273.15:
                raise ValueError("Temperature below absolute zero is invalid")

            self._celsius = value

        @property
        def fahrenheit(self) -> float:
            return self._celsius * 9 / 5 + 32

    t: Temperature = Temperature(25.0)
    print(t.celsius)
    print(t.fahrenheit)

    print()


# ----------------------------------------
# 5) DESIGN NOTES
# ----------------------------------------
#
# Properties should be used when:
# - Attribute access needs validation
# - Value is derived from internal state
# - Internal representation may change in the future
#
# Do NOT use properties:
# - For heavy computations (violates expectation of cheap access)
# - When method semantics are clearer than attribute semantics
#
# Properties preserve clean public API
# while allowing internal refactoring.


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    property_basics_demo()
    setter_validation_demo()
    readonly_property_demo()
    validation_design_demo()
