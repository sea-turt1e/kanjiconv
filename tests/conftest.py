"""Test configuration for kanjiconv.

Provides lightweight stubs for optional third-party dependencies so that
unit tests can run without downloading large external dictionaries.
"""
from __future__ import annotations

import sys
import types


def _install_stub(module_name: str, stub: types.ModuleType) -> None:
    """Register a stub module if the real dependency is not installed."""
    if module_name not in sys.modules:
        sys.modules[module_name] = stub


# Stub for sudachipy -------------------------------------------------------
_sudachipy_stub = types.ModuleType("sudachipy")


class _StubSudachiDictionary:  # pragma: no cover - simple holder
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def create(self):  # pragma: no cover - patched in tests
        raise RuntimeError(
            "sudachipy.Dictionary stub used without patching; tests should patch this class."
        )


_sudachipy_stub.Dictionary = _StubSudachiDictionary
_install_stub("sudachipy", _sudachipy_stub)


# Stub for fugashi ---------------------------------------------------------
_fugashi_stub = types.ModuleType("fugashi")


class _StubTagger:  # pragma: no cover - safety fallback
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, text):
        return []


_fugashi_stub.Tagger = _StubTagger
_install_stub("fugashi", _fugashi_stub)


# Stub for unidic ----------------------------------------------------------
_unidic_stub = types.ModuleType("unidic")
_unidic_stub.DICDIR = "/usr/share/unidic"
_install_stub("unidic", _unidic_stub)
