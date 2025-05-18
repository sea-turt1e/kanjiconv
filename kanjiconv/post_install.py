#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys


def download_unidic():
    """UniDic辞書をダウンロードします。"""
    print("UniDicの辞書をダウンロードしています...")
    try:
        subprocess.check_call([sys.executable, "-m", "unidic", "download"])
        print("UniDic辞書のダウンロードが完了しました。")
    except Exception as e:
        print(f"警告: UniDic辞書のダウンロード中にエラーが発生しました: {e}")
        print("必要に応じて手動で `python -m unidic download` を実行してください。")


def main():
    """インストール後のセットアップを実行します。"""
    download_unidic()


if __name__ == "__main__":
    main()
