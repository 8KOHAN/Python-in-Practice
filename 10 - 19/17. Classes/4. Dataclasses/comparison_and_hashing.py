"""
Demonstration of comparison and hashing behavior in dataclasses.

This file explains how dataclasses generate comparison methods,
how ordering works, and how hashing interacts with mutability
and frozen dataclasses.
"""

from dataclasses import dataclass


# ----------------------------------------
# 1) DEFAULT EQUALITY (__eq__)
# ----------------------------------------

# By default, dataclasses generate an equality method (__eq__).
#
# Two instances are considered equal if:
# - they belong to the same class
# - all declared fields compare equal
#
# The comparison is performed field-by-field in the order
# the fields were defined.


@dataclass
class User:
    name: str
    age: int


def equality_demo() -> None:
    print("=== equality_demo ===")

    user1 = User("Alice", 20)
    user2 = User("Alice", 20)
    user3 = User("Bob", 30)

    print(user1 == user2)
    print(user1 == user3)

    print()


# ----------------------------------------
# 2) COMPARISON WITH DIFFERENT TYPES
# ----------------------------------------

# Equality checks also require that both objects have
# the same type.
#
# Even if two objects have identical fields, they are
# not considered equal if their classes differ.


@dataclass
class Customer:
    name: str
    age: int


def different_type_demo() -> None:
    print("=== different_type_demo ===")

    user = User("Alice", 20)
    customer = Customer("Alice", 20)

    print(user == customer)

    print()


# ----------------------------------------
# 3) ORDERING METHODS
# ----------------------------------------

# Dataclasses can automatically generate ordering methods:
#
# - __lt__  (less than)
# - __le__  (less than or equal)
# - __gt__  (greater than)
# - __ge__  (greater than or equal)
#
# To enable this behavior we use order=True.
#
# Ordering compares fields sequentially in the order they
# are declared.


@dataclass(order=True)
class Score:
    points: int
    player: str


def ordering_demo() -> None:
    print("=== ordering_demo ===")

    s1 = Score(100, "Alice")
    s2 = Score(200, "Bob")

    print(s1 < s2)
    print(s2 > s1)

    print()


# ----------------------------------------
# 4) HASHING AND MUTABILITY
# ----------------------------------------

# Hashing is used by dictionaries and sets.
#
# Objects used as keys must have stable hash values.
#
# Mutable objects are dangerous as dictionary keys because
# their internal state may change after insertion.
#
# For this reason, normal (mutable) dataclasses do NOT
# automatically generate a hash method.


@dataclass
class MutablePoint:
    x: int
    y: int


def mutable_hash_demo() -> None:
    print("=== mutable_hash_demo ===")

    p = MutablePoint(1, 2)

    # Attempting to hash a mutable dataclass instance
    # will raise a TypeError.
    #
    # print(hash(p))

    print("Mutable dataclass instances are not hashable by default")

    print()


# ----------------------------------------
# 5) HASHING WITH FROZEN DATACLASSES
# ----------------------------------------

# Frozen dataclasses are treated as immutable objects.
#
# Because their state should not change after creation,
# Python can safely generate a hash method.


@dataclass(frozen=True)
class FrozenPoint:
    x: int
    y: int


def frozen_hash_demo() -> None:
    print("=== frozen_hash_demo ===")

    p1 = FrozenPoint(1, 2)
    p2 = FrozenPoint(3, 4)

    point_set: set[FrozenPoint] = {p1, p2}

    print(point_set)

    point_map: dict[FrozenPoint, str] = {
        p1: "A",
        p2: "B",
    }

    print(point_map)

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    equality_demo()
    different_type_demo()
    ordering_demo()
    mutable_hash_demo()
    frozen_hash_demo()
