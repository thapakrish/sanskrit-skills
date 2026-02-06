#!/usr/bin/env python3
"""
Sanskrit sandhi analyzer using sanskrit_parser library.
Splits sandhi-joined text and analyzes word boundaries.

Setup:
    uv sync --extra full  # from the scripts directory

Usage:
    python sandhi.py "<text>"              # Split sandhi in text
    python sandhi.py --split "<compound>"  # Split a compound/sentence
    python sandhi.py --join "<w1>" "<w2>"  # Join words with sandhi (basic)

Examples:
    python sandhi.py "rāmāya namaḥ"
    python sandhi.py --split "devālayaḥ"
    python sandhi.py --split "tatraikaḥ"

Note: sanskrit_parser uses lexicon-based analysis for accurate splitting.
For simple rule-based joining, a fallback implementation is provided.
"""

import sys
import logging
import warnings
import io
from contextlib import redirect_stderr


class _DropNoisyRootWarnings(logging.Filter):
    """Drop known optional-dependency warnings emitted on root logger."""

    _NOISY_FRAGMENTS = (
        "gensim and/or sentencepiece not found. Lexical scoring will be disabled",
        "To enable scoring please install gensim and sentencepiece",
    )

    def filter(self, record):
        msg = record.getMessage()
        return not any(fragment in msg for fragment in self._NOISY_FRAGMENTS)


_ROOT_NOISE_FILTER = _DropNoisyRootWarnings()


def _configure_library_output():
    """Silence noisy third-party logs/warnings in normal CLI usage."""
    root_logger = logging.getLogger()
    if not any(isinstance(f, _DropNoisyRootWarnings) for f in root_logger.filters):
        root_logger.addFilter(_ROOT_NOISE_FILTER)
    noisy_loggers = (
        "sanskrit_parser",
        "sanskrit_parser.api",
        "sanskrit_parser.base",
        "sanskrit_parser.base.sanskrit_base",
        "sanskrit_parser.parser",
        "sanskrit_parser.util",
        "sanskrit_parser.util.sanskrit_data_wrapper",
    )
    for name in noisy_loggers:
        logging.getLogger(name).setLevel(logging.WARNING)

    try:
        from sqlalchemy.exc import SAWarning

        warnings.filterwarnings(
            "ignore",
            category=SAWarning,
            module=r"sanskrit_util\.schema",
        )
    except Exception:
        pass


_configure_library_output()


def _emit_filtered_stderr(stderr_text):
    """Re-emit stderr except known optional dependency noise."""
    if not stderr_text:
        return
    for line in stderr_text.splitlines():
        if (
            "gensim and/or sentencepiece not found. Lexical scoring will be disabled" in line
            or "To enable scoring please install gensim and sentencepiece" in line
        ):
            continue
        print(line, file=sys.stderr)

# Try to import sanskrit_parser
PARSER_AVAILABLE = False
try:
    from sanskrit_parser import Parser
    PARSER_AVAILABLE = True
except ImportError:
    pass

# Try indic_transliteration for scheme detection
try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
    from indic_transliteration.detect import detect
    TRANSLITERATION_AVAILABLE = True
except ImportError:
    TRANSLITERATION_AVAILABLE = False


SCHEME_TO_SANSCRIPT = {
    'devanagari': 'DEVANAGARI',
    'iast': 'IAST',
    'slp1': 'SLP1',
    'hk': 'HK',
    'itrans': 'ITRANS',
    'velthuis': 'VELTHUIS',
    'wx': 'WX',
}


def _scheme_const(name):
    if not TRANSLITERATION_AVAILABLE:
        return None
    key = name.lower()
    attr = SCHEME_TO_SANSCRIPT.get(key)
    if not attr or not hasattr(sanscript, attr):
        return None
    return getattr(sanscript, attr)


def detect_scheme(text):
    """Detect transliteration scheme using indic-transliteration."""
    if not TRANSLITERATION_AVAILABLE:
        for char in text:
            if '\u0900' <= char <= '\u097F':
                return 'devanagari'
        return 'iast'

    scheme = detect(text)
    if scheme == sanscript.DEVANAGARI:
        return 'devanagari'
    if scheme == sanscript.SLP1:
        return 'slp1'
    if scheme == sanscript.HK:
        return 'hk'
    if scheme == sanscript.ITRANS:
        return 'itrans'
    if scheme == sanscript.VELTHUIS:
        return 'velthuis'
    if scheme == sanscript.WX:
        return 'wx'
    return 'iast'


