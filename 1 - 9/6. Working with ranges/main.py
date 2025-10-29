# -----------------------------
# BASIC USAGE OF range()
# -----------------------------
print("BASIC RANGE EXAMPLES:")

# range(stop)
for i in range(5):
    print(i, end=" ")  # 0, 1, 2, 3, 4
print("\n")

# range(start, stop)
for i in range(2, 7):
    print(i, end=" ")  # 2, 3, 4, 5, 6
print("\n")

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i, end=" ")  # 0, 2, 4, 6, 8
print("\n")

# Negative step (reverse)
for i in range(10, 0, -2):
    print(i, end=" ")  # 10, 8, 6, 4, 2
print("\n")

# -----------------------------
# CONVERTING range() TO LIST OR TUPLE
# -----------------------------
print("Converting range to list and tuple:")

numbers_list = list(range(1, 6))
numbers_tuple = tuple(range(1, 6))

print("List:", numbers_list)
print("Tuple:", numbers_tuple)
print()

# -----------------------------
# USING range() IN LOOPS
# -----------------------------
print("Using range in loops:")
for i in range(3):
    print(f"Iteration {i + 1}: Hello, world!")
print()

# -----------------------------
# SUM, MIN, MAX, LEN with range()
# -----------------------------
print("Using built-in functions with range:")

r = range(1, 11)  # 1 to 10
print("Sum of numbers 1..10 =", sum(r))
print("Min =", min(r))
print("Max =", max(r))
print("Count =", len(r))
print()

# -----------------------------
# RANGE IN CONDITIONAL EXPRESSIONS
# -----------------------------
print("Checking if a number belongs to a range:")
x = int(input("Enter a number (1-10): "))

if x in range(1, 11):
    print(f"{x} is within the range 1–10.")
else:
    print(f"{x} is out of range!")
print()

# -----------------------------
# USING RANGE IN LIST COMPREHENSIONS
# -----------------------------
print("List comprehension with range:")
squares = [n ** 2 for n in range(1, 6)]
print("Squares 1–5:", squares)
print()

# -----------------------------
# MULTIPLE NESTED RANGES (TABLE)
# -----------------------------
print("Multiplication table using range:")
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i * j:3}", end=" ")
    print()
print()

# -----------------------------
# RANGE DOES NOT CREATE A REAL LIST
# -----------------------------
print("Memory efficiency of range:")
big_range = range(1_000_000_000)
print("Range created successfully!")
print("It doesn’t take much memory because range() is lazy (it generates numbers on demand).")
print()

# -----------------------------
# ADVANCED: CUSTOM STEP CALCULATIONS
# -----------------------------
print("Custom step example:")
for i in range(0, 21, 5):
    print(f"Step {i // 5}: value = {i}")
print()

