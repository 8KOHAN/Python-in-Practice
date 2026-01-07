"""
Demonstration of I/O related exceptions:
how file operations fail, what different I/O errors mean,
and how to handle them correctly.
"""

from __future__ import annotations
from pathlib import Path


# ----------------------------------------
# 1) FileNotFoundError
# ----------------------------------------

def file_not_found_demo() -> None:
    print("=== file_not_found_demo ===")

    # FileNotFoundError is raised when attempting to open
    # a file that does not exist.
    #
    # This is a very common and expected error condition
    # when working with external resources.

    path: Path = Path("non_existent_file.txt")

    try:
        with path.open("r") as file:
            file.read()
    except FileNotFoundError as exc:
        print(f"FileNotFoundError caught: {exc}")

    print()


# ----------------------------------------
# 2) PermissionError
# ----------------------------------------

def permission_error_demo() -> None:
    print("=== permission_error_demo ===")

    # PermissionError is raised when the file exists,
    # but the current process does not have enough rights
    # to perform the requested operation.
    #
    # This depends on the operating system and environment,
    # so this demo focuses on the exception type itself.

    path: Path = Path("/root/forbidden_file.txt")

    try:
        with path.open("r") as file:
            file.read()
    except PermissionError as exc:
        print(f"PermissionError caught: {exc}")
    except FileNotFoundError:
        # On some systems the file may not exist at all.
        print("File does not exist (PermissionError not triggered)")

    print()


# ----------------------------------------
# 3) IsADirectoryError
# ----------------------------------------

def is_a_directory_error_demo() -> None:
    print("=== is_a_directory_error_demo ===")

    # IsADirectoryError is raised when trying to treat
    # a directory as a regular file.

    path: Path = Path(".")

    try:
        with path.open("r") as file:
            file.read()
    except IsADirectoryError as exc:
        print(f"IsADirectoryError caught: {exc}")

    print()


# ----------------------------------------
# 4) GENERIC OSError AND WHY IT EXISTS
# ----------------------------------------

def os_error_hierarchy_demo() -> None:
    print("=== os_error_hierarchy_demo ===")

    # Most I/O-related exceptions inherit from OSError.
    #
    # Examples:
    # - FileNotFoundError
    # - PermissionError
    # - IsADirectoryError
    #
    # Catching OSError is sometimes reasonable,
    # but only when you genuinely want to handle
    # multiple I/O failure modes the same way.

    path: Path = Path("another_missing_file.txt")

    try:
        with path.open("r") as file:
            file.read()
    except OSError as exc:
        print(f"OSError caught: {type(exc).__name__}: {exc}")

    print()


# ----------------------------------------
# 5) IO ERRORS VS PRE-CHECKS
# ----------------------------------------

def io_error_vs_precheck_demo() -> None:
    print("=== io_error_vs_precheck_demo ===")

    # A common pattern is to check for file existence
    # before opening it.
    #
    # This can introduce race conditions:
    # the file may disappear or change between the check
    # and the actual open() call.
    #
    # Relying on exceptions avoids this class of bugs.

    path: Path = Path("yet_another_missing_file.txt")

    try:
        with path.open("r") as file:
            file.read()
    except FileNotFoundError:
        print("File does not exist (handled via exception)")

    print()


# ----------------------------------------
# 6) CONTEXT MANAGERS AND RESOURCE SAFETY
# ----------------------------------------
#
# Context managers (the `with` statement) are not about convenience.
# They are about correctness and guarantees.
#
# The key guarantee:
# - Resource cleanup happens no matter how the block is exited:
#   * normal execution
#   * raised exception
#   * early return
#
# For file objects, this means:
# - the file descriptor is always closed
# - even if an exception is raised while reading or writing
#
# Why this matters:
# - leaking file descriptors is a real bug
# - on some systems, it leads to "too many open files"
# - on Windows, it may prevent file deletion or modification
#
# Important subtlety:
# - If the file fails to open, no resource is acquired
# - In that case, there is nothing to clean up
# - This is why examples that only raise FileNotFoundError
#   do NOT demonstrate the value of context managers
#
# The real benefit of `with` appears when:
# - the resource is successfully acquired
# - an exception happens later inside the block
#
# This will be demonstrated in a later section
# together with custom context managers.



# ----------------------------------------
# 7) I/O ERRORS — SUMMARY
# ----------------------------------------

def io_errors_summary_demo() -> None:
    print("=== io_errors_summary_demo ===")

    # Key ideas:
    #
    # - I/O errors are expected, not exceptional in practice
    # - They depend on the environment and external state
    # - Most of them inherit from OSError
    # - Correct handling focuses on:
    #   * clarity of intent
    #   * proper resource cleanup
    #   * minimal assumptions about the filesystem

    examples: list[tuple[str, BaseException]] = [
        ("open('missing.txt')", FileNotFoundError()),
        ("open('/root/file')", PermissionError()),
        ("open('.')", IsADirectoryError()),
    ]

    for expression, error in examples:
        print(f"{expression} -> {type(error).__name__}")

    print()


# ----------------------------------------
# 8) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    file_not_found_demo()
    permission_error_demo()
    is_a_directory_error_demo()
    os_error_hierarchy_demo()
    io_error_vs_precheck_demo()
    io_errors_summary_demo()
