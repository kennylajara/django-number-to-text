from .token import Token, TokenType


class AST:
    def __init__(self, tokens: list[Token]):
        self._left, self._right = self._parse(tokens)

    def _parse(self, tokens: list[Token]) -> tuple[list[Token], list[Token]]:
        left: list[Token] = []
        right: list[Token] = []
        dot_found = False

        for token in tokens:
            if token.type == TokenType.DOT:
                dot_found = True
            else:
                if dot_found:
                    right.append(token)
                else:
                    left.append(token)

        return left, right

    def __str__(self):
        left = ",".join(str(x) for x in self._left)
        right = "".join(str(x) for x in self._right)
        if right:
            return left + "." + right
        return left

    def __repr__(self):
        return f"AST('{str(self)}')"

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def get(self):
        return self._left, self._right
