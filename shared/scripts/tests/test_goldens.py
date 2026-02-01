import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from chandas import analyze_verse
from dhatu import lookup_dhatu, list_by_gana, search_by_meaning
from sandhi import join_sandhi, split_sandhi_parser


def _load_json(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("case", _load_json("golden_chandas.json"))
def test_golden_chandas(case):
    result = analyze_verse(case["input"])
    expected = case["expected"]

    first = result["padas"][0]
    if "pattern" in expected:
        assert first["pattern"] == expected["pattern"]
    if "syllables" in expected:
        assert first["syllable_count"] == expected["syllables"]

    if "meter" in expected:
        assert any(m[0] == expected["meter"] for m in result["probable_meters"])


@pytest.mark.parametrize("case", _load_json("golden_sandhi.json"))
def test_golden_sandhi(case):
    if case["type"] == "join":
        out = join_sandhi(case["input"][0], case["input"][1])
        assert out == case["expected"]
    elif case["type"] == "split_parser":
        out = split_sandhi_parser(case["input"])
        assert out is not None
        assert case["expected"] in out
    else:
        raise AssertionError(f"Unknown sandhi golden type: {case['type']}")


@pytest.mark.parametrize("case", _load_json("golden_dhatu.json"))
def test_golden_dhatu(case):
    if case["type"] == "lookup":
        info = lookup_dhatu(case["input"])
        assert info is not None
        for key, value in case["expected"].items():
            if key == "forms":
                for form_key, form_val in value.items():
                    assert info["forms"][form_key] == form_val
            else:
                assert info[key] == value
    elif case["type"] == "list_by_gana_contains":
        dhatus = list_by_gana(case["input"])
        for expected_key in case["expected"]:
            assert expected_key in dhatus
    elif case["type"] == "search_by_meaning_contains":
        results = search_by_meaning(case["input"])
        for expected_key in case["expected"]:
            assert expected_key in results
    else:
        raise AssertionError(f"Unknown dhatu golden type: {case['type']}")
