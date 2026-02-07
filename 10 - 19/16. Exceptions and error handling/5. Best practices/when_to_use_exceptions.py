"""
This file demonstrates best practices for when to use exceptions in Python.
It explains scenarios where raising exceptions is appropriate versus situations
where other control flow mechanisms should be preferred.
"""

from __future__ import annotations


# ----------------------------------------
# 1) BASIC EXCEPTION USAGE
# ----------------------------------------
def basic_exception_demo() -> None:
    print("=== basic_exception_demo ===")

    # Example: dividing numbers
    # Correct use of exception: handling unexpected ZeroDivisionError
    try:
        numerator: int = 10
        denominator: int = 0
        result: float = numerator / denominator
    except ZeroDivisionError as exc:
        # We use an exception because division by zero is truly exceptional
        print("Caught ZeroDivisionError:", exc)

    # Avoid using exceptions for normal flow control
    # Example: do not use exceptions to check a variable's presence if it's easy to check otherwise
    my_dict: dict[str, int] = {"a": 1, "b": 2}
    key: str = "c"

    if key in my_dict:
        value: int = my_dict[key]
        print("Value found:", value)
    else:
        # This is better than trying to access and catching KeyError
        print("Key not found, handled without exception")

    print()


# ----------------------------------------
# 2) WHEN EXCEPTIONS ARE APPROPRIATE
# ----------------------------------------
def appropriate_exception_demo() -> None:
    print("=== appropriate_exception_demo ===")

    # Exceptions are appropriate when:
    # - something truly unexpected occurs
    # - the function cannot continue normally
    # - the caller must be informed of a failure

    # Example: parsing integer from user input
    user_input: str = "abc"

    try:
        value: int = int(user_input)
    except ValueError as exc:
        print("Caught ValueError:", exc)
        # Raising exception here is correct because the input is invalid
        # Normal program flow cannot continue with invalid input

    print()


# ----------------------------------------
# 3) WHEN NOT TO USE EXCEPTIONS
# ----------------------------------------
def inappropriate_exception_demo() -> None:
    print("=== inappropriate_exception_demo ===")

    # Do NOT use exceptions for:
    # - expected or common control flow
    # - situations that can be handled with simple checks
    # - minor optional behaviors

    # Example: checking if a list is empty
    my_list: list = []

    if not my_list:
        print("List is empty, handling gracefully without exception")
    else:
        print("Processing list")

    print()


# ----------------------------------------
# 4) QUICK-RUN
# ----------------------------------------
if __name__ == "__main__":
    basic_exception_demo()
    appropriate_exception_demo()
    inappropriate_exception_demo()
