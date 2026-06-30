# Chapter 9. Token Reduction, Distillation and Tiered Compute

> Chapter focus: separate agent cost into call count, tokens per call and cost per token, so distillation is not confused with token reduction.

## 9.1 The Question

One of the easiest phrases to get wrong in agent cost discussions is: "use distillation to reduce tokens." The phrase points at a real problem: agents can be expensive. But it mixes two different optimization axes.

If a small model and a large model receive the same prompt, the input token count does not become smaller just because the model is smaller. Distillation mainly reduces the compute cost of processing each token, or moves a class of tasks into a cheaper compute layer. Token count is reduced by context trimming, output compression, caching, fewer round trips and planner limits.

This chapter separates those costs.

## 9.2 A Simple Cost Model

An agent's cost can be approximated as:

```text
Total cost ~= call count x tokens per call x cost per token
```

This is not a billing formula. It is an engineering model. Its value is that it puts each optimization in the right place.

The planner influences call count. Context engineering influences tokens per call. Distillation, small models and routing influence cost per token. When a system becomes expensive, the first question is which factor is growing, not whether the model is generally too expensive.

## 9.3 An End-to-End Cost Example

An abstract formula only means something once it lands on concrete numbers. Consider a common task: an agent that summarizes a GitHub issue and drafts a reply. To keep the arithmetic clear, use an illustrative price set (not tied to any specific vendor): a large model at roughly $3 per million input tokens and $15 per million output tokens, and a small model at about one tenth of that.

Start with a naive implementation. Every step pushes the full issue, the entire comment history and the whole repository AGENTS.md into context, and the planner iterates freely:

| Step | Model | Input tokens | Output tokens | Note |
| --- | --- | --- | --- | --- |
| Read and understand the issue | Large | 9,000 | 500 | All comments + full AGENTS.md |
| Retrieve related code | Large | 8,000 | 400 | Untrimmed top-k chunks |
| Think one more step | Large | 8,500 | 400 | Planner with no stop condition |
| Draft the reply | Large | 9,500 | 700 | Carries the context again |

Four calls: about 35,000 input tokens and 2,000 output tokens. At the illustrative prices: input 35,000 x $3/1e6 ~= $0.105, output 2,000 x $15/1e6 ~= $0.030, about **$0.135** per task.

Now optimize each of the three factors. First, cut call count: merge "understand + retrieve + draft" and cap planner iterations, dropping from four calls to two. Second, cut tokens per call: keep only the issue body and a summary of the three latest comments, move AGENTS.md into a cached stable prefix, and trim retrieval to the two chunks that actually matter. Third, cut cost per token: route low-risk subtasks such as "classify the issue and extract key fields" to a small model.

| Step | Model | Input tokens | Output tokens | Note |
| --- | --- | --- | --- | --- |
| Classify and extract key points | Small | 2,500 | 300 | Low risk, safe to route down |
| Retrieve + draft reply | Large | 4,000 | 700 | Cached prefix + trimmed context |

The small-model call: input 2,500 x $0.3/1e6 + output 300 x $1.5/1e6 ~= $0.0012. The large-model call: input 4,000 x $3/1e6 + output 700 x $15/1e6 ~= $0.0225. About **$0.024** per task, roughly one fifth of the naive version.

The point is not the exact "82% saved" figure. It is three things. First, the three factors fall independently and multiply together, so the savings compound rather than add. Second, the cheapest, fastest wins, merging calls and trimming context, need no training; they are just structural changes. Third, the model tier (routing to a small model) is used on only one low-risk subtask; it contributes the per-token cost reduction but is not the main source of savings here. Getting this arithmetic straight is what tells you which factor to optimize first.

## 9.4 Two Orthogonal Axes

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

## 9.5 What Actually Reduces Tokens

Reducing tokens is an IO problem: read less, transmit less, write less and loop less.

First, context engineering uses retrieval, trimming, summarization and structured rewriting so the model only sees the working set needed for the current task. The context builder, prompt index and context routing from Chapters 7-8 all serve this purpose.

Second, prompt caching can make stable prefixes cheaper. System prompts, tool definitions, project rules and AGENTS.md-like files repeat inside agent loops and are good cache candidates.

Third, tool output must be compressed. Shell output, logs, search results and API responses should not be pasted back into the model unchanged. The tool layer should preserve facts, state, error codes and verifiable references while removing noise.

Fourth, planners need iteration limits. Many agent costs do not come from one long prompt. They come from an unbounded loop of think, search, think again and call another tool.

## 9.6 What Distillation Optimizes

Distillation moves capability from a large model into a small model or fixed workflow for a class of tasks. It reduces unit compute cost. It does not directly shorten the context.

If both models receive 8k tokens, both still process 8k tokens. The smaller model is cheaper, possibly faster and easier to run at higher throughput.

Distillation reduces total tokens only in one indirect case: when it collapses a multi-round large-model workflow into a single small-model call. The saved tokens come from removed calls, not from distillation making each prompt shorter. Token reduction is a side effect, not the direct target.

## 9.7 Tiered Compute

The more precise design is not "distill to save tokens." It is tiered compute.

Simple, stable, frequent and low-risk tasks can be handled by small models, rules, caches or precomputed results. Complex, open-ended, high-risk and cross-context tasks should escalate to large models. This resembles hot/cold tiering, service degradation and request routing.

| Tier | Suitable Work | Typical Implementation |
| --- | --- | --- |
| Cache / Rule | Deterministic or repeated requests | Prompt cache, templates, rules |
| Small Model | Classification, extraction, rewriting, low-risk judgment | Small or distilled model |
| Large Model | Complex planning, cross-context reasoning, high-risk decisions | General-purpose large model |
| Human Escalation | High-impact, low-confidence or irreversible operations | Confirmation and approval flow |

The key is not model size by itself. The key is the routing policy: when to use a cheap tier, when to escalate and when to stop.

## 9.8 A Realistic Order for Independent Developers

For independent developers, distillation is rarely the first move. It requires labeled data, a training pipeline, evaluation, deployment and enough stable traffic to justify the work.

The practical order is usually to squeeze the first two factors first: reduce call count and tokens per call. Caching, trimming, tool-output compression, retrieval filtering, planner limits and model routing often produce savings without training.

Once the system has a stable task distribution, enough samples and clear evals, distillation may be worth considering. Before that, it can easily become an expensive engineering project with unclear payoff.

## 9.9 Summary

This chapter separated agent cost into three factors: call count, tokens per call and cost per token. Token reduction mostly optimizes the first two. Distillation mostly optimizes the third.

That distinction matters because it sets engineering priorities. To reduce cost, start with caching, trimming, compression and routing before distillation. The next chapter moves from cost to reliability: if agents enter production systems, they need idempotency, state machines, replay and reconciliation.
