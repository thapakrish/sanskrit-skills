import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "dhatu.py"


def _run_dhatu(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_gana_non_integer_exits_cleanly():
    proc = _run_dhatu("--gana", "foo")
    assert proc.returncode == 1
    assert "gana must be an integer from 1 to 10" in proc.stdout


def test_gana_out_of_range_exits_cleanly():
    proc = _run_dhatu("--gana", "11")
    assert proc.returncode == 1
    assert "gana must be between 1 and 10" in proc.stdout
