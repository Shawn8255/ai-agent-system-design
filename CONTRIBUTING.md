# Contributing

This project is maintained as a bilingual Markdown book.

## Content Layout

- Chinese source lives in `docs/zh`.
- English source lives in `docs/en`.
- Figures live in each language's `assets/` directory.
- DOCX and PDF release artifacts live in `releases/`.

## Editing Guidelines

- Keep Chapters 1-3 unchanged in meaning.
- Do not add Chapter 4 prose yet.
- Keep planned chapters as plan entries, not drafted chapters.
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
- Chapters 1-3
- `99-future-chapters.md` to confirm it remains a plan only

## Review Checklist

- No new Chapter 4 content was introduced.
- The bilingual directory structure remains intact.
- Terminology tables are preserved.
- Chapter plan status still marks later chapters as planned/future.
- Figure assets render from relative Markdown links.
