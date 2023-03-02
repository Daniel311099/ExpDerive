import openai

class ExpressionExtractor():
    def __init__(
        self,
        engine: str = 'ada',
        model=None,
    ):
        self.engine = engine
        self.model = model

    def gpt_call(self, phrase):
        response = openai.Completion.create(
            engine=self.engine,
            prompt=phrase,
            max_tokens=100,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response
    
    def extract(self, phrase):
        response = self.gpt_call(phrase)
        nl_expression = self.parse_expression(response)
        return nl_expression
    
    def parse_expression(self, response):
        return response.choices[0].text
    
class MyExpressionExtractor(ExpressionExtractor):
    def gpt_call(self, phrase):
        response = openai.Completion.create(
            engine=self.engine,
            prompt=phrase,
            max_tokens=50,
            temperature=0.6,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response


class ColumnExtractor():
    def __init__(
        self,
        engine: str = 'ada',
        model=None,
    ):
        model = None

class FuncExtractor():
    def __init__(
        self,
        engine: str = 'ada',
        model=None,
    ):
        model = None