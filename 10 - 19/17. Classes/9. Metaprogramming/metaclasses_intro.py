"""
Introduces metaclasses in Python: what they are, how they work,
and how they control class creation itself.
"""

from __future__ import annotations

# ----------------------------------------
# 1) CLASSES ARE OBJECTS
# ----------------------------------------

def classes_are_objects_demo() -> None:
    print("=== classes_are_objects_demo ===")

    # In Python, classes are objects too

    class A:
        pass

    print(f"type(A): {type(A)}")
    print(f"A is object: {isinstance(A, object)}")

    # Key idea:
    # If A is an object, then it must be created by something

    print()


# ----------------------------------------
# 2) WHAT CREATES A CLASS
# ----------------------------------------

def class_creation_mechanism_demo() -> None:
    print("=== class_creation_mechanism_demo ===")

    # When you define a class:

    class A:
        x = 10

    # Python internally does something like:

    # A = type("A", (object,), {"x": 10})

    print(f"A.x: {A.x}")
    print(f"type(A): {type(A)}")

    print()


# ----------------------------------------
# 3) METACLASS IS "CLASS OF A CLASS"
# ----------------------------------------

def metaclass_concept_demo() -> None:
    print("=== metaclass_concept_demo ===")

    class A:
        pass

    # A is instance of type
    print(f"type(A): {type(A)}")

    # type is the default metaclass in Python

    print()


# ----------------------------------------
# 4) CUSTOM METACLASS
# ----------------------------------------

def custom_metaclass_demo() -> None:
    print("=== custom_metaclass_demo ===")

    # Metaclass controls class creation

    class Meta(type):
        def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict):
            print(f"Creating class: {name}")

            # You can modify class BEFORE it is created
            namespace["added_attr"] = "injected by metaclass"

            return super().__new__(mcs, name, bases, namespace)

    class A(metaclass=Meta):
        x = 10

    a = A()

    print(f"A.added_attr: {A.added_attr}")

    print()


# ----------------------------------------
# 5) WHEN METACLASSES ARE USED
# ----------------------------------------
#
# Metaclasses are a very low-level mechanism in Python.
# They control how classes themselves are created, not instances.
#
# They are typically used in advanced frameworks and infrastructure code:
#
# - frameworks (Django ORM, SQLAlchemy)
#   → automatic generation of model classes and query behavior
#
# - automatic class registration
#   → classes are registered in global registries when defined
#
# - generating APIs or DSL-like systems
#   → building domain-specific class behavior automatically
#
# Metaclasses should NOT be used for:
#
# - simple logic
#   → regular functions or class methods are enough
#
# - business rules
#   → should live in domain/services, not in class creation layer
#
# - small modifications
#   → class decorators are simpler, clearer, and safer
#
# Key idea:
# Metaclasses operate at the highest level of the Python object model.
# They define how classes are constructed, before any instances exist.


# ----------------------------------------
# 6) THEORETICAL MODEL
# ----------------------------------------
#
# Class creation pipeline in Python:
#
# 1) class body executes
# 2) namespace dictionary is created
# 3) metaclass is chosen (default: type)
# 4) metaclass.__new__ is called
# 5) class object is created
# 6) metaclass.__init__ runs (optional step)
#
# Equivalent:
#
# MyClass = Meta("MyClass", bases, namespace)


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    classes_are_objects_demo()
    class_creation_mechanism_demo()
    metaclass_concept_demo()
    custom_metaclass_demo()
