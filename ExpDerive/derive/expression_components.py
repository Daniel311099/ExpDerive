from typing import Optional, TypedDict, List, Callable, Union

from sympy import Symbol, sympify, Eq, Function as SymFunction
from sympy.parsing.latex import parse_latex
from sympy.core.function import AppliedUndef
# import Expression from sympy
from sympy.core.expr import Expr

import ExpDerive.derive.imports as imports

class Func():
    # TODO:
    # defines a function object,
    # a tree structure that is callable and is able to flatten itself out
    # can be defined with a latex string or a pure python function
    # wrap eval with a function that takes a string and returns the evaluated value
    # refactor, move some functions from VAR to here 
    def __init__(self, name, params=(), latex=None, func=None, func_resolver=None, var_resolver=None):
        self.name = name
        # self.arguments = arguments
        # self.latex = latex
        # self.expression: Optional[Expr] = parse_latex(latex) if latex else None
        self.expression: Optional[imports.expression.Expression] = Expression(latex, func_resolver=func_resolver, var_resolver=var_resolver) if False else None
        self.func = func
        self.flat = None 
        self.params = params # needed as the order of the params is important, mainly for the latex string

    def unpack(self, func_resolver, var_resolver):
        # if self.latex:
            # self.expression.derive_funcs(var_resolver)
        func_def = func_resolver(self.name)
        # change the branch condition to not require a latex string if a function is provided
        # if func_def['latex']:
        try:
            self.latex = func_def['latex']
            self.expression = imports.expression.Expression(self.latex, func_resolver=func_resolver, var_resolver=var_resolver, is_func=True)
            self.expression.derive_vars()
            self.expression.derive_funcs()
            self.params = func_def['params']
        # elif func_def['func']:
        except KeyError:
            self.func = func_def['func']
            self.params = self.func.__code__.co_varnames[:self.func.__code__.co_argcount]
            # self.flat is a sympy function based on func
            self.flat = SymFunction(self.name)(*self.params)
    

    # expands a given call
    def flatten_func(self):

        if self.expression:
            self.expression.flatten(params=self.params)
            # self.flat = self.sub_args(self.params)
            # self.sub_args(args)

            
    def __call__(self, *args):
        # TODO: allow to pass kwargs instead of args
        if self.func:
            return self.func(*args)
        elif self.expression:
            expanded = self.expression.eval(*args)
            # params = self.expression.expression.atoms(Symbol)
            # to_sub = {p: a for p, a in zip(params, expanded)}
            # return self.expression.expression.evalf(subs=to_sub)
            return expanded
        
    def sub_args(self, args):
        to_sub = {p: a for p, a in zip(self.params, args)}
        return self.expression.expr.evalf(subs=to_sub)


class Var():
    def __init__(self, name, latex=None, namespace=None, var_resolver=None, func_resolver=None):
        self.name = name
        self.latex = latex
        self.expression: Optional[imports.expression.Expression] = imports.expression.Expression(latex, var_resolver=var_resolver, func_resolver=func_resolver) if latex else None # can be changed to None if latex param is removed
        self.symbol = Symbol(name)
        self.namespace = namespace # namespace of the parent expression, used to identify and unpack the variable
    
    def eval(self, resolver):
        if not self.latex:
            val = resolver(self.name, self.namespace)
            return val
        else:
            self.expression.eval(val)

    def unpack(self, var_resolver, func_resolver):
        if self.namespace:
            print(var_resolver.__code__.co_varnames)
            var_content = var_resolver(name=self.name, namespace=self.namespace)
        else:
            var_content = var_resolver(self.name)
        try:
            # var_content['latex']
            self.latex = var_content['latex']
            self.expression = imports.expression.Expression(self.latex, var_resolver=var_resolver, func_resolver=func_resolver)
            self.expression.derive_vars(var_content['namespace'])
            self.expression.derive_funcs()
        except KeyError:
            pass

    def flatten_var(self):
        if self.expression:
            self.expression.flatten()

