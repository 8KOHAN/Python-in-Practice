# data_input_output.py

# -----------------------------
# SAFE INPUT FUNCTION
# -----------------------------
def get_int(prompt):
    """Safely read an integer from user input."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter an integer number.")

def get_float(prompt):
    """Safely read a float from user input."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter a number (use '.' for decimals).")


# -----------------------------
# BASIC INPUT WITH ERROR HANDLING
# -----------------------------
name = input("Enter your name: ").strip()  # strip() removes extra spaces
if not name:
    name = "Anonymous"

print(f"Hello, {name}!")
print()

# -----------------------------
# CONVERTING INPUT DATA TYPES SAFELY
# -----------------------------
age = get_int("Enter your age: ")
height = get_float("Enter your height (in meters): ")

print(f"You are {age} years old and {height} meters tall.")
print()

# -----------------------------
# MULTIPLE INPUTS IN ONE LINE WITH VALIDATION
# -----------------------------
while True:
    try:
        print("Enter two integers separated by space:")
        a, b = map(int, input().split())
        break
    except ValueError:
        print("Error: please enter two valid integer numbers!")

print(f"a = {a}, b = {b}, sum = {a + b}")
print()

# -----------------------------
# LIST INPUT AND PROCESSING WITH VALIDATION
# -----------------------------
while True:
    try:
        print("Enter several integers separated by space:")
        numbers = list(map(int, input().split()))
        if len(numbers) == 0:
            raise ValueError("Empty input!")
        break
    except ValueError:
        print("Error: please enter valid numbers separated by spaces!")

print("You entered:", numbers)
print("Sum =", sum(numbers))
print("Max =", max(numbers))
print("Min =", min(numbers))
print()

# -----------------------------
# STRING INPUT PROCESSING
# -----------------------------
sentence = input("Enter a sentence: ").strip()
if not sentence:
    print("You entered an empty sentence.")
else:
    words = sentence.split()
    print("Words in your sentence:", words)
    print("Number of words:", len(words))
print()

# -----------------------------
# FORMATTED OUTPUT
# -----------------------------
pi = 3.1415926535
radius = get_float("Enter circle radius: ")
area = pi * (radius ** 2)
print(f"Circle area with radius {radius} = {area:.3f}")
print()

# -----------------------------
# OUTPUT EXAMPLES
# -----------------------------
print("Processing", end="")
print(".", end="")
print(".", end="")
print(". Done!\n")

print("Values with custom separator:")
print(10, 20, 30, 40, sep=" | ")
print()
