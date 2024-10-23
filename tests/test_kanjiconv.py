from unittest.mock import patch

import pytest

from kanjiconv.entities import SudachiDictType
from kanjiconv.kanjiconv import KanjiConv


class MockToken:
    def __init__(self, reading):
        self._reading = reading

    def reading_form(self):
        return self._reading


@patch("os.path.isfile", return_value=True)
@patch("sudachipy.Dictionary")
def test_to_hiragana(mock_dictionary, mock_isfile):
    # モックされた辞書を返すように設定
    mock_tokenizer = mock_dictionary.return_value.create.return_value
    mock_tokenizer.tokenize.return_value = [
        MockToken("ユウユウハクショ"),
        MockToken("ハ"),
        MockToken("、"),
        MockToken("サイコウ"),
        MockToken("ノ"),
        MockToken("マンガ"),
        MockToken("デス"),
        MockToken("。"),
    ]
    kanji_conv = KanjiConv(sudachi_dict_type=SudachiDictType.FULL.value, separator="/")
    result = kanji_conv.to_hiragana("幽☆遊☆白書は、最高の漫画ﾃﾞｽ。")
    assert result == "ゆうゆうはくしょ/は/、/さいこう/の/まんが/です/。"


@patch("os.path.isfile", return_value=True)
@patch("sudachipy.Dictionary")
def test_to_katakana(mock_dictionary, mock_isfile):
    # モックされた辞書を返すように設定
    mock_tokenizer = mock_dictionary.return_value.create.return_value
    mock_tokenizer.tokenize.return_value = [
        MockToken("ユウユウハクショ"),
        MockToken("ハ"),
        MockToken("、"),
        MockToken("サイコウ"),
        MockToken("ノ"),
        MockToken("マンガ"),
        MockToken("デス"),
        MockToken("。"),
    ]

    kanji_conv = KanjiConv(sudachi_dict_type=SudachiDictType.FULL.value, separator="/")
    result = kanji_conv.to_katakana("幽☆遊☆白書は、最高の漫画ﾃﾞｽ。")
    assert result == "ユウユウハクショ/ハ/、/サイコウ/ノ/マンガ/デス/。"


@patch("os.path.isfile", return_value=True)
@patch("sudachipy.Dictionary")
def test_to_roman(mock_dictionary, mock_isfile):
    # モックされた辞書を返すように設定
    mock_tokenizer = mock_dictionary.return_value.create.return_value
    mock_tokenizer.tokenize.return_value = [
        MockToken("ユウユウハクショ"),
        MockToken("ハ"),
        MockToken("、"),
        MockToken("サイコウ"),
        MockToken("ノ"),
        MockToken("マンガ"),
        MockToken("デス"),
        MockToken("。"),
    ]

    kanji_conv = KanjiConv(sudachi_dict_type=SudachiDictType.FULL.value, separator="/")
    result = kanji_conv.to_roman("幽☆遊☆白書は、最高の漫画ﾃﾞｽ。")
    assert result == "yuuyuuhakusho/ha/, /saikou/no/manga/desu/. "


if __name__ == "__main__":
    pytest.main()
