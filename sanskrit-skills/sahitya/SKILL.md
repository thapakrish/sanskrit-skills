---
name: sahitya
description: Sanskrit literature guide for text-level discussions — plot summaries, author biographies, literary genres, kavya theory (rasa, dhvani, alankara schools). Use when asking about poets (Kalidasa, Bharavi), texts as wholes (what is Meghaduta about?), literary history, or aesthetic theory. For analyzing a specific verse, use sloka instead.
---

# Sahitya (Sanskrit Literature)

Guide to Sanskrit literary tradition: texts, authors, genres, and aesthetics.

## Literary Genres

### काव्य (Poetry)

| Type | Description | Examples |
|------|-------------|----------|
| **महाकाव्य** | Epic poem (8+ sargas) | रघुवंशम्, कुमारसम्भवम् |
| **खण्डकाव्य** | Minor poem | मेघदूतम्, ऋतुसंहारम् |
| **मुक्तक** | Standalone verses | अमरुशतकम्, भर्तृहरिशतकत्रयम् |
| **चम्पू** | Mixed prose-verse | नलचम्पूः |

### नाटक (Drama)

| Type | Description | Examples |
|------|-------------|----------|
| **नाटक** | 5-10 acts, heroic theme | अभिज्ञानशाकुन्तलम् |
| **प्रकरण** | Invented plot | मृच्छकटिकम् |
| **भाण** | One-act monologue | — |
| **प्रहसन** | Farce/comedy | मत्तविलासप्रहसनम् |

### गद्य (Prose)

| Type | Description | Examples |
|------|-------------|----------|
| **आख्यायिका** | Romance/adventure | कादम्बरी, हर्षचरितम् |
| **कथा** | Story collection | पञ्चतन्त्रम्, हितोपदेशः |

## The Five Mahakavyas

| # | Text | Author | Subject | Sargas |
|---|------|--------|---------|--------|
| 1 | रघुवंशम् | कालिदास | Raghu dynasty | 19 |
| 2 | कुमारसम्भवम् | कालिदास | Birth of Kartikeya | 17 (8 authentic) |
| 3 | किरातार्जुनीयम् | भारवि | Arjuna vs Shiva | 18 |
| 4 | शिशुपालवधम् | माघ | Killing of Shishupala | 20 |
| 5 | नैषधीयचरितम् | श्रीहर्ष | Nala-Damayanti | 22 |

## Major Authors

### कालिदासः (Kalidasa) — c. 4th-5th century CE

**"The Shakespeare of Sanskrit"**

| Work | Genre | Theme |
|------|-------|-------|
| रघुवंशम् | महाकाव्य | Raghu dynasty from Dilipa to Agnivarna |
| कुमारसम्भवम् | महाकाव्य | Shiva-Parvati marriage, Kartikeya's birth |
| मेघदूतम् | खण्डकाव्य | Yaksha's message via cloud |
| ऋतुसंहारम् | खण्डकाव्य | Six seasons |
| अभिज्ञानशाकुन्तलम् | नाटक | Dushyanta-Shakuntala love story |
| विक्रमोर्वशीयम् | नाटक | Pururavas-Urvashi love story |
| मालविकाग्निमित्रम् | नाटक | Agnimitra-Malavika romance |

**Style**: माधुर्य (sweetness), उपमा mastery, nature imagery

### Other Major Poets

See [references/authors.md](references/authors.md) for complete profiles.

## References

Detailed information:
- [references/mahakavyas.md](references/mahakavyas.md) - Epic poems with sarga summaries
- [references/natakas.md](references/natakas.md) - Drama tradition and major plays
- [references/authors.md](references/authors.md) - Poet biographies and styles
- [references/rasa.md](references/rasa.md) - Aesthetic theory (rasa, dhvani)

## Rasa Theory (Quick Reference)

The nine rasas (aesthetic emotions):

| Rasa | Emotion | Sthayibhava | Color | Deity |
|------|---------|-------------|-------|-------|
| शृङ्गार | Erotic | रति (love) | श्याम | विष्णु |
| हास्य | Comic | हास (mirth) | सित | प्रमथ |
| करुण | Pathetic | शोक (sorrow) | कपोत | यम |
| रौद्र | Furious | क्रोध (anger) | रक्त | रुद्र |
| वीर | Heroic | उत्साह (energy) | गौर | इन्द्र |
| भयानक | Terrible | भय (fear) | कृष्ण | काल |
| बीभत्स | Odious | जुगुप्सा (disgust) | नील | महाकाल |
| अद्भुत | Marvelous | विस्मय (wonder) | पीत | ब्रह्मा |
| शान्त | Peaceful | शम (tranquility) | स्फटिक | नारायण |

## Kavya Definition

> शब्दार्थौ सहितौ काव्यम् — "Word and meaning united is poetry"
> — Bhamaha

> रसात्मकं वाक्यं काव्यम् — "Poetry is language ensouled with rasa"
> — Vishvanatha

## Famous Opening Verses

| Text | Opening |
|------|---------|
| रघुवंशम् | वागर्थाविव संपृक्तौ... |
| कुमारसम्भवम् | अस्त्युत्तरस्यां दिशि देवतात्मा... |
| मेघदूतम् | कश्चित्कान्ताविरहगुरुणा... |
| शाकुन्तलम् | या सृष्टिः स्रष्टुराद्या... |
| किरातार्जुनीयम् | श्रियः कुरूणामधिपस्य पालनीम्... |

## Scripts

Utilities in `shared/scripts/`:

```bash
cd shared/scripts && uv sync
```

| Script | Use |
|--------|-----|
| `transliterate.py` | Convert text between scripts |
| `chandas.py` | Identify meter of sample verses |

## Related Skills

| Need | Use |
|------|-----|
| Analyze specific verse | **sloka** |
| Grammar questions | **vyakarana** |
| Word meanings | **kosha** |
| Devotional hymns | **stotra** |
