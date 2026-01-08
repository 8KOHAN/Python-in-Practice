"""
Demonstration of runtime and state-related exceptions:
errors that indicate invalid program state or violated assumptions.
"""

from __future__ import annotations

from typing import Iterator


# ----------------------------------------
# 1) RUNTIME ERROR AS A SIGNAL
# ----------------------------------------

def runtime_error_demo() -> None:
    print("=== runtime_error_demo ===")

    # RuntimeError is a generic exception that signals:
    # - the program reached a state it cannot reasonably handle
    # - no more specific exception type applies
    #
    # It is often used as a "this should never happen" signal.

    try:
        raise RuntimeError("Unexpected runtime condition")
    except RuntimeError as exc:
        print(f"RuntimeError caught: {exc}")

    print()


# ----------------------------------------
# 2) NOT IMPLEMENTED ERROR
# ----------------------------------------

def not_implemented_error_demo() -> None:
    print("=== not_implemented_error_demo ===")

    # NotImplementedError indicates that:
    # - the code path is intentionally incomplete
    # - the function or method defines an interface or contract
    #
    # It is commonly used in:
    # - abstract base classes
    # - template methods
    # - extension points

    def feature_placeholder() -> None:
        raise NotImplementedError("Feature not implemented yet")

    try:
        feature_placeholder()
    except NotImplementedError as exc:
        print(f"NotImplementedError caught: {exc}")

    print()


# ----------------------------------------
# 3) RECURSION ERROR
# ----------------------------------------

def recursion_error_demo() -> None:
    print("=== recursion_error_demo ===")

    # RecursionError is raised when the maximum recursion depth
    # is exceeded.
    #
    # This protects the interpreter from stack overflow.
    #
    # It usually indicates:
    # - missing termination condition
    # - unintended recursion

    def infinite_recursion() -> None:
        infinite_recursion()

    try:
        infinite_recursion()
    except RecursionError as exc:
        print(f"RecursionError caught: {exc}")

    print()


# ----------------------------------------
# 4) ASSERTION ERROR
# ----------------------------------------

def assertion_error_demo() -> None:
    print("=== assertion_error_demo ===")

    # AssertionError is raised by the assert statement.
    #
    # Assertions express developer assumptions, not user errors.
    # They are intended for debugging and internal consistency checks.
    #
    # Important:
    # - Assertions can be globally disabled with the -O flag
    # - They must NOT be used for program logic or validation

    value: int = -1

    try:
        assert value >= 0, "Value must be non-negative"
    except AssertionError as exc:
        print(f"AssertionError caught: {exc}")

    print()


# ----------------------------------------
# 5) STOP ITERATION AS CONTROL FLOW
# ----------------------------------------

def stop_iteration_demo() -> None:
    print("=== stop_iteration_demo ===")

    # StopIteration is not an error in the usual sense.
    #
    # It signals the natural end of an iterator.
    #
    # It becomes an exception only when it leaks
    # outside the iteration protocol.

    iterator: Iterator[int] = iter([1, 2, 3])

    try:
        while True:
            value: int = next(iterator)
            print(value)
    except StopIteration:
        print("StopIteration caught: iterator exhausted")

    print()


# ----------------------------------------
# 6) INVALID STATE VS INVALID DATA
# ----------------------------------------
#
# Invalid state errors differ from data errors:
#
# - ValueError / TypeError:
#   the input data is wrong
#
# - RuntimeError / AssertionError:
#   the program state is wrong
#
# State errors usually indicate:
# - broken invariants
# - incorrect control flow
# - violated assumptions
#
# Invalid data -> input problem
# Invalid state -> program logic problem


# ----------------------------------------
# 7) RUNTIME AND STATE ERRORS — SUMMARY
# ----------------------------------------
#
# Key ideas:
#
# - Runtime and state errors indicate logic bugs
# - They are not caused by user input or environment
# - They often signal broken assumptions
#
# These exceptions are most valuable during development
# and should usually fail fast.
#
#Runtime errors reveal broken program invariant


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    runtime_error_demo()
    not_implemented_error_demo()
    recursion_error_demo()
    assertion_error_demo()
    stop_iteration_demo()
