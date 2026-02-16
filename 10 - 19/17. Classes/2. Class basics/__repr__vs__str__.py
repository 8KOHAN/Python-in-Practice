"""
Explains the semantic and practical difference between __repr__ and __str__,
including debugging philosophy, round-trippable representations,
and interaction with print(), repr(), and f-strings.
"""

from __future__ import annotations


# ----------------------------------------
# 1) DEFAULT BEHAVIOR
# ----------------------------------------

def default_behavior_demo() -> None:
    print("=== default_behavior_demo ===")

    class User:
        pass

    user: User = User()

    # print() calls str(obj)
    print(f"print(user): {user}")

    # repr() calls obj.__repr__()
    print(f"repr(user): {repr(user)}")

    # If __str__ is not defined,
    # Python falls back to __repr__.

    print()


# ----------------------------------------
# 2) DEFINING ONLY __repr__
# ----------------------------------------

def repr_only_demo() -> None:
    print("=== repr_only_demo ===")

    class Point:
        def __init__(self, x: int, y: int, /) -> None:
            self.x: int = x
            self.y: int = y

        def __repr__(self) -> str:
            # __repr__ should be:
            # - unambiguous
            # - developer-focused
            # - ideally valid Python expression
            return f"Point(x={self.x}, y={self.y})"

    p: Point = Point(1, 2)

    print(f"print(p): {p}")        # falls back to __repr__
    print(f"repr(p): {repr(p)}")

    print()


# ----------------------------------------
# 3) DEFINING BOTH __repr__ AND __str__
# ----------------------------------------

def repr_vs_str_demo() -> None:
    print("=== repr_vs_str_demo ===")

    class User:
        def __init__(self, username: str, /) -> None:
            self.username: str = username

        def __repr__(self) -> str:
            # Developer-oriented representation
            return f"User(username={self.username!r})"

        def __str__(self) -> str:
            # User-friendly representation
            return self.username

    user: User = User("alice")

    print(f"print(user): {user}")        # calls __str__
    print(f"repr(user): {repr(user)}")   # calls __repr__

    print()


# ----------------------------------------
# 4) ROUND-TRIP PRINCIPLE
# ----------------------------------------

def round_trip_demo() -> None:
    print("=== round_trip_demo ===")

    class Vector:
        def __init__(self, x: float, y: float, /) -> None:
            self.x: float = x
            self.y: float = y

        def __repr__(self) -> str:
            # Ideal case:
            # eval(repr(obj)) == obj
            return f"Vector({self.x}, {self.y})"

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Vector):
                return NotImplemented
            return self.x == other.x and self.y == other.y

    v1: Vector = Vector(1.0, 2.0)

    reconstructed: Vector = eval(repr(v1))

    print(f"v1 == reconstructed: {v1 == reconstructed}")

    print()


# ----------------------------------------
# 5) f-STRINGS AND FORMAT BEHAVIOR
# ----------------------------------------

def formatting_behavior_demo() -> None:
    print("=== formatting_behavior_demo ===")

    class Item:
        def __repr__(self) -> str:
            return "Item(repr)"

        def __str__(self) -> str:
            return "Item(str)"

    item: Item = Item()

    # Default f-string uses str()
    print(f"default: {item}")

    # !r forces repr()
    print(f"repr forced: {item!r}")

    print()


# ----------------------------------------
# 6) DESIGN GUIDELINES (THEORETICAL)
# ----------------------------------------
#
# __repr__ should:
# - be unambiguous
# - target developers
# - include enough information to understand object state
# - ideally be valid constructor syntax
#
# __str__ should:
# - be readable
# - target end users
# - avoid exposing internal details


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    default_behavior_demo()
    repr_only_demo()
    repr_vs_str_demo()
    round_trip_demo()
    formatting_behavior_demo()
