"""
Explains attributes, methods, and the real attribute lookup algorithm:
including descriptor protocol and shadowing behavior.
"""

from __future__ import annotations


# ----------------------------------------
# 1) REAL ATTRIBUTE LOOKUP ORDER (WITH DESCRIPTORS)
# ----------------------------------------

def attribute_lookup_with_descriptors_demo() -> None:
    print("=== attribute_lookup_with_descriptors_demo ===")

    # Real attribute resolution order in Python:
    #
    # Given obj.attr:
    #
    # 1) Look in type(obj).__dict__ for a DATA descriptor.
    #    If found -> call descriptor.__get__ and return.
    #
    # 2) Look in obj.__dict__.
    #    If found -> return value.
    #
    # 3) Look in type(obj).__dict__ for NON-DATA descriptor or plain attribute.
    #    If descriptor -> call __get__.
    #    Otherwise return attribute.
    #
    # 4) Continue lookup via MRO.
    #
    # Implemented inside object.__getattribute__.

    class DataDescriptor:
        def __get__(self, instance: object | None, owner: type, /) -> str:
            if instance is None:
                return "data descriptor accessed via class"
            return "data descriptor value"

        def __set__(self, instance: object, value: str, /) -> None:
            # Presence of __set__ makes this a DATA descriptor
            pass

    class NonDataDescriptor:
        def __get__(self, instance: object | None, owner: type, /) -> str:
            if instance is None:
                return "non-data descriptor accessed via class"
            return "non-data descriptor value"

    class Example:
        data = DataDescriptor()
        non_data = NonDataDescriptor()

    obj: Example = Example()

    # Attempt to shadow both descriptors
    obj.data = "instance value"
    obj.non_data = "instance value"

    # DATA descriptor wins over instance attribute
    print(f"obj.data: {obj.data}")

    # Instance attribute wins over NON-DATA descriptor
    print(f"obj.non_data: {obj.non_data}")

    # Access via class (instance is None)
    print(f"Example.data: {Example.data}")
    print(f"Example.non_data: {Example.non_data}")

    print()


# ----------------------------------------
# 2) METHODS ARE NON-DATA DESCRIPTORS
# ----------------------------------------

def method_descriptor_demo() -> None:
    print("=== method_descriptor_demo ===")

    class Service:
        def process(self, value: int, /) -> int:
            return value * 2

    # Functions defined inside a class are non-data descriptors.
    # They implement __get__, but not __set__.

    service: Service = Service()

    # Access via class -> raw function
    print(f"Service.process: {Service.process}")

    # Access via instance -> bound method
    print(f"service.process: {service.process}")

    # Non-data descriptors can be shadowed
    service.process = lambda x: 999

    print(f"Shadowed service.process(10): {service.process(10)}")

    print()


# ----------------------------------------
# 3) PROPERTY IS A DATA DESCRIPTOR
# ----------------------------------------

def property_descriptor_demo() -> None:
    print("=== property_descriptor_demo ===")

    class User:
        def __init__(self, name: str, /) -> None:
            self._name: str = name

        @property
        def name(self) -> str:
            return self._name

    user: User = User("Alice")

    # property is a DATA descriptor because it defines __set__
    # even if no setter is explicitly provided.
    # That is why instance assignment does not shadow it.

    print(f"user.name: {user.name}")

    try:
        user.name = "Bob"
    except AttributeError as exc:
        print(f"Assignment raised: {exc}")

    print()


# ----------------------------------------
# 4) ATTRIBUTE SHADOWING RULES SUMMARY (THEORETICAL)
# ----------------------------------------

# Resolution priority in Python attribute lookup:
#
# 1) DATA descriptor
#    - Any descriptor defining __get__ and __set__
#    - Examples: property with setter, framework-defined descriptors
#    - Always takes precedence over instance attributes
#
# 2) Instance attribute
#    - Attributes stored in obj.__dict__
#    - Shadows non-data descriptors but is overridden by data descriptors
#
# 3) NON-DATA descriptor
#    - Any descriptor defining only __get__ (no __set__)
#    - Examples: plain functions/methods in a class
#    - Can be shadowed by instance attributes
#
# 4) Plain class attribute
#    - Any attribute in the class dictionary that is not a descriptor
#    - Lowest priority, accessed only if none of the above exist
#
# Notes:
# - Understanding this order is essential for:
#     * properties
#     * methods (bound vs unbound)
#     * ORMs and frameworks
#     * metaprogramming and custom descriptors
# - Access via the class (Class.attr) vs instance (obj.attr) may differ:
#     * instance is None when accessed via class
#     * bound methods are created only when accessed via instance


# ----------------------------------------
# 5) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    attribute_lookup_with_descriptors_demo()
    method_descriptor_demo()
    property_descriptor_demo()
