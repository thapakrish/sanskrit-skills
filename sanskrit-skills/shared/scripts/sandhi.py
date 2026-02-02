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
    if scheme == 'devanagari':
        return transliterate(text, sanscript.DEVANAGARI, sanscript.SLP1)
    if scheme == 'slp1':
        return text
    if scheme == 'hk':
        return transliterate(text, sanscript.HK, sanscript.SLP1)
    if scheme == 'itrans':
        return transliterate(text, sanscript.ITRANS, sanscript.SLP1)
    if scheme == 'velthuis':
        return transliterate(text, sanscript.VELTHUIS, sanscript.SLP1)
    if scheme == 'wx':
        return transliterate(text, sanscript.WX, sanscript.SLP1)
    else:
        return transliterate(text, sanscript.IAST, sanscript.SLP1)


def from_slp1(text, target='iast'):
    """Convert SLP1 back to target scheme."""
    if not TRANSLITERATION_AVAILABLE:
        return text
    if target == 'devanagari':
        return transliterate(text, sanscript.SLP1, sanscript.DEVANAGARI)
    if target == 'slp1':
        return text
    else:
        return transliterate(text, sanscript.SLP1, sanscript.IAST)


def split_sandhi_parser(text):
    """Split sandhi using sanskrit_parser library."""
    if not PARSER_AVAILABLE:
        return None

    parser = Parser()

    # Detect original scheme for output
    original_scheme = detect_scheme(text)

    # Convert to SLP1 for parser
    slp1_text = to_slp1(text)

    try:
        splits = parser.split(slp1_text, limit=5)
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
        return [f"Error: {e}"]


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

    w1 = word1
    w2 = word2

    if TRANSLITERATION_AVAILABLE and (scheme1 == 'devanagari' or scheme2 == 'devanagari'):
        if scheme1 == 'devanagari':
            w1 = transliterate(word1, sanscript.DEVANAGARI, sanscript.IAST)
        if scheme2 == 'devanagari':
            w2 = transliterate(word2, sanscript.DEVANAGARI, sanscript.IAST)

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

    if TRANSLITERATION_AVAILABLE and output_scheme == 'devanagari':
        return transliterate(result, sanscript.IAST, sanscript.DEVANAGARI)

    return result


def print_splits(text, results):
    """Print sandhi split results."""
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
    elif isinstance(results[0], str) and results[0].startswith("Error"):
        print(results[0])
    else:
        print(f"\nFound {len(results)} possible split(s):")
        for i, split in enumerate(results, 1):
            print(f"  {i}. {' + '.join(split)}")


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
        results = split_sandhi_parser(text)
        print_splits(text, results)

    elif sys.argv[1] == '--join':
        if len(sys.argv) < 4:
            print("Usage: python sandhi.py --join <word1> <word2>")
            sys.exit(1)
        word1, word2 = sys.argv[2], sys.argv[3]
        result = join_sandhi(word1, word2)
        print(f"\nJoining: {word1} + {word2}")
        print(f"Result:  {result}")

    else:
        # Default: split the input
        text = ' '.join(sys.argv[1:])
        results = split_sandhi_parser(text)
        print_splits(text, results)


if __name__ == "__main__":
    main()
