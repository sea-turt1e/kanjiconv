# kanjiconv
Japanese REAMED is here.  
https://github.com/morikatron/kanjiconv/blob/main/README_ja.md

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
### Import
```python
>>> from kanjiconv import kanjiconv
```

### Parse Sentence
```python
>>> sentence = "幽☆遊☆白書は最高の漫画です"
>>> parsed_list = kanjiconv.get_parsed_list(sentence)
```

### Get Reading
```python
# convert to hiragana
>>> hiragana_sentence = kanjiconv.get_hiragana_sentence(parsed_list)
>>> print(hiragana_sentence)
ゆうゆうはくしょはさいこうのまんがです

# convert to katakana
>>> katakana_sentence = kanjiconv.get_katakana_sentence(parsed_list)
>>> print(katakana_sentence)
ユウユウハクショハサイコウノマンガデス

# convert to Latin alphabet
>>> roma_sentence = kanjiconv.get_roma_sentence(parsed_list)
>>> print(roma_sentence)
yuuyuuhakushohasaikounomangadesu
```

### Get Pronunciation
```python
# convert to hiragana
>>> hiragana_sentence = kanjiconv.get_hiragana_sentence(parsed_list, is_hatsuon=True)
>>> print(hiragana_sentence)
ゆーゆーはくしょわさいこーのまんがです

# convert to katakana
>>> katakana_sentence = kanjiconv.get_katakana_sentence(parsed_list, is_hatsuon=True)
>>> print(katakana_sentence)
ユーユーハクショワサイコーノマンガデス

# convert to Latin alphabet
>>> roma_sentence = kanjiconv.get_roma_sentence(parsed_list, is_hatsuon=True)
>>> print(roma_sentence)
yuｰyuｰhakushowasaikoｰnomangadesu
```


## Licenses
- [kanjiconv](https://github.com/morikatron/kanjiconv/blob/main/LICENSE): Apache License 2.0
- [SudachiPy]
