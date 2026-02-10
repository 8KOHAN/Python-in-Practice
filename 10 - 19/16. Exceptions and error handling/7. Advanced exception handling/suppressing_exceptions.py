"""
Suppressing exceptions in Python: how it works, why it is dangerous,
and when it is actually acceptable.
"""

from __future__ import annotations

from contextlib import suppress


# ----------------------------------------
# 1) WHAT "SUPPRESSING AN EXCEPTION" MEANS
# ----------------------------------------
#
# Suppressing an exception means:
# - an exception is raised
# - but does NOT propagate to the caller
#
# This is fundamentally different from:
# - handling an exception
# - transforming an exception
# - logging and re-raising
#
# Suppression removes information from the error flow.
# This is why it is dangerous by default.


# ----------------------------------------
# 2) SUPPRESSION VIA try / except
# ----------------------------------------

def try_except_suppression_demo() -> None:
    print("=== try_except_suppression_demo ===")

    # The most common form of suppression.
    # The exception is caught and silently ignored.

    try:
        int("not-a-number")
    except ValueError:
        # Nothing is done here.
        # The program continues as if nothing happened.
        pass

    print("ValueError was raised but suppressed.")
    print()


# ----------------------------------------
# 3) WHY SILENT SUPPRESSION IS DANGEROUS
# ----------------------------------------

def silent_failure_demo() -> None:
    print("=== silent_failure_demo ===")

    values: list[str] = ["10", "20", "oops", "30"]
    parsed: list[int] = []

    for value in values:
        try:
            parsed.append(int(value))
        except ValueError:
            # The error is ignored.
            # We silently lose information about invalid input.
            pass

    print(f"Parsed values: {parsed}")
    print("Invalid data was silently dropped.")
    print()


# ----------------------------------------
# 4) contextlib.suppress
# ----------------------------------------

def contextlib_suppress_demo() -> None:
    print("=== contextlib_suppress_demo ===")

    # contextlib.suppress is explicit exception suppression.
    # It is equivalent to a try / except block that ignores errors.

    with suppress(ValueError):
        int("still-not-a-number")

    print("ValueError suppressed using contextlib.suppress.")
    print()


# ----------------------------------------
# 5) WHY contextlib.suppress IS STILL DANGEROUS
# ----------------------------------------

def suppress_hides_bugs_demo() -> None:
    print("=== suppress_hides_bugs_demo ===")

    # suppress does NOT distinguish between:
    # - expected errors
    # - programming mistakes
    #
    # If the wrong exception type is listed,
    # real bugs can disappear silently.

    with suppress(KeyError):
        data: dict[str, int] = {"a": 1}
        # This is a programming error.
        # But it will be silently ignored.
        _ = data["missing"]

    print("KeyError suppressed, bug hidden.")
    print()


# ----------------------------------------
# 6) WHEN SUPPRESSION IS ACTUALLY ACCEPTABLE
# ----------------------------------------

def acceptable_suppression_demo() -> None:
    print("=== acceptable_suppression_demo ===")

    # Suppression is acceptable when:
    # - failure is explicitly non-critical
    # - the absence of an operation is expected
    # - the code is best-effort by design

    cache: dict[str, int] = {}

    with suppress(KeyError):
        # Cache miss is not an error here.
        # It is part of normal control flow.
        value: int = cache["missing"]
        print(value)

    print("Cache miss ignored intentionally.")
    print()


# ----------------------------------------
# 7) SUPPRESSION VS EAFP
# ----------------------------------------

def suppression_vs_eafp_demo() -> None:
    print("=== suppression_vs_eafp_demo ===")

    # EAFP means:
    # - assume the operation works
    # - handle failure explicitly
    #
    # Suppression is NOT EAFP.
    # EAFP still reacts to failure.
    # Suppression pretends failure did not happen.

    try:
        int("bad")
    except ValueError as exc:
        print(f"Handled error: {exc}")

    print("Error handled, not suppressed.")
    print()


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    try_except_suppression_demo()
    silent_failure_demo()
    contextlib_suppress_demo()
    suppress_hides_bugs_demo()
    acceptable_suppression_demo()
    suppression_vs_eafp_demo()
