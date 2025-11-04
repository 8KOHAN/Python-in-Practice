# -----------------------------
# INTRODUCTION
# -----------------------------
# A set is an unordered collection of unique, hashable items.
# Sets are mutable: you can add/remove elements.
# Use set() to create an empty set, {} creates an empty dict.

# -----------------------------
# CREATION EXAMPLES
# -----------------------------
print("=== CREATION ===")
s1 = {1, 2, 3}
s2 = set([3, 4, 5])          # from iterable (list)
s3 = set("hello")            # from string -> chars, duplicates removed
s_empty = set()              # empty set (NOT {}!)

print("s1:", s1)
print("s2:", s2)
print("s3 (from 'hello'):", s3)
print("empty set:", s_empty)
print()

# -----------------------------
# UNIQUENESS & NO ORDER GUARANTEE
# -----------------------------
print("=== UNIQUENESS & ORDER ===")
dup_list = [1, 2, 2, 3, 3, 3]
s_from_dup = set(dup_list)
print("original list:", dup_list)
print("set from list (duplicates removed):", s_from_dup)

# Note: sets are unordered. Iteration order may be unpredictable
print("Iterating set elements (order may vary):")
for elem in s_from_dup:
    print(elem, end=" ")
print("\n")

# If you need a consistent presentation, sort when printing:
print("Sorted view of set:", sorted(s_from_dup))
print()

# -----------------------------
# MUTATING METHODS (add, update, remove, discard, pop, clear)
# -----------------------------
print("=== MUTATION METHODS ===")
s = {1, 2, 3}
s.add(4)                    # add single element
print("after add(4):", s)

s.update([5, 6, 2])         # add multiple; duplicates ignored
print("after update([5,6,2]):", s)

# remove vs discard
s.discard(10)               # no error if missing
print("after discard(10) (no error):", s)

try:
    s.remove(10)            # raises KeyError if missing
except KeyError as e:
    print("remove(10) raised KeyError as expected:", e)

# pop removes and returns an arbitrary element
popped = s.pop()
print("popped (arbitrary):", popped)
print("set after pop():", s)

s.clear()
print("after clear():", s)
print()

# -----------------------------
# SET OPERATIONS (union, intersection, difference, symmetric_difference)
# -----------------------------
print("=== SET OPERATIONS ===")
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print("A:", A)
print("B:", B)
print("A union B  (A | B):", A | B)
print("A intersection B (A & B):", A & B)
print("A difference B (A - B):", A - B)
print("B difference A (B - A):", B - A)
print("symmetric difference (A ^ B):", A ^ B)

# In-place versions
C = A.copy()
C |= B   # C.update(B)  in-place union
print("C after in-place union with B (C |= B):", C)
print()

# -----------------------------
# SUBSET / SUPERSET / DISJOINT
# -----------------------------
print("=== RELATION CHECKS ===")
X = {1, 2}
Y = {1, 2, 3, 4}

print("X:", X, "Y:", Y)
print("X issubset Y:", X.issubset(Y))    # X <= Y
print("Y issuperset X:", Y.issuperset(X))# Y >= X
print("Are A and B disjoint?:", A.isdisjoint(B))
print()

# -----------------------------
# SET COMPREHENSIONS
# -----------------------------
print("=== SET COMPREHENSIONS ===")
squares = {n * n for n in range(6)}
print("squares:", squares)

# Filtering example
evens = {n for n in range(20) if n % 2 == 0}
print("evens (0..18):", evens)
print()

# -----------------------------
# HASHABILITY & IMMUTABILITY OF ELEMENTS
# -----------------------------
print("=== HASHABILITY ===")
good = {1, "a", (1, 2)}     # int, str, tuple are hashable
print("good set:", good)

try:
    bad = {1, [2, 3]}      # list is not hashable -> TypeError
except TypeError as e:
    print("Trying to create set with list raised TypeError:", e)

# You can store tuples containing immutable objects:
t = (1, (2, 3))
S = {t}
print("set with tuple element allowed:", S)
print()

# -----------------------------
# FROZENSET (immutable set)
# -----------------------------
print("=== FROZENSET ===")
fs = frozenset([1, 2, 3])
print("frozenset:", fs)
# fs.add(4)  # AttributeError if uncommented: frozenset has no add()
# frozenset is hashable, so it can be used as a dict key or element of a set
d = {fs: "value"}           # valid because frozenset is immutable & hashable
print("frozenset can be dict key:", d)
print()

# -----------------------------
# COMMON USE CASES
# -----------------------------
print("=== COMMON USE CASES ===")
# 1. Remove duplicates from a list (order not preserved)
nums = [3, 1, 2, 3, 2, 1]
unique = set(nums)
print("unique (order may change):", unique)

# 2. Fast membership test (O(1) average)
s_lookup = set(range(1000000))
print("Membership test example: 999999 in set?", 999999 in s_lookup)

# 3. Find unique words in text
text = "apple banana apple orange banana pear"
unique_words = set(text.split())
print("unique words:", unique_words)
print()

# -----------------------------
# PERFORMANCE NOTE (brief)
# -----------------------------
# - Membership checks (x in s) are on average O(1).
# - Building a set from an iterable is O(n).
# - Keep elements hashable for sets to work.

print("End of set examples.")

