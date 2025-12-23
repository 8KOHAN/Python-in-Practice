# This module explores hidden references in Python — references that are not
# obvious from the source code, but which can keep objects alive.
# It covers:
# - stack frame references
# - closure variables (cell objects)
# - temporary evaluation references
# - hidden references in containers and comprehensions
#
# All examples are CPython-specific.

from __future__ import annotations
import sys
from typing import Callable


def header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------------------
# 1. Hidden references in stack frames
# ---------------------------------------------------------------------------
# Local variables in a function are stored in the frame object.
# As long as the frame is alive, all locals hold references to their objects.
# Even if you delete the variable from your code, the frame may keep it alive.

def frame_ref_demo() -> None:
    header("frame_ref_demo")

    def f() -> list[int]:
        x: list[int] = [1, 2, 3]
        print("Inside f(), getrefcount(x):", sys.getrefcount(x))
        return x

    x_ref: list[int] = f()
    print("After f() returned, x_ref is alive, getrefcount(x_ref):", sys.getrefcount(x_ref))
    del x_ref
    print("After deleting x_ref, object may be freed (refcount drops to 0)")


# ---------------------------------------------------------------------------
# 2. Hidden references in closures (cell objects)
# ---------------------------------------------------------------------------
# Variables captured by inner functions are stored in cell objects.
# They are invisible from the outer scope but keep objects alive.

def closure_ref_demo() -> None:
    header("closure_ref_demo")

    def outer() -> Callable[[], list[int]]:
        y: list[int] = [10, 20]
        def inner() -> list[int]:
            return y
        return inner

    f: Callable[[], list[int]] = outer()  # inner function keeps y alive in a cell
    cell_refcount = sys.getrefcount(f())
    print("Refcount of y inside closure (via call):", cell_refcount)
    del f
    print("After deleting inner function, y can be collected if no other refs exist")


# ---------------------------------------------------------------------------
# 3. Hidden references in temporary expressions
# ---------------------------------------------------------------------------
# Python sometimes creates temporary references during evaluation, e.g.,
# when using list comprehensions, chained operations, or function calls.

def temporary_refs_demo() -> None:
    header("temporary_refs_demo")
    x: object = object()

    print("Initial refcount:", sys.getrefcount(x))
    _ = [x for _ in range(5)]
    print("After list comprehension, temporary refs gone, refcount back:", sys.getrefcount(x))


# ---------------------------------------------------------------------------
# 4. Pitfalls and GC interaction
# ---------------------------------------------------------------------------
# - Objects may survive longer than expected because of hidden references
# - Cycles involving closures or frames require the cyclic garbage collector
# - sys.getrefcount always includes a temporary reference from the call itself
# - Hidden references are invisible in locals() if a frame is gone, but cell objects
#   in closures still keep the objects alive.


if __name__ == "__main__":
    frame_ref_demo()
    closure_ref_demo()
    temporary_refs_demo()
