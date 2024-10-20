# kanjiconv
Japanese REAMED is here.  （日本語のREADMEはこちらです。）
https://github.com/sea_turt1e/kanjiconv/blob/main/README_ja.md

Kanji Converter to Hiragana, Katakana, Latin alphabet.  

You can get the reading and pronunciation of Japanese sentences based on sudachidict.  

## Test Environments
```
macOS Sonoma 14.5
python==3.11.7
```

## Install
### Install kanjiconv
```bash
pip install kanjiconv
```

### Install sudachidict
You can install either sudachidict_full(recomend), sudachidict_core, sudachidict_small.
- If you want detailed readings, I recommend using sudachidict_full.
- If you prioritize lighter operation, then sudachidict_small is the way to go.
- sudachidict_core offers a balance between the operation speed and accuracy of sudachidict_full and sudachidict_small.
```bash
pip install sudachidict_full
pip install sudachidict_small
pip install sudachidict_core
```

## How to use
### Import & Create Instance
```python
>>> from kanjiconv import KanjiConv
>>> kanji_conv = KanjiConv(separator="/")
```

### Get Reading
```python
# convert to hiragana
>>> text = "幽☆遊☆白書は、最高の漫画デス。"
>>> print(kanji_conv.to_hiragana(text))
ゆうゆうはくしょ/は/、/さいこう/の/まんが/です/。

# convert to katakana
>>> text = "幽☆遊☆白書は、最高の漫画デス。"
>>> print(kanji_conv.to_katakana(text))
ユウユウハクショ/ハ/、/サイコウ/ノ/マンガ/デス/。

# convert to Latin alphabet
>>> text = "幽☆遊☆白書は、最高の漫画デス。"
>>> print(kanji_conv.to_roman(text))
yuuyuuhakusho/ha/, /saikou/no/manga/desu/. 

# You can change separator to another character or None
>>> kanji_conv = KanjiConv(separator="_")
>>> print(kanji_conv.to_hiragana(text))
ゆうゆうはくしょ_は_、_さいこう_の_まんが_です_。

>>> kanji_conv = KanjiConv(separator="")
>>> print(kanji_conv.to_hiragana(text))
ゆうゆうはくしょは、さいこうのまんがです。
```

## Update Dict
kanjiconv reading function is based on SudachiDict, and you need to update SudachiDict regularly via pip.
```bash
pip install -U sudachidict_full
pip install -U sudachidict_small
pip install -U sudachidict_core
```

## Licenses
- [kanjiconv](https://github.com/morikatron/kanjiconv/blob/main/LICENSE): Apache License 2.0
- [SudachiPy](https://github.com/WorksApplications/SudachiPy/blob/develop/LICENSE): Apache License 2.0
- [SudachiDict](https://github.com/WorksApplications/SudachiDict/blob/develop/LICENSE-2.0.txt):  Apache License 2.0
