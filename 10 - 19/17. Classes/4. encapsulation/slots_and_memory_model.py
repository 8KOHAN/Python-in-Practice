"""
Explains __slots__, instance memory layout,
absence of __dict__, and how attribute storage works in CPython.
"""

from __future__ import annotations
import sys


# ----------------------------------------
# 1) DEFAULT INSTANCE MEMORY MODEL
# ----------------------------------------

def default_instance_memory_demo() -> None:
    print("=== default_instance_memory_demo ===")

    # By default, every instance of a user-defined class
    # stores attributes inside a dictionary.
    #
    # That dictionary is accessible via:
    # instance.__dict__
    #
    # This provides flexibility:
    # - dynamic attribute creation
    # - runtime mutation of structure
    #
    # But it has a memory cost.

    class User:
        def __init__(self, name: str, age: int) -> None:
            self.name: str = name
            self.age: int = age

    user: User = User("alice", 30)

    print("Instance dict:", user.__dict__)
    print("Has __dict__:", hasattr(user, "__dict__"))

    # Memory size of the object itself
    print("Instance size:", sys.getsizeof(user))

    print()


# ----------------------------------------
# 2) INTRODUCTION TO __slots__
# ----------------------------------------

def slots_basic_demo() -> None:
    print("=== slots_basic_demo ===")

    # __slots__ removes the per-instance __dict__.
    #
    # Instead of a dictionary,
    # attributes are stored in a fixed internal structure.
    #
    # This reduces memory usage
    # and prevents dynamic attribute creation.

    class User:
        __slots__ = ("name", "age")

        def __init__(self, name: str, age: int) -> None:
            self.name: str = name
            self.age: int = age

    user: User = User("bob", 25)

    print("Has __dict__:", hasattr(user, "__dict__"))
    print("Instance size:", sys.getsizeof(user))

    # Trying to assign a new attribute will fail.
    # user.email = "test@example.com"  # AttributeError

    print()


# ----------------------------------------
# 3) MEMORY COMPARISON
# ----------------------------------------

def memory_comparison_demo() -> None:
    print("=== memory_comparison_demo ===")

    class Regular:
        def __init__(self) -> None:
            self.x: int = 1
            self.y: int = 2

    class Slotted:
        __slots__ = ("x", "y")

        def __init__(self) -> None:
            self.x: int = 1
            self.y: int = 2

    regular: Regular = Regular()
    slotted: Slotted = Slotted()

    # Important:
    # sys.getsizeof does NOT show total memory footprint.
    # It shows only the object header size.
    #
    # For regular objects, attribute data lives in __dict__,
    # which is a separate object in memory.

    print("Regular instance size:", sys.getsizeof(regular))
    print("Regular __dict__ size:", sys.getsizeof(regular.__dict__))
    print("Slotted instance size:", sys.getsizeof(slotted))

    print()


# ----------------------------------------
# 4) INHERITANCE WITH __slots__
# ----------------------------------------

def slots_inheritance_demo() -> None:
    print("=== slots_inheritance_demo ===")

    # __slots__ interacts with inheritance in non-trivial ways.
    #
    # If a base class defines __slots__,
    # subclasses must also define __slots__
    # to avoid reintroducing __dict__.

    class Base:
        __slots__ = ("x",)

        def __init__(self, x: int) -> None:
            self.x: int = x

    class Child(Base):
        __slots__ = ("y",)

        def __init__(self, x: int, y: int) -> None:
            super().__init__(x)
            self.y: int = y

    child = Child(1, 2)

    print("Has __dict__:", hasattr(child, "__dict__"))

    print()


# ----------------------------------------
# 5) DESIGN LIMITATIONS
# ----------------------------------------

# __slots__ limitations and design implications:
#
# - No dynamic attribute creation
# - Harder to use with multiple inheritance
# - Some libraries expect __dict__ to exist
# - Slightly reduced flexibility for debugging
#
# __slots__ is beneficial when:
# - Creating many small objects
# - Memory footprint matters
# - Object structure is stable and known in advance
#
# It is NOT primarily a performance optimization.
# It is a memory layout optimization.


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    default_instance_memory_demo()
    slots_basic_demo()
    memory_comparison_demo()
    slots_inheritance_demo()
