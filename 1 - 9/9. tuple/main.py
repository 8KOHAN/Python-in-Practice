# ---------------------------------------------
# TOPIC: Tuples in Python
# ---------------------------------------------
# A tuple is an immutable sequence in Python.
# Once created, its elements cannot be modified.
# Tuples can contain elements of any type, including other tuples.

# ---------------------------------------------
# CREATING TUPLES
# ---------------------------------------------
empty_tuple = ()
single_element = (5,)  # note the comma! without it, it's not a tuple
numbers = (1, 2, 3, 4, 5)
mixed = (10, "hello", 3.14, True, None)

print("Empty tuple:", empty_tuple)
print("Single element tuple:", single_element)
print("Numbers tuple:", numbers)
print("Mixed tuple:", mixed)
print("Type of numbers:", type(numbers))
print()

# ---------------------------------------------
# ACCESSING ELEMENTS
# ---------------------------------------------
print("First element:", numbers[0])
print("Last element:", numbers[-1])
print("Slice [1:4]:", numbers[1:4])
print("Every second element:", numbers[::2])
print()

# ---------------------------------------------
# IMMUTABILITY
# ---------------------------------------------
# Tuples cannot be changed in place.
try:
    numbers[0] = 100
except TypeError as e:
    print("Error trying to modify tuple:", e)
print()

# ---------------------------------------------
# TUPLE OPERATIONS
# ---------------------------------------------
t1 = (1, 2, 3)
t2 = (4, 5)

# Concatenation
t3 = t1 + t2
print("Concatenation t1 + t2:", t3)

# Repetition
t4 = t1 * 2
print("Repetition t1 * 2:", t4)

# Membership
print("Is 2 in t1?", 2 in t1)
print("Is 10 not in t1?", 10 not in t1)

# Length
print("Length of t3:", len(t3))
print()

# ---------------------------------------------
# NESTED TUPLES
# ---------------------------------------------
nested = ((1, 2), (3, 4), (5, 6))
print("Nested tuple:", nested)
print("Access element nested[1][0]:", nested[1][0])
print()

# ---------------------------------------------
# TUPLE UNPACKING
# ---------------------------------------------
point = (10, 20)
x, y = point
print("Tuple unpacking point -> x:", x, ", y:", y)

# Using * for remaining elements
numbers = (1, 2, 3, 4, 5)
first, *middle, last = numbers
print("Unpacking with * -> first:", first, ", middle:", middle, ", last:", last)
print()

# ---------------------------------------------
# METHODS AND FUNCTIONS
# ---------------------------------------------
t = (1, 2, 2, 3, 4, 2)

print("Count of 2 in t:", t.count(2))
print("Index of 3 in t:", t.index(3))
print("Max:", max(t))
print("Min:", min(t))
print("Sum:", sum(t))
print()

# ---------------------------------------------
# CONVERTING BETWEEN TUPLES AND LISTS
# ---------------------------------------------
lst = [1, 2, 3]
tpl = tuple(lst)  # list -> tuple
print("List -> Tuple:", tpl)

new_lst = list(tpl)  # tuple -> list
new_lst.append(4)
print("Tuple -> List -> modified list:", new_lst)
print()

# ---------------------------------------------
# IMMUTABLE VS MUTABLE INSIDE TUPLE
# ---------------------------------------------
# While the tuple itself is immutable, mutable objects inside it can be changed
tpl = ([1, 2], [3, 4])
print("Original tuple with lists:", tpl)
tpl[0].append(99)
print("After modifying inner list:", tpl)
print("Notice: the tuple object is still the same, but inner mutable objects changed.")
print()

# ---------------------------------------------
# COMMON ERRORS
# ---------------------------------------------
try:
    tpl[0] = [5, 6]  # error
except TypeError as e:
    print("Error trying to change a tuple element:", e)

try:
    single_element = (10)  # not a tuple, just int
    print(type(single_element))
except Exception as e:
    print("Error:", e)
print()

# ---------------------------------------------
# SUMMARY
# ---------------------------------------------
print("=" * 40)
print("        TUPLES DEMONSTRATION COMPLETE        ")
print("=" * 40)
