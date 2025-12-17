"""
This module explains how *frames* and *closures* keep references alive
in CPython, often much longer than programmers expect.

Key ideas covered:
- what a frame object is
- how local variables live inside frames
- how closures capture variables via cell objects
- why inner functions can keep objects alive indefinitely
- how frames, closures, and reference counting interact
"""

from __future__ import annotations

import sys
from types import FrameType
from typing import Callable


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def header(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------------------
# 1. Frame objects and local variables
# ---------------------------------------------------------------------------
# Every function call in CPython creates a *frame object*.
#
# A frame contains:
#   - local variables (f_locals)
#   - globals (f_globals)
#   - builtins (f_builtins)
#   - a reference to the previous frame (f_back)
#
# As long as the frame object exists, *all local variables referenced by
# that frame remain alive*.

def frame_locals_demo() -> None:
    header("frame_locals_demo")

    def inner() -> None:
        x: list[int] = [1, 2, 3]
        frame: FrameType = sys._getframe()
        print("Inside function, refcount(x):", sys.getrefcount(x))
        print("Frame locals:", frame.f_locals)

    inner()
    # After inner() returns, its frame is destroyed,
    # and x becomes eligible for deallocation.


# ---------------------------------------------------------------------------
# 2. Frames can outlive the function call
# ---------------------------------------------------------------------------
# If a frame object is stored somewhere, it can keep all of its local
# variables alive even after the function has "returned".

def leaked_frame_demo() -> None:
    header("leaked_frame_demo")

    leaked_frame: FrameType | None = None

    def inner() -> None:
        nonlocal leaked_frame
        x: list[str] = ["I should be temporary"]
        leaked_frame = sys._getframe()
        print("Inside function, refcount(x):", sys.getrefcount(x))

    inner()

    # The function is finished, but the frame is still alive.
    assert leaked_frame is not None
    print("After function return, frame still alive")
    print("Leaked frame locals:", leaked_frame.f_locals)

    x = leaked_frame.f_locals["x"]
    print("Refcount(x) after function return:", sys.getrefcount(x))


# ---------------------------------------------------------------------------
# 3. Closures: capturing variables
# ---------------------------------------------------------------------------
# A closure happens when an inner function references variables from an
# enclosing scope.
#
# These variables are stored in *cell objects*, not in normal locals.
# The cell holds a strong reference to the captured object.

def closure_basic_demo() -> None:
    header("closure_basic_demo")

    def outer() -> Callable[[], None]:
        x = [1, 2, 3]

        def inner() -> None:
            print("Inner sees x:", x)

        print("In outer, refcount(x):", sys.getrefcount(x))
        return inner

    fn: Callable[[], None] = outer()
    # outer() has returned, but x is still alive!
    print("After outer returned, closure still exists")
    fn()


# ---------------------------------------------------------------------------
# 4. Closure cells keep objects alive
# ---------------------------------------------------------------------------
# Closure variables live in `__closure__` as cell objects.
# Each cell contains a strong reference to the captured value.

def closure_cell_demo() -> None:
    header("closure_cell_demo")

    def outer() -> Callable[[], None]:
        x: list[str] = ["captured object"]

        def inner() -> None:
            print(x)

        return inner

    fn: Callable[[], None] = outer()

    cells = fn.__closure__
    assert cells is not None

    cell = cells[0]
    print("Closure cell:", cell)
    print("Cell contents:", cell.cell_contents)
    print("Refcount(cell_contents):", sys.getrefcount(cell.cell_contents))


# ---------------------------------------------------------------------------
# 5. Closures can accidentally cause memory leaks
# ---------------------------------------------------------------------------
# Long-lived closures (callbacks, handlers, lambdas) can keep large object
# graphs alive if they capture objects unintentionally.

def closure_leak_demo() -> None:
    header("closure_leak_demo")

    callbacks: list[Callable[[], None]] = []

    def register_callback() -> None:
        large_object: list[int] = [i for i in range(100_000)]

        def callback() -> None:
            # large_object is captured here
            print(len(large_object))

        callbacks.append(callback)
        print("Inside register_callback, refcount(large_object):",
              sys.getrefcount(large_object))

    register_callback()

    # register_callback() returned, but large_object is still alive
    cb: Callable[[], None] = callbacks[0]
    cell = cb.__closure__[0]
    large_object = cell.cell_contents
    print("After function return, refcount(large_object):",
          sys.getrefcount(large_object))


# ---------------------------------------------------------------------------
# 6. Frames + closures together
# ---------------------------------------------------------------------------
# Frames and closures often interact:
#   - frames keep locals alive
#   - closures keep cells alive
#   - cells keep objects alive
#
# This combination is very powerful — and very dangerous in long-running
# programs.

def frame_and_closure_demo() -> None:
    header("frame_and_closure_demo")

    def outer() -> Callable[[], tuple[FrameType, list[str]]]:
        x: list[str] = ["frame + closure"]

        def inner() -> tuple[FrameType, list[str]]:
            # x is referenced here -> becomes a closure variable
            return sys._getframe(), x

        return inner

    fn = outer()
    frame, x_ref = fn()

    print("Frame locals:", frame.f_locals)
    print("x from closure:", x_ref)
    print("Refcount(x):", sys.getrefcount(x_ref))


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
# - Frames keep *all locals* alive
# - Closures keep *captured variables* alive via cell objects
# - Frames can outlive function calls
# - Closures can outlive both frames and functions
# - Together, they are a common source of accidental memory retention
#
# Always be careful with:
#   - long-lived closures
#   - callbacks
#   - lambdas capturing large objects
#   - storing frame objects
#   - storing exceptions / tracebacks


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    frame_locals_demo()
    leaked_frame_demo()
    closure_basic_demo()
    closure_cell_demo()
    closure_leak_demo()
    frame_and_closure_demo()
