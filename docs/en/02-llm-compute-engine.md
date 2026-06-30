# Chapter 2. LLM as a New Compute Engine

> Chapter focus: position the LLM as a compute node, not as the entire system.

![Figure 2](assets/figure-02.png)

Figure 2. LLM as an expensive compute engine inside an agent system.

## 2.1 The Question

People often mix products such as ChatGPT, Claude or Gemini with the underlying LLM. A product is not just a model. It usually includes a user interface, an agent layer, memory, tool calling, permissions, file handling, monitoring, billing and safety policies. The LLM is only the most important and often the most expensive compute node inside the larger system.

Thinking of the LLM as a compute engine helps clarify agent architecture. The model does not inherently store your long-term memory or your project history. It performs inference based on the context provided in the current request. The agent layer is responsible for recovering state, selecting information and calling tools.

## 2.2 System Role of the LLM

In classical systems, expensive compute services are rarely exposed directly to all business logic without a management layer. Search engines have indexing services. Databases have optimizers. GPU inference clusters may have batching, caching and routing layers in front of them.

LLMs should be understood in a similar way. They can process language, code, reasoning and planning, but that does not mean all state should live inside the model or every task should go directly to the largest model. An LLM is a powerful but expensive remote compute service. Every call consumes input tokens, output tokens, latency and GPU resources.

## 2.3 Stateless Compute

From the perspective of a single inference request, an LLM can mostly be treated as stateless compute. It does not permanently remember a specific user in its weights just because it had a conversation with that user in the previous turn. If the next request does not include the relevant context, the model cannot reliably know what happened before.

This means that when a product appears to remember you, the memory usually comes from the agent layer. The agent retrieves memory, recent conversation, file snippets and tool results, then composes them into the prompt. The model appears to remember because the required state has been restored for that request.

![Figure 3](assets/figure-03.png)

Figure 3. A stateless LLM requires the agent to restore context for each request.

## 2.4 LLM API as an Expensive Remote Call

Calling an LLM API is similar to calling an expensive remote service. It is slower than a local function call, more expensive than most database reads, and less deterministic than traditional APIs. Therefore, a central goal of agent design is reducing unnecessary calls to large models.

This mirrors classical system optimization. We used to reduce cross-service RPC calls, database queries and disk IO. Now we also reduce unnecessary LLM calls, redundant context and repeated reasoning. Tokens, context length, model tier and call count are becoming new performance metrics for AI systems.

## 2.5 Token Cost and Compute Cost Are Not the Same

It is important to distinguish token count from compute cost. Prompt compression, retrieval and indexing can directly reduce input tokens. Distillation, however, does not necessarily reduce token count. A small model and a large model may receive the same number of tokens, but the small model is cheaper to run.

Therefore, a more precise statement is that distillation primarily reduces the use of expensive large models, not necessarily the number of tokens. Token usage decreases only when distillation shortens the workflow, reduces repeated planning calls, or replaces several large-model calls with a smaller computation.

## 2.6 Analogy to Classical Compute

As a compute engine, an LLM can be compared to a database execution engine, a remote compute service or a GPU inference cluster. It is powerful, but it should not carry every responsibility in the system. A database does not own business workflow. A CPU does not perform operating-system scheduling by itself. Similarly, an LLM should not be viewed as the entire agent system.

This viewpoint explains why the agent layer matters. The agent does not replace the model; it ensures that the model is called at the right time, with the right context, and at a reasonable cost.

## 2.7 Summary

This chapter positions the LLM as a new high-capability compute engine. It is powerful, expensive, mostly stateless and usually accessed through an API. This explains why memory, context, tools and planning should be viewed as parts of the agent system rather than as properties of the model alone.
