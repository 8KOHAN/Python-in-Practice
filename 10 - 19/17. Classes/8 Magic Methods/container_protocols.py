"""
Container protocols in Python.
Defines how objects behave like collections: indexing, iteration, membership.
"""

from __future__ import annotations


# ----------------------------------------
# 1) WHAT IS A CONTAINER
# ----------------------------------------
#
# A container is an object that can:
# - store elements
# - provide access to them
#
# Core dunder methods:
#
# __len__        -> len(obj)
# __getitem__    -> obj[index]
# __contains__   -> value in obj
#
# Optional:
# __iter__       -> iteration support


def basic_container_demo() -> None:
    print("=== basic_container_demo ===")

    class SimpleList:
        def __init__(self, items: list[int]) -> None:
            self.items = items

        def __len__(self) -> int:
            return len(self.items)

        def __getitem__(self, index: int) -> int:
            return self.items[index]

    s = SimpleList([10, 20, 30])

    print(len(s))
    print(s[1])

    print()


# ----------------------------------------
# 2) ITERATION PROTOCOL
# ----------------------------------------
#
# Iteration works in this order:
#
# 1) If __iter__ exists -> use it
# 2) Otherwise fallback to __getitem__ starting from index 0
#
# Stop condition:
# - StopIteration exception


def iteration_demo() -> None:
    print("=== iteration_demo ===")

    class Iterable:
        def __init__(self, items: list[int]) -> None:
            self.items = items

        def __iter__(self):
            return iter(self.items)

    obj = Iterable([1, 2, 3])

    for value in obj:
        print(value)

    print()


# ----------------------------------------
# 3) __getitem__ FALLBACK ITERATION
# ----------------------------------------
#
# If __iter__ is not defined,
# Python will try __getitem__(0), __getitem__(1), ...
#
# Until IndexError is raised


def getitem_iteration_demo() -> None:
    print("=== getitem_iteration_demo ===")

    class Sequence:
        def __init__(self, items: list[int]) -> None:
            self.items = items

        def __getitem__(self, index: int) -> int:
            return self.items[index]

    seq = Sequence([5, 6, 7])

    for value in seq:
        print(value)

    print()


# ----------------------------------------
# 4) MEMBERSHIP TEST: __contains__
# ----------------------------------------
#
# "value in obj" works like this:
#
# 1) Try __contains__
# 2) Else iterate and compare


def contains_demo() -> None:
    print("=== contains_demo ===")

    class Container:
        def __init__(self, items: list[int]) -> None:
            self.items = items

        def __contains__(self, value: int) -> bool:
            return value in self.items

    c = Container([1, 2, 3])

    print(2 in c)
    print(5 in c)

    print()


# ----------------------------------------
# 5) SLICING SUPPORT
# ----------------------------------------
#
# __getitem__ also receives slice objects
#
# Example:
# obj[1:3] -> __getitem__(slice(1, 3))


def slicing_demo() -> None:
    print("=== slicing_demo ===")

    class Sliceable:
        def __init__(self, items: list[int]) -> None:
            self.items = items

        def __getitem__(self, key: int | slice) -> int | list[int]:
            return self.items[key]

    s = Sliceable([10, 20, 30, 40])

    print(s[1])
    print(s[1:3])

    print()


# ----------------------------------------
# 6) DESIGN EXPECTATIONS
# ----------------------------------------
#
# Good container behavior:
# - predictable indexing
# - consistent length
# - stable iteration
#
# Bad:
# - changing size during iteration
# - returning wrong types
# - inconsistent __len__ vs actual data


# ----------------------------------------
# 7) NON-GUARANTEES
# ----------------------------------------
#
# Python does NOT guarantee:
# - that __len__ reflects actual storage
# - that iteration is stable
# - that __contains__ is efficient
#
# These depend on implementation


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_container_demo()
    iteration_demo()
    getitem_iteration_demo()
    contains_demo()
    slicing_demo()
