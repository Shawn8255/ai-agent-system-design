# Contributing

This project is maintained as a bilingual Markdown book.

## Content Layout

- Chinese source lives in `docs/zh`.
- English source lives in `docs/en`.
- Figures live in each language's `assets/` directory.
- DOCX and PDF release artifacts live in `releases/`.

## Editing Guidelines

- Keep Chapters 1-3 unchanged in meaning.
- Edit Chapters 4-6 in the same system-design voice as the existing book.
- Do not add Chapter 7 prose yet.
- Keep planned chapters from Chapter 7 onward as plan entries, not drafted chapters.
- Keep terminology consistent within and across languages.
- When updating one language, check whether the corresponding section in the other language needs an equivalent maintenance change.

## Regenerating Markdown

The current Markdown was extracted from the DOCX sources with:

```bash
python3 tools/docx_to_markdown.py
```

The script overwrites `docs/zh` and `docs/en`. After regeneration, inspect:

- front matter and chapter plan
- terminology tables
- figure links
- Chapters 1-6
- `99-future-chapters.md` to confirm it remains a plan only

## Review Checklist

- No new Chapter 7 or later drafted prose was introduced.
- The bilingual directory structure remains intact.
- Terminology tables are preserved.
- Chapter plan status still marks later chapters as planned/future.
- Figure assets render from relative Markdown links.
