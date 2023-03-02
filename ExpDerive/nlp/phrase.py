from typing import Optional

from .classifiers import ColumnClassifier, FuncClassifier


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
    ):
        # preprocess(self.phrase)
        # extract columns
        # extract functions
        column_phrases = []
        columns = column_classifier.classify_columns(column_phrases)
        # classify columns
        # classify functions
        # generate latex
        pass