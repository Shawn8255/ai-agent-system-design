# Chapter 4. Memory, Tools and Planner

> Chapter focus: separate the responsibilities that are often mixed inside an agent.

## 4.1 The Question

The previous chapters positioned the agent as an orchestrator. But it is not enough to say that an agent organizes memory, tools, planning and context. In real system design, the hard part is not whether these components exist. The hard part is whether their responsibilities are separated.

Many agent products put everything into one large prompt: user history, project background, tool results, planning steps, errors and the final answer. This can make a demo work, but it creates long-term problems. State becomes hard to control, tool calls become hard to audit, and planning becomes hard to replay.

This chapter asks a more precise question: what should memory store, what should tools do, and what should the planner decide? These components roughly map to storage, external APIs and workflow scheduling, but they are not the same thing.

## 4.2 Memory Stores State; It Does Not Think for the Model

Memory stores reusable state. It can include user preferences, project background, historical decisions, task progress, file summaries and long-lived facts. It should not be understood as a magic layer that makes the model smarter. It is external state managed by the agent system.

From an engineering perspective, memory is closer to a database or cache than to the model itself. The model is still stateless compute for each inference call. The agent reads relevant information from memory, then puts only part of it into the current context. In other words, memory can store a lot, but the model only sees the working set selected by the context builder.

This distinction matters. If memory is designed as an endlessly growing chat transcript, the system soon becomes a mechanism for pushing more history into the prompt. A better design separates stable long-term facts, recent task state and temporary tool results. Only results that are worth reusing should be summarized and written back into long-term memory.

## 4.3 Tools Produce Effects; They Do Not Own Long-Term Meaning

Tools connect the agent to the outside world. They can read files, send email, inspect calendars, access GitHub, run shell commands, call databases or operate business systems. The defining property of a tool is that it may produce real side effects.

This makes tools fundamentally different from memory. Memory is state managed by the agent. A tool is an external capability. A tool call may create an issue, send a message, modify a file, start a payment, update an order or delete a resource. These actions cannot be treated as just another piece of model output. They are system actions that need auditability, retry rules and sometimes rollback or reconciliation.

A tool layer therefore needs to handle at least four concerns: permissions, parameter validation, execution results and error semantics. The agent should record which tool was called, which arguments were passed, what result came back, whether side effects occurred, and whether a failure can be retried.

## 4.4 The Planner Decides Steps; It Should Not Execute Everything

The planner decomposes a user goal into executable steps and decides their order. It answers the question "what should happen next?" It should not own tool internals or persistence logic.

This resembles a workflow engine or scheduler. A workflow engine does not itself send email, write databases or run queries. It decides when those operations happen, what prerequisites they require, whether failures should be retried and whether human confirmation is needed. An agent planner should play a similar role. It organizes work; it should not hide all business logic inside a prompt.

A common mistake is giving the planner too much freedom. A model can generate a long plan, but long plans create more failure points, higher cost and weaker auditability. A safer design asks the planner for short plans and re-evaluates after each step based on tool results.

## 4.5 The Context Builder Connects the Components

Memory, tools and planner need another component that is easy to overlook: the context builder. It turns long-term state, current task state, tool results and planning steps into the context for the next model call.

The context builder is not just string concatenation. It decides which memories are relevant, which tool results should remain visible, which steps are already done, which errors the model must know about, and which information should be compressed or dropped. It resembles a mixture of query optimization and working-set management.

Without a context builder, memory becomes uncontrolled text, tool results become a growing log, and the planner becomes a long list without feedback. Much of agent reliability depends on whether this layer clearly manages what the model sees in the current request.

## 4.6 Responsibility Boundaries

| Component | Main responsibility | Should not do | Engineering analogy |
| --- | --- | --- | --- |
| Memory | Store long-term state, preferences, project context and task history | Reason for the model or send all history into the prompt | Database / Cache |
| Tool | Call external systems and return results, with side effects when necessary | Own long-term semantics or hide side effects | RPC / API |
| Planner | Decompose goals, order steps and decide whether to continue or escalate | Execute external operations directly or produce an unchangeable long plan | Workflow Engine / Scheduler |
| Context Builder | Select the working set for the current request | Concatenate unlimited information | Query Optimizer / Buffer Manager |

The point of this table is not naming. It is preventing responsibility leakage. Memory should not become a prompt junk drawer. Tools should not be treated as pure functions when they have side effects. The planner should not become an unauditable natural-language script. The context builder should not be just a string builder.

## 4.7 Failure Modes

Blurry responsibility boundaries produce predictable failure modes.

First, memory pollution. Incorrect facts, stale information or temporary tool results are written into long-term memory and then reused in future tasks.

Second, uncontrolled tool side effects. The model calls the same tool repeatedly, creating duplicate issues, sending duplicate messages or modifying files twice, while the system lacks idempotency keys and call logs.

Third, runaway planning. The model creates a long plan without checkpoints or feedback from tool results. When the task fails, it is unclear which step caused the failure.

Fourth, context bloat. All history and tool results are sent to the model. Token cost rises, and important facts are buried under noise.

## 4.8 Summary

This chapter separated memory, tools, planner and context builder. Memory is the state layer. Tools are the external capability layer. The planner is the orchestration layer. The context builder manages the working set for the current request.

This separation prepares the next chapters. Chapter 5 explains why compute and storage should be separated. Chapter 6 explains why the agent itself should remain as stateless as possible. Later chapters on production reliability will return to tool side effects, idempotency, state machines and replay.
