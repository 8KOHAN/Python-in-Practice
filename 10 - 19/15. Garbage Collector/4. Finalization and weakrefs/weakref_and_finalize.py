"""
Safe object finalization with weakref.finalize.

This module demonstrates a safer alternative to __del__ for running
cleanup logic when objects become unreachable.

Key ideas:
- weakref.finalize is NOT a method on the object
- it does not resurrect objects
- it does not depend on object attribute integrity
- it behaves well with cyclic garbage collection
- it avoids most shutdown-related hazards of __del__
"""

from __future__ import annotations
import weakref
import gc


# ----------------------------------------
# 1) WHY NOT __del__ (COMMENTARY ONLY)
# ----------------------------------------
# __del__ is problematic because:
# - it runs in object context (self may be partially destroyed)
# - it can resurrect objects
# - it depends on object graph integrity
# - execution order is not guaranteed
# - shutdown environment may be broken
#
# weakref.finalize avoids these issues by decoupling finalization logic
# from the object's lifetime and structure.


# ----------------------------------------
# 2) SIMPLE OBJECT
# ----------------------------------------

class Resource:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def __repr__(self) -> str:
        return f"Resource({self.name})"


# ----------------------------------------
# 3) BASIC FINALIZE DEMO
# ----------------------------------------

def finalize_demo() -> None:
    print("=== finalize_demo ===")

    res: Resource = Resource("R1")

    weakref.finalize(
        res,
        print,
        f"finalizing resource {res.name}"
    )

    print("created:", res)
    print("deleting reference")
    del res

    # force collection for demonstration
    gc.collect()
    print()


# ----------------------------------------
# 4) FINALIZE VS __del__ (KEY DIFFERENCES)
# ----------------------------------------
# - finalize callback does NOT receive the object
# - it cannot access object attributes unless explicitly captured
# - it runs at most once
# - resurrection is impossible
#
# The cleanup logic is treated as independent code, not as part of the object.


# ----------------------------------------
# 5) FINALIZE AND REFERENCE CYCLES
# ----------------------------------------

def finalize_cycle_demo() -> None:
    print("=== finalize_cycle_demo ===")

    class Node:
        def __init__(self, name: str) -> None:
            self.name: str = name
            self.other: Node | None = None

        def __repr__(self) -> str:
            return f"Node({self.name})"

    a: Node = Node("A")
    b: Node = Node("B")

    a.other = b
    b.other = a

    weakref.finalize(a, print, "finalizing A")
    weakref.finalize(b, print, "finalizing B")

    print("created cycle:", a, "<->", b)
    print("deleting external references")

    del a
    del b

    unreachable = gc.collect()
    print("gc.collect() found unreachable:", unreachable)
    print()


# ----------------------------------------
# 6) FINALIZE LIFETIME SEMANTICS
# ----------------------------------------
# - finalize is triggered when the referent becomes unreachable
# - the callback may run immediately (refcount) or later (GC)
# - finalize is NOT guaranteed to run at interpreter shutdown
# - but it has fewer failure modes than __del__


# ----------------------------------------
# 7) PRACTICAL RULES OF THUMB
# ----------------------------------------
# Use weakref.finalize when:
# - cleanup is optional or best-effort
# - object graph integrity is not required
# - you want to avoid resurrection
# - you do not control object lifetime precisely
#
# Prefer explicit cleanup (close(), context managers) when:
# - cleanup is logically required
# - resource management must be deterministic


# ----------------------------------------
# 8) QUICK RUN
# ----------------------------------------

if __name__ == "__main__":
    finalize_demo()
    finalize_cycle_demo()
