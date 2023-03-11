# convert here to latex
# clean final string, things like add /mathit{ } to all words
from typing import Any

from saytex import Saytex

from sympy.parsing.latex import parse_latex

class LatexTranslator():
    def __init__(self):
        self.saytex = Saytex()
    
    def convert(self, phrase: str) -> str:
        return self.saytex.to_latex(phrase)

class Latex():
    def __init__(self, model = LatexTranslator()):
        # self.latex = latex
        self.model = model
    
    def generate(self, phrase: str, vars, funcs=[]) -> str:
        latex = self.model.convert(phrase)
        print(parse_latex(latex), 'before', latex)
        latex = self.group_names(latex, vars)
        latex = self.group_names(latex, funcs)
        print(parse_latex(latex), 'after', latex)
        return latex
    
    def group_names(self, latex: str, names: list[tuple[str, str]]) -> str:
        for name in names:
            latex = latex.replace(name[1], '\\'+name[1])
        return latex