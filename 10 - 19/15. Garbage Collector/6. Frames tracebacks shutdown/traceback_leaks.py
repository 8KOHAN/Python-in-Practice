"""
Traceback objects, frames, and memory leaks in CPython.

This module explains:
- what traceback objects are
- how exceptions keep references to frames
- why tracebacks can accidentally cause memory leaks
- how `except Exception as e` differs from bare `except`
- how to explicitly break reference chains
"""

from __future__ import annotations

from typing import Any
import sys
import gc
import traceback


# ----------------------------------------
# 1) WHAT IS A TRACEBACK OBJECT?
# ----------------------------------------
#
# In CPython, when an exception occurs, a traceback object is created.
# The traceback contains a linked list of frames:
#
#   traceback -> frame -> locals -> objects
#
# This means:
# - keeping a traceback alive keeps the entire stack alive
# - locals() inside frames may reference large object graphs
#
# Traceback objects are *normal Python objects* and participate in GC.


# ----------------------------------------
# 2) A LARGE OBJECT FOR DEMONSTRATION
# ----------------------------------------

class BigObject:
    def __init__(self, size: int) -> None:
        self.data: list[int] = [i for i in range(size)]

    def __repr__(self) -> str:
        return f"<BigObject size={len(self.data)}>"


# ----------------------------------------
# 3) LEAK VIA "except Exception as e"
# ----------------------------------------

def leak_via_exception_binding() -> None:
    print("=== leak_via_exception_binding ===")

    try:
        obj: BigObject = BigObject(1_000_000)
        raise RuntimeError("boom")
    except Exception as e:
        # IMPORTANT:
        # 'e' keeps a reference to the exception object
        # exception.__traceback__ keeps frames alive
        print("caught exception:", e)

        tb = e.__traceback__
        print("traceback object:", tb)
        print("traceback refcount:", sys.getrefcount(tb))

    # At this point:
    # - obj is still reachable through:
    #   e -> __traceback__ -> frame -> locals -> obj
    #
    # Even though obj is out of scope textually, it is still alive.
    print("GC collect:", gc.collect())
    print()


# ----------------------------------------
# 4) VERIFY THAT OBJECT IS STILL ALIVE
# ----------------------------------------

def verify_leak() -> None:
    print("=== verify_leak ===")

    objects: list[Any] = gc.get_objects()
    big_objects: list[BigObject] = [o for o in objects if isinstance(o, BigObject)]

    print("BigObject instances still alive:", len(big_objects))
    if big_objects:
        print("example:", big_objects[0])
    print()


# ----------------------------------------
# 5) FIX 1: DEL THE EXCEPTION VARIABLE
# ----------------------------------------

def fix_by_deleting_exception() -> None:
    print("=== fix_by_deleting_exception ===")

    try:
        obj = BigObject(1_000_000)
        raise ValueError("boom")
    except Exception as e:
        print("caught:", e)
        del e  # BREAK THE REFERENCE CHAIN

    print("GC collect:", gc.collect())
    print()


# ----------------------------------------
# 6) FIX 2: CATCH EXCEPTION WITHOUT BINDING
# ----------------------------------------

def fix_by_bare_except() -> None:
    print("=== fix_by_bare_except ===")

    try:
        obj = BigObject(1_000_000)
        raise KeyError("boom")
    except Exception:
        # Exception object is intentionally NOT bound
        # to avoid keeping traceback alive
        pass

    print("GC collect:", gc.collect())
    print()


# ----------------------------------------
# 7) LIMITATION: CLEARING TRACEBACK IS NOT ENOUGH
# ----------------------------------------
#
# IMPORTANT:
# Clearing traceback frames does NOT free objects referenced by the
# *currently executing frame*. Local variables of an active frame
# remain alive until the frame exits.
#
# In this example, `obj` is still referenced by the active frame,
# so clearing the traceback has no effect on its lifetime.

def clearing_traceback_is_not_enough() -> None:
    print("=== clearing_traceback_is_not_enough ===")

    try:
        obj: BigObject = BigObject(1_000_000)
        raise RuntimeError("boom")
    except Exception as e:
        tb = e.__traceback__
        print("traceback before clear:", tb)

        # This removes references held *by the traceback object*,
        # but the active frame still holds `obj` in its locals.
        traceback.clear_frames(tb)

        # Break the link from the exception to the traceback,
        # but the frame itself is still alive.
        e.__traceback__ = None

    # GC cannot collect `obj` here because the frame has not exited yet.
    print("GC collect:", gc.collect())
    print()


# ----------------------------------------
# 8) FIX: CLEAR TRACEBACK AFTER FRAME EXIT
# ----------------------------------------
#
# Here we ensure that the frame holding `obj` has already finished
# execution before clearing the traceback. This allows the object
# graph to become unreachable.

def fix_clear_traceback_after_frame_exit() -> None:
    print("=== fix_clear_traceback_after_frame_exit ===")

    def inner():
        try:
            obj = BigObject(1_000_000)
            raise RuntimeError("boom")
        except Exception as e:
            # Returning the exception keeps it alive,
            # but the frame (and its locals) will be destroyed
            # once this function returns.
            return e

    exc = inner()

    tb = exc.__traceback__

    # Now the frame referenced by the traceback is no longer active,
    # so clearing its frames actually breaks the last strong references.
    traceback.clear_frames(tb)
    exc.__traceback__ = None

    print("GC collect:", gc.collect())
    print()


# ----------------------------------------
# 9) WHY THIS HAPPENS (SUMMARY)
# ----------------------------------------
#
# - traceback objects reference frames
# - frames reference locals
# - locals reference arbitrary objects
#
# This is NOT a bug — it's a consequence of Python's introspection model.
#
# CPython does NOT automatically clear tracebacks because:
# - debuggers need them
# - interactive environments rely on them
# - sys.last_traceback exists for a reason


# ----------------------------------------
# 10) PRACTICAL RULES
# ----------------------------------------
#
# 1) Avoid long-lived exception objects
# 2) Prefer bare `except` if exception object is unused
# 3) Explicitly `del e` in long-running loops
# 4) Be careful with logging systems that store exceptions
# 5) Use tracemalloc / gc.get_referrers when debugging leaks


# ----------------------------------------
# 11) QUICK RUN
# ----------------------------------------

if __name__ == "__main__":
    gc.collect()

    leak_via_exception_binding()
    verify_leak()

    fix_by_deleting_exception()
    verify_leak()

    fix_by_bare_except()
    verify_leak()

    clearing_traceback_is_not_enough()
    verify_leak()

    fix_clear_traceback_after_frame_exit()
    verify_leak()
