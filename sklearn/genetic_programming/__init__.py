"""
Geometric Semantic Genetic Programming (GSGP) is an algorithm for evolving programs across different domains, such as arithmetic, boolean, and classifier domains. This package provides a Python implementation of GSGP, along with additional utility classes and functions for working with evolved programs.

The arithmetic domain focuses on evolving mathematical expressions to solve problems with real numbers, specifically polynomial-based, while the boolean domain focuses on evolving logical expressions for binary classification problems. The classifier domain involves evolving rule-based classifiers for multi-class classification probl in the form of 'if then else'.

This package includes three main modules: 
- arithmetic.py for real domain GSGP 
- boolean.py for boolean domain GSGP
- program.py for classifier domain GSGP

Each module provides a `(Boolean/Arithmetic/Program)GSGP` class for creating and evolving programs, as well as additional utility classes for working with evolved programs.

This package also includes a `(Boolean/Arithmetic/Program)Population` class for generating populations of random functions, which can be useful for testing and experimentation, however the package will handle this automatically.
"""

"""import _base
import _arithmetic
import _boolean
import _program

import tests

__all__ = ['_base', 
           '_arithmetic', 
           '_boolean', 
           '_program']
"""