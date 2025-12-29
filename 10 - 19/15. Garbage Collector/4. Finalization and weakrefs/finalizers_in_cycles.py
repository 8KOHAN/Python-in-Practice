"""
Finalizers and reference cycles in CPython.

This module explains:
- why reference cycles + __del__ are problematic
- how the cyclic GC handles such objects
- what changed with PEP 442 (safe object finalization)
- why __del__ is still discouraged in cycles
"""

from __future__ import annotations
import gc


# ----------------------------------------
# 1) A SIMPLE CYCLE WITH __del__
# ----------------------------------------

class NodeWithDel:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.other: NodeWithDel | None = None

    def __del__(self) -> None:
        # This code is intentionally minimal and side-effect free.
        print(f"__del__ called for {self.name}")

    def __repr__(self) -> str:
        return f"NodeWithDel({self.name})"


def cycle_with_del_demo() -> None:
    print("=== cycle_with_del_demo ===")

    a: NodeWithDel = NodeWithDel("A")
    b: NodeWithDel = NodeWithDel("B")

    a.other = b
    b.other = a

    # Remove external references
    del a
    del b

    print("forcing gc.collect()")
    unreachable = gc.collect()

    print("gc.collect() found unreachable:", unreachable)
    print("gc.garbage:", gc.garbage)
    print()


# ----------------------------------------
# 2) WHAT THE GC SEES
# ----------------------------------------
# The cyclic GC detects unreachable *groups* of objects.
#
# Problem:
# - Objects define __del__
# - GC cannot determine a safe order to call finalizers
#
# Historically:
# - such objects were left uncollected
# - placed into gc.garbage
#
# This prevented unsafe finalization.


# ----------------------------------------
# 3) PEP 442 — SAFE OBJECT FINALIZATION
# ----------------------------------------
# PEP 442 (Python 3.4+) changed the rules:
#
# - Cycles with __del__ can now be collected
# - __del__ is called *after* breaking reference cycles
# - Objects are finalized in a safe, deterministic phase
#
# HOWEVER:
# - order between objects is still undefined
# - globals/modules may already be cleared
# - resurrection is still possible (and dangerous)
#
# Conclusion:
# PEP 442 made GC *less broken*, not __del__ safe.


def pep442_demo() -> None:
    print("=== pep442_demo ===")

    gc.set_debug(gc.DEBUG_SAVEALL)

    a: NodeWithDel = NodeWithDel("A")
    b: NodeWithDel = NodeWithDel("B")

    a.other = b
    b.other = a

    del a
    del b

    print("gc.garbage size:", len(gc.garbage))
    print("forcing gc.collect()")
    unreachable = gc.collect()

    print("gc.collect() found unreachable:", unreachable)
    print("gc.garbage size:", len(gc.garbage))

    # Cleanup
    gc.garbage.clear()
    gc.set_debug(0)

    print()


# ----------------------------------------
# 4) WHY __del__ IS STILL DISCOURAGED
# ----------------------------------------
# Even after PEP 442:
#
# - Finalization order is undefined
# - __del__ may run very late
# - __del__ may run during interpreter shutdown
# - Other objects may already be gone
#
# GC guarantees memory safety, NOT logical correctness.


# ----------------------------------------
# 5) SUMMARY
# ----------------------------------------
# - Cycles + __del__ are fundamentally hard
# - GC must break cycles before finalization
# - PEP 442 fixed crashes and leaks
# - __del__ remains a footgun
# - Prefer weakref.finalize() or context managers


# ----------------------------------------
# 6) QUICK RUN
# ----------------------------------------

if __name__ == "__main__":
    cycle_with_del_demo()
    pep442_demo()
