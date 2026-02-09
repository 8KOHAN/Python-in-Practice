"""
This file explains how exceptions interact with static typing in Python.
The focus is on practical consequences for type checkers and code design.
"""

from __future__ import annotations


# ----------------------------------------
# 1) EXCEPTIONS AND TYPE NARROWING
# ----------------------------------------

def type_narrowing_demo() -> None:
    print("=== type_narrowing_demo ===")

    value: str | None = "123"

    # Type checkers can narrow types after explicit checks.
    # This is predictable and easy to reason about.
    if value is None:
        print("Value is None")
    else:
        number: int = int(value)
        print("Parsed number:", number)

    # Now compare this with try/except-based flow control.
    value = None

    try:
        number: int = int(value)
        print("Parsed number:", number)
    except TypeError:
        # Type checkers usually cannot narrow types reliably here.
        print("Failed to parse value")

    print()


# ----------------------------------------
# 2) EXCEPTIONS VS EXPLICIT VALIDATION
# ----------------------------------------

def validation_vs_exception_demo() -> None:
    print("=== validation_vs_exception_demo ===")

    def parse_positive_int(value: str) -> int:
        # This function relies on exceptions to signal invalid input.
        # From a typing perspective, the return type is always int.
        # All invalid states are represented by raised exceptions.
        number: int = int(value)
        if number <= 0:
            raise ValueError("Value must be positive")
        return number

    try:
        result: int = parse_positive_int("-5")
        print("Result:", result)
    except ValueError as exc:
        print("Validation failed:", exc)

    # Using exceptions keeps the function signature clean.
    # No Optional[int], no sentinel values, no unions.

    print()


# ----------------------------------------
# 3) WHY except Exception BREAKS TYPE REASONING
# ----------------------------------------

def except_exception_typing_issue_demo() -> None:
    print("=== except_exception_typing_issue_demo ===")

    def unsafe_parse(value: str) -> int:
        try:
            return int(value)
        except Exception:
            # This hides whether the error is:
            # - ValueError
            # - TypeError
            # - or a programming bug
            return 0

    result: int = unsafe_parse("abc")
    print("Result:", result)

    # From a type checker perspective, this function looks safe.
    # From a semantic perspective, it is lying.
    # Errors are silently converted into valid-looking values.

    print()


# ----------------------------------------
# 4) EXCEPTIONS AS NON-RETURNING PATHS
# ----------------------------------------

def non_returning_paths_demo() -> None:
    print("=== non_returning_paths_demo ===")

    def fail(message: str) -> None:
        # This function never returns normally.
        # It always raises an exception.
        raise RuntimeError(message)

    def process(value: int) -> int:
        if value < 0:
            fail("Negative values are not allowed")
        return value * 2

    try:
        result: int = process(-1)
        print("Result:", result)
    except RuntimeError as exc:
        print("Processing failed:", exc)

    # Type checkers understand that code after fail() is unreachable.
    # This allows precise type reasoning without unions.

    print()


# ----------------------------------------
# 5) WHY RESULT TYPES ARE NOT ALWAYS BETTER
# ----------------------------------------

# In some ecosystems, errors are modeled explicitly:
# Result[T, E], Either, Ok/Error, etc.
#
# This approach makes error handling fully explicit
# and forces the caller to handle both success and failure cases.
#
# In Python, however, this often leads to:
# - more complex and verbose types
# - nested conditionals instead of linear code
# - weaker readability for the common (successful) path
#
# Exceptions integrate naturally with the language:
# - automatic stack unwinding
# - clear separation between success and failure paths
# - simpler and more honest function signatures
#
# A function that returns `int` and raises on failure
# communicates intent better than `int | Error` in most cases.
#
# This does NOT mean Result-like types are wrong.
# They can be useful:
# - at API boundaries
# - in highly functional codebases
# - when failures are part of normal business logic
#
# The key idea:
# exceptions are usually the more idiomatic choice in Python,
# especially when failures are exceptional rather than expected.



# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    type_narrowing_demo()
    validation_vs_exception_demo()
    except_exception_typing_issue_demo()
    non_returning_paths_demo()
