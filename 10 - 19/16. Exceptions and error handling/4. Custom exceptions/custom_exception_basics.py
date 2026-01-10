"""
Basics of custom exceptions in Python.

This file introduces the minimal and correct way to define,
raise, and catch custom exceptions without unnecessary complexity.
"""

from __future__ import annotations


# ----------------------------------------
# Custom exception definitions
# ----------------------------------------

class ApplicationError(Exception):
    # Base custom exception for the application.
    #
    # At this level we do not add behavior.
    # The main goal is semantic clarity:
    # catching ApplicationError means "any domain-level failure".
    pass


class InvalidUserInputError(ApplicationError):
    # Raised when user-provided data is structurally valid
    # but semantically incorrect for the current operation.
    pass


# ----------------------------------------
# 1) BASIC DEFINITION (THEORY ONLY)
# ----------------------------------------

# A custom exception is a regular Python class that inherits from Exception.
#
# It does not introduce new mechanics to the language.
# The try / except behavior is exactly the same as with built-in exceptions.
#
# The primary reason to introduce custom exceptions is semantic clarity.
# They allow the code to express *intent*, not just *failure*.
#
# In larger systems, catching ValueError or RuntimeError is often ambiguous:
# - Did the error come from parsing?
# - From validation?
# - From an internal programming mistake?
#
# Custom exception types make this distinction explicit.
#
# Important:
# Custom exceptions should inherit from Exception, not BaseException.
#
# BaseException is reserved for system-level events such as:
# - KeyboardInterrupt
# - SystemExit
# - GeneratorExit
#
# Catching BaseException almost always leads to incorrect behavior.


# ----------------------------------------
# 2) RAISING CUSTOM EXCEPTIONS
# ----------------------------------------

def raising_custom_exception_demo() -> None:
    print("=== raising_custom_exception_demo ===")

    # Custom exceptions are raised exactly like built-in ones.
    # The difference is not in syntax, but in meaning.

    user_age: int = -5

    if user_age < 0:
        # We deliberately raise a domain-specific exception.
        # ValueError would be technically acceptable,
        # but much less expressive at system boundaries.
        raise InvalidUserInputError("User age cannot be negative")

    print()


# ----------------------------------------
# 3) CATCHING BY SEMANTIC LEVEL
# ----------------------------------------

def catching_custom_exception_demo() -> None:
    print("=== catching_custom_exception_demo ===")

    try:
        raising_custom_exception_demo()
    except InvalidUserInputError as exc:
        # Catching the most specific exception enables
        # precise recovery, logging, or user feedback.
        print(f"Caught InvalidUserInputError: {exc}")
    except ApplicationError:
        # Catching the base domain exception creates
        # a clean boundary between application logic
        # and unexpected system failures.
        print("Caught a generic application error")

    print()


# ----------------------------------------
# 4) WHY NOT JUST USE VALUEERROR? (THEORY ONLY)
# ----------------------------------------

# Using built-in exceptions everywhere scales poorly.
#
# ValueError, TypeError, and RuntimeError describe *what* went wrong,
# but not *where* or *why* in terms of business or domain logic.
#
# When a high-level layer catches ValueError, it cannot know:
# - whether this is a user input problem
# - a violated business invariant
# - or a bug in the implementation
#
# Custom exceptions solve this by encoding intent in the type itself.
#
# This allows:
# - selective catching
# - clear error boundaries between layers
# - stable error-handling contracts
#
# In short:
# built-in exceptions describe mechanics,
# custom exceptions describe meaning.


# ----------------------------------------
# 5) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    catching_custom_exception_demo()
