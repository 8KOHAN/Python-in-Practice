"""
Callable objects and context managers in Python.
Covers __call__, __enter__, and __exit__ behavior.
"""

from __future__ import annotations


# ----------------------------------------
# 1) CALLABLE OBJECTS (__call__)
# ----------------------------------------

# If object defines __call__, it can be used like a function:
#
# obj() -> obj.__call__()
#
# This allows objects to:
# - store state
# - behave like functions


def callable_demo() -> None:
    print("=== callable_demo ===")

    class Counter:
        def __init__(self) -> None:
            self.value = 0

        def __call__(self) -> int:
            self.value += 1
            return self.value

    counter = Counter()

    print(counter())
    print(counter())
    print(counter())

    print()


# ----------------------------------------
# 2) STATEFUL CALLABLE OBJECTS
# ----------------------------------------

# Objects with __call__ can encapsulate behavior + state.
# This is often used instead of closures.


def stateful_callable_demo() -> None:
    print("=== stateful_callable_demo ===")

    class Multiplier:
        def __init__(self, factor: int) -> None:
            self.factor = factor

        def __call__(self, value: int) -> int:
            return value * self.factor

    double = Multiplier(2)
    triple = Multiplier(3)

    print(double(10))
    print(triple(10))

    print()


# ----------------------------------------
# 3) CONTEXT MANAGER BASICS
# ----------------------------------------

# Context managers are used with "with" statement:
#
# with obj:
#     ...
#
# They define resource management behavior.


def context_manager_basic_demo() -> None:
    print("=== context_manager_basic_demo ===")

    class SimpleContext:
        def __enter__(self) -> str:
            print("Entering context")
            return "resource"

        def __exit__(self, exc_type, exc, tb) -> None:
            print("Exiting context")

    with SimpleContext() as resource:
        print(f"Using {resource}")

    print()


# ----------------------------------------
# 4) EXCEPTION HANDLING IN CONTEXT
# ----------------------------------------

# __exit__ receives exception info:
#
# exc_type, exc, traceback
#
# If __exit__ returns True -> exception is suppressed


def context_exception_demo() -> None:
    print("=== context_exception_demo ===")

    class SafeContext:
        def __enter__(self) -> SafeContext:
            print("Start")
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            print("Exception handling")
            if exc_type is None:
                return False

            if issubclass(exc_type, ValueError):
                return True  # suppress exception

            return False

    with SafeContext():
        print("Inside context")
        raise ValueError("Something went wrong")
        print("code below is skipped")

    print("Execution continues")

    print()


# ----------------------------------------
# 5) DESIGN GUIDELINES
# ----------------------------------------

# Callable objects:
# - good for stateful logic
# - should be predictable
#
# Context managers:
# - must guarantee cleanup
# - should not hide errors silently unless intentional


# ----------------------------------------
# 6) NON-GUARANTEES
# ----------------------------------------

# Python does NOT guarantee:
# - __exit__ will fix broken state
# - suppressed exceptions are safe
#
# Responsibility is on developer


def non_guarantees_demo() -> None:
    print("=== non_guarantees_demo ===")

    class BadContext:
        def __enter__(self) -> None:
            print("Enter")

        def __exit__(self, exc_type, exc, tb) -> bool:
            return True  # hides all errors

    with BadContext():
        raise RuntimeError("Hidden error")

    print("Error was silently ignored")

    print()


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    callable_demo()
    stateful_callable_demo()
    context_manager_basic_demo()
    context_exception_demo()
    non_guarantees_demo()
