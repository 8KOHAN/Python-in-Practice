"""
Attribute resolution order in Python.

This file demonstrates:
- How attribute lookup actually works
- Instance namespace vs class namespace
- Method Resolution Order (MRO)
- Multiple inheritance linearization
- How attribute shadowing happens
- How to inspect MRO
"""
from __future__ import annotations


# ----------------------------------------
# 1) INSTANCE NAMESPACE VS CLASS NAMESPACE
# ----------------------------------------

def instance_vs_class_namespace_demo() -> None:
    print("=== instance_vs_class_namespace_demo ===")

    # Attribute lookup always starts from the instance.
    # Only if the attribute is not found in the instance namespace,
    # Python continues searching in the class.

    class User:
        role: str = "admin"  # class attribute

        def __init__(self, name: str) -> None:
            self.name: str = name  # instance attribute

    user: User = User("Alice")

    # Instance has its own namespace.
    print("user.__dict__:", user.__dict__)

    # Class has its own namespace.
    print("User.__dict__ contains 'role':", "role" in User.__dict__)

    # 'name' is found directly in instance.
    print("user.name:", user.name)

    # 'role' is not in instance namespace,
    # so Python searches in the class.
    print("user.role:", user.role)

    print()


# ----------------------------------------
# 2) ATTRIBUTE SHADOWING
# ----------------------------------------

def attribute_shadowing_demo() -> None:
    print("=== attribute_shadowing_demo ===")

    # Shadowing happens when an instance attribute
    # has the same name as a class attribute.

    class Config:
        timeout: int = 30

    config: Config = Config()

    print("Before shadowing:")
    print("config.timeout:", config.timeout)

    # This creates a new attribute in instance namespace.
    config.timeout = 10

    print("After shadowing:")
    print("config.timeout:", config.timeout)

    # The class attribute remains unchanged.
    print("Config.timeout:", Config.timeout)

    # The instance now has its own 'timeout'.
    print("config.__dict__:", config.__dict__)

    print()


# ----------------------------------------
# 3) BASIC LOOKUP ALGORITHM
# ----------------------------------------

def lookup_algorithm_demo() -> None:
    print("=== lookup_algorithm_demo ===")

    # Simplified attribute lookup order for obj.attr:
    #
    # 1) Check obj.__dict__
    # 2) Check obj.__class__.__dict__
    # 3) Follow MRO chain of base classes
    # 4) If not found -> AttributeError
    #
    # This is a simplified explanation.
    # Descriptors introduce additional rules, but are not covered here.

    class Base:
        base_attr: str = "from Base"

    class Child(Base):
        pass

    child: Child = Child()

    print("child.base_attr:", child.base_attr)

    print()


# ----------------------------------------
# 4) METHOD RESOLUTION ORDER (MRO)
# ----------------------------------------

def mro_basic_demo() -> None:
    print("=== mro_basic_demo ===")

    # MRO defines the order in which base classes are searched.
    # Python uses C3 linearization algorithm.
    #
    # The result is stored in __mro__ and available via .mro().

    class A:
        value: str = "A"

    class B(A):
        pass

    class C(B):
        pass

    print("C.__mro__:", C.__mro__)
    print("C.mro():", C.mro())

    print()


# ----------------------------------------
# 5) MULTIPLE INHERITANCE AND LINEARIZATION
# ----------------------------------------

def multiple_inheritance_mro_demo() -> None:
    print("=== multiple_inheritance_mro_demo ===")

    # Multiple inheritance complicates lookup order.
    # Python guarantees:
    # - No class appears twice
    # - Local precedence order is preserved
    # - The order is monotonic

    class A:
        value: str = "A"

    class B(A):
        value: str = "B"

    class C(A):
        value: str = "C"

    class D(B, C):
        pass

    # The order in which base classes are listed matters.
    print("D.__mro__:", D.__mro__)

    d: D = D()

    # Attribute 'value' will be taken from the first class in MRO
    # where it is found.
    print("d.value:", d.value)

    print()


# ----------------------------------------
# 6) HOW PYTHON ACTUALLY CALLS ATTRIBUTE ACCESS
# ----------------------------------------

def getattr_mechanism_demo() -> None:
    print("=== getattr_mechanism_demo ===")

    # Attribute access:
    # obj.attr
    #
    # Is internally translated into:
    # obj.__getattribute__("attr")
    #
    # If that fails, __getattr__ may be called as a fallback.

    class Demo:
        def __init__(self) -> None:
            self.value: int = 100

        def __getattr__(self, name: str) -> str:
            # Called only if normal lookup fails.
            return f"{name} not found"

    demo: Demo = Demo()

    print("demo.value:", demo.value)
    print("demo.missing:", demo.missing)

    print()


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    instance_vs_class_namespace_demo()
    attribute_shadowing_demo()
    lookup_algorithm_demo()
    mro_basic_demo()
    multiple_inheritance_mro_demo()
    getattr_mechanism_demo()
