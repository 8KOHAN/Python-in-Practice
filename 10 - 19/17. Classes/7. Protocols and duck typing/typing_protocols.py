"""
Demonstrates typing.Protocol and structural typing in Python.
Focuses on how Protocol defines behavior-based interfaces.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


# ----------------------------------------
# 1) BASIC PROTOCOL DEFINITION
# ----------------------------------------

# Protocol defines an interface based on structure, not inheritance.
# Any object that matches required methods is considered valid.

class SupportsClose(Protocol):
    def close(self) -> None:
        ...


def close_resource(resource: SupportsClose) -> None:
    print("=== close_resource ===")

    # No isinstance checks required
    # If object has .close(), it is valid
    resource.close()

    print()


def basic_protocol_demo() -> None:
    print("=== basic_protocol_demo ===")

    class File:
        def close(self) -> None:
            print("File closed")

    class Socket:
        def close(self) -> None:
            print("Socket closed")

    file = File()
    socket = Socket()

    # Both objects satisfy protocol without inheritance
    close_resource(file)
    close_resource(socket)

    print()


# ----------------------------------------
# 2) PROTOCOL WITH MULTIPLE METHODS
# ----------------------------------------

# Protocol can define multiple required methods.
# Object must implement ALL of them.

class SupportsReadWrite(Protocol):
    def read(self) -> str:
        ...

    def write(self, data: str) -> None:
        ...


def use_io(device: SupportsReadWrite) -> None:
    print("=== use_io ===")

    data = device.read()
    print(f"Read: {data}")

    device.write("new data")

    print()


def multi_method_protocol_demo() -> None:
    print("=== multi_method_protocol_demo ===")

    class MemoryBuffer:
        def __init__(self) -> None:
            self._data = "initial"

        def read(self) -> str:
            return self._data

        def write(self, data: str) -> None:
            self._data = data
            print("Buffer updated")

    buffer = MemoryBuffer()
    use_io(buffer)

    print()


# ----------------------------------------
# 3) RUNTIME CHECKABLE PROTOCOL
# ----------------------------------------

# By default, Protocol is only for static type checking.
# runtime_checkable allows using isinstance()

@runtime_checkable
class SupportsLen(Protocol):
    def __len__(self) -> int:
        ...


def runtime_check_demo() -> None:
    print("=== runtime_check_demo ===")

    data: list[int] = [1, 2, 3]

    # Works because of runtime_checkable
    if isinstance(data, SupportsLen):
        print(f"Length: {len(data)}")

    print()


# ----------------------------------------
# 4) PROTOCOL WITH ATTRIBUTES
# ----------------------------------------

# Protocol can define required attributes, not just methods.

class HasName(Protocol):
    name: str


def greet(entity: HasName) -> None:
    print("=== greet ===")

    print(f"Hello, {entity.name}")

    print()


def attribute_protocol_demo() -> None:
    print("=== attribute_protocol_demo ===")

    class User:
        def __init__(self, name: str) -> None:
            self.name = name

    class Product:
        def __init__(self, name: str) -> None:
            self.name = name

    user = User("Alice")
    product = Product("Laptop")

    greet(user)
    greet(product)

    print()


# ----------------------------------------
# 5) PROTOCOL VS INHERITANCE (CONCEPT)
# ----------------------------------------

# Key idea:
# Protocol = structural typing (what object can do)
# Inheritance = nominal typing (what object is)

# Important properties:
# - No need to inherit from Protocol
# - No explicit registration required
# - Works naturally with duck typing
# - Checked by static type checkers (mypy, pyright)

# Non-guarantees:
# - No runtime enforcement without runtime_checkable
# - Does not prevent incorrect implementations at runtime


# ----------------------------------------
# 6) LIMITATIONS AND PITFALLS
# ----------------------------------------

# Protocol does NOT:
# - enforce method signatures at runtime
# - validate return types dynamically
# - guarantee behavior correctness

# Example (theoretical, not executed):
#
# class Bad:
#     def read(self) -> int:   # wrong return type
#         return 123
#
# Static checker will warn, but Python runtime will not.


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_protocol_demo()
    multi_method_protocol_demo()
    runtime_check_demo()
    attribute_protocol_demo()