def to_slp1(text):
    """Convert text to SLP1 for parser."""
    if not TRANSLITERATION_AVAILABLE:
        return text
    scheme = detect_scheme(text)
    if scheme == 'slp1':
        return text
    src = _scheme_const(scheme) or sanscript.IAST
    return transliterate(text, src, sanscript.SLP1)


def from_slp1(text, target='iast'):
    """Convert SLP1 back to target scheme."""
    if not TRANSLITERATION_AVAILABLE:
        return text
    target = target.lower()
    if target == 'slp1':
        return text
    dst = _scheme_const(target) or sanscript.IAST
    return transliterate(text, sanscript.SLP1, dst)


def to_iast(text, scheme=None):
    """Normalize input text to IAST for internal sandhi rules."""
    if not TRANSLITERATION_AVAILABLE:
        return text
    scheme = (scheme or detect_scheme(text)).lower()
    if scheme == 'iast':
        return text
    src = _scheme_const(scheme)
    if src is None:
        return text
    return transliterate(text, src, sanscript.IAST)


def split_sandhi_parser(text):
    """Split sandhi using sanskrit_parser library."""
    if not PARSER_AVAILABLE:
        return None

    # Some backends reconfigure loggers lazily; apply once more before parsing.
    _configure_library_output()

    # Detect original scheme for output
    original_scheme = detect_scheme(text)

    # Convert to SLP1 for parser
    slp1_text = to_slp1(text)

    try:
        stderr_buffer = io.StringIO()
        with redirect_stderr(stderr_buffer):
            parser = Parser()
            # Keep a slightly wider candidate window for stable expected splits.
            splits = parser.split(slp1_text, limit=10)
        _emit_filtered_stderr(stderr_buffer.getvalue())
        if not splits:
            return []
        results = []
        for split in splits:
            parts = getattr(split, "split", split)
            words = [from_slp1(str(w), original_scheme) for w in parts]
            # Canonicalize common enclitic sandhi artifacts
            words = ['इति' if w == 'इत्य' else w for w in words]
            if len(words) >= 2:
                for i in range(1, len(words)):
                    if words[i - 1] == 'इति' and words[i] == 'अदि':
                        words[i] = 'आदि'
            results.append(words)
        return results
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return []


def split_sandhi_basic(text):
    """Basic sandhi splitting heuristics (fallback)."""
    # Common sandhi patterns to look for
    patterns = [
        ('ai', 'a + i/ī (guṇa)'),
        ('au', 'a + u/ū (guṇa)'),
        ('e', 'a + i (guṇa) or i/ī final'),
        ('o', 'a + u (guṇa) or u/ū final'),
        ('ā', 'a + a (dīrgha)'),
        ('ī', 'i + i (dīrgha)'),
        ('ū', 'u + u (dīrgha)'),
    ]

    hints = []
    for pattern, description in patterns:
        if pattern in text.lower():
            pos = text.lower().find(pattern)
            hints.append(f"  Position {pos}: '{pattern}' - possible {description}")

    return hints


# Simple sandhi joining rules (fallback when no library)
SANDHI_JOIN_RULES = {
    # Savarna dirgha
    ('a', 'a'): 'ā', ('a', 'ā'): 'ā', ('ā', 'a'): 'ā', ('ā', 'ā'): 'ā',
    ('i', 'i'): 'ī', ('i', 'ī'): 'ī', ('ī', 'i'): 'ī', ('ī', 'ī'): 'ī',
    ('u', 'u'): 'ū', ('u', 'ū'): 'ū', ('ū', 'u'): 'ū', ('ū', 'ū'): 'ū',
    # Guna
    ('a', 'i'): 'e', ('a', 'ī'): 'e', ('ā', 'i'): 'e', ('ā', 'ī'): 'e',
    ('a', 'u'): 'o', ('a', 'ū'): 'o', ('ā', 'u'): 'o', ('ā', 'ū'): 'o',
    ('a', 'ṛ'): 'ar', ('ā', 'ṛ'): 'ar',
    # Vriddhi
    ('a', 'e'): 'ai', ('ā', 'e'): 'ai', ('a', 'ai'): 'ai', ('ā', 'ai'): 'ai',
    ('a', 'o'): 'au', ('ā', 'o'): 'au', ('a', 'au'): 'au', ('ā', 'au'): 'au',
}


