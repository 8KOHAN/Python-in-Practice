# ---------------------------------------------------------------------------
# INTRODUCTION
# ---------------------------------------------------------------------------
# A Higher-Order Function (HOF):
# - accepts one or more functions as arguments, OR
# - returns a function as a result.
#
# They allow functional-style programming, flexible configuration, and
# help abstract repeated patterns of behavior.
# ---------------------------------------------------------------------------
from typing import Callable, Iterable, Any


# ---------------------------------------------------------------------------
# EXAMPLE 1 — APPLY FUNCTION TO EVERY ELEMENT (CUSTOM MAP)
# ---------------------------------------------------------------------------
# This HOF is similar to Python's built-in map(), but implemented manually.


def apply_to_each(*, function: Callable[[Any], Any], values: Iterable[Any]) -> list:
    """Apply a function to each element in an iterable and return the results."""
    result = []
    for item in values:
        result.append(function(item))
    return result


def square(num: int) -> int:
    return num * num

print(apply_to_each(function=square, values=[1, 2, 3, 4]))
print()


# ---------------------------------------------------------------------------
# EXAMPLE 2 — CUSTOM FILTER FUNCTION
# ---------------------------------------------------------------------------
# Works like built-in filter(), but explicit and typed.


def filter_items(*, predicate: Callable[[Any], bool], values: Iterable[Any]) -> list:
    """Return items for which predicate(item) is True."""
    return [item for item in values if predicate(item)]


def is_even(num: int) -> bool:
    return num % 2 == 0

print(filter_items(predicate=is_even, values=[1, 2, 3, 4, 5, 6]))
print()


# ---------------------------------------------------------------------------
# EXAMPLE 3 — HIGHER-ORDER FUNCTION THAT RETURNS A FUNCTION
# ---------------------------------------------------------------------------
# Similar to closures.py but focused on the HOF concept.


def power_factory(*, exponent: int) -> Callable[[int], int]:
    """Return a function that raises numbers to the given exponent."""

    def power(base: int) -> int:
        return base ** exponent

    return power


square_f = power_factory(exponent=2)
cube_f = power_factory(exponent=3)

print(square_f(5))  # 25
print(cube_f(5))    # 125
print()


# ---------------------------------------------------------------------------
# EXAMPLE 4 — FUNCTION COMPOSER (ADVANCED, VERY USEFUL)
# ---------------------------------------------------------------------------
# compose(f, g) returns a new function h(x) = f(g(x)).
# This is common in functional programming.


def compose(f: Callable[[Any], Any], g: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Return a new function that is the composition of f and g."""

    def composed(x: Any) -> Any:
        return f(g(x))

    return composed


def add_one(x: int) -> int:
    return x + 1

add_one_then_square = compose(square, add_one)
print(add_one_then_square(4))  # (4+1)^2 = 25
print()


# ---------------------------------------------------------------------------
# EXAMPLE 5 — PASSING BEHAVIOR INTO AN ALGORITHM
# ---------------------------------------------------------------------------
# HOFs allow customizing algorithms without rewriting them.


def process_numbers(*, values: Iterable[int], transform: Callable[[int], int]) -> list:
    """Apply a transform function to all numbers and return the new list."""
    return [transform(v) for v in values]


print(process_numbers(values=[1, 2, 3], transform=square))
print(process_numbers(values=[1, 2, 3], transform=lambda x: x * 10))
print()


# ---------------------------------------------------------------------------
# BEST PRACTICES
# ---------------------------------------------------------------------------
# Use HOFs to:
#   - reduce code duplication
#   - introduce abstraction layers
#   - pass strategies or small behavior units
#   - build modular pipelines
#
# Avoid HOFs when:
#   - business logic becomes unreadable
#   - too many lambdas reduce clarity
#   - stateful behavior is needed → use classes instead
# ---------------------------------------------------------------------------
