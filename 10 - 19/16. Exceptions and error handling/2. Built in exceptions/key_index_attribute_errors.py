"""
Demonstration of KeyError, IndexError, and AttributeError:
what they signal, how they differ, and how to work with them correctly.
"""

from __future__ import annotations


# ----------------------------------------
# 1) KeyError BASICS
# ----------------------------------------

def key_error_basic_demo() -> None:
    print("=== key_error_basic_demo ===")

    # KeyError is raised when a mapping (usually a dict)
    # does not contain the requested key.
    #
    # Important:
    # - The container exists
    # - The key lookup operation itself is valid
    # - The specific key is missing

    data: dict[str, int] = {
        "a": 1,
        "b": 2,
    }

    try:
        value: int = data["c"]
        print(f"Value: {value}")
    except KeyError as exc:
        # KeyError contains the missing key as its argument.
        print(f"KeyError caught, missing key: {exc}")

    print()


# ----------------------------------------
# 2) KeyError VS SAFE ACCESS
# ----------------------------------------

def key_error_vs_get_demo() -> None:
    print("=== key_error_vs_get_demo ===")

    data: dict[str, int] = {
        "x": 10,
        "y": 20,
    }

    # Using dict.get() avoids KeyError,
    # but silently returns None (or a default value).
    #
    # This can be useful, but it can also hide bugs
    # if a missing key is actually an error condition.

    value: int | None = data.get("z")

    if value is None:
        print("Key is missing, but no exception was raised")
    else:
        print(f"Value: {value}")

    print()


# ----------------------------------------
# 3) IndexError BASICS
# ----------------------------------------

def index_error_basic_demo() -> None:
    print("=== index_error_basic_demo ===")

    # IndexError is raised when accessing a sequence
    # (list, tuple, string) with an invalid index.
    #
    # The type of the index is correct,
    # but it is outside the valid range.

    values: list[int] = [1, 2, 3]

    try:
        value: int = values[10]
        print(f"Value: {value}")
    except IndexError as exc:
        print(f"IndexError caught: {exc}")

    print()


# ----------------------------------------
# 4) IndexError VS LENGTH CHECKS
# ----------------------------------------

def index_error_vs_len_check_demo() -> None:
    print("=== index_error_vs_len_check_demo ===")

    values: list[int] = [10, 20, 30]
    index: int = 5

    # Checking length manually is a common pattern,
    # but it can make code more verbose and error-prone.
    #
    # In many cases, relying on IndexError
    # leads to clearer and more robust logic.

    try:
        value: int = values[index]
        print(f"Value: {value}")
    except IndexError:
        print("Index out of range")

    print()


# ----------------------------------------
# 5) AttributeError BASICS
# ----------------------------------------

def attribute_error_basic_demo() -> None:
    print("=== attribute_error_basic_demo ===")

    # AttributeError is raised when accessing
    # a non-existent attribute on an object.
    #
    # The object exists,
    # but the requested attribute does not.

    number: int = 42

    try:
        result = number.non_existent_attribute
        print(result)
    except AttributeError as exc:
        print(f"AttributeError caught: {exc}")

    print()


# ----------------------------------------
# 6) AttributeError VS DUCK TYPING
# ----------------------------------------

def attribute_error_and_duck_typing_demo() -> None:
    print("=== attribute_error_and_duck_typing_demo ===")

    # Duck typing relies on trying an operation
    # and handling AttributeError if the object
    # does not provide the expected interface.

    class FileLike:
        def read(self) -> str:
            return "data"

    def read_from_object(obj: object) -> str:
        try:
            return obj.read()  # type: ignore[attr-defined]
        except AttributeError:
            return "Object does not support reading"

    print(read_from_object(FileLike()))
    print(read_from_object(123))

    print()


# ----------------------------------------
# 7) KEY / INDEX / ATTRIBUTE — SUMMARY
# ----------------------------------------

def key_index_attribute_summary_demo() -> None:
    print("=== key_index_attribute_summary_demo ===")

    # KeyError:
    # - Missing key in a mapping
    #
    # IndexError:
    # - Invalid index for a sequence
    #
    # AttributeError:
    # - Missing attribute on an object
    #
    # All three signal:
    # "The container/object exists, but the lookup failed"

    examples: list[tuple[str, BaseException]] = [
        ("{'a': 1}['b']", KeyError("b")),
        ("[1, 2, 3][10]", IndexError("list index out of range")),
        ("42.foo", AttributeError("'int' object has no attribute 'foo'")),
    ]

    for expression, error in examples:
        print(f"{expression} -> {type(error).__name__}")

    print()


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    key_error_basic_demo()
    key_error_vs_get_demo()
    index_error_basic_demo()
    index_error_vs_len_check_demo()
    attribute_error_basic_demo()
    attribute_error_and_duck_typing_demo()
    key_index_attribute_summary_demo()
