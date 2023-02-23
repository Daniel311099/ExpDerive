from typing import Optional, TypedDict, List, Callable

from sympy import Symbol, sympify, Function as SymFunction
from sympy.parsing.latex import parse_latex
from sympy.core.function import AppliedUndef
# import Expression from sympy
from sympy.core.expr import Expr

from ExpDerive.derive.imports import expression, evaluate

class Variable(TypedDict):
    custom: bool # leaf or not
    plc: Optional[str]
    column_name: str
    table_name: str
    latex: Optional[str]

class ResolverReturn(TypedDict):
    latex: str
    variables: Optional[List[Variable]]


    


class Var():
    def __init__(self, name, leaf, latex=None, namespace=None):
        self.name = name
        self.latex = latex
        self.expression: Optional[Expr] = parse_latex(latex) if latex else Symbol(name)
        self.vars = {
            # v: Var(v, '') 
            # for v in parse_latex(latex).atoms(Symbol)
        }
        self.leaf = leaf
        self.namespace = namespace

    # def flatten(self, tree: str, resolver: Callable[[str, Optional[str]], ResolverReturn], variables: Optional[List[Variable]] = None):
    #     explicit_vars = bool(variables)
    #     exp = parse_latex(tree)
    #     if explicit_vars:
    #         variable_list = exp.atoms(Symbol)
    #     else:
    #         variable_list = [Symbol(v) for v in variables]
    #     for v in variable_list:
    #         if True:
    #             # change to if v is a base column
    #             # effectively the base case as each iteration will be skipped resulting in no recursive calls
    #             continue
    #         latex = resolver(v)
    #         if explicit_vars:
    #             flattened = self.flatten(latex, resolver, variables)
    #         else:
    #             flattened = self.flatten(latex, resolver)
    #         exp = exp.subs(Symbol(v), flattened)
        
    #     return exp

    def build(self, resolver, func_resolver): # recursive
        # sub_funcs here
        print(self.expression)
        self.sub_funcs(func_resolver)

        if self.leaf:
            return

        for v in self.expression.atoms(Symbol):
            print(self.expression)
            v_tree = resolver(v, self.namespace)
            v_Var = Var(**v_tree)
            v_Var.build(resolver, func_resolver)
            self.vars[str(v)] = v_Var

    def flatten(self):
        if self.leaf:
            return 
        print(self.latex)
        # print(self.vars)
        for k, v in self.vars.items():
            v.flatten()
            print(self.expression, k, v)
            self.expression = self.expression.subs(Symbol(k), v.expression)

        print('//////////')

    def unpack_func(self, exp, func_resolver):
        # exp = parse_latex(latex)
        funcs = exp.atoms(AppliedUndef)
        print(funcs, 11, exp)

        for f in funcs:
            func = func_resolver(f.func)
            args = f.args
            definition = parse_latex(func['latex']) 
            params = definition.atoms(Symbol) # this is wrong, args may be in different order to order in latex string
            for p, a in zip(params, args):
                definition = definition.subs(p, a)
            unpacked = self.unpack_func(definition, func_resolver)
            exp = exp.subs(f, unpacked)
        print(exp, 22)
        return exp

    def sub_funcs(self, func_resolver):
        funcs = self.expression.atoms(AppliedUndef)
        for f in funcs:
            func = func_resolver(f.func)
            # args = [Symbol(a) for a in func['args']]
            args = f.args
            definition = parse_latex(func['latex'])
            definition = self.unpack_func(definition, func_resolver)
            params = definition.atoms(Symbol)
            print( list(zip(params, args)), f, definition)
            for p, a in zip(params, args):
                definition = definition.subs(p, a)
            print(definition)
            # self.expression = self.expression.subs(f, Function(func['latex'])(*args))
            self.expression = self.expression.subs(f, definition)
            # add support to unpack nested definitions, custom functions that call other custom functions
            
            

class ExpTree():
    def __init__(self, latex, name, exp_resolver=None, eval_resolver=None, namespace=None, func_resolver=None):
        self.latex = latex
        self.expression: Expr = parse_latex(latex)
        self.exp_resolver = exp_resolver
        self.eval_resolver = eval_resolver
        self.variables: Optional[List] = None
        self.functions = None
        self.flattened = None
        self.namespace = namespace
        self.tree = None
        self.name = name
        self.func_resolver = func_resolver
        # TODO: add memoization
    
    def build_expression(self):
        # TODO: add an args param to the resolver
        tree = Var(self.name, False, self.latex, self.namespace)
        self.functions = tree.expression.atoms(AppliedUndef)
        
        # tree.sub_funcs(self.func_resolver)


        tree.build(self.exp_resolver, self.func_resolver)
        tree.flatten()
        # TODO: simplify tree.expression
        # sub funcs
        self.tree = tree
        self.variables = tree.expression.atoms(Symbol)

    def check_python_funcs(self):
        for f in self.functions:
            function = self.func_resolver(f.func)
            if function['type'] == 'python':
                return True

        return False

    # def flatten(self, expression: Expr):
    #     # exp = parse_latex(self.latex)
    #     vars = expression
    #     if self.variables:
    #         variable_list = self.variables
    #     else:
    #         variable_list = expression.atoms(Symbol)
    #     for v in variable_list:
    #         pass

    def validate(self):
        # TODO: 
        # check arguments are valid
        # check functions are valid
        # check mathit is valid, use regex
        pass
    
    def sub_funcs(self):
        pass

    def evaluate(self, subjects):
        records = self.get_records(subjects)
        evaluated = list(map(
            lambda record: {
                'subject': record['subject'],
                'value': self.tree.expression.evalf(subs=record['stats'])
            },
            records
        ))
        return evaluated

    def get_records(self, subjects):
        records = [
            {
                'subject': subject,
                'stats': {
                    stat: self.eval_resolver(stat, subject)
                    for stat in self.variables
                }
            }
            for subject in subjects
        ]
        return records


# # pass variables as a list if not encoded in the expression
# # variables needs a resolver
# # resolver is a function that takes the placeholder and returns the latex



# def get_variables(exp):
#     # add string manipulation

#     return list(exp.atoms(Symbol))

# # not exposed to the user
# def sub_funcs(exp):
#     for f in exp.atoms(AppliedUndef):
#         if f.func not in resolver:
#             raise Exception("Undefined function: {}".format(v.func))
#         v.func = resolver[v.func]
#     return exp

class ExpAPI():
    def __init__(self, latex: str, plc_resolver=None, record_resolver=None, func_resolver=None, namespace=None):
        self.plc_resolver = plc_resolver
        self.record_resolver = record_resolver
        self.func_resolver = func_resolver
        self.latex = latex
        self.expression = expression.Expression(latex, var_resolver=plc_resolver, func_resolver=func_resolver)
        self.namespace = namespace

    def build_expression(self):
        self.expression.var_resolver = self.plc_resolver
        self.expression.func_resolver = self.func_resolver
        self.expression.derive_vars(self.namespace)
        # print(self.expression.expr)
        self.expression.derive_funcs()
        print(self.expression.expr, self.expression.functions, self.expression.variables)
        self.expression.flatten()
        # print(self.expression.expr)
        self.expression.simplify()
        # print(self.expression.expr)
        self.expression.build_evaluator()
        return self.expression

    def evaluate(self, subjects):
        subject_list = evaluate.SubjectList(subjects)
        subject_list.get_records(self.record_resolver, self.expression)
        subject_list.evaluateSubjects(self.expression)
        return subject_list

    def validate(self):
        # should be called after build_expression
        # add safe param to build_expression that calls validate after building
        pass
