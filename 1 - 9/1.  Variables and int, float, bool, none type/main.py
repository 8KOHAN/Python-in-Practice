# -----------------------------
# INTRODUCTION
# -----------------------------
# In Python, everything is an object.
# Variables are just names that refer to data stored in memory.
# Here we explore basic data types: int, float, bool, and NoneType.

# -----------------------------
# INTEGER (int)
# -----------------------------
age = 25
year = 2025
negative_number = -10
big_number = 12345678901234567890  # Python supports very large integers

print("=== INTEGER EXAMPLES ===")
print("age:", age)
print("year + 5:", year + 5)
print("negative_number * 2:", negative_number * 2)
print("big_number:", big_number)
print("Division with int (//):", year // age)  # integer division
print("Is age an integer?", isinstance(age, int))
print("Type of age:", type(age))
print()

# -----------------------------
# FLOAT (float)
# -----------------------------
height = 1.75
weight = 68.5
temperature = -3.2
pi = 3.1415926535

print("=== FLOAT EXAMPLES ===")
print("height:", height)
print("weight / 2:", weight / 2)
print("height * weight:", height * weight)
print("Rounded height * weight:", round(height * weight, 2))
print("Is height a float?", isinstance(height, float))
print("Type of weight:", type(weight))
print()

# -----------------------------
# BOOLEAN (bool)
# -----------------------------
is_student = True
has_pet = False
is_adult = age >= 18

print("=== BOOLEAN EXAMPLES ===")
print("is_student:", is_student)
print("has_pet:", has_pet)
print("is_adult:", is_adult)
print("is_student AND has_pet:", is_student and has_pet)
print("is_student OR has_pet:", is_student or has_pet)
print("NOT is_student:", not is_student)
print("Is is_student a boolean?", isinstance(is_student, bool))
print("Type of is_student:", type(is_student))
print()

# -----------------------------
# NONE TYPE (NoneType)
# -----------------------------
middle_name = None

print("=== NONE TYPE EXAMPLES ===")
print("middle_name:", middle_name)
print("Is middle_name None?", middle_name is None)
print("Type of middle_name:", type(middle_name))
print("Compare None to None:", middle_name == None)  # not recommended, but possible
print()

# -----------------------------
# TYPE CONVERSIONS (Casting)
# -----------------------------
print("=== TYPE CONVERSIONS ===")
print("int to float:", float(age))           # 25 -> 25.0
print("float to int:", int(height))          # 1.75 -> 1
print("int to bool:", bool(age))             # any non-zero number -> True
print("0 to bool:", bool(0))                 # 0 -> False
print("bool to int:", int(is_student))       # True -> 1
print("bool to float:", float(has_pet))      # False -> 0.0
print("float to string:", str(weight))       # 68.5 -> "68.5"
print("string to int:", int("42"))           # "42" -> 42
print("string to float:", float("3.14"))     # "3.14" -> 3.14
print()

# -----------------------------
# MIXED OPERATIONS
# -----------------------------
print("=== MIXED OPERATIONS ===")
print("age + height:", age + height)         # int + float -> float
print("year / age:", year / age)             # division always gives float
print("age == 25:", age == 25)
print("is_student AND (age > 20):", is_student and (age > 20))
print("bool behaves like int:", True + True, False + True)  # 1 + 1, 0 + 1
print("int(False) + int(True):", int(False) + int(True))
print()

# -----------------------------
# TYPE CHECKING FUNCTIONS
# -----------------------------
print("=== TYPE CHECKING ===")
print("type(age):", type(age))
print("type(height):", type(height))
print("type(is_student):", type(is_student))
print("type(middle_name):", type(middle_name))
print("isinstance(age, (int, float)):", isinstance(age, (int, float)))
print()

# -----------------------------
# COMMON MISTAKES & ERRORS
# -----------------------------
print("=== TYPE ERRORS EXAMPLES ===")
try:
    print(age + middle_name)  # int + None -> error
except TypeError as e:
    print("Error:", e)

try:
    print(is_student + middle_name)  # bool + None -> error
except TypeError as e:
    print("Error:", e)

try:
    print("25" + 5)  # string + int -> error
except TypeError as e:
    print("Error:", e)

print()

# -----------------------------
# SUMMARY PRINT (VISUAL OUTPUT)
# -----------------------------
print("=" * 35)
print("     VARIABLES AND DATA TYPES     ")
print("=" * 35)
print(f"age (int)          : {age}")
print(f"height (float)     : {height}")
print(f"is_student (bool)  : {is_student}")
print(f"middle_name (None) : {middle_name}")
print("=" * 35)
print("End of demonstration.")
