"""
Demonstration of __post_init__ in dataclasses.

This file explains when __post_init__ is executed, why it exists,
and how it is used for validation and derived fields after the
auto-generated __init__ method finishes.
"""

from dataclasses import dataclass, field


# ----------------------------------------
# 1) WHY __post_init__ EXISTS
# ----------------------------------------

# When a dataclass is created, Python automatically generates
# an __init__ method that assigns all declared fields.
#
# Sometimes we need additional logic that should run *after*
# those assignments happen.
#
# __post_init__ is a hook that runs immediately after the
# generated __init__ finishes.


@dataclass
class User:
    name: str
    age: int

    def __post_init__(self) -> None:
        # This method runs automatically after __init__
        print(f"Object created for {self.name}")


def basic_post_init_demo() -> None:
    print("=== basic_post_init_demo ===")

    user: User = User("Alice", 20)

    print(user)

    print()


# ----------------------------------------
# 2) DATA VALIDATION
# ----------------------------------------

# A very common use of __post_init__ is validation.
#
# Because all fields already exist at this moment,
# we can safely inspect their values.


@dataclass
class Account:
    username: str
    balance: float

    def __post_init__(self) -> None:
        if self.balance < 0:
            raise ValueError("Balance cannot be negative")


def validation_demo() -> None:
    print("=== validation_demo ===")

    account: Account = Account("bob", 100.0)

    print(account)

    # Example of invalid construction.
    # This code is commented out to avoid interrupting execution.
    #
    # invalid_account = Account("bob", -10)

    print()


# ----------------------------------------
# 3) DERIVED / COMPUTED FIELDS
# ----------------------------------------

# Sometimes a field should not be passed to the constructor
# but instead computed from other values.
#
# For this we use:
# field(init=False)
#
# This prevents the attribute from appearing in __init__.


@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self) -> None:
        # area is derived from other fields
        self.area = self.width * self.height


def computed_field_demo() -> None:
    print("=== computed_field_demo ===")

    rect: Rectangle = Rectangle(10.0, 5.0)

    print(rect)
    print("area:", rect.area)

    print()


# ----------------------------------------
# 4) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_post_init_demo()
    validation_demo()
    computed_field_demo()
