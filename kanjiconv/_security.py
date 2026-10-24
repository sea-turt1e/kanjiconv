import os
import sys
import warnings

__all__ = ["InsecurePythonWarning", "check_python_version"]

# First CPython release of each series that ships the fix for the eMudhra / emSign
# intermediate CA key compromise (bundled pip 26.2.2 with certifi 2026.10.19).
# https://emudhra.we-have-a-problem.com/
PATCHED_PYTHON_VERSIONS = {
    (3, 13): (3, 13, 17),
    (3, 14): (3, 14, 9),
    (3, 15): (3, 15, 1),
}

SUPPRESS_ENV_VAR = "KANJICONV_SUPPRESS_PYTHON_WARNING"


class InsecurePythonWarning(UserWarning):
    """Warns that the running Python predates the eMudhra CA fix."""


def _is_patched(version_info) -> bool:
    patched = PATCHED_PYTHON_VERSIONS.get((version_info[0], version_info[1]))
    return patched is not None and tuple(version_info[:3]) >= patched


def check_python_version(version_info=None) -> bool:
    """Warn when the running Python does not include the eMudhra CA fix.

    Returns True when the interpreter is a patched release.
    """
    if version_info is None:
        version_info = sys.version_info
    if _is_patched(version_info):
        return True
    if os.environ.get(SUPPRESS_ENV_VAR):
        return False

    current = ".".join(str(part) for part in version_info[:3])
    recommended = ", ".join(".".join(map(str, v)) for v in PATCHED_PYTHON_VERSIONS.values())
    warnings.warn(
        f"Python {current} does not include the fix for the eMudhra CA certificate "
        f"compromise (https://emudhra.we-have-a-problem.com/). Upgrade to Python "
        f"{recommended} or later in the same series, or at least run "
        f'"pip install -U pip certifi" (pip>=26.2.2, certifi>=2026.10.19). '
        f"Set {SUPPRESS_ENV_VAR}=1 to silence this warning.",
        InsecurePythonWarning,
        stacklevel=3,
    )
    return False
