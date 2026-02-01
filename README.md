# Sanskrit Skills Suite for AI Agents

A comprehensive suite of Agent Skills for learning, analyzing, and exploring Sanskrit language and literature. This project follows the open Agent Skill format, making it compatible with any supported AI agent or CLI environment.

This suite transforms your AI assistant into a knowledgeable Sanskrit tutor, capable of analyzing verses, explaining complex grammar, looking up vocabulary, and discussing literature with scholarly depth.

## Features

- **🔎 Sloka Analysis (`sloka-analysis`)**
  - Break down verses (Padachheda) & rearrange syntax (Anvaya).
  - Identify meters (Chandas) automatically using Python algorithms.
  - Explain figures of speech (Alankaras) and traditional commentaries.

- **📚 Grammar Engine (`vyakarana`)**
  - Paninian grammar analysis (Sandhi, Samasa, Vibhakti).
  - Verb conjugation (Tiganta) and noun declension (Subanta) tables.
  - Powered by `sanskrit_parser` and `vidyut`.

- **📖 Lexicon (`kosha`)**
  - Word meanings, genders, and etymology (Nirukta).
  - Synonyms (Paryaya) based on Amarakosha.

- **📜 Literature (`sahitya` & `stotra`)**
  - Detailed info on Mahakavyas, Natakas, and authors.
  - Devotional hymns (Stotras) with recitation guidance.

## Prerequisites

1.  **AI Agent CLI**: Ensure you have the latest version.
2.  **Python 3.10+**: Required for the utility scripts.
3.  **[uv](https://github.com/astral-sh/uv)**: Universal Python Packaging tool (required for dependency management).
    - Install via: `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `pip install uv`)

## Installation

Install the suite using your agent's skill management tool. For environments supporting the `skills` registry:

```bash
npx skills add https://github.com/thapakrish/sanskrit-skills --skill sanskrit-skills
```

## First-Time Setup

After installation, you must initialize the Python environment to enable the grammar and meter engines.

1.  Ask your agent: *"Setup the Sanskrit environment"*
2.  Or manually run:

```bash
cd shared/scripts
uv sync --extra full
```

This installs powerful libraries like `sanskrit_parser`, `indic_transliteration`, and `vidyut`.

## Usage Examples

Once installed, just ask questions naturally!

- **Verse Analysis**:
  > "Analyze this shloka: वागर्थाविव संपृक्तौ..."
  > "What meter is verse 1.1 of Raghuvamsha?"

- **Grammar**:
  > "Explain the sandhi in 'devālayaḥ'"
  > "Decline the word 'rāma' in all cases"
  > "What is the root of 'gacchati'?"

- **Literature**:
  > "Tell me about Kalidasa's works."
  > "List synonyms for 'lotus' from Amarakosha."

## Architecture

This project uses a **Suite Architecture**.
- **`SKILL.md` (Root)**: The Router. It decides which sub-skill to load.
- **`shared/scripts/`**: Central Python logic used by all skills.
- **`vyakarana/`, `kosha/`, etc.**: Specialized instruction sets.

## License

MIT
