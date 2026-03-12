"""
Demonstration of frozen dataclasses.

This file explains how frozen dataclasses work, what guarantees they provide,
and what limitations they have. It also demonstrates how immutability affects
hashability and object behavior.
"""

from dataclasses import dataclass


# ----------------------------------------
# 1) BASIC FROZEN DATACLASS
# ----------------------------------------

# frozen=True makes dataclass instances read-only after initialization.
#
# Once the object is created, attribute reassignment is not allowed.
# Python will raise a dataclasses.FrozenInstanceError.
#
# Important: this restriction applies to normal attribute assignment.


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def basic_frozen_demo() -> None:
    print("=== basic_frozen_demo ===")

    p: Point = Point(10, 20)

    print(p)

    # Attempting to modify the object would raise an exception.
    #
    # The code below is intentionally commented out because executing it
    # would stop program execution.
    #
    # p.x = 50

    print()


# ----------------------------------------
# 2) FROZEN DOES NOT MEAN TRUE IMMUTABILITY
# ----------------------------------------

# "Frozen" prevents normal attribute assignment, but it does not make the
# object truly immutable.
#
# Python still allows modification through low-level mechanisms such as
# object.__setattr__.
#
# This behavior exists because Python enforces immutability at the
# attribute-access level, not at the memory level.


@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def bypass_frozen_demo() -> None:
    print("=== bypass_frozen_demo ===")

    c: Coordinates = Coordinates(50.45, 30.52)

    print("before:", c)

    # Direct attribute assignment is blocked:
    #
    # c.latitude = 0.0

    # But the low-level attribute setter can still modify the value.
    object.__setattr__(c, "latitude", 0.0)

    print("after:", c)

    print()


# ----------------------------------------
# 3) HASHABILITY
# ----------------------------------------

# One important consequence of immutability is hashability.
#
# Mutable objects should generally not be hashable because their state
# can change after being used as dictionary keys or set elements.
#
# Frozen dataclasses are safe to hash because their fields are expected
# to remain stable after creation.


@dataclass(frozen=True)
class UserID:
    id: int


def hashability_demo() -> None:
    print("=== hashability_demo ===")

    u1: UserID = UserID(1)
    u2: UserID = UserID(2)

    # Frozen dataclass instances can be used in sets.
    users = {u1, u2}

    print(users)

    # They can also be used as dictionary keys.
    user_map: dict[UserID, str] = {
        u1: "Alice",
        u2: "Bob",
    }

    print(user_map)

    print()


# ----------------------------------------
# 4) MUTABLE FIELDS INSIDE FROZEN OBJECTS
# ----------------------------------------

# Frozen dataclasses prevent reassignment of attributes, but they do not
# automatically freeze objects stored inside those attributes.
#
# If a field contains a mutable object (like a list), that object can still
# be modified.


@dataclass(frozen=True)
class Container:
    values: list[int]


def mutable_field_demo() -> None:
    print("=== mutable_field_demo ===")

    container: Container = Container([1, 2, 3])

    print("before:", container)

    # This does not reassign the attribute itself.
    # Instead, it mutates the list stored inside the attribute.
    container.values.append(4)

    print("after:", container)

    print()


# ----------------------------------------
# 5) WHEN FROZEN DATACLASSES ARE USEFUL
# ----------------------------------------

# Frozen dataclasses are commonly used for:
#
# - value objects
# - configuration objects
# - identifiers
# - keys used in dictionaries or sets
#
# They are especially useful when object identity should depend only
# on its data and not on mutable state.


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_frozen_demo()
    bypass_frozen_demo()
    hashability_demo()
    mutable_field_demo()
