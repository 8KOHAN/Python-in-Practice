"""
GC Debug Tools — Inspecting Object Graphs in CPython.

This module demonstrates practical tools provided by the `gc` module
to inspect object relationships and debug garbage collection behavior.

Focus:
- gc.get_objects
- gc.get_referrers
- gc.get_referents
- gc.DEBUG_* flags
- gc.garbage and unreachable objects
"""

from __future__ import annotations
import gc


# ----------------------------------------
# 1) A SIMPLE OBJECT GRAPH
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
# 2) gc.get_objects()
# ----------------------------------------
# gc.get_objects() returns a list of ALL objects
# currently tracked by the cyclic GC.
#
# IMPORTANT:
# - Only GC-tracked objects appear here
# - Small immutables (int, float, etc.) do NOT appear

def get_objects_demo() -> None:
    print("=== get_objects_demo ===")

    objs = gc.get_objects()
    print(f"Total tracked objects: {len(objs)}")

    nodes = [o for o in objs if isinstance(o, Node)]
    print(f"Tracked Node objects: {len(nodes)}")
    print()


# ----------------------------------------
# 3) gc.get_referents()
# ----------------------------------------
# gc.get_referents(obj) shows objects that `obj`
# directly references.
#
# This answers: "What does this object point to?"

def get_referents_demo() -> None:
    print("=== get_referents_demo ===")

    node: Node = create_cycle()
    refs = gc.get_referents(node)

    print("Node referents:")
    for r in refs:
        print(" ", type(r).__name__, "->", r)
    print()


# ----------------------------------------
# 4) gc.get_referrers()
# ----------------------------------------
# gc.get_referrers(obj) shows objects that reference `obj`.
#
# This answers: "Who is holding a reference to this object?"
#
# WARNING:
# - The result often includes stack frames and locals
# - Use only for debugging and exploration

def get_referrers_demo() -> None:
    print("=== get_referrers_demo ===")

    node: Node = create_cycle()
    referrers = gc.get_referrers(node)

    print(f"Number of referrers: {len(referrers)}")
    for r in referrers:
        print(" ", type(r).__name__)
    print()


# ----------------------------------------
# 5) DEBUG FLAGS
# ----------------------------------------
# GC provides debug flags that print information
# during collection.
#
# Common flags:
# - gc.DEBUG_STATS    -> print statistics
# - gc.DEBUG_SAVEALL  -> save unreachable objects in gc.garbage

def debug_flags_demo() -> None:
    print("=== debug_flags_demo ===")

    gc.set_debug(gc.DEBUG_STATS)

    # create unreachable cycles
    node: Node = create_cycle()
    del node

    print("Running gc.collect() with DEBUG_STATS")
    gc.collect()

    # reset flags
    gc.set_debug(0)
    print()


# ----------------------------------------
# 6) gc.garbage and DEBUG_SAVEALL
# ----------------------------------------
# If DEBUG_SAVEALL is enabled:
# - unreachable objects are NOT freed
# - they are appended to gc.garbage
#
# This is useful to inspect objects
# that would normally be collected.

def garbage_demo() -> None:
    print("=== garbage_demo ===")

    gc.set_debug(gc.DEBUG_SAVEALL)

    node: Node = create_cycle()
    del node

    collected: int = gc.collect()
    print(f"gc.collect() collected: {collected}")
    print(f"gc.garbage length: {len(gc.garbage)}")

    for obj in gc.garbage:
        print(" garbage:", obj)

    # cleanup
    gc.garbage.clear()
    gc.set_debug(0)
    print()


# ----------------------------------------
# 7) IMPORTANT WARNINGS
# ----------------------------------------
# - gc.get_referrers() can keep objects alive
# - Debug tools themselves affect GC behavior
# - Never use these functions in production logic
#
# They are for:
# - debugging
# - teaching
# - exploratory analysis


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    get_objects_demo()
    get_referents_demo()
    get_referrers_demo()
    debug_flags_demo()
    garbage_demo()
