"""
CPython memory allocation: pymalloc, arenas, pools, blocks.

This module explains how CPython allocates memory for Python objects,
how this relates to garbage collection, and why freeing objects does
NOT necessarily return memory to the operating system.
"""

from __future__ import annotations

import sys
import gc
from typing import Any


# ----------------------------------------
# 1) BIG PICTURE: GC vs MEMORY ALLOCATION
# ----------------------------------------
#
# IMPORTANT DISTINCTION:
#
# - Garbage Collection (GC) decides *WHEN* an object is no longer needed
# - Memory Allocator decides *HOW* memory is obtained and reused
#
# In CPython:
# - refcount + cyclic GC decide object lifetime
# - pymalloc decides how memory blocks are allocated and recycled
#
# Even if an object is destroyed:
# - its memory is usually returned to pymalloc
# - NOT returned to the OS immediately


# ----------------------------------------
# 2) WHAT IS pymalloc?
# ----------------------------------------
#
# pymalloc is CPython's private memory allocator for SMALL OBJECTS.
#
# Rough rules (64-bit CPython, typical build):
# - Objects <= 512 bytes -> pymalloc
# - Larger objects        -> system malloc()
#
# pymalloc hierarchy:
#
#   ARENA  (256 KB)
#     └── POOLS (4 KB, one OS page)
#           └── BLOCKS (fixed-size slots, e.g. 32B, 64B, 128B...)
#
# pymalloc reuses freed blocks aggressively.
# Memory almost never goes back to the OS.


# ----------------------------------------
# 3) OBSERVING pymalloc FROM PYTHON
# ----------------------------------------

def small_object_allocation_demo() -> None:
    print("=== small_object_allocation_demo ===")

    objs: list[Any] = []

    for i in range(10_000):
        objs.append(object())

    print("created 10k small objects")
    print("example object id:", hex(id(objs[0])))
    print("object tracked by GC?:", gc.is_tracked(objs[0]))

    # delete references
    del objs

    # force GC (does NOT free arenas!)
    collected = gc.collect()
    print("gc.collect() -> collected:", collected)
    print("NOTE: memory not returned to OS\n")


# ----------------------------------------
# 4) sys.getsizeof VS REAL MEMORY USAGE
# ----------------------------------------
#
# sys.getsizeof(obj):
# - size of the PyObject struct + inline data
# - DOES NOT include allocator overhead
#
# Real memory cost includes:
# - block padding
# - pool fragmentation
# - arena retention

def sizeof_demo() -> None:
    print("=== sizeof_demo ===")

    lst: int = []
    print("empty list getsizeof:", sys.getsizeof(lst))

    for i in range(100):
        lst.append(i)

    print("list with 100 items getsizeof:", sys.getsizeof(lst))
    print("NOTE: actual memory usage is larger due to overallocation\n")


# ----------------------------------------
# 5) ARENAS: WHY MEMORY IS NOT RELEASED
# ----------------------------------------
#
# Arenas (~256 KB) are obtained from the OS.
# Even if all objects inside are freed:
# - arena usually stays reserved
#
# This explains:
# - RSS grows
# - RSS does not shrink
#
# This is NOT a memory leak.

def arena_behavior_demo() -> None:
    print("=== arena_behavior_demo ===")

    big_list: list[list[int]] = []
    for _ in range(50_000):
        big_list.append([0] * 10)

    print("allocated many small lists")

    del big_list

    print("objects deleted")
    print("BUT arenas are still held by pymalloc\n")


# ----------------------------------------
# 6) BLOCK SIZES AND ALLOCATION CLASSES
# ----------------------------------------
#
# pymalloc uses size classes:
# 8, 16, 24, 32, ..., up to 512 bytes
#
# Objects are rounded UP to the nearest class.
#
# Example:
# - object of size 33 bytes -> uses 40 or 48 byte block

def allocation_rounding_demo() -> None:
    print("=== allocation_rounding_demo ===")

    print("sizeof(object()):", sys.getsizeof(object()))

    ints: list[int] = [sys.getsizeof(i) for i in range(5)]
    print("sizeof small ints:", ints)
    print("NOTE: allocator rounds sizes internally\n")


# ----------------------------------------
# 7) LARGE OBJECTS: BYPASSING pymalloc
# ----------------------------------------
#
# Objects > 512 bytes usually:
# - allocated via system malloc
# - may return memory to OS (platform dependent)

def large_object_demo() -> None:
    print("=== large_object_demo ===")

    big_list: list[int] = [0] * 1_000_000
    print("big list getsizeof:", sys.getsizeof(big_list))

    del big_list

    print("large object deleted")
    print("memory MAY be returned to OS (depends on libc)\n")


# ----------------------------------------
# 8) ctypes VIEW: MEMORY IS REUSED
# ----------------------------------------
#
# Demonstrate that freed memory is reused for new objects.

def memory_reuse_demo() -> None:
    print("=== memory_reuse_demo ===")

    a = object()
    addr_a = id(a)
    print("object a id:", hex(addr_a))

    del a

    b = object()
    addr_b = id(b)
    print("object b id:", hex(addr_b))

    print("addresses equal?:", addr_a == addr_b)
    print("NOTE: reuse is common but not guaranteed\n")


# ----------------------------------------
# 9) COMMON MISCONCEPTIONS
# ----------------------------------------
#
# "GC frees memory"
# "del returns memory to OS"
# "gc.collect reduces RSS"
#
# GC frees OBJECTS
# pymalloc reuses MEMORY
# OS memory return is allocator/platform specific


# ----------------------------------------
# 10) QUICK CHECKLIST
# ----------------------------------------
#
# - Growing RSS ≠ memory leak
# - pymalloc keeps arenas
# - sys.getsizeof is NOT full memory cost
# - Use tracemalloc to debug real leaks


# ----------------------------------------
# 11) QUICK RUN
# ----------------------------------------

if __name__ == "__main__":
    small_object_allocation_demo()
    sizeof_demo()
    arena_behavior_demo()
    allocation_rounding_demo()
    large_object_demo()
    memory_reuse_demo()
