# Contributing

This project is maintained as a bilingual Markdown book.

## Content Layout

- Chinese source lives in `docs/zh`.
- English source lives in `docs/en`.
- Figures live in each language's `assets/` directory.
- DOCX and PDF release artifacts live in `releases/`.

## Editing Guidelines

- Keep Chapters 1-3 unchanged in meaning.
- Edit Chapters 4-13 in the same system-design voice as the existing book.
- Do not add new chapters beyond Chapter 13 without first proposing the chapter plan in both languages.
- Keep terminology consistent within and across languages.
- When updating one language, check whether the corresponding section in the other language needs an equivalent maintenance change.

## Contribution Scope

Good contributions include typo fixes, broken-link fixes, terminology consistency fixes, citations, small examples, and translation improvements. Larger structural changes should start as an issue so the authorial voice and chapter flow remain coherent.

The current manuscript is a single-author technical book rather than an open-ended wiki. Community changes should strengthen the existing line of argument instead of replacing the chapter structure.

## Regenerating Markdown

The current Markdown was extracted from the DOCX sources with:

```bash
python3 tools/docx_to_markdown.py
```

The script overwrites `docs/zh` and `docs/en`. After regeneration, inspect:

- front matter and chapter plan
- terminology tables
- figure links
- Chapters 1-13
- `99-future-chapters.md` to confirm it remains future revision notes only

## Review Checklist

- No new Chapter 14 or later drafted prose was introduced.
- The bilingual directory structure remains intact.
- Terminology tables are preserved.
- Chapter plan status marks Chapters 1-13 consistently across both languages.
- Figure assets render from relative Markdown links.
- Release artifacts are regenerated only when the Markdown source changed intentionally.
