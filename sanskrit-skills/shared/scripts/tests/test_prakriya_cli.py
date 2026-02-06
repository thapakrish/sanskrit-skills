import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import prakriya  # noqa: E402


SCRIPT = Path(__file__).resolve().parents[1] / "prakriya.py"


def _run_prakriya(*args):
    env = os.environ.copy()
    env.setdefault("UV_CACHE_DIR", "/tmp/uv-cache")
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def test_requires_subcommand():
    proc = _run_prakriya()
    assert proc.returncode != 0


@pytest.mark.skipif(not prakriya.VIDYUT_AVAILABLE, reason="vidyut not installed")
def test_invalid_lakara_exits_nonzero():
    proc = _run_prakriya("tinanta", "gam", "1", "Kartari", "Prathama", "Eka", "BadLakara")
    assert proc.returncode == 1
    assert "Invalid parameter:" in proc.stdout


@pytest.mark.skipif(not prakriya.VIDYUT_AVAILABLE, reason="vidyut not installed")
def test_iast_dhatu_is_accepted():
    proc = _run_prakriya("tinanta", "bhū", "1", "Kartari", "Prathama", "Eka", "Lat")
    assert proc.returncode == 0
    assert "Result:" in proc.stdout
