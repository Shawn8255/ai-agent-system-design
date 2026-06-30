# Publication and Open Source Notes

This project is suitable for GitHub, but it is useful to separate public visibility from community co-authoring. A technical book is not the same as a codebase. Code has tests, interfaces and more objective correctness boundaries. A book depends more on a consistent authorial voice. The practical model is: the author owns the main line, while the community contributes corrections, examples, terminology discussions, translations and issues rather than rewriting chapters.

The main value of GitHub is visibility, feedback and credibility. It can host the complete artifact and serve as a portfolio piece for interviews or professional conversations. The README should state the positioning honestly: this is not pretending that AIOS, MemGPT or Compound AI Systems do not exist. It is a survey and engineering map with a distributed-systems and production-reliability perspective.

Contribution boundaries should be explicit. Typos, factual corrections, references, examples and translations are welcome. The main structure, chapter order and core thesis remain author-maintained. For prose, a Creative Commons license is usually more appropriate than an MIT license.

## Using X

X is better as a distribution channel than as the home for full chapters. One thread should carry one idea. The book is the source material; X is for single-point distribution.

The strongest first thread is the point that distillation does not directly reduce tokens. It has a counterintuitive claim, a cost model and a practical engineering tradeoff.

## Thread Draft: What Cost Does Distillation Actually Reduce?

1. I saw someone say they wanted to use distillation to save tokens. The direction is slightly off. Distillation usually does not reduce tokens; it reduces a different cost.

2. The cost of an agent call can be decomposed as: call count x tokens per call x cost per token. Three factors, three different optimization families.

3. A small model and a large model may consume the same number of tokens. Distillation changes the compute price of each token, not the number of tokens. In distributed-systems terms, it moves work to a cheaper compute tier; it does not reduce RPC payload size.

4. The techniques that actually reduce token count are different: RAG, context pruning, summarization, prompt caching, compressed tool outputs and planner iteration limits. These usually require no training and can work through engineering changes and configuration.

5. The one case where distillation can reduce total tokens is when it collapses a multi-round large-model workflow into one small-model step. In that case, the saved tokens come from removed calls; token reduction is a side effect.

6. If the goal is to save money, the practical order is: exhaust caching, pruning and call-count reduction first; then use routing or small models; consider distillation last. Distillation needs labeling, training, evaluation and hosting, so it usually belongs after stable traffic and data.

## Publishing Rhythm

The book does not need to be complete before it becomes public. Part I is already coherent. After one or two differentiating chapters, such as production reliability or security, it can start collecting feedback. X can break the book into weekly single-point threads, while GitHub remains the durable home for the full content.
