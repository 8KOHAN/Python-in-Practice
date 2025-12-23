# ------------------------------------------------------------
# IMPORTANT CLARIFICATION ABOUT OPERATORS IN LAMBDA
# ------------------------------------------------------------
# In Python, you *can* use arithmetic operators (*, /, +, -, **, %, //)
# inside lambda expressions. There is no restriction on using these.
# The only limitation is that a lambda may contain only *one expression*,
# not statements (if, for, return, try, etc.).
# Example:
#   valid:   lambda x: (x * 2) / 3
#   invalid: lambda x: (x *= 2)   # assignment is a statement, not allowed
# ------------------------------------------------------------
# LAMBDA FUNCTIONS — BASIC CONCEPTS
# ------------------------------------------------------------
# A lambda function is an anonymous, single-expression function.
# It has no name (unless assigned to a variable)
# ------------------------------------------------------------
from typing import Callable

# Basic lambda example
square: Callable[[int | float], int | float] = (
    lambda x: x * x
)  # returns x squared

print("=== BASIC LAMBDA EXAMPLE ===")
print("square(5):", square(5))
print()

# Multiple arguments
add: Callable[[int | float, int | float], int | float] = (
    lambda a, b: a + b
)

print("=== MULTI-ARGUMENT LAMBDA ===")
print("add(3, 4):", add(3, 4))
print()

# Lambdas inside other expressions
numbers: list[int] = [1, 2, 3, 4, 5]

print("=== USING LAMBDA IN LIST COMPREHENSION ===")
doubled: list[int] = [
    (lambda x: x * 2)(n) for n in numbers
]
print("doubled:", doubled)
print()

# Lambdas used as key functions (common use-case)
print("=== LAMBDA AS KEY FUNCTION ===")
words: list[str] = ["banana", "apple", "kiwi", "strawberry"]
sorted_words: list[str] = sorted(
    words,
    key=lambda w: len(w)
)

print("sorted by length:", sorted_words)
print()

# Assigning a lambda to meaningful variable names improves readability
# (BAD)
bad_name: Callable[[float, float], float] = (
    lambda x, y: (x * y) / (x + y)
)

# (GOOD)
def combine_ratio(x: float, y: float) -> float:
    """Return ratio of x and y using a meaningful operation."""
    return (x * y) / (x + y)

print("=== READABILITY COMPARISON ===")
print("bad(2, 3):", bad_name(2, 3))
print("combine_ratio(2, 3):", combine_ratio(2, 3))
print()


# ------------------------------------------------------------
# MORE LAMBDA BASICS — EXTENDED EXAMPLES
# ------------------------------------------------------------

# Lambda with default arguments
print("=== LAMBDA WITH DEFAULT ARGUMENTS ===")
power: Callable[[int | float, int | float], int | float] = (
    lambda x, p=2: x ** p
)

print("power(3):", power(3))        # default p=2
print("power(3, 3):", power(3, 3))  # custom p
print()

# Lambda returning tuples
print("=== LAMBDA RETURNING MULTIPLE VALUES ===")
pair: Callable[[int | float], tuple[int | float, int | float]] = (
    lambda x: (x, x * 2)
)
print("pair(5):", pair(5))
print()

# Lambda inside sorted() with complex logic via expression
print("=== LAMBDA WITH CONDITIONAL EXPRESSION ===")
numbers2: list[int] = [10, 3, 7, 2, 15]
sorted_custom: list[int] = sorted(
    numbers2,
    key=lambda n: n if n % 2 == 0 else n + 100
)

print("sorted with custom rule:", sorted_custom)
print()

# Lambda inside map
print("=== MAP WITH LAMBDA ===")
tripled: list[int] = list(map(lambda x: x * 3,
                              numbers))

print("tripled:", tripled)
print()

# Lambda inside filter
print("=== FILTER WITH LAMBDA ===")
filtered: list[int] = list(filter(lambda x: x % 2 == 0,
                                  numbers))

print("even numbers:", filtered)
print()

# Lambda cannot contain statements (example showing limitation)
print("=== LAMBDA LIMITATION EXAMPLE ===")
# The following is NOT allowed:
# lambda x: if x > 0: return x   # SyntaxError
# Lambdas can only contain expressions, not statements.
print("Lambdas cannot contain statements like if/for/return.")
print()
