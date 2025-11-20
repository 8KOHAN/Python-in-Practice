# ----------------------------------------
# Modern variable typing examples (PEP 585, PEP 604, Python 3.10+)
# Comments are in English. This file focuses on variable annotations,
# not on function parameter/return typing (those are covered separately).
# Avoids typing.Optional / typing.Union / typing.List / typing.Dict.
# ----------------------------------------

from typing import Literal, TypedDict, Protocol, Final, Never, Callable, Self, Any, cast

# -----------------------------
# 0) SHORT NOTE
# -----------------------------
# Use Python 3.10+ to get `|` for unions and Python 3.9+ for builtin generics.
# Prefer builtins: list[int], dict[str, int], tuple[int, ...]
# Use typing.* sparingly only when needed (Literal, TypedDict, Protocol, Final, Never, Callable, Self).

# -----------------------------
# 1) BASIC VARIABLE ANNOTATIONS
# -----------------------------
age: int = 25
name: str = "Alice"
price: float = 19.99
is_active: bool = True

# collections - use built-in generics (PEP 585)
tags: list[str] = ["python", "typing"]
counts: dict[str, int] = {"a": 1, "b": 2}
coords: tuple[float, float] = (50.0, 30.0)
scores: list[int] = [10, 20, 30]

# union-like and optional: use X | None
maybe_age: int | None = None   # preferred modern style
id_or_name: int | str = 42     # id can be int or name can be str

# dynamic/no type hint - IDE can't help
raw = None

# -----------------------------
# 2) OLD STYLE FOR COMPARISON (EXAMPLES)
# -----------------------------
# Old style used typing imports - still valid but verbose:
# from typing import List, Dict, Optional, Union
# old_tags: List[str] = ["python"]
# old_counts: Dict[str, int] = {"a": 1}
# old_maybe_age: Optional[int] = None
# old_id_or_name: Union[int, str] = 42

# Problems with old style:
# - verboseness in small modules
# - less idiomatic for modern Python
# - mixing old and new styles reduces consistency

# -----------------------------
# 3) WHY DECLARE VARIABLES' TYPES AT ALL?
# -----------------------------
# - IDE autocompletion and inline docs
# - static analysis (mypy, pyright) catches mistakes early
# - documentation: reading code shows intended shapes
# - helps large teams: you see contract immediately at hover

# Example: without annotation, an IDE cannot warn you about None usage.
maybe_age2 = None  # no hint -> ambiguous
# Later accidental arithmetic will be silent at runtime and uncovered in editor.

# -----------------------------
# 4) LITERAL - fixed allowed values
# -----------------------------
mode: Literal["r", "w", "a"] = "r"     # only these values are allowed (checked by type checker)
# type checkers will warn if you assign an invalid literal:
# mode = "x"  -> flagged by tools

# -----------------------------
# 5) TYPEDDICT - typed dictionaries for structured data
# -----------------------------
class UserDict(TypedDict):
    id: int
    name: str
    email: str
    tags: list[str]

user: UserDict = {"id": 1, "name": "Alice", "email": "a@example.com", "tags": ["py"]}

# Good: TypedDict tells tools what keys exist and their types.
# Bad: plain dict with no annotation loses this contract:
config = {"retries": 3}  # no type info - unclear expected keys/types

# ------------------------------------------------------------
# 6.) Define a Protocol: an interface by structure (not inheritance)
# ------------------------------------------------------------
class SupportsSend(Protocol):
    """Any object with a .send(data: bytes) -> int method matches this protocol."""
    def send(self, data: bytes) -> int: ...

# ------------------------------------------------------------
# Concrete class does NOT need to inherit from Protocol
# It just needs to have the same "shape" (method signature)
# ------------------------------------------------------------
class SocketLike:
    def send(self, data: bytes) -> int:
        print("sending", len(data))
        return len(data)

# ------------------------------------------------------------
# Static typing check: SocketLike matches SupportsSend
# ------------------------------------------------------------
s: SupportsSend = SocketLike()  # accepted: structural match

# ------------------------------------------------------------
# Explanation:
# 1. Protocols allow "duck typing" in a statically-checked way:
#    - If it has the right methods/signatures, it's accepted.
# 2. Unlike ABCs (abstract base classes):
#    - No need for inheritance
#    - Focuses on the object's "shape"
# 3. Useful in large codebases:
#    - You can type-hint a function expecting "anything that can send data"
#      without forcing classes to inherit from a common base class.
# 4. Example usage in functions:
def broadcast(*, sender: SupportsSend, message: bytes) -> None:
    """Any object that implements send() can be used here."""
    sender.send(message)

