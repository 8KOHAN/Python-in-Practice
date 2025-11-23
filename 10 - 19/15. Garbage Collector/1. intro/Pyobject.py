"""
Introduction to CPython objects (PyObject) — technical overview.
This module targets Python 3.10+ and aims to explain internal object layout
and observable consequences in pure Python.

Contents
- PyObject and PyVarObject (conceptual, C struct shown as comment)
- ob_refcnt and ob_type: what they mean at Python level
- how id() relates to memory address (CPython implementation detail)
- simple use of ctypes for low-level introspection (read-only, non-portable)

Note: this file is educational. The code uses CPython-specific assumptions
(e.g., id(obj) gives the memory address) that are true for the common
CPython implementation but are not guaranteed across all Python implementations.
"""


# ----------------------------------------
# 1) IMPORTS
# ----------------------------------------
import sys
import ctypes
import gc


# ----------------------------------------
# 2) CONCEPTUAL C-LEVEL STRUCTURES (EXPLAINED)
# ----------------------------------------
# Below are accurate, C-valid simplified representations of how CPython
# defines its fundamental object structures. These definitions come from
# CPython's C headers (mainly Include/object.h), but are shown here in a
# condensed form so you can see the true memory layout.
#
# --- PyObject -------------------------------------------------------------
# This is the base structure for *all* Python objects:
#
# typedef struct _object {
# Py_ssize_t ob_refcnt; /* reference count */
# struct _typeobject *ob_type; /* pointer to object's type */
# } PyObject;
#
# - ob_refcnt: how many active references exist to this object
# - ob_type: pointer to the object's PyTypeObject (its class)
# Every Python object carries its type at runtime.
#
# --- PyVarObject ----------------------------------------------------------
# For objects whose size varies at runtime (lists, tuples, strings, etc.),
# CPython extends PyObject into PyVarObject:
#
# typedef struct {
# PyObject ob_base; /* the PyObject header */
# Py_ssize_t ob_size; /* number of elements/items */
# } PyVarObject;
#
# This means variable-length objects contain:
# - ob_base.ob_refcnt
# - ob_base.ob_type
# - ob_size (their logical length)
# Followed by actual data stored immediately after the struct in memory.
#
# --- Python-level visibility ----------------------------------------------
# Pure Python code cannot directly access these C fields.
# However, their effects *are observable*:
# - sys.getrefcount(obj) gives the reference count associated with ob_refcnt
# - id(obj) returns the memory address where the PyObject struct begins
# (CPython uses this address to find ob_refcnt, ob_type, etc.)


# ----------------------------------------
# 3) SMALL HELPER
# ----------------------------------------

def hex_id(obj: object, /) -> str:
    """
    Return a human-friendly hex representation of id(obj).
    On CPython id(obj) is the memory address; we show it in hex for readability.
    """
    return hex(id(obj))


# ----------------------------------------
# 4) IMMORTAL OBJECTS (Python 3.12+)
# ----------------------------------------
# Some objects are "immortal": their ob_refcnt is set to a very large value
# (e.g., 2**63-1 on 64-bit builds). They will never be deallocated.
#
# Examples usually include:
# - small integers
# - empty tuple
# - interned strings
#
# sys.getrefcount() on such objects returns huge numbers. This is not
# a bug — CPython simply never frees these objects, so a large refcount
# removes the need to maintain a real one.


# ----------------------------------------
# 5) Basic Refcount Behavior on Built-in Types
# ----------------------------------------

def builtins_demo() -> None:
    print("=== builtins_demo ===")
    a = 42
    b = 111222333
    print("int value a:", a)
    print("int value b:", b)
    print()

    print("id(a):", hex_id(a))
    print("id(b):", hex_id(b))
    print()

    print("int a tracked by GC?:", gc.is_tracked(a))
    print("int b tracked by GC?:", gc.is_tracked(a))
    print()

    print("getrefcount(a):", sys.getrefcount(a))
    print("getrefcount(b):", sys.getrefcount(b))
    print()

    lst = []
    print("list id:", hex_id(lst))
    print("list tracked by GC?:", gc.is_tracked(lst))
    print("list refcount:", sys.getrefcount(lst))
    print()

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
    print("refcount(o):", sys.getrefcount(o))

    alias = o
    print("after alias = o -> refcount:", sys.getrefcount(o))
    container = [o]
    print("after container holds o -> refcount:", sys.getrefcount(o))

    # remove alias but container keeps reference
    del alias
    print("after del alias -> refcount:", sys.getrefcount(o))

    # remove container reference
    del container
    print("after del container -> refcount:", sys.getrefcount(o))
    print()

    # end of function: local 'o' will go out of scope, reference count decreases
    # to the point where object can be deallocated (in CPython, immediately)


# ----------------------------------------
# 7) IDENTITY & ADDRESS INSPECTION (ctypes)
# ----------------------------------------
# We can read (not write) memory near the object address to illustrate
# that id(obj) corresponds to an address. This is for demonstration only.

def read_pointer_contents(obj: object, /, *, bytes_to_read: int = 64) -> bytes:
    """
    Read raw bytes starting at the memory address of obj.

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
    raw = read_pointer_contents(o, bytes_to_read=32)
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
    lst: list[int] = []
    print("initial id(list):", hex_id(lst), "size:", sys.getsizeof(lst))
    for i in range(32):
        lst.append(i)
        if i % 8 == 7:
            print(f"after {i+1} appends -> id: {hex_id(lst)} size: {sys.getsizeof(lst)}")
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
            self.other: Node | None = None
        def __repr__(self) -> str:
            return f"Node({self.name})"

    a = Node("A")
    b = Node("B")
    a.other = b
    b.other = a
    print("a id:", hex_id(a), "b id:", hex_id(b))
    print("a refcount:", sys.getrefcount(a), "b refcount:", sys.getrefcount(b))

    # drop external references
    del a
    del b
    # At this point refcounts do not drop to 0 because objects reference each other.
    # The cyclic garbage collector can detect and collect such cycles.
    found = gc.collect()
    print("gc.collect() found unreachable objects:", found)
    print()


# ----------------------------------------
# 10) PRACTICAL CHECKLIST FOR DEBUGGING OBJECT LIFETIME
# ----------------------------------------
# 1) Use getrefcount to estimate live references (remember the +1).
# 2) Use gc.is_tracked to see if object participates in cycle detection.


# ----------------------------------------
# 11) QUICK-RUN WHEN EXECUTED DIRECTLY
# ----------------------------------------

if __name__ == "__main__":
    builtins_demo()
    custom_class_demo()
    ctypes_demo()
    varobject_demo()
    circular_ref_demo()
