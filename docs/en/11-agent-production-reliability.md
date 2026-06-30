# Chapter 11. Agent Production Reliability: Idempotency, State Machines and Replay

> Chapter focus: treat agents as production systems that need SLAs, audit, replay and reconciliation, not just intelligent flows that can run.

## 11.1 The Question

Many agent architecture discussions stop at "the model can plan, call tools and finish the task." That is a prototype. In production, the harder question is not whether the agent can reason. It is whether the system remains controlled when the agent fails.

If an agent sends two emails, charges twice, overwrites the wrong file or writes half-completed state into a database, the user will not care why the planner thought it was reasonable. A production system must answer: has this step already executed? Can it be retried? What is the current state? Who authorized it? Can we replay the execution? Can we reconcile it?

This chapter is the most production-oriented part of the book. An agent is not merely a chat window. It is a distributed workflow that can produce side effects.

## 11.2 Side-Effect Boundaries

Read-only tasks and write tasks have completely different risk profiles. Summarizing a document, explaining code and looking up information can usually be retried. Sending email, creating pull requests, changing orders, calling payments, writing CRM records and running shell commands cross a side-effect boundary.

Once the boundary is crossed, the system cannot rely on "the model probably will not do it twice." It needs explicit records of intent, execution result and idempotency keys.

| Operation Type | Example | Reliability Requirement |
| --- | --- | --- |
| Read-only | Search, file read, database query | Retryable and cacheable |
| Reversible write | Draft email, generated file, created issue | State record, rollback or overwrite path |
| External side effect | Send email, payment, shipment, deployment | Idempotency, authorization, audit, confirmation |
| Irreversible operation | Delete data, close account, production migration | Strong approval, isolation, replay evidence |

## 11.3 Idempotency Is the First Tool Constraint

Agents naturally retry. The model may be uncertain, the tool may time out, the network may fail and the planner may decide to run a step again. Without idempotent tools, retries become incidents.

Idempotency keys should be generated from business semantics, not random request IDs. "Create a refund for user A's order B" is a better idempotency boundary than "tool call number 17." The former expresses intent. The latter only describes execution.

The tool layer should return explicit states: executed, duplicate request, retryable failure, non-retryable failure or human confirmation required. The agent should not infer the next action from free-form error text.

## 11.4 State Machines Beat Free Text

Agents are good at explanations, but production state should not live only in free text. Orders, payments, deployments, approvals, file modifications and multi-step tasks need explicit state machines.

A state machine limits the next step. It tells the system which transitions are legal, which operations need locks, which failures can be retried and which failures must escalate.

```text
planned -> approved -> executing -> succeeded
                    \-> retryable_failed -> executing
                    \-> terminal_failed
                    \-> needs_human
```

The model may participate in judgment, but state transitions should be validated by the system. An agent can suggest "execute the refund next," but the system must check whether the current state allows it, whether an idempotency key exists and whether the capability is authorized.

## 11.5 Optimistic Locking and Concurrent Changes

Agents often run long tasks. By the time an agent writes, the outside world may have changed: a user edited the file, another person closed the issue, an order status changed or approval was revoked.

Writes therefore need version checks. Optimistic locks, ETags, revisions, updated_at values and compare-and-set all answer the same question: which version did the agent reason from?

If the version does not match, the correct behavior is usually not to overwrite. The agent should reread, replan or escalate for confirmation. For agents, "my context is stale" must be a first-class error.

## 11.6 Retry, Degradation and Escalation

Production agents need explicit failure classes.

| Failure Type | Example | Handling |
| --- | --- | --- |
| Transient failure | Timeout, rate limit, unavailable service | Backoff, retry, keep idempotency key |
| Context failure | Missing information, version conflict, unreliable retrieval | Reread and rebuild context |
| Capability failure | Low small-model confidence, unsupported tool case | Escalate to large model or human |
| Policy failure | Insufficient permission, high-risk operation | Stop and request authorization |
| Terminal failure | Business rule rejection, unrecoverable error | Record final state and stop retrying |

Without failure classes, agents drift between "try again" and "give up." Reliable systems put the policy into the runtime instead of improvising it in each prompt.

## 11.7 Observability, Audit and Replay

Agent execution logs should not be just chat transcripts. Production logs need at least model-input summaries, tool calls, parameters, return states, state transitions, permission checks, user confirmations and final outputs.

The goal of replay is not to reproduce the exact same model tokens. It is to reconstruct enough causality: what information the agent used, what decision it made, which tool produced a side effect and how the system verified that the side effect was not duplicated.

Reconciliation also matters. After an agent modifies an external system, local state, external state and user-visible state must be comparable. Payment systems need reconciliation. Agent workflows need it too.

## 11.8 Summary

This chapter placed agents inside the production-system frame. A reliable agent does not merely call tools. It has idempotency keys, state machines, version checks, failure classes, audit logs, replay and reconciliation.

This is a key difference from many OS-analogy architecture discussions. Running is only the start. Being retryable, auditable, recoverable and explainable is what makes a production system. The next chapter moves the OS analogy to its most literal part: multi-agent, multi-tenant concurrent scheduling.
