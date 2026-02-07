"""
Using dataclasses for custom exceptions.

This file demonstrates when and why it is reasonable
to use dataclasses for exceptions, and what problems
they actually solve.
"""

from __future__ import annotations

from dataclasses import dataclass


# ----------------------------------------
# BASE EXCEPTION
# ----------------------------------------

class ApplicationError(Exception):
    # Root exception for all application-level errors.
    pass


# ----------------------------------------
# 1) WHY DATACLASSES FOR EXCEPTIONS? (THEORY ONLY)
# ----------------------------------------

# By default, exceptions carry information through:
# - their type
# - an optional string message
#
# This approach breaks down when:
# - multiple structured values must be attached to the error
# - the error must be inspected programmatically
# - string parsing would otherwise be required
#
# Dataclasses solve this by making error data explicit,
# typed, and self-documenting.
#
# Important:
# Dataclass-based exceptions are NOT about convenience.
# They are about clarity, correctness, and contracts.


# ----------------------------------------
# 2) A SIMPLE DATACLASS EXCEPTION
# ----------------------------------------

@dataclass(frozen=True)
class ValidationError(ApplicationError):
    field_name: str
    reason: str

    # We intentionally do NOT override __str__.
    #
    # The default dataclass-generated representation
    # already contains structured information and is
    # usually sufficient for logs and debugging.


def simple_dataclass_exception_demo() -> None:
    print("=== simple_dataclass_exception_demo ===")

    field_value: str = ""
    field_name: str = "username"

    if not field_value:
        raise ValidationError(
            field_name=field_name,
            reason="Value must not be empty",
        )

    print()


# ----------------------------------------
# 3) STRUCTURED DATA VS STRING MESSAGES (THEORY ONLY)
# ----------------------------------------

# Compare the following two approaches:
#
# raise ValueError("username must not be empty")
#
# vs
#
# raise ValidationError(field_name="username", reason="Value must not be empty")
#
# The second form:
# - avoids string parsing
# - allows programmatic inspection
# - survives refactoring
#
# Higher layers can make decisions based on data,
# not on fragile message text.


# ----------------------------------------
# 4) CATCHING AND USING STRUCTURED ERROR DATA
# ----------------------------------------

def catching_dataclass_exception_demo() -> None:
    print("=== catching_dataclass_exception_demo ===")

    try:
        simple_dataclass_exception_demo()
    except ValidationError as exc:
        # We can safely access structured fields.
        # This is the core benefit of dataclass-based exceptions.
        print(f"Field: {exc.field_name}")
        print(f"Reason: {exc.reason}")

    print()


# ----------------------------------------
# 5) IMMUTABILITY AND SAFETY (THEORY ONLY)
# ----------------------------------------

# The exception is declared with frozen=True.
#
# This guarantees:
# - the error object cannot be mutated after creation
# - error data remains trustworthy
#
# Exceptions are often passed across layers.
# Mutable error objects introduce subtle bugs
# and should be avoided.


# ----------------------------------------
# 6) WHEN NOT TO USE DATACLASS EXCEPTIONS (THEORY ONLY)
# ----------------------------------------

# Dataclass-based exceptions are NOT always appropriate.
#
# Avoid them when:
# - the error carries no structured data
# - a simple semantic marker is enough
# - performance is extremely critical (rare)
#
# Overusing dataclass exceptions leads to:
# - bloated APIs
# - unnecessary coupling between layers


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    catching_dataclass_exception_demo()
