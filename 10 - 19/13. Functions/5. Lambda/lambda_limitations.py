# ------------------------------------------------------------
# LAMBDA FUNCTIONS — LIMITATIONS AND ANTI-PATTERNS
# ------------------------------------------------------------
# This file explains WHY lambda functions are intentionally limited
# in Python and when they should NOT be used.
# ------------------------------------------------------------

from typing import Callable

# ------------------------------------------------------------
# 1. SINGLE EXPRESSION ONLY
# ------------------------------------------------------------
print("=== SINGLE EXPRESSION LIMITATION ===")

# VALID: single expression
valid_lambda: Callable[[int], int] = (
    lambda x: x * 2
)
print(valid_lambda(5))

# INVALID: statements are not allowed
# lambda x:
#     y = x * 2      # SyntaxError
#     return y

print("Lambda can contain only one expression, not statements.")
print()


# ------------------------------------------------------------
# 2. NO ASSIGNMENTS
# ------------------------------------------------------------
print("=== NO ASSIGNMENTS IN LAMBDA ===")

# INVALID examples:
# lambda x: x = 10
# lambda x: (x := 10)  # walrus is expression, but bad practice here

print("Assignments are not allowed inside lambda expressions.")
print()


# ------------------------------------------------------------
# 3. NO MULTI-LINE LOGIC
# ------------------------------------------------------------
print("=== NO MULTI-LINE LOGIC ===")

# BAD: complex logic in lambda
bad_lambda: Callable[[int], int] = (
    lambda x: x * 2 if x > 0 else x * -2
)

print(bad_lambda(-5))

# GOOD: use a regular function

def normalize(num: int, /) -> int:
    """Return absolute value of x."""
    if num > 0:
        return num
    return -num

print(normalize(-5))
print()


# ------------------------------------------------------------
# 4. NO TYPE ANNOTATIONS INSIDE LAMBDA
# ------------------------------------------------------------
print("=== NO TYPE ANNOTATIONS IN LAMBDA ===")

# INVALID:
# lambda x: int: x * 2

# VALID: annotate variable instead
annotated_lambda: Callable[[int], int] = (
    lambda x: x * 2
)
print(annotated_lambda(10))
print()


# ------------------------------------------------------------
# 5. POOR READABILITY WITH COMPLEX EXPRESSIONS
# ------------------------------------------------------------
print("=== READABILITY PROBLEM ===")

complex_lambda: Callable[[int, int, int], int] = (
    lambda a, b, c: a * b + c if a > b else b * c - a
)

print(complex_lambda(2, 3, 4))

print("Above lambda is hard to read and should be replaced by def.")
print()


# ------------------------------------------------------------
# 6. DEBUGGING IS HARDER
# ------------------------------------------------------------
print("=== DEBUGGING LIMITATION ===")

# Lambdas have no name in stack traces
error_lambda: Callable[[int], int] = (
    lambda x: 10 / x
)

try:
    error_lambda(0)
except ZeroDivisionError as e:
    print("Error occurred inside lambda:", e)

print("Stack traces from lambda are less informative.")
print()


# ------------------------------------------------------------
# 7. ANTI-PATTERN: USING LAMBDA INSTEAD OF def
# ------------------------------------------------------------
print("=== ANTI-PATTERN EXAMPLE ===")

# BAD
calculate_discount: Callable[[float], float] = (
    lambda price: price * 0.9 if price > 100 else price * 0.95
)

# GOOD

def calculate_discount_def(price: float, /) -> float:
    """Calculate discount based on price."""
    if price > 100:
        return price * 0.9
    return price * 0.95

print(calculate_discount(120))
print(calculate_discount_def(120))
print()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("=== SUMMARY ===")
print("Lambda functions should be avoided when:")
print(" - logic becomes complex")
print(" - readability suffers")
print(" - debugging is required")
print(" - meaningful naming is needed")
print("Use lambda only for short, simple expressions.")
