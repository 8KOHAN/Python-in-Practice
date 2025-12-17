# ------------------------------------------------------------
# NONLOCAL KEYWORD — EXPLAINED
# ------------------------------------------------------------
# The `nonlocal` keyword is used to modify a variable
# that is defined in an enclosing (outer) function scope.
#
# Scope levels in Python:
# 1. Local      — inside the current function
# 2. Enclosing  — inside an outer function (for nested functions)
# 3. Global     — module-level variables
# 4. Built-in   — Python built-ins
#
# `nonlocal` works ONLY with enclosing scope.
# It does NOT work with global variables.
# ------------------------------------------------------------


# ------------------------------------------------------------
# EXAMPLE 1 — Problem without nonlocal
# ------------------------------------------------------------
def counter_without_nonlocal() -> None:
    """Demonstrates why nonlocal is needed."""
    count: int = 0

    def increment() -> None:
        # This creates a NEW local variable `count`
        # instead of modifying the outer one
        count = count + 1  # UnboundLocalError

    try:
        increment()
    except UnboundLocalError as error:
        print("Error without nonlocal:", error)


print("=== WITHOUT NONLOCAL ===")
counter_without_nonlocal()
print()


# ------------------------------------------------------------
# EXAMPLE 2 — Correct usage of nonlocal
# ------------------------------------------------------------
def counter_with_nonlocal() -> None:
    """Uses nonlocal to modify enclosing scope variable."""
    count: int = 0

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    print("Increment 1:", increment())
    print("Increment 2:", increment())
    print("Increment 3:", increment())


print("=== WITH NONLOCAL ===")
counter_with_nonlocal()
print()


# ------------------------------------------------------------
# EXAMPLE 3 — nonlocal enables stateful closures
# ------------------------------------------------------------
def make_counter(start: int = 0, /):
    """
    Factory function that creates a stateful counter.
    Demonstrates a real-world use of nonlocal.
    """
    value: int = start

    def counter() -> int:
        nonlocal value
        value += 1
        return value

    return counter


print("=== STATEFUL CLOSURE WITH NONLOCAL ===")
counter_a = make_counter(10)
counter_b = make_counter(100)

print(counter_a())  # 11
print(counter_a())  # 12
print(counter_b())  # 101
print(counter_b())  # 102
print()


# ------------------------------------------------------------
# EXAMPLE 4 — nonlocal vs global
# ------------------------------------------------------------
value: int = 999  # global variable

def outer() -> None:
    value: int = 10  # enclosing variable

    def inner() -> None:
        nonlocal value
        value += 1
        print("Inner value:", value)

    inner()
    inner()
    print("Outer value after calls:", value)


print("=== NONLOCAL DOES NOT TOUCH GLOBAL ===")
outer()
print("Global value remains unchanged:", value)
print()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("=== SUMMARY ===")
print("nonlocal allows modification of enclosing scope variables")
print("nonlocal works only with nested functions")
print("nonlocal does NOT work with global scope")
print("nonlocal is essential for closures with state")
