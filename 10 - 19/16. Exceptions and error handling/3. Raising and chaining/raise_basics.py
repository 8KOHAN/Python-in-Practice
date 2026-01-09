"""
Realistic usage of the `raise` statement.

This file focuses on when and why exceptions should be raised explicitly
in real-world code, not on artificial or abstract examples.
"""

from __future__ import annotations


# ----------------------------------------
# 1) RAISING TO ENFORCE BUSINESS RULES
# ----------------------------------------

def business_rule_demo() -> None:
    print("=== business_rule_demo ===")

    # Here `raise` is used to enforce business constraints.
    #
    # This is not about malformed input,
    # but about rules that define what is allowed.

    def withdraw(*, balance: int, amount: int) -> int:
        if amount < 0:
            raise ValueError("Withdrawal amount must be non-negative")

        if amount > balance:
            raise ValueError("Insufficient funds")

        return balance - amount

    try:
        withdraw(balance=100, amount=250)

    except ValueError as exc:
        print(f"Caught exception: {exc}")

    print()


# ----------------------------------------
# 2) WHEN *NOT* TO RAISE
# ----------------------------------------

def when_not_to_raise_demo() -> None:
    print("=== when_not_to_raise_demo ===")

    # Not every unusual situation should result in `raise`.
    #
    # If a situation is expected and recoverable,
    # normal control flow is often clearer.

    def find_user(users: list[str], name: str) -> bool:
        # Absence of a user is a normal outcome here,
        # not an exceptional condition.
        return name in users

    users = ["alice", "bob"]

    found = find_user(users, "charlie")
    print(f"User found: {found}")

    print()


# ----------------------------------------
# 3) QUICK-RUN
# ----------------------------------------

if __name__ == "__main__":
    business_rule_demo()
    when_not_to_raise_demo()
