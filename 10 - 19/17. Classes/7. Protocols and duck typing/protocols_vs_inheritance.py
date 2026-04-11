"""
Compares Protocol (structural typing) and inheritance (nominal typing).
Focuses on differences in flexibility, coupling, and design implications.
"""

from __future__ import annotations

from typing import Protocol


# ----------------------------------------
# 1) NOMINAL TYPING (INHERITANCE)
# ----------------------------------------

# In nominal typing, type compatibility is based on explicit inheritance.
# Object must inherit from a base class to be considered compatible.

class Animal:
    def speak(self) -> str:
        raise NotImplementedError


class Dog(Animal):
    def speak(self) -> str:
        return "woof"


class Cat(Animal):
    def speak(self) -> str:
        return "meow"


def make_sound_nominal(animal: Animal) -> None:
    print("=== make_sound_nominal ===")

    print(animal.speak())

    print()


def nominal_typing_demo() -> None:
    print("=== nominal_typing_demo ===")

    dog = Dog()
    cat = Cat()

    make_sound_nominal(dog)
    make_sound_nominal(cat)

    print()


# ----------------------------------------
# 2) STRUCTURAL TYPING (PROTOCOL)
# ----------------------------------------

# In structural typing, compatibility is based on behavior.
# Object does NOT need to inherit from anything.

class SupportsSpeak(Protocol):
    def speak(self) -> str:
        ...


def make_sound_structural(obj: SupportsSpeak) -> None:
    print("=== make_sound_structural ===")

    print(obj.speak())

    print()


def structural_typing_demo() -> None:
    print("=== structural_typing_demo ===")

    class Robot:
        def speak(self) -> str:
            return "beep"

    class Human:
        def speak(self) -> str:
            return "hello"

    robot = Robot()
    human = Human()

    # No inheritance, but both are valid
    make_sound_structural(robot)
    make_sound_structural(human)

    print()


# ----------------------------------------
# 3) FLEXIBILITY VS CONTROL
# ----------------------------------------

# Inheritance:
# + Explicit relationships
# + Clear hierarchy
# - Strong coupling
# - Harder to extend without modifying base classes

# Protocol:
# + Loose coupling
# + Works with existing code (no modification required)
# + More flexible in large systems
# - Less explicit relationships
# - Easier to accidentally match wrong structure


def flexibility_vs_control_demo() -> None:
    print("=== flexibility_vs_control_demo ===")

    class LegacyPrinter:
        def print(self) -> None:
            print("Printing...")

    # Protocol-like usage without inheritance
    def use_printer(obj: object) -> None:
        if hasattr(obj, "print"):
            obj.print()

    printer = LegacyPrinter()
    use_printer(printer)

    print()


# ----------------------------------------
# 4) RETROFITTING EXISTING CODE
# ----------------------------------------

# One of the biggest advantages of Protocol:
# You can apply it to existing classes without modifying them.

class SupportsLen(Protocol):
    def __len__(self) -> int:
        ...


def use_length(obj: SupportsLen) -> None:
    print("=== use_length ===")

    print(f"Length: {len(obj)}")

    print()


def retrofitting_demo() -> None:
    print("=== retrofitting_demo ===")

    data = [1, 2, 3]

    # list already has __len__, no changes needed
    use_length(data)

    print()


# ----------------------------------------
# 5) WHEN TO USE EACH APPROACH
# ----------------------------------------

# Use inheritance when:
# - you control the class hierarchy
# - you need shared implementation
# - relationships are stable and explicit

# Use Protocol when:
# - you care about behavior, not identity
# - you work with external or legacy code
# - you want loose coupling
# - you design flexible APIs


# ----------------------------------------
# 6) COMMON MISTAKE
# ----------------------------------------

# Mistake:
# Treating Protocol as a replacement for inheritance everywhere

# Protocol is not a universal solution.
# It complements inheritance, not replaces it.


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    nominal_typing_demo()
    structural_typing_demo()
    flexibility_vs_control_demo()
    retrofitting_demo()
