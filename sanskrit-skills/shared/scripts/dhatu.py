#!/usr/bin/env python3
"""
Sanskrit verbal root (dhatu) lookup tool.
Look up dhatu meanings, gana, and conjugation patterns.

Usage:
    python dhatu.py <dhatu>
    python dhatu.py --gana <gana_number>
    python dhatu.py --search <meaning>

Examples:
    python dhatu.py bhū
    python dhatu.py --gana 1
    python dhatu.py --search "to go"
"""

import sys
import re

try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
    TRANSLITERATION_AVAILABLE = True
except ImportError:
    TRANSLITERATION_AVAILABLE = False

# Dhatu database (subset of important roots)
DHATUS = {
    # Gana 1 - Bhvadi (भ्वादिगण) - Parasmaipada typically
    'bhū': {'gana': 1, 'meaning': 'to be, to become', 'pada': 'P', 'forms': {'lat': 'bhavati', 'lit': 'babhūva', 'lrt': 'bhaviṣyati'}},
    'gam': {'gana': 1, 'meaning': 'to go', 'pada': 'P', 'forms': {'lat': 'gacchati', 'lit': 'jagāma', 'lrt': 'gamiṣyati'}},
    'sthā': {'gana': 1, 'meaning': 'to stand', 'pada': 'P', 'forms': {'lat': 'tiṣṭhati', 'lit': 'tasthau', 'lrt': 'sthāsyati'}},
    'dā': {'gana': 1, 'meaning': 'to give', 'pada': 'P', 'forms': {'lat': 'dadāti', 'lit': 'dadau', 'lrt': 'dāsyati'}},
    'pat': {'gana': 1, 'meaning': 'to fall', 'pada': 'P', 'forms': {'lat': 'patati', 'lit': 'papāta', 'lrt': 'patiṣyati'}},
    'pac': {'gana': 1, 'meaning': 'to cook', 'pada': 'U', 'forms': {'lat': 'pacati', 'lit': 'papāca', 'lrt': 'pakṣyati'}},
    'vad': {'gana': 1, 'meaning': 'to speak', 'pada': 'P', 'forms': {'lat': 'vadati', 'lit': 'uvāda', 'lrt': 'vadiṣyati'}},
    'nī': {'gana': 1, 'meaning': 'to lead', 'pada': 'U', 'forms': {'lat': 'nayati', 'lit': 'nināya', 'lrt': 'neṣyati'}},
    'ji': {'gana': 1, 'meaning': 'to conquer', 'pada': 'P', 'forms': {'lat': 'jayati', 'lit': 'jigāya', 'lrt': 'jeṣyati'}},
    'kṛ': {'gana': 1, 'meaning': 'to do, to make', 'pada': 'U', 'forms': {'lat': 'karoti', 'lit': 'cakāra', 'lrt': 'kariṣyati'}},
    'śru': {'gana': 1, 'meaning': 'to hear', 'pada': 'P', 'forms': {'lat': 'śṛṇoti', 'lit': 'śuśrāva', 'lrt': 'śroṣyati'}},
    'dṛś': {'gana': 1, 'meaning': 'to see', 'pada': 'P', 'forms': {'lat': 'paśyati', 'lit': 'dadarśa', 'lrt': 'drakṣyati'}},
    'vṛt': {'gana': 1, 'meaning': 'to exist, turn', 'pada': 'A', 'forms': {'lat': 'vartate', 'lit': 'vavṛte', 'lrt': 'vartsyate'}},
    'labh': {'gana': 1, 'meaning': 'to obtain', 'pada': 'A', 'forms': {'lat': 'labhate', 'lit': 'lebhe', 'lrt': 'lapsyate'}},
    'budh': {'gana': 1, 'meaning': 'to know, awaken', 'pada': 'U', 'forms': {'lat': 'bodhati', 'lit': 'bubodha', 'lrt': 'bodhiṣyati'}},

    # Gana 2 - Adadi (अदादिगण) - Root class
    'ad': {'gana': 2, 'meaning': 'to eat', 'pada': 'P', 'forms': {'lat': 'atti', 'lit': 'āda', 'lrt': 'atsyati'}},
    'as': {'gana': 2, 'meaning': 'to be', 'pada': 'P', 'forms': {'lat': 'asti', 'lit': 'āsa', 'lrt': 'bhaviṣyati'}},
    'han': {'gana': 2, 'meaning': 'to kill', 'pada': 'P', 'forms': {'lat': 'hanti', 'lit': 'jaghāna', 'lrt': 'haniṣyati'}},
    'i': {'gana': 2, 'meaning': 'to go', 'pada': 'P', 'forms': {'lat': 'eti', 'lit': 'iyāya', 'lrt': 'eṣyati'}},
    'vid': {'gana': 2, 'meaning': 'to know', 'pada': 'P', 'forms': {'lat': 'vetti', 'lit': 'vidāṃcakāra', 'lrt': 'vediṣyati'}},
    'śī': {'gana': 2, 'meaning': 'to lie down', 'pada': 'A', 'forms': {'lat': 'śete', 'lit': 'śiśye', 'lrt': 'śayiṣyate'}},
    'brū': {'gana': 2, 'meaning': 'to speak', 'pada': 'U', 'forms': {'lat': 'bravīti', 'lit': 'uvāca', 'lrt': 'vakṣyati'}},

    # Gana 3 - Juhotyadi (जुहोत्यादिगण) - Reduplicating class
    'hu': {'gana': 3, 'meaning': 'to sacrifice', 'pada': 'P', 'forms': {'lat': 'juhoti', 'lit': 'juhāva', 'lrt': 'hoṣyati'}},
    'dhā': {'gana': 3, 'meaning': 'to place', 'pada': 'U', 'forms': {'lat': 'dadhāti', 'lit': 'dadhau', 'lrt': 'dhāsyati'}},
    'mā': {'gana': 3, 'meaning': 'to measure', 'pada': 'A', 'forms': {'lat': 'mimīte', 'lit': 'mamau', 'lrt': 'māsyate'}},

    # Gana 4 - Divadi (दिवादिगण) - Ya class
    'div': {'gana': 4, 'meaning': 'to play, shine', 'pada': 'P', 'forms': {'lat': 'dīvyati', 'lit': 'dideva', 'lrt': 'deviṣyati'}},
    'nah': {'gana': 4, 'meaning': 'to bind', 'pada': 'U', 'forms': {'lat': 'nahyati', 'lit': 'nanāha', 'lrt': 'natsyati'}},
    'pad': {'gana': 4, 'meaning': 'to go, fall', 'pada': 'A', 'forms': {'lat': 'padyate', 'lit': 'pede', 'lrt': 'patsyate'}},
    'puṣ': {'gana': 4, 'meaning': 'to nourish', 'pada': 'P', 'forms': {'lat': 'puṣyati', 'lit': 'pupoṣa', 'lrt': 'poṣyati'}},
    'kup': {'gana': 4, 'meaning': 'to be angry', 'pada': 'P', 'forms': {'lat': 'kupyati', 'lit': 'cukopa', 'lrt': 'kopiṣyati'}},
    'mad': {'gana': 4, 'meaning': 'to rejoice', 'pada': 'P', 'forms': {'lat': 'mādyati', 'lit': 'mamāda', 'lrt': 'madiṣyati'}},

    # Gana 5 - Svadi (स्वादिगण) - Nu class
    'su': {'gana': 5, 'meaning': 'to press out (soma)', 'pada': 'U', 'forms': {'lat': 'sunoti', 'lit': 'suṣāva', 'lrt': 'soṣyati'}},
    'āp': {'gana': 5, 'meaning': 'to obtain', 'pada': 'P', 'forms': {'lat': 'āpnoti', 'lit': 'āpa', 'lrt': 'āpsyati'}},
    'śak': {'gana': 5, 'meaning': 'to be able', 'pada': 'P', 'forms': {'lat': 'śaknoti', 'lit': 'śaśāka', 'lrt': 'śakṣyati'}},

    # Gana 6 - Tudadi (तुदादिगण) - Accented ya class
    'tud': {'gana': 6, 'meaning': 'to strike', 'pada': 'P', 'forms': {'lat': 'tudati', 'lit': 'tutoda', 'lrt': 'totsyati'}},
    'muc': {'gana': 6, 'meaning': 'to release', 'pada': 'U', 'forms': {'lat': 'muñcati', 'lit': 'mumoca', 'lrt': 'mokṣyati'}},
    'viś': {'gana': 6, 'meaning': 'to enter', 'pada': 'P', 'forms': {'lat': 'viśati', 'lit': 'viveśa', 'lrt': 'vekṣyati'}},
    'likh': {'gana': 6, 'meaning': 'to write', 'pada': 'P', 'forms': {'lat': 'likhati', 'lit': 'lilekha', 'lrt': 'lekhiṣyati'}},
    'kṣip': {'gana': 6, 'meaning': 'to throw', 'pada': 'P', 'forms': {'lat': 'kṣipati', 'lit': 'cikṣepa', 'lrt': 'kṣepsyati'}},
    'spṛś': {'gana': 6, 'meaning': 'to touch', 'pada': 'P', 'forms': {'lat': 'spṛśati', 'lit': 'pasparśa', 'lrt': 'sparkṣyati'}},

    # Gana 7 - Rudhadi (रुधादिगण) - Nasal infix class
    'rudh': {'gana': 7, 'meaning': 'to obstruct', 'pada': 'U', 'forms': {'lat': 'ruṇaddhi', 'lit': 'rurodha', 'lrt': 'rotsyati'}},
    'bhid': {'gana': 7, 'meaning': 'to split', 'pada': 'U', 'forms': {'lat': 'bhinatti', 'lit': 'bibheda', 'lrt': 'bhetsyati'}},
    'chid': {'gana': 7, 'meaning': 'to cut', 'pada': 'U', 'forms': {'lat': 'chinatti', 'lit': 'ciccheda', 'lrt': 'chetsyati'}},
    'yuj': {'gana': 7, 'meaning': 'to join', 'pada': 'U', 'forms': {'lat': 'yunakti', 'lit': 'yuyoja', 'lrt': 'yokṣyati'}},
    'bhuj': {'gana': 7, 'meaning': 'to enjoy', 'pada': 'U', 'forms': {'lat': 'bhuṅkte', 'lit': 'bubhuje', 'lrt': 'bhokṣyate'}},

    # Gana 8 - Tanadi (तनादिगण) - U class
    'tan': {'gana': 8, 'meaning': 'to stretch', 'pada': 'U', 'forms': {'lat': 'tanoti', 'lit': 'tatāna', 'lrt': 'taniṣyati'}},
    'san': {'gana': 8, 'meaning': 'to obtain', 'pada': 'U', 'forms': {'lat': 'sanoti', 'lit': 'sasāna', 'lrt': 'saniṣyati'}},
    'kṣan': {'gana': 8, 'meaning': 'to injure', 'pada': 'P', 'forms': {'lat': 'kṣaṇoti', 'lit': 'cakṣāṇa', 'lrt': 'kṣaṇiṣyati'}},

    # Gana 9 - Kryadi (क्र्यादिगण) - Nā class
    'krī': {'gana': 9, 'meaning': 'to buy', 'pada': 'U', 'forms': {'lat': 'krīṇāti', 'lit': 'cikrāya', 'lrt': 'kreṣyati'}},
    'jñā': {'gana': 9, 'meaning': 'to know', 'pada': 'U', 'forms': {'lat': 'jānāti', 'lit': 'jajñau', 'lrt': 'jñāsyati'}},
    'grah': {'gana': 9, 'meaning': 'to seize', 'pada': 'U', 'forms': {'lat': 'gṛhṇāti', 'lit': 'jagrāha', 'lrt': 'grahīṣyati'}},
    'pū': {'gana': 9, 'meaning': 'to purify', 'pada': 'U', 'forms': {'lat': 'punāti', 'lit': 'pupāva', 'lrt': 'paviṣyati'}},
    'prī': {'gana': 9, 'meaning': 'to please', 'pada': 'U', 'forms': {'lat': 'prīṇāti', 'lit': 'piprāya', 'lrt': 'preṣyati'}},

    # Gana 10 - Curadi (चुरादिगण) - Causative class
    'cur': {'gana': 10, 'meaning': 'to steal', 'pada': 'U', 'forms': {'lat': 'corayati', 'lit': 'corayāṃcakāra', 'lrt': 'corayiṣyati'}},
    'cint': {'gana': 10, 'meaning': 'to think', 'pada': 'U', 'forms': {'lat': 'cintayati', 'lit': 'cintayāṃcakāra', 'lrt': 'cintayiṣyati'}},
    'kath': {'gana': 10, 'meaning': 'to tell', 'pada': 'U', 'forms': {'lat': 'kathayati', 'lit': 'kathayāṃcakāra', 'lrt': 'kathayiṣyati'}},
    'pūj': {'gana': 10, 'meaning': 'to worship', 'pada': 'U', 'forms': {'lat': 'pūjayati', 'lit': 'pūjayāṃcakāra', 'lrt': 'pūjayiṣyati'}},
    'sev': {'gana': 10, 'meaning': 'to serve', 'pada': 'A', 'forms': {'lat': 'sevate', 'lit': 'sevāṃcakre', 'lrt': 'seviṣyate'}},
}

