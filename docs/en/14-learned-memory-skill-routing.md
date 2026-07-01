# Chapter 14. Part II Opening: Learned Memory, Skill and Routing

> Chapter focus: the start of Part II. Revisit the components Part I treated as rule-driven and ask which of them can be learned — while keeping the runtime boundaries Part I established.

## 14.1 The Question

Part I (Chapters 1-13) carried an implicit premise: memory pruning and recall, context selection, the timing of distillation and the routing thresholds were all decided by human-written rules. Engineers define "keep the last N items," "recall only above similarity t," "escalate to the large model below confidence c." These rules are clear, auditable and controllable — which is exactly what Part I wanted.

But rules have a ceiling. Task distributions shift, users change, cost structures change, and hand-tuned thresholds quickly stop being optimal. A natural question follows: can those decisions themselves be learned? Let the agent learn from its own history what to store, what to recall, which workflow to solidify and when to escalate the model.

This is where Part II begins. The register needs to be clear first: this chapter discusses directions and boundaries, not finished, battle-tested solutions. It is closer to a feasibility analysis of the step "replace Part I's rule-based components with learnable ones" — the upside is attractive, and the risks are concrete.

| Part I rule-based component | Part II learned direction | Learning signal |
| --- | --- | --- |
| Memory pruning / recall rules | Learned memory | Whether it is later reused; task success |
| Distillation timing (human-set) | Learned skill | Workflow frequency and stability |
| Routing thresholds (human-set) | Learned routing | Confidence, cost, whether escalation helped |

## 14.2 A Precedent That Already Exists: From Query Optimizer to Learned Index

Databases have walked this path. A traditional query optimizer uses a hand-written cost model to estimate scan cost and choose indexes; then adaptive optimizers appeared, correcting estimates with runtime feedback; then the "learned index" used a model to learn the data distribution directly, turning a "key to position" lookup into a prediction — faster and more space-efficient than a classic B-tree on some workloads.

This precedent matters here because Chapter 7 already framed context engineering as query optimization. If a query optimizer can evolve from a hand-written cost model to a learned one, then an agent's context builder, router and memory management can logically follow the same path: from hand-written policies to policies learned from data.

But remember the lesson of the learned index: it is not unconditionally better. It pays off on stable, predictable distributions; when the distribution shifts frequently, the learned model goes stale and must be retrained or fall back to the traditional structure. This dependence on stability runs through all three directions in this chapter.

## 14.3 Learned Memory: Learning What to Store, Recall and Promote

Chapter 4 noted that reading memory already resembles retrieval with relevance ranking, not a precise SQL query. If it is ranking, the ranker can be learned. The core of learned memory is handing three rule-decided actions to a model: writing (which results are worth promoting into long-term facts), recall (which entries the current task should pull in) and eviction (which memories are stale and can be dropped).

The learning signal comes from the agent's own execution history. After a memory is written, do later tasks actually reuse it? After recalling a memory, did the task succeed or was it misled? This feedback can train a policy that gradually approaches "high hit rate, low pollution" memory management — exactly the goal Chapter 7 stressed: over-recall pollutes the context, under-recall makes the model guess.

The risks are concrete. First, feedback loops: the agent recalls memory using a learned policy, and the recalled results shape the next training signal, which easily reinforces bias. Second, evaluation: how good a memory policy is needs an independent evaluation set, not self-assessment on the same online data. Third, fallback: once a learned policy degrades on a new distribution, the system must be able to fall back to rule-based recall instead of amplifying the error.

## 14.4 Learned Skill: From "Re-plan Every Time" to Solidified Skills

Chapter 9 defined distillation as moving large-model capability into a small model or fixed workflow. That chapter took a mostly offline view: first a stable task distribution, then distillation. Learned skill is its online version: in use, the agent continuously discovers recurring, stable workflows and solidifies them into a skill — a small model, a parameterized flow, or a reusable tool sequence.

