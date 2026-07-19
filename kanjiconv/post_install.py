#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helper for the optional `kanjiconv[unidic]` extra: downloads the UniDic dictionary.

Run with: python -m kanjiconv.post_install
"""

import subprocess
import sys


def download_unidic():
    """Download the UniDic dictionary."""
    print("Downloading the UniDic dictionary...")
    try:
        subprocess.check_call([sys.executable, "-m", "unidic", "download"])
        print("UniDic dictionary download complete.")
    except Exception as e:
        print(f"Warning: an error occurred while downloading the UniDic dictionary: {e}")
        print("Please run `python -m unidic download` manually if needed.")


def main():
    """Run post-install setup."""
    download_unidic()


if __name__ == "__main__":
    main()
