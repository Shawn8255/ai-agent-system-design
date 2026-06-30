# Repository Instructions

This repository contains a bilingual Markdown edition of a technical book on AI Agent system design.

## Editing Rules

- Keep Chinese content under `docs/zh`.
- Keep English content under `docs/en`.
- Preserve the meaning of Chapters 1-3 when editing. Prefer small corrections over rewrites.
- Do not continue or draft Chapter 4 yet. Chapter 4 may appear only as a planned chapter.
- Keep the chapter plan and terminology table aligned across both languages.
- Preserve existing terminology unless there is a clear consistency fix:
  - LLM
  - Agent
  - Memory
  - Context
  - Tool
  - Distillation
  - Compute Engine
  - Orchestrator
  - Tiered Compute

## Structure

- `docs/zh/00-preface.md` and `docs/en/00-preface.md` contain the preface, chapter plan, terminology table, and first figure.
- `01-*`, `02-*`, and `03-*` contain Chapters 1-3.
- `99-future-chapters.md` contains only the future writing plan.
- `assets/` folders contain figures extracted from the DOCX files.

## Regeneration

Use `tools/docx_to_markdown.py` only when intentionally regenerating Markdown from the DOCX release files. Regeneration overwrites `docs/zh` and `docs/en`, so review diffs carefully afterwards.
