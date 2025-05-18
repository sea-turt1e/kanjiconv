from unittest.mock import patch

import pytest

from kanjiconv.entities import SudachiDictType
from kanjiconv.kanjiconv import KanjiConv


class MockToken:
    def __init__(self, reading, surface=None):
        self._reading = reading
        self._surface = surface if surface is not None else reading

    def reading_form(self):
        return self._reading

    def surface(self):
        return self._surface


@patch("os.path.isfile", return_value=True)
@patch("sudachipy.Dictionary")
def test_to_hiragana(mock_dictionary, mock_isfile):
    # Set up mocked dictionary
    mock_tokenizer = mock_dictionary.return_value.create.return_value
    mock_tokenizer.tokenize.return_value = [
        MockToken("ユウユウハクショ", "幽☆遊☆白書"),
        MockToken("ハ", "は"),
        MockToken("、", "、"),
        MockToken("サイコウ", "最高"),
        MockToken("ノ", "の"),
        MockToken("マンガ", "漫画"),
        MockToken("デス", "ﾃﾞｽ"),
        MockToken("。", "。"),
    ]
    kanji_conv = KanjiConv(sudachi_dict_type=SudachiDictType.FULL.value, separator="/")
    result = kanji_conv.to_hiragana("幽☆遊☆白書は、最高の漫画ﾃﾞｽ。")
    assert result == "ゆうゆうはくしょ/は/、/さいこう/の/まんが/です/。"


@patch("os.path.isfile", return_value=True)
@patch("sudachipy.Dictionary")
def test_to_katakana(mock_dictionary, mock_isfile):
    # Set up mocked dictionary
    mock_tokenizer = mock_dictionary.return_value.create.return_value
    mock_tokenizer.tokenize.return_value = [
        MockToken("ユウユウハクショ", "幽☆遊☆白書"),
        MockToken("ハ", "は"),
        MockToken("、", "、"),
        MockToken("サイコウ", "最高"),
        MockToken("ノ", "の"),
        MockToken("マンガ", "漫画"),
        MockToken("デス", "ﾃﾞｽ"),
        MockToken("。", "。"),
    ]

    kanji_conv = KanjiConv(sudachi_dict_type=SudachiDictType.FULL.value, separator="/")
    result = kanji_conv.to_katakana("幽☆遊☆白書は、最高の漫画ﾃﾞｽ。")
    assert result == "ユウユウハクショ/ハ/、/サイコウ/ノ/マンガ/デス/。"


@patch("os.path.isfile", return_value=True)
@patch("sudachipy.Dictionary")
def test_to_roman(mock_dictionary, mock_isfile):
    # Set up mocked dictionary
    mock_tokenizer = mock_dictionary.return_value.create.return_value
    mock_tokenizer.tokenize.return_value = [
        MockToken("ユウユウハクショ", "幽☆遊☆白書"),
        MockToken("ハ", "は"),
        MockToken("、", "、"),
        MockToken("サイコウ", "最高"),
        MockToken("ノ", "の"),
        MockToken("マンガ", "漫画"),
        MockToken("デス", "ﾃﾞｽ"),
        MockToken("。", "。"),
    ]

    kanji_conv = KanjiConv(sudachi_dict_type=SudachiDictType.FULL.value, separator="/")
    result = kanji_conv.to_roman("幽☆遊☆白書は、最高の漫画ﾃﾞｽ。")
    assert result == "yuuyuuhakusho/ha/, /saikou/no/manga/desu/. "


@patch("os.path.isfile", return_value=True)
@patch("sudachipy.Dictionary")
def test_custom_kanji_readings(mock_dictionary, mock_isfile):
    """Test for custom kanji reading dictionary functionality"""
    # Set up mocked dictionary
    mock_tokenizer = mock_dictionary.return_value.create.return_value

    # Assuming '激' cannot be read correctly by Sudachi
    mock_tokenizer.tokenize.return_value = [
        MockToken("", "激"),  # Case when reading is not available
        MockToken("ヲ", "を"),
        MockToken("トバス", "飛ばす"),
    ]

    # Set up custom reading dictionary for testing
    kanji_conv = KanjiConv(sudachi_dict_type=SudachiDictType.FULL.value, separator="/")
    kanji_conv.custom_readings = {
        "single": {"激": ["ゲキ"]},
        "compound": {"激を飛ばす": "ゲキヲトバス"},
    }

    # Test for single kanji
    result = kanji_conv.to_hiragana("激を飛ばす")
    assert result == "げき/を/とばす"

    # Test for compound expression
    kanji_conv.use_custom_readings = True
    result = kanji_conv.to_hiragana("激を飛ばす")
    assert result == "げき/を/とばす"


@patch("os.path.isfile", return_value=True)
@patch("sudachipy.Dictionary")
@patch("fugashi.Tagger")
@patch("kanjiconv.kanjiconv.UNIDIC_AVAILABLE", True)
@patch("unidic.DICDIR")
def test_with_unidic(mock_unidic_find, mock_fugashi_tagger, mock_dictionary, mock_isfile):
    import unidic

    mock_unidic_find.return_value = unidic.DICDIR

    # Mock Fugashi Tagger
    class MockUnidicFeature:
        def __init__(self, kana):
            self.kana = kana

    class MockUnidicNode:
        def __init__(self, surface, kana):
            self.surface = surface
            self.feature = MockUnidicFeature(kana)

    mock_unidic_node = MockUnidicNode("激", "ゲキ")
    mock_tagger_instance = mock_fugashi_tagger.return_value
    mock_tagger_instance.side_effect = lambda text: [mock_unidic_node]

    # Mock Sudachi failing to get reading
    mock_tokenizer = mock_dictionary.return_value.create.return_value

    # Configure token that can't be read
    mock_tokenizer.tokenize.return_value = [
        MockToken("", "激"),  # Case when reading is not available
    ]

    # Test using UniDic
    kanji_conv = KanjiConv(
        sudachi_dict_type=SudachiDictType.FULL.value,
        separator="/",
        use_custom_readings=False,
        use_unidic=True,
    )

    result = kanji_conv.to_hiragana("激")
    assert result == "げき"

    result = kanji_conv.to_katakana("激")
    assert result == "ゲキ"

    result = kanji_conv.to_roman("激")
    assert result == "geki"


if __name__ == "__main__":
    pytest.main()
