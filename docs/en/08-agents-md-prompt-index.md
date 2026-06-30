# Chapter 8. AGENTS.md as a Prompt Index

> Chapter focus: explain why AGENTS.md is closer to a project-level index than to a normal README.

## 8.1 The Question

When an agent enters a project, it does not face one file. It faces a workspace: code, docs, configuration, tests, scripts, historical conventions and implicit workflows. Even a strong model becomes expensive, slow and inconsistent if it has to rediscover the whole project every time.

This is where AGENTS.md matters. It is not just a note for humans, and not merely a prompt for the model. From a systems perspective, it is a project-level prompt index: a small entry point that tells the agent where to begin, which rules matter and which files form the critical path.

This chapter explains why AGENTS.md behaves like an index, and what it should and should not contain.

## 8.2 README, Docs and AGENTS.md

A README usually serves human readers. It explains the project goal, installation and basic usage. Detailed documentation explains design, APIs and operational workflows. AGENTS.md serves the agent. Its goal is not to explain the whole project, but to help the agent locate relevant knowledge quickly.

This means AGENTS.md should not duplicate all documentation. It should point to where build commands live, how tests run, what style constraints are hard requirements, which directories contain core modules, which files should not be edited casually and where to start for common task types.

If the README is the project homepage, AGENTS.md is closer to a query entry point and routing table. It does not replace documentation. It helps the agent decide which documentation to load.

## 8.3 AGENTS.md as Prompt Index

The value of an index is using a small structure to locate large content. A database index does not store every field of every row, but it helps the query find relevant rows quickly. AGENTS.md is similar. It should not contain all project knowledge, but it should contain enough routing information to find the right places.

A project-level prompt index should answer several questions. What is the technology stack? What are the common commands? How do tests, formatting and release generation work? How are core directories organized? Where is task-specific documentation? Which conventions override local guesses? Which operations are risky?

If this information is scattered across the repository, the agent has to rediscover it every time. AGENTS.md centralizes the entry points, reducing context loading cost and lowering the chance of misreading project structure.

## 8.4 What a Good AGENTS.md Contains

| Content type | Example | Purpose |
| --- | --- | --- |
| Project role | API service, frontend app, data pipeline or documentation project | Establish task boundaries |
| Key directories | `src/`, `tests/`, `docs/`, `scripts/` | Locate files quickly |
| Common commands | Test, format, build, release generation | Avoid guessing commands |
| Code/doc conventions | Naming, formatting, terminology, chapter structure | Keep edits consistent |
| Risk boundaries | Do not edit generated files, rewrite chapters or delete releases | Avoid destructive changes |
| Task routing | Where to start for API fixes or documentation edits | Guide context selection |

These entries should be concise, stable and actionable. AGENTS.md is not a long architecture document. It is a high-signal index.

## 8.5 What Does Not Belong in AGENTS.md

The main risk of AGENTS.md is bloat. If it becomes another manual, the agent still has to read a large amount of text and the index loses value.

Bad candidates for AGENTS.md include full business background, long tutorials, every API detail, all historical decisions, information already obvious from code, and temporary task lists that change frequently. Those belong in dedicated documents or issues, with AGENTS.md pointing to them.

In short, AGENTS.md should store "where to look" and "what must be obeyed," not all knowledge itself. Its purpose is to improve the context builder's hit rate, not to enlarge the prompt.

## 8.6 Layered AGENTS.md and Scope

Large projects may need multiple AGENTS.md files. The root file provides global rules. Subdirectory files provide local rules. Backend, frontend, mobile, documentation and data-pipeline areas may all have different commands and conventions.

This resembles configuration inheritance or routing tables. Global rules apply across the repository. Local rules apply only in a specific directory. When editing a file, the agent should load the relevant AGENTS.md files along the path from the root to the target directory, not just one global file.

Scope matters. If every local rule is placed in the root AGENTS.md, the file bloats. If only local rules exist without global rules, the agent may miss project-wide constraints. Layered indexes balance the two.

## 8.7 Failure Modes

First, staleness. Commands, directories or conventions change but AGENTS.md does not, so the agent follows the wrong index.

Second, length. AGENTS.md becomes an encyclopedia. Loading cost rises and critical rules get buried.

Third, vagueness. It says "keep code quality high" or "remember tests" but gives no concrete commands or boundaries.

Fourth, conflict with source. AGENTS.md says one convention, while the code follows another, and the agent cannot tell which source to trust.

Fifth, no task routing. The file lists rules but does not tell the agent where to start for different types of work.

## 8.8 Summary

This chapter positioned AGENTS.md as a prompt index. It does not replace the README or full documentation. It gives the agent a low-cost, high-signal project entry point.

A good AGENTS.md helps the agent perform context routing: finding the rules, docs and code that matter for the current task. Chapter 9 continues with retrieval and context routing, showing why retrieval is not just similar-text search but choosing the right context path.
