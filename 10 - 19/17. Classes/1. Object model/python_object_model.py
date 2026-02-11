"""
Core mechanics of Python object model.

This file demonstrates:
- Everything is an object
- Relationship between objects, types and metaclasses
- type() and id()
- Identity vs equality
- Object mutability at the model level
- Basic introspection primitives
"""
from __future__ import annotations


# ----------------------------------------
# 1) EVERYTHING IS AN OBJECT
# ----------------------------------------

def everything_is_object_demo() -> None:
    print("=== everything_is_object_demo ===")

    # In Python, every value is an object.
    # That includes:
    # - integers
    # - floats
    # - strings
    # - functions
    # - classes
    # - modules
    # - even types themselves

    number: int = 42
    text: str = "hello"
    items: list[int] = [1, 2, 3]

    print(f"type(number): {type(number)}")
    print(f"type(text): {type(text)}")
    print(f"type(items): {type(items)}")

    # Functions are also objects.
    def sample_function() -> None:
        pass

    print(f"type(sample_function): {type(sample_function)}")

    # Classes are objects.
    class SampleClass:
        pass

    print(f"type(SampleClass): {type(SampleClass)}")

    # Even 'type' itself is an object.
    print(f"type(type): {type(type)}")

    print()


# ----------------------------------------
# 2) TYPE, CLASS AND METACLASS RELATIONSHIP
# ----------------------------------------

def type_and_metaclass_demo() -> None:
    print("=== type_and_metaclass_demo ===")

    # Every object has a type.
    # Every class is also an object.
    # The type of most classes is 'type'.
    #
    # 'type' is the default metaclass in Python.
    # It is responsible for creating classes.

    class User:
        pass

    user: User = User()

    print(f"type(user): {type(user)}")
    print(f"type(User): {type(User)}")

    # This forms a core loop in Python's object model:
    # - user is instance of User
    # - User is instance of type
    # - type is instance of type

    print(f"type(type): {type(type)}")

    print()


# ----------------------------------------
# 3) IDENTITY VS EQUALITY
# ----------------------------------------

def identity_vs_equality_demo() -> None:
    print("=== identity_vs_equality_demo ===")

    # Identity refers to object identity in memory.
    # It is checked using 'is'.
    #
    # Equality refers to value comparison.
    # It is checked using '=='.

    a: list[int] = [1, 2, 3]
    b: list[int] = [1, 2, 3]
    c: list[int] = a

    print(f"a == b: {a == b}")   # same value
    print(f"a is b: {a is b}")   # different objects

    print(f"a is c: {a is c}")   # same object

    # id() returns the identity of the object.
    # CPython uses memory address as identity implementation detail.
    print(f"id(a): {id(a)}")
    print(f"id(b): {id(b)}")
    print(f"id(c): {id(c)}")

    print()


# ----------------------------------------
# 4) MUTABILITY AT OBJECT MODEL LEVEL
# ----------------------------------------

def mutability_demo() -> None:
    print("=== mutability_demo ===")

    # Mutability means whether the internal state of an object
    # can be changed without changing its identity.

    # Immutable example
    x: int = 10
    print(f"id(x) before change: {id(x)}")

    x = x + 1
    print(f"id(x) after change:  {id(x)}")

    # The identity changed because a new integer object was created.

    # Mutable example
    data: list[int] = [1, 2, 3]
    print(f"id(data) before append: {id(data)}")

    data.append(4)
    print(f"id(data) after append:  {id(data)}")

    # The identity stayed the same.
    # The internal state changed.

    print()


# ----------------------------------------
# 5) BASIC INTROSPECTION
# ----------------------------------------

def introspection_demo() -> None:
    print("=== introspection_demo ===")

    # Introspection is the ability to examine objects at runtime.

    class Product:
        price: float

        def __init__(self, price: float) -> None:
            self.price: float = price

        def apply_discount(self, percent: float) -> None:
            self.price *= (1 - percent)

    product: Product = Product(100.0)

    # dir() lists attributes and methods.
    print("Has attribute 'price':", "price" in dir(product))

    # hasattr checks existence safely.
    print("hasattr(product, 'apply_discount'):", hasattr(product, "apply_discount"))

    # getattr retrieves attribute dynamically.
    method = getattr(product, "apply_discount")
    method(0.1)

    print("New price:", product.price)

    # __dict__ contains instance namespace.
    print("product.__dict__:", product.__dict__)

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    everything_is_object_demo()
    type_and_metaclass_demo()
    identity_vs_equality_demo()
    mutability_demo()
    introspection_demo()
