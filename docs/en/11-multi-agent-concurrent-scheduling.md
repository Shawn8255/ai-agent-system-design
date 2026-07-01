# Chapter 11. Multi-Agent, Concurrent Scheduling and Multi-Tenancy

> Chapter focus: move the planner/scheduler analogy from single-task execution into multi-agent, multi-task and multi-tenant resource contention.

## 11.1 The Question

The previous chapters mostly looked at one agent executing one task: read context, plan steps, call tools and update state. But the most literal part of the OS analogy is not the single-task planner. It is concurrent scheduling.

A real platform will not run just one agent. It will serve many users, tenants, task queues, tool calls and model tiers at the same time. The questions become: who runs first? How much token, time, tool quota and external API capacity can each task consume? Which tasks may run concurrently, and which must be serialized? How are failures isolated?

This is where an Agent OS or AIOS becomes valuable: not merely making one agent run, but making many agents run on shared resources in a controlled way.

## 11.2 A Single-Task Planner Is Not a Global Scheduler

The planner orders steps inside one task. The scheduler allocates resources across tasks. These roles should not be collapsed.

An agent's planner may decide, "search again and call the model one more time." The global scheduler may know that the tenant is close to its budget, the same file is being modified by another task or an external API is rate-limited. The system should then pause, queue, degrade or reject the request.

| Component | Scope | Decision |
| --- | --- | --- |
| Planner | Inside one task | Next step, retry, finish |
| Scheduler | Across tasks | Who runs first, resource allocation, isolation |
| Runtime | Execution environment | Tool calls, state records, permission checks |
| Policy Engine | Constraints | Quotas, priorities, tenant boundaries, risk level |

## 11.3 Resource Dimensions for Agent Tasks

Traditional service schedulers manage CPU, memory, IO and network. Agent scheduling adds several special resources.

The first is token budget. Long context and multi-round reasoning can expand cost quickly. The second is model concurrency: different model tiers have different rate limits and prices. The third is tool quota, including search, mail, GitHub, databases, browsers and shell. The fourth is the external side-effect window, where some operations need exclusive locks or approval.

These resources cannot always be handled by one queue. Read tasks can run concurrently. Writes to the same object need serialization. High-risk tasks need an approval queue. Low-value tasks can be degraded or delayed.

This also exposes the limit of the agent-scheduler / OS-scheduler analogy. The CPU time an OS schedules is homogeneous, preemptible and precisely metered: a time slice is a time slice, preemption is almost free, and a swapped-out process resumes unchanged. Agent resources are not like that. Token budgets and model calls are neither preemptible nor easy to reclaim mid-flight, once a large-model call is issued you pay for it and cannot "slice back"; model tiers differ tenfold in price and are not interchangeable units; and a tool call with side effects cannot simply be swapped out and resumed once executed. So the agent scheduler borrows the "quota, priority, isolation" ideas from OS scheduling, but it governs a set of heterogeneous, partly non-preemptible resources that carry real side effects, which puts it closer to admission control under cost and risk constraints than to classical time-slice round-robin.

## 11.4 Multi-Tenant Isolation

A multi-tenant agent platform must isolate context, memory, tool permissions, logs and cost.

The most dangerous failure is not that one task is slow. It is that one tenant's context leaks into another tenant, or one user's tool capability is reused by another task. Context routing and memory reads must carry tenant, user, project and permission boundaries.

Multi-tenancy also means budget isolation. One tenant's infinite loop should not exhaust global model quota. One user's long task should not starve high-priority tasks. One failing tool should not block every queue.

## 11.5 Concurrent Writes and Locks

Agents often modify shared objects: files, issues, orders, database records, documents and calendar events. Concurrent writes need explicit policy.

| Scenario | Recommended Strategy |
| --- | --- |
| Read-only retrieval | Run concurrently and cache results |
| Writes to different objects | Run concurrently and record state separately |
| Writes to the same object | Object-level lock or optimistic lock |
| High-risk external side effects | Serialize and require confirmation |
| Long transaction | Split into short steps connected by a state machine |

Agents should not hold long pessimistic locks. A better pattern is short transactions, version checks, conflict detection and replanning. The system must surface conflicts explicitly instead of letting the model keep writing from stale context.

## 11.6 Redundant Execution and Agent Handoff

The previous sections assumed each task runs on exactly one agent. Real platforms are often the opposite: the same task can be picked up by several agents at once, a retry spawns a duplicate, a load balancer routes the request to two instances, or the user simply fires it again. Left unhandled, "multiple agents doing the same thing" turns straight into duplicated side effects: two emails sent, a card charged twice, two PRs opened.

This is an old problem in distributed systems, with a few mature patterns. First, deduplication and an exactly-once boundary: use the business-semantic idempotency keys from Chapter 10 so whoever persists first executes, and late arrivals just return the existing result. Second, leader election: allow only one agent to become the executor of a given task, with the rest observing or standing by. Third, work stealing: a standby agent takes over only when the holder times out or fails, rather than racing it from the start.

More subtle than dedup is agent handoff. A long task may change executors mid-flight: the original instance crashes, a rolling deploy replaces it, or the task is escalated to a more capable agent. The point of a handoff is not "copy the chat history over." It is handing over recoverable state: which step of the state machine we are on, which tool calls already produced side effects (with their idempotency keys), and which external sources the context should be rebuilt from. This is the payoff of the stateless agent from Chapter 6 — because state lives outside, the handoff can be clean.

| Scenario | Distributed analogue | Agent-side approach |
| --- | --- | --- |
| Multiple agents grab one task | Idempotent consumption / exactly-once | Deduplicate on a business-semantic key; first to persist executes |
| Only one executor allowed | Leader election | Task-level lock or lease; the rest stand by |
| Take over after the executor fails | Failover / work stealing | On lease timeout, a standby resumes from the state machine |
| Swap in a stronger agent mid-task | Process migration / checkpoint-restore | Hand over recoverable state, not a copy of the transcript |

The point: redundancy is not removed by "hoping the model won't repeat itself." It is controlled with idempotency keys, leases and externalized state. Design for duplicate execution as the default, and the platform stays correct under retries and failures.

## 11.7 Scheduling Policies

Agent scheduling can borrow classical policies, but it must adapt them to cost and risk.

FIFO is simple but lets long tasks block short ones. Priority queues protect high-value tasks but must avoid starving low-priority work. Budget scheduling limits token and tool cost. Deadline scheduling fits tasks with time windows. Risk scheduling sends high-impact operations into stricter queues.

The practical answer is usually a combination: apply quotas by tenant and user, split queues by task type, decide whether confirmation is needed by risk level, then schedule by model and tool availability.

## 11.8 Observability: From Trace to Load

A single agent trace explains one task. The scheduling system also needs global metrics: queue length, wait time, model concurrency, token usage, tool rate limits, failure rate, escalation rate, tenant budget and lock conflicts.

These metrics determine whether the system is healthy. An agent can look intelligent, but if it causes queue buildup, repeated retries, budget exhaustion or tenant starvation, the platform is still unreliable.

## 11.9 Summary

This chapter moved from the single-task view to the concurrent-system view. A planner solves ordering inside a task. A scheduler resolves competition across agents, tenants and resources.

This is one core value of an Agent OS: it provides queues, quotas, locks, isolation, scheduling policy and global observability. The next chapter covers another OS theme that cannot be skipped: security.
