"""
How to document raised exceptions without misleading readers or tools.

This file explains what `Raises:` documentation actually means,
what it does NOT guarantee, and how to keep documentation honest
and useful in typed Python code.
"""

from __future__ import annotations


# ----------------------------------------
# 1) WHAT `Raises:` REALLY IS (AND IS NOT)
# ----------------------------------------

def raises_docstring_is_not_a_contract_demo() -> None:
    print("=== raises_docstring_is_not_a_contract_demo ===")

    # `Raises:` in a docstring is documentation only.
    # It is not enforced by:
    # - the Python runtime
    # - type checkers
    # - static analyzers
    #
    # It is a promise made by the author to the reader,
    # not a guarantee checked by tools.

    def parse_int(value: str) -> int:
        """
        Converts a string to an integer.

        Raises:
            ValueError: If the string is not a valid integer.
        """
        return int(value)

    try:
        parse_int("not-a-number")
    except ValueError:
        print("ValueError was raised as documented")

    print()


# ----------------------------------------
# 2) DOCUMENT ONLY WHAT YOU ACTUALLY RAISE
# ----------------------------------------

def document_only_direct_exceptions_demo() -> None:
    print("=== document_only_direct_exceptions_demo ===")

    # A common mistake is documenting every possible exception
    # that might happen indirectly.
    #
    # This quickly becomes dishonest and unmaintainable.

    def read_positive_int(value: str) -> int:
        """
        Parses a positive integer.

        Raises:
            ValueError: If the value is not a valid positive integer.
        """
        number = int(value)

        if number <= 0:
            raise ValueError("number must be positive")

        return number

    # Even though int(value) can raise TypeError,
    # we do NOT document it here:
    #
    # - it is obvious to experienced readers
    # - documenting it adds noise
    # - it is not part of the function's domain logic

    try:
        read_positive_int("-5")
    except ValueError as exc:
        print(f"Caught ValueError: {exc}")

    print()


# ----------------------------------------
# 3) WHEN `Raises:` BECOMES ACTIVELY MISLEADING
# ----------------------------------------

def misleading_raises_demo() -> None:
    print("=== misleading_raises_demo ===")

    # This example shows a docstring that looks correct,
    # but actually lies about behavior.

    def unsafe_divide(a: int, b: int) -> float:
        """
        Divides two integers.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        # This condition silently changes behavior.
        if b == 0:
            return float("inf")

        return a / b

    # The docstring claims ZeroDivisionError may be raised,
    # but it never happens.
    #
    # This is worse than having no documentation at all.

    result = unsafe_divide(10, 0)
    print(f"Result: {result}")

    print()


# ----------------------------------------
# 4) DOCUMENTING EXCEPTIONS VS HANDLING THEM
# ----------------------------------------

def documenting_vs_handling_demo() -> None:
    print("=== documenting_vs_handling_demo ===")

    # If a function catches an exception internally
    # and converts it to another one, documentation
    # must reflect the final behavior.

    def parse_port(value: str) -> int:
        """
        Parses a TCP port number.

        Raises:
            ValueError: If the value is not a valid port number.
        """
        try:
            port = int(value)
        except ValueError as exc:
            # Original ValueError is intentionally hidden.
            raise ValueError("port must be an integer") from exc

        if not (0 < port < 65536):
            raise ValueError("port out of range")

        return port

    try:
        parse_port("invalid")
    except ValueError as exc:
        print(f"Caught ValueError: {exc}")

    print()


# ----------------------------------------
# 5) WHY `Raises:` DOES NOT BELONG IN EVERY FUNCTION
# ----------------------------------------

def over_documentation_demo() -> None:
    print("=== over_documentation_demo ===")

    # Over-documentation is a real problem.
    # If a function:
    # - simply forwards a call
    # - performs trivial operations
    # - has obvious failure modes
    #
    # then `Raises:` adds no real value.

    def to_int(value: str) -> int:
        return int(value)

    # Documenting this function with a Raises section
    # would be pure noise.

    try:
        to_int("abc")
    except ValueError:
        print("ValueError raised as expected")

    print()


# ----------------------------------------
# 6) PRACTICAL RULES (THEORY-ONLY SECTION)
# ----------------------------------------
#
# Rules to follow when documenting raised exceptions:
#
# 1) Document only exceptions that are part of the function's public API.
#    If the caller is expected to handle the exception explicitly,
#    it probably belongs in the documentation.
#
# 2) Do NOT document obvious low-level exceptions.
#    Examples:
#    - ValueError from int(...)
#    - TypeError from incorrect argument types
#    These are assumed knowledge for experienced readers.
#
# 3) Never document exceptions that cannot actually occur.
#    A documented exception that is never raised is worse than
#    having no documentation at all.
#
# 4) Documentation must evolve together with behavior.
#    If exception handling logic changes, the Raises section
#    must be reviewed immediately.
#
# 5) Prefer a small number of accurate exceptions over exhaustive lists.
#    Exhaustive documentation creates noise and gives a false
#    sense of precision.


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    raises_docstring_is_not_a_contract_demo()
    document_only_direct_exceptions_demo()
    misleading_raises_demo()
    documenting_vs_handling_demo()
    over_documentation_demo()
