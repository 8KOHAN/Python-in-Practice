"""
Fundamental concepts of class inheritance in Python.

This file demonstrates:
- how inheritance works
- how attributes and methods are inherited
- method overriding
- using super()
- how Python resolves attributes in a simple inheritance chain
"""

# ----------------------------------------
# 1) BASIC INHERITANCE
# ----------------------------------------

# Inheritance allows a class to reuse behavior from another class.
# The class being inherited from is usually called:
#
# base class
# parent class
# superclass
#
# The class that inherits from it is called:
#
# child class
# subclass
#
# In Python, inheritance is declared directly in the class definition.


class Animal:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def speak(self) -> None:
        print("Some generic animal sound")

    def describe(self) -> None:
        print(f"This animal is named {self.name}")


class Dog(Animal):
    pass


def basic_inheritance_demo() -> None:
    print("=== basic_inheritance_demo ===")

    # Dog does not define its own __init__
    # so Python uses Animal.__init__
    dog = Dog("Rex")

    dog.describe()
    dog.speak()

    print()


# ----------------------------------------
# 2) METHOD OVERRIDING
# ----------------------------------------

# A subclass can redefine a method from its parent class.
# This is called method overriding.
#
# The child class provides its own implementation,
# replacing the behavior defined in the parent.


class Cat(Animal):
    def speak(self) -> None:
        print("Meow")


def method_overriding_demo() -> None:
    print("=== method_overriding_demo ===")

    cat = Cat("Misty")

    # Cat overrides the speak method
    cat.speak()

    # describe is still inherited
    cat.describe()

    print()


# ----------------------------------------
# 3) EXTENDING BEHAVIOR WITH super()
# ----------------------------------------

# Overriding does not always mean replacing behavior completely.
# Often we want to extend the parent's implementation.
#
# The built-in function super() provides access to the parent class.


class Bird(Animal):
    def __init__(self, name: str, can_fly: bool) -> None:
        # Instead of manually assigning self.name,
        # we delegate initialization to the parent class.
        super().__init__(name)

        self.can_fly = can_fly

    def describe(self) -> None:
        # Call the parent method first
        super().describe()

        if self.can_fly:
            print("This bird can fly")
        else:
            print("This bird cannot fly")


def super_usage_demo() -> None:
    print("=== super_usage_demo ===")

    parrot = Bird("Polly", True)
    penguin = Bird("Pingu", False)

    parrot.describe()
    print()

    penguin.describe()

    print()


# ----------------------------------------
# 4) ATTRIBUTE INHERITANCE
# ----------------------------------------

# Attributes defined in the parent class are inherited by the child.
# They become part of the child's instance state.
#
# The child class can:
#
# - use them directly
# - modify them
# - extend them with new attributes


class Vehicle:
    def __init__(self, brand: str) -> None:
        self.brand = brand

    def show_brand(self) -> None:
        print(f"Brand: {self.brand}")


class Car(Vehicle):
    def __init__(self, brand: str, model: str) -> None:
        super().__init__(brand)
        self.model = model

    def show_model(self) -> None:
        print(f"Model: {self.model}")


def attribute_inheritance_demo() -> None:
    print("=== attribute_inheritance_demo ===")

    car = Car("Toyota", "Corolla")

    car.show_brand()
    car.show_model()

    print()


# ----------------------------------------
# 5) SIMPLE INHERITANCE CHAIN
# ----------------------------------------

# Inheritance can form chains.
#
# Example:
#
#   LivingBeing
#       ↓
#     Animal
#       ↓
#       Dog
#
# Each class inherits behavior from all classes above it.


class LivingBeing:
    def exist(self) -> None:
        print("This being exists")


class Mammal(LivingBeing):
    def warm_blooded(self) -> None:
        print("Mammals are warm-blooded")


class Wolf(Mammal):
    def howl(self) -> None:
        print("A wolf howls")


def inheritance_chain_demo() -> None:
    print("=== inheritance_chain_demo ===")

    wolf = Wolf()

    wolf.exist()
    wolf.warm_blooded()
    wolf.howl()

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    basic_inheritance_demo()
    method_overriding_demo()
    super_usage_demo()
    attribute_inheritance_demo()
    inheritance_chain_demo()
