# -----------------------------------------
# INTRODUCTION
# -----------------------------------------
# Nested data structures are data structures
# that contain other data structures inside them.
#
# Examples:
# - list of lists
# - list of dicts
# - dict of lists
# - dict of dicts
# - combinations of lists, dicts, tuples, sets, etc.


# -----------------------------------------
# LIST OF LISTS
# -----------------------------------------
print("=== LIST OF LISTS ===")
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

print("matrix:", matrix)
print("matrix[0]:", matrix[0])
print("matrix[1][2]:", matrix[1][2])      # 6
print()

# modifying nested element
matrix[2][1] = 88
print("matrix after modification:", matrix)
print()


# -----------------------------------------
# LIST OF DICTIONARIES
# -----------------------------------------
print("=== LIST OF DICTS ===")
users = [
    {"name": "Alice", "age": 25, "is_admin": False},
    {"name": "Bob", "age": 30, "is_admin": True},
    {"name": "Charlie", "age": 28, "is_admin": False},
]

print("users:", users)
print("Second user name:", users[1]["name"])
print("Is Charlie admin?:", users[2]["is_admin"])
print()

# modifying values
users[0]["age"] = 26
print("Updated users:", users)
print()


# -----------------------------------------
# DICTIONARY OF LISTS
# -----------------------------------------
print("=== DICT OF LISTS ===")
grades = {
    "Alice": [5, 4, 5],
    "Bob": [3, 4],
    "Charlie": [5, 5, 5],
}

print("grades:", grades)
print("Alice grades:", grades["Alice"])
print("Bob second grade:", grades["Bob"][1])
print()

# adding new grade
grades["Alice"].append(3)
print("Alice updated grades:", grades["Alice"])
print()


# -----------------------------------------
# DICTIONARY OF DICTIONARIES
# -----------------------------------------
print("=== DICT OF DICTS ===")
employees = {
    "emp1": {"name": "Anna", "salary": 5000, "active": True},
    "emp2": {"name": "John", "salary": 7000, "active": False},
}

print("employees:", employees)
print("emp1 salary:", employees["emp1"]["salary"])
print("emp2 active status:", employees["emp2"]["active"])
print()

# update nested dictionary
employees["emp1"]["salary"] = 5500
print("updated employees:", employees)
print()


# -----------------------------------------
# MIXED NESTED STRUCTURES
# -----------------------------------------
print("=== MIXED STRUCTURES ===")
data = {
    "numbers": [1, 2, 3, (10, 20)],
    "info": {
        "names": ("Alice", "Bob"),
        "details": {"city": "Paris", "zipcode": 75001},
    },
    "flags": {"online", "offline"}
}

print("data:", data)
print("Access tuple inside list:", data["numbers"][3][0])  # 10
print("Access nested dict:", data["info"]["details"]["city"])
print("Access tuple element:", data["info"]["names"][1])
print()


# -----------------------------------------
# ITERATING OVER NESTED STRUCTURES
# -----------------------------------------
print("=== ITERATING OVER NESTED STRUCTURES ===")
for user in users:
    print(f"Name: {user['name']}, Age: {user['age']}")
print()

for name, g_list in grades.items():
    print(name, "average grade:", sum(g_list) / len(g_list))
print()


# -----------------------------------------
# COMPLEX EXAMPLE: JSON-LIKE STRUCTURE
# -----------------------------------------
print("=== JSON-LIKE STRUCTURE ===")

config = {
    "server": {
        "host": "localhost",
        "ports": [8080, 8081, 8082],
        "ssl": {"enabled": True, "version": "TLS1.2"},
    },
    "users": [
        {"username": "admin", "roles": ["read", "write", "delete"]},
        {"username": "guest", "roles": ["read"]},
    ],
    "features": {
        "logging": True,
        "backup": {"enabled": False, "path": "/backup"},
    }
}

print("SSL enabled:", config["server"]["ssl"]["enabled"])
print("Admin roles:", config["users"][0]["roles"])
print("Guest role:", config["users"][1]["roles"])
print("Backup path:", config["features"]["backup"]["path"])
print()

