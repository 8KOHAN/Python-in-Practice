# ---------------------------------------------------------------------------
# WHAT IS A CLOSURE?
# ---------------------------------------------------------------------------
# A closure is a function that remembers values from the enclosing (outer) scope
# even after the outer function has finished execution.
#
# A closure happens when:
# 1. You have a nested function.
# 2. The nested function uses variables from the outer function.
# 3. The outer function returns the nested function.
#
# The returned inner function keeps access to the captured variables.
# ---------------------------------------------------------------------------
from typing import Callable

# ---------------------------------------------------------------------------
# EXAMPLE 1 — CLEAN, REALISTIC CLOSURE: A DISCOUNT CALCULATOR
# ---------------------------------------------------------------------------
# This version is NOT abstract: it models real behavior.
# The inner function "apply" remembers the discount_percentage.


def create_discount_calculator(*, discount_percentage: float) -> Callable[[float], float]:
    """
    Create a price calculator with a predefined discount.
    Parameters:
        discount_percentage (float): discount to apply (0.0–1.0)
    Returns:
        callable: function that applies the stored discount.
    """

    def apply(*, price: float) -> float:
        """Apply the stored discount to the given price."""
        return price * (1 - discount_percentage)

    return apply


student_discount = create_discount_calculator(discount_percentage=0.15)
print("Student price for 100:", student_discount(price=100))
print("Student price for 250:", student_discount(price=250))
print()


# ---------------------------------------------------------------------------
# EXAMPLE 2 — CLOSURE AS A STATEFUL COUNTER (COMMON PATTERN)
# ---------------------------------------------------------------------------
# The closure keeps its own internal state.
# Useful for encapsulating counters without using classes.


def make_counter(*, start: int = 0) -> Callable[[], int]:
    """Return a counter function that increases each time it's called."""

    count = start  # local state captured by inner function

    def increment() -> int:
        nonlocal count  # required to modify outer variable
        count += 1
        return count

    return increment


counter = make_counter(start=10)
print(counter())  # 11
print(counter())  # 12
print(counter())  # 13
print()


# ---------------------------------------------------------------------------
# EXAMPLE 3 — ADVANCED: PARAMETRIZED LOGGER
# ---------------------------------------------------------------------------
# A closure that stores configuration (prefix) and applies it to messages.


def build_logger(*, prefix: str) -> Callable[[str], None]:
    """Create a logger function with predefined prefix."""

    def log(*, message: str) -> None:
        print(f"[{prefix}] {message}")

    return log


info = build_logger(prefix="INFO")
error = build_logger(prefix="ERROR")

info(message="System started")
error(message="Connection failed")
print()


# ---------------------------------------------------------------------------
# HOW TO INSPECT A CLOSURE
# ---------------------------------------------------------------------------
# A closure stores captured variables in __closure__.
# This is rarely needed in production but good for learning.


def inspect_closure() -> None:
    x = 42

    def inner():
        return x

    func = inner
    print("Closure cells:", func.__closure__)
    print("Captured value:", func.__closure__[0].cell_contents)


inspect_closure()
print()


# ---------------------------------------------------------------------------
# CLOSURE LIMITATIONS AND BEST PRACTICES
# ---------------------------------------------------------------------------
# Use closures for:
#   - simple stateful behavior (counters, caching)
#   - function factories (discount creators, loggers)
#   - hiding implementation details
#
# Avoid closures when:
#   - state becomes too complex → use a class instead
#   - too many nested levels → reduces readability
#   - performance-critical code → closures add overhead
# ---------------------------------------------------------------------------
