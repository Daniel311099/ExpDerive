from typing import Optional, TypedDict

from .classifiers import ColumnClassifier, FuncClassifier

class ParsedPhrase(TypedDict):
    phrase: str
    latex: str
    columns: list

class Phrase():
    def __init__(self, phrase: str):
        self.phrase = phrase
        self.latex: Optional[str] = None
    
    def parse(
        self,
        preprocessor,
        column_extractor,
        func_extractor,
        column_classifier: ColumnClassifier,
        func_classifier: Optional[str]=None,
        latex_generator: Optional[str]=None,
    ) -> ParsedPhrase:
        # preprocess(self.phrase)
        # extract columns
        # extract functions
        column_phrases = []
        columns = column_classifier.classify_columns(column_phrases)
        # classify columns
        # classify functions
        # generate latex
        return {
            'phrase': self.phrase,
            'latex': self.latex,
            'columns': columns,
        }