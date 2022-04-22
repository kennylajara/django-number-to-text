from enum import Enum, auto


class TokenType(Enum):
    """
    Enum for token types.
    """

    COMMA = auto()
    DOT = auto()
    INVALID = auto()
    NUMBER = auto()


class Token:
    """
    Class for tokens.
    """

    def __init__(self, value, type):
        self.value: str = value
        self.type: TokenType = type

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Token('{self.value}', {self.type})"
