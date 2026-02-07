"""
Exception inheritance and hierarchy design.

This file demonstrates how and why custom exceptions
should be organized into clear inheritance hierarchies.
"""

from __future__ import annotations


# ----------------------------------------
# BASE EXCEPTION LAYER
# ----------------------------------------

class ApplicationError(Exception):
    # Root exception for all application-level errors.
    #
    # Catching this exception means:
    # "Something went wrong inside the application domain,
    #  not due to system-level failures."
    pass


class ValidationError(ApplicationError):
    # Raised when input data violates validation rules.
    #
    # This exception represents problems with *data correctness*,
    # not with program logic.
    pass


class BusinessRuleError(ApplicationError):
    # Raised when a business invariant is violated.
    #
    # This is distinct from ValidationError:
    # the data may be valid, but the operation is not allowed.
    pass


# ----------------------------------------
# 1) WHY INHERITANCE MATTERS (THEORY ONLY)
# ----------------------------------------

# Exception inheritance is not about code reuse.
#
# It is about *classification*.
#
# A well-designed exception hierarchy allows code to:
# - catch errors at the right semantic level
# - separate validation problems from business logic failures
# - avoid accidental catching of unrelated exceptions
#
# Flat exception structures do not scale.
# As the system grows, they force higher layers
# to inspect error messages instead of types.
#
# Inheritance shifts this responsibility to the type system.


# ----------------------------------------
# 2) RAISING DIFFERENT LEVELS OF EXCEPTIONS
# ----------------------------------------

def validation_error_demo() -> None:
    print("=== validation_error_demo ===")

    user_email: str = "invalid-email-format"

    if "@" not in user_email:
        # The data is structurally incorrect.
        # This is a validation concern.
        raise ValidationError("Email address is not valid")

    print()


def business_rule_error_demo() -> None:
    print("=== business_rule_error_demo ===")

    account_balance: int = 0
    withdrawal_amount: int = 100

    if withdrawal_amount > account_balance:
        # The data itself is valid.
        # The operation violates a business rule.
        raise BusinessRuleError("Insufficient funds for withdrawal")

    print()


# ----------------------------------------
# 3) CATCHING AT DIFFERENT SEMANTIC LEVELS
# ----------------------------------------

def semantic_catching_demo() -> None:
    print("=== semantic_catching_demo ===")

    try:
        business_rule_error_demo()
    except ValidationError as exc:
        # Handles only data validation problems.
        print(f"Validation failed: {exc}")
    except BusinessRuleError as exc:
        # Handles violations of business invariants.
        print(f"Business rule violation: {exc}")
    except ApplicationError:
        # Fallback for any other domain-level error.
        print("Generic application error occurred")

    print()


# ----------------------------------------
# 4) WHY NOT A SINGLE CUSTOM EXCEPTION? (THEORY ONLY)
# ----------------------------------------

# Using a single custom exception type defeats the purpose
# of having custom exceptions at all.
#
# If everything raises ApplicationError:
# - higher layers cannot react differently
# - error handling becomes message-based again
# - semantic information is lost
#
# A hierarchy allows progressive handling:
# - specific where possible
# - generic where necessary
#
# This mirrors how built-in exceptions work:
# IndexError -> LookupError -> Exception


# ----------------------------------------
# 5) DESIGN GUIDELINES (THEORY ONLY)
# ----------------------------------------

# Practical rules for exception hierarchies:
#
# 1) Keep the hierarchy shallow.
#    Deep trees are hard to reason about.
#
# 2) Name exceptions after *what went wrong*, not *where*.
#
# 3) Prefer multiple specific exceptions
#    over one generic "SomethingWentWrongError".
#
# 4) Do not mix technical failures and domain failures
#    in the same branch.
#
# 5) Catch broad exceptions only at system boundaries.


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    semantic_catching_demo()
