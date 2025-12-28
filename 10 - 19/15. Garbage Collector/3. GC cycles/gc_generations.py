"""
GC Cycles — Generational Garbage Collector in CPython.

This module explains and demonstrates how CPython's cyclic garbage
collector works: generations (0, 1, 2), thresholds, and collection triggers.

Focus:
- Difference between refcounting and cyclic GC
- Generational hypothesis
- gc.get_threshold / gc.get_count
- Forcing collections and observing behavior
"""

from __future__ import annotations
import gc


# ----------------------------------------
# 1) GC OVERVIEW (CONCEPTUAL)
# ----------------------------------------
# CPython uses:
# 1) Reference counting — immediate deallocation when refcount reaches zero
# 2) Cyclic GC — detects reference cycles that refcounting cannot break
#
# The cyclic GC is *generational*:
# - Generation 0: youngest objects, collected most often
# - Generation 1: objects that survived gen0 collections
# - Generation 2: long-lived objects, collected rarely


# ----------------------------------------
# 2) INSPECTING GC THRESHOLDS
#
# gc.get_threshold() returns a tuple (t0, t1, t2):
#
# t0 — generation 0 threshold
# How many net allocations (allocs - deallocs) must happen
# before GC automatically runs a generation-0 collection.
#
# t1 — generation 1 threshold
# How many generation-0 collections must occur
# before generation-1 is collected.
#
# t2 — generation 2 threshold
# How many generation-1 collections must occur
# before generation-2 (full GC) is collected.
#
# Example (typical defaults):
# gen0 = 2000
# gen1 = 10
# gen2 = 10
#
# Meaning:
# - After ~2000 allocations → collect gen0
# - After 10 gen0 collections → collect gen1
# - After 10 gen1 collections → collect gen2
#
# This reflects the *generational hypothesis*:
# most objects die young, so young generations are collected often,
# and old generations are collected rarely.
# ----------------------------------------

def show_thresholds() -> None:
    print("=== GC thresholds ===")
    t0, t1, t2 = gc.get_threshold()
    print(f"gen0 threshold: {t0}")
    print(f"gen1 threshold: {t1}")
    print(f"gen2 threshold: {t2}")
    print()


# ----------------------------------------
# 3) GC COUNTERS (ALLOCATION COUNTS)
# ----------------------------------------

def show_counts(label: str = "") -> None:
    if label:
        print(f"--- {label} ---")
    c0, c1, c2 = gc.get_count()
    print(f"gen0 count: {c0}")
    print(f"gen1 count: {c1}")
    print(f"gen2 count: {c2}")
    print()


# ----------------------------------------
# 4) CREATING GARBAGE OBJECTS
# ----------------------------------------

class Cycle:
    def __init__(self) -> None:
        self.other: Cycle | None = None


def make_cycles(n: int) -> list[Cycle]:
    """
    Create n isolated 2-object reference cycles.
    Objects are unreachable immediately after creation.
    """
    cycles: list[Cycle] = []
    for _ in range(n):
        a: Cycle = Cycle()
        b: Cycle = Cycle()
        a.other = b
        b.other = a
        cycles.append(a)
    return cycles


# ----------------------------------------
# 5) TRIGGERING GENERATION 0 COLLECTION
# ----------------------------------------

def gen0_demo() -> None:
    print("=== gen0_demo ===")
    show_counts("before allocations")

    garbage: list[Cycle] = make_cycles(5_000)
    # remove external references
    garbage.clear()

    show_counts("after allocations (before gc)")

    collected: int = gc.collect(0)
    print(f"gc.collect(0) collected: {collected}")
    show_counts("after gen0 collection")


# ----------------------------------------
# 6) PROMOTION TO HIGHER GENERATIONS
# ----------------------------------------

def promotion_demo() -> None:
    print("=== promotion_demo ===")

    survivors: list[list[int]] = []

    for round_ in range(5):
        # create long-lived objects
        survivors.append([i for i in range(1000)])
        show_counts(f"after round {round_}")
        gc.collect(0)

    print("Objects surviving multiple collections are promoted")
    show_counts("final")


# ----------------------------------------
# 7) FULL COLLECTION (GENERATION 2)
# ----------------------------------------

def full_collection_demo() -> None:
    print("=== full_collection_demo ===")
    show_counts("before")

    garbage: list[Cycle] = make_cycles(10_000)
    garbage.clear()

    collected: int = gc.collect()
    print(f"gc.collect() collected: {collected}")
    show_counts("after full collection")


# ----------------------------------------
# 8) DISABLING GC (DANGEROUS)
# ----------------------------------------

def disable_gc_demo() -> None:
    print("=== disable_gc_demo ===")
    print("GC enabled?:", gc.isenabled())

    gc.disable()
    print("GC enabled after disable?:", gc.isenabled())

    garbage: list[Cycle] = make_cycles(5_000)
    garbage.clear()

    print("Created cyclic garbage with GC disabled")
    show_counts("gc disabled")

    gc.enable()
    print("GC re-enabled")
    collected = gc.collect()
    print(f"collected after re-enable: {collected}")
    show_counts("gc enable")
    print()


# ----------------------------------------
# 9) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    show_thresholds()
    gen0_demo()
    promotion_demo()
    full_collection_demo()
    disable_gc_demo()
