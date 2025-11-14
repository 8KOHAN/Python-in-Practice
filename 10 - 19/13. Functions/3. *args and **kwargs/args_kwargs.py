# ------------------------------------------------------------
# *ARGS AND **KWARGS IN PYTHON
# ------------------------------------------------------------
# *args  - collects extra POSITIONAL arguments into a tuple.
# **kwargs - collects extra KEYWORD arguments into a dictionary.
# Both mechanisms provide flexibility but should be used carefully.
# ------------------------------------------------------------

# ------------------------------------------------------------
# EXAMPLE 1 — Using *args (positional arguments collector)
# ------------------------------------------------------------
def sum_all(*numbers: int) -> int:
    """Return the sum of all provided positional integer arguments."""
    return sum(numbers)

print("=== *ARGS EXAMPLE ===")
print(sum_all(1, 2, 3, 4))
print()


# ------------------------------------------------------------
# EXAMPLE 2 — Using **kwargs (keyword arguments collector)
# ------------------------------------------------------------
def print_user_info(**info: str) -> None:
    """Print key-value pairs received as keyword arguments."""
    for key, value in info.items():
        print(f"{key}: {value}")

print("=== **KWARGS EXAMPLE ===")
print_user_info(name="Alice", city="Berlin", age=26)
print()


# ------------------------------------------------------------
# EXAMPLE 3 — Combining *args and **kwargs
# ------------------------------------------------------------
def demo(*args: int, **kwargs: str) -> None:
    """Demonstrate receiving both positional and keyword arguments."""
    print("Positional args:", args)
    print("Keyword args:", kwargs)

print("=== COMBINED *ARGS + **KWARGS ===")
demo(10, 20, 30, name="Alice", role="admin")
print()


# ------------------------------------------------------------
# EXAMPLE 4 — Restricting arguments: normal + args + kwargs
# ------------------------------------------------------------
def process_user(id: int, *scores: float, **meta: str) -> None:
    """
    Demonstrates a function with:
      - a required positional argument (id)
      - variable number of scores (*scores)
      - metadata via keyword arguments (**meta)
    """
    print(f"ID: {id}")
    print("Scores:", scores)
    print("Metadata:", meta)

print("=== MIXED SIGNATURE ===")
process_user(1001, 9.5, 8.7, 10.0, name="Bob", city="Paris")
print()


# ------------------------------------------------------------
# EXAMPLE 5 — BEST PRACTICE: *args for homogeneous data only
# ------------------------------------------------------------
# BAD PRACTICE:
# def process(*data):  # unclear what type data should contain
#     ...

# GOOD PRACTICE:
def multiply_all(*values: float) -> float:
    """Multiply all floats provided via *args."""
    result = 1.0
    for v in values:
        result *= v
    return result

print("=== BEST PRACTICE FOR *ARGS ===")
print(multiply_all(1.5, 2.0, 3.0))
print()


# ------------------------------------------------------------
# EXAMPLE 6 — BEST PRACTICE: **kwargs for optional config
# ------------------------------------------------------------
def render_text(text: str, **options: str) -> None:
    """Render text with optional styling passed through **kwargs."""
    style = ", ".join(f"{k}={v}" for k, v in options.items()) or "no styling"
    print(f"TEXT: '{text}' | OPTIONS: {style}")

print("=== BEST PRACTICE FOR **KWARGS ===")
render_text("Hello world", color="blue", weight="bold")
render_text("No styles here")
print()
