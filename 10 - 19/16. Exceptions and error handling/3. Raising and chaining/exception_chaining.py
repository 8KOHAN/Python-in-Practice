"""
Exception chaining using `raise ... from ...`.

This file demonstrates explicit exception chaining,
why it exists, and how it preserves causal relationships
between errors in real-world code.
"""

from __future__ import annotations


# ----------------------------------------
# 1) IMPLICIT CONTEXT VS EXPLICIT CHAINING
# ----------------------------------------

def implicit_vs_explicit_demo() -> None:
    print("=== implicit_vs_explicit_demo ===")

    # When an exception is raised inside an except block,
    # Python automatically attaches the previous exception
    # as context.
    #
    # However, this implicit context does not always clearly
    # communicate intent.

    def implicit_context() -> None:
        try:
            int("not-a-number")
        except ValueError:
            # Implicit context is created here.
            raise ValueError("Failed to parse configuration value")

    def explicit_chaining() -> None:
        try:
            int("not-a-number")
        except ValueError as exc:
            # Explicit chaining documents intent:
            # this error is a direct consequence of the previous one.
            raise ValueError("Failed to parse configuration value") from exc

    for demo in (implicit_context, explicit_chaining):
        try:
            demo()
        except ValueError as exc:
            print(f"Caught exception: {exc}")

    print()


# ----------------------------------------
# 2) CHAINING AT ABSTRACTION BOUNDARIES
# ----------------------------------------

def abstraction_boundary_demo() -> None:
    print("=== abstraction_boundary_demo ===")

    # Exception chaining is most valuable at abstraction boundaries.
    #
    # Low-level exceptions are often too technical,
    # while higher-level code needs domain-relevant meaning.

    def read_timeout(raw_value: str) -> int:
        try:
            return int(raw_value)
        except ValueError as exc:
            raise ValueError("Timeout configuration must be an integer") from exc

    try:
        read_timeout("ten-seconds")
    except ValueError as exc:
        print(f"Caught exception: {exc}")

    print()


# ----------------------------------------
# 3) PRESERVING ROOT CAUSE INFORMATION
# ----------------------------------------

def root_cause_preservation_demo() -> None:
    print("=== root_cause_preservation_demo ===")

    # Chaining preserves the original exception,
    # which is critical for debugging and observability.
    #
    # Without chaining, the root cause may be lost entirely.

    def load_port(value: str) -> int:
        try:
            port = int(value)
        except ValueError as exc:
            raise ValueError("Invalid port value") from exc

        if not 0 < port < 65536:
            raise ValueError("Port out of valid range")

        return port

    try:
        load_port("eighty")
    except ValueError as exc:
        print(f"Caught exception: {exc}")

    print()


# ----------------------------------------
# 4) WHEN NOT TO USE EXCEPTION CHAINING
# ----------------------------------------

def when_not_to_chain_demo() -> None:
    print("=== when_not_to_chain_demo ===")

    # Exception chaining should NOT be used when:
    # - the new error is not causally related
    # - the previous exception is irrelevant noise
    #
    # In such cases, chaining reduces clarity instead of improving it.

    def validate_username(name: str) -> None:
        if not name.isidentifier():
            # No previous exception caused this failure.
            # Chaining here would be misleading.
            raise ValueError("Username contains invalid characters")

    try:
        validate_username("invalid-user-name")
    except ValueError as exc:
        print(f"Caught exception: {exc}")

    print()


# ----------------------------------------
# 5) SUPPRESSING CONTEXT EXPLICITLY
# ----------------------------------------

def suppress_context_demo() -> None:
    print("=== suppress_context_demo ===")

    # Python allows explicit suppression of exception context
    # using `from None`.
    #
    # This should be used sparingly and intentionally.

    def parse_flag(value: str) -> bool:
        try:
            return bool(int(value))
        except ValueError:
            # The low-level parsing detail is irrelevant here.
            raise ValueError("Flag must be 0 or 1") from None

    try:
        parse_flag("maybe")
    except ValueError as exc:
        print(f"Caught exception: {exc}")

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    implicit_vs_explicit_demo()
    abstraction_boundary_demo()
    root_cause_preservation_demo()
    when_not_to_chain_demo()
    suppress_context_demo()
