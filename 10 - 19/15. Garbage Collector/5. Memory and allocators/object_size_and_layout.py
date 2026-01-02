"""
Object size and memory layout in CPython.

This module explains:
- what sys.getsizeof() really measures
- how PyObject and PyVarObject affect object size
- why containers over-allocate memory
- how logical size != physical memory usage
"""

from __future__ import annotations
import sys
import gc


# ----------------------------------------
# 1) WHAT sys.getsizeof() MEASURES
# ----------------------------------------
#
# sys.getsizeof(obj):
# - returns size of the object in bytes
# - includes: PyObject header + inline data
# - excludes: memory referenced by the object
#
# IMPORTANT:
# - this is CPython-specific
# - it does NOT include allocator overhead (pymalloc)


def sizeof_basic_demo() -> None:
    print("=== sizeof_basic_demo ===")

    objs = [
        None,
        0,
        1.0,
        "",
        (),
        [],
        {},
        object(),
    ]

    for obj in objs:
        print(f"{type(obj).__name__:>10} -> {sys.getsizeof(obj)} bytes")

    print()


# ----------------------------------------
# 2) PyObject HEADER COST
# ----------------------------------------
#
# Every Python object has:
# - ob_refcnt
# - ob_type
#
# On 64-bit CPython:
# - header usually costs 16 bytes
#
# This is the MINIMUM cost of any object.


def pyobject_header_demo() -> None:
    print("=== pyobject_header_demo ===")

    class Empty:
        pass

    e: Empty = Empty()
    print("empty user object size:", sys.getsizeof(e))
    print("NOTE: this includes only PyObject + __dict__ pointer\n")


# ----------------------------------------
# 3) PyVarObject AND VARIABLE-SIZED OBJECTS
# ----------------------------------------
#
# Variable-sized objects (list, tuple, str, bytes) use PyVarObject:
# - PyObject header
# - ob_size (length)
# - inline storage for elements (or pointer to it)


def varobject_demo() -> None:
    print("=== varobject_demo ===")

    lst: list[int] = []
    print("empty list:", sys.getsizeof(lst))

    for i in range(5):
        lst.append(i)
        print(f"list len={len(lst):2d} size={sys.getsizeof(lst)}")

    print("NOTE: list grows in steps due to overallocation\n")


# ----------------------------------------
# 4) OVER-ALLOCATION STRATEGY
# ----------------------------------------
#
# CPython containers grow exponentially to keep amortized O(1) append.


def list_overallocation_demo() -> None:
    print("=== list_overallocation_demo ===")

    lst: list[int] = []
    prev: int = sys.getsizeof(lst)

    for i in range(64):
        lst.append(i)
        current = sys.getsizeof(lst)
        if current != prev:
            print(f"len={len(lst):2d} size changed {prev} -> {current}")
            prev = current

    print()


# ----------------------------------------
# 5) REFERENCED MEMORY IS NOT INCLUDED
# ----------------------------------------
#
# sys.getsizeof(container) does NOT include:
# - elements
# - nested objects
#
# Only the container itself.


# ----------------------------------------
# 6) IMMUTABLE VS MUTABLE OBJECTS
# ----------------------------------------
#
# Immutable objects often pack data tightly.
# Mutable ones need spare capacity.


def immutable_vs_mutable_demo() -> None:
    print("=== immutable_vs_mutable_demo ===")

    t = tuple(range(10))
    l = list(range(10))

    print("tuple size:", sys.getsizeof(t))
    print("list  size:", sys.getsizeof(l))
    print()


# ----------------------------------------
# 7) COMMON MISCONCEPTIONS
# ----------------------------------------
#
# "sys.getsizeof shows full memory usage"
# "objects shrink when elements are removed"
#
# getsizeof shows object layout only
# memory may stay reserved


# ----------------------------------------
# 8) QUICK CHECKLIST
# ----------------------------------------
#
# - Every object has a header cost
# - Containers over-allocate
# - Referenced objects not counted
# - pymalloc overhead is invisible here


# ----------------------------------------
# 9) QUICK RUN
# ----------------------------------------

if __name__ == "__main__":
    sizeof_basic_demo()
    pyobject_header_demo()
    varobject_demo()
    list_overallocation_demo()
    immutable_vs_mutable_demo()
