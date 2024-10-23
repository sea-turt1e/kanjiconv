# kanjiconv
Japanese REAMED is here.  （日本語のREADMEはこちらです。）  
https://github.com/sea-turt1e/kanjiconv/blob/main/README_ja.md

Kanji Converter to Hiragana, Katakana, Roman alphabet.  
You can get the reading and pronunciation of Japanese sentences based on sudachidict.  
Sudachidict is a regularly updated dictionary, so it can relatively handle new proper nouns and other terms.

## Environments
```
macOS Sonoma 14.5
python==3.11.7
```

## Install
### Install kanjiconv
```bash
pip install kanjiconv
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

# convert to Roman alphabet
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

## (Optional) Installing sudachidict other than the default
The default dictionary is sudachidict_full. If you want to use a lighter dictionary, you can install either sudachidict_small or sudachidict_core.
- If you need detailed readings, we recommend using sudachidict_full. The default is set to sudachidict_full.
- If you prefer lighter operation, sudachidict_small is recommended.
- sudachidict_core offers a balanced option between speed and accuracy.
```bash
pip install sudachidict_small
pip install sudachidict_core
```
- If using sudachidict_small or sudachidict_core, specify it like this:
```python
>>> kanji_conv = KanjiConv(sudachi_dict_type="small", separator="/")
>>> kanji_conv = KanjiConv(sudachi_dict_type="core", separator="/")
```

## Update Dict
kanjiconv reading function is based on SudachiDict, and you need to update SudachiDict regularly via pip.
```bash
pip install -U sudachidict_full
pip install -U sudachidict_small
pip install -U sudachidict_core
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).

### Open Source Software Used

- [SudachiPy](https://github.com/WorksApplications/SudachiPy): Apache License 2.0
- [SudachiDict](https://github.com/WorksApplications/SudachiDict): Apache License 2.0

This library uses SudachiPy and its dictionary SudachiDict for morphological analysis. These are also distributed under the Apache License 2.0.

For detailed license information, please refer to the LICENSE files of each project:

- [SudachiPy LICENSE](https://github.com/WorksApplications/SudachiPy/blob/develop/LICENSE)
- [SudachiDict LICENSE](https://github.com/WorksApplications/SudachiDict/blob/develop/LICENSE-2.0.txt)
