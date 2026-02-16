"""
Covers best practices for writing __init__ methods:
validation, invariants, minimal responsibility, and common design mistakes.
"""

from __future__ import annotations


# ----------------------------------------
# 1) __init__ SHOULD ESTABLISH INVARIANTS
# ----------------------------------------

def invariants_demo() -> None:
    print("=== invariants_demo ===")

    class User:
        def __init__(self, username: str, age: int, /) -> None:
            # __init__ must leave the object in a valid state.
            # If validation fails, object construction should fail immediately.

            if not username:
                raise ValueError("username must not be empty")

            if age < 0:
                raise ValueError("age must be non-negative")

            self.username: str = username
            self.age: int = age

    user: User = User("alice", 30)
    print(f"user.username: {user.username}")
    print(f"user.age: {user.age}")

    print()


# ----------------------------------------
# 2) DO NOT PERFORM HEAVY LOGIC IN __init__
# ----------------------------------------

def heavy_logic_antipattern_demo() -> None:
    print("=== heavy_logic_antipattern_demo ===")

    class Report:
        def __init__(self, raw_data: list[int], /) -> None:
            # __init__ should not perform expensive computation.
            # It should only store input and establish invariants.

            self._raw_data: list[int] = raw_data

        def compute_statistics(self) -> float:
            # Heavy logic belongs in dedicated methods.
            return sum(self._raw_data) / len(self._raw_data)

    report: Report = Report([1, 2, 3, 4])
    print(f"Average: {report.compute_statistics()}")

    print()


# ----------------------------------------
# 3) AVOID SIDE EFFECTS DURING INITIALIZATION
# ----------------------------------------

def side_effects_demo() -> None:
    print("=== side_effects_demo ===")

    class Logger:
        def __init__(self, file_path: str, /) -> None:
            # Avoid performing irreversible side effects in __init__.
            # Example of bad design:
            #
            # opening files
            # connecting to databases
            # making network requests
            #
            # These actions should be explicit and separated.

            self.file_path: str = file_path

        def open(self) -> None:
            # Explicit side-effect method
            print(f"Opening file at {self.file_path}")

    logger: Logger = Logger("app.log")
    logger.open()

    print()


# ----------------------------------------
# 4) DO NOT LEAK PARTIALLY CONSTRUCTED SELF
# ----------------------------------------

def partially_constructed_self_demo() -> None:
    print("=== partially_constructed_self_demo ===")

    registry: list[Service] = []

    class Service:
        def __init__(self, name: str, /) -> None:
            # Dangerous pattern:
            # registering self before full initialization.

            self.name: str = name

            # Safe only after all attributes are assigned
            registry.append(self)

    service: Service = Service("api")
    print(f"Registered services: {[s.name for s in registry]}")

    print()


# ----------------------------------------
# 5) KEEP __init__ SMALL AND EXPLICIT
# ----------------------------------------

def minimal_init_demo() -> None:
    print("=== minimal_init_demo ===")

    class Config:
        def __init__(
            self,
            host: str,
            port: int,
            debug: bool = False,
            /,
        ) -> None:
            # __init__ should:
            # - validate
            # - assign
            # - establish invariants
            #
            # Nothing more.

            if port <= 0:
                raise ValueError("port must be positive")

            self.host: str = host
            self.port: int = port
            self.debug: bool = debug

    config: Config = Config("localhost", 8080)
    print(f"{config.host}:{config.port} debug={config.debug}")

    print()


# ----------------------------------------
# 6) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    invariants_demo()
    heavy_logic_antipattern_demo()
    side_effects_demo()
    partially_constructed_self_demo()
    minimal_init_demo()
