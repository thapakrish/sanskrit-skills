#!/usr/bin/env python3
"""
Sanskrit meter (chandas) analyzer using robust SLP1 transliteration.
Detects the meter of a Sanskrit verse based on syllable patterns.

Usage:
    cd shared/scripts && uv run python chandas.py \"<verse_in_iast_or_devanagari>\"
"""

import sys
import re
from indic_transliteration import sanscript
from indic_transliteration.detect import detect

# SLP1 Vowels
# Short: a, i, u, f (r), x (l)
SHORT_VOWELS = set('aiufx')
# Long: A, I, U, F (RR), X (LL), e, E (ai), o, O (au)
LONG_VOWELS = set('AIUFXeEoO')
ALL_VOWELS = SHORT_VOWELS | LONG_VOWELS
ANUSVARA_VISARGA = set('MH')
SLP1_CONSONANTS = set('kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh')
SLP1_VALID = ALL_VOWELS | ANUSVARA_VISARGA | SLP1_CONSONANTS

# Common meters with their patterns (G=guru/heavy, L=laghu/light)
METERS = {
    # Syllabic meters (varnavrittas)
    'anuṣṭup': {
        'syllables_per_pada': 8,
        'padas': 4,
        'pattern': None,  # Variable
        'description': 'Most common meter. 5th syllable usually Laghu, 6th Guru.',
    },
    'indravajrā': {
        'syllables_per_pada': 11,
        'padas': 4,
        'pattern': 'GGLGGLLGLGG',
        'description': '11 syllables: GGL GG L L G L GG (ta-ta-ja-ga-ga)',
    },
    'upendravajrā': {
        'syllables_per_pada': 11,
        'padas': 4,
        'pattern': 'LGLGGLLGLGG',
        'description': '11 syllables: LGL GG L L G L GG (ja-ta-ja-ga-ga)',
    },
    'upajāti': {
        'syllables_per_pada': 11,
        'padas': 4,
        'pattern': None, # Mixed Indra/Upendra
        'description': 'Mix of Indravajrā and Upendravajrā lines',
    },
    'vaṃśastha': {
        'syllables_per_pada': 12,
        'padas': 4,
        'pattern': 'LGLGGLGGLGLG',
        'description': '12 syllables: LGL GGL GGL GLG (ja-ta-ja-ra)',
    },
    'vasantatilakā': {
        'syllables_per_pada': 14,
        'padas': 4,
        'pattern': 'GGLGLLLLGLGGLG',
        'description': '14 syllables: GGL GLL LLG LGG LG (ta-bha-ja-ja-ga-ga)',
    },
    'mālinī': {
        'syllables_per_pada': 15,
        'padas': 4,
        'pattern': 'LLLLLLGGLLGGLGG',
        'description': '15 syllables: LLL LLL GGL LGG LGG (na-na-ma-ya-ya)',
    },
    'mandākrāntā': {
        'syllables_per_pada': 17,
        'padas': 4,
        'pattern': 'GGGGLLLLLLGGLGGLG',
        'description': '17 syllables: GGGG LLL LLL GGL GGL G (ma-bha-na-ta-ta-ga-ga)',
    },
    'śikhariṇī': {
        'syllables_per_pada': 17,
        'padas': 4,
        'pattern': 'LGGGGLLLLLGGLGGLG',
        'description': '17 syllables: LGG GGL LLL LGG LGG LG (ya-ma-na-sa-bha-la-ga)',
    },
    'hariṇī': {
        'syllables_per_pada': 17,
        'padas': 4,
        'pattern': 'LLLLGLGGLLGGLGGLG',
        'description': '17 syllables: LLL LGL GGL LGG LGG LG (na-sa-ma-ra-sa-la-ga)',
    },
    'śārdūlavikrīḍita': {
        'syllables_per_pada': 19,
        'padas': 4,
        'pattern': 'GGGLGGLGLLLGGLGGLG',
        'description': '19 syllables: GGG LGG LGL LLG GLG GLG (ma-sa-ja-sa-ta-ta-ga)',
    },
    'sragdharā': {
        'syllables_per_pada': 21,
        'padas': 4,
        'pattern': 'GGGGLGGLGGLLLLLGGLGGG',
        'description': '21 syllables: GGG GLG GLG GLL LLL GGL GGG (ma-ra-bha-na-ya-ya-ya)',
    },
}

def _strip_common_punctuation(text):
    return re.sub(r"[।॥|,.;:!?()\[\]{}'\"0-9]", '', text)


def _is_slp1(text):
    if not text:
        return False
    return all(ch in SLP1_VALID or ch.isspace() for ch in text)


def to_slp1(text):
    """Convert input text to SLP1 scheme for analysis."""
    text = _strip_common_punctuation(text)

    scheme = detect(text)
    if scheme == sanscript.DEVANAGARI:
        return sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.SLP1)
    if scheme == sanscript.SLP1 or _is_slp1(text):
        return text
    if scheme == sanscript.HK:
        return sanscript.transliterate(text, sanscript.HK, sanscript.SLP1)
    if scheme == sanscript.ITRANS:
        return sanscript.transliterate(text, sanscript.ITRANS, sanscript.SLP1)
    if scheme == sanscript.VELTHUIS:
        return sanscript.transliterate(text, sanscript.VELTHUIS, sanscript.SLP1)
    if scheme == sanscript.WX:
        return sanscript.transliterate(text, sanscript.WX, sanscript.SLP1)

    try:
        return sanscript.transliterate(text, sanscript.IAST, sanscript.SLP1)
    except Exception as exc:
        raise ValueError("Unsupported or unknown input scheme for chandas analysis") from exc

