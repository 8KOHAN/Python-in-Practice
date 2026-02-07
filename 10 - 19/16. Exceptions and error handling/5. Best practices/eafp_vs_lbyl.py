"""
EAFP vs LBYL — Python Error Handling Philosophies.

This module demonstrates the two main styles for handling
potential errors in Python: *Easier to Ask Forgiveness than Permission* (EAFP)
and *Look Before You Leap* (LBYL).

Focus:
- How EAFP encourages handling exceptions
- How LBYL checks conditions before acting
- Pros and cons of each approach
- When to prefer one over the other
"""

from __future__ import annotations


# ----------------------------------------
# 1) EAFP: Easier to Ask Forgiveness than Permission
# ----------------------------------------
# In EAFP, you assume the operation will succeed and handle exceptions
# if something goes wrong. This is idiomatic in Python.

def eafp_demo(data: dict[str, int], key: str) -> None:
    """
    Demonstrate EAFP approach for dictionary access.
    """
    print("=== EAFP Demo ===")

    try:
        value: int = data[key]
        print(f"Value found: {value}")
    except KeyError:
        print(f"Key '{key}' not found!")
    print()


# ----------------------------------------
# 2) LBYL: Look Before You Leap
# ----------------------------------------
# In LBYL, you check conditions before performing operations
# to avoid exceptions. This style is more common in other languages.

def lbyl_demo(data: dict[str, int], key: str) -> None:
    """
    Demonstrate LBYL approach for dictionary access.
    """
    print("=== LBYL Demo ===")

    if key in data:
        value: int = data[key]
        print(f"Value found: {value}")
    else:
        print(f"Key '{key}' not found!")
    print()


# ----------------------------------------
# 3) COMPARISON
# ----------------------------------------
# - EAFP:
#     * More concise
#     * Handles race conditions better in concurrent code
#     * Pythonic style
# - LBYL:
#     * More explicit
#     * Can prevent exceptions from occurring
#     * Slightly more verbose

def compare_eafp_lbyl() -> None:
    """
    Compare both approaches with sample data.
    """
    sample: dict[str, int] = {"a": 1, "b": 2}

    # Existing key
    eafp_demo(sample, "a")
    lbyl_demo(sample, "a")

    # Missing key
    eafp_demo(sample, "u")
    lbyl_demo(sample, "u")


# ----------------------------------------
# 4) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    compare_eafp_lbyl()
