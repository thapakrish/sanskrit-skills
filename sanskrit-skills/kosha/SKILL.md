---
name: kosha
description: Sanskrit vocabulary and lexicon skill covering word meanings, synonyms (paryaya), etymology (nirukta), gender, and technical terminology. Based on Amarakosha and traditional lexicography. Use when looking up Sanskrit word meanings, finding synonyms, explaining word derivations, identifying gender of nouns, or exploring vocabulary by category (gods, nature, body parts, etc.).
---

# Kosha (Sanskrit Lexicon)

Provide vocabulary assistance based on traditional Sanskrit lexicography, especially the Amarakosha.

## Workflow

When explaining a word:

### 1. Basic Entry
```
Word: सूर्यः
Gender: पुंल्लिङ्ग (masculine)
Meaning: The sun
Category: ज्योतिष/खगोल (Astronomy)
```

### 2. Paryaya (Synonyms)
List synonyms from Amarakosha tradition:
```
सूर्यः = आदित्यः, दिवाकरः, भास्करः, रविः,
        भानुः, अर्कः, मार्तण्डः, सविता,
        पूषा, मिहिरः, तपनः, प्रभाकरः
```

### 3. Nirukta (Etymology)
Explain derivation:
```
सूर्य = सृ (to move) + क्यप् → "one who moves (across the sky)"
दिवाकर = दिवा + कर → "day-maker"
भास्कर = भास् + कर → "light-maker"
```

### 4. Usage Context
Note any special usages, compounds, or literary significance.

## Coverage & Online Fallback Policy

The local markdown references are curated and intentionally finite. If a requested word is missing, use this fallback chain:

1. **Local first (required):** check `references/paryaya.md` and `references/amarakosha.md`.
2. **Normalize before declaring miss:** handle common script/transliteration variants (Devanagari/IAST/HK).
3. **Trusted web lookup (fallback):** consult authoritative lexical sources (e.g., Cologne/Monier-Williams, Apte, Ambuda, DSAL-backed dictionaries).
4. **Return with provenance:** each synonym set must include source label + link.
5. **Confidence note:** mark output as:
   - `exact_headword_match`
   - `lemma_or_inferred_match`
   - `not_found_in_curated_amarakosha`

### Source Quality Rules

- Prefer primary lexicons/dictionaries first for lexical evidence: Cologne (MW), Apte, DSAL, and Ambuda lexicons.
- Treat secondary portals (e.g., general aggregators, blog-style explainers) as supplementary only.
- Avoid unverified blogs/forum posts as primary evidence.
- If sources disagree, show the overlap first, then source-specific variants.
- If no reliable source is found, say so explicitly instead of guessing.

## Quick Lookup Format

For simple queries, provide concise entries:

| Word | Gender | Meaning | Key Synonyms |
|------|--------|---------|--------------|
| अग्निः | पुं. | fire | वह्निः, पावकः, हुताशनः |
| जलम् | न. | water | वारि, नीरम्, अम्बु, उदकम् |
| वायुः | पुं. | wind | पवनः, मारुतः, अनिलः |

## References

Detailed vocabulary by category:
- [references/amarakosha.md](references/amarakosha.md) - Organized by Amarakosha structure
- [references/paryaya.md](references/paryaya.md) - Comprehensive synonym lists
- [references/nirukta.md](references/nirukta.md) - Common etymologies
- [references/linganushasana.md](references/linganushasana.md) - Gender rules

## Amarakosha Structure

The Amarakosha (अमरकोशः) by Amarasimha has three kandas:

### 1. स्वर्गादिकाण्ड (Heavenly)
- देवता (Gods), दिक् (Directions), काल (Time)

### 2. भूम्यादिकाण्ड (Earthly)
- भूमि (Earth), नगर (City), वनस्पति (Plants), मृग (Animals), मनुष्य (Humans)

### 3. सामान्यादिकाण्ड (General)
- विशेष्य-विशेषण (Noun-Adjective), नानार्थ (Polysemous), अव्यय (Indeclinables)

## Gender Quick Rules

### Generally Masculine (पुंल्लिङ्ग)
- Mountains, oceans, days of week, trees (as individuals), agent nouns

### Generally Feminine (स्त्रीलिङ्ग)
- Rivers, abstract nouns in -ति/-ता, creepers, earth

### Generally Neuter (नपुंसकलिङ्ग)
- Fruits, metals, many body parts, abstract concepts (सुखम्, दुःखम्)

## Example Entry

**Query**: Synonyms for "moon"

### चन्द्रः (Moon) — पुंल्लिङ्ग

| Sanskrit | Etymology | Meaning |
|----------|-----------|---------|
| चन्द्रः | √चन्द् + रक् | the shining one |
| इन्दुः | √उन्द् | the moist one |
| कुमुदबान्धवः | कुमुद + बान्धव | friend of water-lilies |
| विधुः | √व्यध् | the piercer (of darkness) |
| सुधांशुः | सुधा + अंशु | having nectar-rays |
| निशाकरः | निशा + कर | night-maker |
| शशाङ्कः | शश + अङ्क | hare-marked |
| मृगाङ्कः | मृग + अङ्क | deer-marked |
| सोमः | √सु | the Soma |

## Scripts

Utilities in `shared/scripts/`:

```bash
cd shared/scripts && uv sync
```

| Script | Use |
|--------|-----|
| `transliterate.py` | Convert between Devanagari/IAST/HK |
| `dhatu.py` | Look up verbal roots (for etymology) |

## Related Skills

| Need | Use |
|------|-----|
| Grammar analysis | **vyakarana** |
| Verse analysis | **sloka** |
| Literary context | **sahitya** |
