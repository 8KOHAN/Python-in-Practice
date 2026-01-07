"""
Demonstrates the correct and intentional use of else and finally
in try/except blocks.

This file focuses on semantics and control-flow guarantees,
not on syntax.
"""

from __future__ import annotations


# ----------------------------------------
# 1) TRY / EXCEPT / ELSE
# ----------------------------------------
# The else block executes ONLY if:
#   - no exception was raised in try
#
# Its purpose is often misunderstood.
# else is NOT "optional sugar" — it is a structural tool
# that helps separate:
#   - code that may fail
#   - code that must run only on success

def try_except_else_demo() -> None:
    print("=== try_except_else_demo ===")

    raw_values: list[str] = ["10", "invalid", "20"]

    for raw in raw_values:
        try:
            value: int = int(raw)
        except ValueError:
            print(f"Failed to parse value: {raw}")
        else:
            # Code placed here is guaranteed to run ONLY
            # if the try block succeeded completely.
            #
            # This avoids accidental coupling between
            # error-prone code and success-only logic.
            doubled: int = value * 2
            print(f"{value} -> {doubled}")

    print()


# ----------------------------------------
# 2) WHY ELSE IS BETTER THAN PUTTING CODE IN TRY
# ----------------------------------------
# A common anti-pattern is putting too much logic into try.
# This makes it unclear which operation actually failed.
#
# else allows us to keep try blocks minimal and precise.

def else_vs_wide_try_demo() -> None:
    print("=== else_vs_wide_try_demo ===")

    raw: str = "5"

    try:
        value: int = int(raw)
    except ValueError:
        print("Parsing failed")
    else:
        # If this code were inside try and failed,
        # the except block would incorrectly handle it.
        #
        # Using else prevents such accidental masking.
        result: int = value + 100
        print(f"Result: {result}")

    print()


# ----------------------------------------
# 3) FINALLY: WHAT IT GUARANTEES
# ----------------------------------------
# finally executes:
#   - after try
#   - after except
#   - after else
#   - even if an exception is re-raised
#
# Its role is NOT business logic.
# Its role is cleanup.

def finally_cleanup_demo() -> None:
    print("=== finally_cleanup_demo ===")

    resource_acquired: bool = False

    try:
        resource_acquired = True
        print("Resource acquired")
        raise RuntimeError("Simulated failure")
    except RuntimeError:
        print("Handling runtime error")
    finally:
        # finally must be safe, simple, and predictable.
        #
        # It should NOT:
        #   - raise new exceptions
        #   - change program state in complex ways
        #   - contain logic that can fail
        if resource_acquired:
            print("Resource released")

    print()


# ----------------------------------------
# 4) WHAT FINALLY IS *NOT*
# ----------------------------------------
# This section is intentionally theoretical.
#
# finally should NOT be used for:
#   - normal control flow
#   - error recovery logic
#   - conditional branching
#
# Code inside finally is executed unconditionally.
# This makes it a poor place for anything
# that depends on program state or success.


# ----------------------------------------
# 5) ELSE + FINALLY TOGETHER
# ----------------------------------------
# else and finally serve different purposes:
#   - else: success-only logic
#   - finally: unconditional cleanup
#
# Using them together makes intent explicit.

def else_and_finally_combined_demo() -> None:
    print("=== else_and_finally_combined_demo ===")

    raw: str = "7"

    try:
        value: int = int(raw)
    except ValueError:
        print("Conversion failed")
    else:
        print(f"Parsed value: {value}")
    finally:
        # This will always execute, regardless of outcome.
        print("End of processing block")

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    try_except_else_demo()
    else_vs_wide_try_demo()
    finally_cleanup_demo()
    else_and_finally_combined_demo()