def analyze_weights_slp1(slp1_text):
    """
    Analyze weights (G/L) from SLP1 text string. 
    
    SLP1 Logic:
    - Vowels are explicit.
    - Consonants are explicit.
    - No inherent 'a' ambiguity.
    """
    weights = []
    syllables = []
    
    # Clean up input: remove spaces and non-SLP1 symbols
    clean_text = "".join(ch for ch in slp1_text if ch in SLP1_VALID)
    
    length = len(clean_text)
    i = 0
    
    # We iterate through the string looking for VOWELS as nuclei
    while i < length:
        char = clean_text[i]
        
        if char in ALL_VOWELS:
            # Found a syllable nucleus
            weight = 'L'
            
            # Rule 1: Long vowel = Guru
            if char in LONG_VOWELS:
                weight = 'G'
            
            # Look ahead for conjuncts or anusvara/visarga
            # Count consonants immediately following this vowel
            consonant_cluster_len = 0
            j = i + 1
            has_anusvara_visarga = False
            
            while j < length:
                next_char = clean_text[j]
                if next_char in ANUSVARA_VISARGA:
                    has_anusvara_visarga = True
                    j += 1
                    continue # Keep checking
                
                if next_char not in ALL_VOWELS:
                    consonant_cluster_len += 1
                    j += 1
                else:
                    break # Hit next vowel
            
            # Rule 2: Anusvara/Visarga = Guru
            if has_anusvara_visarga:
                weight = 'G'
                
            # Rule 3: Conjunct (2+ consonants) following = Guru
            if consonant_cluster_len >= 2:
                weight = 'G'
            
            # Rule 4: End of Pada = Guru (Always treated as heavy for meter)
            # Check if this is the last vowel in the line
            is_last_syllable = True
            k = i + 1
            while k < length:
                if clean_text[k] in ALL_VOWELS:
                    is_last_syllable = False
                    break
                k += 1
                
            if is_last_syllable:
                weight = 'G'
                
            weights.append(weight)
        
        i += 1
            
    return "".join(weights), len(weights)


def _is_upajati(padas):
    if len(padas) < 2:
        return False
    indra = METERS['indravajrā']['pattern']
    upendra = METERS['upendravajrā']['pattern']
    patterns = [p['pattern'] for p in padas if p['pattern']]
    if not patterns:
        return False
    has_indra = any(p == indra for p in patterns)
    has_upendra = any(p == upendra for p in patterns)
    return has_indra and has_upendra

def analyze_verse(verse):
    """Analyze a complete verse."""
    # Split into padas (quarters)
    # Handle standard separators
    padas_raw = re.split(r'[।॥|\n]+', verse)
    padas = [p.strip() for p in padas_raw if p.strip()]

    results = {
        'padas': [],
        'overall_pattern': '',
        'total_syllables': 0,
        'probable_meters': [],
    }

    all_patterns = []

    for pada in padas:
        slp1_text = to_slp1(pada)
        pattern, count = analyze_weights_slp1(slp1_text)
        
        results['padas'].append({
            'text': pada,
            'slp1': slp1_text,
            'syllable_count': count,
            'pattern': pattern,
        })
        all_patterns.append(pattern)
        results['total_syllables'] += count

    results['overall_pattern'] = ' | '.join(all_patterns)

    # Meter Identification
    if results['padas']:
        first_pada = results['padas'][0]
        # Check against database
        matches = []
        fp_pattern = first_pada['pattern']
        fp_count = first_pada['syllable_count']
        
        for name, meter in METERS.items():
            if meter['syllables_per_pada'] == fp_count:
                if meter['pattern']:
                    if fp_pattern == meter['pattern']:
                        matches.append((name, 100, meter['description']))
                    else:
                        # Simple diff
                        match_count = sum(1 for a, b in zip(fp_pattern, meter['pattern']) if a == b)
                        pct = (match_count / len(meter['pattern'])) * 100
                        if pct > 75:
                            matches.append((name, pct, meter['description']))
                elif name == 'anuṣṭup' and fp_count == 8:
                     matches.append(('anuṣṭup', 95, meter['description']))

        if _is_upajati(results['padas']):
            matches.append(('upajāti', 90, METERS['upajāti']['description']))

        matches.sort(key=lambda x: -x[1])
        results['probable_meters'] = matches

    return results

def print_analysis(results):
    print("\n" + "=" * 60)
    print("CHANDAS ANALYSIS (Engine: SLP1)")
    print("=" * 60)

    for i, pada in enumerate(results['padas'], 1):
        print(f"\nPada {i}: {pada['text']}")
        print(f"  SLP1: {pada['slp1']}")
        print(f"  Count: {pada['syllable_count']}")
        print(f"  Pattern: {pada['pattern']}")

    print(f"\nOverall: {results['overall_pattern']}")

    if results['probable_meters']:
        print("\nProbable Meter(s):")
        for name, conf, desc in results['probable_meters'][:3]:
            print(f"  • {name} ({conf:.0f}% match)")
            print(f"    {desc}")
    else:
        print("\nMeter: Unidentified or irregular.")
    print("=" * 60)


def print_engine_trace():
    """Show backend/library calls used for this result."""
    print(
        "[engine] backend=indic_transliteration + internal_slp1_analyzer "
        "call=detect()->transliterate(..., SLP1)->analyze_weights_slp1()"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    input_verse = " ".join(sys.argv[1:])
    print_engine_trace()
    data = analyze_verse(input_verse)
    print_analysis(data)
