from typing import Optional, TypedDict, List, Callable

from sympy import Symbol, sympify, Function as SymFunction
from sympy.parsing.latex import parse_latex
from sympy.core.function import AppliedUndef
# import Expression from sympy
from sympy.core.expr import Expr

class VarTable(TypedDict):
    str: str

class VarResolverReturn(TypedDict):
    latex: str
    namespace: Optional[List[VarTable]]