# This module demonstrates common pitfalls, misconceptions, and surprising
# behaviors related to CPython's reference counting. These examples help clarify
# why refcount-based reasoning is sometimes unintuitive, incomplete, or misleading.
#
# Covered topics:
# - sys.getrefcount() always lies (temporaries)
# - reference spikes caused by function calls
# - refcount behavior in loops and comprehensions
# - refcount vs. GC: cycles that refcount cannot collect
# - refcount interference from caches and interning
# - refcounts distorted by error handling and exception frames
# - dangerous patterns: resurrecting objects in __del__
#
# All examples are CPython-specific.

from __future__ import annotations
import sys
import gc
from types import FrameType, TracebackType
from typing import Any


def header(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------------------
# 1. sys.getrefcount() always lies
# ---------------------------------------------------------------------------
# sys.getrefcount(obj) adds a *temporary* reference to obj when passing it
# into the function, so the reported value is always +1 higher than the real one.

def getrefcount_lies_demo() -> None:
    header("getrefcount_lies_demo")
    obj: object = object()
    print("Real refcount is 1, but sys.getrefcount reports:", sys.getrefcount(obj))


# ---------------------------------------------------------------------------
# 2. Reference spikes during function calls
# ---------------------------------------------------------------------------
# Passing an object into a function increases its reference count.
# The temporary argument binding inside the function creates a hidden reference.

def ref_spike_demo() -> None:
    header("ref_spike_demo")

    def f(x: Any) -> None:
        print("Inside f():", sys.getrefcount(x))

    x: list = []
    print("Before call:", sys.getrefcount(x))
    f(x)
    print("After call:", sys.getrefcount(x))


# ---------------------------------------------------------------------------
# 3. Loops and comprehensions create hidden references (detailed explanation)
# ---------------------------------------------------------------------------
# List comprehensions in CPython are not simple syntactic sugar for loops.
# They are implemented as hidden functions with their own stack frames,
# locals, cell variables, and temporary values pushed onto the evaluation
# stack. All of these can briefly or temporarily increase refcounts.
#
# Why this matters:
# -----------------
# A list comprehension such as:
#
#     [x for _ in range(10)]
#
# is compiled into a *separate internal function* that:
#   - captures `x` as a *free variable* (stored in a closure cell),
#   - executes LOAD_DEREF or LOAD_FAST on each iteration,
#   - allocates a frame object to run the comprehension,
#   - uses LIST_APPEND, which interacts with the evaluation stack.
#
# This entire structure can keep references to `x` alive longer than
# expected, even after the comprehension "finishes", because CPython keeps
# internal objects (cells, frames, iterators) alive until the function fully
# returns and all references are dropped.
#
# That is why code like this:
#
#     x = object()
#     _ = [x for _ in range(10)]
#
# can show `sys.getrefcount(x)` jump by 10 or more — even though the
# comprehension only *appears* to "touch" x 10 times. In reality, refcount
# rises because of:
#
#   1. The hidden listcomp function receiving `x` as a free variable (+1)
#   2. The function’s frame keeping references to locals (+1)
#   3. The closure cell storing `x` (+1)
#   4. LOAD_DEREF/LOAD_FAST creating temporary stack references (+10 peaks)
#   5. The iterator object sometimes holding temporary references
#
# Most temporary references *are released immediately*, but the closure cell
# and frame objects live long enough that the increased refcount appears in
# measurements right after the list comprehension.
#
# After the hidden frame is finally destroyed, refcount returns to normal.
#
# Loops vs comprehensions:
# ------------------------
# A simple for-loop does not create a hidden function, so it does not add
# these extra structural references. A loop like:
#
#     for i in range(5):
#         y = x
#
# only creates a single additional persistent reference (variable `y`),
# while LOAD_FAST creates transient +1/-1 refcount spikes that do not remain.
#
# Therefore:
#   - list comprehensions → may show large refcount jumps (hidden function)
#   - normal loops → only stable references matter (“y = x”), stack refs vanish
#
# Demonstration:
# ---------------------------------------------------------------------------

def loop_comprehension_pitfall_demo() -> None:
    header("loop_comprehension_pitfall_demo")

    x: object = object()
    print("Initial:", sys.getrefcount(x))

    # This comprehension creates a hidden function + frame + closure cell.
    _ = [x for _ in range(10)]
    print("After list comprehension:", sys.getrefcount(x))

    # A normal loop does not create a hidden function.
    y: object
    for i in range(5):
        y = x           # only 1 persistent reference (variable y itself)
    print("After loop:", sys.getrefcount(x))



# ---------------------------------------------------------------------------
# 4. Cycles cannot be freed by refcount alone
# ---------------------------------------------------------------------------
# Objects that reference each other but are unreachable from program roots
# have refcounts > 0 forever unless GC intervenes.

def cycle_pitfall_demo() -> None:
    header("cycle_pitfall_demo")

    class Node:
        def __init__(self, name: str):
            self.name = name
            self.other: Node | None = None
        def __repr__(self) -> str:
            return f"Node({self.name})"

    a: Node = Node("A")
    b: Node = Node("B")
    a.other = b
    b.other = a

    print("Refcounts: A:", sys.getrefcount(a), "B:", sys.getrefcount(b))

    del a
    del b
    # They are not deleted from memory because they still refer to each other, although they are not available to us.
    # We will talk about this in more detail in 15. Garbage Collector/3. gc cycles/

    print("Running gc.collect():", gc.collect())


# ---------------------------------------------------------------------------
# 5. Caches and interning distort refcounts
# ---------------------------------------------------------------------------
# Small integers, interned strings, empty tuples, and some other objects are
# immortal or reused by CPython. Their refcounts are meaningless for lifetime.

def caching_interning_demo() -> None:
    header("caching_interning_demo")

    print("Refcount of small int 1:", sys.getrefcount(1))
    print("Refcount of empty tuple:", sys.getrefcount(()))


# ---------------------------------------------------------------------------
# 6. Exception frames keep references alive (detailed explanation)
# ---------------------------------------------------------------------------
# When an exception is raised, CPython creates a traceback object (`PyTracebackObject`).
# A traceback contains:
#
#       tb.tb_frame   → the execution frame where the exception happened
#       tb.tb_next    → pointer to the next traceback in the chain
#
# A frame object contains:
#
#       f_locals      → dictionary of all local variables
#       f_globals     → module globals
#       f_builtins    → builtins
#       f_back        → the previous frame (caller)
#
# IMPORTANT CONSEQUENCE:
# ----------------------
# As long as a traceback object exists, its frames exist.
# As long as frames exist, *all local variables inside them also stay alive*.
#
# This means:
#
#   - A local variable from a function that already returned
#     may remain alive much longer if an exception was raised.
#
#   - Even if the programmer thinks a function has ended,
#     the garbage collector cannot free objects referenced by that frame.
#
#   - This is one of the most subtle sources of "unexpected leaks" in Python.
#
# Real-world example:
# -------------------
# Web frameworks or async systems that log exceptions but store traceback
# objects can accidentally keep huge object graphs alive:
#
#       - local caches
#       - large lists
#       - temporary buffers
#       - database connections
#
# All because the traceback → frame → locals chain keeps references alive.
#
# Why this happens:
# -----------------
# CPython cannot drop a traceback until all code that might inspect it finishes.
# So variables like `x` below stay alive until:
#
#       1. The exception is fully handled
#       2. The traceback object is destroyed
#       3. All references to the traceback are dropped
#
# Even referencing the exception object (`e`) in an `except` block
# keeps the traceback reachable!
#
# Recommended practice:
# ---------------------
# To avoid accidental retention of large objects:
#       - Use "except Exception as e:" only when necessary.
#       - Call "del e" once you're done with the exception.
#       - In long-running systems: call "del e; del tb; gc.collect()"
#       - Use "raise ... from None" to avoid long chains of __cause__.
#
# Demonstration:
# ---------------------------------------------------------------------------

def exception_frame_pitfall_demo() -> None:
    header("exception_frame_pitfall_demo")

    def broken():
        x: list[int] = [1, 2, 3]   # this variable survives longer than expected
        raise Exception("boom")

    try:
        broken()
    except Exception as e:
        tb: TracebackType | None = e.__traceback__
        print("Walking through traceback frames:")

        # Traverse the traceback chain to inspect frames and their locals.
        while tb is not None:
            frame: FrameType = tb.tb_frame
            print("Frame locals:", frame.f_locals)

            if "x" in frame.f_locals:
                print("FOUND x! refcount:", sys.getrefcount(frame.f_locals["x"]))

            tb = tb.tb_next



# ---------------------------------------------------------------------------
# 7. Resurrecting objects in __del__ (dangerous!)
# ---------------------------------------------------------------------------
# If __del__ stores 'self' somewhere, the object becomes alive again right
# when Python tries to delete it. This leads to extremely tricky lifetime bugs.

def resurrection_pitfall_demo() -> None:
    header("resurrection_pitfall_demo")

    zombies: list[Zombie] = []

    class Zombie:
        def __del__(self):
            zombies.append(self)   # resurrected — object lives again!

    z: Zombie = Zombie()
    print("Initial refcount:", sys.getrefcount(z))

    del z
    gc.collect()

    print("Zombies list:", zombies)
    if zombies:
        print("Resurrected object refcount:", sys.getrefcount(zombies[0]))


if __name__ == "__main__":
    getrefcount_lies_demo()
    ref_spike_demo()
    loop_comprehension_pitfall_demo()
    cycle_pitfall_demo()
    caching_interning_demo()
    exception_frame_pitfall_demo()
    resurrection_pitfall_demo()