GANA_NAMES = {
    1: 'Bhvādi (भ्वादि)',
    2: 'Adādi (अदादि)',
    3: 'Juhotyādi (जुहोत्यादि)',
    4: 'Divādi (दिवादि)',
    5: 'Svādi (स्वादि)',
    6: 'Tudādi (तुदादि)',
    7: 'Rudhādi (रुधादि)',
    8: 'Tanādi (तनादि)',
    9: 'Kryādi (क्र्यादि)',
    10: 'Curādi (चुरादि)',
}

PADA_NAMES = {
    'P': 'Parasmaipada (परस्मैपद)',
    'A': 'Ātmanepada (आत्मनेपद)',
    'U': 'Ubhayapada (उभयपद)',
}

LAKARA_NAMES = {
    'lat': 'Laṭ (वर्तमान/Present)',
    'lit': 'Liṭ (परोक्षभूत/Perfect)',
    'lrt': 'Lṛṭ (भविष्यत्/Future)',
}


def _normalize_dhatu(dhatu):
    dhatu = dhatu.strip()
    if not dhatu:
        return dhatu
    if TRANSLITERATION_AVAILABLE:
        if any('\u0900' <= ch <= '\u097F' for ch in dhatu):
            dhatu = transliterate(dhatu, sanscript.DEVANAGARI, sanscript.IAST)
    return dhatu.lower()


