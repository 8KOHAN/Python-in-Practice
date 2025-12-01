# -----------------------------
# WHILE LOOP (basic example)
# -----------------------------
print("WHILE LOOP EXAMPLE:")
count = 1
while count <= 5:
    print(f"Count = {count}")
    count += 1
print("Loop ended.\n")

# -----------------------------
# WHILE LOOP WITH USER INPUT
# -----------------------------
print("WHILE LOOP WITH INPUT:")
password = "python123"
attempt = ""

while attempt != password:
    attempt = input("Enter the password: ")
    if attempt == password:
        print("Access granted!")
    else:
        print("Incorrect password, try again.")
print()

# -----------------------------
# FOR LOOP (iteration over range)
# -----------------------------
print("FOR LOOP WITH RANGE:")
for i in range(5):  # 0 to 4
    print("i =", i)
print()

# Custom range
print("Custom range (2 to 10 step 2):")
for i in range(2, 11, 2):
    print(i, end=" ")
print("\n")

# -----------------------------
# ITERATING OVER STRINGS AND LISTS
# -----------------------------
print("Iterating over a string:")
for char in "Python":
    print(char, end=" ")
print("\n")

print("Iterating over a list:")
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")
print()

# -----------------------------
# FOR LOOP WITH DICTIONARY
# -----------------------------
print("Iterating over a dictionary:")
person = {"name": "Alice", "age": 25, "city": "London"}
for key, value in person.items():
    print(f"{key}: {value}")
print()

# -----------------------------
# BREAK AND CONTINUE
# -----------------------------
print("BREAK and CONTINUE examples:")

for i in range(1, 10):
    if i == 5:
        print("Skipping number 5")
        continue  # skip the rest of this iteration
    if i == 8:
        print("Breaking at number 8")
        break  # exit the loop completely
    print("Number:", i)
print("Loop finished.\n")

# -----------------------------
# LOOP ELSE CLAUSE
# -----------------------------
print("FOR-ELSE example:")
for i in range(3):
    print("Iteration", i)
else:
    print("Loop completed successfully (no break used).")
print()

print("FOR-ELSE with break:")
for i in range(3):
    if i == 1:
        print("Breaking loop!")
        break
    print("Iteration", i)
else:
    print("This will not run because of break.")
print()

# -----------------------------
# NESTED LOOPS (multiplication table)
# -----------------------------
print("NESTED LOOP EXAMPLE (Multiplication Table):")
for i in range(1, 6):  # rows
    for j in range(1, 6):  # columns
        print(f"{i * j:3}", end=" ")
    print()  # new line after each row
print()

# -----------------------------
# SUM OF NUMBERS USING LOOPS
# -----------------------------
print("SUM OF NUMBERS USING FOR LOOP:")
total = 0
for i in range(1, 6):
    total += i
    print(f"Adding {i}, current sum = {total}")
print(f"Final sum = {total}\n")

# -----------------------------
# WHILE LOOP WITH BREAK CONDITION
# -----------------------------
print("WHILE LOOP WITH BREAK:")
number = 0
while True:
    number += 1
    print("Number =", number)
    if number == 3:
        print("Breaking the loop.")
        break
print()

# -----------------------------
# CONTINUE EXAMPLE WITH WHILE
# -----------------------------
print("CONTINUE in WHILE loop:")
num = 0
while num < 5:
    num += 1
    if num == 3:
        print("Skipping number 3")
        continue
    print("Current number:", num)
print()

# -----------------------------
# ENUMERATE EXAMPLES
# -----------------------------
print("ENUMERATE EXAMPLES:")

fruits = ["apple", "banana", "cherry"]

# Basic enumerate loop
print("Basic enumerate:")
for index, fruit in enumerate(fruits):
    print(f"Index = {index}, Fruit = {fruit}")
print()

# Enumerate with custom start index
print("Enumerate start=1:")
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
print()

# Enumerating over a string
print("Enumerate over string:")
for index, char in enumerate("Python"):
    print(f"{index}: {char}")
print()


# -----------------------------
# PRACTICAL EXAMPLE: FACTORIAL
# -----------------------------
print("FACTORIAL CALCULATION USING FOR LOOP:")
n = int(input("Enter a number to find factorial: "))
factorial = 1
for i in range(1, n + 1):
    factorial *= i
    print(f"i = {i}, current factorial = {factorial}")
print(f"Factorial of {n} is {factorial}\n")
