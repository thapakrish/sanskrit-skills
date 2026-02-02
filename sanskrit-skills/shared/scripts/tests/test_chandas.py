import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from chandas import to_slp1, analyze_weights_slp1, analyze_verse


def test_to_slp1_devanagari():
    assert to_slp1("वागर्थाविव") == "vAgarTAviva"


def test_to_slp1_iast():
    assert to_slp1("vāgarthāviva") == "vAgarTAviva"


def test_weights_slp1_long_vowel():
    pattern, count = analyze_weights_slp1("A")
    assert pattern == "G"
    assert count == 1


def test_anushtup_detection():
    result = analyze_verse("a a a a a a a a")
    assert result["padas"][0]["syllable_count"] == 8
    assert any(m[0] == "anuṣṭup" for m in result["probable_meters"])


def test_upajati_not_auto_added():
    result = analyze_verse("a a a a a a a a a a a")
    assert not any(m[0] == "upajāti" for m in result["probable_meters"])
