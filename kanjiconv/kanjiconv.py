import importlib
import importlib.resources
import json
from typing import Callable

import sudachipy

from kanjiconv.entities import SudachiDictType


def parse_text(func: Callable) -> Callable:
    """
    Decorator function to tokenize text and convert it into readings before applying the given function.

    Args:
        func (Callable): The function to be wrapped, which takes the readings as input.

    Returns:
        Callable: Wrapped function that processes the readings.
    """

    def wrapper(self, text: str):
        tokens = self.tokenizer.tokenize(text)
        readings = self.separator.join([token.reading_form() for token in tokens])
        return func(self, readings)

    return wrapper


class KanjiConv:
    """
    Class for converting Japanese text between different formats such as Hiragana, Katakana, and Roman characters.
    """

    def __init__(
        self,
        sudachi_dict_type: SudachiDictType = SudachiDictType.FULL.value,
        separator: str = " ",
    ) -> None:
        """
        Initializes the KanjiConv instance with a tokenizer and kana conversion data.

        Args:
            sudachi_dict_type (SudachiDictType): Type of the Sudachi dictionary to use for tokenization.
            data_path (str): Path to the JSON file containing kana conversion data.
            separator (str): Separator to use between token readings.
        """
        # Load the kana.json file from the package.
        kana_path = importlib.resources.files("kanjiconv.data").joinpath("kana.json")
        with kana_path.open("r") as f:
            self.kana = json.load(f)

        # Initialize Sudachi tokenizer
        sudachi_dict = sudachipy.Dictionary(dict=sudachi_dict_type)
        self.tokenizer = sudachi_dict.create()
        self.separator = separator

    @parse_text
    def to_hiragana(self, text: str) -> str:
        """
        Convert Katakana characters in the given text to Hiragana.

        Args:
            text (str): The input text containing Katakana characters.

        Returns:
            str: The converted text with Hiragana characters.
        """
        hiragana_text = ""
        for char in text:
            # Convert Katakana characters to Hiragana by adjusting their Unicode code point
            if "ァ" <= char <= "ン":
                hiragana_text += chr(ord(char) - 0x60)
            else:
                hiragana_text += char
        return hiragana_text

    @parse_text
    def to_katakana(self, text: str) -> str:
        """
        Convert the given text to Katakana format.

        Args:
            text (str): The input text to be converted.

        Returns:
            str: The converted text in Katakana.
        """
        return text

    @parse_text
    def to_roman(self, text: str) -> str:
        """
        Convert Katakana characters in the given text to their Romanized (Romaji) equivalents.

        Args:
            text (str): The input text containing Katakana characters.

        Returns:
            str: The Romanized representation of the input text.
        """
        roman_text = ""
        i = 0
        while i < len(text):
            # Check for combined small Katakana to handle contracted sounds (拗音)
            if (
                i + 1 < len(text)
                and text[i] in self.kana["full_katakana"]
                and text[i + 1] in self.kana["small_katakana"]
            ):
                combined = text[i] + text[i + 1]
                if combined in self.kana["katakana2roman"]:
                    roman_text += self.kana["katakana2roman"][combined]
                    i += 2  # Consume two characters for contracted sounds
                    continue

            # Process normal Katakana characters
            char = text[i]

            if "ァ" <= char <= "ン" or "、" <= char <= "ー":
                roman_text += self.kana["katakana2roman"].get(char, "")
            else:
                roman_text += char
            i += 1
        return roman_text
