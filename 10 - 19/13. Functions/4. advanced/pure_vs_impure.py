# ------------------------------------------------------------
# PURE VS IMPURE FUNCTIONS
# ------------------------------------------------------------
# A *pure function*:
#   - depends ONLY on its input arguments
#   - does NOT modify external state
#   - does NOT read external state (global/local I/O)
#   - always returns the same result for the same input
#
# An *impure function*:
#   - reads or modifies external state
#   - has side effects (prints, writes files, modifies globals)
#   - result may change without changing the arguments
#
# Pure functions are much easier to test, debug, reason about,
# reuse, and combine into pipelines.
# ------------------------------------------------------------


# ------------------------------------------------------------
# EXAMPLE 1 — Pure function
# ------------------------------------------------------------
def add(*, num1: int, num2: int) -> int:
    """Return the sum of two integers (pure function)."""
    return num1 + num2


# ------------------------------------------------------------
# EXAMPLE 2 — Impure function (uses external state)
# ------------------------------------------------------------
counter: int = 0  # external mutable state

def increment_counter() -> int:
    """
    Increase global counter (impure function).
    This function depends on and modifies external state.
    """
    global counter
    counter += 1
    return counter


# ------------------------------------------------------------
# EXAMPLE 3 — Impure function (I/O side effects)
# ------------------------------------------------------------
def log_message(*, text: str) -> None:
    """
    Print a message (impure: printing is a side effect).
    """
    print(f"[LOG] {text}")


# ------------------------------------------------------------
# EXAMPLE 4 — Pure function used inside an impure context
# ------------------------------------------------------------
def calculate_discount(*, price: float, percent: float) -> float:
    """Return discounted price (pure calculation)."""
    return price - price * (percent / 100)


def apply_and_log(*, price: float, percent: float) -> float:
    """
    Impure wrapper: logs result (side effect),
    but core calculation remains pure inside.
    """
    result = calculate_discount(price=price, percent=percent)
    print(f"Discount applied: {result}")   # side effect → impure
    return result


if __name__ == "__main__":

    print("=== PURE FUNCTION ===")
    print(add(num1=3, num2=5))
    print(add(num1=3, num2=5))  # same input -> same output
    print()

    print("=== IMPURE FUNCTION (GLOBAL STATE) ===")
    print(increment_counter())
    print(increment_counter())
    print()

    print("=== IMPURE FUNCTION (SIDE EFFECT) ===")
    log_message(text="Something happened")
    print()

    print("=== PURE + IMPURE MIX ===")
    apply_and_log(price=100.0, percent=15.0)
