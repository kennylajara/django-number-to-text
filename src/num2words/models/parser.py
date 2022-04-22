from typing import Optional

from django.db import models

from .token import Token, TokenType


class ParseError(Exception):
    pass


class Parser(models.Model):
    """
    Parser model.
    """

    def parse(self, tokens: list[Token]) -> Optional[list[Token]]:

        if len(tokens) == 0:
            raise ParseError("Empty tokens")
        elif len(tokens) == 1:
            return self._single_parsing(tokens)
        else:
            return self._multiple_parsing(tokens)

    def _single_parsing(self, tokens: list[Token]) -> Optional[list[Token]]:
        if tokens[0].type == TokenType.NUMBER:
            if tokens[0].value != "0" and tokens[0].value.startswith("0"):
                raise ParseError("Non-zero number starts with zero")
            return tokens
        else:
            raise ParseError("Does not starts with number")

    def _multiple_parsing(self, tokens: list[Token]) -> Optional[list[Token]]:
        comman_found = False
        dot_found = False
        is_first_token = True
        result = []
        ends_with_number = False

        for token in tokens:
            ends_with_number = token.type == TokenType.NUMBER
            if is_first_token:
                if token.type != TokenType.NUMBER:
                    raise ParseError("Does not starts with number")
                elif token.value != "0" and token.value.startswith("0"):
                    raise ParseError("Non-zero number starts with zero")
                is_first_token = False

            if token.type == TokenType.NUMBER:
                if comman_found and not dot_found and len(token.value) != 3:
                    raise ParseError(
                        "Numbers after comma and before dot must be 3 digits"
                    )
            elif token.type == TokenType.COMMA:
                if dot_found:
                    raise ParseError("Can't not use comma after dot")
                if len(tokens[0].value) > 3:
                    raise ParseError("Numbers before comma must be 3 digits or less")
                comman_found = True
            elif token.type == TokenType.DOT:
                if dot_found:
                    raise ParseError("Only one dot is allowed")
                dot_found = True
            else:
                raise ParseError("Invalid character found")

            if token.type != TokenType.COMMA:
                result.append(token)

        if not ends_with_number:
            raise ParseError("Does not ends with number")

        return result

    class Meta:
        managed = False
