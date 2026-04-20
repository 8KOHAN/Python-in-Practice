"""
Comparison dunder methods in Python.
Covers equality, ordering, and consistency rules.
"""

from __future__ import annotations


# ----------------------------------------
# 1) EQUALITY: __eq__ AND __ne__
# ----------------------------------------
#
# __eq__ defines behavior of ==
# __ne__ defines behavior of !=
#
# If __ne__ is not defined, Python will invert __eq__


def equality_demo() -> None:
    print("=== equality_demo ===")

    class User:
        def __init__(self, user_id: int) -> None:
            self.user_id = user_id

        def __eq__(self, other: object) -> bool:
            # Always check type safety
            if not isinstance(other, User):
                return NotImplemented

            return self.user_id == other.user_id

    u1 = User(1)
    u2 = User(1)
    u3 = User(2)

    print(u1 == u2)  # True
    print(u1 == u3)  # False
    print(u1 != u2)  # False (inverted __eq__)

    print()


# ----------------------------------------
# 2) ORDERING METHODS
# ----------------------------------------
#
# Ordering methods:
# __lt__  -> <
# __le__  -> <=
# __gt__  -> >
# __ge__  -> >=
#
# Python does NOT infer all of them automatically
# You must define what you need


def ordering_demo() -> None:
    print("=== ordering_demo ===")

    class Product:
        def __init__(self, price: float) -> None:
            self.price = price

        def __lt__(self, other: object) -> bool:
            if not isinstance(other, Product):
                return NotImplemented

            return self.price < other.price

    p1 = Product(10.0)
    p2 = Product(20.0)

    print(p1 < p2)   # True
    print(p1 > p2)   # Works via fallback logic

    print()


# ----------------------------------------
# 3) NOTIMPLEMENTED AND FALLBACKS
# ----------------------------------------
#
# Returning NotImplemented is critical.
#
# It tells Python:
# "I don't know how to compare with this type"
#
# Then Python tries:
# other.__eq__(self)
#
# If both fail -> TypeError


def notimplemented_demo() -> None:
    print("=== notimplemented_demo ===")

    class A:
        def __eq__(self, other: object) -> bool:
            if not isinstance(other, A):
                return NotImplemented
            return True

    class B:
        pass

    a = A()
    b = B()

    print(a == b)  # False, no valid comparison

    print()


# ----------------------------------------
# 4) CONSISTENCY RULES
# ----------------------------------------
#
# Important expectations:
#
# 1) Reflexive: a == a is True
# 2) Symmetric: (a == b) == (b == a)
# 3) Transitive: if a == b and b == c -> a == c
#
# Violating these breaks logic in sets, dicts, etc.


def consistency_demo() -> None:
    print("=== consistency_demo ===")

    class Weird:
        def __eq__(self, other: object) -> bool:
            return True  # breaks logic

    a = Weird()
    b = Weird()

    print(a == b)  # True
    print(a == a)  # True (but meaningless)

    print()


# ----------------------------------------
# 5) __hash__ INTERACTION
# ----------------------------------------
#
# If you override __eq__, you must think about __hash__.
#
# Rule:
# Equal objects MUST have same hash
#
# If __eq__ is defined and __hash__ is not:
# object becomes unhashable (by default in modern Python)


def hash_interaction_demo() -> None:
    print("=== hash_interaction_demo ===")

    class Item:
        def __init__(self, value: int) -> None:
            self.value = value

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Item):
                return NotImplemented
            return self.value == other.value

        def __hash__(self) -> int:
            return hash(self.value)

    i1 = Item(10)
    i2 = Item(10)

    s = {i1, i2}

    print(len(s))  # 1, because objects are equal

    print()


# ----------------------------------------
# 6) PARTIAL IMPLEMENTATION PROBLEM
# ----------------------------------------
#
# Defining only one comparison method can lead to confusing behavior.
#
# Python does not automatically generate full ordering logic.
#
# Solution:
# Either implement all methods
# or use tools like functools.total_ordering (not covered here)


# ----------------------------------------
# 7) DESIGN GUIDELINES
# ----------------------------------------
#
# Good comparison design:
# - based on meaningful attributes
# - consistent
# - predictable
#
# Bad:
# - random comparisons
# - changing logic over time
# - ignoring type safety


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    equality_demo()
    ordering_demo()
    notimplemented_demo()
    consistency_demo()
    hash_interaction_demo()
