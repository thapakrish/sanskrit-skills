#!/usr/bin/env python3
"""
Sanskrit word derivation analyzer using vidyut-prakriya.
Provides step-by-step Paninian derivations for subantas (nominals) and tinantas (verbals).

Usage:
    python prakriya.py subanta <pratipadika> <linga> <vibhakti> <vacana>
    python prakriya.py tinanta <dhatu> <gana> <prayoga> <purusha> <vacana> <lakara>

Examples:
    python prakriya.py subanta rAma Pum Prathama Eka
    python prakriya.py tinanta gam 1 Kartari Prathama Eka Lat
"""

import sys
import argparse

try:
    from vidyut.prakriya import (
        Vyakarana, Pratipadika, Pada, Linga, Vibhakti, Vacana,
        Dhatu, Prayoga, Purusha, Lakara, Gana
    )
    VIDYUT_AVAILABLE = True
except ImportError:
    VIDYUT_AVAILABLE = False

try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
    from indic_transliteration.detect import detect
    TRANSLITERATION_AVAILABLE = True
except ImportError:
    TRANSLITERATION_AVAILABLE = False


SUPPORTED_SCHEMES = {
    sanscript.DEVANAGARI,
    sanscript.IAST,
    sanscript.HK,
    sanscript.ITRANS,
    sanscript.SLP1,
    sanscript.VELTHUIS,
    sanscript.WX,
} if TRANSLITERATION_AVAILABLE else set()


def to_slp1(text):
    """Normalize known transliteration schemes to SLP1."""
    if not TRANSLITERATION_AVAILABLE:
        return text

    scheme = detect(text)
    if scheme == sanscript.SLP1:
        return text

    if scheme in SUPPORTED_SCHEMES:
        return transliterate(text, scheme, sanscript.SLP1)

    try:
        return transliterate(text, sanscript.IAST, sanscript.SLP1)
    except Exception:
        return text

def format_prakriya(p):
    print(f"\nResult: {p.text}")
    print("-" * 40)
    for step in p.history:
        # Some steps might not have a sutra code (e.g. initial terms)
        code = step.code if step.code else "---"
        terms = " + ".join(step.result)
        print(f"[{code:8}] {terms}")

def derive_subanta(args):
    v = Vyakarana()
    try:
        pratipadika = Pratipadika.basic(to_slp1(args.pratipadika))
        linga = getattr(Linga, args.linga)
        vibhakti = getattr(Vibhakti, args.vibhakti)
        vacana = getattr(Vacana, args.vacana)
        
        subanta = Pada.Subanta(pratipadika, linga, vibhakti, vacana)
        results = v.derive(subanta)
        
        if not results:
            print("No derivation found.")
            return 1

        for p in results:
            format_prakriya(p)
        return 0
            
    except AttributeError as e:
        print(f"Invalid parameter: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def derive_tinanta(args):
    v = Vyakarana()
    try:
        # Map gana integer to Gana enum
        # Note: Gana enum names are like 'Bhvadi', 'Adadi', etc.
        # But we can also use from_int if available, or a map.
        gana_map = {
            1: Gana.Bhvadi, 2: Gana.Adadi, 3: Gana.Juhotyadi, 4: Gana.Divadi,
            5: Gana.Svadi, 6: Gana.Tudadi, 7: Gana.Rudhadi, 8: Gana.Tanadi,
            9: Gana.Kryadi, 10: Gana.Curadi
        }
        gana = gana_map.get(args.gana)
        if not gana:
            print(f"Invalid gana: {args.gana}")
            return 1

        dhatu = Dhatu.mula(to_slp1(args.dhatu), gana)
        prayoga = getattr(Prayoga, args.prayoga)
        purusha = getattr(Purusha, args.purusha)
        vacana = getattr(Vacana, args.vacana)
        lakara = getattr(Lakara, args.lakara)
        
        tinanta = Pada.Tinanta(dhatu, prayoga, lakara, purusha, vacana)
        results = v.derive(tinanta)
        
        if not results:
            print("No derivation found.")
            return 1

        for p in results:
            format_prakriya(p)
        return 0
            
    except AttributeError as e:
        print(f"Invalid parameter: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Sanskrit Prakriya Analyzer")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")
    
    # Subanta parser
    sub_parser = subparsers.add_parser("subanta", help="Derive subanta (nominal)")
    sub_parser.add_argument("pratipadika", help="Nominal stem (SLP1 or IAST)")
    sub_parser.add_argument("linga", choices=["Pum", "Stri", "Napumsaka"], help="Gender")
    sub_parser.add_argument("vibhakti", choices=["Prathama", "Dvitiya", "Trtiya", "Caturthi", "Panchami", "Sasthi", "Saptami", "Sambodhana"], help="Case")
    sub_parser.add_argument("vacana", choices=["Eka", "Dvi", "Bahu"], help="Number")
    
    # Tinanta parser
    tin_parser = subparsers.add_parser("tinanta", help="Derive tinanta (verbal)")
    tin_parser.add_argument("dhatu", help="Verbal root (SLP1 or IAST)")
    tin_parser.add_argument("gana", type=int, choices=range(1, 11), help="Gana (1-10)")
    tin_parser.add_argument("prayoga", choices=["Kartari", "Karmani", "Bhave"], help="Voice")
    tin_parser.add_argument("purusha", choices=["Prathama", "Madhyama", "Uttama"], help="Person")
    tin_parser.add_argument("vacana", choices=["Eka", "Dvi", "Bahu"], help="Number")
    tin_parser.add_argument("lakara", help="Lakara (e.g. Lat, Lit, Lut, Lrt, Let, Lot, Lan, AshirLin, VidhiLin, Lun, Lrn)")
    
    args = parser.parse_args()

    if not VIDYUT_AVAILABLE:
        print("Error: vidyut is not installed. Run: uv sync --extra full")
        return 1

    if args.command == "subanta":
        return derive_subanta(args)
    elif args.command == "tinanta":
        return derive_tinanta(args)

    return 1

if __name__ == "__main__":
    sys.exit(main())
