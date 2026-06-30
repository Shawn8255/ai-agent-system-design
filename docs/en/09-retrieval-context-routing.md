# Chapter 9. Retrieval and Context Routing

> Chapter focus: expand retrieval from similar-text search into context routing for agents.

## 9.1 The Question

RAG is often described as "retrieve, then generate." That definition is not wrong, but it is too narrow for agent systems. Real agents do not only face knowledge-base documents. They face project files, code, memory, tool results, task state, issues, logs and external systems.

Retrieval inside an agent should therefore not mean only vector similarity search. It is closer to context routing: based on task type, permissions, state and cost, the agent decides which information sources to read, what to read from them and how to place the result into model context.

This chapter asks: what role does retrieval actually play inside an agent? Why is "find similar text" only one part of the problem?

## 9.2 RAG Is One Read Path

Chapter 5 positioned RAG as one read path from storage into context. It is useful for large bodies of unstructured text such as docs, knowledge bases, manuals and historical records. The retrieval system finds relevant chunks, and the context builder places them into the prompt.

But an agent has many read paths beyond RAG. Querying a database, reading files, calling APIs, loading memory, reading task state and inspecting tool logs are also read paths. They may not use vector search, but they answer the same question: what external information does this model call need?

A more precise architecture statement is: RAG is one implementation technique inside context routing. It is not the entire context system.

## 9.3 Inputs to Context Routing

Context routing uses multiple signals to choose read paths.

| Signal | Example | Effect |
| --- | --- | --- |
| Task type | Coding, fact lookup, email summary, document edit, bug debugging | Prioritize code, docs, memory or tool results |
| Data shape | Structured table, long document, code, log, image | Choose SQL, full-text search, vector search or file read |
| Freshness | Current file, historical memory, real-time API | Decide whether cached data is safe or live reads are required |
| Permission | User auth, repository access, tool capability | Decide which sources can be accessed |
| Cost | Tokens, latency, API cost | Decide how much to read and whether to compress |
| Risk | Production impact, private data | Decide whether confirmation or audit is required |

These signals show that retrieval is not just similarity ranking. Similarity is one score. Context routing is a system-level decision.

## 9.4 Value and Limits of Vector Retrieval

Vector retrieval is good at finding semantically similar content in large text collections. It is useful for documentation, historical discussions, similar issues and conceptual explanations. For agents, it can reduce the cost of understanding a project from scratch.

But vector retrieval has limits. First, it may return content that looks relevant but is stale or wrong. Second, it does not naturally understand permissions or task state. Third, it is not always better than SQL for structured queries. Fourth, it returns chunks, which may lose full context and causality.

Vector retrieval should therefore be combined with metadata filters, timestamps, permission checks, file paths, code structure and task state. Pure top-k similar chunks can easily send the wrong context to the model.

## 9.5 Hybrid Retrieval

Production agents often need hybrid retrieval. Different sources and methods complement each other. Keyword search is good for exact identifiers. Vector search is good for semantic similarity. Structured queries are good for state and permissions. File paths are good for project structure. Tool calls are good for live information.

For example, debugging a bug may require several reads. The agent may first search the error message as a keyword, then use file paths to locate the module, then read tests, then inspect recent changes, then load project conventions from memory. No single retrieval method solves the whole task.

The key is routing order. What to read first, what to read next, when to stop and when to escalate to a more expensive retrieval or model call all affect cost and quality.

## 9.6 Retrieval Results Are Not Final Context

Retrieval results are not the same as final context. They still need filtering, deduplication, ordering, compression and verification.

A common mistake is placing top-k chunks directly into the model. Those chunks may contain duplicates, stale content, conflicts or irrelevant details. The context builder should first decide which chunks actually support the task, then choose whether to summarize, quote, keep raw text or discard them.

This is especially true for code and tool outputs. Code snippets need function names, file paths and call relationships. Logs need timestamps, error codes and key stack frames. Tool outputs need verifiable facts and side-effect state. Different content needs different compression strategies.

## 9.7 Failure Modes

First, wrong source routing. The agent uses document retrieval when it should query a database, or loads old memory when it should read the current file.

Second, recall bias. Retrieved content is semantically similar but does not match the current task constraints.

Third, permission leakage. The agent loads information the current user should not see.

Fourth, freshness errors. The system uses a cache or stale index instead of reading current state.

Fifth, unclear stopping conditions. The agent keeps retrieving and appending context, increasing cost without improving quality.

These failures show that retrieval must be integrated with permissions, state, caching, audit and planning. It should not exist as a standalone module.

## 9.8 Summary

This chapter placed RAG and retrieval inside the broader frame of context routing. RAG is an important read path, but an agent's context system also includes databases, files, memory, tool results, task state and logs.

Useful retrieval does not merely find similar text. It chooses the right information source based on task, permission, state and cost, then turns the result into context the model can actually use. The next chapter returns to the cost model and discusses token reduction, distillation and tiered compute.
