"""
Introduction to CPython objects (PyObject) — technical overview.
This module targets Python 3.10+ and aims to explain internal object layout
and observable consequences in pure Python. It is written for a developer
reader who wants concrete, runnable examples and direct links to internals.

Contents
- PyObject and PyVarObject (conceptual, C struct shown as comment)
- ob_refcnt and ob_type: what they mean at Python level
- how id() relates to memory address (CPython implementation detail)
- simple use of ctypes for low-level introspection (read-only, non-portable)
- custom classes showing refcount behavior and raw id values
- short exercises and recommended references

Note: this file is educational. The code uses CPython-specific assumptions
(e.g., id(obj) gives the memory address) that are true for the common
CPython implementation but are not guaranteed across all Python implementations.
"""

# ----------------------------------------
# 1) IMPORTS
# ----------------------------------------
from __future__ import annotations

import sys
import ctypes
import gc
from typing import Any, Optional

# ----------------------------------------
# 2) CONCEPTUAL C-LEVEL STRUCTURES (EXPLAINED)
# ----------------------------------------
# For reference only — CPython C struct shapes (simplified):
#
# typedef struct _object {
#     Py_ssize_t ob_refcnt;      /* reference count */
#     struct _typeobject *ob_type;/* pointer to type */
# } PyObject;
#
# typedef struct {
#     PyObject ob_base;
#     Py_ssize_t ob_size;        /* number of items for variable-size objects */
# } PyVarObject;
#
# We cannot directly access these fields in pure Python, but their effects
# are visible: sys.getrefcount(obj) approximates ob_refcnt, and id(obj)
# corresponds to an address that CPython uses to locate the PyObject.

# ----------------------------------------
# 3) SHORT FAQ (VERY PRACTICAL)
# ----------------------------------------
# Q: What does sys.getrefcount(obj) return?
# A: It returns the reference count plus one because the function call
#    itself temporarily creates a new reference to the object.
#
# Q: Is id(obj) a memory address?
# A: On CPython, id(obj) is the memory address of the object. This is an
#    implementation detail but widely relied upon in debugging and introspection.
#
# Q: Can I modify ob_refcnt from Python?
# A: No. Manipulating reference counts directly is unsafe and not possible
#    from pure Python. ctypes/extension modules can read memory, but writing
#    is dangerous and should be avoided.

# ----------------------------------------
# 4) SMALL HELPERS
# ----------------------------------------

def hex_id(obj: object) -> str:
    """Return a human-friendly hex representation of id(obj).

    On CPython id(obj) is the memory address; we show it in hex for readability.
    """
    return hex(id(obj))


def get_refcount(obj: object) -> int:
    """Return the approximate reference count for `obj`.

    Note: sys.getrefcount(obj) creates a temporary reference for the call,
    so the reported number is one higher than the native ob_refcnt.
    """
    return sys.getrefcount(obj)


# ----------------------------------------
# 5) SIMPLE DEMONSTRATION WITH BUILT-INS
# ----------------------------------------

def builtins_demo() -> None:
    print("=== builtins_demo ===")
    a = 42
    b = a
    print("int value:", a)
    print("id(a):", hex_id(a))
    print("getrefcount(a):", get_refcount(a))

    lst = []
    print("list id:", hex_id(lst))
    print("list tracked by GC?:", gc.is_tracked(lst))
    print("list refcount:", get_refcount(lst))

    # small immutable objects may be interned (small ints, short strings)
    s1 = "hello"
    s2 = "hello"
    print("string ids equal?:", hex_id(s1) == hex_id(s2))
    print()

# ----------------------------------------
# 6) CUSTOM CLASS: SHOWING REFCOUNT & ID
# ----------------------------------------

class SimpleObject:
    def __init__(self, name: str) -> None:
        self.name = name
        self.payload = [i for i in range(16)]  # small list to see nested containers

    def __repr__(self) -> str:
        return f"SimpleObject({self.name})"


def custom_class_demo() -> None:
    print("=== custom_class_demo ===")
    o = SimpleObject("o1")
    print("object:", o)
    print("id(o):", hex_id(o))
    print("refcount(o):", get_refcount(o))

    alias = o
    print("after alias = o -> refcount:", get_refcount(o))
    container = [o]
    print("after container holds o -> refcount:", get_refcount(o))

    # remove alias but container keeps reference
    del alias
    print("after del alias -> refcount:", get_refcount(o))

    # remove container reference
    del container
    print("after del container -> refcount:", get_refcount(o))

    # end of function: local 'o' will go out of scope, reference count decreases
    # to the point where object can be deallocated (in CPython, immediately)
    print()

