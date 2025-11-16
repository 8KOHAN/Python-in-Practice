# ------------------------------------------------------------
# INTRODUCTION
# ------------------------------------------------------------
# Nested functions are functions defined inside other functions.
# They allow controlled scoping, hiding implementation details,
# creating closures, and structuring logic at different abstraction levels.
#
# They should *not* be used for every small helper, only when:
# - The helper function is logically tied to the outer function.
# - It should not be accessible from the outside.
# - It depends on the outer function's state.
# ------------------------------------------------------------
from typing import Callable

# ------------------------------------------------------------
# 1 - BASIC EXAMPLE OF A NESTED FUNCTION
# ------------------------------------------------------------
def greet_user(*, name: str) -> None:
    """Greet a user by creating a formatting helper inside the function."""

    def format_name(*, name: str) -> str:  # nested helper
        """Format a user name (local helper)."""
        return name.strip().title()

    formatted_name = format_name(name=name)
    print(f"Hello, {formatted_name}!")


greet_user(name="   alice   ")
print()


# ------------------------------------------------------------
# 2 - NESTED FUNCTION THAT CAPTURES OUTER VARIABLES (CLOSURE PREVIEW)
# ------------------------------------------------------------
def make_multiplier(*, factor: int) -> Callable[[int], int]:
    """
    Return a function that multiplies by a fixed factor.
    Demonstrates how inner functions capture variables.
    """

    def multiplier(*, value: int) -> int:  # nested
        return value * factor  # uses outer scope variable "factor"

    return multiplier


triple = make_multiplier(factor=3)
print(triple(value=10))  # expected 30
print()


# ------------------------------------------------------------
# CLEAR CLOSURE EXAMPLE: discount calculator factory
# ------------------------------------------------------------

def make_discount_function(*, percent: float) -> Callable[[float], float]:
    """
    Create a function that applies a discount.
    The nested function 'apply' remembers the 'percent' value,
    even after make_discount_function has finished executing.
    """

    # Validate discount percent
    if percent <= 0 or percent >= 100:
        raise ValueError("Discount percent must be between 0 and 100.")

    def apply(*, price: float) -> float:
        """Apply a discount to the given price."""
        return price - (price * (percent / 100))

    return apply


discount_10 = make_discount_function(percent=10)   # function with 10% discount
discount_25 = make_discount_function(percent=25)   # function with 25% discount

print(discount_10(price=200))  # expected 180.0 (10% off)
print(discount_25(price=200))  # expected 150.0 (25% off)
print()

# ------------------------------------------------------------
# 3 - NESTING FOR STRUCTURING COMPLEX LOGIC
# ------------------------------------------------------------
def process_order(*, id: int, user: str) -> None:
    """
    Simulate order processing with nested steps.
    All steps are private and logically part of the high-level process.
    """

    def validate() -> bool:
        # In real systems, validation would be more complex.
        print(f"Validating order {id}...")
        return id > 0

    def charge() -> None:
        # Charging logic.
        print(f"Charging user '{user}' for order {id}...")

    def notify() -> None:
        # Notification logic.
        print(f"Sending notification to {user}...")

    # High-level orchestration
    if not validate():
        print("Order validation failed!")
        return

    charge()
    notify()
    print("Order processed successfully.")


process_order(id=101, user="Alice")
print()


# ------------------------------------------------------------
# LIMITATIONS & WARNINGS
# ------------------------------------------------------------
# - Nested functions are recreated on every function call.
# - Do NOT use nested functions for performance-critical logic.
# - Do NOT overuse them; too many layers harm readability.
# - Use them when they improve abstraction and encapsulation.
# ------------------------------------------------------------
