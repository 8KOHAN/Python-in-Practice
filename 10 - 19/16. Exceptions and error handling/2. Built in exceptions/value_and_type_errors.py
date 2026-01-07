"""
Demonstration of ValueError and TypeError:
when they occur, why they exist, and how to handle them correctly.
"""

from __future__ import annotations


# ----------------------------------------
# 1) ValueError BASICS
# ----------------------------------------

def value_error_basic_demo() -> None:
    print("=== value_error_basic_demo ===")

    # ValueError is raised when a value has the correct type,
    # but an invalid or unacceptable value.
    #
    # Important:
    # - The type of the object is correct
    # - The semantic meaning of the value is wrong

    raw_value: str = "not_a_number"

    try:
        number: int = int(raw_value)
        print(f"Parsed number: {number}")
    except ValueError as exc:
        # We catch ValueError explicitly.
        # Catching a more general exception here would hide intent.
        print(f"ValueError caught: {exc}")

    print()


# ----------------------------------------
# 2) ValueError VS PRE-CHECKS
# ----------------------------------------

def value_error_vs_precheck_demo() -> None:
    print("=== value_error_vs_precheck_demo ===")

    # A common beginner instinct is to "pre-check" values.
    # For example: checking whether a string contains only digits.
    #
    # This approach is often fragile and incomplete.
    # The EAFP principle prefers trying the operation
    # and handling the exception if it fails.

    raw_value: str = "-42"

    try:
        number: int = int(raw_value)
        print(f"Parsed number: {number}")
    except ValueError:
        print("Invalid integer representation")

    print()


# ----------------------------------------
# 3) TypeError BASICS
# ----------------------------------------

def type_error_basic_demo() -> None:
    print("=== type_error_basic_demo ===")

    # TypeError is raised when an operation is applied
    # to an object of an inappropriate type.
    #
    # Unlike ValueError, here the *type itself* is the problem.

    value: int = 10

    try:
        # This operation is invalid:
        # you cannot add an integer and a string.
        result = value + "5"  # type: ignore[operator]
        print(result)
    except TypeError as exc:
        print(f"TypeError caught: {exc}")

    print()


# ----------------------------------------
# 4) TypeError FROM WRONG CALL SIGNATURES
# ----------------------------------------

def type_error_call_signature_demo() -> None:
    print("=== type_error_call_signature_demo ===")

    def add(a: int, b: int) -> int:
        return a + b

    try:
        # Passing too many arguments triggers TypeError.
        result = add(1, 2, 3)  # type: ignore[call-arg]
        print(result)
    except TypeError as exc:
        print(f"TypeError caught: {exc}")

    print()


# ----------------------------------------
# 5) ValueError VS TypeError — SUMMARY
# ----------------------------------------

def value_vs_type_error_summary_demo() -> None:
    print("=== value_vs_type_error_summary_demo ===")

    # Rule of thumb:
    #
    # TypeError:
    # - The operation itself is invalid for the given type
    #
    # ValueError:
    # - The operation is valid for the type
    # - The specific value is unacceptable
    #
    # This distinction is important when designing APIs
    # and especially important for custom exceptions.

    examples: list[tuple[str, Exception]] = [
        ("int('abc')", ValueError("invalid literal for int()")),
        ("1 + '2'", TypeError("unsupported operand type(s)")),
    ]

    for expression, error in examples:
        print(f"{expression} -> {error.__class__.__name__}")

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    value_error_basic_demo()
    value_error_vs_precheck_demo()
    type_error_basic_demo()
    type_error_call_signature_demo()
    value_vs_type_error_summary_demo()
