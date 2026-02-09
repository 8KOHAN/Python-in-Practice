"""
This file demonstrates common exception-related anti-patterns in Python.
Each section shows what should NOT be done and explains why it is problematic.
"""

from __future__ import annotations


# ----------------------------------------
# 1) CATCHING BASE Exception
# ----------------------------------------

def catching_base_exception_demo() -> None:
    print("=== catching_base_exception_demo ===")

    # Catching Exception hides too much information.
    # It swallows unrelated errors such as programming mistakes,
    # making debugging significantly harder.
    try:
        value: int = int("not-a-number")
    except Exception:
        # This is an anti-pattern.
        # We have no idea what exactly went wrong.
        print("Something went wrong, but we do not know what")

    # Correct approach (shown elsewhere in the project):
    # catch the most specific exception possible.

    print()


# ----------------------------------------
# 2) USING EXCEPTIONS FOR NORMAL CONTROL FLOW
# ----------------------------------------

def exceptions_for_control_flow_demo() -> None:
    print("=== exceptions_for_control_flow_demo ===")

    data: dict[str, int] = {"a": 1, "b": 2}

    # Anti-pattern: using KeyError as a normal branching mechanism
    try:
        value: int = data["c"]
        print("Value:", value)
    except KeyError:
        print("Key does not exist")

    # This situation is expected and common.
    # Using an exception here makes the code:
    # - harder to read
    # - slower
    # - misleading about what is truly exceptional

    print()


# ----------------------------------------
# 3) SILENTLY IGNORING EXCEPTIONS
# ----------------------------------------

def silent_exception_demo() -> None:
    print("=== silent_exception_demo ===")

    # Anti-pattern: completely ignoring exceptions
    try:
        result: float = 10 / 0
        print("Result:", result)
    except ZeroDivisionError:
        # The error is silently ignored.
        # The program continues in an invalid or unknown state.
        pass

    # Silent failures are extremely dangerous.
    # At minimum, exceptions should be logged or re-raised.

    print()


# ----------------------------------------
# 4) RAISING GENERIC EXCEPTIONS
# ----------------------------------------

def raising_generic_exception_demo() -> None:
    print("=== raising_generic_exception_demo ===")

    # Anti-pattern: raising Exception directly
    def process_value(value: int) -> None:
        if value < 0:
            raise Exception("Invalid value")

    try:
        process_value(-1)
    except Exception as exc:
        print("Caught generic exception:", exc)

    # Generic exceptions:
    # - do not communicate intent
    # - make it impossible to distinguish error categories
    # - break structured error handling

    print()


# ----------------------------------------
# 5) LOSING ORIGINAL EXCEPTION CONTEXT
# ----------------------------------------

def losing_context_demo() -> None:
    print("=== losing_context_demo ===")

    try:
        int("abc")
    except ValueError:
        # Anti-pattern: original exception context is lost
        raise RuntimeError("Failed to parse integer")

    # Without exception chaining, debugging becomes much harder.
    # Proper chaining with `raise ... from ...` is shown in other files.

    print()


# ----------------------------------------
# 6) OVERUSING TRY BLOCKS
# ----------------------------------------

def overly_broad_try_block_demo() -> None:
    print("=== overly_broad_try_block_demo ===")

    # Anti-pattern: wrapping too much code in a single try block
    try:
        numbers: list[int] = [1, 2, 3]
        index: int = 10
        value: int = numbers[index]
        result: float = value / 2
        print("Result:", result)
    except IndexError:
        print("Index error occurred")
    except ZeroDivisionError:
        print("Division error occurred")

    # Broad try blocks obscure which operation actually failed.
    # Prefer small, focused try blocks around the risky operation only.

    print()


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    catching_base_exception_demo()
    exceptions_for_control_flow_demo()
    silent_exception_demo()
    raising_generic_exception_demo()
    losing_context_demo()
    overly_broad_try_block_demo()
