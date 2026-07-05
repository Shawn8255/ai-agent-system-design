# Chapter 3. Agent as an Orchestrator

> Chapter focus: the agent is the orchestration layer that routes work to the right resource.

![Figure 4](assets/figure-04.png)

Figure 4. The agent as an orchestrator rather than a chatbot.

## 3.1 The Question

If the LLM is the compute engine, what is the agent? A common misunderstanding is to treat an agent as a wrapper around a large model or as a chatbot with tools. That description captures part of the surface behavior, but it misses the architectural role.

A better definition is that an agent is an orchestrator. It receives a user goal, restores relevant state, selects context, decides whether to call tools, chooses which model or compute layer to use, and organizes multiple steps into an executable workflow.

## 3.2 Core Components of an Agent

A typical agent contains several logical components. Memory stores long-term preferences, project background and task history. A context builder decides what should enter the current prompt. A planner decomposes the user goal into steps. A tool layer calls external systems. A router or scheduler decides whether to use rules, small models or large models. An evaluator or guardrail decides whether the result is reliable enough.

These components may be physically distributed across multiple services or hidden inside a product. But logically, they are part of the agent layer, not part of the LLM itself.

## 3.3 Typical Execution Flow

When an agent receives a request, it should not immediately send the raw user message to the largest model. A more efficient flow is to classify the task, retrieve relevant memory or files, build context, then select a compute resource. If a simple rule can solve the task, no model is needed. If the task matches a common pattern, a small model may be enough. If the task is complex or risky, the agent escalates to a large model.

This is the difference between a chatbot and an agent. A chatbot tends to map one input to one response. An agent receives a goal and organizes a set of computations and operations to complete it.

## 3.4 Agent, API Gateway and Scheduler

From a systems perspective, an agent resembles a mixture of API gateway, workflow engine and scheduler. It exposes a unified interface to the user while connecting internally to models, tools, memory, files and external services. It also chooses an execution path based on task complexity and cost.

That is the role of an orchestrator. It may not perform all computation by itself, but it decides which resources participate, in what order they participate, how results are combined, and whether failures should trigger retries, fallbacks or escalation.

## 3.5 Tiered Compute: Rule, Cache, Small Model, Large Model

Agent scheduling can be abstracted as tiered compute. The lowest layer is rules: lowest cost and fastest, but limited coverage. The next layer is cache or retrieval, which reuses existing results or finds relevant context. Above that is a small model. A small model does not store fixed answers like a cache; it stores capabilities learned through training or distillation. The highest layer is the large model, which is the most capable and the most expensive.

This resembles multi-level caches, hot/cold storage tiers and service degradation strategies in traditional systems. A good agent should not route every request directly to the most expensive model. It should solve as many requests as possible at cheaper layers.

![Figure 5](assets/figure-05.png)

Figure 5. Tiered compute prevents every request from hitting the largest model.

## 3.6 Why a Small Model Is Not Just a Cache

Small models are sometimes compared to caches, but that analogy needs refinement. A normal cache stores results. On a hit, it returns a fixed value. A small model stores capability. It still performs inference based on the input. It cannot guarantee a fixed answer like Redis, but it can generalize to problems that were not explicitly seen during training.

A better phrase is capability cache. Distillation compresses behavior observed from a larger model into a lower-cost compute layer. It does not eliminate computation; it moves computation from an expensive model to a cheaper model.

## 3.7 Risks and Limits of Agent Orchestration

An agent as orchestrator introduces new risks. A bad router may send simple tasks to an expensive model or complex tasks to an underpowered model. Bad memory retrieval can make the model reason over the wrong context. Multi-step tool calls can amplify small mistakes. Probabilistic model behavior makes traditional testing incomplete.

Therefore, agent systems need observability, logs, audits, replay, evaluation sets and escalation policies. This again shows that agents are not just conversation interfaces. They are software systems that need system engineering discipline.

## 3.8 Harness: The Industry's Other Name for This Layer

The previous sections positioned the agent as an orchestrator, the term this book uses. The industry has another, increasingly common word for the same layer: harness. Anthropic calls Claude Code a harness. Teams like METR that evaluate agent capability routinely talk about "running a benchmark with harness X on model Y." Both words point at the same thing: the runtime around an LLM responsible for tool calls, context construction and the execution loop.

The terms differ, but the boundaries are worth separating clearly, especially from a third concept that gets blended in: the framework.

| Concept | What it is | Example |
| --- | --- | --- |
| LLM | Stateless inference engine | A specific model |
| Framework | A toolkit for building a harness; not itself a running agent | A general-purpose agent-building library |
| Harness | The running runtime scaffold: tool definitions, execution loop, context management, permissions | Claude Code, various coding-agent products |
| Agent | Model + harness + tools + memory combined into a system that completes tasks autonomously | One concrete execution instance |

There is a fact here that is easy to overlook but matters for system design: a harness and the model running behind it are not locked into a one-to-one pair. Some harnesses are indeed built around a single model, but a more common pattern is a model-agnostic harness that can plug in models from different vendors, or even route different steps of the same task to different models within one harness — cheap models for low-risk steps, the strongest model only for the steps that need it. This is the tiered compute idea from section 3.5 showing up at the harness level: the thing being tiered is not just "whether to call the large model," but "which vendor's model handles this particular step."

This decoupling matters again in section 13.6: once harnesses and models can be freely combined, keeping harnesses interoperable with each other becomes a problem that needs standardized interfaces to solve.

## 3.9 Summary

This chapter positions the agent as an orchestrator, also commonly called a harness in the industry. It is not the model itself. It is the system layer that organizes memory, tools, planning, context and resource scheduling around the model. This prepares the ground for later chapters: why memory resembles storage, why AGENTS.md resembles an index, why distillation resembles tiered compute, and why multi-agent systems increasingly resemble distributed systems.
