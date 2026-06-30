# Chapter 10. Token Reduction, Distillation and Tiered Compute

> Chapter focus: separate agent cost into call count, tokens per call and cost per token, so distillation is not confused with token reduction.

## 10.1 The Question

One of the easiest phrases to get wrong in agent cost discussions is: "use distillation to reduce tokens." The phrase points at a real problem: agents can be expensive. But it mixes two different optimization axes.

If a small model and a large model receive the same prompt, the input token count does not become smaller just because the model is smaller. Distillation mainly reduces the compute cost of processing each token, or moves a class of tasks into a cheaper compute layer. Token count is reduced by context trimming, output compression, caching, fewer round trips and planner limits.

This chapter separates those costs.

## 10.2 A Simple Cost Model

An agent's cost can be approximated as:

```text
Total cost ~= call count x tokens per call x cost per token
```

This is not a billing formula. It is an engineering model. Its value is that it puts each optimization in the right place.

The planner influences call count. Context engineering influences tokens per call. Distillation, small models and routing influence cost per token. When a system becomes expensive, the first question is which factor is growing, not whether the model is generally too expensive.

## 10.3 Two Orthogonal Axes

| Dimension | Reduce Token Count | Reduce Per-Token Compute Cost |
| --- | --- | --- |
| Target | Tokens sent to and produced by each request | Compute or price needed to process the same tokens |
| Distributed-systems analogy | Fewer RPCs, smaller payloads, fewer round trips | Move work to a cheaper compute layer |
| Typical techniques | RAG, trimming, summarization, prompt caching, compressed tool output, planner iteration limits | Distillation, small models, routing, cascades |
| Training required | Usually no; engineering and configuration are enough | Distillation yes; routing and existing small models not always |
| Time to impact | Low cost and fast | Distillation is expensive; routing is medium |
| Main risk | Over-trimming and losing context | Wrong routing tier causes waste or errors |
| Priority for indie developers | Do first | Do after traffic and data stabilize |

These axes can be stacked, but they do not replace each other. Smaller payloads do not change the model price. Smaller models do not automatically shrink payloads.

## 10.4 What Actually Reduces Tokens

Reducing tokens is an IO problem: read less, transmit less, write less and loop less.

First, context engineering uses retrieval, trimming, summarization and structured rewriting so the model only sees the working set needed for the current task. The context builder, prompt index and context routing from Chapters 7-9 all serve this purpose.

Second, prompt caching can make stable prefixes cheaper. System prompts, tool definitions, project rules and AGENTS.md-like files repeat inside agent loops and are good cache candidates.

Third, tool output must be compressed. Shell output, logs, search results and API responses should not be pasted back into the model unchanged. The tool layer should preserve facts, state, error codes and verifiable references while removing noise.

Fourth, planners need iteration limits. Many agent costs do not come from one long prompt. They come from an unbounded loop of think, search, think again and call another tool.

## 10.5 What Distillation Optimizes

Distillation moves capability from a large model into a small model or fixed workflow for a class of tasks. It reduces unit compute cost. It does not directly shorten the context.

If both models receive 8k tokens, both still process 8k tokens. The smaller model is cheaper, possibly faster and easier to run at higher throughput.

Distillation reduces total tokens only in one indirect case: when it collapses a multi-round large-model workflow into a single small-model call. The saved tokens come from removed calls, not from distillation making each prompt shorter. Token reduction is a side effect, not the direct target.

## 10.6 Tiered Compute

The more precise design is not "distill to save tokens." It is tiered compute.

Simple, stable, frequent and low-risk tasks can be handled by small models, rules, caches or precomputed results. Complex, open-ended, high-risk and cross-context tasks should escalate to large models. This resembles hot/cold tiering, service degradation and request routing.

| Tier | Suitable Work | Typical Implementation |
| --- | --- | --- |
| Cache / Rule | Deterministic or repeated requests | Prompt cache, templates, rules |
| Small Model | Classification, extraction, rewriting, low-risk judgment | Small or distilled model |
| Large Model | Complex planning, cross-context reasoning, high-risk decisions | General-purpose large model |
| Human Escalation | High-impact, low-confidence or irreversible operations | Confirmation and approval flow |

The key is not model size by itself. The key is the routing policy: when to use a cheap tier, when to escalate and when to stop.

## 10.7 A Realistic Order for Independent Developers

For independent developers, distillation is rarely the first move. It requires labeled data, a training pipeline, evaluation, deployment and enough stable traffic to justify the work.

The practical order is usually to squeeze the first two factors first: reduce call count and tokens per call. Caching, trimming, tool-output compression, retrieval filtering, planner limits and model routing often produce savings without training.

Once the system has a stable task distribution, enough samples and clear evals, distillation may be worth considering. Before that, it can easily become an expensive engineering project with unclear payoff.

## 10.8 Summary

This chapter separated agent cost into three factors: call count, tokens per call and cost per token. Token reduction mostly optimizes the first two. Distillation mostly optimizes the third.

That distinction matters because it sets engineering priorities. To reduce cost, start with caching, trimming, compression and routing before distillation. The next chapter moves from cost to reliability: if agents enter production systems, they need idempotency, state machines, replay and reconciliation.
