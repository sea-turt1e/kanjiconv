# kanjiconv
![Python](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI Downloads](https://static.pepy.tech/badge/kanjiconv)](https://pepy.tech/projects/kanjiconv)

Japanese REAMED is here.  （日本語のREADMEはこちらです。）  
https://github.com/sea-turt1e/kanjiconv/blob/main/README_ja.md

![kanjiconv](images/kanjiconv.png)

Kanji Converter to Hiragana, Katakana, Roman alphabet.  
You can get the reading and pronunciation of Japanese sentences based on sudachidict.  
Sudachidict is a regularly updated dictionary, so it can relatively handle new proper nouns and other terms.

## Environment
```
3.10 <= Python <= 3.13
```

## Install
### Install kanjiconv
```bash
pip install kanjiconv
```

`fugashi`/`unidic` are not installed by default. If you want to use the UniDic dictionary
with the `use_unidic` option, install the optional extra and download the dictionary:

```bash
pip install "kanjiconv[unidic]"
python -m unidic download
```

Passing `use_unidic=True` (or `--use-unidic` on the CLI) without this extra installed
raises `ImportError` with the install instructions above.

## How to use

### CLI usage
After installing kanjiconv, you can use the `kanjiconv` command from your terminal.

```bash
kanjiconv "幽☆遊☆白書は、最高の漫画デス。"
```

By default, the CLI converts text to roman alphabet and inserts a single space between token readings.

```text
yuuyuuhakusho ha ,  saikou no manga desu .
```

Use `-m`/`--mode` to choose the output format:

```bash
# Convert to hiragana
kanjiconv "幽☆遊☆白書は、最高の漫画デス。" --mode hiragana

# Convert to katakana
kanjiconv "幽☆遊☆白書は、最高の漫画デス。" --mode katakana

# Convert to roman alphabet (which is already the default)
kanjiconv "幽☆遊☆白書は、最高の漫画デス。" --mode roman
```

Use `-s`/`--separator` to change the separator inserted between token readings:

```bash
kanjiconv "幽☆遊☆白書は、最高の漫画デス。" --mode hiragana --separator "/"
# ゆうゆうはくしょ/は/、/さいこう/の/まんが/です/。

kanjiconv "幽☆遊☆白書は、最高の漫画デス。" --mode hiragana --separator ""
# ゆうゆうはくしょは、さいこうのまんがです。
```

Additional options:

```bash
# Use UniDic as a fallback for readings when available
kanjiconv "東京に行く" --mode hiragana --use-unidic

# Disable the custom reading fallback
kanjiconv "激を飛ばす" --mode hiragana --no-custom-readings
```

## CLI flags/options

| Option                                   | Description                                                            |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| `-m`/`--mode {roman,hiragana,katakana}`  | Conversion mode. Defaults to `roman`.                                  |
| `-s`/`--separator SEPARATOR`             | Separator inserted between token readings. Defaults to a single space. |
| `--use-unidic`                           | Use UniDic as a fallback for readings when available (requires the `kanjiconv[unidic]` extra). |
| `--no-custom-readings`                   | Disable custom reading fallback.                                       |
| `--split-mode {A,B,C}`                   | Sudachi split granularity. Defaults to `C` (longest units).            |
| `--version`                              | Show the installed version.                                            |
| `-h`/`--help`                            | Show help.                                                             |

### Import & Create Instance
```python
from kanjiconv import KanjiConv

# Basic usage
kanji_conv = KanjiConv(separator="/")

# Using UniDic for improved kanji reading accuracy
# (requires `pip install "kanjiconv[unidic]"` and `python -m unidic download`,
# otherwise raises ImportError)
kanji_conv = KanjiConv(separator="/", use_unidic=True)

# Using custom dictionary for kanji readings not covered by SudachiDict or UniDic
kanji_conv = KanjiConv(separator="/", use_custom_readings=True)
```

### Get Reading
```python
# convert to hiragana
text = "幽☆遊☆白書は、最高の漫画デス。"
print(kanji_conv.to_hiragana(text))
ゆうゆうはくしょ/は/、/さいこう/の/まんが/です/。

# convert to katakana
text = "幽☆遊☆白書は、最高の漫画デス。"
print(kanji_conv.to_katakana(text))
ユウユウハクショ/ハ/、/サイコウ/ノ/マンガ/デス/。

# convert to Roman alphabet
text = "幽☆遊☆白書は、最高の漫画デス。"
print(kanji_conv.to_roman(text))
yuuyuuhakusho/ha/, /saikou/no/manga/desu/. 

# You can change separator to another character or None
kanji_conv = KanjiConv(separator="_")
print(kanji_conv.to_hiragana(text))
ゆうゆうはくしょ_は_、_さいこう_の_まんが_です_。

kanji_conv = KanjiConv(separator="")
print(kanji_conv.to_hiragana(text))
ゆうゆうはくしょは、さいこうのまんがです。
```

## Using Custom Kanji Reading Dictionary
KanjiConv supports a custom dictionary for handling special kanji readings that are not properly recognized by SudachiDict or UniDic. This is particularly useful for:

1. Special expressions with unique readings
2. Technical terms or proper nouns
3. Ambiguous kanji with multiple readings based on context

The custom dictionary is automatically loaded from the package if available, but you can also define your own:

```python
from kanjiconv import KanjiConv

# Create instance with custom readings enabled (enabled by default)
kanji_conv = KanjiConv(separator="/", use_custom_readings=True)

# You can also define your own custom readings
kanji_conv.custom_readings = {
    "single": {
        "激": ["げき"],
        "飛": ["と", "ひ"]
    },
    "compound": {
        "激を飛ばす": "げきをとばす",
        "飛ばす": "とばす"
    }
}

# Now the special expression will be properly converted
print(kanji_conv.to_hiragana("激を飛ばす"))
# Output: げき/を/とばす
```

### Custom Dictionary Structure
The custom dictionary uses the following format:

- `single`: A dictionary mapping individual kanji to their reading(s)
  - Each kanji can have multiple readings as a list
  - The first reading in the list is used as default
- `compound`: A dictionary mapping multi-character expressions to their reading
  - These are processed before tokenization and given priority

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
kanji_conv = KanjiConv(sudachi_dict_type="small", separator="/")
kanji_conv = KanjiConv(sudachi_dict_type="core", separator="/")
```

## Update Dict
kanjiconv reading function is based on SudachiDict, and you need to update SudachiDict regularly via pip.
```bash
pip install -U sudachidict_full
pip install -U sudachidict_small
pip install -U sudachidict_core
```

## Local MCP Server
If you want to use kanjiconv as a local MCP Server, see [kanjicon-mcp](https://github.com/sea-turt1e/kanjiconv_mcp)


## License

This project is licensed under the [Apache License 2.0](LICENSE).

### Open Source Software Used

- [SudachiPy](https://github.com/WorksApplications/SudachiPy): Apache License 2.0
- [SudachiDict](https://github.com/WorksApplications/SudachiDict): Apache License 2.0
- [fugashi](https://github.com/polm/fugashi): MIT License
- [unidic-py](https://github.com/polm/unidic-py): MIT License

This library uses SudachiPy and its dictionary SudachiDict for morphological analysis. These are also distributed under the Apache License 2.0.

For detailed license information, please refer to the LICENSE files of each project:

- [SudachiPy LICENSE](https://github.com/WorksApplications/SudachiPy/blob/develop/LICENSE)
- [SudachiDict LICENSE](https://github.com/WorksApplications/SudachiDict/blob/develop/LICENSE-2.0.txt)
- [fugashi LICENSE](https://github.com/polm/fugashi/blob/main/LICENSE)
- [unidic-py LICENSE](https://github.com/polm/unidic-py/blob/master/LICENSE)
