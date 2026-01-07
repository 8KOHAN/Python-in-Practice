"""
Demonstrates common and dangerous mistakes when working with try/except.

This file focuses on patterns that look harmless,
but actively make code harder to debug, reason about, and maintain.
"""

from __future__ import annotations


# ----------------------------------------
# 1) BARE EXCEPT
# ----------------------------------------
# A bare `except:` catches *everything*, including:
#   - SystemExit
#   - KeyboardInterrupt
#   - GeneratorExit
#
# This almost always leads to broken program behavior
# and makes graceful shutdown impossible.

def bare_except_demo() -> None:
    print("=== bare_except_demo ===")

    try:
        print("Doing some work")
        raise KeyboardInterrupt
    except:
        # This block catches KeyboardInterrupt,
        # preventing the program from being interrupted properly.
        print("Exception swallowed")

    print()


# ----------------------------------------
# 2) EXCEPT EXCEPTION
# ----------------------------------------
# `except Exception:` is often treated as "safe".
# It is not.
#
# It still hides important information and
# usually signals poor error modeling.

def except_exception_demo() -> None:
    print("=== except_exception_demo ===")

    try:
        value: int = int("not_a_number")
    except Exception:
        # The original exception type and message
        # are discarded unless explicitly preserved.
        print("Something went wrong")

    print()


# ----------------------------------------
# 3) SILENT EXCEPT
# ----------------------------------------
# Catching an exception and doing nothing is one
# of the most harmful patterns.
#
# It creates the illusion of stability while
# silently corrupting program logic.

def silent_except_demo() -> None:
    print("=== silent_except_demo ===")

    numbers: list[str] = ["1", "x", "3"]

    results: list[int] = []

    for item in numbers:
        try:
            results.append(int(item))
        except ValueError:
            # The error is ignored completely.
            # The caller has no idea data was lost.
            pass

    print(f"Results: {results}")
    print()


# ----------------------------------------
# 4) TOO WIDE TRY BLOCK
# ----------------------------------------
# A wide try block obscures the real failure point.
# Debugging becomes guesswork instead of analysis.

def wide_try_block_demo() -> None:
    print("=== wide_try_block_demo ===")

    raw: str = "10"

    try:
        value: int = int(raw)
        result: int = value / 0
        print(result)
    except ZeroDivisionError:
        # Was the failure caused by parsing or division?
        # The try block gives no clear answer.
        print("Division by zero")

    print()


# ----------------------------------------
# 5) USING EXCEPT FOR NORMAL CONTROL FLOW
# ----------------------------------------
# Exceptions are for exceptional situations.
# Using them for normal branching hides intent
# and damages readability.

def exception_as_control_flow_demo() -> None:
    print("=== exception_as_control_flow_demo ===")

    data: dict[str, int] = {"a": 1}

    try:
        value: int = data["b"]
    except KeyError:
        # This should have been an explicit conditional.
        print("Key missing")

    print()


# ----------------------------------------
# 6) LOSING ORIGINAL EXCEPTION CONTEXT
# ----------------------------------------
# Raising a new exception without chaining
# destroys valuable debugging information.

def lost_context_demo() -> None:
    print("=== lost_context_demo ===")

    try:
        int("invalid")
    except ValueError:
        # The original ValueError is lost here.
        raise RuntimeError("Parsing failed")

    print()


# ----------------------------------------
# 7) WHAT THESE MISTAKES HAVE IN COMMON
# ----------------------------------------
# This section is intentionally theoretical.
#
# All patterns above share the same root problem:
#   - they trade short-term convenience
#     for long-term loss of information
#
# Good exception handling preserves:
#   - intent
#   - context
#   - failure boundaries
#
# These ideas will be revisited later
# when discussing exception chaining and design patterns.


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    bare_except_demo()
    except_exception_demo()
    silent_except_demo()
    wide_try_block_demo()
    exception_as_control_flow_demo()

    # lost_context_demo() is intentionally NOT executed here,
    # because it raises an unhandled exception and terminates the program.
