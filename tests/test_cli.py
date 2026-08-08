#!/usr/bin/env python3

import io
import sys
from unittest.mock import patch

from kanjiconv.cli import create_parser, main


def test_create_parser_defaults() -> None:
    parser = create_parser()
    args = parser.parse_args(["幽☆遊☆白書は、最高の漫画ﾃﾞｽ。"])
    assert args.mode == "roman"
    assert args.separator == " "
    assert args.use_unidic is False
    assert args.no_custom_readings is False
    assert args.text == ["幽☆遊☆白書は、最高の漫画ﾃﾞｽ。"]


@patch("kanjiconv.cli.KanjiConv")
def test_main_uses_to_roman(mock_kanji_conv):
    mock_instance = mock_kanji_conv.return_value
    mock_instance.to_roman.return_value = "yuuyuuhakusho ha, saikou no manga desu."

    stdout = io.StringIO()
    with patch.object(sys, "stdout", stdout):
        result = main(["幽☆遊☆白書は、最高の漫画ﾃﾞｽ。"])

    assert result == 0
    assert stdout.getvalue() == "yuuyuuhakusho ha, saikou no manga desu.\n"
    mock_kanji_conv.assert_called_once_with(
        separator=" ",
        use_custom_readings=True,
        use_unidic=False,
        sudachi_split_mode="C",
    )
    mock_instance.to_roman.assert_called_once_with("幽☆遊☆白書は、最高の漫画ﾃﾞｽ。")


@patch("kanjiconv.cli.KanjiConv")
def test_main_uses_hiragana_mode(mock_kanji_conv):
    mock_instance = mock_kanji_conv.return_value
    mock_instance.to_hiragana.return_value = "ゆうゆうはくしょは、さいこうのまんがです。"

    stdout = io.StringIO()
    with patch.object(sys, "stdout", stdout):
        result = main(["幽☆遊☆白書は、最高の漫画ﾃﾞｽ。", "-m", "hiragana"])

    assert result == 0
    assert stdout.getvalue() == "ゆうゆうはくしょは、さいこうのまんがです。\n"
    mock_instance.to_hiragana.assert_called_once_with("幽☆遊☆白書は、最高の漫画ﾃﾞｽ。")


@patch("kanjiconv.cli.KanjiConv")
def test_main_use_unidic_without_extra_exits_with_hint(mock_kanji_conv):
    mock_kanji_conv.side_effect = ImportError(
        'use_unidic=True requires the optional "unidic" extra. Install it with: '
        'pip install "kanjiconv[unidic]", then run: python -m unidic download'
    )

    stderr = io.StringIO()
    with patch.object(sys, "stderr", stderr):
        result = main(["テスト", "--use-unidic"])

    assert result == 1
    assert "kanjiconv[unidic]" in stderr.getvalue()
