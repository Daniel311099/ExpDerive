from typing import Optional, TypedDict, List, Callable, Union

from sympy import Symbol, sympify, Function as SymFunction
from sympy.parsing.latex import parse_latex
from sympy.core.function import AppliedUndef
# import Expression from sympy
from sympy.core.expr import Expr

# from .imports import Evaluator as MyEvaluator, Var, Func
import ExpDerive.derive.imports as imports




# expressions cannot be leafs, must have latex
class Expression():
    def __init__(self, latex, var_resolver=None, func_resolver=None, is_func=False):
        self.latex = latex
        self.expr: Expr = parse_latex(latex) 
        self.variables: dict[str, imports.expression_components.Var] = {}
        self.functions: dict[str, imports.expression_components.Func] = {}
        self.record_resolver = None
        self.flattend = None
        self.eval_resolver = None # built at runtime
        self.var_resolver = var_resolver 
        self.func_resolver = func_resolver
        self.is_func = is_func
    
    def derive_vars(self, namespace=None):
        vars = self.expr.atoms(Symbol)
        for v in vars:
            v_obj = imports.expression_components.Var(name=str(v), namespace=namespace, func_resolver=self.func_resolver, var_resolver=self.var_resolver)
            v_obj.unpack(self.var_resolver, self.func_resolver)
            self.variables[str(v)] = v_obj

    def derive_funcs(self):
        func_calls = self.expr.atoms(AppliedUndef)
        func_names = set(map(
            lambda f: f.func.__name__,
            func_calls
        )) # means that each function is only unpacked once even if called in multiple places
        for f in func_names:
            # f_name = f.func.__name__
            f_obj = imports.expression_components.Func(name=f, func_resolver=self.func_resolver, var_resolver=self.var_resolver)
            f_obj.unpack(self.func_resolver, self.var_resolver)
            self.functions[f] = f_obj


    def flatten_vars(self, params=[]):
        # for var in self.variables.values():
        #     if var.expression:
        #         var.expression.flatten_vars()
        #         var.expression.flatten_funcs()
        #         var.expression.simplify()
        #         self.expr = self.expr.subs(var.symbol, var.expression.expression)
        non_params = [v for v in self.expr.atoms(Symbol) if str(v) not in params]
        for var in non_params:
            print(self.expr, 99, self.variables)
            var_obj = self.variables[str(var)]
            if var_obj.expression:
                var_obj.flatten_var()
                # var_obj.flatten_funcs()
                var_obj.expression.simplify()
                self.expr = self.expr.subs(var, var_obj.expression.expr)

    def flatten_funcs(self):
        for func_call in self.expr.atoms(AppliedUndef):
            func = self.functions[func_call.func.__name__]
            if func.expression:
                # may need to return something from the following functions
                func.flatten_func()
                subbed = func.sub_args(func_call.args)
                print(self.expr, 7, subbed, 7,func_call,7,func.expression.expr)
                self.expr = self.expr.subs(func_call, subbed)
                print(self.expr, 8)


    def flatten(self, params=[]):
        self.flatten_vars(params=params)
        print(self.expr, 1)
        self.simplify()
        self.flatten_funcs()
        print(self.expr, 2)
        self.simplify()
        self.flattend = True

    def simplify(self):
        self.expr = self.expr.evalf()
        
    def eval(self, subjects, *args):
        # params = self.expression.atoms(Symbol)

        to_sub = {p: a for p, a in zip(params, args)}
        value = self.expr.evalf(subs=to_sub)
        return value

    def eval_args(self, *args, **kwargs):
        value = self.expr.evalf()
        # if kwargs:
        #     value = self.
        pairs = zip(self.variables.items(), args)
        for var, val in pairs:
            child_val = var[1].eval(val) # no need to pass anything else as the deeper structure wll have already been built
            value = value.subs(var[0], child_val)
        return value

    def eval_funcs(self, *args):
        pass

    def build_evaluator(self):
        self.eval_resolver = imports.evaluate.Evaluator(self)
        def evaluator(*args):
            return self.eval_args(*args)


class Request():
    pass
    # wrap the request object to make it easier to access the data
    # add caching to the request object


class Stat():
    pass

