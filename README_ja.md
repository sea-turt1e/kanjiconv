# kanjiconv
English README is here. （英語のREADMEはこちらです。）  
https://github.com/sea-turt1e/kanjiconv/blob/main/README.md

漢字をひらがな、カタカナ、ローマ字に変換するツールです。  
sudachidictをベースに、日本語の文の読みや発音を取得することができます。

## 環境
```
macOS Sonoma 14.5
python==3.11.7
```

## インストール
### kanjiconvのインストール
```bash
pip install kanjiconv
```

### sudachidictのインストール
sudachidict_full（推奨）、sudachidict_core、sudachidict_smallのいずれかをインストールできます。
- 詳細な読みが必要な場合は、sudachidict_fullの使用をお勧めします。
- 軽量な動作を優先する場合は、sudachidict_smallがお勧めです。
- sudachidict_coreは、動作速度と精度のバランスを取った選択肢です。
```bash
pip install sudachidict_full
pip install sudachidict_small
pip install sudachidict_core
```

## 使用方法
### インポートとインスタンスの生成
```python
>>> from kanjiconv import KanjiConv
>>> kanji_conv = KanjiConv(separator="/")
```

### 読みの取得
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

## 辞書の更新
kanjiconvの読み取り機能はSudachiDictに基づいており、pipを使って定期的にSudachiDictを更新する必要があります。
```bash
pip install -U sudachidict_full
pip install -U sudachidict_small
pip install -U sudachidict_core
```

## ライセンス
## ライセンス

本プロジェクトは[Apache License 2.0](LICENSE)の下でライセンスされています。

### 使用しているオープンソースソフトウェア

- [SudachiPy](https://github.com/WorksApplications/SudachiPy): Apache License 2.0
- [SudachiDict](https://github.com/WorksApplications/SudachiDict): Apache License 2.0

本ライブラリは形態素解析にSudachiPyとその辞書であるSudachiDictを使用しています。これらもApache License 2.0の下で配布されています。

詳細なライセンス情報については、各プロジェクトのLICENSEファイルをご確認ください。

- [SudachiPyのLICENSE](https://github.com/WorksApplications/SudachiPy/blob/develop/LICENSE)
- [SudachiDictのLICENSE](https://github.com/WorksApplications/SudachiDict/blob/develop/LICENSE-2.0.txt)
