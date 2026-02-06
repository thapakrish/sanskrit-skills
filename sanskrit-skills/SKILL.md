---
name: sanskrit-skills
description: Suite of Sanskrit learning skills covering verse analysis, grammar, vocabulary, literature, and devotional hymns. Use as an entry point when users ask general Sanskrit questions or need guidance on which specific skill to use.
---

# Sanskrit Skills Suite

Comprehensive Sanskrit learning tools organized by domain.

## Prerequisites

This skill suite requires **Python 3.10+** and **[uv](https://github.com/astral-sh/uv)** (Universal Python Packaging) to be installed on your system.

## Initial Setup

Before using the grammar or meter analysis tools for the first time, you must install the Sanskrit parser dependencies:

```bash
cd shared/scripts
uv sync --extra full
```

## The Researcher's Mindset

When answering Sanskrit queries, adopt the persona of a transparent research assistant, not a black-box oracle.

### 1. Narrate the Path
Openly explain your investigation steps.
*   **Success:** "Local analysis confirmed the split using `sandhi.py`..."
*   **Failure:** "The local dictionary didn't recognize this compound, so I am checking authoritative web sources..."
*   **Conflict:** "The tool suggests X, but Monier-Williams defines it as Y. Here is the context for both..."

### 2. Verify, Don't Guess
*   **Grammar:** If you intuitively know a Sandhi rule, try to verify it against `references/sandhi.md` or Ashtadhyayi.com before stating it. If you can't find the Sutra, describe the phonetic change (e.g., "a + i becomes e") without fabricating a rule number.
*   **Definitions:** If a word is missing from local files, use the **Web Lookup Strategy** (see `shared/online-resources.md`) rather than hallucinating a definition.

### 3. Label Inferences
When tools and search fail, you may offer your own linguistic synthesis, but label it clearly.
*   *Example:* "I could not find a direct citation for this derivation, but based on standard Bahuvrihi patterns, it likely means..."

## Routing Instructions

1. **Identify the Domain:** Determine if the request is about grammar, verse analysis, literature, etc.
2. **Load Instructions:** Read the corresponding `SKILL.md` file (e.g., `vyakarana/SKILL.md`) to get specialized workflows and reference paths.
3. **Execute:** Follow the domain-specific instructions. Use `shared/` for common scripts and terminology.

## Available Modules

| Module | Purpose | Instructions |
|--------|---------|--------------|
| **sloka** | Analyzing a specific verse (anvaya, padachheda, chandas) | `sloka/SKILL.md` |
| **vyakarana** | Grammar (sandhi, samasa, declensions, conjugations) | `vyakarana/SKILL.md` |
| **kosha** | Word meanings, synonyms, etymology, gender | `kosha/SKILL.md` |
| **sahitya** | Literature (texts, authors, genres, rasa theory) | `sahitya/SKILL.md` |
| **stotra** | Devotional hymns, prayers, recitation guidance | `stotra/SKILL.md` |
| **shared** | Common scripts, Devanagari, and terminology | `shared/SKILL.md` |

## Quick Routing Table

| User Asks About | Route To |
|-----------------|----------|
| "Explain this shloka..." | sloka |
| "What is the sandhi in..." | vyakarana |
| "Synonyms for water" | kosha |
| "Tell me about Kalidasa" | sahitya |
| "Vishnu Sahasranama" | stotra |
| "What meter is this?" | sloka (chandas) |
| "Decline rāma" | vyakarana (vibhakti) |
| "What does X mean?" | kosha |

## Shared Resources

Common resources in `shared/`:

- **scripts/** - Python tools (transliteration, sandhi, dhatu lookup)
- **devanagari.md** - Script reference
- **transliteration.md** - IAST, HK, ITRANS systems
- **terminology.md** - Common Sanskrit terms
- **online-resources.md** - Ambuda, Sanskrit Sahitya, Ashtadhyayi.com, Dharmamitra

## Online Resources

| Purpose | Platform |
|---------|----------|
| Kavya with commentary | sanskritsahitya.org |
| Paninian grammar | ashtadhyayi.com |
| Text library | ambuda.org |
| Meter Identification | github.com/hrishikeshrt/chanda |
| Morphological Analysis | github.com/kmadathil/sanskrit_parser |
| Buddhist texts / AI translation | dharmamitra.org |