broadcast(sender=SocketLike(), message=b"Hello")  # works, type-checked

# -----------------------------
# 7) FINAL - constants and intent
# -----------------------------
API_URL: Final = "https://api.example.com"
# Type checkers will warn if reassigned API_URL = "..." later.
# Final communicates intent to humans and tools.

# -----------------------------
# 8) NEVER — indicates code paths that cannot happen
# -----------------------------
# `Never` represents the "empty type": a value that can never exist.
# It is mainly used in two scenarios:
#
# (1) Functions that never return (they either raise an exception or exit)
#     The type checker understands that execution stops after this call.

def fatal(msg: str) -> Never:
    """This function never returns successfully."""
    raise SystemExit(msg)

# Example usage:
# fatal("critical error")
# Code after this will be considered unreachable by type checkers.

# (2) Exhaustive checks (usually with match-case):
#     If all valid variants are handled, the remaining branch is `Never`.
#     Type checkers can detect missing cases in enums or Literal unions.

Status = Literal["ok", "error"]

def handle_status(s: Status) -> None:
    match s:
        case "ok":
            print("Everything is fine.")
        case "error":
            print("Something went wrong.")
        case _ as unreachable:
            ...
            # This branch should be impossible.
            # `unreachable` has type `Never`, so type checkers warn if new
            # cases appear in Status but are not handled above.
            # reveal_type(unreachable)  # type: Never  (static analyzers show this)

# (3) Variables typed as `Never`:
#     Rare, but signals "this variable will never hold a value".
#     If you try assigning to it, type checkers will report an error.

never_var: Never  # This name can never be assigned to.

# never_var = 10   # static error: cannot assign to Never

# -----------------------------
# 9) CALLABLE - variable holding a function signature
# -----------------------------
handler: Callable[[str], None] = lambda s: print("handled:", s)
# Note: we annotate the variable that holds a callable, not the function itself here.

# A more explicit assignment (still variable-only typing):
def greet_user(user: str) -> None:
    print("hello", user)

greet_handler: Callable[[str], None] = greet_user

# -----------------------------
# 10) SELF – PEP 673 (Python 3.11+)
# -----------------------------
# Self is a special typing helper that refers to the *current class*.
# It is extremely useful for:
#   • fluent interfaces (methods returning self)
#   • builder patterns
#   • subclasses: return type automatically adjusts to the subclass
#
# Without Self, older code relied on:
#   - -> "Box": string forward references
#   - -> Box: which breaks inheritance (method returning subclass still typed as Box)
#
# Self fixes all of this.

class Box:
    def __init__(self: Self, value: int) -> None:
        # 'self: Self' means: this is an instance of the current class (or subclass)
        self.value = value

    def set(self: Self, value: int) -> Self:
        # Method returns 'self', so annotate with Self.
        # This ensures fluent method chaining keeps correct types.
        self.value = value
        return self

box: Box = Box(1)
box.set(2).set(3)  # type checker knows this returns a Box

# Example with inheritance: Self works correctly
class SpecialBox(Box):
    def multiply(self: Self, k: int) -> Self:
        self.value *= k
        return self

sb: SpecialBox = SpecialBox(10)
result: SpecialBox = sb.set(5).multiply(3).set(51)
# 'result' is correctly inferred as SpecialBox, not Box.

# -----------------------------
# 11) TYPE NARROWING PATTERNS (how to safely handle unions)
# -----------------------------
value: int | str = "x"

# BAD: using value as int without checking - type checker warns and runtime may fail
# n = value + 1   # unsafe

# GOOD: guard with isinstance/is None checks to narrow type
if isinstance(value, int):
    number: int = value + 1
else:
    number = len(value)  # safe branch for str

maybe_age = None # type: int | None

# BAD: arithmetic without check
# total = maybe_age + 5  # mypy warns

# GOOD: explicit guard
if maybe_age is not None:
    total = maybe_age + 5
else:
    total = 0

# -----------------------------
# 12) CASTING — overriding type checkers intentionally
# -----------------------------

# --------------------------------------------------------
# WHAT cast() DOES
# --------------------------------------------------------
# cast(T, value) tells static analyzers:
#     "treat 'value' as type T — trust me."
#
# IMPORTANT:
#   • cast() performs NO runtime checks
#   • cast() does NOT convert the value
#   • cast() simply returns the same object
#
# It is purely a static typing tool.
# --------------------------------------------------------

# --------------------------------------------------------
# GOOD USE CASE 1:
# You validated the type manually, but the analyzer can't deduce it.
# --------------------------------------------------------
raw: Any = "123"

