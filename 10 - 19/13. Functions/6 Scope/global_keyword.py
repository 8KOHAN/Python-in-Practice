# ------------------------------------------------------------
# THE "global" KEYWORD IN PYTHON
# ------------------------------------------------------------
# The 'global' keyword allows a function to MODIFY
# a variable defined in the global (module) scope.
#
# IMPORTANT:
# - Reading a global variable does NOT require 'global'
# - Modifying a global variable DOES require 'global'
#
# The use of 'global' tightly couples a function to external state
# and should generally be avoided in well-designed code.
# ------------------------------------------------------------


# ------------------------------------------------------------
# READING A GLOBAL VARIABLE (NO 'global' REQUIRED)
# ------------------------------------------------------------
counter: int = 10  # global variable

def read_counter() -> None:
    """Read-only access to a global variable."""
    print("Counter value:", counter)

print("=== READING GLOBAL VARIABLE ===")
read_counter()
print()


# ------------------------------------------------------------
# MODIFYING A GLOBAL VARIABLE (REQUIRES 'global')
# ------------------------------------------------------------
def increment_counter() -> None:
    """
    Increment the global counter.
    This function modifies external state.
    """
    global counter
    counter += 1

print("=== MODIFYING GLOBAL VARIABLE ===")
increment_counter()
increment_counter()
print("Counter after increments:", counter)
print()


# ------------------------------------------------------------
# COMMON MISTAKE: FORGETTING 'global'
# ------------------------------------------------------------
def broken_increment() -> None:
    """
    This function will raise UnboundLocalError
    because Python treats 'counter' as local.
    """
    # counter += 1  # Uncommenting this line will cause an error
    pass

print("=== COMMON MISTAKE ===")
print(
    "If you try to modify a global variable without 'global', "
    "Python raises UnboundLocalError."
)
print()


# ------------------------------------------------------------
# WHY 'global' IS DANGEROUS
# ------------------------------------------------------------
# Example: function behavior depends on external hidden state

tax_rate: float = 0.2  # global configuration

def calculate_tax(amount: float, /) -> float:
    """
    Calculate tax using a global tax rate.
    This function is NOT pure and depends on hidden state.
    """
    return amount * tax_rate

print("=== HIDDEN DEPENDENCY EXAMPLE ===")
print("Tax for 100:", calculate_tax(100))

# Somewhere else in the program...
tax_rate = 0.25  # silently changes behavior

print("Tax for 100 after tax_rate change:", calculate_tax(100))
print()


# ------------------------------------------------------------
# BETTER APPROACH: PASS STATE EXPLICITLY
# ------------------------------------------------------------
def calculate_tax_explicit(amount: float, /, *, tax_rate: float) -> float:
    """
    Calculate tax using explicitly passed parameters.
    This function is pure and predictable.
    """
    return amount * tax_rate

print("=== EXPLICIT STATE (GOOD PRACTICE) ===")
print("Tax for 100:", calculate_tax_explicit(100, tax_rate=0.2))
print("Tax for 100:", calculate_tax_explicit(100, tax_rate=0.25))
print()


# ------------------------------------------------------------
# VALID USE CASES FOR 'global'
# ------------------------------------------------------------
# 'global' may be acceptable for:
# - simple scripts
# - quick prototypes
# - constants that never change (but usually better as config)
# - educational examples
#
# In production code, prefer:
# - passing parameters
# - using objects
# - closures
# - dependency injection
# ------------------------------------------------------------


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("=== SUMMARY ===")
print("1. 'global' allows modifying module-level variables")
print("2. Reading globals does not require 'global'")
print("3. Modifying globals does require 'global'")
print("4. 'global' creates hidden dependencies")
print("5. Prefer explicit parameters over global state")