The key judgment is when solidifying is worth it. A workflow that appears often, is structurally stable and forces the large model to re-plan every time is a good candidate; a low-frequency, always-different task will only bring maintenance cost and overfitting risk. This matches Chapter 9's "distillation last" discipline: prove the pattern is stable, then solidify.

After solidifying, the boundaries still hold. A learned skill must not bypass the constraints of Chapters 10-13 just because it "looks like it can run automatically" — the side effects it produces still need idempotency keys, state machines, capability boundaries and sandboxes. Learning optimizes "how to do it faster and cheaper," not "whether safety and reliability can be skipped."

## 14.5 Learned Routing: Learning the Thresholds of Tiered Compute

The tiered compute of Chapter 9 depends on a set of human-set thresholds: when to use a small model, when to escalate to a large one, when to stop. Learned routing uses online or reinforcement learning to tune these thresholds so the routing policy adapts to real feedback.

The reward signal is a combination of cost and quality: a task routed to a small model whose result is accepted is a cheap win; one that the user rejects or that needs rework later pays the price for a wrong downgrade. The router must balance exploration (occasionally trying a cheaper tier) against exploitation (using the tier known to work) — the classic exploration/exploitation problem.

But routing errors are asymmetric. Wrongly escalating a simple task to a large model only wastes money; wrongly downgrading a high-risk task to a small model can cause real harm. So learned routing must carry a rule-based safety envelope: high-risk, irreversible operations do not participate in "downgrade to save money" learning and always take the conservative path. Learning can optimize average cost, but it must not trade away tail risk.

## 14.6 Shared Engineering Constraints of Learned Components

The three directions look different, but their underlying engineering constraints are highly aligned. None of them is "plug in a model and it gets better." Each must satisfy a set of preconditions, or learning becomes an uncontrolled source of risk.

| Constraint | Meaning | Consequence if unmet |
| --- | --- | --- |
| Stable task distribution | The learned policy depends on a relatively stable distribution | After drift the policy goes stale and biases worsen |
| Independent evaluation set | Measure the policy with independent data | Self-assessment causes overfitting and inflated metrics |
| Bounded feedback delay | The reward signal cannot lag too much | Wrong decisions cannot be corrected in time |
| Rule-based safety envelope | High-risk decisions are not left to learning | Tail risk is amplified into incidents |
| Fallback | Revert to rule policy at any time | No safety net when learning degrades |

This table really carries Part I's discipline into Part II: learned components still live inside the same runtime boundaries — idempotency, state machines, capability boundaries, sandboxes, observability and replay, none of them dropped. The only difference is that the decision policy went from hand-written to learned, while the boundaries stay the same.

## 14.7 When Not to Learn

Learning is not the default better option. In several situations, rules are clearly more appropriate. First, cold start: with too little history, a learned policy is worse than one clear rule. Second, low-frequency tasks: too few occurrences give learning no signal and only cause overfitting. Third, high-risk and irreversible: operations whose error cost is unacceptable should use conservative rules, not a learned policy that may fail. Fourth, strong auditability: some compliance settings require explainable, traceable decisions, and a black-box learned policy becomes a liability.

This is the same logic as Chapter 9's advice to independent developers: first squeeze the deterministic wins from rules, caching and trimming, and only after stable traffic, enough samples and clear evaluation consider learning a specific decision. Learning is a heavy weapon, not an opening move.

## 14.8 Summary and Part II Outlook

This chapter revisited several rule-driven decisions from Part I — memory management, skill solidification, tiered routing — as components that can be learned, and used the database precedent of "from query optimizer to learned index" to show the path has engineering grounding.

But the core conclusion is restrained: learning optimizes the decision policy, not the safety and reliability boundaries. A learned memory policy, skill or router still lives inside the runtime built in Chapters 10-13, and still has to satisfy stable distribution, independent evaluation, fallback and a rule-based safety envelope.

This is also the tone of Part II as a whole: Part I answered "how to put the model inside a runtime controlled like an operating system," and Part II continues by asking "can the decisions inside that runtime learn to be better themselves." It is an open direction, and later chapters will continue along evaluation systems, the stability of online learning and learning within multi-agent collaboration.
