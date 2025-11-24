# -----------------------------
# BASIC ARITHMETIC OPERATIONS
# -----------------------------
a: int = 10
b: int = 3

print("Basic arithmetic operations:")
print("a + b =", a + b)   # addition
print("a - b =", a - b)   # subtraction
print("a * b =", a * b)   # multiplication
print("a / b =", a / b)   # division (float)
print("a // b =", a // b) # integer division
print("a % b =", a % b)   # modulo (remainder)
print("a ** b =", a ** b) # exponentiation
print()

# -----------------------------
# OPERATOR PRIORITY
# -----------------------------
# In Python, the order of operations is:
# 1. Parentheses ()
# 2. Exponentiation **
# 3. Multiplication *, Division /, Integer division //, Modulo %
# 4. Addition + and Subtraction -

print("Operator priority examples:")

result1: int = 2 + 3 * 4      # multiplication is executed first
result2: int = (2 + 3) * 4    # parentheses change the order
result3: int = 2 ** 3 * 4     # exponentiation first
result4: int = 2 ** (3 * 4)   # parentheses change exponentiation order
result5: int = 10 - 4 + 2     # left-to-right for equal precedence

print("2 + 3 * 4 =", result1)
print("(2 + 3) * 4 =", result2)
print("2 ** 3 * 4 =", result3)
print("2 ** (3 * 4) =", result4)
print("10 - 4 + 2 =", result5)
print()

# -----------------------------
# COMBINING DIFFERENT OPERATIONS
# -----------------------------
x: int = 5
y: int = 2
z: int = 3

combined_result = x + y * z ** 2 - (x // y)  # combined arithmetic
print("x + y * z ** 2 - (x // y) =", combined_result)
print()

# ----------------------------
# PRACTICAL EXAMPLES
# -----------------------------
# 1. Calculate rectangle area
length: int = 7
width: int = 3
area: int = length * width
print("Rectangle area =", area)

# 2. Calculate average of numbers
num1: int = 10
num2: int = 20
num3: int = 30
average: float = (num1 + num2 + num3) / 3
print("Average =", average)

# 3. Check if a number is even using modulo
number: int = 15
is_even: bool = (number % 2 == 0)
print("Is number even?", is_even)
