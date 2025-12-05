# -----------------------------
# INTRODUCTION
# -----------------------------
# A list in Python is a mutable (changeable) sequence that can store multiple items.
# It can contain elements of any type, including other lists.

# -----------------------------
# LIST CREATION
# -----------------------------
from typing import Any
import copy

numbers: list[int] = [10, 20, 30, 40, 50]
fruits: list[str] = ["apple", "banana", "cherry"]
mixed: list[Any] = [1, "hello", 3.14, True, None]

print("=== LIST CREATION ===")
print("numbers:", numbers)
print("fruits:", fruits)
print("mixed:", mixed)
print("Type of 'numbers':", type(numbers))
print()

# -----------------------------
# ACCESSING ELEMENTS
# -----------------------------
print("=== ACCESSING ELEMENTS ===")
print("First element:", fruits[0])
print("Second element:", fruits[1])
print("Last element:", fruits[-1])  # negative index = from the end
print("Slice [1:3]:", numbers[1:3])
print("Every second element:", numbers[::2])
print()

# -----------------------------
# MODIFYING LISTS
# -----------------------------
print("=== MODIFYING LISTS ===")
fruits[1] = "blueberry"  # change element
print("After modification:", fruits)

fruits.append("mango")  # add one element
print("After append:", fruits)

fruits.insert(1, "kiwi")  # insert at index
print("After insert:", fruits)

fruits.extend(["pear", "melon"])  # add multiple
print("After extend:", fruits)

removed = fruits.pop(2)  # remove by index
print("After pop:", fruits, "-> removed:", removed)

fruits.remove("apple")  # remove by value
print("After remove 'apple':", fruits)
print()

# -----------------------------
# LIST FUNCTIONS AND METHODS
# -----------------------------
print("=== LIST FUNCTIONS AND METHODS ===")
print("Length of numbers:", len(numbers))
print("Sum of numbers:", sum(numbers))
print("Max of numbers:", max(numbers))
print("Min of numbers:", min(numbers))
print("Count of 20:", numbers.count(20))
print("Index of 30:", numbers.index(30))

numbers.reverse()
print("Reversed list:", numbers)

numbers.sort()
print("Sorted list:", numbers)

numbers.sort(reverse=True)
print("Sorted descending:", numbers)
print()

# -----------------------------
# ITERATION
# -----------------------------
print("=== ITERATION ===")
for fruit in fruits:
    print("Fruit:", fruit)
print()

# Enumerate gives index + value
for index, value in enumerate(numbers):
    print(f"Index {index}: {value}")
print()

# -----------------------------
# NESTED LISTS (2D LISTS)
# -----------------------------
print("=== NESTED LISTS ===")
matrix: list[list[int]] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print("Matrix:", matrix)
print("Element [0][1]:", matrix[0][1])  # 2
print("Row 2:", matrix[1])

# Flattening a nested list (turn 2D → 1D)
flat: list[int] = [num for row in matrix for num in row]
print("Flattened list:", flat)
print()

# -----------------------------
# LIST COPYING
# -----------------------------
print("=== LIST COPYING ===")
a: list[int] | list[list[int]] = [1, 2, 3]
b: list[int] | list[list[int]] = a  # same list (reference)
c: list[int] | list[list[int]] = a.copy()  # real copy

a.append(4)
print("a:", a)
print("b (same reference):", b)
print("c (independent copy):", c)
print()

# -----------------------------
# MEMBERSHIP TESTING
# -----------------------------
print("=== MEMBERSHIP TESTING ===")
print("Is 20 in numbers?", 20 in numbers)
print("Is 100 not in numbers?", 100 not in numbers)
print("Is 'banana' in fruits?", "banana" in fruits)
print()

# -----------------------------
# LIST COMPREHENSIONS
# -----------------------------
print("=== LIST COMPREHENSIONS ===")
squares: list[int] = [x**2 for x in range(1, 6)]
print("Squares 1–5:", squares)

evens: list[int] = [x for x in range(10) if x % 2 == 0]
print("Even numbers:", evens)

upper_fruits: list[str] = [fruit.upper() for fruit in fruits]
print("Uppercase fruits:", upper_fruits)
print()

# -----------------------------
# COMMON ERRORS
# -----------------------------
print("=== COMMON ERRORS ===")
try:
    print(fruits[100])  # IndexError
except IndexError as e:
    print("Error:", e)

try:
    fruits.remove("orange")  # ValueError
except ValueError as e:
    print("Error:", e)
print()

# -----------------------------
# SUMMARY OUTPUT
# -----------------------------
print("=" * 40)
print("        LISTS DEMONSTRATION COMPLETE        ")
print("=" * 40)
print(f"Final fruits list: {fruits}")
print(f"Final numbers list: {numbers}")
print(f"Matrix flatten: {flat}")
print("=" * 40)

# ---------------------------------------------
# COPYING LISTS — SHALLOW VS DEEP COPY
# ---------------------------------------------
print("# Copying Lists — shallow vs deep copy")
print("# --------------------------------------")

# Create a nested list (list inside list)
a: list[list[int]] = [[1, 2], [3, 4]]

# SHALLOW COPY: creates a new outer list, but inner lists are shared
b: list[list[int]] = a.copy()

# DEEP COPY: creates a completely independent copy (new inner and outer lists)
c: list[list[int]] = copy.deepcopy(a)

print("Initial state:")
print("a =", a)
print("b =", b)
print("c =", c)
print(f"IDs -> a: {id(a)}, b: {id(b)}, c: {id(c)}")

print("\nNow modify b[0]:")
b[0].append(99)  # This changes the shared inner list
print("a =", a)
print("b =", b)
print("c =", c)
print("Notice: a changed too, because b[0] and a[0] are the same list!")
print()

# Let's confirm inner list IDs to prove the sharing:
print("Inner list IDs:")
print(f"a[0]: {id(a[0])}")
print(f"b[0]: {id(b[0])}")
print(f"c[0]: {id(c[0])}")
print("=> a[0] and b[0] share the same ID (same inner list).")
print("=> c[0] has a different ID (independent inner list).")
print()

# Modify the deep copy (c) — should not affect a or b
c[1].append(42)
print("After modifying c:")
print("a =", a)
print("b =", b)
print("c =", c)
print("Only c changed, because deepcopy created fully independent objects.")
print()
