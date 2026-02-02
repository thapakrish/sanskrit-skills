---
name: sanskrit-shared
description: Shared Sanskrit resources including Devanagari script guide, transliteration systems, terminology glossary, online resources, and Python utility scripts. Use for script conversion, general Sanskrit reference, or when other skills need common resources.
---

# Shared Sanskrit Resources

Common reference materials and tools used across all Sanskrit skills.

## Reference Files

| File | Contents |
|------|----------|
| [devanagari.md](devanagari.md) | Vowels, consonants, conjuncts, numerals, pronunciation |
| [transliteration.md](transliteration.md) | IAST, Harvard-Kyoto, ITRANS, SLP1, Velthuis systems |
| [terminology.md](terminology.md) | 150+ common terms (grammar, prosody, poetics, philosophy) |
| [online-resources.md](online-resources.md) | Curated platforms, dictionaries, tools, academic resources |

## Scripts

Python utilities in `shared/scripts/`. Setup:

```bash
cd shared/scripts
uv sync                  # Core dependencies
uv sync --extra full     # Include sanskrit_parser, vidyut
```

### Available Tools

| Script | Purpose | Example |
|--------|---------|---------|
| `transliterate.py` | Script conversion | `uv run python transliterate.py "राम" devanagari iast` → `rāma` |
| `sandhi.py` | Sandhi split/join | `uv run python sandhi.py --join "deva" "ālaya"` → `devālaya` |
| `dhatu.py` | Verbal root lookup | `uv run python dhatu.py bhū` |
| `chandas.py` | Meter detection | `uv run python chandas.py "<verse>"` |

### Libraries Used

| Library | Purpose |
|---------|---------|
| [indic-transliteration](https://github.com/indic-transliteration/indic_transliteration_py) | 15+ script conversions |
| [sanskrit_parser](https://github.com/kmadathil/sanskrit_parser) | Sandhi splitting, morphology |
| [vidyut](https://github.com/ambuda-org/vidyut) | Prakriya, kosha (Ambuda project) |

## Online Platforms

| Platform | Best For |
|----------|----------|
| **ambuda.org** | Text library, volunteer-proofed |
| **sanskritsahitya.org** | Kavya + Mallinatha commentary, AI search |
| **ashtadhyayi.com** | Paninian grammar, prakriya, dhatu patha |
| **dharmamitra.org** | Buddhist texts, AI translation, OCR |

## Quick Transliteration Reference

| Devanagari | IAST | HK | ITRANS |
|------------|------|-----|--------|
| अ आ इ ई | a ā i ī | a A i I | a A i I |
| उ ऊ ऋ | u ū ṛ | u U R | u U RRi |
| ए ऐ ओ औ | e ai o au | e ai o au | e ai o au |
| क ख ग घ | k kh g gh | k kh g gh | k kh g gh |
| ट ठ ड ढ ण | ṭ ṭh ḍ ḍh ṇ | T Th D Dh N | T Th D Dh N |
| श ष स | ś ṣ s | z S s | sh Sh s |
| ं ः | ṃ ḥ | M H | M H |
