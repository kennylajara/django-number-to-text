from typing import Union


def num2english(number: Union[int, float, str]) -> str:
    """
    Converts numbers into words.
    """
    from .models.lexer import Lexer
    from .models.parser import Parser
    from .models.ast import AST
    from .models.translator import TranslatorEnglish

    lexer = Lexer()
    parser = Parser()
    translator = TranslatorEnglish()

    tokens = lexer.tokenize(str(number))
    parsed_tokens = parser.parse(tokens)
    ast = AST(parsed_tokens)
    translation = translator.translate(ast)

    return translation


def number_format(number: Union[int, float, str]) -> str:
    """
    Converts numbers into words.
    """
    from .models.lexer import Lexer
    from .models.parser import Parser
    from .models.ast import AST

    lexer = Lexer()
    parser = Parser()

    tokens = lexer.tokenize(str(number))
    parsed_tokens = parser.parse(tokens)
    ast = AST(parsed_tokens)

    return str(ast)