# ----------------------------------------
# 7) IDENTITY & ADDRESS INSPECTION (ctypes)
# ----------------------------------------
# We can read (not write) memory near the object address to illustrate
# that id(obj) corresponds to an address. This is for demonstration only.


def read_pointer_contents(obj: object, bytes_to_read: int = 64) -> bytes:
    """Read raw bytes starting at the memory address of obj.

    WARNING: reading raw memory is CPython-specific and should be used only
    in controlled educational scenarios. The layout and contents are not
    part of the Python language specification.
    """
    addr = id(obj)
    buf = (ctypes.c_char * bytes_to_read).from_address(addr)
    return bytes(buf)


def ctypes_demo() -> None:
    print("=== ctypes_demo ===")
    o = SimpleObject("ct1")
    addr = id(o)
    print("object:", o)
    print("id(o):", hex(addr))
    raw = read_pointer_contents(o, 32)
    # show first few bytes as hex pairs
    print("first bytes at id(o):", raw[:16].hex())
    print("(Note: interpretation depends on platform/ABI and is not portable)")
    print()

# ----------------------------------------
# 8) VARIABLE-SIZED OBJECTS AND ob_size
# ----------------------------------------
# For variable-sized objects (lists, tuples, strings) CPython uses PyVarObject
# which adds an ob_size field. We can observe growth behavior by checking
# sizes via sys.getsizeof and by inspecting ids of containers when resizing.


def varobject_demo() -> None:
    print("=== varobject_demo ===")
    l: list[int] = []
    print("initial id(list):", hex_id(l), "size:", sys.getsizeof(l))
    for i in range(32):
        l.append(i)
        if i % 8 == 7:
            print(f"after {i+1} appends -> id: {hex_id(l)} size: {sys.getsizeof(l)}")
    print("Note: list resizes may reallocate internal buffer; id(list) remains same")
    print()

# ----------------------------------------
# 9) REFCOUNT AND CIRCULAR REFERENCES (DEMONSTRATION)
# ----------------------------------------

def circular_ref_demo() -> None:
    print("=== circular_ref_demo ===")
    class Node:
        def __init__(self, name: str):
            self.name = name
            self.other: Optional["Node"] = None
        def __repr__(self) -> str:
            return f"Node({self.name})"

    a = Node("A")
    b = Node("B")
    a.other = b
    b.other = a
    print("a id:", hex_id(a), "b id:", hex_id(b))
    print("a refcount:", get_refcount(a), "b refcount:", get_refcount(b))

    # drop external references
    del a
    del b
    # At this point refcounts do not drop to 0 because objects reference each other.
    # The cyclic garbage collector can detect and collect such cycles.
    found = gc.collect()
    print("gc.collect() found unreachable objects:", found)
    print()

# ----------------------------------------
# 10) EXPLAIN WHY id() AND getrefcount ARE LIMITED
# ----------------------------------------
# - getrefcount is approximate (adds a temporary ref for the call)
# - id(obj) address should not be dereferenced or mutated in real code
# - low-level inspection is educational only; production code must rely on
#   high-level semantics and not on memory addresses

# ----------------------------------------
# 11) PRACTICAL CHECKLIST FOR DEBUGGING OBJECT LIFETIME
# ----------------------------------------
# 1) Use getrefcount to estimate live references (remember the +1).
# 2) Use gc.is_tracked to see if object participates in cycle detection.
# 3) If you suspect a leak, use gc.get_referrers and gc.get_referents to walk refs.
# 4) Use tracemalloc for allocation hotspots and heap growth.

# ----------------------------------------
# 12) EXERCISES (SHORT)
# ----------------------------------------
# 1) Create a custom object that holds a reference to another object; show how
#    refcount changes with different containers.
# 2) Use ctypes.read into object memory and note the bytes; explain why output
#    is platform-dependent.
# 3) Create a pair of objects that reference each other and verify that gc.collect
#    removes them after deleting external references.

# ----------------------------------------
# 13) QUICK-RUN WHEN EXECUTED DIRECTLY
# ----------------------------------------
if __name__ == "__main__":
    # Keep demos small and self-contained so they are suitable for notebooks/tests
    builtins_demo()
    custom_class_demo()
    ctypes_demo()
    varobject_demo()
    circular_ref_demo()
    print("\npyobject_intro demo finished")
