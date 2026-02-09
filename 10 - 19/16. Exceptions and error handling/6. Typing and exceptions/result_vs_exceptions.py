"""
Comparison of exceptions and Result-like patterns in typed Python code.

This file demonstrates how different error-handling approaches affect
readability, type signatures, control flow, and cognitive load.
"""

from __future__ import annotations

from typing import NamedTuple


# ----------------------------------------
# 1) EXCEPTIONS AS THE DEFAULT ERROR MECHANISM
# ----------------------------------------

def exceptions_as_default_demo() -> None:
    print("=== exceptions_as_default_demo ===")

    def parse_int(value: str) -> int:
        # This function assumes invalid input is exceptional.
        # The caller is expected to either ensure correctness
        # or handle the exception.
        return int(value)

    try:
        result = parse_int("123")
        print(f"Parsed value: {result}")
    except ValueError as exc:
        print(f"Caught ValueError: {exc}")

    print()


# ----------------------------------------
# 2) A SIMPLE RESULT TYPE (SUCCESS / ERROR)
# ----------------------------------------

class Result(NamedTuple):
    value: int | None
    error: str | None


def simple_result_type_demo() -> None:
    print("=== simple_result_type_demo ===")

    def parse_int(value: str) -> Result:
        try:
            return Result(value=int(value), error=None)
        except ValueError:
            return Result(value=None, error="invalid integer")

    result = parse_int("not-a-number")

    if result.error is not None:
        print(f"Error: {result.error}")
        print()
        return

    print(f"Parsed value: {result.value}")

    print()


# ----------------------------------------
# 3) HOW RESULT TYPES AFFECT TYPE SIGNATURES
# ----------------------------------------

def result_types_affect_signatures_demo() -> None:
    print("=== result_types_affect_signatures_demo ===")

    # With exceptions:
    #
    def parse_int(value: str) -> int:
        pass
    #
    # With Result:
    #
    def parse_int(value: str) -> Result:
        pass
    #
    # The second signature forces every caller to handle
    # both success and failure explicitly, even if failure
    # is truly exceptional.
    print()


# ----------------------------------------
# 4) ERROR PROPAGATION COST
# ----------------------------------------

def error_propagation_cost_demo() -> None:
    print("=== error_propagation_cost_demo ===")

    def parse_int_result(value: str) -> Result:
        try:
            return Result(value=int(value), error=None)
        except ValueError:
            return Result(value=None, error="invalid integer")

    def double_result(value: str) -> Result:
        result = parse_int_result(value)

        if result.error is not None:
            # Error propagation must be done manually.
            return result

        return Result(value=result.value * 2, error=None)

    result = double_result("abc")

    if result.error is not None:
        print(f"Error propagated: {result.error}")
    else:
        print(f"Result: {result.value}")

    print()


# ----------------------------------------
# 5) WHEN RESULT TYPES MAKE SENSE (THEORY-ONLY SECTION)
# ----------------------------------------
#
# Result-like patterns can be useful when:
#
# - failure is expected and common
# - error handling is part of normal control flow
# - you want to avoid try/except in hot paths
# - you are modeling external systems (IO, network, parsing user input)
#
# They are less useful when:
#
# - failure is truly exceptional
# - error propagation should be automatic
# - the happy path should remain uncluttered
# - readability matters more than exhaustiveness


# ----------------------------------------
# 6) PRACTICAL GUIDELINES
# ----------------------------------------
#
# Practical guidelines for choosing between exceptions and Result:
#
# 1) Use exceptions for exceptional situations.
# 2) Use Result types when errors are part of normal operation.
# 3) Do not mix both approaches randomly.
# 4) Prefer exceptions for internal APIs.
# 5) Prefer Result-like patterns at system boundaries.


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    exceptions_as_default_demo()
    simple_result_type_demo()
    result_types_affect_signatures_demo()
    error_propagation_cost_demo()