def lookup_dhatu(dhatu):
    """Look up a dhatu in the database."""
    dhatu = _normalize_dhatu(dhatu)

    if dhatu in DHATUS:
        return DHATUS[dhatu]

    # Try alternate spellings
    alternates = {
        'bhu': 'bhū', 'gam': 'gam', 'stha': 'sthā', 'da': 'dā',
        'ni': 'nī', 'kri': 'kṛ', 'dris': 'dṛś', 'drs': 'dṛś',
        'vrit': 'vṛt', 'vrt': 'vṛt', 'i': 'i', 'dha': 'dhā',
        'jña': 'jñā', 'jnā': 'jñā', 'grah': 'grah', 'sru': 'śru',
        'shru': 'śru', 'shi': 'śī', 'bru': 'brū',
    }

    if dhatu in alternates:
        alt = alternates[dhatu]
        if alt in DHATUS:
            return DHATUS[alt]

    return None


def list_by_gana(gana_num):
    """List all dhatus in a specific gana."""
    return {k: v for k, v in DHATUS.items() if v['gana'] == gana_num}


def search_by_meaning(query):
    """Search dhatus by meaning."""
    query = _normalize_dhatu(query).lower()
    results = {}
    for dhatu, info in DHATUS.items():
        if query in info['meaning'].lower():
            results[dhatu] = info
    return results


