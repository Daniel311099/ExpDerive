from .extractors import BaseExtractor

class Preprocessor():
    def __init__(self) -> None:
        self.expression_extractor = ExpressionExtractor()
    def preprocess(self, phrase: str):
        return self.expression_extractor.extract(phrase)

class ExpressionExtractor(BaseExtractor):
    def __init__(
        self,
        engine: str = 'gpt-3.5-turbo', # change to chat gpt
    ):
        super().__init__(
            template='Extract the phrase from the following sentance that describes a mathematical expression: ',
            engine=engine,
        )

    def parse_response(self, response):
        parsed = response.choices[0].message.content.split('\n')[0]
        print(parsed)
        return parsed