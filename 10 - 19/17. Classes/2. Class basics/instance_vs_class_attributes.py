"""
Explains the difference between instance attributes and class attributes,
including mutation semantics, shadowing behavior, and common pitfalls.
"""

from __future__ import annotations


# ----------------------------------------
# 1) CLASS ATTRIBUTE BASICS
# ----------------------------------------

def class_attribute_basics_demo() -> None:
    print("=== class_attribute_basics_demo ===")

    class Config:
        # Class attribute
        version: int = 1

    # Access via class
    print(f"Config.version: {Config.version}")

    obj: Config = Config()

    # Access via instance (resolved from class)
    print(f"obj.version: {obj.version}")

    # No instance attribute exists yet
    print(f"'version' in obj.__dict__: {'version' in obj.__dict__}")

    print()


# ----------------------------------------
# 2) INSTANCE ATTRIBUTE CREATION
# ----------------------------------------

def instance_attribute_creation_demo() -> None:
    print("=== instance_attribute_creation_demo ===")

    class User:
        role: str = "guest"

        def __init__(self, name: str, /) -> None:
            # Instance attribute
            self.name: str = name

    user: User = User("Alice")

    # Instance attribute
    print(f"user.name: {user.name}")

    # Class attribute accessed via instance
    print(f"user.role: {user.role}")

    print(f"user.__dict__: {user.__dict__}")

    print()


# ----------------------------------------
# 3) SHADOWING CLASS ATTRIBUTE
# ----------------------------------------

def shadowing_class_attribute_demo() -> None:
    print("=== shadowing_class_attribute_demo ===")

    class Settings:
        mode: str = "production"

    s: Settings = Settings()

    # Initially resolved from class
    print(f"s.mode (before): {s.mode}")

    # This creates an instance attribute, shadowing the class attribute
    s.mode = "debug"

    print(f"s.mode (after): {s.mode}")
    print(f"Settings.mode (class unchanged): {Settings.mode}")

    print(f"s.__dict__: {s.__dict__}")

    print()


# ----------------------------------------
# 4) MUTABLE CLASS ATTRIBUTE PITFALL
# ----------------------------------------

def mutable_class_attribute_demo() -> None:
    print("=== mutable_class_attribute_demo ===")

    class Registry:
        # Dangerous pattern: mutable class attribute
        items: list[str] = []

    a: Registry = Registry()
    b: Registry = Registry()

    # Mutating via instance mutates shared class-level object
    a.items.append("A")

    print(f"a.items: {a.items}")
    print(f"b.items (shared): {b.items}")
    print(f"Registry.items: {Registry.items}")

    print()

    # Correct pattern: initialize mutable state per instance

    class SafeRegistry:
        def __init__(self, /) -> None:
            self.items: list[str] = []

    x: SafeRegistry = SafeRegistry()
    y: SafeRegistry = SafeRegistry()

    x.items.append("X")

    print(f"x.items: {x.items}")
    print(f"y.items (independent): {y.items}")

    print()


# ----------------------------------------
# 5) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    class_attribute_basics_demo()
    instance_attribute_creation_demo()
    shadowing_class_attribute_demo()
    mutable_class_attribute_demo()
