# ---------------------------------------------------------------------------
# FUNCTIONS ARE OBJECTS
# ---------------------------------------------------------------------------
# In Python, functions are FIRST-CLASS OBJECTS:
# - They can be assigned to variables
# - They can be passed to other functions
# - They can be stored in collections
# - They can be returned from functions
# - They have attributes and metadata
# ---------------------------------------------------------------------------
from typing import Callable, Any


def greet(*, name: str) -> str:
    return f"Hello, {name}!"


# Assign function to a variable
say_hi = greet
print(say_hi(name="Alice"))
print()


# ---------------------------------------------------------------------------
# PASSING FUNCTIONS AS ARGUMENTS
# ---------------------------------------------------------------------------

def run_twice(*, func: Callable[[Any], Any], value: Any) -> Any:
    """Run a function twice on the same value."""
    return func(func(value))


def add_one(x: int) -> int:
    return x + 1


print(run_twice(func=add_one, value=5))  # (5 + 1) + 1 = 7
print()


# ---------------------------------------------------------------------------
# RETURNING FUNCTIONS FROM FUNCTIONS
# ---------------------------------------------------------------------------

def make_repeater(*, times: int) -> Callable[[str], str]:
    """Return a new function that repeats strings N times."""

    def repeater(text: str) -> str:
        return text * times

    return repeater


repeat_3 = make_repeater(times=3)
print(repeat_3("Hi"))
print()


# ---------------------------------------------------------------------------
# STORING FUNCTIONS IN DATA STRUCTURES
# ---------------------------------------------------------------------------
# Useful for strategy tables, command patterns, dispatchers.

def mul(x: int, y: int) -> int:
    return x * y


def sub(x: int, y: int) -> int:
    return x - y


operations: dict[str, Callable[[int, int], int]] = {
    "add": lambda a, b: a + b,
    "mul": mul,
    "sub": sub,
}

print(operations["add"](4, 7))
print(operations["mul"](3, 5))
print(operations["sub"](10, 6))
print()


# ---------------------------------------------------------------------------
# FUNCTIONS HAVE ATTRIBUTES
# ---------------------------------------------------------------------------
# Like any object, functions store fields.

def sample_function() -> None:
    pass

sample_function.description = "This is a custom attribute attached to a function object."

print(sample_function.description)
print()


# ---------------------------------------------------------------------------
# FUNCTIONS ARE OBJECT INSTANCES OF TYPE 'function'
# ---------------------------------------------------------------------------
print(type(greet))  # <class 'function'>
