# ------------------------------------------------------------
# FUNCTION DESIGN PHILOSOPHY
# ------------------------------------------------------------
# A function is not just a syntactic element, but a semantic unit.
# It should express one meaningful action at a clear level of abstraction.
#
# Bad design often comes from writing functions for the wrong reasons:
#   "to avoid code repetition"
#   "to move some code out of main"
#   "because it looks cleaner"
#
# Good design means:
#   Each function represents a meaningful operation.
#   Each function solves ONE problem (Single Responsibility).
#   Each function hides internal complexity.
#   Each function has a clear name that reflects what it does.
# ------------------------------------------------------------


# ------------------------------------------------------------
# EXAMPLE 1 — BAD FUNCTION: no single responsibility
# ------------------------------------------------------------
def handle_user_data(user: dict) -> None:
    """
    This function does too many things:
       - validates input
       - prints a message
       - calculates a value
       - modifies the dictionary
    """
    if not isinstance(user, dict):
        print("Invalid user data!")
        return

    print("User:", user.get("name"))
    age = user.get("age", 0)
    if age < 18:
        print("Minor user.")
    else:
        print("Adult user.")
    user["processed"] = True


print("=== BAD FUNCTION ===")
user_data = {"name": "Alice", "age": 22}
handle_user_data(user_data)
print("User after processing:", user_data)
print()


# ------------------------------------------------------------
# EXAMPLE 2 — GOOD DESIGN: one responsibility per function
# ------------------------------------------------------------
def validate_user(*, user: dict) -> bool:
    """Check that user dictionary has required structure."""
    return isinstance(user, dict) and "name" in user and "age" in user


def describe_user(*, user: dict) -> str:
    """Return a human-readable description of the user."""
    return f"{user['name']} ({user['age']} years old)"


def is_adult(*, user: dict) -> bool:
    """Return True if the user is 18 or older."""
    return user["age"] >= 18


def mark_processed(*, user: dict) -> None:
    """Mark user as processed."""
    user["processed"] = True


def process_user(*, user: dict) -> None:
    """
       This function orchestrates other small functions.
       It expresses a high-level action — processing a user.
    """
    if not validate_user(user=user):
        print("Invalid user data!")
        return

    print("User:", describe_user(user=user))
    if is_adult(user=user):
        print("Category: adult")
    else:
        print("Category: minor")

    mark_processed(user=user)
    print("User marked as processed.")


print("=== GOOD FUNCTION DESIGN ===")
user_info = {"name": "Bob", "age": 17}
process_user(user=user_info)
print("User after processing:", user_info)
print()


# ------------------------------------------------------------
# EXAMPLE 3 — LEVELS OF ABSTRACTION
# ------------------------------------------------------------
# Functions should exist on the same "semantic level".
# High-level functions call lower-level ones,
# but they should not mix conceptual layers.

def calculate_area(*, width: float, height: float) -> float:
    """Low-level math operation."""
    return width * height


def print_rectangle_info(*, width: float, height: float) -> None:
    """High-level, user-oriented function."""
    area = calculate_area(width=width, height=height)
    print(f"Rectangle {width} x {height} has area = {area}")


print("=== LEVELS OF ABSTRACTION ===")
print_rectangle_info(width=5.0, height=3.2)
print()


# ------------------------------------------------------------
# EXAMPLE 4 — NAMING MATTERS
# ------------------------------------------------------------
# Names should communicate intent, not mechanics.

def x(a, b):
    return a * b

def multiply(num1: float, num2: float) -> float:
    """Clearer and self-documenting name."""
    return num1 * num2


print("=== NAMING COMPARISON ===")
print("x(2, 3):", x(2, 3))  # unclear
print("multiply(2, 3):", multiply(2, 3))  # clear meaning
print()


# ------------------------------------------------------------
# EXAMPLE 5 — BAD VS GOOD COHESION
# ------------------------------------------------------------
# BAD: unrelated logic in one function
def bad_function(a: int, b: int, name: str) -> None:
    print(a + b)
    print(f"Hello {name}")
    print("Unrelated tasks combined")

# GOOD: separate, cohesive responsibilities
def add_numbers(a: int, b: int) -> int:
    return a + b

def greet_user(*, name: str) -> None:
    print(f"Hello, {name}!")

print("=== BAD COHESION ===")
bad_function(2, 3, "Eve")
print("=== GOOD COHESION ===")
result = add_numbers(2, 3)
print("Sum:", result)
greet_user(name="Eve")
print()


# ------------------------------------------------------------
# EXAMPLE 6 — KEYWORD-ONLY ARGUMENTS (*)
# ------------------------------------------------------------
# The '*' symbol in function definition forces the caller to use keyword arguments.
# It improves readability, prevents ordering mistakes, and makes APIs more stable.

def resize_image(*, width: int, height: int, mode: str) -> None:
    """Example of using * to require keyword arguments."""
    print(f"Resizing to {width}x{height} in mode '{mode}'")

print("=== KEYWORD-ONLY ARGUMENTS ===")
# resize_image(1920, 1080, "cover")  # Error — positional args not allowed
resize_image(width=1920, height=1080, mode="cover")  # Clear and safe
print()

# When to use '*':
# - When argument order has no real meaning
# - When function has many parameters of different kinds
# - When function is part of a public API
#
# When NOT to use '*':
# - In simple math-like functions where order is obvious
#   Example: add(num1, num2), multiply(num1, num2)
#
# In short:
#   '*' improves clarity and reduces ambiguity in larger codebases.


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("=== SUMMARY ===")
print("Each function should represent ONE clear responsibility.")
print("Each function should have a meaningful name.")
print("High-level and low-level logic must be separated.")
print("Keyword-only arguments (*) enforce clarity in function calls.")
print("Functions exist to create meaning — not just to reduce repetition.")
print("End of file: function_design_philosophy.py")
