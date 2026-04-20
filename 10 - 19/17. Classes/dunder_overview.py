"""
Overview of Python magic (dunder) methods.
Explains what they are, how they work, and why they exist.
Focus on behavior, not memorization.
"""

from __future__ import annotations


# ----------------------------------------
# 1) WHAT ARE DUNDER METHODS
# ----------------------------------------

# Dunder methods (double underscore methods) are special methods
# that define how objects behave in built-in operations.
#
# Example:
# __init__  -> object initialization
# __str__   -> string representation
# __len__   -> len(obj)
# __add__   -> obj + other
#
# Important:
# You NEVER call them directly in real code.
# Python calls them implicitly.


def basic_dunder_concept_demo() -> None:
    print("=== basic_dunder_concept_demo ===")

    class Example:
        def __init__(self, value: int) -> None:
            self.value = value

        def __str__(self) -> str:
            return f"Example(value={self.value})"

    obj = Example(10)

    # __str__ is called implicitly by print()
    print(obj)

    # Direct call is possible but not idiomatic
    print(obj.__str__())

    print()


# ----------------------------------------
# 2) DUNDER METHODS AS PROTOCOLS
# ----------------------------------------

# Dunder methods are not just "magic tricks".
# They are part of Python protocols.
#
# Protocol = a set of methods that define behavior.
#
# Example:
# If object has __len__ -> it behaves like a container
# If object has __iter__ -> it is iterable
#
# This is the foundation of Python's design.


def protocol_demo() -> None:
    print("=== protocol_demo ===")

    class Container:
        def __init__(self, items: list[int]) -> None:
            self.items = items

        def __len__(self) -> int:
            return len(self.items)

    c = Container([1, 2, 3])

    # len() calls __len__()
    print(len(c))

    print()


# ----------------------------------------
# 3) IMPLICIT BEHAVIOR MAPPING
# ----------------------------------------

# Python maps operations to dunder methods.
#
# Examples:
# obj + other      -> obj.__add__(other)
# obj == other     -> obj.__eq__(other)
# obj[key]         -> obj.__getitem__(key)
# callable(obj)    -> obj.__call__()
#
# This mapping is consistent and predictable.


def operator_mapping_demo() -> None:
    print("=== operator_mapping_demo ===")

    class Number:
        def __init__(self, value: int) -> None:
            self.value = value

        def __add__(self, other: Number) -> Number:
            return Number(self.value + other.value)

        def __repr__(self) -> str:
            return f"Number({self.value})"

    a = Number(5)
    b = Number(7)

    result = a + b  # calls __add__

    print(result)

    print()


# ----------------------------------------
# 4) BUILT-IN FUNCTION INTEGRATION
# ----------------------------------------

# Many built-in functions rely on dunder methods.
#
# len(obj)     -> __len__
# str(obj)     -> __str__
# repr(obj)    -> __repr__
# bool(obj)    -> __bool__
#
# Without these methods, objects lose integration with Python.


def builtin_integration_demo() -> None:
    print("=== builtin_integration_demo ===")

    class Flag:
        def __init__(self, active: bool) -> None:
            self.active = active

        def __bool__(self) -> bool:
            return self.active

    f1 = Flag(True)
    f2 = Flag(False)

    print(bool(f1))
    print(bool(f2))

    print()


# ----------------------------------------
# 5) NON-GUARANTEES AND LIMITATIONS
# ----------------------------------------

# Important rules:
#
# 1) Not all dunder methods are always used
#    Python may fallback or skip them depending on context
#
# 2) Some operations have multiple fallback paths
#    Example:
#    __add__ -> __radd__ -> TypeError
#
# 3) Returning wrong types breaks expectations
#
# 4) Overloading everything is a bad idea
#    It reduces readability and predictability


def non_guarantees_demo() -> None:
    print("=== non_guarantees_demo ===")

    class BadNumber:
        def __add__(self, other: BadNumber) -> int:
            # This breaks expectation:
            # __add__ should return same semantic type
            return 42

    a = BadNumber()
    b = BadNumber()

    result = a + b

    print(result)

    print()


# ----------------------------------------
# 6) DESIGN PRINCIPLES
# ----------------------------------------

# Key idea:
# Dunder methods should make objects feel natural.
#
# Good:
# - predictable behavior
# - consistent return types
# - matches built-in expectations
#
# Bad:
# - surprising behavior
# - hidden side effects
# - abusing operators


def design_principles_demo() -> None:
    print("=== design_principles_demo ===")

    class Vector:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

        def __add__(self, other: Vector) -> Vector:
            return Vector(self.x + other.x, self.y + other.y)

        def __repr__(self) -> str:
            return f"Vector(x={self.x}, y={self.y})"

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)

    print(v1 + v2)

    print()


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_dunder_concept_demo()
    protocol_demo()
    operator_mapping_demo()
    builtin_integration_demo()
    non_guarantees_demo()
    design_principles_demo()
