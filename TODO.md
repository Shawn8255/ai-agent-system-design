# TODO

## Content

- [x] Extract Chinese Markdown into `docs/zh`.
- [x] Extract English Markdown into `docs/en`.
- [x] Preserve Chapters 1-3 from the current DOCX sources.
- [x] Draft Chapter 4: Memory, Tools and Planner.
- [x] Draft Chapter 5: Compute / Storage Separation.
- [x] Draft Chapter 6: Stateless Agent.
- [x] Draft Chapter 7: Context Engineering, Prompt Index and Query Optimization (merged the former Context Engineering and AGENTS.md chapters).
- [x] Draft Chapter 8: Retrieval and Context Routing.
- [x] Draft Chapter 9: Token Reduction, Distillation and Tiered Compute.
- [x] Draft Chapter 10: Agent Production Reliability.
- [x] Draft Chapter 11: Multi-Agent, Concurrent Scheduling and Multi-Tenancy.
- [x] Draft Chapter 12: Agent Security.
- [x] Draft Chapter 13: Toward an Agent Operating System.
- [x] Preserve the terminology table.
- [x] Preserve the chapter plan.
- [x] Review bilingual terminology consistency before any public release.
- [ ] Add editorial notes only after the Markdown extraction has been reviewed.
- [x] Expand the future chapter plan around agent production reliability: idempotency, optimistic locking, state machines, retries, degradation, escalation, observability, audit, replay and reconciliation.
- [x] Add a dedicated agent security chapter plan covering prompt injection as exploit, sandboxing, least privilege, capability boundaries and audit.
- [x] Add a concurrent scheduling thread for multi-agent and multi-tenant execution in the later Agent OS chapters.
- [x] Expand the token chapter (now Chapter 9) around the token-cost model: call count, tokens per call and cost per token.
- [x] Update DOCX/PDF release sources after the Markdown chapter plan is reviewed.
- [x] Generate the first DOCX/PDF release artifacts from Markdown.

## Maintenance

- [x] Decide whether DOCX/PDF releases should continue to be generated from Markdown.
- [x] Update `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, and bilingual README files for the current Chapters 1-13 draft.
- [ ] Add a formal release checklist for public publication.
- [x] Choose and add a text-oriented license (CC BY 4.0).
- [x] Add citations and reference notes for the public release (`docs/{zh,en}/98-references.md`).
- [x] Merge former Chapters 7-8 into one context-engineering + prompt-index chapter and renumber the book to Chapters 1-13.
- [x] Add examples or case studies for the production reliability chapter (now Chapter 10).
- [x] Add a cost optimization example to the token chapter (now Chapter 9) using the cost model.
- [x] Add a redundant-execution and agent-handoff section to the multi-agent chapter (Chapter 11.6).
- [x] Add a cross-runtime standards and portability section to the Agent OS chapter (Chapter 13.6).
- [x] Add a Part II forward-looking plan for learned memory / skill / routing in `99-future-chapters.md`.
- [x] Generate v0.8 DOCX/PDF release artifacts for Chapters 1-13.
- [ ] Turn the distillation-vs-token-reduction argument into a publishable X thread derived from Chapter 9.
- [ ] Add a short English summary to the root README for overseas readers if the repository is promoted publicly.
- [ ] Decide whether release DOCX/PDF artifacts should stay committed or move to GitHub Releases after public launch.
