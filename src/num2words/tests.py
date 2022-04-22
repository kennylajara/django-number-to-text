from django.test import SimpleTestCase

from .models.token import Token, TokenType
from .models.lexer import Lexer
from .models.parser import Parser, ParseError
from .models.ast import AST
from .models.translator import TranslatorEnglish


class TestLexer(SimpleTestCase):
    def test_lexer_tokenize_numbers_from_0_to_999_correctly(self):
        lexer = Lexer()

        for num in range(0, 1000):
            num_str = str(num)
            tokens = lexer.tokenize(num_str)
            self.assertIsInstance(tokens, list)

            for token in tokens:
                self.assertIsInstance(token, Token)
                self.assertEqual(token.value, num_str)
                self.assertEqual(token.type, TokenType.NUMBER)

    def test_lexer_tokenize_numbers_from_higher_than_999_correctly(self):
        lexer = Lexer()
        tests = [
            ("1234", ("1", "234")),
            ("12345", ("12", "345")),
            ("123456", ("123", "456")),
            ("1234567", ("1", "234", "567")),
            ("12345678", ("12", "345", "678")),
            ("123456789", ("123", "456", "789")),
            ("1234567890", ("1", "234", "567", "890")),
        ]

        for test in tests:
            tokens = lexer.tokenize(test[0])
            expected_result = [Token(t, TokenType.NUMBER) for t in test[1]]

            with self.subTest(number=test[0]):
                for tokenized, expected_token in zip(tokens, expected_result):
                    self.assertIsInstance(tokenized, Token)
                    self.assertEqual(type(tokenized.value), type(expected_token.value))
                    self.assertEqual(type(tokenized.type), type(expected_token.type))
                    self.assertEqual(tokenized.value, expected_token.value)
                    self.assertEqual(tokenized.type, expected_token.type)

    def test_lexer_tokenize_non_numberic_chars_correctly(self):
        lexer = Lexer()

        for char in ".,!@#$%^&*()_+abcdefghijklmnopqrstuvwxyz":
            tokens = lexer.tokenize(char)
            self.assertIsInstance(tokens, list)

            for token in tokens:
                self.assertIsInstance(token, Token)
                self.assertEqual(token.value, char)
                if char == ".":
                    self.assertEqual(token.type, TokenType.DOT)
                elif char == ",":
                    self.assertEqual(token.type, TokenType.COMMA)
                else:
                    self.assertEqual(token.type, TokenType.INVALID)

    def test_lexer_tokenize_number_with_comman_and_dot_correctly(self):
        lexer = Lexer()
        number = "123,456.789"
        tokens = lexer.tokenize(number)
        expected_result = [
            Token("123", TokenType.NUMBER),
            Token(",", TokenType.COMMA),
            Token("456", TokenType.NUMBER),
            Token(".", TokenType.DOT),
            Token("789", TokenType.NUMBER),
        ]

        for token, expected_token in zip(tokens, expected_result):
            self.assertIsInstance(token, Token)
            self.assertEqual(type(token.value), type(expected_token.value))
            self.assertEqual(type(token.type), type(expected_token.type))
            self.assertEqual(token.value, expected_token.value)
            self.assertEqual(token.type, expected_token.type)


