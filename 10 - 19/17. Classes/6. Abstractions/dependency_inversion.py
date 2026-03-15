"""
Demonstration of the Dependency Inversion Principle using abstractions.

This file shows why high-level modules should depend on abstractions
instead of concrete implementations.
"""

from abc import ABC, abstractmethod


# ----------------------------------------
# 1) WHAT IS DEPENDENCY INVERSION
# ----------------------------------------

# The Dependency Inversion Principle (DIP) is one of the SOLID principles.
#
# It states:
#
# - High-level modules should not depend on low-level modules
# - Both should depend on abstractions
#
# and
#
# - Abstractions should not depend on details
# - Details should depend on abstractions
#
# In simpler terms:
#
# Application logic should not care about specific implementations.
#
# Instead of depending on concrete classes,
# code should depend on interfaces or abstract base classes.


# ----------------------------------------
# 2) A SIMPLE ABSTRACTION
# ----------------------------------------

class Storage(ABC):

    # This interface describes a simple storage mechanism.

    @abstractmethod
    def save(self, data: str) -> None:
        pass


class FileStorage(Storage):

    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def save(self, data: str) -> None:
        with open(self.filename, "a") as f:
            f.write(data + "\n")
        print("from save in class [FileStorage]")


class MemoryStorage(Storage):

    def __init__(self) -> None:
        self._data: list[str] = []

    def save(self, data: str) -> None:
        self._data.append(data)
        print("from save in class [MemoryStorage]")


# ----------------------------------------
# 3) HIGH-LEVEL MODULE
# ----------------------------------------

# The high-level component does not depend on FileStorage
# or MemoryStorage directly.
#
# Instead it depends on the Storage abstraction.


class DataProcessor:

    def __init__(self, storage: Storage) -> None:
        self.storage: Storage = storage

    def process(self, value: str) -> None:
        # Some business logic

        processed: str = value.upper()
        self.storage.save(processed)

        print("from process in class [DataProcessor]")


def dependency_injection_demo() -> None:
    print("=== dependency_injection_demo ===")

    storage: Storage = MemoryStorage()

    processor: DataProcessor = DataProcessor(storage)
    processor.process("hello")

    print()


# ----------------------------------------
# 4) SWAPPING IMPLEMENTATIONS
# ----------------------------------------

# Because the system depends on an abstraction,
# implementations can be swapped easily.


def swapping_implementations_demo() -> None:
    print("=== swapping_implementations_demo ===")

    memory_storage = MemoryStorage()
    processor1 = DataProcessor(memory_storage)

    processor1.process("memory example")

    print(str("="*50))

    file_storage = FileStorage("data.txt")
    processor2 = DataProcessor(file_storage)

    processor2.process("file example")

    print()


# ----------------------------------------
# 5) WHY THIS MATTERS
# ----------------------------------------

# Systems designed around abstractions gain several advantages:
#
# - easier testing
# - easier extension
# - lower coupling
# - more flexible architecture
#
# For example, tests can use an in-memory storage
# instead of writing to disk.


# ----------------------------------------
# 6) TESTING WITH FAKE IMPLEMENTATIONS
# ----------------------------------------

class FakeStorage(Storage):

    # This class simulates storage for testing purposes.

    def __init__(self) -> None:
        self.saved: list[str] = []

    def save(self, data: str) -> None:
        self.saved.append(data)


def testing_demo() -> None:
    print("=== testing_demo ===")

    fake_storage = FakeStorage()

    processor = DataProcessor(fake_storage)

    processor.process("test value")

    print("Saved values:", fake_storage.saved)
    print()


# ----------------------------------------
# 7) DESIGN OBSERVATIONS
# ----------------------------------------

# Dependency inversion is not about adding abstract classes everywhere.
#
# It is useful when:
#
# - systems grow large
# - components evolve independently
# - multiple implementations exist
#
# Overusing abstractions can also create unnecessary complexity.
#
# Good architecture balances flexibility and simplicity.


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    dependency_injection_demo()
    swapping_implementations_demo()
    testing_demo()
