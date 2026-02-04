import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sandhi import PARSER_AVAILABLE, from_slp1, join_sandhi, split_sandhi_parser


def test_join_preserves_hk_output_scheme():
    assert join_sandhi("deva", "Alaya") == "devAlaya"


def test_from_slp1_respects_target_scheme():
    assert from_slp1("rAmaH", "hk") == "rAmaH"


@pytest.mark.skipif(not PARSER_AVAILABLE, reason="sanskrit_parser not installed")
def test_split_parser_no_result_returns_empty_list():
    assert split_sandhi_parser("qqqqq") == []
