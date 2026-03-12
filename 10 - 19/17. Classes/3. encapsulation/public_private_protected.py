"""
Demonstrates public, protected and private attributes in Python,
name mangling mechanics, and why access control in Python is convention-based.
"""

from __future__ import annotations


# ----------------------------------------
# 1) PUBLIC ATTRIBUTES
# ----------------------------------------

def public_attributes_demo() -> None:
    print("=== public_attributes_demo ===")

    # Public attributes have no leading underscore.
    # They are part of the object's public API.
    # External code is allowed to read and modify them.

    class User:
        def __init__(self, username: str, age: int) -> None:
            self.username: str = username
            self.age: int = age

    user: User = User("alice", 30)

    # Direct access is normal and expected.
    print(user.username)
    print(user.age)

    # Mutation is allowed.
    user.age = 31
    print(user.age)

    # Public attributes are a contract.
    # Changing their name later is a breaking API change.

    print()


# ----------------------------------------
# 2) PROTECTED ATTRIBUTES (CONVENTION)
# ----------------------------------------

def protected_attributes_demo() -> None:
    print("=== protected_attributes_demo ===")

    # A single leading underscore signals:
    # "This is an implementation detail."
    # It is still accessible, but external code SHOULD NOT depend on it.
    # Python does not enforce this restriction.

    class Account:
        def __init__(self, balance: float) -> None:
            self._balance: float = balance

        def deposit(self, amount: float) -> None:
            self._balance += amount

    account: Account = Account(100.0)

    # Technically allowed:
    print(account._balance)

    # But modifying protected attributes from outside
    # violates encapsulation and may break invariants.
    account._balance = -1.0
    print(account._balance)

    # Protected attributes exist for developers,
    # not for the interpreter.

    print()


# ----------------------------------------
# 3) PRIVATE ATTRIBUTES (NAME MANGLING)
# ----------------------------------------

def private_attributes_demo() -> None:
    print("=== private_attributes_demo ===")

    # Double underscore triggers name mangling.
    # This is NOT true privacy.
    # It is a mechanism to avoid accidental overriding in subclasses.

    class DatabaseConnection:
        def __init__(self, dsn: str) -> None:
            self.__dsn: str = dsn

        def get_dsn(self) -> str:
            return self.__dsn

    db: DatabaseConnection = DatabaseConnection("postgres://localhost")

    # Direct access will fail:
    # print(db.__dsn)  # AttributeError

    # Name mangling transforms:
    # __dsn -> _DatabaseConnection__dsn
    print(db._DatabaseConnection__dsn)

    # Name mangling is deterministic and class-based.
    # It prevents accidental clashes in inheritance hierarchies,
    # but does not provide real access protection.

    print()


# ----------------------------------------
# 4) NAME MANGLING AND INHERITANCE
# ----------------------------------------

def name_mangling_inheritance_demo() -> None:
    print("=== name_mangling_inheritance_demo ===")

    # Demonstrates why double underscore exists.

    class Base:
        def __init__(self) -> None:
            self.__value: int = 10

        def get_value(self) -> int:
            return self.__value

    class Child(Base):
        def __init__(self) -> None:
            super().__init__()
            self.__value: int = 999  # This does NOT override Base.__value

    child: Child = Child()

    # Base value remains unchanged.
    print(child.get_value())

    # Child has its own mangled attribute.
    print(child._Child__value)

    # And Base still has its own.
    print(child._Base__value)

    # This demonstrates that name mangling
    # isolates attributes per class.

    print()


# ----------------------------------------
# 5) WHEN TO USE EACH LEVEL
# ----------------------------------------
#
# Public attributes:
# Use when the attribute is part of the stable and documented API.
# External code is expected to rely on it.
# Renaming or removing it is a breaking change.
# Public attributes define how the object is meant to be used.
#
# Protected attributes (_attribute):
# Use for internal mechanics of the class.
# Signals to other developers:
# "This is an implementation detail. Do not depend on it."
# Still accessible, but modifying it externally violates design boundaries.
# Protection is based on convention, not enforcement.
#
# Private attributes (__attribute):
# Use when you need name isolation inside inheritance hierarchies.
# The main purpose is preventing accidental overriding in subclasses.
# This is not real privacy — it is name mangling.
# Suitable for:
# - complex base classes
# - framework-level abstractions
# - protecting fragile internal invariants
#
# Important:
# Python does not enforce access modifiers.
# Encapsulation is a design discipline.
# It relies on developer responsibility rather than compiler restrictions.


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    public_attributes_demo()
    protected_attributes_demo()
    private_attributes_demo()
    name_mangling_inheritance_demo()
