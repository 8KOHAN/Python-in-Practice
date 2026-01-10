"""
Re-raising exceptions in Python.

This file demonstrates when and why exceptions should be re-raised,
and how re-raising differs from swallowing or transforming errors.
"""

from __future__ import annotations


# ----------------------------------------
# 1) SIMPLE RE-RAISE (DO NOT SWALLOW ERRORS)
# ----------------------------------------

def simple_reraise_demo() -> None:
    print("=== simple_reraise_demo ===")

    # A very common real-world situation:
    # - we need to log or observe an error
    # - but we are NOT responsible for handling it
    #
    # In such cases, the exception must be re-raised.

    def load_config(path: str) -> str:
        try:
            with open(path) as file:
                return file.read()
        except FileNotFoundError:
            # We do some local work (logging, metrics, debugging)
            print("Config file not found, cannot continue")
            # And then re-raise the same exception
            raise

    try:
        load_config("missing.conf")
    except FileNotFoundError as exc:
        print(f"Caught exception at top level: {exc}")

    print()


# ----------------------------------------
# 2) WHY SILENTLY SWALLOWING IS A BUG
# ----------------------------------------

def swallowing_exception_demo() -> None:
    print("=== swallowing_exception_demo ===")

    # This function demonstrates a bug, not a pattern.
    # It exists purely as a warning example.

    def read_number(path: str) -> int:
        try:
            with open(path) as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            # Swallowing the exception hides the real problem.
            # The caller cannot distinguish:
            # - missing file
            # - invalid content
            # - real zero value
            return 0

    result = read_number("missing.txt")
    print(f"Result after swallowing exception: {result}")

    print()


# ----------------------------------------
# 3) RE-RAISE AFTER PARTIAL HANDLING
# ----------------------------------------

def reraise_after_partial_handling_demo() -> None:
    print("=== reraise_after_partial_handling_demo ===")

    # Sometimes we handle part of the problem locally,
    # but still cannot recover fully.
    #
    # Re-raising preserves the original error semantics.

    def parse_user_age(value: str) -> int:
        try:
            age = int(value)
        except ValueError:
            print("Failed to parse user age")
            raise

        if age < 0:
            raise ValueError("Age must be non-negative")

        return age

    try:
        parse_user_age("not-a-number")
    except ValueError as exc:
        print(f"Caught exception: {exc}")

    print()


# ----------------------------------------
# 4) RE-RAISE VS RAISING A NEW EXCEPTION
# ----------------------------------------

def reraise_vs_new_exception_demo() -> None:
    print("=== reraise_vs_new_exception_demo ===")

    # Re-raising keeps:
    # - the original exception type
    # - the original traceback
    #
    # Raising a new exception discards that information
    # unless exception chaining is used (next file).

    def read_positive_int(path: str) -> int:
        try:
            with open(path) as file:
                value: int = int(file.read())
        except FileNotFoundError:
            print("File missing")
            raise

        if value <= 0:
            raise ValueError("Expected a positive integer")

        return value

    try:
        read_positive_int("missing.txt")
    except (FileNotFoundError, ValueError) as exc:
        print(f"Caught exception: {exc}")

    print()


# ----------------------------------------
# 5) WHEN RE-RAISE IS THE CORRECT DEFAULT
# ----------------------------------------

def default_reraise_policy_demo() -> None:
    print("=== default_reraise_policy_demo ===")

    # A useful rule of thumb:
    #
    # If a function cannot:
    # - fix the problem
    # - substitute a meaningful value
    # - or fully handle the error
    #
    # then re-raising is the correct default behavior.

    def open_resource(path: str) -> None:
        try:
            with open(path):
                pass
        except OSError:
            # No recovery strategy here.
            # This function is not responsible for deciding what to do next.
            raise

    try:
        open_resource("nonexistent.resource")
    except OSError as exc:
        print(f"Caught exception: {exc}")

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    simple_reraise_demo()
    swallowing_exception_demo()
    reraise_after_partial_handling_demo()
    reraise_vs_new_exception_demo()
    default_reraise_policy_demo()
