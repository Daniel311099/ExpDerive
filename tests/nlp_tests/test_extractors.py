from ExpDerive.nlp.extractors import ColumnExtractor, FuncExtractor
from ExpDerive.nlp.preprocessor import Preprocessor, ExpressionExtractor

def test_response_parser(
        response, 
        expected, 
        extractor
):
    parsed = extractor.parse_response(response)
    assert parsed == expected


# extractor tests:
# test response parsers
# test extract method