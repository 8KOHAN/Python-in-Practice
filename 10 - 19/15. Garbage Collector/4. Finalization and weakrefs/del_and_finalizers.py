"""
Finalization in CPython: __del__ (destructor semantics).

IMPORTANT:
This file intentionally avoids demonstrating unsafe patterns
(resurrection, global state access, reliance on shutdown order).
Those cases are described in comments instead.
"""

from __future__ import annotations

import sys
import gc


# ----------------------------------------
# 1) BASIC FINALIZER (SAFE DEMO)
# ----------------------------------------

class WithDel:
    def __init__(self, name: str) -> None:
        self.name = name

    def __del__(self) -> None:
        # This is safe ONLY for demonstration.
        # Do not rely on other objects, modules, or globals here.
        print(f"__del__ called for {self.name}")

    def __repr__(self) -> str:
        return f"WithDel({self.name})"


def basic_del_demo() -> None:
    print("=== basic_del_demo ===")

    obj: WithDel = WithDel("A")
    print("created:", obj)
    print()

    # In CPython, when this function returns,
    # the local reference is dropped and __del__
    # is typically called immediately.


# ----------------------------------------
# 2) REFCOUNT-DRIVEN FINALIZATION (CPython)
# ----------------------------------------

def refcount_del_demo() -> None:
    print("=== refcount_del_demo ===")

    obj: WithDel = WithDel("B")
    alias: WithDel = obj

    print("refcount:", sys.getrefcount(obj))

    del alias
    print("after del alias -> refcount:", sys.getrefcount(obj))
    print()

    # Dropping the last strong reference.
    del obj

    # In CPython:
    # - refcount reaches zero
    # - __del__ is invoked immediately
    #
    # NOTE:
    # This behavior is an implementation detail,
    # not a Python language guarantee.


# ----------------------------------------
# 3) GC IS NOT RESPONSIBLE FOR __del__
# ----------------------------------------

def gc_vs_refcount_demo() -> None:
    print("=== gc_vs_refcount_demo ===")

    class NoCycle:
        def __del__(self):
            print("__del__ NoCycle")

    obj: NoCycle = NoCycle()
    del obj

    print("forcing gc.collect()")
    print()
    gc.collect()

    # __del__ has already run before gc.collect().
    # The cyclic GC does NOT trigger __del__.
    # It only finds unreachable object graphs.


# ----------------------------------------
# 4) IMPORTANT NON-GUARANTEES (COMMENTARY)
# ----------------------------------------
# The following behaviors are NOT demonstrated with code
# to avoid unsafe or misleading examples:
#
# 1) __del__ may NEVER run:
#    - at interpreter shutdown
#    - if objects participate in reference cycles
#    - if the program exits abruptly
#
# 2) Finalization order is undefined:
#    - globals may already be cleared
#    - modules may be partially destroyed
#
# 3) __del__ can resurrect objects:
#    - this is legal but dangerous
#    - resurrected objects are finalized only once
#
# 4) Objects with __del__ in cycles:
#    - are handled specially by the GC
#    - can end up in gc.garbage
#
# These cases are covered conceptually here
# and demonstrated carefully in the next module.


# ----------------------------------------
# 5) SUMMARY
# ----------------------------------------
# - __del__ is tied to refcount reaching zero in CPython
# - __del__ is NOT reliable for resource management
# - GC does not call __del__
# - Prefer context managers and weakref.finalize()


# ----------------------------------------
# 6) QUICK RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_del_demo()
    refcount_del_demo()
    gc_vs_refcount_demo()
