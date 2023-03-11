from typing import Optional, TypedDict

# import parse_latex from sympy
from sympy.parsing.latex import parse_latex

from .preprocessor import Preprocessor
from .extractors import ColumnExtractor, FuncExtractor
from .classifiers import ColumnClassifier, FuncClassifier
from .latex import Latex

class ParsedPhrase(TypedDict):
    phrase: str
    latex: str
    columns: list

class Phrase():
    def __init__(self, phrase: str):
        self.phrase = phrase
        self.latex: Optional[str] = None
        self.columns: Optional[list] = None
        self.functions: Optional[list] = None
    
    def parse(
        self,
        preprocessor,
        column_extractor,
        func_extractor,
        column_classifier: ColumnClassifier,
        func_classifier: Optional[str]=None,
        latex_generator: Optional[str]=None,
    ) -> ParsedPhrase:
        # preprocessed = preprocessor.preprocess(self.phrase)
        # column_descriptions = column_extractor.extract(preprocessed)
        column_descriptions = column_extractor.extract(self.phrase)
        classified_columns = column_classifier.classify_list(column_descriptions)
        self.columns = classified_columns
        processed = self.replace_descriptions(classified_columns)
        latex = latex_generator.generate(processed, classified_columns)
        self.latex = latex

        # extract columns
        # extract functions
        # classify columns
        # classify functions
        # generate latex
        return {
            'phrase': self.phrase,
            'latex': latex,
            'columns': classified_columns,
            'functions': []
        }
    
    def replace_descriptions(self, entities: list[tuple[str, str]]):
        processed = self.phrase
        for entity in entities:
            processed = processed.replace(entity[0].lower(), entity[1])
        return processed
    
    def __str__(self):
        return str(parse_latex(self.latex)) if self.latex else self.phrase