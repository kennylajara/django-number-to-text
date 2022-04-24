from django.db import models

from .token import Token, TokenType


class Lexer(models.Model):
    """
    Lexer model.
    """

    def tokenize(self, number: str) -> list[Token]:
        """
        Tokenize the given number string
        """
        tokens = []
        for char in number:
            if char == ".":
                tokens.append(Token(char, TokenType.DOT))
            elif char == ",":
                tokens.append(Token(char, TokenType.COMMA))
            elif char.isdigit():
                if len(tokens) == 0 or tokens[-1].type != TokenType.NUMBER:
                    tokens.append(Token(char, TokenType.NUMBER))
                else:
                    tokens[-1].value += char
            else:
                tokens.append(Token(char, TokenType.INVALID))

        return self._resize_tokens(tokens)

    def _resize_tokens(self, tokens: list[Token]) -> list[Token]:

        new_tokens = []
        for token in tokens:
            if token.type == TokenType.NUMBER and len(token.value) > 3:
                new_tokens += self._explode_token(token)
            else:
                new_tokens.append(token)

        return new_tokens

    def _explode_token(self, token: Token) -> list[Token]:
        tokens: list[Token] = []
        token_reversed_value = token.value[::-1]
        for i in range(0, len(token_reversed_value), 3):
            new_token = Token(token_reversed_value[i : i + 3][::-1], TokenType.NUMBER)
            tokens.insert(0, new_token)

        return tokens

    class Meta:
        managed = False
