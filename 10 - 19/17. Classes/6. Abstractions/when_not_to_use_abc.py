"""
Guidelines for situations when Abstract Base Classes (ABC) should not be used.

This file explains scenarios where duck typing, Protocols,
or simple concrete classes are more appropriate than ABCs.
"""


# ----------------------------------------
# 1) INTRODUCTION
# ----------------------------------------

# Abstract Base Classes are powerful, but not always necessary.
#
# Overusing ABCs can lead to rigid architectures, unnecessary complexity,
# and more boilerplate code.
#
# Python's dynamic nature allows alternatives:
# - Duck typing
# - Protocols (structural typing)
# - Simple concrete classes without enforced abstraction


# ----------------------------------------
# 2) DUCK TYPING INSTEAD OF ABC
# ----------------------------------------

# Duck typing relies on the presence of methods and attributes
# rather than formal inheritance.
#
# Example: any object with a "read" method can be used in a function
# that expects something readable, regardless of its class hierarchy.
#
# Advantages:
# - No extra boilerplate
# - Flexible
# - Works naturally with Python's dynamic style
#
# When to prefer duck typing:
# - Interfaces are simple
# - There is only one or two implementations
# - Type checking is not critical at runtime


# ----------------------------------------
# 3) PROTOCOLS INSTEAD OF ABC
# ----------------------------------------

# Protocols (from typing module) allow structural typing.
#
# Advantages over ABC:
# - No need to inherit
# - Less rigid
# - Ideal for large codebases with multiple unrelated implementations
#
# Use Protocols when:
# - You want static type checking
# - You want behavior contracts without inheritance
# - ABC would force artificial class hierarchy


# ----------------------------------------
# 4) SIMPLE CONCRETE CLASSES
# ----------------------------------------

# Sometimes there is no need for ABC at all.
#
# If you have a single implementation or a small number of classes,
# an abstract base class is overkill.
#
# Simple concrete classes are sufficient and reduce boilerplate.


# ----------------------------------------
# 5) PERFORMANCE CONSIDERATIONS
# ----------------------------------------

# ABCs introduce minor runtime overhead because Python
# tracks __abstractmethods__ and enforces instantiation checks.
#
# In performance-critical code, or code that creates millions of objects,
# consider whether ABCs are truly necessary.


# ----------------------------------------
# 6) SUMMARY RECOMMENDATIONS
# ----------------------------------------

# Use ABCs when:
# - You need a formal behavioral contract
# - Multiple concrete subclasses exist
# - You want to enforce method implementation strictly

# Avoid ABCs when:
# - Only one implementation exists
# - Duck typing suffices
# - Protocols provide the necessary static checks
# - You want to keep the system flexible and lightweight

# Good design balances abstraction with simplicity and readability.
