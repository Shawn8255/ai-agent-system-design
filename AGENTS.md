# Repository Instructions

This repository contains a bilingual Markdown edition of a technical book on AI Agent system design.

## Editing Rules

- Keep Chinese content under `docs/zh`.
- Keep English content under `docs/en`.
- Preserve the meaning of Chapters 1-3 when editing. Prefer small corrections over rewrites.
- Chapters 4-9 are now drafted in Markdown and should be edited consistently with the established system-design voice.
- Do not draft Chapter 10 or later yet. Chapter 10 and later may appear only as planned chapters.
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
  - Sandbox
  - Prompt Injection
  - Idempotency
  - State Machine
  - Replay
  - Observability
  - Audit
  - Concurrent Scheduling

## Structure

- `docs/zh/00-preface.md` and `docs/en/00-preface.md` contain the preface, chapter plan, terminology table, and first figure.
- `01-*` through `09-*` contain Chapters 1-9.
- `99-future-chapters.md` contains only the future writing plan.
- `assets/` folders contain figures extracted from the DOCX files.

## Regeneration

Use `tools/docx_to_markdown.py` only when intentionally regenerating Markdown from the DOCX release files. Regeneration overwrites `docs/zh` and `docs/en`, so review diffs carefully afterwards.
