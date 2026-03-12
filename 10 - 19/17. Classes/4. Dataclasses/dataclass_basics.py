"""
Basic introduction to dataclasses.

This file demonstrates why dataclasses exist, how they reduce boilerplate
in class definitions, and what functionality the decorator automatically
generates for us.
"""

from dataclasses import dataclass


# ----------------------------------------
# 1) MANUAL CLASS IMPLEMENTATION
# ----------------------------------------

# Before dataclasses existed, writing simple data containers required
# significant boilerplate code.
#
# Even a small class needed:
#
# - __init__
# - __repr__
# - sometimes __eq__
#
# When many such classes exist in a codebase, this repetition becomes
# noisy and error-prone.


class ManualUser:
    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: int = age

    def __repr__(self) -> str:
        return f"ManualUser(name={self.name!r}, age={self.age!r})"


def manual_class_demo() -> None:
    print("=== manual_class_demo ===")

    user: ManualUser = ManualUser("Alice", 30)

    # Printing the object calls __repr__
    print(user)

    print()


# ----------------------------------------
# 2) BASIC DATACLASS
# ----------------------------------------

# A dataclass automatically generates several special methods
# based on the declared attributes.
#
# By default, the decorator generates:
#
# - __init__
# - __repr__
# - __eq__
#
# This dramatically reduces boilerplate when creating simple
# classes whose main purpose is to store data.


@dataclass
class User:
    name: str
    age: int


def basic_dataclass_demo() -> None:
    print("=== basic_dataclass_demo ===")

    user: User = User("Bob", 25)

    # __repr__ is generated automatically
    print(user)

    print()


# ----------------------------------------
# 3) GENERATED EQUALITY
# ----------------------------------------

# Dataclasses also generate an equality method (__eq__).
#
# Two instances are considered equal if:
# - they are instances of the same class
# - all fields compare equal
#
# This behavior is often exactly what we want for value-like objects.


def equality_demo() -> None:
    print("=== equality_demo ===")

    user1: User = User("Charlie", 40)
    user2: User = User("Charlie", 40)

    # Because __eq__ is generated automatically,
    # these objects compare by value.
    print(user1 == user2)

    print()


# ----------------------------------------
# 4) TYPE ANNOTATIONS AS FIELD DEFINITIONS
# ----------------------------------------

# Dataclasses rely on type annotations to detect fields.
#
# Every annotated attribute becomes a dataclass field.
#
# Without type annotations the attribute would simply be a
# normal class variable.


@dataclass
class Product:
    name: str
    price: float
    quantity: int


def field_definition_demo() -> None:
    print("=== field_definition_demo ===")

    product = Product("Keyboard", 99.99, 3)

    print(product)

    print()


# ----------------------------------------
# 5) DEFAULT VALUES
# ----------------------------------------

# Dataclass fields may define default values.
#
# This behaves similarly to default arguments in functions.


@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False


def default_values_demo() -> None:
    print("=== default_values_demo ===")

    config = Config()

    print(config)

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    manual_class_demo()
    basic_dataclass_demo()
    equality_demo()
    field_definition_demo()
    default_values_demo()
