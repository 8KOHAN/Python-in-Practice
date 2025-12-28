"""
GC Cycles — How CPython Detects and Collects Reference Cycles.

This module focuses on *how* CPython finds unreachable objects
in reference cycles and why reference counting alone is insufficient.

Focus:
- What makes an object "GC-tracked"
- Reachability vs refcount
- How unreachable cycles are detected
- gc.is_tracked / gc.get_objects
"""

from __future__ import annotations
import gc


# ----------------------------------------
# 1) WHY REFCOUNT IS NOT ENOUGH
# ----------------------------------------
# Reference counting fails when objects reference each other:
#
#   A -> B
#   B -> A
#
# Even if no external references exist, refcount never drops to zero.
# Cyclic GC solves this by *graph analysis*.


# ----------------------------------------
# 2) A SIMPLE CYCLIC STRUCTURE
# ----------------------------------------

class Node:
    def __init__(self, name: str):
        self.name = name
        self.other: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.name})"


def create_cycle() -> Node:
    a: Node = Node("A")
    b: Node = Node("B")
    a.other = b
    b.other = a
    return a


# ----------------------------------------
# 3) TRACKED VS UNTRACKED OBJECTS
# ----------------------------------------
# The cyclic GC does NOT track all Python objects.
#
# GC tracking is about whether an object needs to be examined
# for participation in reference cycles.
#
# IMPORTANT:
# - "immutable" does NOT automatically mean "untracked"
# - GC tracking is a dynamic optimization, not a type property
#
# General rules (CPython implementation details):
# - User-defined class instances are always GC-tracked
#   because they can dynamically reference other objects.
# - Small immutable objects (int, float, None, etc.) are not tracked.
# - Container objects (tuple, list, dict, set) are usually created as tracked.
# - Immutable containers MAY later become untracked if:
#     * they contain only untracked objects
#     * and the GC has had a chance to optimize them
#
# As a result, gc.is_tracked(obj) may return different values
# depending on timing, GC activity, and Python version.


def tracking_demo() -> None:
    print("=== tracking_demo ===")

    node: Node = create_cycle()
    # User-defined class instances are always tracked
    print("Node tracked?:", gc.is_tracked(node))
    print("Node.other tracked?:", gc.is_tracked(node.other))

    # Small immutable objects are not tracked
    i = 42
    print("int tracked?:", gc.is_tracked(i))

    # Immutable containers may or may not be tracked
    t = (1, 2, 3)
    print("tuple tracked (before GC)?:", gc.is_tracked(t))

    # Force a GC run to give CPython a chance to untrack it
    gc.collect()
    print("tuple tracked (after GC)?:", gc.is_tracked(t))

    # If a container references a tracked object,
    # it must remain tracked itself
    t2 = (node,)
    gc.collect()
    print("tuple with Node tracked?:", gc.is_tracked(t2))
    print()


# ----------------------------------------
# 4) UNREACHABLE OBJECTS
# ----------------------------------------
# GC does NOT care about refcount directly.
# It cares whether objects are *reachable* from GC roots.

def unreachable_demo() -> None:
    print("=== unreachable_demo ===")

    node: Node = create_cycle()
    print("created cycle")

    # remove last external reference
    del node

    # At this point:
    # - refcount != 0
    # - objects are unreachable
    collected: int = gc.collect()
    print(f"gc.collect() collected: {collected}")
    print()


# ----------------------------------------
# 5) LISTING TRACKED OBJECTS
# ----------------------------------------

def list_tracked_demo() -> None:
    print("=== list_tracked_demo ===")

    objs = gc.get_objects()
    print(f"Total tracked objects: {len(objs)}")

    nodes: list[Node] = [o for o in objs if isinstance(o, Node)]
    print(f"Tracked Node objects: {len(nodes)}")
    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    tracking_demo()
    unreachable_demo()
    list_tracked_demo()
