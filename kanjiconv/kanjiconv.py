import json
import os

import sudachipy

from kanjiconv.entities import SudachiDictType


def parse_text(func):
    def wrapper(self, text):
        tokens = self.tokenizer.tokenize(text)
        readings = self.separator.join([token.reading_form() for token in tokens])
        return func(self, readings)

    return wrapper


class KanjiConv:
    def __init__(
        self,
        sudachi_dict_type: SudachiDictType = SudachiDictType.FULL,
        data_path="kanjiconv/data/kana.json",
        separator: str = " ",
    ):
        assert os.path.isfile(data_path), "File does not exist"
        with open(data_path, "r") as f:
            self.kana = json.load(f)
            assert isinstance(self.kana, dict), "JSON must be a dictionary"
        sudachi_dict = sudachipy.Dictionary(dict=sudachi_dict_type.value)
        self.tokenizer = sudachi_dict.create()
        self.separator = separator

    @parse_text
    def to_hiragana(self, text: str) -> str:
        hiragana_text = ""
        for char in text:
            if "ァ" <= char <= "ン":
                hiragana_text += chr(ord(char) - 0x60)
            else:
                hiragana_text += char
        return hiragana_text

    @parse_text
    def to_katakana(self, text: str) -> str:
        return text

    @parse_text
    def to_roman(self, text: str) -> str:
        roman_text = ""
        i = 0
        while i < len(text):
            # 2文字を取り出して拗音をチェック
            if (
                i + 1 < len(text)
                and text[i] in self.kana["full_katakana"]
                and text[i + 1] in self.kana["small_katakana"]
            ):
                combined = text[i] + text[i + 1]
                if combined in self.kana["katakana2roman"]:
                    roman_text += self.kana["katakana2roman"][combined]
                    i += 2  # 拗音の場合は2文字を消費
                    continue

            # 通常のカタカナの処理
            char = text[i]

            if "ァ" <= char <= "ン" or "、" <= char <= "ー":
                roman_text += self.kana["katakana2roman"].get(char, "")
            else:
                roman_text += char
            i += 1
        return roman_text


if __name__ == "__main__":
    kanji_conv = KanjiConv(separator="/")
    text = "幽☆遊☆白書は、最高の漫画デス。"
    print(kanji_conv.to_hiragana(text))
    print(kanji_conv.to_katakana(text))
    print(kanji_conv.to_roman(text))