if isinstance(raw, str):
    safe_str: str = cast(str, raw)  # analyzer trusts this
    # Now IDE knows safe_str is str
    length: int = safe_str.count("3")

# --------------------------------------------------------
# GOOD USE CASE 2:
# Complex data from external sources (JSON, APIs, DB)
# Analyzer cannot know exact structure.
# --------------------------------------------------------
data: dict[str, Any] = {"id": 1, "name": "Alice"}

# We know this field must be str, but type checker sees Any.
name = cast(str, data["name"])

# --------------------------------------------------------
# GOOD USE CASE 3:
# Working with untyped third-party libraries.
# --------------------------------------------------------
# untyped_value: Any = get_from_legacy_library()
# processed_value = cast(int, untyped_value)  # you guarantee it's an int

# --------------------------------------------------------
# BAD PRACTICE 1: using cast instead of real validation
# --------------------------------------------------------
maybe_int: int | None = None

# WRONG: cast hides the problem — runtime may crash
unsafe_value = cast(int, maybe_int)

# RIGHT: validate explicitly
if maybe_int is None:
    safe_value = 0
else:
    safe_value = maybe_int

# --------------------------------------------------------
# BAD PRACTICE 2: using cast to silence IDE warnings
# --------------------------------------------------------
# unknown: Any = load_data()

# WRONG:
# user_id: int = cast(int, unknown)  # you don't know if it's an int

# --------------------------------------------------------
# BAD PRACTICE 3: using cast when normal typing can solve it
# --------------------------------------------------------
# WRONG:
raw_num: Any = 10
num = cast(int, raw_num)

# RIGHT:
raw_num: int = 10   # annotate correctly instead of casting

# --------------------------------------------------------
# SUMMARY:
# Use cast() ONLY when:
#   • You logically ensured the type is correct, AND
#   • The type checker cannot infer the type.
# --------------------------------------------------------

# -----------------------------
# 13) EXAMPLES: WHY TYPING HELPS (IDE hints and safer code)
# -----------------------------
# Example 1: maybe_age warns when used directly
maybe_age = None  # type: int | None
# total = maybe_age + 5  # static checker warns (may be None)

# Example 2: TypedDict helps discover keys
class UserDict(TypedDict):
    id: int
    name: str
    email: str

user: UserDict = {
    "id": 1,
    "name": "Alice",
    "email": "a@example.com"
}
# user["id"] -> IDE knows it's int, user["unknown"] -> IDE warns

# P.S. We create a typed dictionary with a fixed set of keys using TypedDict.

# Example 3: Protocol enables structural typing
class Logger(Protocol):
    def info(self, msg: str) -> None: ...

class ConsoleLogger:
    def info(self, msg: str) -> None:
        print("INFO:", msg)

logger: Logger = ConsoleLogger()
logger.info("works")

# -----------------------------
# 14) BAD PRACTICES (LOTS OF EXAMPLES)
# -----------------------------

# BAD PRACTICE 1: using Any everywhere - defeats static analysis
data: Any = {"x": 1}
# Later code reads/writes without checks - errors become runtime-only

# BAD PRACTICE 2: untyped public module-level variables
config = {"retries": 3}
# Other developers cannot know expected shape from hover; tools can't help.

# BAD PRACTICE 3: mixing styles in one project
# Some files use typing.List, others list[int] -> inconsistency and mental friction.

# BAD PRACTICE 4: sloppy unions without guarding
value2: int | str = "x"
# n = value2 + 1  # mypy warns; runtime error if value2 is str

# BAD PRACTICE 5: using mutable defaults (here shown as a variable example)
# global_default: list[int] = []  # mutable global - can be modified from anywhere

# BAD PRACTICE 6: using a plain dict instead of a TypedDict annotation
raw_user = {"id": 1, "name": "Alice"}  # no TypedDict -> less tooling help

# -----------------------------
# 15) PATTERNS & RECOMMENDATIONS FOR VARIABLES (practical rules)
# -----------------------------
# - Annotate all variables.
# - Use built-in generics list[X], dict[K, V], tuple[...] (PEP 585).
# - Use X | None for optionals (PEP 604).
# - Use Literal for small enumerations of allowed values.
# - Use TypedDict for JSON-like records or configs with fixed keys.
# - Use Protocol for "shape" typing (duck typing).
# - Use Final for constants and to express intent.
# - Avoid Any except at boundaries; prefer narrow types.
# - Prefer guards (isinstance, is None) to narrow unions.
# - Use assert for runtime assumptions that help static checkers.
# - Keep variable names and annotations in sync; update annotations if code changes.
