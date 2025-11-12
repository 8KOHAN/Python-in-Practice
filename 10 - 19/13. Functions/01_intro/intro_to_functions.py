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
def print_values(values: list[int]) -> None:
    """
    Print all integers provided in a list.
    This function has a clear, single responsibility.
    """
    for item in values:
        print(f"Value: {item}")


print("=== GOOD FUNCTION EXAMPLE ===")
print_values([10, 20, 30])
print()


# ------------------------------------------------------------
# EXAMPLE 3 — Functions improve readability
# ------------------------------------------------------------
# Bad approach: inline logic everywhere
print("=== INLINE LOGIC (BAD READABILITY) ===")
numbers = [1, 2, 3, 4, 5]
squared_inline = []
for n in numbers:
    squared_inline.append(n * n)
print("Inline squares:", squared_inline)

# Good approach: use a dedicated function
def square_list(values: list[int]) -> list[int]:
    """Return a new list where each element is squared."""
    return [v * v for v in values]

print("=== USING A FUNCTION FOR MEANING ===")
print("Squares:", square_list(numbers))
print()


# ------------------------------------------------------------
# EXAMPLE 4 — Levels of abstraction
# ------------------------------------------------------------
# BAD: mixed abstraction (low-level and high-level mixed)
print("=== BAD MIXED ABSTRACTION ===")
print("User registered:")
print("name:", "Alice")
print("age:", 25)
print("email:", "alice@example.com")

# GOOD: one meaningful function for one meaningful action
def print_user(name: str, age: int, email: str) -> None:
    """Display user information in a readable format."""
    print("User registered:")
    print(f"  Name:  {name}")
    print(f"  Age:   {age}")
    print(f"  Email: {email}")

print("=== GOOD ABSTRACTION ===")
print_user("Alice", 25, "alice@example.com")
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


