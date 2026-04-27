"""
Demonstrates how class decorators work, how they modify classes,
and how they differ from inheritance and metaclasses.
"""

from __future__ import annotations

# ----------------------------------------
# 1) BASIC CLASS DECORATOR
# ----------------------------------------

def basic_class_decorator_demo() -> None:
    print("=== basic_class_decorator_demo ===")

    # A class decorator is just a function that receives a class
    # and returns a class (or any callable object used instead of it)

    def simple_decorator(cls: type) -> type:
        print(f"Decorating class: {cls.__name__}")

        # We can modify the class directly
        cls.added_attr = "injected value"

        return cls

    @simple_decorator
    class A:
        pass

    a = A()

    print(f"a.added_attr: {a.added_attr}")

    print()


# ----------------------------------------
# 2) MODIFYING METHODS
# ----------------------------------------

def method_modification_demo() -> None:
    print("=== method_modification_demo ===")

    # A decorator can wrap or replace methods

    def method_logger(cls: type) -> type:
        original_method = cls.process

        def new_method(self) -> None:
            print("Before process")
            original_method(self)
            print("After process")

        cls.process = new_method
        return cls

    @method_logger
    class Service:
        def process(self) -> None:
            print("Processing...")

    s = Service()
    s.process()

    print()


# ----------------------------------------
# 3) RETURNING A NEW CLASS
# ----------------------------------------

def returning_new_class_demo() -> None:
    print("=== returning_new_class_demo ===")

    # A decorator can return a completely new class

    def replace_with_wrapper(cls: type) -> type:
        class Wrapper(cls):  # inheritance used internally
            def extra(self) -> None:
                print("Extra method")

        return Wrapper

    @replace_with_wrapper
    class A:
        def hello(self) -> None:
            print("Hello")

    a = A()

    a.hello()
    a.extra()

    print(f"type(a): {type(a)}")

    print()


# ----------------------------------------
# 4) PARAMETRIZED CLASS DECORATOR
# ----------------------------------------

def parametrized_decorator_demo() -> None:
    print("=== parametrized_decorator_demo ===")

    # Same idea as function decorators:
    # outer function -> configuration
    # inner function -> actual decorator

    def add_tag(tag: str):
        def decorator(cls: type) -> type:
            cls.tag = tag
            return cls
        return decorator

    @add_tag("service")
    class Service:
        pass

    s = Service()
    print(f"s.tag: {s.tag}")

    print()


# ----------------------------------------
# 5) VALIDATION / CONTRACT ENFORCEMENT
# ----------------------------------------

def validation_decorator_demo() -> None:
    print("=== validation_decorator_demo ===")

    # Class decorators are often used to enforce structure

    def require_method(method_name: str):
        def decorator(cls: type) -> type:
            if not hasattr(cls, method_name):
                raise TypeError(
                    f"{cls.__name__} must define method '{method_name}'"
                )
            return cls
        return decorator

    @require_method("run")
    class Worker:
        def run(self) -> None:
            print("Running")

    w = Worker()
    w.run()

    print()


# ----------------------------------------
# 6) ADDING __repr__
# ----------------------------------------

def add_repr_demo() -> None:
    print("=== add_repr_demo ===")

    # Common real-world use:
    # auto-generating __repr__ for debugging

    def auto_repr(cls: type) -> type:
        def __repr__(self) -> str:
            attrs = ", ".join(
                f"{k}={v!r}" for k, v in self.__dict__.items()
            )
            return f"{cls.__name__}({attrs})"

        cls.__repr__ = __repr__
        return cls

    @auto_repr
    class Point:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    p = Point(1, 2)
    print(p)

    print()


# ----------------------------------------
# 7) WHEN NOT TO USE CLASS DECORATORS
# ----------------------------------------
#
# Class decorators are NOT a universal tool and should not be used
# as a replacement for proper architecture.
#
# Avoid class decorators when:
#
# 1) Logic becomes complex
# If the decorator starts:
# - modifying multiple methods
# - depending on internal class structure
# - introducing branching logic
# it becomes hard to understand and maintain.
# In such cases, prefer composition or metaclasses.
#
# 2) Behavior depends on inheritance hierarchy
# Decorators are applied AFTER class creation and do not participate
# in inheritance mechanics.
# If behavior depends on parent classes or MRO, decorators are the wrong tool.
#
# 3) You need predictable structure
# Decorators can:
# - inject attributes
# - replace methods
# - return a completely different class
# This breaks expectations and makes code harder to reason about.
#
# 4) Debugging becomes unclear
# When reading code:
#
# @decorator
# class A:
#     ...
#
# it is not obvious what A actually is after decoration.
# This increases cognitive load and complicates debugging.
#
# When class decorators ARE appropriate:
#
# - small, isolated transformations
# - validation (enforcing required methods/attributes)
# - adding simple, predictable behavior
# - lightweight instrumentation (logging, tagging)
#
# Guideline:
# Use class decorators for LOCAL transformations,
# not for GLOBAL architecture decisions.


# ----------------------------------------
# 8) THEORETICAL NOTES
# ----------------------------------------
#
# Class decorator:
# - receives a class
# - returns a class (or compatible object)
#
# Execution order:
# 1) class body executes
# 2) class object is created
# 3) decorator is applied
#
# Equivalent transformation:
#
# @decorator
# class A:
#     ...
#
# becomes:
#
# A = decorator(A)
#
# This means:
# - you work with a fully constructed class
# - you can modify or replace it
#
# Non-guarantees:
# - decorator may return a completely different type
# - class identity may change
# - debugging may become harder


# ----------------------------------------
# 9) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_class_decorator_demo()
    method_modification_demo()
    returning_new_class_demo()
    parametrized_decorator_demo()
    validation_decorator_demo()
    add_repr_demo()
