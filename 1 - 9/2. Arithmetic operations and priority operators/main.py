# -----------------------------
# BASIC ARITHMETIC OPERATIONS
# -----------------------------
a = 10
b = 3

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

result1 = 2 + 3 * 4      # multiplication is executed first
result2 = (2 + 3) * 4    # parentheses change the order
result3 = 2 ** 3 * 4     # exponentiation first
result4 = 2 ** (3 * 4)   # parentheses change exponentiation order
result5 = 10 - 4 + 2     # left-to-right for equal precedence

print("2 + 3 * 4 =", result1)
print("(2 + 3) * 4 =", result2)
print("2 ** 3 * 4 =", result3)
print("2 ** (3 * 4) =", result4)
print("10 - 4 + 2 =", result5)
print()

# -----------------------------
# COMBINING DIFFERENT OPERATIONS
# -----------------------------
x = 5
y = 2
z = 3

combined_result = x + y * z ** 2 - (x // y)  # combined arithmetic
print("x + y * z ** 2 - (x // y) =", combined_result)
print()

# ----------------------------
# PRACTICAL EXAMPLES
# -----------------------------
# 1. Calculate rectangle area
length = 7
width = 3
area = length * width
print("Rectangle area =", area)

# 2. Calculate average of numbers
num1 = 10
num2 = 20
num3 = 30
average = (num1 + num2 + num3) / 3
print("Average =", average)

# 3. Check if a number is even using modulo
number = 15
is_even = (number % 2 == 0)
print("Is number even?", is_even)
