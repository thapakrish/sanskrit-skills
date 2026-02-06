---
name: sloka
description: Detailed analysis of individual Sanskrit verses (shlokas) including anvaya (prose order), padachheda (word-by-word breakdown), chandas (meter), alankara (figures of speech), traditional commentary, and meaning. Use when a user provides a specific verse to analyze or asks to explain a particular shloka. For text-level discussions (author info, plot summaries, literary history), use sahitya instead.
---

# Sloka Analysis

Analyze Sanskrit verses with scholarly rigor, providing layered understanding from literal meaning to literary significance.

## Analysis Workflow (Structural First)

To ensure accuracy, always perform word-level breakdown before syntactical reordering.

1.  **Padachheda (Splitting):** Identify every individual word (pada). If sandhi is present, split it using `sandhi.py` or web search.
2.  **Morphological Analysis:** Identify the gender, case (vibhakti), and number for each noun, and the tense, person, and number for each verb.
3.  **Anvaya (Reordering):** Group adjectives with their nouns and find the verb. Arrange them into a logical prose sequence (Subject -> Object -> Verb).
4.  **Translation & Interpretation:** Only after the structure is clear, provide the English meaning.

## Researcher's Mindset in Sloka Analysis

*   **Transparency:** If you are unsure of a specific word's relationship in the Anvaya, mention it (e.g., "The word X could grammatically qualify either Y or Z; I have chosen Y because...").
*   **Verification:** Use `chandas.py` to verify the meter before stating it. If the meter is irregular or unknown, describe the syllable count and patterns rather than guessing a name.
*   **Provenance:** Cite commentaries (Mallinatha, etc.) if your interpretation follows a specific traditional line.

## Analysis Components

For each sloka, provide these sections in order:

### 1. Mula Sloka (Original Verse)
Display the verse in Devanagari with proper punctuation and diacritical marks.

### 2. Padachheda (Word-by-Word Breakdown)
Break each word and analyze before reordering. This is the foundation of the analysis.

| Word | Root/Stem | Grammar (Vibhakti/Lakara) | Meaning |
|------|-----------|---------------------------|---------|
| संपृक्तौ | सम्+√पृच् | क्त प्रत्यय, द्वि. पुं. | united |

*Note: For complex compounds (Samasa), break them down into their component words.*

### 3. Anvaya (Syntactical Prose Order)
Rearrange the analyzed words into natural prose order showing grammatical relationships:
- Add implied subjects/objects in parentheses: (अहम्), (त्वम्)
- Show case relationships explicitly
- Convert poetic inversions to logical sequence

Example:
```
Verse: वागर्थाविव संपृक्तौ वागर्थप्रतिपत्तये
Anvaya: (अहम्) वागर्थप्रतिपत्तये वाक् अर्थौ इव संपृक्तौ (पार्वतीपरमेश्वरौ वन्दे)
```

### 4. Chandas (Meter Analysis)
Identify and analyze:
- **Meter name**: e.g., अनुष्टुप्, वसन्ततिलका, शार्दूलविक्रीडितम्
- **Characteristics**: syllables per pada, laghu/guru pattern
- **Syllabic breakdown**: Mark ल (laghu) and ग (guru) for each pada

### 5. Alankara (Figures of Speech)
Identify literary devices:
- **Upama** (simile): indicated by इव, यथा, etc.
- **Rupaka** (metaphor)
- **Anuprasa** (alliteration)
- **Yamaka** (repetition with different meanings)

### 6. Commentary (Tika)
Reference authentic commentaries:
- **Mallinatha** (मल्लिनाथ): Sanjivini on Raghuvamsha, Kumarasambhava, Meghaduta
- **Shankaracharya**: Bhagavad Gita Bhashya
- **Vallabhacharya**: Subodhini on Bhagavata
- **Sridhara Swami**: Bhagavata Purana commentary

Summarize key interpretive insights from traditional commentators.

### 7. Saransha (Summary)
Provide:
- **Literal translation** in English
- **Interpretive meaning** with cultural/philosophical context
- **Significance** within the larger text

## Scripts

Utility scripts in `shared/scripts/`:

```bash
cd shared/scripts
uv sync                    # Setup
uv run python chandas.py "<verse>"                    # Meter analysis
uv run python transliterate.py "संस्कृतम्" devanagari iast  # → saṃskṛtam
uv run python sandhi.py --split "<compound>"          # Sandhi splitting
```

## References

For detailed information, see:
- [references/chandas.md](references/chandas.md) - Complete meter patterns and gana system
- [references/alankaras.md](references/alankaras.md) - Figures of speech with examples
- [references/commentators.md](references/commentators.md) - Traditional commentators by text

**Online sources** for authentic commentaries and meter identification:
- sanskritsahitya.org - Sloka database with Mallinatha commentary
- gitasupersite.iitk.ac.in - Bhagavad Gita with multiple commentaries
- github.com/hrishikeshrt/chanda - Deep meter analysis and pattern matching
- wisdomlib.org - Encyclopedia of Sanskrit texts

## Related Skills

| Need | Use |
|------|-----|
| Grammar details (sandhi, vibhakti) | **vyakarana** |
| Word meanings, synonyms | **kosha** |
| About the text/author | **sahitya** |
| Devotional hymn context | **stotra** |
