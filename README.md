# AI Agent System Design

A bilingual technical book about AI Agent system design from the perspective of classical computer engineering.

This repository keeps the editable book source in Markdown. Chapters 1-3 were extracted from the original DOCX releases, and Chapters 4-6 continue the same system-design line.

## Languages

- [中文文档](docs/zh/README.md)
- [English documentation](docs/en/README.md)

## Current Scope

- Chapters 1-6 are complete in Markdown.
- Chapter 7 and later chapters are represented only in the chapter plan.
- The terminology table and chapter plan are maintained in each language's `00-preface.md`.
- The expanded future plan now includes agent production reliability, concurrent scheduling, multi-tenancy, and security/sandboxing as first-class topics.

## Source Files

The original DOCX and PDF release artifacts remain under `releases/`. The latest generated release is `v0.4`, built from the Markdown source for Chapters 1-6.

The historical Chapters 1-3 Markdown extraction can be regenerated from the original DOCX files with:

```bash
python3 tools/docx_to_markdown.py
```

That extractor is only for the original DOCX source conversion. The current authored source of truth is Markdown under `docs/`.

DOCX/PDF releases can be regenerated from the Markdown source with:

```bash
python3 tools/markdown_to_release.py
```

Use the bundled Codex Python runtime if available, because it includes `python-docx`.
