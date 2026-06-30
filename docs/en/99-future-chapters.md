# Plan for the Remaining Chapters

Part I now completes the first nine chapters of the foundational system perspective. Later chapters will continue the same line of reasoning into the cost boundary between token reduction and distillation, production reliability, multi-agent / multi-tenant scheduling, agent security and agent OS.

The next stage should also add three engineering themes that strengthen the book's differentiation. First, agent security should not remain a footnote. Operating-system security models will migrate into agent systems: prompt injection behaves more like an exploit, tool use needs capability boundaries, and code or external-system access needs sandboxing. Second, concurrent scheduling is where the OS analogy becomes most literal. Multi-agent, multi-tenant execution, task queues and resource isolation go beyond the single-task Planner-to-Scheduler analogy. Third, agents should be treated as production systems: they need SLAs, idempotency, optimistic locking, state machines, retries, degradation, escalation, observability, audit, replay and reconciliation. This production reliability perspective is the main difference from OS-analogy papers that focus mostly on architecture and runnable prototypes.

1. Chapters 1-9 have established the core architecture line from LLMs and agents to memory / tools / planner, compute/storage separation, stateless agents, context engineering, prompt indexes and context routing.

1. Chapter 10 will discuss token reduction, distillation, small models and tiered compute, with emphasis on separating token-count reduction from per-token compute-cost reduction.

1. Chapter 11 will treat agents as production systems, focusing on idempotency, optimistic locking, state machines, retries, degradation, escalation, observability, audit, replay and reconciliation.

1. Chapter 12 will cover multi-agent, multi-tenant and concurrent scheduling, moving the Planner-to-Scheduler analogy from single-task execution to resource contention and orchestration.

1. Chapter 13 will add the missing agent security model, including prompt injection as exploit, tool capability boundaries, sandboxing, least privilege and audit.

1. Chapter 14 will return to the agent operating system idea and connect memory, tools, planning, security, scheduling and production reliability into one system view.
