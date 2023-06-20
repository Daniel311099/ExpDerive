from typing import Union
from sympy.parsing.latex import parse_latex
from saytex import Saytex

from .myTypes import Func


class AST():
    def __init__(self, root_func: Func) -> None:
        # self.latex = latex
        # self.phrase = phrase
        self.root_func = root_func
        # self.expr = parse_latex(latex)
        self.args: list[Union[ALeaf, AST]] = []
        self.expression = None

    def flatten(self):
        print("flattening: ", self.root_func.name)
        if self.root_func.type == "infix":
            exp = self.args[0].flatten() if isinstance(self.args[0], AST) else f"??{self.args[0].name}##"
            exp += ' ' + self.root_func.name + ' '
            exp += self.args[1].flatten() if isinstance(self.args[1], AST) else f"??{self.args[1].name}##"
            print("flattened: ", exp)
            return exp
        exp = self.root_func.name + ' '
        args = [
            arg.flatten() if isinstance(arg, AST) else f"??{arg.name}##"
            for arg in self.args
        ]
        exp += ' and '.join(args)
        # exp += ' end '
        print("flattened: ", exp)
        return exp
    
    def build(self):
        if not self.expression:
            self.expression = self.flatten()
        variables = []
        while True:
            var = self.expression.find("??")
            if var == -1:
                break
            end = self.expression.find("##")
            var = self.expression[var+2:end]
            trimmed = var.replace("_", "")
            variables.append((var, trimmed))
            self.expression = self.expression.replace("??", "", 1)
            self.expression = self.expression.replace("##", "", 1)
            self.expression = self.expression.replace(var, trimmed, 1)
        print("expression: ", self.expression)
        saytex = Saytex()
        asLat = saytex.to_latex(self.expression)
        for var, trimmed in variables:
            asLat = asLat.replace(trimmed, r"{\mathit{"+trimmed+"}}")
        return asLat

class ALeaf():
    def __init__(self, name: str) -> None:
        self.name = name

    def build(self):
        return self.name