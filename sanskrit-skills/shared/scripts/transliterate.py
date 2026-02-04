#!/usr/bin/env python3
"""
Sanskrit transliteration converter using indic-transliteration library.
Converts between Devanagari, IAST, Harvard-Kyoto, ITRANS, SLP1, Velthuis, and more.

Setup:
    uv sync  # from the scripts directory

Usage:
    python transliterate.py <input_text> <from_scheme> <to_scheme>

Examples:
    python transliterate.py "संस्कृतम्" devanagari iast
    python transliterate.py "saṃskṛtam" iast hk
    python transliterate.py "saMskRtam" hk devanagari
    python transliterate.py "rAma" itrans devanagari

Supported schemes:
    devanagari, iast, hk (Harvard-Kyoto), itrans, slp1, velthuis, wx,
    kolkata, tamil, telugu, kannada, malayalam, bengali, gujarati, oriya
"""

import sys

try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
except ImportError:
    print("Error: indic-transliteration not installed.")
    print("Run: uv sync")
    sys.exit(1)


# Map user-friendly names to sanscript constants
SCHEME_MAP = {
    'devanagari': sanscript.DEVANAGARI,
    'iast': sanscript.IAST,
    'hk': sanscript.HK,
    'harvard-kyoto': sanscript.HK,
    'itrans': sanscript.ITRANS,
    'slp1': sanscript.SLP1,
    'velthuis': sanscript.VELTHUIS,
    'wx': sanscript.WX,
    'kolkata': sanscript.KOLKATA,
    'tamil': sanscript.TAMIL,
    'telugu': sanscript.TELUGU,
    'kannada': sanscript.KANNADA,
    'malayalam': sanscript.MALAYALAM,
    'bengali': sanscript.BENGALI,
    'gujarati': sanscript.GUJARATI,
    'oriya': sanscript.ORIYA,
    'gurmukhi': sanscript.GURMUKHI,
}


def get_scheme(name):
    """Get sanscript scheme constant from user-friendly name."""
    name = name.lower().strip()
    if name in SCHEME_MAP:
        return SCHEME_MAP[name]
    # Try direct attribute access
    if hasattr(sanscript, name.upper()):
        return getattr(sanscript, name.upper())
    return None


def convert(text, from_scheme, to_scheme):
    """Convert text between transliteration schemes."""
    src = get_scheme(from_scheme)
    dst = get_scheme(to_scheme)

    if src is None:
        raise ValueError(f"Unknown source scheme: {from_scheme}")
    if dst is None:
        raise ValueError(f"Unknown target scheme: {to_scheme}")

    return transliterate(text, src, dst)


def print_engine_trace(from_scheme, to_scheme):
    """Show backend/library call used for this result."""
    print(
        "[engine] backend=indic_transliteration.sanscript "
        f'call=transliterate(text, "{from_scheme}", "{to_scheme}")'
    )


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        print("\nAvailable schemes:")
        for name in sorted(SCHEME_MAP.keys()):
            print(f"  {name}")
        sys.exit(1)

    text = sys.argv[1]
    from_scheme = sys.argv[2]
    to_scheme = sys.argv[3]

    try:
        print_engine_trace(from_scheme, to_scheme)
        result = convert(text, from_scheme, to_scheme)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
