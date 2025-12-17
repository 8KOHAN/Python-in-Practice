# ------------------------------------------------------------
# LAMBDA FUNCTIONS — ADVANCED USAGE
# ------------------------------------------------------------
# This file demonstrates advanced and *practical* use cases
# of lambda functions in real Python code.
# Lambdas are useful when behavior is passed as data.
# ------------------------------------------------------------

from typing import Callable
from functools import reduce, partial

# ------------------------------------------------------------
# 1. LAMBDAS AS STRATEGIES (STRATEGY PATTERN)
# ------------------------------------------------------------
print("=== LAMBDA AS STRATEGY ===")

operation_add: Callable[[int, int], int] = (
    lambda a, b: a + b
)
operation_mul: Callable[[int, int], int] = (
    lambda a, b: a * b
)


def apply_operation(a: int, b: int, *, operation: Callable[[int, int], int]) -> int:
    """Apply a strategy operation to two numbers."""
    return operation(a, b)

print(apply_operation(2, 3, operation=operation_add))
print(apply_operation(2, 3, operation=operation_mul))
print()


# ------------------------------------------------------------
# 2. LAMBDAS AND CLOSURES
# ------------------------------------------------------------
print("=== LAMBDA WITH CLOSURE ===")


def make_multiplier(factor: int) -> Callable[[int], int]:
    """Return a lambda that multiplies by a fixed factor."""
    return lambda x: x * factor

multiply_by_10 = make_multiplier(10)
print(multiply_by_10(5))
print()


# ------------------------------------------------------------
# 3. LAMBDAS WITH REDUCE
# ------------------------------------------------------------
print("=== REDUCE WITH LAMBDA ===")

numbers: list[int] = [1, 2, 3, 4, 5]
result: int = reduce(
    lambda a, b: a * b,
    numbers
)
print("product:", result)
print()


# ------------------------------------------------------------
# 4. PARTIAL FUNCTIONS VS LAMBDA
# ------------------------------------------------------------
print("=== PARTIAL VS LAMBDA ===")

# Using lambda
add_five_lambda: Callable[[int], int] = (
    lambda x: x + 5
)

# Using functools.partial
add_five_partial: Callable[[int], int] = partial(
    lambda a, b: a + b,
    5
)

print(add_five_lambda(10))
print(add_five_partial(10))
print()


# ------------------------------------------------------------
# 5. LAMBDA IN SORTING COMPLEX DATA
# ------------------------------------------------------------
print("=== SORTING COMPLEX STRUCTURES ===")

users: list[dict[str, int | str]] = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
]

sorted_by_age = sorted(
    users,
    key=lambda user: user["age"]
)
print(sorted_by_age)
print()


# ------------------------------------------------------------
# 6. LAMBDA WITH BOOLEAN LOGIC
# ------------------------------------------------------------
print("=== BOOLEAN LOGIC IN LAMBDA ===")

is_valid_user: Callable[[dict[str, int | str]], bool] = (
    lambda user: user["age"] >= 18 and user["name"] != ""
)

print(is_valid_user({"name": "Anna", "age": 20}))
print(is_valid_user({"name": "", "age": 20}))
print()


# ------------------------------------------------------------
# 7. USING 'is' OPERATOR INSIDE LAMBDA
# ------------------------------------------------------------
print("=== 'is' OPERATOR IN LAMBDA ===")

# Lambda checking identity, not equality
is_none: Callable[[object], bool] = (
    lambda value: value is None
)

print(is_none(None))     # True
print(is_none(0))        # False
print(is_none(""))       # False
print()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("=== SUMMARY ===")
print("Lambda functions are powerful when used:")
print(" - as short strategies")
print(" - as callbacks")
print(" - with higher-order functions")
print(" - when behavior must be passed, not named")
