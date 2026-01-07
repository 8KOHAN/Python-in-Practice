"""
Demonstration of numeric and arithmetic-related exceptions:
when mathematical operations fail and what different failures mean.
"""

from __future__ import annotations


# ----------------------------------------
# 1) ZERO DIVISION ERROR
# ----------------------------------------

def zero_division_error_demo() -> None:
    print("=== zero_division_error_demo ===")

    # ZeroDivisionError is raised when dividing by zero.
    #
    # This applies to:
    # - integer division
    # - floating-point division
    #
    # The type of the operands is correct.
    # The operation itself is defined.
    # The problem is a mathematically invalid value.

    numerator: int = 10
    denominator: int = 0

    try:
        result = numerator / denominator
        print(result)
    except ZeroDivisionError as exc:
        print(f"ZeroDivisionError caught: {exc}")

    print()


# ----------------------------------------
# 2) INTEGER MODULO BY ZERO
# ----------------------------------------

def modulo_by_zero_demo() -> None:
    print("=== modulo_by_zero_demo ===")

    # Modulo by zero is also a division-related operation
    # and therefore raises ZeroDivisionError.
    #
    # This is sometimes surprising to beginners,
    # but it is mathematically consistent.

    value: int = 42
    divisor: int = 0

    try:
        result = value % divisor
        print(result)
    except ZeroDivisionError as exc:
        print(f"ZeroDivisionError caught: {exc}")

    print()


# ----------------------------------------
# 3) OVERFLOW ERROR
# ----------------------------------------

def overflow_error_demo() -> None:
    print("=== overflow_error_demo ===")

    # OverflowError is raised when a numerical result
    # is too large to be represented.
    #
    # Important Python-specific detail:
    # - Python integers have arbitrary precision
    # - Therefore, OverflowError is rare with ints
    #
    # It is more commonly encountered with:
    # - float operations
    # - low-level numeric libraries
    # - explicit size-limited contexts

    try:
        value = 1e308
        result = value ** 5
        print(result)
    except OverflowError as exc:
        print(f"OverflowError caught: {exc}")

    print()


# ----------------------------------------
# 4) FLOATING POINT ERROR (WHY IT IS RARE)
# ----------------------------------------
#
# FloatingPointError exists, but is almost never raised
# in normal Python code.
#
# Reason:
# - IEEE 754 floating-point behavior
# - operations usually result in:
#   * inf
#   * -inf
#   * nan
#
# Instead of raising exceptions.
#
# FloatingPointError can appear only if:
# - special floating-point traps are explicitly enabled
#
# This is uncommon in typical Python applications.

#FloatingPointError is defined, but rarely encountered in practice


# ----------------------------------------
# 5) ARITHMETIC ERROR BASE CLASS
# ----------------------------------------

def arithmetic_error_hierarchy_demo() -> None:
    print("=== arithmetic_error_hierarchy_demo ===")

    # ArithmeticError is the base class for:
    # - ZeroDivisionError
    # - OverflowError
    # - FloatingPointError
    #
    # Catching ArithmeticError allows handling
    # multiple arithmetic failures uniformly.

    try:
        result = 1 / 0
        print(result)
    except ArithmeticError as exc:
        print(f"ArithmeticError caught: {type(exc).__name__}: {exc}")

    print()


# ----------------------------------------
# 6) NUMERIC ERRORS VS TYPE AND VALUE ERRORS
# ----------------------------------------

def numeric_error_comparison_demo() -> None:
    print("=== numeric_error_comparison_demo ===")

    # Numeric and arithmetic errors are distinct from:
    # - TypeError (wrong operand types)
    # - ValueError (invalid value semantics)
    #
    # Here, the operands are numeric and valid,
    # but the operation itself violates mathematical rules.

    examples: list[tuple[str, BaseException]] = [
        ("1 / 0", ZeroDivisionError()),
        ("1 + '2'", TypeError()),
        ("int('abc')", ValueError()),
    ]

    for expression, error in examples:
        print(f"{expression} -> {type(error).__name__}")

    print()


# ----------------------------------------
# 7) NUMERIC AND ARITHMETIC ERRORS — SUMMARY
# ----------------------------------------

# Key ideas:
#
# - Numeric errors are about mathematical impossibility
# - Types are usually correct
# - Values may be valid in isolation
# - The failure happens at the operation level
#
# These errors signal logic bugs,
# invalid assumptions,
# or missing edge-case handling.
#
# ZeroDivisionError, OverflowError, and FloatingPointError
# all indicate mathematical operation failures


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    zero_division_error_demo()
    modulo_by_zero_demo()
    overflow_error_demo()
    arithmetic_error_hierarchy_demo()
    numeric_error_comparison_demo()
