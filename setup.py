#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

if __name__ == "__main__":
    setup(
        name="kanjiconv",
        entry_points={
            "console_scripts": ["kanjiconv-post-install=kanjiconv.post_install:main"],
        },
    )