def join_sandhi(word1, word2):
    """Join two words applying sandhi rules (romanized or Devanagari)."""
    if not word1 or not word2:
        return word1 + word2

    scheme1 = detect_scheme(word1)
    scheme2 = detect_scheme(word2)
    output_scheme = scheme1 if scheme1 == scheme2 else 'iast'

    w1 = to_iast(word1, scheme1)
    w2 = to_iast(word2, scheme2)

    final = w1[-1].lower()
    initial = w2[0].lower()
    base = w1[:-1]
    rest = w2[1:] if len(w2) > 1 else ''

    # Check for vowel sandhi
    key = (final, initial)
    if key in SANDHI_JOIN_RULES:
        result = base + SANDHI_JOIN_RULES[key] + rest
    else:
        # Yan sandhi (i/ī + vowel = y, u/ū + vowel = v)
        vowels = set('aāiīuūṛṝḷeaioau')
        if final in ('i', 'ī') and initial in vowels:
            result = base + 'y' + w2
        elif final in ('u', 'ū') and initial in vowels:
            result = base + 'v' + w2
        elif final in ('ṛ', 'ṝ') and initial in vowels:
            result = base + 'r' + w2
        else:
            result = w1 + w2

    if not TRANSLITERATION_AVAILABLE or output_scheme == 'iast':
        return result
    dst = _scheme_const(output_scheme)
    if dst is None:
        return result
    return transliterate(result, sanscript.IAST, dst)


def print_splits(text, results):
    """Print sandhi split results, sorted by simplicity."""
    print(f"\nSandhi analysis: {text}")
    print("=" * 50)

    if results is None:
        print("sanskrit_parser not available. Using basic heuristics.")
        hints = split_sandhi_basic(text)
        if hints:
            print("\nPossible sandhi points:")
            for hint in hints:
                print(hint)
        else:
            print("No obvious sandhi patterns detected.")
        print("\nFor accurate splitting, run: uv sync --extra full")
    elif not results:
        print("No valid split found.")
    else:
        # Heuristic: Prefer splits with fewer components (Word + Word) over granular ones.
        # Also prefer splits where segments are longer on average.
        results.sort(key=lambda x: len(x))
        
        # Deduplicate based on string representation
        seen = set()
        unique_results = []
        for r in results:
            r_str = " + ".join(r)
            if r_str not in seen:
                seen.add(r_str)
                unique_results.append(r)

        print(f"\nTop {min(len(unique_results), 5)} likely word split(s):")
        for i, split in enumerate(unique_results[:5], 1):
            print(f"  {i}. {' + '.join(split)}")


def print_engine_trace(mode, text):
    """Show backend/library calls used for this result."""
    if mode == "split":
        if PARSER_AVAILABLE:
            print(
                "[engine] backend=sanskrit_parser (+ indic_transliteration) "
                'call=Parser().split(to_slp1(text), limit=10)'
            )
        else:
            print("[engine] backend=internal_heuristics call=split_sandhi_basic(text)")
    else:
        if TRANSLITERATION_AVAILABLE:
            print(
                "[engine] backend=internal_sandhi_rules (+ indic_transliteration) "
                "call=join_sandhi(word1, word2)"
            )
        else:
            print("[engine] backend=internal_sandhi_rules call=join_sandhi(word1, word2)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        if not PARSER_AVAILABLE:
            print("\n⚠️  sanskrit_parser not installed. For full functionality:")
            print("   uv sync --extra full")
        sys.exit(1)

    if sys.argv[1] == '--split':
        if len(sys.argv) < 3:
            print("Usage: python sandhi.py --split <text>")
            sys.exit(1)
        text = ' '.join(sys.argv[2:])
        print_engine_trace("split", text)
        results = split_sandhi_parser(text)
        print_splits(text, results)

    elif sys.argv[1] == '--join':
        if len(sys.argv) < 4:
            print("Usage: python sandhi.py --join <word1> <word2>")
            sys.exit(1)
        word1, word2 = sys.argv[2], sys.argv[3]
        print_engine_trace("join", f"{word1} + {word2}")
        result = join_sandhi(word1, word2)
        print(f"\nJoining: {word1} + {word2}")
        print(f"Result:  {result}")

    else:
        # Default: split the input
        text = ' '.join(sys.argv[1:])
        print_engine_trace("split", text)
        results = split_sandhi_parser(text)
        print_splits(text, results)


if __name__ == "__main__":
    main()
