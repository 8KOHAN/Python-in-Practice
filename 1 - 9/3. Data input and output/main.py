# data_input_output.py

# -----------------------------
# SAFE INPUT FUNCTIONS
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
# FORMATTED OUTPUT (using f-strings)
# -----------------------------
pi = 3.1415926535
radius = get_float("Enter circle radius: ")
area = pi * (radius ** 2)
print(f"Circle area with radius {radius} = {area:.3f}")
print()

# -----------------------------
# PRINT FUNCTION CAPABILITIES
# -----------------------------

# Basic printing
print("Hello, world!")
print("Python", "is", "awesome!")
print()

# Separator (sep)
print("Using default separator:")
print("apple", "banana", "cherry")
print("\nUsing custom separator:")
print("apple", "banana", "cherry", sep=", ")
print("2025", "10", "27", sep="-")
print()

# End parameter
print("Loading", end="")
print(".", end="")
print(".", end="")
print(". Done!\n")

# Escape characters
print("Line1\nLine2\nLine3")  # new lines
print("Column1\tColumn2\tColumn3")  # tab spaces
print("Use \\ to print a backslash")
print("He said: \"Python is great!\"")
print()

# Printing variables
print("Name:", name, "Age:", age, "Score:", area)
print(f"Name: {name}, Age: {age}, Score: {area:.2f}")
print("Name: {}, Age: {}, Score: {:.2f}".format(name, age, area))
print()

# Number formatting
pi = 3.1415926535
print("Pi (2 decimals): {:.2f}".format(pi))
print(f"Pi (3 decimals): {pi:.3f}")
print("Pi as integer:", int(pi))
print()

# Alignment and width
print("Left aligned  :", f"{'Python':<10}rocks!")
print("Right aligned :", f"{'Python':>10}rocks!")
print("Centered      :", f"{'Python':^10}rocks!")
print()

# Multiline printing
print("""This is
a multi-line
string output.""")
print()

# Printing without spaces
print("Hello" + "World!")      # no space
print("Hello" + " " + "World!")  # manual space
print()

# Printing data structures
fruits = ["apple", "banana", "cherry"]
info = {"name": "Alice", "age": 25}
print("List:", fruits)
print("Dictionary:", info)
print()

# Custom ASCII styled output
print("=" * 30)
print("      USER INFORMATION      ")
print("=" * 30)
print(f"Name : {name}")
print(f"Age  : {age}")
print(f"Height: {height:.2f} m")
print(f"Score : {area:.2f}")
print("=" * 30)
print("End of output")
print()
