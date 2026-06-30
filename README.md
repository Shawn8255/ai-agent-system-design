# AI Agent System Design

A bilingual technical book about AI Agent system design from the perspective of classical computer engineering.

This repository now keeps the editable book source in Markdown, extracted from the DOCX releases for Part I, Chapters 1-3.

## Languages

- [中文文档](docs/zh/README.md)
- [English documentation](docs/en/README.md)

## Current Scope

- Chapters 1-3 are extracted from the existing DOCX source files and should preserve the current meaning.
- Chapter 4 and later chapters are represented only in the chapter plan.
- The terminology table and chapter plan are maintained in each language's `00-preface.md`.

## Source Files

The original DOCX and PDF release artifacts remain under `releases/`.

Markdown can be regenerated from the DOCX files with:

```bash
python3 tools/docx_to_markdown.py
```

Use the bundled Codex Python runtime if available, because it includes `python-docx`.
