# kanjiconv
![Python](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI Downloads](https://static.pepy.tech/badge/kanjiconv)](https://pepy.tech/projects/kanjiconv)

English README is here. （英語のREADMEはこちらです。）  
https://github.com/sea-turt1e/kanjiconv/blob/main/README.md

![kanjiconv](images/kanjiconv.png)

漢字をひらがな、カタカナ、ローマ字に変換するツールです。  
sudachidictをベースに、日本語の文の読みや発音を取得することができます。  
sudachidictは定期的に更新される辞書なので、新しい固有名詞等にも比較的対応できます。

## ローカルMCPサーバー
ローカル環境でkanjiconvをMCPサーバーとして使用したい場合は、[kanjicon-mcp](https://github.com/sea-turt1e/kanjiconv_mcp)を参照してください。  

## 環境
```
python>=3.11.7
```

## インストール
### kanjiconvのインストール
```bash
pip install kanjiconv
```

use_unidicオプションでUniDic辞書を使用する場合、unidic辞書をダウンロードしてください。

```bash
python -m unidic download
```

## 使用方法
### インポートとインスタンスの生成
```python
from kanjiconv import KanjiConv

# 基本的な使い方
kanji_conv = KanjiConv(separator="/")

# UniDicを使用する場合（漢字読みの精度向上）
kanji_conv = KanjiConv(separator="/", use_unidic=True)

# カスタム辞書を使用する場合（SudachiDictやUniDicでカバーされない漢字の読み）
kanji_conv = KanjiConv(separator="/", use_custom_readings=True)
```

### 読みの取得
```python
# ひらがなへの変換
text = "幽☆遊☆白書は、最高の漫画デス。"
print(kanji_conv.to_hiragana(text))
ゆうゆうはくしょ/は/、/さいこう/の/まんが/です/。

# カタカナへの変換
text = "幽☆遊☆白書は、最高の漫画デス。"
print(kanji_conv.to_katakana(text))
ユウユウハクショ/ハ/、/サイコウ/ノ/マンガ/デス/。

# ローマ字への変換
text = "幽☆遊☆白書は、最高の漫画デス。"
print(kanji_conv.to_roman(text))
yuuyuuhakusho/ha/, /saikou/no/manga/desu/. 

# 区切り文字を変える、区切り文字無し
kanji_conv = KanjiConv(separator="_")
print(kanji_conv.to_hiragana(text))
ゆうゆうはくしょ_は_、_さいこう_の_まんが_です_。

kanji_conv = KanjiConv(separator="")
print(kanji_conv.to_hiragana(text))
ゆうゆうはくしょは、さいこうのまんがです。
```

## カスタム漢字読み辞書の使用方法
KanjiConvは、SudachiDictやUniDicで正しく認識されない特殊な漢字の読みに対応するカスタム辞書をサポートしています。これは以下のような場合に特に有用です：

1. 特殊な表現や独自の読み方
2. 専門用語や固有名詞
3. 文脈によって複数の読み方がある曖昧な漢字

カスタム辞書はパッケージから自動的に読み込まれますが、独自の辞書を定義することもできます：

```python
from kanjiconv import KanjiConv

# カスタム読みを有効にしてインスタンスを作成（デフォルトで有効）
kanji_conv = KanjiConv(separator="/", use_custom_readings=True)

# 独自のカスタム読みを定義
kanji_conv.custom_readings = {
    "single": {
        "激": ["げき"],
        "飛": ["と", "ひ"]
    },
    "compound": {
        "激を飛ばす": "げきをとばす",
        "飛ばす": "とばす",
    }
}

# これで特殊表現が正しく変換されます
print(kanji_conv.to_hiragana("激を飛ばす"))
# 出力: げき/を/とばす
```

### カスタム辞書の構造
カスタム辞書は以下の形式を使用します：

- `single`：個々の漢字とその読み方のマッピング
  - 各漢字はリストとして複数の読み方を持つことができます
  - リストの最初の読みがデフォルトとして使用されます
- `compound`：複数文字の表現とその読み方のマッピング
  - これらはトークン化前に処理され、優先されます

## （オプション）デフォルト以外のsudachidictのインストール
辞書のデフォルトはsudachidict_fullです。軽量な辞書を使用したい場合はsudachidict_small、sudachidict_coreのいずれかをインストールできます。
- 詳細な読みが必要な場合は、sudachidict_fullの使用をお勧めします。デフォルトがsudachidict_fullになっています。
- 軽量な動作を優先する場合は、sudachidict_smallがお勧めです。
- sudachidict_coreは、動作速度と精度のバランスを取った選択肢です。
```bash
pip install sudachidict_small
pip install sudachidict_core
```

- sudachdict_small, sudachidict_coreを使用する場合は指定してください。
```python
kanji_conv = KanjiConv(sudachi_dict_type="small", separator="/")
kanji_conv = KanjiConv(sudachi_dict_type="core", separator="/")
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
- [fugashi](https://github.com/polm/fugashi): MIT License
- [unidic-py](https://github.com/polm/unidic-py): MIT License

本ライブラリは形態素解析にSudachiPyとその辞書であるSudachiDictを使用しています。これらもApache License 2.0の下で配布されています。

詳細なライセンス情報については、各プロジェクトのLICENSEファイルをご確認ください。

- [SudachiPyのLICENSE](https://github.com/WorksApplications/SudachiPy/blob/develop/LICENSE)
- [SudachiDictのLICENSE](https://github.com/WorksApplications/SudachiDict/blob/develop/LICENSE-2.0.txt)
- [fugashiのLICENSE](https://github.com/polm/fugashi/blob/main/LICENSE)
- [unidic-pyのLICENSE](https://github.com/polm/unidic-py/blob/master/LICENSE)
