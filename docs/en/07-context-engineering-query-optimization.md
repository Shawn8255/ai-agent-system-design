# Chapter 7. Context Engineering and Query Optimization

> Chapter focus: treat context engineering as data loading and query optimization, not just prompt writing.

## 7.1 The Question

The previous chapters positioned the LLM as compute, memory/files/indexes as storage, and context as the working set of one compute request. The next question is: before each model call, which information should be loaded?

Many people treat context engineering as writing a better prompt. That is part of it, but from a systems perspective it is closer to query optimization. A database does not send an entire table into the execution engine. An operating system does not load the entire disk into memory. An agent should not send every chat message, every document and every tool result to the model.

The core goal of context engineering is not more context. It is more relevant, cheaper and more verifiable context. It balances recall, precision, cost, latency and reliability.

## 7.2 Context Is the Execution Input for a Model Call

A model call looks like a function call, but the input is not simply the user's raw message. The input is context constructed by the agent. It may include system instructions, user goals, memory summaries, file snippets, tool results, planning state, errors and output format requirements.

Context therefore resembles the execution input after query planning. A database execution engine does not see the entire business world. It sees data and operations selected by the optimizer. Similarly, the LLM does not see the entire project. It sees the working set selected by the context builder.

This means context quality directly affects model quality. A strong model will still guess if key facts are missing. It will be misled if wrong facts are included. If context is too long, important information is diluted by noise and cost increases.

## 7.3 The Query Optimization Analogy

A database optimizer estimates available indexes, join choices, filter selectivity and scan cost. A context builder needs similar judgment: which memories are relevant, which file snippets should be loaded, whether tool results are still valid and which old context can be dropped.

The analogy is not perfect. Databases have schemas, statistics and deterministic execution plans. Natural-language tasks are blurrier and relevance is harder to estimate. But the engineering motivation is the same: do not waste expensive compute on irrelevant data.

If the LLM is an expensive execution engine, context engineering is data selection, filtering, ordering and compression before the call. It decides what the model sees and what it does not see.

## 7.4 Inputs to the Context Builder

| Input source | Typical content | Main risk | Optimization problem |
| --- | --- | --- | --- |
| User request | Current goal, constraints, preferences | Ambiguity and goal drift | Clarify intent and extract the task |
| Memory | User preferences, project context, decisions | Stale or polluted memory, over-recall | Select stable and relevant state |
| File system | README, code, docs, config | Too many files, version mismatch | Find files that matter to the current task |
| Retrieval | Document chunks, knowledge base content | Wrong recall, broken chunks | Balance recall and precision |
| Tool result | API output, shell output, search results | Too long, temporary or erroneous | Compress while preserving verifiable facts |
| Planner state | Current step, completion state, failure reason | Overlong plans and state drift | Keep the minimum state needed for the next step |

Context is not one text blob. It is a composition of multiple sources. The hard part is cross-source selection, not optimizing one prompt paragraph.

## 7.5 Pruning, Summarization and Ordering

The context builder commonly performs three actions: pruning, summarization and ordering.

Pruning decides what does not enter context. It is the most direct token-reduction technique, but the risk is removing a critical fact. Pruning should not be based only on length. It should consider task goal, recent changes, file type, permissions and historical importance.

Summarization compresses long content into shorter content. It reduces tokens, but it can lose information. Technical docs, code diffs, tool outputs and error logs should not be summarized in the same way. A good summary preserves verifiable facts, identifiers, failure causes and constraints needed for the next step.

Ordering decides what the model sees first. LLMs are sensitive to position. Important information buried in the middle or at the end may be underused. The context builder should place task goals, constraints, latest state and strongest evidence where the model can use them.

## 7.6 Prompt Caching and Stable Prefixes

A lot of agent cost comes from repeatedly sending stable content: system instructions, tool definitions, output formats, project-level rules and terminology. These change little during an agent loop and are good candidates for stable prefixes.

Prompt caching reduces the cost of repeated prefixes. It does not change the agent's logic, but it does influence prompt structure. Stable content should be centralized, ordered consistently and rewritten only when necessary. Dynamic content should come later and contain only task-relevant information.

This resembles cache-friendly system design. Cache hits require stable keys, stable structure and predictable change boundaries. Agent prompts are similar. If each round injects changing timestamps, random phrasing or irrelevant logs into the prefix, prompt caching becomes less useful.

## 7.7 Failure Modes

Context engineering failures usually come from bad data-loading strategy, not from the model suddenly becoming worse.

First, under-recall. A key file, memory or tool result does not enter context, so the model guesses.

Second, over-recall. Too much irrelevant content enters context, distracting the model and increasing cost.

Third, lossy summarization. The summary removes constraints, edge cases or error details, and the model reasons from a damaged compression.

Fourth, bad ordering. The right information is present but placed where the model does not use it well.

Fifth, cache misses. Stable prefixes are rewritten unnecessarily, preventing prompt caching from helping.

## 7.8 Summary

This chapter positioned context engineering as query optimization. Agents should not chase unlimited context. They should select, filter, order and compress data the way query optimizers prepare execution.

This perspective explains why AGENTS.md matters. It is not just a note file. It is an index-like entry point that helps the agent find project knowledge. Chapter 8 discusses AGENTS.md as a prompt index.
