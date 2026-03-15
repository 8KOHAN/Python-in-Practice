"""
Designing interfaces with Abstract Base Classes.

This file focuses on how abstract classes are used to define
behavioral contracts between parts of a system.
"""

from abc import ABC, abstractmethod


# ----------------------------------------
# 1) WHAT IS AN INTERFACE IN PYTHON
# ----------------------------------------

# Python does not have a dedicated "interface" keyword like Java or C#.
#
# Instead, interfaces are typically expressed using:
#
# - Abstract Base Classes (ABC)
# - Protocols
#
# In practice an interface means:
#
# A class that defines *what operations must exist*,
# without specifying how they are implemented.
#
# Good interfaces describe behavior, not structure.


# ----------------------------------------
# 2) SIMPLE INTERFACE DESIGN
# ----------------------------------------

class Logger(ABC):

    # This abstract class defines the minimal behavior
    # expected from any logging implementation.

    @abstractmethod
    def log(self, message: str) -> None:
        pass


class ConsoleLogger(Logger):

    # Concrete implementation of the interface.

    def log(self, message: str) -> None:
        print("[console]", message)


class FileLogger(Logger):

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def log(self, message: str) -> None:
        with open(self.filename, "a") as f:
            f.write(message + "\n")


def simple_interface_demo() -> None:
    print("=== simple_interface_demo ===")

    logger: Logger = ConsoleLogger()

    # Code depends on the interface, not the concrete class.

    logger.log("Application started")

    print()


# ----------------------------------------
# 3) DEPENDING ON ABSTRACTIONS
# ----------------------------------------

# One of the core principles of good architecture:
#
# High-level modules should not depend on concrete classes.
# They should depend on abstractions.
#
# This idea is often called the Dependency Inversion Principle.
#
# Instead of hardcoding a concrete logger,
# we accept any object that follows the Logger interface.


def process_data(logger: Logger) -> None:
    logger.log("Processing data...")


def dependency_on_interface_demo() -> None:
    print("=== dependency_on_interface_demo ===")

    logger: Logger = ConsoleLogger()

    process_data(logger)

    print()


# ----------------------------------------
# 4) BAD INTERFACE DESIGN
# ----------------------------------------

# A common mistake is creating interfaces that expose
# too many implementation details.
#
# For example:
#
# - too many methods
# - unrelated responsibilities
# - forcing subclasses to implement unnecessary behavior
#
# Large interfaces are difficult to maintain
# and difficult to implement correctly.
#
# A good rule:
#
# Interfaces should be *small and focused*.


# ----------------------------------------
# 5) MULTIPLE IMPLEMENTATIONS
# ----------------------------------------

class NetworkLogger(Logger):

    def log(self, message: str) -> None:
        # In real systems this might send data
        # to a remote logging service.
        print("[network]", message)


def multiple_implementations_demo() -> None:
    print("=== multiple_implementations_demo ===")

    loggers: list[Logger] = [
        ConsoleLogger(),
        NetworkLogger(),
    ]

    for logger in loggers:
        logger.log("Interface-based logging")

    print()


# ----------------------------------------
# 6) DESIGN OBSERVATIONS
# ----------------------------------------

# Interfaces should describe *capabilities*.
#
# Examples of good interface ideas:
#
# - Logger
# - Storage
# - Serializer
# - AuthenticationProvider
#
# Interfaces should not represent concrete things like:
#
# - DatabaseConnectionMySQL
# - FileReaderImplementation
#
# Those are implementations, not abstractions.


# ----------------------------------------
# 7) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    simple_interface_demo()
    dependency_on_interface_demo()
    multiple_implementations_demo()
