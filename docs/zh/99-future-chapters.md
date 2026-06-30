# 后续章节写作计划

第一部分完成了前三章的基础架构视角。后续章节将沿着这条主线继续展开：Memory 如何对应 Storage，Stateless Agent 如何对应无状态服务，Context Engineering 为什么像 Query Optimization，AGENTS.md 为什么像 Index，以及 Distillation 和 Small Model 为什么更适合放在 Tiered Compute 的框架下理解。

后续写作还需要补上三块更能体现工程差异化的内容。第一，Agent 安全不能只作为风险提示处理。OS 的安全模型会迁移到 Agent 系统里：prompt injection 更接近 exploit，工具调用需要权限边界，代码执行和外部系统访问需要 sandbox。第二，并发调度是 OS 类比最直接的一部分，多 Agent、多租户、多任务队列和资源隔离，比单任务 Planner 更接近 Scheduler。第三，Agent 应该被当成生产系统来讨论：它需要 SLA、幂等、乐观锁、状态机、retry、降级、升级、可观测、审计、回放和对账。这是本文区别于只讨论“能跑起来”的 OS-analogy 架构文章的重点。

1. 第 4 章将拆解 Memory、Tool、Planner 的边界。

1. 第 5-6 章将重点讨论 Compute / Storage Separation 与 Stateless。

1. 第 7-8 章将把 Context Engineering、AGENTS.md 与数据库优化建立联系。

1. 第 9-10 章将讨论 Retrieval、Token Reduction、Distillation、Small Model 和分层计算，重点拆开“减少 token 量”和“降低单 token 算力成本”这两条不同优化轴。

1. 第 11 章将把 Agent 当成生产系统来讨论，重点包括幂等、乐观锁、状态机、retry、降级、升级、可观测、审计、回放和对账。

1. 第 12 章将讨论 Multi-Agent、多租户和并发调度，把 Planner 与 Scheduler 的类比从单任务执行推进到资源竞争和任务编排。

1. 第 13 章将补上 Agent 安全模型，重点包括 prompt injection 作为 exploit、工具权限边界、sandbox、最小权限和审计。

1. 第 14 章将回到 Agent Operating System，把 Memory、Tool、Planner、安全、调度和生产可靠性放回统一系统视角。
