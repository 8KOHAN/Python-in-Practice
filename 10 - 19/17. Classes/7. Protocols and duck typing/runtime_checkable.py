"""
Demonstrates @runtime_checkable for Protocol.
Focuses on enabling isinstance() checks and their limitations.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


# ----------------------------------------
# 1) DEFAULT PROTOCOL BEHAVIOR
# ----------------------------------------

# By default, Protocol is only used by static type checkers.
# isinstance() and issubclass() do NOT work with plain Protocol.

class SupportsClose(Protocol):
    def close(self) -> None:
        ...


def default_protocol_behavior_demo() -> None:
    print("=== default_protocol_behavior_demo ===")

    class File:
        def close(self) -> None:
            print("File closed")

    file = File()

    # This will raise TypeError if uncommented:
    # isinstance(file, SupportsClose)

    # Protocol without runtime_checkable has no runtime presence
    print("Protocol cannot be used with isinstance() by default")

    print()


# ----------------------------------------
# 2) ENABLING RUNTIME CHECKING
# ----------------------------------------

# runtime_checkable adds minimal runtime support
# Now isinstance() works, but only checks attribute presence

@runtime_checkable
class RuntimeSupportsClose(Protocol):
    def close(self) -> None:
        ...


def runtime_checkable_basic_demo() -> None:
    print("=== runtime_checkable_basic_demo ===")

    class File:
        def close(self) -> None:
            print("File closed")

    file = File()

    if isinstance(file, RuntimeSupportsClose):
        print("Object supports close() at runtime")
        file.close()

    print()


# ----------------------------------------
# 3) ONLY STRUCTURE IS CHECKED
# ----------------------------------------

# runtime_checkable does NOT validate signatures deeply
# It only checks that attribute exists

@runtime_checkable
class SupportsRead(Protocol):
    def read(self) -> str:
        ...


def shallow_check_demo() -> None:
    print("=== shallow_check_demo ===")

    class BadReader:
        # Wrong return type, but still passes runtime check
        def read(self) -> int:
            return 123

    reader = BadReader()

    if isinstance(reader, SupportsRead):
        print("Reader passes runtime check")

        # This works at runtime but violates expected contract
        result = reader.read()
        print(f"Returned value: {result}")

    print()


# ----------------------------------------
# 4) ATTRIBUTE-BASED CHECKING
# ----------------------------------------

# Protocol can require attributes, not just methods

@runtime_checkable
class HasName(Protocol):
    name: str


def attribute_runtime_check_demo() -> None:
    print("=== attribute_runtime_check_demo ===")

    class User:
        def __init__(self, name: str) -> None:
            self.name = name

    class Nameless:
        def __init__(self) -> None:
            self.id = 1

    user = User("Alice")
    nameless = Nameless()

    print(isinstance(user, HasName))       # True
    print(isinstance(nameless, HasName))  # False

    print()


# ----------------------------------------
# 5) LIMITATIONS AND NON-GUARANTEES
# ----------------------------------------

# runtime_checkable DOES:
# - allow isinstance() with Protocol
# - check attribute presence at runtime

# runtime_checkable DOES NOT:
# - validate method signatures
# - validate return types
# - validate argument types
# - guarantee correct behavior

# It is a shallow structural check, not a full contract validation.


# ----------------------------------------
# 6) WHEN TO USE runtime_checkable
# ----------------------------------------

# Use it when:
# - you need runtime flexibility
# - you want lightweight interface checks
# - you work with dynamic or plugin-like systems

# Avoid relying on it for:
# - strict validation
# - enforcing correctness
# - replacing static type checking


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    default_protocol_behavior_demo()
    runtime_checkable_basic_demo()
    shallow_check_demo()
    attribute_runtime_check_demo()
