---
name: sloka-analysis
description: Detailed analysis of individual Sanskrit verses (shlokas) including anvaya (prose order), padachheda (word-by-word breakdown), chandas (meter), alankara (figures of speech), traditional commentary, and meaning. Use when a user provides a specific verse to analyze or asks to explain a particular shloka. For text-level discussions (author info, plot summaries, literary history), use sahitya instead.
---

# Sloka Analysis

Analyze Sanskrit verses with scholarly rigor, providing layered understanding from literal meaning to literary significance.

## Analysis Components

For each sloka, provide these sections in order:

### 1. Mula Sloka (Original Verse)
Display the verse in Devanagari with proper punctuation and diacritical marks.

### 2. Anvaya (Syntactical Prose Order)
Rearrange words into natural prose order showing grammatical relationships:
- Add implied subjects/objects in parentheses: (अहम्), (त्वम्)
- Show case relationships explicitly
- Convert poetic inversions to logical sequence

Example:
```
Verse: वागर्थाविव संपृक्तौ वागर्थप्रतिपत्तये
Anvaya: (अहम्) वागर्थप्रतिपत्तये वाक् अर्थौ इव संपृक्तौ (पार्वतीपरमेश्वरौ वन्दे)
```

### 3. Padachheda (Word Analysis)
Break each word with:

| Word | Root | Formation | Grammar | Meaning |
|------|------|-----------|---------|---------|
| संपृक्तौ | सम्+√पृच् | सम्√पृच्+क्त | द्विवचन, पुल्लिङ्ग | united/joined |

Include:
- **Dhatu** (verbal root) with gana
- **Pratyaya** (suffix) used
- **Vibhakti** (case) and **Vacana** (number)
- **Linga** (gender)
- **Samasa** (compound) type if applicable

### 4. Chandas (Meter Analysis)
Identify and analyze:
- **Meter name**: e.g., अनुष्टुप्, वसन्ततिलका, शार्दूलविक्रीडितम्
- **Characteristics**: syllables per pada, laghu/guru pattern
- **Syllabic breakdown**: Mark ल (laghu) and ग (guru) for each pada

Example:
```
Meter: अनुष्टुप् (8 syllables per pada)
Pattern per half-verse: ग ग ल ग | ल ग ल ग
```

### 5. Alankara (Figures of Speech)
Identify literary devices:
- **Upama** (simile): indicated by इव, यथा, etc.
- **Rupaka** (metaphor)
- **Anuprasa** (alliteration)
- **Yamaka** (repetition with different meanings)
- **Arthantaranyasa**, **Svabhavokti**, etc.

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

**Online sources** for authentic commentaries:
- sanskritsahitya.org - Sloka database with Mallinatha commentary
- gitasupersite.iitk.ac.in - Bhagavad Gita with multiple commentaries
- wisdomlib.org - Encyclopedia of Sanskrit texts

## Example Analysis

**Input**: वागर्थाविव संपृक्तौ वागर्थप्रतिपत्तये। जगतः पितरौ वन्दे पार्वतीपरमेश्वरौ॥

**Output**:

### मूलश्लोकः
वागर्थाविव संपृक्तौ वागर्थप्रतिपत्तये।
जगतः पितरौ वन्दे पार्वतीपरमेश्वरौ॥

### अन्वयः
(अहम्) वागर्थप्रतिपत्तये वाक् अर्थौ इव संपृक्तौ जगतः पितरौ पार्वतीपरमेश्वरौ वन्दे।

### पदच्छेदः
| पदम् | धातु/प्रकृति | प्रत्ययः | व्याकरणम् | अर्थः |
|------|-------------|----------|-----------|-------|
| वागर्थौ | वाच्+अर्थ | द्वन्द्व समास | द्विवचन | word and meaning |
| इव | अव्ययम् | - | - | like, as |
| संपृक्तौ | सम्+√पृच् | क्त | द्वि., पुं. | united |
| वागर्थप्रतिपत्तये | वाच्+अर्थ+प्रतिपत्ति | तत्पुरुष | चतुर्थी, एक. | for understanding word-meaning |
| जगतः | जगत् | - | षष्ठी, एक. | of the world |
| पितरौ | पितृ | - | द्वि., पुं. | parents |
| वन्दे | √वन्द् | लट्, आत्मनेपद | उत्तम, एक. | I salute |
| पार्वतीपरमेश्वरौ | पार्वती+परमेश्वर | द्वन्द्व | द्वि., पुं. | Parvati and Parameshwara |

### छन्दः
**वृत्तम्**: अनुष्टुप् (श्लोक)
**लक्षणम्**: प्रतिपादं अष्टाक्षराणि
**विश्लेषणम्**:
```
वा गर् था वि व सं पृ क्तौ = ग ग ग ल ल ग ल ग
वा गर् थ प्र ति प त्त ये = ग ग ल ल ल ग ग ग
```

### अलङ्कारः
**उपमा**: वाक् च अर्थः च इव संपृक्तौ - Parvati and Parameshwara are compared to word and meaning, inseparably united.

### टीका (मल्लिनाथः)
The poet invokes the divine parents through the simile of word and meaning - just as word cannot exist without meaning nor meaning without word, Shiva and Shakti are eternally united. This mangalacharana seeks blessings for proper expression (vak) aligned with intended meaning (artha).

### सारांशः
**Literal**: "For the correct understanding of word and meaning, I salute the parents of the world, Parvati and Parameshwara, who are united like word and meaning."

**Significance**: This is the opening verse (mangalacharana) of Kalidasa's Raghuvamsha. The poet seeks divine blessing for his poetic endeavor, cleverly choosing a simile that reflects his concern as a poet - the unity of expression and meaning.

## Related Skills

| Need | Use |
|------|-----|
| Grammar details (sandhi, vibhakti) | **vyakarana** |
| Word meanings, synonyms | **kosha** |
| About the text/author | **sahitya** |
| Devotional hymn context | **stotra** |
