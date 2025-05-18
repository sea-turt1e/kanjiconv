import importlib
import importlib.resources
import json
from typing import Callable

import sudachipy

try:
    import fugashi
    import unidic

    UNIDIC_AVAILABLE = True
except ImportError:
    UNIDIC_AVAILABLE = False

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
        # Try custom compound conversion
        if hasattr(self, "custom_readings") and self.use_custom_readings:
            for compound, reading in self.custom_readings.get("compound", {}).items():
                if compound in text:
                    text = text.replace(compound, reading)

        # Tokenize using Sudachi and get readings
        tokens = self.tokenizer.tokenize(text)
        readings = []

        # Process each token
        for token in tokens:
            if token.surface().startswith("[") and token.surface().endswith("]"):
                # Process custom readings in brackets
                readings.append(token.surface()[1:-1])  # Remove brackets
                continue

            reading = token.reading_form()

            # If reading is not available, use UniDic
            has_no_reading = not reading or reading == token.surface()
            if has_no_reading and hasattr(self, "use_unidic") and self.use_unidic and self.unidic_tagger:
                try:
                    surface = token.surface()
                    # Run morphological analysis with UniDic
                    unidic_nodes = self.unidic_tagger(surface)
                    if unidic_nodes:
                        # Extract readings from UniDic
                        unidic_readings = []
                        for node in unidic_nodes:
                            if hasattr(node.feature, "kana") and node.feature.kana:
                                unidic_readings.append(node.feature.kana)
                        if unidic_readings:
                            reading = "".join(unidic_readings)
                except Exception:
                    # Ignore errors with UniDic and continue
                    pass

            # If still no reading is available, use custom dictionary
            has_no_reading = not reading or reading == token.surface()
            if has_no_reading and hasattr(self, "custom_readings") and self.use_custom_readings:
                surface = token.surface()
                if surface in self.custom_readings.get("single", {}):
                    reading = self.custom_readings["single"][surface][0]

            readings.append(reading if reading else token.surface())

        # Join with separator
        joined_readings = self.separator.join(readings)
        return func(self, joined_readings)

    return wrapper


class KanjiConv:
    """
    Class for converting Japanese text between different formats such as Hiragana, Katakana, and Roman characters.

    This class uses multiple dictionaries to convert kanji readings:
    1. SudachiPy: Used as the main dictionary
    2. UniDic: Used as a fallback when SudachiPy cannot resolve readings (optional)
    3. Custom dictionary: Used as a fallback when both SudachiPy and UniDic fail
    """

    def __init__(
        self,
        sudachi_dict_type: SudachiDictType = SudachiDictType.FULL.value,
        separator: str = " ",
        use_custom_readings: bool = True,
        use_unidic: bool = False,
    ) -> None:
        """
        Initializes the KanjiConv instance with a tokenizer and kana conversion data.

        Args:
            sudachi_dict_type (SudachiDictType): Type of the Sudachi dictionary to use for tokenization.
            separator (str): Separator to use between token readings.
            use_custom_readings (bool): Whether to use custom readings dictionary as fallback.
            use_unidic (bool): Whether to use UniDic for additional readings.
        """
        # Load the kana.json file from the package.
        kana_path = importlib.resources.files("kanjiconv.data").joinpath("kana.json")
        with kana_path.open("r", encoding="utf-8") as f:
            self.kana = json.load(f)

        # Load custom kanji readings
        try:
            readings_path = importlib.resources.files("kanjiconv.data").joinpath("kanji_readings.json")
            with readings_path.open("r", encoding="utf-8") as f:
                self.custom_readings = json.load(f)
        except (FileNotFoundError, KeyError):
            self.custom_readings = {"single": {}, "compound": {}}

        # Initialize Sudachi tokenizer
        sudachi_dict = sudachipy.Dictionary(dict=sudachi_dict_type)
        self.tokenizer = sudachi_dict.create()
        self.separator = separator
        self.use_custom_readings = use_custom_readings

        # Initialize UniDic if enabled
        self.use_unidic = use_unidic and UNIDIC_AVAILABLE
        self.unidic_tagger = None
        if self.use_unidic:
            try:
                unidic_dict_path = unidic.DICDIR
                self.unidic_tagger = fugashi.Tagger(unidic_dict_path)
            except Exception as e:
                print(f"UniDic initialization failed: {e}")
                self.use_unidic = False

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
