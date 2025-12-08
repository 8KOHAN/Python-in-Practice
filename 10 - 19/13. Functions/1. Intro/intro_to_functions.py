# ------------------------------------------------------------
# INTRODUCTION TO FUNCTIONS — ENGINEERING PERSPECTIVE
# ------------------------------------------------------------
# A function is NOT "just a block of code" and NOT "anything you
# move out of the main program to avoid repetition".
#
# A proper function is:
# -> a named, reusable, well-defined unit of behavior
# -> performing one clear and meaningful task
# -> operating at a consistent level of abstraction
#
# A good function answers the question:
#     "What does this action MEAN in the domain of this program?"
#
# Examples of good function names:
#     calculate_tax(), validate_user(), format_date(), read_config()
#
# Examples of BAD function names:
#     do_stuff(), handle(), process(), helper(), util()
#
# Functions are fundamental to:
# - structuring code
# - avoiding complexity growth
# - making the program readable
# - enabling testing
# - enabling code reuse without duplication of meaning
#
# NOTE:
# Not every repeated piece of code should become a function.
# Repetition alone is NOT a reason to extract a function.
# A function must represent a meaningful, logical operation.
# ------------------------------------------------------------


# ------------------------------------------------------------
# EXAMPLE 1 — Bad function (no meaning, just reused code)
# ------------------------------------------------------------
def do_three_prints():  # BAD EXAMPLE
    """This is a bad example, it has no logical meaning."""
    print("Value:", 10)
    print("Value:", 20)
    print("Value:", 30)


print("=== BAD FUNCTION EXAMPLE ===")
do_three_prints()
print()


# ------------------------------------------------------------
# EXAMPLE 2 — Good function (has clear meaning)
# ------------------------------------------------------------
def print_values(*, values: list[int]) -> None:
    """
    Print all integers provided in a list.
    This function has a clear, single responsibility.
    """
    for item in values:
        print(f"Value: {item}")


print("=== GOOD FUNCTION EXAMPLE ===")
print_values(values=[10, 20, 30])
print()


# ------------------------------------------------------------
# EXAMPLE 3 — Functions improve readability
# ------------------------------------------------------------
print("=== INLINE LOGIC (BAD READABILITY) ===")
numbers = [1, 2, 3, 4, 5]
squared_inline = []
for n in numbers:
    squared_inline.append(n * n)
print("Inline squares:", squared_inline)


def square_list(*, values: list[int]) -> list[int]:
    """Return a new list where each element is squared."""
    return [v * v for v in values]


print("=== USING A FUNCTION FOR MEANING ===")
print("Squares:", square_list(values=numbers))
print()


# ------------------------------------------------------------
# EXAMPLE 4 — Levels of abstraction
# ------------------------------------------------------------
print("=== BAD MIXED ABSTRACTION ===")
print("User registered:")
print("name:", "Alice")
print("age:", 25)
print("email:", "alice@example.com")


def print_user(*, name: str, age: int, email: str) -> None:
    """Display user information in a readable format."""
    print("User registered:")
    print(f"  Name:  {name}")
    print(f"  Age:   {age}")
    print(f"  Email: {email}")


print("=== GOOD ABSTRACTION ===")
print_user(name="Alice", age=25, email="alice@example.com")
print()


# ------------------------------------------------------------
# EXAMPLE 5 — Default parameters (correct and incorrect usage)
# ------------------------------------------------------------
# A "default parameter" is a parameter that already has a value
# if the caller does not provide it.
#
# BUT default parameters must follow strict good practices:
# - Never use mutable defaults (lists, dicts, sets)
# - Use defaults only when they express meaningful behavior
# - Do NOT use defaults to hide missing arguments or design flaws


# ------------------------------------------------------------
# BAD EXAMPLE — Mutable default parameter
# ------------------------------------------------------------
def add_value_bad(*, value: int, container: list[int] = []):
    """
    BAD PRACTICE:
    The list 'container' is created only once.
    All calls share the same list => unexpected behavior.
    """
    container.append(value)
    return container


print("=== BAD DEFAULT PARAMETER EXAMPLE ===")
print(add_value_bad(value=10))  
print(add_value_bad(value=20))  # <- unexpected: list is shared!
print()


# ------------------------------------------------------------
# GOOD EXAMPLE — Correct immutable default
# ------------------------------------------------------------
def add_value_good(
    *,
    value: int,
    container: list[int] | None = None
) -> list[int]:
    """
    GOOD PRACTICE:
    Use None as default, then create a new list inside the function.
    Ensures isolation between calls.
    """
    if container is None:
        container = []
    container.append(value)
    return container


print("=== GOOD DEFAULT PARAMETER EXAMPLE ===")
print(add_value_good(value=10))
print(add_value_good(value=20))
print()


# ------------------------------------------------------------
# GOOD EXAMPLE — Default conveys meaningful behavior
# ------------------------------------------------------------
def greet_user(
    *,
    name: str,
    greeting: str = "Hello"
) -> None:
    """
    Here the default makes semantic sense:
    Most greetings are 'Hello', but caller may override.
    """
    print(f"{greeting}, {name}!")


print("=== MEANINGFUL DEFAULT EXAMPLE ===")
greet_user(name="Alice")
greet_user(name="Bob", greeting="Hi")
print()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("=== SUMMARY ===")
print("Functions should:")
print(" - represent meaningful actions")
print(" - follow single-responsibility")
print(" - improve readability")
print(" - operate at one consistent level of abstraction")
print(" - NOT exist only to remove duplicated lines")
print("End of introduction.")
