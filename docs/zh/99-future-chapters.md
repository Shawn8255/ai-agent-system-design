# 后续修订方向

第一部分已经完成第 1-13 章的完整草稿。后续工作不再是继续追加章节，而是围绕公开发布、读者反馈和案例补强进行修订。

## 1. 引用与文献

后续需要为关键论点补充更完整的引用，尤其是 AIOS、MemGPT、Compound AI Systems、LLM OS、Prompt Injection、Sandbox、Agent 安全和多 Agent 调度相关资料。本文的定位应保持清晰：它不是重新发明这些概念，而是把它们放进分布式系统和生产可靠性的工程视角里。

## 2. 案例与例子

第 9 章已经补入一个端到端成本案例，把调用次数、单次 token 量和单 token 成本分别算清楚；后续可以再补不同任务分布下的对比数据。第 10 章已经补入“支付幂等 / 订单状态机”类比案例，用更具体的工程流程解释 Agent 工具调用为什么需要幂等、回放和对账。第 11-12 章可以补调度和安全事件的伪流程。

## 3. 公开发布素材

第 9 章关于“蒸馏不是直接减少 token”的内容适合拆成独立 X thread。核心表达可以围绕：

```text
总成本 ≈ 调用次数 × 单次 token 量 × 单 token 成本
```

这条公式可以作为公开传播的锚点：Context Engineering 主要减少 token 量，Planner 和缓存减少调用次数，Distillation 与 Routing 降低单 token 成本。

## 4. 双语一致性

后续每次修改中文正文时，都应该同步检查英文版本是否需要等价更新。术语表中的 LLM、Agent、Memory、Context、Tool、Planner、Context Routing、Distillation、Sandbox、Idempotency、Replay、Scheduler、Capability Boundary 和 Agent OS 应保持稳定。

## 5. 发行检查

正式公开前需要执行一次发行检查：Markdown 链接、DOCX/PDF 生成、图表显示、目录状态、README 说明、License 选择和贡献边界。书稿可以接受勘误、补例子和翻译改进，但主线结构应保持由作者维护。

## 6. Part II 进展与后续方向

Part II 已由第 14 章开篇，正式讨论了把 Memory、Skill 和 Routing 从"规则驱动"改为"学习驱动"的方向（Learned Memory、Learned Skill、Learned Routing），并借数据库"从查询优化器到 Learned Index"的先例说明其工程可行性与边界。

在此之后，Part II 还可以沿以下方向继续展开（尚未成章）：

- **学习型组件的评估体系**：如何为 Learned Memory / Skill / Routing 建立独立、可复现的评估集，避免用在线数据自评导致的指标虚高。
- **在线学习的稳定性**：分布漂移检测、策略回退机制、反馈延迟下的收敛与安全边界。
- **多 Agent 协作中的学习**：当多个 Agent 共享记忆与技能时，如何避免反馈回路互相放大偏差，以及技能在租户之间的隔离与复用。

写作时应保持本书一贯的克制：给出类比和边界，不承诺尚未验证的效果。这些方向的收益依赖稳定的任务分布、评估体系和足够样本。

> 说明：关于"多 Agent 冗余执行与交接"和"跨 Agent 端标准与可移植性"两个主题，已分别并入第 11 章（11.6）和第 13 章（13.6）正文。
