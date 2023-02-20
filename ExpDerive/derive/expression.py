from typing import Optional, TypedDict, List, Callable, Union

from sympy import Symbol, sympify, Function as SymFunction
from sympy.parsing.latex import parse_latex
from sympy.core.function import AppliedUndef
# import Expression from sympy
from sympy.core.expr import Expr

class Func():
    # TODO:
    # defines a function object,
    # a tree structure that is callable and is able to flatten itself out
    # can be defined with a latex string or a pure python function
    # wrap eval with a function that takes a string and returns the evaluated value
    # refactor, move some functions from VAR to here 
    def __init__(self, name, params=None, latex=None, func=None):
        self.name = name
        # self.arguments = arguments
        # self.latex = latex
        # self.expression: Optional[Expr] = parse_latex(latex) if latex else None
        self.expression: Optional[Expression] = Expression(latex) if latex else None
        self.func = func
        self.params = params

    def unpack(self, func_resolver):
        # if self.latex:
            # self.expression.derive_funcs(var_resolver)
        func_def = func_resolver(self.name)
        if func_def['latex']:
            self.latex = func_def['latex']
            self.expression = Expression(self.latex)
            self.expression.derive_funcs()
        elif func_def['func']:
            self.func = func_def['func']
            self.params = self.params
            
    
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

class Var():
    def __init__(self, name, latex=None, namespace=None):
        self.name = name
        self.latex = latex
        self.expression: Optional[Expression] = Expression(latex) if latex else None # can be changed to None if latex param is removed
        self.symbol = Symbol(name)
        self.namespace = namespace # namespace of the parent expression, used to identify and unpack the variable
    
    def eval(self, resolver):
        if not self.latex:
            val = resolver(self.name, self.namespace)
            return val
        else:
            self.expression.eval(val)

    def unpack(self, var_resolver):
        if self.latex:
            if self.namespace:
                var_content = var_resolver(name=self.name, namespce=self.namespace)
            else:
                var_content = var_resolver(self.name)
            self.latex = var_content['latex']
            self.expression = Expression(self.latex)
            self.expression.derive_vars(var_content['namespace'])


# expressions cannot be leafs, must have child vars or funcs, must have latex
class Expression():
    def __init__(self, latex):
        self.latex = latex
        self.expression: Expr = parse_latex(latex) 
        self.variables: dict[str, Var] = {}
        self.functions: dict[str, Func] = {}
        self.record_resolver = None
        self.flattend = None
        self.eval_resolver = None # built at runtime
        self.var_resolver = None 
        self.func_resolver = None
    
    def derive_vars(self, namespace=None):
        vars = self.expression.atoms(Symbol)
        for v in vars:
            v_obj = Var(name=v, namespace=namespace)
            v_obj.unpack(self.var_resolver)
            self.variables[v] = v_obj

    def derive_funcs(self):
        func_calls = self.expression.atoms(AppliedUndef)
        # func_names = set(map(
        #     lambda f: f.func.__name__,
        #     func_calls
        # ))
        for f in func_calls:
            f_name = f.func.__name__
            f_obj = Func(name=f_name)
            f_obj.unpack(self.func_resolver)
            self.functions[f_name] = f_obj


    def flatten_vars(self):
        pass

    def flatten_funcs(self):
        pass

    def flatten(self):
        pass

    def simplify(self):
        pass
        
    def eval(self, subjects, *args):
        # params = self.expression.atoms(Symbol)

        to_sub = {p: a for p, a in zip(params, args)}
        value = self.expression.evalf(subs=to_sub)
        return value

    def eval_args(self, *args, **kwargs):
        value = self.expression.evalf()
        # if kwargs:
        #     value = self.
        pairs = zip(self.variables.items(), args)
        for var, val in pairs:
            child_val = var[1].eval(val) # no need to pass anything else as the deeper structure wll have already been built
            value = value.subs(var[0], child_val)
        return value

    def eval_funcs(self, *args):
        pass

class Request():
    pass
    # wrap the request object to make it easier to access the data
    # add caching to the request object


class Stat():
    pass

class Subject():
    def __init__(self, subject_id):
        self.subject_id = subject_id
        self.stats = {}
        self.value = None

    def eval(self, eval_resolver):
        self.value = eval_resolver(self.stats)

class SubjectList():
    def __init__(self, subjects: List[str]):
        self.subjects: List[Subject] = [Subject(s) for s in subjects]

    def get_records(self, record_resolver, columns):
        for subject in self.subjects:
            subject.stats = record_resolver(subject.subject_id, columns)
        # return self.records
    
    def evaluateSubjects(self, eval_resolver):
        for subject in self.subjects:
            subject.eval(eval_resolver)