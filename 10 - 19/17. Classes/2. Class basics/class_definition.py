"""
Demonstrates what a class definition really is in Python:
its runtime nature, namespace creation, and object instantiation mechanics.
"""

from __future__ import annotations


# ----------------------------------------
# 1) CLASS STATEMENT IS EXECUTABLE CODE
# ----------------------------------------

def class_statement_execution_demo() -> None:
    print("=== class_statement_execution_demo ===")

    # In Python, a class is NOT a compile-time structure.
    # The `class` statement is executed at runtime.
    # It creates a new namespace (a dictionary-like mapping),
    # executes the body inside that namespace,
    # and then constructs a class object.

    class Example:
        x: int = 10

        def method(self) -> int:
            return self.x

    # The class itself is an object.
    print(f"Type of Example: {type(Example)}")

    # A class has its own namespace.
    # __dict__ stores attributes defined in the class body.
    print(f"Example.__dict__ keys: {list(Example.__dict__.keys())}")

    print()


# ----------------------------------------
# 2) CLASS OBJECT VS INSTANCE OBJECT
# ----------------------------------------

def class_vs_instance_demo() -> None:
    print("=== class_vs_instance_demo ===")

    class User:
        species: str = "Homo sapiens"

        def __init__(self, name: str) -> None:
            # Instance attribute
            self.name: str = name

    # The class itself is an object.
    print(f"User is instance of: {type(User)}")

    user: User = User("Alice")

    # The instance is a separate object.
    print(f"user is instance of: {type(user)}")

    # Instance has its own namespace.
    print(f"user.__dict__: {user.__dict__}")

    # Class attributes live on the class.
    print(f"User.species: {User.species}")

    print()


# ----------------------------------------
# 3) CLASS NAMESPACE CREATION
# ----------------------------------------

def class_namespace_demo() -> None:
    print("=== class_namespace_demo ===")

    # When Python executes a class statement:
    # 1) It creates a temporary namespace (mapping).
    # 2) Executes the body inside it.
    # 3) Wraps that namespace into a class object.

    class Product:
        category: str = "general"

        def get_category(self) -> str:
            return self.category

    # Class attributes are stored in __dict__
    print(f"'category' in Product.__dict__: {'category' in Product.__dict__}")

    # Methods are just functions stored in class namespace.
    print(f"'get_category' in Product.__dict__: {'get_category' in Product.__dict__}")

    # A method is a function until accessed via instance.
    print(f"Raw method object: {Product.__dict__['get_category']}")

    print()


# ----------------------------------------
# 4) METHODS ARE DESCRIPTORS
# ----------------------------------------

def method_binding_demo() -> None:
    print("=== method_binding_demo ===")

    class Logger:
        def log(self, message: str) -> None:
            print(f"LOG: {message}")

    # Accessing through class gives function object.
    print(f"Logger.log: {Logger.log}")

    logger: Logger = Logger()

    # Accessing through instance triggers descriptor protocol.
    # The function becomes a bound method.
    print(f"logger.log: {logger.log}")

    # Bound method already has `self` attached.
    logger.log("Hello")

    print()


# ----------------------------------------
# 5) CLASS OBJECT IS CALLABLE
# ----------------------------------------

def class_is_callable_demo() -> None:
    print("=== class_is_callable_demo ===")

    class Point:
        def __init__(self, x: float, y: float) -> None:
            self.x: float = x
            self.y: float = y

    # A class is callable because it implements __call__
    # via its metaclass (usually `type`).

    p: Point = Point(1.0, 2.0)

    print(f"Created instance: {p}")
    print(f"Point.__call__ exists: {'__call__' in dir(Point)}")
    print(f"hasattr(Point, '__call__') exists: {hasattr(Point, "__call__")}")

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    class_statement_execution_demo()
    class_vs_instance_demo()
    class_namespace_demo()
    method_binding_demo()
    class_is_callable_demo()
