# Repository Instructions

This repository contains a bilingual Markdown edition of a technical book on AI Agent system design.

## Current State

- Part I is drafted through Chapter 13 in both Chinese and English.
- The current generated release is `v0.7` for Chapters 1-13.
- Markdown under `docs/` is the source of truth; DOCX/PDF files under `releases/` are generated artifacts.
- `99-future-chapters.md` is now a revision-notes file, not a chapter backlog.

## Editing Rules

- Keep Chinese content under `docs/zh`.
- Keep English content under `docs/en`.
- Preserve the meaning of Chapters 1-3 when editing. Prefer small corrections over rewrites.
- Chapters 4-13 are now drafted in Markdown and should be edited consistently with the established system-design voice.
- Do not add new chapters beyond Chapter 13 without first updating the chapter plan and bilingual README files.
- Keep the chapter plan and terminology table aligned across both languages.
- Preserve existing terminology unless there is a clear consistency fix:
  - LLM
  - Agent
  - Memory
  - Context
  - Context Builder
  - Context Routing
  - Tool
  - Planner
  - Prompt Index
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
  - Scheduler
  - Concurrent Scheduling
  - Capability Boundary
  - Agent OS

## Structure

- `docs/zh/00-preface.md` and `docs/en/00-preface.md` contain the preface, chapter plan, terminology table, and first figure.
- `01-*` through `13-*` contain Chapters 1-13. Chapter 7 covers context engineering together with AGENTS.md as a prompt index (the former separate AGENTS.md chapter was merged in).
- `98-references.md` contains the bilingual reference appendix and is included in generated releases.
- `99-future-chapters.md` contains future revision notes rather than planned chapter prose.
- `assets/` folders contain figures extracted from the DOCX files.
- `releases/docx` and `releases/pdf` contain generated release artifacts.
- The repository is licensed under CC BY 4.0 (`LICENSE`) for book content.

## Regeneration

Use `tools/docx_to_markdown.py` only when intentionally regenerating Markdown from the DOCX release files. Regeneration overwrites `docs/zh` and `docs/en`, so review diffs carefully afterwards.

Use `tools/markdown_to_release.py` to regenerate the current DOCX/PDF releases from Markdown. After regenerating release artifacts, verify the output files exist and check Markdown links before committing.

## Review Priorities

- Treat content changes as bilingual unless they are language-only edits.
- Keep chapter headings, chapter status, and terminology aligned across `docs/zh/00-preface.md` and `docs/en/00-preface.md`.
- Prefer examples, citations, and clarifying notes over broad rewrites of the current structure.
- Public-release work should focus on references, case studies, license choice, and contribution boundaries.
