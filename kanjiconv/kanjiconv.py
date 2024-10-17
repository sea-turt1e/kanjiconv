import json
import os

import ipdb
import sudachipy
from entities import SudachiDictType


def parse_text(func):
    def wrapper(self, text):
        tokens = self.tokenizer.tokenize(text)
        readings = "".join([token.reading_form() for token in tokens])
        return func(self, readings)

    return wrapper


class KanjiConv:
    def __init__(self, sudachi_dict_type: SudachiDictType = SudachiDictType.FULL, data_path="data/kana.json"):
        assert os.path.isfile(data_path), "File does not exist"
        with open(data_path, "r") as f:
            self.kana = json.load(f)
            assert isinstance(self.kana, dict), "JSON must be a dictionary"
        sudachi_dict = sudachipy.Dictionary(dict=sudachi_dict_type.value)
        self.tokenizer = sudachi_dict.create()

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
                if combined in self.kana["katakana"]:
                    roman_text += self.kana["katakana"][combined]
                    i += 2  # 拗音の場合は2文字を消費
                    continue

            # 通常のカタカナの処理
            char = text[i]
            if "ァ" <= char <= "ン":
                roman_text += self.kana["katakana"].get(char, "")
            i += 1

        return roman_text


if __name__ == "__main__":
    kanji_conv = KanjiConv()
    text = "幽☆遊☆白書は最高の漫画ﾃﾞｽ"
    print(kanji_conv.to_hiragana(text))
    print(kanji_conv.to_katakana(text))
    print(kanji_conv.to_roman(text))
