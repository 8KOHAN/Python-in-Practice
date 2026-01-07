"""
Demonstrates basic try/except mechanics in a disciplined, production-oriented style.

This file intentionally avoids trivial examples and focuses on how try/except
should be structured, commented, and reasoned about in real code.
"""

from __future__ import annotations


# ----------------------------------------
# 1) BASIC TRY / EXCEPT SHAPE
# ----------------------------------------
# This section demonstrates the minimal, canonical structure of try/except.
# The goal is not to show "how exceptions work" (this is assumed knowledge),
# but how to *structure* the code so that:
#   - the try block is as small as possible
#   - the except block is explicit and intentional
#   - no unrelated logic is mixed in


def basic_try_except_demo() -> None:
    print("=== basic_try_except_demo ===")

    raw_value: str = "123"

    # The try block should contain ONLY the operation(s)
    # that are expected to potentially fail.
    #
    # A common beginner mistake is to put too much code into try,
    # which hides the real source of errors.
    try:
        parsed_value: int = int(raw_value)
    except ValueError:
        # At this level, we intentionally keep handling minimal.
        # Swallowing exceptions silently is almost always a bad idea,
        # but printing is acceptable for demonstration purposes.
        print("Failed to parse integer")
        print()
        return

    # Code that depends on the success of try goes AFTER it,
    # not inside the try block.
    print(f"Parsed value: {parsed_value}")
    print()


# ----------------------------------------
# 2) WHY TRY BLOCKS SHOULD BE SMALL
# ----------------------------------------
# This section explains, via code, why "wide" try blocks are dangerous.
# The key idea:
#   - try does NOT document intent
#   - except does NOT know *where* the exception came from
# Therefore, scope matters.


def narrow_try_block_demo() -> None:
    print("=== narrow_try_block_demo ===")

    values: list[str] = ["10", "20", "not_a_number", "40"]

    for value in values:
        try:
            # Only the conversion is inside try.
            # If something else breaks later, we WANT it to crash.
            number: int = int(value)
        except ValueError:
            print(f"Skipping invalid value: {value}")
            continue

        # This code is guaranteed to work if we reached here.
        # Mixing it into try would make debugging harder.
        doubled: int = number * 2
        print(f"{number} -> {doubled}")

    print()


# ----------------------------------------
# 3) MULTIPLE OPERATIONS VS MULTIPLE FAILURES
# ----------------------------------------
# This section highlights a subtle but important rule:
#   If multiple operations can fail for different reasons,
#   they should usually NOT live in the same try block.
#
# This is a design rule, not a syntax rule.


def multiple_failure_sources_demo() -> None:
    print("=== multiple_failure_sources_demo ===")

    data: dict[str, str] = {
        "count": "5",
        # "count" key might be missing
        # value might be non-numeric
    }

    # First failure domain: dictionary access
    try:
        raw_count: str = data["count"]
    except KeyError:
        print("Missing 'count' key in data")
        print()
        return

    # Second failure domain: type conversion
    try:
        count: int = int(raw_count)
    except ValueError:
        print("Value of 'count' is not a valid integer")
        print()
        return

    print(f"Parsed count: {count}")
    print()


# ----------------------------------------
# 4) WHAT TRY / EXCEPT IS *NOT*
# ----------------------------------------
# This section is intentionally theoretical.
#
# try/except is often misunderstood and misused as a general-purpose
# control-flow tool. This is incorrect.
#
# try/except:
#   - is NOT a replacement for if/else branching
#   - is NOT a data validation mechanism
#   - is NOT a way to "probe" program state
#
# Using exceptions for normal control flow makes code harder to read,
# harder to reason about, and harder to maintain.
#
# These topics will be revisited later in the context of EAFP vs LBYL.
# At this point, it is enough to explicitly state these non-goals
# without demonstrating them in code.


# ----------------------------------------
# 5) QUICK-RUN
# ----------------------------------------


if __name__ == "__main__":
    basic_try_except_demo()
    narrow_try_block_demo()
    multiple_failure_sources_demo()
