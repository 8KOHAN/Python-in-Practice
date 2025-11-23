# This module provides a deep, step‑by‑step introduction to CPython’s
# reference counting mechanism. It explains what refcounts are, how
# CPython updates them, why they increase or decrease, and how to
# observe them safely.
#
# Important assumptions:
# - This material is CPython‑specific. PyPy, Jython, etc. do not behave
#   this way.
# - `sys.getrefcount(obj)` adds a temporary reference while evaluating the
#   call, so refcounts observed are always one higher than the “real”
#   value.
# - The refcount is the value of `ob_refcnt` inside the `PyObject` header
#
# Contents
# ========
# 0. Immortal Objects
# 1. What is a reference?
# 2. What is a refcount?
# 3. When does the refcount increase?
# 4. When does the refcount decrease?
# 5. How to use `sys.getrefcount`
# 6. Demonstrations of typical refcount patterns
# 7. Demonstration of temporary references
# 8. Pitfalls

from __future__ import annotations
import sys
from typing import Any


def header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# 0. Immortal Objects (Brief Overview)
#
# Some CPython objects are *immortal*, meaning their reference count never reaches zero
# and they are never deallocated. Introduced in PEP 683 for CPython 3.12+, this mechanism
# assigns certain frequently used singleton-like objects an extremely large refcount
# (typically `PY_IMMORTAL_REFCNT`, e.g., 2**60), making their lifetime effectively permanent.
#
# Why this matters for refcount basics:
# - `sys.getrefcount()` on numbers like 0, 1, small strings, empty tuple, and other core
# objects may show huge values.
# - This does not represent real references; it is an implementation detail for speed
# and future GIL removal work.
# - Immortal objects still participate in normal reference semantics at the API level,
# but their memory is never reclaimed.
#
# Examples:
# >>> import sys
# >>> sys.getrefcount(0)
# 1152921504606846977 # example huge immortal refcount (may vary by build)
#
# A full dedicated chapter will in the project inside
# `15. Garbage Collector/6. memory/immortal_objects.py`.


# ---------------------------------------------------------------------------
# 1. What is a reference?
# ---------------------------------------------------------------------------
# A *reference* in CPython is simply a pointer to a PyObject.
# Every name, variable, attribute, list slot, tuple item, function argument,
# temporary evaluation result, and most internal C stack operations create
# such references.
#
# For example:
#     a = []     # the name 'a' holds one reference to the list object
#
# If we now do:
#     b = a
# Then 'b' becomes another reference to the same object.
#
# The object therefore has **two references** keeping it alive.
# When the number of references drops to zero, CPython immediately frees the
# object (unless it participates in a cycle that requires the cyclic GC).


# ---------------------------------------------------------------------------
# 2. What is a refcount?
# ---------------------------------------------------------------------------
# Every CPython object includes an integer field `ob_refcnt`.
# It stores how many references currently point to that object.
#
# CPython updates this counter aggressively on every creation, assignment,
# function call, temporary expression evaluation, and cleanup.
#
# CPython's memory model is:
#     - reference counting is responsible for *immediate* deallocation
#     - the cyclic garbage collector detects and collects reference
#       cycles — sets of objects that reference one another yet are unreachable from any
#       root references (such as module globals, local variables on the stack, or active interpreter internals).
#       their reference counts never reach zero, and thus they require cycle detection to be reclaimed.



# ---------------------------------------------------------------------------
# 3. When does the refcount increase?
# ---------------------------------------------------------------------------
# Typical cases:
#   a) Assigning the object to a new variable
#   b) Inserting it into a container (list, dict, tuple, set)
#   c) Passing it as a function argument
#   d) Returning it from a function
#   e) Putting it into a temporary expression (Python/C stack)
#   f) Storing it inside an object attribute
#
# Example:
#     a = []          # list created; refcount = 1 (name 'a')
#     b = a           # refcount = 2 (names 'a' and 'b')
#     lst = [a, a]    # refcount = 4 (two slots in lst + two names)


# ---------------------------------------------------------------------------
# 4. When does the refcount decrease?
# ---------------------------------------------------------------------------
#   a) Removing a name with 'del'
#   b) Leaving a function scope
#   c) Reassigning a variable (old object loses one reference)
#   d) Removing an element from a container
#   e) Container deallocation
#   f) Destruction of temporary evaluation results


# ---------------------------------------------------------------------------
# 5. sys.getrefcount
# ---------------------------------------------------------------------------
# CPython provides sys.getrefcount(obj) for debugging.
# BUT: It adds a temporary reference for the duration of the call.
# So the real refcount is (getrefcount(obj) - 1).


# ---------------------------------------------------------------------------
# 6. Demo: simple refcount changes
# ---------------------------------------------------------------------------

def basic_refcount_demo() -> None:
    header("basic_refcount_demo")

    obj = []
    print("Initial refcount (1 name + temporary):", sys.getrefcount(obj))

    a = obj
    print("After 'a = obj':", sys.getrefcount(obj))

    b = obj
    print("After 'b = obj':", sys.getrefcount(obj))

    lst = [obj]
    print("After list containing obj:", sys.getrefcount(obj))

    del a
    print("After 'del a':", sys.getrefcount(obj))

    del lst
    print("After deleting the list:", sys.getrefcount(obj))

    # At the end of function: 'obj' and 'b' will go out of scope


# ---------------------------------------------------------------------------
# 7. Demo: temporary references
# ---------------------------------------------------------------------------
# Many operations temporarily increase refcount. Example:
#   sys.getrefcount(obj)
#   f(obj)         # during call creation
#   [obj] + [obj]  # constructing new lists


def temporary_refs_demo() -> None:
    header("temporary_refs_demo")
    x = object()

    print("Raw getrefcount(x):", sys.getrefcount(x))
    # It is actually real_refcount + 1
    print("Real refcount is one lower.")

    print("Evaluating in a list expression:")
    print([sys.getrefcount(x), sys.getrefcount(x)])
    # Both expressions add temporary references.

    print("Passing x as a function argument (observe temporary bump):")

    def f(obj: Any) -> None:
        print("Inside f():", sys.getrefcount(obj))

    print("Before call:", sys.getrefcount(x))
    f(x)  # CPython pushes 'x' on stack, adding a temporary ref
    print("After call:", sys.getrefcount(x))


# ---------------------------------------------------------------------------
# 8. Pitfalls
# ---------------------------------------------------------------------------
# Example pitfalls:
#   - Using refcounts to determine object identity or lifetime in
#     non-CPython implementations.
#   - Assuming refcount alone handles cycles (it does not).
#   - Forgetting about hidden references in stack frames and closures.
#   - Misinterpreting sys.getrefcount output.


if __name__ == "__main__":
    basic_refcount_demo()
    temporary_refs_demo()
