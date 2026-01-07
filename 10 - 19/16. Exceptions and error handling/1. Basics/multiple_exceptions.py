"""
Demonstrates handling multiple exception types in a single try block.

The focus of this file is not syntax, but intent:
when multiple except clauses are justified,
how they should be ordered,
and when they should be avoided altogether.
"""

from __future__ import annotations


# ----------------------------------------
# 1) MULTIPLE EXCEPT CLAUSES
# ----------------------------------------
# A single try block may legitimately fail in different ways.
# In such cases, handling each failure explicitly improves clarity.
#
# The key rule:
#   - different exception types => different failure semantics
#   - different semantics => different handling


def multiple_except_clauses_demo() -> None:
    print("=== multiple_except_clauses_demo ===")

    data: dict[str, str] = {
        "count": "10",
    }

    try:
        raw_value: str = data["count"]
        value: int = int(raw_value)
    except KeyError:
        # The key is missing entirely.
        # This is a structural problem with the input data.
        print("Required key 'count' is missing")
    except ValueError:
        # The key exists, but its value is malformed.
        # This is a data quality problem.
        print("Value of 'count' is not a valid integer")
    else:
        # else executes only if no exception was raised.
        print(f"Parsed value: {value}")

    print()


# ----------------------------------------
# 2) EXCEPT ORDER MATTERS
# ----------------------------------------
# except clauses are checked from top to bottom.
# More specific exceptions MUST come before more general ones.
#
# Reversing the order may lead to unreachable code
# or unintentionally broad handling.


def except_order_demo() -> None:
    print("=== except_order_demo ===")

    values: list[str | None] = ["5", None, "invalid"]

    for value in values:
        try:
            # Two distinct failure modes:
            #   - TypeError: int(None)
            #   - ValueError: int("invalid")
            parsed: int = int(value)  # type: ignore[arg-type]
        except TypeError:
            print("TypeError: value is None")
        except ValueError:
            print("ValueError: value is not numeric")
        else:
            print(f"Parsed value: {parsed}")

    print()


# ----------------------------------------
# 3) GROUPING EXCEPTIONS (WHEN IT MAKES SENSE)
# ----------------------------------------
# Multiple exception types can be grouped into a single except clause.
#
# This is justified ONLY if:
#   - handling logic is identical
#   - semantic meaning of failures is equivalent


def grouped_exceptions_demo() -> None:
    print("=== grouped_exceptions_demo ===")

    inputs: list[str | None] = ["42", None, "oops"]

    for item in inputs:
        try:
            number: int = int(item)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            # Grouping is intentional here:
            # both failures mean "cannot convert to int"
            print(f"Skipping invalid input: {item}")
            continue

        print(f"Valid number: {number}")

    print()


# ----------------------------------------
# 4) WHAT MULTIPLE EXCEPT IS *NOT*
# ----------------------------------------
# This section is intentionally theoretical.
#
# Multiple except clauses should NOT be used to:
#   - mask unrelated failures
#   - approximate switch/case logic
#   - silently normalize broken program state
#
# If different exceptions require wildly different handling,
# reconsider whether they belong in the same try block at all.


# ----------------------------------------
# 5) QUICK-RUN
# ----------------------------------------


if __name__ == "__main__":
    multiple_except_clauses_demo()
    except_order_demo()
    grouped_exceptions_demo()