def print_dhatu_info(dhatu, info):
    """Print detailed dhatu information."""
    print(f"\n{'=' * 50}")
    print(f"DHATU: √{dhatu}")
    print(f"{'=' * 50}")
    print(f"Meaning: {info['meaning']}")
    print(f"Gaṇa: {info['gana']} - {GANA_NAMES[info['gana']]}")
    print(f"Pada: {info['pada']} - {PADA_NAMES[info['pada']]}")

    if 'forms' in info:
        print(f"\nPrincipal forms:")
        for lakara, form in info['forms'].items():
            print(f"  {LAKARA_NAMES[lakara]}: {form}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable gaṇas:")
        for num, name in GANA_NAMES.items():
            print(f"  {num}. {name}")
        sys.exit(1)

    if sys.argv[1] == '--gana':
        if len(sys.argv) < 3:
            print("Usage: python dhatu.py --gana <gana_number>")
            sys.exit(1)
        gana = int(sys.argv[2])
        dhatus = list_by_gana(gana)
        print(f"\nGaṇa {gana} - {GANA_NAMES[gana]}")
        print("=" * 50)
        for dhatu, info in dhatus.items():
            print(f"  √{dhatu}: {info['meaning']} ({info['pada']})")

    elif sys.argv[1] == '--search':
        if len(sys.argv) < 3:
            print("Usage: python dhatu.py --search <meaning>")
            sys.exit(1)
        query = ' '.join(sys.argv[2:])
        results = search_by_meaning(query)
        if results:
            print(f"\nDhatus matching '{query}':")
            print("=" * 50)
            for dhatu, info in results.items():
                print(f"  √{dhatu} ({info['gana']}): {info['meaning']}")
        else:
            print(f"No dhatus found matching '{query}'")

    else:
        dhatu = sys.argv[1]
        info = lookup_dhatu(dhatu)
        if info:
            print_dhatu_info(dhatu, info)
        else:
            print(f"Dhatu '{dhatu}' not found in database.")
            # Suggest similar
            suggestions = search_by_meaning(dhatu)
            if suggestions:
                print("\nDid you mean one of these?")
                for d, i in list(suggestions.items())[:5]:
                    print(f"  √{d}: {i['meaning']}")


if __name__ == "__main__":
    main()
