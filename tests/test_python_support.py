from __future__ import annotations

from pathlib import Path

import pytest
from packaging.specifiers import SpecifierSet
from packaging.version import Version

try:  # Python >= 3.11
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib  # type: ignore[no-redef]


@pytest.mark.parametrize("version", ["3.10", "3.11", "3.12", "3.13"])
def test_supported_python_versions(version: str) -> None:
    """Ensure the advertised Python version range includes the expected interpreters."""
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject_path.open("rb") as fh:
        payload = tomllib.load(fh)

    spec = SpecifierSet(payload["tool"]["poetry"]["dependencies"]["python"])
    assert Version(version) in spec, f"Python {version} is not included in the supported range"
