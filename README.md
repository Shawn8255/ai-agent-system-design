# AI Agent System Design

A bilingual technical book about AI Agent system design from the perspective of classical computer engineering.

This repository keeps the editable book source in Markdown. Chapters 1-3 were extracted from the original DOCX releases, and Chapters 4-13 continue the same system-design line as a complete Part I draft. Chapter 14 opens Part II. The Markdown files under `docs/` are now the source of truth.

## Languages

- [中文文档](docs/zh/README.md)
- [English documentation](docs/en/README.md)

## Current Scope

- Chapters 1-13 are complete in Markdown as the Part I draft; Chapter 14 opens Part II.
- The terminology table and chapter plan are maintained in each language's `00-preface.md`.
- The final chapters cover token cost, production reliability, concurrent scheduling, multi-tenancy, security/sandboxing, and the Agent OS synthesis as first-class topics.

## Latest Release

The latest generated release is `v0.10`, built from the Markdown source for Chapters 1-14:

- Chinese DOCX: `releases/docx/AI_Agent_System_Design_CN_Part1_Ch1-14_v0.10.docx`
- Chinese PDF: `releases/pdf/AI_Agent_System_Design_CN_Part1_Ch1-14_v0.10.pdf`
- English DOCX: `releases/docx/AI_Agent_System_Design_EN_Part1_Ch1-14_v0.10.docx`
- English PDF: `releases/pdf/AI_Agent_System_Design_EN_Part1_Ch1-14_v0.10.pdf`

## Content Map

- Chapters 1-3: original foundation extracted from the DOCX sources.
- Chapters 4-8: memory, tools, planner, storage separation, stateless agents, context engineering, prompt index, and retrieval routing.
- Chapters 9-13: token cost, distillation, tiered compute, production reliability, concurrent scheduling, security, and Agent OS.
- Chapter 14: Part II opening on learned memory, skill and routing.
- `99-future-chapters.md`: future revision notes, not planned chapter prose.

## Source Files

The original DOCX and PDF release artifacts remain under `releases/`.

The historical Chapters 1-3 Markdown extraction can be regenerated from the original DOCX files with:

```bash
python3 tools/docx_to_markdown.py
```

That extractor is only for the original DOCX source conversion. The current authored source of truth is Markdown under `docs/`.

DOCX/PDF releases can be regenerated from the Markdown source with:

```bash
python3 tools/markdown_to_release.py
```

The release script requires `python-docx`. PDF conversion also requires LibreOffice's `soffice` binary on `PATH`, or an explicit `SOFFICE=/path/to/soffice` environment variable.

## License

The book content (text and figures) is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE). See `docs/zh/98-references.md` and `docs/en/98-references.md` for source references and further reading.

## Maintenance Notes

- Update both `docs/zh` and `docs/en` when changing shared structure, chapter status, or terminology.
- Keep Chapters 1-3 stable in meaning; prefer small corrections over rewrites.
- Do not add Chapter 15 or later prose until the bilingual chapter plan has been intentionally extended.
- Use `TODO.md` for publication tasks such as citations, examples, release checklist, and X thread drafts.
