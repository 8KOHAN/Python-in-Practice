# -----------------------------
# INTEGER
# -----------------------------
age = 25
year = 2025
negative_number = -10

print("Integer examples:")
print("age:", age)
print("year + 5:", year + 5)
print("negative_number * 2:", negative_number * 2)
print("Is age an integer?", isinstance(age, int))
print()

# -----------------------------
# FLOAT
# -----------------------------
height = 1.75
weight = 68.5

print("Float examples:")
print("height:", height)
print("weight / 2:", weight / 2)
print("height * weight:", height * weight)
print("Is height a float?", isinstance(height, float))
print()

# -----------------------------
# BOOLEAN
# -----------------------------
is_student = True
has_pet = False

print("Boolean examples:")
print("is_student AND has_pet:", is_student and has_pet) 
print("is_student OR has_pet:", is_student or has_pet)    
print("NOT is_student:", not is_student)               
print("Is is_student a boolean?", isinstance(is_student, bool))
print()

# -----------------------------
# NONE TYPE
# -----------------------------
middle_name = None

print("NoneType examples:")
print("middle_name:", middle_name)
print("Is middle_name None?", middle_name is None)
print()

# -----------------------------
# TYPE CONVERSIONS
# -----------------------------
print("Type conversions:")
print("int to float:", float(age))       # 25 -> 25.0
print("float to int:", int(height))      # 1.75 -> 1
print("int to bool:", bool(age))         # any non-zero number -> True
print("0 to bool:", bool(0))             # 0 -> False
print("bool to int:", int(is_student))   # True -> 1
print("bool to float:", float(has_pet))  # False -> 0.0
print()

# -----------------------------
# MIXED OPERATIONS
# -----------------------------
print("Mixed operations:")
print("age + height:", age + height)     # int + float -> float
print("age == 25:", age == 25)      
print("is_student AND (age > 20):", is_student and (age > 20))
print()

# -----------------------------
# ERRORS
# -----------------------------
print("Type errors examples:")
try:
    print(age + middle_name)  # int + None -> error
except TypeError as e:
    print("Error:", e)

try:
    print(is_student + middle_name)  # bool + None -> error
except TypeError as e:
    print("Error:", e)

print()
