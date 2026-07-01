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

## 6. Part II Direction: Letting Agents Learn Their Own Memory and Skills (Forward-Looking)

Part I treats memory, context, distillation and routing as components driven by engineering rules: humans decide the pruning strategy, the recall strategy and the routing thresholds. A natural forward-looking direction is to hand those decisions themselves to learning. This is research-oriented, so it is kept as a separate Part II rather than mixed into Part I's production-constraint voice.

- Learned memory: instead of fixed rules deciding "what to store, what to recall, when to promote a result into a long-term fact," use a model to learn the memory-management policy from past tasks, the way learned indexes and adaptive query optimizers do in databases. The core analogy follows Chapters 4 and 7: reading memory already resembles retrieval with relevance ranking, and the ranker can be learned.
- Learned skill: gradually solidify recurring workflows from "re-plan with the large model every time" into skills. This is the same thread as distillation in Chapter 9, but it emphasizes online accumulation — the agent discovers stable patterns in use, then pushes them down into a small model or a fixed workflow.
- Learned routing: use reinforcement or online learning to tune the routing thresholds of tiered compute (Chapter 9), deciding when to escalate and when to stop based on real confidence and cost feedback.

The writing should keep the book's usual restraint: give analogies and limits, and do not promise unproven results. The payoff of these directions depends on a stable task distribution, an evaluation system and enough samples.

> Note: the topics "multi-agent redundant execution and handoff" and "standards and portability across agent runtimes" have been incorporated into the main text of Chapter 11 (11.6) and Chapter 13 (13.6) respectively, and are no longer separate Part II directions.
