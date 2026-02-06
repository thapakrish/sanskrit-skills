---
name: vyakarana
description: Sanskrit grammar analysis including sandhi (euphonic combinations), samasa (compounds), vibhakti (case declensions), dhatu (verbal roots), pratyaya (suffixes), and lakara (tenses/moods). Use when explaining Sanskrit grammar rules, breaking down word formations, analyzing declensions or conjugations, identifying compound types, or teaching Paninian grammar concepts.
---

# Vyakarana (Sanskrit Grammar)

Analyze and explain Sanskrit grammatical constructions following the Paninian tradition.

## Provenance & Accuracy

*   **Narrate:** Explain if you are using a local script (`sandhi.py`), a web lookup (Ashtadhyayi.com), or your own inference.
*   **Verify:** Check derived rules against `references/sandhi.md` or web sources. If a Sutra is not verified, describe the rule phonetically (e.g., "Guṇa: a + i = e") without inventing a Sutra number.
*   **Label:** Clearly mark inferred derivations or simplified analogies (e.g., "This is a simplified explanation...").

## Analysis Workflow

When analyzing a word or explaining grammar:

### 1. Identify the Word Type
- **Subanta** (nominal): Ends in a case suffix (सुप्)
- **Tiganta** (verbal): Ends in a verbal suffix (तिङ्)
- **Avyaya** (indeclinable): No inflection

### 2. For Subanta (Nominals)

```
प्रकृति (stem) + प्रत्यय (suffix) = पद (word)
```

Identify:
- **Pratipadika** (nominal stem)
- **Linga** (gender): पुंल्लिङ्ग, स्त्रीलिङ्ग, नपुंसकलिङ्ग
- **Vacana** (number): एकवचन, द्विवचन, बहुवचन
- **Vibhakti** (case): प्रथमा through सप्तमी + सम्बोधन

### 3. For Tiganta (Verbals)

```
धातु (root) + विकरण (class marker) + तिङ् प्रत्यय (personal ending)
```

Identify:
- **Dhatu** (root) with gana (class 1-10)
- **Lakara** (tense/mood): लट्, लिट्, लुट्, etc.
- **Pada** (voice): परस्मैपद, आत्मनेपद, उभयपद
- **Purusha** (person): प्रथम, मध्यम, उत्तम
- **Vacana** (number)

### 4. For Samasa (Compounds)

Break down showing:
- Component words (पूर्वपद, उत्तरपद)
- Compound type (see references/samasa.md)
- Vigrahavakya (dissolution)

### 5. Apply Sandhi Rules

When forms combine, identify:
- Type of sandhi (स्वर, व्यञ्जन, विसर्ग)
- Rule applied
- Original forms

## Quick Reference Tables

### Vibhakti (Case) Meanings

| Case | Name | Karaka | Meaning | Markers |
|------|------|--------|---------|---------|
| 1 | प्रथमा | कर्ता | subject, nominative | -स्, -औ, -अस् |
| 2 | द्वितीया | कर्म | object, accusative | -अम्, -औ, -अस् |
| 3 | तृतीया | करण | by/with, instrumental | -आ, -भ्याम्, -भिस् |
| 4 | चतुर्थी | सम्प्रदान | to/for, dative | -ए, -भ्याम्, -भ्यस् |
| 5 | पञ्चमी | अपादान | from, ablative | -अस्, -भ्याम्, -भ्यस् |
| 6 | षष्ठी | सम्बन्ध | of, genitive | -अस्, -ओस्, -आम् |
| 7 | सप्तमी | अधिकरण | in/on/at, locative | -इ, -ओस्, -सु |

### Lakara (Tense/Mood) Overview

| Lakara | Name | Usage |
|--------|------|-------|
| लट् | वर्तमान | Present tense |
| लङ् | अनद्यतन भूत | Past (not today) |
| लुङ् | सामान्य भूत | Aorist (general past) |
| लिट् | परोक्ष भूत | Perfect (unwitnessed past) |
| लुट् | अनद्यतन भविष्यत् | Periphrastic future |
| लृट् | सामान्य भविष्यत् | Simple future |
| लोट् | आज्ञा | Imperative |
| विधिलिङ् | विधि | Optative (should) |
| आशीर्लिङ् | आशीः | Benedictive (blessing) |
| लृङ् | सङ्केत | Conditional |

## Scripts

Utility scripts in `shared/scripts/`. Libraries: [indic-transliteration](https://github.com/indic-transliteration/indic_transliteration_py), [sanskrit_parser](https://github.com/kmadathil/sanskrit_parser), [vidyut](https://github.com/ambuda-org/vidyut).

```bash
cd shared/scripts
uv sync                    # Core dependencies
uv sync --extra full       # + sanskrit_parser, vidyut
```

### Usage
```bash
# Transliteration
uv run python transliterate.py "संस्कृतम्" devanagari iast  # → saṃskṛtam
uv run python transliterate.py "rāma" iast devanagari       # → राम

# Sandhi
uv run python sandhi.py --split "devālayaḥ"
uv run python sandhi.py --join "deva" "ālaya"  # → devālaya

# Prakriya (Derivation)
uv run python prakriya.py subanta rAma Pum Prathama Eka
uv run python prakriya.py tinanta gam 1 Kartari Prathama Eka Lat

# Dhatu lookup
uv run python dhatu.py bhū
uv run python dhatu.py --gana 1
uv run python dhatu.py --search "to go"
```

## References

For detailed rules, see:
- [references/sandhi.md](references/sandhi.md) - Euphonic combination rules
- [references/samasa.md](references/samasa.md) - Compound types with examples
- [references/vibhakti.md](references/vibhakti.md) - Declension paradigms
- [references/dhatu.md](references/dhatu.md) - Common verbal roots by gana
- [references/pratyaya.md](references/pratyaya.md) - Krit and Taddhita suffixes
- [references/lakara.md](references/lakara.md) - Conjugation paradigms

## Example Analysis

**Word**: गच्छति

**Analysis**:
```
धातु: √गम् (गतौ) - 1st gana (भ्वादि)
विकरण: शप् (→ अ)
लकार: लट् (वर्तमान)
पद: परस्मैपद
पुरुष: प्रथम
वचन: एकवचन

Formation: गम् + शप् + ति
           गम् + अ + ति
           गच्छ् + अ + ति  (म् → च्छ् by गमॢ॰॰॰ rule)
           = गच्छति
```

**Word**: राज्ञः

**Analysis**:
```
प्रातिपदिक: राजन् (m. king)
लिङ्ग: पुंल्लिङ्ग
वचन: एकवचन
विभक्ति: षष्ठी (genitive) OR पञ्चमी (ablative)

Formation: राजन् + अस् (षष्ठी/पञ्चमी एकवचन)
           राज् + ञ् + अस् (न् → ञ् before अस्)
           = राज्ञस् → राज्ञः (विसर्ग)
```

**Compound**: नीलोत्पलम्

**Analysis**:
```
समास: कर्मधारय (विशेषणपूर्वपद)
विग्रह: नीलम् उत्पलम् (a blue lotus)
पूर्वपद: नील (adj. blue)
उत्तरपद: उत्पल (n. lotus)
सन्धि: नील + उत्पल → नीलोत्पल (गुण सन्धि: अ + उ = ओ)
```

## Related Skills

| Need | Use |
|------|-----|
| Full verse analysis | **sloka** |
| Word meanings, synonyms | **kosha** |
| Literary context | **sahitya** |
| Shared scripts/references | **shared** |
