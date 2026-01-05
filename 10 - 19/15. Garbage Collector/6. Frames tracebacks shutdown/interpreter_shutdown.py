"""
Interpreter shutdown: object finalization pitfalls (CPython).

This module demonstrates how object destruction behaves during
Python interpreter shutdown and why __del__, weakref callbacks,
and GC are unreliable at exit time.

Key ideas:
- globals may already be cleared (set to None)
- module-level state is destroyed early
- active frames are gone, but finalizers run in degraded environment
- cyclic GC may be disabled
- finalization order is NOT guaranteed
"""

from __future__ import annotations

import gc
import weakref
import atexit


# ----------------------------------------
# 1) GLOBAL STATE DISAPPEARS DURING SHUTDOWN
# ----------------------------------------

# This global will be cleared during interpreter shutdown.
GLOBAL_RESOURCE: list[str] = ["alive"]


class UsesGlobalInDel:
    """
    Demonstrates that globals may already be None
    when __del__ is executed during shutdown.
    """

    def __del__(self) -> None:
        # During shutdown, module globals may be cleared.
        print("[UsesGlobalInDel.__del__] GLOBAL_RESOURCE =", GLOBAL_RESOURCE)

        # This may fail or behave unexpectedly.
        if GLOBAL_RESOURCE is not None:
            GLOBAL_RESOURCE.append("used in __del__")


def demo_globals_in_del() -> None:
    print("=== demo_globals_in_del ===")
    obj: UsesGlobalInDel = UsesGlobalInDel()
    print("object created; relying on __del__ at shutdown")
    print()


# ----------------------------------------
# 2) __del__ ORDER IS NOT GUARANTEED
# ----------------------------------------

class DependsOnOther:
    def __init__(self, other: DependsOnOther | None = None) -> None:
        self.other: DependsOnOther | None = other

    def __del__(self) -> None:
        print(
            "[DependsOnOther.__del__] other is:",
            self.other,
        )


def demo_del_order_is_unreliable() -> None:
    print("=== demo_del_order_is_unreliable ===")

    a: DependsOnOther = DependsOnOther()
    b: DependsOnOther = DependsOnOther(a)
    a.other = b

    print("objects created with circular dependency")
    print("finalization order at shutdown is undefined")
    print()


# ----------------------------------------
# 3) GC BEHAVIOR DURING SHUTDOWN
# ----------------------------------------

class CycleWithDel:
    def __init__(self) -> None:
        self.other: CycleWithDel | None = None

    def __del__(self) -> None:
        print("[CycleWithDel.__del__] called")


def demo_gc_during_shutdown() -> None:
    print("=== demo_gc_during_shutdown ===")

    a: CycleWithDel = CycleWithDel()
    b: CycleWithDel = CycleWithDel()
    a.other = b
    b.other = a

    print("cycle with __del__ created")
    print(
        "Such cycles may NOT be collected at shutdown, "
        "or __del__ may never run."
    )
    print()


# ----------------------------------------
# 4) weakref.finalize VS __del__
# ----------------------------------------

class WithFinalize:
    def __init__(self, name: str) -> None:
        self.name: str = name
        weakref.finalize(self, self._cleanup, name)

    @staticmethod
    def _cleanup(name: str) -> None:
        # finalize callbacks are safer than __del__,
        # but still not guaranteed during shutdown
        print(f"[weakref.finalize] cleaning up {name}")


def demo_weakref_finalize() -> None:
    print("=== demo_weakref_finalize ===")

    obj: WithFinalize = WithFinalize("resource-1")
    print("object with weakref.finalize created")
    print(
        "finalize is usually safer than __del__, "
        "but still may not run at shutdown"
    )
    print()


# ----------------------------------------
# 5) atexit: BEST-EFFORT, NOT A GUARANTEE
# ----------------------------------------

def atexit_handler() -> None:
    print("[atexit_handler] interpreter exiting")
    print("gc.isenabled():", gc.isenabled())


def demo_atexit() -> None:
    print("=== demo_atexit ===")

    atexit.register(atexit_handler)
    print("atexit handler registered")
    print(
        "atexit runs late in shutdown, "
        "but globals and modules may already be gone"
    )
    print()

    # atexit handlers run in a degraded interpreter state.
    # They must not rely on globals, modules, or object invariants.


# ----------------------------------------
# 6) WHAT YOU SHOULD *NOT* DO
# ----------------------------------------
#
# - Do NOT rely on __del__ for critical cleanup
# - Do NOT assume globals exist
# - Do NOT assume GC will collect cycles
# - Do NOT assume finalization order
#
# Interpreter shutdown is a degraded environment.


# ----------------------------------------
# 7) RECOMMENDED PATTERNS
# ----------------------------------------
#
# - Explicit close() methods
# - Context managers (with)
# - try/finally blocks
# - Deterministic lifetime management
#
# Treat shutdown cleanup as best-effort only.


# ----------------------------------------
# 8) QUICK-RUN WHEN EXECUTED DIRECTLY
# ----------------------------------------

if __name__ == "__main__":
    demo_globals_in_del()
    demo_del_order_is_unreliable()
    demo_gc_during_shutdown()
    demo_weakref_finalize()
    demo_atexit()
