# Future Revision Notes

Part I now has a complete Chapter 1-13 draft. Future work should focus on public release quality, reader feedback and stronger examples rather than adding more chapters.

## 1. References and Literature

Later revisions should add fuller references for key claims, especially around AIOS, MemGPT, Compound AI Systems, LLM OS, prompt injection, sandboxing, agent security and multi-agent scheduling. The positioning should remain explicit: this book does not claim to invent those concepts. It organizes them through distributed systems and production reliability.

## 2. Cases and Examples

Chapter 9 now includes an end-to-end cost example that separately accounts for call count, tokens per call and cost per token; later revisions can add comparison data across task distributions. Chapter 10 now includes a payment idempotency and order state-machine analogy explaining why agent tool calls need idempotency, replay and reconciliation. Chapters 11-12 can add pseudo-flows for scheduling and security incidents.

## 3. Public Writing Material

The Chapter 9 argument that "distillation does not directly reduce tokens" is a good candidate for an X thread. The anchor can be:

```text
Total cost ~= call count x tokens per call x cost per token
```

This formula makes the separation clear: context engineering mostly reduces token volume, planner limits and caching reduce call count, and distillation plus routing reduce per-token cost.

## 4. Bilingual Consistency

Whenever the Chinese prose changes, the English version should be checked for an equivalent update. The terminology table should keep LLM, Agent, Memory, Context, Tool, Planner, Context Routing, Distillation, Sandbox, Idempotency, Replay, Scheduler, Capability Boundary and Agent OS stable.

## 5. Release Checklist

Before a public release, run one full release pass: Markdown links, DOCX/PDF generation, figure rendering, chapter status, README wording, license choice and contribution boundaries. The manuscript can accept errata, examples and translation improvements, while the main structure should remain author-maintained.

## 6. Part II Progress and Further Directions

Part II now opens with Chapter 14, which formally discusses moving memory, skill and routing from rule-driven to learned (learned memory, learned skill, learned routing), and uses the database precedent of "from query optimizer to learned index" to show the engineering feasibility and limits.

Beyond that, Part II can continue along the following directions (not yet drafted):

- Evaluation systems for learned components: how to build independent, reproducible evaluation sets for learned memory / skill / routing, avoiding inflated metrics from self-assessment on online data.
- Stability of online learning: distribution-drift detection, policy fallback mechanisms, and convergence and safety boundaries under delayed feedback.
- Learning in multi-agent collaboration: when multiple agents share memory and skills, how to avoid feedback loops that amplify each other's bias, and how to isolate and reuse skills across tenants.

The writing should keep the book's usual restraint: give analogies and limits, and do not promise unproven results. The payoff of these directions depends on a stable task distribution, an evaluation system and enough samples.

> Note: the topics "multi-agent redundant execution and handoff" and "standards and portability across agent runtimes" have been incorporated into the main text of Chapter 11 (11.6) and Chapter 13 (13.6) respectively.
