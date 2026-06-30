# 后续章节写作计划

第一部分已经完成前九章的基础架构视角。后续章节将沿着这条主线继续展开：Token Reduction 与 Distillation 的成本边界，Agent 作为生产系统的可靠性问题，多 Agent / 多租户调度，以及 Agent 安全和 Agent OS。

后续写作还需要补上三块更能体现工程差异化的内容。第一，Agent 安全不能只作为风险提示处理。OS 的安全模型会迁移到 Agent 系统里：Prompt Injection 更接近 exploit，工具调用需要权限边界，代码执行和外部系统访问需要 Sandbox。第二，并发调度是 OS 类比最直接的一部分，多 Agent、多租户、多任务队列和资源隔离，比单任务 Planner 更接近 Scheduler。第三，Agent 应该被当成生产系统来讨论：它需要 SLA、幂等、乐观锁、状态机、Retry、降级、升级、可观测、审计、回放和对账。这是本文区别于只讨论“能跑起来”的 OS-analogy 架构文章的重点。

1. 第 1-9 章已经建立从 LLM、Agent、Memory / Tool / Planner、Compute / Storage Separation、Stateless Agent 到 Context Engineering、Prompt Index 和 Context Routing 的基础架构主线。

1. 第 10 章将讨论 Token Reduction、Distillation、Small Model 和分层计算，重点拆开“减少 token 量”和“降低单 token 算力成本”这两条不同优化轴。

1. 第 11 章将把 Agent 当成生产系统来讨论，重点包括幂等、乐观锁、状态机、retry、降级、升级、可观测、审计、回放和对账。

1. 第 12 章将讨论 Multi-Agent、多租户和并发调度，把 Planner 与 Scheduler 的类比从单任务执行推进到资源竞争和任务编排。

1. 第 13 章将补上 Agent 安全模型，重点包括 Prompt Injection 作为 exploit、工具权限边界、Sandbox、最小权限和审计。

1. 第 14 章将回到 Agent Operating System，把 Memory、Tool、Planner、安全、调度和生产可靠性放回统一系统视角。
