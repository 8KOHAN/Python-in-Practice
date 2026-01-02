"""
Fragmentation in CPython memory management.

This module demonstrates why freeing Python objects does NOT necessarily
return memory to the operating system and why memory usage may appear
to "leak" even when GC runs successfully.

Focus:
- internal vs external fragmentation
- pymalloc behavior
- arenas, pools, and blocks
- why CPython does not compact memory
"""

from __future__ import annotations
import gc
import tracemalloc


# ----------------------------------------
# 1) Fragmentation basics
# ----------------------------------------
# Fragmentation means that free memory exists, but it is split into
# chunks that cannot be reused efficiently or returned to the OS.
#
# - Internal fragmentation:
#   Memory wasted *inside* allocated blocks (rounding, fixed sizes)
#
# - External fragmentation:
#   Memory wasted *between* allocated blocks (holes)


# ----------------------------------------
# 2) Why GC does not fix fragmentation
# ----------------------------------------
# CPython's GC:
# - detects unreachable objects
# - calls their deallocators
#
# GC does NOT:
# - move objects
# - compact memory
# - reorder allocations
#
# Therefore, fragmentation remains.


# ----------------------------------------
# 3) Fragmentation in pymalloc
# ----------------------------------------
# pymalloc hierarchy:
#
#   arena (256 KB)
#     └── pool (4 KB)
#           └── blocks (8..512 bytes)
#
# Freeing objects:
# - frees blocks
# - pools remain
# - arenas remain
#
# Memory is reusable by Python, but not returned to the OS.


# ----------------------------------------
# 4) Allocation / deallocation demo
# ----------------------------------------

def fragmentation_demo() -> None:
    print("=== fragmentation_demo ===")

    tracemalloc.start()

    # allocate many small objects
    data: list[list[int]] = []
    for _ in range(50_000):
        data.append([0] * 10)

    current, peak = tracemalloc.get_traced_memory()
    print("after allocation:")
    print(f"  current = {current / 1024:.1f} KB")
    print(f"  peak    = {peak / 1024:.1f} KB")

    # remove references
    del data
    gc.collect()

    current, peak = tracemalloc.get_traced_memory()
    print("after deletion + gc:")
    print(f"  current = {current / 1024:.1f} KB")
    print(f"  peak    = {peak / 1024:.1f} KB")

    tracemalloc.stop()
    print()

    # NOTE:
    # tracemalloc reports Python-level allocations only.
    # After objects are freed, tracemalloc.current drops,
    # even though allocator arenas and pools may remain
    # allocated at the OS level (fragmentation).


# ----------------------------------------
# 5) Why CPython cannot compact memory
# ----------------------------------------
# - id(obj) == memory address (CPython)
# - moving objects would invalidate:
#   - C extensions
#   - ctypes pointers
#   - borrowed references
#
# Therefore, CPython uses non-moving GC.


# ----------------------------------------
# 6) Practical implications
# ----------------------------------------
# - "Memory leak" symptoms without real leaks
# - Long-lived processes grow RSS
# - Restarting process frees arenas
# - tracemalloc shows Python-level leaks only


# ----------------------------------------
# 7) Quick run
# ----------------------------------------

if __name__ == "__main__":
    fragmentation_demo()