class TestParser(SimpleTestCase):
    def test_parser_parse_numbers_correctly(self):
        parser = Parser()

        for number in range(0, 1000):
            tokens = [Token(str(number), TokenType.NUMBER)]
            expected_result = tokens  # no change
            parsed = parser.parse(tokens)

            with self.subTest(number=number):
                for parsed_token, expected_token in zip(parsed, expected_result):
                    self.assertIsInstance(parsed_token, Token)
                    self.assertEqual(
                        type(parsed_token.value), type(expected_token.value)
                    )
                    self.assertEqual(type(parsed_token.type), type(expected_token.type))
                    self.assertEqual(parsed_token.value, expected_token.value)
                    self.assertEqual(parsed_token.type, expected_token.type)

    def test_parser_parse_numbers_with_comma_correctly(self):
        parser = Parser()
        tests = [
            (("1", ",", "234"), ("1", "234")),
            (("12", ",", "345"), ("12", "345")),
            (("123", ",", "456"), ("123", "456")),
            (("1", ",", "234", ",", "567"), ("1", "234", "567")),
            (("12", ",", "345", ",", "678"), ("12", "345", "678")),
            (("123", ",", "456", ",", "789"), ("123", "456", "789")),
            (("1", ",", "234", ",", "567", ",", "890"), ("1", "234", "567", "890")),
        ]

        for test in tests:
            tokens = [
                Token(t, TokenType.NUMBER) if t != "," else Token(t, TokenType.COMMA)
                for t in test[0]
            ]
            expected_result = [Token(t, TokenType.NUMBER) for t in test[1]]
            parsed = parser.parse(tokens)

            with self.subTest(number=test[0]):
                for parsed_token, expected_token in zip(parsed, expected_result):
                    self.assertIsInstance(parsed_token, Token)
                    self.assertEqual(
                        type(parsed_token.value), type(expected_token.value)
                    )
                    self.assertEqual(type(parsed_token.type), type(expected_token.type))
                    self.assertEqual(parsed_token.value, expected_token.value)
                    self.assertEqual(parsed_token.type, expected_token.type)

    def test_parser_parse_numbers_with_dot_correctly(self):
        parser = Parser()
        tests = [
            ("1", ".", "234"),
            ("12", ".", "345"),
            ("123", ".", "456"),
            ("1234", ".", "567"),
            ("12", ".", "345678"),
            ("123", ".", "456789"),
            ("1234", ".", "567890"),
        ]

        for test in tests:
            tokens = [
                Token(t, TokenType.DOT) if t == "." else Token(t, TokenType.NUMBER)
                for t in test
            ]
            expected_result = tokens  # no change
            parsed = parser.parse(tokens)

            with self.subTest(number=test):
                for parsed_token, expected_token in zip(parsed, expected_result):
                    self.assertIsInstance(parsed_token, Token)
                    self.assertEqual(
                        type(parsed_token.value), type(expected_token.value)
                    )
                    self.assertEqual(type(parsed_token.type), type(expected_token.type))
                    self.assertEqual(parsed_token.value, expected_token.value)
                    self.assertEqual(parsed_token.type, expected_token.type)

    def test_parser_parse_numbers_with_comma_and_dot_well_formated_correctly(self):
        parser = Parser()
        tests = [
            ("1", ",", "234", ".", "567"),
            ("12", ",", "345", ".", "678"),
            ("123", ",", "456", ".", "789"),
            ("1", ",", "234", ",", "567", ".", "890"),
        ]

        for test in tests:
            tokens = []
            expected_result = []
            for t in test:
                if t == ",":
                    tokens.append(Token(t, TokenType.COMMA))
                    # Don't add a comma to the expected result
                elif t == ".":
                    tokens.append(Token(t, TokenType.DOT))
                    expected_result.append(Token(t, TokenType.DOT))
                else:
                    tokens.append(Token(t, TokenType.NUMBER))
                    expected_result.append(Token(t, TokenType.NUMBER))

        parsed = parser.parse(tokens)

        with self.subTest(number=test):
            for parsed_token, expected_token in zip(parsed, expected_result):
                self.assertIsInstance(parsed_token, Token)
                self.assertEqual(type(parsed_token.value), type(expected_token.value))
                self.assertEqual(type(parsed_token.type), type(expected_token.type))
                self.assertEqual(parsed_token.value, expected_token.value)
                self.assertEqual(parsed_token.type, expected_token.type)

    def test_parser_parse_numbers_bad_formated_correctly(self):
        parser = Parser()
        tests = [
            # Empty
            tuple(),
            # Invalid character
            ("a"),
            # Comma after dot
            ("1", ".", "234", ",", "567"),
            # Leading zero
            ("01",),
            ("012", "345"),
            # Starts with non-number
            (",", "1"),
            (".", "1"),
            # Ends with non-number
            ("1", ","),
            # Two dots
            ("1", ".", "234", ".", "567"),
            # Number after comma and before doesn't have 3 digits
            ("1", ",", "23", ".", "567"),
            ("1", ",", "1", ".", "567"),
            ("1", ",", "2345", ".", "678"),
            # Number before comman with more than 3 digits
            ("12345", ",", "678"),
        ]

        for test in tests:
            tokens = []
            for t in test:
                if t == ",":
                    tokens.append(Token(t, TokenType.COMMA))
                elif t == ".":
                    tokens.append(Token(t, TokenType.DOT))
                elif t.isdigit():
                    tokens.append(Token(t, TokenType.NUMBER))
                else:
                    tokens.append(Token(t, TokenType.INVALID))

            with self.subTest(number=test):
                with self.assertRaises(ParseError):
                    parser.parse(tokens)


class TestAST(SimpleTestCase):
    def test_ast_initialization(self):
        token_list = [
            Token("1", TokenType.NUMBER),
            Token("234", TokenType.NUMBER),
            Token(".", TokenType.DOT),
            Token("567", TokenType.NUMBER),
            Token("890", TokenType.NUMBER),
        ]
        expected_left = [
            Token("1", TokenType.NUMBER),
            Token("234", TokenType.NUMBER),
        ]
        expected_right = [
            Token("567", TokenType.NUMBER),
            Token("890", TokenType.NUMBER),
        ]

        ast = AST(token_list)
        self.assertIsInstance(ast, AST)
        self.assertEqual(str(ast), "1,234.567890")
        for token, expected_token in zip(ast.left, expected_left):
            self.assertIsInstance(token, Token)
            self.assertEqual(type(token.value), type(expected_token.value))
            self.assertEqual(type(token.type), type(expected_token.type))
            self.assertEqual(token.value, expected_token.value)
            self.assertEqual(token.type, expected_token.type)
        for token, expected_token in zip(ast.right, expected_right):
            self.assertIsInstance(token, Token)
            self.assertEqual(type(token.value), type(expected_token.value))
            self.assertEqual(type(token.type), type(expected_token.type))
            self.assertEqual(token.value, expected_token.value)
            self.assertEqual(token.type, expected_token.type)
