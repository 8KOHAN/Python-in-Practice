# ------------------------------------------------------------
# TYPING AND ANNOTATIONS — MODERN AND PRE-3.10 COMPARISON
# ------------------------------------------------------------
# Python type hints improve readability, reduce ambiguity,
# and allow tools (IDE, linters, type checkers) to detect errors early.
#
# This file demonstrates:
#   1. Pre-Python-3.10 typing style (Union, Optional, List, Dict)
#   2. Modern Python 3.10+ typing style (| operator, list[...] etc.)
#   3. Advanced typing features (TypedDict, Literal, Protocol)
#
# Type hints DO NOT enforce runtime safety unless explicitly checked.
# ------------------------------------------------------------

from typing import (
    Optional,
    Union,
    List,
    Dict,
    Callable,
    TypedDict,
    Literal,
    Protocol,
)


print("=== TYPING AND ANNOTATIONS DEMO ===")
print()


# ------------------------------------------------------------
# SECTION 1 — BASIC FUNCTION ANNOTATIONS
# ------------------------------------------------------------
def castom_sum(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def format_name(*, first: str, last: str) -> str:
    """Return a formatted full name."""
    return f"{first} {last}"


print("=== BASIC ANNOTATIONS ===")
print(castom_sum(5, 10))
print(format_name(first="Ada", last="Lovelace"))
print()


# ------------------------------------------------------------
# SECTION 2 — PRE-PYTHON-3.10 STYLE (OLD TYPING SYNTAX)
# ------------------------------------------------------------
# Old style used capitalized containers and Union/Optional.

def sum_list_old(*, numbers: List[float]) -> float:
    """Sum a list of floats using old-style List[...] annotation."""
    return sum(numbers)


def parse_value_old(*, value: Union[int, float, str]) -> str:
    """Accept int | float | str using old 'Union' style."""
    return f"Received: {value}"


def get_user_age_old(*, age: Optional[int]) -> str:
    """Old Optional[T] style."""
    return "Unknown age" if age is None else f"Age: {age}"


print("=== OLD PRE-3.10 TYPING STYLE ===")
print(sum_list_old(numbers=[1.5, 2.5, 3.5]))
print(parse_value_old(value="Hello"))
print(get_user_age_old(age=None))
print()


# ------------------------------------------------------------
# SECTION 3 — MODERN PYTHON 3.10+ TYPING
# ------------------------------------------------------------
# Python 3.10 simplified many type annotations:
#   Union[X, Y] -> X | Y
#   Optional[X] -> X | None
#   List[X] -> list[X]
#   Dict[K, V] -> dict[K, V]


def sum_list(*, numbers: list[float]) -> float:
    """Modern list[float] syntax."""
    return sum(numbers)


def parse_value(*, value: int | float | str) -> str:
    """Modern union syntax using | operator."""
    return f"Received: {value}"


def get_user_age(*, age: int | None) -> str:
    """Modern Optional[int] equivalent."""
    return "Unknown age" if age is None else f"Age: {age}"


print("=== MODERN PYTHON 3.10+ TYPING STYLE ===")
print(sum_list(numbers=[10.0, 20.0, 30.0]))
print(parse_value(value=42))
print(get_user_age(age=18))
print()


# ------------------------------------------------------------
# SECTION 4 — CALLABLE ANNOTATIONS
# ------------------------------------------------------------
def apply_function(
    a: int,
    b: int,
    /,
    *,
    func: Callable[[int, int], int]
) -> int:
    """Apply a math operation to two integers."""
    return func(a, b)


print("=== CALLABLE EXAMPLE ===")
print(apply_function(3, 4, func=lambda x, y: x * y))
print()


# ------------------------------------------------------------
# SECTION 5 — TYPEDDICT (STRUCTURED DICTIONARY)
# ------------------------------------------------------------
class User(TypedDict):
    id: int
    name: str
    active: bool


def create_user(*, user_id: int, name: str) -> User:
    """Return a dictionary matching the User TypedDict structure."""
    return {"id": user_id, "name": name, "active": True}


print("=== TYPEDDICT ===")
print(create_user(user_id=1, name="Grace"))
print()


# ------------------------------------------------------------
# SECTION 6 — LITERAL TYPES (RESTRICTED VALUES)
# ------------------------------------------------------------
def set_mode(*, mode: Literal["debug", "release", "test"]) -> str:
    """Accept only specific string values."""
    return f"Mode set to: {mode}"


print("=== LITERAL TYPES ===")
print(set_mode(mode="debug"))
print()


# ------------------------------------------------------------
# SECTION 7 — PROTOCOLS (STRUCTURAL TYPING)
# ------------------------------------------------------------
# Protocols allow describing behavior without requiring inheritance.
#
# NOTE ABOUT PROTOCOLS AND THIS EXAMPLE:
# --------------------------------------
# This example is valid and demonstrates correct usage of Protocols.
# Protocols implement *structural typing*: an object is accepted if it
# has the required methods/attributes — regardless of inheritance.
#
# However, in real production code this pattern should be used carefully:
#
# 1. Protocols are most useful when you design "behavior-based" APIs
#    (e.g., something that can be called, saved, logged, processed, etc.)
#    without forcing users to inherit from a specific base class.
#
# 2. But for very small, simple cases — like different greeter classes —
#    a Protocol can be unnecessary overhead. A simple base class or even
#    duck-typing (calling .greet() directly) is often enough.
#
# 3. Protocols shine when:
#       - You work with external libraries
#       - You expect many implementations from different teams
#       - You want mypy/pyright to validate that objects implement
#         certain behavior *without coupling them through inheritance*
#
# 4. The important point:
#       This example is correct, but it is intentionally minimalistic.
#       In real projects, Protocols are most beneficial when the interface
#       describes *meaningful, stable behavior*, not a trivial one-method class.
#
# So: the example itself is fine, but do not overuse Protocols for trivial
# cases — use them when structural typing meaningfully improves flexibility.



class Greeter(Protocol):
    def greet(self) -> str:
        pass


class EnglishGreeter:
    def greet(self) -> str:
        return "Hello!"


class SpanishGreeter:
    def greet(self) -> str:
        return "¡Hola!"


def run_greeting(*, greeter: Greeter) -> None:
    """Accept any object that matches the Greeter protocol."""
    print(greeter.greet())


print("=== PROTOCOLS ===")
run_greeting(greeter=EnglishGreeter())
run_greeting(greeter=SpanishGreeter())
print()


# ------------------------------------------------------------
# SECTION 8 — RUNTIME TYPE CHECKING
# ------------------------------------------------------------
def safe_add(*, x: int, y: int) -> int:
    """Demonstrate that type hints do NOT enforce runtime behavior."""
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Arguments must be integers")
    return x + y


print("=== RUNTIME TYPE CHECKING ===")
try:
    safe_add(x=3, y="7")
except TypeError as e:
    print("Caught error:", e)
print(safe_add(x=10, y=20))
print()
