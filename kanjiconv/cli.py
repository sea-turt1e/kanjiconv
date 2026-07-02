#!/usr/bin/env python3

from __future__ import annotations
import argparse
from importlib.metadata import PackageNotFoundError, version

from .kanjiconv import KanjiConv


def get_version() -> str:
    try:
        return version("kanjiconv")
    except PackageNotFoundError:
        return "0.0.0"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kanjiconv",
        description="Convert Japanese text containing kanji to hiragana, katakana, or romaji.",
    )
    parser.add_argument(
        "text",
        nargs="+",
        help="The Japanese sentence to convert.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["roman", "hiragana", "katakana"],
        default="roman",
        help="Conversion mode. Default is roman.",
    )
    parser.add_argument(
        "-s",
        "--separator",
        default=" ",
        help="Separator inserted between token readings. Default is a single space.",
    )
    parser.add_argument(
        "--use-unidic",
        action="store_true",
        help="Use UniDic as a fallback for readings when available.",
    )
    parser.add_argument(
        "--no-custom-readings",
        action="store_true",
        help="Disable custom reading fallback.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=get_version(),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)
    text = " ".join(args.text)

    converter = KanjiConv(
        separator=args.separator,
        use_custom_readings=not args.no_custom_readings,
        use_unidic=args.use_unidic,
    )

    if args.mode == "hiragana":
        result = converter.to_hiragana(text)
    elif args.mode == "katakana":
        result = converter.to_katakana(text)
    else:
        result = converter.to_roman(text)

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
)
