import re

from django.db import models

from .ast import AST
from .token import Token


class TranslatorError(Exception):
    pass


class TranslatorBase(models.Model):
    """
    Translator model.
    """

    def translate(self, ast: AST) -> str:
        """
        Translate the given AST
        """
        raise NotImplementedError()

    class Meta:
        managed = False


class TranslatorEnglish(TranslatorBase):
    """
    Translator model for English.
    """

    def translate(self, ast: AST) -> str:
        """
        Translate the given AST
        """
        left, right = ast.get()
        left_translation = self._translate_tokens(left, accept_leading_zero=False)
        right_translation = self._translate_tokens(right, accept_leading_zero=True)

        if right_translation.strip() == "":
            result = left_translation
        else:
            result = left_translation + " POINT " + right_translation

        return re.sub(" +", " ", result.strip())

    def _translate_tokens(self, tokens: list[Token], accept_leading_zero: bool) -> str:
        translated_tokens = []
        for token in tokens:
            if len(token.value) == 1:
                translated_tokens.append(self._translate_one_digit(token.value))
            elif len(token.value) == 2:
                translated_tokens.append(
                    self._translate_two_digits(token.value, accept_leading_zero)
                )
            elif len(token.value) == 3:
                translated_tokens.append(
                    self._translate_three_digits(token.value, accept_leading_zero)
                )
            else:
                raise ValueError("Invalid token value: " + token.value)

        return self._join_three_digits_translations(translated_tokens)

    def _join_three_digits_translations(self, translations: list[str]) -> str:
        result = ""
        for i, translation in enumerate(translations):
            translation = re.sub(" +", " ", translation.strip())
            full_zero_translation = (len(translation.split(" ")) * "ZERO ").strip()

            print("translation", translation)
            print("full_zero_translation", full_zero_translation)

            if translation == full_zero_translation:
                result += " " + translation + " "
            else:
                j = len(translations) - i - 1
                if j == 0:
                    result += translation
                elif j == 1:
                    result += translation + " THOUSAND "
                elif j == 2:
                    result += translation + " MILLION "
                elif j == 3:
                    result += translation + " BILLION "
                elif j == 4:
                    result += translation + " TRILLION "
                elif j == 5:
                    result += translation + " QUADRILLION "
                elif j == 6:
                    result += translation + " QUINTILLION "
                elif j == 7:
                    result += translation + " SEXTILLION "
                elif j == 8:
                    result += translation + " SEPTILLION "
                elif j == 9:
                    result += translation + " OCTILLION "
                elif j == 10:
                    result += translation + " NONILLION "
                elif j == 11:
                    result += translation + " DECILLION "
                else:
                    max_length = (
                        11 * 3 + 3
                    )  # Last value of j multiplied by 3 + 3 for the 'THOUSAND'
                    raise TranslatorError(
                        f"Invalid number of digits. Max is {max_length} at each side of the point."
                    )

        return result

    def _translate_three_digits(self, number: str, accept_leading_zero: bool) -> str:
        first_digit = self._translate_one_digit(number[0])
        last_two_digits = self._translate_two_digits(number[1:], accept_leading_zero)

        if first_digit.strip() == "":
            result = last_two_digits
        elif last_two_digits.strip() == "":
            result = first_digit
        else:
            if first_digit == "ZERO":
                result = first_digit + " " + last_two_digits
            else:
                result = first_digit + " HUNDRED " + last_two_digits

        return " " + result + " "

    def _translate_one_digit(self, number: str) -> str:
        translation = {
            "0": "ZERO",
            "1": "ONE",
            "2": "TWO",
            "3": "THREE",
            "4": "FOUR",
            "5": "FIVE",
            "6": "SIX",
            "7": "SEVEN",
            "8": "EIGHT",
            "9": "NINE",
        }
        return translation[number]

    def _translate_two_digits(self, number: str, accept_leading_zero: bool) -> str:
        translation = {
            "00": "ZERO ZERO" if accept_leading_zero else "",
            "10": "TEN",
            "11": "ELEVEN",
            "12": "TWELVE",
            "13": "THIRTEEN",
            "14": "FOURTEEN",
            "15": "FIFTEEN",
            "16": "SIXTEEN",
            "17": "SEVENTEEN",
            "18": "EIGHTEEN",
            "19": "NINETEEN",
            "20": "TWENTY",
            "30": "THIRTY",
            "40": "FORTY",
            "50": "FIFTY",
            "60": "SIXTY",
            "70": "SEVENTY",
            "80": "EIGHTY",
            "90": "NINETY",
        }
        try:
            return translation[number]
        except KeyError:
            try:
                if number[0] == "0":
                    if accept_leading_zero:
                        return " ZERO " + self._translate_one_digit(number[1])
                    else:
                        return self._translate_one_digit(number[1])
                else:
                    return (
                        self._translate_two_digits(number[0] + "0", True)
                        + " "
                        + self._translate_one_digit(number[1])
                    )
            except IndexError:
                return ""
