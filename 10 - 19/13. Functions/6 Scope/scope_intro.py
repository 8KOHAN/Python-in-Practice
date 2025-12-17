# ------------------------------------------------------------
# SCOPE IN PYTHON — INTRODUCTION
# ------------------------------------------------------------
# Scope defines where a variable is accessible in the program.
#
# Python follows the LEGB rule to resolve variable names:
#   L — Local
#   E — Enclosing
#   G — Global
#   B — Built-in
#
# Python searches for a variable in this exact order.
# Understanding scope is CRITICAL for writing predictable code.
# ------------------------------------------------------------


# ------------------------------------------------------------
# GLOBAL SCOPE
# ------------------------------------------------------------
x: int = 10  # global variable

def show_global() -> None:
    """Access a global variable (read-only)."""
    print("Inside function, x =", x)

print("=== GLOBAL SCOPE ===")
show_global()
print("Outside function, x =", x)
print()


# ------------------------------------------------------------
# LOCAL SCOPE
# ------------------------------------------------------------
def local_example() -> None:
    """Demonstrate local variable scope."""
    y: int = 5  # local variable
    print("Inside function, y =", y)

print("=== LOCAL SCOPE ===")
local_example()

# The following line would raise NameError if uncommented:
# print(y)
print()


# ------------------------------------------------------------
# LOCAL DOES NOT MODIFY GLOBAL
# ------------------------------------------------------------
counter = 0

def try_to_modify() -> None:
    """This creates a local variable, not modifying global one."""
    counter = 100  # local shadowing
    print("Inside function, counter =", counter)

print("=== LOCAL SHADOWING ===")
try_to_modify()
print("Outside function, counter =", counter)
print()


# ------------------------------------------------------------
# NAME RESOLUTION (LEGB RULE)
# ------------------------------------------------------------
value: str = "global value"

def outer() -> None:
    value: str = "enclosing value"

    def inner() -> None:
        value: str = "local value"
        print("Inner:", value)

    inner()
    print("Outer:", value)

print("=== LEGB RESOLUTION ===")
outer()
print("Global:", value)
print()


# ------------------------------------------------------------
# BUILT-IN SCOPE
# ------------------------------------------------------------
def builtin_example() -> None:
    """Use built-in names from built-in scope."""
    print("Length of list:", len([1, 2, 3]))

print("=== BUILT-IN SCOPE ===")
builtin_example()
print()


# ------------------------------------------------------------
# SHADOWING BUILT-IN NAMES (BAD PRACTICE)
# ------------------------------------------------------------
def bad_shadowing() -> None:
    """Shadowing built-in names is dangerous."""
    len = 100  # BAD: shadows built-in len
    print("Shadowed len:", len)

print("=== SHADOWING BUILT-IN (BAD PRACTICE) ===")
bad_shadowing()

# The built-in len is still available outside the function
print("Built-in len still works:", len([1, 2, 3]))
print()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("=== SUMMARY ===")
print("Python resolves names using LEGB rule.")
print("Local variables exist only inside their function.")
print("Assignment creates local scope unless declared otherwise.")
print("Avoid shadowing global and built-in names.")
