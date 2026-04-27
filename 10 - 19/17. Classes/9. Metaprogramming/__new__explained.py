"""
Demonstrates how __new__ works, how it differs from __init__,
and when it should actually be used in real code.
"""

from __future__ import annotations


# ----------------------------------------
# 1) BASIC OBJECT CREATION FLOW
# ----------------------------------------

def basic_creation_flow_demo() -> None:
    print("=== basic_creation_flow_demo ===")

    # In Python, object creation happens in TWO steps:
    #
    # 1) __new__  -> creates the object (memory allocation)
    # 2) __init__ -> initializes the object (sets attributes)
    #
    # __new__ returns the instance
    # __init__ receives that instance as 'self'

    class Simple:
        def __new__(cls) -> Simple:
            print("Calling __new__")
            instance = super().__new__(cls)
            return instance

        def __init__(self) -> None:
            print("Calling __init__")

    obj = Simple()

    # Expected output:
    # Calling __new__
    # Calling __init__

    print()


# ----------------------------------------
# 2) __new__ CONTROLS INSTANCE CREATION
# ----------------------------------------

def new_controls_creation_demo() -> None:
    print("=== new_controls_creation_demo ===")

    # __new__ can completely control WHAT instance is returned
    # It does NOT have to return an instance of the class

    class A:
        def __new__(cls) -> int:
            print("Returning int instead of A")
            return 18

        def __init__(self) -> None:
            # This will NEVER be called
            print("This will not execute")

    obj = A()

    print(f"type(obj): {type(obj)}")
    print(f"value: {obj}")

    # Important:
    # If __new__ does NOT return an instance of cls,
    # __init__ will NOT be executed.

    print()


# ----------------------------------------
# 3) IMMUTABLE TYPES USE __new__
# ----------------------------------------

def immutable_objects_demo() -> None:
    print("=== immutable_objects_demo ===")

    # __new__ is REQUIRED when working with immutable types
    # because their value must be set during creation

    class MyInt(int):
        def __new__(cls, value: int) -> MyInt:
            print("Modifying value before creation")
            return super().__new__(cls, value * 2)

    x = MyInt(10)

    print(f"x: {x}")  # 20

    # __init__ would be too late here,
    # because int is immutable

    print()


# ----------------------------------------
# 4) SINGLETON VIA __new__
# ----------------------------------------

def singleton_demo() -> None:
    print("=== singleton_demo ===")

    # __new__ is often used to control instance uniqueness

    class Singleton:
        _instance: Singleton | None = None

        def __new__(cls) -> Singleton:
            if cls._instance is None:
                print("Creating new instance")
                cls._instance = super().__new__(cls)
            else:
                print("Reusing existing instance")

            return cls._instance

    a = Singleton()
    b = Singleton()

    print(f"a is b: {a is b}")

    print()


# ----------------------------------------
# 5) __new__ VS __init__
# ----------------------------------------

def new_vs_init_demo() -> None:
    print("=== new_vs_init_demo ===")

    # Key differences:
    #
    # __new__:
    # - static method (implicitly)
    # - receives class (cls)
    # - MUST return an instance
    #
    # __init__:
    # - instance method
    # - receives instance (self)
    # - MUST return None

    class Example:
        def __new__(cls) -> Example:
            print(f"__new__: cls = {cls}")
            return super().__new__(cls)

        def __init__(self) -> None:
            print(f"__init__: self = {self}")

    Example()

    print()


# ----------------------------------------
# 6) WHEN NOT TO USE __new__
# ----------------------------------------

def when_not_to_use_new_demo() -> None:
    print("=== when_not_to_use_new_demo ===")

    # __new__ should NOT be used for:
    #
    # - normal attribute initialization
    # - validation logic (usually __init__ or property)
    # - business logic
    #
    # Using __new__ unnecessarily makes code harder to read
    # and breaks expectations of other developers

    class BadExample:
        def __new__(cls) -> BadExample:
            instance = super().__new__(cls)
            instance.value = 10  # WRONG PLACE
            return instance

    obj = BadExample()
    print(f"value: {obj.value}")

    # This works, but violates expectations.
    # Initialization belongs to __init__.

    print()


# ----------------------------------------
# 7) THEORETICAL NOTES
# ----------------------------------------

# __new__ is rarely needed in everyday code.
#
# It becomes relevant when:
# - working with immutable types (int, str, tuple)
# - implementing object caching / pooling
# - controlling instance creation (Singleton-like logic)
# - building frameworks or low-level libraries
#
# Non-guarantees:
# - __init__ is NOT guaranteed to run
# - returned object may NOT be instance of the class
#
# This makes __new__ a powerful but dangerous tool.


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_creation_flow_demo()
    new_controls_creation_demo()
    immutable_objects_demo()
    singleton_demo()
    new_vs_init_demo()
    when_not_to_use_new_demo()
