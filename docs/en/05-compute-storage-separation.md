# Chapter 5. Compute / Storage Separation

> Chapter focus: explain why an agent architecture should not merge model, state and knowledge into one blob.

## 5.1 The Question

In classical system design, separation of compute and storage is a basic principle. The compute layer executes logic. The storage layer persists state. Web services do not keep all user state in process memory. Databases do not own every business workflow. Distributed systems do not assume that a compute node permanently holds the complete context.

AI agents face the same problem. The LLM is a high-capability compute engine, but it is not long-term storage. An agent may call a model, read memory, retrieve documents, invoke tools and update state. If all of these responsibilities are pushed into a prompt or into model weights, the system becomes expensive, fragile and hard to maintain.

The core question of this chapter is: what should count as compute, and what should count as storage in an agent system? Why does separating them make agents easier to scale, debug and cost-control?

## 5.2 The LLM Is Compute, Not Storage

The LLM's role is to reason, generate and judge based on the current input. It can handle complex language, code and planning tasks, but it should not be treated as the place where all history and business state live.

From the perspective of one call, the LLM is a remote compute service. It reads the prompt, performs inference and returns a result. On the next call, if the relevant state is not provided in the prompt, it cannot reliably recover what happened before. Even a long context window does not make the model a database. A long context window is a larger working set, not durable storage.

Therefore, pushing everything into context is not compute/storage separation. It is moving storage temporarily into the compute request. That can work for small ad hoc tasks, but it is not a good long-term system design.

## 5.3 Memory, Files and Indexes Are Storage

The storage layer inside an agent system can take many forms: structured databases, vector indexes, file systems, object storage, caches, event logs, user-preference tables and task-state tables. Their shared responsibility is to persist state and let the agent read it when needed.

Memory is only one part of storage. Project files, tool results, user configuration, permission policies, task progress and audit logs all belong to the broader storage layer. Calling all of them memory blurs the design. A more precise statement is: memory is the state view used to restore model context, while storage is the full set of durable system state.

This distinction affects architecture. User preferences may go into memory. Order state should live in a business database. Tool-call logs should go into an audit log. Large documents should live in a file system or object store. Retrieval chunks should live in an index. These should not all become prompt text.

## 5.4 Context Is the Working Set of a Compute Request

Compute/storage separation does not mean compute needs no state. Every compute request needs a selected subset of state. That subset is context.

Context is like the pages loaded into a database buffer pool for a query, or the working set of an operating-system process. It comes from storage, but it is not storage itself. Before each model call, the agent selects a small amount of information from memory, files, indexes and tool results, then organizes it into input the model can use.

This explains why context engineering is central to agent systems. It is not merely prompt style. It is the data-loading strategy between storage and compute. Load too little and the model lacks context. Load too much and cost rises, noise increases and important facts get buried.

## 5.5 RAG Is a Read Path, Not the Whole System

RAG is often treated as the center of agent architecture, but more precisely it is a read path from storage into context. Retrieval finds relevant document chunks and places them into the model context so the LLM can answer using external knowledge.

This is useful, but it is not complete state management. RAG mostly solves the problem of finding relevant content in a large text corpus. It does not automatically handle task state, permissions, side effects, retries, audits, long-term preferences or business consistency. A production agent cannot manage all state through RAG alone.

RAG should therefore be placed in the right architectural role: one read path from storage. It sits alongside database queries, file reads, cache hits and tool-result loading. The agent must decide when to use retrieval, when to query structured state, when to read files and when to call tools.

## 5.6 The Write Path Matters Too

Many agent discussions focus on how to put information into the prompt, but ignore what should be written back to storage. For a long-running system, the write path is just as important.

After completing a task, the agent may need to write back several kinds of results: user preferences, task progress, decision records, tool-call summaries, errors, evaluation results and audit logs. Not every model output should be persisted. Before writing back, the system must decide whether the information is stable, true, reusable and allowed to be stored.

This resembles write paths in classical systems. Database writes need schemas, constraints and transactions. Cache writes need expiration policies. Event logs need ordering and immutability. Agent memory writes need similar discipline. Otherwise the system will permanently store hallucinations, temporary guesses and stale state.

## 5.7 Engineering Benefits of Separation

| Design problem | Merged design | Separated design |
| --- | --- | --- |
| Long-term state | Put everything into the prompt or chat history | Store it in databases, files, memory or event logs |
| Current context | Concatenate history without limits | Select a working set from storage |
| Cost control | Context grows indefinitely | Control tokens through indexes, caches and pruning |
| Debuggability | Unclear which state influenced the answer | Inspect which memory, files and tool results were loaded |
| Consistency | Treat model output as fact | Validate, structure and permission-check before writing back |
| Scalability | Carry large history in every request | Scale storage independently and load on demand |

The main benefit of compute/storage separation is control. The model remains powerful, but it is no longer the container for all system state. Where state is stored, when it is read, how much is loaded and when results are written back become designable and auditable engineering decisions.

## 5.8 Summary

This chapter separated compute and storage in agent systems. The LLM is compute. Memory, files, indexes, databases and logs form storage. Context is the working set of a compute request. RAG is one read path, not the whole system.

This viewpoint explains why long context does not solve everything. Long context expands the working set of one request, but it does not replace durable state, indexes, write-back policies or consistency control. Chapter 6 extends this idea: once state is externalized, the agent itself can behave more like a stateless service.
