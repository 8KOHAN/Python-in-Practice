# -----------------------------
# INTRODUCTION
# -----------------------------
# A dict (dictionary) maps keys to values.
# - Keys must be hashable (immutable): int, str, tuple, etc. (NOT list/dict/set)
# - Values can be any objects.
# - Preserves insertion order (Python 3.7+).
# - Average O(1) lookup, insert, delete.

# -----------------------------
# CREATION
# -----------------------------
print("=== CREATION ===")
d1 = {"name": "Alice", "age": 25, "city": "Kyiv"}
d2 = dict(country="Ukraine", code=380)           # keyword args
d3 = dict([("a", 1), ("b", 2)])                 # from iterable of pairs
d4 = {}                                         # empty dict
d5 = {("x", 1): "tuple key allowed"}             # tuple as a key (hashable)

print("d1:", d1)
print("d2:", d2)
print("d3:", d3)
print("d4:", d4)
print("d5:", d5)
print()

# -----------------------------
# ACCESS & SAFE ACCESS
# -----------------------------
print("=== ACCESS ===")
print("d1['name'] ->", d1["name"])               # direct access (KeyError if missing)

# Safe access with get() (returns None if missing, or default provided)
print("d1.get('email') ->", d1.get("email"))
print("d1.get('email', 'not set') ->", d1.get("email", "not set"))

# Avoid KeyError with 'in'
print("'age' in d1? ->", "age" in d1)
print()

# -----------------------------
# INSERT / UPDATE / MERGE
# -----------------------------
print("=== INSERT / UPDATE / MERGE ===")
d = {"a": 1}
d["b"] = 2                                     # insert or overwrite
d["a"] = 100                                   # update
print("after assignments:", d)

d.update({"c": 3, "d": 4})                     # update from another dict
print("after update:", d)

# Python 3.9+: merge operator
e = {"d": 40, "e": 5}
merged = d | e                                  # produces a new dict
print("merged d | e:", merged)

d |= {"f": 6}                                   # in-place merge
print("d after |= {'f': 6}:", d)
print()

# -----------------------------
# DELETE / POP / POPITEM / SETDEFAULT
# -----------------------------
print("=== DELETE / POP / POPITEM / SETDEFAULT ===")
user = {"name": "Bob", "age": 30, "country": "UA"}

# del by key (KeyError if missing)
del user["country"]
print("after del country:", user)

# pop returns and removes key (KeyError if missing without default)
age_value = user.pop("age")
print("popped age:", age_value, "; user:", user)

# pop with default to avoid KeyError
missing = user.pop("unknown", "not found")
print("pop('unknown','not found') ->", missing)

# popitem removes the last inserted key-value (since Py3.7 order preserved)
last_key, last_val = {"x": 1, "y": 2, "z": 3}.popitem()
print("popitem example:", (last_key, last_val))

# setdefault: return existing value OR set and return default
profile = {"name": "Eve"}
lang = profile.setdefault("lang", "en")        # creates 'lang' if missing
print("profile after setdefault:", profile, "; returned:", lang)
print()

# -----------------------------
# VIEWS: KEYS / VALUES / ITEMS
# -----------------------------
print("=== VIEWS (DYNAMIC) ===")
v = {"a": 1, "b": 2}
keys_view = v.keys()
values_view = v.values() 
items_view = v.items()
print("keys before:", list(keys_view))
print("values before:", list(values_view))
print("items before:", list(items_view))
v["c"] = 3                                     # views reflect live changes
print("keys after adding 'c':", list(keys_view))
print("values after adding 'c':", list(values_view))
print("items after adding 'c':", list(items_view))
print()

# -----------------------------
# ITERATION PATTERNS
# -----------------------------
print("=== ITERATION ===")
grades = {"Alice": 95, "Bob": 82, "Cara": 91}

print("iterate keys:")
for name in grades:
    print(name, end=" ")
print()

print("iterate values:")
for score in grades.values():
    print(score, end=" ")
print()

print("iterate items (key, value):")
for name, score in grades.items():
    print(f"{name} -> {score}")
print()

# -----------------------------
# SORTING A DICT VIEW
# -----------------------------
print("=== SORTING ===")
print("sorted keys:", sorted(grades))
print("sorted by value desc:", sorted(grades.items(), key=lambda kv: kv[1], reverse=True))
print()

# -----------------------------
# DICT COMPREHENSIONS
# -----------------------------
print("=== DICT COMPREHENSIONS ===")
squares = {n: n * n for n in range(6)}
even_map = {n: "even" for n in range(10) if n % 2 == 0}
print("squares:", squares)
print("even_map:", even_map)
print()

# -----------------------------
# NESTED DICTS
# -----------------------------
print("=== NESTED DICTS ===")
users = {
    1: {"name": "Alice", "roles": ["admin", "editor"]},
    2: {"name": "Bob", "roles": ["viewer"]},
}
print("users:", users)
print("user 1 name:", users[1]["name"])
print("user 2 first role:", users[2]["roles"][0])
print()

# -----------------------------
# ERROR HANDLING: KeyError
# -----------------------------
print("=== KeyError HANDLING ===")
conf = {"host": "localhost", "port": 8000}
try:
    print("protocol:", conf["protocol"])  # KeyError
except KeyError as e:
    print("KeyError caught for missing key:", e)
print()

# -----------------------------
# IMMUTABLE vs MUTABLE KEYS
# -----------------------------
print("=== KEY HASHABILITY ===")
ok = {42: "int key", "x": "str key", (1, 2): "tuple key"}
print("ok keys:", ok)

try:
    bad = {[1, 2]: "list as key not allowed"}  # TypeError: unhashable type: 'list'
except TypeError as e:
    print("TypeError (unhashable key) example:", e)
print()

# -----------------------------
# SHALLOW vs DEEP COPY
# -----------------------------
print("=== COPY ===")
import copy

orig = {"a": 1, "nested": {"x": 10}}
shallow = orig.copy()                # or dict(orig)
deep = copy.deepcopy(orig)

orig["nested"]["x"] = 99
print("orig:", orig)
print("shallow (nested changed too):", shallow)  # shares nested dict
print("deep (independent nested):", deep)
print()

# -----------------------------
# COMMON PATTERNS
# -----------------------------
print("=== COMMON PATTERNS ===")
# 1) Counting occurrences
text = "apple banana apple orange banana apple"
counter = {}
for word in text.split():
    counter[word] = counter.get(word, 0) + 1
print("word counts:", counter)

# Short form
from collections import Counter
counter = Counter(text.split())
print(counter)

# 2) Grouping items with setdefault
pairs = [("A", 1), ("B", 2), ("A", 3), ("B", 4), ("C", 5)]
grouped = {}
for k, v in pairs:
    grouped.setdefault(k, []).append(v)
print("grouped:", grouped)

# Using defaultdict for cleaner grouping
from collections import defaultdict
grouped2 = defaultdict(list)
for k, v in pairs:
    grouped2[k].append(v)
print("grouped2 (defaultdict):", dict(grouped2))  # cast to dict for pretty print
print()

print("End of dict examples.")

