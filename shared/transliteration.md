# Sanskrit Transliteration Systems

## Overview

Multiple systems exist for representing Sanskrit in Roman script. IAST is the scholarly standard.

---

## IAST (International Alphabet of Sanskrit Transliteration)

The **standard** for academic work.

### Vowels

| Devanagari | IAST | Notes |
|------------|------|-------|
| अ | a | short |
| आ | ā | long (macron) |
| इ | i | short |
| ई | ī | long |
| उ | u | short |
| ऊ | ū | long |
| ऋ | ṛ | vocalic r (short) |
| ॠ | ṝ | vocalic r (long) |
| ऌ | ḷ | vocalic l (rare) |
| ए | e | always long |
| ऐ | ai | diphthong |
| ओ | o | always long |
| औ | au | diphthong |

### Consonants

| Devanagari | IAST | Notes |
|------------|------|-------|
| क ख ग घ ङ | k kh g gh ṅ | velars |
| च छ ज झ ञ | c ch j jh ñ | palatals |
| ट ठ ड ढ ण | ṭ ṭh ḍ ḍh ṇ | retroflexes (underdot) |
| त थ द ध न | t th d dh n | dentals |
| प फ ब भ म | p ph b bh m | labials |
| य र ल व | y r l v | semivowels |
| श ष स | ś ṣ s | sibilants |
| ह | h | aspirate |
| ं | ṃ | anusvara |
| ः | ḥ | visarga |

### Key IAST Features
- Macrons (ā, ī, ū) for long vowels
- Underdots (ṭ, ḍ, ṇ, ṣ, ṛ, ḷ) for retroflexes
- Acute accent (ś) for palatal sibilant
- Tilde (ñ) for palatal nasal

---

## Harvard-Kyoto (HK)

ASCII-only system for digital use.

| Devanagari | IAST | HK |
|------------|------|-----|
| आ | ā | A |
| ई | ī | I |
| ऊ | ū | U |
| ऋ | ṛ | R |
| ॠ | ṝ | RR |
| ऌ | ḷ | lR |
| ऐ | ai | ai |
| औ | au | au |
| ङ | ṅ | G |
| ञ | ñ | J |
| ट | ṭ | T |
| ठ | ṭh | Th |
| ड | ḍ | D |
| ढ | ḍh | Dh |
| ण | ṇ | N |
| श | ś | z |
| ष | ṣ | S |
| ं | ṃ | M |
| ः | ḥ | H |

**Example**:
- IAST: saṃskṛtam
- HK: saMskRtam

---

## ITRANS

Popular for typing Sanskrit online.

| Devanagari | IAST | ITRANS |
|------------|------|--------|
| आ | ā | A or aa |
| ई | ī | I or ii |
| ऊ | ū | U or uu |
| ऋ | ṛ | RRi or R^i |
| ऐ | ai | ai |
| औ | au | au |
| ङ | ṅ | ~N or N^ |
| ञ | ñ | ~n or n^ |
| ट | ṭ | T |
| ठ | ṭh | Th |
| ड | ḍ | D |
| ढ | ḍh | Dh |
| ण | ṇ | N |
| श | ś | sh |
| ष | ṣ | Sh or shh |
| ं | ṃ | M or .m |
| ः | ḥ | H or .h |

**Example**:
- IAST: saṃskṛtam
- ITRANS: sa.nskRRitam or saMskRitam

---

## Velthuis

Another ASCII system.

| Devanagari | IAST | Velthuis |
|------------|------|----------|
| आ | ā | aa |
| ई | ī | ii |
| ऊ | ū | uu |
| ऋ | ṛ | .r |
| ॠ | ṝ | .rr |
| ऌ | ḷ | .l |
| ङ | ṅ | "n |
| ञ | ñ | ~n |
| ट | ṭ | .t |
| ठ | ṭh | .th |
| ड | ḍ | .d |
| ढ | ḍh | .dh |
| ण | ṇ | .n |
| श | ś | "s |
| ष | ṣ | .s |
| ं | ṃ | .m |
| ः | ḥ | .h |

---

## SLP1 (Sanskrit Library Phonetic)

Bijective system (one-to-one mapping) for computational work.

| Devanagari | IAST | SLP1 |
|------------|------|------|
| अ | a | a |
| आ | ā | A |
| इ | i | i |
| ई | ī | I |
| उ | u | u |
| ऊ | ū | U |
| ऋ | ṛ | f |
| ॠ | ṝ | F |
| ऌ | ḷ | x |
| ए | e | e |
| ऐ | ai | E |
| ओ | o | o |
| औ | au | O |
| क | k | k |
| ख | kh | K |
| ग | g | g |
| घ | gh | G |
| ङ | ṅ | N |
| श | ś | S |
| ष | ṣ | z |
| स | s | s |

---

## Comparison Table

| Devanagari | IAST | HK | ITRANS | Velthuis | SLP1 |
|------------|------|-----|--------|----------|------|
| संस्कृतम् | saṃskṛtam | saMskRtam | sa.nskRRitam | sa.msk.rtam | saMskftam |
| शिव | śiva | ziva | shiva | "siva | Siva |
| विष्णु | viṣṇu | viSNu | viShNu | vi.s.nu | vizRu |
| कृष्ण | kṛṣṇa | kRSNa | kRRiShNa | k.r.s.na | kfzRa |

---

## Choosing a System

| Purpose | Recommended |
|---------|-------------|
| Academic papers | IAST |
| Digital text (ASCII) | Harvard-Kyoto |
| Online typing | ITRANS |
| Computational work | SLP1 |
| Casual use | Any consistent system |

---

## Unicode Input

### IAST Characters

| Character | Unicode | HTML |
|-----------|---------|------|
| ā | U+0101 | &amacr; |
| ī | U+012B | ī |
| ū | U+016B | ū |
| ṛ | U+1E5B | ṛ |
| ṝ | U+1E5D | ṝ |
| ḷ | U+1E37 | ḷ |
| ṃ | U+1E43 | ṃ |
| ḥ | U+1E25 | ḥ |
| ṅ | U+1E45 | ṅ |
| ñ | U+00F1 | &ntilde; |
| ṭ | U+1E6D | ṭ |
| ḍ | U+1E0D | ḍ |
| ṇ | U+1E47 | ṇ |
| ś | U+015B | ś |
| ṣ | U+1E63 | ṣ |

---

## Conversion Tools

Online converters:
- Sanscript.js (JavaScript library)
- Sanskrit Dictionary tools
- Aksharamukha (multi-script)
