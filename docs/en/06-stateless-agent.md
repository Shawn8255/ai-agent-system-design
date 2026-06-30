# Chapter 6. Stateless Agents

> Chapter focus: explain why the agent layer should be mostly stateless, and how externalized state improves reliability.

## 6.1 The Question

Chapter 5 discussed compute/storage separation. This chapter takes the next step: if the LLM is stateless compute and memory/files are external storage, what kind of state should the agent layer itself hold?

One intuitive implementation is to let the agent process keep a large amount of session state: the current plan, historical tool results, user preferences, execution progress and error context. This is simple at first, but it creates the same problems as stateful services in classical microservice systems: scaling, restarts, retries and recovery become harder.

A more robust design is to make the agent as stateless as practical. It may hold temporary execution context during a request, but long-lived state should live in memory, databases, file systems, task queues or event logs. Then agent instances can scale horizontally, retry safely, be replaced and support replay.

## 6.2 Stateless Does Not Mean No State

A stateless agent does not mean the system has no state. It means the state should not depend on the memory of one agent process. State still exists, but it is stored externally and restored through explicit read paths.

This is similar to web services. A stateless web service still handles login, carts and orders. It simply does not keep those states only in the memory of one server. When a request arrives, it restores state from cookies, a session store, a database or a cache. When the request completes, it writes necessary results back to external systems.

Agents should work similarly. Before a task runs, the agent can read user memory, project files, task state and tool logs. During execution, it builds context. After execution, it writes stable results back. As long as that state is not tied to one process, the agent can behave more like a stateless service.

The analogy to a stateless web service has a limit worth naming. A typical web request is short and cheap, so re-restoring state on every request costs little. An agent task is often long, multi-step and expensive: it may span many model and tool calls and minutes of wall-clock time. Rebuilding full context from external state before every step can become a real cost, and unlike a web handler the agent must also reason about side effects already committed mid-task. So statelessness here does not mean "cheap to restart anywhere." It means the durable state lives outside the process, while the system still has to make restoration efficient (caching, snapshots) and make partial progress recoverable, which a stateless web service rarely has to worry about.

## 6.3 Why Agents Drift Toward Stateful Mud

Agents easily become stateful mud because natural-language tasks have blurry boundaries. What the model said in the previous turn, what tools returned, what the user changed temporarily and where the planner currently is all feel like things the system should remember.

Without explicit design, the simplest implementation is to put all of that into a runtime object and keep appending. This is convenient in the short term, but it creates long-term problems. A process restart loses task state. Multiple instances disagree. Retries cannot tell whether a tool already executed. A page refresh cannot fully recover context. Logs and real state diverge.

This is why agent systems cannot focus only on prompts. A prompt is the input for one model call. It is not the only source of system state. Real state needs structure, lifecycle and write-back rules.

## 6.4 Basic Forms of External State

A stateless agent puts different kinds of state into different external systems.

| State type | Good location | Explanation |
| --- | --- | --- |
| User preferences | Memory / user configuration table | Long-lived, but must be editable and deletable |
| Project background | File system / document index / memory summary | Searchable, but not all loaded into context |
| Task progress | Task state table / workflow state | Used for recovery, progress display and retries |
| Tool calls | Audit log / event log | Records arguments, results, side effects and errors |
| Temporary context | Request memory / short-lived cache | Used only during the current task lifecycle |
| Final artifacts | Files, databases or external business systems | Persisted according to task type |

The key idea is lifecycle. Not all state should be stored forever, and not all state should go into memory. Temporary context can disappear when the task ends. Tool-call logs may need long retention. User preferences need edit and delete paths. Task state must be structured enough to support recovery and replay.

## 6.5 Scalability Benefits

Once the agent is stateless, the system can scale like a normal microservice. Multiple agent instances can handle requests because they do not depend on local long-term memory. If one instance fails, another can recover the task from external state. When traffic grows, the system can add instances. When the model or agent code changes, rolling deployment becomes easier.

This matters especially for agents because agent tasks may be slow. A task can involve multiple model calls, multiple tool calls and waiting for external systems. The system cannot assume that one process will stay alive forever, or that the whole task will complete inside one short connection. Task queues, state tables and event logs are more reliable than in-process objects.

Statelessness also makes multi-tenancy easier. State for different users and projects can be managed through tenant IDs, permission policies and storage isolation, rather than relying on an agent process to remember whom it is serving.

## 6.6 Retry and Recovery Benefits

The most dangerous part of agent execution is retry. Model calls can be retried. Retrieval calls can be retried. But tool calls may already have produced side effects. If agent state only lives in memory, the system may not know whether a failure happened before or after the side effect.

External state makes retries controllable. Each task step can have a state such as pending, running, succeeded, failed or needs_review. Each tool call can have an idempotency key, argument digest, result summary and side-effect record. Before retrying, the agent checks state and avoids repeating operations that already succeeded.

This is the same discipline used in production systems. Payment systems, order systems and message queues store whether an action has already happened. They do not rely on process memory. Once agents start calling real tools, they need the same discipline.

## 6.7 The Cost of Statelessness

Statelessness is not free. Externalizing state requires more infrastructure: databases, caches, object storage, task queues, event logs and permission systems. Each request also needs state restoration before context construction, which increases latency and complexity.

External state also exposes schema design questions. Which fields should be structured? Which content should remain raw text? Should tool results be saved fully or summarized? Should memory writes require human confirmation? These questions cannot be avoided by putting everything into the prompt.

The goal is therefore not to over-engineer every agent from the beginning. It is to choose the right tradeoff between reliability and implementation cost. An early product can start with a lightweight state table and simple logs. As tasks become more complex, it can add stricter workflow state, audit logs and replay mechanisms.

## 6.8 Summary

This chapter treated the agent layer as a mostly stateless service. Stateless does not mean no state. It means state is not tied to one agent process. Memory, task state, tool logs and final artifacts should be managed through external storage.

This design makes agents easier to scale, restart, retry, recover and audit. It also leads into later chapters. Context engineering will explain how to construct the current working set from external state. Production reliability will return to idempotency, state machines, replay and reconciliation.
