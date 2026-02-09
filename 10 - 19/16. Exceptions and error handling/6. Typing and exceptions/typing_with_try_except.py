"""
Typing behavior when using try/except blocks.

This file demonstrates how exception handling affects type inference,
control flow, and readability, even when no exceptions are actually raised.
"""

from __future__ import annotations


# ----------------------------------------
# 1) BASIC TYPE NARROWING WITH try/except
# ----------------------------------------

def basic_type_narrowing_demo() -> None:
    print("=== basic_type_narrowing_demo ===")

    value: str | None = "123"

    # At this point, the type of `value` is `str | None`
    # Static type checkers cannot assume it is a string.
    try:
        # int() accepts str, bytes, or bytearray.
        # If `value` is None, a TypeError will be raised.
        result: int = int(value)
    except TypeError:
        # Inside this block we know that `value` was not a valid input
        # for int(). We handle the failure explicitly.
        print("value is None and cannot be converted to int")
        print()
        return

    # If we reached this point, conversion succeeded.
    # This means `value` must have been a valid string representation
    # of an integer.
    print(f"Converted value: {result}")

    print()


# ----------------------------------------
# 2) try/except DOES NOT NARROW TYPES AUTOMATICALLY
# ----------------------------------------

def try_except_does_not_narrow_types_demo() -> None:
    print("=== try_except_does_not_narrow_types_demo ===")

    value: str | None = None

    try:
        int(value)
    except TypeError:
        pass

    # Even after the try/except block, the type of `value`
    # is still `str | None`.
    #
    # The exception handler does NOT tell the type checker
    # that `value` is now safe to use as a string.
    #
    # Control flow guarantees and type guarantees are
    # two different things.
    if value is None:
        print("value is still None")
    else:
        print("value is a string")

    print()


# ----------------------------------------
# 3) WHY `except Exception` IS BAD FOR TYPING
# ----------------------------------------

def broad_exception_hurts_typing_demo() -> None:
    print("=== broad_exception_hurts_typing_demo ===")

    value: str = "42"

    try:
        result: int = int(value)
    except Exception:
        # Catching Exception hides too much information:
        # - TypeError
        # - ValueError
        # - unexpected runtime issues
        #
        # From a typing perspective, this block gives
        # no useful signal about what went wrong.
        print("Something went wrong")
        print()
        return

    # Because the except block is too broad,
    # static analyzers cannot reason precisely
    # about what `result` represents here.
    print(f"Result: {result}")

    print()


# ----------------------------------------
# 4) EXPLICIT EXCEPTIONS IMPROVE READABILITY AND TYPING
# ----------------------------------------

def explicit_exception_demo() -> None:
    print("=== explicit_exception_demo ===")

    value: str = "not-a-number"

    try:
        result: int = int(value)
    except ValueError:
        # ValueError explicitly documents the failure mode:
        # the string is not a valid integer representation.
        print("ValueError: invalid integer string")
        print()
        return

    print(f"Result: {result}")

    print()


# ----------------------------------------
# 5) TYPE CHECKERS CARE ABOUT CONTROL FLOW, NOT INTENT
# ----------------------------------------

def control_flow_vs_intent_demo() -> None:
    print("=== control_flow_vs_intent_demo ===")

    value: str | None = "10"

    # This check narrows the type for both runtime
    # and static analysis.
    if value is None:
        print("value is None")
        print()
        return

    # From here on, `value` is statically known to be `str`.
    try:
        result: int = int(value)
    except ValueError:
        print("Invalid integer format")
        print()
        return

    print(f"Result: {result}")

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_type_narrowing_demo()
    try_except_does_not_narrow_types_demo()
    broad_exception_hurts_typing_demo()
    explicit_exception_demo()
    control_flow_vs_intent_demo()
