from typing import Optional, Callable

import pickle

from .phrase import Phrase
from .classifiers import ColumnClassifier, FuncClassifier
from .extractors import ExpressionExtractor, ColumnExtractor, FuncExtractor
from .latex import Latex

class NlpAPI():
    def __init__(
        self,
        api_key: str,
        preprocessor = ExpressionExtractor(engine='ada'),
        column_extractor = ColumnExtractor(engine='ada'),
        func_extractor = FuncExtractor(engine='ada'),
        latex_generator = Latex(),
    ):
        self.api_key = api_key
        # fine tuned gpt 3
        self.preprocessor = ExpressionExtractor(preprocessor) if type(preprocessor) == str else preprocessor
        self.column_extractor: ColumnExtractor = ColumnExtractor(column_extractor) if type(column_extractor) == str else column_extractor
        self.func_extractor: FuncExtractor = FuncExtractor(func_extractor) if type(func_extractor) == str else func_extractor
        # user made models, must be ivy models
        self.column_classifier = None
        self.func_classifier = None
        # saytex or fine tuned gpt 3
        self.latex_generator = latex_generator

    # pass filepaths to classifiers, used if the cli was used to train the models, if not allow users to assign their own models to self.column_classifier and self.func_classifier
    def load_column_classifier(self, filepath: str):
        file = open(filepath, 'rb')
        column_classifier: ColumnClassifier = pickle.load(file)
        # self.column_classifier = ColumnClassifier(column_classifier)
        self.column_classifier = column_classifier
        file.close()

    def load_func_classifier(self, filepath: str):
        file = open(filepath, 'rb')
        func_classifier = pickle.load(file)
        self.func_classifier = FuncClassifier(func_classifier)
        file.close()

    def parse_phrase(self, phrase):
        phrase_obj = Phrase(phrase)
        phrase_obj.parse(
            self.preprocessor,
            self.column_extractor,
            self.func_extractor,
            self.column_classifier,
            self.func_classifier,
            self.latex_generator,
        )
        return phrase_obj
    
    def set_column_classifier(self, model):
        self.column_classifier = ColumnClassifier(model)
    
    # def train_preprocessor(self, phrases):
    #     pass

    # def train_column_extractor(self, phrases):
    #     pass

    # def train_func_extractor(self, phrases):
    #     pass

    def train_column_classifier(self, phrases):
        pass

    def train_func_classifier(self, phrases):
        pass

    # def train_latex_generator(self, phrases):
    #     pass