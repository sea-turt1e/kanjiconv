import warnings

import pytest

from kanjiconv._security import SUPPRESS_ENV_VAR, InsecurePythonWarning, check_python_version


@pytest.mark.parametrize(
    "version_info",
    [(3, 13, 17), (3, 13, 18), (3, 14, 9), (3, 14, 10), (3, 15, 1), (3, 15, 2)],
)
def test_patched_versions_do_not_warn(version_info) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert check_python_version(version_info) is True


@pytest.mark.parametrize(
    "version_info",
    [(3, 10, 19), (3, 11, 14), (3, 12, 12), (3, 13, 16), (3, 14, 8), (3, 15, 0)],
)
def test_unpatched_versions_warn(version_info, monkeypatch) -> None:
    monkeypatch.delenv(SUPPRESS_ENV_VAR, raising=False)
    with pytest.warns(InsecurePythonWarning, match="eMudhra"):
        assert check_python_version(version_info) is False


def test_warning_can_be_suppressed(monkeypatch) -> None:
    monkeypatch.setenv(SUPPRESS_ENV_VAR, "1")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert check_python_version((3, 12, 12)) is False
