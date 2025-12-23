# This module demonstrates strict, professional API design using:
#
#     - positional-only parameters declared with '/'
#     - keyword-only parameters declared with '*'
#     - a consistent rule that every parameter must belong
#       strictly to ONE category: positional-only OR keyword-only.
#       Never both.
#
# -------------- WHY THIS MATTERS (EXTENDED THEORY) ----------------
#
# In modern Python codebases (especially large teams and long-lived
# projects) function signatures serve as a *public contract*.
# Poorly defined signatures create:
#
#     - silent bugs due to argument mis-ordering
#     - API breakage when parameter names are changed
#     - unclear meaning of optional parameters
#     - unreadable call sites with “magic positional values”
#     - functions that are easy to misuse and hard to maintain
#
# Well-structured signatures improve:
#
#     API stability  
#     static analysis and type checking  
#     IDE autocompletion  
#     readability and self-documentation  
#     refactor safety  
#     predictable behavior  
#
# ------------------------------------------------------------------
#
# WHY KEYWORD-ONLY ARGUMENTS ARE OFTEN SUPERIOR
# ------------------------------------------------------------------
#
# Keyword-only parameters are ideal when:
#
#     - the parameter controls behavior
#     - there are many optional values
#     - passing the wrong value could silently break logic
#     - readability is more important than call brevity
#     - you want strong guarantees of API usage style
#
# They make call sites explicit:
#
#     process_data(values, /, *, round_result=True)
#
# This is self-documenting and safe.
#
# Drawbacks:
#     - If you rename a keyword-only parameter, ALL call sites break.
#     - Not ideal inside inner/nested functions (no IDE hints).
#     - Not suitable for mathematical helpers passed into other functions.
#
# ------------------------------------------------------------------
#
# WHY POSITIONAL-ONLY PARAMETERS ARE SOMETIMES NECESSARY
# ------------------------------------------------------------------
#
# Positional-only parameters:
#
#     def add(a, b, /): ...
#
# Guarantee that:
#
#     - callers cannot rely on internal parameter names
#     - renaming a, b will NOT break external code
#     - the function call is short and lightweight
#     - mathematical functions remain clean: sqrt(x), sin(x), pow(a, b)
#
# They protect the API and allow safe refactoring.
#
# ------------------------------------------------------------------
#
# HOW '/' AND '*' CREATE “THE IDEAL SIGNATURE”
# ------------------------------------------------------------------
#
# Python allows a very strict layout:
#
#     def func(pos1, pos2, /, mid1, mid2, *, key1, key2):
#
# Categories:
#     pos1, pos2 → positional-only  
#     mid1, mid2 → positional-or-keyword  
#     key1, key2 → keyword-only  
#
# This style:
#     - minimizes mistakes
#     - maximizes clarity
#     - is used in the Python standard library itself
#
# ------------------------------------------------------------------
#
# RULE OF CONSISTENCY
# ------------------------------------------------------------------
#
# A parameter should NEVER be passable in two different ways.
# It must be exclusively:
#
#     - positional-only
#     - keyword-only
#
# Mixed styles (allowing both) cause unpredictable APIs.
#
# ------------------------------------------------------------------
#
# WHEN NOT TO USE KEYWORD-ONLY (IMPORTANT)
# ------------------------------------------------------------------
#
# Avoid keyword-only parameters in:
#
#     - short mathematical functions
#     - inner/nested helper functions
#     - callbacks passed into higher-order functions
#     - hot performance-critical loops
#
# ------------------------------------------------------------------
#
# ADDITIONAL BEST PRACTICES
# ------------------------------------------------------------------
#
# • If a parameter is a *flag* → make it keyword-only.  
# • If a parameter is *data* → positional is fine.  
# • Optional parameters should almost always be keyword-only.  
# • More than 3 positional parameters → reconsider design.  
# • For public APIs, ALWAYS use '/' and '*' to enforce stability.  




# ================================================================
# 1. Bad example: no keyword-only arguments → easy to misuse
# ================================================================

def create_user_bad(name: str, age: int, active: bool) -> dict:
    """A function WITHOUT keyword-only args — unsafe API."""
    return {"name": name, "age": age, "active": active}


print("=== MISUSE WITHOUT KEYWORD-ONLY ===")
    # Wrong order, but Python allows it — silent bug.
user = create_user_bad("John", True, 25)
print("User:", user)

print()


# ================================================================
# 2. Safe version: keyword-only parameters
# ================================================================

def create_user(
    *,
    name: str,
    age: int,
    active: bool
) -> dict:
    return {"name": name, "age": age, "active": active}


print("=== SAFE KEYWORD-ONLY EXAMPLE ===")
try:
    # Wrong: trying to pass keyword-only args by position
    create_user("John", 20, True)
except TypeError as e:
    print("Caught error:", e)

user = create_user(name="John", age=20, active=True)
print("Correct:", user)
print()


# ================================================================
# 3. Positional-only parameters using '/'
# ================================================================

def multiply(x: float, y: float, /) -> float:
    """
    A mathematical helper should NOT expose parameter names.

    - x and y MUST be positional-only.
    - This avoids API breakage if parameter names ever change.
    """
    return x * y


print("=== POSITIONAL-ONLY EXAMPLE ===")
print("multiply(3.5, 4.2) =", round(multiply(3.5, 4.2), 3))

try:
    multiply(x=3.5, y=4.2)
except TypeError as e:
    print("Caught error:", e)

print()


# ================================================================
# 4. Combining '/' and '*' → strict, professional API layout
# ================================================================

def reverse_string(
    text: str,
    /,
    *,
    uppercase: bool = False
) -> str:
    """
    A function with clean API separation:

    - text → positional-only (main data)
    - uppercase → keyword-only (behavior modifier)

    Demonstrates the best pattern:
        main data = positional
        configuration = keyword
    """
    reversed_text = text[::-1]
    return reversed_text.upper() if uppercase else reversed_text


print("=== COMBINING '/' AND '*' ===")

# Correct usage
print(reverse_string("Hello"))
print(reverse_string("Hello", uppercase=True))

# Incorrect usage: passing positional-only argument by name
try:
    reverse_string(text="Hello")
except TypeError as e:
    print("Caught error:", e)

print()


# ================================================================
# 5. Practical API: strict separation for network/server config
# ================================================================

def configure_server(
    host: str,
    port: int,
    /,
    *,
    timeout: float,
    retries: int
):
    """
    Example of a robust public API.

    - host, port → positional-only (core data)
    - timeout, retries → keyword-only (behavior settings)

    This style prevents accidental misuse in large codebases.
    """
    print("=== configure_server() called ===")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Timeout: {timeout}")
    print(f"Retries: {retries}")


configure_server("example.com", 443, timeout=5.0, retries=3)

try:
    configure_server(host="example.com", port=443, timeout=5.0, retries=3)
except TypeError as e:
    print("ERROR:", e)

print()
