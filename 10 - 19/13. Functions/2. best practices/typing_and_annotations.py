# ------------------------------------------------------------
# TYPING AND ANNOTATIONS
# ------------------------------------------------------------
# Python supports type hints (annotations) to improve readability,
# catch errors early, and help IDEs and linters.
# Annotations do NOT enforce types at runtime unless explicitly checked.
# ------------------------------------------------------------

from typing import Optional, Union, Callable

# ------------------------------------------------------------
# EXAMPLE 1 — BASIC TYPE ANNOTATIONS
# ------------------------------------------------------------
def add_numbers(*, num1: int, num2: int) -> int:
    """Add two integers and return an integer."""
    return num1 + num2

def greet_user(*, name: str) -> None:
    """Print greeting; returns nothing."""
    print(f"Hello, {name}!")

print("=== BASIC TYPE ANNOTATIONS ===")
print("Sum:", add_numbers(num1=3, num2=5))
greet_user(name="Alice")
print()


# ------------------------------------------------------------
# EXAMPLE 2 — OPTIONAL AND DEFAULT VALUES
# ------------------------------------------------------------
def describe_person(*, name: str, age: Optional[int] = None) -> str:
    """Return description; age can be omitted."""
    if age is None:
        return f"{name}, age unknown"
    return f"{name}, {age} years old"

print("=== OPTIONAL ARGUMENTS ===")
print(describe_person(name="Bob", age=30))
print(describe_person(name="Charlie"))
print()


# ------------------------------------------------------------
# EXAMPLE 3 — COMPLEX TYPES
# ------------------------------------------------------------
def sum_numbers(*, numbers: list[float]) -> float:
    """Sum a list of floats."""
    return sum(numbers)

def create_user(**kwargs: Union[str, int]) -> dict[str, Union[str, int]]:
    """Return a dictionary representing a user."""
    return kwargs

print("=== COMPLEX TYPES ===")
print("Sum list:", sum_numbers(numbers=[1.2, 3.4, 5.6]))
user_dict = create_user(name="Eve", age=25)
print("User dict:", user_dict)
print()


# ------------------------------------------------------------
# EXAMPLE 4 — CALLABLES (functions as arguments)
# ------------------------------------------------------------
def apply_operation(*, num1: int, num2: int, func: Callable[[int, int], int]) -> int:
    """Apply a function to two integers."""
    return func(num1, num2)

print("=== CALLABLE ARGUMENTS ===")
print("Multiply 3*4:", apply_operation(num1=3, num2=4, func=lambda x, y: x * y))
print("Add 5+6:", apply_operation(num1=5, num2=6, func=lambda x, y: x + y))
print()


# ------------------------------------------------------------
# EXAMPLE 5 — TYPE CHECKING AT RUNTIME
# ------------------------------------------------------------
def safe_add(*, num1: int, num2: int) -> int:
    """Check types manually."""
    if not isinstance(num1, int) or not isinstance(num2, int):
        raise TypeError("Arguments must be integers")
    return num1 + num2

print("=== RUNTIME TYPE CHECKING ===")
try:
    print(safe_add(num1=3, num2="5"))  # will raise TypeError
except TypeError as e:
    print("Error:", e)

print(safe_add(num1=7, num2=8))
print()


# ------------------------------------------------------------
# KEY POINTS
# ------------------------------------------------------------
# 1. Annotations improve readability and tooling support.
# 2. Use Optional[type] for values that can be None.
# 3. Use Union[type1, type2] for multiple acceptable types.
# 4. Use List[type], Dict[key_type, value_type] for collections.
# 5. Use Callable[[arg1_type, ...], return_type] for function arguments.
# 6. Annotations do NOT enforce type at runtime unless checked manually.
# ------------------------------------------------------------

print("=== SUMMARY OF TYPING AND ANNOTATIONS ===")
print("Type hints help readability, catching errors early, and tooling support.")
print("They are strongly recommended in large projects and team code.")
print("End of file: typing_and_annotations.py")
