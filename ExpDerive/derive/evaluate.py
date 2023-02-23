from typing import Optional, TypedDict, List, Callable, Union

from sympy import Symbol, sympify, Function as SymFunction
import sympy
from sympy.parsing.latex import parse_latex
from sympy.core.function import AppliedUndef
# import Expression from sympy
from sympy.core.expr import Expr

# from .imports import Expression1 as MyExpression
import ExpDerive.derive.imports as imports

# MyExpression = imports.Expression


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

    def get_records(self, record_resolver, expression: imports.expression.Expression):
        columns = expression.expr.atoms(Symbol)
        for subject in self.subjects:
            subject.stats = self.get_record(record_resolver, subject.subject_id, columns)
        # return self.records

    def get_record(self, record_resolver, subject_id, columns):
        stats = {}
        for column in columns:
            stat = record_resolver(column, subject_id)
            stats[column] = stat
        return stats
        # return self.records
    
    def evaluateSubjects(self, expression: imports.expression.Expression):
        for subject in self.subjects:
            subject.value = expression.eval_resolver(subject)

# syntax to round to 2 decimal places



    def view_values(self):
        return {
            subject.subject_id: round(float(subject.value), 3) if type(subject.value) == sympy.core.numbers.Float else subject.value
            for subject in self.subjects
        }


class Evaluator():
    def __init__(self, expression: imports.expression.Expression):
        self.expression = expression

    def __call__(self, subject: Subject):
        subbed = self.expression.expr.evalf(subs=subject.stats)
        for func_call in subbed.atoms(AppliedUndef):
            func = self.expression.functions[func_call.func.__name__].func
            result = func(*func_call.args)
            subbed = subbed.subs(func_call, result)
            # catch errors here suchas as zero division
        subbed = subbed.evalf()
        return subbed

