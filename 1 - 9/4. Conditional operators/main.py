# -----------------------------
# BASIC IF STATEMENT
# -----------------------------
x: int = 10

# Simple condition
if x > 5:
    print("x is greater than 5")

# This code will always run after 'if'
print("End of simple if\n")

# -----------------------------
# IF-ELSE STATEMENT
# -----------------------------
age: int = int(input("Enter your age: "))

if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")
print()

# -----------------------------
# IF-ELIF-ELSE CHAIN
# -----------------------------
temperature: float = float(input("Enter the temperature in °C: "))

if temperature < 0:
    print("It's freezing cold!")
elif 0 <= temperature < 15:
    print("It's quite chilly.")
elif 15 <= temperature < 25:
    print("The weather is pleasant.")
else:
    print("It's hot outside!")
print()

# -----------------------------
# MULTIPLE CONDITIONS (AND, OR, NOT)
# -----------------------------
has_ticket: bool = input("Do you have a ticket? (yes/no): ").lower().strip() == "yes"
is_vip: bool = input("Are you a VIP? (yes/no): ").lower().strip() == "yes"

# 'and' - both must be true
if has_ticket and is_vip:
    print("Welcome, VIP guest with a ticket!")
# 'or' - at least one must be true
elif has_ticket and not is_vip:
    print("You can enter, but VIP access is unavailable.")
elif not has_ticket and is_vip:
    print("Sorry, even VIPs need a ticket to enter.")
# 'not' - reverses logical value
else:
    print("No entry. You need both a ticket and VIP status.")
print()

# -----------------------------
# COMPARISON OPERATORS
# -----------------------------
a: int = int(input("Enter first number (a): "))
b: int = int(input("Enter second number (b): "))

print("a == b:", a == b)   # equal
print("a != b:", a != b)   # not equal
print("a > b :", a > b)    # greater
print("a < b :", a < b)    # less
print("a >= b:", a >= b)   # greater or equal
print("a <= b:", a <= b)   # less or equal
print()

# -----------------------------
# NESTED CONDITIONS
# -----------------------------
score: int = int(input("Enter your exam score (0-100): "))

if score >= 60:
    print("You passed the exam.")
    if score >= 90:
        print("Excellent! Grade: A")
    elif score >= 75:
        print("Good job! Grade: B")
    else:
        print("You passed, but there's room for improvement.")
else:
    print("Unfortunately, you failed the exam.")
print()

# -----------------------------
# TERNARY (INLINE IF) OPERATOR
# -----------------------------
# Syntax: value_if_true if condition else value_if_false
number: int = int(input("Enter a number: "))
parity: str = "even" if number % 2 == 0 else "odd"
print(f"The number {number} is {parity}.")
print()

# -----------------------------
# CHAINED COMPARISONS
# -----------------------------
# You can check multiple ranges in a clean way
num: int = int(input("Enter a number between 1 and 100: "))

if 1 <= num <= 100:
    print("Valid number within range.")
else:
    print("Number out of range!")
print()

# -----------------------------
# USING 'not' FOR NEGATION
# -----------------------------
logged_in: bool = input("Are you logged in? (yes/no): ").lower().strip() == "yes"

if not logged_in:
    print("Please log in first!")
else:
    print("Access granted.")
print()

# -----------------------------
# COMBINATION EXAMPLE
# -----------------------------
print("=== ACCESS CONTROL SYSTEM ===")
user_age: int
get_age: int
user_age = get_age = int(input("Enter your age: "))
has_id = input("Do you have an ID card? (yes/no): ").lower().strip() == "yes"

if user_age >= 18 and has_id:
    print("Access granted.")
elif user_age >= 18 and not has_id:
    print("You are old enough, but ID is required.")
else:
    print("Access denied: minors are not allowed.")
print()
